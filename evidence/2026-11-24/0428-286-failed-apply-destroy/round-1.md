# 0428-286 — Recover failed apply destroy — round 1 (lane w128)

Card: t-20261116-r28-bug-failed-apply-destroy (0428-286), claim: w128 (plan commit e82fc8868).
Branch: `lane-0428-286-failed-apply-destroy` in mcpdev80/baseharbor, cut from develop tip `8bfc76edd90bb54bbe12f31a2c200a1de67bd7b0` (verified via `git ls-remote origin develop` at session start).
PR: https://github.com/mcpdev80/baseharbor/pull/1834

## PLAN

- read mission + card + parallel card 0428-293 (destroy diagnostics)
- overlap-check vs 0428-293 BEFORE writing (result below)
- verify the reported observations in code (goal is user evidence, not proof)
- red-first deterministic regression reproducing the exact ownership error on baseline
- implement smallest causal fix in own worktree
- gofmt / go vet / go build prechecks (non-test) + source-readability-audit
- push, open PR, two hosted runs on the exact head, watch to terminal
- END_DONE with head SHA + run IDs

## Overlap check (mission duty, done before first edit)

Write-set of this candidate: `internal/application/provider_registry_pending.go`,
`cmd/baha/app_core_requirement.go`, new test file. Card 0428-293 (`t-20261116-r28-bug-destroy-diagnostics`)
targets the ERROR MESSAGE side of the same failure: the generic message is produced at
`cmd/baha/app_core_requirement.go:387` (machine.Error construction) and wired at
`cmd/baha/app_destroy_lifecycle.go:253` (Check registration). Neither card is claimed and no
remote branch/PR for 0428-293 exists (checked ls-remote + open PRs).

Decision: this candidate does NOT change any error text, Check wiring or reporting surface
(`app_destroy_lifecycle.go`, `runtime_destroy_report.go` untouched — 0428-293's space stays
clear). It changes the reconciliation BEHAVIOR inside `checkRetainedApplicationProviderOwnership`
so the ownership error stops firing for the never-realized state. The one shared function is
`checkRetainedApplicationProviderOwnership` (called only from `app_destroy_lifecycle.go:254`):
0428-293 needs its error construction, this fix its return path. If 0428-293 starts, it must
rebase over this behavior change; documenting the lead here per mission. No STOP+QUESTION
trigger: the card contracts do not demand the same functions — 0428-293's contract is
per-provider diagnostic output, 0428-286's is destroy reconciliation.

## Verified in code (before declaring the product fix)

1. Apply retains app-scoped provider owners BEFORE realization:
   `cmd/baha/app_apply.go:207` (`application.RetainPendingProviderOwnersAt`) immediately after
   `recordDeploymentBeforeMutation(..., "applying", ...)` (app_apply.go:203), i.e. before
   preflight (app_apply.go:212). The "applying" record is `Source.Kind "incomplete"` with
   applied intent but NO last-applied reference (deployment_record.go:520 leaves it empty when
   `Applied.LastAppliedRef == ""`).
2. Preflight rejection (privileged cadvisor / docker.sock floci →
   `internal/application/workload_security.go:324`, docker-socket case) fails the apply AFTER
   retention; `recordFailedDeployment` (app_apply.go:254) flips the record observed state to
   "failed" → `app list` reconciles "failed" to DEGRADED (`cmd/baha/app_list_reconciliation.go:29`)
   while `app status` reports NOT APPLIED because no runtime.env/compose exists
   (`cmd/baha/app_status_collect.go:57`, render at `app_observe.go:81`). Both reported symptoms
   confirmed.
