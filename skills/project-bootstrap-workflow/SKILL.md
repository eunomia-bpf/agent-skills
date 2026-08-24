---
name: project-bootstrap-workflow
description: Bootstrap a lean new project, repository, research prototype, tutorial, demo, paper artifact, OSS library, CLI/tooling repo, or small web/app project. Use when creating a fresh project directory, choosing initial structure, initializing git/GitHub, writing the first README, CLAUDE.md, .gitignore, package/build files, smoke test, or first runnable example. Emphasizes minimal files, main/master direct-push for immature projects, and avoiding premature CI, release, multi-agent, or production scaffolding. Do not use for ordinary feature changes in an existing repo, release preparation, or CI debugging.
---

# Project Bootstrap Workflow

Use this skill to start a project that can run, be understood, and iterate without premature structure. After the first usable commit, use `oss-change-workflow` for normal code changes.

## Default Mode

Treat a new project as immature unless the user explicitly says it is mature. Use the current checkout or target directory; do not create a git worktree unless the user explicitly asks.

Default to direct work on `main` or `master`, then commit and push when a remote exists. Do not open a PR, add CI, add release workflow, or create production guardrails unless the user asks or the repository already enforces them.

Use human commit messages and project text. Do not include AI/tool attribution, generated-by lines, or assistant `Co-authored-by` trailers.

## First Step

Identify the real target directory before writing. Do not assume the whole workspace is the project.

If the target exists, inspect current files first and preserve them. Ask only for missing essentials:

- project name or target directory,
- project type,
- first runnable outcome,
- language or stack if it is not implied,
- license only when the project is meant to be public.

Then define the smallest first milestone: one command, example, page, script, benchmark, or artifact path that proves the project exists.

## Project Type

Classify the bootstrap as one of:

- research prototype: smallest experiment or analysis loop;
- paper artifact: reproducible command, artifact layout, and result path;
- tutorial/demo: first runnable lesson or example;
- OSS library: minimal public API, example, and test;
- CLI/tooling: command entrypoint, help text, and smoke test;
- infra/dev tool: config or automation with dry-run or check mode;
- web/app: first usable screen or flow, not a landing page unless requested.

If type is unclear, choose the smallest reversible structure and state the assumption.

## Minimal File Set

Create only files needed for the first milestone:

- `README.md` with purpose, quick start, current status, and validation command;
- `.gitignore` matched to the actual stack;
- minimal source/example files;
- minimal build, run, or test metadata when the stack requires it;
- one smoke test or verification command when practical.

Create `CLAUDE.md` only when there are project-specific recurring rules worth preserving. Keep it short and path-based; move durable background into focused docs only when the user asks for persistence.

For research prototypes and paper artifacts, do not create arbitrary research-memory files. If the user asks for durable research docs during bootstrap, use only:

- `docs/paper/` for the current paper source and build entrypoint
- `docs/user-instruction.md` for current and timestamped human intent
- `docs/idea-story.md`
- `docs/background-related-work.md`
- `docs/design.md`
- `docs/implementation.md`
- `docs/evaluation.md`

When `auto-research-orchestrator` owns the project, detailed task records live in its timestamped `docs/tmp/<phase>/step-<NNNN>-<timestamp>/` step directories (step report plus owner child files). Otherwise, explicitly useful standalone notes may use a timestamped directory under `docs/tmp/`.

## Avoid By Default

Do not create these unless the user asks, maturity requires them, or the stack cannot function without them:

- `.github/workflows`, release config, changelog, contributing guide, code of conduct;
- Docker, devcontainer, pre-commit hooks, secret scanning hooks;
- ADRs, roadmap files, planning folders, multi-agent coordination folders;
- layered architecture, service abstractions, plugin systems, generated examples;
- large dependency stacks or framework migrations.

## Mature Project Path

If the user marks the new project as mature or production-bound, add only the maturity layer that serves the stated goal: CI, release, packaging, contribution policy, security hooks, or deployment. Prefer adding those after the first runnable milestone works.

For mature repos, hand off ongoing changes to `oss-change-workflow` so PR review and CI rules apply.

## Output Shape

Return:

1. project type and target directory,
2. first runnable milestone,
3. files created or intentionally skipped,
4. validation command and result,
5. git commit/push status,
6. next small iteration.

## References

Read `references/source-notes.md` only when comparing against outside bootstrap practices, explaining why the workflow is lean, or deciding whether a mature-project bootstrap layer is justified.
