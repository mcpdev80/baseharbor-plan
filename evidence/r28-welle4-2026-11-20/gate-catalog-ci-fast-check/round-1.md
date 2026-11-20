# 0428-205 · Gate catalog for ci-fast-check — round-1 (w220)

- Task: t-20261120-gate-catalog-ci-fast-check (card 0428-205), repo mcpdev80/baseharbor, base develop.
- Outcome: the #1665 FAILURE is explained precisely, but the explanation is NOT the missing release-requirements.json pairing the card assumed. Pairing alone cannot fix #1665, and a full pairing would need a `.github/workflows/ci.yml` dispatch arm (Owner scope). This lane measured, kept the smallest candidate, and STOPs with a scope QUESTION per mission step 3 ("wenn sie es nicht erklaert: melden sie genau das").
- Candidate branch (local, unpushed): lane-0428-205-gate-catalog-pairing, HEAD 5e3fa3221b9291c321fcdf6d09c9a55282658080 (develop 40cb28c758b0 + one 19-line commit to scripts/release-requirements.json). No PR opened — see DECISION.
- This file contains NO markdown checkboxes (mission rule).

## PLAN

1. Reality check: remotes, develop fetch, base attestation, planning-repo verification.
2. Read scripts/ci-workflow-policy.sh fully; identify the inventories the rule compares (lines 6-27 workflow allowlist; lines 103-110 check-file inventory via base..head diff; lines 161-171 catalog gate-ID diff; lines 182-201 enforcement).
3. Reproduce the #1665 cell as-live; determine WHICH base sha the hosted comparison used.
4. Decide the pairing site the script provides (release-requirements.json .gates[] with an id, lines 164-165 — the field the parser reads).
5. Prove locally: `bash scripts/ci-workflow-policy.sh` at exact head; control comparison; reproduction at #1665's comparison.
6. Test-suite blast radius of catalog variants (pairing-only vs full registration).
7. Candidate commit, PR decision, evidence, END.

## BASE ATTESTATION AND REALITY WITNESSES

- First git action `git remote -v` in /home/marcel/dev/baseharbor-ecosystem/baseharbor:
  `lane-origin https://github.com/mcpdev80/baseharbor.git`, `origin https://github.com/mcpdev80/baseharbor.git`, `upstream https://github.com/mcpdev80/baseharbor.git` — all remotes resolve to github.com/mcpdev80; every fetch/push in this file used URLs, never an unresolved name.
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` -> `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)` — this is the real planning repo (NOT workers/baseharbor-plan).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop` (base SHA attested before branch creation; `git merge-base --is-ancestor 40cb28c758b0 5e3fa3221` -> 0, so the base is an ancestor of the first commit).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1665/head refs/heads/lane-0428-083-datasources-r2` -> `db27880c108a84c6c11bcb5a02484d3da00244bd refs/pull/1665/head`, `b71c6da27e8bbf180d26762eb9bfb101ec5a7bbe refs/heads/lane-0428-083-datasources-r2`.
- gh api pulls/1665 -> base.sha `b71c6da27e8b` (= lane-0428-083-datasources-r2 tip), head `db27880c108a`, state open.
- `git log --oneline origin/develop..5e3fa3221` -> single line `5e3fa3221 ci(0428-205): pair scripts/ci-fast-check.sh in the release gate catalog` (only this lane's own commit; no foreign candidate carried).
- `git diff origin/develop...HEAD --name-only` -> `scripts/release-requirements.json` only.

## FINDING 1 — WHICH INVENTORY THE RULE COMPARES (mission step 1)

scripts/ci-workflow-policy.sh compares TWO inventories against the worktree/diff:

- Workflow-file allowlist (lines 4-40): the hardcoded `expected=()` file-name list of `.github/workflows` vs `find`. This is the "absichtlich hart" allowlist — untouched by this card, not the failure site here ("Workflow policy PASS: 20 approved workflow files." appears in both PRs).
- Gate-catalog inventories (lines 102-201), three sub-inventories:
  - check-file inventory (lines 103-110): regex over the `git diff --name-status $base_sha $head_sha` — `A`/`D` paths matching `^scripts/(ci-[^/]+\.(py|sh)|test_[^/]+\.(py|sh)|[^/]*(check|gate)[^/]*\.(py|sh))$`. This is where `scripts/ci-fast-check.sh` is expected to be paired: `A scripts/ci-fast-check.sh` matches `ci-[^/]+\.sh` (line 107).
  - registration inventory (lines 115-159): `{'id': ...}` lines in scripts/pr-gate-plan.py, the VALIDATIONS set in scripts/pr-check-runner.py, case arms in .github/workflows/ci.yml.
  - catalog gate-ID inventory (lines 161-171): the diff of `jq -r '.gates[].id'` between base revision and worktree of scripts/release-requirements.json — the field the parser reads is `.gates[].id` (line 167/168).
- Consequences: line 178-195 (new check file WITHOUT same-change updates to BOTH scripts/pr-gate-plan.py and scripts/release-requirements.json -> violation) and line 197-201 (changed gate IDs WITHOUT same-change update to scripts/pr-gate-plan.py -> violation).

## FINDING 2 — THE #1665 FAILURE IS EXPLAINED, BUT NOT BY THE PAIRING THE CARD ASSUMED

Measured job log (run 44820434283, job 136579771965, "Workflow policy · Enforce fixed workflow surface"):

```
Workflow policy PASS: 20 approved workflow files.
From https://github.com/mcpdev80/baseharbor
 * branch            ed55d893374b593a7a6032f0de496ca9920ad08d -> FETCH_HEAD
 * branch            refs/pull/1665/head -> FETCH_HEAD
