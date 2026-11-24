# PR Sweep Inventory — 2026-11-24

Card family `0428-216` / task `t-20261121-stale-pr-hop-and-baserefs`. Read-only inventory, no product changes, no pushes, no closes/merges. Owner closes/merges.

## PLAN

- Attest planning remote URL + fetch origin develop, confirm planning repo pin is real.
- Fetch origin develop + all open PR heads via git ls-remote; build merge-base ancestry.
- Enumerate open PRs via gh pr list; collect branch, head SHA, base-ref, draft, changed files.
- Compute patch-ids per PR and detect duplicates across open PRs.
- Check for commits authored with a different lane's git identity on each PR.
- Resolve #1650 vs #1818 supersession, #1820 void-run duplication, non-contract base-refs.
- Write this dossier and commit+push atomically to planning repo main.
- Verify path on origin/main; END when published.

## Base attestation

- Planning repo (this repo) confirmed real pin:
  `git remote -v` -> `origin https://github.com/mcpdev80/baseharbor-plan.git`
- NOT `workers/baseharbor-plan` (quarantined bookkeeping checkout).
- Current develop head measured via `git ls-remote`:
  develop = `2b9a2c6d1611ea85e11bf81e9650c28165c8293a`
  main (planning) = `d696c4679351846b5f3f95e15797ac9cfa82a4ed`

## Open PRs (measured against develop = 2b9a2c6d)

| PR | branch | head SHA | base-ref | develop ancestor of head? | behind (develop commits after merge-base) | commits-on-head | changed (non-CI core files) | draft? | patch-id | dup of another open PR? | diff-lane-identity commits | supersession note |
|----|--------|----------|----------|---------------------------|--------------------------------------------|-----------------|-----------------------------|--------|----------|-------------------------|---------------------------|-------------------|
| #1812 | lane-0428-249-runtime-image-fix | f2433d7f | develop | NO — behind | 1 | 1 | `cmd/baha/env_destroy_integration_test.go`, `internal/deployment/environment_destroy_scope.go`, `..._scope_test.go` (+ `.github` pre-release suite) | no | `8fc35132618528a67b34a5e94ed40602ee1a6858` | no | authored `codex@openai.com` (NOT a lane id) — feed to 0428-224 | fix(0428-270-ish ci): reload runtime image before ORAS publish; single commit |
| #1818 | lane-0428-078-cf-fix | 20fc1cb7 | develop | NO — behind | 3 | 4 | keycloak/perses identity dashboard work + operatorauth + metrics | no | `0fd41dbfdcd9589bdd339d99b9e1a2d3077c5569` | no | 3 commits under `246-footprint@baseharbor.local` (lane `w21-pr1702-0428-246-footprint`) + 1 under `w53-0428-152-alertfix` — diff-lane identities; feed to 0428-224 | **Same card 0428-078 as #1650** |
| #1819 | w54-0428-181-export | 17381017 | develop | NO — behind | 1 | 2 | runtime_postgres, perses_dashboard_provision, environment_destroy | no | `a88204e35f81c100912d826ff4feeb73345752a8` | no | 2 authors: `w54-0428-181-export` (own lane) + `0428-061@baseharbor.local` (lane `0428-061-sourcepull`) — diff-lane identity; feed to 0428-224 | 0428-181 export-path work |
| #1820 | fix/broker-build-identity | 28803d11 | develop | NO — behind | 1 | 4 | `cmd/baha/app_broker.go`, `app_broker_compat_test.go` (+ env_destroy tests) | no | `9db1d8ed47d34f378108b87a16ca2f9b0dabb510` | no | 3 commits `0428-061@baseharbor.local` + 1 `worker@baseharbor.local` (lane `lv4-verify`) — diff-lane identity; feed to 0428-224 | **VOID cancelled runtime gate** (`PR · Selected Runtime` cancelled); content NOT in merged #1824; broker commit-identity fix still live |
| #1823 | lane-0428-277-revealallow | 8ffd9fd1 | develop | NO — behind | 1 | 2 | secret_audit, secret_operations, environment_destroy | no | `898fa024ff836c3863493c0b340a6390e4664f55` | no | 2 commits all `0428-061@baseharbor.local` (own lane 0428-061-sourcepull; lane name is 0428-277) | fix(0428-277) fail-closed reveal; newest open 0428-2xx |
| #1650 | lane-0428-078-perses-identity-on-resolver | 84943695 | develop | NO — behind | 8 | 13 (incl hops/merges) | large 0428-078 Perses/Keycloak identity fan-in (24 files) | no | `ebadf230b1fea13db096ae8cea169c0efd0662fa` | no | authors: `Marcel Pfingstgräf` (owner), `246-footprint@baseharbor.local` (own lane), `0428-061@baseharbor.local` — mixed; hop commits carry already-merged base commits | **Same card 0428-078 as #1818** |

