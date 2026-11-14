---
name: eunomia-community-patrol
description: Inspect, triage, and actively maintain all open GitHub issues and pull requests across public, non-archived, non-fork eunomia-bpf repositories. Use for recurring Eunomia community patrols, organization-wide issue and PR sweeps, follow-up of prior maintenance comments or pull requests, and scheduled maintenance that may comment, fix verified bugs, push, open pull requests, rebase and proactively repair contributor pull requests through review and CI readiness, and merge normal pull requests in small independent repositories, while leaving every other merge and every destructive or privileged action to a maintainer.
---

# Eunomia Community Patrol

Treat this skill as the versioned source of truth for the Eunomia community
maintenance task. Keep runtime state, credentials, private logs, and
deduplication records outside the repository.

## Meta Rule: Everything Automatic Except Destructive, Privileged or Merging

Operator, 2026-11-13, verbatim:

> “说说全部的. meta 的规则就是除了破坏性的, 特权的, 或者需要合并的都可以做对吧, 要全自动维护? 300 star 以下, 比较正常的 pr, 没有被别的 repo 引用的独立项目也都可以自行处置非特权是不是? 这个也要写在开头? 没说的这部分如果有的话也可以去看看去留意一下? 包括增长 metrics 也可以留意?”

> “删库之类的本身就被保护起来需要二次验证了对吧? 240 star 以下吧”

> “我自己写的 pr 我自己也要负责 review 吧, 并且确保. 且“敏感文件”判断过宽，把 docs/security_model.md 误判为安全策略文件 这个不要搞? 干嘛要敏感文件?”

> “巡检 rview 需要标记来自巡检 rveiew (两三个词), 这样我自己的别的 comment 回答你也要去看和回复, 但是不要回复自己”

> “脚本只作为提示. 脚本出问题之后巡检 agent 可自己做必要的修复或者改进, 但是不改 skills 文本.”

> “其他 agent 也用你的账号发言却不带标记，巡检会把它们当作你的话来回复 没错, 就要回复”

> “不带标记都回复”

> “巡检也是吧? 确认的问题直接修，拿不准的就发评论讨论”

This rule comes first; every other passage of this skill applies it.

- Maintain the community fully automatically. Every action that is neither
  destructive, privileged nor a merge happens without asking: reviews,
  comments, labels, fixes, pull requests, CI approval and repair, rebases of
  pull request branches, dependency upgrades, answers in Discussions, tracking
  issues.
- Destructive: deleting or archiving a repository, branch, tag, release,
  package, issue, comment or workflow log; closing another author's issue or
  pull request; force-pushing or rewriting a default or release branch or a
  tag. The patrol's token cannot delete a repository (it carries no
  `delete_repo` scope, and GitHub's web page asks for re-authentication), but
  its `repo` scope reaches everything else on this list, so this rule is the
  guard.
- Privileged: repository and organization settings, permissions, branch
  protection, secrets, webhooks, runners, environments, Actions settings,
  deployment configuration, an administrator's bypass of branch protection,
  an approving review, and publishing a release, tag or package.
- Merging stays with a maintainer, with one exception the patrol carries out
  itself: in a small independent repository (fewer than 240 stars, and no
  other repository depends on it) the patrol merges a normal pull request,
  under the conditions in **Merging** below.
- Pull requests from `yunwei37` (the operator's account, which the patrol
  posts as) are the patrol's own responsibility: it reviews them as strictly
  as anyone's, builds and tests them, fixes what it finds, and makes sure
  they work before they merge.
- Every review, review reply and comment the patrol posts ends with the
  standalone line `*AI patrol review*`. A comment from `yunwei37` without that
  mark is the operator's own: read every one and answer what it asks or tells.
  Other agents that post from the account without the mark are answered the
  same way.
  Never reply to a comment that carries the mark (or the longer footer used
  before 2026-11-13); that is the patrol's own.
- The worklist script is a hint, never the authority on what needs doing. When
  it fails, misses or misreports something, the patrol fixes or improves the
  script itself: commit to `skills/eunomia-community-patrol/scripts/` in
  `eunomia-bpf/agent-skills` and move the eunomia.dev pointer. It never edits
  the text of this skill.
- Fix what is confirmed, discuss what is not. A problem the patrol confirms
  (reproduced, or unambiguous from the code), in a pull request or anywhere
  else, is fixed in the same run: a focused forward-only commit with a test on
  the pull request branch when writable, otherwise a follow-up pull request;
  a confirmed missing split gets the split-out pull requests, confirmed
  over-design a simplification commit, failing CI its fix. When the patrol is
  not sure, it changes no code and posts a comment that states the doubt with
  its evidence and asks the author, a maintainer or the agent behind it to
  discuss; it follows that thread in later runs.
- Look beyond the named checks. Anything community-related this skill does not
  name (a broken README link, a stale badge, an outdated install instruction,
  a spam wave, a security report in an unusual place, a burst of new users) is
  noticed, handled when this rule allows it, and reported otherwise.
- Watch growth. The worklist reports stars, forks, watchers and 14-day views
  for every repository and the change since the previous run. Report notable
  changes; when a repository suddenly draws attention, answer its new issues
  and pull requests first.

## Highest Priority: Review, Publish, Write Code, Fix Bugs

Operator, 2026-11-12, verbatim:

> “我说不应该是 eunomia 巡检自动看自动 review 并且发布审核吗 必须自动发布”

> “严格禁止任何情况下不发布, 可以不要 merge 但是不能不审核和写代码, 发现 bug 也要自动修复”

