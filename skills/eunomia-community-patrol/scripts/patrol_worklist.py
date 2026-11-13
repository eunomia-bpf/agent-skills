#!/usr/bin/env python3
"""Deterministic worklist for the eunomia community patrol.

Walks every public, non-archived, non-fork repository of the organization
through the GitHub API (gh) and lists what needs the patrol, item by item:
pull requests without a patrol review of their current head, conflicting or
failing pull requests, pull requests whose author has been silent for two
weeks, waiting workflow runs, reported bugs with neither a fix pull request nor
a `false positive` label, issues and Discussions whose last word is not a
maintainer's, failing default branches and open dependency alerts.

The script only reads. The patrol works the items and runs it again at the end
of the run; the difference between the two outputs is the run's result.

Usage: patrol_worklist.py [--org eunomia-bpf] [--patrol yunwei37]
                          [--json out.json] [--markdown]
"""
import argparse
import concurrent.futures
import datetime as dt
import json
import os
import re
import subprocess
import sys

MAINTAINER = {"OWNER", "MEMBER", "COLLABORATOR"}
RESOLVED_LABELS = {"false positive"}
FIXED_LABELS = {"fixed-on-master"}
BUG_LABEL = re.compile(r"bug|crash|regression|defect", re.I)
BUG_WORDS = re.compile(
    r"\b(bug|crash(es|ed)?|segfault|segmentation fault|panic|error|fail(s|ed|ure)?"
    r"|broken|does not work|doesn't work|not working|wrong|incorrect|leak)\b",
    re.I,
)
FAILING = {"FAILURE", "ERROR"}


def gh(args, allow_fail=False):
    proc = subprocess.run(["gh"] + args, capture_output=True, text=True,
                          encoding="utf-8")
    if proc.returncode != 0:
        if allow_fail:
            return None
        raise RuntimeError(f"gh {' '.join(args[:3])}: {proc.stderr.strip()[:300]}")
    return json.loads(proc.stdout) if proc.stdout.strip() else None


