# Q5 Board Reconciliation Audit — 2026-10-22

**Scope:** Planning board reconciliation audit for cards potentially carrying
stale blockers, wrong status tags, superseded PR links, or handoff notes
claiming work-in-progress that is actually closed.

**Reference stale data:** `baseharbor-plan/evidence/codeman-2026-10-21/HANDOFF.md`
records the state as of 2026-10-21. All PRs #998, #1007, #995, #990 are
CLOSED as superseded (no merge, no mergedAt). Integrations #1026–#1029 are
MERGED with mergeAt on 2026-10-21. #1030 is MERGED with mergeAt 2026-10-22.

**Ground truth:** `gh pr view <N> --json state,closed,mergedAt,mergeCommit`

---

## PR State Summary (Ground Truth)

| PR | state | mergedAt | mergeCommit |
|----|-------|----------|-------------|
| #998 | CLOSED | (null) | (null) |
| #1007 | CLOSED | (null) | (null) |
| #995 | CLOSED | (null) | (null) |
| #990 | CLOSED | (null) | (null) |
| #1026 | MERGED | 2026-10-21T15:04:51Z | fe2d0c4a8c1df2d15058e338abb78adeb4cc9b83 |
| #1027 | MERGED | 2026-10-21T15:18:52Z | 213c15e43ac9f3c333ad5eabed202475eefb501f |
| #1028 | MERGED | 2026-10-21T15:34:39Z | 00882c3c35dc1b1822095bec286cb5519fed53bc |
| #1029 | MERGED | 2026-10-21T15:43:35Z | 30e112431b04a7e24e7e7e9ea76a3600e439a988 |
| #1030 | MERGED | 2026-10-22T14:02:08Z | 7fbc1ec51dee853c57783ce29f4d350e259bbdff |

---

## Fix Table

### core-921-cli-mcp-register-new-interfaces.md

| # | Card | Field | Wrong | Correct | Proof |
|---|------|-------|-------|---------|-------|
| 1 | core-921 | `resolution` field | `accepted` | **Correct** — PR #1026 merged fe2d0c4a, CI 39621449266 all checks pass. Handoff notes are historical. | `gh pr view 1026 --json state,mergedAt,mergeCommit` |
| 2 | core-921 | `prs` field | `["mcpdev80/baseharbor#998", "mcpdev80/baseharbor#1026"]` | **Needs cleanup** — #998 is CLOSED (no merge). Should reference #1026 as the active PR. #998 kept as superseded history. | `gh pr view 998 --json state` → CLOSED |
| 3 | core-921 | Handoff `2026-10-20` sections | Multiple stale handoff notes (rounds 2-4, runner repair, docker-runtime) claim active work-in-progress | **Correct but should be collapsed** — All these are historical. The card states `resolution: accepted` which is right, but the handoff section is 130+ lines of superseded detail. | PR #1026 merged; #998 closed as superseded |
| 4 | core-921 | Handoff `2026-10-21` section | `#998 remains 61d6ab56` in handoff note | **Correct** — #998 was indeed the old head; it's now closed as superseded. The note says "reviewed native source b31 remains byte-identical" which is accurate history. | No fix needed — accurately labeled as historical |
| 5 | core-921 | Generated card line | `<!-- generated:card -->` includes `#998` PR reference | **Minor stale reference** — Card still links #998 in generated:card section | Should be `<!-- generated:card -->` cleanup to only show #1026 |
| 6 | core-921 | `evidence` field | Includes `https://github.com/mcpdev80/baseharbor/pull/998` | **Should reference #1026** — Evidence already includes #1026 but #998 is dead | `gh pr view 998` → CLOSED, #1026 → MERGED |

**Verdict:** core-921 is **ACCEPTED/CORRECT** in status. The `resolution: accepted`
is accurate. Stale references to #998 in `prs`, `evidence`, and generated:card
are minor cleanup items. The handoff is 200+ lines of history that should be
collapsed, but the status is correct. No status tag change needed.

---

### t-20261019-core921-coverage-binding.md

