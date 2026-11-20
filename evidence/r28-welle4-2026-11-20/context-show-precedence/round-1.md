# 0428-178 context show precedence — regression evidence

## 1. Mission & Scope
Karte 0428-178: Die Produktions-Reihenfolge der context-auswahl (override → shell-env → **persistierte Auswahl** → konfigurierter Default) ist implementiert, aber KEIN Test beweise sie durch den echten CLI-Pfad. Ziel: eine Regression in `cmd/baha/context_terminal_test.go`, die die Kette durchfahrzt, plus Mutation in beide Richtungen, plus CI-Aufnahme.

## 2. Modellidentitaet
- Workersitz (frei geworden), Kanal laptop. Festlegung 'immer Qwen Flash' gilt NUR fuer den Coordinator, nicht fuer Worker-Modelle; Identitaet nicht weiter geprueft (Mission-Weisung).
- Session: f2966474-030f-4c58-be49-22d0ea888dae

## 3. Remote-Realitaet (bas-check witnesses)
- baseharbor-plan remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (correct)
- develop head via `git ls-remote lane-origin refs/heads/develop`: `f5ce95afce1cfec053dd7717ed05e89bfe153535`
- Base SHA (develop head, geschnitten): `f5ce95afce1cfec053dd7717ed05e89bfe153535`
- worktree: `/tmp/opencode/lane-0428-178-contextshow` bei f5ce95af (frisch; der Checkout bei baseharbor-ecosystem/baseharbor war quarantiniert, branch lane-0428-174 mit fremden uncommitted changes)
- PR: #1718, base develop, head aa3c9d2a5b799756837e6238fe82c948778e7a15

## 4. Vier Stufen der echten Praedenzen (Datei:Zeile)
Quelle: `cmd/baha/context_terminal.go:187-213` (effectiveContextOrigin).
Reihenfolge (niedrig -> hoch), Akzeptanz-Kriterium:
1. persisted selection: `:206-210` — `readPersistedTarget()`; `persisted != "" && selected == persisted` => origin "persisted".
2. shell env: `:195-205` — `os.Getenv("BASEHARBOR_TARGET")` => origin "shell-env" (schlaegt persisted, weil vor dem Check).
3. persistierte Auswahl => "persisted".
4. konfigurierter Default: `:211-213` — `cfg.DefaultTarget` => origin "configured-default".
Produktion hat override(`:187-190`) und default(`:211-213`) additionally; die Kette default-vs-persisted ist bei `:206-213` fixiert.
Bestande fehlen der Nachweis durch den ECHTEN 'baha context show'-Pfad:
- `context_terminal_test.go:122-135` (TestContextPrecedenceDefaultFallback) ruft `effectiveContextOrigin` DIREKT auf, nicht 'context show'.
- `context_terminal_test.go:156-163` (TestContextShowReportsWinningStage) uebt NUR die default-Stufe aus.

## 5. TEST
`TestContextShowPersistedWinsOverConfiguredDefault` (cmd/baha/context_terminal_test.go), eingefuegt nach TestContextShowReportsWinningStage.
- configureTestTarget(t) setzt DefaultTarget = "docker-dev" (A).
- configureSecondContextTarget(t) registriert "prod" (damit die persistierte Auswahl existiert).
- writePersistedTarget("prod") setzt B = "prod".
- os.Unsetenv(contextShellVar) — kein env-override.
- runContextShowCommand(t) -> ruft runContextShow (ECHTER command path, nicht effectiveContextOrigin).
- Assert: Output enthaelt "Effective context: prod (persisted)" und NICHT "configured-default".
gofmt clean (gofmt -l cmd/baha leer), go vet ./cmd/baha sauber, go build ./cmd/baha OK.

## 6. MUTATION BEWEIS (beide Richtungen, woertliche Ausgabe ungekuerzt)

### Mutation (a): persistierte Stufe auskommentieren (:206-210) -> DIESER Test ROT
Kommando: `go test ./cmd/baha -run 'TestContextShowPersistedWinsOverConfiguredDefault' -count=1 -v`
Ausgabe (ungekuerzt):
```
=== RUN   TestContextShowPersistedWinsOverConfiguredDefault
    context_terminal_test.go:182: context show must report persisted 'prod' over configured-default, got:
        Effective context: prod (unique-configured)
--- FAIL: TestContextShowPersistedWinsOverConfiguredDefault (0.01s)
FAIL
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	0.021s
```
Beweis: Ohne die persistierte Stufe faehrt effectiveContextOrigin in den "unique-configured"-Zweig; der Test ROT.

