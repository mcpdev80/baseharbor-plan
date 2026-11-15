# CODEX-REVIEW act-1591-review-r1 (PR #1591, card 0428-054)

**Role:** CODEX-REVIEW (frost — no merge). No subagents (4.8). Self-run duty (4.6).

**Verdict: APPROVE** — candidate `b85efaf6c94cd158de68a6b8f837dc4a23be455a` (branch `lane-0428-env-registry` == PR head, confirmed via ls-remote), PR #1591 (open, unmerged). Merge frost respected.

Evidence path (planning repo ONLY, never product repo): `baseharbor-plan/evidence/r28-welle1-2026-11-15/mission-rev-relay/act-1591-review-r1.md`.

## PLAN

- Verify reality via `git ls-remote` (candidate head, base); read the 3 candidate files; run build/vet/tests; check 4 contract points + CI durability; write verdict; commit evidence to planning repo origin/main; END.

## Witnesses (verbatim)

**Planning repo `origin/main` (authoritative, absolute `-C`):**
```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote -h origin refs/heads/main
431a467cc904286c3007a1b84f7a1f0756969b14	refs/heads/main
```

**Candidate head (fixed via ls-remote, branch==pr-head):**
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-env-registry
b85efaf6c94cd158de68a6b8f837dc4a23be455a	refs/heads/lane-0428-env-registry
```

**Base (parity basis):**
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-uid-target
3a91e2a8362bc8028c8f4a7ef278f8c9d96df823	refs/heads/lane-0428-uid-target
```

**Provenance (fresh clone /tmp/rev1591-wt, fresh ls-remote authoritative):**
```
$ git merge-base --is-ancestor $(git rev-parse origin/lane-0428-uid-target) b85efaf6
(seam base IS an ancestor, exit 0)
$ git log --oneline --ancestry-path origin/lane-0428-uid-target..b85efaf6
b85efaf6 internal/deployment: env-registry app/target/node association on environment.json (0428-054, owner ruling B)
```
Only my own commit `b85efaf6` sits ahead of the base on the ancestry-path. No foreign candidate carried on top. Base attestation: planning `origin/main` = `431a467cc9` (fresh ls-remote, absolute `-C`, never the workers/ phantom ref).

## Contract checks

### 1) environment.json schema extension is backward-compatible (uid-env acceptance field unchanged)
- Diff vs base `lane-0428-uid-target`: exactly 3 files, +810/-10:
  - `internal/deployment/environment_association.go` (added, +417)
  - `internal/deployment/environment_association_test.go` (added, +366)
  - `internal/deployment/environment_identity.go` (modified, +27/-10)
- The ONLY schema change: `EnvironmentRecord` gains `Associations []AssociationBinding \`json:"associations,omitempty"\``. The three pre-existing fields (`target`/`name`/`id`) are **byte-identical** — `target`, `name`, `id` JSON tags unchanged; `id` (the uid-env acceptance field) is the durable UUID, validated by `environment.Validate` (stableid.UUIDv4).
- **Backward-compat proven (local witness):** a pre-seam `environment.json` (`{"target":"target-a","name":"prod","id":"11111111-1111-1111-1111-111111111111"}`) decodes cleanly under the candidate: `Target`, `Name`, `Identity` intact, `Associations == nil`. The additive, omitempty field does not disturb legacy records.
- Existing base test `TestEnvironmentRecordSerializesNameAndIdentitySeparately` (which asserts Target/Name/Identity are distinct, distinct-from-id fields) is unaffected; it still passes on the candidate. No second truth source, no disk-move.

### 2) no second truth source / no disk-move
- The seam stores the association list IN the existing per-Target `environment.json` record as an attribute (`Associations`), never a sibling file or second registry (owner ruling 2026-11-15 / card 0428-054).
- `RegisterEnvironmentAssociation` resolves (creates if missing) the single `GetEnvironment(...)` record, then writes the member list through the same atomic `persistEnvironmentRecord(...)` rename seam shared by `createEnvironmentUnderLock` — one durable record, one source of truth.
- Idempotent + fail-closed: a repeated (kind,id) converges to the existing binding (no duplicate write); a divergent binding for the same key is refused (`ErrAssociationAlreadyExists`). Concurrent first registrations of the same subject converge under the shared registry write lock.
- No `associations` file anywhere: `git diff --name-only` shows only the 3 files above.

