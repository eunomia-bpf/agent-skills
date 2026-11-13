#!/usr/bin/env python3
"""Deterministic worklist for the eunomia community patrol.

Walks every public, non-archived, non-fork repository of the organization
through the GitHub API (gh), and the pages of the eunomia.dev sitemap, and
lists what needs attention, item by item. Every category has a level:

WARN  the patrol works every item in this run: the operator's latest comments
      on closed issues and pull requests, failing default branches and
      pull request CI, conflicting pull requests and pull requests behind
      their base (rebase them), workflow runs waiting for approval or queued
      for hours, offline self-hosted runners, workflows GitHub disabled for
      inactivity, secret, code and dependency alerts, reported bugs with
      neither a fix pull request nor a `false positive` label, pull requests
      without a patrol review of their head, unresolved review threads on the
      patrol's own pull requests, ready pull requests in small independent
      repositories (the patrol merges them), authors silent for two weeks,
      issues, pull requests and Discussions whose last word is not a
      maintainer's, and broken site pages.
INFO  reported for maintainers: pull requests ready to merge elsewhere, bugs
      fixed on the default branch waiting to be closed, releases far behind
      the default branch, manually disabled workflows, unlabeled issues,
      first-time contributors, growth metrics, and the checks the token could
      not read.

A small independent repository has fewer than 240 stars and is no git
submodule of another repository in the organization; a ready pull request
there is listed for the patrol to merge once its review finds it normal.

The patrol posts from the operator's account and ends its own reviews and
comments with `*AI patrol review*`; the same account without that mark is the
operator, whose comments count as waiting for a patrol reply.

The script only reads, and it is a hint: the patrol works the items, finds
what the list misses, repairs the script when it is wrong, and runs it again
at the end of the run; the difference between the two outputs is the run's
result.

Usage: patrol_worklist.py [--org eunomia-bpf] [--patrol yunwei37]
                          [--site SITEMAP_URL | --no-site]
                          [--growth] [--previous earlier.json]
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
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

MAINTAINER = {"OWNER", "MEMBER", "COLLABORATOR"}
# The patrol posts from the operator's account; its own reviews and comments
# carry this marker (or the longer footer it used before 2026-11-13). The same
# account without a marker is the operator, whom the patrol answers.
PATROL_MARKS = ("ai patrol review",
                "ai-generated response; a maintainer will review and follow up later")
FIRST_TIMER = {"FIRST_TIME_CONTRIBUTOR", "FIRST_TIMER"}
RESOLVED_LABELS = {"false positive"}
FIXED_LABELS = {"fixed-on-master"}
BUG_LABEL = re.compile(r"bug|crash|regression|defect", re.I)
BUG_WORDS = re.compile(
    r"\b(bug|crash(es|ed)?|segfault|segmentation fault|panic|error|fail(s|ed|ure)?"
    r"|broken|does not work|doesn't work|not working|wrong|incorrect|leak)\b",
    re.I,
)
FAILING = {"FAILURE", "ERROR"}
QUEUED_STALE = dt.timedelta(hours=6)
RELEASE_STALE = dt.timedelta(days=90)
SELF_MERGE_STARS = 240
# gh failures worth another try: network drops and GitHub's rate pushback.
TRANSIENT = re.compile(r"timeout|TLS handshake|connection reset|EOF|HTTP 50[234]"
                       r"|error connecting|dial tcp|connectex|connection refused"
                       r"|no such host|secondary rate limit|submitted too quickly", re.I)
SUBMODULE_URL = re.compile(
    r"^\s*url\s*=\s*\S*github\.com[:/]+([^/\s]+)/([^/\s]+?)(?:\.git)?/?\s*$", re.M)
SITEMAP = "https://eunomia.dev/sitemap.xml"
USER_AGENT = "eunomia-community-patrol"

# Every category with its level, in the order the patrol works them.
CATEGORIES = [
    ("operator_comment_unanswered", "WARN"),
    ("default_branch_failing", "WARN"),
    ("pr_ci_failing", "WARN"),
    ("pr_conflicting", "WARN"),
    ("pr_behind_base", "WARN"),
    ("runs_action_required", "WARN"),
    ("runs_queued_stale", "WARN"),
    ("runners_offline", "WARN"),
    ("workflows_disabled_inactivity", "WARN"),
    ("secret_scanning_open", "WARN"),
    ("code_scanning_open", "WARN"),
    ("alerts_open", "WARN"),
    ("bug_unresolved", "WARN"),
    ("pr_needs_review", "WARN"),
    ("pr_threads_awaiting_patrol", "WARN"),
    ("pr_merge_small_repo", "WARN"),
    ("pr_author_silent_14d", "WARN"),
    ("pr_awaiting_reply", "WARN"),
    ("issue_awaiting_reply", "WARN"),
    ("discussion_unanswered", "WARN"),
    ("site_broken", "WARN"),
    ("pr_ready_for_maintainer", "INFO"),
    ("bug_fixed_awaiting_close", "INFO"),
    ("release_pending", "INFO"),
    ("workflows_disabled_manually", "INFO"),
    ("issue_unlabeled", "INFO"),
    ("pr_first_time_contributor", "INFO"),
]


def run_gh(args, allow_fail):
    for attempt in range(5):
        proc = subprocess.run(["gh"] + args, capture_output=True, text=True,
                              encoding="utf-8")
        if proc.returncode == 0:
            return proc.stdout
        if attempt < 4 and TRANSIENT.search(proc.stderr):
            time.sleep(2 ** (attempt + 1))
            continue
        if allow_fail:
            return None
        raise RuntimeError(f"gh {' '.join(args[:3])}: {proc.stderr.strip()[:300]}")


def gh(args, allow_fail=False):
    out = run_gh(args, allow_fail)
    if out is None:
        return None
    return json.loads(out) if out.strip() else None


def gh_lines(args, allow_fail=False):
    """For --paginate with --jq: one JSON value per line."""
    out = run_gh(args, allow_fail)
    if out is None:
        return None
    return [json.loads(line) for line in out.splitlines() if line.strip()]


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
        name isArchived hasDiscussionsEnabled stargazerCount forkCount
        watchers { totalCount }
        gitmodules: object(expression: "HEAD:.gitmodules") { ... on Blob { text } }
        latestRelease { tagName publishedAt url }
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
        author { login } authorAssociation
        baseRefName headRefOid isCrossRepository maintainerCanModify
        headRepository { nameWithOwner }
        reviews(last: 40) { nodes { author { login } state body commit { oid } } }
        reviewThreads(last: 30) { nodes { isResolved
          comments(last: 1) { nodes { author { login } body } } } }
        commits(last: 1) { nodes { commit {
          committedDate statusCheckRollup { state } } } }
        comments(last: 30) { nodes { author { login } authorAssociation createdAt } }
        lastComment: comments(last: 1) { nodes {
          author { login } authorAssociation body } }
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
        lastComment: comments(last: 1) { nodes {
          author { login } authorAssociation body } }
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
        comments(last: 20) { nodes { author { login } authorAssociation body } }
      }
    }
  }
}"""


