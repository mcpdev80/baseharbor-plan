# PR #1577 Review R3 — Perses release/reference wording

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1577 head/base ancestry, branch provenance, PR #1583 closure, and specified pull_request run.
2. Compare all four English and German release/reference passages with the exact three-state definitions in the approved #1575 spec.
3. Search Perses contexts for unsupported and legacy state vocabulary; reconcile the r2 recipe and acceptance readiness of both cards.
4. Write verdict and evidence, validate and publish on planning origin/main, verify remote evidence, and post END.

## Candidate and provenance

PR #1577 is OPEN and DRAFT, base `develop`, branch `0428-092-perses-boundary`, exact head `e51911a5f3cd7205b6bc4d38cb1cd46d9611925f`. The exact product `git ls-remote` output is:

```text
e51911a5f3cd7205b6bc4d38cb1cd46d9611925f	refs/heads/0428-092-perses-boundary
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
e51911a5f3cd7205b6bc4d38cb1cd46d9611925f	refs/pull/1577/head
e51911a5f3cd7205b6bc4d38cb1cd46d9611925f	refs/pull/1583/head
af308e66d38ad1204345bbe83d066dd7548ea6e6	refs/pull/1575/head
```

Planning repository root witness (`git rev-parse --show-toplevel`):

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Planning remote witness immediately before publishing this evidence (`git ls-remote origin refs/heads/main`):

```text
5cb90b034d617faa25cb456f098863c5347a1690	refs/heads/main
```

The fetched `develop` SHA `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` is an ancestor of `e51911a5`. The #1577 log from the initial card head `29dba54dddb02f48568c571e9ce37f671d21e6aa` contains exactly one correction commit, `e51911a5`; the ancestry check passes and `git rev-list --count 29dba54..e51911a5` is `1`. The r2 provenance recipe is satisfied: #1577 uses its existing card branch, and PR #1583 is CLOSED (`closedAt` `2026-11-15T03:15:21Z`) with the same old correction head. The pre-existing `/tmp/opencode/mission-rev1577-r3-wt` directory was not used or modified; the fresh review clone is `/tmp/opencode/w077-pr1577-review-r3-wt`.

The specified run witness from `gh run view 43671511011 --json databaseId,status,conclusion,event,headSha,workflowName` is:

```json
{"conclusion":"success","databaseId":43671511011,"event":"pull_request","headSha":"e51911a5f3cd7205b6bc4d38cb1cd46d9611925f","status":"completed","workflowName":"CI · Source & Quality"}
```

## Contract comparison and findings

Verdict: REJECT. The four named passages correct `unsupported` to `not_configured` and `configured_unverified`, but the Perses documentation still contains stale state vocabulary and does not state the full `verified` definition required by the approved #1575 contract.

1. The latest #1575 spec at candidate `af308e66d38ad1204345bbe83d066dd7548ea6e6`, `docs/spec/management-access-v1.md:51-64`, defines exactly three states: `not_configured` for no selected working surface or invalid/unavailable pin; `configured_unverified` for selected plus validated pin without a real health-path observation; and `verified` only when a real Perses health probe observes the surface. Pin validation alone cannot produce `verified`.

2. The four requested files use the first two states but do not carry the complete verified definition. EN release `docs/releases/v0.4.28.md:15` says no release reports Perses verified when it is not provisioned, and DE release `docs/de/releases/v0.4.28.md:13` similarly ties the limit to provisioning. EN reference `docs/reference/releases.md:31` and DE reference `docs/de/reference/releases.md:30` say reachability stays unverified because there is no health probe, but none states positively that `verified` is reserved exclusively for an actual probe observing the surface. This leaves provisioning as an ambiguous proxy for health. Recipe: align all four passages with the spec by stating that `verified` is emitted only after an actual Perses health-path observation; a valid pin or successful provisioning alone is insufficient. Preserve the existing `not_configured` and `configured_unverified` definitions in both languages.

3. Legacy vocabulary remains in Perses contexts outside those four files. `docs/how-to/observability.md:32` says an unprovisioned selected Perses surface is `unsupported`; `docs/de/how-to/observability.md:28` uses the same `unsupported` state. The repository grep `rg -n -i -C 2 'perses.{0,250}(unsupported|not supported|not_configured|configured_unverified|verified|health probe|health-path|unverifiziert|nicht konfiguriert)|(unsupported|not supported).{0,250}perses' docs --glob '*.md'` found these stale Perses assertions. Recipe: replace both with `configured_unverified` and state that reachability remains unverified absent a real health probe. Keep `unsupported` only for concepts that are not state names and are genuinely unsupported, not as a Perses status value.

4. The requested four-file diff is otherwise clean: `git diff --check 29dba54..e51911a5` passes. The r2 correction moved the existing one-commit documentation fix onto the proper #1577 branch and closed the stray PR; no branch or PR changes were made by this review.

## Related card readiness

PR #1575 is OPEN and DRAFT on exact head `af308e66d38ad1204345bbe83d066dd7548ea6e6`. Its r8 review `evidence/r28-welle1-2026-11-15/perses-seam/act-1575-review-r8.md` records APPROVE for card 0428-075 and exact-head run `43670440466` completed/success. Card 0428-075 is review/CI acceptance-ready subject to the standing merge frost. Card 0428-092 / PR #1577 is not acceptance-ready until findings 2 and 3 are corrected and reviewed. No merge was performed or authorized here.

## repo-rule compliance

Read-only review in a fresh clone at the exact PR head. No product, workflow, PR metadata, or task files were changed; no tests, containers, or VMs were run. Evidence is stored only in the actual `baseharbor-plan` repository. The existing review worktree path was left untouched.

END mission-rev1577-r3.md DONE — REJECT #1577 at `e51911a5f3cd7205b6bc4d38cb1cd46d9611925f`; #1575 card 0428-075 remains review/CI acceptance-ready subject to merge frost.
