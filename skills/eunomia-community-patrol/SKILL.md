---
name: eunomia-community-patrol
description: Inspect, triage, and actively maintain all open GitHub issues and pull requests across public, non-archived, non-fork eunomia-bpf repositories. Use for recurring Eunomia community patrols, organization-wide issue and PR sweeps, follow-up of prior maintenance comments or pull requests, and scheduled maintenance that may comment, fix verified bugs, push, open pull requests, and proactively repair contributor pull requests through review and CI readiness and autonomously merge eligible PRs in repositories with fewer than 500 stars, while reserving higher-star repository merges for the user.
---

# Eunomia Community Patrol

Treat this skill as the versioned source of truth for the Eunomia community
maintenance task. Keep runtime state, credentials, private logs, and
deduplication records outside the repository.

## Scope and Schedule

- Operate only in the `eunomia-bpf` GitHub organization.
- Inspect every public repository that is neither archived nor a fork.
- Private repositories are outside this scope. Check the repository's
  visibility in every inventory, sweep, and write decision, and never inspect,
  diagnose, fix, or push to a private repository. Repository lists that do not
  filter visibility will include private repositories by default.
- Inspect every open issue and open pull request.
- Perform GitHub writes in `eunomia-bpf` repositories; the contributor-repair
  authorization below also permits scoped commits to the exact writable fork
  branch of a pull request targeting this organization.
- Run in the Linux maintenance workspace. Do not redirect the task to Windows
  or PowerShell.
- Schedule the patrol for 09:00 `America/Vancouver` every calendar day. A
  successful manual patrol does not skip the next scheduled day. Retry a failed
  run at the next daily scheduler wake and prevent overlapping runs with a
  local lock.
- Resume the designated Agent conversation for each eligible run so the final
  report appears in that conversation. If the target session is unavailable,
  fail without starting a second patrol, preserve the local log, and retry at
  the next scheduler wake.

Keep all new and previously tracked actionable items in the queue. Prioritize
security, confirmed bugs, blocked fixes, needs-info, documentation or support,
and stale items in that order when useful, but never permanently skip a lower-
priority item.

## Start Every Run

1. Read the local automation memory completely. Use it to avoid duplicate
   comments and resume every unresolved item.
2. Read and follow `oss-issue-triage` for issue and pull request
   classification.
3. Refresh the organization repository list instead of relying on the previous
   inventory.
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
- the latest workflow run on each public repository's default branch, not only
  open issues and pull requests. Broken main or master CI can persist for
  months with no open item tracking it, so sweep the in-scope repositories for
  a failing default-branch run and diagnose it from its own job log. Filter on
  the repository's visibility and exclude private repositories, which are
  outside this patrol's inspection and write scope.

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

Do not upgrade dependencies, dismiss or resolve alerts, or change alert
settings: those are outside the authorized writes. Establish whether a real
upgrade is available, whether the pinned version would need a major-version
jump, and how long the alert has been open, then report it as a maintainer
decision with that evidence. A dependency pinned far behind its patched release
for years is usually a deliberate deferral rather than an oversight, and say so
rather than presenting it as newly discovered.

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
  with no new public action.
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
- Apart from the required disclosure footer below, never mention the patrol,
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
  evidence-backed code reviews are already authorized below. Merge authority
  follows the live-star threshold below; product and API decisions remain
  separate from routine maintenance.
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
  final paragraph:

  `AI-generated response; a maintainer will review and follow up later`

- Keep the disclosure exactly as written, in English, and include it exactly
  once. When editing an existing patrol reply, preserve its substantive text
  and add the footer if it is missing.
- Apply this disclosure only to public GitHub replies authored by the patrol.
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
- submit evidence-backed PR reviews, including approval when review and
  relevant validation support it; PR approval alone does not satisfy the merge
  gates below;
- merge an eligible PR in a target repository with fewer than 500 live GitHub
  stars after all of the merge gates below pass;
- review and approve pending GitHub Actions runs for the current pull-request
  head, and rerun CI after a verified transient failure as described below.

