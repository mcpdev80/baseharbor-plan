# 0427-034-maintenance-client — Evidence round 1 (t-20261018-r27-maintenance-client)

Worker lane `0427-maintenance-client`. Coordinator session `594fd2f5-4e80-43b6-9841-92879146a85e`.
Repository `mcpdev80/baseharbor`, branch `lane/0427-maintenance-client-wt`, PR #1428 against `develop`.

## PLAN

1. Read mission and task card verbatim; capture scope, write-set, stop criteria.
2. Confirm the published claim for this lane before any edit.
3. Establish base: fetch origin/develop, attest the exact base SHA, prove ancestorship, show only own commits.
4. Create the isolated worktree and single candidate branch; survey existing lifecycle, authority and remote-routing owners.
5. Implement the maintenance-client routing and the durable maintenance window inside the card write-set.
6. Add bounded tests: behavior tests plus causal mutants that require each guard to be load-bearing.
7. Identify the CI job and trigger that executes the new tests; report any `.github/**` need as a finding.
8. Local checks: `go build`, `go vet`, `gofmt`, focused `go test` on the affected packages.
9. Commit, push the branch, open the PR against `develop` with ancestor and log witnesses.
10. Observe the hosted CI run to its terminal state and record run IDs and outcomes.
11. Write this evidence, commit and verify it is present on `origin/main`.
12. Confirm no compose/docker project was started and post the END handoff.

## Reality witnesses

