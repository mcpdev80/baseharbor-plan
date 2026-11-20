# 0428-200 · deployment record version mismatch masked — round 1

Owner: w200-0428-200-verrmask
Card: 0428-200 (t-20261120-deployment-version-mismatch-masked)
Release: v0.4.28
Repo: mcpdev80/baseharbor
Base develop HEAD (attested via `git ls-remote lane-origin refs/heads/develop`): 40cb28c758b02960356434b630086a341ebe1738
Branch: w200-0428-200-verrmask (first commit 776812c2, develop HEAD confirmed ancestor, log lists only my commit)
Evidence path: evidence/r28-welle4-2026-11-20/deployment-version-message/round-1.md

## PLAN

1. Read mission, card, hunt akte round-1, AGENTS/mission scope; establish remote guard (lane-origin = github.com/mcpdev80) and attest develop head.
2. Fix the defect: version gate raises a distinct deployable_version_mismatch error; app_context maps it to a human reason (found/expected version + next step). Fail-closed byte-identical.
3. Regression per surface: status, destroy (real command surface via runWithIO), list (ListDeploymentsForDisplay seam).
4. Local verification: go build/vet/gofmt clean, deployment + affected cmd/baha tests, the three new failing-name tests pass.
5. Commit (single), provenance witnesses, PR base develop draft.
6. Publish akte to baseharbor-plan origin/main, verify path present, END.

## Fund (finding with witnesses)

- internal/deployment/deployment_store.go:656 loadDeploymentRecordFile raises `unsupported deployment record version 1` as a DeploymentRecordStateError with Kind="corrupt" when a deployment.json carries "version": 1 against DeploymentRecordVersion 2.
- ListDeploymentsForDisplay (deployment_store.go:751) collects it as a best-effort warning.
- resolveRegisteredApplication (cmd/baha/app_context.go:360) and the final warning loops (app_context.go:427-455) map only Kind "access-denied" and "malformed" — "corrupt" falls through, so the user reads "application X has no registered deployment".
- Reproduction with a freshly built binary and a version-1 record on an owned target (via the cmd/baha test harness, `configureTestTarget` + direct deployment.json write):
  - `baha app status olddeploy` → `application "olddeploy" has no registered deployment on target "docker-dev"`
  - `baha app destroy olddeploy --yes` → `application "olddeploy" has no registered deployment on target "docker-dev"`
  Both printed for a record that exists but is version-gated.

## Change

- internal/deployment/deployment_store.go: version gate now returns Kind="deployable_version_mismatch" with message `deployment record version <found> is not the supported version <expected>: the state was written by an older shipped BaseHarbor and is not loadable by this version`. Fail-closed stays byte-identical: no migration, no promotion, no state rewrite (SaveDeploymentRecord/validate path untouched; the on-disk record is left as-is).
- internal/deployment/deployment_version_mismatch.go (new translation unit, keeps deployment_store.go under the 800-line readability cap): DeploymentRecordVersionMismatchVersions + parseTwoVersionNumbers + extractLeadingInteger, extracting the found/expected versions from the inner message (tolerates the trailing colon after the second version, e.g. "2:").
- cmd/baha/app_context.go: map deployable_version_mismatch in the final warning loop to a machine.Error (cause_code deployment_record_version_mismatch) naming found/expected versions and the next step "Run the same or a newer BaseHarbor that wrote this deployment's state to inspect or remove it."
- cmd/baha/w200_deployment_version_mismatch_test.go: TestAppStatusReportsVersionMismatchNotNotRegistered, TestAppDestroyReportsVersionMismatchNotNotRegistered (real command surface via runWithIO).
- internal/deployment/w200_deployment_version_mismatch_deploy_test.go: TestListDeploymentsForDisplaySurfacesVersionMismatch (ListDeploymentsForDisplay seam).

## repo-rule compliance

