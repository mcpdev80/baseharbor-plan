# 0428-283 — Demo operator-auth provisioning inventory (READ-ONLY desk, Befund only)

- Lane: w98-0428-283-opinvent
- Date: 2026-11-24
- Model/session: flash worker session (this file is the only artifact; no product edits, no PR, no CI trigger)
- baseharbor origin/develop SHA: f14fb87c8f5afd91168e4f174d620c9f00e6341e (matches the expected f14fb87c8)
- baseharbor-demo origin/develop SHA: c23bd9ac58919302ffad3a43f43afb1a34bfbc96

Planning-repo remote witness (before first evidence commit):

    origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

SHA witnesses (real remotes):

    $ git -C baseharbor ls-remote origin refs/heads/develop
    f14fb87c8f5afd91168e4f174d620c9f00e6341e  refs/heads/develop
    $ git -C baseharbor-demo ls-remote origin refs/heads/develop
    c23bd9ac58919302ffad3a43f43afb1a34bfbc96  refs/heads/develop

## PLAN

1. Done — Verify planning repo remote and fetch real SHAs (baseharbor + baseharbor-demo origin/develop).
2. Done — Read baseharbor gate contract cmd/baha/ci_integration_operator_enabled.go and locate ciIntegrationManagedLocalGateReason.
3. Done — Read .github/workflows/pre-release-runtime-suite.yml build paths — which binary builds carry the operator tag.
4. Done — Inventory demo gate harnesses calling managed baha ops (static/mcp, Light, cleanup, connectivity/reconciliation/other gates).
5. Done — Classify each gate: operator path ENGAGED vs NOT ENGAGED.
6. Done — Derive consolidated single-fix scope, mark owner-scope (.github/product) vs demo-harness files.
7. Done — Write this evidence file in baseharbor-plan (no checkboxes), pull --rebase, commit+push atomically.
8. Done — Verify evidence on origin/main via ls-tree, then post END line.

Evidence-on-origin witness (second-to-last action, exact output):

    $ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle6-2026-11-25/0428-283-operator-inventory
    evidence/r28-welle6-2026-11-25/0428-283-operator-inventory/round-1.md

## The gate contract being tested against

The synthetic test-only operator exists ONLY in binaries built with the Go tag
`baseharbor_ci_operator_testonly` (baseharbor `cmd/baha/ci_integration_operator_enabled.go:1`; the
untagged no-op is `cmd/baha/ci_integration_operator_disabled.go:1`). The injected principal
(`ciIntegrationOperatorContext`, enabled.go:557-564) does NOT enable enforcement; the CLI root does
that always (`main.go:143` `operatorauth.WithEnforcementIfAbsent`, then `main.go:148`
`withCIIntegrationOperator`). Therefore, without the tagged binary, every managed machine operation
hits the fail-closed denial `operator_authentication_required`
(`internal/operatorauth/authorization.go:286-288`, surfaced at `cmd/baha/mcp.go:326-336`:
"Managed-environment machine operations require an authenticated BaseHarbor operator.").

Within the tagged binary, `withCIIntegrationOperator` injects the operator only under:
- `DEMO_ATOMIC_GATE=1` (enabled.go:25), AND
- either the local disposable-gate path whose env contract `ciIntegrationManagedLocalGateReason`
  (enabled.go:96-103) checks: `BASEHARBOR_DEMO_OPERATOR_GATE` set AND equal to the job `GATE` env,
  `BASEHARBOR_TEST_RUNTIME` in {docker,podman}, resolved target name == `atomic-<runtime>-<gate>`
  == `BASEHARBOR_TARGET` env, `AccessProvider == "local"`, no tenant, matching runtime provider —
  and the command admitted either as a `LocalWorkloadOperation`
  (`internal/operatorauth/local_runtime.go:54`, the env-independent app plan/apply/status/destroy
  set) or via one of the ~20 exact gate-scoped literal admissions (enabled.go ~110-255:
  `app new/edit`, `dev domain`, MCP footprint parity, `app logs demo-app` observability,
  `app exec demo-app` identity/security, `config organization set` policy, `policy explain` policy,
  `app inspect .` connectivity, `target -o json` reconciliation (enabled.go:167),
  `app list --all-targets` full-destroy, read-only doctor, root init, root destroy + preview,
  `down` control-plane-recovery), OR
