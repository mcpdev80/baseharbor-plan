# MERGE-ORDER + Gate-Mapping-Lücken — integrate-map (read-only)

**Rolle:** ANALYSE (nur lesend; gh api + git, keine Änderung/Gen/Merge/CI)
**Modell:** Ornith · **Zeit:** 2026-11-01 · **Repo:** `mcpdev80/baseharbor`, develop = `cb6b7387`
**Datenbasis:** `gh api …/pulls/<n>/files` + lokales `pr-diff-base.py`-Resolverergebnis auf merge-base→head für JEDES PR, ausgewertet mit `scripts/pr-gate-plan.py` unter (a) Develop-Stand und (b) Branch `work/gate-map` (`9581193d`).

> Reproduzierbar: merge-base lokal (alle PRs teilen develop `cb6b7387` als merge-base), `resolve_pr_diff` → `plan(diff, REQ, MAP, …, context_repository=mcpdev80/baseharbor, context_target_branch=develop)`.

---

## 0. Was die gate-map-Aenderung tut (9581193d)

`scripts/pr-gate-plan.py` erhält eine neue `elif`-Rule **vor** der Resolver-Rule:

```python
elif path.startswith('internal/runtime/') and path.endswith('.go') and not path.startswith('internal/runtime/resolver/'):
    area = 'runtime-docker-engine'
    require(CODE_CHECKS)          # go test ./internal/application/... ./contracts/...
    require(CLI_CHECKS)           # go vet/build ./cmd/baha (über CLI_CHECKS)
    selected.add('atomic/docker/lifecycle')
```

→ Jede Datei `internal/runtime/*.go` (außer resolver/) war unter Develop **„unknown impact“** (fail-closed, kein Gate) und ist nach gate-map mit `atomic/docker/lifecycle` **mapped**. Branch enthält 6 Passendtests (docker_engine.go, openbao_runtime_prepare.go, docker_engine_test.go, Bundle mit unreviewter Datei → fail-closed, resolver/ bleibt unresolved).

**Wichtig:** die Rule mappt `atomic/docker/lifecycle` (docker **only**). Podman-lifecycle (`atomic/podman/lifecycle`) wird **nicht** abgedeckt — nur die go-Tests (`go test ./internal/runtime/...`) laufen lokal; das eigentliche Podman-Gate bleibt eine separate Host-Disposition.

---

## 1. PRO-TABELLE (PR | files | Klassifizierung nach gate-map | Lücke? | braucht-Rebase | braucht-gate-map-add | Merge-Fenster)

