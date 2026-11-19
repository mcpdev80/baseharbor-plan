# Exact-head documentation gate witness — PR #1697

Maintainer-directed sweep update, 2026-11-19. The original 0428-153 witness-only scope was extended by the Maintainer's instruction to finish eligible open PRs by fixing, checking, and merging. PR #1697 has now been merged after the required hosted witness.

## Candidate and gate selection

- PR head: `d1f97a63a38271a1326b5b49faf114028e67a26a` (branch `lane-0428-131-en-docs-warning-term`).
- Target `develop`: `28fb427f057499efca705c1b7459e7653bd532a8`.
- `git ls-remote origin refs/heads/lane-0428-131-en-docs-warning-term` returned `d1f97a63a38271a1326b5b49faf114028e67a26a`.
- `git diff --name-only origin/develop...HEAD` returned exactly three `docs/internal/*.json` files: `v0.4.25-destruction-workspace-checkpoint.json`, `v0.4.25-external-provider-delivery-source-evidence.json`, and `v0.4.25-installation-destruction-runtime-evidence.json`.
- Local `scripts/pr-diff-base.py` plus `scripts/pr-gate-plan.py` output at that exact head had `coverage_status: resolved`, `broad_required: false`, and required `documentation-audit`, `mkdocs-en-strict`, `mkdocs-de-strict`, and `pages-candidate-build`.
- Trusted planner mapping in `scripts/pr-gate-plan.py`:
  - `{'id': 'documentation-audit', 'owner': 'scripts/documentation-audit.sh', 'command': 'bash scripts/documentation-audit.sh'},`
  - `path.startswith('docs/internal/') and path.endswith('.json')`
  - `require(DOC_CHECKS)`

## Hosted exact-head execution

- Run: [44622989624](https://github.com/mcpdev80/baseharbor/actions/runs/44622989624), terminal `success`, PR #1697 at the exact head above (workflow synthetic merge `ee57be7aed13669aff74c8752eea0e7ec9844ae9`, based on `28fb427f`).
- Documentation job: [PR · Validation · documentation-audit](https://github.com/mcpdev80/baseharbor/actions/runs/44622989624/job/135909418860), terminal `success`.
- Job log identifies `Complete job name: PR · Validation · documentation-audit`; the authenticated job environment selected `VALIDATION: documentation-audit`; executed command: `bash scripts/documentation-audit.sh`.
- Output included `EN/DE page coverage OK: 171 matched Markdown pages`, `DE technical integrity: PASS (171 paired pages)`, `Documentation audit`, and `Internal evidence PASS`.
- The exact run also passed Workflow policy, PR Trusted Plan, PR Source format, PR Focused Python, strict EN and DE MkDocs, and Pages candidate build. Unrelated Go/native/release jobs were skipped by impact selection.
- Local `bash scripts/documentation-audit.sh` also passed after exposing `python3` as `python` in a temporary PATH shim; no repository file was changed for this environment workaround.

## Merge result

- No unresolved review threads; PR was ready, mergeable, and had no blocking review submissions.
- PR #1697 merged with expected head `d1f97a63a38271a1326b5b49faf114028e67a26a` as merge commit `4b3a3559070e9b81b1886a357f6a46bc6dfce790`.
- The merge closes EN warning-term task 0428-131 and supplies the documentation-audit acceptance witness for 0428-144 / PR #1705.
