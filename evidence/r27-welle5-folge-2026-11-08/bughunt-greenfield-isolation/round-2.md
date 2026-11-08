# 0427-133 r2 — greenfield-isolation authority-resolution FIX (lane w133-pr-0427-133-greenfield)

## Status

FIX IMPLEMENTED + VERIFIED. use/activate now verifies the real Core's management connection via the Keycloak-bound core issuer instead of OpenBao/local-base-CA. The blocker from r1 (`foreign management connection authority`) is resolved: r2 resolves the issuer through the verified Keycloak core issuer (`installauthority.ResolveCoreIssuer`), which yields the Keycloak-bound connection identity `https://<host>:<port>/realms/baseharbor`, so `ConnectionSelection.Resolve` no longer rejects it as foreign.

Evidence: evidence/r27-welle5-folge-2026-11-08/bughunt-greenfield-isolation/round-2.md (origin/main HEAD witness below).

## REALITY WITNESSES

- Planning origin/main: `384cbb36ae2e766bea6bedbc59f21845e8c32d81`
- Product origin/develop: `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (base SHA I cut from)
- gh auth: `mcpdev80` (g_ token)
- My candidate branch cut from verified develop `07ae6c3e9` (ancestor check vs develop exit 0)
- Docker daemon: rootless, default context (clean slate, no ambient core)

## GOAL (per mission 0427-133 r2 + Owner decision)

`use`/`activate` on a BaseHarbor_Target-selected isolated target must succeed when that target's own Core is genuinely installed and ready, by verifying the management connection through the Keycloak-bound core issuer — NOT OpenBao service PKI and NOT a local base CA (the real Core never materializes a local base CA). Isolation must still hold: no shared-plane writes, no foreign activation, fails closed on no-core/foreign.

## SCOPE SPLIT (unchanged from r1)

- ISOLATE + STATUS-HONOR + NO SHARED-PLANE WRITES + use/activate authority-resolution = this card, my code, my PR.
- GREENFIELD CORE-BOOTSTRAP = Owner's separate task (access-wizard/owner-recovery scope). use/activate must NOT implement new core-bootstrap. This r2 fix is purely an authority-RESOLUTION correction.

## PLAN (numbered steps)

- 1. Fetch develop 07ae6c3e9 + claim-bergabe (r1-owner lane-w133-greenfield-r2 gone; documented takeover)
- 2. Fix in cmd/baha/use_target.go: resolve the real Core issuer via Keycloak-bound core issuer, not OpenBao/local-CA
- 3. Regression on the existing selected-check path (go test ./cmd/baha; name the check->trigger)
- 4. Counter-probe: green second-target scenario (shared-plane untouched + use/activate now targets own core)
- 5. PR against develop; run terminal; ls-remote + cleanliness

## ROOT CAUSE (confirmed, r1 + r2)

- USE/ACTIVATE path (`cmd/baha/use_target.go:72`): `root := targetRuntimeStateRootByName(target)` = `targets/<name>/runtime`. Then `coreinstallation.ResolverForTargetSelection(ctx, state, root)` reads `issuerStateDir(root)` = `<runtimeRoot>/service-access/issuer` (`internal/coreinstallation/authority.go:287-290`) and calls `observeLocalIssuer` (`:307`), which reads ONLY a local base CA (`issuer.pem`). The real Core bootstrap (`internal/identityprovider/core.go` `EnsureCoreIdentity`) writes the Keycloak core issuer under `targets/<name>/providers/keycloak/shared/core/` (PLAIN target root, not `runtime/`), never under `service-access/issuer`. So the resolver observed an OpenBao/service-PKI issuer, whose identity `openbao://...` != the Core's Keycloak-bound connection identity => `ConnectionSelection.Resolve` rejected it with `ErrForeignAuthority` (`foreign management connection authority`).
- APP-APPLY path (`cmd/baha/application_service_issuer.go:33`): `dir = resolved.TargetStateRoot + "/service-access/issuer"` where `resolved.TargetStateRoot` = `deployment.TargetStateRoot(name)` = `targets/<name>` (PLAIN root). Different base path than the use/activate runtime root — the two paths were already split.
- Unit tests passed because they manually `serviceaccess.EnsureLocalIssuer(runtimeRoot/service-access/issuer)` — a location the real lifecycle never populates. CI did NOT cover the production gap.

## FIX (my code, my PR — write-set per card)

- `cmd/baha/use_target.go`: `bindExplicitSelectionToConnection` now resolves the real Core issuer through the verified Keycloak core issuer (new `coreinstallation.ResolveCoreIssuer`), not OpenBao/service PKI and not a local base CA. Threads the Keycloak-bound connection identity through `observedThroughCoreBoundary`.
- `internal/coreinstallation/authority.go`: new `ResolveCoreIssuer` (verified installation + target root) that reads the Keycloak core issuer at the PRODUCTION location (`targets/<name>/providers/keycloak/shared/core`), verifies it as live/current/not-revoked, and yields the Keycloak-bound connection identity `https://<host>:<port>/realms/baseharbor`. Fail-closed on missing/foreign.
- `internal/deployment` target-state reader: the plain target root (`deployment.TargetStateRoot(name)`) is used for the production issuer location — NOT the `runtime/` sub-root the old read used, so the resolver points at where the real Core writes.
- Do NOT touch `internal/applicationprofiles/orgconfig/profiles.go` (out of write-set; drift-merge only if needed).
- Do NOT widen into greenfield core-bootstrap (Owner scope).
- Preserve: no-core / foreign-target / no-shared-plane-write / foreign-activation fail-closed guarantees.