CLOSED_COMMENTED = """
query($q: String!, $after: String) {
  search(query: $q, type: ISSUE, first: 50, after: $after) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on Issue { number title url repository { name }
        lastComment: comments(last: 1) { nodes { author { login } body createdAt } } }
      ... on PullRequest { number title url repository { name }
        lastComment: comments(last: 1) { nodes { author { login } body createdAt } } }
    }
  }
}"""
OPERATOR_WINDOW = dt.timedelta(days=14)
# Before this moment the patrol's comments carried no mark, so an unmarked
# comment from the shared account could be either; only later ones count.
MARK_SINCE = dt.datetime(2026, 11, 13, 7, 20, tzinfo=dt.timezone.utc)


def operator_comments_on_closed(org, patrol, now):
    """Closed issues and pull requests whose latest comment is the operator's
    (open ones already land in the awaiting-reply lists)."""
    since = (now - OPERATOR_WINDOW).date().isoformat()
    query = f"org:{org} commenter:{patrol} is:closed updated:>={since}"
    items, after = [], None
    while True:
        page = graphql(CLOSED_COMMENTED, q=query, after=after)["search"]
        for node in page["nodes"]:
            last = ((node.get("lastComment") or {}).get("nodes") or [None])[0]
            if (last and by_operator(last, patrol)
                    and parse_time(last["createdAt"]) >= MARK_SINCE):
                items.append({"repo": node["repository"]["name"], "number": node["number"],
                              "url": node["url"], "title": node["title"][:90],
                              "detail": "operator: " + " ".join(last["body"].split())[:120]})
        if not page["pageInfo"]["hasNextPage"]:
            return items
        after = page["pageInfo"]["endCursor"]


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


