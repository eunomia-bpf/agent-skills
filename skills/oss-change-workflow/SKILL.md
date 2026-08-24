---
name: oss-change-workflow
description: Maintainer-quality workflow for open-source code, documentation, examples, feature requests, bug fixes, regressions, compatibility fixes, or issue-backed patches. Use when changing an OSS repository and the task needs scope control, validation, docs/changelog sync, maturity-aware commit/push or PR handoff, monitored CI closure, and review-comment closure. Pure content changes use a lightweight self-review path; mature-project changes that touch code, behavior, tests, tooling, configuration, dependencies, builds, or runnable examples use mandatory subagent and independent cross-agent-tool review. Do not use for issue triage without repository changes, release preparation, or standalone GitHub CI debugging.
---

# OSS Change Workflow

Use this skill to make an OSS repository change look like a maintainer would accept it. It complements GitHub PR/CI tools; it does not replace them.

## Default Mode

Implement the requested change unless the user asks for analysis only. After validation, use the project maturity policy to decide whether to direct-push or use a PR.

Do not merge branches or PRs, force-push, tag releases, publish packages, write changelog entries, or create report files unless the user explicitly asks.

## Project Maturity And Branch Policy

Start new work from the repository default branch, `main` or `master`, unless the user names another branch, but do not treat this as permission to switch away from an active checkout. Before any branch, worktree, stash, rebase, reset, or commit operation, run `git status --short --branch`, identify the current branch, upstream state, dirty tracked files, and untracked files, then decide whether moving branches is safe.

When the worktree contains uncommitted changes, untracked files, or signs of another person or agent working in parallel, preserve that state in place. Continue on the current branch if it matches the requested task. If the task needs a different base, ask first or create an explicitly requested separate worktree; do not silently switch branches, stash, reset, or move someone else's work to make the workspace look clean.

Treat a repository as mature only when the user says it is mature or it is one of: `bpftime`, `eunomia-bpf`, `wasmbpf`, `agentsight`, or `tutorial`. Treat all other repositories as immature by default.

- Immature projects: work directly on `main` or `master`, then commit and push. Do not open a PR, wait for CI, or run release workflow steps unless the user asks or repository protection requires it.
- Mature projects: use `main` or `master` as the base when starting clean work, push a branch, open or update a non-draft PR, and run the PR, review, and CI loop. If work is already in progress on a task branch, keep using that branch unless the user asks to split it or the change clearly belongs elsewhere.
- Name branches for the technical scope using repository conventions or neutral prefixes such as `fix/`, `feat/`, `docs/`, or `chore/`. Never put AI tool, model, assistant, or provider names in branch names.
- Commit step by step: when a step of the task completes and validates, commit it immediately as its own commit with a message naming the step. Fine-grained sequential commits are the audit trail — do not batch a whole session into one commit, and do not leave completed work sitting uncommitted.

On session resume, after a worktree operation, or before any commit, run `git status --short --branch`, confirm the current branch, and compare against upstream. Report the branch state proactively instead of discovering mid-task that work landed on the wrong branch. Stage only the intended files with explicit pathspecs, especially when parallel work left unrelated dirty files in the checkout.

## First Step

Read the local repository contract before editing:

- `README`, `CONTRIBUTING`, `CLAUDE`, or maintainer notes;
- package metadata and test/build configuration;
- issue text, failing logs, or user-provided repro steps;
- relevant nearby tests before implementation.

Use the repository's documented build and test entrypoints. If the repo says to use `make`, a task runner, or a project script, do not bypass it with hidden component commands.

## Classify The Change

Classify the request as one of:

- bug/regression: behavior was expected to work;
- feature: new supported behavior or public surface;
- compatibility: runtime, dependency, platform, version, or packaging change;
- docs/examples: behavior explanation without production code changes;
- refactor: internal structure without behavior change.

If the type is unclear, infer the smallest safe scope and state the assumption.

## Content-Only Lightweight Path

Use this path only when every intended change is limited to authored prose, static documentation content, or doc-only media. Static metadata is content-only only when it does not control routes, navigation, builds, deployment, or runtime behavior. Illustrative code fences may qualify when they are not compiled, executed, or treated as repository examples.

