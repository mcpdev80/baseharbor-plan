# Evidence — mission native-probe (board-2026-10-31)

Lane: native-probe (worktree /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/native-probe, repo baseharbor)
Date: 2026-11-01
Goal: BEWEISEN, dass der native Docker-Durchspiel-Lauf auf GitHub-hosted mit Endpoint-Fix #1245 (head c201c516) + System-daemon-Skript #1239 (work/gh-ci-core head 486abbca) ECHT GRUEN wird. Kein Produkt-PR; PRUEF-Kandidat + Push-Mode 'Targeted HA · docker'.

## PLAN
- [x] 0. Todo-Plan in nativem Tool + hier angelegt; Worktree und Baseline verifiziert
- [x] 1. fetch origin develop, pull/1245/head, pull/1239/head, work/gh-ci-core — SHAs bestätigt:
      - pr-1245 head = c201c51624300206a00226da88afed5e68abaa86 (fix(runtime): resolve the ACTIVE Docker context …)
      - work/gh-ci-core head = 486abbca1b298b4980912ddaa94565add718f5e5 (#1239, ci.yml + ci-core-rootless-runtime.sh)
      - origin/develop = cb6b73875f478b6be5624412fb9f4c3695e51518
- [x] 2. Merge --no-ff pr-1245 in probe/int0427 -> 049adc0b61e85c9d5064812ebab88a9f3d89a5c6 (nur internal/runtime/docker_engine{,_test}.go, clean)
- [x] 3. Merge --no-ff work/gh-ci-core -> 0f6c5dab611741ae17f7af779eeeae1ae9786242 (.github/workflows/ci.yml, nextjs-greenfield-e2e.yml, scripts/ci-core-rootless-runtime.sh, scripts/test_ci_docker_runtime_doctor.py, clean; disjunkte Write-Sets bestaetigt)
- [x] 4. Lokale Checks: go vet ./internal/runtime OK; go test ./internal/runtime -run 'Docker|Endpoint|Context' ok; ci.yml YAML-parse OK
- [x] 5. Push probe/int0427:refs/heads/runtime-validation/ha/control-plane/docker/int0427 (SAUBER = 0f6c5dab, damit 'Prepare verified rootless runtime' = #1239-Skript laeuft)
- [ ] 6. Run bis terminaler Zustand beobachten; Run-ID + Job-Status + Fehlerzeilen sichern
- [ ] 7. Runtime-Validation-Ref nach terminalem Zustand aufräumen
- [ ] 8. Handoff post

## Kandidat / Trigger
- Kandidat-SHA: 0f6c5dab611741ae17f7af779eeeae1ae9786242
- Branch (lokal): probe/int0427; Remote-Ref: runtime-validation/ha/control-plane/docker/int0427
- Workflow-Run: 41266351533 "CI · runtime-validation/ha/control-plane/docker/int0427"
- Job: "Targeted HA · docker" (job id 124729855022), runner-label ubuntu-latest (GH-hosted, bestaetigt via API: runner_name "GitHub Actions 1000026950", labels ["ubuntu-latest"])
- Paralleler Run 41266351436 "Targeted · Integration · …" wurde mit getriggert (targeted-integration.yml); entscheidender Nachweis ist Job 'Targeted HA · docker' in 41266351533.

## Zwischenstaende (beobachtet, 2026-11-01)
- Steps bis "Reset Docker runtime": success — inkl. "Prepare verified rootless runtime" (#1239-Skript auf GH-hosted ohne Rootless-Provisionierung, System-daemon-Pfad).
- "Run targeted HA acceptance" in_progress (HA-Gruppe control-plane: TestExistingControlPlaneRestartRequiresAndUsesRecoveryFile, Timeout 20m, Job-Timeout 30m).

## Randbefund (NICHT der Entscheidungsnachweis)
- Der parallel getriggerte Run 41266351436 ("Targeted · Integration", targeted-integration.yml) hat einen Job "Targeted runtime · docker" mit conclusion=failure. Das ist ein anderer Workflow/Jobsatz auerbhalb des Missionstempos ("Ziel ist der GH-hosted 'Targeted HA · docker'-Job"). Als Befund dokumentiert; nur bei einem HA-Job-Fehler mit derselben endpoint/rootless-Fehlerzeile waere er zusaetzliche Evidenz fuer eine #1245/#1239-Nachziehung.

## Endstatus
(pendet — wird nach terminalem Run-Zustand von 41266351533 / Job 'Targeted HA · docker' eingetragen)

## Aufraeumen
(pendet)

## Handoff
(pendet)
