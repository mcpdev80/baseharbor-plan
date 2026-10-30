# cutoverb2 — §6.1 Bootstrap-Selbstqualifizierung #1226 · BLOCKED mit Trigger

**Lane:** cutoverb2 (Fortsetzung der cutoverb-Aufgabe)
**Worktree:** `/home/marcel/dev/baseharbor-ecosystem/worktrees/cutover`
**Branch (Fix-Kandidate):** `work/r27-receipt-enforcement` → Fix-SHA `d2fc3432`
**Bootstrap-Branch:** `runtime-validation/ci/pr-gate/1226` (push-getriggert)
**Repo-Regeln:** baseharbor/AGENTS.md + docs/DEVELOPMENT_GUIDELINES.md
**Zeitraum:** 2026-10-30

## Kontext (Anweisung Coordinator 23:4xZ, Run 41081616567)

Focused Python ist HEIL (Extraktor behoben). Einziger Rest: §6.1 Bootstrap-Selbstqualifizierung — der PR darf seinen eigenen `ci.yml`+runner-Diff nicht selbst qualifizieren. Muster aus #1220 (core-766):
1. Push `HEAD:refs/heads/runtime-validation/...` für einen push-getriggerten Lauf,
2. Lauf bis terminal beobachten (`gh run watch`), Run-ID + Runner-Kontext in Evidence,
3. PR-Body um diesen Qualifizierungs-Nachweis erweitern,
4. Branch rebasen (`origin/develop` rein), EXAKTE SHA push nach `ls-remote`, Selected-Checks terminal zeigen.

## PLAN

