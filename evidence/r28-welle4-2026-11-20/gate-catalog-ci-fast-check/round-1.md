# 0428-205 · Gate catalog for ci-fast-check — round-1 (w220)

- Task: t-20261120-gate-catalog-ci-fast-check (card 0428-205), repo mcpdev80/baseharbor, base develop.
- Outcome: the #1665 FAILURE is explained precisely — but by the check-file inventory of the gate-catalog rule (scripts/ci-workflow-policy.sh:103-110 compared over the PR's own base..head diff), NOT by a workflow allowlist or a future-view artifact the card assumed. #1665's base at event time was ed55d893 (w083-perses-datasources), whose tree does NOT contain scripts/ci-fast-check.sh; its head does, so the compared diff carries `A scripts/ci-fast-check.sh` and the chain never paired it in scripts/release-requirements.json in the same change. The card's premise is confirmed on live runs; but the pairing, in every catalog form measurable without owner-scope files, CANNOT produce a green cell anywhere: the release-requirements.json edit itself trips the second inventory (gate-ID change -> same-change scripts/pr-gate-plan.py update, lines 161-171 and 197-201), a content-neutral planner edit does not exist on develop (measured), and — decisive — rule 184-187 requires the pairing INSIDE the compared diff, so no develop-side change can ever green #1665's cell; only #1665's own branch can. This lane reports exactly that per mission step 3 and STOPs for a scope decision.
- Candidate branch (local, deliberately NOT pushed): lane-0428-205-gate-catalog-pairing, HEAD fab709a45bd753bce170af6968d2ec9d5a5fb778 = attested develop 40cb28c758b0 + ONE commit touching scripts/release-requirements.json only (V2 form, +12 lines). No PR opened — see DECISION.
- This file contains NO markdown checkboxes (mission rule).

## PLAN

1. Reality check: remotes, develop fetch, base attestation, planning-repo verification.
2. Read scripts/ci-workflow-policy.sh fully; identify the inventories the rule compares against the worktree/diff.
3. Reproduce the #1665 cell as-live; determine WHICH comparison the hosted job evaluated.
4. Decide the pairing site the script provides (the field the parser reads: `.gates[].id`, lines 164-168).
5. Prove locally: `bash scripts/ci-workflow-policy.sh` at exact candidate head; the #1665 comparison replayed both ways.
6. Test-suite blast radius of the three catalog forms (V1/V2/V3).
7. Candidate commit, PR decision, evidence, END.

## BASE ATTESTATION AND REALITY WITNESSES

- First git action `git remote -v` in /home/marcel/dev/baseharbor-ecosystem/baseharbor:
  `lane-origin https://github.com/mcpdev80/baseharbor.git`, `origin https://github.com/mcpdev80/baseharbor.git`, `upstream https://github.com/mcpdev80/baseharbor.git` — all three resolve to github.com/mcpdev80; every fetch/ls-remote below used the URL directly.
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` -> `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)` — this is the real planning repo (NOT workers/baseharbor-plan).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop` (attested BEFORE branch creation; re-checked at END, still the tip). `git merge-base --is-ancestor 40cb28c758b0 HEAD` -> 0.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1665/head refs/heads/lane-0428-083-datasources-r2` -> `db27880c108a84c6c11bcb5a02484d3da00244bd refs/pull/1665/head`, `b71c6da27e8bbf180d26762eb9bfb101ec5a7bbe refs/heads/lane-0428-083-datasources-r2`.
- gh api pulls/1665 -> base.sha `b71c6da27e8b` (= lane-0428-083-datasources-r2 tip), head `db27880c108a`, state open, updated 2026-11-20T21:29:37Z; timeline: head_ref_force_pushed 21:24:30Z, ready_for_review 21:27:06Z.
- `git log --oneline origin/develop..HEAD` -> exactly one line `fab709a45 ci(0428-205): pair scripts/ci-fast-check.sh in the release gate catalog (V2)` (only this lane's commit).
- `git diff origin/develop...HEAD --name-only` -> `scripts/release-requirements.json` only.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-205-gate-catalog-pairing` -> empty (branch exists locally only; before/after witnesses for the no-extra-branch rule: no push happened, and the only branch this lane created is the named one).

