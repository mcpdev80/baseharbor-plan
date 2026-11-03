---
id: t-20261018-r27-profile-contract
areas: [access]
type: architecture
release: v0.4.27
version: ""
parent: core-777
priority: critical
owner: codeman-coordinator (w1-profile lane)
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-profile-contract · Access: define portable connection and device profile records #task #release/v0-4-27 #status/active #view/active #area/access #kind/architecture
    <!-- generated:card -->
    **Owner:** codeman-coordinator (w1-profile lane) · **Priority:** critical  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-device-enrollment](t-20261018-r27-device-enrollment.md), [t-20261018-r27-native-auth](t-20261018-r27-native-auth.md), [t-20261018-r27-profile-codec](t-20261018-r27-profile-codec.md), [t-20261018-r27-team-auth](t-20261018-r27-team-auth.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Owner:** codeman-coordinator (w1-profile lane)  
**Priority:** critical  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Define non-secret profile versus sensitive one-use device enrollment versus explicitly encrypted local-credential export. Pin installation identity/trust/recipient/scope/expiry; import grants no rights, cannot run plugins or redirect credentials. Document native Git/SSH/kube/cloud reuse; session-only versus protected durable storage and DR separation. Publish minimal profile/credential-source interfaces and golden fixtures; no provider implementations.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

docs/spec/credential-access-v1.md and DE counterpart; bounded versioned connection/profile records and fixtures under contracts/managementaccess/v1/. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Schema/golden/negative fixture tests and focused docs/EN-DE checks. Use existing trusted contract/docs/package checks for this prerequisite; acceptance must not wait on downstream ci-lanes. Any genuinely missing contract-check route is resolved explicitly before assignment, without self-exemption. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Night lane `w1-profile` (t-20261018-r27-profile-contract) claimed 2026-11-02 and implemented the portable management-access contract. Candidate PR #1324 `work/r27-profile-contract` @ `7eaec1a5ae51ca8126a4aad6f46c2088acae4b5f`, base `develop`. Output: `contracts/managementaccess/v1/{profile.schema.json, interfaces.md, profile.golden.json, profile_test.go}` + `docs/de/spec/credential-access-v1.md`. Positive/negative regression tests pass locally (`go test ./contracts/` ok, `go build`/`go vet` rc=0). Import grants no rights / cannot run plugins / cannot redirect credentials is schema- and test-enforced. No provider implementations, no CI/register files, shared indexes untouched. Open PR awaiting Maintainer acceptance — no merge/release/tag. Evidence: `baseharbor-plan/evidence/r27-night-2026-11-02/profile-contract/evidence.md`.

---

### l3-profile-fold lane hand (2026-11-03, worker)

One-off doc-fold lane folded `docs/(de)/spec/management-access-profiles-v1.md` into the reserved
`docs/(de)/spec/credential-access-v1.md` (EN + DE), deleted the two orphaned sources, ran
`go build ./...` / `go test ./contracts/managementaccess/v1` / full `documentation-audit.sh` — all PASS.
Local commit `8b01eda5`, verified.

**Blocker for THIS lane (not a product block):** after pushing `8b01eda5`, the shared
`work/r27-profile-contract` ref moved under another lane — remote HEAD is now `0db72d35`
"docs: restore credential profile example parity", which resolves the exact same
`documentation-audit` EN/DE integrity findings I was fixing. Because the branch is a shared PR
candidate I must NOT force-push/rewrite history; the audit gate is already green on `0db72d35`.

Terminal state: `8b01eda5` (fold) + `0db72d35` (audit-parity) + `e57ecf89` (l7-profile-r5: export-per-kind schema + EnrollDevice device-enrollment entry, closes review-1324e OPEN items) → PR #1324
`work/r27-profile-contract` @ `e57ecf89a3a0dbbac8a691a0c01b6e866789faa6`, base `develop`. No merge/release/tag. Evidence: `baseharbor-plan/evidence/r27-night-2026-11-02/profile-contract/fix-r5.md`.

### Coordinator scope decision on finding 2 (2026-11-03, night wave)

Integrated enforcement entry: bind validation to the EXISTING accepted surfaces on develop
(internal/serviceaccess issuer identity/trust + ExpiresAt, contracts/connection-profile surfaces already
in tree). Any genuinely absent predecessor interface must be named in the spec (EN/DE) as an explicit
deferred dependency with a follow-up card reference; silent claims of enforcement are forbidden. This
keeps the contract slice closeable while the full production consumer lands with its own card.

### Coordinator scope decision on profile integration depth (2026-11-03, night wave, r1324f)

IN SCOPE to close now: real AEAD nonce spec (document actual base64url(32B) or agreed value)
consistent across schema/EN/DE/fixtures; rename/fix the truly-absent-export test; bind Go
ValidateKindEnforcement to the schema whitelist; side-effect-witness tests for import effects
(no grants, no plugin, no redirect) using local fakes; align DE to EN (remove stale targetsession
assertion, same nonce wording). DEFERRED with named follow-up cards (NOT silent): independent
anchor + installation/scope binding and the production consumer entry depend on
t-20261018-r27-authority-contract + t-20261018-r27-state-owner (unaccepted, same files) — the spec
must state this as required-but-enforced-later, removing any claim the profile path verifies them now.
This is a documented deferral; misleading present-tense claims must still be corrected in this round.
