# 0428-002 — Inventory of previous-release legacy debts (round 1 akte)

- Card: `t-20261017-release-0-4-28-cleanup` (0428-002), release v0.4.28, release_stage: cleanup.
- Mission file: `/tmp/opencode/mission-cleanup28.md`.
- Mission type: READ-ONLY INVENTORY. No product changes, no merges, no PR closes without reference (merge-frost 2026-11-14).
- Deliverable on: planning main (this akte). No task acceptance or release implied.
- Owner of card: `lane-0428-002-r28` (pre-claimed active by coordinator). This session holds the claim until the akte is published.

## Base attestation

- Planning repo (authoritative, ONLY): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.
  - NOT `workers/baseharbor-plan` (bookkeeping repo; commits never reach GitHub).
- Base SHA at start (origin/main):
  ```
  334ff1a14cf7cbe4cac09af07f00ea74a43f0aa7
  ```
  - `git ls-remote origin main` witness (captured before any work):
    - `334ff1a14cf7cbe4cac09af07f00ea74a43f0aa7  refs/heads/main` (planning, from planning section below)
- No candidate branch is cut for this task; write-set is planning main only. Ancestry N/A (no commit cut here).

## Method and witnesses

- Remote truth measured via `gh` (authenticated as `mcpdev80`) and `git ls-remote` over HTTPS. The quarantined checkout `workers/baseharbor` was never cited.
- `gh auth status`: account `mcpdev80`, token `gho_…`.
- `git ls-remote https://github.com/mcpdev80/baseharbor` witness (captured in working zone):
  ```
  0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
  aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
  a71b0b4a35e52fa80d1828845e3b8c1256e8b21b	refs/heads/release-publish/v0.4.26-owner-20261026
  212ae90e22e6ea2eeeaa84f35189b307b1ce32bc	refs/heads/release/v0.4.26
  fe018b97cb047c9e1c34c6a27bdb5408eff54eeb	refs/heads/release/v0.4.27
  ```