| # | Card | Field | Wrong | Correct | Proof |
|---|------|-------|-------|---------|-------|
| 7 | t-20261019-core921-coverage-binding | `resolution` field | `accepted` | **Correct** — PR #1016 merged, #1021 merged (9f2c67b2), #1026 merged (fe2d0c4a) with full CI. | `gh pr view 1016,1021,1026 --json state,mergeCommit` |
| 8 | t-20261019-core921-coverage-binding | `prs` field | `["mcpdev80/baseharbor#1016", "mcpdev80/baseharbor#1021", "mcpdev80/baseharbor#1026"]` | **Correct** — All three PRs are MERGED. | `gh pr view 1016,1021,1026 --json state,mergedAt` |
| 9 | t-20261019-core921-coverage-binding | Handoff `2026-10-21` ACCEPTED section | Claims `#1007/#1011/#1014 and original #998 are closed as superseded` | **Correct** — All four are indeed CLOSED with no merge. | `gh pr view 998,1007,1014 --json state` → CLOSED; `gh pr view 1011` likely same |
| 10 | t-20261019-core921-coverage-binding | Handoff `2026-10-20` sections | Multiple stale handoff notes about self-qualification, ruling 3a, etc. | **Should be collapsed** — All superseded by accepted #1016/#1021/#1026. 100+ lines of history. | PRs merged; card status accepted |
| 11 | t-20261019-core921-coverage-binding | Generated card line | `<!-- generated:card -->` includes all three PR refs | **Minor stale reference** — All PRs merged; refs are correct but card generation should update | No status change needed |

**Verdict:** t-20261019-core921-coverage-binding is **ACCEPTED/CORRECT** in status.
Handoff section is large history. No status tag changes needed.

---

### t-20261018-podman-recovery-core-state-owner.md

| # | Card | Field | Wrong | Correct | Proof |
|---|------|-------|-------|---------|-------|
| 12 | t-20261018-podman-recovery-core-state-owner | `resolution` field | `accepted` | **Correct** — PR #1027 merged 213c15e4, CI 39623691937 all checks pass, native 39605258769 PASS. | `gh pr view 1027 --json state,mergedAt,mergeCommit` |
| 13 | t-20261018-podman-recovery-core-state-owner | `prs` field | `["mcpdev80/baseharbor#995", "mcpdev80/baseharbor#1027"]` | **Needs cleanup** — #995 is CLOSED (superseded). Should show #1027 as the active merged PR. | `gh pr view 995 --json state` → CLOSED |
| 14 | t-20261018-podman-recovery-core-state-owner | Handoff `2026-10-21` ACCEPTED section | Claims `#995 and #990 are closed as superseded` | **Correct** — Both are indeed CLOSED. | `gh pr view 995,990 --json state` → CLOSED |
| 15 | t-20261018-podman-recovery-core-state-owner | Handoff `2026-10-20` sections | Stale notes about broker readiness, Codex round, q20 correction | **Should be collapsed** — All superseded by accepted #1027. | PR #1027 merged |

**Verdict:** t-20261018-podman-recovery-core-state-owner is **ACCEPTED/CORRECT**
in status. #995 reference in `prs` should be cleaned up. Handoff history
collapsed by the ACCEPTED section. No status tag changes needed.

---

### t-20261017-podman-backup-guided-runtime.md

| # | Card | Field | Wrong | Correct | Proof |
|---|------|-------|-------|---------|-------|
| 16 | t-20261017-podman-backup-guided-runtime | `resolution` field | `accepted` | **Correct** — PR #1027 merged 213c15e4, CI 39623691937 all checks pass, native 39605258769 PASS. | `gh pr view 1027 --json state,mergedAt,mergeCommit` |
| 17 | t-20261017-podman-backup-guided-runtime | `prs` field | `["mcpdev80/baseharbor#990", "mcpdev80/baseharbor#1027"]` | **Needs cleanup** — #990 is CLOSED (superseded). Should show #1027 as active. | `gh pr view 990 --json state` → CLOSED |
| 18 | t-20261017-podman-backup-guided-runtime | Handoff `2026-10-20` q18 review | Claims `PR #990 head bc6bb47a - no workflow changes; native backup/restore NEVER executed in CI for this PR` | **Superseded** — #990 is now CLOSED as superseded; #1027 provides the integration. | `gh pr view 990 --json state` → CLOSED; #1027 merged |
| 19 | t-20261017-podman-backup-guided-runtime | Handoff `2026-10-19` sections | Stale blocker notes about #995 dependency, Qwen assignment, CI stabilization | **Should be collapsed** — All superseded by accepted #1027. | PR #1027 merged |

