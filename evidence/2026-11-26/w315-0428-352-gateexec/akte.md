# w315-0428-352-gateexec — akte (read-only gate-execution investigation, findings only)

- lane: w315-0428-352-gateexec (registered session name; mission w315-0428-352-gateexec.txt)
- card: 0428-352 (tasks/t-20261126-trusted-catalog-baseline-identity-tests.md)
- date (host clock): 2026-11-26/27
- mission: settle with evidence whether ONE catalog row in scripts/pr-gate-coverage.json makes the 14 Docker/Podman-Light gates EXECUTE (not merely select) for a pull_request candidate that modifies .github/workflows/pre-release-runtime-suite.yml. Read-only; no product change; no new cards; no card edits.
- plan repo remote witness (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`):
  `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)` — verified BEFORE the first evidence commit; evidence published ONLY from the isolated worktree workers/w315-0428-352-gateexec-plan via a scoped plan PR, never a direct push to plan main.

## Visible ANSATZ block (owner directive, content-attested)

- exact per-card frontmatter owner, fetched from plan origin/main at runtime (commit 59ab8ee255, file tasks/t-20261126-trusted-catalog-baseline-identity-tests.md): `owner: ""` (card 0428-352 unassigned in frontmatter; kanban_status: planned)
- git user.name: w315-0428-352-gateexec
- git user.email: w315-0428-352-gateexec@baseharbor.local
- literal invocation: `git -c user.name=w315-0428-352-gateexec -c user.email=w315-0428-352-gateexec@baseharbor.local commit` (and the same -c form for any merge commit)
- pre-push identity gate line: `git log --format='%h an=%an cn=%cn' -1` (printed below, before the push)
- remote guard: real GitHub URLs used for all measurement (https://github.com/mcpdev80/baseharbor.git via `git ls-remote`/`git fetch <url>` and api.github.com via gh); the quarantined workers/baseharbor checkout was NOT used as a remote-truth witness.

## ## PLAN (numbered, mirrors the board file todos/w315-0428-251-0428-352-gateexec.json)

1. Base attestation: frontmatter owner verbatim, remotes, develop/main SHAs, commit identity — done (ANSATZ block)
2. Isolated plan worktree workers/w315-0428-352-gateexec-plan from origin/main; akte head with ANSATZ block — done
3. Read pr-gate-plan.py catch-all (~1702), reviewed-head bindings (377-389, 938-945) and pr-gate-coverage.json on #1859 head 0716d20be — done (STEP A)
4. Read ci.yml:183/225 and identify the 14 gates of card 0428-352 — done (STEP B)
5. #1859 exact-head run census per_page=100 (jobs executed vs skipped, gate family) — done (STEP C1)
6. #1812 latest run census per_page=100 (head b962e6d2c) — done (STEP C2)
7. runtime-validation/ha ref existence check — done (STEP D)
8. One-paragraph conclusion: catalog row alone EXECUTE-capable vs runtime-validation/ha push path — done (STEP E)
9. Publish akte via ONE scoped plan PR, own identity, own validate run watched to terminal, head+run as PR comment — done (plan-pub section)
10. Verify evidence on origin/main (second-to-last action) + END line — final actions

## STEP A — planner/catalog semantics on #1859's head

- #1859 = mcpdev80/baseharbor PR, branch w309-0428-352-14gatecatalog, head 0716d20becc1f0acc1156e3120f6ca3351e12f4b, base develop b7855f78a, state OPEN, mergeable CLEAN, NOT merged (refs/heads/develop still b7855f78a at both investigation start and END; `git ls-remote` witnesses in STEP F).
- `git diff b7855f78a 0716d20be --name-only` → exactly scripts/pr-gate-coverage.json + scripts/test_pr_gate_coverage.py. The full catalog delta is in pr-gate-coverage-1859-vs-base.diff beside this akte:
  - 10 new DECLARED surfaces (source.gate.atomic.{docker,podman}.{connectivity,failure,full.destroy,policy,reconciliation});
  - ONE new component row source.workflow.pre.release.runtime.suite → path .github/workflows/pre-release-runtime-suite.yml, 14 surfaces, runtime_specific: true;
  - 10 new `source.gate.*` cover tokens added to the gate.covers arrays of the same 10 gates (verified present in the 0716d20be blob; w309's earlier akte line 85 pre-announced exactly this: "a 14-gate variant needs one extra cover token per such gate in coverage.json (still catalog-only)").
- catch-all (pr-gate-plan.py:1702 on the head): `elif path.startswith('.github/workflows/'): area='ci-workflow'; require(CI_CHECKS); require(WORKFLOW_SYNTAX_CHECKS)` — adds nothing to selected; it never marks the path unowned.
- reviewed-head bindings: RUNTIME_STEP_CAP_REVIEWED_HEAD line 377 = 75efeef89…, files 378-380 = exactly {pre-release-runtime-suite.yml: modified}; the binding-loop tuple at ~938-940 uses CI_CHECKS + WORKFLOW_SYNTAX_CHECKS and RETURNS `'selected_gates': []` (the loop return constructs the dict with an empty selected set). A binding alone therefore arms validations but dispatches ZERO gates — matching w309 finding (b).
- final authority: plan() (pr-gate-plan.py:1897-1985) OVERWRITES result['selected_gates'] with resolve_covered_gates() output ("The catalog is the sole authority for runtime gate selection", line 1970). The catch-all does not need to change.
- resolve_covered_gates (validate-pr-gate-coverage.py on head): component row surfaces → gates whose `covers` intersect them, `selection_scope == focused`. The row's surfaces AND the gates' cover-token additions must BOTH exist for the intersection to fire; with only the component row (10 gate covers still token-less) resolution returns 6, not 14.
- pr-selected-runtime-matrix.py (develop blob, unchanged by #1859) turns a non-empty selected set into include rows + required=true; the PR · Selected Runtime job (ci.yml ~1480) dispatches the reusable pre-release-runtime-suite.yml per row when pr_plan.outputs.runtime_required == 'true'.

## STEP B — the 14 gates and the other family

- The 14 = the Light gates: `jobs` containing runtime_light_gates_{docker,podman} in release-requirements.json AND `v0.4.27` in required_for → measured n=14:
  atomic/{docker,podman} × {guided, lifecycle, policy, connectivity, reconciliation, failure, full-destroy}. This is exactly the 14 surfaces of #1859's component row.
- Family distinction (the mission's question): the 14 Light gates are dispatched by the pull_request job PR · Selected Runtime (ci.yml:1480, `uses: ./.github/workflows/pre-release-runtime-suite.yml`) under `if: github.event_name == 'pull_request' && … runtime_required == 'true'`. "Targeted HA · docker/podman" (ci.yml:183/225) belong to the push-triggered HA acceptance family (scripts/v0.4.21-ha-acceptance.sh, refs runtime-validation/ha/<group>/<docker|both>); they are a DIFFERENT family and are not among the 14. Card 0428-352's gates are therefore the PR-path Selected-Runtime family, NOT the runtime-validation/ha path.

## STEP C — per-run job censures (per_page=100, attempt 1 via REST)

### C1 — #1859 exact head 0716d20be: run 45783262677 (event pull_request, completed success, 32 jobs)

- executed 11: PR · Trusted Plan, PR · Native gate plan, Workflow policy, PR · Source format, PR · Focused Python, PR · Candidate-added checks (advisory), PR · Validation · {pr-planner-tests, ci-policy, ci-executor-tests, receipt-execution-tests}, PR Selected Checks.
- skipped 21: includes PR · Selected Runtime (job id 139783736333, conclusion SKIPPED, started==completed 08:27:20Z), Targeted HA · docker (139783643565, skipped), Targeted HA · podman (139783643358, skipped), plus all release/pre-release families.
- 0 failed. Census 11/21/0 CONFIRMS w309's claimed figures for this run — but the headline claim is false for THIS run: the run's own trusted-pr-plan artifact (downloaded) shows
  `coverage_status=resolved, selected_gates=[], head_sha=0716d20be…, target_base_sha=b7855f78a…, reasons: ['scripts/pr-gate-coverage.json: ci-executor', 'scripts/test_pr_gate_coverage.py: ci-planner', 'No declared runtime gate owner for: scripts/pr-gate-coverage.json, scripts/test_pr_gate_coverage.py']`.
  No "Declared coverage selected gates:" reason — the catalog step returned covered=[] because the diff shape of #1859 is the two SCRIPTS, not a workflow file, and the TRUSTED BASE catalog (b7855f78a) has no row for the suite.
- run 45782087038 (cited by w309 as an own-run): its head_sha is f6fc8a71f (the PREVIOUS push), NOT 0716d20be. It is not exact-head evidence for 0716d20be.
- NOTE on how a pull_request run can end SUCCESS while Selected Runtime is SKIPPED: the PR · Selected Runtime `if` is FALSE (runtime_required=false → the job never dispatches, conclusion 'skipped'); 'PR Selected Checks' (ci.yml, the final verifier) treats skipped-but-not-required runtimes as consistent and succeeded, exactly as the validation_contract line prescribes. The 14-gate matrix children (pre-release-runtime-suite reusable-workflow callers) are therefore 0 executed — the claim that this PR's own runs EXECUTED them is empirically false, and the mission's "census 11 executed" is consistent with zero gate executions (the 11 executed jobs are plan/validations only).

### C2 — #1812 latest head b962e6d2c: run 45771862723 (pull_request, success, 33 jobs)

- executed 12: PR · Trusted Plan, PR · Native gate plan, Workflow policy, PR · Source format, PR · Focused Python, PR · Candidate-added checks (advisory), PR · Validation · {ci-actionlint, pr-planner-tests, ci-policy, ci-executor-tests, receipt-execution-tests}, PR Selected Checks.
- skipped 21 (per_page=100 attempt-1 census): includes PR · Selected Runtime (SKIPPED, job 139746230693), Targeted HA · docker/podman (both skipped), release/main families.
- trusted-pr-plan artifact: selected_gates=[], reasons ['…: ci-workflow', 'No declared runtime gate owner for: .github/workflows/pre-release-runtime-suite.yml'] (base catalog b7855f78a has no row; no gate cover tokens).

### Family tally for both runs

Every one of the three pull_request runs on #1859 and the latest #1812 run shows the SAME execution pattern: 0 Light gates executed; PR · Selected Runtime skipped (runtime_required=false); Targeted HA · docker/podman skipped (event is pull_request, so the push-only if at ci.yml:183/225 is false).

## STEP D — runtime-validation/ha refs

`git ls-remote https://github.com/mcpdev80/baseharbor.git` (1765 refs total) → ZERO refs under refs/heads/runtime-validation/* (grep count 0, both at investigation start and at END). The mission's premise is correct: no such ref exists in the repository; that family is an owner-action push path, unavailable to a pull_request candidate.

