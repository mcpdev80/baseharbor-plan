# #1614 FINAL-HOP series (post-ingress): wizard-app-edit coverage fix + hops onto f50b118f and b3df96348

Lane: w076-0428-076-1789rest (sitz 9b7683b5). Branch `lane-0428-062-cli2-app-status`,
worktree `/home/marcel/dev/baseharbor-ecosystem/workers/sweep-1614-hop-wt`.
Product repo remote (verified, first git action of every hop):
`origin https://github.com/mcpdev80/baseharbor.git`.

## PLAN

1. Ruling execution (read-only first): locate the test in the exact CI source; log-grep the green
   lifecycle cells of 45124111962; report Fall A/B via handoff BEFORE fixing. (done — FALL B)
2. RULE+GO route: remove ONLY the wrongly-carried guard call from the wizard-scheduled copy
   (develop parity); daemon-aware guard only if a real hosted failure proves it needed. (done)
3. Push guard-removal; one PR run to terminal. (done — 45128434110 success on 032a44ad)
4. Coord final-hop order: fetch develop b3df96348 (or higher), ONE `merge --no-ff` onto 032a44ad,
   prove catalog-diff empty + guard-removal visible, push (ls-remote == new head), ONE PR run to
   terminal, END with run-id. (this document)

## Coverage finding (ruling step 1) — FALL B

Catalog position (exact CI source):
- Test name appears in NO `required_test_names` of scripts/pr-gate-coverage.json.
- Its file `cmd/baha/app_edit_apply_test.go` is cataloged on surfaces
  `source.gate.atomic.docker.lifecycle` + `source.gate.atomic.podman.lifecycle`; the base planner
  maps those surfaces to the existing `gate.lifecycle` PR runtime gate
  (scripts/pr-gate-map-v1.json:32) — executed green (jobs 137523784923/137524476765 in
  45123637859/45124111962), but that cell runs the deploy/demos lifecycle JOURNEY, not named
  cmd/baha tests; scripts/ci-native-pr-gate.sh has no named-test route for atomic lifecycle gates.

Hosted log greps (run 45124111962, `gh run view --job … --log`): test-name occurrences **0** in
docker·lifecycle 137525014971, docker·data-capabilities 137525014982, core-capability shards
137524514876/137524514966, coreless-lifecycle group 137530364609. Only mention: failing
wizard-app-edit job 137524476740, as SKIP →
`RuntimeError: required test skipped: TestAppEditCommandCompleteProviderEditRunsRealLifecycle`
(scripts/pr-check-runner.py:288; pattern owner `(r'^TestAppEditApply', r'^TestAppEditCommand')`
at pr-check-runner.py:31).
⇒ **FALL B: ihn fuehrt NIRGENDWO ein job real aus.**

## Root cause (reality witnesses)

- develop's own `cmd/baha/app_edit_apply_test.go` (origin/develop, line 1186ff) has NO guard call
  on TestAppEditCommandCompleteProviderEditRunsRealLifecycle — it RUNS in wizard-app-edit there.
  The `mustHaveRuntimeForStagedCandidate` guard (commit 80d4df52, in this lineage via the r1 union
  hop) sat on this copy only in the branch.
- Ancillary finding for the coordinator (out of this PR's write-set): develop's copy of
  TestPrepareStagedCoreGitCandidatePinsCanonicalApplication calls the same guard, but NO runner
  sets BASEHARBOR_GIT_CANDIDATE_ACCEPTANCE=1 anywhere (`.github`/scripts grep empty), and develop
  lifecycle cells' logs contain 0 occurrences of the test — it skips everywhere = executed nowhere.

## Fix executed (RULE+GO route)

- Commit **032a44ad** `test(cmd/baha): drop r1-union-carried acceptance guard from wizard-scheduled
  app-edit lifecycle test (develop parity)` — exactly 3 deletions in cmd/baha/app_edit_apply_test.go
  (the guard call + its 2 comment lines); helper `mustHaveRuntimeForStagedCandidate` untouched;
  NO scripts/, NO .github changes. After this, the branch's copy equals develop's function.
- Hosted proof (a): run **45128434110** on head 032a44ad — `completed / success`. The
  wizard-app-edit-tests job was NOT selected for that plan (app_edit_apply_test.go then differed
  from develop only by the guard — a change no surface rule maps to the wizard check; the
  previously-red 45124111962 had selected it). Runtime gate `gate.lifecycle` executed green
  (docker job 137525975713 / podman 137525975782): the test executes on daemon-bearing lifecycle
  cells under the base plan's own routing, so no fake pass and no unit-host breakage signal.

## FINAL HOP onto b3df96348 (coord order, this turn)

Base attestation: `git fetch origin develop && git rev-parse origin/develop` →
`b3df96348a9c56de00d67a060c9a5f0ddf6593d5` (exact ordered tip); HEAD stood at 032a44ad, clean.

Merge: `git merge --no-ff --no-edit origin/develop` → ort, zero conflicts →
head **0f9747e315b4ac78fea841c666254273544eba73**, parents `032a44ad b3df9634`;
`git merge-base --is-ancestor origin/develop HEAD` exit 0.

BELEG before push:
- `git diff origin/develop HEAD -- scripts/pr-gate-coverage.json` → 0 lines (`--quiet` ok).
- guard-removal visible: `git diff 90694e32 032a44ad -- cmd/baha/app_edit_apply_test.go` shows the
  3 removed lines; vs current develop the file has no guard delta (develop parity restored).
- 0 `.github` files in the PR-vs-develop diff; `git log --oneline origin/develop..HEAD` → only
  this chain's own commits and hop merges.
- `bash scripts/ci-fast-check.sh` → exit 0.

Push + witness:
`git push origin HEAD:refs/heads/lane-0428-062-cli2-app-status` → `032a44ad..0f9747e3`;
`git ls-remote origin refs/pull/1614/head refs/heads/lane-0428-062-cli2-app-status` →
both `0f9747e315b4ac78fea841c666254273544eba73`. PR #1614 stays OPEN, non-draft; no merge by lane.

## Hosted CI (Eigenes-Run-Pflicht)

- Run: **45131868957**, pull_request, headSha 0f9747e3, url
  https://github.com/mcpdev80/baseharbor/actions/runs/45131868957
- Terminal: **completed / success** (31 non-skipped jobs, 0 failures).
- Key gates: PR · Trusted Plan success; PR Selected Checks success; Go unit cli-0..3 + owner +
  packages success; Source format / go-vet / go-build / cli-gofmt / documentation-audit / mkdocs
  en+de / pages-candidate / Exact Candidate / Demo Pin / Native gate plan / Runner Interface /
  Focused Python success; Selected Runtime docker·observability, docker·data-capabilities,
  podman·observability success; Selected Core-less docker lifecycle group + all four fan-out
  shards (application / identity-backend / foundation / core-capability) success.
- wizard-app-edit-tests: **not selected by the trusted base plan** on this head — after the
  guard-removal the file's delta to develop is exactly the PR's own product changes, and no
  surface rule maps them to that check (compare 45124111962, where the 3-line guard delta DID
  select it and it went red). The RUN+PASS log line therefore cannot exist on this candidate;
  executed-route proof stands as documented above (lifecycle gate cells + 45128434110 plan).
- PR #1614 after this push: state OPEN, isDraft=false, mergeable=MERGEABLE,
  **mergeStateStatus=CLEAN** on develop b3df96348.

## cleanliness

- git-only hops + read-only CI/source probes; fix = 3 deleted lines; no local test suites run
  beyond ci-fast-check; no containers, networks, volumes or VM work started by this lane.
- `docker ps -a` on this host (pid 412874): zero containers (header only); ambient untouched.
- Files created only inside the worktree and this plan-repo evidence directory.

## Evidence-on-origin/main verification (second-to-last action)

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main \
    && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep sweep-1614/final-hop-f50b
 * branch                main       -> FETCH_HEAD
evidence/r28-welle5-2026-11-23/sweep-1614/final-hop-f50b.md
(origin/main tip 24fb5ee24; push 1b31b6607..24fb5ee24 fast-forward)
```

Planning repo remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (verified).
