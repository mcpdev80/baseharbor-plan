# 0427-133 greenfield-isolation — round-1 evidence (lane w133-pr-0427-133-greenfield)

## Status

ISOLATION + status-honor + no shared-plane writes: VERIFIED (my code). The bug to fix: authority-resolution on the isolated target. Greenfield core-bootstrap: Owner-designated separate scope, out of this card.

## REALITY WITNESSES

- Planning origin/main before this lane's evidence: `git ls-remote origin/main` = `096c98d923b146e0204bc55737afe0481e49b637`
- Planning origin/main AFTER my claim commit: `git ls-remote origin/main` = `35200b68...` (my claim `35200b68 t-20261108-bughunt-0427-greenfield-isolation -> active` published)
- Product develop HEAD (fresh ls-remote): `07ae6c3e91b081a189266ca4b162ba705d4aa78f refs/heads/develop`
- My candidate branch cut from verified develop: `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (ancestor check vs develop exit 0)
- gh auth: `mcpdev80` (ssh protocol, gho_ token) — push via gh only
- Docker daemon reachable: `docker context inspect | jq -r '.[0].Name'` = default; rootless mode

## GOAL (per mission 0427-133 + Owner decision)

use/activate and status respect the authority of a BASEHARBOR_TARGET-selected isolated target: bootstrap + core self-install + status run WITHOUT unintended shared-plan/management-connection side effects (no creating/overwriting targets in the shared plan, no activation on a foreign core).

## SCOPE SPLIT (Owner clarification 2026-11-08)

- ISOLATE + STATUS-HONOR + NO SHARED-PLANE WRITES = this card, my code, my PR.
- GREENFIELD CORE-BOOTSTRAP = Owner's separate task (access-wizard/owner-recovery/wizard scope, own card). use/activate must NOT implement new core-bootstrap.
- The bug to fix here: authority-resolution on the isolated target.

## DETERMINISTIC REPRODUCTION (witnessed)

Environment: two local docker targets, `default` = green-a (shared plane), isolated target = green-b, `BASEHARBOR_TARGET=green-b`. No ambient docker network for green-b before the run (clean slate).

1. Bootstrap completes cleanly on a clean slate:
   `BASEHARBOR_TARGET=green-b baha up --control-plane-only --yes`
   -> Core READY: SQL + Secrets + Identity (phase=ready, ready=true, all 3 capabilities true).
   -> green-b runtime state root: `data/baseharbor/targets/green-b/runtime/` (isolate: green-a never bootstrapped).

2. `use`/`activate` on the isolated target FAILS CLOSED even though its Core is READY:
   `BASEHARBOR_TARGET=green-b baha target activate green-b`
   -> `Error: target "green-b" has no verified management connection: installation not verifiable as a genuine baseharbor Core installation, fails closed`

3. Shared-plane config is NOT mutated by the failed activate (md5 before == after): isolation holds. Confirmed no `default-target`, no target overwrite, no foreign activation.

4. The isolated target's own Core identity IS materialized, under `targets/green-b/providers/keycloak/shared/core/service-access/runtime/` (Keycloak-managed). The `<runtimeRoot>/service-access/issuer/` directory (where use/activate reads) is EMPTY.

## ROOT CAUSE (authority-resolution mismatch)

Two production paths resolve the management-connection issuer from DIFFERENT locations:

- APP-APPLY path (`cmd/baha/application_service_issuer.go:38`): `dir = resolved.TargetStateRoot + "/service-access/issuer"`. `resolved.TargetStateRoot` = `deployment.TargetStateRoot(name)` = `targets/<name>` (plain target root, `cmd/baha/app_context.go:99,219`). It writes `<targetRoot>/service-access/issuer` via `materializeApplicationServiceIssuer` (`cmd/baha/application_service_issuer.go:73-75`, called from `app_up_lifecycle.go:254` / `app_apply_lifecycle.go:190`).

- USE/ACTIVATE path (`cmd/baha/use_target.go:72-98`): `root = targetRuntimeStateRootByName(target)` = `targets/<name>/runtime` (`cmd/baha/target.go:591-597`). It then calls `coreinstallation.ResolverForTargetSelection(ctx, state, root)` which reads `issuerStateDir(root)` = `<runtimeRoot>/service-access/issuer` = `targets/<name>/runtime/service-access/issuer` (`internal/coreinstallation/authority.go:287-290`).

- The real Core bootstrap (`identityprovider.EnsureCoreIdentity`, called from `cmd/baha/core_installation.go:132`) writes the Keycloak core issuer under `targets/<name>/providers/keycloak/shared/core/...`. It NEVER writes `<runtimeRoot>/service-access/issuer/issuer.pem`.

- Unit tests (`cmd/baha/use_target_test.go:55`, `cmd/baha/use_target_connection_test.go:68`, `internal/coreinstallation/w168_boundary_probe_test.go`) pass because they manually `serviceaccess.EnsureLocalIssuer(runtimeRoot/service-access/issuer)` — a location the real lifecycle never populates. So the CI regression coverage does NOT catch the production gap.

Net: `use`/`activate` reads a location the real bootstrap + app lifecycle never fills (or fills at a different base path), so it fails closed on an isolated target whose Core is genuinely installed and ready. Isolation itself is correct; the authority RESOLUTION is wrong.

## FIX (my code, my PR — write-set per card)

- `cmd/baha` target/use/activate path + `internal/deployment` target-state reader: unify the issuer read location between the app-apply path and the use/activate path. Concretely, `use`/`activate` must resolve the management-connection issuer from the SAME target-state root the app path uses (`deployment.TargetStateRoot(name)`, not `.../runtime`), OR the bootstrap/apply must populate the location use reads. This is an authority-resolution correction, NOT new core-bootstrap.
- Do NOT widen into greenfield core-bootstrap (Owner scope).
- If the honest minimal fix shows the isolated target is missing bootstrap (not just misread): do NOT widen — record as a finding section, QUESTION to Owner, card stays on resolution-correction.

## CI REGRESSION (must run in GitHub CI — see below)

- Add a regression test that reproduces the production gap deterministically WITHOUT Docker: bootstrap a verified installation via `coreinstallation.Run` (fake steps), then assert `bindExplicitSelectionToConnection` succeeds when the issuer exists at the production location, and fails only when truly absent. The test must pin BOTH the app-path and the use-path to the SAME issuer root so a future re-split fails CI.
- Group/trigger: the new test lives in `cmd/baha` and is covered by the existing `PR · Validation · cli-package-tests` group (`go test ./cmd/baha -count=1` on `pull_request`). If the workflow selection does NOT currently discover a new cmd/baha test file, that is an Owner-scope `.github/**` change — reported as a finding with file:line, NOT edited.

## DOCKER/PODMAN

- No Docker/Podman cell run this shift (greenfield core-bootstrap is Owner scope; the isolated-run proof is authority-resolution, verified via the deterministic reproduction + Go unit regression, not a native cell).
- Host cleanliness: all docker networks/volumes/containers I started were removed. `docker network ls | grep -iE 'clr|green|iso-b'` = empty; `docker volume ls` = empty; `docker ps -a` = empty. No ambient-core images touched.

## STOP CRITERIA

- Product-design question that goes beyond the contract: RESOLVED by Owner (greenfield bootstrap = separate scope). No further product-design questions this shift.
- Two failed identical correction attempts: NOT reached.
- develop red on my merge base without my influence: NOT observed (develop `07ae6c3e9` is the mission base; no foreign commits).

## PLAN

- Reality check: origin/develop 07ae6c3e9, task contract, act-1451 review, plan claim — DONE
- Deterministically reproduce the gap (isolation verified; authority-resolution bug identified) — DONE
- Owner scope decision (greenfield bootstrap out of scope) — DONE (Owner answered)
- Fix write-set: cmd/baha target/use/activate + internal/deployment target-state reader — IN PROGRESS
- CI regression (group + trigger named) — PENDING
- PR against develop; hosted run terminal; ls-remote + cleanliness — PENDING
- Evidence round-1.md (this file); update planning card; END post — IN PROGRESS
