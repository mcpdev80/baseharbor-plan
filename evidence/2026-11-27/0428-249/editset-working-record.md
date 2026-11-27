# w362-0428-249-1812rebase — Evidence (editset round)

Lane: w362-0428-249-1812rebase · Card: 0428-249 · Repo: baseharbor · PR: #1812
Mission: coordinator/missions/w362-0428-249-editset.txt
Prior round (hop 05cb3fd95, parked/VOID attempts): see same-path akte sections below, retained.

## Dual-duty plan (owner instruction 03:34:12Z)
1. DONE 249 round: plan in all three places (board, no native todowrite, evidence ## PLAN).
2. DONE 249: edit-set (14 files) + forward commits 8c83c7091 (3 workflows) + 0b343af5e (2 narrow fixtures),
   4-Feld w362, NO push (remote stays 6ab5310d1).
3. DONE 249: both proof runs terminal; class diagnosis in akte; 'Selected runtime' class booked as
   #283/#284 prerequisite — NOT repaired on #1812 (owner 03:34:12Z).
4. 249 PENDING-GATE: after w255 combined-review ACCEPT + GO → ONE push (fast-forward
   6ab5310d1→0b343af5e), fresh exact-head run to terminal, PR comment, final akte, END.
5. 299: fetch card `tasks/t-20261125-hunt33-go-runtime-prereq.md` (card_number "0428-299") from plan
   origin/main; verbatim owner + ANSATZ identity block.
6. 299: reality check ls-remote (develop tip; refs/pull/1863/head=4160d53f…; stale fail 45913103879);
   base attestation SHAs.
7. 299: CLEAN worktree from branch `w336-0428-299-goprereq`; remote names resolved to github.com/mcpdev80.
8. 299: `git merge origin/develop` forward-only, 4-Feld verify, provenance+log gates (only #1863 commits
   in origin/develop..HEAD).
9. 299: prechecks gofmt/vet/build only; NO local tests, NO VM.
10. 299: ONE normal push + ls-remote delivery witness; identity line before push.
11. 299: fresh pull_request run on exact head to terminal (jobs census per_page=100); failure lines as
    STATE in akte, no blind retry, no waiver.
12. 299: akte `evidence/w362-0428-299-1863hop/akte.md` on plan main via isolated plan worktree + PR;
    verify path on origin/main before END; END post.

2. Fetch card 0428-249 + edit-set spec (qualification-workflow-integrity.md) + w255 ACCEPT review akte from
   plan origin/main; record verbatim frontmatter owner, identity, ANSATZ block.
3. Reality check via `git ls-remote`: develop tip + PR #1812 head/headRefName; BASE ATTESTATION.
4. Fresh worktree `workers/baseharbor/worktrees/w362-0428-249-editset` from the PR branch;
   `git merge origin/develop` forward-only under canonical identity.
5. Apply the accepted edit-set VERBATIM to ONLY the listed workflow files:
   cancel-in-progress=false on evidence jobs, run-unique non-cancelling orchestrator groups, resolver jobs
   with 40-hex output + checkout-equality assert, groups `bh-evidence-<resolved-SHA>-<gate>-<run_id>`,
   Podman single_default_native split into four independent jobs (SQL/Secrets; Node HTTPS enrollment/remote
   CLI; install destroy/interrupted retry; pinned-workload lifecycle/backup), keycloak_single_native stays
   separate.
6. Scope gate: diff vs develop must touch ONLY listed .github/workflows files (+ existing PR deltas);
   STOP (END_BLOCKED with file:line both sides) if an edit row does not apply to current develop wording.
7. Pre-checks: actionlint + gofmt/vet/build only; NO local tests, NO VM.
8. Identity + provenance gates (ancestor, origin/develop..HEAD log, diff --name-only), 4-field verify,
   ONE normal push, ls-remote delivery witness.
9. Observe Hosted CI on the new exact head to terminal (no cancel; jobs enumeration with per_page=100),
   record per-gate lines and failure lines in this akte.
10. PR comment: head SHA + run IDs.
11. Publish lane akte `evidence/w362-0428-249-1812rebase/editset-implementation.md` to plan main via
    isolated plan worktree + PR (no direct main push); verify on origin/main before END; END post.

## ANSATZ (visible block, editset round)
- Card fetched at runtime from plan origin/main (main >= e644c9316): `tasks/t-20261122-runtime-image-registry-artifact-unknown.md`
  frontmatter owner VERBATIM: `owner: "w362-0428-249-1812rebase"` (canonical lane identity; no "(lane X)" wrapper).
- git user.name: `w362-0428-249-1812rebase`; git user.email: `w362-0428-249-1812rebase@baseharbor.local`.
- Literal invocation for every commit/merge:
  `git -c user.name=w362-0428-249-1812rebase -c user.email=w362-0428-249-1812rebase@baseharbor.local commit|merge ...`
- Pre-push gate line: `git show -s --format=%an HEAD` must equal exactly `w362-0428-249-1812rebase`.
- Env: `env | grep -a GIT_(AUTHOR|COMMITTER)` empty (no inherited vars to unset);
  `git var GIT_COMMITTER_IDENT` = `w362-0428-249-1812rebase <w362-0428-249-1812rebase@baseharbor.local> …`.

## Remote resolution witnesses
- `git -C baseharbor-plan remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git` (planning repo verified).
- Product worktree checkout `git remote -v` (shared checkout) → `origin https://github.com/mcpdev80/baseharbor.git`;
  every fetch/push verified against `git ls-remote https://github.com/mcpdev80/baseharbor.git`.

## BASE ATTESTATION (editset round)
- `git ls-remote https://github.com/mcpdev80/baseharbor.git`:
  - refs/heads/develop = `ea5218d72e263f21e79853b679af50074dab8c25`
  - refs/heads/lane-0428-249-runtime-image-fix = refs/pull/1812/head = `05cb3fd95bdb390175482f1c08eadb28d9c9863a`
- Branch: new local worktree branch `lane-0428-249-editset-wip` created AT the PR head 05cb3fd95 (the #1812
  branch head per mission (a)); after the edit-set commits it is fast-forwarded onto the real branch
  `lane-0428-249-runtime-image-fix` and pushed (single candidate, single push). Old hop worktree moved to
  `…-1812hop-held` (held park); the editset worktree reuses the branch path.
- Authorization witnesses: plan main `0637bc3c0` (w255 Final ACCEPT), edit-set basis `f25e06380`
  (spec bytes on origin/main verified identical to f25e06380's copy, diff=0), card active at `e644c9316`.
  Review akte `workflow-integrity-review.md:96`: worker w362 on named card 0428-249 implements exactly this
  Owner-approved edit set (the `.github` exception; no broader authority inferred).

## Edit-set scope decision (posted as QUESTION)
- The spec table names 14 files; mission (d) lists 12 (excludes `targeted-demo-acceptance.yml` and
  `supplemental-release-validation.yml`). Per mission wordings ("NUR die .github/workflows-Dateien, die das
  Edit-Set nennt (Liste)") I implement exactly the 12 named files and report the two unlisted rows as
  untouched edit-set gaps for coordinator/owner disposition. No invention either way.

## Remote resolution witnesses
(pending)

## BASE ATTESTATION
(pending)

## Edit-set drift analysis (mission STOP rule) — STOP+REPORT, no invention
Authority check: the w255 ACCEPT akte (`workflow-integrity-review.md:89`, plan main 0637bc3c0) states
"BaseHarbor develop source reviewed: `6d237ccdf3a5db19c5814ad5b76d01be6c38c35c`". The actual landing basis
after the forward merge is develop `ea5218d72` (= 6d237ccdf + PR #1833 `fix(0428-288) compose service IDs`).
Per-file drift of the edit-set's quoted "Before" lines vs current develop ea5218d72:

| Spec row | Quoted current state | Actual ea5218d72 | Drift |
| --- | --- | --- | --- |
| ci.yml:24-26 | `ci-${{ github.ref }}`; cancel true | identical | none |
| ci.yml:180-182/:222-224 | group `baseharbor-release-qualification`, cancel false | identical | none |
| host-trust-owned-e2e.yml:23-25 | group PR-number-or-ref; cancel true | `host-trust-owned-${{ github.event.pull_request.number \|\| github.ref }}` | none |
| nextjs-greenfield-e2e.yml:13-15 | group PR/ref; cancel true | `greenfield-native-${{ github.event.pull_request.number \|\| github.ref }}` | none |
| observability-acceptance.yml:33-35 | ref+input group; cancel true | `observability-full-stack-${{ github.ref }}-${{ inputs.ref \|\| github.ref_name }}` | none |
| mcp-lifecycle-acceptance.yml:28-30 | ref/input group; cancel true | `mcp-lifecycle-${{ github.ref }}-${{ inputs.ref \|\| github.ref_name }}` | none |
| docker-runtime-acceptance.yml:24-26 | workflow/ref group; cancel true | `${{ github.workflow }}-docker-${{ github.ref }}` | none |
| podman-acceptance.yml:23-25 | workflow/ref group; cancel true; `:106-175` bundles four assertions | identical incl. bundled steps `:129-:172` | none |
| pre-release.yml:6-8 | group develop-run-id OR static lock; cancel false | identical | none |
| pre-release.yml:882/:934 (HA) | per-gate groups | NO job-level concurrency block present at ha_groups_docker/ha_groups_podman | minor (spec adds groups) |
| targeted-integration.yml:51-64 | Before block quoted verbatim | lines 53-58 (inputs.ref) + 60-64 concurrency — byte-equivalent shape | none |
| pre-release-runtime-suite.yml:81-126 | validate raw inputs.ref → checkout raw → `git rev-parse HEAD` | identical (:81-126) | none |
| runtime-broker.yml:6-20,25-37,321-325 | acceptance `:26`, performance `:321`, no resolver/concurrency | identical | none |
| runtime-s3-acceptance.yml:4-23 | dispatch default `develop`, raw checkout `:22` | identical | none |

Decision trace: mission STOPS say "NICHT erfinden" only when a row DRIFTS. All 12 named files match their
quoted Before state on ea5218d72, so the edit set is applicable and I implement it (scope clarification
already posted as QUESTION re: the 12-vs-14 file list; 12 implemented, 2 unlisted rows reported as gaps).
Where the spec states a pattern "After" only as prose (job group literals, resolver wiring), the reusable
resolver block (:186-224) and per-workflow consumer table (:230-238) are applied verbatim.

## Edit-set implementation log (per file)
All 14 authorized files edited (12 in the first edit-set commit `2981efea1`/`860d41572`+`6ab5310d1`
lineage; the 2 late-scope rows `targeted-demo-acceptance.yml` + `supplemental-release-validation.yml`
are staged in the forward commit per coordinator correction 03:12:26Z). Per-file application:
- ci.yml: workflow group → `ci-${{ github.event.pull_request.head.sha || github.sha }}-${{ github.run_id }}`,
  cancel false; targeted_ha_docker/podman job groups → `targeted-ha-docker/podman-<sha>-<run_id>`.
- host-trust-owned-e2e.yml: group → `host-trust-owned-<sha>-<run_id>`, cancel false.
- mcp/nextjs/observability/docker/podman-acceptance, runtime-broker, runtime-s3, pre-release-runtime-suite,
  targeted-integration: run-unique non-cancelling orchestrator groups + `resolve_candidate` jobs (40-hex
  validation, fetch of branch-shaped inputs) + evidence-job groups
  `bh-…-<candidate_sha>-<gate/runtime>[-<matrix identity>]-<run_id>` + resolver-output checkouts with
  `test "$(git rev-parse HEAD)" = "$EXPECTED…"` equality asserts. Podman single_default_native split into
  four independent jobs (sql_secrets / node_https / install_destroy / pinned_workload), each own
  setup/cleanup/timeout; keycloak_single_native untouched-but-grouped.
- pre-release.yml: orchestrator `pre-release-orchestrator-<run_id>`; gate/HA callers keyed by
  `needs.source.outputs.candidate_sha` + matrix identity + run_id.
- podman-acceptance dedup: one cleanup step in pinned_workload (correction 02:53Z, commit 6ab5310d1).

## Provenance / log / diff gates
- `git merge-base --is-ancestor origin/develop HEAD` → OK (develop tip ea5218d72 is ancestor of 6ab5310d1).
- `git log --oneline origin/develop..HEAD` = #1812 chain only (9140b2cbd … 05cb3fd95, 709a9b1be merge,
  860d41572 edit-set, 6ab5310d1 dedup). No foreign commits; merge identity 4-Feld w362.
- `git diff origin/develop...HEAD --name-only` = the 12 listed workflow files +
  `cmd/baha/ci_integration_operator_enabled.go` (pre-existing PR product delta). Staged forward diff adds
  the 2 workflow files + 2 scripts test files (all inside authorized edit-set scope; test files are the
  accepted-editset-mandated routing/routing-matrix expectation updates).


## Forward-commit staging (prepared, NOT committed — push only after BOTH runs terminal)
1. `scripts/test_ci_check_routes.py` lines 130 and 139: the edit set replaced the evidence-job checkout
   `ref: ${{ inputs.ref || github.sha }}` with `ref: ${{ needs.resolve_candidate.outputs.candidate_sha }}`
   (accepted spec rows for docker-runtime-acceptance.yml and podman-acceptance.yml). Routing-test
   expectation updates to the resolver-output form are the test-side of THIS card's gate route
   ('PR · Focused Python' executes scripts/test_ci_check_routes.py via existing discovery; no new gate).
2. Staged targeted-integration.yml group-expression fix (3 lines, actionlint-verified local exit 0).
3. Pending: 'Workflow policy' terminal-log diagnosis on both runs — if `scripts/ci-workflow-policy.sh`
   raises its own changed-file/gate-ID case beyond the actionlint step, that fix goes into the same
   forward commit (or STOP+file:line if outside card scope).

(pending)

## Scope correction 03:12:26Z — 14 files (two late rows added to the forward commit)
- Coordinator korrigiert seine 12/14-Antwort: die ACCEPT-Akte nennt targeted-demo-acceptance.yml und
  supplemental-release-validation.yml ausdrucklich als zu aendernde Zeilen; Mission-Datei berichtigt.
  Forward-commit umfasst damit zusätzlich:
  - targeted-demo-acceptance.yml: workflow-level group war statisches
    `baseharbor-release-qualification` → `targeted-demo-orchestrator-${{ github.run_id }}`
    (cancel-in-progress false). Jeder Downstream-Evidence-Job (ecosystem_source, selected_gate matrix,
    consumer_integration, develop_ecosystem_result, reference_journey) erhaelt job-level
    `targeted-demo-${{ needs.resolve.outputs.ref }}-<identity>-${{ github.run_id }}`, cancel false. Der
    bestehende `resolve` Job (:55-62) emittiert bereits die 40-hex SHA des getesteten Candidates —
    kein neuer Resolver ("use existing resolver outputs").
  - supplemental-release-validation.yml: job-level
    `supplemental-validation-${{ github.sha }}-${{ github.run_id }}`, cancel false + checkout-equality
    assert gegen github.sha ("use the already-resolved proven candidate").
- Staged-state pre-checks: actionlint über ALLE .github/workflows = exit 0; py_compile scripts clean.
- Staged files nun 5: targeted-integration.yml (group exprs), targeted-demo-acceptance.yml,
  supplemental-release-validation.yml, scripts/test_ci_check_routes.py,
  scripts/test_pr_selected_runtime_matrix.py.
- Run 45931118156 weiterhin pending (16 Jobs running); Push bleibt bis terminal gesperrt.

- Edit-set commit `2981efea1` (12 files, 677+/51-) + merge `709a9b1be` of develop `ea5218d72` (runner-health
  landing basis; forward-only, no force, no cherry-pick). Provenance: `git merge-base --is-ancestor
  origin/develop HEAD` = OK; `git log --oneline origin/develop..HEAD` = the #1812 chain only (9140b2cbd …
  05cb3fd95 + 709a9b1be + 2981efea1). Diff vs develop: 12 listed workflow files + the PR's two pre-existing
  deltas (`cmd/baha/ci_integration_operator_enabled.go`, plus pagination/contract files already on the
  develop line of the merge parents).
- Identity: `an=w362-0428-249-1812rebase ae=…@baseharbor.local cn=… ce=…` on BOTH commits; `%an` gate line OK.
- Pre-checks: yaml-parse all 12 files OK; actionlint: 3 expression findings fixed (matrix refs → inputs.gate/
  ref_name); gofmt/vet/build green; NO tests locally.
- Push (first, allowed window): `05cb3fd95..2981efea1`→ delivered as `860d41572`? CORRECTION: push #1 landed
  `860d41572` (the amended 2981efea1), ls-remote head+PR-head witnesses = `860d41572`. Fresh pull_request run
  `45930995254` queued on exact head `860d41572`.
- HALT-LINIE (owner 02:55:27Z): run 45930995254 is the qualification run — do NOT cancel, do NOT push again
  until it is terminal + 'Workflow policy' failure diagnosed (its failure was observed at queue time). The
  dedup fix (single cleanup step in `single_default_native_pinned_workload`, verified locally via yaml +
  actionlint) was pushed prematurely as `6ab5310d1` (run 45931118156 started) — recorded as deviation: from
  here the lane parks; after 45930995254 terminal, ONE forward commit (targeted-integration follow-up edit +
  any policy fix) + ONE push + fresh exact-head run.

## Review-Befund + Ruecknahme (static verification, no flip, no test run)
- Coordinator-Ruecknahme 03:08:10Z akzeptiert; beide Fakten statisch gegen das File verifiziert:
  - `focused` (targeted-integration.yml, job block ab `^  focused:`): KEIN `strategy:`/`matrix:` —
    single job (`runs-on: ubuntu-latest`, name `${{ inputs.gate }}`), dispatch-gated
    (`github.event_name == 'workflow_dispatch'`). Gruppe `…-focused-${{ inputs.gate }}-…` traegt damit
    die volle Gate-Identitaet; keine Runtime-Matrix, keine Verdraengungskollision. Korrektur meines
    frueheren Kommentars ":636 war matrix.runtime" — der Job hat ueberhaupt keine Matrix.
  - `v0421_ha`: hat `strategy.matrix.runtime` (docker/podman aus ref_name-Endung) und traegt im group
    weiterhin `${{ matrix.runtime }}` (`…-v0421_ha-${{ github.ref_name }}-${{ matrix.runtime }}-…`) —
    beide Beine eigene, unabhaengig terminale Gruppen. Keine Umpolung noetig; Folgeedit bleibt wie staged.
- Push-Gate unveraendert: kein Push bis 45931118156 terminal (watcher aktiv).

- (a) Local actionlint against the staged state: exit 0 (all 12+1 files). Proof of carrier: HEAD-only run
  shows 3 findings; with staged targeted-integration.yml fix: clean.
- (b) Failure-class diagnosis from the terminal jobs of run 45931118156 (file:line, both sides):
  1. **Workflow policy** (job 140283718707): `ci-workflow-policy.sh` PASS; FAILURE in "Validate workflow
     syntax" = remote actionlint v1.7.12 on `.github/workflows/targeted-integration.yml:636/:1170/:1286`
     (matrix.runtime/matrix.group/matrix.gate on matrix-less jobs). Carrier: staged group fix (:636→inputs.gate,
     :1170→github.ref_name+matrix.runtime, :1286→inputs.gate).
  2. **ci-actionlint** (job 140283788063): identical 3 findings, same carrier.
  3. **PR · Focused Python** (job 140283787870): `scripts/test_ci_check_routes.py:130` and `:139` asserted
     `ref: ${{ inputs.ref || github.sha }}` in docker-runtime-acceptance.yml / podman-acceptance.yml;
     accepted edit-set rows spec:233/:234 replaced both with the resolver output. Staged fix: expectations
     now `ref: ${{ needs.resolve_candidate.outputs.candidate_sha }}`.
  4. **PR · Validation · ci-executor-tests** (job 140283788015, runs scripts/pr-check-runner.py
     CI_EXECUTION_SUITES incl. test_pr_selected_runtime_matrix + test_ci_check_routes):
     - `test_pr_selected_runtime_matrix.py:231` selected() required an `if:` on EVERY job → new
       `resolve_candidate` prerequisite has none. Staged fix: resolver skipped (not a routed gate).
     - `:91` asserted `needs: pr_selected_coreless_lifecycle_shards` (string); now `[resolve_candidate, …]`
       list form per spec :160 "append, do not replace". Staged fix accepts the list form.
     - `:119-141` asserted the OLD workflow-level group containing `inputs.gate || 'default'`; superseded
       by the accepted orchestrator+job-level scheme (spec :36-38 "earlier raw-input group proposals are
       withdrawn"). Staged fix asserts the run-unique orchestrator group + per-job resolver-SHA groups
       keep gate/runtime isolation (docker vs podman groups differ).
     - test_ci_check_routes failures repeat inside this check → same carrier as (3).
  5. **Policy-check logic read** (c): `scripts/ci-workflow-policy.sh` = "Enforce fixed workflow surface"
     (approved-file list, no new validation-check files) + gate-catalog consistency; it did NOT reject the
     edit set (PASS lines in log). The forward commit adds no check files, so no
     pr-gate-plan.py/release-requirements.json updates are required (doctrine: only check-file/gate-ID
     additions trigger them). Gate route for updated tests: both modified test files already run inside
     'PR · Focused Python' AND ci-executor-tests suites (existing discovery — no new registration).
- Run 45931118156 + 45930995254 remain untouched (watchers active). Old-head witnesses for the akte:
  45915629291 attempts 1-2 VOID; 45930995254 (860d41572) and 45931118156 (6ab5310d1) = the four classes above.

- Carrier check VERIFIED (corrects my earlier mid-analysis note): at HEAD 6ab5310d1 alone,
  `actionlint targeted-integration.yml` exits 1 (the 3 findings persist in the committed head — they were
  fixed in the amended 860d41572 but 6ab5310d1 was rebuilt from the ORIGINAL 2981efea1 tree). With my
  staged follow-up edit applied, actionlint exits 0. The staged targeted-integration.yml group fix IS the
  carrier and stays in the forward commit.
- 'Workflow policy' job (140283718707, head 6ab5310d1) log read early (job already terminal):
  `scripts/ci-workflow-policy.sh` = "Workflow policy PASS: 20 approved workflow files" + "Gate catalog
  consistency PASS: no check-file or gate-ID additions/removals"; the FAILURE came from the second step
  "Validate workflow syntax" → remote actionlint v1.7.12 reports exactly the 3 findings (:636/:1170/:1286).
  So both the policy FAILURE and the ci-actionlint FAILURE are one root cause = the 3 expressions;
  carrier = the staged edit. On head 860d41572 (run 45930995254) the same 3 findings are expected
  (identical lineage) — confirm from its logs at terminal.
- 'PR · Focused Python' FAILURE (already terminal on 6ab5310d1): routing test
  `scripts/test_ci_check_routes.py::CheckRoutingTests::test_docker_dispatch_uses_selected_ref_and_receipt_check_only_runs_after_tests`
  asserts the literal `ref: ${{ inputs.ref || github.sha }}` in docker-runtime-acceptance.yml (:130) and
  podman-acceptance.yml (:139); the accepted edit set replaced both with the resolver output (spec rows
  :233/:234). Forward-commit content: (1) staged targeted-integration group fix, (2) the two routing-test
  expectation lines. Test route: 'PR · Focused Python' runs scripts/test_ci_check_routes.py via existing
  discovery — gate rule satisfied, no new check.
## Push + fresh exact-head run (owner ruling 04:19:09Z executed)
- (1) `git merge origin/develop` (ea5218d72) => `Already up to date` (already-merged via 709a9b1be;
  no conflict, no STOP needed). (2) Carriers forward-only: `git log ea5218d72..HEAD` top = 0b343af5e
  -> 8c83c7091 -> 6ab5310d1 chain; ancestry gate CARRIERS-OK. 4-Feld verified pre-push
  (`an=ae=cn=ce=w362-0428-249-1812rebase`).
- (3) ONE normal push: `6ab5310d1..0b343af5e -> lane-0428-249-runtime-image-fix` (no force).
- (4) Delivery witnesses: ls-remote branch + refs/pull/1812/head = `0b343af5ea895d23cbe808fda50a66d550552bc6`;
  `gh pr view 1812 --json headRefOid` = same SHA.
- (5) Fresh pull_request run on exact head: **45939271268** (gh run watch active in this session;
  census with per_page=100 incl. BOTH native Docker and Podman gates + error classes to be recorded
  at terminal).
## Merge-gate check (owner task 04:16:17Z) — STOP+MELD executed, candidate untouched
- Step (1) reality check first, per protocol. ls-remote witnesses: refs/heads/develop =
  `ea5218d72e263f21e79853b679af50074dab8c25`; refs/heads/lane-0428-249-runtime-image-fix =
  refs/pull/1812/head = `6ab5310d1…`.
- Local ancestry test: `git merge-base --is-ancestor 6ab5310d1 <develop@ea5218d72>` = **NO**. The
  runner-health ruling content (cancel:false, SHA-keyed groups, Podman split) is NOT in develop; it
  exists only on the #1812 branch itself. So "steckt bereits in head 6ab5310d1" is true only about
  MY candidate — the decision has not landed on develop.
- Therefore `git merge origin/develop` into the candidate (`lane-0428-249-editset-wip` @ 0b343af5e)
  is a provable NO-OP: 709a9b1be already merged ea5218d72; `Already up to date.` (witness above).
  The merge step contributes nothing; the premise for a qualification run ("develop tip green for
  this merge base") is unproven.
- A push of 8c83c7091+0b343af5e would trigger the full known-consent-failing matrix (Klasse 5,
  #283/#284 prerequisite) while the demo #183 + pin sequencing stands unchanged in the owner's own
  line. No push made; no force; no cherry-pick. Carriers stay local, remote stays 6ab5310d1.
- Awaiting: either (a) the ruling actually lands on develop (then a real merge/hop + push + fresh
  run), or (b) explicit owner GO that the push+run is wanted exactly despite develop not carrying
  the decision yet.
## Terminal-log diagnosis (both runs terminal 2026-11-27 ~03:29/03:33Z)
- **45931118156** (head 6ab5310d1) = completed/failure. **45930995254** (head 860d41572) = completed/failure.
  Witness: gh run view status/conclusion + per-job listings above.
- Class 1 'Workflow policy' (both runs, jobs 140283718707 / 140283331625): `ci-workflow-policy.sh` PASS
  ("20 approved workflow files", "Gate catalog consistency PASS"); FAILURE = actionlint v1.7.12 step,
  EXACTLY `.github/workflows/targeted-integration.yml:636/:1170/:1286` (matrix.runtime/matrix.group/
  matrix.gate). Carrier: committed 8c83c7091.
- Class 2 'PR · Validation · ci-actionlint' (140283788063/140283393909): identical 3 findings. Same carrier.
- Class 3 'PR · Focused Python' (140283787870/140283393859): test_ci_check_routes.py:130/:139 old
  checkout-form assertion. Carrier: committed 0b343af5e (narrow fixture fix).
- Class 4 'PR · Validation · ci-executor-tests' (140283788015/140283393979): test_pr_selected_runtime_matrix
  old-form expectations (:231 if:-presence incl. resolve_candidate, :91 string-form needs, :119-141 branch
  group). Carrier: committed 0b343af5e. NO executor/planner implementation defect observed → no STOP case.
- Class 5 runtime gates (identical 8 failures on BOTH heads: docker/podman × connectivity, policy,
  reconciliation, full-destroy): job logs show root cause
  `Error: record deployment before mutation: candidate submission requires an explicit
  operator/automation consent (--confirm-candidate); refusing to record deployment state` inside the Demo
  acceptance `run_consented "$BAHA" up --yes` path (baseharbor-demo tests/connectivity/run.sh:36 family),
  preceded by transient registry `blob/manifest unknown` retries on localhost:5000 (per-job local registry,
  same-runner; the runtime-image reload delta applies only to the backup/stop reset paths, not to these
  gates' first push). NOT attributable to the four static classes; the consent-refusal signature matches
  the known Demo consent-recognizer line (cards 0428-281/282 family and the current pin's
  fixture-consent digest extraction). The forward push's fresh exact-head run is the discriminator: if
  class 5 persists with green classes 1-4, it is product/demo-attributable and I STOP+REPORT (no waiver).
## Scope reduction (owner audit 03:42:39Z)
- `6ab5310d1` (the REMOTE head) already contains all three ruling requirements in its workflow diff
  (cancel:false; resolved-SHA + run_id groups; Podman single-default split). My forward carrier set is
  therefore ONLY the fixture correction `0b343af5e` plus the `8c83c7091` matrix-ref expression fixes
  IF they are not already in the remote head (they are not: the terminal actionlint logs of
  45931118156 show `targeted-integration.yml:636/:1170/:1286` findings on 6ab5310d1 itself).
  My akte line "Carrier: committed 8c83c7091" for classes 1/2 stays true and is not duplicated work:
  8c83c7091's edits to targeted-demo-acceptance.yml / supplemental-release-validation.yml are group-
  KEY additions on top of the remote's already-present cancel:false; the targeted-integration.yml part
  is the matrix-ref fix the audit names. No further workflow work; no push before #183 merge + pin.
- Mission (2) #1863 stays active (run census below).

- Push preconditions per owner route: w255 combined-diff review + w267 dispositions awaited; both runs
  terminal (requirement met); local forward state = 8c83c7091 + 0b343af5e on top of 6ab5310d1.

- (1) Scope stays the 14-file list; my forward-commit content for the workflow side is already committed
  locally as `8c83c7091` (3 files, +32/−4; pure workflow groups).
- (2) Test-only narrow adaptation is authorized EXACTLY for the two fixtures that encode the OLD workflow
  form. My earlier staged edits (reverted at the 03:15:43Z scope finding) match this rule and will be
  RE-APPLIED only after both runs are terminal and the terminal logs are confirmed, in narrowest form:
  - `scripts/test_ci_check_routes.py:130/:139` — positive assertion string swapped from
    `ref: ${{ inputs.ref || github.sha }}` to `ref: ${{ needs.resolve_candidate.outputs.candidate_sha }}`
    (docker+podman). The test's other assertions (dispatch required:false/no default, receipt-check
    step ordering) stay untouched. This encodes the OLD checkout form only.
  - `scripts/test_pr_selected_runtime_matrix.py` — three narrow edits, all preserving positive+negative
    semantics: (a) selected() skips only the `resolve_candidate` prerequisite job (not a routed gate) so
    the negative-routing assertions on real gates stay intact; (b) :91 accepts the list form
    `[resolve_candidate, pr_selected_coreless_lifecycle_shards]` (spec row :160 mandates "append, do not
    replace") and keeps the SHARDS_RESULT negative assertion; (c) :119-141 concurrency test rewritten to
    the accepted scheme (run-unique orchestrator group + per-evidence-job groups carrying gate/runtime
    identity) while KEEPING the isolation invariant (docker-group != podman-group, determinism equal).
  - No third test file; no policy/executor/runner/planner code; no actionlint config. If the terminal
    logs show any class needing those, STOP+MELD per rule (3).
- (3) Re-verify carriers against terminal logs before applying: the 4 classes were diagnosed from
  EARLY logs; the confirmation pass uses the full per-run log set (both run IDs + all failing job IDs
  with file:line) which the owner required in the final akte.
- Push-Gate unchanged.

- Scope bestaetigt sauber: staged = nur 3 autorisierte .github/workflows-Pfade
  (supplemental-release-validation.yml, targeted-demo-acceptance.yml, targeted-integration.yml; +32/−4);
  die beiden Test-Fixtures sind auf develop zurueck; der 4-Klassen-Fix (actionlint-Befunde in
  targeted-integration commit content + routing/routing-matrix Test-Erwartungen) liegt bei Codex-Disposition.
- Gate: KEIN Push bis 45931118156 und 45930995254 terminal; Diagnosen beider Runs werden in dieser Akte
  ergaenzt; Vorwaertsfix wird erst mit der Disposition-Antwort (naechster Send, auch an w267) geformt.
- Watcher aktiv auf beiden Runs in dieser Session.

- Delegation accepted (coordinator 02:58:56Z, keine Rüge): 6ab5310d1 ist der aktuelle Beweis-Kopf mit eigenem
  Run 45931118156; beide Runs bleiben unangetastet bis terminal, dann EIN Vorwaertscommit
  (targeted-integration-Folgeedit + policy-Fix; Dedup ist in 6ab bereits drin), 4-Feld w362, EIN push,
  frischer Exakt-Head-Run; Akte fuehrt alle drei Run-IDs.
- Policy-Log-Diagnose run 45931118156 (job "Workflow policy", id 140283718707, step actionlint):
  exactly the 3 findings my local actionlint had already flagged and I fixed —
  targeted-integration.yml:636 `matrix.runtime` in `focused`, :1170 `matrix.group` in `v0421_ha`,
  :1286 `matrix.gate` in `adoption` ("property … not defined in object type"). Root cause of the premature
  push race: the fix landed in the later dedup commit `6ab5310d1`, not in `860d41572`/`2981efea1`-lineage
  content the policy checker saw at 02:55Z. Current head 6ab5310d1 already contains the corrected groups
  (local actionlint on 6ab5310d1: exit 0).
- Diagnosis of run 45930995254 (860d41572): same actionlint failure class expected (its head carried the
  same 3 findings pre-fix); its logs become readable at terminal; recorded then.
- Forward commit after both terminal: targeted-integration follow-up check + (if any residual policy finding)
  the minimal fix; then ONE push + fresh exact-head run.
- Akte published on plan main 8b1451342 via plan PR #176 (validate green 45931313754); worktree kept.
- Both runs unangetastet bis terminal (owner halt-lines 02:55Z/02:56Z): 45930995254 (860d41572),
  45931118156 (6ab5310d1). Watcher active on the proof run in this session.
- Post-terminal plan: 'Workflow policy' log diagnosis → ONE forward commit (targeted-integration follow-up
  + policy fix, canonical w362 identity, 4-Feld) → EIN push → fresh exact-head run → final akte + END.

- Candidate branch: lane-0428-249-runtime-image-fix; head remote = `6ab5310d1` (dedup already in due to the
  premature push; owner accepted the duplicate-visible run 45930995254 as the proof run to let finish).
- Local staged follow-up: none pending beyond the policy fix awaiting 45930995254 diagnosis logs.
- Runs in flight: 45930995254 (head 860d41572, proof run — let terminal), 45931118156 (head 6ab5310d1).
- END marker per coordinator: parked-run+staged-fix.

(pending)

## Hosted CI gate lines (new exact head)
(pending)

## repo-rule compliance
(pending)

## cleanliness
(pending)

## END line
(pending)

---
## Prior-round record (hop mission, parked; kept for continuity)
- Candidate 05cb3fd95 (merge of 210d5d105 + develop c167fa5dd). pull_request run 45915629291: BOTH attempts
  VOID per owner AKTE-KORREKTUR 01:5xZ (attempt 2 CANCELLED 01:12:22Z). Validation dispatch 45918769472
  REJECTed at pre-release.yml:191 pin precedence. Plan akte published: PRs #172/#174/#175 → plan main
  d625e802e. Park quittiert 02:5xZ + 01:32Z; reactivated at w255 Final-ACCEPT (plan main 0637bc3c0,
  edit-set basis f25e06380), card set active (main e644c9316).