Before every write, verify scope, repository policy, and that the action is not
a duplicate. Treat this list as exhaustive. Do not perform other writes such as
changing labels, assignees, or milestones.

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
required checks and outstanding review threads, then apply the live-star merge
policy below. Keep watching for later pushes and regressions. A concrete lack
of access, evidence, required hardware, or an unresolved product/API decision
must name the missing input; merely belonging to another author is not a
blocker. Preserve scope and avoid architecture or public-semantics changes
unrelated to the reported bug or contribution.

### Merge authority by live repository stars

Immediately before a merge, query the target repository's current GitHub
`stargazers_count`; do not use the fork's stars or a cached inventory count.
At 500 or more stars, leave the final merge to the user and report readiness.
Below 500 stars, the Workspace agent may perform the merge without per-PR
confirmation only after all of these conditions hold:

- The PR is open, not a draft, and has no merge conflict.
- The latest head has completed the repository-required review process and
  relevant tests; required checks are successful and no applicable Copilot or
  reviewer finding, correctness issue or security blocker remains unresolved.
- Any intended product/API decision is already settled; low stars do not
  authorize unrelated behavior changes.
- Refresh the PR head, check/review state and star count at the point of merge,
  and bind the merge request to that reviewed head (for example with
  `gh pr merge --match-head-commit`). If the head changed, revalidate it first.

A pull request reporting a mergeable state of blocked with no review decision is
usually waiting on a required approving review, not on a failing check. Read the
default branch's protection settings to see what it actually requires: the
number of required approving reviews and the list of required status checks are
separate, and a repository can require a review while requiring no checks at
all. When an approval is what is missing and review plus relevant validation
support it, submitting the evidence-backed approval is an authorized action that
unblocks the item; do not report a required review as an external blocker when
the patrol can satisfy it. Note that this applies to merge eligibility under the
gate above, not to repositories at or above the star threshold, where the final
merge still belongs to the user.

A review approval is attached to the commit it was submitted against, so a
later push leaves that approval pointing at a superseded head. When reporting an
item as ready, check each approving review's commit against the current head
rather than only counting approvals: a pull request that shows an approval and a
green check set may still have no review covering the revision that would merge.
Say which revision the approval covers when it is not the head, and treat the
item as awaiting re-review rather than as ready.

Use a repository-supported merge method without bypassing branch protection.
If the star count or required evidence is unavailable, preserve the item for
follow-up rather than guessing. Use the agent's immediate merge after these
gates; do not enable deferred GitHub auto-merge or enqueue it in a merge queue,
where the head or star count could change after the authorization check.
Verify the resulting merged state and record its commit and PR link. Never
delete the contributor branch as part of this action.

This replaces both the earlier all-manual-merge rule and the old named
ActPlane/wasm-bpf exceptions: every in-scope repository uses the same threshold.
All patrol-authored public reviews and replies retain the disclosure footer.

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

- Merge a PR whose target repository has 500 or more stars, or merge without
  satisfying the live-star policy above. Never enable deferred auto-merge or
  enqueue a PR in a merge queue.
- Publish a release.
- Close an issue or pull request.
- Delete a branch.
- Change access permissions, organization or repository settings, branch
  protection, secrets, webhooks, or deployment configuration.
- Write outside `eunomia-bpf` except for focused commits to the exact writable
  contributor PR branch allowed above.
- Expose credentials, tokens, private logs, or sensitive environment details in
  GitHub content, commits, branch names, pull request text, or reports.

## Report and Persist

Write a concise, actionable Chinese report that includes:

- total open items discovered and total actionable items;
- actual public replies;
- fixes and newly opened pull requests;
- updated pull requests and verified merges;
- tracked items with no new public action;
- items blocked by a reporter, runner, reviewer, maintainer, CI or
  infrastructure, or the task itself;
- exact links for every important item.

For each important item, state the repository, item type, classification,
current status, action taken, next step, and blocking party. Label any item that
was discovered but not handled as `发现但未处理` and explain why. Never present
discovery as completed work.

Update local automation memory with the minimum deduplication and follow-up
state plus the run summary. Do not commit or publish the memory.
