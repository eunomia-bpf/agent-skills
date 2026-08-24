# Agent Skills

Agent Skills is the public, versioned source for reusable maintainer workflows
and organization-level Eunomia community maintenance. Each skill is
self-contained under `skills/<skill-name>/` and starts with a `SKILL.md` file.

## Collections

The general-purpose workflows cover the full open-source lifecycle:

- `agent-cli-tools`
- `gh-workflow`
- `oss-change-workflow`
- `oss-issue-triage`
- `oss-release-readiness`
- `project-bootstrap-workflow`

The Eunomia organization-level workflow is:

- `eunomia-community-patrol`

Skills tied to one consuming repository's content tree, publishing ledger,
site paths, SEO operation, or research workflow remain in that repository and
are intentionally not collected here.

## Install With Symbolic Links

Clone this repository, then link its skills into the agent's skill directory.
The linker refuses to overwrite a real file or directory.

PowerShell:

```powershell
pwsh -File scripts/link-skills.ps1 -TargetDirectory "$env:USERPROFILE\.codex\skills"
```

Bash:

```bash
./scripts/link-skills.sh "$HOME/.codex/skills"
```

On Windows, the PowerShell linker first attempts a symbolic link and falls back
to a directory junction when Developer Mode or elevation is unavailable. Both
forms keep one canonical copy of each skill. Repository consumers can keep this
repository as a submodule and run their own wrapper around the same linker.

## Validate

Use Codex's `skill-creator` validator on every skill:

```bash
python /path/to/skill-creator/scripts/quick_validate.py skills/<skill-name>
```

The repository intentionally contains only skills, their required resources,
the linking helpers, and maintainer guidance.
