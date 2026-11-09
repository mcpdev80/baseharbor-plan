# 0427-173 round 4 — MCP identity stability, applied-intent byte snapshot, one-name docs, base refresh

**Card:** 0427-173 · `t-20261108-bughunt-app-prune-dangling-record`
**PR:** https://github.com/mcpdev80/baseharbor/pull/1505 (head `bcdede014979de5692b2879eb6ddcd17141c2677`)
**Reviewer verdict (r3):** KORREKTUR; approval withheld (act-1505-review-r3.md, vm-bughunt/, plan a236d382)
**Goal of round 4:** close the four open points of the r3 review: (1) carry the authorized deployment identity through authorization AND mutation, (2) snapshot record bytes before the CLI call, (3) remove stale `--uuid`/`-e` selector claims from prune, (4) integrate current develop HEAD `b3a8042d1`.

## PLAN

- Verify live PR head (bcdede01), develop (b3a8042d1), ancestry, candidate origin
- Fix 1: carry authorized resolved identity through authorization AND mutation (no re-resolve in MCP path); add drift regression
- Fix 2: read before-snapshot BEFORE runWithIO for applied-intent byte preservation
- Fix 3: prune stale --uuid/-e from app_prune.go (docs -e for OTHER commands stay)
- Fix 4: rebase candidate on current develop HEAD b3a8042d1
- Local tests: all prune + golden + doc tests green; go vet; go build; gofmt -l clean
- Push candidate, observe hosted CI terminal on exact head (native cells skipped allowed, report as skipped)
- Publish round-4 evidence to baseharbor-plan origin/main; END (terminal only)

## Reality witnesses (before any change)

- Live PR #1505 head (remote, own persistent zone):
  ```
  git -C /tmp/opencode/0427-173-r2-wt ls-remote origin refs/pull/1505/head
  bcdede014979de5692b2879eb6ddcd17141c2677	refs/pull/1505/head
  ```
- develop drift: live `git ls-remote origin develop` => `b3a8042d18ea60f162a32a51df34a499cad6a237`.
- Base attestation: candidate is cut from `bcdede01` (the exact PR #1505 head r3). `b3a8042d1` (current develop) is NOT yet an ancestor of the candidate — integrate before push.

## END
END_PENDING 0427-173-r4: in progress — verifying and integrating before code changes.
