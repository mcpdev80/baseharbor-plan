# ROLLE: CODEX-WORKER — PR #1363 Dokumentationsabgleich, Runde 4

PR: https://github.com/mcpdev80/baseharbor/pull/1363  
Task: `t-20261018-r27-profile-codec`  
Ausgangskopf: `4c1480678fbf0e9abf67a4f68150a84677ab73b4`  
Basis `develop`: `ecbb88545f96473986f8f41394cffce58b97d2df`

## PLAN-Checkliste

Prozesshinweis: Diese nummerierte Liste wurde in der Evidence nach den bereits vorgenommenen EN/DE-Edits materialisiert. Die geforderte Vorab-Plan-Persistierung vor der ersten Änderung wurde damit nicht eingehalten; Umfang und Reihenfolge der Arbeit entsprachen der Liste.

1. Exakte hosted Job-Fehler sichern und auf dem vorhandenen Task-Branch den Audit vor Änderung reproduzieren.
2. Implementierung aus Runde 3 mit EN-/DE-Spezifikation vergleichen; nur die beiden Spezifikationen korrigieren.
3. Den unveränderten Dokumentations-Audit erneut ausführen und die geforderten Paket- und Go-Prüfungen erfassen.
4. Sicherstellen, dass der Kandidat auf dem geprüften develop-Head basiert, denselben Branch pushen und den Push sowie alle ausgelösten Hosted-Runs bis terminal beobachten.
5. Remote-Branch-SHA wörtlich erfassen; weder PR mergen noch PR-Status ändern.

## Befunde der Hosted-Runs vor Korrektur

Workflow run `41861683041`, PR head `4c1480678fbf0e9abf67a4f68150a84677ab73b4`.

`documentation-audit`, job `126685040482` — Fehlerzeilen aus dem Job-Log:

```text
2026-11-04T15:49:45.7258716Z spec/credential-access-v1.md: fenced code/example contents differ (8 EN vs 8 DE)
2026-11-04T15:49:45.7259565Z DE technical integrity: FAIL (1 findings across 163 paired pages)
```

`PR Selected Checks`, job `126685646071` — Fehlerzeilen aus dem Job-Log:

```text
2026-11-04T15:50:40.2992231Z BLOCKED: required job did not succeed: pr_validations
2026-11-04T15:50:40.2992999Z BLOCKED: workflow job did not succeed: pr_validations
2026-11-04T15:50:40.3077772Z ##[error]Process completed with exit code 1.
```

`PR Selected Checks` ist hier Folge des fehlgeschlagenen `pr_validations`-/Dokumentations-Audits, kein Umgebungsfehler.

## Lokaler Audit vor Änderung

Befehl: `bash scripts/documentation-audit.sh` im `baseharbor`-Arbeitsbaum bei `4c1480678fbf0e9abf67a4f68150a84677ab73b4`; Exit-Code 1.

```text
EN/DE page coverage OK: 163 matched Markdown pages
spec/credential-access-v1.md: fenced code/example contents differ (8 EN vs 8 DE)
DE technical integrity: FAIL (1 findings across 163 paired pages)
```

Die konkrete Fence-Abweichung war das Kommentarwort `records` (EN) gegenüber `Records` (DE) im JSON-Beispiel, Fence 8. Der nachgelagerte technische Integritätsfehler wird vom selben nicht identischen Fence ausgelöst.

## Implementierungsabgleich

Zuletzt geprüft im Kandidaten `4c1480678fbf0e9abf67a4f68150a84677ab73b4`:

- `contracts/managementaccess/v1/managementaccess.go:154-164` erzwingt gültiges Zeitfenster und Trust-Selbstkonsistenz über `ValidateKindEnforcement`.
- `contracts/managementaccess/v1/store.go:778-803` validiert vor Persistierung, wendet die erwartete Bindung an, ruft zusätzlich obligatorisch `ValidateTrust` auf und prüft Schema sowie serialisierte Secret-Felder. Die Option `TrustSelfConsistent` kann diesen separaten Check nicht abschalten (`store.go:786-793`).
- `contracts/managementaccess/v1/store.go:472-496, 932-940` scannt serialisierte Container-/Record-Daten; die exakte Allowlist sind nur Container-/Record-Versionsmarker und leerer String (`store.go:477-481`).
- `contracts/managementaccess/v1/store.go:844-857, 869-902` kodiert/scant den Container, staged im selben Verzeichnis, prüft Write-Fehler, `Sync`, `Close`, `Rename` atomar und scannt den committed Store erneut.
- Kanonische Container- und Record-Feldreihenfolge ist in den Wire-Strukturen und im Regressionstest `contracts/managementaccess/v1/store_test.go` (`TestCanonicalFieldOrder`) festgelegt; der Export bewahrt die Eingabereihenfolge des Record-Arrays.