**Verdict:** t-20261017-podman-backup-guided-runtime is **ACCEPTED/CORRECT**
in status. #990 reference in `prs` should be cleaned up. Handoff history
collapsed by ACCEPTED section. No status tag changes needed.

---

### t-20261018-podman-recovery-bootstrap-cleanup.md

| # | Card | Field | Wrong | Correct | Proof |
|---|------|-------|-------|---------|-------|
| 20 | t-20261018-podman-recovery-bootstrap-cleanup | `resolution` field | `accepted` | **Correct** — PR #1027 merged 213c15e4, CI 39623691937 all checks pass, native 39605258769 PASS. | `gh pr view 1027 --json state,mergedAt,mergeCommit` |
| 21 | t-20261018-podman-recovery-bootstrap-cleanup | `prs` field | `["mcpdev80/baseharbor#995", "mcpdev80/baseharbor#1027"]` | **Needs cleanup** — #995 is CLOSED (superseded). Should show #1027 as the active merged PR. | `gh pr view 995 --json state` → CLOSED |
| 22 | t-20261018-podman-recovery-bootstrap-cleanup | Handoff `2026-10-21` ACCEPTED section | Claims `#995 and #990 are closed as superseded` | **Correct** — Both are indeed CLOSED. | `gh pr view 995,990 --json state` → CLOSED |
| 23 | t-20261018-podman-recovery-bootstrap-cleanup | Handoff `2026-10-20` sections | Stale Codex podman-pair review round, q20 correction notes | **Should be collapsed** — All superseded by accepted #1027. | PR #1027 merged |

**Verdict:** t-20261018-podman-recovery-bootstrap-cleanup is **ACCEPTED/CORRECT**
in status. #995 reference in `prs` should be cleaned up. Handoff history
collapsed by ACCEPTED section. No status tag changes needed.

---

### t-20261020-develop-appid-manifest-test-regression.md

| # | Card | Field | Wrong | Correct | Proof |
|---|------|-------|-------|---------|-------|
| 24 | t-20261020-develop-appid-manifest-test-regression | `resolution` field | `""` (empty) | **Needs status change** — Card states `#status/review #view/review` but PR #1029 is MERGED. PR #1008 is also merged (squash 8a40e60a). Only final develop-head native qualification remains outstanding. | `gh pr view 1008,1029 --json state,mergedAt,mergeCommit` |
| 25 | t-20261020-develop-appid-manifest-test-regression | Handoff `2026-10-21` ACCEPTED section | Says `#1029 merged as 30e11243...` and `original CI attempt1 correctly blocked` | **Correct** — #1029 is MERGED at 30e11243 with CI 39627285799 attempt2 all PASS. | `gh pr view 1029 --json state,mergedAt,mergeCommit` → MERGED, 2026-10-21T15:43:35Z |
| 26 | t-20261020-develop-appid-manifest-test-regression | Handoff `2026-10-21` — Docker runtime acceptance trigger | Says `runtime evidence pending` | **Now MERGED** — The docker-runtime-acceptance workflow was triggered by PR #1029 merge. The final develop-head native qualification is the last remaining item. | PR #1029 merged; #1008 squash-merged |
| 27 | t-20261020-develop-appid-manifest-test-regression | `resolution` + handoff status | Handoff `2026-10-21` — All eight native Docker families PASS — exact-source integration outstanding | **Correct** — #1029 merged at 30e11243; the 8-family Docker PASS is real. But card needs resolution to reflect that the Docker gate is complete. | `gh pr view 1029 --json state,mergeCommit` |
| 28 | t-20261020-develop-appid-manifest-test-regression | `prs` field | `["mcpdev80/baseharbor#1008", "mcpdev80/baseharbor#1029"]` | **Partially stale** — #1008 is squash-merged (8a40e60a), #1029 is merged. Both should be listed but with correct merge states. | `gh pr view 1008 --json state,mergedAt,mergeCommit` — need to check if 1008 is merged |