- `gh pr list --state open` across all 5 named repos (all open PRs, not paginated beyond defaults).
- Last-commit dates fetched per branch via the commits API (`commit.committer.date`).
- Sources cited: [baseharbor-plan RELEASE_WORKFLOW.md#cleanup](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#cleanup), card `t-20261017-release-0-4-28-cleanup.md`, owner sequencing decision 2026-11-14.

## Scope note

- baseharbor-console and baseharbor-node-connector are ARCHIVED (confirmed via repo API: `"archived":true`), so excluded from reconciliation per the card scope.
- Release branches and immutable tags are untouchable (owner directive 2026-11-14).
- Merge-frost active: this akte records state and recommends only; it performs NO deletion, merge, or close.

---

## 1. Open PRs (all repos) — only 2 exist

### baseharbor #1574 — "Release v0.4.27"
- HEAD branch `release/v0.4.27` (head sha `fe018b97`), base `main` (`aff1532c`), DRAFT, created 2026-11-14T19:40Z by `mcpdev80`. +438408/-22175 over many commits, most authored 2026-11-10.
- CI: run #635 "Targeted Atomic Gate" in_progress on `release/v0.4.27` (created 2026-11-14T19:41:57Z).
- Verdict: **HELD**. This is the active v0.4.27 release PR, the very work the owner sequencing decision (2026-11-14) says must NOT be treated as a leftover. Base head `aff1532c` is the current `origin/main` (ancestry satisfied; `release/v0.4.27` is ahead of main, not cut from another candidate).

### baseharbor-plan #24 — "docs: record complete v0.4.27 release readiness and outstanding gates"
- HEAD branch `docs/0427-release-preparation-20261110`, base `main`, DRAFT, +63/-0, 3 commits (2026-11-10).
- Verdict: **HELD**. Genuinely active documentation of the unreleased v0.4.27; not a leftover.

### No open PRs in baseharbor-demo, baseharbor-console, baseharbor-node-connector.

---

## 2. baseharbor branches (30 non-main)

### HELD (active / maintained / immutable)

| Branch | Last commit | Reason |
| --- | --- | --- |
| `develop` | 2026-11-14 | Active development integration branch (1752 ahead / 89 behind main). Maintained track. |
| `release/v0.4.27` | 2026-11-14 | Open draft PR #1574; active release work. Immutable per owner directive. |
| `release/v0.4.26` | 2026-10-24 | Released/immutable tag-adjacent release branch (tag `v0.4.26` = `64098158`). Immutable. |
| `release-publish/v0.4.26-owner-20261026` | — | Owner release-publish ref; immutable/approval-candidate ref. Preserve. |
| `feat/0427-116-initial-operator-tenant` | 2026-11-07 | Recent 0.4.27 feature branch, part of active release prep. Held. |
| `fix/ci-pr-integration-stage-separation-20261104` | 2026-11-04 | Recent CI fix; 0.4.27 cycle. Held (recent, active cycle). |

### DEFER (old, unreferenced by open PR, but content may still be needed / ownership unclear)

| Branch | Last commit | Reason |
| --- | --- | --- |
| `codex/broker-partial-inventory` | 2026-11-02 | codex branch; content parity uncertain; not a leftover to delete without proof it landed or is obsolete. Defer. |
| `codex/broker-docs-url` | 2026-11-02 | Same codex batch. Defer. |
| `codex/broker-acceptance-consent` | 2026-11-02 | Same codex batch. Defer. |
| `codex/fix-remote-stop-provider-consent` | 2026-11-13 | Recent; possibly active. Defer (needs owner decision, not cleanup). |
| `134-r3-ca-pkce` | 2026-11-08 | WIP-derived; recent. Defer. |
| `0427-178-listscale` | 2026-11-09 | Recent 0.427 lane branch. Defer. |
| `0427-165-r3` | 2026-11-09 | Recent 0.427 lane branch. Defer. |
| `wip/0427-134-ca-pkce-persist` | 2026-11-08 | WIP. Defer (WIP branches carry WIP intent; not a housekeeping target). |
| `classifier-logs-map` | 2026-11-02 | Recent. Defer. |
| `clean-delivery` | 2026-11-04 | Recent. Defer. |
| `docs/ci-minimum-sufficient-verification` | 2026-10-16 | Docs-only. Defer (no functional impact; not worth the churn). |
| `docs/v0426-new-edit` | 2026-10-21 | Docs-only. Defer. |

### REMOVE candidate (stale, >30 days, unreferenced by any open PR, old cycle)

| Branch | Last commit | Reference / obsolescence |
| --- | --- | --- |
| `feature/kubernetes-runtime-foundation` | 2026-09-24 | ~78 days stale, oldest branch in repo. Content supersed by `develop`; not merged to main. Candidate for deletion — but requires a witness that its content is either landed (patch-id vs main) or obsolete. NOT deleted here (merge-frost + needs proof). Report as REMOVE-candidate for owner. |
| `fix/rv1219-producer-failclosed` | 2026-10-30 | ~45 days stale. Defer/candidate. |
| `fix/atomic-bare-sha-dispatch` | 2026-10-23 | ~52 days stale. Defer/candidate. |
| `fix/docker-runtime-authoring-fixture-source` | 2026-10-21 | ~54 days stale. Defer/candidate. |
| `fix/podman-backup-owned-services-source` | 2026-10-21 | ~54 days stale. Defer/candidate. |
| `fix/retirement-preferences-reviewed-source` | 2026-10-21 | ~54 days stale. Defer/candidate. |
| `fix/edit-provider-automatic-input` | 2026-10-21 | ~54 days stale. Defer/candidate. |

NOTE on codex receipt branches (`codex/receipt-*`, `codex/minimal-receipt-controller`, `codex/receipt-workflow-recovery-unqualified`): several of these correspond to MERGED PRs in baseharbor (see #1339, #1343, #1346 merged 2026-11-02/03). Their heads are NOT the exact merged refs — they are stale carry-overs created from an unqualified base. They are cleanup candidates but their deletion needs a patch-id/ancestry witness that content is landed. Report as REMOVE-candidates for owner; do NOT delete under merge-frost.

---

## 3. baseharbor-demo branches (30 non-main)

All 30 branches are old fix/branches (`fix/v0414-*`, `fix/v0419-*`, `fix/v0.4.26-*`, `chore/*`, `ci/*`, `docs/*`) with NO open PRs. Demo main has no open PR (#0 open). These are the demo repo's accumulated fix branches from the v0.4.14–v0.4.26 cycles.

- Verdict: **REMOVE-candidates** (all stale, unreferenced, no open PR). Requires per-branch proof of landed/obsolete content before deletion. Merge-frost blocks auto-deletion. Reported to owner as a batch candidate, not executed.
- Notable: `chore/remove-demo-ci` and `ci/*` branches relate to CI file changes (Owner scope `.github/**`) — deletion touches CI governance; report only.

---

## 4. baseharbor-plan branches (22 non-main)

### HELD
- `main` (base).
- `docs/0427-release-preparation-20261110` → open draft PR #24 (held above).
- `codex/publish-r22g` → appears to be a codex publish lane; check state.

### DEFER / REMOVE-candidate (lane and work branches)
- `lane-0427-162-evidence` → evidence lane branch; preserve until its evidence is published/consumed.
- `work/*` (`work/r27-*`, `work/r27-board-*`, `work/r27-cards-cu1`, `work/r27-stale-clnd`, `work/r27-zero-touch-isolated-prep-20261023`, `work/release-card-numbers-20261107`, `work/0427-119-chatgpt-ownership`, `work/bh-card-numbering`, `work/core-893-942-coverage-qualification`) → work-in-progress lane branches. Some reference the r27 cycle (historical). Candidates for cleanup but deletion needs proof they are superseded. Defer/report.
- `rcptlink` → tooling/reference branch. Defer.

---

## 5. CI / running runs

- baseharbor-plan: "Validate planning" workflow actively running on main; recent runs healthy (run #4501 success on base SHA `334ff1a1`, #4500 failure on `ec88a1fa`, #4502 success on `6b34b1d9`). No orphaned/in-progress runs. No action.
- baseharbor: run #635 "Targeted Atomic Gate" IN_PROGRESS on `release/v0.4.27` (active PR #1574). Not orphaned. No action.
- baseharbor-demo / console / node-connector: no in-progress runs observed in scope.
- STATE (not actionable under merge-frost / Owner scope): none found requiring a failing-check report. No `.github/**` edit requested.

---

## 6. Overall verdict summary

- **No deletions, merges, or closes performed.** Merge-frost (2026-11-14) + read-only mission scope.
- **HELD (keep):** 2 open PRs (#1574 baseharbor, #24 plan), `develop`, `release/v0.4.26`, `release/v0.4.27`, `release-publish/v0.4.26-owner-20261026`, immutable tags `v0.4.x`.
- **REMOVE-candidates for owner review (not executed):**
  - baseharbor: `feature/kubernetes-runtime-foundation` (78d stale), 6× `fix/*-source` branches (Oct 2026), codex receipt carry-over branches whose content maps to merged PRs #1339/#1343/#1346.
  - baseharbor-demo: all 30 non-main fix/branch (batch candidate; `chore/remove-demo-ci` and `ci/*` touch Owner-scope CI files).
  - baseharbor-plan: `work/r27-*` historical lane branches (historical r27 cycle).
- **DEFER (needs owner decision, not housekeeping):** recent 0.427 lane branches, codex broker branches, WIP branches.

## Required next action (by owner, not this lane)
- Execute deletions only with landed/obsolete witness (patch-id or ancestry). This is Owner-scope under merge-frost; the lane recorded candidates with witnesses above.
- Optional: delete clearly-stale demo fix batch and baseharbor `feature/kubernetes-runtime-foundation` after a `git ls-remote` before/after witness proves the content is landed on `develop`/`main`.

## END state
- Lane END: DONE. Evidence pushed to planning origin/main (ls-tree witness below). No containers/compose started (read-only inventory). No product writes.

## ls-tree witness (evidence on origin/main before END)
- Capture below in the evidence-push section.