| PR | HEAD | files | Klassifizierung (gate-map) | Lücke? | Rebase | gate-map-add | Merge-Fenster |
|----|------|-------|----------------------------|--------|--------|--------------|---------------|
| **#1245** `work/docker-endpoint-context` `c201c516` | `internal/runtime/docker_engine.go`, `internal/runtime/docker_engine_test.go` | `internal/runtime/*.go` → `atomic/docker/lifecycle` (**resolved** nach gate-map) | **nein** (nach gate-map) | 1 commit ahead, 0 hinter | nein | nein (durch gate-map abgedeckt) | **Früh, Blocker für ganze Kette** (siehe Reihenfolge) |
| **#1241** `work/fix-engine-detect` `ed5ca739` | `cmd/baha/docker_engine.go`, `cmd/baha/docker_engine_podman_test.go` | `cmd/baha/*.go` runtime-impact → **`cli-unresolved-runtime-impact`** (beide Dateien) | **JA — ZUSÄTZLICHE LÜCKE** | 1 ahead, 0 hinter | **JA, nötig** | **JA** (cmd/baha/docker_engine.go unmapped) | **Spät, nach 1245** |
| **#1240** `work/o1249b-openbao-cauth` `116adb3d` | `internal/runtime/openbao_runtime_prepare.go`, `internal/runtime/openbao_sslmode_guard_test.go`, `internal/runtime/stack_test.go` | `internal/runtime/*.go` → `atomic/docker/lifecycle` (**resolved**) | **nein** (nach gate-map) | 2 ahead, 0 hinter | optional (sauberer Rebase) | nein | beliebig, früh machbar |
| **#1239** `work/gh-ci-core` `486abbca` | `.github/workflows/ci.yml`, `.github/workflows/nextjs-greenfield-e2e.yml`, `scripts/ci-core-rootless-runtime.sh`, `scripts/test_ci_docker_runtime_doctor.py` | workflow + ci-executor → **unresolved** (alle 4) | **JA — restliche LÜCKE** | 1 ahead, 0 hinter | optional | **teilweise** (nur workflow/exec) | nach 1245 (GH-hosted docker) |
| **#1238** `work/gh-acc-suite` `38073e9e` | `.github/workflows/mcp-lifecycle-acceptance.yml`, `.github/workflows/observability-acceptance.yml`, `.github/workflows/podman-acceptance.yml` | workflow → **unresolved** (alle 3) | **JA — restliche LÜCKE** | 1 ahead, 0 hinter | optional | **JA** (workflow-mapping fehlt komplett) | beliebig, GH-hosted |
| **#1243** `work/gh-dispatch2` `878a2124` | `.github/workflows/runtime-broker.yml`, `.github/workflows/runtime-s3-acceptance.yml` | workflow → **unresolved** (alle 2) | **JA — restliche LÜCKE** | 1 ahead, 0 hinter | optional | **JA** (workflow-mapping fehlt) | beliebig, GH-hosted |
| **#1242** `work/fix-observ-consent` `f392273` | `cmd/baha/app_observability_acceptance_test.go` | `cmd/baha/*.go` → **`cli-unresolved-runtime-impact`** | **JA — restliche LÜCKE** | 1 ahead, 0 hinter | optional | **JA** (cmd/baha-Test unmapped) | beliebig |
| **#1160** `dependabot/go_modules` `6389342d` | `go.mod`, `go.sum` | → **unknown impact** (beide) | **JA — restliche LÜCKE** | 1 ahead, 0 hinter | optional | **JA** (deps-mapping fehlt) | beliebig |
| **#1225** `fix/750-ci-gate-qualify` `5060cb23` | `.github/workflows/ci.yml`, `.github/workflows/podman-acceptance.yml`, `scripts/pr-check-runner.py`, `scripts/pr-gate-plan.py`, `scripts/test_pr_gate_plan.py` | workflow + ci-executor → **unresolved** | **JA — restliche LÜCKE** | **26 ahead, 4 hinter develop** | **JA, deutlich** | **JA** (ci.yml + scripts) | **Früh, Blocker** (integriert pr-gate-plan-Änderung) |

---

## 2. LINEARE MERGE-REIHENFOLGE

Regel (Auflöse-Kette): **erst grüner GH-hosted native Lauf, dann required self-hosted weg** — ein PR deckt seine Coverage nur, wenn das echte native Gate (GH-hosted, rootful docker/podman) schon läuft.