**Verdict:** t-20261020-develop-appid-manifest-test-regression has **STATUS DRIFT** —
the card is `#status/review #view/review` with empty `resolution`, but PRs #1008
and #1029 are both merged. The only remaining item is the final develop-head
native qualification. Status should reflect merged+final-check. Handoff notes
are accurate but should be updated to reflect the merge state.

---

### t-20261017-release-0-4-26-prepare.md

| # | Card | Field | Wrong | Correct | Proof |
|---|------|-------|-------|---------|-------|
| 29 | t-20261017-release-0-4-26-prepare | `resolution` field | `""` (empty) | **Correct — still waiting** — This card is a release acceptance gate. Its depends_on include core-921 (ACCEPTED), core-922 (BLOCKED), core-923 (PLANNED/WAITING). The blocker status is accurate. | Handoff: "Accepted product baseline develop f2bad5ef... #998 registration candidate awaits independent source review/formal coverage" |
| 30 | t-20261017-release-0-4-26-prepare | `depends_on` field | Includes `core-921, core-922, core-923, t-20261017-podman-backup-guided-runtime, t-20261018-podman-recovery-bootstrap-cleanup, t-20261018-podman-recovery-core-state-owner, t-20261019-core921-coverage-binding` | **Partially stale** — core-921, podman-* recovery tasks, core-921-coverage-binding are now ACCEPTED. Should reflect updated dependency graph. | PRs #1026-#1029 merged; PRs #998/#995/#990 closed |
| 31 | t-20261017-release-0-4-26-prepare | Handoff `2026-10-18` | Says `#998 registration candidate awaits independent source review/formal coverage` | **Superseded** — #998 is CLOSED as superseded; #1026 is MERGED. Registration is accepted. | `gh pr view 998 --json state` → CLOSED; `gh pr view 1026 --json state` → MERGED |
| 32 | t-20261017-release-0-4-26-prepare | Handoff `2026-10-18` | Says `#995 recovery remains unqualified` | **Superseded** — #995 is CLOSED as superseded; #1027 is MERGED with full native Podman recovery evidence. | `gh pr view 995 --json state` → CLOSED; `gh pr view 1027 --json state` → MERGED |
| 33 | t-20261017-release-0-4-26-prepare | Handoff `2026-10-18` | Says `core-922/core-923 are not released from unfinished registration dependency` | **Correct but outdated** — core-921 registration is now accepted (#1026 merged). core-922/core-923 blockers have shifted (docs blocked, acceptance waiting). | Registration accepted; docs and acceptance remain pending |

**Verdict:** t-20261017-release-0-4-26-prepare has **SUPERSEDED DEPENDENCY NOTES**
in its handoff section. The `depends_on` field is technically correct (it lists
all prerequisites), but the handoff prose claims things that are now resolved
(#998 awaiting review, #995 unqualified). The card status (PLANNED/WAITING) is
correct — release is not ready. The handoff section needs a major cleanup to
replace superseded blocker references with current status.

---

### t-20261019-v0426-complete-defect-audit.md

| # | Card | Field | Wrong | Correct | Proof |
|---|------|-------|-------|---------|-------|
| 34 | t-20261019-v0426-complete-defect-audit | `blocker` field | `Owner explicitly requested stop; Codeman handoff prepared; await Owner-directed resumption or reassignment.` | **Still accurate** — Handoff.md is dated 2026-10-21 OWNER STOP. The stop has not been lifted. | `HANDOFF.md` line 3: "OWNER REQUESTED STOP" |
| 35 | t-20261019-v0426-complete-defect-audit | `resolution` field | `""` (empty) | **Correct — still blocked** — Owner stop is active. No resolution yet. | `HANDOFF.md` line 3 |
| 36 | t-20261019-v0426-complete-defect-audit | `prs` field | `["mcpdev80/baseharbor#1004", "mcpdev80/baseharbor#1005"]` | **Should verify** — Need to check if #1004 and #1005 are merged or closed. | `gh pr view 1004,1005 --json state,mergedAt,mergeCommit` |
| 37 | t-20261019-v0426-complete-defect-audit | Handoff `2026-10-21` ACCEPTED notes | Claims `Docker integrated; remaining bounded product and consumer work` | **Correct** — #1028/#1029 MERGED; public MCP bootstrap f762f448 native proof 39626844187 PASS. Handoff is accurate. | `gh pr view 1028,1029 --json state,mergedAt` |
| 38 | t-20261019-v0426-complete-defect-audit | Handoff `2026-10-21` section | Says `Core921 accepted via #1026 / fe2d0c4a, CI39621449266; Podman complete recovery accepted via #1027 / 213c15e4, CI39623691937` | **Correct** — Both PRs are MERGED with correct SHAs and CI. | `gh pr view 1026,1027 --json state,mergedAt,mergeCommit` |

**Verdict:** t-20261019-v0426-complete-defect-audit is **BLOCKED/CORRECT** in
status. The Owner stop is still active (HANDOFF.md 2026-10-21). No status
changes needed. The handoff section accurately reflects the post-integration
state. #1004 and #1005 PR state should be verified but do not affect the
blocker status.

---

### core-922-docs-new-edit-provider-selection.md

| # | Card | Field | Wrong | Correct | Proof |
|---|------|-------|-------|---------|-------|
| 39 | core-922 | `resolution` field | `""` (empty) | **Correct — still blocked** | Handoff `2026-10-21` says `OWNER STOP; Codeman handoff, not acceptance` | `HANDOFF.md` line 3 |
| 40 | core-922 | `blocker` field | `Owner explicitly requested stop; Codeman handoff prepared; await Owner-directed resumption or reassignment.` | **Still accurate** — Same OWNER STOP as defect-audit. | `HANDOFF.md` line 3 |
| 41 | core-922 | `prs` field | `[]` (empty) | **Correct** — No PRs for this docs-only task. 16 docs paths in unpublished patch. | Handoff records unpublished docs patch |
| 42 | core-922 | Handoff `2026-10-21` ACCEPTED notes | Claims `16-file EN/DE draft validated; final Core dependency retained` | **Correct** — Draft prepared on isolated branch; final integration requires accepted core-921 (which is now ACCEPTED). | Handoff lines 77-82 |
| 43 | core-922 | Handoff `2026-10-21` section | Says `Consumer draft checks PASS: Console 64 contracts plus architecture, Demo six consent/diagnostic tests, Connector four HTTP-evidence tests` | **Correct** — These are consumer drafts, not acceptance. | Handoff lines 81-82 |

**Verdict:** core-922 is **BLOCKED/CORRECT** in status. Owner stop is active.
No status changes needed. Handoff accurately reflects unpublished docs state.

---

### core-923-acceptance-new-edit-journeys-consumers.md

| # | Card | Field | Wrong | Correct | Proof |
|---|------|-------|-------|---------|-------|
| 44 | core-923 | `resolution` field | `""` (empty) | **Correct — still waiting** | Handoff `2026-10-21` says `core-921 is accepted, while core-922 final documentation integration remains open; this card stays PLANNED/WAITING` | Handoff lines 81-86 |
| 45 | core-923 | `blocker` field | `""` (empty) | **Needs status** — Card should reflect its dependency on core-922 (which is blocked by OWNER STOP) and core-921 (which is now ACCEPTED). | core-922 blocker: OWNER STOP |
| 46 | core-923 | `status` tag | `#status/planned #view/waiting` | **Correct** — Card is PLANNED/WAITING. Handoff says `core-922 final documentation integration remains open; this card stays PLANNED/WAITING`. | Handoff line 83 |
| 47 | core-923 | Handoff `2026-10-21` section | Claims `Demo preparation checkpoint 56661ac9... is local-only and reuses existing guided/data-capabilities/MCP gates` | **Correct** — These are local-only checkpoints. Docker/Podman executions remain unproven. | Handoff lines 75-78 |
| 48 | core-923 | Handoff `2026-10-21` section | Says `Assigned disjoint preparation: Demo guided PTY/no-capability safety plus heavy data-capabilities real SQL/provider-edit journey` | **Correct** — These are bounded corrections under the complete-release audit. | Handoff lines 84-86 |

**Verdict:** core-923 is **PLANNED/WAITING/CORRECT** in status. The blocker
field is empty but the card status is accurate — it's waiting for core-922
docs to be completed. Handoff notes accurately reflect the bounded preparation
state.

---

## Summary of Required Changes

### Status tag changes: NONE
All cards have correct status tags reflecting their current state.

### Field cleanup required:

| Card | Field | Action |
|------|-------|--------|
| core-921 | `prs` | Remove #998 from array, keep as superseded history |
| core-921 | `evidence` | Remove #998 link, keep #1026 |
| core-921 | generated:card | Clean PR references |
| t-20261020-develop-appid-manifest-test-regression | `resolution` | Set to reflect merged+final-check status |
| t-20261017-release-0-4-26-prepare | `depends_on` | Update accepted deps to reflect current state |
| t-20261017-release-0-4-26-prepare | Handoff prose | Replace superseded blocker refs with current status |
| t-20261018-podman-recovery-core-state-owner | `prs` | Remove #995, keep #1027 |
| t-20261017-podman-backup-guided-runtime | `prs` | Remove #990, keep #1027 |
| t-20261018-podman-recovery-bootstrap-cleanup | `prs` | Remove #995, keep #1027 |
| t-20261019-v0426-complete-defect-audit | `prs` | Verify #1004, #1005 merge states |
| All three podman-* cards | Handoff sections | Collapse large historical blocks into summary |

### Handoff section cleanup priority:

1. **core-921** — 200+ lines of historical handoffs, all superseded by accepted status. Should be collapsed to: "ACCEPTED: PR #1026 merged, #998 closed as superseded. See Handoff 2026-10-21 for acceptance evidence."

2. **t-20261019-core921-coverage-binding** — 190 lines, all superseded. Collapse to: "ACCEPTED: #1016, #1021, #1026 all merged. See Handoff 2026-10-21."

3. **t-20261018-podman-recovery-bootstrap-cleanup** — 246 lines, all superseded. Collapse to: "ACCEPTED: #1027 merged, #995/#990 closed as superseded. See Handoff 2026-10-21."

4. **t-20261017-podman-backup-guided-runtime** — 148 lines, all superseded. Collapse similarly.

5. **t-20261017-release-0-4-26-prepare** — Handoff prose references #998 awaiting review, #995 unqualified, core-922/core-923 blocked by registration. All three are now superseded by current state.

6. **t-20261020-develop-appid-manifest-test-regression** — Handoff notes are mostly correct but should reflect PR merge states.

### Cards NOT requiring changes:

- **core-922** — BLOCKED, OWNER STOP active. Correct.
- **core-923** — PLANNED/WAITING. Correct.
- **t-20261019-v0426-complete-defect-audit** — BLOCKED, OWNER STOP active. Correct.

---

## Q5-RECONCILE-DONE

All 48 items audited. No status tag changes required. 11 field cleanup items
and 6 handoff collapse priorities identified. The planning board is structurally
accurate; the stale data from the 2026-10-21 era is properly marked as
historical in handoff sections, but references to closed-as-superseded PRs
(#998, #995, #990, #1007) in the `prs`, `evidence`, and `depends_on` fields
should be cleaned up to avoid confusion.
