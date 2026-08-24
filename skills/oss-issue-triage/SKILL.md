---
name: oss-issue-triage
description: Triage open-source GitHub issues, maintainer inbox items, and the user's own outbound PRs to external repositories. Use when classifying issues, drafting maintainer replies, deciding labels/priority/milestones, requesting reproduction details, finding duplicates, deciding close/reopen/escalate, separating bug, feature, support, docs, and security reports, or checking whether the user's PRs to other projects have unanswered maintainer feedback. Do not use when the user asks to implement the fix, prepare a release, or debug CI.
---

# OSS Issue Triage

Use this skill to turn an issue or maintainer inbox item into a clear next action. Default to read-only analysis and draft replies; do not post comments, edit labels, close issues, or create issues unless the user explicitly asks.

## First Step

Read the issue body, title, labels, comments, linked PRs, and repository contribution/security policy if available. If issue data is not local, use the available GitHub tool or ask for the issue link.

Use the repository's own labels and templates when present. Do not invent a new label taxonomy if the repo already has one.

## Classification

Classify the item as:

- bug: supported behavior appears broken;
- regression: recent change broke prior behavior;
- feature: new capability or public surface;
- docs: documentation, examples, tutorials, or website;
- support/question: usage help without confirmed defect;
- duplicate: same root issue already tracked;
- invalid/not planned: outside project scope or unsupported environment;
- security: vulnerability, exploit path, secret leak, or unsafe disclosure.

For ambiguous reports, choose `needs-info` rather than guessing.

## Evidence Standard

For bugs and regressions, look for:

- version, commit, platform, environment, and configuration;
- expected behavior and actual behavior;
- minimal reproduction steps or failing test;
- logs, stack traces, screenshots, or result files;
- whether the behavior is documented or inferred.

For feature requests, look for:

- user problem and concrete use case;
- compatibility and maintenance cost;
- relation to existing extension points;
- narrower alternative or workaround;
- acceptance criteria.

## Maintainer Decisions

- Request a minimal reproduction when the report is plausible but underspecified.
- Mark duplicate only when the same root cause or requested outcome is already tracked.
- Close politely when the issue is unsupported, stale after requested information, or outside scope.
- Escalate security reports out of public triage. Do not request public exploit details; point to the repository's security policy or private channel.
- Do not promise timelines, ownership, or acceptance unless the maintainer has already decided.

## Outbound PR Inbox

The inbox works in both directions. When asked to check outbound PRs (or during any general "check my GitHub" triage):

1. List the user's open PRs to external repositories: `gh search prs --author <user> --state open --archived=false` (exclude own repos).
2. For each, fetch maintainer comments, bot flags, and review states. Rank by: maintainer requested changes and we have not responded — oldest first. A change request older than a few days is the highest-priority item in the whole inbox; a promised fix that was never pushed is a reputation debt.
3. Also surface: spam/quality bot flags, unanswered reviewer suggestions (including Copilot/CI bots), and PRs open with zero response for weeks (consider politely pinging or closing).

Outbound etiquette (check before submitting, audit when reviewing history):

- Rate-limit bulk submissions: no more than 1-2 similar PRs per week to the same family of repos (e.g. awesome-lists); batches of near-identical PRs get flagged as spam publicly.
- Each PR must be customized to the target repo's contribution style, and the diff self-checked to contain ONLY the intended entries — never bundle unrelated additions.
- No marketing absolutes ("the only open-source tool...") in PR titles or descriptions; describe what the project does, neutrally.
- Keep a tracking note of outbound PRs and their follow-up state so promises to maintainers do not silently expire.

## Reply Drafts

Draft concise maintainer replies with:

1. classification,
2. what evidence is missing or sufficient,
3. requested next action,
4. label/priority suggestion,
5. close/reopen/escalation recommendation.

Keep tone neutral and specific. Prefer one concrete request over a checklist of everything that could be useful.

## Output Shape

Return:

1. classification,
2. confidence,
3. evidence summary,
4. suggested labels/priority,
5. maintainer reply draft,
6. next action.
