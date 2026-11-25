# w183-0428-320-0428-audits-enonly — card 0428-320 (t-20261125-hunt44-audits-en-only-declaration)

Docs-only: declare the internal-audits tree explicitly EN-only in `docs/STYLE_GUIDE.md` (parity scope = nav pages), per hunt H-V44 finding F5 (`evidence/r28-welle6-2026-11-27/bughunt-hv44-doc-links/hunt-1.md`).

## PLAN

- Step 1: Re-verify anchor via ls-remote (develop tip) and read hunt akte F5. DONE
- Step 2: Inspect current docs/STYLE_GUIDE.md + docs/internal tree structure at tip. DONE
- Step 3: Worktree from attested base SHA; minimal docs edit declaring internal tree EN-only. DONE
- Step 4: Local non-test precheck `bash scripts/documentation-audit.sh`. DONE (pass after wording fix — see gate note)
- Step 5: Single candidate commit with lane identity; %an gate. DONE
- Step 6: Push branch, open one DRAFT PR. DONE (PR #1844)
- Step 7: Watch Hosted CI to terminal; two same-head greens (45613935675, 45614592648, both success, PR Selected Checks pass). DONE
- Step 8: Evidence commit to baseharbor-plan main. IN PROGRESS
- Step 9: origin/main ls-tree witness; END post. PENDING

- Post-push witness (evidence on origin/main before END): `git -C baseharbor-plan fetch origin main && git ls-tree -r --name-only origin/main | grep evidence/r28-welle6-2026-11-27/w183-0428-320-audits-enonly` output: `evidence/r28-welle6-2026-11-27/w183-0428-320-audits-enonly/evidence.md`. Evidence commit a98f5df90 (author `w183-0428-320-0428-audits-enonly`), pushed to main; sits directly on origin/main 0f035ef4b.

## END w183-0428-320-0428-audits-enonly DONE — candidate 2c19c945786da8dd1065f96bfef33bf8fbbdf722, PR https://github.com/mcpdev80/baseharbor/pull/1844 (ready for review), Hosted CI same-head greens: runs 45613935675 and 45614592648 (PR Selected Checks pass, job 139207172390)

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

Two same-head greens, both observed to terminal by this lane (watched via `gh run watch`):
- Run 45613935675 "CI · Source & Quality" (draft-stage scheduling), head 2c19c9457, completed success. Jobs that actually executed and passed: PR · Draft source and routing, PR · Draft Go · cli-0..3, PR · Draft Go · packages (jobs 139204340515/40883/40919/41019/41034/41157).
- Run 45614592648 "CI · Source & Quality" (ready-for-review), head 2c19c9457, conclusion recorded at handoff below. Docs-path jobs that ran and passed there: Workflow policy, PR · Source format, PR · Native gate plan, PR · Trusted Plan, PR · Validation · documentation-audit (139206705541), mkdocs-en-strict (139206705535), mkdocs-de-strict (139206705618), pages-candidate-build (139206705494).
- Aggregate "PR Selected Checks" on run 45614592648: pass, job 139207172390. PR is ready-for-review (moved at handoff).

## cleanliness

- No containers/compose started by this lane; no docker/podman on this host.
- `docker ps -a` before: only the ambient `codeman-app` (Up About an hour); after: identical (see below for terminal witness). Lane pid at check: shell pid recorded in transcript.
- Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/0428-320-audits-enonly-wt` (lane-owned).

## repo-rule compliance

- One PR, one card; branch `lane-0428-320-audits-enonly` cut from current develop tip; no second branch.
- No .github edits, no workflow_dispatch, no reruns triggered by hand (PR push started ordinary CI).
- Evidence lives only in baseharbor-plan; nothing written to a product repo main branch.
- No subagents used.
