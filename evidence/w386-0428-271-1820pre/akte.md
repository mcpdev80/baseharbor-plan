# w386-0428-271-1820pre — disjoint pre-work akte

- LANE w386-0428-271-1820pre, CARD 0428-271, REPO baseharbor, PR #1820
- TYPE: disjoint pre-work (local hop + findings; NO push, NO hosted run, NO merge, NO product/config change)
- plan-main witness (commit SHA, local worktree HEAD): `8cc2a3dabb196c2773b5148e6369be890127f9af`
- plan-main witness (origin/main via ls-remote): `8cc2a3dab` `refs/heads/main`
- real product remote (git remote -v): `baseharbor → https://github.com/mcpdev80/baseharbor.git` (origin also github here; lane-origin is the github.com/mcpdev80 URL)
- real planning remote (git remote -v): `origin → https://github.com/mcpdev80/baseharbor-plan.git`

## 4-FIELD

### F1 — witnesses (a)
- `gh pr view 1820 --repo mcpdev80/baseharbor --json headRefOid,headRefName,baseRefName,state,mergeable`:
  `{"baseRefName":"develop","headRefName":"fix/broker-build-identity","headRefOid":"8f6b2444bdc9baabf4f492e930533c7c36406979","mergeable":"MERGEABLE","state":"OPEN"}`
- PR #1820 is OPEN, base = develop, head branch = `fix/broker-build-identity`, head SHA `8f6b2444b` (remote witness via ls-remote identical), mergeable = MERGEABLE.
- Reference akte paths from the mission (`evidence/2026-11-27/w255-0428-285-1820preflight.md`, `evidence/w255-0428-271-1820hop/akte.md`) do NOT exist on origin/main (ls not found above); the hop-akte was never published. This akte stands alone.

### F2 — hop (c): NO CONFLICT
- Local worktree built from PR branch head `8f6b2444bdc9baabf4f492e930533c7c36406979` (detached, PR branch ref `fix/broker-build-identity`) in `workers/worktrees/w386-0428-271-1820pre` (removed again after hop; no orphan).
- Base attestation: `git ls-remote origin develop → ea5218d72e263f21e79853b679af50074dab8c25`; `git merge-base --is-ancestor origin/develop HEAD` → DEVELOP IS NOT ANCESTOR of the PR head (expected: PR carries its own commits on top).
- `git merge origin/develop` (local only, then `git reset --hard` back to `8f6b2444b`): MERGE_EXIT=0, working tree clean, no conflict markers. Merge commit `0c58d6e1b` "Merge remote-tracking branch 'origin/develop' into HEAD". → **NO CONFLICT, NOOP hop.** No push, no force.

### F3 — checks/runs (d)
- `gh pr checks 1820`: all selected checks PASS on exact head `8f6b2444b`. Run id `45710380590`, event `pull_request`, status success (22m). Selected Runtime (atomic/docker/data-capabilities) Executed docker data-capabilities PASS (20m27s). No check named "superseded" is present; the checks list is current.
- Skipping (not red, expected pre-0.4.27): Main release checks, Draft Go, Exact full Pre-Release, Consumer Pins, Draft source and routing, Main release Go, Native Keycloak/Core, Native, Public Contracts, Selected Core-less, Release Source Preflight, Targeted HA docker/podman, Workstation onboarding, validate.
- Two qualifying run-IDs a NEW head needs (exact-head pair doctrine): run `45710380590` (pull_request) is ONE valid exact-head run on `8f6b2444b`. A second EXACT-HEAD qualified run requires close+reopen (`gh pr close --comment 'second exact-head hosted run trigger (coordinator-authorized)' && gh pr reopen`) — two distinct run IDs on the identical head. A rerun raises run_attempt on the SAME id and is VOID as pair evidence. This lane does NOT trigger either (pre-work boundary).

### F4 — chain finding (e)
- `git cherry -v origin/develop 8f6b2444b`: `#1820` adds its own 0428-271 commits (22ca61bb, 2f9f2f05, 514084f3, 28803d11) plus 0428-181 export commits `9f84f47a7` and `17381017b`, the `9140b2cbd` ci-reload, and `3859d4663`/`101291960` release-requirements add+drop. The single `-` line is the #1819 chore hop `b3c5055ad` (merged #1812 head 394559e + develop 28296a2e into the #1819 candidate) — i.e. #1820 does NOT re-carry the #1819 hop commit.
- `#1820 already contains #1819 core?` YES. `17381017b` (0428-181 RC1 fail-closed producer-path regression + RC2 byte/hash-stability, author `0428-061-sourcepull`, same author as #1820's own `22ca61bb`) is an ancestor of `8f6b2444b` (git merge-base --is-ancestor YES) and appears in #1820's OWN cherry `+` range; byte-identical at `cmd/baha/app_broker.go`. So #1820 carries the #1819 RC1/RC2 content already — not as a re-hop, but as a shared 0428-061-sourcepull commit. Overlap file for the 0428-181 Perses-export content: `cmd/baha/app_broker.go` (and the 0428-181 export path under `internal/metrics/perses_dashboard_provision.go` / `internal/metrics/perses_dashboard_provision_test.go`, both in #1820's changed set).
- `#1820 already contains #1812 core?` YES. Original #1812 head `394559ec6` (hop admitting #1812 onto develop) is an ancestor of `8f6b2444b`; #1812's `app_init_*` demo-login content is in #1820's tree. Overlap file for #1812 core: `cmd/baha/app_init_wizard.go` (changed by #1812 hop `394559ec6`; NOT changed by #1820 vs develop, i.e. it arrives via develop base, not #1820's own commits).
- The mission's named #1812 ref `c2dd3ff04` (w362 `scripts/test_pr_runtime_workflow_shape.py` narrow correction) is NOT an ancestor of `8f6b2444b` and NOT in #1820's changed set (#1820 does not touch that file vs develop); it is a later re-base commit, unrelated to what #1820 carries.

### Next-owner sentence
After the #1812 merge the chain #1812→#1819→#1820: #1819 is NOT yet merged (its hop `b3c5055ad` was rejected by #1820's cherry; #1820 only carries #1819's shared 0428-061-sourcepull content). #1820 itself is green and mergeable. **What becomes incumbent after the #1812 merge: re-derive #1819 onto the post-#1812 develop, confirm #1819's unique content vs #1820 is empty (it already carries the 0428-181 export work), then qualify + merge #1819 before #1820 (strict order #1812→#1819→#1820); #1820 needs a fresh exact-head run pair only once its head moves.** No action taken by this lane — no push, no hosted run, no merge, no product/config change.

## repo-rule compliance
- No product, config, workflow, or card-file edited. No push / force / workflow_dispatch / merge. No subagent. Local hop only; worktree removed after.

## cleanliness
- `docker ps -a` not run on any host (no container/compose started this lane). No compose projects to bring down.
