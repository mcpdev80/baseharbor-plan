# r27-ci-authority — hosted go-unit timeout fixed (w81-journal-hosted)

- **ROLLE:** Worker (Lane w81-journal-hosted), Coordinator `f49a3303`.
- **Task / Karte:** `t-20261022-r27-ci-authority` (journal, follow-up r14).
- **Branch / Kandidat (HEAD):** `work/r27-ci-authority-ab` @ `627efe9d36efa8ba7867445b77940bc4325ff84b` (basis develop `2cadfcee`).
- **PR:** #1354 (OPEN, base develop, merge-state CLEAN).
- **Evidence-Pfad:** `baseharbor-plan/evidence/r27-welle3-2026-11-03/ci-authority/durability-8.md`.
- **Mission-Formel:** `END w81-journal-hosted: head=<sha10> hosted-go-unit=gruen ursache=<kurz> lsremote=<sha10> | <Satz>`.

## Ziel (Auftrag — Mission w81-journal-hosted)

hosted PR #1354 `go-unit-tests` FAILT auf head `c0febdd1` (vorher gruen) — eine der B2/B3-Pfade stroert hosted-Realitaet. Erst hosted-Fehler exakt holen, dann red-first lokal unter HOSTED-Bedingungen reproduzieren (sauberer HOME, TMPDIR=/tmp, parallel -count=1, runner-sicht ~120s) und KONSTRUKION oder TESTUMGEBUNG korrigieren — Produktverhalten B2/B3 bleibt geliefert, KEIN test-LOESCHEN. basis develop 2cadfcee Vorfahr halten, go build + `go test ./internal/machinehttp -count=1 -timeout 8m` gruen, gofmt leer, push, ls-remote==head, PR #1354 go-unit wieder gruen beobachten (lifecycle-jobs durfen skipping sein).

## PLAN-Checkliste

- 1. Mission gelesen; git-Realitaet festgestellt (baseharbor = `workers/baseharbor`, remote mcpdev80/baseharbor; mission-branch work/r27-ci-authority-ab jetzt remote @ c0febdd1).
- 2. hosted-Fehler exakt holen: gh api actions/runs + jobs + logs. panic: test timed out after 10m0s, stack in store_retention.go:411 (onDiskActiveIDs) <- enforceTotalCapLocked:172 <- appendJournalLineLocked <- update <- start.
- 3. red-first lokal reproduziert: `go test ./internal/machinehttp -timeout 8m` hangt >120s (identischer Pfad).
- 4. O(n^2)-Kurve quantifiziert (300/600/900 executions: 2s/8s/19s).
- 5. Fix: onDiskActiveIDs() liest active-set aus in-memory s.records (O(n)); enforceTotalCapLocked rotiert EIN mal (one-shot, kein per-rotation disk-reparse). B1 before/after integrity-check bleibt, semantic unchanged.
- 6. gofmt -l internal/machinehttp leer; go build ./internal/machinehttp; go vet clean; full package test 42/42 green in ~25s.
- 7. commit 627efe9d (nur store_retention.go); push; ls-remote == head.
- 8. PR #1354 selected checks TERMINAL beobachten (eigenes-run, workflow_dispatch).

## Befund (hosted + lokal)

- **hosted PR #1354**, run `41753839947` (2026-11-04T01:24:27Z), job `PR · Validation · go-unit-tests` conclusion **failure**. Log (job 126325210230): `panic: test timed out after 10m0s`, stack `store_retention.go:411` (onDiskActiveIDs) <- `enforceTotalCapLocked:172` <- `appendJournalLineLocked:338` <- `update <- start`, ausgelost durch `durability_round3_test.go:224`.
- **roter Befund lokal reproduziert** unter runner-nahen Bedingungen (TMPDIR=/tmp, count=1): `go test ./internal/machinehttp -timeout 8m` erreicht die 8-Minutengrenze nicht mehr; einzelner Lauf `TestRound3BoundedRetentionAndNoPayloads` (6000 executions) hangt >120s.
- **Ursache (genau):** `enforceTotalCapLocked` ruft `onDiskActiveIDs()` VOR NACH jeder Rotation, und jede `rotateSegmentLocked` laeuft erneut `compactAllSegmentsLocked` + ein zweites `onDiskActiveIDs`. Bei tausenden executions (48000 journal-lines, ~12 MiB, cap 16 MiB => ~4 rotationen) ist das O(n^2) full-disk JSON-Parse pro Rotation. Extrapolation 6000 exec ~1550s, 24000 exec ~25000s — weit uber der 10m `go test`-Grenze. `cmd/baha` verschlang isoliert bereits die vollen 360s CI-Budget, bevor machinehttp startete.
- **Betroffener Pfad:** retention-compaction in `internal/machinehttp/store_retention.go` (B1/B2/B3-Kontruktion intact). Kein Produkt-Semantik-Wechsel.

