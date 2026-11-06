# CODEX-REVIEW — registry access PR #1395 round 2

- Review date: 2026-11-06. Reviewer: Codex (Kanal Luna), read-only.
- Coord-record notice: die Rezensent-Session durfte wegen Approval-Policy `never` die Datei nicht selbst
  schreiben/pushen (dreimal versucht, quota dann policy). Dieser Akten text ist das wörtlich aus ihrem
  Sitzungs-Protokoll überlieferte Urteil des Koordinators als Protokoll-Auszug; die Prüfungshandlungen
  (Diff-Lektüre, Run-Abfrage, Caller-Zelle, Mutante im temporären Worktree) hat sie selbst ausgeführt.

- Verdict: **REJECT** candidate `ef0120aa3d73`.

## Befunde (aus dem Review-Protokoll)

1. Hosted-Run 42132438226 ist am exakten Kopf terminal grün: 14 erfolgreich, 10 übersprungen, 0 fehlgeschlagen.
2. Der Diff enthält zusätzlich zu den erlaubten Adapterdateien und `app_broker.go` auch `app_broker_registry_p*`
   — Scope-Punkt, in Runde 3 gegen das Kartenschreibset zu entscheiden (name-only Liste vorlegen).
3. Die Caller-Zelle ist grün, erkennt das Entfernen des echten produktiven Callers aber nicht (temporäre
   Mutante im Worktree: Zelle blieb grün). Diskriminierungs-Lücke: die Zelle prüft nicht den echten
   Zusammenbau, sondern nur den Adapter.
4. Der Kopf basiert auf `21d8d05`; aktuelles develop ist `f01d2fb`. Develop ist **kein Vorfahr** des
   Kandidaten (Ancestry-Regel verletzt) — develop-Refresh nötig.
5. Hygiene: temporäre Mutante wurde per Checkout zurückgesetzt; PR und Produktbranch wurden nicht geändert.

## Rezept für Runde 3

- (a) develop aktuell einmergen, ancestor rc=0 belegen; (b) Caller-Zelle so verschärfen, dass die echte
  produktive Callers entfernt werden muss und die Zelle dann ROT wird (echte Quellcode-Mutation mit
  git-diff-Beleg + Gegenprobe grün); (c) Scope-Punkt zu app_broker_registry_p* mit name-only Liste klären.
  Mission vorbereitet: coordinator/missions/w210-registry-r3.txt.
