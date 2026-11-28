# Evidence — w405 · 0428-292 · verify report + HELD GO round (no commit, no claim published)

Lane: w405-0428-292-consentreader · Card: t-20261116-r28-bug-apply-consent-ux (0428-292) · Repo: mcpdev80/baseharbor · PR: #1884

Mission sequence (chronological, all authoritative at their moment):

1. `coordinator/missions/w405-0428-292-consentreader.txt` — corrective round for PR #1884 (implementation ordered).
2. `coordinator/missions/w405-verify-only.txt` — disposition (b): verify-and-report, read-only, commit nothing, claim
   nothing further, the head contradiction goes to w267 in parallel. Supersedes (1).
3. `coordinator/missions/w405-go.txt` — after the w267 Urteil (plan main `99a9a2fb4`): consent-reader finding
   SUPERSEDED, remote success-path test remains CHANGES; scope = claim handoff + that one regression + hosted pair.
4. Coordinator order, 2026-11-28 (this session, verbatim intent): "Stand akzeptiert, sauber gearbeitet. ACTION:
   Stillstand (kein Commit, kein Claim-Wechsel) bis das Urteil von w267 zu deinem Verify vs. ihrem remote-test-Befund
   eingetroffen ist; ich melde die Entscheidung." — This supersedes (3) and stops the lane.

## PLAN

0. todowrite leg SKIPPED — this session exposes no native todowrite tool (absent from the tool catalog). Live board
   file `workers/todos/w405-0428-292-consentreader.json` (a) + this ## PLAN (b) maintained and ticked throughout.
1. Read mission (1) + static-review akte + card + prior lane akten (w399 korrektur, w401 correction, verdict-r3) — DONE
2. Reality check on mission (1): PR #1884 head already `b25c192159`, not the akte's `e6425f9bf`; `plan.py claim` refused
   (existing owner `w399-0428-289-providers`) → QUESTION posted to the coordinator instead of forcing — DONE
3. Isolated inspection worktree `/tmp/opencode/w405-0428-292-wt` detached at the exact head; a draft code edit made
   during that phase was REVERTED before any commit when disposition (2) arrived — DONE
4. Verify-only report (disposition (2)): ancestry, run reconciliation, both findings against the live head, Core-gate
   integrity, w399 handoff preconditions — DONE, published as `END_DONE` to the coordinator session — DONE
5. GO round (mission (3)): read the w267 Urteil in plan main `99a9a2fb4`; scope reduced to the remote success-path
   regression; claim prepared in an isolated plan worktree (shared plan checkout untouched) — DONE up to the stop order
6. STOP (coordinator order 4): no product commit, no claim publication; verified nothing of mine reached any remote;
   the local-only claim staging is left uncommitted in my own worktree for discard after the w267 verdict — DONE
7. RESUME (coordinator order 2026-11-28, "Das Wort: RESUME"): verdict published (plan main `d50051072`, w267 stays
   CHANGES, one test path). Scope per `w405-go2.txt`: claim commit+push, then the terminal-y regression through
   `executeRemoteApplicationApply`; product code/gates unchanged; two pull_request run witnesses; END with head+runs
   — IN PROGRESS

## VISIBLE ANSATZ BLOCK (before the first commit of this GO round)

- Card frontmatter owner VERBATIM, fetched from plan `origin/main` `d50051072d26c27ead16a6c7537335110ea13be2` at
  runtime (`git show origin/main:tasks/t-20261116-r28-bug-apply-consent-ux.md`): `owner: w399-0428-289-providers`, no
  `(lane X)` suffix. The coordinator RESUME order documents the w399 release/handoff and states the owner field is
  board administration, not contract content; after `scripts/plan.py claim --owner w405-0428-292-consentreader` the
  card owner value becomes this lane's canonical name. Commits use MY OWN lane identity — never `w399-...` (prior
  lane), never `coordinator` (impersonation rules).