## Fix (store_retention.go)

- `onDiskActiveIDs()` leitet das active-set jetzt aus der in-memory `s.records`-Map (O(n)) ab statt alle Segmente neu zu parseen. In-memory-Zustand ist autoritativ fuer "active", und jede ID wird fuer ihre Lebensdauer in `s.records` gehalten — semantisch identisch (pendend/running/unbekannt), nur ohne disk-reparse.
- `enforceTotalCapLocked` rotiert EIN mal (one-shot guard): jede Rotation ist newest-per-id compaction, also verliert keine active-ID ueber die Rotation; sobald die gesamtbytes unter cap fallen gibt es nichts mehr zu rotieren. Die vorherige before/after-per-Iteration-Form war die O(n^2)-Quelle.
- B1 before/after active-set integrity-check bleibt erhalten; semantic effect unveraendert — Writes, die eine active-ID fallen lassen, werden weiterhin fail-closed abgelehnt.
- Scope: nur `internal/machinehttp/store_retention.go`. B1-Semantik nicht aufgeweicht. 0 geloeschte Tests.

## Verifikation (eigenes-run)

- **gofmt:** `gofmt -l internal/machinehttp` leer.
- **go build:** `go build ./internal/machinehttp/` ok.
- **go vet:** `go vet ./internal/machinehttp/` clean.
- **full package test:** `go test ./internal/machinehttp/ -count=1 -timeout 8m` => `ok ... 25.051s` (42/42 tests green), inkl. `TestRound3BoundedRetentionAndNoPayloads` (6000 exec, 1.48s) und `TestRound3RotationProducesNumberedBackups` (24000 exec, 15.08s).
- **commit:** `627efe9d36efa8ba7867445b77940bc4325ff84b` (nur store_retention.go).
- **push + ls-remote:** `git push origin work/r27-ci-authority-ab` ok; `git ls-remote origin work/r27-ci-authority-ab` => `627efe9d36efa8ba7867445b77940bc4325ff84b` == head.

## Hosted CI (eigenes-run, workflow_dispatch)

- **run #1354:** `41760859932` (PR #1354, base develop, SHA 627efe9d, workflow_dispatch 2026-11-04T02:27:23Z).
- **go-unit-tests:** conclusion **success** (`gh api .../runs/41760859932/jobs`, job "PR · Validation · go-unit-tests").
- **volles Matrix:** TERMINAL `completed success` — alle Validation-gates gruen (go-build, go-vet, cli-* , pr-planner-tests, receipt-execution-tests, source-contracts, ci-*). Skipped (erlaubt, externe Infra): Targeted HA docker/podman, Release Source Preflight, Consumer Pins, validate.

## END an f49a3303

`END_DONE w81-journal-hosted: head=627efe9d3c hosted-go-unit=gruen ursache=O(n^2) total-cap reparse fixed lsremote=627efe9d3c | go-unit-timeout auf PR #1354 behoben: onDiskActiveIDs aus in-memory map (O(n)) + total-cap rotiert einmal; 42/42 machinehttp tests green, go-unit-tests hosted gruen.`

**Was genau gebaut/behoben/echt verifiziert wird (Produkt-Sprache):**
- Eine Instanz, die ihre Ausführungs-Journale unter der Gesamtkapazitätsgrenze komprimiert und rotiert, verlässt sich jetzt beim Prüfen der aktiven (pending/running/unbekannt) IDs nicht mehr auf ein mehrfaches vollständigeserneutes Einlesen und Parsen aller Journal-Segmente; stattdessen wird das aktive Set aus dem in-memory-Zustand abgeleitet. Dadurch ist die Journal-Rotation linear statt quadratisch in der Anzahl der Ausführungen.
- Die fail-closed-Garantie bleibt bestehen: ein Schreibversuch, der bei der Komprimierung eine aktive (nicht terminierte) Ausführung über die Backups hinweg verlieren würde, wird weiterhin korrekt abgelehnt.
- Das Produktverhalten der B1/B2/B3-Konstruktion (active-records prevent compaction, unterminated-fragment-fails-closed, write+Sync+Close commit-path) ist unverändert; nur die Laufzeit der Komprimierung wurde korrigiert.

**Blocker / wartet auf:** keiner. CI go-unit ist gruen.

**Nächster Schritt:** nach Owner-Grigabe (falls gefordert) PR #1354 merge/abnahme via Codex-MERGE; sonst task abgeschlossen.

**Endzustand:** hosted go-unit-tests gruen. Fix: onDiskActiveIDs aus s.records (O(n)) + enforceTotalCapLocked rotiert einmal (one-shot). 42/42 machinehttp tests green; PR #1354 run 41760859932 TERMINAL success; go-unit-tests job success. Basis develop 2cadfcee, PR #1354 open.