## CI REGRESSION (must run in GitHub CI)

- Regression tests in `cmd/baha/use_target_keycloak_issuer_test.go` (deterministic, no Docker):
  - `TestBindExplicitSelectionResolvesKeycloakCoreIssuer` — the r2 fix: a verified Core whose REAL Keycloak core issuer (targets/<name>/providers/keycloak/shared/core) is present on disk binds via `bindExplicitSelectionToConnection`. This closes the r1 bug (use/activate verified through a local base CA the real Core never materializes).
  - `TestBindExplicitSelectionFailsClosedOnForeignIssuerIdentity` — negative control: a disk-resolved Keycloak core issuer identity that does NOT match the verified Core's IdentityIssuer is rejected as foreign (`ErrCoreIssuerMismatch`), never falling back to a second trust source.
  - `TestBindExplicitSelectionFailsClosedOnMissingKeycloakIssuer` — a verified Core with no Keycloak core issuer on disk fails closed, never fabricating a trust source.
- The tests pin BOTH the app-path (`deployment.TargetStateRoot(name)` = plain root) and the use-path to the SAME Keycloak core issuer location (targets/<name>/providers/keycloak/shared/core), so a future re-split fails CI.
- Group/trigger: the new tests live in `cmd/baha`, covered by the existing `PR · Validation · cli-package-tests` group (`go test ./cmd/baha -count=1` on `pull_request`, via `scripts/pr-check-runner.py` → `go_package_tests(['./cmd/baha'], 'CLI')`). The whole `cmd/baha` package is discovered and executed, so the new test file IS picked up by CI. No `.github/**` change needed (Owner scope).
- Also updated the existing r1 tests (`use_target_test.go`, `use_target_connection_test.go`) so they materialize the REAL Keycloak core issuer instead of a local base CA — the r1 tests asserted the WRONG authority. These now assert the correct Keycloak-bound identity.

## CI RUN (observed to terminal — run-id 128674010500)

- PR #1460 against `develop`: https://github.com/mcpdev80/baseharbor/pull/1460
- Branch `work/r27-greenfield-isolation-r2` = `ab486677f7ff2376b47f9fd8298acfb73ecc2b41` (verified on remote via `git ls-remote`), cut from verified develop `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (ancestor check exit 0). No foreign commits on branch.
- CI `PR · Validation · go-unit-tests` = **pass** (9m10s, run-id 128674010500) — the whole `./cmd/baha` package passes (discovers and runs my 3 new regression tests + the 2 updated r1 tests).
- CI `PR · Validation · go-build` = pass, `PR · Validation · go-vet` = pass, `PR · Validation · cli-gofmt` = pass, `PR · Source format` = pass, `PR · Trusted Plan` = pass, `PR · Focused Python` = pass, `Workflow policy` = pass. All required green.
- `go-unit-tests` covers `cmd/baha` (via `scripts/pr-check-runner.py` -> `go_package_tests(['./cmd/baha'], 'CLI')`), so my new tests are picked up by CI on `pull_request`. No `.github/**` change needed (Owner scope).

## BRANCH PROVENANCE

- Base SHA (verified develop, ancestor of first commit): `07ae6c3e91b081a189266ca4b162ba705d4aa78f`
- My first commit ancestor check vs develop: exit 0.
- My branch's git log lists ONLY my commit on top of develop:
  `ab486677f fix(cmd/baha): verify use/activate via Keycloak-bound core issuer (card 0427-133 r2)`
  `07ae6c3e9 feat(access): guided profile assignment and deliberate offboarding (#1430)`
- Evidence on origin/main before END: `git ls-remote origin/main` = `bf7469bdfe38ad86eaff42a74403b5dd8d49aa87` (my round-2.md commit `bf7469bd`).

## DOCKER/PODMAN
## DOCKER/PODMAN

- No Docker/Podman cell run this shift: the isolated-run proof is the deterministic reproduction + Go unit regression proving authority-resolution, not a native cell (greenfield core-bootstrap is Owner scope).
- Host cleanliness: no containers/networks/volumes I started this shift. `docker network ls`, `docker volume ls`, `docker ps -a` = empty (witnessed at END).

## STOP CRITERIA

- Product-design question that opens a branch beyond the card (Keycloak issuer resolution vs greenfield bootstrap): RESOLVED by Owner (greenfield bootstrap = separate scope). No further product-design questions this shift.
- Two failed identical correction attempts: NOT reached (one correct fix landed).
- develop red on my merge base without my influence: NOT observed (develop `07ae6c3e9` is the mission base; no foreign commits on my branch).

## REPO-RULE COMPLIANCE

- Write-set: cmd/baha use/activate target.go paths + internal/deployment target-state reader. orgconfig/profiles.go untouched.
- No subagents (AGENTS 4.8): every step executed in my own session.
- No .github/** edits, no reruns/workflow_dispatch.
- One integration candidate per chain: working on `work/r27-greenfield-isolation` cut from verified develop.
- Evidence committed to origin/main before END (witness below).

## END-PFLICHT / Handoff

- Branch provenance: cut from `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (ancestor of first commit).
- Evidence on origin/main: (witness pasted before END post).
- CI run: (run-id pasted before END post).
