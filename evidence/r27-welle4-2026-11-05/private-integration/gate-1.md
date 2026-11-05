# CODEX-GATE — PR #1379 draft->ready + selected-check observation at exact head

Lane: w166-private-gate. Coord: f49a3303. Card: t-20261104-r27-private-integration-path.
Candidate branch: work/r27-private-integration (PR #1379). Reviewed head: 52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9.

## PLAN

- Confirm PR #1379 is DRAFT with head exactly 52be57c9893 (remote ref match)
- Set PR #1379 from draft to ready via `gh pr ready 1379 -R mcpdev80/baseharbor`
- Trigger + observe a new run to terminal state; record run-id and the named `PR Selected Checks` status; no rerun rat
- Verify run head SHA is exactly 52be57c9893 via ls-remote + a run log line listing only own commits
- Both mode cells (shared/geteilt vs private/privat) evidenced at the new head via run/logs, not just locally
- Write this evidence file; post END to f49a3303

## Step 1 — PR state confirmed

Remote ref and PR head both fixed at `52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9`:

- `git ls-remote origin work/r27-private-integration` -> `52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9 refs/heads/work/r27-private-integration`
- `gh pr view 1379` -> state=OPEN, isDraft=true (before), headRefOid=52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9, baseRefName=develop

Write set: eight files (manifest.go, manifest_parse.go, provider_placement.go, r27_private_integration_test.go, cmd/baha/use_target.go, cmd/baha/use_target_connection_test.go, internal/coreinstallation/selection.go, selection_test.go). Scope contract: ONLY the draft->ready switch + observation. No content change, no base-merge, no .github file touched.

## Step 2 — draft cleared

`gh pr ready 1379 -R mcpdev80/baseharbor` -> marked "ready for review".
Verified: `gh pr view 1379` -> isDraft=false, state=OPEN.

## Step 3 — new run to terminal (no rerun rat)

New run triggered by the ready-for-review transition: **run-id 41978410480** (`CI · PR #1379`).
Watched to terminal myself (self-run duty 4.6); terminal conclusion SUCCESS. No rerun issued.

Per-job result in run 41978410480:

- PR Selected Checks: COMPLETED / SUCCESS (the job previously skipped under draft)
- PR · Validation · go-unit-tests: COMPLETED / SUCCESS
- PR · Validation · go-build: COMPLETED / SUCCESS
- PR · Validation · go-vet: COMPLETED / SUCCESS
- PR · Validation · source-contracts: COMPLETED / SUCCESS
- PR · Focused Python: COMPLETED / SUCCESS
- Workflow policy: COMPLETED / SUCCESS
- PR · Trusted Plan: COMPLETED / SUCCESS
- Release Source Preflight / Targeted HA (docker,podman) / validate / PR · Exact Candidate / Consumer Pins / Public Contracts / Demo Pin / Runner Interface / Selected Runtime: SKIPPED (not part of this candidate's qualification scope per trusted plan)

Run log log line (PR Selected Checks -> Require normal selected job results):
`EXPECTED_HEAD: 52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9`
`git merge-base --is-ancestor "$EXPECTED_BASE" "$EXPECTED_HEAD"` with `EXPECTED_BASE`/BASE_SHA `e444ae117173dcf84e7aa8b17f73c020d3e2923c`.

## Step 4 — provenance (own commits only)

Branch provenance via `gh api .../compare/develop...52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9`:

- base_commit (develop tip): `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7` (r27 device-enrollment #1371)
- commits on candidate vs develop (ONLY my own): `r27 (w144): add private-mode backend switch (own DB+KV in own net)`
- No foreign commit carried on top. Base head `develop...52be57c9893` lists exactly one commit, my own — satisfies branch-provenance-as-proof. Run 41978410480 head_sha `52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9` matches remote ref.

Trusted plan (run artifact trusted-pr-plan/pr-plan.json): merge_base_sha `e444ae117173dcf84e7aa8b17f73c020d3e2923c`, head_sha `52be57c9893d2d824b8cfbcfec97ca4c7fb26ef9`, integration_sha `45a58aa9d7fa810b876e336c824a54bc6a34eeb0`, coverage_status=resolved, selected_gates=[] (valid because coverage resolved), required_validation_checks go-build / go-unit-tests / go-vet / source-contracts.

## Step 5 — both mode cells evidenced at the new head (via run, not just local)

`go test ./internal/application/...` (contains r27_private_integration_test.go) at exact head 52be57c9893:

- source-contracts job (run 41978410480): `ok  	github.com/mcpdev80/baseharbor/internal/application	2.542s`
- go-unit-tests job (run 41978410480): `ok  	github.com/mcpdev80/baseharbor/internal/application	3.697s`

Both mode cells resolve as the review's counter-probes established, and the package test suite passed at this exact head:
- shared/geteilt default (no switch): ResolveConfiguredProviderPlacement -> sql/shared, SQL + Valkey stay shared.
- private/privat (runtime.private: true): SQL + Valkey forced to application scope; manifest parser accepts only the explicit boolean under runtime:.

No content change, no base-merge. Base drift only listed (review already recorded: develop since e444ae11 carries #1378, #1382, #1369, #1381, #1362, #1371). Next round handles a base-merge if needed.

## Repo-rule compliance

- No .github file read-modified or touched (workflow files belong to Owner). Only read the workflow log lines read-only as evidence.
- No product-code change; ONLY draft->ready switch + observation.
- No rerun rat; single new run observed to terminal.
- No subagents (Owner directive 2026-11-04); every step run inside this session.
- No scratch files in the ecosystem root; caches under /tmp.
- No secrets logged.

## END

END_DONE w166-private-gate: head=52be57c9893 ready=ja lauf=41978410480 (PR Selected Checks=success, terminal) zellen=belegt (internal/application ok at exact head via source-contracts 2.542s + go-unit 3.697s) | PR von draft auf ready geschaltet, ausgewählter PR-Check läuft nun terminal Grün am exakten Kopf; beide Moduszellen am Kopf belegt, kein Content/Base-/Workflow-Change.
