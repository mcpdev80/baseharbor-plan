# w183-0428-320-0428-audits-enonly — card 0428-320 (t-20261125-hunt44-audits-en-only-declaration)

Docs-only: declare the internal-audits tree explicitly EN-only in `docs/STYLE_GUIDE.md` (parity scope = nav pages), per hunt H-V44 finding F5 (`evidence/r28-welle6-2026-11-27/bughunt-hv44-doc-links/hunt-1.md`).

## PLAN

- Step 1: Re-verify anchor via ls-remote (develop tip) and read hunt akte F5. DONE
- Step 2: Inspect current docs/STYLE_GUIDE.md + docs/internal tree structure at tip. DONE
- Step 3: Worktree from attested base SHA; minimal docs edit declaring internal tree EN-only. DONE
- Step 4: Local non-test precheck `bash scripts/documentation-audit.sh`. DONE (pass after wording fix — see gate note)
- Step 5: Single candidate commit with lane identity; %an gate. DONE
- Step 6: Push branch, open one DRAFT PR. DONE (PR #1844)
- Step 7: Watch Hosted CI to terminal; record two same-head run IDs. PENDING
- Step 8: Evidence commit to baseharbor-plan main. PENDING
- Step 9: origin/main ls-tree witness; move PR to review; END post. PENDING

## Witnesses

- Planning repo remote (before first evidence commit): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` = `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`.
- Base attestation: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = `2a141387dbbaf24f52501a0f66f1abf61cf8fcda refs/heads/develop`; branch cut from that exact SHA (worktree add at 2a141387d).
- Ancestor test: `git merge-base --is-ancestor 2a141387d... HEAD` -> ANCESTOR_OK.
- Log line: `git log --oneline 2a141387d..HEAD` = `2c19c9457 docs(0428-320): declare internal-audits tree EN-only in style guide` (own commit only; two intermediate commits were folded into one before push, so the branch carries a single candidate commit).
- Name-only diff: `git diff origin/develop...HEAD --name-only` = `docs/STYLE_GUIDE.md`.
- Candidate head: `2c19c945786da8dd1065f96bfef33bf8fbbdf722`, author `%an` = `w183-0428-320-0428-audits-enonly` (identity gate verified before push).
- Push delivery: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-320-audits-enonly` = `2c19c945786da8dd1065f96bfef33bf8fbbdf722 refs/heads/lane-0428-320-audits-enonly`.
- PR: https://github.com/mcpdev80/baseharbor/pull/1844 (draft until handoff).

## The change

`docs/STYLE_GUIDE.md` "Repository structure":
- Added to the German-parity paragraph: "EN/DE parity is measured on mkdocs nav pages only."
- Extended the release-audits sentence: "The internal audits tree is English-only by design: it is maintainer-facing, not part of the nav parity scope, and needs no German counterpart. German pages that cite an internal audit link to the canonical English source directly."

Wording note: an earlier draft backticked `docs/internal/` / `docs/de/internal/`; `scripts/check_de_translation_integrity.py` requires every inline code literal of a paired EN page to appear verbatim in `docs/de/STYLE_GUIDE.md` (docs/** de/internal excluded, lines 23 of the script). To keep the change minimal (no DE-side edit needed beyond the declaration itself), the final wording avoids path literals; the existing `internal/` bullet in the structure list already carries the path context.

## Gate coverage

Docs-only prose change; no new tests. Route: PR -> "CI · Source & Quality" workflow, "Validate documentation" step (`.github/workflows/ci.yml:139-144`: mkdocs build --strict EN+DE + `bash scripts/documentation-audit.sh`), triggered by the `pull_request` event on this PR head. No `.github/**` touched.

## CI (self-run, §4.6)

- Run: 45613935675 "CI · PR #1844 / Source & Quality" on head 2c19c9457. Status watched to terminal below.
- Second same-head ID: check-suite run per workflow (recorded below when terminal).

## cleanliness

- No containers/compose started by this lane; no docker/podman on this host.
- `docker ps -a` before: only the ambient `codeman-app` (Up About an hour); after: identical (see below for terminal witness). Lane pid at check: shell pid recorded in transcript.
- Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/0428-320-audits-enonly-wt` (lane-owned).

## repo-rule compliance

- One PR, one card; branch `lane-0428-320-audits-enonly` cut from current develop tip; no second branch.
- No .github edits, no workflow_dispatch, no reruns triggered by hand (PR push started ordinary CI).
- Evidence lives only in baseharbor-plan; nothing written to a product repo main branch.
- No subagents used.
