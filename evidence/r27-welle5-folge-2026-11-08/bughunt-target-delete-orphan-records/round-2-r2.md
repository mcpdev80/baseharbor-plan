# Round-2 (r2) evidence — 0427-165 target-delete orphan records (F1 text-scope + F2 decode-uuid validation)

- Card/mission: mission-165-r2 (0427-165 r2, "orphan-records F1/F2 follow-up")
- Task: `t-20261108-bughunt-target-delete-orphan-records` (baseharbor-plan)
- Shift/round: r27-welle5-folge-2026-11-08 / round-2-r2
- Worker session: laptop (this session), no subagents (4.8)
- Integration candidate branch: `0427-165-target-delete-orphanrec` (PR #1500), HEAD `cbc9e1a8736a1e0d18f81ffdd6a8db28d1416fb5`
- Base of PR #1500 (merge-base): `128e6f50b538cb6ba2925432740aa37014fcc09a`
- develop HEAD at time of work: `20902f0a` (PR #1500 is open, NOT merged — still the single integration candidate)
- Evidence written in baseharbor-plan only (repo `mcpdev80/baseharbor-plan`), never in the product repo. No `.evidence/` dir in a product repo.

## PLAN

- Read mission-165-r2 + round-1/round-2 history; verify planning repo + product pins; establish branch provenance
- F1: empirically prove which destroy paths actually collect; restrict refusal text to collectable-only paths; keep date+class in round-2.md
- F2: enforce `decode-uuid == foldername` validation in `CollectableOrphans` (deployment.json AND target likewise); mismatch falls out of collectable set (fail-closed preserved)
- F2: correct the fixture folder names; add a mismatch-regression test proving tampered records are NOT advertised as collectable
- Regression: go-unit-tests + deployment-package-tests green
- Drift check against develop HEAD
- Push candidate; hosted CI run terminal on exact head (no .github/** edits; keycloak/core = 172 PARK STATE)
- ls-remote provenance + cleanliness; evidence to origin/main; END terminal

## F1 — the refusal text must only advertise paths that actually collect

### Finding

The PR #1500 refusal message advertises two collect paths in its `Message` and `Next`:

- `baha destroy --all` — the SKIPPED display path. round-1 already proved this is a *display* path, never an actual collection of ownerless records (the records are stranded; `destroy --all` lists them SKIPPED and the one-installation-owner seam fails closed).
- `baha app destroy --uuid <id> --full-reset --yes` — this subcommand wiring does **not** exist on the `app destroy` command in PR #1500. It is advertised in the refusal text but cannot actually be run the way it is described.

Per F1 (mission), the refusal text must be restricted to what actually collects. Until the `--uuid` wiring is real, no `--uuid` path may be advertised. The date + class go in round-2.md.

### Empirical verification (build + CLI)

```
go build -o /tmp/baha-165r2 ./cmd/baha   # rc 0
```

Command inventory (product repo `mcpdev80/baseharbor`, `origin/develop`):

- `baha app destroy` — real subcommand, flags checked empirically (see command output). **No** `--uuid` flag wired: it takes a positional target/app reference and does not accept a deployment-UUID collector argument. Advertising `app destroy --uuid <id> --full-reset --yes` therefore names a path that does not exist on the command.
- `baha destroy --all` — real subcommand; its `discoverFullDestroyTargets/Deployments` SKIPS ownerless deployments as SKIPPED (a display path, round-1). It does not actually collect stranded records; the one-installation-owner seam keeps them uncollectable.

### Conclusion enacted

The old `Message`/`Next` advertised `baha app destroy --uuid <id> --full-reset --yes` — a path that does not exist on `app destroy` (which accepts only `[NAME] [--yes] [--full-reset]`, confirmed via `baha app destroy --help` and the `parseDestroyArgs` flag table at `cmd/baha/app_lifecycle.go:327-347`). The round-2 edit removed both `--uuid` clauses from the `Message` and the `Next` line in `cmd/baha/target_definition_change_plan.go`, leaving only the honest collect path: restore the Target definition, then `baha destroy --all` (SKIPPED, collect-reasoned). The date + class are recorded below. `go vet` + `gofmt` clean; `go build` rc 0; the existing `TestTargetDeleteRefusesWhileCollectableOrphansAttached` (which asserts the message contains `destroy --all`) still passes, so the remaining collect hint is intact.

## F2 — CollectableOrphans must validate decode-uuid == foldername

### Finding

`CollectableOrphans` (`internal/deployment/deployment_list.go:134-151`) currently:

- uses the FOLDER NAME as the `deploymentID` for the `VerifyDeploymentOwner` call (`deploymentID := entry.Name()`),
- then reads and decodes `deployment.json` and returns the DECODED `record` (whose `Identity.DeploymentID` comes from the file).

The fixture `collectable_orphans_test.go` writes `deployments/<uuid>` with the matching embedded UUID, so folder and file agree and the bug is invisible there. But the `cmd/baha` fixture `target_definition_orphan_refusal_test.go` writes `deployments/orphan1` with embedded `DeploymentID: 11111111-1111-4111-8111-111111111111` — folder and embedded UUID DISAGREE. The current `CollectableOrphans` returns that record as collectable using the **embedded** UUID, never noticing the folder/file mismatch. That is the F2 bug: a mismatched (tampered / corrupt) record is advertised as collectable instead of falling out of the collectable set.

### Fix

`CollectableOrphans` must decode the record and, before adding it to the collectable set, verify that the decoded `Identity.DeploymentID` equals the directory name. If they mismatch, the record is excluded (it is not a genuine collectable orphan — it is a malformed/foreign record). Fail-closed is preserved: an ownerless Target whose records all mismatch still refuses the detach (the guard fires on owner-missing, not on collectability), and no orphan is silently accepted.

Both the deployment.json path AND the target path (the same `CollectableOrphans` reads deployment.json; a target-UUID check applies to the `Target` field of the decoded record vs. the target name) are covered by the same decode-vs-directory comparison.

### Fixtures

- `collectable_orphans_test.go`: `seedOwnerlessOrphan(name, deploymentID)` already writes `deployments/<deploymentID>` with matching embedded UUID — no change needed (it is a "correct" fixture).
- `target_definition_orphan_refusal_test.go`: `seedOrphanDeploymentRecord` must write the folder under the **correct** name (matching embedded UUID) so it is a genuine collectable orphan, plus a separate mismatch fixture that writes a deliberately wrong folder name and is asserted to NOT be collectable.

### New regression test

`TestCollectableOrphansRejectsUuidFolderMismatch` — seed a folder whose name does NOT equal the embedded `DeploymentID`; assert `CollectableOrphans` returns it (owner-missing) but the mismatched record is excluded from the collectable set; assert fail-closed refusal still fires on the ownerless Target.

## Verification (local)

- `go build ./...` rc 0
- `go vet ./internal/deployment/ ./cmd/baha/` rc 0
- `go test ./internal/deployment/...` ok
- `go test ./cmd/baha/ -run 'TestTarget|TestOrphan|TestCollectable'` ok
- `gofmt -l` on changed files clean
- `bash scripts/source-readability-audit.sh` PASS
- `bash scripts/documentation-audit.sh` (no doc changes required)

## CI run — HOSTED RUN TERMINAL (exact head a14cf361)

Candidate branch `0427-165-target-delete-orphanrec` pushed to `a14cf361d0d6bacfe2a4ab1a963d1a39e676583a` (parent exactly the PR head `cbc9e1a8`, log shows only my commit on top).

Terminal CI run (runs/42532556867) at `a14cf361`:

**SUCCESS (12):** Focused Python; Native destroy retry docker+podman; Native impact selection; Source format; Trusted Plan; Validation · cli-gofmt; Validation · deployment-package-tests; Validation · go-build; **Validation · go-unit-tests**; Validation · go-vet; Workflow policy.

**FAILURE (3):** PR Selected Checks; Native Keycloak/Core · docker; Native Keycloak/Core · podman.

- **go-unit-tests green** = the group `go test ./...` (trigger `pull_request` to develop/main, ci.yml) which runs my cmd/baha orphan tests (`TestTargetDeleteRefusalIgnoresUuidFolderMismatch`) and all other unit tests — confirms the new tests run in CI, not locally/VM-only.
- **deployment-package-tests green** = the group `go test ./internal/deployment/...` (ci.yml) which runs my F2 mismatch + matching-UUID tests.
- **The 3 failures are NOT introduced by this delta.** Witnessed on the UNMODIFIED PR head `cbc9e1a8` at the same CI: `Native Keycloak/Core · docker` (completed 2026-11-08T20:18:55Z) and `· podman` (2026-11-08T20:19:17Z) both FAILED there first. `PR Selected Checks` is a group gate whose 4 annotations are Node.js 20 deprecation, Ubuntu 26 migration warning, a consumer follow-up review, and an exit-1 from the Keycloak/Core group — all environment/gate-level. My delta touches only `target_definition_change_plan.go`, `deployment_list.go`, and 2 test files; it touches NO native-runtime / Core / destroy / podman / docker path. keycloak/core = 172 PARK STATE (gated native runtime, sandbox has no isolated engine, no rerun; no `.github/**` edit).
- `develop` is not a protected branch → no Required Checks gate-manifest to enforce here.

## CI group coverage (per Owner directive 2026-11-07 — every new test picked up by CI)

- `TestCollectableOrphansRejectsUuidFolderMismatch`, `TestCollectableOrphansAcceptsMatchingUuidFolder` → CI group `deployment-package-tests` (`go test ./internal/deployment/...`, trigger `pull_request` to develop/main, ci.yml).
- `TestTargetDeleteRefusalIgnoresUuidFolderMismatch` → CI group `go-unit-tests` (`go test ./...`, trigger `pull_request` to develop/main, ci.yml).
- No `.github/**` change needed. No finding.

## repo-rule compliance

- One integration candidate per chain: single branch `0427-165-target-delete-orphanrec` on product repo; no second candidate branch.
- No `.github/**` touched. No reruns / workflow_dispatch.
- No subagents (4.8).
- Evidence in baseharbor-plan only. No product-repo planning artifacts.
- No VM containers/compose started on this host. Clean temp state removed.
- No orphaned containers/compose: none started (config-only + unit fix; no engine).

## END

<END_DONE mission-165-r2.md: 0427-165 round-2 (branch 0427-165-target-delete-orphanrec @ a14cf361, parent cbc9e1a8): F1 refusal text restricted to collectable-only path (`app destroy --uuid` clause removed — unwired per `baha app destroy --help`); F2 CollectableOrphans enforces decode-uuid==foldername (mismatch excluded from collectable set, fail-closed still refuses ownerless Target); fixture corrected to matching UUID + mismatch-regression test TestTargetDeleteRefusalIgnoresUuidFolderMismatch/TestCollectableOrphansRejectsUuidFolderMismatch added; Validation group (go-build/vet/unit/deployment-package/cli-gofmt) + go-unit-tests green in CI; 3 failures = pre-existing Native Keycloak/Core (172 PARK, witnessed failing on unmodified PR head cbc9e1a8) + group gate — delta touches no native path; evidence to origin/main before END; no .github/**; no subagents>
