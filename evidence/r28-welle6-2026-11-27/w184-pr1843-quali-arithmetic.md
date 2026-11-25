# w184 row-count reconciliation — PR #1843 / card 0428-319

Lane: w184-0428-319-pr1843-quali
Date: 2026-11-25 (host clock)
Mission: coordinator/missions/w184-pr1843-quali.txt

## Owner count-check (authoritative, binding)

Per the owner arithmetic append on 2026-11-25:

- F1 = 6 rows
- F2 = 28 rows (the hunt-1.md F2 heading "25 rows" is a typo — the F2 table body is 28 rows)
- F3 = 2 rows
- F4 = 2 rows
- **TOTAL = 38 rows repaired**
- F5 = explicitly NO change (must not be counted)

The H-V44 hunt-1.md "40 per-row reference defects" headline is inconsistent with its own
itemized families (6 + 28 + 2 + 2 = 38, plus F5 = 0). Nothing in this lane identifies two
additional true defects, so the authoritative count is **38**, not 40. F5 / the #1844
EN-only policy work is a SEPARATE PR and does not add product rows here.

## Evidence this matches the exact head content (7e1fc3a57 / corrected 1c73aa6e)

Verified against `git show 9f7da6d4` (the content commit carried by the corrected head):

- F1: 6 lines changed across `docs/releases/v0.4.28.md`, `docs/reference/releases.md`,
  `docs/how-to/observability.md` and the three DE counterparts (plain-text
  `docs/spec/management-access-v1.md` → relative link).
- F2: 28 lines changed — 2 current-state pointer sentences (v0.2.0.md:55, v0.3.0.md:3)
  repointed as links + 26 retired-path annotations (v0.4.5:13, v0.4.6:7, v0.4.7:6).
- F3: 2 lines (credential-access-v1.md:129, DE:129) marked as a path that never existed.
- F4: 2 lines (provider-conformance-v1.md:7, DE:7) gained the directory-mapping sentence.
- F5: 0 lines (no edit).

Total added/deleted lines in the content commit: 38 / 38 (verified: 15 docs files changed,
38 insertions(+), 38 deletions(-)).

## Scope correction (this akte)

The lane first committed a stray top-level file `w184-arithmetic.md` (outside docs/**)
to baseharbor. That is out of the docs-only write-set and would have made the PR body scope
claim false. Corrected with ONE additive `git rm` commit (author
`w181-0428-doclink-sweep`, `%an` verified), so the corrected candidate head is
`1c73aa6e` carrying only the 15 docs/** files (15-file, 38/38 line diff against develop).

## Second distinct run ID (w182 requirement)

w182 requires a DISTINCT second run ID on the unchanged final head. The prior rerun of run
45609710215 produced attempt-2 of the SAME databaseId (counts as one run ID) — not qualifying
as a second ID. The corrected head invalidates all prior runs. The supported route (owner
confirmed): ci.yml fires on `pull_request` (push) AND on `ready_for_review` (draft→ready),
both on an unchanged SHA. Run #1 = the natural push-triggered `pull_request` run on the
corrected head; run #2 = a `gh pr ready` toggle producing a distinct databaseId on the same
head_sha. Both verified terminal green via the Actions API before handoff.