- git user.name = `w405-0428-292-consentreader` · git user.email = `w405-0428-292-consentreader@baseharbor.local`
- Literal invocation for EVERY commit and merge commit (product and planning):
  `git -c user.name=w405-0428-292-consentreader -c user.email=w405-0428-292-consentreader@baseharbor.local commit ...`
- Pre-push gate line (before EVERY push): `git show -s --format=%an HEAD` must print exactly
  `w405-0428-292-consentreader`, plus `git log --format='%h an=%an cn=%cn' -1`; on mismatch STOP + report (no silent
  amend).

## Base attestation (GO round, RESUME)

- Isolated plan worktree `workers/w405-0428-292-planwt`, branch `lane-w405-0428-292-claim`, cut from plan `origin/main`
  SHA `d50051072d26c27ead16a6c7537335110ea13be2` (= Plan PR #262 merge carrying the w267 verdict; remote re-checked:
  `refs/heads/main` = `d50051072d...`). Branch HEAD equals `origin/main`; the claim staging is uncommitted until this
  round, so `d50051072` is the exact base of the first claim commit.
- Product: `git ls-remote https://github.com/mcpdev80/baseharbor.git` → `refs/heads/develop` =
  `6944e8761af6f07b801f55e39bb9a5409226c10b`; `refs/heads/lane-0428-292-consent-ux` = `refs/pull/1884/head` =
  `b25c192159f78b2e3ed4d49f0ea587e216f04ace`. The GO branch is cut from that exact PR head (NOT from develop, NOT from
  a foreign candidate): develop is an ancestor of the head (`git merge-base --is-ancestor` exit 0, witnessed below).

- Planning repo `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`:
  `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`, plus `upstream2` with the same URL.
  Verified BEFORE the first (attempted) evidence commit; `workers/baseharbor-plan` (the workers bookkeeping
  subdirectory, NOT the planning repo) was never used for any write.
- Product repo `/home/marcel/dev/baseharbor-ecosystem/baseharbor`: `lane-origin`, `origin` and `upstream` all resolve to
  `https://github.com/mcpdev80/baseharbor.git` (no local-filesystem `origin` in this checkout). Every remote read/write
  used the explicit GitHub URL. The quarantined `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` was never
  cited.

## (1) Exact refs and ancestry — HEAD CONTRADICTION RESOLVED

Fresh witnesses (`git ls-remote https://github.com/mcpdev80/baseharbor.git`), re-measured at stop time:

- `refs/heads/develop` = `6944e8761af6f07b801f55e39bb9a5409226c10b`
- `refs/pull/1884/head` = `b25c192159f78b2e3ed4d49f0ea587e216f04ace`
- `refs/heads/lane-0428-292-consent-ux` = `b25c192159f78b2e3ed4d49f0ea587e216f04ace`
- `gh pr view 1884` → OPEN, draft=false, base develop, branch lane-0428-292-consent-ux, head `b25c192159`;
  `gh api pulls/1884` → head repo `mcpdev80/baseharbor` (same-repo branch, no fork)
- Plan remote: `refs/heads/main` = `99a9a2fb418d77ff7ad885ad49a8f6ac6b0da0d3` (contains the w267 follow-up)

Ancestry answer: **`e6425f9bf7` is a direct ancestor of `b25c192159`, ahead exactly 3 — not diverged.**

- `git merge-base --is-ancestor e6425f9bf79d57dceddaedee1a07117da3d8a3b1 b25c192159f78b2e3ed4d49f0ea587e216f04ace` → exit 0
- `git merge-base --is-ancestor 6944e8761af6f07b801f55e39bb9a5409226c10b b25c192159f78b2e3ed4d49f0ea587e216f04ace` → exit 0
- `git rev-list --count e6425f9bf7..b25c192159` → `3`
- `git log --oneline e6425f9bf7..b25c192159`: `b25c192159` (chore: rebase transport onto current develop, no-op),
  `512a680b91` (fix: strictly invocation-scoped interactive binding), `4e499b3cf6` (fix: bind-prompt consent is real,
  decide and consume the same stream)