def login(node):
    return (node.get("author") or {}).get("login")


def by_patrol(node, patrol):
    """The patrol wrote it: the shared account and the patrol marker."""
    body = (node.get("body") or "").lower()
    return login(node) == patrol and any(mark in body for mark in PATROL_MARKS)


def by_operator(node, patrol):
    """The operator wrote it through the shared account, without the marker."""
    return login(node) == patrol and not by_patrol(node, patrol)


def needs_reply(author, last, patrol):
    """True when the latest comment waits for the patrol: the operator wrote
    it, or someone other than a maintainer did, or the item's own author did.
    The patrol never answers its own comment."""
    if not last or not last.get("author") or by_patrol(last, patrol):
        return False
    if by_operator(last, patrol):
        return True
    return last["authorAssociation"] not in MAINTAINER or login(last) == author


def compare(org, repo, base, head, field):
    """ahead_by or behind_by of head against base; None when unreadable."""
    path = (f"repos/{org}/{repo}/compare/{urllib.parse.quote(base, safe='/')}"
            f"...{urllib.parse.quote(head, safe='/')}?per_page=1")
    data = gh(["api", path, "--jq", f"{{n: .{field}}}"], allow_fail=True)
    return None if data is None else data["n"]


def merge_blocks(org, repos):
    """Why each repository's pull requests stay with a maintainer, or None
    for a small independent repository whose normal pull requests the patrol
    merges itself."""
    users = {}
    for r in repos:
        text = (r.get("gitmodules") or {}).get("text") or ""
        for owner, name in SUBMODULE_URL.findall(text):
            if owner.lower() == org.lower() and name.lower() != r["name"].lower():
                users.setdefault(name.lower(), []).append(r["name"])
    blocks = {}
    for r in repos:
        if r["stargazerCount"] >= SELF_MERGE_STARS:
            blocks[r["name"]] = f"{r['stargazerCount']} stars"
        elif r["name"].lower() in users:
            blocks[r["name"]] = "submodule of " + ", ".join(sorted(users[r["name"].lower()]))
        else:
            blocks[r["name"]] = None
    return blocks


