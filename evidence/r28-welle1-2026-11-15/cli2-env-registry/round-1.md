# Round-1 akte — t-20261114-r28-cli2-env-registry (0428-054)

- Shift: r28-welle1-2026-11-15
- Card: t-20261114-r28-cli2-env-registry (0428-054)
- Owner: lane-0428-env-registry
- Candidate: `lane-0428-env-registry` @ `b85efaf6c94cd158de68a6b8f837dc4a23be455a`
- PR: [baseharbor#1591](https://github.com/mcpdev80/baseharbor/pull/1591) (draft)

## OWNER RULING (2026-11-15, wortlich)

> "B — Fuer 054 die App-/Target-/Node-Zuordnung im bestehenden per-Target-Environment-Zustand (environment.json) ablegen. CLI-Wiring bleibt bei 053."

Decision B is FINAL. HOLD from the open owner-question (2026-11-15) is lifted. Association is stored as an additive field on the existing per-Target `environment.json` record — single source of truth, no second registry. CLI wiring stays with card 053 (env-policy).

## PLAN

1. Confirm reality via ls-remote (base `3a91e2a8` = lane-0428-uid-target; plan origin/main). DONE.
2. Claim centrally (plan.py claim + push). DONE (plan main `5e6aab99`).
3. Create branch from base `3a91e2a8`; attest ancestor. DONE (branch `lane-0428-env-registry`, base ancestor of `b85efaf6`).
4. Read accepted seam; confirm owner ruling. DONE.
5. Implement Option B: association as additive field on environment.json; idempotent migration; collision fail-closed; no second source of truth; no cmd/baha. DONE.
6. Add focused tests in internal/deployment (CI packages shard). DONE (10 tests).
7. Terminal-run: build/vet/test at candidate SHA. DONE (see witnesses).
8. Draft PR base=lane-0428-uid-target (retarget); provenance. DONE (#1591).
9. Write akte; push evidence to origin/main; git log witness; END. IN PROGRESS.

## RESULT

Implemented the app/target/node association registry (Option B) as an additive field on the existing per-Target environment.json record.

- New `internal/deployment/environment_association.go`: seam `RegisterEnvironmentAssociation`, `DeregistrationEnvironmentAssociation`, `ListEnvironmentAssociations`, `EnvironmentRecordAssociations`. `AssociationBinding{SubjectKind: app|node, SubjectID}` — (kind,id) membership key keeps identity roles distinct; no name-matching inference.
- Idempotent membership: repeated (kind,id) converges to the existing binding, never duplicates.
- Concurrent first registration converges under the shared registry write lock (mirrors `GetEnvironment`) — atomic, no state split (precedent 0427).
- Fail-closed: invalid kind/id/target/path; foreign-binding read refused (`ErrEnvironmentBindingMismatch`).
- `EnvironmentRecord` gains additive `Associations []AssociationBinding` (omitempty) — byte-compatible with pre-seam readers.
- No `cmd/baha` touch (053 territory preserved). No `.github/**`.

## TERMINAL RUN (observed at candidate SHA b85efaf6)

- `go build ./...` → exit 0 (clean)
- `go vet ./internal/deployment/` → exit 0 (clean)
- `go test ./internal/deployment/` → ok
- `go test ./internal/deployment/ -run 'TestRegister|TestEnvironmentRecordAssociations'` → 10/10 PASS (concurrent atomicity, per-target isolation, duplicate/conflict fail-closed, deregister idempotency, Core-restart persistence, no-secret-leak, invalid-input refusal, distinct app/node kinds, foreign-path bind-check)
- `go test ./internal/deployment/ -run '...Concurrent...' -race -count=3` → ok (atomicity race-clean)
- `go test ./internal/...` → 3 PRE-EXISTING failures in `internal/controlplaneruntime`, `internal/database`, `internal/development` (environment/executor/openbao/native-Git-archive); VERIFIED identical on clean base HEAD `3a91e2a8` in a fresh clone — NOT caused by this change. My changed packages (deployment) are green.

## CI ROUTING

- Tests live in `internal/deployment` (domain package) → covered by the CI `packages` shard via `go test ./...` (`scripts/pr-go-unit-shard.py packages`). No `.github/**` change needed; no new CI group.
- PR #1591 is a draft; base `lane-0428-uid-target` (chain head, not develop), so the standard PR CI `if (base_ref == develop)` gates do not fire a live run against this draft. No rerun triggered (Owner .github scope). Owner/Codex merge carries the required checks.

## REPO-RULE COMPLIANCE

- AGENTS 4.3 claim before change: plan.py claim published + pushed (plan main `5e6aab99`).
- One task/branch/PR per worker (AGENTS 3.8): single branch `lane-0428-env-registry`, single PR #1591. Log lists ONLY this lane's commit `b85efaf6`.
- Base provenance: cut from `3a91e2a8362bc8028c8f4a7ef278f8c9d96df823` (`lane-0428-uid-target`); `git merge-base --is-ancestor 3a91e2a8 HEAD` → YES. Base head is an ancestor of head.
- No second candidate branch for the card.
- No subagent (AGENTS 4.8): every step executed in this session.
- No `.github/**` touch; no runner build/register.
- Evidence only in baseharbor-plan (product repo untouched). No merge (frost). No release/tag.

## EVIDENCE

- PLAN.md: evidence/r28-welle1-2026-11-15/cli2-env-registry/PLAN.md
- This akte: evidence/r28-welle1-2026-11-15/cli2-env-registry/round-1.md
- Board file: workers/todos/mission-054.md.json

## END lane-0428-env-registry DONE

Candidate `b85efaf6` implemented, tested, draft PR #1591 (base `lane-0428-uid-target`). HOLD lifted per owner ruling B. Awaiting Owner/Codex Maintainer merge (frost preserved).
