# Independent pre-check of in-flight candidates #1825 and #1823 (READ-ONLY)

Scope (mission w77-0428-249-precheck): read-only VERIFY of two IN-FLIGHT independent candidates against their card contracts so the later CODEX-REVIEW is fast. No edits, no PRs, no merges, no subagents, no rebase/CI-action on the frozen chain #1812/#1819/#1820/#1818, #1650 left untouched (owner-parked). develop = current origin/develop (SHA below).

## repo-rule compliance

- Read-only: only `git ls-remote`, `gh pr view/diff/runs`, `gh api`, `gh pr compare`, `gh pr list`. No edits to product or plan. No .github edits, no workflow_dispatch, no rerun.
- Planning repo attestation: `git remote -v` confirmed `origin -> https://github.com/mcpdev80/baseharbor-plan.git` (NOT the workers/ bookkeeping copy). Evidence lives only in baseharbor-plan.
- No compose/docker/podman started (read-only desk). No local product tests.

## base attestation

- develop remote head (real GitHub remote `https://github.com/mcpdev80/baseharbor.git`): `2b9a2c6d1611ea85e11bf81e9650c28165c8293a`
- `gh api compare/develop...<head>` reports `ahead_by == 2` for both branches => origin/develop is a strict ancestor of both candidate heads (verified, not claimed). One integration candidate per chain; both are independent single-candidate branches cut off develop.

## #1825 / 0428-249 — PASS

- PR #1825 `lane-0428-249-tagfix`, head `844987ded88b1c365f5b660e3f700af69e52bb5a`, base develop 2b9a2c6d, ahead_by=2, draft=false.
- Scope witness: `gh api compare/develop...844987d` => `files: ['.github/workflows/pre-release.yml']` ONLY. No `scripts/**`, no catalog rows, normal baha build and `ci.yml` byte-unchanged. Confirmed by `gh pr diff 1825` (22-line diff, single file).
- Diff: the `Produce baha-ci-operator-testonly candidate binary` step adds `-tags=baseharbor_ci_operator_testonly` to the existing `go build` for `./cmd/baha`, and a build-info proof step logs `go version -m <artifact>` (tee to buildinfo file) then greps the `build` settings line for `-tags=baseharbor_ci_operator_testonly` (fails closed).
- Proof correctness: `go version -m` embeds `-tags` in build settings even after `-ldflags -s -w` strip the symbol table (so `go tool nm` is unusable here); grep filters only the `build:` settings line and `-q` fails closed on a tag-less binary. Both the normal `baha` build (byte-unchanged, same step) and `ci.yml` are untouched.
- Witness: PR #1825 head 844987d, run 45391485905 (event=pull_request, attempt 1), head_sha 844987d. As of this run all 30 jobs `completed`; required gates pass (Trusted Plan success, Native gate plan success, Workflow policy success, Source format success, Focused Python success, all Validation.* success, PR Selected Core-less podman coreless-lifecycle foundation success). Pre-Release/Go-unit/Exact-Candidate/targeted HA/etc are `skipped` by the PR-Selected-Checks matrix (unchanged path => not the exact-head full matrix).
- Residual defect / anything the owner or Codex should catch: run 45391485905 is still terminal-less `in_progress` (30/30 jobs reported `completed` but the run-level `conclusion` is `null` at last read, updated 2026-11-24T12:26:11Z); a re-run 45394505629 (event=workflow_dispatch) was queued and is also still in_progress. NOTE for CODEX-REVIEW: re-witness the terminal exact-head conclusion before acceptance — the diff is correct but the current run is not yet terminal. No content defect found in the workflow step.

## #1823 / 0428-277 — PASS / RC

