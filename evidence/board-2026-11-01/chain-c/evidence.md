# chain-c Evidence — Kettenglied-Qualifikation

## PLAN
- Plan 0: Mission lesen, Evidence-Datei erstellen, todo-Liste anlegen
- Plan 1: PR #1247 (work/acc-podman) — rebase + push + native qualification
  - 1a: Rebase on origin/develop → 80a16138 ✓
  - 1b: Push work/acc-podman ✓
  - 1c: Check PR CI → PR Selected Checks fail (workflow-design Grund)
  - 1d: Push 3 runtime-validation/* branches for native qualification
  - 1e: Observe 3 workflow results until terminal → ALL FAILURE
  - 1f: 3 RUNS ROT → END_BLOCKED mit Fehlerzeile

## Ergebnis

### PR #1247 (work/acc-podman)
- **State**: open, base=develop, head=work/acc-podman
- **Branch SHA**: 80a16138 (after rebase on origin/develop)
- **Rebase**: Clean, no conflicts. 1 commit on top of develop.
- **Push**: origin work/acc-podman force-with-lease → 80a16138 ✓
- **PR CI** (Run 41334178631): PR Selected Checks fail → workflow-design Grund
- **Native qualification push** (3 workflows, push trigger, built-in ref):

#### 1. Runtime · Podman Core (41335125682) → **FAILURE**
  - podman-quadlet: **failure** — "Verify Podman Quadlet runner" step failed
  - Step failure: `test -n "$generator"` — kein Podman System-Generator/Quadlet auf GitHub-hosted Runner verfügbar
  - Alle anderen Steps: skipped (Kaskadenfehler)
  - **Fehlerzeile**: `Verify Podman Quadlet runner: failure — Kein Generator gefunden (podman-system-generator, podman-system-generator, /usr/libexec/podman/quadlet)`

#### 2. Acceptance · MCP Lifecycle (41335132272) → **FAILURE**
  - docker: **failure** — "Run generic-client lifecycle acceptance" step failed
  - podman: skipped
  - **Fehlerzeile**: `Run generic-client lifecycle acceptance: failure — TestMCPGenericClientRealApplicationLifecycle scheitert auf GitHub-hosted Runner`

#### 3. Acceptance · Observability Full Stack (41335138959) → **FAILURE**
  - docker: **failure** — "Run focused full-stack observability acceptance" step failed
  - podman: skipped
  - **Fehlerzeile**: `Run focused full-stack observability acceptance: failure — TestObservabilityFullStackAcceptanceInCI scheitert auf GitHub-hosted Runner`

### Chain assessment
- **PR #1247 BLOCKED**: Die GitHub-hosted Runner haben keine native Podman/Quadlet-Infrastruktur und kein lauffähiges Docker für die Test-Workflows.
- **Alle drei nativen Qualifizierungsläufe ROT**: Dies ist ein echter Testfehler, kein workflow-design-Grund.
- **Die PR-Änderungen sind syntaktisch korrekt** (actionlint, ci-policy, ci-executor-verifier-tests, pr-planner-tests, receipt-execution-tests, Focused Python, Trusted Plan, Workflow policy — ALLE GREEN), aber die Runtime-Akzeptanz-Tests scheitern an der Runner-Infrastruktur.
- Die Qualifikation von PR #1247 erfordert, dass baseharbor auf GitHub-Hosted-Runners native Podman/Quadlet-Unterstützung erhält.
- PR #1244 und #1241 hängen von der Qualifikation von #1247 ab — die gesamte chain-c ist BLOCKED.

## END_BLOCKED line
```
chain-c: PR #1247=blocked (3 native qualification runs fail: podman-quadlet runner missing, docker tests fail on GitHub-hosted runners) runs=41334178631,41335125682,41335132272,41335138959 | END_BLOCKED
```