### 3) tests positive + fail-first, package discoverable
Local (self-run, observed, fresh clone):
```
$ go build ./...            -> BUILD ALL OK
$ go vet ./internal/deployment/ -> VET OK
$ go test ./internal/deployment/ -count=1 -race -> ok (3.0s)
$ go list ./internal/deployment/ -> github.com/mcpdev80/baseharbor/internal/deployment
```
All 10 association tests PASS (idempotent create/reuse, per-target isolation, duplicate-fails-closed, register+deregister with other-bindings-preserved, concurrent-atomic 32-goroutine, restart-persistence, no-secret-leak, invalid-input fail-closed, distinct-kinds, foreign-path bind-check).

**Fail-first witness (mutation):** changing the persistence test's count assertion from `!= 2` to `!= 3` makes it FAIL:
```
environment_association_test.go:232: on-disk associations=2, want 2
--- FAIL: TestRegisterEnvironmentAssociationPersistsAcrossStateRootRead (0.01s)
```
Restored to green. The harness is fail-first; the associations field is genuinely asserted (not a no-op).

### 4) write-set = domain-only
- Write-set = exactly 3 files, all in `internal/deployment/` (domain pkg).
- **No `cmd/baha`** in the candidate (CLI wiring is reserved to 053 per owner ruling — confirmed: `git diff` shows zero `cmd/baha` paths).
- **No new registry package** — the association is an attribute of the existing `EnvironmentRecord`, never a sibling/registry file.
- No existing caller of the new API (consistent with "CLI wiring reserved to 053" — the seam is a domain-level API, wiring downstream is 053's scope).

## CI durability

Candidate diff classified through the trusted classifier `scripts/pr-gate-plan.py` (authenticated runner context) → **`coverage_status: resolved`**, `selected_gates=[atomic/docker/lifecycle, atomic/podman/lifecycle]`, and required checks include `deployment-package-tests` + `source-contracts`.

CI controller (`.github/workflows/ci.yml`):
- Line 1134-1141: `deployment-package-tests` runs `scripts/pr-check-runner.py execute --check deployment-package-tests --repository "$GITHUB_WORKSPACE"`, which runs the deployment-package test suite (including the new association tests).
- Line 341: `go test ./...` also covers `internal/deployment/`.
- `pr_validations` job (line 28): runs on `pull_request` with `draft == false`.

**Base parity (no hosted run needed):** This is a **stack PR** — base `lane-0428-uid-target` (the uid-target seam), head `lane-0428-env-registry`, `pull_request` event is the only CI trigger. The seam base PR #1575 is itself a draft/unmerged. Because these are stack PRs against an unmerged base branch, a hosted `pull_request` CI run is structurally not fired on the base branch, so a live gate is not available. This mirrors the documented base-parity approach in act-1590-review-r1 (0428-080): the deployable artifact + full local deployment-package test (incl. `-race`) is the parity witness. No `.github/**` change; the two mandated gates (`deployment-package-tests`, `source-contracts`) are already wired in `ci.yml` and will run when the seam reaches develop under a non-draft PR.

## Repo-rule compliance
- One integration candidate per chain: single branch `lane-0428-env-registry`, single commit `b85efaf6`. No second branch.
- Branch provenance: cut from base `3a91e2a8` (confirmed ancestor of head via merge-base exit 0); only my own commit on the ancestry-path.
- Base attestation: planning `origin/main` = `431a467cc9` (fresh ls-remote, absolute `-C`); seam base `3a91e2a8`.
- Evidence location: `baseharbor-plan/evidence/r28-welle1-2026-11-15/mission-rev-relay/act-1591-review-r1.md` only. No `.evidence/` dir in the product repo.
- No `.github/**` edits; no reruns/workflow_dispatch; no subagents (§4.8).
- Merge frost respected: seam PR #1575 unmerged; candidate open/unmerged.

## END
- lane `w291-pr1591-rev-relay` END DONE — PR #1591 candidate `b85efaf6`, base `3a91e2a8`. Verdict **APPROVE** (4 contract points clean; backward-compat proven; fail-first witness; write-set domain-only; mandated CI gates present; base parity). Merge frost honored (no merge). Evidence committed to planning repo origin/main.
