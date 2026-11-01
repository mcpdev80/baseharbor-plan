# Evidence — o1240-sslguard

## Ergebnis
Regression-Guard-Test fuer PR #1240 (openbao<->postgres TLS/SASL) geschrieben.
Review-A-Punkt 2 erfuellt. Exklusives Write-Set eingehalten: nur NEUE
Test-Datei, Produktionslogik (openbao_runtime_prepare.go, docker_engine.go,
.github/workflows) unangetastet.

- Neue Testdatei: `internal/runtime/openbao_sslmode_guard_test.go`
- Commit SHA: `116adb3d6f85f3db5f7439216fb99d2c9b357254`
- Branch: `work/o1249b-openbao-cauth` (Repo baseharbor)
- Gepusht auf origin: `116adb3d... refs/heads/work/o1249b-openbao-cauth`

## Akzeptanzkriterien
1. Test failt bei sslmode=off|trust|verify-none oder PGSSLMODE=off|trust|disable,
   laesst aber verify-ca/verify-full zu. ✔ (Gegenbeweis unten, rot nach Injection)
2. Isoliert: `go test ./internal/runtime -run TestOpenBaoSSLModeGuard`, kein
   Docker/Daemon (reine String-/Quelltext-Pruefung). ✔
3. `go vet ./internal/runtime` saubér. ✔ VET_OK
4. ECHTER Commit gepusht (40-hex SHA) + go test PASS auf Disk. ✔

## Beweis: go test PASS (gruen) auf Disk
$ cd internal/runtime (Package `runtime`)
$ go test ./internal/runtime -run TestOpenBaoSSLModeGuard
ok  github.com/mcpdev80/baseharbor/internal/runtime  0.005s   [PASS]

$ go vet ./internal/runtime
VET_OK

## Gegenbeweis (rot nach absichtlicher Injection, rueckgaengig)
- Backup: `cp internal/runtime/openbao_runtime_prepare.go /tmp/obp_backup.go`
- Injection: DSN RawQuery von `sslmode=verify-ca&sslrootcert=...` auf
  `sslmode=off` geaendert.
- $ go test ./internal/runtime -run TestOpenBaoSSLModeGuard
  --- FAIL: TestOpenBaoSSLModeGuard
  openbao_sslmode_guard_test.go:68: insecure PostgreSQL TLS mode "sslmode=off"
  must never appear on the openbao<->postgres path
  [TEST ROT wie gefordert]
- Rueckgaengig: `cp /tmp/obp_backup.go internal/runtime/openbao_runtime_prepare.go`
  -> DSN wieder `sslmode=verify-ca`.
- $ go test ./internal/runtime -run TestOpenBaoSSLModeGuard
  ok  github.com/mcpdev80/baseharbor/internal/runtime  0.004s   [PASS]
- Produktionslogik bleibt unveraendert (verify-ca), nur Test-Datei geschrieben.

## Reviewer-Sandbox vs. neutraler Produktionspfad
Pruefung gegen den echten Produktionspfad openbao_runtime_prepare.go (Go-Source
+ generierte HCL/init.sh-Vorlage). Der Guard liest alle .go-Quellen des
Packages (inkl. eingebetteter HCL/Init-Skript-Vorlagen), schlaegt aber nur seine
eigene Datei vor (verbotene Tokens sind dort als String-Literale hinterlegt).
verify-ca/verify-full werden ausdruecklich zugelassen.

## Git-Verifizierung
$ git ls-remote origin work/o1249b-openbao-cauth
116adb3d6f85f3db5f7439216fb99d2c9b357254  refs/heads/work/o1249b-openbao-cauth
$ git rev-parse HEAD
116adb3d6f85f3db5f7439216fb99d2c9b357254
Commit ist remote gepusht; lokaler HEAD == Remote-HEAD.

## Repo-Regel-Konformitaet
- Go 1.26.9, Package `runtime`, import path github.com/mcpdev80/baseharbor/internal/runtime
- Nur Test-Datei geschrieben; git add nur dieser Datei; kein git add -A.
- Produktionslogik, docker_engine.go, .github/workflows unangetastet.
- Kein Force-Push, keine Branch-Protection-Umgehung.

## END
END o1240-sslguard: DONE — 116adb3d6f85f3db5f7439216fb99d2c9b357254 + openbao_sslmode_guard_test.go + go test PASS + Gegenbeweis
