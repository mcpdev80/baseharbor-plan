---
id: t-20261119-r28-prgate-docs-internal-json-mapping
kanban_title: "0428-144 · docs/internal/**/*.json faellt"
card_number: "0428-144"
type: task
areas: [ci, docs]
release: v0.4.28
version: ""
parent: ""
owner: "Codex team (Owner-delegated Maintainer)"
kanban_status: active
kanban_lane: active
blocker: ""
wait_reason: ""
depends_on: []
repos: [mcpdev80/baseharbor]
evidence:
  - "https://github.com/mcpdev80/baseharbor/pull/1705"
  - "https://github.com/mcpdev80/baseharbor/commit/28fb427f057499efca705c1b7459e7653bd532a8"
  - "https://github.com/mcpdev80/baseharbor/actions/runs/44619193702"
resolution: ""
created: 2026-11-19
card_short_title: "docs/internal/**/*.json faellt"
prs: [mcpdev80/baseharbor#1705]

---

- [ ] t-20261119-r28-prgate-docs-internal-json-mapping · docs/internal/**/*.json faellt durch die DOC_CHECKS-verzweigung von pr-gate-plan.py und wird nie validiert #task #release/v0-4-28 #status/active #view/active #area/ci #area/docs #kind/task
    <!-- generated:card -->
    **Owner:** Codex team (Owner-delegated Maintainer)  
    **PR:** [baseharbor#1705](https://github.com/mcpdev80/baseharbor/pull/1705)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1705), [proof 2](https://github.com/mcpdev80/baseharbor/commit/28fb427f057499efca705c1b7459e7653bd532a8), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44619193702)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261119-r28-en-docs-warning-term](t-20261119-r28-en-docs-warning-term.md)  
**Owner:** Codex team (Owner-delegated Maintainer)  
**Priority:** not set  
**PRs:** [baseharbor#1705](https://github.com/mcpdev80/baseharbor/pull/1705)  
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

Current execution: PR #1705 merged as `28fb427f057499efca705c1b7459e7653bd532a8`. Exact head `0b5dd34713fe778aaf4d79dfa0b2a0600fc50e6a` on base `ab77e29d7c1cf981777e1069e51dfff82ffcf654`; hosted run `44619193702` passed PR Selected Checks, PR planner tests, CI policy, focused Python, source format, native gate plan and trusted plan. Local `scripts/ci-fast-check.sh` passed with 286 tests. Independent review found no blocker and prompted the added positive `.yaml` selector test. PR #1697 remains on its old base and old successful run skipped `documentation-audit`; the 0428-144 card remains active until #1697 hops and a new exact-head run executes that check for its internal JSON change.
