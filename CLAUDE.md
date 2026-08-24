# Repository Guidance

This public repository is the canonical source for the skills under `skills/`.

- Keep each skill self-contained at `skills/<skill-name>/SKILL.md` with only the
  references, scripts, assets, and UI metadata it actually needs.
- Preserve skill behavior during mechanical moves or packaging changes. Make
  semantic changes only when the task explicitly requests them.
- Keep credentials, account identifiers, private strategy, local workspace
  identifiers, and private conversation content out of this repository.
- Keep consuming-repository-specific content, publishing, SEO, and research
  skills in their owning repository instead of adding them here.
- Keep the link scripts cross-platform and fail safely instead of overwriting a
  real target directory.
- Validate every changed skill with the `skill-creator` `quick_validate.py`
  script and run changed helper scripts against a temporary target.

Work directly on `main`. Before committing, inspect the worktree, stage only
the intended paths, and push validated changes directly unless the user
explicitly requests another workflow.
