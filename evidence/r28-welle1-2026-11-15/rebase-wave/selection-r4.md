# rebase-wave: Perses selection merges the accepted Perses seam (r4 merge)

## PLAN

- Establish reality witnesses: ls-remote seam + selection heads; planning repo path.
- Cut working branch from selection base head a270725b; record exact base SHA as ancestor proof.
- Verify seam head 492b8e8f is accepted (Luna r4 APPROVE witness).
- Merge seam head into working branch (normal merge, no rebase/force); file-for-file conflict list.
- Run go build ./..., go test ./internal/metrics/... -run Perses (targeted), readability audit.
- Write this akte (numbered, before/after SHAs, test output, conflict solutions, cleanliness).
- Push merge commit to lane-0428-080-r28-perses-selection; verify PR #1590 head; origin/main evidence before END.
- END with new selection head SHA; compose cleanliness.

## Mission

Merge lane-0428-080-r28-perses-selection (selection head ~a270725bd) with the ACCEPTED Perses seam-head 492b8e8f994b16e6f73819a08175f8178cd63292 (PR #1575 / task t-20261114-r28-perses-contract-seam). Rebase-wave task: NO feature scope. Protocol: working branch from selection-head, MERGE of seam-head (no rebase/force of the split branch), conflicts minimal bilaterally-preserving, file-for-file conflict list in akte; go build ./..., targeted Perses test, readability audit; normal merge-commit-push on lane-0428-080-r28-perses-selection (PR #1590 head follows; drafts stay drafts). Limits: NO force-push, NO .github/**, no develop-merge, no ready_for_review, no feature-changes, NO subagent.

## Repo provenance

- Planning repo: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (ONLY correct path).
- `git rev-parse origin/main` in planning repo:
  - a3e11b2f419a8e4e9effd988e0f79a65dbee8f34
- `git ls-remote origin` on planning repo (main line):
  - a3e11b2f419a8e4e9effd988e0f79a65dbee8f34	refs/heads/main
  - a3e11b2f419a8e4e9effd988e0f79a65dbee8f34	HEAD

## Remote witnesses (ls-remote)

- baseharbor `refs/heads/lane-0428-075-perses-seam`:
  - 492b8e8f994b16e6f73819a08175f8178cd63292
- baseharbor `refs/heads/lane-0428-080-r28-perses-selection`:
  - a270725bdd795a5c944caf96fd1161ec44688a55

## Base / anchor attestation

- Base ref cut from: origin/lane-0428-080-r28-perses-selection = a270725bdd795a5c944caf96fd1161ec44688a55
- This is the selection head. The working branch is cut from exactly this SHA.
- Ancestor proof: the working-branch first commit lists only the merge commit on top of a270725b; `git merge-base` of branch and seam == 492b8e8f after merge, and a270725b is an ancestor of the merge.

## Acceptance witness (Luna r4)

- File: evidence/r28-welle1-2026-11-15/perses-seam/act-luna-1575-r4.md
- Reviewer: Codeman 1a678edb-8783-4c14-9707-eddde1e8d286 (codex-rev-pr1575), Model GPT-6-Luna, 2026-11-15 23:08 UTC.
- Reviewed head: 492b8e8f994b16e6f73819a08175f8178cd63292 == refs/heads/lane-0428-075-perses-seam == refs/pull/1575/head.
- Verdict: APPROVE exact candidate 492b8e8f994b16e6f73819a08175f8178cd63292 for PR #1575 / task t-20261114-r28-perses-contract-seam. r3 capability-claim finding resolved (Perses is a distinct management-surface contract, no Metrics claim). Exact-head hosted run 43771897861 SUCCESS.

## Steps

1. ls-remote witnesses established (above); planning path confirmed.
2. Working branch cut from a270725b.
3. Seam head 492b8e8f accepted — Luna r4 APPROVE witness recorded above.
4. Merge seam head into working branch; conflicts listed below.
5. go build ./..., go test ./internal/metrics/... -run Perses, readability audit.
6. Akte written here.
7. Merge push to lane-0428-080-r28-perses-selection; PR #1590 head verified.
8. END with new selection head; compose clean.

## Merge result

- Method: normal fast-forward-protected merge (git merge 492b8e8f) of seam-head into selection working branch. No rebase, no force-push.
- Merge commit SHA: 8ce0df9148e4f388ba18386e3b731f1fc2cbd500
- Parent 1 (selection head): a270725bdd795a5c944caf96fd1161ec44688a55
- Parent 2 (seam head): 492b8e8f994b16e6f73819a08175f8178cd63292
- Ancestor checks: `git merge-base --is-ancestor a270725b HEAD` -> YES; `git merge-base --is-ancestor 492b8e8f HEAD` -> YES.
- `git log --oneline -3`: 8ce0df914 (this merge) / 492b8e8f (seam) / a270725b (selection base). Only my merge commit on top; no foreign commit carried.
- `git diff --check`: clean (no conflict markers).

## Conflict list (file-for-file)

- No conflict markers; clean three-way merge. Changed files (all bilateral Perses changes preserved, both heads' contributions present):
  - internal/capability/perses.go — 90 lines changed: Perses now a distinct management-surface contract (from seam) on top of the selection work.
  - internal/capability/perses_test.go — 144 lines changed.
  - internal/metrics/perses_contract_test.go — 50 lines changed.
  - Net: 192 insertions, 92 deletions. No file required manual conflict resolution; both heads' semantics retained.

## Tests

- go build ./...: EXIT 0 (no errors).
- go test ./internal/metrics/... -run Perses -count=1: ok github.com/mcpdev80/baseharbor/internal/metrics 0.006s — EXIT 0.
- go vet ./internal/metrics/...: EXIT 0; go vet ./internal/capability/...: EXIT 0.
- source-readability audit (>800 lines?): verbatim from scripts/source-readability-audit.sh — "Go file size PASS (<= 800 lines or no worse than explicit baseline) / Function span PASS (<= 200 lines or no worse than explicit baseline) / Regression ratchet PASS". Changed file sizes: perses.go 302 lines, perses_test.go 164 lines, perses_contract_test.go 81 lines — all well under 800.

## Before / After SHAs

- Before (selection head / base cut from): a270725bdd795a5c944caf96fd1161ec44688a55
- Seam head merged (accepted): 492b8e8f994b16e6f73819a08175f8178cd63292
- After (new selection head / merge commit): 8ce0df9148e4f388ba18386e3b731f1fc2cbd500
- Remote head now: `git ls-remote origin lane-0428-080-r28-perses-selection` -> 8ce0df9148e4f388ba18386e3b731f1fc2cbd500
- PR #1590 head: `git ls-remote origin refs/pull/1590/head` -> 8ce0df9148e4f388ba18386e3b731f1fc2cbd500
- Stray temp branch work/0428-080-r28-selection-r4merge deleted from remote (before: 8ce0df914 present; after: gone). Only the named candidate carries the merge.

## Cleanliness

- Compose/docker/podman projects started: none (this is a pure merge task; no containers launched).
- No containers left running; daemon address pools untouched.

## END

DONE