- the bootstrap paths: `target create` for the gate-selected target (enabled.go:34-54,
  `ciIntegrationTargetCreate` enabled.go:540-555) and the local Core bootstrap `up --yes` bound to
  `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT` / the guided fixture root (enabled.go:492-538).
- remote Core targets (`AccessProvider == "baseharbor-core"`) get the operator from enabled.go:54.

`target destroy` is NOT a CLI verb (`cmd/baha/target.go:283-292`: only create/delete/activate/
deactivate; machine ops `target.create`/`target.delete` at `cmd/baha/machine_coverage.go:147`).
`target create` always passes the same authorization seam (`cmd/baha/target_mutation.go:64` →
`authorizeTargetCreation` `cmd/baha/mcp.go:415-430` → `authorizeMCPOperation("target.create")`).
`target delete` routes to `changeTargetDefinition` (`cmd/baha/target.go:598-634`) and is NOT in
`LocalWorkloadOperation`; the tagged binary admits it nowhere. `target activate/deactivate` persist
selection only (`cmd/baha/target.go:295-350`) — no operator.

The workflow env contract (the only place that sets it) is
`.github/workflows/pre-release-runtime-suite.yml:312` (`export BASEHARBOR_TARGET="atomic-…"`) and
`:322` (env line: `BASEHARBOR_DEMO_OPERATOR_GATE="$GATE"`, `BASEHARBOR_DEMO_OPERATOR_TRACE=1`,
`GATE="$GATE"`, `DEMO_ATOMIC_GATE=1`, `BASEHARBOR_TEST_RUNTIME`) inside the "Run runtime gate" step
(class == runtime; `GOFLAGS: -tags=baseharbor_ci_operator_testonly` at :304, used only by the
source-build fallback when no `candidate_artifact` is passed). The demo harness itself never sets
any of these: `grep -rn DEMO_OPERATOR_GATE baseharbor-demo/ tests scripts` is empty.

Candidate-binary provenance:
- Tagged testonly binary exists in artifacts `pre-release-source-candidate`
  (`pre-release.yml:499-513`) and `pr-exact-candidate-<head>` (`ci.yml:1145`); both are
  propagated into `pre-release-runtime-candidate` (`pre-release.yml:599-631`).
- `pre-release-runtime-suite.yml:315-319` uses it ONLY when `candidate_artifact != ''`.
- Static gate path (`:271-277`) always uses the UNTAGGED binary: artifact `baha`
  (`chmod …/pre-release-candidate/baha`, :272-273) or a plain
  `go build -trimpath -o …/atomic-bin/baha ./cmd/baha` (:276). No gate-name exception exists.

## Inventory table (gate | file:line | env | binary tag? | operator ENGAGED? | owner-scope?)

ENGAGED = the step's baha invocation reaches a verified principal without interactive OIDC.
NOT ENGAGED = would hit "requires an authenticated operator" (tagged binary absent and/or env
contract unsatisfied). The mission's "run.sh:48" pointer for the Light policy step lands on
`tests/atomic-bootstrap.sh` content in current develop (run.sh:48 is a comment); real lines are given.

