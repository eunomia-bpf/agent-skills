# Bootstrap Source Notes

Use these notes as background when deciding how much structure a new project needs. They are not templates to copy wholesale.

## Official Skill Guidance

- Claude Code skills documentation: create a skill when the same checklist or multi-step procedure keeps being repeated; skill bodies load on demand, so detailed background should stay out of global instructions.
  Source: https://code.claude.com/docs/en/skills
- Anthropic skill authoring best practices: keep skills concise, use progressive disclosure for detailed references, and use conditional workflows for decision-heavy tasks.
  Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Takeaway for this skill: keep `SKILL.md` procedural and short. Put source comparisons here, not in the live workflow.

## Community Bootstrap Patterns

- Better Init focuses on real target-directory detection, inspecting local files before assuming architecture, asking only for missing essentials, concise `CLAUDE.md`, and draft-first setup.
  Source: https://github.com/dddavid4real/Better-Init
- agent-project-bootstrap uses explicit modes such as single-operator, collaboration-repo, and join-existing-project. It shows that bootstrap should be mode-based rather than one universal tree.
  Source: https://github.com/vggg/agent-project-bootstrap
- Project Bootstrap and Guardrails style skills add repo creation, README, `.gitignore`, hooks, secret scanning, and build checks. That is useful for mature or team projects but too heavy as the default for immature experiments.
  Source: https://mcpmarket.com/tools/skills/project-bootstrap-guardrails-5
- Large project-bootstrap suites, such as Clean Architecture generators, can scaffold production-grade stacks with CI/CD and quality tooling. Use these ideas only when the user asks for production readiness.
  Source: https://github.com/levnikolaevich/claude-code-skills
- Curated skill indexes are useful for discovery but not authority. Review candidate skills before importing their rules.
  Source: https://github.com/VoltAgent/awesome-agent-skills

## Local Policy Extracted From These Sources

- Inspect before generating.
- Ask fewer questions, but ask for target directory and first runnable outcome when missing.
- Prefer a working vertical slice over a complete-looking repository.
- Keep `CLAUDE.md` short and project-specific.
- Make production guardrails opt-in for immature projects.
- Do not import third-party skill files into project output without checking license and relevance.