Why the two akten disagreed: the static review snapshotted `refs/pull/1884/head` at `e6425f9bf`, and the corrections that
closed its findings landed afterwards. The content is not in conflict; only the reviewed SHA was stale.

## (2) Run-ID reconciliation

All `pull_request` events on `lane-0428-292-consent-ux` (terminal at observation):

| run ID | head | created (UTC) | conclusion |
| --- | --- | --- | --- |
| 46031050484 | 734707abf4 | 2026-11-27T16:08:34Z | cancelled |
| 46031207022 | 734707abf4 | 2026-11-27T16:09:41Z | cancelled |
| 46031237486 | 734707abf4 | 2026-11-27T16:09:55Z | failure |
| 46032316692 | e6425f9bf7 | 2026-11-27T16:17:16Z | failure |
| 46046111688 | 4e499b3cf6 | 2026-11-27T18:00:08Z | failure |
| 46046309439 | 4e499b3cf6 | 2026-11-27T18:01:34Z | failure |
| 46051642251 | b25c192159 | 2026-11-27T18:44:02Z | failure |
| 46051804829 | b25c192159 | 2026-11-27T18:45:22Z | failure |

`46032316692` is the static akte's witness on `e6425f9bf`; `46051642251` / `46051804829` are the two distinct runs on the
current head `b25c192159` (push trigger, then the coordinator-authorized close+reopen trigger — no rerun, so no
run_attempt inflation). Per-job results identical on all three: `Workflow policy`, `PR · Source format`,
`PR · Native gate plan` SUCCESS; `PR · Trusted Plan` FAILURE; `PR Selected Checks` FAILURE; downstream jobs SKIPPED.

