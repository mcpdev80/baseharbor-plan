# PLAN — o1240-sslguard

## Task-Vertrag
Mission o1240-sslguard: Regression-Guard-Test fuer PR #1240 (openbao->postgres
TLS/SASL) ergaenzen. Review-A-Punkt 2: "fuege einen Regression-Guard hinzu, der
zukuenftige Downgrades blockiert."

## EXKLUSIVES WRITE-SET
NUR eine (neue) Test-Datei. NICHT: openbao_runtime_prepare.go, docker_engine.go,
.github/workflows/*.

## Abkrenzkriterien (Akzeptanz)
1. Neue Test-Datei, die failt, falls jemals sslmode=off|trust|verify-none oder
   PGSSLMODE=off|trust|disable in openbao_runtime_prepare.go (bzw. HCL/Init-
   Skript-URLs) auftaucht. verify-ca/verify-full werden ausdruecklich zugelassen.
2. Test laeuft isoliert: `go test ./internal/runtime -run <Name>`, kein
   Docker/Daemon (reine String-/Quelltext-Pruefung).
3. `go vet ./internal/runtime` saubér.
4. ECHTER Commit gepusht (40-hex SHA) + go test PASS auf Disk.

## Schritte
0. [ ] Evidence-Ordner + PLAN anlegen, Remote-Zustand/Branch verifizieren
1. [ ] Neue Test-Datei openbao_sslmode_guard_test.go schreiben
2. [ ] Lokal: go test ./internal/runtime -run TestOpenBaoSSLModeGuard (gruen)
3. [ ] Gegenbeweis: absichtlich sslmode=off einbauen -> Test rot -> rueckgaengig
4. [ ] go vet ./internal/runtime
5. [ ] Commit + Push auf work/o1249b-openbao-cauth
6. [ ] Evidence dokumentieren + HANDOFF (END_DONE)

## Repo-Regel-Konformitaet
- Go 1.26.9 Toolchain, Package `runtime`, import path
  github.com/mcpdev80/baseharbor/internal/runtime.
- Nur Test-Datei geschrieben; Produktionslogik unangetastet.
