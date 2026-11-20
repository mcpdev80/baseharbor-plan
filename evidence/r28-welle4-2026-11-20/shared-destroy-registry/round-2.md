# 0428-184 — shared destroy skips registry cleanup (round-2)

- Mission: `/var/tmp/mission-184.md`
- Card: `t-20261120-r28-shared-destroy-no-registry-cleanup` (0428-184), Release v0.4.28
- Owner: `w184-0428-184-shareddestroy`
- Role: WORKER (codeX merge-halt correction, PR #1715)
- Datum: 2026-11-20
- Worktree: `/tmp/opencode/lane-0428-184-shared-destroy`, branch `lane-0428-184-shared-destroy`
- PR: `#1715` head `bc4df42d38bd15e0eb97f7ab9398133a0c742b50`, base develop

## PLAN

1. Verify branch provenance (develop-spitze ls-remote, ancestry, own-commit-only diff, PR-head ls-remote)
2. Confirm terminal CI run #44748241522 conclusion at exact head bc4df42d via the Actions API
3. Write round-2.md with the three witnesses + terminal-run conclusion + the one line attributing the two red cells to card 0428-187
4. Commit evidence to baseharbor-plan main, verify 0 checkboxes + presence on origin/main
5. Post END

## Fix (unchanged from round-1)

`PruneOwnedPlatformSources` (registry.go, new function only; `registryPath` and the `RegisterProviderSignals` collision/owner guard untouched) removes exactly the platform-scoped observability rows for one `environment:<env>` boundary and preserves foreign-owner rows. `DestroyAllSharedBackendsAt` calls it for postgres + valkey per torn-down environment. Regression runs through the productive `RegisterProviderSignals` path for BOTH providers.

## Beweiszeilen (three witnesses)

- branch provenance (ls-remote, real remote `origin` = github.com/mcpdev80/baseharbor.git): `git ls-remote origin refs/heads/develop` → develop tip moved to `f5ce95afce1cfec053dd7717ed05e89bfe153535` since round-1 (a later lane merged); my head is still exactly `bc4df42d38bd15e0eb97f7ab9398133a0c742b50`.
- ancestry: `git diff origin/develop...HEAD --name-only` = only `internal/application/shared_backends_resources_runtime.go`, `internal/application/shared_backends_resources_runtime_test.go`, `internal/observability/registry.go`; `git log --oneline origin/develop..HEAD` = only my two commits `bc4df42d` + `c1485721` (no foreign commit carried on top).
- PR delivery: `git ls-remote origin refs/pull/1715/head refs/heads/lane-0428-184-shared-destroy` = `bc4df42d38bd15e0eb97f7ab9398133a0c742b50` for both refs.
- CI run #44748241522 (CI · Source & Quality, completed 14:10:54Z, head bc4df42d): **PR · Go unit · packages = SUCCESS** (13:56:05Z) — the shard that runs this test; PR · Go unit · cli-0/1/2/3, owner = SUCCESS; PR · Validation · go-build / go-vet = SUCCESS. Only the red gates are **PR · Selected Runtime (atomic/podman/data-capabilities, podman, data-capabilities) / Executed podman · data-capabilities = FAILURE** (job 136329866151, 14:10:39Z) and **PR Selected Checks = FAILURE** (14:10:54Z); the four failing lines are the candidate-consent podman data-capabilities pipeline (no-output timeout 239s/180s), identical to the previous head. Owner of that cell = card 0428-187 (session 425eb851). `ci-fast-check.sh` local on bc4df42d: all PASS, 293 tests OK.

## repo-rule compliance

- KEIN `.github/**` geaendert (owner-scope). KEIN `internal/application/perses_runtime.go` geaendert (0428-083). KEIN `registryPath` umbgebaut, KEIN target-uid/root-Feld eingefuegt (0428-078/186 owner schema field). KEIN Merge, KEIN Subagent (§4.8), KEIN `git add -A`.
- Write-Set: nur drei Produkt-/Testdateien; `registry.go` fuehrt nur die neue Funktion `PruneOwnedPlatformSources`, `registryPath` und `RegisterProviderSignals` unveraendert.
- Branch aus develop-spitze (ancestry gegen aktuellen develop-Spitzen-HEAD verifiziert, nur eigener Commit).
- Evidence in baseharbor-plan main (kein .evidence/ im Produkt, kein main-branch-write im Produkt).

## cleanliness

- Vorher: `docker ps -a` = leer; `docker network ls` = bridge/host/none; `docker compose ls -a` = keine projekte.
- Nachher: identisch. Diese Lane startete keine container/netzwerke/volumes/state-verzeichnisse; reine Go build/vet/test + git/gh/curl-arbeit, keine deployment/compose-aufrufe.
- cleanliness: these lanes starts no containers/networks/volumes/state-dirs; no compose project touched; ambient-core/ bilder fremder karren bleiben unangetastet.

## END

END_DONE mission-184.md (0428-184 shared destroy skips registry cleanup) — PR #1715 head bc4df42d (git ls-remote refs/pull/1715/head = bc4df42d38bd; ancestry gegen develop-spitze, diff nur 3 Dateien; PR delivery witness bc4df42d); CI #44748241522 terminal (head bc4df42d): Go unit packages SUCCESS, red gates = PR Selected Checks + data-capabilities runtime podman cell, beide aus karte 0428-187 (session 425eb851); PR #1715 body = kartennummer + head-sha + aktenpfad (REST PATCH, gh pr edit GraphQL-Fehler umgangen); evidence/r28-welle4-2026-11-20/shared-destroy-registry/round-2.md auf main 0 checkboxen; 0 container/netzwerke; KEIN .github, KEIN registryPath-umbau, KEIN target-uid/root.