Typical content-only work includes writing or revising blog posts, README prose, documentation pages, and translations when the diff changes only authored content.

A change is not content-only when it touches executable code, tests, scripts, dependencies, generated artifacts, schemas, public APIs, runnable examples, or build, CI, deployment, routing, navigation, or tool configuration. Documentation linked to a code or behavior change follows the full code path.

Content-only work still follows the repository contract, scope and authorization checks, branch policy, paragraph-level editing rules, worktree inspection, relevant validation, PR policy, review-comment handling, and CI monitoring. For a mature-project content-only PR:

- skip the mandatory review subagent and independent cross-agent-tool review;
- perform one focused self-review of the complete diff, checking content preservation, factual support, links, headings, code blocks, navigation references, bilingual consistency when applicable, and accidental path or secret leakage;
- run the smallest relevant docs lint, link check, site build, or preview validation available;
- inspect and resolve review comments that actually exist, including Copilot comments, without invoking extra reviewers solely to satisfy a gate.

If the diff crosses the content-only boundary at any point, switch to the full mature-project review path. Do not add the two independent review gates to content-only work unless the user or repository contract explicitly requires them.

## User Authorization Boundary

- Do not change product behavior, public semantics, supported workflows, architecture, abstraction boundaries, or user-facing documentation unless the user explicitly asked for that change or it is the smallest necessary part of the requested fix.
- Bug fixes are especially narrow: fix the defect while preserving the existing design and documented behavior. Do not use a bug fix as permission to introduce a new abstraction, redesign a subsystem, rename public concepts, change defaults, or rewrite final-user docs.
- If a broader design or documentation change looks beneficial but was not requested, report it as a follow-up option or risk instead of implementing it. Ask before proceeding when the requested fix cannot be made without changing behavior or design.
- Interpret user terms narrowly. If the user says "backend", "monitor", "eBPF", "process snapshot", "live", "plain", "TUI", or similar overloaded terms, identify the concrete subsystem before editing and do not disable adjacent subsystems by implication. For example, "do not use backend/monitor" is not permission to remove lightweight process snapshots, fd inspection, or session/process binding.
- Do not add compatibility flags or mode switches to preserve behavior after an avoidable self-inflicted behavior change. Prefer deleting the wrong abstraction and restoring the existing path. Add a new flag only when the user explicitly asks for a new user-facing mode.
- Before implementation, write a one-sentence scope contract: "This change may touch X; it must not touch Y." Keep the final diff within that contract unless the user approves a revised scope.

## Bug Path

- Reproduce the failure when feasible, or identify the narrowest failing test/log path.
- Add or update a regression test when the repo has a practical test layer.
- Fix the root cause, not only the symptom shown by the repro.
- Preserve existing public behavior unless the issue explicitly asks for a breaking change.
- If reproduction is impossible, make the smallest defensible fix and name the residual uncertainty.

## Feature Path

- Define the public behavior, compatibility expectations, and non-goals before editing.
- Follow existing extension points, naming, configuration style, and error-handling conventions.
- Add tests that prove the new behavior and at least one boundary or failure case when practical.
- Update docs/examples only when the feature changes user-visible behavior.
- Avoid broad refactors unless they are necessary for the feature's minimal implementation.

## Shared Quality Bar

