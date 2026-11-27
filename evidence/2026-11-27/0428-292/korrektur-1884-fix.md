# Evidence — 0428-292 apply candidate-consent UX · CORRECTION round (CODEX-comparative verdict)

Lane: w399-0428-289-providers · Card: t-20261116-r28-bug-apply-consent-ux (0428-292) · Repo: baseharbor
Mission: coordinator/missions/w399-next-1884-fix.txt · PR #1884 content-correction on head e6425f9bf7

## PLAN (fix round)

0. todowrite leg SKIPPED — no native todowrite tool in this session; live board file workers/todos/w399-0428-289-providers.json (a) + this ## PLAN (b) maintained
1. Read comparative verdict + card + baseharbor/AGENTS.md; verify remote truth (PR #1884 @ e6425f9bf7, develop 6944e8761a) — DONE
2. Visible Ansatz block (owner verbatim from origin/main, identity, invocation, %an gate) — next section
3. Branch continuity: fix commit lands directly on the PR #1884 head (NO merge, NO rebase — mission line 6)
4. Finding (1): make the bind prompt decide and consume the SAME stream so an interactive [y/N] really counts as granted consent (the card bug) — DONE
5. Finding (2): resolve the app_remote_lifecycle.go comment-vs-code contradiction toward the card goal without weakening any consent check — DONE
6. Regressions positive + negative in cmd/baha/app_candidate_consent_test.go, existing CI route, no .github touch — DONE
7. Pre-checks gofmt/vet/build only; docker ps before/after with pid in ## cleanliness — DONE
8. ONE fix commit 4e499b3cf6 under canonical lane identity, EIN normaler push, ls-remote delivery proof — DONE
9. Two sequential pull_request runs on the exact head (push + close/reopen); format gate green; Trusted Plan stays red (class-A, cited) — DONE (46046111688 + 46046309439)
10. Akte published via plan branch+PR; card wait_reason 'corrected at <head>, gate green pending lift' — this file
11. END line + candidate SHA — final section

## VISIBLE ANSATZ BLOCK

- Card frontmatter owner VERBATIM from origin/main (git show origin/main:tasks/t-20261116-r28-bug-apply-consent-ux.md): `owner: w399-0428-289-providers` — no "(lane X)" suffix, canonical identity = full owner value `w399-0428-289-providers` (exact session name per mission).
- git user.name = w399-0428-289-providers · git user.email = w399-0428-289-providers@baseharbor.local
- Literal invocation for EVERY commit: git -c user.name=w399-0428-289-providers -c user.email=w399-0428-289-providers@baseharbor.local commit ...
- Pre-push gate line: git show -s --format=%an HEAD -> must print exactly w399-0428-289-providers; on mismatch STOP + report. Witness for this round: `4e499b3cf6 an=w399-0428-289-providers cn=w399-0428-289-providers` + GATE_OK printed before the push.

## Base attestation (fix round)

- develop (ls-remote 2026-11-27): 6944e8761af6f07b801f55e39bb9a5409226c10b — ancestor of the PR #1884 head chain (cut point of round 1; witnessed in the round-1 akte).
- Branch chain after this round: git log --oneline origin/develop..HEAD = 4e499b3cf6 (this fix) + e6425f9bf7 (round 2) + 734707abf4 (round 1), all authored w399-0428-289-providers; git diff origin/develop...HEAD --name-only lists exactly the card write-set (cmd/baha apply/consent/remote files + scripts/pr-gate-coverage.json).
- Delivery witness: ls-remote refs/heads/lane-0428-292-consent-ux = refs/pull/1884/head = 4e499b3cf67ad86cb022640589dba05bfa26922d after the single normal push e6425f9bf7..4e499b3cf6 (lane-origin resolved to https://github.com/mcpdev80/baseharbor.git).
- The parked uncommitted refactor in /tmp/opencode/w399-0428-292-wt (stash w399-292-uncommitted-refactor-not-pushed-park-2026-11-27) stayed untouched; this round implemented the verdict findings fresh on the exact head.

## Korrektur block — finding: datei:zeile

- Finding 1 (app_candidate_consent.go:240-258, interactive bind decision on the wrong value):
  - cmd/baha/app_candidate_consent.go — interactiveCandidatePromptAllowed now decides ON THE CONSUMED READER: an *os.File equal to os.Stdin uses the production-pinned terminal seam (test switch); a threaded *os.File/terminalStdinReader not equal to os.Stdin must itself be a terminal; every other stream (pipe, bytes.Buffer seam, bare bufio.Reader) is refused and keeps the --confirm-candidate contract. A real operator's interactive y therefore carries consent straight into the same invocation's write (card bug fixed); a queued y on a non-terminal reader can never bind.
  - cmd/baha/app_candidate_consent.go — promptConfirmCandidateSubmission split: context-aware entry (default os.Stdin) + promptConfirmCandidateSubmissionInput leaf that threads the lifecycle reader; the answer is read from that same reader only.
  - cmd/baha/core_installation.go — withApplicationInput keeps the terminal file identity explicit in the typed terminalStdinReader wrapper (reused as-is, never re-wrapped behind a second bufio.Reader); foreign non-*os.File streams never enter the context.
- Finding 2 (app_remote_lifecycle.go:160-167 comment claims display-only while the code binds consent):
  - cmd/baha/app_remote_lifecycle.go — the remote route intentionally ACCEPTS inline operator consent (one-shot, identity-keyed, re-verified with constant-time digest equality at recordDeploymentBeforeMutation; explicit --confirm-candidate always wins). The false display-only claim is replaced by the accurate contract; NO consent check weakened (direction: behavior stays at the card goal, comment fixed to reality).
- Regressions (cmd/baha/app_candidate_consent_test.go, package-discovered; executed by the cli shard / native gates):
  - TestQueuedNonTerminalReaderNeverGrantsBindConsent (NEW negative): TTY-seam stdin + a different buffered reader containing a queued y as the threaded input -> no bind, write fails closed, --confirm-candidate contract printed. (Exactly the verdict's requested case.)
  - TestWithApplicationInputPreservesTerminalIdentity (NEW): typed wrapper threaded as-is and passes sameTerminalStream; bare os.Stdin passes; non-*os.File streams never become the application input.
  - TestRemoteApplyRouteInlineBindContractIsTruthful (NEW, finding 2 route): remote-shaped invocation, non-terminal -> question never asked, nothing binds, write refuses.
  - Existing TestInteractiveCandidateConsentCarriesToWriteWithoutSecondFlag / RefusalKeepsFailClosed / NonInteractiveKeepsFlagContract rewired to the production reader shapes (terminalStdinReader over the pinned stdin file) and still green.
  - CI route: no .github/** change; the same package shard/native gates that ran the round-1 tests run these (scripts/pr-gate-coverage.json rows already on the branch from e6425f9bf7).

## Hosted CI STATE (fix round)

- Exact-head pair (two distinct pull_request run IDs on 4e499b3cf6): run 46046111688 (trigger: the push) and run 46046309439 (trigger: close+reopen, PR comment 'second exact-head hosted run trigger (coordinator-authorized)'). No rerun, no workflow_dispatch.
- Job outcomes (identical on both runs): Workflow policy SUCCESS; PR · Source format SUCCESS (gofmt delta + readability: consent files checked pre-commit, the #1881 lesson applied); PR · Native gate plan SUCCESS; PR · Trusted Plan FAILURE = known class-A blocker ('invalid trusted PR gate coverage catalog: uncataloged source change' — the trusted planner reads scripts/pr-gate-coverage.json from the BASE/controller checkout, 85965486154284d4 controller; the branch already carries the three new-path rows since e6425f9bf7, but base rows require the owner freeze-lift: #136 + fan-in #1861-#1863).
- PR Selected Checks failure = downstream of the Trusted Plan abort (UNIT_SCOPE empty / UNIT_RESULT skipped because the plan step died before shard selection; REJECT: Go test selection missing or invalid). Mission line 6 read literally, that aggregate is not green on this class-A head; the test-execution route itself is the cli package shard / native gates which are green-eligible once the base rows land. Documented here as STATE, no rerun, no workflow change.

## Known blocker (cited per mission line 6)

Trusted Plan stays RED until the owner lift (same class-A mechanism as #1881; see evidence/2026-11-27/0428-codex-staticreview-pr1881-1882.md 'Trusted-Plan lift mechanism'). After the lift, one fresh exact-head pull_request pair qualifies.

## repo-rule compliance

- Write-set: cmd/baha/app_apply.go, app_candidate_consent.go, app_candidate_consent_test.go, app_remote_lifecycle.go, core_installation.go. Disjoint from #1881/#1882 files (mission line 4). No .github/**, no ci.yml touch. Consent gates intact (digest equality constant-time, one-shot binding, state-root checks).
- One fix commit; canonical lane identity per -c invocation + %an gate; EIN normaler push; delivery via ls-remote (above).
- Local test runs were NON-QUALIFYING pre-checks (named-form go test with the RunsRealLifecycle-class skip list on the coordinator host per the test-runner rule); Hosted CI qualifies.

## cleanliness

- No container/compose started on this host: docker ps -a ID count 0 before and after this round, pid witness 3428508. No VM/SSH use.
- Scratch files (/tmp/opencode/w399-1884-akte staging dirs, probe scripts) removed; only the worktree /tmp/opencode/w399-0428-292-wt remains (branch pushed, clean).

## END

END_DONE w399-0428-289-providers: 1884 head 4e499b3cf6 + runs 46046111688/46046309439 + format-gate green; Trusted Plan red = known class-A base-catalog freeze blocker (cited).
