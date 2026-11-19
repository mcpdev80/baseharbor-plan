---
id: t-20261119-r28-prgate-docs-internal-json-mapping
kanban_title: "0428-144 · docs/internal/**/*.json faellt"
card_number: "0428-144"
type: task
areas: [ci, docs]
release: v0.4.28
version: ""
parent: ""
owner: "Owner-Ausfuehrung (scripts/** + .github/** ist Owner-Scope); auf bitte der unabhaengigen review in abgesetztem worktree ausgefuehrt, Coordinator dispatcht dafuer KEINE worker-lane"
kanban_status: wait
kanban_lane: wait
blocker: ""
wait_reason: "scripts/pr-gate-plan.py ist owner-scope: worker-lanes melden nur befuende mit datei:zeile und aendern keine zuordnungsregeln (AGENTS 4.5, CI-aufnahmepflicht). daher fuehrt der owner bzw. die von ihm beauftragte stelle diese abbildung aus, keine ornith/laptop/flash lane"
depends_on: []
repos: [mcpdev80/baseharbor]
evidence:
  - "https://github.com/mcpdev80/baseharbor/blob/1019190d8dc0ecac7693f3461153e76be0e2cb8a/scripts/pr-gate-plan.py"
resolution: ""
created: 2026-11-19
card_short_title: "docs/internal/**/*.json faellt"
---

- [ ] t-20261119-r28-prgate-docs-internal-json-mapping · docs/internal/**/*.json faellt durch die DOC_CHECKS-verzweigung von pr-gate-plan.py und wird nie validiert #task #release/v0-4-28 #status/wait #view/wait #area/ci #area/docs #kind/task
    <!-- generated:card -->
    **Owner:** Owner-Ausfuehrung (scripts/\*\* + .github/\*\* ist Owner-Scope); auf bitte der unabhaengigen review in abgesetztem worktree ausgefuehrt, Coordinator dispatcht dafuer KEINE worker-lane  
    **Waiting:** scripts/pr-gate-plan.py ist owner-scope: worker-lanes melden nur befuende mit datei:zeile und aendern keine zuordnungsregeln (AGENTS 4.5, CI-aufnahmepflicht). daher fuehrt der owner bzw. die von ihm beauftragte stelle diese abbildung aus,…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/1019190d8dc0ecac7693f3461153e76be0e2cb8a/scripts/pr-gate-plan.py)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Owner-Ausfuehrung (scripts/** + .github/** ist Owner-Scope); auf bitte der unabhaengigen review in abgesetztem worktree ausgefuehrt, Coordinator dispatcht dafuer KEINE worker-lane  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Why this exists

0428-131 (PR #1697) changes three files under `docs/internal/`. Its acceptance requires the existing
`documentation-audit` to run on the exact candidate head. The independent review verified on develop
`1019190d8dc0ecac7693f3461153e76be0e2cb8a` that the trusted planner does not select it: public
Markdown/RST and root docs map to `DOC_CHECKS`, while `docs/internal/**/*.json` misses that branch and
falls through unresolved. The current conservative broad fallback does not include `documentation-audit`
either, so a `documentation-audit` cell shows as skipped/absent. Skipped is not a pass, so #1697 can
never be accepted on its own hopf - the gap is in the path mapping, not in the docs content.

## Scope of this card

- Map `docs/internal/**/*.json` onto the existing `DOC_CHECKS` selection in `scripts/pr-gate-plan.py`
  (reuse the existing docs-audit group; do not invent a second audit path or a new workflow).
- Selector regression coverage, both directions:
  - positive: a diff touching a `docs/internal/*.json` path selects `documentation-audit`;
  - negative: an unrelated JSON path (outside `docs/internal/`) does not select it.
- Preserve the fail-closed behaviour for unknown paths (the broad fallback must stay broad, and unknown
  paths must keep showing the broad fallback in the plan artifact).
- Prove exact-head selection: a hosted run on the candidate head shows the `documentation-audit` cell
  executed, not skipped. Record run id + cell conclusion in the evidence akte.

## Boundaries

- No product behaviour change; no change to the documentation content of #1697.
- `.github/workflows/ci.yml` changes stay minimal and are owned by the owner; the planner change is the
  functional part.
- After this card merges, 0428-131 must hopf onto the new develop and rerun, because its own
  base-abstand then touches `scripts/pr-gate-plan.py` (my base-distance rule).

## Acceptance

- Planner unit tests pass locally and in CI, including the two new selector cases with test IDs mapped
  to their gate (CI intake rule: every new test is executed by the GitHub CI).
- A hosted run on the exact head shows `documentation-audit` executed for a `docs/internal/*.json` diff.
- Evidence akte: `evidence/r28-welle4-2026-11-19/prgate-docs-internal-mapping/fix-1.md`.
