---
id: t-20261120-r28-stale-draft-pr-1665-closeout
card_number: "0428-176"
card_short_title: "restack with evidence or close"
type: maintenance
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w176-pr1665-1665-closeout
kanban_status: active
kanban_lane: active
kanban_summary: "Decide and execute the fate of draft PR mcpdev80/baseharbor#1665 so that the board shows one truthful state: either a restacked,…"
kanban_title: 0428-176 · restack with evidence or close
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-r28-stale-draft-pr-1665-closeout · Stale draft PR #1665 on parked card 0428-082: restack with evidence or close after ancestry proof #task #release/v0-4-28 #status/active #view/active #kind/maintenance
    <!-- generated:card -->
    **Owner:** w176-pr1665-1665-closeout  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w176-pr1665-1665-closeout  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Decide and execute the fate of draft PR mcpdev80/baseharbor#1665 so that the board shows one truthful state: either a restacked, reviewable candidate for card t-20261114-r28-perses-dashboards (0428-082) or a closed draft with ancestry proof that its content is covered by other merged or open cards.

## Scope

- In scope: PR #1665 (head `e580d32414565442376f23ace9a4a2dd7ed03838`, base branch `w083-perses-datasources` from 2026-11-17, `draft=true`, untouched since 2026-11-17T07:43:39Z), its commits and their ancestry against current `develop`, and the card note 0428-082.
- In scope: the dashboard files that the draft carries and that card 0428-123 / 0428-124 and the datasource chain (0428-083, 0428-174) also touch.
- Out of scope: implementing dashboard features here. Out of scope: `.github/**`.

## Acceptance

- Exactly one outcome is recorded with a hosted witness:
  - close: `gh pr view 1665 --json state` reports `CLOSED`, plus a per-file table proving each draft file is already present on `develop` or on an open PR with a named owner card; or
  - restack: the branch is rebased onto current `develop`, the PR base points at `develop`, it is no longer a draft, and one `pull_request` run at the exact head reaches a terminal state with run id and conclusion in the evidence file.
- Card 0428-082 states the same outcome and stays internally consistent (`owner: coord` while parked, PR list matches reality).
- No PR is closed on the basis of "diverged from develop" alone - divergence is not supersession (recorded rule from the 2026-11-20 PR sweep audit).

## Required checks

- **Modified features:** no product behaviour change expected; if the diff turns out to contain live content, that content moves to its owning card as a finding instead of being merged silently.
- **CI integration:** the run evidence is the PR's own check roll-up at the exact head; planning-only edits must not trigger product CI.

## Dependencies and file ownership

- Owned files or areas: PR #1665 metadata/branch, `tasks/t-20261114-r28-perses-dashboards.md`, this card's evidence file.
- Shared files: `internal/metrics/*` and dashboard `testdata` belong to cards 0428-078 / 0428-123 / 0428-124 - read-only here, report overlap as a finding.

## Evidence and witnesses (measured by the Coordinator, 2026-11-20)

- https://github.com/mcpdev80/baseharbor/pull/1665 - `state=open`, `draft=true`, base `w083-perses-datasources`, `updated_at=2026-11-17T07:43:39Z`.
- Independent audit of the other world agrees: "Canonical 0428-082 is Coordinator-owned; stack is stale and has no qualifying native acceptance" - https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/pr-sweep/continuation-2026-11-20.md

## Handoff

- Opened by the Coordinator from the #1665 measurement plus the sweep audit. Newest first.

WARTENDE MISSION dieses ticks, von mir dokumentiert statt verdrängt: PR #1665 ist ein draft auf einem parked source, der die develop-inhalte bereits traegt. gemessen: gh api pulls/1665 liefert draft=true, state=open. die karte ist dep-frei und wartet auf einen freien sitz; pool ist 5/5 (091, 166, 068, 078-in-review, 174), resume-trigger = erstes verdict, das einen sitz freimacht. alternative ware ein bug-hunt auf einem sechsten sitz gewesen, den die runtime nicht hergibt

lane beauftragt auf dem freien sitz (laptop 2/2), mission zugestellt um 13:3xZ und als busy bestaetigt.
GEGENSTAND: das schicksal von draft PR mcpdev80/baseharbor#1665 (karte 0428-082, 33 commits, base = der ALTE lane-branch
w083-perses-datasources @ ed55d893374b, mergeable=dirty, updated 2026-11-17T07:43:39Z). gemessen von mir:
'merge-base --is-ancestor e580d3241456 e3b4300f3f2c' = NEIN, der inhalt wartet also nicht schon in develop; und der branch
traegt ZUGLEICH commits fuer karte 0428-075, deren PR #1575 CLOSED ist - ein PR pro Karte (§3.8) ist hier verletzt.
KRITERIUM, das ich ihr mitgegeben habe: (a) SCHLIESSEN mit benennung der deckenden PRs, wenn der eindeutige inhalt nichts
leistet, was nicht schon gemergt oder auf einer offenen karte steht; (b) RESTACKEN auf develop e3b4300f3f2c mit eigenem
branch, base-retarget auf develop, 0428-075-inhalt NICHT mitnehmen (eigene karte, meldung an mich), dann kandit mit den
drei beweisszeilen. in beiden faellen akte evidence/r28-welle4-2026-11-20/stale-draft-pr-1665/round-1.md + '## decision'
in einem satz + cleanliness-zeile. STOPP + MELDUNG statt eigener entscheidung, wenn 082 eine eigene neue karte brauchte
oder das schliessen fremde, kartenlose arbeit unberuehrt liesse.
