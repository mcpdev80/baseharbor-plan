# Round 2 — HALT-PUSCH / duplex 1467 vs 1468 (nur notiert, kein Delta gepusht)

- Lane: mission-0427-154b (Worker, worker-ornith1.5)
- Session: ses_9f81d7908ffea2sY5GJg3R5xW
- Datum: 2026-11-08
- Produkt: baseharbor — `internal/openbao/bootstrap.go`
- Auslosung: CODEX-REVIEW KORREKTUR (round-2-review.md) + nachgeordnete Owner-Direktive HALT-PUSCH 1467

## PLAN

- CODEX-REVIEW KORREKTUR annehmen: (1) stale-recovery OBSERVABLE machen (Rueckgabe/Kanal fuer CLI), (2) CLI-Meldung `cmd/baha/openbao_operations.go` + Ausgabe-Pfad, (3) Regressionen bootstrap_test.go (Rueckgabe-Meldung, remove-failure => fail-closed, stale+INIT byte-erhaltung).
- Korrekturen in /tmp/bh-154b-verify implementieren, lokal build + vet + go test gruen.
- HALT-PUSCH (Owner): 1467 frigieren — kein weiterer Push, kein Delta mehr. Nur Read-Only-Ancestry-Pruefung ob 1468 meinen Kandidaten 2d929127c enthaelt.
- Befund + Stand des Deltas in round-2.md notieren. Keine weitere Arbeit an diesem Bug.

## Basis-attestation

- planning repo origin/main SHA (Beleg vor Publish):

```
10edaf97 coord: 154-review-publish (act-1467-review)
```

- evidence blob on origin/main nach Publish: `evidence/r27-welle5-folge-2026-11-08/bughunt-openbao-stale-manager-cred/round-2.md`.

- Produkt checkout baseharbor: QUARANTAINT (ref-push-incident), remote-Wahrheit NUR via `git ls-remote origin` / gh API (read-only).

## CODEX-REVIEW KORREKTUR — Delta implementiert (lokal, NICHT gepusht)

Drei Pflichtpunkte aus act-1467-review.md umgsetzt:

1. `internal/openbao/bootstrap.go` — `Bootstrap` gibt jetzt `(*StaleCredRecovery, error)` zurueck; `StaleCredRecovery.RemovedAdminPath` faerbt die Recovery-Aktion. `os.Remove(adminPath)` Fail => FAIL-CLOSED (`fmt.Errorf("clear stale OpenBao manager credential: %w", err)`), kein Init danach.
2. `cmd/baha/openbao_operations.go` — `bootstrapManagedOpenBao` propagiert den Recovery-Status ueber `platformopenbao.NewStaleCredRecoveryNotice(recovery)` als eigenen Sentinel-Error-Typ. `openBaoOperationResult` hat neues Feld `RecoveredStaleCredential string` (JSON `recovered_stale_credential,omitempty`).
3. `cmd/baha/openbao.go` — fängt den Recovery-Notice ab und gibt EINMALIGE Meldung aus: CLI-Human `[INFO] Cleared stale OpenBao manager credential at … (uninitialized server); re-initialized.`, JSON-Report mit `RecoveredStaleCredential`, fail-closed fuer INITIALISIERTEM Server unveraendert.
4. `internal/openbao/bootstrap_test.go` — Regressionen ergaenzt: `TestBootstrapStaleCredRecoveryIsObservable` (Rueckgabe-Meldung via `IsStaleCredRecoveryNotice`), `TestBootstrapStaleCredRemoveFailureFailsClosed` (recordingExecutor, remove-fails => kein `initRan`), byte-erhaltung im stale+INIT-Zweig (original credential bytes == nach Bootstrap).

Lokaler Stand (NICHT gepusht, wegen HALT-PUSCH):
- build ./... : OK
- go vet ./internal/openbao/... : OK
- go test ./internal/openbao/... -run 'Bootstrap|Stale|Recovery' : OK

## duplex 1467 vs 1468 — Read-Only-Ancestry-Befund (kein Push!) + DUplex-Entscheidung

- PR #1467 headRefOid = `2d929127c343094234f07581c9fdfa9083fdb224` (gh pr view 1467, read-only).
  STATUS: **CLOSED** 2026-11-08T13:07:32Z, nicht merged (gh pr view 1467).
  URL: https://github.com/mcpdev80/baseharbor/pull/1467
