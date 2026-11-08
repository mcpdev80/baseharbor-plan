# H-V1 Verifikations-Jagd — NAMENS-IDENTITAET in develop

Mission: `/tmp/opencode/mission-hunt-v1.md`. Pure finding, no product code, no PRs.

## Scope

Prove name-identity handling in develop (HEAD `7af8d440`, owner-merge `d88491982` = PR #1475 present as ancestor). Three empirical questions from the coordinator bug-hunt matrix:

- Q1: can a production path bypass the registry gate via a pre-created deployment directory (gate ordering; decision act-1475 F1 was "yes, can bypass")? Is it healed after the #1475 merge?
- Q2: does a duplicate name resolve per-uuid in EVERY name command including destroy (F2/F3; is the destroy regression missing)?
- Q3: list/status after duplicate cases (card 160 state in develop)?

## PLAN

- Read mission, establish develop baseline (SHA 7af8d440, d88491982 #1475 ancestor) — done
- Q1 empirical: registry-gate ordering — can a pre-created deployment dir bypass the duplicate-name gate? — done
- Q2 empirical: duplicate name resolves per-uuid in every name command incl. destroy (F2/F3, destroy regression missing?) — done
- Q3 empirical: list/status after duplicate cases (card 160 state in develop) — done
- Record positive findings, BF-NN + file:line witnesses — done
- Commit evidence to baseharbor-plan evidence path, confirm origin/main
- Bring down any compose/test stacks, cleanliness sweep
- Post END to inbox + record END line in evidence

## Baseline / branch provenance

- Real develop HEAD (origin/develop): `7af8d440e9a4dd1b633fdc44e4093109fe44ae37`
- Owner-merge `d88491982` (PR #1475) IS an ancestor of develop (verified via `git merge-base --is-ancestor d88491982 HEAD`).
- Follow-ups on develop: `177349187` (PR #1487, same-host conflict gate), `3187cea15` (PR #1488, EOF consent).
- Binary built from develop HEAD in `/tmp/opencode/hv1-wt` (my own clone zone), output `/tmp/opencode/hv1-baha`.
- Tests run against `origin/develop` (7af8d440), NOT the quarantined checkout at `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` and NOT the stale local-tracking ref `cdb4350a6` (the clone's origin/develop was stale; real remote head is 7af8d440).

## Findings

### F1 (Q1) — Registry gate: pre-created same-name deployment does NOT bypass the gate. HEALED. (POSITIVE)

The #1475 merge (`d88491982`) added `refuseDuplicateApplicationName` in `internal/deployment/deployment_duplicate_name.go` (guard) plus a name-based check in the create seam. Empirically verified:

- `internal/deployment/deployment_duplicate_name.go:34` `refuseDuplicateApplicationName`: scans `ListDeployments(target)` for ANY other uuid claiming the same (target, name, env) triple; fails closed with `ErrDuplicateApplicationName` naming the existing deployment. Guard keys on user-visible (target, name, env), never the opaque application_id.
- Guard runs inside `SaveDeploymentRecord` at `internal/deployment/deployment_store.go:394`, BEFORE the owner seam at :400 and before any dir creation.
- Create seam `cmd/baha/app.go:55` `createTargetManagedApplication` has an explicit name+env duplicate check at lines 55-58 BEFORE the `os.MkdirAll(sourceRoot)` at :79 — a pre-created same-name deployment is caught there.
- EMPIRICAL PROOF (run, PASS): probe `TestHV1F1PreCreatedDirBypassThroughSeam` (removed after run — pure-finding mission) seeded two out-of-band same-name/same-env deployments (different uuids) in one shared XDG_DATA_HOME, then called the production seam `createTargetManagedApplication` for the same name → returned `application.ErrExists`. The gate is NOT bypassable by a pre-created same-name deployment.
- EMPIRICAL PROOF (existing, PASS): `TestSaveDeploymentRecordRefusesDuplicateApplicationName` (BF-02, `internal/deployment/duplicate_name_test.go`), `TestCreateTargetManagedApplicationRegistersResolvableDeployment` (second create returns `ErrExists`, `cmd/baha/app_create_target_test.go:66`).
- EMPIRICAL PROOF (existing, PASS): `internal/deployment` full suite + cmd/baha duplicate-name/uuid/ambiguous suite run green against 7af8d440.

CONCLUSION: act-1475 F1 ("yes, can bypass via pre-created dir") is the PRE-fix behaviour; after `d88491982` the guard enforces the duplicate-name gate at both the store seam and the create seam. No bypass.

### F2 (Q2) — Duplicate name resolves per-uuid in EVERY name command incl. destroy. (POSITIVE)

- Shared resolver: `cmd/baha/app_context.go:234` `resolveRegisteredApplication`. `--uuid <id>` selector at :242-255 resolves the exact deployment dir, bypassing the name/environment filter.
- Name collision with same env → actionable `machine.ErrorOwnershipAmbiguous` / cause `application_name_ambiguous` at :330, with `Next` remediation routing to `... --uuid <deployment-id>` (line 335).
- The `--uuid` selector is stripped from positional args and captured separately in the shared `extractApplicationEnvironment` at `cmd/baha/app_context.go:549` (`--uuid` / `--uuid=` consumed, value via `extractApplicationUUID` at :567).
- Destroy uses the SAME shared path: `cmd/baha/app_destroy_lifecycle.go:66` `newApplicationDestroyExecution` → `parseDestroyArgs` (uuid stripped) → `resolveApplicationEnvironment(ctx, ..., "destroy", env)` → `resolveRegisteredApplication(..., command="destroy", deploymentUUID)`.
- EMPIRICAL PROOF (existing, PASS): `TestResolveRegisteredApplicationByUUIDResolvesUnambiguously` resolves BOTH colliding deployments by uuid; `TestResolveRegisteredApplicationAmbiguousNameSurfacesUUID` surfaces the uuid-naming ambiguity; `TestResolveRegisteredApplicationUUIDNotFound` fails closed. All green against 7af8d440.

CONCLUSION: F2/F3 hold for destroy too — no separate destroy regression was needed because destroy shares `resolveRegisteredApplication`/`--uuid` with every other name command. The uuid path resolves a duplicate name unambiguously in destroy.

### F3 (Q3) — list/status after duplicates: list shows the duplicates and surfaces actionable uuids; card 160 list-state reconciliation is NOT yet in develop. (MIXED)

- `ListDeploymentsForDisplay` (`internal/deployment/deployment_list.go`) reads ALL deployment dirs on the target, so both name-colliding deployments appear in `app list`.
- `resolveRegisteredApplication` matches BOTH records by name (:257-265), sees `len(matches) > 1` with same env, and returns the actionable ambiguity error naming both uuids (:311-338) — the operator is routed to the uuid selector.
- Card 160 (`fix/0427-160-list-stale-after-kill`, HEAD `5753eebd`) adds `reconciledListState` (BF-04: downgrade failed/stopped/retired → DEGRADED, flag observed/applied reference drift) — this is the list-status reconciliation for the "after kill" case. It is a fix branch NOT merged into develop. EMPIRICAL: `reconciledListState` does NOT exist in develop HEAD (`grep -rln reconciledListState --include=*.go .` returns nothing); it exists only in the 160 branch.
- `git merge-base --is-ancestor 5753eebd 7af8d440` = NO. Card 160 is pending, not in develop.

CONCLUSION: In develop, list shows both duplicates and surfaces the uuid ambiguity (actionable). The additional list-STATE reconciliation (DEGRADED on kill/drift) is card 160, still pending — NOT a defect in the name-identity work, a separate outstanding fix.

### POSITIVE (explicitly noted, as the mission requires)

- `ErrDuplicateApplicationName` names the existing deployment uuid and colliding env in its message (`deployment_duplicate_name.go:56`) — actionable disambiguation, no longer the opaque "application machine: denied".
- Distinct (name, env) pairs still allowed: `TestSaveDeploymentRecordAllowsDistinctEnvironmentConflict` (`duplicate_name_test.go`) — same name on different environments is legitimate, not a false collision.
- Same-identity re-save (apply retry) is not a collision: `TestSaveDeploymentRecordIdempotentUpdateSameIdentity` — fail-closed guard does not break idempotent apply.

## Cleanliness

- Build binary + test cache isolated to my own zones: `/tmp/opencode/hv1-wt` (clone), `/tmp/opencode/hv1-gocache`, `/home/marcel/dev/baseharbor-ecosystem/work/.hv1-gocache` (+ GOCACHE on `/`). No scratch under `/home/marcel/dev/baseharbor-ecosystem`.
- No compose / docker / podman stacks started (pure code-finding mission, no runtimes invoked).
- Working tree of `/tmp/opencode/hv1-wt` clean (probe test file removed). No product source changed.
- Cleanliness: OK.

## END

MISSION COMPLETE. 3 findings, 0 blockers. No product code, no PRs, no runtimes started.

- F1 (Q1): registry duplicate-name gate is HEALED — pre-created same-name deployment cannot bypass (`createTargetManagedApplication` + `refuseDuplicateApplicationName` fail closed). BF-NN: `internal/deployment/deployment_duplicate_name.go:34`, `cmd/baha/app.go:55`.
- F2 (Q2): duplicate name resolves per-uuid in every name command incl. destroy; F2/F3 regression not separately needed (shared `resolveRegisteredApplication`/`--uuid`). BF-NN: `cmd/baha/app_context.go:234,549,567`, `cmd/baha/app_destroy_lifecycle.go:66`.
- F3 (Q3): list shows duplicates + actionable uuid ambiguity; card 160 list-state reconciliation pending (NOT in develop 7af8d440).
- All empirical runs green against 7af8d440.