| gate | file:line | env | binary tag? | operator ENGAGED? | owner-scope? |
| --- | --- | --- | --- | --- | --- |
| atomic docker/podman — every runtime gate (fixture bootstrap) | baseharbor-demo `scripts/acceptance.sh:50` (`baha target create "$BASEHARBOR_TARGET"`) | workflow env line `pre-release-runtime-suite.yml:322` + target `:312` gives gate contract | YES (prebuilt `baha-ci-operator-testonly`, :313-319) | ENGAGED — target-create bootstrap branch enabled.go:34-54 + `ciIntegrationTargetCreate` :540 | no |
| atomic docker/podman — every runtime gate (atomic bootstrap) | baseharbor-demo `tests/atomic-bootstrap.sh:14` (`target create`), `:15` → `tests/core-bootstrap.sh:10` (`up --yes`), `:14` (`doctor`), `:16` → `tests/guided/drive.py` (fixture) | same env contract; allowed-root `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT` set at core-bootstrap.sh:9 | YES | ENGAGED — bootstrap branch enabled.go:492-538 + read-only doctor admission | no |
| Light policy gate | `tests/atomic-bootstrap.sh:14` + `tests/policy/run.sh:45` (`config organization set`), `:48` (`policy check`), `:47` (`policy explain`) | full contract via runtime-gate env line | YES | ENGAGED — gate-scoped literal admissions enabled.go ~196-204 | no |
| Light full-destroy cleanup + gate | `scripts/acceptance.sh:89` (cleanup trap `baha destroy --all --yes`), `tests/guided/run.sh:34`, `tests/full-destroy/run.sh:9` (`app list --all-targets`), `:12` (`destroy --all --yes`), `:16` | full contract via runtime-gate env line | YES | ENGAGED — root destroy/preview admissions (enabled.go:231-234) + full-destroy `app list --all-targets` literal (~:208) | no |
| Light connectivity | `tests/connectivity/run.sh:15`/`:73` (`app destroy --yes --full-reset` — in LocalWorkloadOperation via app-verb), `:52` (`baha connect` — app.connection-class) | full contract via runtime-gate env line | YES | ENGAGED (app destroy via workload set; connect rides the same gate target) | no |
| Light reconciliation | `tests/reconciliation/run.sh:13` (`baha target -o json`) | full contract via runtime-gate env line | YES | ENGAGED — reconciliation-scoped `target-output-json` literal, enabled.go:167 | no |
| Heavy gates (data-capabilities, observability, identity, security, backup-restore) | backup-restore's own `target create` at `tests/backup-restore/run.sh:38` (non-atomic branch :32) + gate ops | full contract via runtime-gate env line | YES | ENGAGED — bootstrap branch | no |
| static/mcp | `pre-release-runtime-suite.yml:271-277` dispatch (`bash "$workdir/tests/mcp/run.sh"`, BAHA = untagged) → `tests/mcp/new-edit-static.py:83` (`baha target create mcp-static`), `:87` (`init --quick`), MCP `app.new/app.edit/app.footprint.show` calls at :91-100 | runtime=static; NO `BASEHARBOR_TEST_RUNTIME`, NO `GATE`, NO `BASEHARBOR_DEMO_OPERATOR_GATE`, NO `DEMO_ATOMIC_GATE` | NO — untagged artifact `baha` or plain `go build` | NOT ENGAGED — no tag → no injection at all; even tagged, env contract unsatisfiable (target `mcp-static` ≠ `atomic-<runtime>-<gate>`) | workflow build branch (owner-scope) + product contract |
| static init | `tests/init/run.sh:24` (`target create init-source-fixture`), `:30`/`:35`/`:43` (`init --quick`), plus `baha app inspect .` :17-18 | runtime=static, no gate contract | NO | NOT ENGAGED — would hit operator denial without the trusted-local grant (see RISK note) | workflow build branch + product contract |
| static shell-ux | `tests/shell-ux/run.sh:17` (`target create shell-ux-static`, provider docker) | runtime=static, own XDG + `BASEHARBOR_TARGET=shell-ux-static` :15 | NO | NOT ENGAGED | workflow build branch + product contract |
| static config-matrix | `tests/config-matrix/run.sh:30` (`up --yes` Core bootstrap in temp root) — no target create (inherits `demo-docker`) | runtime=static, no allowed-root/env contract | NO | NOT ENGAGED | workflow build branch + product contract |
| static agent | `tests/agent/run.sh:8` (`agent describe -o json`, read-only, unregistered) | runtime=static | NO | N/A — no managed machine op invoked; unaffected | — |
| reference journey (workflow_dispatch, targeted-integration/targeted-demo-acceptance) | `scripts/acceptance.sh:50` + full suite gate scripts incl. `tests/guided/run.sh:43` | env block sets NO `DEMO_ATOMIC_GATE`/`GATE`/`BASEHARBOR_DEMO_OPERATOR_GATE`; `BASEHARBOR_PREBUILT_BINARY` = plain untagged `baha` (`targeted-demo-acceptance.yml:340-344`) | NO | NOT ENGAGED unless a trusted local runtime grant satisfies every step (journey gates pass today, so the trusted-local path evidently covers local dev there) | workflow env (owner-scope) |
| debug-/recovery harnesses (not CI-dispatched) | `tests/debug-restore-demo-route/run.sh:22`, `tests/debug-keycloak-runtime/run.sh:20`, `tests/debug-reconciliation-runtime/run.sh:22`, `tests/debug-restore-route/run.sh:20` (`target create` + `destroy --all`) | manual/diagnostic only, no contract | n/a | NOT ENGAGED (documented; not a CI gate) | demo repo |

## RISK note — why "just use the tagged binary everywhere" is the wrong fix