1. Bootstrap-Muster (#1220/core-766) gegen die Live-CI verifizieren.
2. Push des Fix-SHA auf einen push-getriggerteten Branch (Trigger `push: branches: [runtime-validation/ci/**]`).
3. Lauf 41083351842 bis terminal beobachten.
4. Fehlerursache gegen #1225 (w750b) abgleichen.
5. Status auf `blocked mit Trigger` drehen; Evidence-Eintrag; nichts weiter pushen; Lane wartet auf Owner-Nudge.

## Bootstrap-Ausführung

Branch `runtime-validation/pr-gate/1226` triff den CI-`push`-Trigger **nicht** (nur `ci/**`, `source-preflight/**`, `ha/**` sind gelistet). Korrigiert auf **`runtime-validation/ci/pr-gate/1226`** — Push landete, Lauf #3993 (API-ID `41083351842`) startete.

### Lauf 41083351842 (terminal, FAILED)

```
$ gh run watch 41083351842 --repo mcpdev80/baseharbor
```

Jobs:
- ✓ Workflow policy — 24s (ID 124157971372)  ← CI-only Gate, kein Docker
- ✗ validate — 5m0s (ID 124157971824)  ← fehlgeschlagen in „Run runtime integration tests serially"
- (geskippt/0s): alle PR-Pfad-Jobs — Focused Python, PR · Receipt Approval, Exact Candidate, …

Fehlerursache im `validate`-Log (Schritt „Run runtime integration tests serially", `go test -p 1 ./cmd/baha ./internal/application -run '^(TestRepositoryWorkflowRealLifecycle|TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI|…)$'`):

```
app_repository_integration_test.go:27: compose runtime unavailable:
  selected Docker endpoint unix:///run/user/1001/docker.sock is unavailable;
  start its rootless daemon or correct the Target endpoint/context;
  no fallback to System Docker
--- FAIL: TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI (0.09s)
--- FAIL: TestRepositoryComposeWorkloadOnlyLifecycleInCI (0.11s)
--- FAIL: TestRepositoryBuildWorkloadRebuildsSourceChangesInCI (0.10s)
--- FAIL: TestMultiInstanceComposeLifecycleInCI (0.10s)
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	0.406s
```

Host-Zustand zum Fehlerzeitpunkt verifiziert: `/run/user/1001/docker.sock` existiert nicht, `docker info` → **docker UNAVAILABLE auf dem Host**.

## Diagnose (verifiziert)

Der `validate`-Fehler ist **nicht deins**: es ist exakt der Kontext-Fehler „kein lauffähiger Docker-Runner", den **#1225 (w750b)** gerade repariert. Die Tests SKIP/FAIL allein an der nicht erreichbaren Docker-Socket, **nicht** am Fix-SHA `d2fc3432`.

- **Meine ci.yml-Änderung ist davon unberührt:** Der Fix (`PY`-Heredoc-Terminator + sauberer `with open()`-Block, `pr_gate_receipt_approval` als eigenständige Job-Einheit) ist byte-identisch auf `runtime-validation/ci/pr-gate/1226` verifiziert (`git diff origin/work/r27-receipt-enforcement FETCH_HEAD` leer).
- **CI-only Gates sind grün:** Workflow policy, unit/package tests (`go test ./...`), gofmt, MkDocs EN/DE strict, actionlint — alles bestanden, bevor der Docker-Integrationsschritt greift.
- **§6.1-Blockade sekundär:** `pr-required-final.py` meldet `coverage-unresolved: .github/workflows/ci.yml; scripts/pr-check-runner.py; scripts/pr-receipt-enforcement-check.py`. Diese Blockade löst sich nur über eine **native (docker/podman)-Qualifizierung**, die wiederum einen lauffähigen Docker-Runner voraussetzt. Solange der Runner down ist, kann der Bootstrap-Nachweis nicht erbracht werden.

## Beweise Nr. 6+ (Bootstrap-Selbstqualifizierung #1226)

1. **Bootstrap-Beweis fehlt (Blockade):** Lauf 41083351842 FAILED an Docker-Runner-Verfügbarkeit, nicht am Fix. Kein grüner nativer Qualifizierungslauf vorhanden.
2. **Fix-SHA `d2fc3432` byte-identisch** auf `runtime-validation/ci/pr-gate/1226` (`git diff` gegen `origin/work/r27-receipt-enforcement` = leer).
3. **CI-only Gates grün:** Workflow policy (ID 124157971372), unit tests, gofmt, MkDocs strict, actionlint — bestanden vor Docker-Integration.
4. **Fehlerursache = #1225 (w750k/w750b)-Kontext:** `unix:///run/user/1001/docker.sock` unavailable; Host docker UNAVAILABLE verifiziert.
5. **PR #1226 Receipt-Gates grün** (Run 41081616567): ✓ PR · Receipt Approval (ID 124151933563), ✓ PR · Focused Python (ID 124152018370) — der Receipt-Vertrag funktioniert; der §6.1-Nachweis ist die offene Lücke.
6. **Self-qualification restricted:** `pr-required-final.py` blockiert `.github/workflows/ci.yml` + runner-Diff als `coverage-unresolved`; native Qualifizierung erfordert lauffähigen Docker-Runner.

## Status: blocked mit Trigger (WAIT #1225)

- **Ursache extern:** Docker-Runner auf dem Self-Host-Host nicht lauffähig (#1225/w750b); nicht beherrschbar aus dieser Lane.
- **Trigger:** **#1225 merge** → dann **Rebase `origin/develop` rein** auf `work/r27-receipt-enforcement` + **neuer Bootstrap-Push** (`runtime-validation/ci/pr-gate/1226`, Fix-SHA behalten) → **`gh run watch`** bis terminal → bei Docker-Runner-grün: Run-ID in PR #1226-Body nachtragen → Branch rebasen + EXAKTE SHA push nach `ls-remote` → Selected-Checks terminal zeigen.
- **Nichts weiter gepusht.** Die Bootstrap-Branch `runtime-validation/ci/pr-gate/1226` bleibt als Lauf-Zeugin bestehen; kein neuer Push, kein Rebase, bis Owner den Freigabe-Nudge gibt.

## END cutoverb2 WAITING

- Bootstrap-Lauf 41083351842 FAILED an fehlendem Docker-Runner (exakt #1225/w750b-Kontext), **nicht** an `d2fc3432`.
- CI-only Gates grün; PR #1226 Receipt-Gates grün. §6.1-nativer Qualifizierungsnachweis blockiert extern.
- Status auf `blocked mit Trigger` gedreht. Evidence-Eintrag „WAIT #1225 merge, dann rebase+bootstrap v2" hinterlegt.
- Lane wartet auf Owner-Freigabe-Nudge. Kein weiterer Push/Rebase ohne Freigabe.
