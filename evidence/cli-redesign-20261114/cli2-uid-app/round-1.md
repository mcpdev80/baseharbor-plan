# CLI2 uid-app — round 1 evidence (t-20261114-r28-cli2-uid-app / card 0428-050)

Lane: `lane-0428-uid-app` · Model: ornith · Date: 2026-11-14

## Scope / base attestation

- Product repo base for this lane: `origin/develop` SHA `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (verified: `git ls-remote origin develop` / fresh clone).
- Plan repo authoritative base: `origin/main` `b4a68e686b4770bf17bd43166f840facc427e03c`; `git merge-base --is-ancestor` confirmed.
- Branch cut from base: `lane-0428-uid-app` from `0e9ccb582`. Witness: `git merge-base --is-ancestor 0e9ccb582 HEAD` → ancestor confirmed.
- `git log origin/develop..HEAD` carried only my own commits (none yet).

## Reality witness (remote truth)

- `git remote -v`: `origin https://github.com/mcpdev80/baseharbor.git`.
- `git ls-remote origin develop` → `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`.

## Task and contract read

- Task card `t-20261114-r28-cli2-uid-app`: persist portable app identity. State active, owner `lane-0428-uid-app`, depends on `t-20261114-r28-cli2-contract` (accepted).
- Contract round-1 `cli-command-contract-v1.md` §6/§11 item 1: "app.id in the committed contract ... Decision required ... coordinated with Core + Git authority".
- Owner brief line 14: user wants nonsecret `app.id` committed in versioned `baseharbor.yaml`, generated at new/init, reused, historical preserved, conflicts rejected.

## FINDING: direct conflict with the normative contract — BLOCKER (needs Owner decision)

The mission to commit a portable, non-secret `app.id` into `baseharbor.yaml` conflicts with the product's NORMATIVE, accepted identity contract. Evidence:

1. `docs/spec/application-contract-v1.md` "Stable identity" (normative):
   - "Developer-authored manifests MUST NOT contain `app.id`. BaseHarbor MUST generate a UUIDv4 once during explicit initialization as the stable `application_id` and persist it in the existing system-owned canonical state. Reading/parsing MUST NOT allocate IDs or state. Authored IDs MUST be rejected before mutation."
   - "Deployment identity remains Target-local protected state and MUST NOT become portable Application Intent."

2. `docs/spec/capability-first-v0425.md` SUPersedes ADR 0017: "Developer manifests MUST NOT contain app.id. Internal canonical state owns the ID." Table row: "Developer `app.id` → Actionable rejection, preserving authored file and existing user data."

3. `docs/decisions/0017-stable-application-and-deployment-identity.md` (ADR 0017): states `app.id` lives in `baseharbor.yaml`, but its Status block says this placement is "superseded for v0.4.25 by Capability-first contracts and #872" and "records the historical placement decision, not current authoring instructions."

4. Current implementation enforces the normative contract:
   - `internal/application/manifest_render.go:9-13` `AuthoredYAML()` sets `m.ApplicationID = ""` before serializing — the committed file NEVER carries the ID.
   - `internal/application/manifest_render.go:16-22` `YAML()` (canonical) carries `id:` only when set.
   - `internal/application/manifest_parse.go:268-272` parser REJECTS authored `app.id` in non-canonical mode: "app.id is system-owned; remove app.id from the developer manifest ... BaseHarbor generates and persists the identity".
   - `cmd/baha/application_adoption.go:23-118` `persistRepositoryApplication`: Core is the sole authority that allocates the ID; authored path retains only portable intent. `persistRemoteRepositorySource` writes authored YAML without ID.

5. Existing tests hard-enforce the invariant:
   - `cmd/baha/app_binding_production_test.go:60-66` — authored contract must NOT carry `application_id`.
   - `cmd/baha/bugs_858_860_regression_test.go:366` — CLI must print "app.id is system-owned".
   - `cmd/baha/client_commands_behaviors_test.go:195` — authored contract does not carry the ID.

## What the mission wants vs what the contract forbids

- Mission: generate nonsecret `app.id` at new/init, persist in versioned `baseharbor.yaml`, reuse across checkouts/legacy/checkout, reject collisions — i.e. make `app.id` PORTABLE and Git-committed.
- Normative contract (`application-contract-v1.md`): `app.id` is SYSTEM-OWNED and Target-local protected deployment state; it MUST NOT be portable Application Intent; authored manifests MUST NOT contain it; authored IDs are rejected before mutation.

## Decision required (blocking)

These are mutually exclusive by design. I cannot both (a) commit a portable `app.id` into `baseharbor.yaml` AND (b) honor the normative contract. Per AGENTS §5.6 / §4.2 I must not guess or silently weaken policy. Owner must decide exactly one:

- Option A (confirm mission): Authoritatively amend `application-contract-v1.md` (and reconcile ADR 0017 / capability-first v0.4.25) so `app.id` becomes a committed, portable, non-secret developer identity, with migration of existing stores + reject-conflict. This is a breaking contract change needing full release/audit, not a bounded uid-app slice.
- Option B (confirm contract): The uid-app slice implements something that DOES NOT contradict the normative contract — e.g. identity STABILITY/continuity guarantees (reuse the system-owned ID across checkouts, fail-closed on mismatch, concurrent-create convergence, no secret leakage) WITHOUT committing any ID into `baseharbor.yaml`. This is the bounded, safe slice the code-entry index already points at (`identity_resolution.go`, `manifest_render.go`, `repository_manifest.go`, `app_init_wizard.go`).

## Owner decision (2026-11-14)

Owner confirmed **Option B**: keep `app.id` OUT of `baseharbor.yaml` (contract §6 governs; brief line 14 remains an OPEN decision until the Owner explicitly approves committing it). Build the BOUNDED slice: stable, system-owned identity — reuse across checkouts/legacy, fail-closed on conflict, convergence on concurrent create, no secret leakage. No contract change. This akte carries the open-point note (brief line 14) with one contract-cited line so the Owner sees it in the akte (not the board); the Owner will pour it into a question the next day.

## END STATE

- `END_DONE` pending final acceptance steps. Scope locked to Option B.
