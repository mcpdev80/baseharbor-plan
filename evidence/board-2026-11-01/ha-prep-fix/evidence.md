# ha-prep-fix · Evidence (2026-11-01)

## PLAN
1. [ ] Worktree `ha-prep-fix` off origin/develop (>= 5777c02d).
2. [ ] Inspect `Targeted runtime` job (target lines) and reference jobs (lines 73/144/182/225/274).
3. [ ] Apply minimal patch: add `Prepare verified rootless runtime` step to `Targeted runtime` for the docker leg; document reference-job behavior.
4. [ ] Validate YAML (python yaml.safe_load).
5. [ ] Create PR against develop (title as specified), body with run evidence + reference-job line list.
6. [ ] Observe PR Checks to terminal (`PR Selected Checks` must be success) — eigenes-Run-Pflicht.
7. [ ] Write evidence bullets; publish Planning card via scripts/plan.py + check => 0 errors.

## REPO-RULE COMPLIANCE
- Write-set: exactly `.github/workflows/targeted-integration.yml` + evidence. No product code, no other file, no gate-skip, no matrix changes.
- No Force-Push, no branch-protection bypass, no Release/Tag. PR is a normal push to a feature branch; merge is by another lane/Owner.

## RUNS
- Baseline failure: run 41318456394, job 124883413744 — active docker context never set → engine selection falls to rootless socket → `unix:///run/user/1001/docker.sock unavailable; no fallback` FAIL in 0.39s; etcd/Patroni never reached.

## REFERENCE JOBS (parity)
- (fill: line numbers + exact step text from jobs at lines 73/144/182/225/274)

## PR
- PR nr: (fill)
- HEAD sha: (fill)

## PR CHECKS (terminal)
- `PR Selected Checks` status: (fill) — run id: (fill)

## END
`END_DONE ha-prep-fix: PR=<nr> head=<sha> SelectedChecks=<green|run-id> | <Grund>`
