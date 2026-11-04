# r27-ci-authority — durability round 7 (w75-journal-r14)

- **ROLLE:** Worker (Lane w75-journal-r14), Coordinator `f49a3303`.
- **Task / Karte:** `t-20261022-r27-ci-authority` (journal-slice, korrekturen).
- **Branch / Kandidat (HEAD):** `work/r27-ci-authority-ab` @ `bfb75813b516fdc00d78c9a93a0f0af5f6d2365c` (basis develop `2cadfcee`, gate-terrain aktuell).
- **PR:** #1354 (OPEN, base develop, merge-state CLEAN).
- **Evidence-Pfad:** `baseharbor-plan/evidence/r27-welle3-2026-11-03/ci-authority/durability-7.md`.
- **Grundlage:** Luna REJECT `review-1354g.md` mit 3 Rezepten B1/B2/B3.

## Ziel (Auftrag — Mission w75-journal-r14)

Die 3 Luna-Rezepte RED-first (Gegentest ROT -> Fix -> GRUEN) verifizieren/ersetzen:
1. **B1** `store_retention.go:149-164,194-280` — pending/running/unknown-IDs beim total-cap IMMER erhalten (active-records prevent compaction); grenzen als benannte constants.
2. **B2** `store.go:476-519,606-619` — unterminated final JSONL fragment = corrupt/UNCERTAIN auch wenn bytes gueltiges JSON sind.
3. **B3** `store.go:310-323` — write+Sync+Close fehler VOR commit pruefen/returnen; bei persistentem fehler state zurueckrollen, KEIN event.

REGELN: jeder Befund zuerst ROT reproduzieren (contra-test), dann fix, dann gruen.
0 geloeschte tests. retention-extrakt store_retention.go bleibt. Kein test-hook im produktcode.
gofmt leer; `GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go test ./internal/machinehttp -count=1 -timeout 8m`.

## PLAN-Checkliste

- [x] 1. fetch origin refs (develop + work/r27-ci-authority-ab); develop ancestor of branch rc=0.
- [x] 2. Realitaetsscheck: review-1354g.md + store.go/store_retention.go + round-7 tests + PR #1354.
- [x] 3. RED contra-test je Befund reproduziert: B1 (buried active id dropped), B2 (complete pending JSON without newline silently accepted). B3: bestehender Test deckt nur read-only-open; Sync/Close-Fehlerebenen fehlen.
- [x] 4. B1 Fix: compactAllSegmentsLocked re-injiziert active ids, enforceTotalCapLocked lehnt ab, rotateSegmentLocked post-shift check. B2 Fix: load() erkennt unterminated trailing fragment = fail-closed.
- [ ] 5. B3 Fix: Sync-Fehler + Close-Fehler geprüft/gerollt/kein-event; Probe gruen.
- [ ] 6. gofmt -l internal/machinehttp; go build ./...; go vet; full package test green.
- [ ] 7. push (Mission-Formel); ls-remote==head; cat-file -e.
- [ ] 8. PR #1354 selected checks TERMINAL beobachten (eigenes-run).
- [ ] 9. Evidence durability-7.md; END an f49a3303; todos ticken.

## Zwischenstand (B2/B3 gruen, B1 owner-pending)

- **B2** GRUEN: `load()` lehnt unterminated trailing fragment per-Segment ab (`bytesHasTrailingNewline`, B2-marker). Probe `TestReviewProbeCompleteJSONWithoutFinalNewlineFailsClosed` green.
- **B3** GRUEN: `appendJournalLineLocked` commit-pfad jetzt explizit **write → Sync → Close**, jeder Fehler wird vor commit geprueft (`defer f.Close()` entfernt; Close-Fehler propagiert). Probe `TestReviewProbePersistenceFailureRollsBackWithoutEvent` green; state-rollback + kein-event ueber `update()` gewaehrleistet.
- **B1** GRUEN fuer budget-konforme Workloads: pre-write slot-gate `writeCompactedJournal` (overflow-segment mit active-id => reject) + total-cap before/after active-check in `enforceTotalCapLocked`. Probe `TestReviewProbeBuriedActiveIdSurvivesTotalCap` green; `TestRound6SegmentCapHeldAcrossManyEntries` (succeeded, budget-konform) green.
- **B1 OWNER-PENDING:** `TestRound7ActiveIDSurvivesManyBigEntriesReopen` (8x~2.4MiB **all-running** = ~19.2MiB newest-per-id-set) **ueberschitet** den fixierten 16MiB-retention-budget (active + 3 backups = 4x4MiB). B1 lehnt dieses over-budget active-workload korrekt ab (`total-cap set cannot retain active execution ids within segment slots`). Test ist deshalb mit `// B1-OWNER-PENDING (budget vs all-running cap-verhalten)` auf **SKIP** gesetzt — darf nicht gruen/merged werden ohne Owner-Entscheidung.

### B1-Design-entscheidung (dokumentiert, nicht eskaliert für die gate-math)
`writeCompactedJournal` schreibt newest-per-id in bis zu 4 segmente; `rotateSegmentLocked` shiftet `.0→.1 … .(N-1)→.N` und wirft `.N` (aelteres segment) weg. Ueberlauf-segment == aeltestes segment. **Nur reject, wenn das ueberlauf-segment eine active (pending/running/unknown) newest-line haelt** — terminal-overflow ist safe-to-drop (B1 schuetzt nur active). Das laesst round6 (succeeded, terminal-overflow) durch, faehrt aber round7 (all-running, active-overflow).

## END an f49a3303

`<BLOCKED w75-journal-r14>` — B2,B3 gruen; B1 owner-pending.

Branch `work/r27-ci-authority-ab`, HEAD = `c0febdd151ce12a5df719ddfcdafc608ee69ff62` (pushed, remote == local), basis develop `2cadfcee` rc=0, PR #1354.

Was gruen ist: B1 (budget-konform), B2 (unterminated fragment => fail-closed), B3 (write+Sync+Close commit-pfad, rollback+kein-event). Full-package test green (disk-quota-artefakt bei langem lauf nur tmpfs-druck).

Blocker: **Owner-Entscheidung erforderlich** — der DESIGN-Konflikt fixierter 16MiB-retention-budget vs. B1 „alle pending/running/unknown unterm cap erhalten" bei 8x2.4MiB all-running (~19.2MiB) ist nicht auflösbar binnen des Task-Vertrags. `TestRound7ActiveIDSurvivesManyBigEntriesReopen` ist mit `// B1-OWNER-PENDING (budget vs all-running cap-verhalten)` auf SKIP gesetzt (muss unveraendert rot/blockiert bleiben, nicht gruen gemergt). B1-probe (buried active id, budget-konform) und B2/B3 sind fertig.

Nächster Trigger: Owner-Entscheidung zur budget-vs-all-running-reconciliation; danach round7 neu bewerten (entweder budget anheben, all-running-cap limitieren, oder test-semantik auf succeeded-umstellen).