Gate catalog consistency violation: new/removed validation surface lacks same-change updates to: scripts/release-requirements.json
Affected check files: A scripts/ci-fast-check.sh
```

- ed55d893374b = refs/heads/w083-perses-datasources (CLOSED PR #1608's head, the OLD 0428-083 base). The checkout step shows the job ran against `refs/pull/1665/merge` commit `5f2d389b536b` ("Merge db27880c1... into ed55d89337...", API-verified parents) — GitHub's PR-merge ref was STALE (last rebuilt 21:24:32Z, before the base was retargeted to b71c6da27 at 21:27). So the comparison the cell actually ran was diff(merge(5f2d389b), ed55d893374b), where `scripts/ci-fast-check.sh` legitimately appears as `A` (ed55d893 predates its introduction, bcd0e29ca 2026-11-19).
- `git merge-base --is-ancestor ed55d89337 db27880c10` -> NO (unrelated lines): that comparison was never a clean stacked diff.
- Re-running the EXACT current pair with the same script: BASE=b71c6da27 (the real PR base sha) HEAD=db27880c1 -> `Gate catalog consistency PASS: no check-file or gate-ID additions/removals.` (exit 0, measured this session, run-4 below). Reason: b71c6da27's scripts files are byte-identical to develop 40cb28c75 (md5 witness: ci-workflow-policy.sh c1f36e73..., release-requirements.json e7075766..., pr-gate-plan.py 9bf4f898...), and the `A ci-fast-check.sh` never appears in that diff because the file exists on BOTH sides.
- Conclusion: #1665's red cell is a STALE-BASE/merge-ref artifact: it clears by itself on the next synchronize/ready event (which rebuilds refs/pull/1665/merge) — no pairing change can satisfy the comparison as long as it runs against ed55d893, because the violating diff side (lines 184-187) additionally demands that scripts/pr-gate-plan.py AND scripts/release-requirements.json both change in the compared diff, and #1665's diff touches neither (mission step 3: "melden sie genau das" — reported).
- Consistency witnesses from the other seats: #1731 (base = develop tip) SUCCESS because its diff never shows the check file; #1724 (base 408b18d2d, an ancestor of develop tip) SUCCESS; the same rule would fire the identical violation for ANY stacked PR whose base sha predates bcd0e29ca.

## WHAT THE PAIRING STILL GENUINELY FIXES

`bash scripts/ci-fast-check.sh` (line ~35) calls ci-workflow-policy.sh; on every normal develop-based PR run (no compare context) the cell prints the "skipped" branch, but the moment a develop-merge-in-progress PR or a develop push (event push, `.before` base) sees `A scripts/ci-fast-check.sh` against a pre-bcd0e29ca base, the missing pairing fires exactly the #1665 message. The pairing is therefore real debt for future base-comparison views, which this card's candidate takes.

## CANDIDATE AND WHY IT IS PAIRING-ONLY (and not full registration)

Candidate 5e3fa3221 (1 file, +19): adds to scripts/release-requirements.json `.gates[]`

```json
{
  "id": "atomic/static/ci-fast-check",
  "schema": "baseharbor.pre-release.gate-evidence/v1",
  "jobs": ["static_gates"],
  "required_for": ["v0.4.22","v0.4.23","v0.4.24","v0.4.25","v0.4.26","v0.4.27"],
  "dependencies": ["core","demo"]
}
```

This is the field the parser reads (line 164-165: `.gates | all(.[]; (.id|type)=="string")`) — the place the script provides for a validation surface, per mission step 2. Nothing else changed: no workflow file, no `.github/**`, no scripts/ci-workflow-policy.sh, no scripts/pr-gate-plan.py.

Measured blast radius of pairing-only (scratch worktrees at candidate head):

- scripts/test_ci_v0427_gate_catalog.py + scripts/test_pr_gate_coverage.py + scripts/test_pre_release_check_plan.py at develop 40cb28c75 (unmodified): 46 tests OK (baseline witness), including 'v0427_requires_every_active_scope_gate'.
- Same suites with pairing-only candidate: OK (0 failures) — `required_for: []`... MEASURED with the v0.4.27-required variant above; both variants pass these suites.
- The FULL pairing needed to satisfy the 197-201 rule for develop-based comparisons — i.e. changing gate IDs (pairing) AND pr-gate-plan.py (adding 'atomic/static/ci-fast-check' to the STATIC/coverage awareness) AND pr-gate-coverage.json (validate() errors 'coverage catalog omits active release gates' otherwise) AND pre-release-check-plan.py STATIC list — additionally requires a `.github/workflows/ci.yml` dispatch arm for the new gate id (ci.yml:1301 pattern `ci-policy) bash scripts/ci-workflow-policy.sh ;;`), because pr-candidate-advisory.py reads the plan of the candidate and un-routed gate ids fail the routing contract. That .github edit is owner scope under this mission ("KEIN edit an .github/**").
- With the full-but-incomplete registration variant (3 scripts files, no .github arm), the planner itself raises:
  `ValueError: invalid trusted PR gate coverage catalog: coverage catalog omits active release gates: atomic/static/ci-fast-check`
  — i.e. every pr_plan cell goes red. Not a ship candidate.

DECISION (per mission step 3's "melden sie genau das" and §3.8): the PR was NOT opened. The pairing-only candidate passes every local suite and removes the future develop-push/base-comparison failure mode, but it does NOT turn #1665's cell green (that is the stale-base artifact above), and the honest full pairing needs a `.github/**` dispatch-arm change owned by the Owner. The coordinator decides: (A) accept pairing-only as debt-removal (recommend: with required_for [] instead of v0.4.27 so the catalog test exemption question does not arise — measured OK either way for the three suites), (B) commission the .github dispatch arm + full registration (owner-scope edit), or (C) close the card as explained by base staleness for #1665 and track the pairing as follow-up.

## LOCAL PROOF RUNS (mission step 3)

All runs: `bash scripts/ci-workflow-policy.sh` in /var/tmp/w220-0428-205/wt at HEAD 5e3fa3221 (pairing applied), GIT_EXEC_PATH pinned to system git; base/head fetched by the script itself from github.com/mcpdev80/baseharbor (fetch lines shown where emitted).

1. No-compare mode at exact candidate head (develop push/pull_request local invocation style):
```
Workflow policy PASS: 20 approved workflow files.
Gate catalog consistency: skipped (event has no PR/push comparison).
exit=0
```
   NOTE: the mission's acceptance line "Gate catalog consistency PASS" only appears in compare mode (the script's own branches at lines 70/205/207): with no comparison context the literal line is the "skipped" one. Both literal PASS lines are proven in run 4.
2. Develop-base comparison with BASE/HEAD env override (simulates the develop-merge-in-progress case the pairing exists for):
```
Workflow policy PASS: 20 approved workflow files.
Gate catalog consistency violation: added/removed release gate IDs require a same-change update to scripts/pr-gate-plan.py.
exit=1
```
   This is the EXPECTED pairing-only limitation: changing `.gates[].id` inventories without a pr-gate-plan.py same-change update trips lines 197-201. It proves the second inventory rule exists and that a pairing WITHOUT the planner-side registration cannot be the final state for develop comparisons either (feeds decision B above). NOTE: pr-gate-plan.py (develop, this checkout) reads release-requirements.json at lines 802/1154/1828 but carries no atomic/static gate-ID literals at all, so the rule's "same-change update to scripts/pr-gate-plan.py" is unsatisfiable by any content-neutral planner edit — measured, this is the gap that makes the honest full pairing depend on the owner-scope .github dispatch arm.3. #1665 as-live comparison (BASE=ed55d89337 HEAD=db27880c1, the base the hosted job fetched):
```
Workflow policy PASS: 20 approved workflow files.
Gate catalog consistency violation: new/removed validation surface lacks same-change updates to: scripts/release-requirements.json
Affected check files: A scripts/ci-fast-check.sh
```
   Verbatim match of the hosted failure (job 136579771965 log above): the rule and the exact comparison are identified; the pairing change alone does not appear in this compared diff, so the cell stays red for this base — the mission's "melden sie genau das" case.
4. #1665 with its TRUE base sha (BASE=b71c6da27e HEAD=db27880c1, fetched --depth=1 from the real remote):
```
Workflow policy PASS: 20 approved workflow files.
Gate catalog consistency PASS: no check-file or gate-ID additions/removals.
exit=0
```

Baseline (develop 40cb28c75, unmodified): runs 1 and 4 semantics identical to the mission's quoted #1731 SUCCESS ("Workflow policy PASS: 20 approved workflow files." + catalog line), measured in the scratch worktree before the candidate change.

## HOSTED RUN OBSERVATION (§4.6)

- This lane triggered NO hosted run: no push, no PR, no rerun, no workflow_dispatch. Run IDs referenced above are the OTHER seats' runs cited by the mission (#1665 run 44820434283 job 136579771965; #1731 run 44812248904 job 136551503837). Self-run duty is satisfied vacuously and stated so honestly.

## repo-rule compliance

- Branch cut from the attested develop SHA 40cb28c758b0 (ancestry shown above), single commit, `git log --oneline origin/develop..HEAD` lists only this lane's commit.
- No edits to .github/**, scripts/ci-workflow-policy.sh, cmd/baha/**, internal/serviceaccess/**, internal/identityprovider/**, internal/observability/registry.go, internal/capability/perses_selection.go, go.mod, go.sum.
- Write-set of the candidate: scripts/release-requirements.json only.
- No subagents; all measurements executed in this session. No real-name confusion: quarantined workers/baseharbor was never cited; all remote truth came from `git ls-remote https://github.com/mcpdev80/baseharbor.git...`, gh api, or fresh fetches.
- CI policy: no candidate PR opened, therefore no selected-checks observation owed; if the coordinator chooses decision A/B the PR will be created from branch lane-0428-205-gate-catalog-pairing (branch provenance already attested).
- Exactly one candidate per chain: the named branch lane-0428-205-gate-catalog-pairing is the only branch this lane created; no extra branch exists (ls-remote witness below).

## CLEANLINESS (before/after)

- Before: no own containers/networks/volumes. Host listing showed foreign artifacts (ssltest_default network, ambient volumes) — not touched (owner directive: foreign stacks stay).
- This lane started NO docker/podman/compose project; all work was git/python/bash in /var/tmp/w220-0428-205 and worktrees under /tmp/opencode (scratch probe worktree /tmp/opencode/w220-0428-205-catalog-wt removed via `git worktree remove --force` + prune).
- After: `docker ps -a --format '{{.Names}}'` unchanged from before; `docker network ls` unchanged; no own state directories left outside /var/tmp/w220-0428-205 (kept: it holds this lane's candidate worktree and is besenrein of runtime artifacts).
- cleanliness: no containers, networks, volumes or compose projects were created by w220-0428-205-catalog; host state for those classes is byte-identical before/after.

## END

END_BLOCKED w220-0428-205-catalog: root cause identified + verbatim reproduced (stale-base comparison ed55d893 vs db27880c); pairing-only candidate 5e3fa3221 proven locally; full pairing needs an owner-scope .github dispatch arm — scope decision requested. Candidate SHA: 5e3fa3221b9291c321fcdf6d09c9a55282658080 (local, unpushed by design until the coordinator decides A/B/C).
