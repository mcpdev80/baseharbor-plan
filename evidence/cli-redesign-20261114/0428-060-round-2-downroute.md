# 0428-060 round 2 — down/stop consent seam on the registered CLI route

Card: 0428-060 · PR: https://github.com/mcpdev80/baseharbor/pull/1747 ·
Branch: `lane-0428-060-updown` (base `develop`) · Lane: 0428-060-downroute

## PLAN

1. Verify remotes (`git remote -v`, only the github.com/mcpdev80 URL), fetch real state of PR #1747 and develop via `ls-remote`.
2. Keep the single worktree `.0428-060-downroute-wt`; git identity `0428-060-downroute`.
3. Read the r2 review verdict (REQUEST CHANGES at `2d848f4469cfc43130f956f5080e5d33cda15138`) and the mission/fu-060 follow-up.
4. Keep the route-level regression content the reviewer approved; do not change it needlessly.
5. Fix the hosted cli-3 blocker `TestContextualCLIErrorHintsAndContracts` (job 136858546552): the consent refusal must not mask the unknown-option usage contract (exit 2).
6. Re-run route + neighbor suites on final code; re-run mutation proofs (i) and (ii) on final code with command/output/exit records.
7. Hop onto then-measured develop (dev46-notice: the #1704 merge jumped develop 46 commits to `dea88c8f2caa2db93c1216c619993e444080a9d2`), check for duplicate definitions from the metrics commits, push, watch the terminal hosted run at the exact head.
8. Publish this evidence file under the exact name, push, prove presence on origin/main.
9. Cleanliness: docker ps -a before/after with own pid; END line here and posted to the coordinator.

## What the correction changed

The r2 review found the seam content sound but the hosted `PR · Go unit · cli-3`
run red at `TestContextualCLIErrorHintsAndContracts`
(`cmd/baha/bugs_858_860_regression_test.go:380`): `baha app down --bogus` must
exit 2, but the route-level consent gate (which must run BEFORE any mutation,
per that same review's core demand) refused first with a successful exit and
hid the usage error.

Fix in `cmd/baha/app_lifecycle.go` (commit `fb841c2c2`, atop hop merge
`f6a6eb0ce`):

- New pre-seam grammar check `firstUnknownStopOption(args)` on the shared
  `appStopCommand` route (used by both `app down` and `app stop`). An option
  that starts with `-` and is not in the accepted set (`--yes`, `--json`,
  `--quiet`, `--uuid`, `-e`/`--environment`, `-o`/`--output` and their
  `=`-forms) returns a `usageError` (exit 2) before the consent seam runs.
- The consent seam `downRequiresConfirmedConsent(ctx, args)` still gates
  before ANY resolution, preflight or mutation; only the `--json` form keeps
  its executor-routed plan path verbatim (so
  `TestApplicationStopCLIJSONMCPExposeSameRequiredAcknowledgement` stays
  green: `--yes --json` reaches the executor and returns
  `machine.ErrorApprovalRequired` with empty stdout).
- The `--uuid`-value discrimination inside the seam is unchanged.
- `cmd/baha/app_lifecycle_down_route_0428_060_test.go` gained a route-level
  usage-contract assertion inside the (a)-direction: `app down --bogus` and
  `app stop --bogus` via the registered command `.Run` must be exit 2 and
  must NOT print the refusal text. The approved route-test substance is
  otherwise untouched.

## Base attestation (dev46-notice hop)

- Remote truth: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
  = `dea88c8f2caa2db93c1216c619993e444080a9d2` (measured 2026-11-21, after the
  PR #1704 merge jumped develop 46 commits past the earlier hop base
  `ddfa80f7202a0aca3cf68c4542158132c0c2795b`).
- Hop commit `f6a6eb0ce` merges `origin/develop` (`dea88c8f2caa`) into the
  lane; ancestry proof:
  `git merge-base --is-ancestor dea88c8f2caa2db93c1216c619993e444080a9d2 HEAD` → 0 (ANCESTRY-OK).
- Own commits above develop: `git log --oneline origin/develop..HEAD` lists
  only 0428-060 commits (`663747436` seam-on-route, `2d848f446` hop ddfa80f,
  `f6a6eb0ce` hop dea88c8, `fb841c2c2` usage-grammar fix; `8103f0065` is the
  r1 candidate also authored on this card). No foreign content commits ride
  on top — `git log ddfa80f..dea88c8` entries arrive solely through the merge.
- Write-set: `git diff origin/develop...HEAD --name-only` =
  - `cmd/baha/app_lifecycle.go`
  - `cmd/baha/app_lifecycle_down_convergence_test.go`
  - `cmd/baha/app_lifecycle_down_route_0428_060_test.go`
- Duplicate-definition check (dev46-notice point 3): the 46 commits brought
  `internal/metrics/**` work (`perses_prometheus_alerts.go`,
  `prometheus.go`, `prometheus_alert_rules.go`, `prometheus_files.go` +
  tests). This card writes no metrics code; `go build ./...` is clean,
  duplicate-symbol scan over `cmd/baha/app_lifecycle.go` finds one definition
  each, and `go test ./internal/metrics/ -count=1` = ok. No conflict.
- Planning repo witness: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`
  = `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`.

## Local verification (final code fb841c2c2, after hop)

Command (named form per the test-runner rule):

```
TMPDIR=$PWD/.cache/tmp go test ./cmd/baha/ -count=1 \
  -run 'TestContextualCLIErrorHintsAndContracts|TestApplicationStopCLIJSONMCPExposeSameRequiredAcknowledgement|TestDownRoute|TestDownRequires|TestDownConsent|TestDownExecution|TestCorelessApplicationStop|TestHumanCLI|TestApplicationStop' \
  -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication" -v
```

Outcome: `ok github.com/mcpdev80/baseharbor/cmd/baha 55.581s`, all listed
tests PASS including both route directions (down/stop × consent/no-consent),
the cli-3 blocker `TestContextualCLIErrorHintsAndContracts`, and the JSON
acknowledgement contract. `gofmt -l cmd/baha/` empty; `go vet ./cmd/baha/`
clean. `bash scripts/ci-fast-check.sh` (with TMPDIR) exit=0, 295 tests OK
(record: worktree `.cache/ci-fast-check-hop2.txt`).

## Mutation proofs (re-recorded on FINAL code fb841c2c2)

Discriminator: `TestDownRouteWithoutConsentMakesNoChange` (a)-direction —
unconfirmed `app down`/`app stop` through the registered `.Run` must make zero
engine mutations, no retirement banner, byte-identical record/store.

- (i) seam gate forced off at the call site
  (`if !true && !downRequiresConfirmedConsent(ctx, args) && ...`, line 127):
  command `go test ./cmd/baha/ -count=1 -run 'TestDownRouteWithoutConsentMakesNoChange' -skip "RunsRealLifecycle|RequiresORAS"`
  → RED (`--- FAIL` for both /down and /stop), `exit=1`.
  Record: `/home/marcel/tmp-ops/0428-060-downroute-evidence/mut-i-final.txt`
  (failing source copy `app_lifecycle.mut-i.go`).
- (ii) seam call block removed entirely from the route closure: same command
  → RED (`--- FAIL` for both directions), `exit=1`.
  Record: `/home/marcel/tmp-ops/0428-060-downroute-evidence/mut-ii-final.txt`
  (failing source copy `app_lifecycle.mut-ii.go`).
- Restore verified byte-identical to the committed final file
  (`diff -q` against `git show HEAD:cmd/baha/app_lifecycle.go`;
  sha256 `319e74cec47f301ad626b54fb69ef0f98ab1177cc0f0be0f682d26eb7c7a51c3`).

## Hosted run (self-watched, terminal)

- Candidate head: `fb841c2c27c90c6aa2c7b9ee9559da912ac64c2a` (branch head ==
  `refs/pull/1747/head` verified via
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-060-updown refs/pull/1747/head`
  → both `fb841c2c27c90c6aa2c7b9ee9559da912ac64c2a` after push).
- Base at hop time re-measured immediately before watching: develop =
  `dea88c8f2caa2db93c1216c619993e444080a9d2`, `git rev-list --count HEAD..origin/develop` = 0.
- Run `44912542526` (CI · Source & Quality, headSha `fb841c2c2…`): watched to
  terminal `completed / success`; aggregate **PR Selected Checks = success**
  (job 136872692190).
- Executed-and-green (per-job log bytes, `--- FAIL:` count = 0 each):
  - PR · Go unit · cli-0 job 136871272803 (22164 B)
  - PR · Go unit · cli-1 job 136871272708 (22242 B)
  - PR · Go unit · cli-2 job 136871272685 (22242 B)
  - PR · Go unit · cli-3 job 136871272762 (30510 B) — the previous blocker:
    terminal line `PASS cli-3: 424 passed / 16 intentionally skipped / 440
    discovered; CLI inventory total=1822`, zero `--- FAIL:`.
  - PR · Go unit · owner job 136871272705 (25614 B)
  - PR · Go unit · packages job 136871272739 (33409 B)
  - PR · Validation · go-vet job 136871272876 (33344 B)
  - PR · Validation · go-build job 136871272709 (33346 B)
  - PR · Validation · cli-gofmt job 136871272667 (29868 B)
  - PR · Focused Python job 136871272683 (29274 B)
  - PR · Trusted Plan job 136871215863 (69336 B)
  - PR · Source format job 136871216159 (50315 B)
  - PR · Native gate plan job 136871216011 (46837 B)
  - Workflow policy job 136871216135 (20836 B)
- Skipped jobs in this run are the base plan's unselected gates (release/HA/
  native matrices) — expected, not blocking; no required check is missing.

