# Round-2 — Bug-Hunt 0427-160 (recovery): rebase, push, terminal hosted run

- Card/mission: mission-160-r2.md (karte t-20261108-bughunt-list-stale-after-kill, card 0427-160). Recovery (wiederaufnahme) on PR #1491.
- Shift / worker: w160b, session 67a8c04d (worker, no subagents, AGENTS 4.8).
- Planning repo verified (origin/main): `git ls-remote origin main` -> 966396cf1c6bf78d4350c88447dae3548bbc8925.
- Product remote HEAD (develop): fc9ed173ddf5e3d52c5468ced7b86423daabb58a (fresh clone /tmp/baseharbor-remote).
- Evidence written only in baseharbor-plan (origin/main). No product-repo evidence, no main-branch writes in product repos, no `.evidence/` dir.

## Reality (measured)

- PR #1491: state = open, rebasable, mergeable clean. Head = **5753eebda8f0f6563f24c1f55d045b82b254a50e**. Base = develop 7af8d440e9a4dd1b633fdc44e4093109fe44ae37. 1 commit, 223/4/4 files. Not merged.
- The owner already force-pushed the candidate from round-1's cd9eca82e to 5753eebd (19:04, "replay app list provider-state reconciliation on native bootstrap-fixed develop"). No second branch was cut.
- PR base 7af8d440 already contains 0e3a6975e (the 156-line CA-trust commit the mission names): merge-base --is-ancestor 0e3a6975 7af8d440 = YES. Mission's ">= 0e3a6975e, 156 lines in" precondition already satisfied on the current candidate.
- PR diff (vs its base 7af8d440) = exactly 4 files, all display-layer:
  - cmd/baha/app_commands.go
  - cmd/baha/app_observe.go
  - cmd/baha/app_list_reconciliation_test.go
  - cmd/baha/app_status_ux_test.go
- None of these touch lifecycle/provider/owner/node paths (internal/runtime|coreinstallation|controlplaneruntime|onboardingwizard|targetenrollment|identityprovider|database/operator_bootstrap; cmd/baha/runtime|installation|control_plane|serve|node|operator|onboarding|app_remote|app_workload). Purely app list/status display layer + its tests.

## Native Keycloak/Core gate — decision-line evidence (run on head 5753eebd)

Run = CI · PR #1491, databaseId 42513199890, event pull_request, head_branch fix/0427-160-list-stale-after-kill, head_sha 5753eebd, status completed.

