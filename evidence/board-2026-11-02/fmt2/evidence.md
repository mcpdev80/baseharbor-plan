# fmt2 — Evidence

**Task:** Develop-Formatrückfall beheben — `cmd/baha/podman_doctor_checks_test.go` nicht gofmt-formattiert (Präzedenz #1270).
**Mission file:** `coordinator/missions/fmt2.txt`
**Evidence path (absolut):** `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/board-2026-11-02/fmt2/evidence.md`
**Repo:** baseharbor (fresh GitHub-Worktree in `workers/worktrees/fmt2`)
**Lane-Modell/Session:** Ornith (Worker)
**Base:** `origin/develop` tip `940cc1cd` (Merge PR #1275)

## Lane status
END_DONE. gofmt -w auf der ENE Datei, build+test, PR #1282 work/fmt2 -> develop. CI success (run 41427348336). Merge CODEX-MERGE vorbehalten (AGENTS 5.2).

## CI-Run (Eigenes-Run, Stand 2026-11-02)
- PR: **#1282** `style: gofmt podman_doctor_checks_test.go`, base `develop` (940cc1cd), head `9ea36396` (commit `9ea36396ee25ba4ff9f6291cfd04f4960665b116`).
- URL: https://github.com/mcpdev80/baseharbor/pull/1282 — state OPEN, mergeable MERGEABLE.
- CI run ID **41427348336** —结论 `success` (alle nicht-skip-Gates pass; BEHIND = develop weiter, PR aber mergeable).
- Passing (beobachtet): Trusted Plan(7s), Workflow policy(24s), Demo Pin(4s), Runner Interface(5s), Exact Candidate(50s), cli-build(1m6s), cli-vet(58s), cli-guided-tests(2m14s), source-contracts(49s), Focused Python(2m11s), Selected Runtime lifecycle docker(4m28s), podman(4m31s), Selected Checks(19s).
- Skipped (erwartet für gofmt-only): Consumer Pins, Release Source Preflight, Targeted HA docker/podman, Public Contracts, validate.
- Lokaler Run (vor Push): `go build ./cmd/baha`=0, `go vet ./cmd/baha`=0, `go test -run PodmanRuntimeDoctorChecks`=PASS, alle Podman/Quadlet-Doctor-Tests=PASS.
- Vorab-Prüfung `TestDoctorNotDeployedVersusIncomplete`: FAIL identisch auf clean develop (lebensdocker daemon `unix:///run/user/1000/docker.sock`) → Pre-existing, **nicht** durch gofmt.
- Diff: 1 Datei, 3 Zeilen, rein whitespace (Struct-Ausrichtung 60-62), `git diff --ignore-all-space`=leer.

## PLAN

1. [x] Mission lesen, fresh baseharbor Worktree fmt2 (GitHub origin) klonen, develop-Tip verifizieren.
2. [x] Gehinderte Datei identifizieren: `cmd/baha/podman_doctor_checks_test.go` auf origin/develop (Blob `fd036a65`, `gofmt -l` listet sie).
3. [x] Stale-ref-Klarstellung: alter Local-Mirror hatte develop=5c903560; fresh GitHub-Clone hat develop=940cc1cd (Owner-Bestätigung), Datei present, unformatiert.
4. [x] Scope bestätigt: gofmt ist reine Struct-Ausrichtung (Zeilen 60-62), Inhalt nach whitespace-strip identisch — NUR gofmt -w auf eine Datei.
5. [ ] `gofmt -w` auf der ENE Datei, sonst nichts.
6. [ ] `go test ./cmd/baha -run PodmanDoctor` + build + vet.
7. [ ] Branch `work/fmt2`, Commit `style: gofmt podman_doctor_checks_test.go`, PR gegen `origin/develop` (940cc1cd), PRSC terminal beobachten.
8. [ ] Evidence: bestehende Gate-Bindung `cmd/baha/*_test.go` auf cli-gofmt dokumentieren (NUR dokumentieren, nicht ändern).
9. [ ] Planning-Abschluss + post END_DONE line.

## Befunde (Verifikation, Stand 2026-11-02)

### Zielblob (develop 940cc1cd)
- `git ls-tree origin/develop -- cmd/baha/podman_doctor_checks_test.go` → Blob `fd036a6558f0c43651e8f6a56ab0dbf6ccc361da`.
- `gofmt -l` listet die Datei auf (unformatiert) — bestätigt.
- `gofmt -d` zeigt **nur** Struct-Ausrichtung in Zeilen 60-62 (`Runtime`/`Access`/`Scope` Alignment). Nach `tr -d '[:space:]'` sind alter/neuer Inhalt **identisch** → gofmt ist reine Formatierung, kein Inhalt.

### Stale-ref-Herkunft des ersten Blockers
- Der lokale Base-Mirror `workers/worktrees/podman-gh` hatte `origin/develop` auf `5c903560` (älter als 940cc1cd); daher sah die Datei dort fehl aus.
- Fresh-Clone von `git@github.com:mcpdev80/baseharbor.git` → `origin/develop` = `940cc1cd`, Datei present, unformatiert. Owner-Bestätigung: Datei existiert auf develop-Tip und ist unformatiert.
- Der frühere `pr1274check`/`work/docchk2`-Pfad (`d2094ed3`, "move Podman checks out of cmd/baha") ist ein **anderer** Branch und hier irrelevant — rein develop-Content.

## Gate-Bindung cmd/baha/*_test.go auf cli-gofmt (NUR Dokumentation, §4 Step 4 — nichts geändert)
- **Befund:** In develop gibt es keine *explizite* Gate-Zeile, die `cmd/baha/*_test.go` direkt an `cli-gofmt` bindet; stattdessen greift das generische Format-CI `PR · Selected Checks` / `PR · Validation · cli-build` (bzw. `cli-vet`/`source-contracts`), das `gofmt`/`go fmt`-Prüfungen über die Go-Build-Kette laufen lässt. Deshalb war die gofmt-Abweichung auf develop (Blob `fd036a65`) durch dieses generische Gate sichtbar — und der gofmt-only PR #1282 schlägt dort GRÜN.
- **Konsequenz für die Torseite-NOTIZ:** Die fehlende *dateispezierte* Bindung (`cmd/baha/podman_doctor_checks_test.go → cli-gofmt` als eigener Trigger) ist der Grund, warum #1274 die Datei durchlassen konnte. Eine solche präzisere Bindung ist eine **CI-/Planner-Änderung** und fällt **außerhalb** des fmt2-Scopes (Mission: „NUR gofmt -w", „kein neues Gate", „kein Planner-Change"). **Vorschlag an Owner/CI-Betreiber (nicht umgesetzt):** Gate-Trigger auf `**/*_test.go` (bzw. explizit `cmd/baha/podman_doctor_checks_test.go`) in der Format-CI-Regel verankern — getrennt von diesem Task.

## repo-rule compliance
- NUR `gofmt -w` auf `cmd/baha/podman_doctor_checks_test.go`. Keine andere Datei geändert.
- Kein Gate-/Planner-Change (nur Dokumentation, §4 Step 4). Kein neues Gate.
- Kein Force-Push, keine Branch-Protection-Umgehung.
- Auth: Git-Remote über SSH-Key des Systems (keine Lane-Eigenes-Tokens).
- Kein subagent/codeman-Spawn (Mission STOP).

## Handoff
post `35cdb02e-a3b3-4e6d-86f9-1cbb35822587` "END_DONE fmt2: pr=<n> head=<sha> run=<id> | develop-940cc1cd: gofmt -w auf cmd/baha/podman_doctor_checks_test.go, build+test ok, PR work/fmt2->develop".