def graphql(query, **variables):
    args = ["api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is None:
            continue
        flag = "-F" if isinstance(value, (int, bool)) else "-f"
        args += [flag, f"{key}={value}"]
    data = gh(args)
    return data["data"]


REPOS = """
query($org: String!, $after: String) {
  organization(login: $org) {
    repositories(first: 100, after: $after, privacy: PUBLIC, isFork: false) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name isArchived hasDiscussionsEnabled stargazerCount
        defaultBranchRef { name target { ... on Commit {
          oid committedDate statusCheckRollup { state } } } }
      }
    }
  }
}"""

PULLS = """
query($org: String!, $repo: String!, $after: String) {
  repository(owner: $org, name: $repo) {
    pullRequests(states: OPEN, first: 30, after: $after) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title url isDraft mergeable createdAt updatedAt
        author { login }
        headRefOid
        headRepository { nameWithOwner }
        reviews(last: 40) { nodes { author { login } state commit { oid } } }
        commits(last: 1) { nodes { commit {
          committedDate statusCheckRollup { state } } } }
        comments(last: 30) { nodes { author { login } authorAssociation createdAt } }
      }
    }
  }
}"""

ISSUES = """
query($org: String!, $repo: String!, $after: String) {
  repository(owner: $org, name: $repo) {
    issues(states: OPEN, first: 50, after: $after) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title url createdAt updatedAt
        author { login } authorAssociation
        labels(first: 20) { nodes { name } }
        closedByPullRequestsReferences(first: 5, includeClosedPrs: true) {
          nodes { number state }
        }
        comments(last: 30) { nodes { author { login } authorAssociation createdAt } }
      }
    }
  }
}"""

DISCUSSIONS = """
query($org: String!, $repo: String!, $after: String) {
  repository(owner: $org, name: $repo) {
    discussions(first: 50, after: $after, states: OPEN) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title url createdAt isAnswered
        category { isAnswerable }
        author { login }
        comments(last: 20) { nodes { author { login } authorAssociation } }
      }
    }
  }
}"""


def paged(query, key, **variables):
    items, after = [], None
    while True:
        data = graphql(query, after=after, **variables)
        node = data["repository"][key]
        items += node["nodes"]
        if not node["pageInfo"]["hasNextPage"]:
            return items
        after = node["pageInfo"]["endCursor"]


def parse_time(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def last_word_is_maintainer(author, comments, patrol):
    """True when the latest comment is from a maintainer or the patrol."""
    nodes = [c for c in comments if c.get("author")]
    if not nodes:
        return False
    last = nodes[-1]
    return (last["authorAssociation"] in MAINTAINER
            or last["author"]["login"] == patrol) and last["author"]["login"] != author


def scan_repo(org, repo, patrol, now):
    name = repo["name"]
    out = {k: [] for k in (
        "pr_needs_review", "pr_conflicting", "pr_ci_failing", "pr_author_silent_14d",
        "pr_awaiting_reply", "runs_action_required", "bug_unresolved",
        "bug_fixed_awaiting_close", "issue_awaiting_reply", "discussion_unanswered",
        "alerts_open")}
    ref = repo.get("defaultBranchRef") or {}
    target = ref.get("target") or {}
    rollup = (target.get("statusCheckRollup") or {}).get("state")
    out["default_branch"] = {"branch": ref.get("name"), "sha": (target.get("oid") or "")[:8],
                             "state": rollup}

    for pr in paged(PULLS, "pullRequests", org=org, repo=name):
        author = (pr.get("author") or {}).get("login")
        item = {"repo": name, "number": pr["number"], "url": pr["url"],
                "title": pr["title"][:90], "author": author, "draft": pr["isDraft"],
                "head": pr["headRefOid"][:8]}
        reviewed = any((r.get("author") or {}).get("login") == patrol
                       and (r.get("commit") or {}).get("oid") == pr["headRefOid"]
                       for r in pr["reviews"]["nodes"])
        if not reviewed:
            out["pr_needs_review"].append(item)
        if pr["mergeable"] == "CONFLICTING":
            out["pr_conflicting"].append(item)
        commit = (pr["commits"]["nodes"] or [{}])[0].get("commit") or {}
        if ((commit.get("statusCheckRollup") or {}).get("state")) in FAILING:
            out["pr_ci_failing"].append(item)
        author_times = [parse_time(c["createdAt"]) for c in pr["comments"]["nodes"]
                        if (c.get("author") or {}).get("login") == author]
        author_times.append(parse_time(pr["createdAt"]))
        if commit.get("committedDate"):
            author_times.append(parse_time(commit["committedDate"]))
        if author != patrol and now - max(author_times) > dt.timedelta(days=14):
            out["pr_author_silent_14d"].append(
                dict(item, silent_days=(now - max(author_times)).days))
        comments = pr["comments"]["nodes"]
        if comments and not last_word_is_maintainer(author, comments, patrol) \
                and (comments[-1].get("author") or {}).get("login") != patrol:
            out["pr_awaiting_reply"].append(item)

    for issue in paged(ISSUES, "issues", org=org, repo=name):
        labels = {l["name"].lower() for l in issue["labels"]["nodes"]}
        author = (issue.get("author") or {}).get("login")
        item = {"repo": name, "number": issue["number"], "url": issue["url"],
                "title": issue["title"][:90], "author": author,
                "labels": sorted(labels)}
        bug_like = any(BUG_LABEL.search(l) for l in labels) or BUG_WORDS.search(issue["title"])
        linked = issue["closedByPullRequestsReferences"]["nodes"]
        if bug_like and not linked and not (labels & RESOLVED_LABELS):
            key = "bug_fixed_awaiting_close" if labels & FIXED_LABELS else "bug_unresolved"
            out[key].append(item)
        comments = issue["comments"]["nodes"]
        if not last_word_is_maintainer(author, comments, patrol) \
                and not (comments and (comments[-1].get("author") or {}).get("login") == patrol):
            if issue["authorAssociation"] not in MAINTAINER or comments:
                out["issue_awaiting_reply"].append(item)

    if repo.get("hasDiscussionsEnabled"):
        for d in paged(DISCUSSIONS, "discussions", org=org, repo=name):
            comments = d["comments"]["nodes"]
            answered = d["isAnswered"] if d["category"]["isAnswerable"] else False
            maintainer_spoke = any(c["authorAssociation"] in MAINTAINER
                                   or (c.get("author") or {}).get("login") == patrol
                                   for c in comments)
            if not answered and not maintainer_spoke:
                out["discussion_unanswered"].append(
                    {"repo": name, "number": d["number"], "url": d["url"],
                     "title": d["title"][:90]})

    runs = gh(["api", f"repos/{org}/{name}/actions/runs?status=action_required&per_page=50"],
              allow_fail=True) or {}
    for run in runs.get("workflow_runs", []):
        prs = [p["number"] for p in run.get("pull_requests", [])]
        out["runs_action_required"].append(
            {"repo": name, "run": run["id"], "workflow": run["name"],
             "head": run["head_sha"][:8], "pull_requests": prs, "url": run["html_url"]})

    alerts = gh(["api", f"repos/{org}/{name}/dependabot/alerts?state=open&per_page=100"],
                allow_fail=True)
    if alerts is None:
        out["alerts_unavailable"] = True
    else:
        for a in alerts:
            out["alerts_open"].append(
                {"repo": name, "number": a["number"], "url": a["html_url"],
                 "severity": a["security_advisory"]["severity"],
                 "package": a["dependency"]["package"]["name"],
                 "manifest": a["dependency"]["manifest_path"]})
    return name, out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--org", default="eunomia-bpf")
    ap.add_argument("--patrol", default="yunwei37")
    ap.add_argument("--json", help="write the full worklist here")
    ap.add_argument("--markdown", action="store_true", help="print every item")
    args = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc)

    repos, after = [], None
    while True:
        page = graphql(REPOS, org=args.org, after=after)["organization"]["repositories"]
        repos += [r for r in page["nodes"] if not r["isArchived"]]
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]

    results, errors = {}, {}
    workers = min(32, (os.cpu_count() or 4) * 4)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(scan_repo, args.org, r, args.patrol, now): r["name"]
                   for r in repos}
        for fut in concurrent.futures.as_completed(futures):
            try:
                name, out = fut.result()
                results[name] = out
            except Exception as exc:  # report, never hide, a repository that failed
                errors[futures[fut]] = str(exc)

    totals = {}
    for out in results.values():
        for key, value in out.items():
            if isinstance(value, list):
                totals.setdefault(key, []).extend(value)
    red = [{"repo": n, **o["default_branch"]} for n, o in sorted(results.items())
           if o["default_branch"]["state"] in FAILING]
    worklist = {"generated": now.isoformat(timespec="seconds"), "org": args.org,
                "repositories": len(repos), "scan_errors": errors,
                "alerts_unavailable": sorted(n for n, o in results.items()
                                             if o.get("alerts_unavailable")),
                "default_branch_failing": red,
                **{k: sorted(v, key=lambda i: (i["repo"], i.get("number", 0)))
                   for k, v in totals.items()}}
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(worklist, fh, indent=1, ensure_ascii=False)

    print(f"# Patrol worklist {worklist['generated']} ({len(repos)} repositories)")
    order = ["pr_needs_review", "pr_ci_failing", "pr_conflicting", "pr_author_silent_14d",
             "pr_awaiting_reply", "runs_action_required", "bug_unresolved",
             "bug_fixed_awaiting_close", "issue_awaiting_reply", "discussion_unanswered",
             "alerts_open"]
    print(f"default_branch_failing: {len(red)}")
    for key in order:
        print(f"{key}: {len(worklist.get(key, []))}")
    if errors:
        print(f"scan_errors: {len(errors)} {sorted(errors)}")
    if args.markdown:
        print("\n## default_branch_failing")
        for r in red:
            print(f"- {r['repo']} {r['branch']} {r['sha']} {r['state']}")
        for key in order:
            print(f"\n## {key}")
            for i in worklist.get(key, []):
                print(f"- {i['repo']}#{i.get('number', i.get('run'))} {i.get('title', i.get('workflow', ''))} {i['url']}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
