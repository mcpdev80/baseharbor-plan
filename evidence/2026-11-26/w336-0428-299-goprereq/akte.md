# w336-0428-299-goprereq akte — t-20261125-hunt33-go-runtime-prereq (0428-299)

## Visible Ansatz Block (visible-ansatz-block required, owner directive 2026-11-26)

- Card frontmatter owner VERBATIM (fetched from origin/main at runtime): `owner: ""` (unassigned in plan; mission assigns lane `w336-0428-299-goprereq`).
- Git identity used: `user.name=w336-0428-299-goprereq`, `user.email=w336-0428-299-goprereq@baseharbor.local`.
- Literal commit invocation: `git -c user.name=w336-0428-299-goprereq -c user.email=w336-0428-299-goprereq@baseharbor.local commit -m "..."`.
- Pre-push author gate line: `git -c user.name=w336-0428-299-goprereq -c user.email=w336-0428-299-goprereq@baseharbor.local show -s --format='%h an=%an cn=%cn' HEAD` must equal `34c9d7bd ... an=w336-0428-299-goprereq cn=w336-0428-299-goprereq`.

## Reality witnesses

- Planning repo is /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ONLY (verify): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` -> origin https://github.com/mcpdev80/baseharbor-plan.git (push). Plan work committed via isolated detached worktree, pushed to refs/heads/w336-0428-299-goprereq.
- Product remote (first git action): `git remote -v` in /var/tmp/w336-0428-299-goprereq-clone -> origin https://github.com/mcpdev80/baseharbor.git (push). Used ONLY this github.com/mcpdev80 remote.
- Base attestation (develop head, ls-remote): `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 refs/heads/develop`. Branch cut at exactly this SHA. `git merge-base --is-ancestor origin/develop HEAD` -> YES.
- /var/tmp worktree (mission-ordered): /var/tmp/w336-0428-299-goprereq-clone, clone of https://github.com/mcpdev80/baseharbor.git on develop at 5a37ddbd9a.
- Candidate branch ls-remote proof: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/w336-0428-299-goprereq` -> 34c9d7bdb995ee7cbefb70e4171eb247ad37f8f4.
- Plan worktree origin/main ls-remote proof: `git ls-remote origin refs/heads/main` -> 0e9c89b41790cfa0f68b1ad4eab1254e84197e9f (before the branch commit).

## Fund (hunt H-V33)

On non-linux/amd64 Targets the lifecycle cross-process lock probe falls back to `go build` in `internal/stableid/lock_probe.go::runToolchainProbe`. When the Go toolchain is absent from PATH, `AcquireLifecycleLock` (via `lockNamed` -> `lockProbeRun` -> `runToolchainProbe`) failed with a raw `exec: "go": executable file not found in $PATH`. That does not document the Go toolchain as a runtime prerequisite and leaves the caller guessing which binary is missing (fail-closed, but unactionable).

## Contract (from mission + task Task section + baseharbor/AGENTS.md)

Smallest sufficient; fail-closed error message when go absent; document go as prerequisite. NO consent/auth change. Stay out of cmd/baha/ci_integration_operator_enabled.go + internal/metrics/.

## Changes (own commits only on develop base)

- `git log --oneline origin/develop..HEAD` (candidate branch):
  - `34c9d7bd docs(coverage): catalog internal/stableid sources for gate resolution (0428-299 hunt33)`
  - `4919ef85 fix(stableid): document Go toolchain as lock-probe prerequisite (0428-299 hunt33)`
- `git diff origin/develop...HEAD --name-only`:
  - internal/stableid/lock_probe.go
  - internal/stableid/lock_probe_platform_test.go
  - scripts/pr-gate-coverage.json

### internal/stableid/lock_probe.go
- New sentinel `errGoToolchainMissing`: "Go toolchain is required to run the cross-process lock probe on this platform: install a Go 1.25+ toolchain on PATH or use a Linux/AMD64 Target (the embedded probe binary needs no toolchain)".
- Extract build step into `runToolchainBuild(build *exec.Cmd) error`; wrapped by new `runToolchainBuildFunc` package var test seam (production never sets it).
- In `runToolchainProbe`, on build error: `if execErr, ok := err.(*exec.Error); ok && execErr.Err == exec.ErrNotFound { return false, errGoToolchainMissing }`, else keep original `fmt.Errorf("build lock probe: %w", err)`.

### internal/stableid/lock_probe_platform_test.go (new, package-discovered)
- `TestToolchainProbeReportsGoPrerequisiteWhenGoAbsent`: injects `&exec.Error{Err: exec.ErrNotFound}` into the seam, asserts returned error documents "Go toolchain".
- `TestToolchainProbePreservesNonMissingBuildFailure`: injects an unrelated error, asserts pass-through unchanged.

### scripts/pr-gate-coverage.json
- Added `source.internal_stableid_lock_probe_go` and `source.internal_stableid_lock_probe_platform_test_go` components with surfaces `source.gate.atomic.docker.data.capabilities`, `source.gate.atomic.podman.data.capabilities` (mirrors sibling internal/operatorauth entries). This closes the "uncataloged source change" the trusted gate-plan rejects locally; no CI scope changed.