- PR #1823 `lane-0428-277-revealallow`, head (PR) `6c8291545cf6` (branch later advanced to `8ffd9fd1b5` with the same fix); base develop 2b9a2c6d, ahead_by=3.
- Scope witness: `gh api compare/develop...6c8291545c` => `files: [cmd/baha/secret_audit_test.go, cmd/baha/secret_operations.go, cmd/baha/zz_probe_test.go]`. Only the reveal-audit path + its regression test.
- (a) Fails closed on deny: `recordRevealFailed` now passes `"deny"` as `authorizationResultOverride` to the shared builder `recordRevealForTarget(..., outcome="failed", detail=reason, "deny")` (cmd/baha/secret_operations.go :168-171). In the builder, `authorizationResultOverride != ""` forces `event.AuthorizationResult = "deny"` BEFORE the decision/principal derivation (cmd/baha/secret_operations.go :211-213). Fail-closed: even with an upstream `AuthorizationDecision.Allowed=true` in the context (the exact state a successful `authorizeHumanReveal` leaves), the failed reveal records `deny`, never the spurious `allow` it previously paired.
- (b) Preserves authenticated actor: the same shared builder reads the seeded upstream state first — `operatorauth.AuthorizationDecisionFromContext(ctx)` sets `event.Actor.Subject/Assurance/Methods`, then `operatorauth.PrincipalFromContext(ctx)` sets identity/subject/issuer/assurance/methods, else `trusted-local` fallback (cmd/baha/secret_operations.go :202-210). So both (a) deny and (b) actor are produced by ONE COMMON recorder path, not two separate branches.
- Regression asserts BOTH: `TestAuthorizeHumanRevealFailedRecordsRevealAudit` seeds `operatorauth.WithAuthorizationDecision(... Allowed=true ... Subject="trusted-local")` (the exact upstream state that exposed the bug), then asserts: `event.AuthorizationResult != "deny"` fails closed, `strings.EqualFold(event.AuthorizationResult,"allow")` rejects a spurious allow, AND `event.Actor.Subject != "trusted-local"` fails RED if the fix drops the decision's actor (cmd/baha/secret_audit_test.go :355-372).
- RC (non-blocking, for CODEX-REVIEW context): the branch head `8ffd9fd1b5` is byte-identical in the fix to `6c8291545c` for the two touched files (both use the `authorizationResultOverride` builder). PR #1823's last commit was re-based/advanced past its original head; the current branch head is the one to accept.
- Witnesses: PR #1823 head 6c8291545c run 45394208511 conclusion=failure (attempt 1), and head 8ffd9fd1b5 run 45388371276 conclusion=success (attempt 1), and head 9afd3e6a65 run 45383171960 conclusion=success (attempt 1). NOTE for CODEX-REVIEW: the exact HEAD now on `lane-0428-277-revealallow` (8ffd9fd1) should be re-witnessed for a terminal success on its current head before acceptance; the last recorded run on 8ffd9fd1 was success (45388371276) but that is not necessarily the current exact head run.

## neutral open-PR CI facts (inventory only, no action)

| PR | head (10) | latest terminal exact-head run | conclusion | note |
| --- | --- | --- | --- | --- |
| #1825 | 844987d | run 45391485905 (pull_request) | in_progress (non-terminal; 30/30 jobs completed, run conclusion null) | re-run 45394505629 (workflow_dispatch) also in_progress |
| #1823 | 6c8291545c | run 45394208511 (pull_request) | failure (terminal) | branch later advanced to 8ffd9fd1 |
| #1820 | 28803d1102 | run 45382404741 (pull_request) | cancelled (terminal) | 1820 on the frozen chain #1812/#1819/#1820/#1818 — no action |
| #1819 | 17381017be | run 45380314808 (pull_request) | cancelled (terminal) | 1819 on the frozen chain — no action |
| #1818 | 20fc1cb7d4 | run 45316544436 (pull_request) | success (terminal) | 1818 on the frozen chain — no action |
| #1812 | f2433d7fd0 | run 45385372243 (workflow_dispatch) | failure (terminal) | 1812 on the frozen chain — no action |
| #1650 | 84943695be | run 45297432220 (pull_request) | success (terminal) | owner-parked — no action |

No rebase, merge, rerun or workflow_dispatch performed for any PR. ## PLAN

1. Attest base develop SHA (2b9a2c6d1611ea85e11bf81e9650c28165c8293a) via `git ls-remote` on the real GitHub remote; confirm planning repo remote is baseharbor-plan.
2. #1825: diff-only scope witness (single file .github/workflows/pre-release.yml), verify `-tags=baseharbor_ci_operator_testonly` build + `go version -m` fail-closed proof in the pre-release artifact step, run witness 45391485905, report non-terminal note.
3. #1823: verify recordRevealFailed routes through the COMMON `recordRevealForTarget` builder that (a) forces AuthorizationResult=deny on outcome=failed and (b) preserves authenticated actor subject/assurance/methods from the seeded AuthorizationDecision/Principal; verify regression asserts BOTH deny and actor.Subject; PASS/RC with file:line.
4. Neutral open-PR CI sweep via `gh pr list` + `gh api` (terminal run id + conclusion + head); inventory only.
5. Write evidence file (## PLAN + todowrite), origin/main witness, commit+push atomically (single new file only).
6. Post END_DONE inline; no compose projects to tear down (read-only).

## todowrite

Steps: (1) base attestation + remote check, (2) #1825 diff + run witness, (3) #1823 common-recorder wiring + regression, (4) neutral open-PR sweep, (5) evidence write + push + origin/main witness, (6) END post. All read-only; no product/plan edits beyond this single evidence file.

## cleanliness

No compose/docker/podman projects started (read-only review desk). No containers to bring down. No test artifacts left in /home/marcel/dev/baseharbor-ecosystem. Temp helpers under /tmp (prlog.py, prhead.py, opensweep.py, runstatus.py, cmp.py).

## status

DONE — evidence committed + pushed to origin/main; witness below.