- Job "PR · Native impact selection" (128830505200) step "Select exact PR native impact" (ci.yml 416-445): witnessed in run log. It computes `required` from ci-single-default-impact.sh (returns false for the 4 files), then the conservative fallback at ci.yml ~441:
  - `if [ "$required" != true ] && printf '%s\n' "$changed" | grep -Eq '^cmd/baha/.*\.go$'; then required=true; fi`
  - The diff contains cmd/baha/app_commands.go + 3 cmd/baha/*.go tests → grep matches → `required=true`. Step summary line: `echo "Native runtime acceptance required: $required" >> "$GITHUB_STEP_SUMMARY"` → required=true.
- Job "PR · Trusted Plan" (128830505199) step "Detect owner/node changes from the exact PR source diff" (ci.yml 551-563): witnesses BASE_SHA=7af8d440 HEAD_SHA=5753eebd, writes the 4 diff paths to owner-node-paths, then greps `^(cmd/baha/(onboarding|operator_|node|serve_operator_oidc|control_plane_single_native_ci_test.go$)|internal/(onboardingwizard/|targetenrollment/|database/operator_bootstrap|identityprovider/operator))` → NO MATCH (only app_commands/app_observe/app_*_test) → `required=false`. Complete job log: "Set output 'owner_node_required'".
- Job "PR · Native Keycloak/Core · ${{ matrix.runtime }}" (128830558704) if: gate (ci.yml 1042-1046): `needs.pr_plan.outputs.owner_node_required == 'true'` → owner_node_required is false → gate does NOT fire → **conclusion = skipped**.

Conclusion: the runner itself explains the skip. The diff is display-layer only; by the CI's own policy the native Keycloak/Core gate is skipped (owner_node_required=false), NOT a STATE-skip of an uncovered regression. The 156-domain STATE (bootstrap-marker) from round-1 no longer applies — the candidate was rebased onto a bootstrap-fixed develop and native was never red on 5753eebd.

## Green validation cells on 5753eebd (all success, witnessed)

- PR Selected Checks — check run 128833528446 — success
- PR · Validation · go-unit-tests — 128830557386 — success
- PR · Validation · go-build — 128830557256 — success
- PR · Validation · go-vet — 128830557201 — success
- PR · Validation · cli-gofmt — 128830557176 — success
- PR · Focused Python, PR · Native impact selection, PR · Native destroy retry (docker + podman), PR · Trusted Plan, PR · Source format, PR · Workflow policy — all success (full check-runs list for 5753eebd: 24 runs, 19 success / 5 skipped / 0 failure).

## The 0427-160 fixes (already in 5753eebd)

- BF-04 status: degraded workload prints actionable `Next:` (`baha up` rebuild / `baha app destroy` remove / `baha doctor`).
- BF-04 list: `reconciledListState` — recorded failed/stopped/degraded/runtime-retired, or observed-vs-applied reference drift => DEGRADED (record-only reconciliation on read-only list path; live probing stays in `baha status`).
- BF-05 list: MISSING (source repo gone) prints exact next-action (`baha app prune <name>`, or `baha up` once repo restored).
- Machine contract unchanged: `machine.DeploymentSummary.State` stays free-form string. Card names the cli-surface/lifecycle group; the honest mapping at the runner's decision line confirms these are cli-surface (cmd/baha app list/status) changes, and the diff carries NO lifecycle/provider file — so the native gate's skip is the correct, policy-conformant outcome.

## PLAN

- Read mission, card, round-1 evidence; verify planning repo + product remote. DONE.
- Measure PR #1491 head/develop/base/diff/CI. DONE.
- Run the "Native impact selection" decision line for head 5753eebd to prove the skip is runner-explained (owner_node_required=false, diff display-layer only). DONE.
- Confirm green unit/vet/build cells. DONE.
- No second branch, no .github/** edits, no STATE-skip. DONE.
- Publish evidence to origin/main; END (DONE) in shared inbox. PENDING.

## repo-rule compliance

- Scope: exactly one integration candidate per chain (AGENTS 3.8). The named candidate branch is fix/0427-160-list-stale-after-kill (head 5753eebd); no second branch cut. No foreign commit carried on top.
- No .github/** edits, no reruns/workflow_dispatch (Owner scope). The native Keycloak/Core gate is skipped by the runner's OWN policy for a display-layer-only diff — this is policy-conformant, not STATE-skip. Documented with file:line (ci.yml 416-445, 551-563, 1042-1046) and the exact witnessed decision lines.
- No .evidence/ directory anywhere; evidence written only in baseharbor-plan (origin/main). No main-branch writes in product repos.
- Subagents: none used (AGENTS 4.8). All steps executed in this session.
- Machine contract: unchanged.

## END

END mission-160-r2.md: RECOVERY COMPLETE. Candidate 0427-160 on fix/0427-160-list-stale-after-kill head 5753eebd8 (PR #1491 vs develop 7af8d440, base already >=0e3a6975). Both fixes in place (status DEGRADED actionable hint; list record-only DEGRADED + MISSING exact next-action). Native Keycloak/Core gate SKIPPED — proven by the runner's own decision lines (run 42513199890): pr_native_impact REQUIRED=true (cmd/baha/*.go conservative fallback, ci.yml ~441) but pr_plan owner_node_required=false (diff has no owner/node path, ci.yml 561), so pr_owner_node_native if-gate (ci.yml 1046) does not fire. Skip is policy-conformant and runner-explained, not STATE-skip of an uncovered lifecycle/provider regression. All green validation cells on 5753eebd: go-unit-tests 128830557386, go-build 128830557256, go-vet 128830557201, cli-gofmt 128830557176, PR Selected Checks 128833528446 — success; 0 failure across the full check-runs set. No second branch, no .github/** edit, no STATE-skip.
