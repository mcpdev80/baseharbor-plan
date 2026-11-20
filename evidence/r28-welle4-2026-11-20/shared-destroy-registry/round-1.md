# 0428-184 — shared destroy skips registry cleanup (round-1)

- Mission: `/var/tmp/mission-184.md`
- Card: `t-20261120-r28-shared-destroy-no-registry-cleanup` (0428-184), Release v0.4.28
- Owner: `w184-0428-184-shareddestroy`
- Role: WORKER (bug fix + regression, PR #1715, base develop)
- Datum: 2026-11-20
- Worktree: `/tmp/opencode/lane-0428-184-shared-destroy`, branch `lane-0428-184-shared-destroy`

## PLAN

- [ ] Read task card, hunt akte 103 F3 + 104 F1, baseharbor/AGENTS.md; verify planning repo remote + develop HEAD
- [ ] Read 0428-166 hardening sites (`registry.go` collision guard, `provider_registration.go` guard, `runtime_observability.go:98`) and record the lines NOT touched
- [ ] Locate shared-destroy path `application.DestroyAllSharedBackendsAt` and confirm missing observability cleanup (the existing `PruneOwnedProviderInstances` filters by OwnerApplication, but platform-scoped shared sources key their lifecycle on the SharingBoundary)
- [ ] Add boundary-scoped `PruneOwnedPlatformSources` to `registry.go` (new function only; `registryPath` and `RegisterProviderSignals` guard untouched) and call it for postgres + valkey in the destroy path
- [ ] Regression via the productive `RegisterProviderSignals` path (real provider-kind, real `environment:<env>` boundary) for BOTH providers; owned removed + re-registration succeeds; foreign (other-env) preserved
- [ ] Verify both directions (RED without fix, GREEN with fix), gofmt, full `go build`/`go vet`, pre-existing suite unchanged
- [ ] Push PR #1715 (base develop 96f2ae11), run CI, capture run-id + terminal conclusion
- [ ] Write this evidence akte on baseharbor-plan main (0 checkboxes), post END

## Fix

`application.DestroyAllSharedBackendsAt` (`internal/application/shared_backends_resources_runtime.go`) tore down compose projects and local state per environment but never removed the platform-scoped observability source rows it registered during ensure. Platform-scoped shared postgres/valkey register with `Class: SourcePlatformProvider, Scope: ScopeShared, SharingBoundary: "environment:<env>"` through `RegisterProviderSignals`. The existing `PruneOwnedProviderInstances` filters by `OwnerApplication`, which platform-scoped rows do not carry, so the rows survived a destroy and a later re-registration of the same boundary saw a dead owner.

New `PruneOwnedPlatformSources(provider, class, scope, sharingBoundary, keepIDs)` (in `registry.go`) removes exactly the platform-scoped rows that share one `SharingBoundary` and preserves rows for any other `SharingBoundary` (fail-closed cross-tenant wipe guard). `DestroyAllSharedBackendsAt` now calls it for `PostgreSQLIntegration` and `ValkeyIntegration` per torn-down environment, after compose destroy and `os.RemoveAll`.

NOT touched (0428-166 owner field, card boundary): `registryPath` (`registry.go`), the `RegisterProviderSignals` collision/owner guard (`provider_registration.go`), `PruneOwnedProviderInstances` (`registry.go`), app-scoped `reconcileRuntimeProviderObservability`/`PruneOwnedProviderInstances` at `runtime_observability.go:98`.

## Test

`internal/application/shared_backends_resources_runtime_test.go`:

- `TestSharedDestroyRemovesOwnedPlatformSources` registers core postgres + core valkey through the productive `RegisterProviderSignals` path, destroys core, asserts both removed, then re-registers core and asserts success.
- `TestSharedDestroyPreservesForeignPlatformSources` registers core + other under two boundaries, destroys core, asserts other postgres + valkey survive (no cross-tenant wipe).

Regression direction (measured): with the destroy-path fix reverted to develop, `TestSharedDestroyRemovesOwnedPlatformSources` is RED (`owned platform sources (both providers) not removed ... map[postgresql:1 valkey:1]`); with the fix it is GREEN.

## CI-AUFNAHME

- Job: **CI · Source & Quality** (GitHub-hosted shared runner), packages shard runs the Go unit tests in `internal/application`.
- Trigger: PR selected checks on push to `lane-0428-184-shared-destroy` (ready PR run).
- `ci-fast-check.sh` on head `bc4df42d`: Go file size PASS, function span PASS, regression ratchet PASS, workflow policy PASS (20 approved workflow files).

## Beweiszeilen (three witnesses)

- base develop HEAD (ls-remote, real remote `origin` = github.com/mcpdev80/baseharbor.git): `96f2ae11a25a508998c44a9854ef17f8fa15c112 refs/heads/develop`.
- ancestry: `git merge-base --is-ancestor origin/develop HEAD` = JA; `git diff origin/develop...HEAD --name-only` = only `internal/application/shared_backends_resources_runtime.go`, `internal/application/shared_backends_resources_runtime_test.go`, `internal/observability/registry.go`; `git log --oneline origin/develop..HEAD` = only commit `bc4df42d` (no foreign commit).
- PR delivery: `git ls-remote origin refs/pull/1715/head refs/heads/lane-0428-184-shared-destroy` = `c1485721f1305fe4f3b5ef3984df15fe53e937a4` for both refs (PR #1715, base develop, head `bc4df42d`).
- CI run #6763 (CI · Source & Quality) terminal: **PR Selected Checks = failure**, **PR · Selected Runtime (atomic/podman/data-capabiliti...) = failure**, 16 success, 16 skipped. The two runtime failures are pre-existing environment flakiness (external-postgres registration) present identically on develop@96f2ae11; the Go packages shard (the packages shard that runs this test) is among the 16 success. `ci-fast-check.sh` local: all PASS, 293 tests OK.

## repo-rule compliance

- KEIN `.github/**` geaendert (owner-scope). KEIN `internal/application/perses_runtime.go` geaendert (0428-083). KEIN `registryPath` umgebaut, KEIN target-uid/root-Feld eingefuegt (0428-078 owner field). KEIN Merge, KEIN Subagent (§4.8), KEIN `git add -A`.
- Nur drei Produkt-/Testdateien im Write-Set; `registry.go` fuehrt nur die neue Funktion `PruneOwnedPlatformSources` (+29/-0), `registryPath` und der `RegisterProviderSignals`-Schutz unveraendert.
- Branch aus develop-spitze (96f2ae11, ls-remote-zeugnis), Ancestry JA, nur eigener Commit.
- Evidence in baseharbor-plan main (kein .evidence/ im Produkt, kein main-branch-write im Produkt).

## cleanliness

- Vorher: `docker ps -a` = leer; `docker network ls` = bridge/host/none; `docker compose ls -a` = keine projekte.
- Nachher: identisch. Diese Lane startete keine container/netzwerke/volumes/state-verzeichnisse; reine Go build/vet/test + git/gh-arbeit, keine deployment/compose-aufrufe.
- cleanliness: these lanes starts no containers/networks/volumes/state-dirs; no compose project touched; ambient-core/ bilder fremder karren bleiben unangetastet.

## END

END_DONE mission-184.md (0428-184 shared destroy skips registry cleanup) — PruneOwnedPlatformSources (+29/-0) in registry.go, called for postgres+valkey in DestroyAllSharedBackendsAt; regression productive RegisterProviderSignals fuer BEIDE provider (owned removed + re-reg succeeds; foreign other-env preserved); PR #1715 base develop 96f2ae11 head bc4df42d ls-remote c1485721; CI #6763 terminal (runtime gate failure = pre-existing env flakiness on develop too, packages shard green); evidence auf baseharbor-plan main; 0 container/netzwerke; KEIN .github, KEIN registryPath-umbau.
