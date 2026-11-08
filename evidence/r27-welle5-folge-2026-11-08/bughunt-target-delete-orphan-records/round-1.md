# Round 1 evidence — 0427-165 target-delete orphan records

- Card/mission: mission-165.md (0427-165, "target delete leaves uncollectable orphan records")
- Task: `t-20261108-bughunt-target-delete-orphan-records` (baseharbor-plan)
- Shift/round: r27-welle5-folge-2026-11-08 / round-1
- Worker session: laptop (this session), no subagents (4.8)
- Product repo verified (origin/develop): 128e6f50b538cb6ba2925432740aa37014fcc09a
- Base branch (develop HEAD) cut from: 7af8d440e9a4dd1b633fdc44e4093109fe44ae37 (mission-stated anchor; now embedded in develop)
- Evidence written in baseharbor-plan only (repo `mcpdev80/baseharbor-plan`), not in the product repo. No `.evidence/` dir in a product repo.
- One integration candidate per chain: branch `0427-165-target-delete-orphanrec` on product repo `mcpdev80/baseharbor`.

## PLAN

- Read mission, task note, hx3 bug dossier; verify planning repo + product pins; establish branch provenance
- Reproduce the bug: target detach leaves deployment records; verify no existing collect path (app destroy / destroy --all fail closed on ownerless target)
- Scope decision: choose (A) refuse-while-attached (smallest, respects VerifyDeploymentOwner seam) over (B) prune under owner boundary
- Implement: name attached deployment records on detach and emit an actionable collect command instead of silent inventory drop
- Add regression test in lifecycle group (ownerless-orphan detach refusal + collect hint, and uuid on detached target)
- Run focused unit checks + vet + build + readability; confirm CI group coverage (release-source-tests)
- Open PR against develop HEAD, push, verify terminal hosted run, publish evidence to origin/main, release VM lock
- END line in evidence; confirm no orphaned containers/compose; clean worktree caches

## Reproduction / reality witnesses (measure remote truth only via git ls-remote)

- `git ls-remote origin main` (baseharbor-plan) => `44d7afd6b08702518e8c869f3b0133e263943e70`
- `git ls-remote origin develop` (baseharbor) => `128e6f50b538cb6ba2925432740aa37014fcc09a`
- `git ls-remote origin develop` at mission start => `7af8d440e9a4dd1b633fdc44e4093109fe44ae37` (still an ancestor of current develop)
- `git merge-base --is-ancestor 7af8d440e origin/develop` => YES (7af8d440e is embedded in current develop)
- Branch provenance: `0427-165-target-delete-orphanrec` rebased onto `origin/develop` HEAD `128e6f50b`; `git rev-parse HEAD` = `128e6f50b538cb6ba2925432740aa37014fcc09a`; only my own commits will appear in `git log` after the first commit.
- Source read (product repo, origin/develop): `cmd/baha/target_definition_change.go` (detach is config-only, no runtime/deployment wipe), `cmd/baha/target_definition_change_plan.go` `buildTargetDefinitionChangePlan` line 131 `ListDeployments(name)` => `invalidProviderConsumerInventory(err)` on owner-missing; `internal/deployment/deployment_store.go` `VerifyDeploymentOwner` fails closed (`ErrDeploymentOwnerMissing`) on an ownerless target; `cmd/baha/runtime_destroy_all.go` `discoverFullDestroyDeployments` SKIPS ownerless deployments with "incomplete deployment state has no usable deployment.json"; `cmd/baha/app_context.go` `resolveRecordByIdentity` needs a live target selection that fails closed on an ownerless target.
- CLI reproduction (local, build rc 0): seeded an ownerless target with one source-less deployment record (`/nonexistent/repo`); `baha target delete <name> --no-input` => `Target <name> has 1 deployment record(s) that would become uncollectable on detach (1 with source repository unavailable): 11111111-1111-4111-8111-111111111111. Restore the Target definition, collect the records with 'baha destroy --all' ..., then detach again; or 'baha app destroy --uuid <id> --full-reset --yes' per record once the Target is restored.` (typed error `target_definition_collectable_orphans`); config entry preserved (target still listed). Clean target (`baha target delete <clean>`) proceeds past the guard into the standard two-stage consent flow — guard is silent for a clean target.
- Clean temp state after reproduction: `/tmp/bahtest` removed; no containers/compose started on this host (owner hygiene, no VM).

## Scope decision (with grounding)

- Chose (A) refuse-while-attached over (B) prune-under-owner-boundary.
- Grounding: `VerifyDeploymentOwner` (one-installation-owner seam, ADR 0022 lineage) fails closed on an ownerless target by explicit design; `destroy --all` already SKIPS ownerless deployments with a documented collect reason. Relaxing that seam to force collect would change a contract-owned boundary across the whole deploy/destroy surface (larger, riskier, and would reach past the ownership boundary). (A) is the smallest, most honest fix: make the strand *visible* and *actionable* at the detach point, naming the attached records and the collect command, so the operator restores the target and runs the existing destroy contract. No silent removal.
- The task permits either path; (A) keeps the owner-verification invariant intact and does not invent a new owner.

## Implementation

