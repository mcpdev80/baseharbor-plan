# Bug-Hunt H — use/activate fails closed when the running Core has no service-access/issuer (BF-02, card 0427-162)

- Card/mission: mission-162.md (0427-162, bug-hunt, pure finding + fix recipe, no product change)
- Shift: r27-welle5-folge-2026-11-08 / round-1
- Worker session: laptop (session 594fd2f5-4e80-43b6-9841-92879146a85e), no subagents (4.8)
- Planning repo verified (origin/main): 0272c4b0feee978d5537d5dd6b88b3db81901390 (`git ls-remote origin main`)
- Source pin: origin/develop = cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c (`git ls-remote origin develop`)
- Branch base attestation: origin/develop cdb4350a6 is an ancestor of the checkout HEAD (cdb4350a6) — single integration candidate, no foreign branch carried.
- Source zone: /tmp/opencode/w162-issueruse-wt (fresh clone of mcpdev80/baseharbor @ develop cdb4350a6). Working tree /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor is a 259-commit-stale stale-ref checkout and was NOT used as evidence.
- Build: go build ./cmd/baha OK on develop cdb4350a6 (`go version go1.26.8 linux/amd64`).

## PLAN

- Read mission-162.md, board card, product/coordinator AGENTS; attestation (origin/develop cdb4350a6, origin/main 0272c4b0, working tree stale 259 commits)
- Locate the real failing path on develop HEAD (mission refs use_target.go:61-112, authority.go:356-396/:73, target.go:249 — confirm against current source)
- Reconcile selection branch with the read path (status works): trace observeLocalIssuer / ResolverForTargetSelection vs resolveApplicationServiceIssuer / EnsureLocalIssuer
- Reproduce BF-02 faithfully (seeded verified Core with service-access/issuer dir absent)
- Confirm 'core install' is unreachable and no CLI command materializes the local base CA
- Confirm isolated write-set (no other lane touches use_target.go / use_target_connection_test.go)
- Findings + fix recipe with file:line
- Local tests (go test ./cmd/baha -run TestBindExplicitSelection, go vet, go build) + outcomes
- Commit evidence to origin/main; END

## Finding: BF-02 — use/activate fails closed on a running Core whose service-access/issuer is absent (blocker candidate)

### Symptom
A running Target whose state dir has no `service-access/issuer/` (fresh bootstrap, partial install, moved state) cannot be selected at all:

    $ baha use repro-docker
    Error
      target "repro-docker" has no verified management connection: ...
    What to do
      Install a BaseHarbor Core for this Target (baha core install) so the management connection is present, then re-run baha use.
    EXIT=1

`baha core --help` => `Error: unknown command "core" for baha`. The referenced `core install` subcommand does not exist in this build.

### Root cause (file:line on develop cdb4350a6)
- `cmd/baha/use_target.go` `bindExplicitSelectionToConnection` (lines 61-112): loads the verified installation via `coreinstallation.Load(root)` then calls `coreinstallation.ResolverForTargetSelection(ctx, state, root)`. On `ErrUnverifiableInstallation` it maps to a typed conflict `machine.ErrorConflict` with the "baha core install" guidance (lines ~79-92).
- `internal/coreinstallation/authority.go:356-396` `ResolverForTargetSelection`: fails closed with `ErrUnverifiableInstallation` whenever the issuer material is absent/unreadable. It derives the management connection through `observeLocalIssuer(issuerStateDir(targetStateRoot))` (line ~387) then `observedThroughTargetBoundary` (line ~391).
- `internal/coreinstallation/authority.go:287-288` `issuerStateDir` = `<root>/service-access/issuer`.
- `internal/serviceaccess/local_issuer.go:28-57` `CheckLocalIssuer`: returns **nil (no error) when the dir does not exist** (`os.ErrNotExist` -> `return nil`). So `observeLocalIssuer` returns a `&LocalIssuer{Dir: dir}` even for an absent dir.
- `internal/serviceaccess/local_issuer.go:122-137` `load()`: `os.Lstat(i.Dir/issuer.pem)` returns `os.ErrNotExist` -> `return nil, nil, "", err` -> `TrustBundle` errors -> `observedThroughTargetBoundary` errors -> `ErrUnverifiableInstallation`.

So: an absent `service-access/issuer/` (or one whose `issuer.pem` was removed) yields a `LocalIssuer` whose `load()` errors, and the selection boundary fails closed. The read path does NOT: `resolveApplicationServiceIssuer` (cmd/baha/application_service_issuer.go:24-72) returns `&LocalIssuer{Dir: dir}` for an absent dir and only validates with `CheckLocalIssuer` (line 65); the mutating `materializeApplicationServiceIssuer` (line 75) calls `serviceaccess.EnsureLocalIssuer` which **generates a new base CA** when `issuer.pem` is absent. That is the exact reconciliation the read path performs and the selection path skips.