- Planning repo (authoritative): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, remote `https://github.com/mcpdev80/baseharbor-plan.git`. The `workers/baseharbor-plan` path was not touched.
- Card state at start: `kanban_status: active`, `owner: lane-0427-maintenance-client` on `origin/main` (planning commit `da08b5d7`). `scripts/plan.py claim` therefore refused a re-claim; the claim precondition is satisfied by the published claim, not by a second claim commit.
- Product remote truth when the candidate was cut: `git ls-remote origin refs/heads/develop` = `c8a79faff91cd870ac3904a2a392922a24cc7e13`.
- Worktree: `/tmp/opencode/0427-maintenance-client-wt`, branch `lane/0427-maintenance-client-wt`, cut directly from the attested base.
- Round-2 drift repair (Coordinator correction 2026-11-07): develop had advanced to `812c99c88` (PR #1383 merged) and was no longer an ancestor of the then-head `2e371f5fc`. After `git fetch origin develop`, `git rebase origin/develop` produced the candidate `d4d0f77c0cf0db675b603daaf22ea859fac4290a`; `git merge-base --is-ancestor 812c99c88 HEAD` now succeeds and `git merge-base HEAD origin/develop` = `812c99c88`.
- Ancestor proof (candidate): `git merge-base --is-ancestor 812c99c8873df400348fbc8cc9be5e650b8966c4 HEAD` succeeds.
- Delta against develop is only this lane's maintenance files: `git diff --name-only origin/develop...HEAD`
  lists exactly the nine files below, and the hosted PR file list confirms it independently
  (`GET /repos/mcpdev80/baseharbor/pulls/1428/files` → the same nine paths). The three
  #110/#1383-owned files (`app_repository_integration_test.go`, `app_workload_integration_test.go`,
  `repository_runtime_fixture_test.go`) were never in this lane's diff; their last commit on develop
  is `b11eec12f` (#1383) and this lane contains no change to them, so nothing had to be reverted.
- Commits above the base are only this lane's own: `git log --format='%h %an %s' origin/develop..HEAD` lists exactly the three maintenance commits (`feat`, `docs`, `test`) above.

## What the slice delivers

`baha app maintenance` routing for `update`, `backup`, `restore` and `destroy` goes through the
installation that owns the selected deployment, with no workstation path assumptions:

- The client resolves the durable authority from `deployment.LoadDeploymentRecord` for the identity
  the repository checkout resolved to. A deployment nobody owns is refused with
  `machine.ErrorOwnershipAmbiguous` before any client input file is opened. The client never creates
  deployment state and never substitutes a client-local path for a missing authority.
- Archive and password references are client-local safe channels. A relative filename, an unclean
  spelling, a path inside a Git worktree, a symlink, a non-regular file, an empty archive and a
  group-accessible or too-short password file are each refused with a typed validation failure before
  anything reaches a lifecycle owner. Secrets travel only through a password-file channel; a rejected
  plaintext reference is reported as a non-reversible digest marker, never as content.
- Every verified operation becomes the durable window's next revision. The retained record is the only
  counter, so a replay of the same operation and recovery unit resolves to the operation already
  recorded instead of replaying a mutation, and a revision the deployment history never reached cannot
  be committed. The window history file keeps an older operation answerable after a newer operation
  supersedes it in the current window.
- Remote routing is explicit and capability-honest: only `destroy` has a qualified remote lifecycle
  owner, so `backup`, `restore` and `update` are refused with `machine.ErrorCapabilityMissing` before
  any transport call or pending write. Routing alone is never treated as proof of remote support.
- A submission whose context is already cancelled stops before it reads input, opens a transport or
  writes a window; an operation the lifecycle owner did not converge records nothing.

## Design decisions

- "Maintenance window" is a durable record per deployment, not a scheduler. No `MaintenanceWindow`
  symbol existed in the repository, so the slice defines the record and its revision discipline in
  `internal/application` and keeps all scheduling out of scope.
- The window's revision is the durable record's own counter (first commit = revision 1). A
  `VerifiedAt`-derived revision was tried and abandoned: `deployment.SaveDeploymentRecord` does not
  persist `Observed`, so a timestamp-based counter would not survive reload and could regress.
- The client never resolves a deployment from a client path, so ownership failure and path validation
  failure stay distinguishable in the machine result.

## Write-set and boundaries

- Files created by this change, all card-owned:
  - `cmd/baha/app_maintenance_client.go`
  - `cmd/baha/app_maintenance_lifecycle_owner.go`
  - `cmd/baha/maintenance_remote_safety.go`
  - `cmd/baha/app_maintenance_client_test.go`
  - `cmd/baha/app_maintenance_mutant_test.go`
  - `cmd/baha/maintenance_test_seam_test.go`
  - `internal/application/maintenance_authority.go`
  - `internal/application/maintenance_authority_test.go`
  - `internal/application/maintenance_history.go`
- Kept untouched, as required: `.github/**` (owner scope), `cmd/baha/app_remote_lifecycle.go`
  (card 116), `client_commands_behaviors` / `core_integration` (card 022), `broker` /
  `controlplaneruntime` / `source_oci` (card 118), `access_wizard` and `node_cli`. No `scripts/*` CI
  seam was edited.

## repo-rule compliance

- Plan → preflight → apply → verify: the client resolves authority, validates client channels and
  capability, then hands the mutation to the existing lifecycle owner, then records the durable
  window only for a converged operation.
- Ownership and consent preserved: destructive `destroy` requires explicit approval; `update` with
  durable state requires an explicit recovery choice; the client never bypasses an owner's consent.
- Secret protection: secrets travel only through an owner-only password-file channel; rejected input
  is reduced to a non-reversible digest marker; window records store content digests, never paths or
  secret material.
- Write discipline: only `git add <file>` for the nine card-owned files was used, never `git add -A`;
  no scratch/helper scripts were committed to the product branch; the transient build binary and an
  incidental `go.sum` reorder were reverted before commit.
- Isolation: work happened in the dedicated `/tmp/opencode` worktree; no containers or compose
  projects were started on this session host.

## Findings (for the Coordinator, not acted on here)

1. Shared-surface registration is still open. `applicationMaintenanceCommand` and
   `executeApplicationMaintenance` are reachable only from this package's tests; nothing in
   `cmd/baha/commands.go` references them, and no `"maintenance"` entry exists in
   `internal/machine/contract.go`, `spec/` or `contracts/`. The command and machine-discovery
   registration belongs to `t-20261018-r27-public-surfaces`; this slice deliberately did not register
   it. Witness: `git grep -n "applicationMaintenanceCommand\|executeApplicationMaintenance"` matches
   only `cmd/baha/app_maintenance_client.go` and its tests.
2. No workflow change was needed. `.github/workflows/ci.yml:122` already runs
   `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha` and `.github/workflows/ci.yml:340` runs
   `go test ./...` (unit job), and both job paths trigger on `pull_request` to `develop`. The new
   tests are therefore CI-covered by the existing selection rules, so no `.github/**` change is
   requested from the Owner.

## Local verification

Candidate-level local runs (`go build`, `go vet`, `gofmt`, focused maintenance `go test`,
source-readability audit, race gate, CI selector list) are all green; see the bullets below.
Full-package runs are listed under the separate heading.

### Pre-existing failures on this host, not caused by this change

- `go build -buildvcs=false -o /tmp/baha-mc ./cmd/baha` → OK.
- `go vet ./cmd/baha ./internal/application` → clean; `gofmt -l cmd internal spec contracts` → empty.
- `go test ./internal/... ./contracts/... ./spec/...` → only the pre-existing DB-gated integration
  failures (`BASEHARBOR_TEST_DATABASE_URL fehlt`) and their scheduled-writer log noise; no failure on
  any path this change owns.
- `bash scripts/source-readability-audit.sh` → Go file size PASS, function span PASS, regression ratchet PASS.
- `bash scripts/source-readability-audit.sh` → Go file size PASS, function span PASS, regression ratchet PASS.
- `go test ./internal/application -run Maintenance -count=1` → ok (window contract: identity,
  foreign refusal, revision discipline, history replay, corrupt-record rejection, file mode 0600).
- `go test ./cmd/baha -run 'TestApplicationMaintenance' -count=1` → ok: 6 behavior tests with 3 remote
  subtests plus the mutant group with 7 subguards (20 green signals), covering local routing,
  ownership precedence, path channels, secret handling, cancel, lost response and remote capability
  refusal with zero connector touches.
- Causal mutants were executed by actually breaking the production guards, not only by asserting in
  test: skipping the cancellation gate → red; skipping the client-local path validation → red;
  skipping the authority lookup before routing → red; skipping the remote capability gate → red;
  regenerating the digest instead of re-affirming the retained record → red; skipping history
  append → red (replay of a superseded revision becomes unanswerable). All production files were
  restored from a snapshot afterwards and the suite re-verified green.
- `go test -race -p 2 ./internal/targetsession ./internal/machinehttp -count=1` → ok (the CI race
  job's packages that this change's transport assertions touch).
- `go test ./cmd/baha -run 'TestPodmanRuntimeDoctor|TestCollectControlPlaneDoctor' -count=1` → ok
  (the CI selector at `ci.yml:827`).

### Pre-existing failures on this host, not caused by this change

The full local `go test ./cmd/baha` run finishes with 13 failures. The same 13 fail identically on the
clean base: they were reproduced after `git stash -u` with all new files removed (13 failures before,
13 after, identical names). They were reproduced again on the rebased candidate `d4d0f77c0` with the
identical failure reasons. They are host-state/environment failures, not regressions:

- 12 init/wizard tests (`TestQuickInit…`, `TestGuidedInit…`, `TestAppInit…`,
  `TestInitializeRepositoryManifest…`, `TestDeterministicInit…`) fail with
  `incomplete deployment state for p427-podman-boot// [d38a7c3a-…]: deployment.json is missing`.
  `p427-podman-boot` is another lane's bootstrapped Target that persists in this machine's
  `~/.config/baseharbor` configuration; the tests resolve the deployment identity of that ambient
  Target instead of their own. This is the same class of cross-lane host-state coupling the
  compose-host-isolation card fixed in PR #1383 — the fix arrives in this candidate's base, so the
  hosted CI does not show these failures; only this session host's ambient config still does.
- `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` fails with
  `start real isolated Core for App Edit: existing native network lacks a protected Core or shared
  backend owner`, i.e. a missing isolated native runtime on this session host.

Neither is suppressed or skipped in the candidate.

## Required-check coverage (what the contract demands vs what runs)

- Command-to-TLS-API tests with different local/server filesystem roots: covered by
  `maintenanceClientHome` (an owner-only client root that is a different filesystem root from the
  authority data root) in `TestApplicationMaintenanceSecretChannelStaysClientLocal` and
  `TestApplicationMaintenanceArchiveChannelRequiresTwoHomes`, and by
  `TestApplicationMaintenanceRemoteRoutingRejectsUnsupportedNativeMaintenance`, which routes through
  the real connector transport binding (`remoteApplicationTransport`) with the execution Target on an
  enrolled node and the Core authority on a different Target.
- Safe secret input: the password-file channel is the only accepted secret path; plaintext, relative,
  group-accessible and too-short inputs are refused with typed validation errors.
- Denial, cancellation and lost response: `TestApplicationMaintenanceTypedDenialCancelAndLostResponse`
  asserts a typed denial before any owner, cancellation before any owner or window, exactly-once
  routing, and that a lost response resolves to the durable operation already recorded rather than a
  second mutation.
- Capability discovery rejects unsupported native maintenance explicitly, with zero connector
  dispatches and no durable window.
- Fixtures are used rather than full backup journeys, as the contract requires; this lane started no
  container or compose project.
- Archive transfer integrity: the client records and compares content digests of the recovery unit
  (`maintenanceFileDigest`) and refuses an unreadable or empty binding, so a window can never claim a
  recovery point the client could not establish. The transfer itself stays with the existing backup
  owners, which this slice calls through the lifecycle seam and does not duplicate.

### Host-side witness: the same 13 failures on two different code states

To make sure the failure set belongs to the host and not to this change, it was measured against two
code states in the same working tree:

- candidate `2e371f5fc` (pre-rebase): 13 failures, names as above.
- clean base `c8a79faff` with all nine new files removed via `git stash -u`: 13 failures, identical names.

That is 13 on the change and 13 without it, with identical reasons. The failure text itself names the
foreign artifact (`p427-podman-boot`, deployment id `d38a7c3a-b4c5-484c-827a-e0f699217041`), which no
file in this write-set creates.

## Candidate identity

The candidate for acceptance is the single branch head. Every earlier SHA below is superseded, not
additional work: this lane pushes one coherent candidate per chain and never iterates file-by-file
through CI.

- Final candidate: `d4d0f77c0cf0db675b603daaf22ea859fac4290a`, present on the remote branch
  (`git ls-remote origin refs/heads/lane/0427-maintenance-client-wt` = `d4d0f77c0cf0db675b603daaf22ea859fac4290a`)
  and identical to the PR head (`GET /pulls/1428` → `head.sha = d4d0f77c0…`, base `812c99c88`).
- Superseded SHAs: `4308bc860`, `fd02cd895`, `2e371f5fc` (the pre-rebase line, replaced by the
  Coordinator's drift correction).
- File hashes of the candidate's nine files are fixed by the commit tree; the commit is the reference.

## CI

Run history observed by this lane, with the reason each run ended (attempt 1 for all):

| run id | sha | status | why |
| --- | --- | --- | --- |
| 42384992504 | `4308bc860` | completed/cancelled | superseded by the next push |
| 42385471568 | `fd02cd895` | completed/cancelled | superseded by the next push |
| 42385751579 | `2e371f5fc` | completed/cancelled | superseded by the rebase push; every gate that had reached completion was `success`, go-unit-tests was cancelled mid-step |
| 42386457934 | `d4d0f77c0` | completed/success | run for the final candidate |

Terminal state of run 42386457934 on the final candidate `d4d0f77c0` (observed by this lane via
`gh run watch --exit-status` and the jobs API, attempt 1):

| job | result |
| --- | --- |
| Workflow policy | success |
| PR · Source format | success |
| PR · Trusted Plan | success |
| PR · Focused Python | success |
| PR · Validation · go-build | success |
| PR · Validation · go-vet | success |
| PR · Validation · cli-gofmt | success |
| PR · Validation · go-unit-tests | success (executes the new tests: `go test ./cmd/baha` at `ci.yml:122` inside the unit job, plus the `go test ./...` at `ci.yml:340`) |
| PR Selected Checks | success |
| validate, Release Source Preflight, Targeted HA · docker, Targeted HA · podman, Exact Candidate, Consumer Pins, Demo Pin, Public Contracts, Runner Interface, Selected Runtime | skipped (not selected for this write-set) |

## Handoff

- Candidate: branch `lane/0427-maintenance-client-wt`, head `d4d0f77c0cf0db675b603daaf22ea859fac4290a`,
  PR [baseharbor#1428](https://github.com/mcpdev80/baseharbor/pull/1428) against `develop`
  (`812c99c88`). Drift-free (develop is an ancestor) and collision-free (delta is only the nine
  maintenance files).
- Hosted CI on the final SHA: run `42386457934` `completed/success`, observed to terminal by this lane.
- Card posture: the contract's behavior and regressions are delivered and CI-green, so the candidate is
  ready for CODEX review. The card stays `active` until the Coordinator records abnahmereife; this lane
  does not self-accept.
- Open items owned elsewhere: command/contract registration (`t-20261018-r27-public-surfaces`) — see
  Finding 1. No `.github/**` change is requested — see Finding 2.
- Cleanup: no compose/docker project was created by this lane (`docker compose ls` on this host shows
  no project referencing this worktree; `docker ps -a` shows none owned by this lane), and nothing on
  this host needed teardown. The transient build binary was deleted and `go.sum` restored before
  commit.
- Final remote witness at handoff time: `git ls-remote origin refs/heads/develop` =
  `812c99c8873df400348fbc8cc9be5e650b8966c4` and
  `refs/heads/lane/0427-maintenance-client-wt` = `d4d0f77c0cf0db675b603daaf22ea859fac4290a`, so the
  published candidate is the exact SHA the CI run above tested.