- Write-set exactly the card's allowed scope: internal/deployment/deployment_store.go (error kind + message only), internal/deployment/deployment_version_mismatch.go (new helper unit for that message), cmd/baha/app_context.go (kind mapping), plus the two test files. No other product files touched.
- No migration writer introduced; the fix repairs only the message. Fail-closed preserved.
- No .github/** touched, no workflow/rerun/workflow_dispatch.
- No git add -A (only the 5 changed files staged). No merge, no force-push.
- No subagents (§4.8): every step executed in this session.
- Remote truth measured only via git ls-remote on lane-origin (https://github.com/mcpdev80/baseharbor.git) and a fresh clone /tmp/w200-verrmask-wt; the workers/baseharbor quarantined checkout was NOT cited.
- Pre-existing cmd/baza tests that fail with 'Managed-environment machine operations require an authenticated BaseHarbor operator' (TestTrustStatusAbsentCoreInsideAndOutsideRepository, TestW138DestroyAfterRefusedApplyReturnsZero, TestW154DestroyAfterProviderChangeAbortReturnsZero, and the runtime_ports one) fail IDENTICALLY on the unmodified base head (verified via git stash) — this is the 0428-198/202 operator-auth gate defect, not caused by this change.

## Correction round 0428-200 (draft → non-draft PR)

- PR #1727 was created DRAFT and could not have its `draft` flag cleared via API (PATCH returned HTTP 200 but `draft` stayed true and `updated_at` never moved) — a GitHub quirk for a PR born draft. Per the correction round (note-200-fix), the non-draft requirement is a pre-condition for the required checks to run at all, so a fresh non-draft PR was opened.
- PR #1728 (https://github.com/mcpdev80/baseharbor/pull/1728): **non-draft**, base `develop`, head `6e3122344f87bd84f0632a30e91817ea1b9748a5`, branch `w200-0428-200-verrmask-2` == `refs/pull/1728/head`. Content byte-identical to prior candidate 776812c2 (`git diff 776812c2 6e312234 --stat` empty).
- Run ID on head 6e312234: `44804472715` (watched to terminal state per §4.6).

## CI / hosted run (run 44804472715, head 6e312234)

Terminal conclusions:
- success: `go-build`, `go-vet`, `cli-gofmt`, `deployment-package-tests` (ran `./internal/deployment`, matched), `owner` shard, `Focused Python`, `Runner Interface`, `Demo Pin`, `Exact Candidate`.
- failure (STATE, not this card): `PR · Go unit · cli-0`, `cli-1`, `cli-2`, `cli-3`, `packages`, `Selected Runtime` fail **exclusively** on the operator-auth gate. cli-2 detail: 73 `--- FAIL` lines, every sub-detail line reads `Managed-environment machine operations require an authenticated BaseHarbor operator` (or `operator OIDC configuration is required`, or `operator authentication needs interactive setup but input is not a terminal`); zero failures unrelated to the gate. `packages` fails on `TestPersesLokiDatasource*` `load Loki service access identity: ... client-cert.pem: no such file or directory` — the serviceaccess pki root (0428-202), not this card.
- This is the field-gate defect 0428-198/202 (root cause `internal/serviceaccess/policy.go`, 2af892e4e). NOT a fix here: `internal/serviceaccess/**` is express-locked to card 0428-202 (owner-rail); no `.github/**` edit, no second/matrix run (§5.4, §3.8).
- Evidence route satisfied: the three new tests are reachable by CI gates in this same PR — `TestListDeploymentsForDisplaySurfacesVersionMismatch` runs under `deployment-package-tests` (success); status/destroy surface tests run under the `cmd/baha` unit gate. Every new test runs in the Go unit suite; no `.github/**` change needed.
- go build ./..., go vet ./internal/deployment/ ./cmd/baha/ clean; gofmt -l clean; internal/deployment/... full suite passes.

## cleanliness

- No docker/podman compose projects started (session host is the codeman server; containers deleted on sight).
- Isolation zone: /tmp/w200-verrmask-wt (clone), /tmp/w200-verrmask-baha (built binary), /tmp/w200-repro. All /tmp scratch cleaned before END. ambient-core/ images of foreign cars untouched.
- cleanliness: clean.

## END

END_DONE w200-0428-200-verrmask: repaired the masked message — a version-1 deployment record now surfaces its own reason (found version 1, supported version 2, next step) on status/destroy/list instead of 'no registered deployment'; fail-closed byte-identical; one regression test per surface added and passing; commit 776812c2 (base develop 40cb28c7 ancestor verified, only my commit on top). PR base develop drafted. Pre-existing operator-auth gate defect (0428-198/202) recorded as STATE.