## Local pre-checks (host, NON-qualifying per CI policy — no local test execution of product unit suites)

- `go build ./...` -> exit 0.
- `go vet ./internal/stableid/...` -> exit 0.
- `gofmt -l internal/stableid/lock_probe.go internal/stableid/lock_probe_platform_test.go` -> clean (no output).
- New cells (named form, heavy-lifecycle skips): `go test ./internal/stableid/ -count=1 -run 'TestToolchainProbeReportsGoPrerequisiteWhenGoAbsent|TestToolchainProbePreservesNonMissingBuildFailure' -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication'` -> PASS both.
- Full stableid package: `go test ./internal/stableid/ -count=1 -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication'` -> ok 0.099s.
- Python: `python3 -m unittest scripts.test_pr_gate_coverage` -> 58 OK; `scripts.test_pr_gate_plan` -> 195 + 69 OK.

## CI routing (proven locally, not claimed)

- `scripts/pr-gate-plan.py --diff` (GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop) -> coverage_status=resolved, unresolved_coverage=[], area=authority-package (with candidate's own catalog row).
- Selected required_validation_checks: authority-package-tests (`go test ./internal/stableid`), ci-executor-tests, ci-policy, cli-build, cli-guided-tests, cli-vet, pr-planner-tests, receipt-execution-tests. Native gate `atomic/docker/data-capabilities` also selected.
- Test binding: normal (auto-discovered) — no REQUIRED_CLIENT_TESTS / new check catalog needed.

## HOLD — base-catalog gap (fourth instance, routed to Codex disposition)

- HOLD #1863 CANDIDATE SIDE (Owner-verified 2026-11-26): candidate head 34c9d7bd fails because the TRUSTED-BASE catalog has no owner for `internal/stableid/lock_probe.go` + `lock_probe_platform_test.go`. Candidate-side catalog rows cannot fix this (#1860/#1861/#1862 precedent). Cataloging belongs in develop (the frozen controller reads develop's `scripts/pr-gate-coverage.json`), which is outside this card's write-set.
- Root cause in CI: `.github/workflows/ci.yml` line 862-865 sets `controller=$effective_base` when `85965486` is an ancestor of the effective base; for a develop-based PR the effective base is develop and the planner reads develop's frozen `pr-gate-coverage.json` (never the candidate's). Line 867-868 copies `pr-gate-coverage.json` from the controller.
- develop catalog confirmed still lacking stableid (304 components, 0 stableid) at develop 5a37ddbd (verified twice, including a fresh raw fetch from develop).

### Run A (first attempt)
- Hosted CI run **45844485360** on head 34c9d7bd.
- Job `PR · Trusted Plan` FAILURE.
- Uncataloged-source error line (verbatim from job logs):
  `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/stableid/lock_probe.go (id source.internal_stableid_lock_probe_go): add this source with its surfaces to scripts/pr-gate-coverage.json, e.g. {"id": "source.internal_stableid_lock_probe_go", "path": "internal/stableid/lock_probe.go", "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]}; internal/stableid/lock_probe_platform_test.go (id source.internal_stableid_lock_probe_platform_test_go): add this source with its surfaces to scripts/pr-gate-coverage.json, e.g. {"id": "source.internal_stableid_lock_probe_platform_test_go", "path": "internal/stableid/lock_probe_platform_test.go", "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]}`
- Details: https://github.com/mcpdev80/baseharbor/actions/runs/45844485360

### Run B (re-verify, fresh base checkout at 5a37ddbd)
- Hosted CI run **45844581442** on head 34c9d7bd.
- Same `PR · Trusted Plan` FAILURE, same uncataloged-source ValueError on both stableid paths.
- Details: https://github.com/mcpdev80/baseharbor/actions/runs/45844581442

### Precedent chain
- #1860, #1861, #1862: earlier candidates that failed on the identical base-catalog gap (candidate-side catalog rows cannot resolve a frozen trusted-base owner). This is the fourth instance.

## Action taken

- Held branch; candidate PR #1863 left OPEN (reopened after an accidental close during the HOLD window).
- No further catalog rows pushed (would be a fifth instance).
- Card stays open until it goes green via the baseline landing + rerun.
- Meanwhile: keep working any other 0428-299 contract items that do NOT touch pr-gate-coverage.json.

## PR

- Number: 1863. URL: https://github.com/mcpdev80/baseharbor/pull/1863. base: develop. headRefOid: 34c9d7bdb995ee7cbefb70e4171eb247ad37f8f4 (matches pushed branch). state: OPEN. isDraft: false.

## END lane status

- w336-0428-299-goprereq: HOLD. BLOCKED-BASE-CATALOG (fourth instance, routed to Codex disposition). Candidate PR #1863 OPEN. No card creation, no merges, no further candidate pushes.
