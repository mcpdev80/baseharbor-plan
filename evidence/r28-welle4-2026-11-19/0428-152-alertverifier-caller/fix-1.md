# 0428-152 · alert-verifier caller wiring — fix-1

Lane: w41-0428-152-alertverifier (flash seat)
Card: t-20261119-r28-perses-alert-verifier-caller-wiring
PR: https://github.com/mcpdev80/baseharbor/pull/1816 (base develop, OPEN, not merged — Merge-Frost)
Candidate head: 70ab77ad5e8f88faaac78c90c63a985bb69a72e5

## PLAN

1. Read card via plan.py show + card body; note acceptance and write set — done
2. Resolve real GitHub remote (remote -v); fetch lane-origin develop (d4fa8c589); base attestation — done
3. Create branch lane-0428-152-alertverifier-caller from origin/develop; witnesses — done
4. Inspect verifier contract surface and app_status_collect.go perses observation — done
5. Implement honest consumer (not configured / unavailable owner-gated / never healthy-verified) — done (review rounds moved it into reportPersesSurfaceStatus)
6. Add cmd/baha tests per state; CI/gate route — done; self-cataloging rows REMOVED per coordinator directive (baseline catalog rows land on develop via the CI/catalog owner)
7. Evidence file in baseharbor-plan evidence/r28-welle4-2026-11-19/0428-152-alertverifier-caller/ — this file
8. Push, PR #1816, delivery witnesses — done
9. Watch exact-head Hosted CI run to terminal; record run ID/result — done (45287538708: Trusted Plan red on the missing BASELINE catalog rows; not lane-fixable)
10. Evidence on origin/main before END; post END line — last actions

## Planning repo witness (before first evidence commit)

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
    origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

## Base attestation and branch provenance

    $ git remote -v            # first git action in the worktree
    lane-origin  https://github.com/mcpdev80/baseharbor.git (push)
    origin       https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]

    $ git ls-remote lane-origin refs/heads/develop
    d4fa8c589e02bf6708d9e6beba7a510c1a2efc7e  refs/heads/develop

