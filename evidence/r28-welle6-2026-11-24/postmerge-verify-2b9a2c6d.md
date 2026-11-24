# Post-Merge Verification Desk — r28 Welle 6 (Bug-Hunt fill, Befund only)

Card: w74-0428-216-postmerge. Read-only adversarial verification of the three cards
merged into develop this window; no edits, no PRs, no merges, no subagents (§4.8).

## PLAN

- Fetch origin/develop, record SHA, confirm >= 2b9a2c6d
- Item 1 (#1821 / 0428-270): dead trusted-local fail-open seam gone, fail-closed path
- Item 2 (#1822 / 0428-273/274/275): 6 pr-gate-coverage.json rows each resolve to an executed gate
- Item 3 (#1824 / 0428-276): per-deployment VerifyDeploymentOwner re-check gates applyEnvironmentDestroyScope
- List any cmd/baha/*.go or internal/*.go changed by the three with NO required-gate admission row
- Write Befundakte table with per-item PASS/FINDING, FINDING gets proposed card number + file:line repro
- Commit + push atomically (single file only; pull --rebase origin main first)
- Bring down any containers; post END_DONE

## Repo / provenance attestation

Planning repo (verified):
```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
```
(only origin/main here carries evidence; workers/baseharbor-plan is a bookkeeping dir — never used)

## Evidence commit

(origin/main path witness + commit SHA recorded at END)

## 1. #1821 / 0428-270 — operatorauth trusted-local fail-open seam

Files: internal/operatorauth/authorization.go, internal/operatorauth/config.go

### Read-only reproduction

`<fill from git show / gh>`

### Result
PASS / FINDING

## 2. #1822 / 0428-273/274/275 — pr-gate-coverage 6 rows

File: scripts/pr-gate-coverage.json (6 rows) + pre-release.yml binary

### Read-only reproduction (pr-gate-plan.py read-only)

`<fill>`

### Result
PASS / FINDING

## 3. #1824 / 0428-276 — environment destroy owner re-check

Files: cmd/baha/env_destroy.go (guard), internal/deployment/environment_destroy_scope.go

### Read-only trace

`<fill>`

### Result
PASS / FINDING

## 4. Silent-skip risk: changed files with NO required-gate admission row

`<list>`

## Summary table

| Item | Card | Result | FINDING file:line |
| --- | --- | --- | --- |
| 1 | #1821 / 0428-270 | PASS / FINDING | — |
| 2 | #1822 / 273-275 | PASS / FINDING | — |
| 3 | #1824 / 0428-276 | PASS / FINDING | — |
| 4 | silent-skip sweep | — | — |

## END
END_DONE w74-0428-216-postmerge: post-merge verification desk complete — see table (candidate SHA: <commit>)
