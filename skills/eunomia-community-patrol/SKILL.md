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
- Do not repeat a public comment without new evidence, a changed blocker, a new
  fix, a validation result, or a clear request for another party.
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
approval result and unfinished follow-up in private continuity state; resume
at the next scheduled run if the current run reaches its execution deadline.
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
Use the configured local OpenCode workers for source implementation and tests;
the coordinator owns communication, dispatch, evidence reconciliation and
continuation. Work in the matching managed project Workspace.

For someone else's PR, preserve its intended behavior and contributor work.
Refresh the current head and coordinate with any active work before pushing
focused, forward-only commits to that exact writable branch. This includes a
fork branch only when it is the head of an open PR targeting `eunomia-bpf`;
it does not authorize unrelated writes in the fork. If the branch is not
writable, prepare and validate the fix on a task-owned branch in the target
repository and open a linked replacement/follow-up PR or provide the patch.
Preserve the original PR and explain the relationship to the contributor.

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
