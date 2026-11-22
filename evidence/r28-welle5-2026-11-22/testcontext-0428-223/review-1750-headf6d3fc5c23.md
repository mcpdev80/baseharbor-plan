# CODEX-REVIEW: PR #1750 exact live head

## PLAN

1. Verify the current live PR head, develop ref, PR state, and exact hosted run.
2. Compare live head `f6d3fc5c23e4a3097d4d36130303338b0ff180bd` with approved head `17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99` and the prior reviewed hop.
3. Confirm the exact-head CI aggregate is terminal and inspect failed jobs.
4. Publish this SHA-named review evidence, then allow the separate merge step only if all gates pass.

Session marker: 1450c201
Review role: CODEX-REVIEW, read-only
Candidate: `f6d3fc5c23e4a3097d4d36130303338b0ff180bd`
Develop at review start: `5ca8420c1814f25bea6404e55fd054c60746eae5`

## Verdict

VERDICT: APPROVE

## Hop comparison

`git log 5d47569f3372f76078b040490c261d43233e1d92..f6d3fc5c23e4a3097d4d36130303338b0ff180bd` lists hop commit `f6d3fc5c2` and develop commit `5ca8420c1` (`fix(0428-183): valkey dashboards gated on real availability (#1714)`). The diff from the prior reviewed head contains exactly the four files from merged PR #1714: `internal/metrics/perses_dashboards_valkey.go`, its test file, and two Valkey testdata files. Compared with approved #1750 content, this candidate adds only develop content; it introduces no new #1750 product or test change.

## Live refs and PR state

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1750/head` returned:

    5ca8420c1814f25bea6404e55fd054c60746eae5 refs/heads/develop
    f6d3fc5c23e4a3097d4d36130303338b0ff180bd refs/pull/1750/head

PR #1750 is OPEN, not draft, mergeable, and has `mergeStateStatus=CLEAN` against this exact develop base.

## Exact-head CI

Run `44990801974` completed SUCCESS on exact head `f6d3fc5c23e4a3097d4d36130303338b0ff180bd` with zero failed jobs. Required aggregate `PR Selected Checks` job `137112288306` completed SUCCESS from Actions integration `15368`. Executed relevant jobs include `PR · Go unit · packages` `137111247768` SUCCESS and `PR · Go unit · cli-2` `137111247806` SUCCESS.

## Repo-rule compliance

Read-only product review. No local tests, product changes, workflow dispatch, PR comment, merge, or close performed. Planning remote verified before commit: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push).

## Cleanliness

Before review: PID `2523699`; `docker ps -a` returned no containers. No containers or compose projects were started.

## END codex-rev2-1736 DONE

APPROVE PR #1750 at live head `f6d3fc5c23e4a3097d4d36130303338b0ff180bd`; its hop adds only develop content from #1714. Exact run `44990801974` completed SUCCESS.

## CI selection detail

This exact-head run completed with 14 successful jobs, 0 failed jobs, and 21 skipped jobs. `PR · Validation · go-build` (`137111247772`), `PR · Validation · go-vet` (`137111247789`), and `PR · Native gate plan` (`137111206801`) passed. `validate` (`137111207599`), `PR · Native · ${{ matrix.id }}` (`137111239451`), `PR · Native Keycloak/Core · ${{ matrix.runtime }}` (`137111249223`), and `PR · Selected Runtime` (`137111249509`) were skipped. PR #1756 remains OPEN and unmerged; these native selection skips are expected before #1756 adds the native catalog rows, and they are not treated as passing receipts or as a defect in this #1750 hop.

## Final exact-head CI and skipped selection record

Run `44990801974` is terminal `completed / SUCCESS` at `f6d3fc5c23e4a3097d4d36130303338b0ff180bd`: 14 successful jobs, 0 failed jobs, 21 skipped jobs. Required aggregate `PR Selected Checks` job `137112288306` passed from GitHub Actions integration `15368`. Validation build `137111247772`, validation vet `137111247789`, and Native gate plan `137111206801` passed. The selected `validate` job `137111207599`, Native matrix `137111239451`, Native Keycloak/Core `137111249223`, and Selected Runtime `137111249509` were skipped. These skips are expected before #1756 adds the native catalog rows; they are not counted as passing receipts or treated as a defect in this hop.

## Post-review cleanliness

Session PID `2537271`; `docker ps -a` returned only its header and no containers
## Publication witness

Exact path listed by `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle5-2026-11-22/testcontext-0428-223/review-1750-headf6d3fc5c23.md`:

`evidence/r28-welle5-2026-11-22/testcontext-0428-223/review-1750-headf6d3fc5c23.md`
