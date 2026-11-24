# 0428-284 post-retry triage (round 1)

Card 0428-284 / repo mcpdev80/baseharbor (+ demo). READ-ONLY triage.
Befund/diagnosis ONLY: NO product edits, NO PR, NO CI trigger, NO rebase of #1812.
Logs from CI run 45398943139 (`Pre-Release · v0.4.27`, `workflow_dispatch`), head branch `lane-0428-249-runtime-image-fix`.

## develop base attestation
- Planning remote (baseharbor-plan): `https://github.com/mcpdev80/baseharbor-plan.git` (verified via `git -C baseharbor-plan remote -v`)
- baseharbor develop (github.com/mcpdev80/baseharbor.git): `f14fb87c8f5afd91168e4f174d620c9f00e6341e` (matches expected f14fb87c8)
- CI run 45398943139 headSha: `47590207518ce9501f1b1bbb115d72d64a206d14` (candidate; NOT develop; owner scope #1812)
- demo_ref on failing gate: `f23b6e09be34601ba542a3087e19b80764a4165d`
- CI manifest schema: `baseharbor.pre-release-runtime-gate-evidence/v1`, gate `atomic/docker/*`, runtime `docker`

## PLAN
- establish develop remote SHA (expect f14fb87c8)
- fetch run 45398943139; identify 4 failing vs 3 passing light-docker gates
- download job logs to /tmp; locate consent-accepted marker per gate
- quote first error AFTER consent-accepted in each failing gate (job | line | file:line | class a/b/c/d)
- compute 3-passing vs 4-failing differentiator step
- determine whether develop f14fb87c8+ already fixes it (re-run risk) or genuinely open
- write round-1.md + minimal fix recommendation + owner-scope flag
- commit+push evidence to baseharbor-plan origin/main; verify path present

## Per-job post-retry failure table
Source: `gh api repos/mcpdev80/baseharbor/actions/jobs/<id>/logs` written to /tmp/runlogs/1812/. The consent retry is the `guided-up-consented` phase (elapsed 135s, then `[phase] guided up: READY reached; returning to acceptance gate`). All four failing gates fail in the SAME phase — the acceptance gate AFTER the consented `up`.

| gate (job id) | consent-accepted marker | first error after it | file:line | class |
| --- | --- | --- | --- | --- |
| policy (138466518597) | `[phase] guided up: READY reached; returning to acceptance gate` @ line 1807 | `Error: operator authentication needs interactive setup but input is not a terminal` @ line 1822; `policy gate unexpected ERR: line=48 exit=2 command=tee \$ARTIFACT_DIR/policy-check.txt` @ line 1824; `demo-policy FAIL / RESULT FAIL` @ lines 1834/1836 | `scripts/acceptance.sh` (demo), line 48 of the operator/acceptance step | **c** — operator-provisioning: the `baha policy check` acceptance step needs OIDC operator auth that is not configured in the CI light-gate env |
| connectivity (138466518757) | same phase marker | `demo-connectivity FAIL / RESULT FAIL` @ lines 1859/1861 (same operator-OIDC wall on the cross-app acceptance step) | `scripts/acceptance.sh` (demo) | **c** |
| reconciliation (138466518674) | same phase marker | `demo-reconciliation FAIL / RESULT FAIL` @ lines 2096/2098 | `scripts/acceptance.sh` (demo) | **c** |
| full-destroy (138466518939) | same phase marker | `demo-full-destroy FAIL / RESULT FAIL` @ lines 1855/1857 (secondary `operator authentication needs interactive setup` in cleanup-preparation, line 2068 of the gate's own log) | `scripts/acceptance.sh` (demo) | **c** |

Note: the earlier `Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate)` @ line 1474 is the PRE-consent first attempt; the gate then re-runs with `--confirm-candidate 89c24dd7118e7994507ab6d0173cf5a7b183f8d27eac143d9118924cad57a5ed` and that consented `up` SUCCEEDS. The first failure AFTER consent-accepted is the operator-OIDC wall.

## 3-passing vs 4-failing differentiator (isolated gate step)
Passing gates: lifecycle (138466518714), failure (138466518846), guided (138466518935). Failing gates: policy, connectivity, reconciliation, full-destroy.

The four failing gates all execute a `policy check` / operator-authenticated acceptance step AFTER the consented guided `up` that the three passing gates do NOT execute:
- lifecycle log @ line 1950: `[OK] operator authentication` then full `Runtime verification` group OK, then `RESULT PASS`.
- policy log @ line 1822: the acceptance phase prints `== Environment and policy ==`, `Policy profile: managed`, effective rules (all DENY), `Operator overrides: none`, then `Error: operator authentication needs interactive setup but input is not a terminal` — the policy gate is the ONLY acceptance step that authenticates the operator via OIDC and then runs `baha policy check` under the managed profile.
- The three passing gates skip the operator-OIDC `policy check` acceptance; they only run the runtime/self verification that does not require operator OIDC.

Differentiator step (quoted): after `[phase] guided up: READY reached; returning to acceptance gate`, the failing gates run `== Environment and policy ==` and call the operator-authenticated policy check; the passing gates go straight to runtime verification. That operator-OIDC policy-check acceptance step is the gate step that fails.

## Root cause class + file:line
- class **c** (operator-provisioning family, 0428-283): the baseharbor `baha` runtime does NOT defect here — the consented `up` completes (workload READY, routes READY, env contract OK). The failure is the ACCEPTANCE gate step that authenticates the operator via OIDC and runs `baha policy check` under the `managed` profile. In CI (no TTY, no `BASEHARBOR_DEMO_OPERATOR_*`/OIDC env), operator auth hits `Error: operator authentication needs interactive setup but input is not a terminal`. This is the operator-provisioning contract the light-gate harness (baseharbor-demo, demo_ref f23b6e09) must supply; baseharbor itself has no defect in the up/apply path.
- Exact failing command: the `operator authentication`/`policy check` acceptance step inside `scripts/acceptance.sh` (baseharbor-demo), reported by the gate as `policy gate unexpected ERR: line=48 exit=2 command=tee \$ARTIFACT_DIR/policy-check.txt`.
- All four failing gates share the same wall; the three passing gates pass because they never invoke the operator-OIDC policy-check acceptance step.

## Re-run risk / develop f14fb87c8+
- The failing candidate SHA `47590207518ce9501f1b1bbb115d72d64a206d14` is the #1812 feature branch head, NOT develop. The root cause lives in the demo light-gate acceptance harness (owner scope, demo_ref f23b6e09) and the operator-OIDC env contract — NOT in baseharbor develop code. A re-run of THIS candidate would repeat (the run is deterministic; the consented `up` succeeded and the policy acceptance step still lacks operator OIDC). develop f14fb87c8+ does not fix this because the defect is in the demo gate/env contract (owner scope), not in baseharbor.
- Therefore re-running #1812 on develop is a no-op repeat for this gate; the fix is an owner-scope change (demo harness / operator env) or a 0428-283 operator-provisioning decision.

## Recommended MINIMAL fix (do NOT implement — owner decision)
- Fix owner-scope (baseharbor-demo): supply the `baseharbor_ci_operator_testonly` operator identity / OIDC env in the light-gate acceptance step (demo_ref f23b6e09, `scripts/acceptance.sh`), so the managed-policy `policy check` acceptance authenticates non-interactively instead of hitting the TTY wall. Owner scope (#1819/#1820/#1818/#1826/consent untouched).
- OR 0428-283 operator-provisioning: decide whether the light-gate `managed` policy profile should require operator OIDC at the acceptance step for atomic CI targets, and the env contract to provide it.
- Repo for the fix: baseharbor-demo (demo harness/env) OR baseharbor operator-provisioning (0428-283), pending owner routing. Owner-scope flag: YES — the failing step is demo-gate/operator-provisioning, not baseharbor runtime.

## What the owner must authorize
- This card is diagnosis only. Any fix to `scripts/acceptance.sh` (baseharbor-demo) or the `baseharbor_ci_operator_testonly` operator/env contract is OUTSIDE this read-only scope and requires a separate task / owner routing. Do NOT re-run #1812 on develop (repeat risk). Do NOT touch #1819/#1820/#1818/#1826/consent.

## Evidence
- evidence path: `evidence/r28-welle6-2026-11-25/0428-284-postretry-triage/round-1.md`
- evidence SHA on origin/main: (verified pre-END via ls-tree)
- logs: /tmp/runlogs/1812/{policy,conn,recon,destroy,lifecycle}_full.log (from `gh api .../actions/jobs/<id>/logs`)
- run 45398943139: `https://github.com/mcpdev80/baseharbor/actions/runs/45398943139`

## cleanliness
- read-only triage; created no containers, compose projects, networks, volumes or state; /tmp/runlogs/1812 is scratch under the approved temp zone. No host runtime touched.

END w97-0428-284-postretry DONE