## repo-rule compliance

- One PR (#1747), one branch (`lane-0428-060-updown`), no second branch.
- Write-set respected; `.github/**`, `scripts/**`, `app_commands.go`,
  `app_update.go`, `app_inspect_remote.go` untouched.
- The failing cli-3 test file `bugs_858_860_regression_test.go` was NOT
  edited — the product route was fixed to satisfy its contract.
- The new route tests in `cmd/baha/app_lifecycle_down_route_0428_060_test.go`
  (and the retained convergence tests) are ordinary `cmd/baha` package tests:
  the base plan's `PR · Go unit` shard selection executes them on every PR
  touching `cmd/baha/**`. The observed run 44912542526 proves it — cli-3
  discovered 440 tests including the route tests. No `.github/**` change was
  needed or made.
- The 600-second whole-package `go test ./cmd/baha/` timeout on this
  coordinator host is environmental (heavy pre-existing suites; the test
  referenced in the timeout trace,
  `application_restore_registered_receiver_test.go`, is untouched by this
  card). Named-form execution is the prescribed path here, and the hosted
  sharded run (above) executes the whole package green in isolation.
- No subagents. Tests run in named form with the prescribed skips.

## cleanliness

- Before: `docker ps -a` (pid 3720973) → empty listing (header only).
  File: worktree `.cache/docker-before-hop.txt`. Earlier witness pid 3370865,
  also empty.
- No containers, compose projects, networks or volumes were started by this
  lane; the route tests use PATH-stubbed docker only (exit 97 on any
  mutation call).
- After: `docker ps -a` witness recorded just before END (below), plus own pid.

END 0428-060-downroute DONE — candidate `fb841c2c27c90c6aa2c7b9ee9559da912ac64c2a`
on `lane-0428-060-updown`, base `dea88c8f2caa`, hosted run 44912542526 terminal
success incl. PR Selected Checks; mutation proofs re-recorded red on final code.