```
1. #1225  fix/750-ci-gate-qualify   (5060cb23)   ← BLOCKER / Fundament
   · Integriert die resolver-Registrierung in den trusted executor + pr-gate-plan-Änderungen.
   · Ohne #1225 findet KEIN PR ein gültiges native Gate (executor kennt die Gate-IDs nicht).
   · 26 ahead / 4 hinter → Rebase auf aktuelles develop erforderlich (4 develop-commits #1233/#1235 etc. nachziehen).
   · DANACH: gh-hosted native CI auf #1225 grün → Gate-ID-Registrierung validiert.

2. #1245  work/docker-endpoint-context  (c201c516)  ← BLOCKER / Fundament
   · Endpoint-Fix: resolver wählt aktive docker-context statt hartem rootless-socket.
   · Ohne 1245 schlägt das GH-hosted docker-native-Gate (rootful daemon) fehl → alle docker-lifecycle-PRs blockiert.
   · Nach Merge: gh-hosted docker-native-grün.

3. #1241  work/fix-engine-detect  (ed5ca739)   ← hängt an 1245
   · cmd/baha/docker_engine.go runtime-neutral für podman. Braucht GH-hosted docker+podman native-run.
   · Nach 1245 + gate-map-add (siehe §3).

4. #1239  work/gh-ci-core  (486abbca)   ← hängt an 1245 (docker-native in ci.yml)
   · ci.yml validate + nextjs e2e → GH-hosted ubuntu-latest (rootful system docker).
   · Nach 1245, damit GH-hosted docker-native echt läuft.

5. #1240  work/o1249b-openbao-cauth  (116adb3d)   ← offen (gate-map-mapped, aber keine reviewed-Bindung)
   · openbao→postgres verify-ca + PGSSLROOTCERT. internal/runtime → gate-map-mapped, aber #1240 ist NICHT OPENBAO_RETRY_HEAD
     (das ist internal/openbao/bootstrap.go, anderes Package). Also: gate-map mapped, aber keine SHA-gebundene Review-Bindung;
     native lifecycle-Run nötig.

6. #1238  work/gh-acc-suite  (38073e9e)   ← offen (workflow-mapping fehlt)
   · acceptance-workflows → GH-hosted.

7. #1243  work/gh-dispatch2  (878a2124)   ← offen (workflow-mapping fehlt)
   · broker + s3 acceptance → GH-hosted (100 % GH-hosted).

8. #1242  work/fix-observ-consent  (f392273)   ← offen (cmd/baha unmapped)
   · konsent-gemäße plan→apply-Abfolge im observability-acceptance-Test.

9. #1160  dependabot/go-jose  (6389342d)   ← offen (deps unmapped, rebase-only clean)
   · go-jose 4.1.4 → 4.1.6. Rebase auf aktuelles develop (dependabot-Branch alt). Kein gate-map-add aus Portabilität, aber Mapping erwünscht.
```

**Dependency-Struktur:** `#1225` und `#1245` sind die zwei Fundament-Blocker. Erst danach öffnet sich die parallele GH-hosted-Serie (`#1239/#1238/#1243`) sowie die runtime-Serie (`#1241` nach 1245, `#1240`, `#1242`). `#1160` ist entkoppelt (rebase-only).

---

## 3. ZÜGLICHE gate-map-Ergänigungen (offene Mapping-Lücken — in gate-map-Lane nachziehen)