def scan_repo(org, repo, patrol, now, merge_block, growth):
    """Everything about one repository except the per-PR base comparisons,
    which come back as `pending` for the second, parallel phase."""
    name = repo["name"]
    out = {key: [] for key, _ in CATEGORIES}
    unavailable, pending, traffic = set(), [], None
    ref = repo.get("defaultBranchRef") or {}
    target = ref.get("target") or {}
    rollup = (target.get("statusCheckRollup") or {}).get("state")
    if rollup in FAILING:
        sha = (target.get("oid") or "")[:8]
        out["default_branch_failing"].append(
            {"repo": name, "branch": ref.get("name"), "sha": sha, "state": rollup,
             "title": f"{ref.get('name')} {sha}", "detail": rollup,
             "url": f"https://github.com/{org}/{name}/commits/{ref.get('name')}"})

    for pr in paged(PULLS, "pullRequests", org=org, repo=name):
        author = login(pr)
        item = {"repo": name, "number": pr["number"], "url": pr["url"],
                "title": pr["title"][:90], "author": author, "draft": pr["isDraft"],
                "head": pr["headRefOid"][:8]}
        reviewed = any(by_patrol(r, patrol)
                       and (r.get("commit") or {}).get("oid") == pr["headRefOid"]
                       for r in pr["reviews"]["nodes"])
        if not reviewed:
            out["pr_needs_review"].append(item)
        if pr["mergeable"] == "CONFLICTING":
            out["pr_conflicting"].append(item)
        if pr.get("authorAssociation") in FIRST_TIMER:
            out["pr_first_time_contributor"].append(item)
        commit = (pr["commits"]["nodes"] or [{}])[0].get("commit") or {}
        state = (commit.get("statusCheckRollup") or {}).get("state")
        if state in FAILING:
            out["pr_ci_failing"].append(item)
        author_times = [parse_time(c["createdAt"]) for c in pr["comments"]["nodes"]
                        if login(c) == author]
        author_times.append(parse_time(pr["createdAt"]))
        if commit.get("committedDate"):
            author_times.append(parse_time(commit["committedDate"]))
        if author != patrol and now - max(author_times) > dt.timedelta(days=14):
            out["pr_author_silent_14d"].append(
                dict(item, silent_days=(now - max(author_times)).days))
        if needs_reply(author, (pr["lastComment"]["nodes"] or [None])[0], patrol):
            out["pr_awaiting_reply"].append(item)
        open_threads = [t for t in pr["reviewThreads"]["nodes"] if not t["isResolved"]]
        # On the shared account's pull requests every thread is the patrol's
        # to close; elsewhere the threads the operator answered last.
        lasts = [(t["comments"]["nodes"] or [{}])[-1] for t in open_threads]
        waiting = [c for c in lasts
                   if (author == patrol and not by_patrol(c, patrol))
                   or by_operator(c, patrol)]
        if waiting:
            out["pr_threads_awaiting_patrol"].append(
                dict(item, detail=f"{len(waiting)} unresolved threads"))
        pending.append({
            "item": item, "base": pr["baseRefName"], "headsha": pr["headRefOid"],
            "conflicting": pr["mergeable"] == "CONFLICTING",
            "writable": not pr["isCrossRepository"] or pr["maintainerCanModify"],
            "merge_block": merge_block,
            "ready": (not pr["isDraft"] and pr["mergeable"] == "MERGEABLE"
                      and state == "SUCCESS" and reviewed and not open_threads)})

    for issue in paged(ISSUES, "issues", org=org, repo=name):
        labels = {l["name"].lower() for l in issue["labels"]["nodes"]}
        author = login(issue)
        item = {"repo": name, "number": issue["number"], "url": issue["url"],
                "title": issue["title"][:90], "author": author,
                "labels": sorted(labels)}
        bug_like = any(BUG_LABEL.search(l) for l in labels) or BUG_WORDS.search(issue["title"])
        linked = issue["closedByPullRequestsReferences"]["nodes"]
        if bug_like and not linked and not (labels & RESOLVED_LABELS):
            key = "bug_fixed_awaiting_close" if labels & FIXED_LABELS else "bug_unresolved"
            out[key].append(item)
        if not labels:
            out["issue_unlabeled"].append(item)
        last = (issue["lastComment"]["nodes"] or [None])[0]
        if (needs_reply(author, last, patrol) if last
                else issue["authorAssociation"] not in MAINTAINER):
            out["issue_awaiting_reply"].append(item)

    if repo.get("hasDiscussionsEnabled"):
        for d in paged(DISCUSSIONS, "discussions", org=org, repo=name):
            comments = d["comments"]["nodes"]
            answered = d["isAnswered"] if d["category"]["isAnswerable"] else False
            maintainer_spoke = any(c["authorAssociation"] in MAINTAINER
                                   or login(c) == patrol for c in comments)
            operator_last = bool(comments) and by_operator(comments[-1], patrol)
            if operator_last or (not answered and not maintainer_spoke):
                out["discussion_unanswered"].append(
                    {"repo": name, "number": d["number"], "url": d["url"],
                     "title": d["title"][:90]})

    runs = gh(["api", f"repos/{org}/{name}/actions/runs?status=action_required&per_page=50"],
              allow_fail=True)
    if runs is None:
        unavailable.add("action_required_runs")
    for run in (runs or {}).get("workflow_runs", []):
        prs = [p["number"] for p in run.get("pull_requests", [])]
        out["runs_action_required"].append(
            {"repo": name, "run": run["id"], "workflow": run["name"],
             "head": run["head_sha"][:8], "pull_requests": prs, "url": run["html_url"],
             "title": run["name"], "detail": f"head {run['head_sha'][:8]} PRs {prs}"})

    queued = gh_lines(["api", "--paginate",
                       f"repos/{org}/{name}/actions/runs?status=queued&per_page=100",
                       "--jq", ".workflow_runs[] | {name, created_at, html_url}"],
                      allow_fail=True)
    if queued is None:
        unavailable.add("queued_runs")
    stale = {}
    for run in queued or []:
        age = now - parse_time(run["created_at"])
        if age > QUEUED_STALE:
            stale.setdefault(run["name"], []).append((age, run["html_url"]))
    for workflow, ages in sorted(stale.items()):
        oldest = max(ages)
        out["runs_queued_stale"].append(
            {"repo": name, "title": workflow, "url": oldest[1],
             "detail": f"{len(ages)} runs queued over 6 h, oldest "
                       f"{int(oldest[0].total_seconds() // 3600)} h"})

    workflows = gh(["api", f"repos/{org}/{name}/actions/workflows?per_page=100"],
                   allow_fail=True)
    if workflows is None:
        unavailable.add("workflows")
    for w in (workflows or {}).get("workflows", []):
        key = {"disabled_inactivity": "workflows_disabled_inactivity",
               "disabled_manually": "workflows_disabled_manually"}.get(w["state"])
        if key:
            out[key].append({"repo": name, "title": w["name"], "detail": w["path"],
                             "url": w["html_url"]})

    runners = gh(["api", f"repos/{org}/{name}/actions/runners?per_page=100"],
                 allow_fail=True)
    if runners is None:
        unavailable.add("repository_runners")
    for r in (runners or {}).get("runners", []):
        if r["status"] != "online":
            out["runners_offline"].append(
                {"repo": name, "title": r["name"],
                 "detail": "offline, labels " + ",".join(l["name"] for l in r["labels"]),
                 "url": f"https://github.com/{org}/{name}/settings/actions/runners"})

    secrets = gh(["api", f"repos/{org}/{name}/secret-scanning/alerts?state=open&per_page=100"],
                 allow_fail=True)
    if secrets is None:
        unavailable.add("secret_scanning")
    for s in secrets or []:
        out["secret_scanning_open"].append(
            {"repo": name, "number": s["number"], "url": s["html_url"],
             "title": s.get("secret_type_display_name") or s.get("secret_type", "")})

    code = gh(["api", f"repos/{org}/{name}/code-scanning/alerts?state=open&per_page=100"],
              allow_fail=True)
    if code is None:
        unavailable.add("code_scanning")
    for a in code or []:
        rule = a.get("rule") or {}
        location = ((a.get("most_recent_instance") or {}).get("location") or {}).get("path", "")
        out["code_scanning_open"].append(
            {"repo": name, "number": a["number"], "url": a["html_url"],
             "title": (rule.get("description") or rule.get("id") or "")[:90],
             "detail": f"{rule.get('security_severity_level') or rule.get('severity')} {location}"})

    alerts = gh(["api", f"repos/{org}/{name}/dependabot/alerts?state=open&per_page=100"],
                allow_fail=True)
    if alerts is None:
        unavailable.add("dependency_alerts")
    for a in alerts or []:
        out["alerts_open"].append(
            {"repo": name, "number": a["number"], "url": a["html_url"],
             "severity": a["security_advisory"]["severity"],
             "package": a["dependency"]["package"]["name"],
             "manifest": a["dependency"]["manifest_path"],
             "title": a["dependency"]["package"]["name"],
             "detail": f"{a['security_advisory']['severity']} {a['dependency']['manifest_path']}"})

    release = repo.get("latestRelease")
    if release and release.get("publishedAt") and ref.get("name"):
        age = now - parse_time(release["publishedAt"])
        if age > RELEASE_STALE:
            ahead = compare(org, name, release["tagName"], ref["name"], "ahead_by")
            if ahead is None:
                unavailable.add("release_compare")
            elif ahead > 0:
                out["release_pending"].append(
                    {"repo": name, "title": release["tagName"], "url": release["url"],
                     "detail": f"{age.days} days old, {ahead} commits since"})

    if growth:
        views = gh(["api", f"repos/{org}/{name}/traffic/views"], allow_fail=True)
        if views is None:
            unavailable.add("traffic")
        else:
            traffic = {"views_14d": views["count"], "uniques_14d": views["uniques"]}
    return name, out, unavailable, pending, traffic


