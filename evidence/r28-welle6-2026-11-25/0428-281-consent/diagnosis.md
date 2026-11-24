# w85 / card 0428-281 — root `up` must propagate `--confirm-candidate` into its internal repository apply

Lane: w85-0428-281-consent
Repo: mcpdev80/baseharbor
Mission: /home/marcel/dev/baseharbor-ecosystem/coordinator/missions/w85-0428-281-consent.txt
Card: t-20261125-0428-281-baha-up-candidate-consent-lost (0428-281, bug)
Status: STOPPED — OWNER HOLD (owner directive mid-turn, 2026-11-24), then RESUMED as READ-ONLY
DIAGNOSIS (owner directive 2026-11-24, second message). No product edits, no product branch, no PR.
Deliverable: ## diagnosis plus the findings below.

## Candidate

None. No product commit was ever created, so there is no candidate SHA and no exact-head CI run to
report. The hold instruction supersedes mission step 3.

## PLAN

1. DONE. Create the numbered work plan in all three places.
   - Native `todowrite`: NOT EXPOSED in this session, so leg (0) skipped per the dispatch wording
     ("if unsure, skip leg (0) entirely"). Board file (a) and this list (b) written.
   - Board file: /home/marcel/dev/baseharbor-ecosystem/workers/todos/w85-0428-281-consent.json
2. DONE. `git remote -v` as first git action; only URLs containing github.com/mcpdev80 used. Witnesses below.
3. DONE. `git ls-remote` real URL: develop = `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2`.
4. DONE. Card note existed only untracked locally; claimed and published BEFORE any edit —
   commit `a3d982bf0` on origin/main, owner `w85-0428-281-consent (session w85)`,
   kanban_status/lane `active`. See ## findings item 1 (claim now needs owner action).
