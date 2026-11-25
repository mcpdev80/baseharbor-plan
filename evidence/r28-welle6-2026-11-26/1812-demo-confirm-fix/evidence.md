# w140-0428-249 — Route #1812 Docker-batch `--confirm-candidate` failure out of the workflow-only #1812 diff

Mission: `/home/marcel/dev/baseharbor-ecosystem/coordinator/missions/w140-demo-confirm-candidate-fix.txt`
Session route for the exact-head run 45515666142@eafd5e6d failure (4 red atomic/docker Light gates).
END_BLOCKED w140-0428-249-demo-confirm-candidate-fix: see "## Status" and "## QUESTION" below.

## PLAN

1. Pull the 4 red job logs from run 45515666142 (jobs 138878143819 policy, 138878143903 reconciliation, 138878143925 connectivity, 138878144097 full-destroy) and confirm terminal FAILURE.
2. Locate the demo test/journey path issuing the fail-closed rejected mutation; record file:line + log witness.
3. Decide route (2) demo fix vs route (3) core Befund.
4. Implement minimal fix (add `--confirm-candidate` only at a legitimate confirm point; preserve fail-closed; no consent/auth relaxing; no `.github/**` edits).
5. Prove branch provenance (ancestor + diff + log-line witnesses).
6. Open Draft demo PR, push, prove delivery via `git ls-remote`.
7. Observe my own exact-head hosted CI run to terminal state (self-run duty).
8. Write this evidence, commit, push, prove presence on origin/main.
9. Flag #1830-style pin update + #1812 hop requalification.
10. VM cleanliness + END post.

## Remote / provenance witnesses

Planning repo remote (verified before first evidence commit):
```
origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-plan.git (push)
```

baseharbor-demo remote (GitHub real URL; no filesystem origin present in this checkout):
```
origin  https://github.com/mcpdev80/baseharbor-demo.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-demo.git (push)
```

baseharbor (core) remote resolution (REMOTE GUARD — use the github.com/mcpdev80 URL):
```
git -C .../baseharbor remote -v -> origin/lane-origin/upstream all https://github.com/mcpdev80/baseharbor.git
(one anomalous empty-name remote line also prints the github URL; no local-filesystem origin)
```

