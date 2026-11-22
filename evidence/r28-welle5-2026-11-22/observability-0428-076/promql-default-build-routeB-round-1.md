# 0428-076 / #1597 promql-ci-capture follow-up — ROUTE (b) DONE: dead tagged file removed, default-build selector coverage in hosted CI

lane: w21-pr1702-0428-142-compat
session: 0847d100
card: 0428-076 follow-up — #1597 CI-Aufnahmepflicht for the promqlparser-tagged test (route b)
candidate: 1d67c5676059795eceef9b03950a7a70dff60bb8 (single hop commit, only commit on develop head)
base develop SHA: 66ce00557ef44acc0ca2ec4c4f7173357af6e2f7
PR #1789: https://github.com/mcpdev80/baseharbor/pull/1789 (draft, base develop, head codex/0428-076-promql-ci-capture)
hosted CI run: 45074794402 (head 1d67c5676, conclusion success)
status: END_DONE

## PLAN

1. Read mission m_0847_promqlB.md.g; verify real remote (origin + lane-origin = github.com/mcpdev80), develop head 66ce00557.
2. Confirm the §5.3 hole: tagged witness imports github.com/prometheus/prometheus/promql/parser absent from go.mod -> cannot compile; default-build assertValidPromQL + TestPersesInvalidTrailingMatcherIsRejected already cover selector-validity/malformed rejection with existing deps.
3. Delete the dead tagged file + remove its stale catalog entries from scripts/pr-gate-coverage.json and scripts/test_pr_native_gate_plan.py (all Lane-Write-Set: *_test.go + scripts/**). Verify JSON + catalog python test + no forbidden path.
4. Create additive hop branch codex/0428-076-promql-ci-capture off origin/develop 66ce00557; single commit of exactly the 3 changed files; verify default-build metrics package compiles + TestPersesInvalidTrailingMatcherIsRejected passes (sanctioned form).
5. Push hop, ls-remote pull/1789/head witness; open PR #1789 (draft) referencing #1597 / 0428-076.
6. Hosted CI: confirm Go unit packages job-log shows default-build selector/malformed assertions EXECUTED+PASSED.
7. Publish akte to baseharbor-plan origin/main, verify path present, then post END_DONE to 9142ab1f.

## Realität / base attestation

- Real remote: `origin` = https://github.com/mcpdev80/baseharbor.git, `lane-origin` = same (both github.com/mcpdev80, per REMOTE GUARD). Confirmed first git action.
- develop head (ls-remote): 66ce00557ef44acc0ca2ec4c4f7173357af6e2f7. This SHA is the ancestor of commit 1d67c5676 (verified: `git merge-base --is-ancestor 66ce00557... HEAD` => YES).
- `git log --oneline origin/develop..HEAD` lists ONLY my one commit 1d67c5676 — no foreign candidate carried on top.
- `git diff origin/develop...HEAD --name-only` = internal/metrics/perses_dashboards_promql_test.go (deleted) + scripts/pr-gate-coverage.json + scripts/test_pr_native_gate_plan.py (both edited).
- No go.mod/go.sum, no .github, no product code touched (Lane-Write-Set only).

## BEFUND — §5.3 CI-Aufnahmepflicht-Loch (confirmed, same as prior round-1 akte)

The promqlparser-tagged test exists on develop and is never selected/executed in hosted CI:

- internal/metrics/perses_dashboards_promql_test.go:
  - line 1: //go:build promqlparser
  - line 47: func TestPersesPrometheusParserRejectsMalformedSelectors — parses emitted Prometheus selectors with the real parser.ParseExpr and asserts a trailing-token selector and a missing-brace selector are rejected.
  - line 17: imports parser "github.com/prometheus/prometheus/promql/parser".
  - the file's own comment claims a go.mod direct dependency on github.com/prometheus/prometheus; that dependency does NOT exist.
- go.mod / go.sum on develop 66ce00557 contain NO github.com/prometheus/prometheus (no direct dep, no transitive pull, no replace directive).
- go build -tags promqlparser ./internal/metrics fails:
  internal/metrics/perses_dashboards_promql_test.go:17:2: no required module provides package github.com/prometheus/prometheus/promql/parser.

So the tagged witness neither compiles nor runs under -tags promqlparser in any hosted CI job. This is the missing Qualifying evidence.

## ROUTE (b) — chosen and executed (coordinator-authorized, no new dependency)

The complete fix needs a go.mod/go.sum dependency add, which is OUTSIDE this Lane-Write-Set (mission: *_test.go + scripts/** only, no go.mod/go.sum, no .github, no product). Route (b) instead closes the §5.3 hole by removing the dead tagged file so there is no CI-blind file, while keeping selector-validity + malformed-query rejection in the DEFAULT build (existing deps only). This is within the Lane-Write-Set and needs no dependency decision.

Changes (single commit 1d67c5676):

1. DELETED internal/metrics/perses_dashboards_promql_test.go (56 deletions). It referenced a non-existent dependency and ran nowhere.
2. scripts/pr-gate-coverage.json: removed stale entry source.internal.metrics.perses.dashboards.promql.test.go (the path now dangles otherwise). JSON still valid; 214 components; no dangling promql path.
3. scripts/test_pr_native_gate_plan.py: removed 'internal/metrics/perses_dashboards_promql_test.go' from the native-gate path tuple. Catalog regression test (13 tests) still passes.

Selector-validity + malformed-query rejection remain covered by the existing default-build assertValidPromQL heuristic and TestPersesInvalidTrailingMatcherIsRejected (internal/metrics/perses_dashboards_test.go, existing deps only, no prometheus import). Verified locally:

- go build ./internal/metrics/ (default build, no tag) => BUILD OK
- go test ./internal/metrics/ -run '^TestPersesInvalidTrailingMatcherIsRejected$' -count=1 => ok 0.004s

What was NOT done (out of scope / owner decisions, documented, not performed):

- No go.mod/go.sum change (adding github.com/prometheus/prometheus is a dep-ownership decision, outside this write-set).
- No -tags promqlparser added to scripts/pr-go-unit-shard.py (the file cannot compile; adding the tag would select a non-compiling test).
- No .github/workflows edit, no product change.

## CI-Aufnahmepflicht proof — hosted CI

- Run 45074794402 (head 1d67c5676, conclusion success, https://github.com/mcpdev80/baseharbor/actions/runs/45074794402).
- Job "PR · Draft Go · packages" (job id 137369521174, conclusion success).
- Job log shows the packages() invocation: python3 scripts/pr-go-unit-shard.py --mode packages, which runs `go test -p 1 "${owned[@]}" -count=1` in the DEFAULT build (grep -c "promqlparser" in job log = 0; the dead tagged path never ran).
- internal/metrics compiled and passed: "ok github.com/mcpdev80/baseharbor/internal/metrics 0.501s".
- Therefore selector-validity + malformed rejection (assertValidPromQL / TestPersesInvalidTrailingMatcherIsRejected) executed+passed in the default-build Go unit packages job. CI-Aufnahmepflicht satisfied: a real hosted CI job selects, executes and passes the selector-validity witness under the default build.
- selector validity im default-build CI ausgefuehrt: JA. tagged tote datei entfernt: JA.
- gofmt -l on changed Go files = clean; scripts/source-readability-audit.sh = PASS; scripts/ci-workflow-policy.sh = PASS (20 approved workflow files, catalog consistency skipped — event has no PR/push comparison path in the tool run).

## Evidence witnesses

- ls-remote refs/heads/codex/0428-076-promql-ci-capture = 1d67c5676059795eceef9b03950a7a70dff60bb8
- ls-remote refs/pull/1789/head = 1d67c5676059795eceef9b03950a7a70dff60bb8 (= commit, = branch head)
- CI run 45074794402 databaseId=45074794402, head_sha 1d67c5676, conclusion success, status completed.

## END lane

END_DONE — #1597 / card 0428-076 promql-ci-capture follow-up route (b) is complete. The §5.3 hole (dead promqlparser-tagged witness compiled by no CI job) is closed by deleting the dead tagged file and removing its stale catalog entries, keeping selector-validity + malformed rejection in the default build with existing deps only. Commit 1d67c5676 (single hop, only commit on develop 66ce00557 head), PR #1789 (draft, base develop). Hosted CI run 45074794402 (head 1d67c5676) SUCCESS: Go unit packages ran the metrics package in the default build (no -tags promqlparser), internal/metrics ok 0.501s, 0 promqlparser hits. gofmt/readability/workflow-policy all pass. No go.mod/go.sum, no .github, no product change, no merge (owner/Codex review pending). go.mod/go.sum dependency gap that route (b) deliberately avoids remains an owner/dep decision, documented here.

## cleanliness

- Worktree: /home/marcel/dev/baseharbor-ecosystem/worktrees/0428-076-hop1597 (existing dedicated worktree; no scratch in ecosystem root).
- Stray untracked binary `baha` (built during local verification) removed before END.
- No go.mod/go.sum/product/.github change (scoped to *_test.go + scripts/**).
- No docker/podman compose projects started (git/gh read-only verification of hosted CI; no containers on the coordinator host).
- git ps -a witness: none started (no docker/podman daemon contact).
- CI job-log fetched via gh api to /tmp/opencode/pkg-logs.txt (temporary, outside ecosystem root).
