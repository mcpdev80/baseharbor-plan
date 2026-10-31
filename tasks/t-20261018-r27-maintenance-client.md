---
id: t-20261018-r27-maintenance-client
areas: [remote]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: normal
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-client-commands, t-20261018-r27-state-recovery, t-20261022-r27-ci-runtime]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-maintenance-client · CLI: submit maintenance operations without workstation path assumptions #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/remote #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** t-20261017-release-0-4-27-updates, [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** t-20261017-release-0-4-27-updates, [t-20261018-r27-client-commands](t-20261018-r27-client-commands.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261018-r27-team-proof](t-20261018-r27-team-proof.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Route update/backup/restore/destroy through the selected authority and existing lifecycle/consent owners. Archive upload/download and secret input references are explicit safe channels; a laptop filename is never interpreted as a server-local path. Preserve secret-safe machine behavior, recovery choices and typed double consent; lost response follows the same durable operation. Preserve existing Git/workspace source-acquisition ownership: a source snapshot is not a Git checkout; update must resolve/submit the intended next candidate, not run fetch against an invented server repository. Capability discovery rejects unsupported native maintenance explicitly; routing alone is not proof of remote backup support. No new backup engine or automatic replay.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

bounded remote-maintenance CLI adapters/tests; existing machine maintenance input records only after agreement with public-surfaces owner. No other task owns these files concurrently; shared command/contract registrations remain with public-surfaces.

## Required checks

Actual CLI->TLS API tests with different local/server filesystem roots, archive transfer integrity, safe secret input, denial/cancel/expiry and lost response; use fixtures, not full backup journeys. No automatic full matrix or self-approved trust exemption.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.
