# Mission 084 — perses-lifecycle hopf (fix-1)

Lane: mission-084-hopf-lean
Card: 0428-084 / PR #1598, branch lane-0428-084-perses-lifecycle, expected head e866723746a5c5393aba06cd5da8c8b7800788e7

## PLAN

1. Clone baseharbor (blob:none, no-checkout) into /var/tmp/m084-hopf-clone; fetch origin develop + refs/pull/1598/head; checkout -b hopf FETCH_HEAD.
   - Reality check (git ls-remote origin): refs/pull/1598/head = e866723746a5c5393aba06cd5da8c8b7800788e7, exactly the mission's cited head; refs/heads/develop = da76c5cf9c963207038d5599bd130b89ecb1e8a4. (An initial combined fetch left FETCH_HEAD pointing at develop — corrected by fetching the PR ref last; hopf starts at e8667237.)
2. `git merge origin/develop`; resolve expected conflicts in
   - internal/application/manifest_render.go
   - internal/application/manifest_test.go
   - add/add internal/capability/perses.go
   - add/add internal/metrics/perses_contract_test.go
   Rule: keep both sides' rules, never silence a function; for add/add take the more general content and add the special case. If a perses dashboard/lifecycle model decision is unclear from sources: QUESTION to coordinator, not guessing.
3. Verification: bash scripts/source-readability-audit.sh (800-line limit), gofmt -l . (empty), go build ./..., go vet ./..., go test ./internal/capability ./internal/metrics ./internal/application -run Perses -count=1. Outputs into this file.
4. Ancestor check `git merge-base --is-ancestor e866723746a5c5393aba06cd5da8c8b7800788e7 HEAD` (must be 0), then push hopf:refs/heads/lane-0428-084-perses-lifecycle. No force-push.
5. `gh pr ready 1598`; observe the PR run on the new head to terminal (gh pr checks 1598; gh api check-runs). Fill in: executed cells, skipped cells + reason with file:line of the if-condition (ci.yml 514/1137/1160), and 'PR Selected Checks' explicitly.
6. Evidence commit/push to baseharbor-plan main, ls-remote + path-presence witness, cleanliness docker/podman ps -a, END line.

## Coordinator correction (2026-11-19, second instruction)

The first hopf (candidate 831c2bea) is mechanically in order but the exact-head run fails:
- literal failing lines (job logs of run 44499778660):
  - `machine_documentation_test.go:48: unclassified product command: baha app perses disable`
  - `registration_ci_readiness_test.go:82: unclassified command: baha app perses disable`
  - `human_documentation_test.go:107: machine documentation drift in docs/cli/command-index.md`
- The new `baha app perses enable|disable|status|remove` commands have no classification in
  `cmd/baha/machine_coverage.go:21` (`currentCommandCoverage`): a `gap` row triggers the fatal
  at `cmd/baha/machine_documentation_test.go:47-48`; `semantic` requires an existing entry in
  `machine.OperationByID` (same file, lines 50-53, `internal/machine/contract.go`).
- Decision: follow the existing app-command pattern and give every perses command a genuine
  typed operation (`semantic`) in `internal/machine` + MCP registration + shared CLI/MCP
  execution seam, then regenerate `docs/reference/cli-machine-coverage.md`,
  `docs/cli/command-index.md` and `docs/de/cli/command-index.md` via
  `BASEHARBOR_UPDATE_MACHINE_DOCOS=1 go test ./cmd/baha -run TestMachineDocumentation...`.

## Environment-drift control (same host, plain develop)

The three cmd/baha failures of the first full local suite were checked against a pristine
develop clone (/var/tmp/hopf-base-check @ da76c5cf):
`TestPrepareStagedCoreGitCandidatePinsCanonicalApplication` fails IDENTICALLY on plain
develop on this host ("native Git archive failed: signal: killed", 60s kill). The host runs
a rootful Docker daemon and an INACTIVE podman.socket, so `TestRuntimeUpRequiresORASBeforeCoreBootstrap`
and `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` are engine-environment failures on
this coordinator server, not candidate regressions (mission rule: docker/podman tests run only on
the named SSH hosts). The exact-head GitHub CI shards are authoritative and are recorded below.

## Constraints
- No merge, no review, no .github/scripts edits, no rerun/dispatch, no security.go, no new tests, no card status changes, no subagents, only `git add <file>`, all work in /var/tmp, host left clean.
