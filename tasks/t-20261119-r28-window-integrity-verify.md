---
id: t-20261119-r28-window-integrity-verify
kanban_title: "0428-150 · verify: Fenster-integritaet"
card_number: "0428-150"
card_short_title: "verify: Fenster-integritaet"
type: task
areas: [coordination, ci]
release: v0.4.28
version: ""
parent: ""
owner: w150-pr0428-150-windowverify
kanban_status: wait
kanban_lane: wait
blocker: ""
wait_reason: "arbeit gestartet und pausiert: die fenster-integritaetspruefung braucht mehrere gemergte karten, um sinnvoll zu sein. keine live session, der sitz ist laengst frei."
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
source_note: "coordination: merge-fenster vom 2026-11-19 (develop 223cb97a9d652a4672257cabbadf12e2b41ed9cd)"
evidence:
  - "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/window-integrity/verify-1.md"
resolution: ""
created: 2026-11-19
---

- [ ] t-20261119-r28-window-integrity-verify · fensterstand gegen abnahmebelege pruefen #task #release/v0-4-28 #status/wait #view/wait #area/ci #area/coordination #kind/task
    <!-- generated:card -->
    **Owner:** w150-pr0428-150-windowverify  
    **Waiting:** arbeit gestartet und pausiert: die fenster-integritaetspruefung braucht mehrere gemergte karten, um sinnvoll zu sein. keine live session, der sitz ist laengst frei.  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/window-integrity/verify-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w150-pr0428-150-windowverify  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Der develop-Stand des merge-fensters (223cb97a9) enthaelt heute gemergte karten aus zwei welten und mehrere korrekturrunden. Diese karte prueft NACHTRAEGLICH, ob jeder inhalt, der auf develop liegt, noch das ist, wofuer er abgenommen wurde: blob-identitaet gegen den geprüften PR-kopf, vorhandene und in einem CI-shard AUSGEFUEHRTE regressionen, und die abwesenheit von acceptance-behauptungen, die auf SKIPPED-gates beruhen. Reine verifikation, keine produktaenderung.

## Scope

- In scope: read-only-pruefung auf develop 223cb97a9 fuer die heute gemergten schnitte #1581, #1616, #1598, #1692, #1701 (0428-079), #1703 (0428-148) und die bereits vorher gemergten #1602/#1685/#1694/#1696; je ein blob-/test-/gate-zeugnis.
- In scope: die frage, ob die regressionen der karten im 'PR · Go unit'-shard des gemergten stands tatsaechlich laufen (CI-aufnahmepflicht neuer tests, owner-direktive 2026-11-07).
- Out of scope: aenderungen am produkt, an .github/**, an scripts/**; korrekturen werden als befuend gemeldet, nicht gebaut.

## Acceptance

- Eine tabelle in der akte: karte | PR | geprüfter PR-head | develop-blob-identitaet (ja/nein + hash) | regression vorhanden (datei:zeile) | in CI-shard ausgefuehrt (job + lauf-id) | bemerkung.
- Jeder fall, in dem develop-NICHT dem geprüften inhalt entspricht, ist ein befund mit datei:zeile und wird von mir in eine bug-karte gegossen.
- Kein 'gruen' ohne ausgefuehrten job; SKIPPED wird als nicht erbracht aufgelistet (§5.4).

## Required checks

- **Modified features:** keine (read-only). Die pruefung uses 'git ls-tree'/'git cat-file -p' gegen develop und die PR-heads, plus 'gh api' fuer lauf-id und conclusion.
- **CI integration:** die pruefung loest KEIN produkt-CI aus; ein 'go test ./...' -lauf ist ausdruecklich NICHT gefordert (kein produktwechsel).

zurueckgesetzt auf planned: der einzige freie sitz (laptop:2) ging an die korrekturrunde 0428-142 (echte kartenarbeit vor verify-auftrag, §3.3#5 reihenfolge). karte bleibt als fenster-nachweis offen, naechster freier sitz.

nachweis-pflichtig pro karte, nicht als lump. naechster trigger: der naechste merge im fenster (gerade: f5ce95af, #1716).

Werkzeug-Hinweis: die Ablaufe dieser Karte werden von Coordinator-Skripten getragen; Werkzeug-Details und -Fehler laufen im Tooling-Repo https://github.com/mcpdev80/codeman-coordinator-tooling, nicht als Produktkarten.
