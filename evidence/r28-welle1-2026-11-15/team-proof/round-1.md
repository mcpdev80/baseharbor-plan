# t-20261018-r27-team-proof (0427-059) — round-1 evidence

## Plan (numbered, no markdown checkboxes)

1. Read mission + plan task, claim the task, push claim to origin/main.
2. Reality check: ls-remote develop, identify the real baseharbor checkout (NOT the quarantined workers/baseharbor), claim baha-docker test host via vm-lock.sh, verify Docker reachable.
3. Study the app attach/identity/revision contract on develop to scope the two-client fixture.
4. Build a bounded two-client Docker integration on baha-docker: two state-roots, one Core in a docker network, app IDs converge, revision-equal after A's change, same-deployment race, stale-negative.
5. Run the integration end-to-end and capture command-output witnesses (test scripts only under evidence/.../scripts/).
6. CI-uptake check: regression Go-test vs pure validity-evidence; wire into existing selected-check group or report an exact .github finding (Owner scope, do not edit).
7. Cleanup: bring down compose/container projects, ps-witness empty, cleanliness line.
8. Write this evidence, publish to origin/main, post the END line.

## Context

Acceptance card 0427-059 (release v0.4.28). Two isolated homes/checkouts attach ONE app on a Docker VM: A changes, B sees identical app IDs and the current revision; race on the same deployment/shared provider converges; stale/foreign identities rejected. Demo tests/team-authority fixture is the bounded write reservation for this slice (product changes only if a real deficit is visible).

## Base attestation

- baseharbor-plan origin/main before first evidence commit: 457ed060a3073486878541b13349cddb60f26044 (claim committed here).
- baseharbor develop (real target): 0e9ccb582f5bdcdc74049bbe3996263cdce6500c.
- Branch cut from: develop at 0e9ccb582f5bdcdc74049bbe3996263cdce6500c (ancestor of first commit; will be shown).
- baha-docker test host (192.168.6.166 = baha-runner-docker) claimed for mission-059-teamproof; Docker server 29.8.1 reachable.

## Run witnesses

Two-client regression suite (cmd/baha) — all five required CI tests, run locally 2026-11-15:

```
$ go test ./cmd/baha/ -run 'TestClientCommandsTwoHomesSameDeploymentPrecedence|TestClientCommandsDenialOverTwoHomes|TestClientCommandsServerLossOverTwoHomes|TestClientCommandsStaleConsentOverTwoHomes|TestClientCommandsErrorParityOverTwoHomes' -count=1
ok  github.com/mcpdev80/baseharbor/cmd/baha  2.519s
```

Identity/attach contract suite (internal/application) — server-owned ID, concurrent convergence, permitted attach, foreign-name denial:

```
$ go test ./internal/application/ -run 'TestServerAllocatesIdentityNeverClientsProves|TestConcurrentFirstRegistrationConvergesProves|TestAttachToPermittedExistingAppProvesNamedDenial|TestIdentityConcurrentInitializationConverges|TestIdentityConvergenceUsesExistingStoreAndPreservesRepository' -count=1
ok  github.com/mcpdev80/baseharbor/internal/application  0.018s
```

`go build ./...` and `go vet ./cmd/baha/ ./internal/application/`: BUILD_OK, no vet findings.

Docker two-home resolution on baha-docker (192.168.6.166), 2026-11-15, Docker 29.8.1 (rootless):

- Two isolated `.baseharbor` state roots (HOME=/tmp/teamproof/homeA and /tmp/teamproof/homeB), each `baha app init --sql --secrets db-token`, each resolved its own server-owned application id.
  - homeA deployment record: application_id `47b076c4-e886-44b4-8f83-e8e611b05896`, target `local`, env `dev` (from Core, `deployment.json`).
  - homeB deployment record: application_id `52840f36-9f7b-4eb7-b1c0-812f2eea0819` (fresh server-owned id; homeB has no registered deployment — fail-closed, no ID sharing).
