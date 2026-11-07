# Kanban-Kurzanleitung (Menschen & LLMs)

**Quelle:** `tasks/*.md`. Ein Task = eine Karte. Kanban-Status und Zuordnung immer direkt in der Task-Datei pflegen.

## Spalten: Wann verwenden?

| Spalte | Verwendung |
| --- | --- |
| **Backlog** (`backlog`) | Idee/unsortierte Arbeit; nur Release `backlog` oder `triage`. |
| **Planned** (`planned`) | Geplant, **noch nicht begonnen**. Auch wenn Abhängigkeiten offen oder Worker belegt sind. |
| **Ready** (abgeleitet) | Planned, alle Abhängigkeiten akzeptiert, Release aktiv oder `early: true`. Noch nicht zugewiesen/gestartet. |
| **Active** (`active`) | Bearbeitung hat begonnen. `owner` Pflicht. |
| **Wait** (`wait`) | **Bereits begonnene** Arbeit pausiert: wartet auf andere Karte, Runner, Worker, Ressource oder Rückmeldung. `owner` und `wait_reason` Pflicht. |
| **Review** (`review`) | Umsetzung fertig, Abnahme/Review offen. `owner` und mindestens ein `prs`-Eintrag Pflicht. |
| **Blocked** (`blocked`) | **Alarm:** Owner-Entscheidung erforderlich oder Umsetzung derzeit technisch unmöglich. `blocker` mit genauer Ursache/Entscheidungsbedarf Pflicht. Nicht für normale Wartezeiten! |
| **Closed** (`closed`) | Nach tatsächlicher Abnahme. `resolution` und HTTPS-`evidence` Pflicht. Ein grüner PR allein reicht nicht. |

**Regel:** Unbegonnene Karte bleibt **Planned**, selbst mit offenen `depends_on`. Nur bereits begonnene Arbeit wird bei Wartebedarf **Wait**. Ist die Voraussetzung wieder erfüllt: **Wait → Active**, `wait_reason` leeren. **Blocked** nie als Parkplatz nutzen.

## Felder im YAML-Frontmatter

| Feld | Wert / Regel |
| --- | --- |
| `id` | Eindeutige Task-ID, nie nachträglich ändern. |
| `card_number` | Release-bezogene Nummer, z. B. `0427-013`. |
| `card_short_title` | Kurzer Kartentitel, maximal ca. 30 Zeichen. |
| `kanban_title` | Anzeige `0427-013 · Short Title`; vom Renderer pflegen lassen. |
| `kanban_status` | Kanonischer Zustand: `backlog/planned/active/wait/review/blocked/closed`. |
| `kanban_lane` | Obsidian-Spalte; bei Drag & Drop geändert, anschließend durch Renderer synchronisiert. |
| `kanban_summary` | Kurze Beschreibung; vom Renderer aus Task-Text abgeleitet. |
| `owner` | Tatsächlicher Bearbeiter/Agent; ab **Active**, **Wait**, **Review** Pflicht. Bei eigener Arbeit eintragen; fremden Owner nicht stillschweigend überschreiben. |
| `release` | Zugehöriges Release, z. B. `v0.4.27`. |
| `priority` | `critical`, `high`, `normal`, `low` oder leer. |
| `depends_on` | Task-IDs offener Voraussetzungen, z. B. `[t-20261018-r27-team-auth]`. **Allein kein Wait!** |
| `wait_reason` | Konkreter Wartegrund, nur bei `wait`; beim Fortsetzen leeren. |
| `blocker` | Konkreter Owner-Entscheidungsbedarf oder technische Unmöglichkeit; nur bei `blocked`. |
| `prs` | Zugehörige PRs als `mcpdev80/baseharbor#1433` (oder anderes betroffenes Repo). |
| `repos` | Betroffene Repository-Namen, z. B. `[mcpdev80/baseharbor]`. |
| `resolution` | Nur für Closed: `accepted`, `superseded` oder `dropped`. |
| `evidence` | Bei Closed mindestens ein echter HTTPS-Nachweis (PR, SHA, CI-Lauf, Acceptance); keine angenommenen PASS-Ergebnisse. |

Weitere Felder (`type`, `areas`, `parent`, `sources`, `early`) gemäß `templates/task.md`.

## Beispiel: Begonnene Karte wartet auf Runner

```yaml
owner: "codeman-worker-2"
kanban_status: wait
kanban_lane: wait
wait_reason: "Podman-Runner belegt; native Acceptance ausstehend"
blocker: ""
depends_on: []
prs: [mcpdev80/baseharbor#1433]
resolution: ""
evidence: []
```

## Nach jeder Änderung

```bash
python3 scripts/plan.py render && python3 scripts/plan.py check
```

Danach committen/pushen. `#status/...`, `#view/...`, Checkbox und `views/` **nicht manuell** bearbeiten. Beim Merge/Review immer Karte, Owner, PR, SHA und echte CI-/Abnahmenachweise aktualisieren. **Closed erst nach vollständiger Abnahme.**
