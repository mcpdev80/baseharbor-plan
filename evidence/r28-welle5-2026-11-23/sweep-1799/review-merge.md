# PR #1799 post-merge review

Role: REVIEW, then MERGE only if all contract criteria pass.

## PLAN

- 359. Read the #1799 review contract and create the numbered plan in the live board and Planning evidence.
- 360. Resolve GitHub remotes and verify the live PR head/base, exact terminal run, develop and merge state.
- 361. Verify the exact catalog-only diff, additive record count, normalized IDs, surfaces, and runtime_specific placement.
- 362. Check no records moved or deleted, no global re-sort, and no requirements, release, or workflow changes.
- 363. Spot-check two record routes against pr-gate-plan for guided versus data-caps semantics.
- 364. If every criterion passes, merge normally; otherwise write an exact repair recipe and stop.
- 365. Verify merge/develop witnesses, record cleanliness, validate and publish evidence, update board, and post END.

## Repository and candidate witnesses

- Planning repository verified before the first evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`; push URL is the same GitHub repository.
- Product remote resolved from the active checkout: `https://github.com/mcpdev80/baseharbor.git`; all remote truth below is measured through that GitHub URL or GitHub API. The quarantined `workers/baseharbor` checkout was not used.
- PR #1799 is OPEN, not draft, base branch `develop`; API base SHA `c3e49f3cc1959db68d57e52db0408bd48a043292`; head `7021f0a6d1ad48a52c9dcdab2e4e37a024beec10`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1799/head`:
  `c3e49f3cc1959db68d57e52db0408bd48a043292 refs/heads/develop`
  `7021f0a6d1ad48a52c9dcdab2e4e37a024beec10 refs/pull/1799/head`
- Exact PR files metadata: only `scripts/pr-gate-coverage.json`, with 223 additions and 42 deletions. The declared expected ingress was approximately 11 additions and zero moved/deleted records.

## Catalog census and semantic spot check

- Compared `components` JSON at exact base `c3e49f3cc1959db68d57e52db0408bd48a043292` with exact head `7021f0a6d1ad48a52c9dcdab2e4e37a024beec10`.
- Eleven component records are added; two base records are absent at head: `source.cmd_baha_app_new_wizard_test_go` (`cmd/baha/app_new_wizard_test.go`) and `source.cmd_baha_application_provider_preferences_go` (`cmd/baha/application_provider_preferences.go`). There are no changed common component records. The order of all surviving preexisting component records is preserved, so this is not a global re-sort.
- Both missing records are present at the exact base with the requested guided pair: `source.gate.atomic.docker.guided` and `source.gate.atomic.podman.guided`. In the exact head's `scripts/pr-gate-plan.py`, lines 202–205 route `cmd/baha/app_new_wizard_test.go` to `wizard-app-new-tests` and Docker/Podman lifecycle gates. Removing its guided catalog record is inconsistent with that routing and with the previous accepted catalog state.
- Data-capabilities spot check: `scripts/pr-gate-plan.py` defines `DATA_CAPABILITY_GATES` as atomic Docker and Podman data-capabilities at lines 147–150. The added `source.cmd_baha_app_exec_go` record points at exactly that pair, which matches this non-guided route.
- Of the eleven additions, three test records set `runtime_specific: true`: `source.cmd_baha_app_interact_test_go`, `source.internal_cli_cli_test_go`, and `source.internal_operatorauth_interaction_operations_test_go`. Contract permits exactly two such test rows; current head exceeds that count by one. The contract does not identify which two tests are intended, so the implementer must retain the flag on exactly the two justified by their test behavior and remove it from the third.
- The other top-level catalog fields (`schema`, `release`, `surfaces`, `packages`, `gates`, `native_checks`) compare equal between base and head. The patch also reflows preexisting JSON arrays and gate-list whitespace; that formatting churn is unnecessary for an additive ingress and should be removed in the repair.

## Hosted CI

- Exact-head run `45149446083`, event `pull_request`, head `7021f0a6d1ad48a52c9dcdab2e4e37a024beec10`, terminal conclusion `success`.
- `PR · Trusted Plan` job `137606826203` succeeded and logged `BASE_SHA: c3e49f3cc1959db68d57e52db0408bd48a043292`.
- `PR Selected Checks` job `137607816098` completed `success` from GitHub Actions integration app `15368`. Run terminal state is completed; no active jobs or failing checks remain.
- Catalog-only unrelated runtime/release jobs were skipped and are not treated as passes. The selected-check aggregate succeeded on the exact candidate.

## Review findings and repair recipe

- REQUEST CHANGES: the head deletes two preexisting guided records. Restore both records exactly as they appear at base `c3e49f3cc1959db68d57e52db0408bd48a043292`, preserving their guided Docker/Podman surfaces and the order of all existing component records.
- Keep the eleven intended additions, with IDs and paths unchanged; verify no preexisting records are deleted, moved, or altered. Avoid reformatting unrelated arrays and gate lists so the resulting semantic and textual diff is limited to the requested additive records.
- Set `runtime_specific: true` on exactly two of the new test records, based on their actual runtime-specific behavior. The current head sets it on three; remove it from the unjustified third test row.
- Keep the new `app_exec.go` row on data-capabilities. Preserve the two prior wizard/provider-preference rows on guided surfaces as established by the base and routing map.
- Do not merge this head. A correction changes the candidate and needs a new exact-head CI run before any later merge review.

## Cleanliness

- `docker ps -a` before review, PID 1690794: only the header was returned; no containers listed.
- `docker ps -a` after review, PID 1696223: only the header was returned; no containers listed.
- No local tests were run and no containers or compose projects were started.
- Other preexisting Planning worktree changes were observed in `sweep-1614` and `sweep-1623`; they were not read, staged, or modified.

VERDICT: REQUEST CHANGES — do not merge PR #1799. Restore the two deleted guided records, correct the runtime_specific count to exactly two test rows, and submit a new exact-head CI run.

END DONE codex-rev-1747: #1799 REQUEST CHANGES; PR head 7021f0a6d1ad48a52c9dcdab2e4e37a024beec10 requires catalog repair; no merge SHA.