Branch created from exactly that SHA (the merged #1702 content).

    $ git merge-base --is-ancestor lane-origin/develop HEAD && echo ANCESTOR_OK
    ANCESTOR_OK

    $ git diff lane-origin/develop...HEAD --name-only   # at 70ab77ad5
    cmd/baha/app_status_collect.go
    cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go
    cmd/baha/perses_lifecycle.go

    $ git log --oneline lane-origin/develop..HEAD       # at 70ab77ad5
    70ab77ad5 0428-152: drop the self-cataloging from this PR
    87dcd7a7d 0428-152: use the underscore component ids the validator requires
    836469a39 0428-152: map the three catalog rows to the data.capabilities surfaces
    7fa61146e 0428-152: register gate coverage for the consumer files
    df94c624a 0428-152: resolve the perses status seam by application name
    3b9a75a9d 0428-152: add the alert-evaluator consumer to 'baha app perses status'
    f0fe88edf 0428-152: assert the consumer on the production collection path
    3f8e6fa1b 0428-152: tolerate the absent observation on non-applied command faces
    79f356aaf 0428-152: run the alert-evaluator consumer on the applied status face
    a2d2e8ba9 0428-152: wire the Perses alert-evaluator verifier into 'baha app perses status'

All commits are this lane's own; no foreign candidate is carried. The
scripts/pr-gate-coverage.json self-cataloging (three commits) is fully
reverted-forward by 70ab77ad5: the file is byte-identical to develop and no
longer appears in the diff.

## What was implemented

The Perses alert-evaluator verifier in internal/metrics/perses_prometheus_alerts.go
had NO caller. This card gives it exactly one honest consumer, shared by the
status faces through a single function:

- cmd/baha/perses_lifecycle.go:
  - persesAlertEvaluatorObservation(m): ONE metricsprovider.BuildPersesAlertEvaluator
    call decides the state. Verifier error "Perses is not selected" => "not
    configured"; any other fail-closed verifier error => "unavailable
    (owner-gated evaluator contract)"; success => verifier reachability shown
    verbatim ("configured_unverified" in this Core). A hypothetical "verified"
    reachability is downweighted to the unavailable state, so
    "healthy"/"verified" can never be emitted while
    persesAlertRealEvaluatorContractPresent() is false.
  - reportPersesSurfaceStatus ('baha app perses status' + the MCP
    app.perses.status read model) fills the new AlertEvaluator field
    (*application.StatusCheck, json "alert_evaluator") of persesStatusResult.
- cmd/baha/app_status_collect.go: collectManagedServiceChecks calls
  collectPersesAlertEvaluatorObservation (guarded by the existing manifest
  bindings Services.ObservabilityManagementUI || Services.Perses), which
  delegates to the SAME function — one decision logic, no parallel
  CLI-side path. AddObservation never receives "ready"/"verified", so the
  observation never folds into readiness.

No new state holder, no new manifest field: the decision derives from the
existing manifest bindings the verifier itself reads. internal/metrics/**
(0428-073) untouched (see diff --name-only).

## Tests and CI route

cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go:
TestPersesAlertEvaluatorObservationNotConfiguredWhenUnselected,
...UnavailableWhenSelectedWithoutContract (exact wording),
...SelectedWithContractStaysUnverified (verbatim reachability),
...NeverReportsHealthyOrVerified (fail-closed matrix + verified-marker pin),
...PersesStatusSurface (observation asserted on the OUTPUT of
reportPersesSurfaceStatus, seam call + real `baha app perses status --json`,
by unique application name), ...UnappliedReportsNotConfigured,
...AppStatusCollectionFace, ...OnAppStatusCommandFace.

Unit route exists on the base plan: `go test ./cmd/baha` in
scripts/pr-unit-database.sh runs them in the Hosted PR Go-unit/Draft shards.
The NATIVE gate route does not exist on develop: the trusted catalog
(scripts/pr-gate-coverage.json at trusted develop 0d29c2a9) has no rows for
cmd/baha/app_status_collect.go, cmd/baha/perses_lifecycle.go and
cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go, and — proven by
run 45287538708 (and earlier 45287020021) — the planner loads the catalog from
the trusted BASE, so rows added inside this PR cannot authorize the diff.
Per the coordinator directive (2026-11-23), the three BASELINE catalog rows
(id/path/surfaces exactly as the planner's error text names them, surfaces
source.gate.atomic.{docker,podman}.data.capabilities) are a CI/catalog-owner
action on develop, landed separately; this PR was reduced to product code only.

## Hosted CI (self-run duty §4.6)

- 45283690237 (3f8e6fa, draft): CI · Source & Quality completed/success.
- 45284520538 / 45284526585 (3b9a75a9d): cancelled by superseding pushes.
- 45285233520 (df94c624a): completed/failure — Trusted Plan ValueError
  (uncataloged sources; first appearance of the baseline-catalog blocker).
- 45286007687 (7fa61146e), 45286659035 (836469a39), 45287020021 (87dcd7a7d):
  completed/failure — same ValueError; proved PR-local catalog edits are
  resolved from the trusted base (0d29c2a9), i.e. ineffective (coordinator
  root-cause, adopted).
- 45287538708 (exact head 70ab77ad5): completed. Workflow policy, PR · Source
  format, PR · Native gate plan success; PR · Trusted Plan completed/failure
  with the same "uncataloged source change, no declared runtime gate owner"
  ValueError for the three paths; PR Selected Checks therefore reports the
  planner abort (all downstream shards skipped). This is the STATE: the
  lane-side fix is complete and the remaining red is the external baseline
  catalog rows, per coordinator directive to stop self-cataloging.

## cleanliness

- No containers, networks, volumes or compose projects were started by this
  lane on this host or any SSH host (`docker ps -a` on this host shows no
  w41/test entries; the lane started none).
- Worktree: /home/marcel/dev/baseharbor-ecosystem/workers/w41-0428-152-wt
  (single branch lane-0428-152-alertverifier-caller; no second branch).
- Scratch clone under /tmp/opencode/w41-0428-152-alertverifier-wt only.
- One transient diagnostic test file existed pre-Owner-halt, deleted and never
  committed. After the Hosted-only halt (2026-11-23) no local product test was
  run; verification was exact-head Hosted CI only.

## repo-rule compliance

- Write set: cmd/baha/app_status_collect.go + cmd/baha tests; the coordinator
  directives extended this to cmd/baha/perses_lifecycle.go (same card, the
  reportPersesSurfaceStatus consumer) and back out again to product-code-only.
- .github/** untouched; no reruns or workflow_dispatch.
- scripts/pr-gate-coverage.json: added then reverted-forward per explicit
  coordinator directive; final diff contains no scripts/** change.
- No subagents; every step ran in this session.
- No merge (Merge-Frost); PR #1816 open at 70ab77ad5.

END_BLOCKED 0428-152: product consumer + states + tests complete and delivered
(PR #1816 head 70ab77ad5; exact-head run 45287538708 observed to terminal);
Trusted Plan stays red ONLY on the missing baseline catalog rows for
cmd/baha/app_status_collect.go, cmd/baha/perses_lifecycle.go and
cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go in
scripts/pr-gate-coverage.json on develop (CI/catalog owner action; rows
specified above).
