# fix-3 — 0428-119 equalRegistry content hardening (hopf on delivered head 184eefde)

Card: t-20261118-ownership-stale-consent-hardening (0428-119), PR #1690,
branch lane-0428-119-consent-hard. Rolle: worker, content fix from an
independent review. Prior session (80aa0bf4) delivered the hopf round and was
released; handoff to this lane, same branch, same right.

## PLAN

- 1. Reality check: `git ls-remote` (develop = 558dc42d0, target head 184eefde), confirm no overlap with running lanes #1599/#1684/#1693 (confirmed, mission witness).
- 2. Recover correct working state: local branch was stale (cut from the repo's initial commit aa0a91ea2, diverged from delivered 184eefde). Reset lane-0428-119-consent-hard to delivered remote head 184eefde; remove foreign untracked scratch from a dead lane (0428-121/122 env-filter files + prune-*/trace-* dirs — not mine, not card 119).
- 3. Confirm the defect: `provider_consent_authority.go:432 equalRegistry` compares only `len(Instances)` and `len(Bindings)`. Read `capability.Registry` (registry.go:55-59: Version, Instances []ProviderInstance, Bindings []ProviderBinding), `ProviderInstance` (registry.go:33-46: id, provider_id, provider_version, provider_protocol, Provider{kind,capabilities}, scope, sharing_boundary, ownership, owner_application_id) and `ProviderBinding` (registry.go:48-53: application_id, resource{kind,name,provider,application}, environment, provider_instance_id) to key identity.
- 4. Implement content-equal `equalRegistry`: keyset compare Instances (id + provider_id + provider_version + provider_protocol + Provider{kind} + capabilities + scope + sharing_boundary + ownership + owner_application_id) and Bindings (application_id + resource{kind,name} + environment + provider_instance_id), order-independent; empty/empty equal, empty/non-empty unequal. Added helpers equalInstanceSet, equalBindingSet, sameProviderInstanceAuthority, sameBindingAuthority, findInstanceIndex, findBindingIndex, bindingKey, equalProviderCapabilities.
- 5. Regression tests in `provider_consent_oscillation_test.go` (positive: same content different order => equivalent, no false oscillation; blockend: same COUNT different content => NOT equivalent + following request FAIL-CLOSED; binding retarget blockend; boundary: empty vs empty => equal, empty vs instance => not equal).
- 6. Monotonic merge-hopf onto the delivered hopf head 184eefde (no rebase/reset/force). Proven: `git merge-base --is-ancestor 184eefde HEAD` = 0 (monotonic on delivered branch); 184eefde's base 1019190d8 is an ancestor of current develop 558dc42d0; only my own commit in `origin/lane-0428-119-consent-hard..HEAD`.
- 7. Focused checks: `go build ./...`, `go vet ./internal/application`, `go test ./internal/application -count=1 -run "^Test(ProviderConsent|ConsentAuthority|EqualRegistry|ProviderChange|ConsentOscillation)"`, `bash scripts/ci-fast-check.sh`. No full ./... CI loop.
- 8. Push draft=false; run ONE exact-head CI to terminal; read conclusion + cell lines. Runtime gates SKIPPED (owner-draht 114(a): ORAS-install missing in the PR job, docker-runtime-acceptance.yml :174-330 vs :127-128). Did NOT edit .github/**.
- 9. Write this akte.
- 10. Publish evidence to origin/main; set card BLOCKED with content + limiter reason; host bowl-clean; post END.

## repo-rule compliance

- Exactly one candidate per chain: worked on the named branch lane-0428-119-consent-hard; no second branch invented. No merge by me (card stays BLOCKED).
- No edits to .github/** or scripts/** (Owner scope). The runtime-gate skip is reported as STATE (below), not fixed.
- No subagents (§4.8): every step executed inside this session.
- Write-set: only the two card-119 files touched (provider_consent_authority.go, provider_consent_oscillation_test.go). Foreign untracked scratch removed from the shared worktree; no other lane's work touched, no foreign perses/proto/bh-local-shared objects touched.
- Evidence lives only in baseharbor-plan (this file). Nothing evidence-related committed to a product repo. No .evidence/ dir, no main-branch writes in the product repo.
- Workspace layout: worktree under the baseharbor repo worktree; no scratch/extract in the ecosystem root.

## Fund (finding) with file:line

- `internal/application/provider_consent_authority.go:432` `func equalRegistry(a, b capability.Registry) bool` compared only `len(a.Instances) != len(b.Instances)` and `len(a.Bindings) != len(b.Bindings)`.
- Called from `internal/application/provider_consent_authority.go:385` inside `ConsentAuthority.Equivalent`.
- Consequence: a provider change that keeps the same number of instances/bindings but swaps the instance, retargets a binding, or retitles the version/scope/readiness of a same-id instance read as KONSENT-AEQUIVALENT and passes the fail-closed stale-impact-consent gate — exactly the stale-entry hole card 0428-119 closes.

## New tests (provider_consent_oscillation_test.go)

- `TestEqualRegistryPositiveSameContentDifferentOrder`: identical two-instance content in opposite slice order => equivalent (and reverse order); no false-positive oscillation.
- `TestEqualRegistryBlockendSameCountDifferentContent`: same COUNT, different instance id / different provider_version / different scope => NOT equivalent. The actual befund: the old length-only code passed all three.
- `TestEqualRegistryBlockendBindingRetarget`: same count, binding retargeted to another provider instance => NOT equivalent.
- `TestEqualRegistryBoundaryEmpty`: empty vs empty => equivalent; empty vs one instance => NOT equivalent (symmetry).
- `TestEqualRegistryFailClosedRevalidation` (end-to-end): two plans whose only registry difference is a same-count/different-content instance swap => `ProviderImpactPlansConsentEquivalent` == false AND `ValidateProviderImpactRevalidation` fails closed with `ProviderChangeError{Code: "stale-impact-consent"}`.

## CI run (exact head, terminal)

- Head: 9bb20658354e285024733549e9f938edb031098c (my commit 9bb206583, `fix(0428-119 r4): equalRegistry compares registry content, not just counts`).
- PR #1690 head = 9bb206583.
- Run id: 135806340546 (PR · Go unit · owner); check-runs endpoint for 9bb20658354e285024733549e9f938edb031098c.
- Timestamp (commit): 2026-11-19 19:57:33 +0100.
- Reference timestamp `git show -s --format=%cI origin/develop` = 2026-11-19T18:55:20+01:00.
- REQUIRED jobs, actually executed, terminal = success: PR Selected Checks, Go unit · owner, cli-0, cli-1, cli-2, cli-3, packages, Validation · go-build, Validation · go-vet, Focused Python, Source format, Native gate plan, Trusted Plan, Workflow policy (14 success).
- SKIPPED (20): all runtime gates — Targeted HA · docker, Targeted HA · podman, Selected Runtime, Native gate (native), Main release checks, etc. Cause is the owner-draht 114(a): the ORAS-install step is missing in the PR job (docker-runtime-acceptance.yml :174-330 vs :127-128). This is NOT my failure; I did not and must not edit .github/**.
- No required job is SKIPPED or queued — all required jobs ran to completion with success. The runtime gates are genuinely skipped by CI policy, documented as STATE.

## Card state after this hopf

Card stays BLOCKED, with BOTH reasons in one line:
- content: `equalRegistry` compares only counts (provider_consent_authority.go:432) — BEHOBEN (content now keyset by id+identity; regression suites positive/blockend/boundary/fail-closed).
- limiter: runtime-gates SKIPPED (owner-draht 114(a), ORAS-install missing in PR job) — runtime side can only be belegt when that draht lands or the owner sets acceptance without it.
This is NOT `review`: the runtime side is not yet belegbar. No acceptance by me; owner-ZWEIFEL ("kein abnahme-freiraum fuer unit gruen + runtime-versuch rot") remains in force.

## Host cleanliness (before / after)

- No docker/podman compose projects started this hopf. No containers/volumes/networks/state created.
- before: none. after: none.
- cleanliness: clean. Foreign untracked scratch (0428-121/122 env-filter files + prune-*/trace-* dirs) was a dead-lane residue in the shared baseharbor worktree, not mine — removed to unblock the checkout; no other lane's tracked work or foreign objects touched.

## Evidence provenance

- baseharbor-plan evidence ONLY: evidence/r28-welle4-2026-11-19/consent-hardening-hopf/fix-3.md.
- origin/main provenance for evidence commit: `git remote -l` + exact output pasted in the handoff END line.