| # | Datei (PR) | Status gate-map (9581193d) | Benötigte Ergänzung |
|---|------------|-----------------------------|---------------------|
| **A** | `cmd/baha/docker_engine.go` (#1241) | **UNMAPPED** — fällt in `cli-unresolved-runtime-impact`, `atomic/docker/lifecycle` fehlt | Neue Rule: `cmd/baha/*_engine.go` runtime-impact → `atomic/docker/lifecycle` (podman-Pendant nötig: `atomic/podman/lifecycle`). Test #1241 verlangt beide native Gates. |
| **B** | `cmd/baha/docker_engine_podman_test.go` (#1241) | **UNMAPPED** (neue Test-Datei) | Wie A — podman-native-Abdeckung. |
| **C** | `.github/workflows/*.yml` (alle PRs: 1239,1238,1243,1225,1242) | **UNMAPPED** — `runtime-workflow-unresolved` | PR-Map-Regel für acceptance/runtime-workflows → jeweiliges GH-hosted native Gate (mcp-lifecycle, observability, podman-acceptance, broker/s3). Aktuell nur `docker`-prefix (atomic/docker, ha/docker, integration/docker) in gate-map.json — workflows liegen unter `.github/workflows/` und sind nie gemappt. |
| **D** | `scripts/ci-core-rootless-runtime.sh`, `scripts/test_ci_docker_runtime_doctor.py` (#1239) | **UNMAPPED** — `ci-executor-unresolved` / unknown | CI-executor-/Evidenz-Mapping zum GH-hosted runtime-gate. |
| **E** | `cmd/baha/app_observability_acceptance_test.go` (#1242) | **UNMAPPED** — `cli-unresolved-runtime-impact` | cmd/baha-test → natives acceptance-gate (oder PR-spezifische Review-Bindung). |
| **F** | `go.mod` / `go.sum` (#1160, dependabot) | **UNMAPPED** — unknown | Dependabot-deps-Mapping (rebase-only clean; Portabilität: ggf. nur statisch, kein natives Gate). |
| **G** | `internal/runtime/openbao_*` (#1240) | **MAPPED** (`atomic/docker/lifecycle`), aber **KEINE SHA-gebundene Review-Bindung** | Gate-map deckt den Pfad, aber #1240 ist nicht die reviewed `OPENBAO_RETRY_HEAD` (`internal/openbao/bootstrap.go`, anderes Package). Native lifecycle-Run für openbao→postgres nötig; ggf. reviewed-bindung ergänzen. |

> **Zusammenfassung:** gate-map (9581193d) schließt nur LÜCKE `internal/runtime/*.go` (docker-lifecycle). Offene restliche Lücken: **A,B** (cmd/baha engine-impact), **C** (alle `.github/workflows/*`), **D** (ci-executor scripts), **E** (cmd/baha observability-acceptance-test), **F** (deps), **G** (openbao ohne Review-Bindung). Das sind **7 zusätzliche gate-map-Ergännungen** (G ist mapping-mäßig bereits abgedeckt, aber bindungsoffen).

---

## 4. Rebase-nur (kein Code) vs. gate-map-add

**Nur sauberer Rebase auf develop + gate-map + #1245 (kein Code nötig):**
- **#1245** (1 ahead) — direkt integierbar nach Merge in develop.
- **#1240** (2 ahead) — Rebase auf develop+gate-map+1245; gate-map-mapped.
- **#1243** (1 ahead) — Rebase; workflow-Änderung ist nur runner-swap.
- **#1238** (1 ahead) — Rebase; runner-swap.
- **#1239** (1 ahead) — Rebase; runner-swap + ci-core-runtime.
- **#1242** (1 ahead) — Rebase; Test-Abfolge-Fix.
- **#1160** (dependabot, alt) — **Rebase zwingend** (dependabot-branch hinter develop); kein gate-map-code, aber Mapping-Frage #F.

**Brauchen ZUSÄTZLICHE gate-map-Abbildung (mit Begründung + Datei):**
- **#1241** — `cmd/baha/docker_engine.go` ist im `cmd/baha`-Pfad **nicht** in der gate-map-Dict; classifier wirft `cli-unresolved-runtime-impact`, kein `atomic/docker/lifecycle`. **Datei: `scripts/pr-gate-plan.py`** (neue `elif` für `cmd/baha/*_engine.go`, podman-Pendant `atomic/podman/lifecycle`).
- **#1238, #1243, #1225(ci.yml+podman-acceptance), #1239(ci.yml)** — `.github/workflows/*.yml` sind in gate-map **nie** gemappt (nur `atomic/*,ha/*,integration/*`-prefixes + docs). **Datei: `scripts/pr-gate-map-v1.json`** (workflow-areas) + `scripts/pr-gate-plan.py` (mapping-rule).
- **#1239 (scripts)**, **#1242**, **#1160** — siehe Tabelle §3 (D, E, F).

---

## 5. Nachweise (Witnesses)

- PR-Files + merge-base: `gh api repos/mcpdev80/baseharbor/pulls/<n>/files` (Transkript geführt in `evidence/integrate-map-plan.md`).
- Classifier-Ergebnis (develop vs. gate-map), reproduziert mit `resolve_pr_diff` + `plan()` in `/tmp/run_classify.py` gegen `/tmp/bh-clone` (develop-Checkout).
- gate-map-Diff: `git diff origin/develop..origin/work/gate-map -- scripts/pr-gate-plan.py scripts/test_pr_gate_plan.py`.
- #1241 cmd/baha-Diff: `gh api repos/mcpdev80/baseharbor/pulls/1241/files` (`ensureTargetDockerBinding`/`inspectTargetDockerEngine` → podman, `engineBinaryName`).
- #1225 diverge 26/4: `gh api repos/mcpdev80/baseharbor/compare/5060cb23…develop`.
- Alle PRs offen, nicht gemergt (`state=open, merged=false`).

---

## 6. Repo-Rule-Compliance
- **Nur lesend:** `gh api`, `gh`, `git` (fetch/ls-remote/merge-base/diff/show). **Keine** Änderung, **keine** Merge, **keine** CI-Auslösung, **kein** Push.
- `git clone --no-checkout` + `origin/develop` nur für lokale Resolver-Ausführung der existierenden Skripte; kein Produktbranch verändert.

---

END integrate-map DONE