## STEP E — conclusion (the owner's decision evidence)

The 14 gates of card 0428-352 are the Light gates dispatched by the pull_request-path job PR · Selected Runtime (ci.yml:1480 → pre-release-runtime-suite.yml), NOT the push-only Targeted HA family (ci.yml:183/225, which no pull_request candidate can ever execute and whose runtime-validation/ha refs do not exist). One catalog change in the TRUSTED BASE — #1859's component row PLUS the 10 gate cover tokens (the row's surfaces are inert without the tokens: measured resolve = 6 of 14 with tokens missing) — is by itself sufficient to make a pull_request candidate whose write-set is .github/workflows/pre-release-runtime-suite.yml EXECUTE all 14 Light gates, because plan() replaces selected_gates with the catalog resolution ("The catalog is the sole authority", pr-gate-plan.py:1970), the catch-all at :1702 neither blocks nor owns the path, pr-selected-runtime-matrix.py maps the 14 atomic/{docker,podman} gates to required=true, and the measured replay (this lane, develop + #1859 files under the real CI checkout semantics) gives coverage_status=resolved, 14 selected, include n=14, runtime_required=true. The runtime-validation/ha push path is UNNECESSARY for these 14 gates — it exercises a different family (HA acceptance scripts) and cannot be triggered from any pull_request event. What #1859's own SUCCESS runs did NOT and CANNOT show is the execution itself: on that PR the planned diff is the catalog scripts, selected_gates=[] is CORRECT there, and PR · Selected Runtime stayed skipped; execution will first be observable on the next workflow-modifying pull_request candidate whose BASE contains the merged row (e.g. #1812 after absorbing develop), where the trusted-plan artifact must list 'Declared coverage selected gates: atomic/docker/… × 14' and the job must dispatch 14 matrix children.

