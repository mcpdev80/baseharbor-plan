# w44-ci-authority-b — qualify-2 (BLOCKED, no run)

## Endstatus
END_BLOCKED. **Kein Produkt-Run, kein Commit, kein uncommitted Change.** Working tree sauber,
Branch `work/r27-ci-authority-ab` auf Base-Head `159054c2`. Context-Reset vor Umsetzung —
Coordinator rotiert die Lane.

## Befund (warum blockt)
- `internal/machinehttp/store.go` hält `records` in einer reinen Prozess-Map (`map[string]*executionRecord`);
  das Paket führt **keine** Datei-/OS-I/O aus (kein `os.OpenFile`/`os.Create`/`XDG`/`os.Getenv`; das
  einzige `json.Marshal` schreibt in HTTP-Response-Writer).
- `machinehttp.New(executor)` nimmt **nur** einen Executor; der einzige Produktions-Caller
  `internal/controlplaneruntime/server_run.go:245` (`machinehttp.New(machineExecutor)`) übergeben **keinen**
  State-Root, Data-Dir oder XDG-Pfad. Die einzig existierende Runtime-Dir-Konfig (`RuntimeOperationsDir`,
  `internal/controlplaneruntime/server.go:53`) wird an ein anderes Paket (`runtimeoperation.New`)
  durchgereicht, nie an `New()`.
- Es gibt **kein** bereits im Paket übliches Persistenz-Muster, das man „nur übernehmen" konnte.
  Jede Persistenz würde zwingend einen neuen Wiring-Semantik-Segment in `New()` erfordern —
  das ist ein „new subsystem / invented layout".

## STOP-Kriterium (Mission Zeilen 26–27)
„wenn store.go eine andere persistence-heimat ERZWINGT (zyklus/ownership): END_BLOCKED mit
datei:stelle statt eigenmachtiges neues layout." → Erfüllt: `store.go` erzwingt neuen Heimaten-Segment.
Empfohlener Weg: auf das wartende Produktinterface `t-20261018-r27-execution-journal` verweisen
(disk/reopen/corruption + Heimat-Entscheidung), statt Layout selbst zu erfinden.

## Getane Prä-Arbeit (keine Write im Produkt)
- origin-Fetch + Worktree `/tmp/opencode/w44-ci-authority-b-wt` auf `159054c2` vorbereitet.
- store.go + handler.go + Production-Call-Site gelesen, Persistenz-Heimat-Segment ausgeschlossen.

## Offener Schritt
Owner-Entscheidung: (a) BLOCKED bestätigen, (b) minimalen Bare-Minimum-Anhang gegen
`$XDG_STATE_HOME/baseharbor/machine/journal.jsonl` mit dokumentiertem Hinweis akzeptieren, oder
(c) auf Product-Owner-Heimat warten. Kein Push, PR #1354 bleibt unverändert.