Base attestation (branch cut point):
```
git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/heads/develop
b41127723e523134a1c14ee3c36cf133237162ce  refs/heads/develop
```
Branch `w140-0428-249-demo-confirm-candidate-fix` was created at exactly `b4112772` (develop tip = mission's "b4112772-family"). No commits pushed; no PR opened (blocked on the scope decision below).

Candidate facts:
- Failing exact-head run: baseharbor Pre-Release Validation, run 45515666142, head `eafd5e6d641a65adf7c94e622391b49cfc6f2159` (refs/pull/1812/head), demo_ref `b41127723e523134a1c14ee3c36cf133237162ce`.
- `eafd5e6d` vs develop `f7540e59`: the ONLY changed file is `.github/workflows/pre-release-runtime-suite.yml`. #1812 ships no product Go change; the Light-gate Go code equals develop tip.
- The candidate `baha version` reports commit `f7540e59…` (the PR merge-base stamp); product behaviour is develop-tip behaviour.

## What the CI logs actually show

Red job logs pulled via the Actions logs API (`/repos/mcpdev80/baseharbor/actions/jobs/<id>/logs`).

Per-job "failing command" assertion line (identical root pattern, per mission claim):
- policy 138878143819: `tests/policy/run.sh:30` → the `operator_test_idp_setup` Keycloak step. Console ALSO shows `Invalid key/certificate pair … Unable to read file /opt/keycloak/conf/server.key` (policy run.sh:30 = `operator_test_idp_setup` from tests/policy/operator-test-certificate.sh). The Keycloak test-IdP does not become ready. The `record deployment before mutation` line at log 1476/2048 belongs to the guided `up` capture/consent handshake, NOT the policy assertion.
- reconciliation 138878143903: fails at run.sh:22 (the subshell that runs `run_consented "$BAHA" app apply` then `"$BAHA" app doctor`). ci-operator decision trace shows the apply reached READY with `app apply … --confirm-candidate <digest>`, then `app doctor` as the next gate command.
- connectivity 138878143925: fails at run.sh:36 (subshell `app init --quick` → `run_consented up --yes` → `app doctor`). ci-operator trace shows `up --yes --json --confirm-candidate 01667d3…` executed, then `app doctor`.
- full-destroy 138878144097: fails at run.sh:16 (`"$BAHA" app list --all-targets`). Console shows an `authentication_failed` / "authenticate the BaseHarbor operator" error and a `destroy --all` provider-change plan, i.e. this gate's symptom is NOT the candidate-consent message.

ci-operator.log (build-tag `baseharbor_ci_operator_testonly` audit of every Core call) shows, in each red gate, the mutating `up`/`app apply` invocations run WITH `--confirm-candidate <digest>` (drive.py capture→consent + run_consented wrapper). Only `state=="applying"` calls touch the candidate choke (`promptConfirmCandidateSubmission` + `recordDeploymentBeforeMutation` in cmd/baha/app_apply.go:201-202 and cmd/baha/runtime.go for root `up`). Read paths (`app doctor` without `--fix`, `app list --all-targets`, `doctor`) go to the "configured"/read code and do NOT emit `record deployment before mutation`.

## Why I cannot apply a blind route-(2) fix (root-cause conflict)

The mission asserts: "a demo mutation is fail-closed rejected because `--confirm-candidate` is missing", call site expected in the demo repo test path.

Against the actual evidence:
1. The candidate-consent gate is pre-existing in Core (introduced #1355 / the "up non-TTY: print exact `--confirm-candidate` hash, fail-closed" family; present in develop tip AND in the demo `baseharbor-core.ref` pin `08755645`). #1812 changes no product Go. So this is not a new #1812 regression.
2. The demo guided path already handles the handshake: `tests/guided/drive.py` `run_guided_consent_flow` does capture-run → `binary_supports_confirm_candidate` → re-run `up --confirm-candidate <hash>` → READY, and `run_consented`/`tests/fixture-consent.py` already auto-adds `--confirm-candidate` on the candidate refusal (fixture-consent.py candidate_confirmation/set_candidate_confirmation). The ci-operator trace confirms both ran WITH `--confirm-candidate`.
3. `app doctor` (the command right after the failing apply in reconciliation/connectivity) and `app list --all-targets` (full-destroy) are read commands. `app_doctor_repair.go` `executeApplicationRepairLifecycle` returns `cli.Presented` without any apply unless `--fix` is passed, and `parseAppDoctorRepairArgs` rejects unknown flags — so a plain `app doctor` cannot emit `record deployment before mutation`, and there is no legitimate `--confirm-candidate` to add to a read.
4. full-destroy's console symptom is operator authentication, not the candidate message.

Conclusion: I could not find, in the demo repo test path, a mutating `baha` invocation that is missing `--confirm-candidate`. The candidate rejections in the logs are the expected guided `up` fail-closed capture (then re-run OK). The gates' terminal failure is not explained by a "demo mutation lacking `--confirm-candidate`" in the current code. Fabricating that call site — or wrapping a read command in a consent handler / relaxing consent — would violate the "NO consent/auth relaxing" and "fix the reported defect only" constraints.

## VM smoke diagnosis (brief, isolated, cleaned) — corroboration

Per policy (VM = brief smoke/diagnosis only; Hosted CI is the verification authority). I reproduced the candidate on the named docker host. Early attempts failed at `authentication_failed` because the synthetic CI operator (`cmd/baha/ci_integration_operator_enabled.go`) admits a managed-local-gate only when `BASEHARBOR_DEMO_OPERATOR_GATE` matches the canonical target `atomic-docker-<gate>`. Once I set the exact CI env (line 334 of `.github/workflows/pre-release-runtime-suite.yml`: `BASEHARBOR_DEMO_OPERATOR_GATE=reconciliation GATE=reconciliation BASEHARBOR_DEMO_OPERATOR_TRACE=1 DEMO_ATOMIC_GATE=1 BASEHARBOR_TARGET=atomic-docker-reconciliation`, plus the operator-tagged candidate binary and a runtime image built from it), the gate ran faithfully:
- Built `baha` from `eafd5e6d` with `-tags baseharbor_ci_operator_testonly`; runtime image `baha` reports the matching commit.
- The probe `baha up --confirm-candidate` (no digest) returns exactly `Error: --confirm-candidate requires DIGEST` → `binary_supports_confirm_candidate` returns TRUE for this candidate, so drive.py WILL re-run `up --confirm-candidate <hash>`. (Confirms the consent path is wired, not broken.)
- The faithful reconciliation run reached `>>> demo-reconciliation`, ran the guided `up` capture (rejected `--confirm-candidate 147828706f...` → re-run → `[phase] guided up: READY reached`), entered `== Reconciliation ==`, and then **failed at the FIRST subshell — `run.sh:10`** (the IN_SYNC apply), not line 22:
  `demo-reconciliation FAIL — tests/reconciliation/run.sh:10: assertion command failed (exit 2): ( cd "$DEMO_ROOT"; run_consented "$BAHA" app apply > "$ARTIFACT_DIR/reconcile-insync.txt" )`
  with JSON error `validation_failed: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate) ... next: Re-run with --confirm-candidate 147828706f...`.
  This is the first hard evidence that a `run_consented "$BAHA" app apply` reached the fail-closed gate and the wrapper did NOT bind the candidate — i.e. `run_consented`/`tests/fixture-consent.py` is the suspect consent mechanism for the `app apply` path, not any missing call site or read command.

Reconciling this with the CI logs: in the hosted red gates the IN_SYNC apply at line 9 PASSED and the failure surfaced later (run.sh:22 doctor subshell); in my VM run the very same apply FAILED. The difference is the candidate re-bind timing/state. Either way, the reproducible defect is that `run_consented`'s `app apply` subshell can reach the candidate choke and the auto-retry does not always clear it. The candidate-consent gate itself is correct and fail-closed; this is a demo consent-wrapper (fixture-consent.py) coverage question on the `app apply` path, which is within route-(2) demo scope but must not relax the default.

## What is needed to unblock (scope decision)

Either:
(a) A precise demo call-site pointer — the exact `tests/<gate>/run.sh:LINE` of the mutation missing `--confirm-candidate` — plus a demonstration (log line) that a demo mutation (not a read, not the guided capture) actually failed closed. I searched every `"$BAHA" …up/apply` call site; they are all consent-handled. If one is missed, name it and I will wrap it via `run_consented` in a Draft demo PR.
(b) Route (3): if the missing-`--confirm-candidate` mutation is actually issued from a Core workflow path (the bootstrap `up` in `tests/atomic-bootstrap.sh` invoked by `.github/workflows/pre-release-runtime-suite.yml`, or the core `up --yes --json` capture), then per the mission I must NOT touch it and instead file the Befund (this section + file:line witnesses below are that Befund).

file:line witnesses for route (3) Befund:
- `.github/workflows/pre-release-runtime-suite.yml` (baseharbor): runtime-gate bootstrap invokes the demo acceptance which runs `tests/atomic-bootstrap.sh` → `run_guided_consent_flow` (`tests/guided/drive.py`). This is the Owner-scope workflow file the mission protects.
- `tests/guided/drive.py` run_guided_consent_flow + binary_supports_confirm_candidate; `tests/fixture-consent.py` candidate_confirmation/set_candidate_confirmation — the consent handlers that already add `--confirm-candidate`.

## cleanliness

docker ps -a before: (fresh VM) `count=0`
docker ps -a after: `count=0`. The faithful reconciliation smoke reached READY and left 17 `bh-atomic-docker-reconciliation-*` containers up (the acceptance cleanup exited on the auth boundary); I brought all four compose projects DOWN with `docker compose -p <proj> down -v --remove-orphans`, force-removed any lingering reconciliation containers, removed my smoke networks (baseharbor-*-atomic-docker-reconciliation*), my volumes, and my images (`localhost:5000/baseharbor-runtime:pre-release`, `registry:2.8.3`), and removed all `/tmp` scratch (`/tmp/dec`, `/tmp/wx`, oras).
Final witness: containers=0; recon nets=none; recon vols=none; my images=none; `/tmp` lane dirs gone; my procs NONE.
Ambient images on the VM (`ghcr.io/mcpdev80/baseharbor-runtime:latest` / `:edge`) were left UNTOUCHED per owner-direc…nd the root-path `/usr/local/bin/baha serve` processes (another session's, 5h uptime) were observed and NOT touched, nor was the unrelated `/home/marcel/baha-dev login` process.
Note: the `baha-docker` SSH alias resolves to hostname `baha-runner-docker` (192.168.6.166), a separate VM from this coordinator host `codeman`; it was used only for the smoke diagnosis above and left clean. An unrelated `baha-dev login` process and root-path `baha serve` processes (both another session's) were observed and NOT touched.

## repo-rule compliance

- No `.github/**` edited (Owner scope). No workflow rerun/dispatch triggered.
- No consent/auth relaxing; no product-code change proposed without a confirmed call site.
- Hosted-only: no product test/unit suite run on the coordinator host (`codeman`). VM used only for brief read-only diagnosis, per §4.5.
- Evidence lives only in baseharbor-plan (no evidence files in any product repo; no product-repo planning commits).
- Branch cut from develop tip `b4112772` with ancestor proof; single candidate branch, no second branch.
- No subagents used.

## Status

END_BLOCKED — route decision required, with the precise suspect now identified.

What is confirmed:
- The #1812 diff is workflow-only (`eafd5e6d` vs develop `f7540e59` differ in exactly one file: `.github/workflows/pre-release-runtime-suite.yml`). The candidate's product Go code equals develop tip. So the Light-gate failure is a develop/demo condition, not a #1812 code regression. The candidate-consent gate pre-dates #1812 (introduced ~#1355; present on develop tip and in the demo `baseharbor-core.ref` pin `0875564`).
- All 4 red gates reached `guided up: READY reached` (drive.py capture→`up --confirm-candidate`→READY works); the candidate rejections in the console are the expected guided fail-closed capture, not the failing mutation.
- A faithful VM reproduction (exact CI env: `BASEHARBOR_DEMO_OPERATOR_GATE`+`GATE`+`BASEHARBOR_DEMO_OPERATOR_TRACE`+`DEMO_ATOMIC_GATE`+canonical target, operator-tagged binary, runtime image from it) reproduces a real fail-closed candidate error, but on `run.sh:10` (`run_consented "$BAHA" app apply`, the IN_SYNC apply): the `run_consented`/`fixture-consent.py` wrapper reached the candidate choke and did NOT clear it.

Open conflict (why I do not commit a fix): the mission says "all EXECUTED, identical candidate-consent root cause, fix in baseharbor-demo", but the discriminating factor is not a plainly missing `--confirm-candidate` at any single `tests/<gate>/run.sh` call site — every mutating call there already goes through `run_consented` or the guided driver. The reproducible failure is `run_consented`'s `app apply` re-bind logic (fixture-consent.py), and the CI-log symptom differs from my VM symptom (apply passed then doctor failed vs apply failed). Editing `fixture-consent.py` re-bind logic without the coordinator confirming the exact intended contract risks changing consent behavior (forbidden without confirmation), and it is a shared wrapper, not a one-line add.

What is needed to unblock (route decision): confirm whether the fix is (a) to harden `tests/fixture-consent.py` so its `app apply` re-run reliably binds the candidate digest before the IN_SYNC apply (route 2, demo repo, my scope — I will implement + Draft PR + hosted CI), or (b) a Befund that the call site is the workflow bootstrap in `.github/workflows/pre-release-runtime-suite.yml` (route 3, Owner scope). My lean: (a), `fixture-consent.py` `app apply` re-bind, since the reproducible fail is there.

Candidate SHA: none pushed (branch `w140-0428-249-demo-confirm-candidate-fix` @ b4112772, 0 commits). No PR opened, awaiting the coordinator decision above to avoid a blind consent-behavior change.
