# pr-inventory — PR Inventory Cleanup Evidence

**Mission:** `coordinator/missions/pr-inventory.txt`
**Worker:** Ornith-Worker (lane pr-inventory)
**Start:** 2026-11-01
**Repo:** baseharbor (origin = git@github.com:mcpdev80/baseharbor.git)
**Scope:** NO code. Evidence only + consequences (close/supersede/blocked/ready). No merge, no ruleset, no subagent/task spawn, no codeman spawn/rm/send except the final handoff post.

---

## ## PLAN-Checkliste

- Step 0: todo (GUI) + board JSON + this PLAN (§4.4)
- Step 1: enumerate all 20 open PRs
- Step 2: ancestry check head vs develop
- Step 3: twin/duplicate detection via git patch-id
- Step 4: file-conflict check vs #1258
- Step 5: known candidates (1254/1257, 1231/1232, 1225/1236, 1238/1239/1243/1244/1247, 1248/1249 freeze, 1220/1222/1226/1229/1237)
- Step 6: #1160 dependabot — verify gate binding, rebase+push, watch PRSC to terminal
- Step 7: results table + per-PR witnesses (SHA, ls-remote, patch-id, CI)
- Step 8: planning card 'pr-inventory-2026-11' via plan.py
- Step 9: handoff post 35cdb02e...

---

## Develop reference

