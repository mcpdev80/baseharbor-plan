---
id: t-20261119-coord-tooling-defects
kanban_title: 0428-155 · coordinator script defects
card_number: "0428-155"
card_short_title: "coordinator script defects"
type: task
areas: [coordination, ci, tooling]
release: v0.4.28
version: ""
parent: ""
owner: "folgelane (wird gesetzt)"
kanban_status: active
kanban_lane: active
blocker: ""
wait_reason: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
source_note: "fünf einzeln gemessene werkzeug-defekte, die an diesem abend VIER falsche alarme und DREI still fehlgeschlagene zustandswechsel verursacht haben (coordinator/QUEUE.md queue655, 662, 666, 667). Kein produkt-bezug, nur coordinator/**."
evidence: []
resolution: ""
created: 2026-11-19
---

- [ ] t-20261119-coord-tooling-defects · skript-zeile statt bahn-pruefen #task #release/v0-4-28 #status/active #view/active #area/ci #area/coordination #area/tooling #kind/task
    <!-- generated:card -->
    **Owner:** folgelane (wird gesetzt)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** folgelane (wird gesetzt)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Der coordinator prueft bahnen mit eigenen skripten. Wenn ein skript sich irrt, verliert das fenster zeit an schein-fehler: heute vier falsche alarme (todo-brett 'MISSING', VM-zaehlung, pool-artefakt, codex-praedikat) und drei still fehlgeschlagene karten-pubs. Ziel ist, die fuenf bekannten zeilen so zu korrigieren, dass ein fund wieder eine aussage ueber eine bahn ist und nicht eine aussage ueber mein werkzeug — und dass eine frei-gabe nicht von der uhr-zeit abhaengt.

## Scope

- In scope: coordinator/scripts/card-status.py (:75, :124), coordinator/scripts/release-lane.py (:49), coordinator/scripts/dispatch-lane.sh (:12/:16), coordinator/scripts/vm-audit.sh (:19), ein einmaliger lauf von coordinator/scripts/workspace-hygiene.sh mit protokolliertem ergebnis.
- Out of scope: jede aenderung an baseharbor/** (produkt), an .github/** und scripts/** des produkt-repos (owner-scope), an baseharbor-plan/** ausser der eigenen akte, und jede CRON-installation (vorschlag ja, eintrag nein — owner-entscheidung).

## Acceptance

- card-status.py kann ein LEERES owner/blocker/wait_reason-feld ausdruecklich schreiben und unterscheidet das von 'argument nicht angegeben'; die validierung meldet 'active braucht owner' nur, wenn das feld wirklich leer ist. Regression fuer beide faelle.
- release-lane.py ordnet die OpenCode-session ueber einen GELESENEN verweis zu (spawn-registrierung / agent-feld), nicht ueber ein 10-minuten-uhr-fenster; wenn es trotzdem raten muss, sagt die ausgabe das ausdbruecklich. Die heutigen zwei 'HOLD ... release incomplete'-faelle (bahnen von vor 3+ stunden) wuerden damit durchlaufen.
- dispatch-lane.sh leitet den dateinamen des todo-bretts aus dem LANE-NAMEN ab, nicht aus dem payload-dateinamen; todo-check.sh meldet fuer jede laufende bahn ein vorhandenes brett.
- vm-audit.sh schliesst fremde/teilhaber-container ausdruecklich aus und zeigt im ausgabe-text, was gezaehlt wurde.
- workspace-hygiene.sh: ein dokumentierter einmaliger lauf, der NICHTS loescht, was einer LEBENDEN bahn gehoelt (gegenueberstellung lebende sitze aus pool-reconcile.py vs. registrierte worktrees), mit vorher/nachher-zaehlung.

## Required checks

- **Modified features:** python3 -m py_compile coordinator/scripts/*.py; bash -n coordinator/scripts/*.sh; die neuen regressionen (orchestrator-seitig, OHNE produkt-code). Wenn es KEINEN coordinator-ci-gibt, ist das ein befund an den coordinator (owner-scope fuer .github), keine eigenmacht.
- **CI integration:** die karte hat KEINEN produkt-pr-lauf, wenn kein .github-anteil geaendert wird — dann ist der beweis der lokale regression-lauf, und die akte nennt ihn ausdruecklich als 'kein gehosteter lauf noetig, grund: nur coordinator/**'.

## Nachtrag des Coordinators, 2026-11-20 00:4x UTC — siebter Defekt, gleiche Klasse

`coordinator/scripts/card-status.py:129`:

```python
if a.status == "active" and not re.search(r"(?m)^owner:\s*$", head):
    problems.append("active braucht owner")
```

Das Muster `^owner:\s*$` trifft eine **leere** owner-Zeile. Die Verneinung bedeutet also:
„Wenn ein Inhaber **gesetzt** ist, brich mit active braucht owner." Die Prämisse ist invertiert —
gefragt war „Feld **fehlt**" (`^owner:` irgendeine Zeile). Praktisch: **jeder** `active`-Wechsel einer
Karte mit echtem Inhaber bricht, und ich musste heute **vier** Zustandswechsel durch direkte
Feld-Schnitte umgehen (157, 123, 154, 119). Dasselbe Muster in Zeile 131 für `wait`
(`not re.search(r"(?m)^owner:\s*$", head) or not field(...)`), nur dort durch den
`wait_reason`-Zweit_test verdeckt.

Rezepte:presence-test statt leer-test, und **eine regression pro zeile** — karte mit echtem
inhaber -> `active` muss durchgehen; karte ohne inhaber-zeile -> muss brechen; karte mit
`owner: ""` -> muss brechen.