### Faithful reproduction (authoritative, via a Go repro run on develop cdb4350a6)
Seeded a genuine verified Core installation (all 3 capabilities, ready=true, HTTPS identity issuer) at its runtime root, then removed only `service-access/issuer/`:

    seeded installation id=... ready=true
    ResolverForTargetSelection: issuer=<nil> ... err=installation not verifiable as a genuine baseharbor Core installation, fails closed
    REPRO POSITIVE: resolver failed closed ...
    EnsureLocalIssuer re-derived issuer.pem ... (recovery possible, no named CLI command)

CLI end-to-end on the built develop binary: `baha use <target>` on a Core ready with no issuer dir => the "no verified management connection ... baha core install" error; `baha core --help` => unknown command.

### POSITIVE (counter) — the Core is fully observable
`baha status --target <t>` / `BASEHARBOR_TARGET=<t> baha status` read the running Core (docker/podman compose state) without the issuer and report it — confirming the Core is live and only the selection boundary fails closed.

### Impact
A Core that is running but whose management CA issuer directory is absent (fresh bootstrap, partial install, moved/cleared state) cannot be selected with `use`/`target activate` at all. The operator is pointed at an unreachable `baha core install` subcommand — a dead-end, not a recovery path. This is the BF-02 blocker candidate.

### Fix recipe (two acceptable options; pick one, do not invent a second)
Option A (reconcile selection with the read path, preferred — keeps the fail-closed contract identical for foreign/foreign-identity while recovering a genuinely-absent local base CA): in `resolverForTargetSelection`/`observeLocalIssuer`, distinguish "issuer dir exists but incomplete/unreadable" (must stay fail-closed) from "issuer dir entirely absent on a verified, ready Core" (recoverable). For the absent case, either (i) return a `&serviceaccess.LocalIssuer{Dir: issuerDir}` so the caller's `load()`/`EnsureLocalIssuer` re-derives `issuer.pem` from the verified installation's protected state — mirroring `resolveApplicationServiceIssuer`+`materializeApplicationServiceIssuer`, or (ii) reject with a NEW named sentinel the caller maps to a typed error naming an existing recovery command. Never silently fabricate an issuer for a foreign or partially-present dir (that would be a security regression).

Option B (name a real recovery command): add a minimal, reviewed recovery command such as `baha target issuer recover <NAME>` that runs `serviceaccess.EnsureLocalIssuer` on the verified installation's protected state (never opening a second trust source), and change the errorstring at `cmd/baha/use_target.go` to name that command. Requires a reviewed command addition + a regression test in the cli-surface/lifecycle group.

### Must-fix: remove the irrelevant core-install mention in the errorstring
Regardless of A/B, `cmd/baha/use_target.go` currently references `baha core install` (lines ~79-92 in both `ErrNotExist` and general branches). This subcommand does not exist. The fix must drop/correct this unreachable reference (file:line above).

### Security regression guard
A missing/foreign/unverifiable installation or a foreign identity must still fail closed (existing tests `TestBindExplicitSelectionFailsClosedWithoutCore`, `TestBindExplicitSelectionFailsClosedOnMissingKeycloakIssuer`, `TestBindExplicitSelectionFailsClosedOnForeignIssuerIdentity` must keep passing). The change is scoped to the absent-local-base-CA recovery path only; do not relax the identity-mismatch or foreign-target boundaries.

## Where the regression test goes (CI-covered)
File: `cmd/baha/use_target_connection_test.go` (same file/owner as the boundary it tests).
CI: `/.github/workflows/ci.yml` "Run release-source tests" job runs `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha` (the cli-surface/lifecycle group), so a new test there IS CI-covered (Owner directive 2026-11-07). No `.github/**` change needed — the group already compiles `cmd/baha`.
Suggested test: `TestBindExplicitSelectionReconcilesAbsentLocalIssuer` — seed a verified Core (all 3 caps, ready), remove only `service-access/issuer/`, assert the selection either binds (Option A) or fails closed with a NEW named sentinel naming the recovery command (Option B). Add a companion positive asserting the recovery command (if Option B) re-derives `issuer.pem` from the verified installation.

## Repo-rule compliance
- Pure finding + fix recipe: no product code change made. No `.github/**` touched (Owner scope). Single integration candidate from origin/develop cdb4350a6. Evidence written only to baseharbor-plan (no product-repo writes, no `.evidence/`). No subagents (4.8).