def fetch(url, method="GET", attempts=4):
    """(status, body) after redirects; retries rate limits and server errors."""
    status = None
    for attempt in range(attempts):
        req = urllib.request.Request(url, method=method,
                                     headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.status, resp.read() if method == "GET" else b""
        except urllib.error.HTTPError as exc:
            status = exc.code
            if status == 405 and method == "HEAD":
                return fetch(url, "GET", attempts)
            if status not in (429, 500, 502, 503, 504):
                return status, b""
        except (urllib.error.URLError, OSError) as exc:
            status = type(exc).__name__
        time.sleep(2 ** attempt)
    return status, b""


def sitemap_urls(sitemap):
    status, body = fetch(sitemap)
    if status != 200:
        raise RuntimeError(f"{sitemap}: {status}")
    root = ET.fromstring(body)
    locs = [e.text.strip() for e in root.iter() if e.tag.endswith("loc") and e.text]
    if root.tag.endswith("sitemapindex"):
        return [u for child in locs for u in sitemap_urls(child)]
    return locs


def check_site(sitemap):
    """(broken page items, number of pages checked)."""
    host = urllib.parse.urlsplit(sitemap).netloc
    try:
        urls = sitemap_urls(sitemap)
    except Exception as exc:  # the sitemap itself is the broken page
        return [{"repo": host, "title": "sitemap", "detail": str(exc)[:200],
                 "url": sitemap}], 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        statuses = list(pool.map(lambda u: fetch(u, "HEAD")[0], urls))
    broken = [(u, s) for u, s in zip(urls, statuses)
              if not (isinstance(s, int) and 200 <= s < 400)]
    if len(broken) > len(urls) // 2:
        codes = ", ".join(sorted({str(s) for _, s in broken}))
        return [{"repo": host, "title": "site check", "url": sitemap,
                 "detail": f"{len(broken)} of {len(urls)} pages failed ({codes}); "
                           "the checker itself may be blocked"}], len(urls)
    return [{"repo": host, "title": urllib.parse.urlsplit(u).path, "detail": str(s),
             "url": u} for u, s in broken], len(urls)


def growth_report(repos, traffic, previous):
    """Stars, forks, watchers and 14-day views per repository, with the
    change since an earlier worklist when one is given."""
    before = (previous or {}).get("growth", {}).get("repositories", {})
    rows = {}
    for r in repos:
        row = {"stars": r["stargazerCount"], "forks": r["forkCount"],
               "watchers": r["watchers"]["totalCount"], **(traffic.get(r["name"]) or {})}
        old = before.get(r["name"])
        if old:
            row["stars_delta"] = row["stars"] - old.get("stars", row["stars"])
            row["forks_delta"] = row["forks"] - old.get("forks", row["forks"])
        rows[r["name"]] = row
    totals = {k: sum(row.get(k, 0) for row in rows.values())
              for k in ("stars", "forks", "views_14d", "uniques_14d")}
    if before:
        totals["stars_delta"] = sum(row.get("stars_delta", 0) for row in rows.values())
        totals["forks_delta"] = sum(row.get("forks_delta", 0) for row in rows.values())
    return {"since": (previous or {}).get("generated"), "totals": totals,
            "repositories": rows}


def describe(item):
    ref = item["repo"] + (f"#{item['number']}" if "number" in item else "")
    parts = [ref, item.get("title", ""), item.get("detail", ""), item["url"]]
    return " ".join(p for p in parts if p)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--org", default="eunomia-bpf")
    ap.add_argument("--patrol", default="yunwei37")
    ap.add_argument("--site", default=SITEMAP, help="sitemap whose pages are checked")
    ap.add_argument("--no-site", action="store_true", help="skip the site check")
    ap.add_argument("--growth", action="store_true",
                    help="also read 14-day traffic of every repository")
    ap.add_argument("--previous", help="an earlier --json output, for growth changes")
    ap.add_argument("--json", help="write the full worklist here")
    ap.add_argument("--markdown", action="store_true", help="print every item")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    now = dt.datetime.now(dt.timezone.utc)
    started = time.monotonic()
    previous = None
    if args.previous and os.path.exists(args.previous):
        with open(args.previous, encoding="utf-8") as fh:
            previous = json.load(fh)

    repos, after = [], None
    while True:
        page = graphql(REPOS, org=args.org, after=after)["organization"]["repositories"]
        repos += [r for r in page["nodes"] if not r["isArchived"]]
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
    blocks = merge_blocks(args.org, repos)

    workers = min(32, (os.cpu_count() or 4) * 4)
    site_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    site_future = None if args.no_site else site_pool.submit(check_site, args.site)

    results, errors, unavailable, pending, traffic = {}, {}, {}, [], {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(scan_repo, args.org, r, args.patrol, now,
                               blocks[r["name"]], args.growth): r["name"]
                   for r in repos}
        for fut in concurrent.futures.as_completed(futures):
            try:
                name, out, missing, prs, views = fut.result()
            except Exception as exc:  # report, never hide, a repository that failed
                errors[futures[fut]] = str(exc)
                continue
            results[name] = out
            traffic[name] = views
            for check in missing:
                unavailable.setdefault(check, []).append(name)
            pending += [dict(p, repo=name) for p in prs]

        # Second phase: how far every open pull request is behind its base.
        behind = list(pool.map(
            lambda p: compare(args.org, p["repo"], p["base"], p["headsha"], "behind_by"),
            pending))
    for p, count in zip(pending, behind):
        out = results[p["repo"]]
        if count is None:
            if p["repo"] not in unavailable.setdefault("pull_request_compare", []):
                unavailable["pull_request_compare"].append(p["repo"])
            continue
        if count > 0 and not p["conflicting"]:
            out["pr_behind_base"].append(dict(
                p["item"], behind_by=count, writable=p["writable"],
                detail=f"{count} commits behind {p['base']}"
                       + ("" if p["writable"] else ", branch not writable")))
        if count == 0 and p["ready"]:
            if p["merge_block"] is None:
                out["pr_merge_small_repo"].append(p["item"])
            else:
                out["pr_ready_for_maintainer"].append(
                    dict(p["item"], detail=p["merge_block"]))

    totals = {key: [] for key, _ in CATEGORIES}
    for out in results.values():
        for key, value in out.items():
            totals[key].extend(value)
    try:
        totals["operator_comment_unanswered"] = operator_comments_on_closed(
            args.org, args.patrol, now)
    except Exception as exc:  # report, never hide, a failed search
        errors["operator_comment_search"] = str(exc)
    org_runners = gh(["api", f"orgs/{args.org}/actions/runners?per_page=100"],
                     allow_fail=True)
    if org_runners is None:
        unavailable["organization_runners"] = [args.org]
    for r in (org_runners or {}).get("runners", []):
        if r["status"] != "online":
            totals["runners_offline"].append(
                {"repo": args.org, "title": r["name"],
                 "detail": "organization runner offline, labels "
                           + ",".join(l["name"] for l in r["labels"]),
                 "url": f"https://github.com/organizations/{args.org}/settings/actions/runners"})
    pages = 0
    if site_future:
        totals["site_broken"], pages = site_future.result()
    site_pool.shutdown()

    levels = dict(CATEGORIES)
    growth = growth_report(repos, traffic, previous)
    worklist = {"generated": now.isoformat(timespec="seconds"), "org": args.org,
                "repositories": len(repos), "site_pages": pages,
                "scan_errors": errors, "levels": levels,
                "self_merge_repositories": sorted(n for n, b in blocks.items() if b is None),
                "unavailable": {k: sorted(v) for k, v in sorted(unavailable.items())},
                "growth": growth,
                **{k: sorted(v, key=lambda i: (i["repo"], i.get("number", 0),
                                               i.get("title", "")))
                   for k, v in totals.items()}}
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(worklist, fh, indent=1, ensure_ascii=False)

    print(f"# Patrol worklist {worklist['generated']} ({len(repos)} repositories, "
          f"{pages} site pages, {time.monotonic() - started:.0f} s)")
    for key, level in CATEGORIES:
        print(f"{level} {key}: {len(worklist[key])}")
    warn = sum(len(worklist[k]) for k, level in CATEGORIES if level == "WARN")
    info = sum(len(worklist[k]) for k, level in CATEGORIES if level == "INFO")
    print(f"warn_total: {warn} info_total: {info}")
    print(f"INFO self_merge_repositories: {len(worklist['self_merge_repositories'])} "
          f"(under {SELF_MERGE_STARS} stars, no submodule of another repository)")
    t = growth["totals"]
    since = f" since {growth['since']}" if growth["since"] else ""
    change = (f" ({t['stars_delta']:+d} stars, {t['forks_delta']:+d} forks{since})"
              if "stars_delta" in t else "")
    views = f", 14-day views {t['views_14d']} by {t['uniques_14d']}" if args.growth else ""
    print(f"INFO growth: {t['stars']} stars, {t['forks']} forks{views}{change}")
    for check, names in worklist["unavailable"].items():
        print(f"INFO unavailable {check}: {len(names)} repositories")
    if errors:
        print(f"scan_errors: {len(errors)} {sorted(errors)}")
    if args.markdown:
        for key, level in CATEGORIES:
            if worklist[key]:
                print(f"\n## {level} {key}")
                for item in worklist[key]:
                    print(f"- {level} {describe(item)}")
        rows = sorted(growth["repositories"].items(),
                      key=lambda kv: (-kv[1].get("stars_delta", 0),
                                      -kv[1].get("views_14d", 0), -kv[1]["stars"]))
        print("\n## INFO growth (top 20)")
        for name, row in rows[:20]:
            print(f"- INFO {name} stars {row['stars']}"
                  + (f" ({row['stars_delta']:+d})" if "stars_delta" in row else "")
                  + f" forks {row['forks']}"
                  + (f" views_14d {row['views_14d']}" if "views_14d" in row else ""))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