`cliLocalWorkloadOperation` (`cmd/baha/main.go:158-183`) classifies root `up` → apply and root
`init --quick` → app.adopt as local-workload ops, so on host-local targets the real
in-process runtime grant (`verifiedLocalWorkloadAuthority`, `cmd/baha/local_workload_authority.go:53`)
already satisfies them fail-closed-checked without any operator. The synthetic operator does NOT
satisfy `secret.reveal` (`RequireHumanOperator`, `internal/operatorauth/authorization.go:326-338` —
only a human issuer-verified principal). A fix that routes static/mcp through the tagged
synthetic-operator path must be re-checked against this seam, or it weakens fail-closed behavior.

## Consolidated one-fix scope (owner decision input)

Single minimal change that clears BOTH #1826 static/mcp and the #1812 Docker/Podman Light gates
without per-gate red rounds, preserving fail-closed:

1. Workflow build-branch tagging (OWNER-SCOPE, `.github/**`):
   - `.github/workflows/pre-release-runtime-suite.yml` "Run static gate" step, lines 271-277:
     when `candidate_artifact` is set, export
     `BAHA="$RUNNER_TEMP/pre-release-candidate/baha-ci-operator-testonly"` (artifact existence is
     already guaranteed by `pre-release.yml:499-513` / `ci.yml:1145`); in the source-build fallback
     (line 276) add `-tags=baseharbor_ci_operator_testonly`.
     Same file, lines 185-187 / :271-277 are the only feeding build paths for static gates.
2. Demo harness env/target lines (DEMO repo — baseharbor-demo, worker-executable):
   - `tests/mcp/new-edit-static.py:75-78` (env dict) + `:83`: adopt a contract-satisfiable target
     name/runtime, or add a narrow `DEMO_MCP_STATIC_GATE`-style admission; must not reuse
     `atomic-*` names outside their gate (collision with parallel runtime gates).
   - `tests/init/run.sh:24`, `tests/shell-ux/run.sh:15-17`, `tests/config-matrix/run.sh:30` and
     `scripts/acceptance.sh:45/50`: same treatment if those static gates show the same denial once
     the tagged binary is used (they currently rely on the trusted-local grant — see RISK note).
3. Product contract (BASEHARBOR repo, go decision): if any admitted static path is not already in
   the LocalWorkloadOperation set or a gate-scoped literal, extend
   `cmd/baha/ci_integration_operator_enabled.go` with the minimal exact-gate admission (pattern:
   enabled.go:167 reconciliation `target -o json`), keeping `ciIntegrationManagedLocalGateReason`
   untouched.
4. NOT recommended as the one fix: switching static gates to the trusted-local path or injecting a
   principal into `mcp serve` child processes — both touch `main.go`/`local_workload_authority.go`
   trust behavior and weaken the fail-closed boundary.

Files that are owner-scope (.github / product contract) vs demo-harness:
- owner-scope: baseharbor `.github/workflows/pre-release-runtime-suite.yml` (static gate step).
- baseharbor product (needs the engineering decision, merge like any PR): `cmd/baha/ci_integration_operator_enabled.go`.
- demo-harness: baseharbor-demo `tests/mcp/new-edit-static.py`, `tests/init/run.sh`,
  `tests/shell-ux/run.sh`, `tests/config-matrix/run.sh`, `scripts/acceptance.sh`.

## repo-rule compliance

- Read-only desk: no edits to any product repo, no branches, no PRs, no CI triggers, no local test
  execution, no subagents. Only this evidence file is written, in baseharbor-plan.
- Remote truth witnesses used: the `git ls-remote origin refs/heads/develop` lines at the top of
  this file for both product repos; all source reads were `git show origin/develop:<path>` / reads
  of the fetched baseharbor-demo develop checkout.
- Language: cards and code in English per AGENTS §3.3.7.

## cleanliness

- Read-only desk, no test stack started. pid witness: this lane shell PID 3795475.
  `docker ps -a` and `podman ps -a` were taken before and after the session's work; both diffs are
  empty (DOCKER-UNCHANGED / PODMAN-UNCHANGED witnesses above; only pre-existing ambient entries,
  e.g. `baseharbor-pre-release-registry`, remain untouched). Nothing created, nothing to bring down.

END_DONE w98-0428-283-opinvent: operator-path inventory complete; static/mcp NOT ENGAGED (untagged binary + no env contract), all atomic docker/podman Light+Heavy gates ENGAGED; consolidated one-fix scope in round-1.md; no candidate branch (read-only desk, evidence-only).