5. DONE then REVERTED. Worktree `/home/marcel/dev/baseharbor-ecosystem/workers/0428-281-consent-wt`
   and branch `lane-0428-281-consent` were cut from exactly `46d3dccc1`, then both deleted on the hold
   (witnesses in ## cleanliness). Base attestation: branch was created by
   `git worktree add -b lane-0428-281-consent <wt> 46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2`, so HEAD of the
   first commit would have been a direct descendant of that attested SHA. No commit was ever made, therefore
   `git log --oneline origin/develop..HEAD` was empty and `git diff origin/develop...HEAD --name-only` was empty.
6. DONE. Reference `5f9c671` read via `git show` (shape only; never cherry-picked, its branches/PRs untouched).
   Read `cmd/baha/runtime.go`, `cmd/baha/app_input_resolver.go`, `cmd/baha/app_candidate_consent.go`,
   `cmd/baha/runtime_repository_up.go`, `cmd/baha/repository_up.go`, `cmd/baha/app_up_lifecycle.go` at 46d3dccc.
7. NOT DONE — blocked by owner hold. Also found already implemented (## findings item 2).
8. NOT DONE — blocked by owner hold. Only the missing regression test would have been new work.
9. DONE (trivially). Write-set was never touched: zero changed files.
10. NOT DONE — owner hold forbids branch push and PR. Confirmed none exists.
11. NOT DONE — no candidate, therefore no hosted run was triggered by this lane.
12. DONE. This evidence file, published to baseharbor-plan main.
13. DONE. END post, last action.

## environment witnesses

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` (planning-repo verification,
required before the first evidence commit — this IS the planning repo, not workers/baseharbor-plan):

    origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

`git remote -v` in the product checkout /home/marcel/dev/baseharbor-ecosystem/baseharbor (remote guard:
all three names resolve to github.com/mcpdev80, so no filesystem remote is in play):

    lane-origin     https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
    lane-origin     https://github.com/mcpdev80/baseharbor.git (push)
    origin  https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
    origin  https://github.com/mcpdev80/baseharbor.git (push)
    upstream        https://github.com/mcpdev80/baseharbor.git (fetch)
    upstream        https://github.com/mcpdev80/baseharbor.git (push)

`git remote -v` in /home/marcel/dev/baseharbor-ecosystem/workers (the session host's bookkeeping repo;
NOTE its remotes point at the baseharbor product URL, so it must never be pushed from):

    lane-origin     ssh://git@github.com/mcpdev80/baseharbor.git (fetch)
    lane-origin     ssh://git@github.com/mcpdev80/baseharbor.git (push)
    origin  ssh://git@github.com/mcpdev80/baseharbor.git (fetch)
    origin  ssh://git@github.com/mcpdev80/baseharbor.git (push)

Quarantined paths acknowledged and NOT cited as remote truth:
/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor and
/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan.

Remote truth for develop, measured with ls-remote:

    46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2        refs/heads/develop

## diagnosis (read-only trace, owner RESUME 2026-11-24)

Verdict: NO. There is no product-side gap of the kind the mission describes. The consent value is
already carried on every documented local `baha up` route at develop `46d3dccc1` AND on the tested
candidate `475902075`, so there is nothing left to "carry through the same path". The 4 Docker Light
failures have a different cause: the Demo acceptance harness in
`mcpdev80/baseharbor-demo:tests/fixture-consent.py` does not recognize the nested form of the
candidate refusal that `baha up` emits, so it never re-runs with the digest.

### A. #1807 did change the root-up path (mission item 1)

`git show 7b45db92 -- cmd/baha` is exactly 4 files, 18 insertions / 1 deletion:

    cmd/baha/app_candidate_consent.go |  4 ++++   new helper withRuntimeUpCandidateConsent(ctx, opts)
    cmd/baha/app_input_resolver.go    |  1 +      ctx = withRuntimeUpCandidateConsent(ctx, opts)
    cmd/baha/runtime.go               |  2 +-     replaced a direct withCandidateConsentDigest call
    cmd/baha/runtime_ports_test.go    | 12 ++++    TestRuntimeUpCandidateConsentIsRetainedForLocalApply

`git blame 46d3dccc1 -- cmd/baha/app_input_resolver.go` attributes line 536 to `7b45db92de`, so the
root `up` handler (`commands.go:80` → `runtimeUpCommandWithInputResolver`) does stash the parsed
digest onto its own context on develop.

### B. The refusal lives in app_apply.go:204 and its consent source is ctx, not argv

    cmd/baha/app_apply.go:204   return evidence, fmt.Errorf("record deployment before mutation: %w", err)
    cmd/baha/app_apply.go:203   pending, err := recordDeploymentBeforeMutation(ctx, ..., candidateConsentOverride(ctx))
    cmd/baha/app_apply.go:199   promptConfirmCandidateSubmission(ctx, ...)

So the enforcement reads only the context value set by `withCandidateConsentDigest`. The message is
built inside `recordDeploymentBeforeMutation` (cmd/baha/deployment_record.go:550 →
missingCandidateConsentError, cmd/baha/app_candidate_consent.go:156-161), which joins
`errConsentRequiredForCandidateSubmission` with a `*cli.UsageError` carrying the same sentence —
which is why the candidate path prints the phrase twice.

### C. Every digest-carrying route into that choke, traced (mission item 2)

Root command is registered only at cmd/baha/commands.go:80 → `runtimeUpCommandWithInputResolver`;
`runtimeUpCommand` (cmd/baha/runtime.go:40) is not wired into the CLI tree, so only the resolver path
matters. There are exactly three local routes:

    app_input_resolver.go:536  ctx = withRuntimeUpCandidateConsent(ctx, opts)      (digest -> ctx)
    app_input_resolver.go:577  routeRepositoryRuntimeUp(ctx, ..., opts)
      runtime_repository_up.go:60-61  if opts.CandidateConsent != "" { ctx = withCandidateConsentDigest(ctx, ...) }
      runtime_repository_up.go:63     appApplyCommand(...).Run(ctx, nil, ...)
        app_apply.go:71-72            confirm, rest := stripConfirmCandidateOverride(nil) -> ""
                                      ctx = withCandidateConsentDigest(ctx, "")   <- a NO-OP (app_candidate_consent.go:44-45)
        => digest from :536 survives                                    [COVERED]
    app_input_resolver.go:658-661  repositoryApplicationUp(ctx, ..., opts)
      repository_up.go:86         appApplyCommand(store).Run(ctx, nil, ...)
        app_apply.go:71-72        same no-op strip on empty args
        => digest from :536 survives                                    [COVERED - this was the
                                                                        real #1807 gap]
    app_input_resolver.go:575  remoteApplicationApplyCLI(ctx, target, remoteArgs ...)
      app_input_resolver.go:572-573  remoteArgs += --confirm-candidate <digest>    [COVERED, remote]

The only way to lose the value on a local route is `withCandidateConsentDigest(ctx, "")`, which is a
documented no-op (`app_candidate_consent.go:44-45`: empty digest returns ctx unchanged). Nothing in
`cmd/baha` clears the value outside test fixtures (`clearCandidateConsentDigest` is referenced only
from cmd/baha/app_backup_runtime_fixture_test.go). The digest is also re-validated fail-closed at the
write (`finalizeCandidateConsent`, constant-time compare), so this analysis proposes no weakening.

### D. Why the run still fails: the nested message defeats the consent wrapper (mission item 3)

The gate wrapper is `baseharbor-demo/tests/fixture-consent.py` (invoked as `run_consented`,
tests/lib.sh:182-183). Its recognizer at tests/fixture-consent.py:45 accepts only three exact
messages, and lines 38-44 build them by naive string concatenation:

    direct_message          = prefix + "; refusing to record deployment state"
    wrapped_message         = "record deployment before mutation: " + direct_message
    nested_wrapped_message  = wrapped_message + ": " + direct_message

The real product message is `%w: %w` of `errConsentRequiredForCandidateSubmission`
("; refusing to record deployment state" ALREADY inside it, deployment_record.go:369-371) and a
UsageError with the same sentence. The emitted string is therefore

    candidate submission requires an explicit operator/automation consent (--confirm-candidate);
    refusing to record deployment state: candidate submission requires an explicit
    operator/automation consent (--confirm-candidate); refusing to record deployment state

which contains NONE of the three keys, so `candidate_confirmation()` raises, the wrapper takes the
`digest = ""` branch (line 160), falls through to `current_consent()`, that also raises
("not a current provider-plan refusal") and the loop `break`s at line 168 — it never reaches
`set_candidate_confirmation` (lines 57-74) and never re-invokes with the digest. Its own unit test
(baseharbor-demo/tests/test_fixture_consent.py:32) only pins the direct + single-wrapped forms, i.e.
the nested form has no coverage on either side.

Log evidence, run 45398943139 (head 475902075, workflow "Pre-Release · v0.4.27", created
2026-11-24T13:00:05Z), job 138466518597 (Light · docker · policy):

    :1468 "Candidate to bind for confirmation:" ... "confirm-hash 89c24dd7...a5ed"
    :1474 "Error: record deployment before mutation: candidate submission requires ... : candidate
           submission requires ... refusing to record deployment state"   <- nested, unmatchable
    :1890/1891 [ci-operator-testonly] decision=managed-local-gate command="up --confirm-candidate"
           command="up --confirm-candidate 89c24dd7...a5ed"               <- wrapper DID retry once
    "isolated-demo-fixture" marker count in the whole job log: 0
    "converging application backend and workload" count: 0 (repository_up.go never ran)
    "converging selected application capabilities" count: 2 (runtime_repository_up.go ran twice)

The retry count is one instead of the expected two, and after a successful retry `candidate_confirmation`
would print its acknowledgement marker — neither happened, so I must state one honest limit: from these
logs alone I cannot exclude that the wrapper retried with a stale digest and then hit
`staleCandidateConsentError` (cmd/baha/deployment_record.go:373-378), whose hint
("Review the current submission and re-run with --confirm-candidate ...") does not match the wrapper's
`re.fullmatch` either. That alternative is also a consent-handshake gap, but on the string-contract
side, not in the propagation code the mission targets. Distinguishing the two needs the full
`ci-operator.log` artifact rather than the `tail -n 160` the job prints.

### E. Proposal — NOT implemented, and it is outside this card's write-set

- Minimal, correct and fail-closed: in `mcpdev80/baseharbor-demo/tests/fixture-consent.py`, replace
  the three string-equality keys (lines 36-46) with a structural test — the error message must both
  contain the documented prefix and end in the documented refusal clause — so every honest wrapping
  depth is accepted while the digest check (lines 48-53) and all other branches stay unchanged. The
  same PR should extend tests/test_fixture_consent.py with the nested form. Gate coverage:
  atomic/docker and atomic/podman `policy`, `connectivity`, `reconciliation`, `full-destroy` are the
  gates that consume this handshake, and they are exactly the failing four.
- It is a DIFFERENT REPOSITORY, so it cannot ride on this card's write-set
  (cmd/baha only) and cannot be done here. I did not implement it and did not open any branch or PR.
- No product change is justified for the propagation itself: the candidate already carries every line
  #1807 touched (`git show 475902075:cmd/baha/app_input_resolver.go | grep -n withRuntimeUpCandidateConsent`
  → 536; file-level diff of app_input_resolver.go and app_apply.go between 46d3dccc1 and 475902075 is
  empty). A digest-threading PR would be an empty diff against develop, i.e. the #1807 duplication the
  owner hold forbids.
- The only product-repo work this card could legitimately still carry is the missing regression test
  `TestRootUpCandidateConsentIsAvailableToRepositoryApply` (see findings item 3) — a test-only PR
  asserting the existing behaviour, not a fix.

## findings

### 1. The claim on card 0428-281 is now stale and needs an owner action

Per mission step 1 the card was claimed and published to planning main before any edit:
`a3d982bf0` sets `owner: w85-0428-281-consent (session w85)` and
`kanban_status/kanban_lane: active`. The lane is now stopped and this session is released, so the
card must move back to `planned` (or `waiting`) and the owner field cleared. I did not do this
myself because the hold says "stand by" and card status is a coordination decision, not an
execution step (AGENTS 3.7 says the Coordinator publishes state changes).

### 2. The propagation the card asks for is already on develop, and #1812 already contains it

Confirms the owner's new evidence, from the source at `46d3dccc1`:

- cmd/baha/app_candidate_consent.go:50 — `withRuntimeUpCandidateConsent(ctx, opts)` exists.
- cmd/baha/app_input_resolver.go:536 — `ctx = withRuntimeUpCandidateConsent(ctx, opts)` inside
  `runtimeUpCommandWithInputResolver` (the root `up` handler, cmd/baha/commands.go:80).
- cmd/baha/runtime.go:73 — same call in `runtimeUpCommand`.
- cmd/baha/runtime_repository_up.go:60-62 — `if opts.CandidateConsent != "" { ctx =
  withCandidateConsentDigest(...) }` immediately before the internal
  `appApplyCommand(...).Run(ctx, ...)` at :63.
- `git merge-base --is-ancestor 7b45db92de 46d3dccc1` → true, so PR #1807 ("fix(cli): retain
  candidate consent on local up", merged 2026-11-23T16:03:32Z) is in develop. PR #1808 (its
  gate-coverage rows, merge 4f67760a) is likewise an ancestor of develop.
- `git merge-base --is-ancestor 5f9c67102 46d3dccc1` → false, i.e. #1647 was never merged, exactly
  as the card says — but #1807 is a superset of that change in behaviour: identical call-site
  threading, plus the same threading in runtime.go and a regression test.
  `git merge-base --is-ancestor 5f9c67102 7b45db92de` → false (independent lineage, not a cherry-pick).

A separate 2-file consent PR would therefore re-add an existing line to app_input_resolver.go and
duplicate #1807/#1647. The owner hold is correct.

### 3. What is genuinely missing on develop: only the regression test

- `git grep -n TestRootUpCandidateConsentIsAvailableToRepositoryApply` at 46d3dccc1 → no match.
  The named test in the mission and in the card's second Regression bullet does not exist.
- The only consent-retention test #1807 added is
  `TestRuntimeUpCandidateConsentIsRetainedForLocalApply` at cmd/baha/runtime_ports_test.go:31.
  It exercises `parseRuntimeUpOptions` + `withRuntimeUpCandidateConsent` and asserts the digest lands
  on the context; it never touches the root-up resolve path or the repository apply hand-off.
- Consequence per baseharbor-plan AGENTS "Mandatory test-to-CI routing": the card's acceptance line
  "A CI-discovered Go test asserts up preserves candidate consent (success when granted,
  fail-closed when not)" is NOT satisfied today — the fail-closed branch in particular is unasserted
  in the up path (the fail-closed-without-consent case is covered only for `app apply`, e.g.
  cmd/baha/app_candidate_consent_test.go).

### 4. The card's diagnosis no longer matches the failure evidence

Run 45398943139 (head 475902075, workflow "Release · Pre-Release Validation") failed with exactly
these four jobs: `Light · docker · policy`, `... · connectivity`, `... · reconciliation`,
`... · full-destroy`; `guided`, `lifecycle` and `failure` passed. The aggregate step reported
`AssertionError: runtime_light_gates_docker: expected success, got failure`.
The consent-propagation text the card quotes does not appear anywhere in `gh run view
--log-failed` output, and that head post-dates #1807, so the mechanism the card names is already in
the failing candidate. The log available to me only re-states gate identities and fingerprints, so
the actual per-job cause is still unknown to this lane — the gate logs/artifacts need to be read by
whoever re-scopes the card.

### 5. Suggested re-scope (owner/coordinator decision, not executed here)

Keep the card, retitle it from "up loses candidate consent" to something like "no CI regression test
guards candidate-consent retention in the root up path", narrow the write-set to
cmd/baha/runtime_repository_up_test.go only, and make the Light-gate failures a separate investigation
card — the product code line in the current contract is already done and any PR that "fixes" it is a
no-op diff against develop.

## cleanliness

Baseline before any work, on the session host (pid 3461316): `docker ps -a -q | wc -l` → `0`, empty
name list. After the stop (pid 3484894): `docker ps -a` → 0 containers. No container, compose
project, network or volume was created by this lane at any point, and nothing was started on any
baha-docker / baha-podman host. No product test was executed locally (Hosted-only rule respected:
the only commands run were git, gh read-only queries and plan.py).

Local artifacts removed on the hold:

    $ git worktree remove /home/marcel/dev/baseharbor-ecosystem/workers/0428-281-consent-wt   -> worktree removed
    $ git branch -D lane-0428-281-consent                                                     -> Deleted branch (was 46d3dccc1)
    $ git branch --list 'lane-0428-281*'                                                      -> (empty)
    $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-281-consent -> (empty)
    $ gh pr list --head lane-0428-281-consent --state all                                     -> []
    $ git worktree list | grep -c 281                                                         -> 0

The worktree was never modified: `git -C <wt> status --short` was empty and its HEAD stayed exactly
`46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2` with no commits above origin/develop.

Scratch zone: /tmp/opencode/w85-0428-281-consent/ (this evidence file, the CI job-log captures, a
read-only `cmd/baha` tree extraction and a shallow clone of baseharbor-demo).

SIDEBAND FINDING (reported, not repaired): my read-only `git --work-tree=<scratch> checkout <sha> --
cmd/baha` commands staged trees into the INDEX of the shared product checkout
/home/marcel/dev/baseharbor-ecosystem/baseharbor, whose own HEAD is a foreign lane head
(`306a2b1ea fix(0428-078): ...`, a lane that is not mine and that I did not touch otherwise). The index
now shows 7 entries differing from that HEAD (cmd/baha/app_status_collect.go,
app_status_perses_alert_evaluator_0428_152_test.go, app_status_result.go,
ci_integration_operator_enabled{,_test}.go, env_destroy_integration_test.go, perses_lifecycle.go).
Neither of my mission's write-set files is among them, and no commit, push or branch came from this
lane. I left the index as found because unstaging could destroy that lane's staged work (AGENTS 4.3:
do not overwrite another session's working state). Lesson recorded: in a shared checkout, read a
foreign tree with `git show <sha>:<path>` into the scratch zone instead of `git --work-tree` checkout.
Coordinator may want to tell the 0428-078 lane to re-stage before it commits.

## repo-rule compliance

- Hosted-only: zero local test execution; verification intent was CI-only. Compliant.
- Workflow scope: no `.github/**` and no `scripts/**` edits; no reruns or workflow_dispatch. Compliant.
- One candidate per chain / no chain contact: #1812, #1647, #1807, #1808 branches and PRs were only
  read via `git show` / `gh pr view`; nothing was reopened, rebased or pushed. Compliant.
- No subagents (AGENTS 4.8): every step ran in this session. Compliant.
- Claims published via scripts/plan.py and pushed to planning main directly (WORKFLOW.md: planning
  goes to main, no planning branch/PR). Compliant, but see ## findings item 1.
- Evidence lives only in baseharbor-plan under evidence/; nothing added to a product repo. Compliant.
- Acceptance items the card requires that this lane did NOT meet: Light gates green on an exact
  candidate head (not this lane's deliverable per mission step 3) and a CI-discovered Go test
  (blocked by the hold; see findings item 3). Card therefore cannot close on this lane.

## evidence-on-origin proof

Planning-repo push remote guard (must resolve to github.com/mcpdev80):

    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

`git -C baseharbor-plan fetch origin main && git ls-tree -r --name-only origin/main | grep <evidence-path>`
(verbatim output, after pushing commit `b5c7e114e`):

    From https://github.com/mcpdev80/baseharbor-plan.git
     * branch                main       -> FETCH_HEAD
    evidence/r28-welle6-2026-11-25/0428-281-consent/diagnosis.md

Delivery witness, `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`:

    b5c7e114e1e323e29f3bcb921662e1e5665c9c9f        refs/heads/main

Final re-run of the same pair after the last planning commit (`d283ec19d`, verbatim):

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main
    From https://github.com/mcpdev80/baseharbor-plan
     * branch                main       -> FETCH_HEAD
    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep 0428-281-consent
    evidence/r28-welle6-2026-11-25/0428-281-consent/diagnosis.md

Content witness, `git show origin/main:evidence/r28-welle6-2026-11-25/0428-281-consent/diagnosis.md | head -3`
returns this file's title and lane header (shown in the pushed tree above).

Product repo untouched, `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
refs/heads/lane-0428-281-consent refs/pull/1812/head`:

    46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2        refs/heads/develop
    47590207518ce9501f1b1bbb115d72d64a206d14        refs/pull/1812/head

(the `refs/heads/lane-0428-281-consent` line is absent — this lane created no product branch and no PR;
#1812 head is unchanged by this lane.)

## END

END_DONE w85-0428-281-consent: read-only diagnosis complete — no candidate SHA by design (owner hold: no
branch, no PR). Verdict: the `--confirm-candidate` propagation is already on develop `46d3dccc1`
(cmd/baha/app_input_resolver.go:536 from merged #1807 `7b45db92`, plus runtime_repository_up.go:60-61),
so a digest-threading PR would be an empty diff and duplicate #1807; the 4 failing Docker Light gates
(policy/connectivity/reconciliation/full-destroy) fail instead because baseharbor-demo
tests/fixture-consent.py:38-46 does not match the nested candidate-refusal message and so never re-runs
with the digest. Evidence: evidence/r28-welle6-2026-11-25/0428-281-consent/diagnosis.md (b5c7e114e).
Proposed fix is in another repository (demo harness) and needs a new card + owner authorization.
