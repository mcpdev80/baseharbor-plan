# H-P7 — Adversarial Hunt: #1502 orphan-adoption torn-teardown + #1504 wizard foreign-record

- Shift: r27-welle5-folge-2026-11-08
- Card: mission-hp7 (JAGD / hunt — no product change, no .github/**, no subagents)
- Session model: Ornith
- Date: 2026-11-09 (work done this shift; commands timestamped inline)
- Base develop SHA: fea92f379e55bbe6e143a095d7c2e6c16e0b3a06
- PR #1502 commit: 1912734ff864bdfefd7ab8ae71a25e856859d5d8
- PR #1504 commit: 2abfeee70419140c8115d864572152071406dce9
- Both PRs confirmed landed as ancestors of origin/develop (merge-base --is-ancestor)

## Scope / what was attacked

Two landed commits, both today (2026-11-09), on develop fea92f379:
- #1504 "report foreign provider records as actionable conflicts" — cmd/baha foreign-provider
  resolution/classification + wizard/edit selection surface (internal/application footprint + union).
  Files: cmd/baha/app_core_requirement.go, app_edit.go, app_edit_apply_result.go,
  app_provider_choice.go, app_wizard_controller.go, internal/application/footprint.go,
  internal/application/provider_union.go (+ app_foreign_records_regression_test.go).
- #1502 "fix bootstrap orphan adoption torn teardown" — cmd/baha runtime integration test
  adoption of a dead-owner bootstrap marker. Files: cmd/baha/runtime_integration_test_support_test.go,
  runtime_integration_cleanup_coverage_test.go.

Attack vectors named by the mission:
1. wizard foreign-provider record where own vs foreign record is misattributed.
2. orphan adoption double-adopts / loses a record after torn teardown; scan->adopt window.
3. report-text claims a different fact than the code (cite line + output).

## Reality witnesses

- planning repo origin/main: `git ls-remote --heads origin main` =>
  bd12c5b8f7802852f2c27f0d4e041fb5db8d944c refs/heads/main
- develop head: `git ls-remote --heads origin develop` =>
  fea92f379e55bbe6e143a095d7c2e6c16e0b3a06 refs/heads/develop
- #1502 ancestor of develop: `git merge-base --is-ancestor 1912734ff origin/develop` => true
- #1504 ancestor of develop: `git merge-base --is-ancestor 2abfeee70 origin/develop` => true
- candidate worktree: /tmp/opencode/hp7-hunt at HEAD fea92f379 (detached). Branch cut from
  fea92f379; `git rev-parse fea92f379` is an ancestor of the first commit. No foreign branch carried.

## Findings

FINDING-1 (MISSED — #1504 attribution is correct, report text matches code)

Claim under attack: a foreign consumer's stale provider edge must be reported as the concrete
conflict it is (naming that consumer + instance + recovery), not a generic not-found, and the
wizard/edit view must keep a requirement-local failure visible instead of aborting.

Trace (source, base develop fea92f379):
- internal/application/provider_union.go ResolveProviderPlan: for each active consumer,
  resolveRetainedConsumerFootprint returns *ResolutionError; at lines 96-102 the union fills
  resolution.Consumer = consumer.Key when empty (the pure footprint resolver never sets Consumer).
- cmd/baha/app_core_requirement.go classifyApplicationResolutionError lines 150-195: when
  resolution.Consumer != "" it sets causeCode="provider_stale_consumer_dependency",
  resource=resolution.Consumer, and next = 'Consumer %q references provider realization %q, which
  no longer exists ...; ... release the named consumer through its own lifecycle owner ...; no
  provider was mutated.' with resolution.Consumer and resolution.InstanceID interpolated.
- cmd/baha/app_provider_choice.go appProviderChoicesWithView: in selection view a requirement whose
  resolution fails on THIS requirement's kind/instance stays unresolved-visible on its own line
  (case "missing" -> unresolved[req]); every other failure (incl. any record's dependency edge)
  keeps aborting with the typed error (lines 137-182).

Empirical verification (pure unit, no daemon):
  $ go test ./cmd/baha/ -run 'TestForeignRecord' -v -count=1  (2026-11-09)
  --- PASS: TestForeignRecordDoesNotBlockHttpAppSelection
  --- PASS: TestForeignRecordUnionReportsConcreteConflictWithNextStep
  --- PASS: TestForeignRecordStaleReferenceDoesNotPoisonUnrelatedUnionPlan
All PASS.

Additional probe (two foreign consumers sharing the SAME missing shared realization, http-only
current app): the classified error named the specific foreign consumer
"deployment/00000000-0000-4000-8000-000000000007", code provider_stale_consumer_dependency, and
next named the exact instance "postgresql/shared/environment-dev-91df0423" + "lifecycle owner".
No misattribution to the current app. Report text matches code.

Conclusion: NO defect. #1504 correctly attributes foreign records to their owning consumer and its
next-step text states the actual code behavior. The "missing + Consumer==''" branch of classify
(line 179) only fires outside the union resolver, which never leaves Consumer empty, so it is dead
in the CLI plan/apply path — not a defect, not reachable.

FINDING-2 (MISSED — #1502 adoption is atomic and fail-closed; no double-adoption / no loss)

Claim under attack: a dead-owner bootstrap marker whose target's Core was never provisioned is a
phantom with nothing to reclaim; adoption consumes it cleanly (marker removed, nil), while a real
residual (Core provisioned / owned resources remain / engine error while something WAS up) keeps the
marker and aborts. The scan->adopt window must not double-adopt or lose the claim.

Trace (base develop fea92f379, cmd/baha/runtime_integration_test_support_test.go):
- adoptBootstrapLeftoverMarkerFromDeadProcess (316-345): reads marker -> checks owner pid dead
  (bootstrapProcessAlive, line 348; EPERM-safe). Calls destroyOrphanedBootstrapMarkers; only on
  nil error does it os.Remove(marker) and return (marker, nil). Marker removal is gated on the
  destroy having run (no early consume).
- destroyOrphanedBootstrapMarkers (367-452): iterates config targets matching bootstrapTargetPattern
  (w169-ci-bootstrap-[0-9a-f]{10}). For each: orphanBootstrapTargetHadFootprint (466-517) reads
  runtime files (fail-closed on any I/O error, line 500-507), else ownedFootprintOnEngine
  (533-563). A phantom (no footprint) -> continue (consume); a real footprint -> destroyRuntimeIntegrationTrustPlane.
  Any destroy/inventory failure is appended to errs; errors.Join(errs...) is returned, keeping the
  marker (fail-closed).
- orphanBootstrapTargetHadFootprint: files-not-found -> confirm engine inventory; a genuine not-found
  proves "no provisioned Core"; any other read error fails closed.

Empirical verification (pure unit, no daemon):
  $ go test ./cmd/baha/ -run 'TestBootstrapAdoption' -v -count=1  (2026-11-09)
  --- PASS: TestBootstrapAdoptionIgnoresLiveOwners
  --- PASS: TestBootstrapAdoptionConsumesOrphanWithNoProvisionedCore
  --- PASS: TestBootstrapAdoptionKeepsMarkerWhenCoreExists
  --- PASS: TestBootstrapAdoptionFailsClosedOnEngineInventoryError
  --- PASS: TestBootstrapAdoptionFailsClosedOnResourceInventoryError
  --- PASS: TestBootstrapAdoptionFailsClosedOnRuntimeFilePermissionError
All PASS.

Atomicity probe (my own, removed before push — pure unit, synthetic phantom marker + dead pid):
  first adopt returns (markerPath, nil) and the marker file is gone; second adopt returns ("", nil)
  no-op. No double-adoption, no lost claim. (Probe file cmd/baha/hp7_probe_test.go and
  cmd/baha/hp7_adoption_probe_test.go were deleted after running; not committed.)

Conclusion: NO defect. The torn-teardown fix is atomic (destroy runs, then marker removed) and
fail-closed on every error path. No scan->adopt window that double-adopts or loses a record.

FINDING-3 (NEGATIVE BOUND — #1504 single foreign app with managed secrets + empty registry)

Observed behavior (empirical, pure unit): a Target carrying a SINGLE foreign record whose app
requires the runtime broker (managed secrets) but whose broker instance is not on the registry fails
the union plan with "Provider consumer inventory is incomplete or damaged."
Source: cmd/baha/application_provider_plan.go RuntimeDependencyRoots (internal/application/
runtime_dependency_roots.go:30) returns a non-nil error when RequiresRuntimeBroker(m) and the broker
is not registered; resolveApplicationProviderPlan wraps it via invalidProviderConsumerInventory.
This is the intended fail-closed "broker required but not registered" case, not a mis-report. It
differs from the shipped regression fixture (foreign app with secrets=false, so no broker required),
which is why the two-consumer attribution probe reaches classify while a single broker-required
foreign consumer does not. Documented as a bound, not a defect.

## Negative bounds

- No .github/** read for edit, none changed, no workflow rerun / workflow_dispatch triggered.
- No product code changed. No PR opened.
- No subagents spawned (4.8). Every step ran in this session.
- No docker/podman stack started on this host (coordinator/codeman server). #1502's native
  runtime-integration acceptance runs on the hosted go-test ./../.. matrix (Owner scope); the pure
  unit regressions were run here and pass.
- Build/vet clean: go build ./cmd/baha (exit 0), go vet ./cmd/baha/ (exit 0).

## END

END_DONE mission-hp7: head=fea92f379 pr=1502,1504 behaviour=adversarial audit of #1504 wizard
foreign-record attribution + #1502 orphan adoption torn-teardown — both landings verified correct
(report text matches code; attribution names the owning consumer + instance; adoption is atomic and
fail-closed; no scan->adopt double-adoption or loss). No defect found. Negative bounds + FINDING-3
boundary documented. No .github/**, no product change, no subagents. Evidence on origin/main.
