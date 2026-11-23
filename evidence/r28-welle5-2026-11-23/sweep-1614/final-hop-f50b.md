# #1614 FINAL-HOP onto f50b118f (post-ingress) + wizard-app-edit coverage finding

Lane: w076-0428-076-1789rest (sitz 9b7683b5). Orders: coordinator follow-up 06:26 (final hop),
then ENTSCHEID ruling 06:5x (prove coverage by log-grep, then fix per Fall A/B). Branch
`lane-0428-062-cli2-app-status`, worktree
`/home/marcel/dev/baseharbor-ecosystem/workers/sweep-1614-hop-wt`.

## PLAN

1. Fetch + rev-parse origin/develop (== f50b118f2); attest PR head still cdcf6aa2.
2. `git merge --no-ff origin/develop` onto the 1614 branch.
3. BELEG before push: catalog diff vs develop EMPTY; `.github` untouched; files == product-scope; log-line proof.
4. Push + `ls-remote refs/pull/1614/head` witness; PR ready (non-draft).
5. One PR-triggered run to terminal; report head + run-id + gates.
6. Ruling execution step 1 (read-only): locate the test in the exact CI source; log-grep the green lifecycle cells of 45124111962; report Fall A/B via handoff BEFORE fixing.

## Remote resolution (REMOTE GUARD)

`git remote -v` (first git action):

```
origin	https://github.com/mcpdev80/baseharbor.git (fetch)
origin	https://github.com/mcpdev80/baseharbor.git (push)
```

## BASE ATTESTATION

`git fetch origin develop && git rev-parse origin/develop` →
`f50b118f2dfc670ac040185a0a766370f8d992a2` (exact mission tip; nothing higher at fetch time).
Pre-merge ls-remote: branch and `refs/pull/1614/head` both `cdcf6aa2a8c7ce3b84dc021e7c3333168cd3fe5c`.
merge-base before hop: fc3eecbf.

## Merge

`git merge --no-ff --no-edit origin/develop` → auto-merged (ort), zero conflicts:

```
new head 90694e32d653ca3f9af4bddd417eeeba86c67ea6
git log -1 %P: 90694e32 cdcf6aa2a8c7ce3b84dc021e7c3333168cd3fe5c f50b118f2dfc670ac040185a0a766370f8d992a2
```

`git merge-base --is-ancestor origin/develop HEAD` → exit 0.

## BELEG (step 3)

- `git diff origin/develop HEAD -- scripts/pr-gate-coverage.json` → 0 lines (`--quiet` exit 0).
  242 components, 242 unique ids, release `v0.4.27`: the 12 ingress rows are base — no PR-side duplicates.
- `.github/**`: 0 files in branch-vs-develop diff.
- `git diff origin/develop...HEAD --name-only` → 24 files, all within card 0428-062 product/docs/
  contracts scope (cmd/baha app_* family, machine_coverage, contracts/machine/v1/read-models.schema.json,
  docs EN/DE, internal/machinereadmodels).
- `git log --oneline origin/develop..HEAD` → only this chain's own commits + its hop merges
  (90694e32, cdcf6aa2, 0077c98f, 098d4554, 3ddf61e4, 4bfc775d, 80d4df52, 6377f1b2, 03e28080,
  818d572b, 63468454, 0963d08d, 98877cc1, eda0cd61).

## Push + delivery witness (step 4)

`git push origin HEAD:refs/heads/lane-0428-062-cli2-app-status` → `cdcf6aa2..90694e32`.
`git ls-remote origin refs/pull/1614/head refs/heads/lane-0428-062-cli2-app-status`:

```
90694e32d653ca3f9af4bddd417eeeba86c67ea6	refs/heads/lane-0428-062-cli2-app-status
90694e32d653ca3f9af4bddd417eeeba86c67ea6	refs/pull/1614/head
```

`gh pr view 1614`: isDraft=false (READY), state OPEN. No merge by this lane.

## Hosted CI (step 5, Eigenes-Run-Pflicht) — one PR-triggered run

- Run: **45124111962**, pull_request, headSha `90694e32`,
  url https://github.com/mcpdev80/baseharbor/actions/runs/45124111962
- Terminal: `completed / failure`.
- Success (executed): PR · Trusted Plan (BASE_SHA f50b118f — TP green as expected, my 12 base rows
  admitted), PR · Native gate plan, Workflow policy, Source format, Runner Interface, Go unit
  cli-0..3 + packages + owner, Focused Python, Exact Candidate, Demo Pin, documentation-audit,
  mkdocs en/de strict, pages-candidate-build, go-build/go-vet/cli-gofmt, wizard-registration-tests,
  Selected Runtime docker·lifecycle (137525014971), docker·data-capabilities (137525014982),
  docker·observability (137525014985), podman·observability (137525014990),
  Selected Core-less docker fan-out incl. core-capability shards (137524514876/966, 137530364609).
- Single red: `PR · Validation · wizard-app-edit-tests` (job 137524476740) —
  `RuntimeError: required test skipped: TestAppEditCommandCompleteProviderEditRunsRealLifecycle`
  (scripts/pr-check-runner.py:288 fail-loud on skip; pattern owner
  `wizard-app-edit-tests: (r'^TestAppEditApply', r'^TestAppEditCommand')` at pr-check-runner.py:31).
  Aggregate `PR Selected Checks` → failure.