3. Destroy of that state fails closed at the "retained provider ownership" preflight check:
   `checkRetainedApplicationProviderOwnership` (app_core_requirement.go:370-389) refuses with
   `retained_provider_ownership_unverified` (message text at app_core_requirement.go:387) for
   every application-scoped owner WITHOUT a binding when native observation cannot verify it.
   Root cause why verification can never succeed on baseline:
   - `RetainPendingProviderOwnersAt` (internal/application/provider_registry_pending.go)
     registers projection instances, but projection starts EMPTY of bindings
     (`capability.NewRegistry()`), so `preferredProviderResourceAt`
     (internal/application/provider_preferences.go:263-292) falls through and the generic path
     registers only the descriptorLESS owner instance (`Registry.Register` keeps the existing
     entry on ID collision, provider_registry_pending.go:29). A fresh, never-published
     application therefore has NO registry instance with a provider descriptor.
   - The destroy-time snapshot read path then fails or projects nothing for that instance:
     `applicationLifecycleSnapshotContext` binds only registry bindings that exist
     (app_core_requirement.go ~:100-130; for the unbound instance `ResolvePlacement` finds no
     match → error → `classifyApplicationResolutionError` (application_error.go:25) yields
     `provider_consumer_inventory_invalid` — so the union can't prove ownership either), and
     native observation looks up `existingStandaloneProviderInventory`/canonical renderers
     which need the descriptor the instance lacks.
   - Consequence: `facts[instance.ID]` is missing/unverifiable → the exact reported error, for
     a provider that never existed. Destroy can never succeed; the state is unrecoverable by
     retry — matching the J-Commerce transcript.
4. Distinction from historical accepted card t-20261104-r27-destroy-after-aborted-apply
   (#1375, w154/w138 tests): that state has a record WITH `LastAppliedRef` set (provider change
   aborted mid-apply) and no retained unbound owner problem; this state is an interrupted FIRST
   apply with retained unbound owners and no applied reference. Linked, not reopened.

## Fix (smallest causal change) — as actually implemented

- `internal/application/provider_registry_pending.go`: during retention of an UNBOUND,
  application-owned instance, reconcile it with its canonical realization
  (`referenceProviderInstance`) instead of persisting the projection's descriptorless owner
  stub. Placement drift still fails closed (`canonical.ID != instance.ID` → error).
  Shared/foreign/external entries are untouched. A first apply is exactly the moment this seam
  registers unbound owners; a provider REPLACEMENT never leaves an unbound app-scoped
  instance here (the projection copies the live registry, which still holds the old BOUND
  instance, so the reconcile branch never runs for it), so the drift guard keeps its force
  where it matters. This single change makes the unbound owner verifiable through the
  EXISTING canonical observation paths (standalone/native/shared/exposure observers all resolve
  the instance via `registry.ResolvePlacement`, which needs the descriptor): running owners get
  measured facts and keep the normal fail-closed verification; a never-realized owner gets
  `ProviderAbsentOwned` from `observeCanonicalProviderContainers`.
- `cmd/baha/app_core_requirement.go` (`checkRetainedApplicationProviderOwnership`): accept
  `application.ProviderAbsentOwned` — verified absent through the canonical renderer, not
  unverifiable — as safe alongside running/stopped-owned. This is the destroy-side of the fix:
  it removes the "could not be verified" refusal for the never-realized state while every
  genuinely unverifiable fact still fails closed with the unchanged structured error. No
  reclamation-by-registry-deletion is needed in the preflight: the existing full-reset destroy
  already releases all app references and reclaims unbound owned instances in
  `removeApplicationState` → `ReleaseApplicationProviderRegistryAt`.

The candidate diff is exactly these two source files plus the new test file (`git diff
origin/develop...HEAD --stat`): no other product seam needed changing (the retirement-record
and stale-guard concerns re-checked out as inert on this state: the destroy plan projects from
`applicationRuntimeRetirementIntent(original.Manifest)` and `Stale()` passes with the nil
applied dimension, stage_versions.go:87-92, which the test asserts directly).

Why this closes the whole transcript chain: with the descriptor present, the snapshot/union
resolution no longer dies in `ResolvePlacement` for this instance, so the consumer inventory
stays resolvable (the same root cause also broke `buildApplicationDestructionPlan`'s union);
and `app list`/`app status` diverge no longer matters once destroy succeeds and removes the
failed record.

## Candidate diff (exact)

Commits on `lane-0428-286-failed-apply-destroy`:
- `412c86173` fix(0428-286): reconcile retained provider owners so a failed first apply destroys
- `e2891bc1f` test(0428-286): strengthen regression with applied-reference and stale-guard proofs

Files: `internal/application/provider_registry_pending.go` (+behavior, +docs),
`cmd/baha/app_core_requirement.go` (reclaim branch in the ownership preflight),
`cmd/baha/w128_failed_apply_destroy_test.go` (new regression, red-first).

## Regression and green-test audit

- Existing green paths audited: `w154_destroy_aborted_apply_test.go` (different state — applied
  reference present; does NOT execute the retained-unbound-owner failure mode: it never calls
  RetainPendingProviderOwnersAt), `w138_destroy_never_delivered_test.go` (record MISSING
  entirely; never-delivered proof path), `application_provider_retirement*` and
  `provider_registry_pending_test.go` (unit level: retention keeps bindings untouched but never
  asserted descriptors or destroy reconciliation). Classification of the gap: MISSING TEST —
  no existing test drives retention of unbound owners + destroy reconciliation together; the
  new test covers exactly that.
- Red-first proof mechanism: the test reproduces the state through the REAL production seams
  (`recordDeploymentBeforeMutation` + `RetainPendingProviderOwnersAt`), then (step 3) calls the
  REAL preflight function. On baseline the descriptor assertion (step 2) and/or the preflight
  call fail with the exact `retained_provider_ownership_unverified` machine.Error (the test
  names that failure explicitly in its output). On the candidate all steps pass, including the
  real CLI destroy (rc=0), the ownership/reconciliation persistence proof, the stale-guard
  pass, foreign/shared reference protection, second-destroy idempotency and disappearance from
  the deployment inventory (the record `app list` showed as DEGRADED).
- CI mapping: `cmd/baha` package tests run in the standard "Run release-source tests" job of
  ci.yml (`go test ./cmd/baha`) on PR; the new test is auto-discovered there (same package,
  no build tags). Path-selection: touched `cmd/baha/app_core_requirement.go` is catalogued in
  `scripts/pr-gate-coverage.json` → `source.gate.atomic.{docker,podman}.data.capabilities` +
  `.guided`; `internal/application/provider_registry_pending.go` has no catalog entry (the file
  is absent from the catalog today; per mission no `scripts/`/`.github/` edits are allowed in
  this candidate — see FINDING below), so those heavyweight native gates are not additionally
  selected by the registry file itself. Native evidence for this lifecycle behavior rides the
  existing docker/podman full-destroy/guided PR gates already selected by the cmd/baha change
  (no new heavyweight gates added).
- FINDING (file:line for coordinator/owner): `scripts/pr-gate-coverage.json` has no component
  entry for `internal/application/provider_registry_pending.go` (coverage validator tolerates
  it today — the file predates the catalog). If cataloging is required, add
  `{"id":"source.internal.application.provider.registry.pending.go",
  "path":"internal/application/provider_registry_pending.go",
  "surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}`.
  Not applied here because the mission forbids `scripts/` edits.

## repo-rule compliance

- No `.github/**`, no `scripts/**`, no AGENTS.md/CLAUDE.md edits. Product code only + one test file.
- Consent/auth/authorization seams untouched: the reclaim happens inside the preflight
  ownership check that ALREADY gates all destroy mutation; preflight is never bypassed — the
  destroy still runs its full manifest/connectivity/permissions/workload-contract checks.
  Foreign/shared/ambiguous resources remain protected (filter conditions unchanged; reclamation
  limited to unbound instances owned by THIS application id/environment).
- Transport: normal push of own branch; no force-push, no cherry-pick. Rebase via `git merge
  origin/develop` if needed.
- No subagents (Owner directive 2026-11-04). All work in this session.
- Local checks limited to non-test prechecks: `gofmt -l` clean, `go build ./...`, `go vet
  ./cmd/baha ./internal/application`, `bash scripts/source-readability-audit.sh` (PASS).
  Test execution exclusively in Hosted CI (Owner rule 2026-11-24).

## Hosted CI (fill in on completion)

- Exact head SHA: e2891bc1f… (full SHA + run IDs recorded below once runs terminal)
- Run 1:
- Run 2:
- Outcomes:
