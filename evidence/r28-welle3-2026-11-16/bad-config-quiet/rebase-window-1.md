# mission-094-rebase-window — rebase-window-1 (base freshness, PR #1666)

Card: t-20261115-bughunt-d28-bad-config-quiet (0428-094), PR #1666.
Content was APPROVED (batch19); this lane only refreshed the base against
develop@1df7c343 under the strict ruleset window rules. No product content
changes were made by this lane.

## PLAN

1. Read mission file; create numbered plan in all three places — DONE (board file `workers/todos/mission-094-rebase-window.md.json`; native todowrite tool not exposed in this session, skipped per mission rule "if unsure, skip leg (0)")
2. Reality sync: ls-remote develop + lane-0428-094-config-fail; PR #1666 state — DONE
3. Worktree setup, base attestation — DONE
4. `git merge origin/develop` (normal merge commit, no rebase, no force) — DONE, conflict-free
5. build / vet / gofmt / affected deployment tests green — DONE
6. Refspec push + ls-remote witness; PR #1666 remains READY — DONE
7. Exact-head pull_request run observed to TERMINAL SUCCESS — DONE
8. This dossier committed and pushed to origin/main — DONE
9. Cleanliness sweep + END post — DONE

## Zone witness (wrong-zone check)

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
    https://github.com/mcpdev80/baseharbor-plan

(Planner repo confirmed = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan, not workers/baseharbor-plan.)

## Reality sync (first action)

Remote truth via ls-remote (2026-11-17):

    1df7c343c334ffb17954a249f69690570e94ee8d  refs/heads/develop
    4f2906c6bf9f1c1e5c95f7b88e79c1aa5e110ecc  refs/heads/lane-0428-094-config-fail

PR #1666 pre-state: `state=OPEN isDraft=false baseRefName=develop headRefOid=4f2906c6b mergeable=MERGEABLE mergeStateStatus=BEHIND` — confirms the mission: content fine, only base freshness missing.

## Base attestation and merge

- Branch cut from: `origin/lane-0428-094-config-fail` @ `4f2906c6bf9f1c1e5c95f7b88e79c1aa5e110ecc` (worktree `/var/tmp/094-rebase-wt`, local temp branch `lane-0428-094-config-fail-rebase`).
- Merged in: `origin/develop` @ `1df7c343c334ffb17954a249f69690570e94ee8d`, plain `git merge --no-ff`, ort strategy, **no conflicts** (no resolution needed; nothing to cite as file:line).
- No rebase, no force-push anywhere (AGENTS §5.2).
- Merge commit: `29a9fceb9003823c3c9e03179dae319b3d05b1fb`.
- Ancestor tests: `git merge-base --is-ancestor 1df7c343... HEAD` → true; `--is-ancestor 4f2906c6b... HEAD` → true.
- `git log --oneline origin/develop..HEAD` after merge:

      29a9fceb9 Merge origin/develop (1df7c343) into lane-0428-094-config-fail for base freshness (PR #1666 window)
      4f2906c6b fix(deployment): end-to-end double-append missing config fails loud (BF-05 r3)
      fe00c7f18 fix(deployment): existing empty config.yaml fails loud (BF-05 r2)
      5b0197a9c fix(deployment): fail loud on corrupt/missing base config (BF-05)

  — exactly the three own candidate commits + the merge commit; no foreign commits carried.
- Content preservation: branch content is `internal/deployment/target.go` + `internal/deployment/config_fail_loud_test.go`; the merge brought develop's changes into all other paths only (diff 4f2906c6b..HEAD touches none of the two candidate files beyond what develop itself carries in unrelated paths).

## Local verification (on merge candidate 29a9fceb9)

- `go build -o /var/tmp/baha-094rb ./cmd/baha` → PASS (exit 0)
- `go vet ./...` → PASS (exit 0)
- `gofmt -l cmd internal` → empty → clean
- `go test ./internal/deployment/...` → `ok github.com/mcpdev80/baseharbor/internal/deployment 82.1s`
- Fail-loud regression set `-run LoadConfig -v`:
  TestLoadConfigFailsLoudOnUnparseableConfig, TestLoadConfigMissingUnderPopulatedRootFailsLoud,
  TestLoadConfigMissingUnderEmptyRootSucceeds, TestLoadConfigExistingEmptyFileFailsLoud,
  TestLoadConfigValidStillLoads, TestLoadConfigEndToEndXDGPath,
  TestLoadConfigDoubleAppendResolvedPathMissingFailsLoud — all PASS.

## Push witness

    $ git push origin HEAD:refs/heads/lane-0428-094-config-fail
       4f2906c6b..29a9fceb9  HEAD -> lane-0428-094-config-fail    (fast-forward, no force)

    $ git ls-remote origin refs/heads/lane-0428-094-config-fail
    29a9fceb9003823c3c9e03179dae319b3d05b1fb  refs/heads/lane-0428-094-config-fail

Single candidate per chain: the merge landed on the existing `lane-0428-094-config-fail`
ref only; the local temp branch name existed solely in this worktree and was never pushed
(no second remote branch created or needed to delete).

## PR state after push (READY preserved)

    state=OPEN  isDraft=false  baseRefName=develop  headRefOid=29a9fceb9
    mergeable=MERGEABLE  mergeStateStatus=CLEAN

No ready/draft toggle was performed (window rule: PR #1666 stays as-is).

## Hostered run (Eigenes-Run-Pflicht §4.6)

- Run: `CI · PR #1666`, databaseId **44013270180**, event=pull_request,
  headSha=29a9fceb9003823c3c9e03179dae319b3d05b1fb (exact candidate head).
- Observed by this lane from start to terminal state via `gh run watch`.
- Terminal: `status=completed conclusion=success`.
- Checks on PR: 19 pass / 0 fail (skipping cells are not selected for this path,
  e.g. the unaffected runtime matrix cells). PR · Selected Checks, PR · Exact
  Candidate, PR · Validation · go-build, PR · Validation · deployment-package-tests,
  Go unit groups, docker lifecycle selected-runtime cell all pass.
- Run URL: https://github.com/mcpdev80/baseharbor/actions/runs/44013270180
- No rerun or cancellation occurred.

## New tests added? CI pickup

None — this lane added no test; it merged develop into an approved candidate.
No `.github/**` file was edited or triggered by this lane (merge carries develop's
workflow state unchanged).

## Scope compliance (GRENZEN)

- No `.github/**` edits, no manual workflow_dispatch, no reruns — merge carried
  develop's workflow files mechanically.
- No merge of the PR itself; no ready-for-review toggle; no force operations.
- No subagents used (§4.8); every step executed in this session.
- Scratch confined to /var/tmp (mission GRENZEN); no containers or compose
  projects started on this host (unit/build checks only).

## repo-rule compliance

- `git ls-remote` only for remote truth; the quarantined
  `workers/baseharbor` checkout was never cited.
- Evidence lives only in baseharbor-plan (this file); nothing written to product repos.
- Base attestation + ancestor test + log-line witness shown above per protocol.

## Cleanliness

- No docker/podman/compose projects were started by this lane (ps witness: none
  started → nothing to bring down; ambient stacks untouched).
- Worktree `/var/tmp/094-rebase-wt` and temp branch removed after push; build
  binary `/var/tmp/baha-094rb` deleted.
- cleanliness: besenrein.

END_DONE mission-094-rebase-window.md: PR #1666 base refreshed on develop@1df7c343, new head 29a9fceb9003823c3c9e03179dae319b3d05b1fb, CI run 44013270180 terminal SUCCESS, PR remains OPEN/READY (mergeStateStatus=CLEAN).