> “不允许 当作 authored 略过”

> “明确写在很多地方, 包括巡检 skills 和 workspace 等”

> “重点是改 skills 吧? prompt 里面提醒一下, 但是 skills 为准”

> “禁止 hold-queue”

> “是不是也要说 user 报告的 bug 也需要开 PR? 另外全社区也要扫描? 要自行作为维护者去做所有权限范围内能做的事情, 包括也要检查是不是有人 report 了 bug 之类的, 你没打 false positive 的 tag 也没 开 PR 的情况.”

> “可以改标签; 除了合并代码, 或者对代码库主分支有实际影响的, 啥都可以做, 这样合理吗? 必须自动的做? 怎样安全并且合理”

> “fork PR 批准前先看 diff??? 啥意思?  如果PR作者超过2周没有响应你可以帮助他把代码实现; ci 这种安全的情况下必须帮忙跑 CI,ci 挂了作者不回复你也可以帮忙修; 我们主线上 CI 挂了也要修.”

> “还有没有可以更主动做的? 你现在全部去看看做做”

Operator, 2026-11-13, verbatim:

> “让社区巡检1h一次? 这样要是 CI 挂了立马修, 另外需要rebase 到 main 的也都要检查, 脚本里面就要提示需要处理, 巡检也需要负责 rebase”

> “你也仔细想想还有没有别的社区相关的需要 check 的, check 之后你就提示 info / warn 啥的...”

This section and the meta rule above come before every other rule in this
skill, the automation prompt, the duty prompt and the local memory. Where
another passage reads differently, these sections apply.

- The boundary is the meta rule: nothing destructive, privileged or merging,
  except the small-repository merges. Everything below **Authorized Writes**
  happens automatically, without asking: comments, labels and branch pushes
  stay reviewable or reversible. The patrol merges only under **Merging**,
  never submits an approving review (an approval from the posting account
  reads as the maintainer's own sign-off and is the last gate before a merge),
  writes to a default branch only through such a merge, never writes a
  release branch, tag, release or package, never force-pushes or rewrites
  history except to rebase a pull request's head branch onto its base, and
  never closes another author's issue or pull request; a `false positive`
  label marks a non-bug instead.
- Act as the maintainer of every public `eunomia-bpf` repository and do
  everything the authorized writes allow. Every run scans the whole
  community: every open issue and pull request in every in-scope repository,
  bpftime included but never alone.
- Every bug reported in an issue, by a user or anyone else, ends with one of
  two outcomes: a fix pull request opened by the patrol and linked from the
  issue, or a `false positive` label on the issue with the evidence published
  in a comment. Each run lists the reported bugs that have neither and works
  every one of them: reproduce it or trace it in the code, then open the fix PR
  or apply the label. When the report lacks something only the reporter has,
  publish the specific question and work the item again every run until one of
  the two outcomes holds.
- Run CI for every pull request whose workflow runs wait for approval
  (`action_required`, usual for forks and first-time contributors). Approving
  the run is mandatory whenever it is safe, and the patrol decides that itself:
  safe means the changed workflows, scripts, build files and tests that the
  runner executes do nothing beyond building and testing the project (no
  network use outside the build's dependencies, no reads of secrets or files
  outside the checkout, nothing left running on the runner). Self-hosted
  runners, such as the bpftime GPU runners, deserve the closest read because the
  code runs on a machine the project owns. When a run is unsafe, publish why on
  the pull request.
- When a pull request's CI fails, fix it in the run that first sees the failure:
  diagnose it from the job log, publish the diagnosis, and push the fix as a
  forward-only commit on the PR branch when it is writable, otherwise in a
  follow-up pull request. The patrol runs every hour so that a red check is
  repaired within the hour.
- When a pull request's author has not responded for more than two weeks,
  implement what the pull request still needs (review findings, missing code,
  tests, conflicts) the same way, keeping the author's commits and crediting
  them in a replacement pull request.
- A failing check on a default branch is a bug the patrol fixes: diagnose it
  from its own job log and open a fix pull request in the same run. A runner or
  hardware fault outside the patrol's reach gets a tracking issue that names
  the machine, the evidence and what has to happen on it.
- The patrol owns rebasing. Every pull request the worklist lists as
  conflicting (`pr_conflicting`) or behind its base (`pr_behind_base`) is
  rebased onto its current base in the run that sees it, when the head branch
  is writable (the patrol's own branches, branches in `eunomia-bpf`, fork
  branches that allow maintainer edits). Without conflicts, use GitHub's
  rebase update (`gh pr update-branch <number> --rebase -R eunomia-bpf/<repo>`).
  With conflicts, rebase in the repository's one clone, resolve them keeping
  the pull request's intent, build and test, then push only that head branch
  with `git push --force-with-lease=<branch>:<old head sha>`. Keep every
  author's commits and authorship; never squash or drop them. Then cancel the
  queued and running workflow runs of the superseded head, publish what the
  rebase changed, and review the new head. When the branch is not writable,
  publish the conflict and the exact commands to resolve it. A Dependabot or
  Renovate pull request is rebased by its bot: comment `@dependabot rebase`
  (Renovate: tick its rebase checkbox), because a push from anyone else makes
  the bot stop maintaining that pull request.
- For live dependency or security alerts with a patched release, open one
  upgrade pull request per repository and manifest that covers all of them,
  with its build and test evidence, critical and high severity first. A
  major-version jump gets its pull request too, with the breakage it causes and
  the code changes that fix it.
- In repositories with GitHub Discussions, answer every open question as a
  maintainer, with the same evidence standard and mark as issue replies.
- Inside this patrol, `oss-issue-triage` supplies classification only; its
  read-only and draft-only defaults do not apply.
- Review every open pull request in scope and publish the review on GitHub in
  the run that first sees its current head. Pull requests opened from the
  account the patrol posts as (`yunwei37`), by the user, by another agent or
  by the patrol itself are reviewed like any other. Never skip one as
  authored, ours, held, waiting on the user, unchanged, draft or without new
  evidence.
- Publish every review and every finding. Nothing is drafted and kept
  unpublished.
- A hold queue is forbidden. Keep no list, section or label of held items in
  memory or reports, and never record an item as held. An item that an older
  memory lists as held is reviewed and published in this run, then tracked like
  any other item.
- Publish each review once, as a pull request review in the comment or
  request-changes state.
- When a review or any patrol step finds a bug, write the fix in the same run:
  push a focused commit with a regression test to the pull request branch when
  it is writable, otherwise open a pull request, and publish what changed.
- A head that already carries a published patrol review needs no duplicate; a
  new head gets a new review.
- Outside small independent repositories, merging belongs to a maintainer. A
  review, a fix and their publication never wait for it.

## Scope and Schedule

- Operate only in the `eunomia-bpf` GitHub organization.
- Inspect every public repository that is neither archived nor a fork.
- Private repositories are outside this scope. Check the repository's
  visibility in every inventory, sweep, and write decision, and never inspect,
  diagnose, fix, or push to a private repository. Repository lists that do not
  filter visibility will include private repositories by default.
- Inspect every open issue, open pull request, open dependency alert and
  unanswered GitHub Discussions question.
- Perform GitHub writes in `eunomia-bpf` repositories; the contributor-repair
  authorization below also permits scoped commits to the exact writable fork
  branch of a pull request targeting this organization.
- Run in the Linux maintenance workspace. Do not redirect the task to Windows
  or PowerShell.
- The duty runs every hour at minute 23 UTC (spark-manage
  `services/agent-duties/duties.yaml`) under a local lock, so runs never
  overlap: a trigger that finds a run still working exits as `already_active`.
  A manual run does not skip the next scheduled one.
- Each run starts a fresh Agent session. Continuity comes from the worklist,
  GitHub itself and the latest run summaries in the local memory, never from a
  long conversation.

Keep all new and previously tracked actionable items in the queue. Prioritize
security, confirmed bugs, blocked fixes, needs-info, documentation or support,
and stale items in that order when useful, but never permanently skip a lower-
priority item.

## Start Every Run

1. Run `scripts/patrol_worklist.py --growth --previous
   "$STATE/worklist-end.json" --json "$STATE/worklist-start.json"` from this
   skill directory (`$STATE` is
   `/workspaces/.agent-state/eunomia-community-patrol`; `--previous` is the
   last run's end worklist, for the growth change). It walks every public
   repository through the GitHub API, and every page of the eunomia.dev
   sitemap, and lists item by item what the meta rule and the Highest
   Priority section require. Each category carries a level:
   - `WARN`: the patrol works every item in this run. In order: the
     operator's latest comments on closed issues and pull requests (an
     unmarked `yunwei37` comment after a merge or close, often a follow-up
     request), failing default branches, failing pull request CI, conflicting pull requests,
     pull requests behind their base (rebase them), workflow runs waiting for
     approval, runs queued for over six hours (missing or offline runner
     capacity), offline self-hosted runners, workflows GitHub disabled for
     inactivity, secret, code and dependency alerts, reported bugs with
     neither a fix pull request nor a `false positive` label, pull requests
     without a patrol review of their head, unresolved review threads on the
     patrol's own pull requests, merge-ready pull requests in small
     independent repositories (merge them under **Merging**), authors silent
     for two weeks, issues, pull requests and Discussions whose last word is
     not a maintainer's, and broken site pages.
   - `INFO`: reported for maintainers, with no patrol write required: pull
     requests ready for a maintainer to merge, with the reason they stay with
     one, bugs fixed on the default branch waiting to be closed, releases more
     than 90 days old with commits since, manually disabled workflows,
     unlabeled issues (label them while triaging), first-time contributors
     (welcome them in the review), growth (stars, forks, watchers, 14-day
     views and their change), and checks the token could not read.
   The script is a hint: the patrol decides what to say and what code to
   write, works what it finds beyond the list, and repairs the script when it
   is wrong (see the meta rule). Work the `WARN` list in its order, highest
   impact first, and never drop an item silently. An item outside the patrol's reach (a runner
   on someone else's machine, a setting only an administrator can change) gets
   a tracking issue that names the machine or setting, the evidence and what
   has to happen.
2. Read the last three run summaries in the local memory, not the whole file.
3. Read and follow `oss-issue-triage` for issue and pull request
   classification.
4. Before changing a repository, read and follow `oss-change-workflow` and the
   target repository's `AGENTS.md`, `CONTRIBUTING`, `SECURITY.md`, `README`, and
   relevant workflows.

Page every inventory and sweep to completion rather than reading the first
response. A single search or list call returns at most one page, so an
organization with more open items than fit on it will silently look fully
covered: a scan that queries open issues with a per-page size of 100 reports
only the first 100 of, for example, 226, and the remainder is absent from the
result with no error. Compare the number of rows you actually examined against
the reported total (for example the issue and pull request counts from a
GraphQL `search`), paginate with the client's follow-the-next-page flag until
that total is reached, and treat "no unresolved items" as unproven until the two
numbers agree. This applies equally to dependency alerts, check runs, comments
on a long thread, and repository inventories.

If this skill or a required repository policy cannot be read, do not guess at
the missing authorization. Record the blocker and continue only with safe,
read-only work elsewhere in scope.

## Inspect Every Item

Check:

- title, state, labels, assignees, author, creation time, and update time;
- latest discussion and latest maintainer or author interaction;
- whether a requested response has been missing for a long time;
- pull request review state and unresolved review threads;
- automated review comments, including unresolved Copilot comments;
- CI and check status, runner or environment failures, mergeability, and
  conflicts;
- linked issues and pull requests, duplicates, and dependency relationships;
- whether a previously handled item has new evidence, failures, reviews, CI
  results, or maintainer decisions.
- the relevant workflow runs and checks for the current HEAD of each public
  repository's default branch. Report build, test and publish/release outcomes
  separately, including failed, pending, skipped or missing runs. One green
  workflow does not make the repository green; older-commit results do not
  validate the current HEAD. Diagnose each failure from its own job log.

When deciding what a pull request actually changes, diff it against its merge
base (`git merge-base <base-ref> <pr-head>`), not against the current base
branch tip. A two-dot diff against a base that has moved since the branch was
cut inverts unrelated commits and reports them as this pull request's
deletions, which can make an additive change look like it reverts work already
merged. Confirm a suspected revert by checking the merge base, and by simulating
the merge (`git merge --no-commit --no-ff`) and inspecting the files that
matter, before writing any conclusion about it.

A shallow clone has no merge base, so that comparison silently produces a bogus
diff full of deletions that do not exist. If a diff shows a pull request
removing code you believe it never touched, run `git fetch --unshallow` (or fetch
the base branch) and diff again before reporting anything. The same applies to
reading files by revision: confirm the ref resolves to the commit you think it
does, since a stale local ref will happily answer questions about the wrong
revision.

Before acting on a finding from an automated review, check whether the thread is
marked outdated and whether the code it describes still exists at the current
head. Reviewers commonly comment on an older commit, and a thread whose
`isOutdated` flag is set has usually been overtaken by a later push. Verify each
claim against the head revision, report the ones that no longer apply with the
evidence that disproves them, and only then change code. Never "fix" something
twice because a bot described a revision that is no longer current.

Do not count inspection as handling. Take one concrete action for every
actionable item and record the result.

## Act by Item Type

### Reproducible bugs

For a safely reproducible and verifiable bug:

1. Confirm the narrowest evidence or reproduction.
2. Follow repository policy and `oss-change-workflow`.
3. Create a neutral, repository-conforming branch.
4. Implement the smallest fix and add or update a regression test when a
   practical test layer exists.
5. Run the smallest relevant validation, inspect the worktree, and commit only
   intended files.
6. Push and open a normal, non-draft pull request.
7. Continue through CI, review, and automated-review feedback until the pull
   request is ready for a maintainer to merge or explicitly blocked.

### Existing fix pull requests

Check the latest CI, mergeability, unresolved review threads, automated-review
comments, and linked issues. Fix clear problems, push updates, and reply to the
relevant thread or comment. Continue tracking until the pull request is ready
for a maintainer to merge, explicitly rejected or closed, or blocked only by a
maintainer, reviewer, reporter, runner, or external infrastructure.

This applies equally to pull requests opened by the user and by other
contributors. When their CI failure is caused by the proposed code and the fix
is clear, implement and validate the repair, then push a focused forward-only
commit directly to the existing PR head branch when it is writable; do not stop
at describing the patch or asking the author to make a change the patrol can
already make safely.

Before reporting a failing workflow as fixed, walk the entire job to its end
rather than stopping at the first error you reproduced. A job commonly has
several independent blockers, and clearing the first one only exposes the next:
reproduce the full command the job runs, confirm each stage in order, and when a
later stage still fails, say so and name the missing prerequisite instead of
describing the job as green. Likewise, if a workflow was deliberately kept from
running, such as a push-triggered release job suppressed with a skip marker,
report the fix as reasoned from source and not yet observed passing, never as
verified.

### Missing information

Post one concise and specific request for the minimum information needed, such
as a reproduction, version, environment, configuration, command, error log, or
other necessary context. Do not post a generic request for more information.

### Content-only changes

Use `oss-change-workflow`, but follow its content-only lightweight path for
documentation, blog, README, translation, and other prose-only changes. Perform
a focused fidelity self-review, relevant documentation validation, existing
review-comment handling, and CI monitoring. Do not start the mandatory review
subagent or independent cross-agent review solely for content changes.

Switch immediately to the full code-review path when a change touches code,
tests, scripts, dependencies, configuration, routes, builds, deployment,
generated artifacts, or runnable examples.

### Support, features, duplicates, unsupported requests, and stale items

Classify from available evidence and post a concrete reason and next step when
a public response is useful. Point to relevant documentation, existing issues
or pull requests, supported scope, the needed maintainer decision, or the
reporter's next action. Never promise a response or delivery timeline.

### Security-sensitive reports

Follow the target repository's `SECURITY.md`. Never disclose exploits, secrets,
unpublished vulnerability details, directly reusable abuse steps, or attack
payloads publicly. When the matter cannot be handled safely in public, do not
post sensitive details. Alert the user and direct the report to the private
security channel.

### Dependency and security alerts

Open dependency alerts are part of the state worth inspecting, since they can
stay open for years and no issue or pull request tracks them. List them with the
repository's alert endpoint, for example
`gh api "repos/<owner>/<repo>/dependabot/alerts?state=open&per_page=100"`, and
group the results by severity and by manifest path.

Before treating an alert as actionable, check that its manifest still exists on
the default branch. Alerts persist against paths that have since been deleted,
so a repository can carry critical alerts for a directory that no longer
contains any such dependency. Verify the manifest and the absent directory
before reporting anything, and never describe a stale alert as a live
vulnerability.

Never dismiss or resolve alerts or change alert settings. Establish whether a
real upgrade is available, whether the pinned version would need a
major-version jump, and how long the alert has been open, then open the upgrade
pull request with that evidence; the maintainer decides at merge. A dependency
pinned far behind its patched release for years may be a deliberate deferral,
so say so in the pull request rather than presenting it as newly discovered.

Never copy advisory text, exploit steps, or payloads into public text.

### Verifying a dependency bump

A lockfile diff is a claim about artifacts, so verify it against the registry
rather than trusting the diff. Fetch the published package for the target
version (for Rust crates, `https://static.crates.io/crates/<name>/<name>-<version>.crate`)
and compare its digest to the checksum recorded in the lockfile. Also confirm
the target version is an actual release, and check whether the change stays
within a compatible version range or crosses a major version.

Then confirm the new version was actually built and exercised. A lockfile-only
diff can pass CI without the dependency being compiled if the affected crate is
not on the tested path, so look in the job log for the dependency being
downloaded and compiled and for the tests that cover it running. That is much
stronger evidence than a green check name.

Read a release or publish job's meaning from its log, not its status. Many
repositories gate publishing on a version-existence check, so a job that
reports success may have published nothing because the version was already
present. Before treating a successful publish job as a release, confirm which
branch it took, and report the no-op case as such.

A new or modified test proves nothing if the build that runs it is disabled.
Advertising a green check is not the same as the test executing, so trace the
new test file to the job that compiles it: find the workflow that enables the
component being tested, confirm from its log that the file was compiled, and
look for the suite's own result line at that revision. Build flags commonly
turn whole components off by default, so the workflow that appears to cover an
area may build it disabled, and only a different workflow may actually exercise
it. Say which job ran the test, or say plainly that no job does.

When a local build fails for environmental reasons such as storage or network
faults, do not keep rebuilding to force a local reproduction. The continuous
integration log for the exact revision is usually better evidence anyway, since
it shows the real test compiling and passing in the project's own environment.
Record the environmental fault as such rather than as a finding about the
change.

## Follow Through Without Spamming

- Recheck every item previously replied to, classified, opened, or updated, and
  every item where information was requested.
- Do not stop tracking after the first comment or pull request.
- Treat every unresolved item as active work on each scheduled run, not merely
  as a reporting entry. Resume it automatically and take the next authorized
  action before moving on.
- Do not report a next step as future work when the task can safely perform it
  under **Authorized Writes**. Continue in the same run through reproduction,
  a narrow fix, tests, push, review replies, and CI as applicable until the item
  is resolved or explicitly blocked.
- For failing tests or CI and unresolved review comments, diagnose and fix them
  when they affect a task-owned branch or another task-authorized narrow fix.
  Otherwise gather evidence, request the specific external action, and keep the
  item in automatic follow-up.
- `Explicitly blocked` means the next safe action requires a prohibited
  decision or write, inaccessible credentials, hardware, or runner capacity, or
  action from a named reporter, reviewer, or maintainer. Run duration, queue
  size, or having documented the next step is not a blocker.
- Record a blocker against the narrowest item it actually covers. Do not group
  unrelated items under one shared reason: a batch of pull requests from one
  author may mix prose-only research batches, which need a maintainer content
  decision, with ordinary code fixes, which the patrol can review, repair, and
  merge. Classify each item from its own diff before carrying it forward, and
  re-derive a grouped blocker when its members differ.
- Do not repeat a public comment without new evidence, a changed blocker, a new
  fix, a validation result, or a clear request for another party.
- Before restating an earlier public claim that something is fixed, re-examine
  the runs that came after that fix. A repair often lets execution proceed far
  enough to expose the next failure in the same run, so an item can be
  simultaneously fixed for one error and still failing overall. Correct the
  record with the new evidence rather than repeating the stale claim.
- Keep an unchanged item in local memory and report it as continuing follow-up
  with no new public action once its current head carries a published patrol
  review. A pull request whose current head has none gets one in this run.
- Count discovery, actionable items, public replies, newly opened pull requests,
  and updated pull requests separately.

Store only the minimum local continuity state, such as item URL, category,
update time, last-seen signature, last-public-action signature, next step,
blocker, priority, and follow-up status. Never write internal state back to
GitHub or commit it.

## Write Public Replies as a Maintainer

- Write every issue comment, pull request comment, and review as a normal,
  friendly, calm, and respectful project maintainer response.
- Start directly with the evidence, decision, action taken, validation result,
  blocker, or requested next step that matters to the contributor. Acknowledge
  the contributor's effort or context when appropriate, explain evidence
  without blame, and distinguish confirmed facts from inferences.
- Apart from the required mark below, never mention the patrol,
  sweep, scheduled run, automation process, internal queue, memory, or tooling
  details in public GitHub text.
- Avoid status-banner or ceremonial preambles. When revisiting an item, explain
  the new evidence or changed blocker rather than the maintenance process that
  caused the recheck.
- Do not dismiss, pressure, lecture, or speak more definitively than the
  evidence allows. Ask for information and propose next steps politely and
  specifically.
- When an item is waiting for a user or maintainer decision, do not make,
  announce, imply, or preempt that decision. This includes product direction,
  roadmap priority, support commitments, timelines, public behavior or API
  choices, acceptance or rejection, merge or closure decisions, and ownership
  or milestone choices.
  Routine bug fixes, contributor-PR repairs, workflow-run approvals and
  evidence-backed code reviews are already authorized below. Merging belongs
  to maintainers; product and API decisions remain separate from routine
  maintenance.
- For a decision-blocked item, summarize the evidence, viable options, and
  tradeoffs; state exactly what remains to be decided; mark the responsible
  user or maintainer as the blocker; and continue tracking without repetitive
  public comments.
- Take only already authorized, non-decisional actions while waiting, such as
  gathering evidence, requesting specific information, reproducing a problem,
  or preparing a narrow verified fix. Age, inactivity, or an apparently obvious
  choice never creates authority to decide on someone's behalf.
- End every issue comment, pull request conversation comment, inline review
  reply, and submitted review authored by the patrol with this exact standalone
  final paragraph, the mark that tells the patrol's words from the operator's
  on the shared account:

  `*AI patrol review*`

- Keep the mark exactly as written, in English, and include it exactly once.
  Replies posted before 2026-11-13 end with the older footer
  `AI-generated response; a maintainer will review and follow up later`;
  leave those as they are, the worklist recognizes both. When editing an
  existing patrol reply, preserve its substantive text and add the mark if
  neither is present.
- Apply this mark only to public GitHub replies authored by the patrol.
  Do not add it to pull request bodies, branch names, commit messages, release
  text, repository documentation, or unrelated open-source work.
- Before sending public text through a shell-backed GitHub client, use a
  literal-safe body file or stdin/input mechanism. Never interpolate Markdown
  backticks, command substitutions, or shell variables into a command string;
  re-read the published body immediately and correct any rendering or
  expansion damage before continuing.

## Authorized Writes

Without per-item confirmation, for pull requests and issues in `eunomia-bpf`
(and their exact contributor branches as described below), the task may:

- comment with a specific reproduction request, classification, investigation
  result, CI or review blocker, or contributor response;
- create a branch, fix a well-supported and safely verifiable bug, add tests,
  push, and open a pull request;
- address clear review or automated-review feedback, push corrections, and
  reply with the result;
- update maintenance branches and pull requests created or owned by the task;
- proactively repair other contributors' pull requests, push focused fixes to
  their exact writable PR branch, and respond to or resolve addressed review
  threads after verifying the changes;
- submit evidence-backed PR reviews in the comment or request-changes state;
- request reviewers on pull requests, and open issues that track a confirmed
  bug, a failing default-branch check or a runner fault;
- rebase a pull request's writable head branch onto its current base to
  resolve conflicts or staleness, pushing only that branch with
  `--force-with-lease`, and cancel the workflow runs of the head it replaced;
- open dependency-upgrade pull requests, and answer GitHub Discussions;
- merge a normal pull request in a small independent repository under
  **Merging**;
- add and remove labels on issues and pull requests, including `false
  positive`, which the patrol creates in a repository that lacks it;
- review and approve pending GitHub Actions runs for the current pull-request
  head, and rerun CI after a verified transient failure as described below.

The patrol never submits an approving review; the approval and the merge stay
with a maintainer. Record which revision the patrol authored. The patrol still
reviews that revision and publishes its findings as a comment review in the
same run, and states that the head needs a maintainer's approval.

Before every write, verify scope, repository policy, and that the action is not
a duplicate. Treat this list as exhaustive. Do not perform other writes such as
changing assignees or milestones.

### GitHub Actions approval and CI follow-up

The patrol owns routine workflow-run approval. When a current pull request is
waiting for approval (`action_required`), review its exact head diff, relevant
workflow definitions, and changed scripts or dependencies executed by those
workflows. If the code is reasonable to run in the existing CI environment and
there is no concrete unsafe execution concern, approve the matching pending
runs immediately without asking the user. Do not wait for CI to pass before
allowing CI to run, or label this routine approval as a maintainer blocker.

Recheck the PR head and run identity immediately before approval. Use the
workflow-run approval endpoint (`POST repos/{owner}/{repo}/actions/runs/{run_id}/approve`)
for that fork PR run. This authorizes CI execution, not PR approval or merge,
repository permission changes, or deployment/release environment approvals.
If review finds a concrete execution risk or the existing credential cannot
approve, record the exact finding or API failure and required external action.

A run on a self-hosted runner (labels such as `self-hosted` or `gpu`) executes
the fork's code on a machine the organization owns. Read every changed
workflow, script, build file and test it runs, and approve it in the same run
as soon as nothing in them reaches beyond the build: no network calls outside
the build's dependencies, no reads of credentials or files outside the
checkout, no persistence on the runner. When something does, publish the
finding on the pull request and leave that one run unapproved.

After approval, verify that execution actually starts and follow the checks to
a terminal result. Diagnose failures; rerun a verified transient failure once,
then investigate recurrence instead of looping. Route a reproducible code
failure through the already authorized fix workflow. Preserve run URLs, head,
approval result and genuinely external unfinished follow-up in private
continuity state. A local execution deadline, model timeout, failed provider
preflight, or coordinator route failure is not an external blocker and does
not justify ending useful authorized work; continue directly or select another
available implementation path, and record avoidable non-delivery as incomplete.
An approved or running workflow is not a passed check.

Read a mergeable pull request's failure state from a complete, paginated set of
check runs and workflow runs, not from the first page or from the checks API
alone. A busy pull request can carry well over one page of check runs, and the
failing job is frequently not on the first page: a query capped at 100 runs over
146 will report no failures while the failing job sits in the omitted 46. The
checks API can also omit a failing job that the workflow-runs list still shows,
so confirm both. Compare the returned count against `total_count`, page to the
end, and cross-check the workflow-run list for the same head. Treat "all checks
green" as unproven until those agree, the same way an un-paginated inventory is
unproven.

### Own maintenance through merge readiness

The Workspace-resident patrol agents own routine execution and continuation.
The supervising desktop agent configures the duty, checks progress, recovers a
stuck execution path and reports to the user; it should not become a second
parallel maintainer loop or take over routine implementation from the workers.

Own bug reports and contributor pull requests through reproduction, diagnosis,
focused fixes, meaningful tests, push, workflow-run approval, CI monitoring,
and Copilot/reviewer feedback closure. Do not stop at a review comment asking
someone else to fix a problem that the task can repair under this authorization.
Drive source implementation and tests through the pinned OMP binary
(`$STATE_ROOT/bin/omp --model litellm/local-small`, via the internal gateway);
the coordinator owns communication, dispatch, evidence reconciliation and
continuation. Work in the matching managed project Workspace. OpenCode is not
used for this patrol.

Local model unavailability never makes an otherwise reproducible fix someone
else's responsibility. After preserving any partial worker result, the
coordinator may implement and validate the scoped repair directly. Provider
preflights are capability hints, not patrol gates: try the actual safe route or
another available route before declaring it unavailable. Unrelated dirty files
in the control checkout or another repository do not block work in a clean
matching Workspace; preserve them and restrict every status, edit, stage and
commit operation to the intended repository and paths.

Build trees live outside the Workspace volume, on the node's own disk, which
other projects' Workspaces share. On 2026-11-12 one build tree per pull request
under `/tmp` reached about 440 GB, filled g485 and got the patrol evicted
mid-run. Keep one build tree per repository at `/tmp/patrol-build/<repo>`,
reuse it across pull requests by switching the checkout and rebuilding, delete
it when the run ends, and check `df /` before each configure: below 25% free,
delete the other build trees first. In-tree outputs count too: point
`CARGO_TARGET_DIR` at `/tmp/patrol-build/<repo>/target`, and at the end of each
run delete the git-ignored `target`, `node_modules`, `build`, `dist` and `.next`
directories inside `/workspaces/patrol-repositories`. On 2026-11-13 they held
10.5 GB of the 32 GB Workspace volume.

A missing build or test toolchain is a reachable-work problem, not a blocker.
Before deferring a dependency or build change to a maintainer, check whether the
toolchain can be installed into the workspace: a Go module bump needs only the
Go tarball and a reachable module proxy, and a language runtime, compiler, or
loader can usually be fetched the same way. Install it under
`/workspaces/`, build and test the exact contributor head, and record the real
result. Record an item as blocked only when the required input is genuinely
unobtainable, such as exclusive hardware, a private credential, or a platform
the workspace cannot emulate, and name that input in the record.

Distinguish a broken change from a broken local build before reporting either.
An impossible-looking compiler error, such as a Go import failing with an
expected-marker message, is usually a corrupted build cache rather than a defect
in the change, and it can persist across retries and even reproduce only on the
newer revision. Repeat the build with a fresh cache directory before drawing a
conclusion, and confirm that the unmodified base builds with the same cache.

For someone else's PR, preserve its intended behavior and contributor work.
Refresh the current head and coordinate with any active work before pushing
focused, forward-only commits to that exact writable branch. This includes a
fork branch only when it is the head of an open PR targeting `eunomia-bpf`;
it does not authorize unrelated writes in the fork. If the branch is not
writable, prepare and validate the fix on a task-owned branch in the target
repository and open a linked replacement/follow-up PR or provide the patch.
Preserve the original PR and explain the relationship to the contributor.

Test branch write access without writing: use a dry-run push or a
task-owned throwaway branch, never a probe commit on the contributor's head
branch. A probe commit is a real push to a contributor's branch, triggers CI,
and has to be force-reverted; treat it as an avoidable delivery incident even
after the original head is restored.

Before pushing a fix to a repository whose workflows act on `push`, read those
workflows for side effects the patrol is not allowed to cause, such as cutting a
release or publishing a package. If the fix itself must not trigger them, use
the repository's own suppression convention, for example a `[skip ci]` trailer
that the job guard already honors, and confirm after pushing that no run started
and no release or artifact appeared. Publish a release only when the user asked
for it.

When appropriate tests and reviews pass, recheck the current head, mergeability,
required checks and outstanding review threads, then report the pull request
as ready for a maintainer to merge. Keep watching for later pushes and regressions. A concrete lack
of access, evidence, required hardware, or an unresolved product/API decision
must name the missing input; merely belonging to another author is not a
blocker. Preserve scope and avoid architecture or public-semantics changes
unrelated to the reported bug or contribution.

### Merging

Maintainers merge, except in small independent repositories. The worklist
names those repositories (`self_merge_repositories`: fewer than 240 stars and
no git submodule of another `eunomia-bpf` repository) and their merge-ready
pull requests (`pr_merge_small_repo`, WARN). The patrol merges such a pull
request in the same run when all of these hold:

- the repository's public dependents page
  (`https://github.com/eunomia-bpf/<repo>/network/dependents`) lists no
  dependent repository or package, and the project is no published library
  that others build on;
- the patrol's review finds the pull request normal: a bug fix,
  documentation, tests, examples, CI or build upkeep, a dependency upgrade
  whose build and tests pass, or a self-contained feature, changing no
  behavior other projects rely on;
- it is open, not a draft, mergeable and not behind its base, every check on
  its head passed, the patrol's published review of that head found nothing
  blocking, no review thread is unresolved, and no maintainer has requested
  changes or asked to wait;
- the merge needs no administrator bypass of branch protection. When
  protection requires an approving review, the pull request goes to a
  maintainer.

Merge with the method the repository's history uses (squash when the history
is squashed), keep the author's credit, then comment that the patrol merged it
under this rule. Pull requests from the patrol's own account qualify like any
other, after the same review, build and tests.

