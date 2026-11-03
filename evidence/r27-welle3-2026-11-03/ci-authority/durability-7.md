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
- [ ] 3. RED contra-test je Befund (B1 active-id, B2 unterminated JSONL, B3 sync/close) reproduzieren.
- [ ] 4. Fix bestaetigen/anwenden, contra-tests GRUEN (mutation controls scharf lassen).
- [ ] 5. gofmt -l internal/machinehttp; go build ./...; go vet; full package test green.
- [ ] 6. push (Mission-Formel); ls-remote==head; cat-file -e.
- [ ] 7. PR #1354 selected checks TERMINAL beobachten (eigenes-run).
- [ ] 8. Evidence durability-7.md; END an f49a3303; todos ticken.

## END an f49a3303

`<PENDING>`
