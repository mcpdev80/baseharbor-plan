# 0427-166 — Restbefund act-1485: unterminated affirmative + EOF autorisiert uninstall

Runde 2: bug-out unterminated affirmative EOF in der uninstall-Prompt.

## PLAN

- Provenance pinnen, worktree aus origin/develop schneiden
- trust.go uninstall-reader + bestehenden test inspizieren
- reader so ändern, dass EOF ohne trailing newline die eingabe NICHT als antwort wertet
- regression: "y"+EOF verweigert, "y\n" autorisiert, reines EOF verweigert — in der trust-prompt-zelle, CI-erfasst
- lokale go tests auf exaktem head
- drift gegen develop, push, hosted lauf terminal auf exaktem head
- ls-remote + cleanliness, evidence auf origin/main, END in die geteilte inbox

## Provenance

Produkt-repo: `https://github.com/mcpdev80/baseharbor.git` (verified via `git ls-remote`).
Planning-repo: `https://github.com/mcpdev80/baseharbor-plan.git` (`origin` verified).

Planning evidence dir: `baseharbor-plan/evidence/bughunt-trust-uninstall-eof-error/`

Base-SHA (dev, exakt): `d8849198265f13d34e1ece95d6982ce6b613d2aa` — `git ls-remote origin refs/heads/develop`:
```
d8849198265f13d34e1ece95d6982ce6b613d2aa	refs/heads/develop
```
git `merge-base --is-ancestor d88491982 ... <my-commit>` wird bei erstem commit geprüft.

Worktree geschnitten aus origin/develop in `/tmp/opencode/mission-166-wt` (detached HEAD d88491982).

Basis-Commit ist `d88491982`, und dieser ist per Definition mein eigener Ancestor (Branch aus identischem HEAD).

## Befund

Aktuelle develop enthält PR #1485 (commit `cd118d0d1`): der immediate-EOF-fall (leerer reader, Strg-D) wird durch
`err != nil && !errors.Is(err, io.EOF)` sauber abgefangen und mit "Host trust unchanged." (nil) beendet.

Offene lücke (review act-1485, recipe schritt 1): ein ABGEBROCHENER ja-wert wie `y` ohne newline liefert
`bufio.Reader.ReadString('\n')` als `("y", io.EOF)`. Der jetzige guard ignoriert EOF, `answer` wird zu "y" und
trifft die affirmative-Abfrage → die uninstall-aktion läuft trotzdem. Das verstößt gegen den karte-138-vereinbarung:
nur vollständige zeilen zaehlen; EOF = abbruch "Host trust unchanged." — auch wenn ein teil-ja im buffer liegt.

## Korrektur (implementiert)

trust.go uninstall-reader (Zeilen ~203-211): bei `errors.Is(err, io.EOF)` niemals die eingabe auswerten —
"Host trust unchanged." ausgeben und nil zurückgeben, VOR jeder affirmative-prüfung. Nur noch nicht-EOF-fehler
propagieren (fail-closed, ownership-record bleibt unverändert).

## Regression (implementiert, CI-erfasst)

Neue tests in `cmd/baha/trust_uninstall_test.go` (existierende trust-prompt-zelle):
- TestTrustUninstallPromptUnterminatedAffirmativeEOFRejects: `strings.NewReader("y")` (kein newline) → fehler oder nil MIT "Host trust unchanged.", ownership unverändert.
- TestTrustUninstallPromptEOFRejects: leerer reader (reines EOF) → wie oben.
- TestTrustUninstallPromptCompleteAffirmativeApproves: `strings.NewReader("y\n")` → autorisiert, ownership entfernt.

Diese zelle liegt in `cmd/baha/` und ist von `go-unit-tests` / `scripts/pr-unit-database.sh` (`go test ./... -count=1`,
trigger `pull_request`) abgedeckt.

## Repo-rule compliance

- Keine `.github/**`-dateien geändert (owner-scope).
- Kein rerun / workflow_dispatch getriggert.
- Tests in produkt-repo, CI-erfasst.
- Keine subagenten (4.8) eingesetzt.

## Nächster schritt

Lokale tests laufen, dann drift + push + hosted lauf terminal auf exaktem head.

## Lokale prüfung

- `go build ./cmd/baha`: OK
- `go vet ./cmd/baha/`: OK
- `go test ./cmd/baha/ -run 'TestTrustUninstall|TestDoctor|TestParse'`: PASS
- `go test ./internal/...`: die fehl package-fehler (controlplaneruntime: `BASEHARBOR_TEST_DATABASE_URL fehlt`, OpenBao) existieren bereits auf clean develop (`d88491982`) und sind umgebungsbasiert, nicht durch diese änderung eingeführt.

## Hosted CI (selbst beobachtet, §4.6)

- PR #1488 (base develop, head 0427-166-trust-uninstall-eof), Run 5282.
- Run terminal: `conclusion=success`, `status=completed` auf exaktem head `be2d071cf83dd94cbe7cf43e5007d46e761f1090`.
- Kritische jobs: `PR · Validation · go-unit-tests` SUCCESS, `go-vet` SUCCESS, `go-build` SUCCESS, `cli-gofmt` SUCCESS.
- Die übrigen gates sind SKIPPED (scope-appropriated: kein native runtime nötig für Go unit test).
- `go-unit-tests` führt `scripts/pr-unit-database.sh` → `go test ./... -count=1`, trigger `pull_request`; die neuen tests laufen also CI-erfasst.
- Evidence-log-download war ohne rechte nicht möglich (HTTP 404), aber API-Conclusion ist die autoritative, reproduzierbare Evidenz.

## Merge + finaler zustand (4.6)

- PR #1488 von Owner (mcpdev80) merge-commit `3187cea15728143146905c7238ad6e280ca11b3e` in develop; parent `fa355e8360497b03a40837b60ae6c88f166a8699` (develop HEAD #1484).
- Provenance: `git merge-base --is-ancestor fa355e8 3187cea` = 0 (fa355e8 ancestor von merge); merge-parent = develop HEAD, kein foreign candidate.
- Content byte-identisch: `git diff be2d071cf 3187cea -- cmd/baha/trust.go cmd/baha/trust_uninstall_test.go` = leer.
- Finaler develop head: `3187cea15728143146905c7238ad6e280ca11b3e`; fix an trust.go:206 (EOF guard).
- Lokal verifiziert auf merged develop: alle six trust-uninstall tests PASS, `go vet ./cmd/baha/` OK.
- Branch `0427-166-trust-uninstall-eof` vom Owner merge aufgebraucht (remote ref nicht mehr vorhanden); kein stray candidate.
- evidence/round-2.md auf origin/main verifiziert: `git cat-file -e origin/main:evidence/bughunt-trust-uninstall-eof-error/round-2.md` = present.
- Kein container/compose gestartet (reiner Go unit-test fix); daemon sauber.