## FINDING 1 — WHICH INVENTORY THE RULE COMPARES (mission step 2)

scripts/ci-workflow-policy.sh compares TWO inventories against the worktree/diff:

- Workflow-file allowlist (lines 4-40): hardcoded `expected=()` names vs `find .github/workflows`. The "deliberately hard" allowlist; untouched here, not this failure's site — every observed run prints "Workflow policy PASS: 20 approved workflow files." before the catalog part.
- Gate-catalog inventories (lines 102-201), three sub-inventories:
  - check-file inventory (lines 102-110): over `git diff --name-status $base_sha $head_sha`, regex on line 107 `^scripts/(ci-[^/]+\.(py|sh)|test_[^/]+\.(py|sh)|[^/]*(check|gate)[^/]*\.(py|sh))$`. THIS is the line where the new check file is expected: `A scripts/ci-fast-check.sh` matches `ci-[^/]+\.sh`. base_sha/head_sha are the PR's OWN base/head (from the event JSON, lines 56-59) — not develop.
  - registration inventory (lines 115-159): `{'id': ...}` lines in scripts/pr-gate-plan.py, the VALIDATIONS set in scripts/pr-check-runner.py, case arms in .github/workflows/ci.yml.
  - catalog gate-ID inventory (lines 161-171): diff of `jq -r '.gates[].id'` between `${base_sha}:scripts/release-requirements.json` and the worktree file — the field the parser reads is `.gates[].id` (lines 164-168).
- Consequences: lines 178-195 (a NEW check file in the compared diff requires same-change updates to BOTH scripts/pr-gate-plan.py AND scripts/release-requirements.json); lines 197-201 (CHANGED catalog gate IDs require a same-change update to scripts/pr-gate-plan.py).

## FINDING 2 — THE #1665 FAILURE: ITS OWN DIFF ADDS THE UNPAIRED CHECK FILE

Measured hosted job log (run 44820434283, job 136579771965, step "Enforce fixed workflow surface"):

```
Workflow policy PASS: 20 approved workflow files.
From https://github.com/mcpdev80/baseharbor
 * branch            ed55d893374b593a7a6032f0de496ca9920ad08d -> FETCH_HEAD
 * branch            refs/pull/1665/head -> FETCH_HEAD
Gate catalog consistency violation: new/removed validation surface lacks same-change updates to: scripts/release-requirements.json
Affected check files: A scripts/ci-fast-check.sh
```