- Keep diffs local to the change.
- Make the smallest code change that solves the issue. Avoid opportunistic refactors, formatting churn, dependency churn, and generated-file churn unless required.
- After the first working implementation, do a reduction pass: remove redundant helpers, collapse unnecessary abstractions, and prefer less code when behavior, readability, and tests stay intact.
- For refactors or design cleanups, treat net code reduction as an explicit goal when the user asks for simplicity. Preserve behavior while continuing to shrink the implementation where possible.
- Do not fix unrelated bugs, even obvious ones, unless the user asks or the bug blocks the requested change. Mention them as residual risks instead.
- You may delete unrelated dead code when it is clearly unreachable/unused and deletion reduces churn or complexity without changing supported behavior.
- Preserve user changes and unrelated dirty worktree state.
- Use the current checkout by default. Do not create a new git worktree unless the user explicitly asks.
- Before committing, inspect the worktree and stage only the intended files.
- Use human commit messages and PR/release text. Never put AI tool, model, assistant, or provider names in commit subjects or bodies, or in PR titles. Do not include AI/tool attribution, generated-by lines, or `Co-authored-by` trailers in PR bodies or release text. Describe the technical change itself instead.
- Prefer existing helper APIs and repository patterns over new abstractions.
- Run the smallest relevant validation first, then broader validation if the blast radius justifies it.
- Do not hide failing tests. Report what failed, what passed, and what was not run.
- If the change affects a public API, CLI, config, file format, migration, or user-facing docs, flag release-note or changelog impact inline.
- For README-style docs, keep Quick Start stable. Do not edit Quick Start unless the primary onboarding command or first-run flow changes; put mode-specific behavior, persistence paths, storage formats, and operational caveats in Usage, FAQ, or dedicated reference docs instead.
- Documentation edits are paragraph-level patches, never whole-file rewrites. After any doc change, diff against the previous version from the end backwards and confirm no existing content was lost; restore anything dropped without an explicit reason.
- Docs and examples must be real. Never fabricate example output, numbers, or "demo" data presented as actual behavior; every README example must be reproducible from a real run, and outputs must be scanned for leaked usernames, private paths, and tokens before publishing.
- Exploration/refactor tasks record a baseline first (diffstat and LOC against upstream main). At the end, split the net-useful change from exploration residue into separate commits or branches; a task that promised code reduction proves it with the final diffstat.
- If the same file or the same class of merge conflict occurs a second time (e.g., vendored binaries), do not just resolve it again — open an issue or propose the root-cause fix. "先这样" is not an accepted resolution twice.

## PR, Review, And CI Loop