### Mutation (b): default-Stufe auskommentieren (:211-213) -> TestContextShowReportsWinningStage ROT
Kommando: `go test ./cmd/baha -run 'TestContextShowReportsWinningStage|TestContextShowPersistedWinsOverConfiguredDefault' -count=1 -v`
Ausgabe (ungekuerzt):
```
=== RUN   TestContextShowReportsWinningStage
    context_terminal_test.go:161: expected configured-default in output, got:
        Effective context: docker-dev (unique-configured)
--- FAIL: TestContextShowReportsWinningStage (0.01s)
=== RUN   TestContextShowPersistedWinsOverConfiguredDefault
--- PASS: TestContextShowPersistedWinsOverConfiguredDefault (0.03s)
FAIL
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	0.116s
```
Beweis: Ohne die default-Stufe faehrt der zweite Test in "unique-configured"; TestContextShowReportsWinningStage ROT.
Beide Mutationen danach zurueckgesetzt (diff wieder identisch zum Original, verifiziert mit diff).

## 7. CI-Aufnahme
Job: `PR · Go unit · cli-2` (ci.yml:1592 shard-Liste; cmd/baha wird via scripts/pr-go-unit-shard.py, ci.yml:1657, in den cli-shards ausgewaehlt).
Run-ID: `44759243414` (event pull_request, head aa3c9d2a5b799756837e6238fe82c948778e7a15).
Terminal conclusion: **success** (run 44759243414 completed).
Job-Conclusion cli-2: **success** (job 136367205376).
Ausgabezeile aus cli-2 Logs (/tmp/cli2-logs.txt):
```
2026-11-20T15:06:31.6292748Z PASS cli-2: 434 passed / 19 intentionally skipped / 453 discovered; CLI inventory total=1784
```
Der Test ist einer der 434 ausgefuehrten (nicht skip); cmd/baha compiliert und fuehrt aus. Kein FAIL in cli-2 (ein "FAIL"-Match ist ein false-positive in einer shell: Zeile).
Andere cli-shards am exakten head cli-0/cli-1/cli-3/cli-2: alle success (jobs 136367205307/136367205137/136367205376/136367205160).

## 8. PROOF WITNESSES
- PROOF 1: `git ls-remote lane-origin refs/pull/1718/head` -> aa3c9d2a5b799756837e6238fe82c948778e7a15 (== branch head aa3c9d2a5b79)
- PROOF 2: `git merge-base --is-ancestor f5ce95afce1cfec053dd7717ed05e89bfe153535 HEAD` -> JA
- PROOF 3: `git log --oneline origin/develop..HEAD` -> nur aa3c9d2a5 (eigener Commit)
- `git diff origin/develop...HEAD --name-only` -> cmd/baha/context_terminal_test.go

## 6. repo-rule compliance
- Write-Set disjunkt zu 0428-187/184/183/083. Nur cmd/baha/context_terminal_test.go.
- KEIN .github/**. KEIN Container/Compose. gofmt/vet/build OK.
- Evidence auf baseharbor-plan main: evidence/r28-welle4-2026-11-20/context-show-precedence/round-1.md (origin/main bestaetigt).

## 10. cleanliness
- vorher: kein git-Arbeitsbaum fuer baseharbor im persistenten Zone; baseharbor-ecosystem/baseharbor war quarantiniert (stale lane-0428-174).
- nachher: worktree /tmp/opencode/lane-0428-178-contextshow (commit aa3c9d2a5, branch lane-0428-178-context-show-precedence); PR #1718 offen.
- Container/Compose/Volumes/Netzwerke: KEINE gestartet, nichts zurueckzulassen.
- ambient-core/ Bilder fremder karren: unangetastet.
- cleanliness: CLEAN — nur Go-Test, kein Runtime-Stack.

## 11. ZUSATZ-FUND (Owner Gate-Regel 2026-11-20, baseharbor-plan/main 51d95b99)
Der Test ist von einem CI-Job erfasst (cli-2, siehe section 7). Der PR ist damit bereit fur die Review; kein separater .github-Bedarf, da cmd/baha im bestehenden cli-shard-Mechanismus lauft.

## END
mission-178.md: DONE — PR #1718 (base develop, head aa3c9d2a5b79), CI run 44759243414 cli-2 success, beide Mutationen rot, Evidence auf baseharbor-plan main.