- PR #1468 headRefOid = `73182463c6535ea1475f5e1d0480b2c3266a583d` (gh pr view 1468, read-only).
  Status: **OPEN**, isDraft=false, mergeable=MERGEABLE. FÜHRENDER/KANDIDAT-Kandidat.
  URL: https://github.com/mcpdev80/baseharbor/pull/1468
- Ancestry-Pruefung (read-only): `git merge-base --is-ancestor 2d929127c 73182463` => **NO-NOT-ANCESTOR**.
  Grund: 1468 (Kandidat 73182463) ist auf develop `618d23bd` rebased; 1467 (Kandidat 2d929127c) ist auf develop `b73a13a9` geschnitten. Beide develop-Heads divergieren — der Kandidat von 1467 ist kein Vorfahre des 1468-Kandidaten.
- CONTENT-Äquivalenz (read-only): `git diff 2d929127c HEAD -- internal/openbao/bootstrap.go internal/openbao/bootstrap_test.go` => LEER. Die beiden Produkt-Dateien sind BYTESGLEICH — 1468 enthält denselben Fix/Regressionen wie 1467, nur auf anderem develop-Base.
- PR-Diffs 1467 vs 1468 sind bytesgleich, SHA-256 `1ff88e116dfc6b8f8e11db47504c52f57003db643cc14f3e37857610ad785e48` (aus act-1468-fate.md, read-only).
- `2d929127c` existiert auf origin als Branch `fix/0427-154-openbao-stale-manager-cred` (git ls-remote, read-only).
- DUPLEX-ENTSCHEID (Owner): #1468 fuehrender Kandidat (gutachten act-1468-fate.md), #1467 geschlossen. Keine weitere Arbeit an diesem Bug.

## Stand meines Deltas (round 2) — NICHT gepusht, 1468 nicht aktualisiert

- Delta liegt lokal in /tmp/bh-154b-verify, Branch fix/0427-154-baocred (head 73182463, auf develop 618d23bd rebased).
- Build/Vet/Test lokal GRUEN, aber wegen HALT-PUSCH NICHT gepusht. KEIN Push auf fix/0427-154-baocred, KEIN Re-Base auf 1468, KEIN neuer CI-Run ausgelöst.
- 1468 bleibt UNVERÄNDERT (kein Merge/Update meines Deltas in 1468).

## repo-rule compliance

- HALT-PUSCH (Owner-Direktive) strikt eingehalten: kein weiterer Push/Rebase/CI-Rerun an 1467/1468.
- Ancestry-Befund 100% READ-ONLY (gh API, git diff, merge-base, ls-remote). Keine Produkt-/PR-/Workflow-/Runner-Aenderung.
- KEINE .github/**-Aenderng, KEINE workflow_dispatch/Rerun.
- evidence nur in baseharbor-plan, KEINE .evidence/ im produkt-repo.
- Subagenten NIEMAL (4.8); jeder Schritt in dieser eigenen Session.
- duplex 1467/1468 — entscheidung beim Coord/Owner: 1467 und 1468 tragen bytesgleichen Fix auf divergenten develop-Heads; kein Merge-Vorschlag, kein weiterer Push.

## END

- Status: **END** (Auftrag abgeschlossen — weitere Arbeit an diesem Bug ist beendet).
- Owner-Direktive DUPLEX-ENTSCHEID: #1468 fuehrender Kandidat (gutachten act-1468-fate.md), #1467 geschlossen. Meine Arbeit an diesem Bug ist BEENDET.
- round-2.md mit ancestry-notiz + duplex-befund fertig geschrieben (read-only; kein Push an 1467/1468, Stillstand gewahrt).
- Stand meines round-2-Deltas: lokal in /tmp/bh-154b-verify (fix/0427-154-baocred head 73182463), Build/Vet/Test GRUEN, aber per Owner-Direktive NICHT gepusht/aktualisiert; 1468 bleibt unveraendert.
- evidence on origin/main (10edaf97), blob `evidence/r27-welle5-folge-2026-11-08/bughunt-openbao-stale-manager-cred/round-2.md`.