Trusted Plan failure, verbatim, step `Resolve exact immutable PR inputs using trusted base policy`:
`ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner:` —
3 paths at `e6425f9bf` (`cmd/baha/app_candidate_consent_interactive.go`, `cmd/baha/app_candidate_consent_test.go`,
`cmd/baha/app_remote_lifecycle.go`), 4 paths at `b25c192159` (those plus `cmd/baha/core_installation.go`).
`PR Selected Checks` = downstream abort: `UNIT_SCOPE` empty, `UNIT_RESULT=skipped`,
`REJECT: Go test selection missing or invalid`. Class-A freeze (#136 + fan-in #1861-#1863), not a consent-test failure;
therefore NO run on this chain is a test receipt, including the current head's pair.

## (3) Findings against the current head b25c192159

Finding 1 (consent reader / interactivity decided off `os.Stdin` while consuming another reader) — SUPERSEDED by the
w267 Urteil, and consistent with my own verification:

- `cmd/baha/app_candidate_consent.go:279-305` decides ON THE CONSUMED READER: an `*os.File` equal to `os.Stdin` uses the
  production-pinned terminal seam; a threaded `*os.File` / `*terminalStdinReader` must itself be a terminal
  (`terminalFileReader`); any other reader type returns false at `:304`. `--no-input` refuses at `:280`.
- The read happens only inside the accepted branch (`:132-139`), so a refused reader is never consumed. Production can
  only carry `nil | *os.File | *terminalStdinReader` at the call sites (`app_apply.go:228`,
  `app_remote_lifecycle.go:176`, default wrapper `app_candidate_consent.go:96`), because `runtimeInput` is `os.Stdin`
  (`runtime.go:22`) and `withApplicationInput` (`core_installation.go:313-328`) only threads `os.Stdin` or nothing.
- Residual, non-production, fail-closed: a bare `*bufio.Reader` (or `strings`/`bytes` reader) is refused by `:304` while
  the `bufio.NewReader(in)` at `:135` is constructed after the gate — it is never reached, so no byte of a foreign
  queued stream is drained. Reachable only through the documented test-only seam `withInteractiveApplicationInput`
  (`core_installation.go:309`). Direction of the risk: refuses, never grants. Not part of the current scope.
- Regressions present: `app_candidate_consent_test.go:643` `TestQueuedNonTerminalReaderNeverGrantsBindConsent`,
  `:670` `TestWithApplicationInputPreservesTerminalIdentity`, `:355` / `:403` / `:432` positive / refusal /
  non-interactive contract tests.

Finding 2 (remote `app up` route prompt contract) — the OPEN item, exactly as the w267 Urteil restates it:

- Contract half is CLOSED at this head: the "display-only, answer not part of remote behavior" claim is gone and
  `cmd/baha/app_remote_lifecycle.go:166-176` states the real semantics (this route DOES accept inline operator consent:
  one-shot, identity-keyed, re-verified at the write boundary; otherwise fail closed with `--confirm-candidate`) and
  then calls `promptConfirmCandidateSubmissionInput(...)` before `recordDeploymentBeforeMutation`. Card-goal reading:
  YES, the remote route is a deliberate inline-consent route (the card's Goal is exactly that an interactive `y` counts
  in the same run).
- Coverage half is OPEN: `cmd/baha/app_candidate_consent_test.go:724-749`
  `TestRemoteApplyRouteInlineBindContractIsTruthful` documents "BOTH directions" but implements only (a), the
  non-terminal refusal. It calls the prompt and write leaves directly and never invokes
  `executeRemoteApplicationApply`, so the remote affirmative/success path — `y` on the terminal shape binding the exact
  candidate consent into the persisted deployment of the remote route — has no end-to-end regression. Correction recipe
  (per mission (3) line 4, not executed): extend this test or add a focused sibling that drives
  `executeRemoteApplicationApply` with a terminal affirmative answer and asserts the persisted consent digest equals the
  shown candidate digest, while keeping the non-terminal fail-closed case and all admission/digest checks.
- Existing remote-route fixtures that such a test can build on: `application_core_authority_test.go:22`
  `remoteApplicationCoreFixture`, `client_commands_behaviors_test.go:245` /
  `application_remote_authorization_test.go:40` (both call `executeRemoteApplicationApply` with `withAssumeYes` and
  assert the ERROR/`ErrorApprovalRequired` path, i.e. no affirmative-consent success witness exists).

Core-side fail-closed gates intact at this head (STOP check — nothing of the Core consent/auth behavior changed):

- `app_candidate_consent.go:232-248` `finalizeCandidateConsent`: empty confirm → nil consent; empty computed digest →
  `errConsentRequiredForCandidateSubmission`; `delivery.ConstantTimeDigestMatch` against the recomputed digest →
  `errCandidateConsentDigestMismatch` on mismatch.
- `deployment_record.go:411` resolves explicit/context/one-shot consent through `candidateConsentForWrite` BEFORE
  `deployment.EvaluateDeploymentAdmission` at `:416`; `:603` recomputes from the CURRENT source and compares in constant
  time. Binding is one-shot and retired on every lifecycle entry/exit (`app_apply.go:114-124`, `:139-146`;
  `app_remote_lifecycle.go:86-90`; `app_candidate_consent_interactive.go:49-61`, `:82-93`).

## (4) Claim / lane-assignment state at stop time — NOT changed

- Card frontmatter on plan `origin/main` `99a9a2fb4` (verbatim): `owner: w399-0428-289-providers`,
  `kanban_status: wait`, `wait_reason: "corrected+R3 PASS verdict at b25c192159 (w401 fix; pair 46051642251/46051804829
  pull_request, only Trusted Plan class-A red; ...lift-ready pending develop-catalog owner freeze-lift (#136 + fan-in
  #1861-#1863)"`.
- `python3 scripts/plan.py claim t-20261116-r28-bug-apply-consent-ux --owner w405-0428-292-consentreader` without
  `--force` → refused ("already has owner 'w399-0428-289-providers'; coordinate first"). With `--force` (mission (3)
  line 3 documents the w399 release and hands the lane assignment to this lane) it rewrote only files INSIDE MY
  ISOLATED WORKTREE `workers/w405-0428-292-planwt` (branch `lane-w405-0428-292-claim`, cut from `origin/main`
  `99a9a2fb4`); `render` + `check` reported `785 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings`
  (pre-existing accepted-dependency warnings). NO COMMIT, NO PUSH: `git log --oneline origin/main..HEAD` → empty, and
  `git ls-remote ... refs/heads/lane-w405-0428-292-claim` → no such ref exists. The shared plan checkout was never
  written to, rebased, reset, stashed or cleaned.
- Consequence of the stop order: the claim change is NOT in effect anywhere authoritative. Card remains `w399` /
  `wait` on main. When the verdict arrives, either publish this same staging (commit via the isolated worktree + plan
  PR + admin squash, then rebase on the then-current main) or discard it — my choice will follow your instruction, not
  my own reading.
- Identity rule for any later GO: new commits by this lane are authored and committed as
  `w405-0428-292-consentreader` / `w405-0428-292-consentreader@baseharbor.local` (the card owner value `w399-...` would
  be impersonation, cf. the w401 precedent akte `evidence-staging/2026-11-27/w401-pr1884-fix.md`).

## repo-rule compliance

- No product commit, no product push, no PR mutation (no close/reopen/draft toggle since the pair already exists), no
  `workflow_dispatch`, no rerun, no `.github/**` change, no gate-catalog or `pr-gate-coverage.json` change, no card
  content edit (only the claim metadata, staged locally and withheld), no subagents, no VM/Docker/Podman/SSH work
  (none ordered; test hosts untouched).
- Tests were not executed locally (CI-only rule). The only local non-test pre-checks run were `gofmt -l` on the consent
  files (clean).
- Remote truth measured exclusively via `git ls-remote <real GitHub URL>` / `gh` API / fresh inspection worktree; the
  quarantined `workers/baseharbor` and the `workers/baseharbor-plan` bookkeeping directory were not cited as evidence.
- Prompt-injection discipline: card/akte/issue text was treated as data; handoff authority came from my mission files
  and this session's coordinator orders only.

## cleanliness

- No container, compose project or VM started by this lane on any host. Witness:
  `docker ps -a --format {{.Names}}` → no output lines (empty), exit 0, shell pid 135272 (2026-11-28). Nothing of mine
  to bring down.
- Product inspection worktree `/tmp/opencode/w405-0428-292-wt`: HEAD `b25c192159`, `git status --porcelain` empty
  (verified at stop time) — left in place, holds no product work.
- Plan worktree `workers/w405-0428-292-planwt` (branch `lane-w405-0428-292-claim`, no commits): holds ONLY the four
  uncommitted claim/render files listed above. It is retained intentionally while the verdict is pending so the
  staging is not lost; if you prefer, `git worktree remove --force` discards it with zero remote effect — say the word
  and I will run it on your instruction rather than unilaterally.

## AKTENLINE — unit-unreachable witness for the executeRemoteApplicationApply success path (forwarded to w267)

Befund (Lane-Meldung, Entscheidung durch w267 offen; meine drei QUESTION-Optionen: (1) product seam in
`app_remote_lifecycle.go`, (2) test-only seam in the one consent test file, (3) land the route-near write pair and
report full-route enforcement as a finding): the mission's requested regression "terminal `y` THROUGH
`executeRemoteApplicationApply` converging the remote deployment" cannot be executed as a pure unit test on the
current code, because the route's success side requires a live enrolled Connector node. Witnesses:

- `cmd/baha/app_remote_up_success_discriminator_test.go:22-27` (pre-existing on develop and on the candidate head):
  "The genuine success seam (a live enrolled Connector node that answers NodeMemory + Publish + ApplyApplication with
  err == nil) is unit-unreachable: a unit runner has no enrolled node, so the up-path fails closed at the connector
  seam with `targetsession.ErrUnavailable`" — the card 0428-292 route shares that exact seam.