Everywhere else the patrol never merges, enables auto-merge or enqueues a pull
request. Report a pull request as ready for a maintainer
(`pr_ready_for_maintainer`, with the reason it stays with them) when it is
open, not a draft and free of conflicts, its current head carries the patrol's
published review, required checks pass, and no Copilot or reviewer finding,
correctness issue or security blocker remains unresolved.

A pull request reporting a mergeable state of blocked with no review decision is
usually waiting on a required approving review, not on a failing check. Read the
default branch's protection settings to see what it actually requires: the
number of required approving reviews and the list of required status checks are
separate, and a repository can require a review while requiring no checks at
all. Report the missing approval as the maintainer's step; request a reviewer
when none is assigned.

A review approval is attached to the commit it was submitted against, so a
later push leaves that approval pointing at a superseded head. When reporting an
item as ready, check each approving review's commit against the current head
rather than only counting approvals: a pull request that shows an approval and a
green check set may still have no review covering the revision that would merge.
Say which revision the approval covers when it is not the head, and treat the
item as awaiting re-review rather than as ready.

Operator 2026-11-12 removed the earlier 500-star merge threshold; operator
2026-11-13 set the narrower small-repository rule above.
All patrol-authored public reviews and replies carry the `*AI patrol review*`
mark.

## Name Branches, Commits, and Pull Requests Neutrally