- The compared pair was base=ed55d893 HEAD=refs/pull/1665/head=db27880c1. The `ed55d893` fetch is line 80 fetching `event.pull_request.base.sha` — the PR's base was still w083-perses-datasources (ed55d893) when the run started 21:27:12Z (the base was retargeted to lane-0428-083-datasources-r2 later; the CURRENT base sha is b71c6da27 — both facts from gh api + ls-remote above). So the job compared the PR's real base..head pair, and #1665's own diff carries `A scripts/ci-fast-check.sh`:
  - ed55d893 does NOT contain scripts/ci-fast-check.sh at all (`git rev-parse ed55d893:scripts/ci-fast-check.sh` -> fatal: path exists on disk but not in ed55d893; measured 2026-11-21). The file entered the 083/082 lane line AFTER ed55d893 via develop's bcd0e29ca (blob 3cf87b29d7c3), and db27880c1 inherits that blob — the same blob develop has. `git diff ed55d893 db27880c1` therefore shows `A scripts/ci-fast-check.sh` while `git diff develop db27880c1` shows nothing for it (identical blobs).
  - The 083/082 chain never paired the file in scripts/release-requirements.json in any of its commits (release-requirements.json on ed55d893 == develop's, md5 e70757660b3d, no ci-fast entry).
- Replay at THIS lane's head (run R1c): identical command BASE=ed55d893 HEAD=db27880c1 produces the verbatim violation. The failure is fully explained by the missing pairing (rule 178-195) in #1665's own diff — the card's premise. R1f (pairing applied to the compared base view) shows the check-file rule STILL fires: rule 184-187 requires the pairing inside the compared DIFF, so only #1665's own branch can carry it.
- Why other cells stay green: #1731/#1650 diffs touch no scripts/ path (measured `gh pr diff --name-only | grep ^scripts/` = empty), #1684's diff likewise; their comparisons show no `A` check file and no gate-ID change. The mission's "kein .github-anteil mehr im diff" holds for `.github/**` but not for `scripts/` — the rule reads only `git diff` paths, and #1665's diff carries the check-file addition.

## FINDING 3 — WHY THE PAIRING CANNOT GO GREEN WITHOUT THE PLANNER HALVES (measured, all three forms)

Any edit that adds a gate ID to `.gates[].id` changes the catalog inventory, which trips rule 197-201 — and that rule is evaluated against the PR's OWN base..head too: it demands a same-change scripts/pr-gate-plan.py update whenever gate IDs change. Measured at develop 40cb28c75 with the candidate's diff (form = the pairing):

- V1 full-shape (id + jobs + required_for all six releases): own-develop comparison VIOLATION (197-201); scripts/test_ci_v0427_gate_catalog.py FAILS 3 errors (gate not registered in pr-gate-plan.py literals).
- V2 id + jobs:["static_gates"] + dependencies + required_for []: own-develop comparison VIOLATION (197-201); the three suites test_ci_v0427_gate_catalog + test_pr_gate_coverage + test_pre_release_check_plan: 46 tests OK.
- V3 id-only + required_for []: own-develop comparison VIOLATION (197-201 — the rule is inventory-based, independent of form); suites: 1 subtest failure in test_ci_v0427_gate_catalog (assertIn('v0.4.27', required_for) at scripts/test_ci_v0427_gate_catalog.py:54 for the exempted-from-releases gate).
- A content-neutral scripts/pr-gate-plan.py edit does not exist: pr-gate-plan.py carries NO 'atomic/static' literals at all (measured; its catalog reads are lines 802/1154/1828), so the planner half that satisfies 197-201 must be a REAL registration — and the only durable catalog regression (test_v0427_requires_every_active_scope_gate) forces required_for to include v0.4.27 for every catalogued gate, which then forces the executor/routing chain: pre-release-check-plan.py select() needs the id in its STATIC list (its 'selected check has no executor' raise, V1-measured), which then needs a static_gates execution entry whose workflow case arm lives at .github/workflows/ci.yml:1301 (pattern `ci-policy) bash scripts/ci-workflow-policy.sh ;;`) = owner scope under this mission ("KEIN edit an .github/**").
- Consequence for #1665 specifically: the complete same-change fix belongs to #1665's chain (it must carry BOTH the catalog gate and the planner/coverage/STATIC-list registration in its own diff, plus the .github dispatch arm). A develop-side pairing cannot reach into #1665's base..head diff (base ed55d893/b71c6da27 predates it), so this card cannot make #1665 green by itself, and a PR containing this candidate would show its own cell RED (measured). Mission step 3's "melden sie genau das" applies: the pairing IS what makes #1665's cell explainable and fixable, but the fix is not a one-line develop pairing — it is the 083/082 chain's unmerged gate-registration debt plus one owner-scope ci.yml arm.

## CANDIDATE

Final candidate fab709a45 (form V2, 1 file, +12): adds to scripts/release-requirements.json `.gates[]`, after atomic/static/shell-ux:

```json
{
  "id": "atomic/static/ci-fast-check",
  "schema": "baseharbor.pre-release.gate-evidence/v1",
  "required_for": [],
  "jobs": ["static_gates"],
  "dependencies": ["core", "demo"]
}
```

Nothing else changed: no workflow file, no `.github/**`, no scripts/ci-workflow-policy.sh, no scripts/pr-gate-plan.py, no scripts/pr-check-runner.py, no scripts/pre-release-check-plan.py. V2 keeps all 46 catalog-regression tests green at develop. The branch is NOT pushed: its own PR's Workflow policy cell would be red (measured, Finding 3) — opening it would violate the "red base färbt / kein roter Kandidat" discipline and produce a false STATE on the very cell this card is about.

DECISION (per mission step 3 and §3.8): the coordinator decides: (A) commission ONE follow-up PR on the 083/082 chain (or a develop-side combined PR) that pairs AND registers: release-requirements.json gate + pr-gate-plan.py + pre-release-check-plan.py STATIC + pr-check-runner.py + the ci.yml:1301 case arm (that arm = owner scope) — then #1665, #1732-style chains and this card all go green in one reviewed change; (B) close 0428-205 as explained (the card was cut too narrow for a develop-only pairing, which Finding 3 measures) and pour the registration into a properly scoped card; (C) merge this V2 candidate together with the planner+runner+pre-release-check-plan registration and the owner ci.yml arm as the same change (this card + owner-scope lines fused — allowed only with Owner sign-off).

## LOCAL PROOF RUNS (mission step 3)

All runs: `bash scripts/ci-workflow-policy.sh` in /var/tmp/w220-0428-205/wt at HEAD fab709a45 (V2 pairing committed), GIT_EXEC_PATH pinned; base/head fetched by the script itself from https://github.com/mcpdev80/baseharbor (fetch lines shown where emitted).

R1a no-compare at exact candidate head (local invocation, event-less):
```
Workflow policy PASS: 20 approved workflow files.
Gate catalog consistency: skipped (event has no PR/push comparison).
exit=0
```
R1b own develop-base comparison (BASE=40cb28c758b0 HEAD=fab709a45):
```
Workflow policy PASS: 20 approved workflow files.
Gate catalog consistency violation: added/removed release gate IDs require a same-change update to scripts/pr-gate-plan.py.
exit=1
```
R1c #1665 as-live comparison (BASE=ed55d89337 HEAD=db27880c1) — verbatim hosted failure:
```
Workflow policy PASS: 20 approved workflow files.
Gate catalog consistency violation: new/removed validation surface lacks same-change updates to: scripts/release-requirements.json
Affected check files: A scripts/ci-fast-check.sh
exit=1
```
R1d same with the candidate pairing applied to the compared base view — pairing invisible to that diff (base predates it), still red on the gate-ID half only:
```
Workflow policy PASS: 20 approved workflow files.
Gate catalog consistency violation: added/removed release gate IDs require a same-change update to scripts/pr-gate-plan.py.
exit=1
```
R1e replay of R1d semantics at worktree level (pairing in worktree, BASE=b71c6da27 HEAD=db27880c1): identical rule-197 violation, exit=1. (Note: the #1665 base at CURRENT b71c6da27 hides the check-file `A` — b71c6da27's copy is blob-identical to develop's — so only the gate-ID rule remains; with the true base the check-file rule re-fires: R1c.)
R1f decisive run: pairing applied to the compared BASE view (#1665 as-live, BASE=ed55d893 HEAD=db27880c1): the check-file rule STILL fires ("...lacks same-change updates to: scripts/release-requirements.json", exit=1) — rule 184-187 demands scripts/release-requirements.json change IN THE COMPARED DIFF (base..head), not merely exist in the worktree. Conclusion: NO develop-side pairing, in any form, can ever turn #1665's cell green. The fix must be carried in #1665's own branch (its diff adds the unpaired A line): pairing + registration in that chain's next candidate.
Variant own-develop comparisons (BASE=40cb28c758b0 HEAD=worktree-as-head, 2026-11-21): V1 exit=1 (rule-197) + 3 unittest errors; V2 exit=1 (rule-197) + 46 tests OK; V3 exit=1 (rule-197) + 1 unittest failure. Baseline develop 40cb28c75 (no edits): 46 tests OK, rule fires only for diffs carrying check-file `A`/gate-ID changes.
Mission-acceptance note: the two literal lines "Workflow policy PASS" AND "Gate catalog consistency PASS" appear together only in comparisons WITHOUT catalog changes (e.g. #1731, R1d-family cells with unchanged inventories; measured in the unmodified scratch worktree at develop and #1665-true-base views). No catalog-pairing-only candidate can print both — Finding 3 is the reason, reported per mission step 3.

## HOSTED RUN OBSERVATION (§4.6)

- This lane triggered NO hosted run: no push, no PR, no rerun, no workflow_dispatch (mission 3.8 respected). The run IDs cited are the OTHER seats' runs from the mission brief (#1665 run 44820434283 job 136579771965; #1731 run 44812248904). Self-run duty is satisfied vacuously and stated so.

## repo-rule compliance

- Branch lane-0428-205-gate-catalog-pairing cut from the attested develop SHA 40cb28c758b02960356434b630086a341ebe1738 (ancestry shown; `git log --oneline origin/develop..HEAD` lists only this lane's commit). Exactly one candidate per chain: the named branch, no second branch; not pushed pending the coordinator's scope decision (red-on-arrival would violate 3.8/GATE RULE completeness).
- Write-set of the candidate: scripts/release-requirements.json only. No edits to .github/**, scripts/ci-workflow-policy.sh, scripts/pr-gate-plan.py, scripts/pr-check-runner.py, cmd/baha/**, internal/**, go.mod, go.sum. V1/V3 forms existed only as measurement variants and were reverted (git checkout --).
- No subagents; every step executed in this session. No 'codeman agent post' to third sessions.
- Remote truth only via git ls-remote https://github.com/mcpdev80/baseharbor.git..., gh api, or fresh fetches; the quarantined workers/baseharbor was never cited (the shared baseharbor checkout was used only as an object store with URL-resolved refs).
- Scratch discipline: probe worktree /tmp/opencode/w220-0428-205-catalog-wt removed (`git worktree remove --force` + prune; ls-remote-independent witness: `git worktree list` shows only /var/tmp/w220-0428-205/wt now for this lane); candidate worktree under /var/tmp/w220-0428-205/wt (persistent lane zone); diff/plan probes under /tmp/opencode.

## CLEANLINESS (before/after, 3.3.5)

- Before: host listing (docker ps -a / docker network ls / docker volume ls) showed ambient artifacts only (network ssltest_default; anonymous volumes from other tooling) — foreign state, untouched per owner directive.
- This lane started NO container, NO compose project, NO network or volume; nothing ran on baha-docker/baha-podman (no runtime tests in this mission); the only "state" was git worktrees under /var/tmp and /tmp/opencode.
- After: identical listings; zero runtime resources created or left by this lane.
- cleanliness: zero containers/networks/volumes/compose projects created by w220-0428-205-catalog; before/after lists match; no orphans left.

## END

END_BLOCKED w220-0428-205-catalog: #1665 red explained verbatim (its own diff adds scripts/ci-fast-check.sh with no same-change release-requirements.json pairing, rule ci-workflow-policy.sh:107+178-195, replayed at R1c); the develop-side pairing is NOT sufficient anywhere it can be placed (rule 197-201 + test_ci_v0427_gate_catalog:54 force a planner/runner/STATIC-list/ci.yml-arm registration = 083-chain debt + owner scope ci.yml:1301). Candidate (V2, unpushed, local): fab709a45bd753bce170af6968d2ec9d5a5fb778 on branch lane-0428-205-gate-catalog-pairing. Scope decision A/B/C requested.