All six PRs are **behind** current develop (develop is not an ancestor of any PR head). No two open PRs share a patch-id — **no exact-content duplicates** among the open set. Every open PR touches `internal/deployment/environment_destroy_scope.go` (+ its test and `cmd/baha/env_destroy_integration_test.go`); this is the shared `0428-276` change (#1824, merged 2026-11-24 11:59Z) carried forward — a stale hop artifact on all six heads.

## Specific flag #1

**#1650 vs #1818 — same card 0428-078. Verdict: NOT fully superseded.**

- Both target 0428-078 (Perses/Keycloak identity dashboard).
- #1818 head is **not** built on #1650 head: `git merge-base --is-ancestor 1650 1818` is **false**. merge-base of the two is `d4fa8c58` (#1813, `ci: register open PR gate coverage`), i.e. a shared older develop point, not #1650's tip.
- #1818's real 0428-078 work is 2 commits (`8e2c50c1` select real provider-class labels; `20fc1cb7` wire keycloak dashboard into metrics catalog) sitting on hop commits `e0a93ce0`/`888e2193` that reference #1650.
- #1650's own 0428-078 body (the 114-line `perses_dashboards.go`/`keycloak_files.go`/`perses_dashboards_keycloak.go` change) is **not** present in #1818; #1818 rewrites those files along different lines. The two are **overlapping but divergent** branches on the same card — not a clean superset/subset.
- Net: #1818 is a *conflicting continuation*, not a full supersession. Only one should land; recommend Owner picks one and closes the other. Feed the overlap to card 0428-224.

## Specific flag #2

**#1820 (fix/broker-build-identity, head 28803d11) — VOID cancelled run, content NOT duplicated.**

- GitHub run `PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities)` = `completed | cancelled` (void). Go-unit / vet / build / exact-candidate / focused-python all `success`; the runtime gate is the cancelled one.
- Content (`app_broker.go` `verifyRuntimeBrokerBuildIdentity`: fail closed when both CLI and runtime report a concrete commit and they disagree) is **not** present in merged #1824 (which only touches env_destroy files). No other open PR carries the broker commit-identity change.
- Base freshness: #1820 base merge-base = `05ef4853` (the #1821 commit). develop has moved 1 commit past it. #1820 is a stale-hop branch but its broker fix is still live and unmerged.

## Specific flag #3

**Non-contract base-refs (§3.3.8 stacked bases).**

- All six PRs declare `base=develop`. None has `base` on `main` or a non-develop ref.
- However, #1650 and #1818 carry **stacked/merged base commits** on top of their merge-base:
  - #1650 (merge-base `d4fa8c58` = #1813) carries hop commits that fold in already-merged develop points (`9a49c330 include current develop`, `dfe8f2b7 include merged source pull`) plus merged PR commits — the head is 8 develop-commits behind.
  - #1818 (merge-base `3ebfb90d` = #1815, now merged) sits on a merged base; its head is 3 develop-commits behind and only 246-footprint + w53 do the real 0428-078 work.
  - #1819, #1823, #1812 each sit on `05ef4853` (#1821) — 1 develop-commit behind.
  - None is based on the current develop tip `2b9a2c6d`; all six are stale-hop and would need a rebase onto current develop before landing.

## Diff-lane identity → card 0428-224 (summary)

Every open PR carries at least one commit authored under a lane git identity other than the PR's own lane name:

- #1812: `codex@openai.com` (not a lane id at all) — 1 commit.
- #1818: `246-footprint@baseharbor.local` (lane w21-pr1702-0428-246-footprint) ×3 + `w53-0428-152-alertfix@baseharbor.local` ×1.
- #1819: `0428-061@baseharbor.local` (lane 0428-061-sourcepull) ×1 alongside own lane `w54-0428-181-export`.
- #1820: `0428-061@baseharbor.local` ×1 + `worker@baseharbor.local` (lane lv4-verify) ×1 alongside own lane.
- #1823: all 2 commits own lane `0428-061-sourcepull` (PR lane is 0428-277) — identity/label mismatch.
- #1650: `246-footprint@baseharbor.local` + `0428-061@baseharbor.local` + owner `Marcel Pfingstgräf` — mixed across three identities.

Raw author lists per PR are in the table above; full per-commit `git log` is the source for card 0428-224.

## Method / witnesses

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `2b9a2c6d1611ea85e11bf81e9650c28165c8293a`
- Open PR heads via `git ls-remote ... refs/pull/<N>/head`; ancestry via `git merge-base --is-ancestor origin/develop <pr-head>` in a blob-less clone (`/tmp/prsweep-wt`, remote `origin https://github.com/mcpdev80/baseharbor.git`).
- patch-id via `git diff develop...head | git patch-id --stable`.
- No subagents (§4.8); product repo read-only (fetch/ls-remote/gh pr view/api); no checkout-modify, no GitHub write actions.

## Deliverable

Evidence dossier: `evidence/r28-welle6-2026-11-24/pr-sweep-inventory-2026-11-24.md` (baseharbor-plan).

## cleanliness

- No docker/podman compose projects started this lane. No containers running.
- Scratch clone at `/tmp/prsweep-wt` (blob-less), no artifacts in ecosystem root.

## END

END w71-0428-216-prsweep3 DONE
