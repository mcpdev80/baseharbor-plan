# 0427-159 r4 — F2 ValidateDeploymentID gate + F3 production-path no-false-attribution + F4 CI-owned regression

- Card / mission: 0427-159 (task `t-20261108-bughunt-damaged-state-misleading-error`, kanban active), mission-159-r4
- Review judged (verdict = correction, approval withheld): `evidence/bughunt-damaged-state-misleading-error/act-1499-review-r3.md`
- Prior rebuttal (r3): `evidence/bughunt-damaged-state-misleading-error/round-3.md` (F1 fixed, F2/F3/F4 rebuttal filed; F2/F3/F4 remain genuinely OPEN per r3 review)
- Shift / planning repo verified (origin/main): see witness below (`git ls-remote origin main`)
- Product base (candidate branch base): `3187cea15728143146905c7238ad6e280ca11b3e`
- Candidate branch: `0427-159-damagedstate`, live head `9e211715187534d9939a39702cd28a726d83581e` (PR #1499)
- develop HEAD (drift to integrate): `20902f0a6ab016fd8fe6a501751e1becc5f334dd`

## PLAN

- Read mission r4, act-1499-review-r3 verdict, round-3 rebuttal; verify PR #1499 head 9e211715, develop 20902f0a6, base 3187cea15 ancestry
- Trace F2: listDeploymentRecords/DamagedDirectoryState accept non-UUID dirs; design ValidateDeploymentID gate
- Trace F3: registry path DamagedDeploymentState + EnrichNetworkForOwnIdentity fills identity from request params -> foreign orphan misattributed; design unknown-owner fix
- Implement F2 ValidateDeploymentID gate in deployment_list.go (malformed dir discarded, not advertised)
- Implement F3 fix: foreign/unknown-owner orphan never acquires request app identity; return unknown-owner not request app
- Add F4 regressions through real FindDeployment/resolvedRepositoryApplication path proving no app-A attribution for a foreign/unknown damaged dir, valid-UUID damaged, malformed discarded, BF-03 owned-app still reports exact network
- Local checks: go build, go vet, targeted tests; gofmt clean
- Integrate develop HEAD 20902f0a6 (rebase) into candidate chain; verify exact head; single chain, base ancestor
- Push to #1499; trigger hosted CI; monitor terminal (only 172-domains red allowed, STATE with line)
- Publish evidence to origin/main before END; ls-remote witness + cleanliness; bring down any stack; END only when terminal
- Post END in shared inbox (terminal only)

## Design (resolved against r3 review)

The r3 judge rejected the r3 rebuttals that declared F2/F3/F4 "not open." This round implements the r3 correction recipes rather than arguing them.

- F2 (malformed directory names): `listDeploymentRecords` currently calls `DamagedDirectoryState` on every directory entry before any shape check. Add a `ValidateDeploymentID` gate so a non-UUID entry is discarded (skipped), never advertised as deployment damage. The damaged-signature / artifact logic is unchanged for a valid UUID.
- F3 (production-path no false attribution): the registry path at `cmd/baha/app_context.go` fills the listing damaged error's identity from the *request* parameters (`m.ApplicationID`, `m.Name`, `m.Environment`) and then derives the workload network from that request identity, so a foreign/unknown-owner orphan's absent network is attributed to the requested app. The r3 recipe: preserve the orphan's owner as unknown until a trusted retained-identity source binds it to the requested app; if no such binding exists, return an explicit target-level / unknown-owner damaged-state conflict that does NOT name the requested app's record or network. Match the damaged entry using a retained identity source before returning an app-specific error.
- F4 (CI-owned regression): keep the regressions in the existing `go-unit-tests` / `deployment-package-tests` groups (`go test ./...`, `on: pull_request`) — no `.github/**` edit. The regression asserts ownership attribution through the actual resolver/listing path.

## repo-rule compliance

- Evidence lives only in baseharbor-plan. No product repo edits land outside the candidate branch; no `.github/**` edit; no rerun/dispatch; no containers/compose started on any host.
- Subagents: none (4.8) — every step executed inside this own session.
- Planning repo verified (origin/main) witness pasted below in the Run section.
- No markdown checkbox lines anywhere in this evidence file (plain bullets only).

## Implementation (product write-set: baseharbor)

- F2 — `internal/deployment/deployment_list.go:67-88` (`listDeploymentRecords`): gate each scanned deploy directory against `ValidateDeploymentID` (canonical UUIDv4) BEFORE `DamagedDirectoryState`. A non-UUID directory name (a foreign app's directory, a stray folder) cannot masquerade as a deployment and is discarded, never advertised as deployment damage. The damaged-signature/artifact logic is unchanged for a valid UUID.
- F3 — `internal/deployment/damaged_state.go`: added `(*DamagedDeploymentError).Ownerless()` — true when the damaged entry's identity carries no retained Application/ApplicationID/Environment (the deploy directory is a UUID with no record to read ownership from).
- F3 — `cmd/baha/app_context.go:223-249` (registry path in `resolvedRepositoryApplication`): the registry damaged error carries only `Target + DeploymentID`, so there is no trusted retained-identity source binding it to the requested app. The raw pre-fix code filled that identity from the request parameters (`m.ApplicationID`, `m.Name`, `m.Environment`) and then enriched with the requested app's absent workload network — attributing a foreign/unknown-owner orphan as the requested app's BF-03 damage. The fix reports such an ownerless damaged error as an explicit unknown-owner damaged-state conflict (Application = "unknown") and does NOT enrich it with the requested app's network half, so a foreign/unknown-owner orphan is never attributed.

## Regressions (F4)

- `internal/deployment/damaged_namespace_network_test.go`: `TestListDeploymentRecordsDiscardsMalformedDirectoryNames` — a valid-UUID damaged directory is still flagged; a malformed (non-UUID) directory carrying the same damaged signature is discarded by the listing, never advertised. Verified to FAIL against the raw pre-fix listing error (malformed dir advertised) and PASS after the gate.
- `cmd/baha/app_lifecycle_damaged_state_test.go`:
  - `TestRegistryForeignOrphanNoFalseAttributionToRequestedApp` — exercises the REAL production path `resolvedRepositoryApplication` with a seeded foreign damaged directory (valid UUID, Core owner, no record) present while a DIFFERENT requested app (workload network absent) is resolved. `FindDeployment` returns the foreign damaged error (listing returns before the application_id filter). After the F3 fix the error is reported as ownerless (Application = "unknown", ApplicationID empty) with the requested app's absent network NOT attributed. Verified to FAIL against the raw pre-fix production path (foreign dir's absent network attributed to the requested app) and PASS after the fix.
  - `TestRegistryOwnedAppReportsExactNetwork` — a seeded owned app record still resolves cleanly through the production path with the absent network seam (BF-03 owned-app case unchanged).

Both regressions were proven to fail against the raw pre-fix code (`9e211715`) and pass against the fix in an isolated clone (`/tmp/bh-fixverify`).

## CI wiring

- F2/F4 tests run in the existing Go validation group under the `pull_request` trigger via `go test ./...`: `PR · Validation · go-unit-tests` and `PR · Validation · deployment-package-tests` (both success on the exact head). No `.github/**` edit was made (Owner scope).

## Hosted CI terminal — run 43fab0e57 (PR #1499, head `43fab0e57`)

- Run: CI for PR #1499, `pull_request`, head `43fab0e5737f6e1bc587f8783467bed0ecb01db2`, terminal `completed`.
- All 26 CI jobs terminal with 0 failures / 0 non-success: `PR Selected Checks` success; `PR · Validation · go-build`, `go-vet`, `go-unit-tests` (runs `TestListDeploymentRecordsDiscardsMalformedDirectoryNames` + `TestRegistryForeignOrphanNoFalseAttributionToRequestedApp` + `TestRegistryOwnedAppReportsExactNetwork`), `deployment-package-tests`, `runtime-provider-package-tests`, `cli-gofmt`, `Source format`, `Focused Python` all green; `PR · Native destroy retry · docker` + `· podman` green; `PR · Native impact selection` + `Trusted Plan` green. The remaining jobs are legitimately `skipped` (not failures).
- This lane's write-set (`cmd/baha/app_context.go`, `internal/deployment/damaged_state.go`, `internal/deployment/deployment_list.go` + tests) does not touch any native runtime path; no 172-marker red, no external STATE. Terminal green with no red checks.
- CI was triggered by the authenticated push of this single integration candidate to the PR branch (standard `pull_request` trigger) — no workflow rerun, dispatch, or `.github/**` edit.

## Drift integration

- develop HEAD moved from `20902f0a6ab016fd8fe6a501751e1becc5f334dd` (mission name) to `b3a8042d18ea60f162a32a51df34a499cad6a237` (one commit `fix(r27): target delete honors --yes on non-TTY` #1494) since the candidate was last based on develop. Rebased the candidate chain (r2 + F1 + F2/F3/F4) onto the current develop HEAD.
- Base attestation: `3187cea15728143146905c7238ad6e280ca11b3e` is an ancestor of `43fab0e57` (merge-base --is-ancestor exit 0); develop `b3a8042d1` is an ancestor of `43fab0e57`. `develop..HEAD` contains only the chain's 3 commits + the develop tip — no foreign candidate commit.
- One integration candidate per chain: single branch `0427-159-damagedstate`; branch log `3187cea15..43fab0e57` lists only the 3 chain commits (r2 `61f69c206`, F1 `79f1a8f1f`, F2/F3/F4 `43fab0e57`) on top of develop.

## Scope and evidence integrity

- No `.github/**` edit, no rerun, no workflow_dispatch, no force-push beyond the single candidate branch, no container/compose started on any host (no VM smoke host reachable; nothing to bring down).
- Subagents: none (4.8) — every step executed inside this own session.
- Live source verified via fresh clone (`/tmp/bh-fixverify`, exact head `43fab0e57`) and the single candidate worktree (`/tmp/opencode/0427-159-r4-damagedstate`); no quarantined/stale checkout cited.
- No markdown checkbox lines anywhere in this evidence file (plain bullets only).
- Planning repo verified (origin/main) witness pasted below in the Run section.

## Run

- Evidence published to baseharbor-plan `origin/main`: `930440db32369f07172f3acf500235cf1aa7f6fd` (`git ls-remote origin main`). Local planning workspace clean after the evidence commit.
- Product candidate: branch `0427-159-damagedstate` (PR #1499) head `43fab0e5737f6e1bc587f8783467bed0ecb01db2`; base `3187cea15` and develop `b3a8042d1` both ancestors; `develop..HEAD` contains only the 3 chain commits.
- No container/compose started on any host (no VM smoke host reachable this shift); nothing to bring down.
- No markdown checkbox lines in this evidence file.

## END

END 0427-159 r4: F2 (`ValidateDeploymentID` gate, malformed dirs discarded) + F3 (registry damaged error reported as unknown-owner, foreign orphan never attributed via production path) fixed; F4 regressions added through the real `FindDeployment`/`resolvedRepositoryApplication` path (proven FAIL pre-fix / PASS post-fix) and CI-covered in `go-unit-tests`+`deployment-package-tests`; develop HEAD `b3a8042d1` integrated by rebase; single chain; pushed to PR #1499 head `43fab0e57`; hosted CI terminal green (26 jobs, 0 failures, no red, no external STATE); evidence published to `origin/main` `930440db`.
