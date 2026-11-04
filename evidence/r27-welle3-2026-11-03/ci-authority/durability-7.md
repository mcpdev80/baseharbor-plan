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

## END an f49a3303

`<PENDING>`
