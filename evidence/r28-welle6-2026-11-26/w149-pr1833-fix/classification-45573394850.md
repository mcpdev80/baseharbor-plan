# w149 #1833 Docker Light-gate classification (run 45573394850 @ a7b0a4804)

**Lane:** w149-0428-288-pr1833-fix
**Run:** 45573394850 (workflow_dispatch, tag=v0.4.28, demo_ref=b41127723e523134a1c14ee3c36cf133237162ce, only_gates=atomic/docker/{guided,lifecycle,policy,connectivity,reconciliation,failure}, ref=lane-0428-288-compose-ids)
**Exact head:** a7b0a48048c11d20234160eede941532ddc33156 (== PR #1833 head == named branch)
**Date:** 2026-11-25

## Per-card classification

### (a) connectivity / reconciliation -> dependency on demo re-consent fix (NOT a product defect)

Both `Light · docker · connectivity` (job 139069249766) and `Light · docker · reconciliation` (job 139069249808) FAIL.

Root-cause log lines (verbatim, from captured job logs):
- `[ci-operator-testonly] decision=managed-local-gate-rejected: target-resolution-failed: target "atomic-docker-connectivity" is not configured`
- `[ci-operator-testonly] decision=managed-local-gate-rejected: target-resolution-failed: target "atomic-docker-reconciliation" is not configured`
- `Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`
- `demo-connectivity FAIL — … run_consented "$BAHA" app inspect . … "$BAHA" app init --quick` (assertion exit 1)
- `demo-reconciliation FAIL — … cd "$DEMO_ROOT"; run_consented "$BAHA" app apply … "$BAHA" app doctor` (assertion exit 1)
- fixture path absent: `lstat …/baseharbor-demo-fixture…/data/baseharbor/targets/atomic-docker-{connectivity,reconciliation}/runtime/installation.json: no such file or directory`

Classification: INPUT / ENV (demo-fixture) failure. The demo fixture (`baseharbor-demo` @ b41127723) does not provide a consented `targets/atomic-docker-{connectivity,reconciliation}` installation, so `run_consented` refuses and the gate rejects. Same TEST/demo re-consent path the w140 lane found for #1812.

Dependency cited: mission w152 (demo repo, card 0428-249 chain) fixes the demo re-consent. Owner ruling (coordinator, 2026-11-25): this IS the #1812 demo re-consent issue; w152 covers the dependency.

### (b) runtime_light_gates_docker expected-success-got-failure -> SAME root, not separate

The other failing Light gate `Light · docker · policy` (job 139069249859) FAILS with the identical refusal:
- `Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`
- `demo-policy FAIL — … return 1` (assertion exit 1)

So all three Light gates (connectivity 139069249766, reconciliation 139069249808, policy 139069249859) share one root cause: the demo re-consent refusal in the baseharbor-demo fixture. Not a separate product failure.

### (c) policy gate result

`Light · docker · policy` (job 139069249859) = **failure**, same demo re-consent root cause as (a)/(b).

## What is green in the same run (for scope isolation)

Source + unit + static path all terminal / success at a7b0a4804:
- Source · Candidate and Gate Plan, Go Vet, Format and Readability, Go Tests · cli-0/cli-1/cli-2/cli-3/packages, Docs · Workflow and Release Validation, Release · Candidate Artifact, Source · Qualified, Candidate · Runtime Image, HA groups · All runtime results = success.

Only the atomic/Light Docker runtime gates that need a consented demo target fail, on the demo fixture.

## Consequence for #1833

- #1833 product fix (name-map + fail-closed + regression) is present and UNTOUCHED at head a7b0a4804; the pre-release run left the working tree clean.
- Docker + rootless Podman Light-gate requalification CANNOT go green before w152's demo re-consent fix merges and the demo pin (b41127723) is updated. Report this as the END state with the dependency cited.
- #1833 diff stays strictly per-card (internal/application/workload.go, manifest_validation.go, workload_test.go). No move toward #1812/demo files. No consent/auth/authorization bypass anywhere.
- Podman batch NOT yet dispatched; held on the same dependency (w152 fix + demo pin).