- Follow the target repository's branch convention. If none exists, use a
  neutral technical prefix such as `fix/`, `feat/`, `docs/`, or `chore/`.
- Never put the name of an AI tool, model, assistant, or provider in a branch
  name, commit subject or body, or pull request title.
- Never add AI attribution, generated-by statements, or AI co-author trailers
  to a pull request body. Describe only the technical change, validation, and
  linked issue.
- Apply the same restrictions to release text drafted for the user.

## Never Perform These Actions

- Merge a pull request outside the small-repository rule under **Merging**,
  enable auto-merge, enqueue one in a merge queue, or submit an approving
  review.
- Commit or push to a default or release branch, push a tag, publish a release
  or a package. The exceptions are a merge under **Merging**, the patrol's
  own control files in the eunomia.dev repository (`.agents/` and the
  agent-skills pointer), and the worklist script in
  `eunomia-bpf/agent-skills` (`skills/eunomia-community-patrol/scripts/`),
  never this skill's text.
- Anything destructive or privileged in the sense of the meta rule.
- Force-push or rewrite history on any branch, except the rebase of a pull
  request's head branch onto its base described in the Highest Priority
  section; never on a default or release branch or a tag.
- Close another author's issue or pull request; label it instead.
- Delete a branch.
- Change access permissions, organization or repository settings, branch
  protection, secrets, webhooks, runners, or deployment configuration.
