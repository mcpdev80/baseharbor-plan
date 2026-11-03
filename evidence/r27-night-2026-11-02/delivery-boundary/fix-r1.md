# delivery-boundary fix round r1 — w3-delivery-r2

- **Role:** Worker (lane `w3-delivery-r2`), correction round to PR #1333.
- **Task:** `t-20261018-r27-delivery-boundary` (active). Coord `f49a3303`.
- **Candidate head:** `be6ce48f6d15a1be288e90a8ff79cc9dfa3235d9` (unchanged — no code change possible within write-set).
- **Remote heads (ls-remote, verified):** `work/r27-delivery-boundary = be6ce48f...`, `develop = 470642ac...`.
- **Repo:** `mcpdev80/baseharbor`, worktree at `/tmp/opencode/w3-delivery-r2-wt` (branch `work/r27-delivery-boundary`), not the main session checkout.
- **Local checks:** `go build ./...` green; `go test ./internal/delivery ./internal/deployment` green (`ok`).
- **Result:** `END_BLOCKED` — step 3 (B1, KERN) cannot be completed within the card write-set. See stop reason below.

## Plan

1. (B3, history) rebuild history from develop without `8a2aa75f`/removal authority commits.
2. (B4, docs) fix DE `aufgehalten werden` → `erfasst/protokolliert` and the false "empty owner rejected" claim (EN+DE) → `Selection.Normalize` defaults empty owner for direct mode.
3. (B1, KERN) add the one-writer guard to the real deployment production apply/observe path.
4. (B2, docs) standards/feature-check clauses → concrete qualified support or "not qualified".

## repo-rule compliance

- **STOP criteria honored:** no CI files touched; no merge/release/tag; no changes to `docs/spec/credential-access-v1.md` or `coreinstallation/stableid` (parallel-lane territory).
- **No authority commits:** current branch already contains none; net diff vs `develop` is 7 files, all card write-set.
- **Write-set:** card scope = `docs/spec/delivery-provider-v1.md` (EN/DE) + `internal/delivery/contract.go` + `internal/delivery/contract_test.go` + `docs/decisions/0022-...` (EN/DE). `internal/deployment/**` is NOT in this scope.

## Findings (from review #1333)

1. **B3 history** — Already clean. `git log 470642ac..be6ce48f` contains no `8a2aa75f` and no removal-authority commits; net diff = 7 files, all card write-set. Rebuild NOT needed. ✅ (satisfied pre-work)
2. **B4 docs** — DE still uses `aufgehalten werden` (line 73, 142) which does NOT mean "recorded". Both EN (line 129) and DE (line 132) still claim "empty owner is rejected", which contradicts `Selection.Normalize` (contract.go:64-66) that defaults empty owner to `OwnerBaseHarbor` for `ModeDirect`. **Both still unfixed** in current candidate.
3. **B1 one-writer guard** — **BLOCKED** (see below).
4. **B2 standards/feature checks** — **BLOCKED** (see below; tied to same scope boundary as B1).

## B1 — one-writer guard: BLOCKED (outside write-set)

**What the task/ADR require.** Task "one writer per resource" + ADR 0022 §2 ("a selection observing both a direct `baseharbor` owner and a delegated `external` owner active for the same resource set fails closed; BaseHarbor reports the conflict and refuses to apply or observe"). Review #1333 #1: the guard must live in the *actual* production apply/observe path, with positive (direct/delegated) and negative (conflicting-owner, unauthorized-mutation) tests + fixtures.

**Why it is blocked.** The guard cannot be built in this card's write-set. The canonical production apply path is `internal/deployment/deployment_store.go` `SaveDeploymentRecord` (file:144) → `record.Applied.Delivery.Validate()` (file:155). The observation (two-active-owners conflict detection) belongs on `ObservedDeployment` (`internal/deployment/deployment_store.go:67-80`), a struct that is **never populated by any production code** (`Observed` on `DeploymentRecord` is dead state — no `ObserveDeployment` exists anywhere in the module). Both `internal/deployment/**` files are outside this card's write-set. ADR 0022 §2 is therefore currently a *documentation assertion* with no enforcing code: the observed conflict never reaches the applied selection's validation.

**Feasibility proof (outside module build).** A standalone proof-of-concept (deleted after use, kept only under `/tmp`) compiles and passes positive/negative cases, proving the design is realizable by editing files outside this write-set:

```go
// refuseDirectMutation(applied Selection, observed Observed) error
//   1. applied.Validate()                // existing single-record contract (delivery)
//   2. if observed.Conflict  { return ErrConflictingOneWriter }   // ADR 0022 §2 fail-closed
//   3. if applied.Mode==Direct && observed.Owner==External { return ErrUnauthorizedMutation }
```

`internal/deployment` imports `internal/delivery` (contract.go) — the guard can call the accepted `Selection.Validate()` and add the conflict/ownership denial on the `Observed` observation at the `SaveDeploymentRecord` apply path — no new module, no import cycle.

**Exact boundary (for Coordinator / Task-Vertrag):**
- Real production apply path: `internal/deployment/deployment_store.go:144` (`SaveDeploymentRecord`) — line 155 validates the applied selection; the conflict guard must be inserted **here (≤ file:155)**, after validation, before the state write.
- Observation source: `internal/deployment/deployment_store.go:67` (`ObservedDeployment`) — must be populated (e.g. an `ObserveDeployment` on the deployment record or a conflict check in `reconciliation.Evaluate`-driven path, `internal/capability/lifecycle.go:354`/`427`).
- Card write-set (mine): `docs/spec/delivery-provider-v1.md`, `internal/delivery/contract.go`, `internal/delivery/contract_test.go`, `docs/decisions/0022-...` (EN/DE).
- Not mine (needs Coordinator coordination): `internal/deployment/**` (all files), `internal/capability/lifecycle.go`, `internal/reconciliation/**`.

**Decision required from Coordinator / Task-Vertrag:** (a) extend this card's write-set to include `internal/deployment/` (owner decision), or (b) route B1 to the deployment/owner lane. Either way the docs fixes in #2/B4 can still land here; #3/B2 remain open because concrete qualified feature/version support must be evidenced in the same `internal/deployment` production path this card may not own.

## B4 — docs fixes (still pending, would be a separate small commit)

Not executed because B1 is the KERN blocker and the mission steps are sequential (B3→B4→B1→B2). When B1 scope is resolved, B4 is a contained EN/DE doc edit within the write-set and needs no external coordination:
- DE line 73 & 142: `aufgehalten werden` → `erfasst/protokolliert` (recorded).
- EN line 129 & DE line 132: replace "empty/unknown owner is rejected" with the actual contract: empty owner defaults to `baseharbor` for `direct` mode (`Selection.Normalize`, contract.go:64-66); empty owner is *not* a valid delegated selection.
- DE line 93: `stillständig` → `ständig` (typo in the feature-check clause).

## Local checks

```
$ cd /tmp/opencode/w3-delivery-r2-wt
$ TMPDIR=/tmp GOCACHE=/tmp/bh-w3-gocache go build ./...
ok  github.com/mcpdev80/baseharbor/internal/delivery         0.005s
ok  github.com/mcpdev80/baseharbor/internal/deployment       0.013s
```

## END

END_BLOCKED w3-delivery-r2: head=be6ce48f6d15a1be288e90a8ff79cc9dfa3235d9 step=3 | B3 history already clean. B1 one-writer guard BLOCKED — production path internal/deployment/deployment_store.go SaveDeploymentRecord (file:144), outside card write-set; exact boundary + feasibility proof documented; B4/B2 ready once write-set resolved.
