# 0427-175 round 5 — the advertised uuid repair reaches the mutation; identity carried unchanged

Mission: MISSION 0427-175 r5 on PR #1512 (owner directive 2026-11-09, after uncovered r3/r4).
Lane: `mission-175-r5`, worker-flash seat, worktree `/tmp/opencode/w175r3-wt/1512`
(branch checkout `0427-175-r3` at `a6afd633c`, pushed to `0427-175-initlock`).
Recipe: `evidence/r27-welle5-folge-2026-11-08/vm-bughunt/act-1512-review-r4.md`, verbatim.
No `.github/**` edits. No subagents (AGENTS §4.8).

## Remote-truth witnesses (own reads)

    git ls-remote origin refs/pull/1512/head  (before push)  -> a6afd633ce38a4cedfb74bc71d6703d3df56312b
    git push origin HEAD:refs/heads/0427-175-initlock        -> a6afd633c..cbe322c88  HEAD -> 0427-175-initlock
    git ls-remote origin refs/pull/1512/head  (after push)   -> cbe322c88445e4f72694785ec4f5c522720838c3
    git ls-remote origin refs/heads/develop                  -> fea92f379 (0 commits ahead of HEAD: no drift merge needed)

Hosted run on exactly the pushed head (own `gh api` read):

    run 42629021041  "CI · PR #1512"  head_sha=cbe322c88445e4f72694785ec4f5c522720838c3
    status=completed conclusion=success  https://github.com/mcpdev80/baseharbor/actions/runs/42629021041
    jobs: 19 success, 12 skipped (matrix/label-gated lanes: draft-focused, HA podman/docker,
    Keycloak/Core, runtime validate, runner interface), 0 failure, 0 cancelled.

## PLAN

All steps completed on candidate `cbe322c88`:

1. Re-fetch remote truth (branch, PR head, develop) before editing; confirm a6afd633c base.
2. Acceptance (1): implement `--uuid` selection in the real destroy CLI path and carry the selected deployment identity unchanged through resolution, authorization, preflight and mutation.
3. Fix the parse path: `parseDestroyArgs` consumes the whole `--uuid` pair so the deployment id can never land in the NAME slot (`cmd/baha/app_lifecycle.go`).
4. Fix the resolver-arg paths: the command seam reads the selector via `extractApplicationUUID(args)` and forwards `[]string{"--uuid", id}` plus the selection to `resolveApplicationEnvironment` (`cmd/baha/app_destroy_lifecycle.go`).
5. Make the located record authoritative at the identity seams (repository lookup, source hydration, backend projection) so a poisoned twin is reachable while its sibling is present (`cmd/baha/app_context.go`, `cmd/baha/application_backend_placement_selection.go`, `internal/deployment/deployment_repair_read.go`).
6. Recheck the selected deployment id immediately before the destructive record removal (fail closed on drift).
7. Acceptance (2): poisoned-registry CLI regression invoking the advertised repair; selected twin gone, sibling byte-identical, strict inventory healthy, listing shows only the survivor; a conflict error is an explicit test FAILURE.
8. Counterfactual probes: routing-off => conflict/error, routing-on => deletion succeeds (proves the cell is load-bearing).
9. Acceptance (3): race regression — child emits witness lines from inside the registry-lock seam and races the SAME application name/id; the parent switches on the witness, never on a bare exit code; no silent success.
10. Fail-closed selector matrix (no selector, `--uuid` without value, empty value, NAME+uuid, conflicting uuids) leaves both twins untouched.
11. CLI face parity vs the base binary on every no-selector invocation.
12. gofmt, go vet, go build, targeted regressions, -race run, source-readability audit, documentation audit.
13. Commit, re-fetch refs/pull/1512/head, push, ls-remote witness, watch the hosted run to a terminal state, publish this evidence, END to shared inbox.

## What was actually blocking the repair (root causes, each proven by probe)

The r3/r4 advice was right that the twins are indistinguishable by identity — that IS the poison:
same `application_id`, same `environment`, same application NAME, same repository source. Every
seam that asks the registry "which record belongs to this pair" must refuse. The repair therefore
needs the selected deployment id carried EXPLICITLY, and the record itself authoritative:

- `parseDestroyArgs` saw the bare selector VALUE (left behind by the environment splitter) as a NAME.
- `resolveApplicationEnvironment` read `extractApplicationUUID(filtered)` — the half-split list, so a
  value could be mistaken for the flag token and the conflict gate pre-empted the targeted command.
- The deferred `resolveAppliedBackendSelection` re-identified the deployment through
  `DesiredProviderPreferencesAt` -> `FindDeployment` -> strict `ListDeployments`, so resolution raised
  the conflict AFTER a successful selection (proved: env-flagged projection-off probe resolves, projection-on refuses).
- `resolvedRepositoryApplication` -> `FindDeployment` and `resolveRecordByIdentity` ->
  `resolveRepositoryLifecycleIntent` -> `repositoryIdentityClaims` -> `ListDeployments` each independently
  refused the selected twin, and a caller-side `application_id` comparison cannot help because the pair
  matches both twins. Fix: `LoadDeploymentRecordForRepair` keeps the loader's path/identity proof but
  does not compare a caller-side `application_id` (new `internal/deployment/deployment_repair_read.go`).

