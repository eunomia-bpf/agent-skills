---
name: agent-cli-tools
description: "Use when Codex needs to run, compare, authenticate, troubleshoot, or document local command-line AI coding agents: OpenAI Codex CLI, Anthropic Claude Code, Moonshot Kimi Code, xAI Grok Build, or their agent aliases. Trigger for requests about local agent CLI usage, non-interactive prompt calls, login/device-code flows, PATH/version checks, permission modes, or choosing which terminal agent to use."
---

# Agent CLI Tools

This skill documents how to invoke and troubleshoot the supported agent CLIs. It does not define infrastructure policy for containers, mounted directories, credentials, SSH, Docker, networking, or service architecture.

## Start Here

Use the installed command itself as the source of truth before relying on remembered flags:

```powershell
where.exe codex
where.exe claude
where.exe kimi
where.exe grok
codex --help
claude --help
kimi --help
grok --help
```

On Windows, refresh PATH for a new-terminal view when needed:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable('Path','User') + ';' + [Environment]::GetEnvironmentVariable('Path','Machine')
```

Read `references/installation.md` when a command is missing, the user asks how to install/update, authentication is stale, PATH looks wrong, or exact local paths/versions matter.

## Choose The Agent

- Use `codex` for OpenAI Codex local repository work, Codex review, `AGENTS.md`, skills/plugins/MCP, `codex exec` automation, and Codex cloud handoff.
- Use `claude` for Anthropic Claude Code tasks or when the user explicitly wants Claude's coding agent.
- Use `kimi` for Kimi Code agent tasks, Kimi API Platform or Kimi managed login, `kimi web`, `kimi acp`, or Kimi provider experiments.
- Use `grok` or `agent` for xAI Grok Build, Grok model testing, or tasks the user wants routed through Grok.

Prefer the agent the user names. If the request is comparative, run the same small prompt against each logged-in agent and report exact command/output differences.

## Common Workflows

### Validate the local setup

Run versions first, then one tiny prompt:

```powershell
claude --version
kimi --version
grok --version
claude -p "Reply with exactly: ok"
kimi -p "Reply with exactly: ok"
grok -p "Reply with exactly: ok" --no-alt-screen
```

Kimi may print extra session commentary after the model answer. Grok may print non-fatal telemetry warnings after a successful answer. Treat the model answer and exit code as the primary signal.

### Use Codex CLI

If `codex` is installed, start it in the project directory:

```powershell
cd C:\path\to\repo
codex
```

Useful interactive slash commands from the official CLI entrypoint include:

- `/init` to scaffold an `AGENTS.md`.
- `/status` to inspect session configuration.
- `/permissions` to review or change allowed actions.
- `/model` to choose model and reasoning effort.
- `/review` to review changes.

Use non-interactive or workflow-oriented commands only after checking `codex --help` in the current environment:

```powershell
codex exec "Explain the repository structure and stop before editing."
codex resume
codex cloud
codex mcp
codex completion
```

Use `codex --search` when the task depends on current external documentation, and `codex --image` when the first prompt needs visual context.

### Use Claude Code

```powershell
claude
claude -p "Summarize this repository without editing files."
claude auth status
claude auth login
```

Use `claude -p` for one-shot automation. Use the interactive TUI for multi-step code work where command approvals, diffs, and follow-ups matter.

### Use Kimi Code

```powershell
kimi
kimi -p "Summarize this repository without editing files."
kimi doctor
kimi login
kimi provider list
kimi web
kimi acp
```

Use `kimi doctor` before debugging providers or config. Use `kimi login` for the device-code flow.

### Use Grok Build

```powershell
grok
grok -p "Summarize this repository without editing files." --no-alt-screen
grok login --device-code
agent --version
```

`agent.exe` is an alias installed with Grok Build on this machine. This Grok version does not expose `grok auth status`; validate auth with `grok -p "Reply with exactly: ok" --no-alt-screen`.