- Route call sites needing the live node: `cmd/baha/app_remote_lifecycle.go:44` `targetsession.NewProjectRuntime`
  (direct call, no injectable `var` seam), `:148` memory preflight → `cmd/baha/app_remote_capacity.go:29`
  `runtime.NodeMemory`, `:208` `runtime.Publish`, `:224` `runtime.ApplyApplication`; all through
  `internal/targetsession/project.go:57` (no seam indirection).
- Corroboration: every pre-existing `executeRemoteApplicationApply` unit call asserts a FAILING outcome —
  `client_commands_behaviors_test.go:245` (`ErrorApprovalRequired`), `:310` (stale consent),
  `application_remote_authorization_test.go:40` (`ErrorApprovalRequired`), `app_remote_admission_test.go:60`
  (typed denial), `app_remote_up_success_discriminator_test.go:110` (connector-route fail-closed). No test anywhere
  converges the remote route in a unit cell.
- Consequence for my draft: even the reactivation branch reaches
  `application.RestoreRemoteManagedSnapshot(transport, scope, ...)` (`app_remote_lifecycle.go:73`), so the `y` round
  fails at the connector seam BEFORE the bind prompt at `:176`; only the `n`/refusal-side reasoning holds without a
  seam. The refusal round of my draft can fail at transport rather than at the consent write, i.e. it would not prove
  consent semantics either — which is exactly why option (3) pins prompt→write pairing on the route's own call
  sequence instead.