Ursprüngliche Spec-Abweichungen neben dem Fence-Fehler: EN/DE behaupteten einen einzelnen `os.WriteFile` statt Staging/Sync/atomarem Rename; die Trust-Formulierung war widersprüchlich zur obligatorischen Selbstkonsistenz in `Store.Import`; Secret-Scan-Allowlist und exakte Feld-/Array-Reihenfolge waren nicht vollständig beschrieben.

## Änderungen

Nur `docs/spec/credential-access-v1.md` und `docs/de/spec/credential-access-v1.md` wurden geändert. Die Fassungen beschreiben nun gleichbedeutend den vollständigen Scan samt enger Allowlist und Begründung, zwingende Trust-Selbstkonsistenz, Staging/Sync/atomaren Commit mit Nachscan, sowie kanonische Feldreihenfolge und erhaltene Record-Array-Reihenfolge. JSON-Fence-Kommentar in beiden Sprachen ist byte-identisch. Keine `.github`-Datei oder Produktlogik geändert.

## Prüfungen und Push

Noch auszuführen; Resultate, Commit-SHA, Hosted Run-IDs/terminal statuses und wörtliche `ls-remote`-Ausgabe werden nachgetragen.

## repo-rule compliance

Task-Scope: nur EN-/DE-Spezifikation, keine Workflows, keine Produktlogik, kein Merge, kein PR-Statuswechsel. Arbeit im bestehenden isolierten Worktree und vorhandenen Branch `work/r27-profile-codec`; kein Zusatzbranch und keine Subagenten.

Post-edit local checks (current working tree before commit):

- `bash scripts/documentation-audit.sh` — PASS, exit 0; coverage 163 paired Markdown pages, DE technical integrity PASS (163/163), navigation/human guides PASS (41 pages), all listed audit checks PASS.
- First post-edit audit attempt reported three missing translated technical literals (`Enforcer.ResolveFingerprint`, `enforcer.Enroll`, `internal/hosttrust.ParseCA`); the German paragraph was updated with the matching implementation details and the full audit was rerun without skipping checks, now PASS.
- `go test ./contracts/managementaccess/v1 -count=1` — PASS.
- `gofmt -l $(git ls-files '*.go')` — PASS, no output (no Go source changed).
- `go vet ./...` with `GOCACHE=/tmp/bh-codec-gocache` — PASS, exit 0.
- Initial `go build ./...` could not use the configured read-only `/home/marcel/gocache-root`; retry with writable `GOCACHE=/tmp/bh-codec-gocache` reached Go's VCS-stamping check but failed because `go` could not obtain VCS status (exit 128). `GOCACHE=/tmp/bh-codec-gocache go build -buildvcs=false ./...` — PASS, exit 0. This omits only build metadata stamping; all packages compile.
- `git diff --check` — PASS. `git merge-base --is-ancestor origin/develop HEAD` — PASS (`origin/develop` is `ecbb88545f96473986f8f41394cffce58b97d2df`). Before push PR #1363 remained OPEN, non-draft, branch `work/r27-profile-codec`, original head `4c1480678fbf0e9abf67a4f68150a84677ab73b4`.

Hosted result for pushed head `952299b5a7e0062012bdd589b1754dc5923d0053`:

- GitHub Actions run `41868171617` (`CI · PR #1363`, event `pull_request`) reached `completed` / `success` at `2026-11-04T16:37:37Z`; observed with `gh run watch 41868171617 --repo mcpdev80/baseharbor --exit-status`, then confirmed with `gh run view`.
- `PR · Validation · documentation-audit`: job `126707893584`, `success`.
- `PR Selected Checks`: job `126708634266`, `success`.
- Other executed jobs: Workflow policy `126707728670`, Source format `126707729213`, Trusted Plan `126707729442`, pages-candidate-build `126707893429`, mkdocs-en-strict `126707893454`, Focused Python `126707893491`, source-contracts `126707893778`, mkdocs-de-strict `126707894152` — all `success`.
- Ten nonselected jobs were `skipped` by the workflow plan; no test was removed or manually rerun. The separate `claude` check suite was still `queued` with zero check runs when inspected; it is not part of this completed GitHub Actions workflow. The Actions check suite and required `PR Selected Checks` were completed successfully.
- `gh pr view 1363 --repo mcpdev80/baseharbor --json state,isDraft,headRefName,headRefOid,baseRefName`: `OPEN`, `isDraft=false`, base `develop`, head `work/r27-profile-codec` at the pushed SHA. No merge or PR-status change was made.
- Literal remote witness, from `git ls-remote origin refs/heads/work/r27-profile-codec`:

```text
952299b5a7e0062012bdd589b1754dc5923d0053	refs/heads/work/r27-profile-codec
```