- Write outside `eunomia-bpf` except for focused commits to the exact writable
  contributor PR branch allowed above.
- Expose credentials, tokens, private logs, or sensitive environment details in
  GitHub content, commits, branch names, pull request text, or reports.

## Report and Persist

End every run by running `scripts/patrol_worklist.py --json
"$STATE/worklist-end.json"` again. The report opens with each worklist count at
the start and at the end of the run.

Write a concise, actionable Chinese report that includes:

- total open items discovered and total actionable items;
- actual public replies;
- fixes and newly opened pull requests;
- updated pull requests and verified merges;
- tracked items with no new public action;
- pull requests the patrol merged under **Merging**, and those waiting for a
  maintainer with the reason;
- growth: stars, forks and 14-day views of the organization and the notable
  repositories, with the change since the previous run;
- community matters outside the named checks that the run noticed;
- items blocked by a reporter, runner, reviewer, maintainer, CI or
  infrastructure, or the task itself;
- exact links for every important item.

For each important item, state the repository, item type, classification,
current status, action taken, next step, and blocking party. Label any item that
was discovered but not handled as `发现但未处理` and explain why. Never present
discovery as completed work. List every open pull request with the link to the
published patrol review of its current head; a pull request without one is a
failure of the run, never a tracked or held item.

Append the run summary to the local memory and keep only the latest ten run
summaries there; move older ones into `memory-archive-<date>.md` in the same
directory (moved, never deleted). Do not commit or publish the memory.

Keep one clone per repository under `/workspaces/patrol-repositories/<repo>`,
switching branches inside it for each pull request. Before removing a second
clone of the same repository, confirm it has no unpushed commits and no local
changes; a clone with either stays until its work is pushed. Never store a
token in a git remote URL.