- Remote `develop` HEAD (ls-remote): `790e5426e566017b397761b36ae65c8388a0f5ad` (this IS merged PR #1260 "ci/gate-map: bind go.mod/go.sum to build-test gates")
- Local branch `develop` in this worktree: `5c903560...` (a forward-merge of develop into a work branch — diverged from remote; **REMOTE develop is authoritative for ancestry**)

## Method witnesses

- `git ls-remote origin develop` -> `790e5426...` (SSH, mcpdev80/baseharbor)
- 20 open PRs via `gh api repos/mcpdev80/baseharbor/pulls?state=open`; none merged (mergeCommit=null)
- Ancestry: `git merge-base --is-ancestor <head> 790e5426` for all 20 -> **all NOT ancestor of develop**
- Twins: `git diff <merge-base> <head> | git patch-id --stable` -> #1254 == #1257 patch-id `23acb1dd4bb913ed1e8c619178b2ba60010b203f` (byte-identical targeted-integration.yml hunk)
- #1160 CI failure root (run 41341879087, job 124954000825): `BLOCKED: coverage-unresolved: unknown impact for go.mod; unknown impact for go.sum`
- #1160 fix present in develop: `git show 790e5426:scripts/pr-gate-plan.py` has `elif path in ('go.mod', 'go.sum'): area = 'go-module-dependency'; require(CODE_CHECKS); require(CLI_CHECKS)` — comment explicitly: "Without this branch a Dependabot-only go.mod/go.sum diff fell to 'unknown impact' catch-all and left PR Selected Checks coverage-unresolved (#1160)."

## Open PR inventory (20)

| # | head SHA | base | merge? | disposition | witness |
|---|----------|------|--------|-------------|---------|
| 1258 | d11b12c3… | develop | no | **ACTIVE — keep** (lead migration PR, 10 files, own work in progress) | CI FAIL 3 (env), 5 ok |
| 1257 | 8207d018… | develop | no | **ACTIVE — keep** (newer twin; targeted rootless-runtime step on runtime-validation/ha/ refs, not in develop) | identical to 1254 |
| 1254 | a6e79c76… | develop | no | **CLOSE superseded by #1257** | identical patch-id 23acb1dd (created 15:15 vs 17:39) |
| 1249 | 22f55b96… | develop | no | **FROZEN — keep, status note** (mission: EINFRIEREN, do not touch) | ci.yml only |
| 1248 | 5aa85f05… | develop | no | **FROZEN — keep, status note** (mission: EINFRIEREN) | ci.yml + pr-gate-plan.py |
| 1247 | 80a16138… | develop | no | **blocked-on-#1258** (touches mcp-lifecycle, observability, podman-acceptance + ci-podman-gh-runtime.sh) | overlap with #1258 |
| 1244 | 46bef235… | develop | no | **blocked-on-#1258** (touches ci.yml, adds ci-podman-gh-runtime.sh) | overlap with #1258 |
| 1243 | 5b5ba323… | develop | no | **blocked-on-#1258** (runtime-broker.yml + runtime-s3-acceptance.yml = #1258 migration files) | overlap with #1258 |
| 1239 | 55d32c18… | develop | no | **blocked-on-#1258** (ci.yml, nextjs-greenfield-e2e, ci-core-rootless-runtime.sh) | overlap with #1258 |
| 1238 | 38073e9e… | develop | no | **blocked-on-#1258** (mcp-lifecycle, observability, podman-acceptance) | overlap with #1258 |
| 1237 | 029bb433… | main | no | **legacy — keep, log** (base main; 1 file; no overlap) | ancestry+CI logged |
| 1236 | 8155a1dc… | develop | no | **keep — resolver offshoot** (superset scope of #1225, both open, overlapping CI-gate resolver work) | 8 files, both open |
| 1232 | 34e60037… | develop | no | **keep — o265** (newer engine probe; successor of #1231) | 3 files |
| 1231 | b3dcb602… | develop | no | **keep — o261** (predecessor engine probe; 1232 supersedes scope) | 2 files |
| 1229 | 2337286e… | develop | no | **keep — legacy stock** (service-binding core-390; ancestry+CI logged) | 5 files |
| 1226 | d2fc3432… | develop | no | **keep — receipt enforcement** (ci.yml + pr-gate-plan.py; overlaps #1258 ci) | 5 files |
| 1225 | d3e6d383… | develop | no | **keep — resolver offshoot** (pr-gate-plan.py resolver checks; sibling of #1236) | 5 files |
| 1222 | b93d2fdd… | develop | no | **keep — source-neutral findings** (6 files, no file overlap) | 6 files |
| 1220 | 5d5b5c30… | develop | no | **keep — cleanup orphaned runtime** (3 files, no overlap) | 3 files |
| 1160 | 88604ee6… | develop | no | **REBASE+PUSH on develop; watch PRSC; ready-to-merge if green** (gate binding now resolves go.mod/go.sum coverage) | go.mod/go.sum bump |

## Detailed reasoning

### #1254 superseded by #1257 (close)
- #1254 created 2026-11-01T15:15:30Z, #1257 created 2026-11-01T17:39:54Z (newer).
- #1257 title literally: "candidate of #1254 on current develop".
- Identical diff: both add the same 5-line "Prepare verified rootless runtime" step to `.github/workflows/targeted-integration.yml` (patch-id `23acb1dd...`).
- Not in develop's version (develop uses a broader `[rootless-runtime]` commit-message trigger, not the specific `runtime-validation/ha/` ref condition), so #1257 carries real, non-duplicated value.
- Consequence: `gh pr close 1254` with comment "superseded by #1257".

### Chain PRs 1238/1239/1243/1244/1247 => blocked-on-#1258
- #1258 is the active "runner migration" PR touching the 7 migration workflow files (ci.yml, mcp-lifecycle-acceptance.yml, nextjs-greenfield-e2e.yml, observability-acceptance.yml, podman-acceptance.yml, runtime-broker.yml, runtime-s3-acceptance.yml) plus scripts.
- Each chain PR modifies at least one of those exact files (overlap check above).
- #1258's version of the shared files already contains each chain PR's core change (e.g. runtime-broker.yml: `runs-on: ubuntu-latest` + extra BASEHARBOR_TEST_RUNTIME/rootless-runtime additions; ci.yml: ubuntu-latest migration) — the chain PRs are in-flight sub-components of the same migration.
- Per mission rule (c): PRs touching the 7 migration workflow files must NOT be closed; note blocked-on-#1258.

### #1225 vs #1236 (resolver offshoots)
- Both register resolver checks in the trusted executor / CI PR gate; overlapping scope (pr-gate-plan.py, ci.yml, podman-acceptance.yml, test files).
- #1236 is the larger superset (adds pr-authenticated-results.py, ci-core-rootless-runtime.sh changes); #1225 is rv1224 forward-fix.
- Both still open, both with failing CI. Neither merged into develop. No clear single owner/merge order — flag as keep for Owner triage; do not close either.

### #1231 (o261) vs #1232 (o265)
- #1232 created later (2026-10-31T02:19 vs #1231 2026-10-30T20:05); title "independent of BASEHARBOR_TEST_RUNTIME; podman behind LookPath boundary (o265)".
- #1232 supersedes #1231's scope (same engine-probe area, newer). Both open, both failing CI. Flag keep/successor; no close without Owner confirmation of supersession policy.

### #1160 dependabot (rebase + push + watch) — DONE, ready-to-merge
- Root cause of CI block: go.mod/go.sum "unknown impact" -> coverage-unresolved (run 41341879087, job 124954000825).
- Fixed in develop: pr-gate-plan.py now classifies go.mod/go.sum as go-module-dependency, binds CODE_CHECKS+CLI_CHECKS -> coverage resolved.
- Action (authorized by mission): rebase `dependabot/go_modules/go_modules-315d795eac` on develop(790e5426); force-with-lease push `88604ee6 -> b756d008`. Net diff vs develop still exactly go.mod + go.sum (go-jose 4.1.4→4.1.6, +75/-50).
- Eigenes-Run CI run **41355831582** -> conclusion **SUCCESS** (terminal, completed 2026-11-01T22:13:14Z). Green gates: PR Selected Checks SUCCESS; PR · Validation · source-contracts/cli-build/cli-vet/cli-guided-tests SUCCESS; PR · Trusted Plan SUCCESS. (Targeted HA / Release Preflight skipped — no Go native runtime change needed.)
- **Verdict: #1160 is ready-to-merge. Per mission: NOT merged by this worker** — awaiting Owner/Codex-MERGE.

---

## Handoff summary

- **closed = 1** — #1254 closed (superseded by #1257, identical patch-id).
- **ready = 1** — #1160 ready-to-merge (rebase-pushed b756d008; CI run 41355831582 SUCCESS). NOT merged.
- **declared/erklaert = 18** — all 20 open PRs dispositioned in the table above. Of these: 2 active keep (1258, 1257), 2 frozen keep (1248, 1249), 5 blocked-on-#1258 (1238/1239/1243/1244/1247), 9 need Owner triage (1220/1222/1225/1226/1229/1231/1232/1236/1237), 1 ready (1160).
- **Remaining Owner actions:** merge #1160 (or decline); decide merge order for resolver offshoots #1225/#1236 and engine probes #1231/#1232; confirm frozen #1248/#1249; close/supersede remaining duplicates.
- No product code, no ruleset, no subagent/task spawn, no codeman spawn/rm/send.

## END_LINE
END_DONE pr-inventory: geschlossen=1 ready=1 erklaert=20 | 20/20 offene PRs dispositioniert; #1254 als Superseded geschlossen, #1160 dependabot auf develop rebase-pushed (b756d008) und CI-Run 41355831582 SUCCESS => ready-to-merge (nicht selbst gemergt); 5 PRs blocked-on-#1258, 4 frozen/active keep, 9 benoetigen Owner-Triage.
