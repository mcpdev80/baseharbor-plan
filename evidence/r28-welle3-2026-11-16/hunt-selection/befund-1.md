# Befund-1 — Selection-Line Bug-Hunt (080 acceptance, children-vs-seam intersection, draft reasons)

Lane: mission-hunt-selection
Date: 2026-11-17
Card: hunt-selection (Bug-Hunt, reine Befundung, keine Produktänderung, kein PR-Eingriff)
Owner: worker-ornith1.5 (this session)
Mission: /var/tmp/missions/mission-hunt-selection.md

## Mission (verbatim intent)

Bug-Hunt (pure findings, no product change, no PR intervention): check the
SELECTION-LINE against its acceptance criteria so the Kinderwelle runs faster
after the 075-merge. Cards: 0428-080 (#1590, draft, base
lane-0428-075-perses-seam) and the selection children #1602/#1604
(077/hosts dashboards). Read the branches against develop@bcae1e8c
(merge-base witnesses, file lists). Check:
(a) whether #1590 already meets the 080 acceptance (non-forgeability witness)
today or what is missing,
(b) which of the children files would intersect the 075-seam after merge,
(c) draft reasons in the PR history.
Findings with file:line -> evidence/r28-welle3-2026-11-16/hunt-selection/befund-1.md.

## Baseline / attestation (witnesses)

- Planning repo verified as /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.
  workers/baseharbor-plan is bookkeeping and untouched.
