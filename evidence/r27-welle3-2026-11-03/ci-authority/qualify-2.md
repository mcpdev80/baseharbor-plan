# w44-ci-authority-b — qualify-2 (DONE, run)

## Endstatus
**END_DONE.** Slice „journal-wiring" (karte t-20261022-r27-ci-authority, explizit als Slice
geführt; Owner-Scope-Freigabe 2026-11-03) umgesetzt. Head `99556b9a7f25cfaad84974bffbb6e92a0db40abb`,
FF von `159054c2` auf PR-Branch `work/r27-ci-authority-ab`, PR #1354 bleibt DRAFT.
Push bestätigt via `git ls-remote` == push-Head; develop Vorfahr (ancestry rc=0).

## Review-Grundlage
review-1354a.md (3 Befunde): #1 behauptete „Dauerhaftigkeit" ohne Disk/Reopen/Corruption-Nachweis;
#2 gehostete Trusted-CI-Auswahl = Owner-CI-Punkt; #3 nur In-Memory-Zustandsübergänge nachgewiesen.
Dieser Slice bearbeitet **nur #1** als minimale Persistenz des bestehenden Stores — kein neues
Subsystem, nur echte Persistenz des bestehenden `executionStore`.

## Product-Diff (je Befund, mit Testname)
- **Befund #1 — journal now persisted (disk/reopen/corruption):**
  - `internal/machinehttp/store.go`: `newPersistedExecutionStore(stateRoot)` lädt bei Konstruktion
    `<state-root>/journal/journal.jsonl` (`journalDir()`); `update()` (einziger Mutation-Pfad von
    start/progress/succeed/fail) append-persists jeden Transition-Schritt via `appendJournalLocked()`;
    leerer stateRoot ⇒ in-memory (Bestandsverhalten). `load()` schlägt bei korrupter Zeile **fail-closed**
    fehl (kein silent skip).
  - `internal/machinehttp/handler.go`: `New(executor, stateRoot string)` — minimale Signatur-Erstweiterung.
  - `internal/controlplaneruntime/server_run.go:245`: **ein** Übergabe-Punkt, übergibt `cfg.RuntimeOperationsDir`
    (bestehendes Runtime-Dir-Feld, keine neue Flagge).
  - Tests: `TestExecutionJournalDurableReopen` (save ⇒ neuer Store über dieselbe root ⇒ Transition sichtbar;
    `succeed` mit strukturiertem Resultat), `TestExecutionJournalCorruptLogFailsClosed` (korrupte Zeile ⇒ Error),
    `TestPersistedStoreEmptyRootIsInMemory` (leere root ⇒ in-memory, kein Disk).
  - `TestExecutionJournalDurableTransitions` ⇒ umbenannt zu `TestExecutionJournalInMemoryTransitions`
    (Kommentar: same-process map, keine Persistenz-Behauptung).
- **Befund #2 — gehostete CI-Auswahl:** Owner-CI-Punkt, **nicht** Lane-Feld. Aktuell auf PR übersprungen
  (skipped), kein `.github/scripts`-Diff. In Evidence nur dokumentiert.
- **Befund #3 — slice-matrix:** execution-journal (durable) jetzt gegen Disk/Reopen/Corruption belegt;
  authority-contract, state-owner, mutation-lock, app-binding, candidate-ingress, management-host bleiben
  bei ihren Ownern (unabhängige Tests/CI-Zuordnung).

## Verifikation (eigener Run, witnesses)
- `go build ./...` ⇒ exit 0.
- `go test ./internal/machinehttp -count=1` ⇒ `ok` (alle inkl. DurableReopen / CorruptLogFailsClosed /
  EmptyRootIsInMemory / InMemoryTransitions / FailsClosedOnUnknownID / RejectsInvalidContractStates /
  BoundedSequenceFuzz).
- `go vet ./internal/controlplaneruntime/ ./cmd/baha/` ⇒ exit 0 (Aufrufer-Pakete kompilieren).
- Diff nur im erlaubten Write-Set: `internal/machinehttp/**` (+ Tests) + `server_run.go:245` +
  `cmd/baha/machine_http_executor_validation_test.go`. `.github/**` unverändert; PR bleibt DRAFT.

## OFFENE / Handoff
- CI-Gate (Docker/Podman/Integrations-Kette): Coordinator/CI-Owner triggert; lane ändert kein Gate.
- Merge + Planning-Abschluss (accepted→closed) nach erfolgreicher Codex-Abschlussprüfung des SHA-genuen
  Kandidaten durch den Merge-Owner.