## Changes (candidate cbe322c88)

- `cmd/baha/app_lifecycle.go`: `parseDestroyArgs` consumes the `--uuid <id>` pair (`--uuid` and `--uuid=` forms);
  destroy Usage documents `baha app destroy [NAME] [--uuid DEPLOYMENT-ID] [--yes] [--full-reset]`.
- `cmd/baha/app_destroy_lifecycle.go`: selector extraction from raw args, NAME/uuid mutual exclusion,
  intact `[]string{"--uuid", id}` routing to the resolver, `selection` field on the execution, and a
  pre-delete identity recheck so a drifted selection can never delete the sibling.
- `cmd/baha/app_context.go`: optional selection on `resolveApplicationEnvironment`, record-authoritative
  selection at the repository-lookup and record-hydration seams (`registeredRepositoryDeployment`,
  `resolveRecordByIdentity`), and a final "did the selection route the resolution" check.
- `cmd/baha/application_backend_placement_selection.go` (new): selection token helpers, the record-scoped
  backend-placement/desired-preference projection (`resolveAppliedBackendSelectionForDeployment`),
  applied-intent decoding and authored-workload discovery — the projection the shared path yields for a
  healthy registry, computed from the SELECTED record only.
- `internal/deployment/deployment_repair_read.go` (new): `LoadDeploymentRecordForRepair`,
  `DeploymentRecordIdentityIs` (same validation path; no caller-side application_id comparison).
- `internal/deployment/deployment_store.go`: the repair seams live in the new file, so the store keeps
  its base length (778 lines) and the readability audit stays clean.
- Tests: `TestRegistryConflictRepairCommandDeletesSelectedTwinOnly`,
  `TestRegistryConflictRepairOmittedOrInvalidUUIDFailsClosed`, `poisonTwinFixture` (real shared repository
  source so the repair reaches the repository branch); `TestParseDestroyArgsAcceptsUUIDSelector` +
  `mustSplit`; `app_init_concurrent_race_test.go` child witnesses
  (`reached-registration-seam`, `persisted-record`, `converged-on-existing-claim`, `refused-busy-lock`)
  and parent assertion on the witness instead of `_ = out`.
- Docs: EN/DE `command-index.md` destroy usage line (documentation-audit PASS).

## Verification results (all on candidate worktree, GOCACHE on /home, -buildvcs=false)

- `go build` / `go vet` / `gofmt -l` clean; `scripts/source-readability-audit.sh` PASS (size, function
  span, regression ratchet); `scripts/documentation-audit.sh` PASS.
- `go test ./cmd/baha -run 'TestRegistryConflict|TestPoisonedTarget|TestPlanningPaths|TestParseDestroyArgs|TestConcurrentInit|TestUUID|TestAppContext|TestDeployment|TestNeverDelivered|TestAppDestroy|TestDestroy|TestAppStatus|TestAppList|TestAppShow|TestAppPlan'` => ok.
- `go test ./internal/deployment/ ./internal/application/` => ok.
- `-race` run of destroy/poison/parse/concurrency cells => ok (4.6s).
- Repair regression detail: victim `deployment.json` gone, keeper byte-identical (bytes.Equal), strict
  `ListDeployments` healthy with exactly 1 record, display listing shows only the survivor, and the
  production `runPreflight` of the selected twin passes.
- Counterfactual: with routing disabled the same invocation fails at the poison gate (test FAILs), so
  the cell cannot pass on a conflict error.
- CLI face matrix: identical to the base binary (`a6afd633c` build) on `--yes`, `demo --yes`, `abc`,
  `--bogus`, `a b`, `demo`, `--full-reset`, `--uuid`; `--uuid <id>` routes to
  `deployment "<id>" has no registered deployment on target "local"` instead of the base CWD fallthrough.
- Local full `cmd/baha` run: the ONLY failure is `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`
  ("existing native network lacks a protected Core or shared backend owner"), reproduced identically on a
  clean `a6afd633c` checkout => environmental (shared home/network state), not this candidate. The hosted
  run's `go-unit-tests` job (same head) is green.

## Repo-rule compliance

- Plan -> preflight -> apply -> verify preserved: the repair routes through the same authorization and
  preflight seam as any destroy; only the identity source changed, the consent checks are untouched.
- Ownership/secret protection unchanged: no secrets in evidence, no new state written on the repair
  read paths (the projection only reads records; the authored baseharbor.yaml is never rewritten).
- Readability: oversized-file rule respected by extracting the selection projection to its own focused
  file instead of a baseline ratchet entry; `deployment_store.go` back to base length.
- CI discipline: one coherent push, one hosted run observed to a terminal state by this lane.

## Handoff

Candidate chain: `0427-175-initlock`, head `cbe322c88` (ancestor `a6afd633c`, develop contained).
Awaiting CODEX-REVIEW against `act-1512-review-r4.md` acceptance (1)(2)(3). No merge, tag or release
action taken or claimed.
