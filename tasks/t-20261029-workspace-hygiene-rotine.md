---
id: t-20261029-workspace-hygiene-rotine
type: task
status: active
areas: [ops]
release: v0.4.27
version: ""
parent: v0.4.27
priority: medium
owner: coordinator
depends_on: []
repos: []
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261029-workspace-hygiene-rotine · Betrieb: Workspace-Hygiene-Routine (Dauerkarte) #task #release/v0-4-27 #status/active #view/active #area/ops #kind/task
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** medium  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** none  
**Owner:** coordinator  
**Priority:** medium  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Purpose
Dauerhaft saubere Arbeitsumgebung ohne Manueraufruesten: Worktree-/Branch-Pflege, tmp-Sweep, Watcher-Registry als Cron-Routine mit Bundle-Nachweis und Aktiven-Schutz.

## Betrieb
- taeglich 05:30Z: `evidence/board-2026-10-19/scripts/workspace-hygiene.sh 1440` (Log: hygiene.log; Bundles: tmp-ops/worktree-graveyard/)
- alle 12h: `tmp-sweep.sh 24` (/tmp-RAM)
- alle 15min: `prune-watch.sh` (Watcher-Registry), alle 10min: `ci-watch.sh` (PR-Wachen)
- Eingreifpflicht Coordinator: >80 Worktree-Register; KEEP-Zeilen 'not-integrated' aelter 3 Tage; bundle-failed.

## PLAN
- 1. Routine gebaut und getestet (removed=0, age guard aktiv)
- 2. Crons installiert
- 3. Erstlauf-Bewertung nach o234-Bereinigung
