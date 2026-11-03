# w53-ci-authority-c — r27-ci-authority durability round 3

## Mission
- ROLLE: Worker (Lane w53). Coord f49a3303. KARTE: t-20261022-r27-ci-authority (journal-slice runde 3).
- Branch `work/r27-ci-authority-ab` head `99556b9a7f25cfaad84974bffbb6e92a0db40abb` (PR #1354).
- Grundlage: review-1354b.md rezepte 1-5.
- Write-set: `internal/machinehttp/**` + max one `cmd/baha serve` übergabe-zeile + server_run wiring. NO `.github/scripts`.
- END an f49a3303: `"END_DONE w53-ci-authority-c: head=<sha> accepted-restart=ja semantik=ja nofallback=ja retention=<wert> | <Satz>"`
- Evidence file: `baseharbor-plan/evidence/r27-welle3-2026-11-03/ci-authority/durability-3.md` (plain bullets je punkt + testnamen).

## END
- Status: BLOCKED — Retention-Grenze aus Kartenlaut mehrdeutig, STOP-Klausel bindet. Cannot publish retention value or final END_DONE (END_DONE format requires retention=<wert> which the mission forbids guessing).
- STOP citation: card t-20261018-r27-execution-journal.md line 42 says only "Bound retention, no secrets/artifact payloads in ordinary journal" — NO numeric bound anywhere in any r27 card. Mission STOP: "kartenlaut zur retention-grenze mehrdeutig => END_BLOCKED mit zeile der karte, nicht raten."
- Evidence posted to f49a3303: END_BLOCKED.

## PLAN (numbered)
1. Fetch origin refs, worktree add, verify ancestry (99556b9a reachable from develop).
2. P1: persisted execution store — commit accepted ID+actor+context before 202/202; load restores under lock; test pending-reopen after restart.
3. P2: semantic validation on load (real enum, bogus state rejected) + write ordering (commit before mutate/notify, append-failure rolls back); one counter-test each.
4. P3: fail-closed at production boundary when operations-dir absent (no silent in-memory); server-construction integration test for set/missing root.
5. P4: bounded retention + no Result/Progress/error-payload in journal (status+id+time only). BLOCKED on exact bound (STOP).
6. P5: gofmt -l internal/machinehttp empty; PR status untouched.
7. Local checks green (build + ./internal/machinehttp); push FF; ls-remote==head.

## repo-rule compliance
- Write-set strictly internal/machinehttp/** + one serve.go line + server_run wiring.
- No .github/scripts touched. gofmt clean.
- PR #1354 status NOT modified (draft reset forbidden per mission P5).

## Evidence
- (retention value BLOCKED — STOP clause forbids guessing the exact bound; card line cited in END above)
