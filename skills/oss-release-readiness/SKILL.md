---
name: oss-release-readiness
description: Audit or prepare an open-source release. Use when checking whether a repo is ready to tag, publish, cut a GitHub release, update changelog/release notes, bump versions, publish packages, document breaking changes, or verify release smoke tests and provenance. Do not use for ordinary feature/bug implementation, issue triage, or paper prose review.
---

# OSS Release Readiness

Use this skill to decide whether a repository is ready to release and what blocks the release. Default to inline audit mode. Preserve unrelated dirty worktree state. Do not tag, publish packages, edit changelogs, or create GitHub releases unless the user explicitly asks.

## First Step

Read the repository's release contract:

- `README`, `CONTRIBUTING`, release docs, maintainer notes, or CI release workflow;
- package manifests and version files;
- changelog or release-note convention;
- recent commits, merged PRs, or user-provided change list;
- test, build, packaging, and smoke-test entrypoints.

If no release contract exists, report that as a blocker and infer the smallest safe checklist from the package ecosystem.

Use the repository's documented test, build, and release entrypoints. Do not bypass them with direct tool commands.

## Release Scope

Classify the release as:

- patch: bug/security/docs-compatible fix;
- minor: backward-compatible feature;
- major: breaking change, migration, or public contract change;
- prerelease/nightly: explicitly unstable preview.

If versioning policy conflicts with SemVer or ecosystem norms, follow the repository's policy and state the mismatch.

## Readiness Checklist

Check:

- version bump is consistent across manifests, lockfiles, docs, and generated metadata;
- changelog/release notes summarize user-visible changes, fixes, breaking changes, and migration notes;
- public APIs, CLI flags, config files, schemas, examples, and docs are synchronized;
- CI is green or known failures are explained;
- package/build artifacts are reproducible enough for the repo's standard;
- dependency or security updates are called out when relevant;
- release smoke tests cover install/import/run paths for the supported platform matrix;
- tags, package names, registry targets, and GitHub release title/body match the version.

After publishing (when the user asks to execute the release), the release is not done until a post-release live smoke passes: install the artifact from the public registry/release page (not the local build), run it, and fetch any deployed site/docs URL to confirm the new version is actually served (mind CDN caches). Report the evidence with the completion claim.

Do not require heavyweight process for small internal prereleases, but do not skip user-visible compatibility checks.

## Blocking Rules

Block release when:

- the version cannot be determined;
- tests or package builds fail without an accepted exception;
- breaking changes lack migration notes;
- docs/examples contradict released behavior;
- generated files or lockfiles are stale where the repo expects them;
- package publishing target is ambiguous;
- security-sensitive changes lack maintainer review.

## Output Shape

Return:

1. release type and proposed version,
2. readiness verdict: ready / blocked / conditional,
3. blockers,
4. release-note/changelog items,
5. validation status,
6. exact next action.
