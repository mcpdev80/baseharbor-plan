---
id: t-20261018-r27-authority-contract
card_number: "0427-016"
card_short_title: "define one installation owner"
areas: [architecture]
type: architecture
release: v0.4.27
version: ""
parent: core-777
priority: critical
owner: w1-authority (lane)
kanban_lane: closed
kanban_summary: Define installation identity versus management connection versus Target; one authoritative state/lock owner per managed…
kanban_status: closed
kanban_title: "0427-016 · define one installation owner"
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1348"]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/review-1326k.md","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/merge-1348.md"]
---

- [x] t-20261018-r27-authority-contract · Authority: define one installation owner for local and remote work #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/architecture #kind/architecture
    <!-- generated:card -->
    **Owner:** w1-authority (lane) · **Priority:** critical  
    **PR:** [baseharbor#1348](https://github.com/mcpdev80/baseharbor/pull/1348)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/review-1326k.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-night-2026-11-02/merge-1348.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261018-r27-candidate-contract](t-20261018-r27-candidate-contract.md), [t-20261018-r27-connection-client](t-20261018-r27-connection-client.md), [t-20261018-r27-delivery-boundary](t-20261018-r27-delivery-boundary.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261018-r27-execution-journal](t-20261018-r27-execution-journal.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md), [t-20261018-r27-state-owner](t-20261018-r27-state-owner.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Owner:** w1-authority (lane)  
**Priority:** critical  
**PRs:** [baseharbor#1348](https://github.com/mcpdev80/baseharbor/pull/1348)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Define installation identity versus management connection versus Target; one authoritative state/lock owner per managed deployment. Local direct execution uses the same semantic core without mandatory login/server or SQL/Secrets/Identity bundle. Remote clients never own authoritative state or fall back locally. Specify accepted revision/consent, observed-at freshness and independent security boundaries. Deliver minimal callable selection/authority types for downstream owners, not a new framework.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

docs/spec/target-access-v1.md; docs/spec/control-plane-runtime.md; corresponding DE specs; one new ADR; bounded internal/coreinstallation management-selection types and tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

> Coordinator authorization 2026-11-02 (night): shared-write update per final sentence —
> extraction of lock primitives into `internal/stableid` is permitted for cycle-breaking
> `coreinstallation -> serviceaccess` consumption, ONLY if zero `serviceaccess` files change
> and behavior is preserved; documented in task evidence r27-night-2026-11-02.
>
> **Ownership / cycle-break recorded (fix round, 2026-11-02):** The permitted write set is
> `internal/coreinstallation` only. The real production authority boundary is
> `serviceaccess.Issuer` (issuer reference = identity, revocation = foreign rejection,
> `ExpiresAt` = freshness); the candidate's self-contained `RemoteAuthority` was never
> consumed. A Go import cycle forced a minimal, acyclic break: the lifecycle-lock
> primitives moved from `internal/coreinstallation` to the stdlib-only leaf
> `internal/stableid` (new `internal/stableid/lock.go` + `lock_test.go`;
> `serviceaccess/local_issuer.go` re-imports `stableid`; `coreinstallation` re-exports the
> lock with unchanged signatures). Verified: `go build ./...`, focused authority-type tests,
> `internal/stableid` lock tests, `go vet`, `mkdocs-en-de-strict`, `documentation-audit`,
> `pages-candidate-build` all pass. Zero `serviceaccess` files changed beyond the import swap
> (no logic edit). This is the documented, coordinator-authorized dependency/ownership
> update; no other shared index/registration was touched.

## Required checks

Existing docs/link/EN-DE checks and focused authority-type tests; no native runtime. Use existing trusted contract/docs/package checks for this prerequisite; acceptance must not wait on downstream ci-lanes. Any genuinely missing contract-check route is resolved explicitly before assignment, without self-exemption. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

### Coordinator ownership decision (2026-11-03, night wave, per card rule)

The accepted predecessor interfaces named in this card (serviceaccess.Issuer identity/revocation,
ExpiresAt as the single freshness bound) ARE in-scope integration points: the lane may make minimal
glue/integration edits in internal/serviceaccess for authority wiring only; all other files there
remain read-only. Freshness policy per card: observation is fresh iff now <= Issuer ExpiresAt
(no additional maxAge constant; zero/future now fails closed). Recorded for review traceability.

### Coordinator ownership decision on composition wiring (2026-11-03, night wave)

The production authority/selection boundary is composed at cmd/baha/application_service_issuer.go
(exists on develop). The lane MAY make a MINIMAL wiring edit in that single file to bind the accepted
serviceaccess.Issuer into coreinstallation authority via the new internal/installauthority leaf interface.
No other cmd/baha files; no new cmd/baha files; coreinstallation imports only leaf packages (acyclic).
Recorded per card rule update dependencies/ownership before work.

### Coordinator revocation-authority decision (2026-11-03, night wave, r1326b2)

No read-only revocation predicate exists on accepted develop surfaces (LocalIssuer.revocations is
private; only Revoke mutates). The lane MAY add a minimal read-only method to serviceaccess.LocalIssuer
(e.g. Revoked(serial) bool, reusing the private revocations loader, NO state change) as authorized glue
per the existing composition/ownership notes, expose it through the installauthority interface, and use
it in FreshlyObservedConnection. Mutating Revoke must NOT appear on any verification path; regression
test asserts revocations.pem bytes unchanged across successful verification. Index navigation entries
for ADR 0021 are permitted (navigation-only, public-surfaces note acknowledged).

### Coordinator ownership extension for revocation predicate (2026-11-03, night wave, r3)

To make verification read-only the lane additionally touched internal/openbao/service_issuer.go
and service_pki.go (Revoked predicate on the openbao issuer, mirroring the LocalIssuer method),
internal/serviceaccess/issuer.go (interface), and internal/testsupport/serviceissuer (fake with the
method). These are accepted-boundary glue per the composition-wiring note; no behavior other than
exposing revocation STATUS (no writes) may live there. Recorded before review.

### Coordinator decision on production-selection wiring depth (2026-11-03, night wave, r1326c2)

Punkt 2/3 production call-site wiring across the seven cmd/baha resolvers is DEFERRED to the
consumer seam cards (t-20261018-r27-state-owner owns the deployment Load/Save seams; app-level
mutation-phase Issue() side effects are explicitly out of contract scope for verification paths).
THIS card must deliver: fail-closed revocation/observation predicates (no error path may yield
'valid'), the installauthority boundary itself with production-shape tests through its own real
functions, ObservedAt freshness inside Fresh, and EN/DE docs stating the wiring deferral with the
named cards. resolveManagementConnectionIssuer stays as the documented integration point that
consumers call; a test demonstrating it end-to-end is required, a cmd-side call fan-out is not.

### Coordinator decision confirming w8-authority-r4 delivery (2026-11-03, night wave, r4)

w8-authority-r4 delivered: tri-state read-only revocation (`RevokedStatus(ctx, serial) (bool,
error)`) on `serviceaccess.LocalIssuer`, `openbao.ServiceIssuer` and the test fake;
`installauthority.Fresh` rejects on `err != nil || revoked == true` so an unreadable/missing/
malformed revocation status fails closed; `observedAt` freshness inside `Fresh` (zero/future/
stale); end-to-end test through `resolveManagementConnectionIssuer` itself (`TestResolveManage mentConnectionIssuerEndToEnd`) proving live pass plus revoked and unreadable-CRL fail-closed via the
authorized wrapper only. `observedThroughBoundary` no longer issues a leaf (no `Issue()` on the
verification path) — it observes the existing connection through `BaseSerial`/`BaseExpiry`. EN/DE
`target-access-v1.md` state the call-site fan-out deferral to the state-owner lane. Only the
authorized `cmd/baha/application_service_issuer.go` (+ its test) changed among cmd files.

### Coordinator note on identity cross-binding deferral (2026-11-03, review-1326f)

The card contract line (serviceaccess.Issuer: issuer reference = identity, revocation =
foreign rejection, ExpiresAt = freshness) does NOT include same-target identity cross-binding
against an independently stored selection value; that check is deferred to the state-owner
authority seams (installation-ID binding note on t-20261018-r27-state-owner, 2026-11-03).
Expiry checking itself is REQUIRED on this card and is not deferred.

### Coordinator acceptance note (2026-11-03, r1326k)

CODEX-REVIEW verdict on head cf95e6e1: **ACCEPT-WITH-DEFERRAL** (evidence/r27-night-2026-11-02/review-1326k.md).
Deferrals: independent CA/installation cross-binding -> state-owner seams (note 2026-11-03 there);
authority call-site fan-out -> consumer surfaces. Merge via CODEX-MERGE in flight.