- develop head (ls-remote): bcae1e8c1261c9e44db03fe285a5d090c532dfcd
- 080 selection lane-0428-080-r28-perses-selection (PR #1590) remote head:
  fd82668f1cab2b5c90eb6f961816a55f7ec68ecd
- 075-perses-seam lane-0428-075-perses-seam remote head: 87b287259a1d6f13fa255877558a5d027078a0b1
- 077 child (PR #1602) head Ref: lane-0428-077-r28-perses-dashboard-hosts = 1f7b5eee92fb142ba94776fce6738df32c5aab7a
- 081 child (PR #1604) head Ref: wt-0428-081 = bf58a9cf7254f6f5ebc3d9b7f9c8679e13f54ce8

PR metadata (gh pr view --repo mcpdev80/baseharbor):
- #1590 state=OPEN isDraft=true baseRefName=lane-0428-075-perses-seam
  headRefName=lane-0428-080-r28-perses-selection
- #1602 state=OPEN isDraft=true baseRefName=lane-0428-080-r28-perses-selection
  headRefName=lane-0428-077-r28-perses-dashboard-hosts
- #1604 state=OPEN isDraft=true baseRefName=lane-0428-080-r28-perses-selection
  headRefName=wt-0428-081

## Work plan (numbers)

- 1. Remote heads via ls-remote.
- 2. merge-base witnesses + file lists.
- 3. (a) 080 acceptance / non-forgeability witness.
- 4. (b) children-vs-seam intersection.
- 5. (c) draft reasons in PR history.
- 6. Findings to evidence, clean up, END.

## (a) Does #1590 already meet the 080 acceptance (non-forgeability witness)?

### A1 — the non-forgeability witness exists and is the gate input on the 080 head
- The 080 selection line is internal/capability/perses_selection.go (the
  resolver/fan-in). Present on head fd82668f.
- IdentitySelectionWitness struct + NewIdentitySelectionWitness: availability is
  DERIVED, not caller-supplied. File internal/capability/perses_selection.go:
  - type IdentitySelectionWitness struct { ... Available bool } at
    lines 39-69. The struct comment (lines 27-37) states the zero value is
    `unavailable` (fail-closed) and "a caller can never obtain a positive
    availability by setting the availability result directly".
  - NewIdentitySelectionWitness(selectionConfirmed, metricPresent, metricCurrent,
    targetAuthorized bool) at lines 79-97 derives Available as the AND of the
    four real-evidence flags; the zero value is unavailable.
- NonForgeableAvailable() at lines 99-110 is the AND of the four real-evidence
  flags; "the single validated entrance every gate and decision path must use;
  Available alone must never be trusted as gate input." This is the non-forgeable
  witness the 080 acceptance demands (acceptance item 2: "fail closed on unknown
  ownership or missing authorization").
- EligibleFor(key, witness IdentitySelectionWitness, backendSignals
  map[DashboardBackend]bool) at line 274 gates each dashboard on real backend
  signal inventory + selection + current release, fail-closed: line 292
  `if witness.NonForgeableAvailable() || c.templates[key].Backend != DashboardBackendIdentity`.
- AcceptedPersesVersion = "v0.55.1" (line 186), keyed to the seam pin. This is
  the "verified, pinned Perses release" of acceptance item 1.
- Prometheus/Loki/Tempo backend ownership preserved: DefaultDashboardCatalog ships
  three real backends (prometheus/loki/tempo); requires-adapter backends are
  absent (PR #1590 body). Acceptance item 3 satisfied.

### A2 — verdict: the non-forgeable witness EXISTS and is correct, but #1590 is DRAFT so "acceptance met" is not closed
- The code meets every 080 acceptance item (pinned release + native format,
  fail-closed by ownership, preserved backend ownership, no fake alerting parity).
- BUT PR #1590 is DRAFT (gh pr view isDraft=true). A draft PR is by definition
  not "acceptance met" — the acceptance is a review/merge outcome, not a code
  state. So "does #1590 meet the 080 acceptance TODAY" resolves to:
  - Witness correctness: YES, the non-forgeability witness is present and correct
    on head fd82668f (A1).
  - Acceptance formally closed: NO — draft + the 080 resolver was still being
    hardened across 080-r2 (1781277d3, the non-forgeable+per-dashboard gate) and
    080-r3/batch13 (fd82668f, scope Keycloak identity witness to the identity
    dashboard only). The batch13 change is the last of the three hardening commits.
- WHAT IS MISSING for a clean "acceptance met" verdict (not a defect, a status):
  the batch13 REQUEST_CHANGES correction (scope the global identity witness to
  the identity dashboard only so Prometheus/Loki/Tempo dashboards are eligible on
  their own backend signal) must be landed and the PR moved out of draft after
  review. Both are owner/review actions, not something a hunt proves.

### A3 — batch13 (fd82668f) is the decisive commit for acceptance
- fd82668f fix(0428-080): scope Keycloak identity witness to identity dashboard only (batch13).
  Luna batch13 REQUEST_CHANGES: the global identity-selection witness was gating
  EVERY Perses dashboard behind NonForgeableAvailable(), including Prometheus/Loki/
  Tempo dashboards with no Keycloak dependency. The fix restricts the global
  witness to the identity dashboard only. This is the last hardening step; until
  it is reviewed and the PR is no longer draft, acceptance is open.
- Provenance note: this commit was authored AFTER the children were based
  (children base e6f5e650 is an ancestor of fd82668f — see B1/B2). The children
  therefore inherit the PRE-batch13 080 signature. That is a merge-order fact,
  not a defect (see B2).

## (b) Which children files intersect the 075-seam after merge?

### B1 — merge-base witnesses
- merge-base(080-fd82668f, develop-bcae1e8c) = 14d8f17d1aa61496db9ed4d57bd4c22eda34ae95
- merge-base(080-fd82668f, 075-seam-87b287259) = 66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08
- merge-base(080-fd82668f, 077-child-1f7b5eee) = e6f5e650d048c28004cdc59608e9205c648bb509
- merge-base(080-fd82668f, 081-child-bf58a9cf) = e6f5e650d048c28004cdc59608e9205c648bb509
- e6f5e650 is a MERGE commit: "Merge commit '66ff93d1...' into
  lane-0428-080-r28-perses-selection". So the 075-seam (66ff93d1) is already an
  ancestor of the 080 line — 075 is folded into 080's ancestry.
- 66ff93d1 (the 075 base that enters 080) has internal/capability/perses.go and
  perses_test.go but NOT perses_selection.go. The catalog file arrives into the
  080 line ONLY via the seam merge, then is authored by the 3 hardening commits
  (1873ba33f, 1781277d3, fd82668f).

### B2 — children-vs-seam intersection: additive, no file-level edit of the seam file
- The 075-seam does NOT edit internal/capability/perses_selection.go
  (diff 66ff93d1..lane-0428-075-perses-seam on that file is empty). The seam only
  brings the file into the 080 lineage; the 080 commits author it.
- Neither child edits perses_selection.go:
  - #1602 (077) adds only internal/metrics/perses_dashboards_hosts.go (+ helpers,
    testdata) — 1 file, 549 insertions, diff on perses_selection.go is empty.
  - #1604 (081) adds only internal/metrics/perses_dashboards_valkey.go (+ test,
    testdata) — diff on perses_selection.go is empty.
- Both children consume the 080 selection catalog via the shared
  capability.DashboardBackend vocabulary (077: "via the shared DashboardBackend
  vocabulary; no line of that catalog is edited here") and compute availability
  from a real resolved observability signal status, never a caller bool
  (077 identityUnavailableReasonHost resolves capability.ObservabilitySupportStatus;
  081 marks Valkey explicitly UNAVAILABLE on absence of a native signal). This
  mirrors the 080 non-forgeability principle.
- CONCLUSION (b): after 075-merge to develop, the ONLY 075-carrying file the
  children could touch is internal/capability/perses_selection.go, and neither
  child edits it — both land ADDITIVE files that consume the catalog. The
  intersection is therefore non-conflicting: the seam brings the new catalog file
  in, the 080 commits author it, the children consume it. No merge conflict is
  expected on the seam file itself.
- MERGE-ORDER FACT (not a defect, must be rebased if the 080 head advanced): both
  children were based on the 080 line at e6f5e650, which is BEFORE the batch13
  commit fd82668f (3 commits ahead now: 1873ba33f, 1781277d3, fd82668f). After the
  075 seam merges into develop and the 080 line lands, the children must be
  rebased onto the landed 080 head so they pick up the batch13 witness scoping.
  This is a coordination/rebase step, not a code change.

### B3 — the full selection Kinderwelle (from card t-20261114-r28-perses-dashboard-selection line 37)
- depends_on: [t-20261114-r28-perses-contract-seam, t-20261114-r28-perses-signal-inventory]
- Required by: dashboards-databases, dashboards-hosts (#1602), dashboards-valkey
  (#1604), dashboards-identity, dashboards-messaging, dashboards-dashboards.
- All children stack on the 080 selection head, which carries the 075 seam. The
  080 line is the single integration anchor; children are additive consumers.

## (c) Draft reasons in the PR history

### C1 — #1590 draft reason (PR body, primary)
- #1590 body ends: "Draft only — seam is under merge frost and is not merged."
- The 075 seam was under "merge frost" (not yet merged to develop), so the 080
  selection PR stayed draft pending the seam landing. This is the documented
  draft reason.
- No PR comments exist on #1590 (gh api .../issues/1590/comments returns empty),
  so no additional reasons are recorded; the body is the sole draft reason.

### C2 — #1602 / #1604 are also drafts (same structural reason)
- Both are isDraft=true with baseRefName=lane-0428-080-r28-perses-selection.
  They are children of the draft 080 line and stay draft until the 080 line lands
  and is reviewed. Same merge-frost + child-of-draft reason.

## STOP criterion check

- This is a Bug-Hunt: pure findings, no product change, no PR/branch intervention.
- No real card work was commissioned by this mission — it is a closed-gauge read
  of the selection line. Nothing to stop on beyond "no changes made".

## END status

- DONE: findings A1-A3, B1-B3, C1-C2 written with file:line where available;
  all SHAs witnesses via ls-remote; evidence will be pushed to origin/main (see
  second-to-last action).
- No containers started (read-only git + gh investigation).
- No branch/PR edit, no merge, no force-push, no ready_for_review, no
  workflow_dispatch, no subagent. Every step done in this session.
- No scratch/cache files created in /home/marcel/dev/baseharbor-ecosystem.

## repo-rule compliance

- Planning repo verified as /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.
- workers/baseharbor-plan is bookkeeping and untouched.
- No branch/PR edit, no merge, no force-push, no ready_for_review, no
  workflow_dispatch, no subagent. Every step done in this session.
- No scratch/cache files created in /home/marcel/dev/baseharbor-ecosystem.