## repo-rule compliance

- Read-only investigation: no file in baseharbor or baseharbor-demo was created, modified, or pushed; no PR opened/updated; no workflow_dispatch; no rerun; no test executed locally; no subagent used; all measurement ran in this session via git show + pure-python importlib on fetched objects (no containers, no network side effects).
- Planner invocations used fixture diffs with fake/real SHAs exactly as scripts/test_pr_gate_coverage.py does; pure function evaluation, no CI triggering.
- .github/** untouched (read only); no new cards; no card edits (raw findings here go to a Codex disposition lane).
- Evidence lives ONLY in baseharbor-plan (this directory), never in a product repo.
- No markdown checkboxes used; plain bullets.

## cleanliness

- this lane started zero containers/networks/volumes/compose projects on any host; ambient stacks untouched
- docker ps -a by this lane: not needed (no docker command invoked; read-only + GitHub API + local python replay)
- scratch files confined to /tmp/opencode (w315-*.{json,py,yml,diff,tsv,log}, sim* replay dirs, a*.zip artifacts) and this evidence directory
- worktree: workers/w315-0428-352-gateexec-plan (own isolated plan worktree, removed after merge per protocol)

## STEP G1 — product merge witness (mission context check)

- `gh pr view 1859 --json state,mergedAt`: state MERGED, mergedAt 2026-11-26T11:17:50Z → the catalog change is now part of the trusted BASE; the develop head moved b7855f78a → 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` at END: 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74.
- `git log --oneline b7855f78a0253b9423e07da6ae92009b8f0fd1ae..5a37ddbd9a06dd44f6068d3266ff2ed853a84a74` = exactly one commit: "feat(0428-352): trusted catalog row so runtime-suite candidates select Docker/Podman gates (#1859)" — a merge/squash of #1859's own 3 commits; no foreign candidate is carried on top.
- `git merge-base --is-ancestor b7855f78a 5a37ddbd9` = TRUE (base head is an ancestor of the new develop head, i.e., the attested SHA from which the merged-catalog state was cut).
- `git diff --name-only b7855f78a 5a37ddbd9` = [scripts/pr-gate-coverage.json, scripts/test_pr_gate_coverage.py] and `git diff 0716d20be 5a37ddbd9` is empty — the catalog blob on develop is byte-identical to the head blob 4f6a4af85 this lane measured.

## STEP G — base-attestation replay witnesses (mission branch-provenance duty, applied to the read objects)

For the two candidate commits this mission evaluates, the base heads were fetched from the real URL and attested:
- #1812 chain: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = b7855f78a0253b9423e07da6ae92009b8f0fd1ae; `git merge-base --is-ancestor b7855f78a… b962e6d2c…` = TRUE; `git diff --name-only b7855f78a… b962e6d2c…` = [.github/workflows/pre-release-runtime-suite.yml] (single file).
- #1859 chain: base b7855f78a (same witness); `git merge-base --is-ancestor b7855f78a… 0716d20be…` = TRUE; `git log --oneline b7855f78a..0716d20be` = exactly w309's 3 own commits (7549a503c, f6fc8a71f, 0716d20be, all author w309-0428-352-14gatecatalog).
- The local replay in STEP E ran the planner with checkout semantics matching ci.yml:818-871 (checkout at the effective base = the base parent of the integration merge commit 8b96407aa, catalog staged from that same commit): result 14 selected / include n=14 / required=true.

## STEP F — remote truth witnesses

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1859/head refs/pull/1812/head` (at END):
  develop = b7855f78a0253b9423e07da6ae92009b8f0fd1ae (unchanged all mission); refs/pull/1859/head = 0716d20becc1f0acc1156e3120f6ca3351e12f4b; refs/pull/1812/head = b962e6d2cc56258730e0d580d053565561da6d5a
- gh pr view 1859: state OPEN, isDraft false, mergeable MERGEABLE, base develop b7855f78a, merged false
- run pair cited by w309 for head 0716d20be: run 45783262677 pull_request attempt 1 SUCCESS; run 45782087038 exists but head f6fc8a71f
- #1859 PR comments: both assert the 14 Light gates now execute on #1859's own runs, citing "census per_page=100: 32 jobs = 11 executed / 21 skipped / 0 failed". The census itself reproduces (STEP C1), but the run's own trusted-pr-plan artifact (downloaded by this lane) shows selected_gates=[] and PR · Selected Runtime SKIPPED. Sources split rather than contradict once the two gate families are separated: the comments' execution claim is wrong FOR THIS PR (its diff is the catalog scripts, selected 0 is correct there), the mission's ci.yml:183/225 observation is right for the other family (Targeted HA). Resolved in STEP E, no stop needed.

## contradictions-and-precedent (flagged, non-blocking — per mission STOP-and-report applies to contradicting SOURCES; here sources are consistent once split)

1. #1859 PR comments (and w309's impl akte 2d1813c9d3) read the 11/21/0 census as "14 gates execute". The run's own artifact proves 0 executed for that run. The claim holds only PROSPECTIVELY (post-merge on a workflow-file candidate), which STEP E states.
2. w309's akte STEP 6 self-description "tick it as you work" style aside: w315 found the 14-gate resolution requires the 10 gate-cover-token additions in the SAME PR (the row alone yields 6). #1859 includes them; any future minimal row must too.
3. LOCAL-OBJECT ANOMALY (self-corrected; NOT a remote finding — the remote stays clean). While reproducing the STEP E replay in the shared workers/baseharbor checkout, the LOCAL object 8b96407aa (the PR's integration merge commit, which the run's plan artifact legitimately reports as integration_sha) appeared to carry the plan repository's commit 44168d2d3c in its history. That was a cross-repo object leak of this machine's shared object store (w309's akte records that lane already fetched the plan repo into the baseharbor object store: `git fetch --quiet origin refs/pull/1859/merge`-style cross fetches), not remote truth. Remote REST truth: `GET /repos/mcpdev80/baseharbor/commits/8b96407aa…` → exactly TWO parents [b7855f78a, 0716d20be], tree 8cfac9cb10; `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1859/merge` → 8b96407aa (GitHub's merge ref for the PR). No plan-repo graft exists on any product remote object; no disposition needed. Local `git merge-base --is-ancestor 44168d2d3c 8b96407aa` returning FALSE on a freshly-fetched copy and TRUE inside the polluted shared store is the proof of the pollution; per the quarantined-checkout rule, no workers/baseharbor ref was cited as remote evidence anywhere in this akte (all remote claims come from ls-remote or api.github.com).

## plan-pub delivery evidence (second-to-last action)

- published via scoped plan PR https://github.com/mcpdev80/baseharbor-plan/pull/118 (never a direct push to protected main); branch head pushed and verified via `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/lane/w315-0428-352-gateexec` = 70054d03c2258f118e64cf4d0a2030967d5d5875
- own validate runs watched to terminal by this lane (self-run duty): 45810961423 SUCCESS (head efec9f623e), 45811558009 SUCCESS (head be0ab36311), 45811832727 SUCCESS (final head 70054d03c2); head/run pairs posted as PR comments on #118
- pre-push identity gate lines (`git log --format='%h an=%an cn=%cn' -1` before each push): 488aafaab4 an=w315-0428-352-gateexec cn=w315-0428-352-gateexec; dc0a63f5ff an=cn=w315-0428-352-gateexec; efec9f623e/be0ab36311/70054d03c2 all an=w315-0428-352-gateexec cn=w315-0428-352-gateexec
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/2026-11-26/w315-0428-352-gateexec` at the second-to-last action: output EMPTY (origin/main = b5678f2e12, latest merge of another plan PR #119). The akte is fully staged on plan PR #118, head 4bac87a5df…, run pair witnessed as FINAL: pull_request run 45812252198 'Plan · validate' SUCCESS on that exact head. plan main is PROTECTED (never direct-pushed): the merge into main is the admin/coordinator act (precedents #52/#61/#62). The grep above becomes non-empty with that merge.

## STEP H — live post-merge witness (#1859 merged to develop 2026-11-26)

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` (11:5x local): 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74. Ancestry: `git merge-base --is-ancestor b7855f78a 5a37ddbd9` TRUE; `git log --oneline b7855f78a..5a37ddbd9` = exactly one commit "feat(0428-352): trusted catalog row so runtime-suite candidates select Docker/Podman gates (#1859)". #1859's catalog files on develop are byte-identical to the head blob 4f6a4af85 (`git diff 0716d20be 5a37ddbd9` empty).
- New develop push runs 45809297842/45809298052: both completed SUCCESS (push-path runs; not the pull_request Selected-Runtime path).
- Live-execution status: the merge of #1859 itself makes the catalog row part of the TRUSTED BASE for every subsequent pull_request candidate (ci.yml:867-868 stages pr-gate-plan.py/validate-pr-gate-coverage.py/pr-gate-coverage.json from controller=effective base; measured replay of that exact trio gives 14 selected / include n=14 / required=true — STEP E). A workflow-modifying OPEN PR (e.g. #1812) needs one NEW pull_request event to show it: at this writing #1812 still has no run at base 5a37ddbd9 (`/actions/runs?head_sha=b962e6d2c…` lists only run 45771862723 from 06:58:04Z; PR updatedAt 06:58:00Z, state OPEN). No lane triggered anything (mission rule: lanes never rerun/toggle); that trigger is the coordinator/owner action.

## END line

END_DONE w315-0428-352-gateexec: 14 Light gates = PR-path Selected-Runtime family (ci.yml PR · Selected Runtime → pre-release-runtime-suite.yml), NOT the push-only Targeted HA family; #1859 (merged to develop 5a37ddbd9 at 11:17:50Z) makes the catalog row + 10 gate cover tokens EXECUTE-capable for any workflow-file pull_request candidate (measured replay 14 selected / required=true); its own runs executed 0 of them (census 11/21/0 confirmed, Selected Runtime SKIPPED); no runtime-validation/ha ref exists and that path is not needed for these gates; next trigger (coordinator/owner act): one new pull_request event on #1812 at the new base to show the executed 14.