- Use this loop for mature projects or repository-enforced PRs. Skip it for immature direct-push work unless the user asks.
- After pushing, create or update a normal PR. Never create a draft PR by default.
- For content-only changes, follow the lightweight path above. For every other mature-project PR, complete both mandatory independent review gates: (1) spawn a dedicated review subagent to inspect the pushed PR or branch, and (2) obtain a separate review through an external agent tool on the same pushed state. The cross-agent reviewer must use a provider or model family independent of the implementation agent. Acceptable reviewers include Claude, Gemini, Grok, Kimi, and OpenCode backed by GLM; Grok or Kimi may also be invoked through OpenCode when that is the configured provider. Do not hard-code Claude as the reviewer for Codex-authored changes. If the user names one reviewer or a set of reviewers, use exactly that choice; otherwise select at least one available independent reviewer. The subagent and cross-agent-tool review must be distinct review passes; one invocation cannot satisfy both gates. Neither reviewer may be the implementation agent, and the task is not complete until both reviewers have no blocking findings on the final pushed head.
- Discover locally available reviewer clients before choosing one (for example `claude`, `gemini`, `grok`, `kimi`, `opencode`, or `codex`) and inspect the installed client's help instead of inventing command-line flags. Run the reviewer in a real read-only/plan mode or an externally enforced read-only sandbox; never use auto-edit, YOLO, or unrestricted write mode for review. If no independent reviewer can be run safely, report the gate as blocked rather than counting another subagent invocation as the cross-agent review.
- Count a cross-agent review only when it returns a complete, auditable final verdict for the exact pushed commit. Progress text, an exit status of zero, truncated output, malformed structured output, or an interim placeholder verdict does not satisfy the gate; rerun with a compatible output mode or report the gate as blocked.
- Every mandatory reviewer prompt must include a code-growth review. Ask the reviewer to inspect the final diffstat and LOC delta, separate production-code growth from test/fixture growth when practical, and state whether the diff size is reasonable for the bug or feature. The reviewer must explicitly answer whether there is test boilerplate or fixture bloat, whether the same behavior could be implemented with less code, and whether the patch violates any user request or project requirement to keep code changes small or net-reducing. If the user asked for minimal code, simplicity, or net code reduction, unexplained LOC growth, avoidable helper proliferation, broad rewrites, or bloated test scaffolding are blocking review findings until reduced or justified with concrete evidence.
- Every mandatory reviewer prompt must also include a targeted scope-boundary review. Ask the reviewer to identify the user's explicit request, list any changed public behavior/defaults/docs/architecture/abstractions, and answer whether each one was explicitly authorized or strictly necessary for the fix. Any unauthorized behavior change, new mode flag, docs rewrite, or abstraction change is a blocker unless the user approves it.
- When running a cross-agent-tool review, do not wrap the invocation in a short timeout or treat early silence as failure. Run it as a long-running process, poll for progress, and wait at least 30 minutes before declaring it unavailable. If an external infrastructure limit or command wrapper kills the reviewer before 30 minutes, that run does not satisfy the review gate; restart it without that limit or explicitly report the gate as blocked.
- For non-content changes, record both independent review results on GitHub as PR reviews or comments. Do not stop on private-only review feedback unless the user explicitly tells you not to publish review notes.
- Non-negotiable Copilot gate: after every PR push, explicitly inspect GitHub Copilot PR reviews, inline review comments, and review threads from GitHub, not only the check summary. Query both PR reviews and pull-request review comments (for example `gh pr view --json reviews,latestReviews,comments` plus `gh api repos/<owner>/<repo>/pulls/<number>/comments`, or equivalent connector calls). Treat every Copilot comment as a required finding: implement the fix when applicable; if a comment is factually inapplicable, post an evidence-backed response and resolve the thread. Do not complete, mark ready, or say "done" unless the final response includes evidence that Copilot comments were checked and that no Copilot thread/comment remains unanswered, unresolved, or applicable.
- Fix actionable findings with the smallest additional diff, then commit and push the fixes. Rerun the relevant validation after every fix. For non-content changes, continue the full independent-review loop; for content-only changes, repeat the focused self-review and recheck existing review threads.
- For non-content changes, track blockers across rounds: keep one numbered blocker list covering subagent, cross-agent-tool, and Copilot findings from the first reviews; each re-review prompt names the unresolved blockers and asks the reviewer to check only those plus the new diff instead of re-reviewing everything. Close a blocker only when re-review confirms the fix, and require both mandatory reviewers to confirm the final pushed head has no blockers.
- If review feedback suggests broader unrelated fixes, do not take them. Either narrow the fix to the requested scope or report the unrelated issue separately.
- Actively monitor GitHub CI after every push with a watch or polling loop until every required check reaches a terminal green state. A one-time status lookup is not monitoring. Do not stop while checks are queued, pending, running, stale, or failing, and do not call CI green when the repository has no required checks.
- If CI fails, inspect logs, fix the cause, commit and push again, then restart CI monitoring and applicable review-comment checks. For non-content changes, also rerun both independent reviewers on the final pushed head. Continue until required CI is green and no applicable review thread remains open.
- Do not merge after approval and green CI unless the user explicitly asks.

## Completion Verification (live acceptance)

"CI is green" is not "done". Before reporting completion:

- Verify at the final-artifact level: if the change deploys a site or docs, fetch the live URL and confirm the new content is actually served (mind CDN caches — check `cache-control`/`age` headers or a cache-busting query, and say so if propagation is pending); if it publishes a binary or package, install and smoke-test the published artifact, not the local build.
- Every completion claim carries its evidence: command output, HTTP status, CI run link, or the published artifact's version string. If a step was not verified, say "pushed, not yet verified live" — never imply verification that did not happen.

## Output Shape

Return:

1. change type and scope,
2. files changed,
3. validation run and result,
4. commit, push, and PR status,
5. review status: for content-only changes, report the focused self-review and existing review-comment status; otherwise report the subagent review, separate independent cross-agent-tool review, and Copilot-comment status with GitHub review/comment links,
6. diff-size result: for content-only changes, report content diffstat and preservation checks; otherwise report code-growth review, production-vs-test growth where practical, whether the size is justified, and any reduction pass performed,
7. monitored CI status and the final green run link,
8. docs/changelog/release-note impact,
9. remaining risks or follow-up.
