# BaseHarbor native Obsidian Kanban

Open [BaseHarbor.base](BaseHarbor.base) with Obsidian 1.15+ and the core Bases plugin.

Each task Markdown note is one card. `kanban_status` is the writable lifecycle source of truth. Dragging a card edits this property. The original task checkbox and `#status/...` tag are compatibility output updated by `python3 scripts/plan.py render`; don't edit the tag independently. Legacy notes without this property continue to work.

Columns: backlog, planned, active, review, blocked, closed. Dependency-derived ready/waiting/queued remain read-only; Ready is a separate table filtered through `#view/ready`.

Active requires owner. Review requires owner and prs. Blocked requires blocker text. Closed requires resolution (accepted, superseded, dropped) and real HTTPS evidence. Superseded requires superseded_by. Dragging to Closed alone is not acceptance.

After dragging, run `python3 scripts/plan.py render && python3 scripts/plan.py check`, then commit/push. Existing validation remains authoritative. To reopen a closed task, clear resolution before validating. Legacy CardBoard configuration is kept for rollback; native Bases does not depend on that plugin.

https://obsidian.md/help/bases/syntax
https://obsidian.md/help/bases/views/kanban

## Kanban v2: Ready and compact card details

The writable `kanban_lane` property drives Obsidian's status columns. The lifecycle `kanban_status` remains authoritative for all other API and CLI consumers; the planning renderer reconciles a card drag to the lifecycle state and updates the derived `kanban_lane` (ready/waiting/queued are planned tasks with dependency/release computation). Codeman should change `kanban_status` via standard planning processes, not `kanban_lane` directly. Native dragging from Ready to Active is supported after a render, with ordinary owner and release safeguards.

Card properties: `kanban_title` (display title), `id`, `owner`, `kanban_summary` (first authored overview paragraph, max 130 chars). No generated claim or invented summary. Native Kanban cannot collapse columns; inactive states are shown in separate inventory views/count tables instead. For wider columns use Kanban view settings > Column width in Obsidian (officially supported).

## Themen-Tags und Prioritaetsfarben

Jede Release-Kanban-Ansicht zeigt jetzt zusaetzlich `areas` als Themen-Tags und `priority` als Prioritaet. Diese Felder stammen aus den bestehenden Aufgaben-Metadaten; es gibt keine duplizierte Status- oder Tag-Datenquelle.

Farbige Karten benoetigen in Obsidian 1.15 das separat zu aktivierende Community-Plugin **Bases Colors** (`bases-kanban-card-colors`; https://community.obsidian.md/plugins/bases-kanban-card-colors). Das Plugin wird **nicht automatisch installiert** und das Board bleibt ohne Plugin benutzbar.

Empfohlene Regeln unter Bases Colors > Card/row colors > Rules by property, in dieser Reihenfolge, nur fuer `BaseHarbor.base` und Kanban:

| Property | Is | Farbe | Darstellung |
| --- | --- | --- | --- |
| priority | critical | Rot | Linker Farbstreifen |
| priority | high | Orange | Linker Farbstreifen |
| priority | normal | Blau | Linker Farbstreifen |
| priority | low | Grau | Linker Farbstreifen |

Unter Property/tag colors die Anzeige fuer `areas` aktivieren, damit ein Thema (zum Beispiel `identity`) immer dieselbe Farbe erhaelt. Falls das Plugin die Kartendatei nicht zuordnen kann, muss auch `file.name` als anzeigbare Karteneigenschaft vorhanden sein; die Plugin-Dokumentation fordert einen sichtbaren Dateinamen. Das ist eine Plugineigenschaft, kein natives Obsidian-Feature.

Quelle: https://obsidian.md/help/bases/views/kanban
