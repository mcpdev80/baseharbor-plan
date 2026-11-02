# Evidence: w1-authority — t-20261018-r27-authority-contract

**Lane:** w1-authority (Worker)
**Task:** t-20261018-r27-authority-contract (critical, architecture, v0.4.27)
**Owner (plan):** `w1-authority (lane)` — claimed, committed `cd3e6b8`, pushed to baseharbor-plan main
**Base:** baseharbor `develop` @ `c8fddea3f7cd341130baddbace48bc8d4ccaaa2c` (verified, green develop self-test)
**Branch:** `work/r27-authority-contract`
**Mission:** coordinator/missions/w1-authority.txt (Night, Owner-Direktive 2026-11-02)

## PLAN (numbered)

1. [done] Read mission + task contract + release plan (v0.4.27) + input specs/ADRs.
2. [done] Public CLAIM: `plan.py claim t-20261018-r27-authority-contract --owner "w1-authority (lane)"` → commit + push baseharbor-plan main (rebase over `500b451..afd117d`).
3. [done] Isolated branch `work/r27-authority-contract` off develop `c8fddea3`; left the other session's uncommitted `internal/application/shared_backends.go` edit untouched.
4. [done] Read remote state of inputs and recorded Ist-Stand below.
5. [ ] New ADR (install-owned authority) aligned to ADR convention + `docs/spec/target-access-v1.md` update + `docs/spec/control-plane-runtime.md` update + DE-Pendants.
6. [ ] Bounded `internal/coreinstallation` selection/authority types.
7. [ ] Positive + negative regression tests (Connection != Target != Installation; no local fallback; stale observed-at rejected; foreign revision/consent rejected).
8. [ ] `go build ./... && go test ./internal/coreinstallation/...` + touched packages.
9. [ ] Open PR (base develop) with exact SHA + test evidence; NO merge/push to main/develop; NO `.github/**` / CI / workflow / register files.
10. [ ] Evidence finalize + HANDOFF post; `END_CODE_READY` line.

## Ist-Stand (source facts, remote develop @ c8fddea3)

- **Installation identity (existing, authoritative):** `internal/coreinstallation/installation.go` owns the one-installation core lifecycle. `State` is keyed by an opaque `installation_id` (UUIDv4), `Owner:"baseharbor"`, `Placement:"shared"`, version `baseharbor.core-installation/v1`. `Run()` creates the identity once, fails closed on conflicting `Spec{Target,Runtime,MachineRole,HA}`, serializes bootstrap via kernel lifecycle lock, persists `installation.json` (0600, protected owner). Capabilities `{sql,secrets,identity}` + `verified`. This is the existing semantic core a local direct-execution path must reuse **without** mandatory login/server or an SQL/Secrets/Identity stack bundle.
- **Lock/State ownership (existing):** `internal/deployment/deployment_store.go` — deployment state keyed by `targets/<target>/deployments/<deployment_id>/deployment.json`. `DeploymentIdentity` = `{deployment_id, application_id, target, application, environment}`; multiple deployments claiming one `application_id`+`environment` on one target → fail closed (`FindDeployment`). `SaveExpected`/`saveWithPreparation` (`config_mutation.go`) take a `.installation.lock` + `coreinstallation.AcquireStateFileLock` → one authoritative mutation owner per Target config root.
- **Target vs Access (existing, `target-access-v1.md`):** Runtime Provider ≠ Target Access Provider; effective projection = `{runtime_provider, access_provider, access_reference, scope}`. `access.provider=local` = Core executes the already-selected runtime op locally. `baseharbor-node-connector`/`native-api` are remote access providers. **Clients never call a connector directly.** Security: every non-local access provider fails closed, verified peer identity, no plaintext/opportunistic fallback. Startup binds **one local installation** even when Connector enrollment is disabled (`target-access-v1.md` lines ~316-331). This already encodes the "local direct execution, remote clients never own authoritative state" contract.
- **Shared core / multiple control surfaces (ADR 0009):** one shared domain/lifecycle core with CLI/API/UI/Operator adapters; no surface invents a more optimistic readiness model.
- **Stable identity (ADR 0017):** application UUID + deployment UUID owned by Core/Target state, not by mutable names.
- **Deployment reuse facts (release plan §Source review):** `internal/deployment/deployment_store.go` already has Environment-keyed identity, source revision/digest + applied/observed records; `internal/application/environment.go` resolves environment contracts; `internal/runtime/compose_network.go` PullImage; `internal/runtime/image_identity.go` pinned OCI. New work extends these owners, does not start from zero; **no new coreinstallation state database**.
- **Release plan §24 (authoritative summary):** "One selected installation owns authoritative deployment/provider state, identity, consent revisions and mutation locks for its admitted Targets. Management connection and Target are different selections. Local work uses the same semantic core directly without login/server or an unconditional SQL/Secrets/Identity stack; remote CLI/JSON/MCP/HTTP clients address the selected authority, never a connector directly. No authoritative remote state on developer workstations, NFS, home-directory synchronization, Baha-to-Baha federation or new generic state framework."
- **Write reservations (task §Dependencies):** `docs/spec/target-access-v1.md`; `docs/spec/control-plane-runtime.md`; corresponding DE specs; one new ADR; bounded `internal/coreinstallation` management-selection types + tests. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces`.

## Hard limits (Owner-Direktive 2026-11-02 Nacht)

- FORBIDDEN: `.github/**`, `scripts/pr-gate-plan.py`, `scripts/pr-check-runner.py`, all CI/workflow/register files (other session). Do not change; report as finding if needed.
- FORBIDDEN: Merge, Release, Tag, shared indexes, foreign draft branches.
- No gate weakening, no test removal/weakening.

## Write-Set (files actually changed)

7 files, +455/-0 (exact head `5c5b1f9a`, base develop `c8fddea3`):
- `docs/decisions/0021-one-installation-authority.md` (new ADR)
- `docs/spec/target-access-v1.md` (EN authority boundary section)
- `docs/de/spec/target-access-v1.md` (DE Zuständigkeitsgrenze)
- `docs/spec/control-plane-runtime.md` (EN server vs local execution)
- `docs/de/spec/control-plane-runtime.md` (DE counterpart)
- `internal/coreinstallation/authority.go` (new: Selection/StateOwner/RemoteAuthority)
- `internal/coreinstallation/authority_test.go` (new: positive + negative regressions)

## Deviations / Blockers

- Uncommitted `internal/application/shared_backends.go` + submodules `baseharbor-plan/`, `contracts/managementaccess/` present on the baseharbor working tree. **Left untouched** (AGENTS 4.1). Not part of my write-set (targeted `git add <file>` only).
- During work my commit accidentally landed on local `develop`; reset develop to `origin/develop` (`c8fddea3`) and re-created the branch cleanly, cherry-picked the commit as `5c5b1f9a`. Verified clean base before PR.
- No blocker.

## HANDOFF

codeman agent post f49a3303-e8bb-491b-9e2c-b629783c4e5f "END_CODE_READY|END_BLOCKED w1-authority: task=t-20261018-r27-authority-contract pr=#1323 head=5c5b1f9a tests=pass ci_files=none | <Satz>"

**END_CODE_READY** — ADR 0021 + EN/DE spec updates + bounded coreinstallation authority types + positive/negative regressions; PR #1323 open (base develop). No merge/release/tag. CI/registry files untouched (other session).