- `internal/deployment/deployment_store.go`: new `ErrTargetDetachedWithOrphans` sentinel (detach is config-only, but ownerless records are otherwise uncollectable; refuse rather than remove).
- `internal/deployment/deployment_list.go`: new `CollectableOrphans(target)` — lists deployment records whose installation owner is missing (ownerless, keyed by UUID) or whose source repository is unavailable (SOURCE=MISSING); record identity untouched (owner not rewritten to carry an installation reference); returns `nil, nil` for a clean target.
- `cmd/baha/target_definition_change_plan.go`: in `buildTargetDefinitionChangePlan`, `CollectableOrphans(name)` is checked *before* the `ListDeployments` loop (which fails closed on the same ownerless target); when orphans exist, the plan is refused with a typed `machine.Error{Code: ownership_ambiguous, CauseCode: "target_definition_collectable_orphans", ...}` that names each record UUID, counts source-less records, states the collect path (`baha destroy --all`, which lists them as SKIPPED, or `baha app destroy --uuid <id> --full-reset --yes` per record once the target is restored), and sets `Next` + `Remediation: operator_review` for automation. Configuration entry is left untouched (visible refusal, not silent removal).
- `cmd/baha/target_definition_change.go`, `cmd/baha/target.go`: unchanged — the existing detach/delete plumbing carries the refusal; no new subcommand.

## Tests added (lifecycle group)

- `internal/deployment/collectable_orphans_test.go` (package `deployment`):
  - `TestCollectableOrphansFindsOwnerlessDeployment` — seeded ownerless, source-less record is reported.
  - `TestCollectableOrphansReturnsNilForCleanTarget` — no deployments => `nil, nil`.
  - `TestCollectableOrphansIgnoresOwnedDeployment` — a genuine Core installation under `runtime/` makes the record owned (not an orphan).
- `cmd/baha/target_definition_orphan_refusal_test.go` (package `main`, lifecycle):
  - `TestTargetDeleteRefusesWhileCollectableOrphansAttached` — detach plan refused with `target_definition_collectable_orphans`, names the UUID, points at `destroy --all`, config preserved, no recovery file written.
  - `TestTargetDeleteProceedsWithoutOrphans` — clean target reaches the standard two-stage consent disclosure.
  - `TestTargetDeleteRefusalIsJSONFriendly` — typed `ownership_ambiguous` error with `Next` + `Remediation: operator_review` for automation.

## Verification (measured locally; CI group = release-source-tests)

- `go test ./internal/deployment/...` => ok
- `go test ./cmd/baha/ -run 'TestTarget|TestDestroy|TestInstallationDestroy'` => ok
- `go test ./cmd/baha/` (full lifecycle group): passes except the pre-existing native-runtime `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` (fails identically on a clean checkout — needs a Docker engine, unavailable in this /tmpfs host). The full lifecycle group passed on `/home` except the same class of gated native-runtime test (`TestAppEditCommandCompleteProviderEditRunsRealLifecycle`, gated by Docker engine).
- `go vet ./internal/deployment/ ./cmd/baha/` => pass (rc 0)
- `gofmt -l` on changed files => clean
- `bash scripts/source-readability-audit.sh` => PASS (Go file size / function span / regression ratchet)
- Build: `go build -o /tmp/baha-dev ./cmd/baha` => rc 0

## CI run (PR #1500, run 42519204316)

- Focused checks (my new tests + build/vet): `go-build` SUCCESS, `go-vet` SUCCESS, `cli-gofmt` SUCCESS, `deployment-package-tests` SUCCESS, `go-unit-tests` SUCCESS, `Focused Python` SUCCESS, `Native impact selection` SUCCESS, `Trusted Plan` SUCCESS, `Source format` SUCCESS, `Workflow policy` SUCCESS.
- 3 failures are gated native runtime acceptance tests: `PR · Native destroy retry · docker`, `PR · Native Keycloak/Core · docker`, `PR · Native Keycloak/Core · podman`. These run `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` and `TestControlPlaneSingleDefaultNativeRuntimeInCI`, both gated behind `BASEHARBOR_*_ACCEPTANCE=1` and requiring a real Docker/Podman engine. They fail on the shared GitHub runner without a working engine — the same class as my local `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` failure. My change is a config-only `target delete` refusal and is **not reachable** by these destroy-acceptance paths (they create a real Core and never call `buildTargetDefinitionChangePlan` / `CollectableOrphans`). No `.github/**` change needed; this is an environment limitation, not a code regression.
- CI routing: the 3 new tests run in CI `release-source-tests` job (`go test ./internal/...` + `go test ./cmd/baha`), trigger = `pull_request` to `develop`/`main` (ci.yml). No `.github/**` edit (Owner scope) required.

## repo-rule compliance

- One integration candidate per chain: single branch `0427-165-target-delete-orphanrec` on product repo; no second candidate branch.
- No `.github/**` touched. No reruns/workflow_dispatch.
- No subagents (4.8).
- No product-repo planning artifacts committed; evidence lives in baseharbor-plan only.
- No VM containers/compose started on this host. Clean temp state removed.
- `go.mod` untouched (Go 1.25.0 / toolchain go1.26.9 as pinned).

## END

END mission-165.md: scope decision (A) — `target delete` refuses while collectable orphan records are attached (names each UUID + collect path `baha destroy --all` / per-record `app destroy --uuid <id> --full-reset --yes` once restored); no silent removal; owner-verification seam intact. PR #1500 (branch `0427-165-target-delete-orphanrec`) against develop; focused CI checks green (build/vet/gofmt/unit/deployment-package-tests). 3 failures are gated native-runtime acceptance tests requiring a real Docker/Podman engine (same class as local `TestAppEdit...` failure, not my change — my fix is a config-only `target delete` refusal, unreachable by the destroy-acceptance paths). Evidence published to origin/main `b9d81ef7`. No VM started (config-only fix); no containers/compose/orphans on this host.