## Coverage finding (ruling step 1: EXAKTE CI-QUELLE + log-grep) → **FALL B**

Catalog position (exact CI source, this head):
- Test name appears in NO `required_test_names` of scripts/pr-gate-coverage.json.
- Its file `cmd/baha/app_edit_apply_test.go` is cataloged on surfaces
  `source.gate.atomic.docker.lifecycle` + `source.gate.atomic.podman.lifecycle` (id
  source.cmd.baha.app.edit.apply.test.go); catalog gate entries `atomic/docker/lifecycle`,
  `atomic/podman/lifecycle` (class runtime, scope pr, covers the source.gate surfaces above) exist.

Hosted log greps (run 45124111962, `gh run view --job … --log`):
- docker·lifecycle cell 137525014971: test name occurrences **0**.
- docker·data-capabilities 137525014982: **0**. core-capability shards 137524514876/137524514966: **0**.
- coreless-lifecycle group 137530364609: **0**.
- Only job mentioning the name: failing wizard-app-edit 137524476740 (as SKIP → RuntimeError).

Route analysis in the exact CI source:
- scripts/ci-native-pr-gate.sh runs named `run_exact_test` lines only for enumerated gate ids
  (installation-destroy, second-target-conflict, greenfield, onboarding/guided, perses-runtime-smoke,
  data-capabilities, coreless-lifecycle, environment-destroy, service-stop). NO case for
  `atomic/docker/lifecycle` / `atomic/podman/lifecycle`.
- The Selected Runtime docker·lifecycle cell that ran green executes the lifecycle DEMO journey
  (deploy/demos/workload-only), not named cmd/baha tests — the test was not among what it executed
  (0 log hits prove this).
⇒ **FALL B: ihn fuehrt NIRGENDWO ein job wirklich aus** (declared surface + green runtime cell exist,
but no runner executes the test by name; the wizard cell where it is scheduled only ever skips it).

## Root cause (reality witnesses)

- `git show 80d4df52` (in this lineage via r1): added `mustHaveRuntimeForStagedCandidate(t)`
  (skip unless `BASEHARBOR_GIT_CANDIDATE_ACCEPTANCE=1`) to
  TestAppEditCommandCompleteProviderEditRunsRealLifecycle and
  TestPrepareStagedCoreGitCandidatePinsCanonicalApplication.
- Reality witness: develop itself carries the same guard (`git grep
  BASEHARBOR_GIT_CANDIDATE_ACCEPTANCE origin/develop` hits both files), and develop's copy of
  TestAppEditCommandCompleteProviderEditRunsRealLifecycle has NO guard call (verified in
  origin/develop:cmd/baha/app_edit_apply_test.go:1186-1188) — the marker was applied to the STAGED
  -CANDIDATE test only. #1614's r1 hop-wave union resolution wrongly kept the guard call on the
  app-edit lifecycle test as well, exposing it to the wizard prefix runner.
- No PR-run of develop has ever executed this test in wizard-app-edit on a daemon host under the
  guard… the hole on develop itself: TestPrepareStagedCoreGitCandidate… skips everywhere (marker
  set by NO runner) — recorded here as a separate observation for the coordinator (out of this
  PR's write-set).

## Fix plan per ruling Fall-B (to execute after the log-grep handoff, minimal, no .github)

1. cmd/baha/app_edit_apply_test.go: remove the wrongly-carried `mustHaveRuntimeForStagedCandidate(t)`
   call from TestAppEditCommandCompleteProviderEditRunsRealLifecycle → test runs (and is required)
   in the wizard-app-edit cell exactly like develop does; real-lifecycle execution stays where the
   lifecycle-capable runner provides DOCKER_HOST.
2. cmd/baha/management_core_git_candidate_test.go: make the guard daemon-aware — run when
   `docker info`/`podman info` answers within a short probe (honoring BASEHARBOR_TEST_RUNTIME),
   skip only when genuinely no runtime exists, keep the marker as an additional always-run path.
   This gives the native executing cells (which set no marker today) a real execution route
   without a unit-host fake pass. Pure removal of the guard is NOT done (ruling forbids).
3. scripts/test_ci_native_gates.py-style coverage: the wizard-app-edit required-run itself
   (run 45124111962 rerun on the new head) is the durable proof that the test now executes; no
   .github change needed — wizard-app-edit-tests is a base validation check already wired to
   cmd/baha paths including app_edit_apply_test.go (base plan selects it).

## cleanliness

- git-only hop + read-only CI/source probes so far; no containers, compose projects, networks,
  volumes or VM work started; no local test suites run (mission: keine lokalen suites).
- `docker ps -a` on this host (pid 4096656): zero containers (header only) before and after; ambient untouched.
- Files created only inside the worktree and this plan-repo evidence directory.

## Evidence-on-origin/main verification (second-to-last actions)

```
<output appended after push>
```

Planning repo remote verified before first evidence commit:
`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` →
`origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

HANDOFF (finding, pre-fix): FALL B — kein hosted-job fuehrt TestAppEditCommandCompleteProviderEditRunsRealLifecycle real aus (log-grep 0 hits in lifecycle/data-cap/core-cap/coreless cells of 45124111962; ci-native-pr-gate.sh has no atomic-lifecycle named-test route); wizard-app-edit job 137524476740 shows it SKIPs. #1614 head 90694e32 (run 45124111962: TP+everything green except that one required-test-skip). Fix per Fall-B plan next.
