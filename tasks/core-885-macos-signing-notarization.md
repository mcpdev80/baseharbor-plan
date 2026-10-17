---
id: core-885
areas: [platform]
type: feature
release: backlog
version: ""
parent: core-818
owner: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#885"]
source_updated: "2026-10-15T16:49:12Z"
labels: [kind/feature, area/compatibility, area/artifacts, status/backlog]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-885 · macOS: signing and notarization #task #release/backlog #status/backlog #view/backlog #area/platform #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** backlog  
**Release:** [backlog](../releases/backlog.md)  
**Parent:** [core-818](../epics/core-818-host-platforms.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#885](https://github.com/mcpdev80/baseharbor/issues/885)
<!-- /generated:links -->

## Goal



## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

Parent: #818 · **Follow-up, not part of v0.4.29 #876**

### Context

v0.4.29 ships darwin arm64/amd64 artifacts **without notarization** (decision 2026-10-14, #876/#822):

- Go ad-hoc signs darwin/arm64 binaries at link time, so they run.
- The curl/Go-HTTP installation/update path must be qualified on a clean supported Mac, including actual quarantine/Gatekeeper behavior and checksum/provenance checks. Absence of a quarantine attribute is not publisher identity or a universal guarantee of execution.
- Qualify browser-downloaded artifact behavior separately and document observed Gatekeeper warnings/restrictions. v0.4.29 documents the qualified installer path and its unsigned/not-notarized distribution limits.

### Scope

- Apple Developer Program membership and a Developer ID Application certificate owned by the project.
- Release workflow: codesign with the hardened runtime, `notarytool submit --wait` and record the notarization result in the release evidence. Bare CLI binaries in a tar.gz cannot be stapled, so check whether a signed `.pkg`/zip distribution is needed.
- Secrets handling in `release.yml` without exposing signing material in logs or artifacts.
- Verify with `spctl --assess` and `codesign --verify --strict` on a clean Mac.
- Optional: Homebrew tap (separate decision).

## Acceptance

- Browser-downloaded darwin artifact runs without a Gatekeeper override.
- Signing and notarization evidence is part of the release receipt.
- No signing secret leaks into logs or artifacts.

## Required checks

- To be defined when scheduled.

## Dependencies and file ownership

- Unscheduled (`status/backlog`). Referenced source issues: none.

## Handoff

- Not scheduled.