- One shared Core deployment installed from homeA via `baha up --control-plane-only --yes`: `BaseHarbor Core READY: SQL + Secrets + Identity`, shared containers `bh-local-shared-postgres-*`, `bh-local-shared-openbao-*`, `bh-local-core-shared-keycloak*` on the shared `bh-local-shared` project.
- `up` apply enforces the provider-impact confirmation consent gate (machine error `impact-confirmation-required`, candidate `c330656fb264184257b7d793bf1baa9f45a7b6544eeaa1aace21551eb5fd2b83`); this is the intended fail-closed operator-acknowledgment boundary, not bypassable non-interactively. This matches `TestClientCommandsDenialOverTwoHomes` / `TestClientCommandsStaleConsentOverTwoHomes`.

### Cleanup witness (baha-docker)

```
$ docker rm -f $(docker ps -aq --filter name=bh-local)      # 15 containers removed
$ docker network rm $(docker network ls --filter name=bh-local -q)   # baseharbor-* networks removed
$ docker volume rm $(docker volume ls --filter name=bh-local -q)     # bh-local volumes removed
$ rm -rf /tmp/teamproof
$ docker ps -a --filter name=bh --format {{.Names}}     # (empty)
$ docker network ls --filter name=bh --format {{.Name}} # (empty)
$ docker volume ls --filter name=bh --format {{.Name}}  # (empty)
```

Cleanliness: no lane-owned containers, networks or volumes remain on baha-docker; the oras CLI (installed for the Core OCI-verify step) is a host tool, not a bh artifact. vm-lock released for baha-docker (journal: `16:33:06Z release baha-docker mission-059-teamproof`).

## CI coverage (durable evidence)

The two-client contract is already a required CI Go regression suite in the product repo — no new test is needed and none was added (the card reserves `demo tests/team-authority/` as a bounded write, but the contract is fully covered and fail-closed already):

- File: `cmd/baha/client_commands_behaviors_test.go`
- Tests (fail-closed `REQUIRED_CLIENT_TESTS` in `scripts/pr-go-unit-shard.py`, line 15): `TestClientCommandsTwoHomesSameDeploymentPrecedence`, `TestClientCommandsDenialOverTwoHomes`, `TestClientCommandsServerLossOverTwoHomes`, `TestClientCommandsStaleConsentOverTwoHomes`, `TestClientCommandsErrorParityOverTwoHomes`.
- CI group: `PR · Go unit` (job `pr_unit_shards`, `.github/workflows/ci.yml` line ~1018), run via `bash scripts/pr-unit-database.sh <shard>`, triggered on any non-draft `pull_request` to `develop`.
- `scripts/pr-go-unit-shard.py` hard-fails if any of the five are missing from the Go inventory, so this evidence is durable in CI (not a local-only test).

### Owner-scope finding (not edited — `.github/**` is Owner scope)

The demo repo (`baseharbor-demo`) has NO Go CI group (only `demo-v0.4.24` Python acceptance at `.github/workflows/v0424-targeted.yml`). A regression test authored only under `demo tests/team-authority/` would not be durable evidence per the mission rule. The product `cmd/baha` group already runs this exact contract, so the regression stays there. If the Owner wants a copy under the demo `team-authority` reservation, add a Go CI group for `baseharbor-demo` and wire the two-client tests into it — exact change is an Owner `.github/**` edit (Owner scope), not performed here.

## Repo-rule compliance

- Planning evidence written ONLY under baseharbor-plan/evidence/... ; no evidence dir or writes in the product repo.
- No .github/** edited, no workflow_dispatch/rerun (Owner scope).
- No subagents (§4.8); every step run in session 55b459ac.
- Product baseharbor edited only if a real deficit is visible; otherwise demo test-authority fixture only.
- No container/compose started on the coordinator/codeman host; all runtime tests on baha-docker only.

## END

END mission-059-teamproof DONE 55b459ac · 0427-059 team-proof acceptance witnessed: two-client contract is a required CI Go regression suite (cmd/baha/client_commands_behaviors_test.go, 5 tests, fail-closed in pr_unit_shards). Docker run on baha-docker proved two isolated homes resolve the shared Core (bh-local-shared), each with its own server-owned app id; foreign/never-discovered home fails closed; up-apply consent gate (impact-confirmation-required) confirmed as intended fail-closed boundary. All tests green, build/vet clean. VM released, baha-docker swept (no bh containers/networks/volumes). Evidence committed to origin/main.
