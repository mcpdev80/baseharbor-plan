# PR #1577 Review R4 — Perses three-state wording

ROLE: CODEX-REVIEW (no merge).

## PLAN

1. Verify exact PR #1577 head/base refs, ancestry, prior PR #1583 closure, PR metadata, and run 43677090058.
2. Scan docs in both languages for unsupported Perses state vocabulary and inspect the two observability how-to passages.
3. Compare verified definitions in all affected passages with the approved #1575 spec and confirm no spec-text drift.
4. Write APPROVE or REJECT with exact ls-remote/run witnesses, validate and publish evidence on origin/main.

## Candidate and provenance

PR #1577 is OPEN and DRAFT, base `develop`, branch `0428-092-perses-boundary`, exact head `2c4ccc311fb1f792a2f1fdaafa343acd8ea3dbcd`. Product `git ls-remote` witness:

```text
2c4ccc311fb1f792a2f1fdaafa343acd8ea3dbcd	refs/heads/0428-092-perses-boundary
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
af308e66d38ad1204345bbe83d066dd7548ea6e6	refs/pull/1575/head
2c4ccc311fb1f792a2f1fdaafa343acd8ea3dbcd	refs/pull/1577/head
e51911a5f3cd7205b6bc4d38cb1cd46d9611925f	refs/pull/1583/head
```

Planning repository root witness (`git rev-parse --show-toplevel`):

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Planning remote witness immediately before publishing this evidence (`git ls-remote origin refs/heads/main`):

```text
db4dff2aff778dcc6bafd699aae4e52aded23786	refs/heads/main
```

PR metadata confirms #1577 is OPEN/DRAFT at that head, and #1583 is CLOSED (`closedAt` `2026-11-15T03:15:21Z`) at the superseded `e51911a5` head. Current `develop` `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` is an ancestor of the candidate. The base-to-head log since the r3 head `e51911a5f3cd7205b6bc4d38cb1cd46d9611925f` contains only the task commit:

```text
2c4ccc311fb1f792a2f1fdaafa343acd8ea3dbcd docs(0428-077): align how-to Perses prose to three-state names + verified-health-probe (r3)
```

The exact-head run witness from `gh run view 43677090058 --repo mcpdev80/baseharbor --json databaseId,status,conclusion,event,headSha,workflowName` is:

```json
{"conclusion":"success","databaseId":43677090058,"event":"pull_request","headSha":"2c4ccc311fb1f792a2f1fdaafa343acd8ea3dbcd","status":"completed","workflowName":"CI · Source & Quality"}
```

## State wording review

Verdict: REJECT. The r4 changes resolve the obsolete state value in the two how-to passages, but leave the r3 release/reference finding open and omit an accepted `not_configured` case in both how-to passages.

1. `docs/how-to/observability.md:32` and `docs/de/how-to/observability.md:28` now name `not_configured`, `configured_unverified`, and `verified`, and both state that `verified` requires an actual Perses health observation. However, both define `not_configured` for unselected Perses or an invalid pin only; the approved spec also requires a selected declaration with an unavailable pin to be `not_configured`. Recipe: include both invalid and unavailable pins in the fail-closed `not_configured` branch in EN and DE.

2. The four release/reference passages remain unchanged by r4 (`docs/releases/v0.4.28.md:15`, `docs/de/releases/v0.4.28.md:13`, `docs/reference/releases.md:31`, `docs/de/reference/releases.md:30`). They say the current Core has no health probe and reachability stays unverified, but they do not explicitly define `verified` as available only after a real health-path observation. EN release additionally says the seam must gate on actual provisioning before a release reports `verified`; provisioning alone is weaker than the approved spec and can imply a false positive. Recipe: amend each of those four paragraphs to state that `verified` requires a real Perses health probe observing the surface; a valid pin or provisioned container alone cannot produce it.

3. Approved #1575 spec at exact head `af308e66d38ad1204345bbe83d066dd7548ea6e6`, `docs/spec/management-access-v1.md:51-64`, defines exactly: `not_configured` for no selection or invalid/unavailable pin; `configured_unverified` for selected plus validated pin without a real health-path observation; and `verified` only when a real Perses health probe observes the surface. The r4 how-to change states the health-probe condition, and the two obsolete `unsupported` state uses are gone. Grep witness: `rg -n -i 'perses.*(unsupported|not supported)|(unsupported|not supported).*perses' docs` returned `no Perses unsupported/not supported matches`. The remaining mismatches are the unavailable-pin case in the how-to pair and the missing positive verified definition in the four release/reference passages.

4. `git diff --stat e51911a5..2c4ccc31` shows only `docs/how-to/observability.md` and `docs/de/how-to/observability.md`; `git diff --check` passes. The #1575 r8 verdict remains APPROVE at exact head `af308e66d38ad1204345bbe83d066dd7548ea6e6`, run `43670440466` completed/success. Card 0428-077 is review/CI acceptance-ready subject to the merge frost. Card 0428-092 / PR #1577 remains not acceptance-ready until findings 1 and 2 are corrected and reviewed.

## repo-rule compliance

Read-only review of a fresh clone at exact PR head. No product or workflow files, PR metadata, tests, containers, or VMs were changed or run. No merge was performed. Evidence is stored only in the actual `baseharbor-plan` repository.

END mission-rev1577-r4.md DONE — REJECT #1577 at `2c4ccc311fb1f792a2f1fdaafa343acd8ea3dbcd`; how-to unavailable-pin coverage and four release/reference verified definitions remain open.
