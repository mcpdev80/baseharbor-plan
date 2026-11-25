# w216-1852-hop — PR-Hop #1852

**Card:** 0428-307 / t-20261125-hunt37-runtime-identity-fallback (PR #1852)
**Role / mission scope:** restore the 3 runtime-identity catalog payload rows as a commit authored w211-0428-307-fallback, on top of current develop 28296a2e6, normal push, watch fresh pull_request run to terminal. No rebase games.
**Owner stop note:** w136 disposition live — do NOT start independent work outside this card.

## Visible Ansatz Block (pre-commit)
- Per-card frontmatter owner (verbatim, fetched from origin/main at runtime): **0428-307** (card t-20261125-hunt37-runtime-identity-fallback).
- Git identity: `user.name=w211-0428-307-fallback`, `user.email=w211-0428-307-fallback@baseharbor.local`.
- Commit invocation: `git -c user.name=w211-0428-307-fallback -c user.email=w211-0428-307-fallback@baseharbor.local commit ...`
- Pre-push `%an/%cn` gate line: `git show -s --format='%an | %cn' HEAD` must equal `w211-0428-307-fallback | w211-0428-307-fallback`.

## Reality Witnesses (git ls-remote, own session)
- Planning repo remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`
- develop tip: `28296a2e6e920592741c9397486358deac7e95b2`
- carrier-0428-307-catalog head (remote): `d3db4d898414ead953afcda530155fdef8b227cf`
- PR #1852: OPEN, headRef carrier-0428-307-catalog, `https://github.com/mcpdev80/baseharbor/pull/1852`

## ROOT CAUSE (w136 akte)
- `10df9c69f` (my earlier 3-parent hop, pushed to remote) was a two-PARENT MERGE (150e3c0e + 28296a2e); during conflict resolution the merge collapsed the payload: its `scripts/pr-gate-coverage.json` blob `293dc02f` has **0** runtime-identity rows. Old blob `68ad2b451` proves the content existed on the carrier base.
- Trusted Plan CI: the 3-parent hop also structurally fails the resolver's integration-parent gate (`parents==3` → exit 1); run `45692231985` = FAILURE.

## RESTORE (corrected)
- Rebuilt on develop tip 28296a2e; restored the 3 rows verbatim from old carrier head 150e3c0e7 (same content, blob 68ad2b451) into `scripts/pr-gate-coverage.json`.
- Committed with identity w211-0428-307-fallback.
- Delta proof: `git diff origin/develop...HEAD -- scripts/pr-gate-coverage.json` = **+27 lines, 0 removed, exactly the 3 runtime-identity rows added**.
- Hop commit `d3db4d898414ead953afcda530155fdef8b227cf` (2 parents: carrier base 150e3c0e + develop 28296a2e), blob = 68ad2b451 (payload intact).

## CI Evidence (fresh pull_request run on current head, per_page=100 census)
- Run **45693544910** — event=pull_request — status=completed — conclusion=**success** — head=d3db4d898414ead953afcda530155fdef8b227cf
- Executed-not-skipped census (all success): Workflow policy, PR · Trusted Plan, PR · Native gate plan, PR · Source format, PR · Validation (receipt-execution-tests, pr-planner-tests, ci-policy, ci-executor-tests), PR · Focused Python, PR · Candidate-added checks (advisory). No non-success among executed jobs.
- Skipped jobs are release/HA gates outside PR scope (Expected full Pre-Release, Targeted HA docker/podman, Draft Go/Main release Go/source, Release Source Preflight, validate, etc.).
- Prior runs for context: 45692231985 (head 10df9c69f) = FAILURE (collapsed payload + 3-parent gate); 45683928092 (head 150e3c0e) = SUCCESS.

## Delivery proof (ls-remote)
- `git ls-remote origin refs/heads/carrier-0428-307-catalog` → `d3db4d898414ead953afcda530155fdef8b227cf`
- PR #1852 headRefOid = `d3db4d898414ead953afcda530155fdef8b227cf` (via gh API)

## END STATUS
END_DONE w216-0428-307-1852hop: hop + payload restored, green on CI.
- new head: **d3db4d898414ead953afcda530155fdef8b227cf**
- ancestry: 2 parents `150e3c0e79cc4f7bacb54311dde50846959d4cde` (carrier base) + `28296a2e6e920592741c9397486358deac7e95b2` (develop)
- run IDs: **45693544910** (pull_request, completed/success)
- delta: `git diff origin/develop...HEAD -- scripts/pr-gate-coverage.json` = +27 lines / 0 removed, exactly 3 runtime-identity rows added
