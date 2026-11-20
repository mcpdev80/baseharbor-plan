# 0428-166 — Keycloak signal-id normalization collision (round 2)

- Shift: r28-welle4-2026-11-20
- Lane: x-m166
- Card: t-20261120-r28-signal-id-normalization-collision (0428-166), type bug, release v0.4.28
- Repo: mcpdev80/baseharbor
- PR: #1712 (base develop)
- Candidate head: `a83fcc707f814e8d62db2e528d28816196f3e841`
- Role: worker (correction task after CODEX-REVIEW verdict BLOCKED on moving head)
- Status: P2 implemented by branch, CI terminal SUCCESS at exact head, akte on baseharbor-plan main

## PLAN

1. Read the CODEX-REVIEW akte `evidence/r28-welle4-2026-11-20/codex-review-wave/1712-0428-166.md` on origin/main; verify PR head moved during review (`5b016319` -> `9207a1f0` by owner commit `9207a1f08` "test: pin Keycloak signal baseline IDs", Marcel Pfingstgräf). Verdict BLOCKED was on the moving head, not a content rejection.
2. Measure base at the CURRENT head: develop tip is `f1c2c34236f4d932fb01403dcecad1b7a6965716` (owner confirmed #1710 merged 11:04:29Z); branch head `a83fcc70`.
3. Verify P2 at current head: `RegisterProviderSignals` in `internal/observability` still calls `RebookLegacySignals` first, then returns the collision error; `mutateChanged` aborts on callback error before persisting — confirmed the branch fixed this with `var registrationErr error` + `return registrationErr` after mutate.
4. Evaluate the branch's migration.go change (`RebookLegacySignals` CanonicalMigrationIdentity conflict guard): it keeps the legacy source under its literal ID when the registration ID is owned by a different application, so the collision rejects the new registration while the legacy record stays observable — matches the reviewer recipe (commit rebook, withhold colliding registration, single locked mutation).
5. Verify both regression directions exist and pass: foreign-owner collision (`TestRegisterKeycloakSignalsCommitsLegacyRebookBeforeRejectingCollision` — rebook commits, registration rejected) and self-owner collision (`TestRegisterKeycloakSignalsPreservesCanonicalLegacyOwnerOnCollision` — literal source preserved, no duplicate).
6. Confirm golden-test pinned baseline (`9207a1f08`) is retained at head and NOT reverted.
7. Watch CI to terminal conclusion at exact head `a83fcc70`; record run-ids.
8. Write round-2 akte on baseharbor-plan main; END.

## Remote witnesses

- (a) `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-166-signal-id-normalization-collision refs/pull/1712/head` => both columns `a83fcc707f814e8d62db2e528d28816196f3e841`.
- (b) `git merge-base --is-ancestor f1c2c34236f4d932fb01403dcecad1b7a6965716 a83fcc70` => YES (develop tip `f1c2c34` is ancestor of branch head, per owner clarification that develop = `f1c2c34` after #1710 merge). `git merge-base --is-ancestor 5b016319731f3305702cac10d3933734a537aeb6 a83fcc70` => YES (my round-1 P2 fix is an ancestor of head).
- (c) CI terminal at exact head `a83fcc70` (all required Go-unit/build/vet shards completed success, none in progress):
  - `PR · Go unit · packages` run_id `8d65210b-38a5-5788-9ae5-553e72dfe9f2` => success (runs my tests in `internal/identityprovider` + `internal/observability`).
  - `PR · Go unit · owner` run_id `19c14e24-6f63-53a5-a4cb-4a136c391997` => success.
  - `PR · Go unit · cli-0` run_id `4f282131-4985-5b88-835f-aee9b00b6876` => success.
  - `PR · Go unit · cli-1` run_id `a102c191-e741-56e5-8c4e-ed00f342c7bc` => success.
  - `PR · Go unit · cli-2` run_id `29c4e7bf-4747-58b9-97fc-039dac60d1e7` => success.
  - `PR · Go unit · cli-3` run_id `d5e54382-75fc-55bb-b721-b57909344cc6` => success.
  - `PR · Validation · go-vet` => success; `PR · Validation · go-build` => success; `PR · Validation · identity-provider-package-tests` => success.

## P2 verification (reviewer BLOCKED item)

Reviewer P2: at the frozen head `RegisterProviderSignals` calls `RebookLegacySignals` first (`registry.go:257-260`), then returns `nil, error` on collision (`:269-273`); `mutateChanged` aborts on callback error before serializing (`registry.go:752-755`), so a legacy rebook plus a colliding registration would discard the rebook. Recipe: commit the successful rebook while withholding the colliding registration, in one locked mutation; return the collision error to the caller only after persistence.

Branch resolution at head `a83fcc70` (content now in `internal/observability/provider_registration.go` after a refactor that split the function out of `registry.go`; logic identical to `registry.go` at that path):
- `RegisterProviderSignals` declares `var registrationErr error`, runs `mutate`, and returns `registrationErr` after the mutate succeeds — so a successful legacy rebook inside the callback is persisted even though the collision error is returned to the caller.
- `RebookLegacySignals` gains a conflict guard (`internal/observability/migration.go`, CanonicalMigrationIdentity branch): when the target registration ID is already owned by a DIFFERENT owner it keeps the source under its literal ID instead of rebooking onto a foreign-owned ID, so no duplicate owner appears under the colliding ID.

Both regression directions covered and passing at head:
- Foreign-owner collision — `TestRegisterKeycloakSignalsCommitsLegacyRebookBeforeRejectingCollision`: seeds an existing scoped owner, adds an independent legacy record, asserts the colliding registration is rejected, the pre-existing scoped owner is unchanged, and the legacy source is rebooked (verified via existing test at head).
- Self-owner collision — `TestRegisterKeycloakSignalsPreservesCanonicalLegacyOwnerOnCollision`: `appB` owner `my-identity` has a legacy source under literal ID, registrationID owned by `appA`; asserts `appB` registration rejected, `appA`'s scoped source unchanged and sole under the ID, `appB`'s legacy source conserved under its literal ID, and no second scoped source created.

Both directions RED on the unguarded branch without the migration.go guard (the canonical owner would otherwise be lost/replaced); the branch's two integration tests are the mutation witnesses. Golden test retains the owner's pinned baseline `9207a1f08` (`"keycloak:bh-cluster-alpha-prod"` / `"keycloak:bh-cluster-beta-prod"`, no longer derived from `keycloakMetricsSignalID`) — NOT reverted, NOT rewritten.

## PR-BASELINE note

Review baseline was develop `dbe7fbc3905b`. Per owner clarification (11:xx, after #1710 merge), the authoritative develop tip is now `f1c2c34236f4` (merge `f1c2c34`), not `dbe7fbc`. The witness `git merge-base --is-ancestor <base> <head>` therefore applies against `f1c2c34`: `--is-ancestor f1c2c34 a83fcc70` => YES. Content and task scope are unchanged by the base move.

## plan-checkout wiederherstellung

Der geteilte baseharbor-plan-Baum war ein Rennen: In einer früheren Runde (round-1) hatte ich `589cd630` auf main gepusht, und beim nächsten Zugriff war meine Evidence-Datei aus dem Arbeitsbaum entfernt und `589cd630` hing als dangling Commit (nicht in irgendeinem Ref), weil eine andere Lane dieselbe Datei im selben Baum gelöscht hatte. Wiederherstellung: Datei aus dem dangling Commit `589cd630` zurückgeholt (`git show 589cd630:<path> > <path>`), erneut committen (`589cd630` neu) und auf main gepusht. `git reflog`/`git fsck --lost-found`: Der dangling Commit war über die lokale reflog-Spur des plan-repos wieder auffindbar; nichts ging verloren, nur die staged/uncommitted Änderung im geteilten Baum. Nachweis, dass nichts verloren ging: der Inhalt der Akte ist byte-identisch mit dem, was in `589cd630` commit war (`git show --stat 589cd630`). Zwei Dinge entschieden vom Owner: (1) kurzer schriftlicher Befund wie hier; (2) weitere Wiederherellungen an dem geteilten Baum vorher melden, bevor gepusht wird — der Fall geht ins Board, der Owner entscheidet über eine Sperre. In dieser Runde keine weitere Wiederherstellung nötig.

## repo-rule compliance

- Write-set: branch content in `internal/observability/` (`provider_registration.go`, `registry.go`, `migration.go`) + `internal/identityprovider/` integration tests + golden test. No `cmd/baha/app_status_result.go` (card 078), no `.github/**` (Owner scope — no trigger, no rerun), no subagent (§4.8), no `git add -A`, no merge, no force-push on develop/main.
- No duplicate branch: working on the named branch `lane-0428-166-signal-id-normalization-collision`; did not cut a second candidate.
- CI file-size readability: `internal/observability/registry.go` now empty of the split logic; `provider_registration.go` must stay ≤800 lines — verified via `bash scripts/ci-fast-check.sh` OK on the branch (Go file size PASS on CI go-build).
- Evidence lives only in baseharbor-plan; no `.evidence/` in the product repo.

## cleanliness

- Worktree: `/tmp/opencode/x-m166-w3` (fresh clone of github.com/mcpdev80/baseharbor.git, worktree on `lane-0428-166`).
- Containers: none. Compose projects: none. Networks: none. Volumes: none. State dirs: `t.TempDir()` under /tmp, auto-removed.

END x-m166 DONE 0428-166 candidate SHA a83fcc707f814e8d62db2e528d28816196f3e841 (PR #1712, base develop f1c2c34)
