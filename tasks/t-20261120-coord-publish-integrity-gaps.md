---
id: t-20261120-coord-publish-integrity-gaps
card_number: "0428-175"
card_short_title: "card-status.py bypasses the"
type: maintenance
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w175-pr0428-175-publish-gate
kanban_status: active
kanban_lane: active
kanban_summary: "Every published planning text passes the same integrity gates a dispatched payload passes, and the watch registry can be cleaned…"
kanban_title: 0428-175 · card-status.py bypasses the
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

- [ ] t-20261120-coord-publish-integrity-gaps · Coordinator tooling: card-status.py bypasses the payload integrity gates; watch.py rm signature unusable #task #release/v0-4-28 #status/active #view/active #kind/maintenance
    <!-- generated:card -->
    **Owner:** w175-pr0428-175-publish-gate  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w175-pr0428-175-publish-gate  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Every published planning text passes the same integrity gates a dispatched payload passes, and the watch registry can be cleaned with the documented call.

## Scope

- In scope: `coordinator/scripts/card-status.py` (run the charset check and the English-tech-word check used by `/var/tmp/sanitize.py` over card note/blocker text before commit + publish; fail closed with a non-zero exit on a hit). In scope: `coordinator/scripts/watch.py` `rm` subcommand (accept a short session id, print the real signature in `--help`).
- Out of scope: product code, `.github/**`, planning schema changes.

## Acceptance

- A deliberately garbled note (one CJK character, or one forced German re-formulation of an English technical term) is REJECTED by `card-status.py` before anything reaches `main`, with the offending line reported.
- `python3 coordinator/scripts/watch.py rm <short-sid>` removes the entry for a released lane; `watch.py list` no longer shows it. Measured defect: `watch.py: error: argument c: invalid` for a released session id (precedent: lane `fd49077a` left a stale entry after release).
- Regression evidence shows both cases in one run transcript plus the commit SHA of the fix.

## Required checks

- **Modified features:** adapt the existing coordinator-script self-tests; add a fixture that feeds a garbled note through `card-status.py` and asserts a non-zero exit.
- **CI integration:** coordinator tooling is not part of the product CI matrix; a local self-test run is the evidence here (state that explicitly in the handoff instead of inventing a gate).

## Dependencies and file ownership

- Owned files or areas: `coordinator/scripts/card-status.py`, `coordinator/scripts/watch.py`.
- Shared files: `/var/tmp/sanitize.py` gate is read-only reference - reuse its rules, do not edit the Owner's file.

## Handoff

- Opened by the Coordinator on 2026-11-20 from two self-measured incidents: a CJK garble (`ein nicht-lateinisches Zeichen`) published into card t-20261120-r28-develop-runtime-integration-red because `card-status.py` does not call the payload sanitizer, and an unusable `watch.py rm` call for released lane fd49077a.

second live instance measured 2026-11-20, by me: a non-latin token entered the note of card t-20261114-r28-perses-tempo-source through card-status.py and reached origin/main while plan.py check reported 0 errors. the token was stripped and republished (board-sha 232ff2cbfb1c). additionally the same call printed NOTHING and did not publish once, then published silently on retry with a token of the same class: the failure mode is inconsistent and must be pinned. implementation of both fixes is coordinator tooling (coordinator/scripts), not product code, and runs after the merge window clears unless a free seat appears first

delegate statt selbst: die beiden defekte habe ich gemessen (card-status.py laesst den zeichensatz-gate von sanitize.py passieren — zweimal live belegt, board-sha 232ff2cbfb1c und die 091-note; watch.py rm nimmt keine short session id — 'error: argument c: invalid choice', zweimal belegt). write-set ist coordinator/scripts, damit keine beruehrung mit den laufenden produktkarten. abnahme macht eine andere session, nicht der coordinator ueber sich selbst
