# Bug-Hunt Round 1 — trust uninstall prompt EOF

- Lane/Session: 594fd2f5-4e80-43b6-9841-92879146a85e (worker, worker-ornith1.5, via AgentGateway, server host codeman)
- Shift: mission-161 (0427-161)
- Mission: /tmp/opencode/mission-161.md
- Repository: baseharbor (product), checkout /tmp/opencode/mission-161-wt
- Scope: BUGFIX — io.EOF-schutz fuer trust uninstall prompt, PR gegen develop HEAD
- Evidence-Ziel: evidence/bughunt-trust-uninstall-eof-error/round-1.md (in baseharbor-plan, NICHT im Produktrepo)

## PLAN (plain bullets; no markdown checkboxes)

- DONE 1 Remote-Wirklichkeit belegen (develop HEAD cdb4350a6 via ls-remote), saubere worktree auf develop HEAD
- DONE 2 Bug in cmd/baha/trust.go lokalisieren (uninstall-reader Zeile 203-206); install-pfad Zeile 353 schon korrekt
- DONE 3 Bestehende trust-prompt-testzelle studiert (trust_uninstall_test.go)
- DONE 4 Regressionstest geschrieben (uninstall prompt EOF -> 'Host trust unchanged.', kein raw error)
- DONE 5 Fix implementiert: io.EOF-guard im uninstall-reader, identisch zum install-pfad
- DONE 6 Fokalisierte lokale Pruefungen: unit (trust + regressions), go vet, go build
- DONE 7 PR #1485 gegen develop HEAD + branch provenance (ls-remote + ancestry), CI terminal green
- DONE 8 Evidence committen (origin/main), END

## Fakten / Rahrendaten

- Server-Host (Session): codeman; Sessionmodell worker-ornith1.5 bestaetigt via models tool
- baseharbor remote: develop = cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c (ls-remote origin develop, frischer fetch); main = aff1532c2f6c6782a8c13afad83245d1351815e7 (ls-remote origin main)
- PR: #1485 develop -> fix/trust-uninstall-prompt-eof, head SHA 4fcff755e20a72347c4019536710831fcdaaf5e6 (ls-remote origin fix/trust-uninstall-prompt-eof bestaetigt), mergeStateStatus CLEAN
- Branch-provenance: cdb4350a6 (develop HEAD) ist ancestor von 4fcff755e; log listet NUR meine Commits
- go.mod toolchain; CI: GitHub-hosted shared runners, PR workflow
- Produktrepo-NOTIZ: /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor ist QUARANTINE (stale refs) — NICHT als Evidence genutzt; baseharbor-plan ONLY unter /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan

## Bug-Befund (BF-26)

- BF-26 class=EOF-handling datei:cmd/baha/trust.go:203-206
- uninstall prompt ruft `bufio.NewReader(guidedTrustInput).ReadString('\n')` auf; EOF/Strg-D wirft io.EOF; code wrappt dies mit `fmt.Errorf("read host trust removal approval: %w", err)` (Zeile 205) -> reale symptome "read /dev/stdin: input/output error"
- install-pfad (maybeOfferManagedHostTrust, Zeile 352-355) hat korrekten io.EOF-schutz: `if readErr != nil && !errors.Is(readErr, io.EOF) { return readErr }`; EOF -> "Host trust unchanged."
- karte-138-vereinheitlichung: beide pfade sollen bei EOF sauber "Host trust unchanged." ausgeben und nil zurueckgeben

## Fix

- aenderung: cmd/baha/trust.go, trustUninstallCommand, Zeilen 203-211
- io.EOF-guard vor dem answer-match: `if err != nil && !errors.Is(err, io.EOF) { return err }`
- EOF -> answer bleibt leer -> existierende [y/N] != y/yes/ja/j branch -> "Host trust unchanged." -> return nil; exakt identische semantik wie install-pfad

## Regressionstest

- datei: cmd/baha/trust_uninstall_test.go
- TestTrustUninstallPromptEOFAbortsCleanly: trigger = owned anchor record in host-trust.json, guidedTrustInput = strings.NewReader("") (EOF sofort); check: Run==nil, out contains "Host trust unchanged.", host-trust.json unveraendert; fiel vor Fix durch mit "read host trust removal approval: EOF"
- existierende TestTrustUninstallWizardDeclinePreservesOwnedState bleibt gruen

## Lokale Pruefungen (self-run)

- go vet ./cmd/baha/ ./internal/hosttrust/ : OK
- go build -o /tmp/baha-161 ./cmd/baha : OK (exit 0)
- go test cmd/baha -run 'TestTrust|TestBug864|TestBug868|TestBug869|TestBug871|TestBug867|TestBug866|TestBug865|TestOnboarding|TestPrompt|TestAppNewWizard|TestAppApplySecretPrompt' : ok (alle gruen, incl. NEW test)
- go test internal/hosttrust + internal/serviceaccess : ok
- PRE-EXISTING (unrelated, NICHT durch Aenderung): TestAppEditCommandCompleteProviderEditRunsRealLifecycle faellt auch auf clean develop (native Core lifecycle); integration tests require BASEHARBOR_TEST_DATABASE_URL (lokal nicht lauffaehig)

## Hosted CI (self-run, run 42498653903)

- run id: 42498653903; event pull_request; head_sha 4fcff755e
- completed jobs: Workflow policy=success, Source format=success, Trusted Plan=success, Native impact selection=success, Focused Python=success, go-vet=success, go-build=success, cli-gofmt=success, go-unit-tests=success, Native destroy retry (docker+podman)=success
- skipped (scope, core/native 156-domain): Targeted HA docker/podman, Native Keycloak/Core, Public Contracts, Selected Runtime, Runner Interface, Consumer Pins, Exact Candidate, Demo Pin, Release Source Preflight, validate
- KEINE failures. Core-gates (go-unit-tests) gruen.
- Kein .github/** aenderung; kein rerun/workflow_dispatch von mir ausgeloest

## Status

- STATUS: DONE — fix verifiziert (lokal + hosted CI green), PR #1485 OPEN gegen develop; Abnahme/Merge durch Codex (Owner scope); evidence committed