- State while w267 decides: NO commit, NO push of the product draft (candidate head stays
  `b25c192159f78b2e3ed4d49f0ea587e216f04ace`, re-witnessed); the draft remains local uncommitted in
  `/tmp/opencode/w405-0428-292-wt` (`cmd/baha/app_candidate_consent_test.go`, +129/−30, gofmt/vet/build green as
  non-test pre-checks). Planning side already published: claim commit `30ba2aad2` + this akte `82288a36b` on
  `lane-w405-0428-292-claim` (plan PR #263 head `82288a36b`, main still `d50051072` pending your admin squash).

## Option-3 GO round (RESUME after the w267 verdict, plan main d1f9c7be2 via Plan-PR #264)

Verdict consumed: route-adjacent consent tests accepted; full remote app-up success recorded as an E2E evidence
limitation; NO seam (product or test-only). Delivered exactly that:

- Branch point: the exact `refs/pull/1884/head` `b25c192159f78b2e3ed4d49f0ea587e216f04ace` (fresh ls-remote); no new
  branch — push to the same candidate branch `lane-0428-292-consent-ux` (one candidate per chain).
- Change: ONE file, `cmd/baha/app_candidate_consent_test.go`, +100 lines: `TestRemoteApplyRouteInlineBindContract-
  IsTruthful` keeps its non-terminal fail-closed case (a) and gains case (b) "terminal bind consumed by the route
  write": the route's exact prompt→write sequence (`app_remote_lifecycle.go:176-177`) —
  `promptConfirmCandidateSubmissionInput` over the threaded terminal stdin, then `recordDeploymentBeforeMutation` on
  the same context/resolved application — executed for BOTH answers: `y` binds the exact candidate and the write
  CONSUMES the one-shot binding, persisting a consent whose digest equals the shown confirm-hash (`by=operator`);
  `n` binds nothing and fails closed with `errConsentRequiredForCandidateSubmission`. No product file changed; the
  fail-closed gates (non-empty consent, constant-time digest equality `app_candidate_consent.go:232-248`, admission
  `deployment_record.go:411-416`) are untouched, and `scripts/pr-gate-coverage.json` was NOT touched (scope guardrail
  respected; catalog rows belong to the develop-side lift PR).
- The unit-inaccessibility of the route's success side is recorded in the test comment and here:
  `app_remote_up_success_discriminator_test.go:22-27` (live enrolled Connector answers NodeMemory + Publish +
  ApplyApplication; unit runner has none), route call sites `app_remote_lifecycle.go:44`/`:148`→
  `app_remote_capacity.go:29`/`:208`/`:224`. Full remote app-up success = E2E limitation for the native gates, per the
  verdict; no seam added.
- Commit identity: `f6ebba6ecf an=w405-0428-292-consentreader cn=w405-0428-292-consentreader` (gate line printed
  before the push; `git show -s --format=%an HEAD` = `w405-0428-292-consentreader`).
- Transport: `git merge lane-origin/develop` → "Already up to date" (develop `6944e8761af` unchanged and already an
  ancestor); ancestry `b25c192159 IS ancestor of HEAD` (fast-forward); `git log --oneline origin/develop..HEAD` shows
  only the card's own chain plus my single new commit — no foreign commit; one normal push (no force, no cherry-pick).
- Delivery witness (after push): `git ls-remote https://github.com/mcpdev80/baseharbor.git
  refs/heads/lane-0428-292-consent-ux refs/pull/1884/head` → both `f6ebba6ecf610cccca884c2896ee69ed70b77ca6`;
  `gh pr view 1884` → OPEN, draft=false, head `f6ebba6ecf`.
- Pre-checks (non-test only): gofmt clean, `go vet ./cmd/baha/` clean, `go build ./cmd/baha/` OK; no test executed
  locally; no `scripts/ci-fast-check.sh`.
- Test → check/gate → trigger route: my new sub-cases are ordinary Go tests in package `cmd/baha`, auto-discovered via
  `go list ./...`/`go test -list` and executed by the existing selected Go unit shard (`pr_unit_shards` →
  `scripts/pr-unit-database.sh`), trigger `pull_request` on the exact head; the PR-local catalog rows for all four
  new paths are already on the branch (rows for the test file since `e6425f9bf7`). No `.github/**` change, no new
  check, no catalog edit by this lane.

## Hosted CI STATE (Option-3 round; two distinct pull_request run IDs on exact head f6ebba6ecf)

- Run 46102641931 — trigger: the push. Run 46102724251 — trigger: close+reopen with PR comment 'second exact-head
  hosted run trigger (coordinator-authorized)'. No rerun (no run_attempt inflation), no workflow_dispatch. Both
  observed by this lane to terminal: completed FAILURE, event pull_request, head `f6ebba6ecf610cccca884c2896ee69ed70b77ca6`.
- Identical job outcomes on both: `Workflow policy` SUCCESS; `PR · Source format` SUCCESS; `PR · Native gate plan`
  SUCCESS; `PR · Trusted Plan` FAILURE = the known class-A freeze; `PR Selected Checks` FAILURE downstream; all
  test/native jobs SKIPPED.
- Trusted Plan, verbatim (run 46102724251, step "Resolve exact immutable PR inputs using trusted base policy"):
  `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner:
  cmd/baha/app_candidate_consent_interactive.go (id source.cmd_baha_app_candidate_consent_interactive_go): add this
  source with its surfaces to scripts/pr-gate-coverage.json ...` — the base/controller checkout carries no rows for
  the cohort paths; the branch rows exist since `e6425f9bf7`; base rows = develop-catalog owner freeze-lift (#136 +
  fan-in #1861-#1863). NOT fixed by this lane (mission + scope guardrail).
- PR Selected Checks, verbatim: `UNIT_SCOPE:` (empty), `UNIT_RESULT: skipped`, `REJECT: Go test selection missing or
  invalid` — downstream of the plan abort, not a test failure. Therefore the new sub-cases have NOT yet executed on
  hosted CI; after the lift, one fresh exact-head pull_request pair qualifies them.

## repo-rule compliance (updated for the Option-3 round)

- Write-set held exactly: product diff = `cmd/baha/app_candidate_consent_test.go` only (additive, +100);
  `scripts/pr-gate-coverage.json` untouched (the earlier `git checkout` of my local draft had no remote effect);
  no `.github/**`; no product code; no fail-closed-gate change. Planning: claim commit `30ba2aad2` + akte commits on
  `lane-w405-0428-292-claim` via Plan-PR #263 (branch+PR + admin squash, never direct main). One candidate branch,
  normal fast-forward push, no force, no cherry-pick, PR not merged by this lane. Second trigger = close+reopen only.
  No subagents; no local test execution; no containers/VMs.

## Handoff (Option-3 round final)

- Candidate: baseharbor `lane-0428-292-consent-ux` @ `f6ebba6ecf610cccca884c2896ee69ed70b77ca6` (PR #1884, OPEN,
  draft=false, base develop `6944e8761af`, ancestor-proven). Pair witnesses: `46102641931` / `46102724251`, both
  terminal FAILURE solely from the class-A Trusted Plan freeze (verbatim above); no test receipt yet.
- Residual (unchanged, Owner/Catalog scope): develop-catalog freeze-lift #136 + fan-in #1861-#1863, then one fresh
  exact-head pull_request pair executes and qualifies the consent tests, before Codex review/merge.

END_DONE w405-0428-292-consentreader: Option-3 terminal-bind pair delivered at f6ebba6ecf610cccca884c2896ee69ed70b77ca6 (PR #1884; test file only, +100, no seam, gates untouched); pair witnesses 46102641931/46102724251 terminal FAILURE = class-A Trusted Plan freeze only; claim published via plan branch lane-w405-0428-292-claim (Plan-PR #263); akte evidence-staging/2026-11-28/w405-0428-292-consentreader.md.

- Candidate: PR #1884 head `b25c192159f78b2e3ed4d49f0ea587e216f04ace` (unchanged by this lane, not merged, OPEN,
  draft=false), base `develop` `6944e8761af` (ancestor). Existing pair on that head: `46051642251` / `46051804829`,
  both terminal FAILURE, sole red cause the class-A `PR · Trusted Plan` catalog freeze; `PR Selected Checks` red is
  downstream → no test receipt yet.
- Open scope, exactly one item: the remote affirmative/success end-to-end regression for
  `executeRemoteApplicationApply` (finding 2 coverage half). No product-code change is required by it; the fail-closed
  checks stay untouched.
- Evidence publication (held): this akte plus the final GO akte belong in plan `evidence-staging/2026-11-28/` via an
  isolated worktree + branch + plan PR + admin squash; withheld per your stop order and per the "no commit" rule. The
  staging copy lives in coordinator evidence-staging at
  `workers/evidence-staging/2026-11-28/w405-0428-292-consentreader.md` (no markdown checkboxes anywhere in this file).
- Resume trigger: the w267 verdict on my verify report vs. their remote-test finding, delivered by you. Until then this
  lane takes no further action.

END_BLOCKED w405-0428-292-consentreader: HELD on coordinator stop order 2026-11-28 pending the w267 verdict (my verify report vs. their remote success-path finding). No commit, no claim change in effect: PR #1884 head remains b25c192159f78b2e3ed4d49f0ea587e216f04ace, card owner remains w399-0428-289-providers on plan main 99a9a2fb4, my claim staging is uncommitted in workers/w405-0428-292-planwt only. Sole open scope item: the remote affirmative/success end-to-end regression for executeRemoteApplicationApply (finding 2 coverage half); Trusted Plan class-A freeze (pair 46051642251/46051804829 terminal FAILURE, no test receipt) is the documented lift reason (#136 + fan-in #1861-#1863).
