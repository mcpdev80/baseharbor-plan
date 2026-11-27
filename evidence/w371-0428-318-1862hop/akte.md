# Akte — w371-0428-318-1862hop (0428-318 / baseharbor PR #1862)

## What
Forward-squash (integrating develop tip) of product card **0428-318**, product-PR **#1862** `0428-318 low-severity pair: guard executor image + S3 admin file` on branch `lane-0428-318-lowpair`, plus registration of the two uncataloged runtimeexecutor sources so the required PR `Trusted Plan` check resolves instead of failing.

## Visible Ansatz Block (visible, pre-commit)

- Owner verbatim (card 0428-318 frontmatter, owner field): `w371-0428-318-1862hop`
- Git identity: `user.name=w371-0428-318-1862hop`, `user.email=w371-0428-318-1862hop@baseharbor.local` (both author and committer, set per command; global config `w351-0428-359-bhop3` was unset from env)
- Literal commit invocation:
  `git -c user.name=w371-0428-318-1862hop -c user.email=w371-0428-318-1862hop@baseharbor.local commit ...`
- Literal merge invocation:
  `git -c user.name=w371-0428-318-1862hop -c user.email=w371-0428-318-1862hop@baseharbor.local merge --no-ff baseharbor/develop`
- Pre-push admission gate (verified): `git show -s --format=%an HEAD` == `w371-0428-318-1862hop` exactly

## Reality witnesses (remote, own tooling)

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `ea5218d72e263f21e79853b679af50074dab8c25`
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1862/head` (pre) => `ab65312c56fef2b217ee4f6581aa75686374450f`
- PR #1862: `headRefName=lane-0428-318-lowpair`, base `develop`, state OPEN, title `0428-318 low-severity pair: guard executor image + S3 admin file`

## Catalog fix (gate route, no waiver)

Gate failure (runs 45926926999 and 45929247724, head `2fcf32609`, class #136 Landing-Gate / `PR Trusted Plan` step 4 `Resolve exact immutable PR inputs`):

```
ValueError: invalid trusted PR gate coverage catalog: uncataloged source change,
no declared runtime gate owner: internal/runtimeexecutor/compose.go
(id source.internal_runtimeexecutor_compose_go): add ...
"surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]
... internal/runtimeexecutor/compose_test.go (id source.internal_runtimeexecutor_compose_test_go) ...
```

Both sources are pre-existing files (present at old head `c04d92df` and `ab65312c`, NOT in the old..new diff): the landing gate #136 changed them. Fix added to `scripts/pr-gate-coverage.json` under `packages`:

- `{"id":"source.internal_runtimeexecutor_compose_go","path":"internal/runtimeexecutor/compose.go","surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}`
- `{"id":"source.internal_runtimeexecutor_compose_test_go","path":"internal/runtimeexecutor/compose_test.go","surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]}`

`python3 scripts/validate-pr-gate-coverage.py --coverage scripts/pr-gate-coverage.json` => `PR gate coverage catalog is valid` (exit 0). `resolve_covered_gates([...compose paths...])` => `unresolved=[]`, selected gate `atomic/docker/data-capabilities`. Same exact fix already landed remotely as `2fcf32609` (w370-0428-318-1862hop, catalog-only, no develop-merge) — reset onto it to keep one integration candidate.

## Head / parents / run IDs

- Candidate head: **`6a1d63430bd542f7628919c0278e542fd86324cd`**
  - `H=6a1d63430 ... an=w371-0428-318-1862hop ae=w371-0428-318-1862hop@baseharbor.local cn=w371-0428-318-1862hop ce=w371-0428-318-1862hop@baseharbor.local`
  - parent pair = `(2fcf326092e4066f71d3ed7641ed231ce49a55dc, ea5218d72e263f21e79853b679af50074dab8c25)` — develop parent is the current tip `ea5218d7`
- `git diff ab65312c56fef2b217ee4f6581aa75686374450f..HEAD --name-only` (old head .. new head):
  - `internal/application/manifest_validation.go`, `internal/application/workload.go`, `internal/application/workload_test.go`, `scripts/pr-gate-coverage.json`
- `git log --oneline baseharbor/develop..HEAD` = only my merge commit `6a1d63430` on top of `2fcf32609` / `ab65312c5` / `c04d92df1` — no foreign commit
- Delivery proven: `git ls-remote ... refs/pull/1862/head` and `refs/heads/lane-0428-318-lowpair` both == `6a1d63430`
- Push: `2fcf32609..6a1d63430 lane-0428-318-lowpair -> lane-0428-318-lowpair` (normal push, no force)

## CI — Hosted runs (class comparison)

- Head `2fcf32609` (catalog-only, w370): run **45926926999** and run **45929247724**, both FAILURE in class #136 Landing-Gate, `PR Trusted Plan` step 4 fails with the uncataloged-source ValueError above (pre-existing — the landing gate that changed compose.go is on the old head, not my diff).
- Head `6a1d63430` (my forward-squashed candidate): run **7949** queued by GitHub on push; awaited to terminal, no Cancel.

## STOP criteria check

- No conflict outside write-set. Catalog change is within the card write-set (CI routing file). Product files in the diff are the landing-gate #136 changes already on the branch, carried by the develop-merge — no new product edit.
- No foreign commit carried on top (only my merge commit).

## Baseline-gated blocker (owner end-befund 2026-11-27 03:26)

The source registration for the #136 landing-gate sources
`source.internal_runtimeexecutor_compose_go` +
`source.internal_runtimeexecutor_compose_test_go` is a BASELINE-FAMILIE change
(#136 / 0428-359) that must land on develop through its own lane. It is NOT part
of this PR (#1862). Reverting the catalog to the owner baseline therefore
re-introduces the same Trusted Plan failure the baseline family owns.

Head `5c20c2e32` (catalog cleanly removed, confirmed clean) -> Run **45933999005**
terminal FAILURE, class **GATE-136 (Trusted Plan)**:

```
FAIL 140292877390 | PR · Trusted Plan  (STEP 4 Resolve exact immutable PR inputs)
FAIL 140293003170 | PR Selected Checks (STEP 5)
ValueError: invalid trusted PR gate coverage catalog: uncataloged source change,
no declared runtime gate owner: internal/runtimeexecutor/compose.go
(id source.internal_runtimeexecutor_compose_go): ... surfaces
["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]
... internal/runtimeexecutor/compose_test.go (id source.internal_runtimeexecutor_compose_test_go) ...
```

No retrigger / rerun of #1862 until the baseline family (#136 / 0428-359) lands
those lines on develop.

## Run witnesses (three)

- 45931218713 — head `6a1d63430` (with catalog lines) — FAILURE, class GATE-136 (owner-baseline finding)
- Revert-hop run — head `5c20c2e32` (catalog reverted) — FAILURE, class GATE-136 (owner end-befund)
- 45933999005 — head `5c20c2e32` — FAILURE, class GATE-136, job 140292877390 `PR Trusted Plan` step 4, exact ValueError above

## END line

END_BLOCKED w371-0428-318-1862hop: head `5c20c2e32`, parents (6a1d63430, ea5218d7), catalog reverted to owner baseline, forward-squash onto develop pushed, delivery 5c20c2e32. Class = **BASELINE-GATED**: #136 landing-gate source registration must land on develop via baseline family (#136/0428-359), not this PR. No retrigger of #1862. Run witnesses 45931218713, revert-hop run, 45933999005. Session freed for coordinator.
