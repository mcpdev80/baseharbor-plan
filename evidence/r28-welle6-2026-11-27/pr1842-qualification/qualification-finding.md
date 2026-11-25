# PR #1842 pin qualification finding (read-only analysis)

- Card: t-20261125-0428-284-1812-postretry-gate-failure, lane w177-0428-284-demo-pin-1812
- PR: https://github.com/mcpdev80/baseharbor/pull/1842 (DRAFT, base develop)
- Head: 317d2f2593336a4e4dddfa7f4d304bc034ee5515 (single additive commit)
- Change: `docs/releases/v0.4.28.demo-ref` only, b41127723e523134a1c14ee3c36cf133237162ce -> 1a3c055cc0eef3f961722f12d843e33f6c1ca43e (the merged Demo develop tip incl. PR #175 consent-retry)

## Run witness
- CI run 45603924448 (run_number 7717), attempt 1 AND attempt 2, both on exact head 317d2f259, terminal conclusion `success`.
- Executed (6, all success): PR · Draft source and routing, PR · Draft Go · cli-0/1/2/3, packages.
- Skipped (27): PR Selected Checks, PR · Native gate plan, PR · Native, PR · Demo Pin, PR · Trusted Plan, PR · Exact Candidate, all Main release / release groups.

## Root cause of the skips (READ-ONLY, exact ci.yml lines)
- Every required-native / PR-Selected-Checks / release group carries the guard `github.event.pull_request.draft == false`.
  - ci.yml line 1502: `PR · Selected Checks`  `if: ... && github.event.pull_request.draft == false`
  - ci.yml line 556:  `PR · Native · ...`      `if: ... && github.event.pull_request.draft == false`
  - ci.yml line 529:  `PR · Native impact`     `if: ... && draft == false && needs.pr_native_impact.outputs.required == 'true'`
  - ci.yml line 1080: `PR · Demo Pin`          `if: ... && draft == false && (runtime||integration||public_contracts)==true`
- PR #1842 is a draft (isDraft=true) => those groups are correctly skipped BY DESIGN.
- The skip is NOT a data-only-pin effect (the file path is irrelevant to the skip). It is a draft-vs-ready gate: converting #1842 to ready fires the required gates.

## Two-run rule
- The draft Go + source/routing jobs ran twice green on the identical head (attempt 1 + attempt 2).
- The missing required gates (native / demo-pin / PR Selected Checks) execute only on a non-draft PR.

## Decision sought from CODEX (w136, merge-authorization authority)
- (1) Convert PR #1842 to ready so the required native/demo-pin/selected gates fire and reach terminal green, OR
- (2) Defer that qualification to the #1812 ready-PR requal head (post pin merge).
- Cite the ruling in your akte. No merge and no #1812 opening until the ruling is recorded.
