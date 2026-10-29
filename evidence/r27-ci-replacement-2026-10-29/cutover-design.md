# R27 CI cutover design — candidate-bound asynchronous completion (lane q201)

Task: t-20261029-r27-ci-cutover-design (v0.4.27). READ-ONLY design: no product commits,
no planning commits, no ruleset activation. This file is the sole write of lane q201.

## PLAN

[✔] 0. basics-check run; dispatch prompt q201.txt read; scope: READ-ONLY + this file
[✔] 1. `git -C baseharbor fetch origin`; develop HEAD recorded via `rev-parse` + `ls-remote`
[✔] 2. `.github/workflows` on `origin/develop` inspected (`git show`): `receipt-approval.yml`,
      `receipt-shadow.yml`, `receipt-post-run.yml`, `ci.yml` (`pr_selected_final`)
[✔] 3. `scripts/pr-gate-plan.py` and `scripts/pr-required-final.py` inspected; receipt
      candidate semantics in `scripts/receipt_verifier.py` (`extract_facts`, `retained`, `approve`)
[✔] 4. Pins inventoried (checkout/shadow/controller/workflow-pin, see §0 table)
[✔] 5. Live rulesets read via `gh api` (25223521 + 23754541 + repo listing)
[✔] 6. Live check-run placement verified (app id 15368, PR head SHA binding; no receipt-path
      check exists on any PR head today)
[✔] 7. Design §1 written (new required context name + producing job mechanics)
[✔] 8. Design §2 written (stale / missing / failed / mismatched behavior)
[✔] 9. Design §3 written (exact ruleset JSON patch, activation deferred to maintainer)
[✔] 10. Design §4 written (rollback = revert of the ruleset patch only)
[✔] 11. Design §5 written (unresolved rights and gaps)
[✔] 12. END line appended

## 0. Reality ground (read-only commands, 2026-10-29)

| Fact | Evidence |
|---|---|
| develop HEAD | `git -C baseharbor ls-remote origin refs/heads/develop` → `7a4debccc4e2fa5e78287e9b9388b0cb521d66e2` |
| Ruleset 25223521 | `gh api repos/mcpdev80/baseharbor/rulesets/25223521`: `enforcement=disabled`, rule `required_status_checks` → `[{context: "PR Selected Checks", integration_id: 15368}]`, `strict_required_status_checks_policy=true`, `do_not_enforce_on_create=false`, `bypass_actors=[]`, `current_user_can_bypass=never` (updated_at 2026-10-28) |
| Ruleset 23754541 | `enforcement=disabled` (branch rules incl. `pull_request`; bypass User 22537373 always) — integration gate lives elsewhere in the live state; not modified by this design |
| Legacy producer | `ci.yml` job `pr_selected_final`, `name: PR Selected Checks` (ci.yml:808), `if: always() && github.event_name == 'pull_request' && github.base_ref == 'develop'`; runs `scripts/pr-required-final.py` against `trusted-pr-plan` + authenticated results |
| App binding | PR #1188 head `c03cdfb0…`: check run `PR Selected Checks` has `app.id=15368`, `app.slug=github-actions`, `head_sha` = PR head. `/actions/runs/40835806321` shows `workflow_run` runs also place job check runs (app 15368) on the producer `head_sha` |
| Receipt pipeline | `receipt-post-run.yml`: on `workflow_run` of "CI · Source & Quality" success → publishes UNAPPROVED receipt to Planning (controller pin `e13f1570550f4b6b09f3727728293d91afbebf94`, attempt must be 1). `receipt-approval.yml`: Owner-only (`github.actor == 'mcpdev80' && github.triggering_actor == 'mcpdev80'`) manual dispatch; verify+approve+publish, outputs `receipt/plan/candidate/publication`; calls `receipt-shadow.yml@f57b30ed48f19e62452ab793801a02ccd2658414` (job `PR · Receipt Shadow Consumption`, offline retained verify at the exact publication commit) |
| Candidate semantics | `receipt_verifier.extract_facts`: `candidate_sha = integration_sha` (the producer run's merge-commit head); the plan fixture also carries `head_sha` (PR head) and `base_sha`; `live()`/`retained()` fail closed on `wrong candidate SHA` / `plan candidate mismatch` |
| Dormancy | `TRUSTED_SOURCE: ''` in `receipt-approval.yml` (fails closed until coordinator registration updates it + the shadow pin to the final integrated reviewed head); `receipt-approval.yml` has NEVER run (workflow runs list empty); `receipt-post-run.yml` recent runs 2026-10-29: 40834168626 failure, 40811856878 failure (step "Publish receipt to Planning"), 40835806321 skipped |
| No candidate check yet | PR head `c03cdfb0…` check-run list contains NO `Receipt`/`Shadow`/`Post-Run` name — the receipt path currently produces zero GitHub-visible completion |

Interpretation of "producing app/workflow event": the required context must be satisfied by a
check run whose delivering app is GitHub Actions (`id 15368`), so the ruleset matcher
(`integration_id: 15368`) binds it and GitHub delivers `check_run`/`check_suite` app events for
it. All three delivery mechanisms observed above (pull_request job, workflow_run job, REST
`POST /check-runs` with the Actions token) attribute to app 15368.

## 1. New required context (durable receipt-approved completion of the exact candidate)

**Exactly one new required context:**

```
Receipt · Candidate Completion        (integration_id 15368, check-run name set verbatim,
                                       including the U+00B7 middle dot)
```

Producer: a new final job `gate` in `.github/workflows/receipt-approval.yml` (same file, so the
Owner-only dispatch precondition and authenticated inputs apply unchanged):

- `needs: [approve, shadow]`, `if: always()` — so failure/neutral chains still report (see §2).
- `permissions: {contents: read, actions: read, checks: write}`.
- Inputs it may use: `inputs.pr_number` (string), `needs.approve.outputs.{receipt,plan,candidate,publication}`
  plus ONE new required output `head` (the PR head SHA auto-resolved by
  `receipt_verifier.resolve_pull` during approve; never a manual input). Implementation task must
  extend the approval step's output capture loop with `head:*` and its completeness check
  (`head` must match `^[0-9a-f]{40}$`), mirroring the existing R27-F6 fail-closed pattern.
- SHA placement: the check run is created with `head_sha = <current PR head SHA>` read LIVE from
  `gh api repos/mcpdev80/baseharbor/pulls/<N> --jq .head.sha`. Chosen deliberately over placing
  it on `candidate` (the merge commit): the ruleset merge gate evaluates required checks on the
  PR head commit (grounded: `PR Selected Checks` check runs sit on head SHA `c03cdfb0…`), and
  merge refs are rewritten by GitHub whenever head or base moves, so a merge-commit placement
  could silently detach from the evaluated commit. The EXACT candidate is nonetheless bound to
  the check run by content: the `external_id`, `details_url` and annotations carry
  `candidate`, `receipt`, `plan`, `publication`, producer `run_id`/`attempt` (see below), and the
  approval chain already proved `receipt.sha == plan.candidate_sha == producer run head_sha`
  (`live()`) and offline durable re-proof at the publication revision (`retained`).
- Creation protocol:
  1. `POST /repos/mcpdev80/baseharbor/check-runs` with `name="Receipt · Candidate Completion"`,
     `head_sha=<live head>`, `status=completed`, `conclusion=<success|failure>`,
     `external_id="<candidate>:<publication>"`,
     `details_url=<evidence_reference(publication, receipt)>` (content-addressed Planning blob URL),
     `output={title, summary, annotations}`.
  2. Annotations (one per fact, always present): receipt path; plan revision; exact candidate
     (integration) SHA; durable publication commit; producer run id + attempt; the verdict rule
     applied. Failure annotations carry the machine-checkable reason line from §2.
- Verdict rule (`success` only when ALL hold; otherwise `failure`):
  a. `needs.approve.result == 'success'` (live verification + durable approval publication done);
  b. `needs.shadow.result == 'success'` (offline retained verification AT the publication commit);
  c. all four approve outputs present and well-formed (40-hex, `evidence/receipts/*.json` path);
  d. live PR head SHA == approved `head` output, and live PR base develop-HEAD ancestry is
     current (see strict policy, §5 gap 5);
  e. the authenticated PR number equals the dispatched `pr_number` input.
- Idempotence/rerun: creation is keyed by `(name, head_sha)`; a second dispatch after head move
  targets the new head; the old head's check becomes irrelevant naturally (stale, §2).

Why exactly one context: the durable proof is atomic — CI completion without Owner approval, or
approval without durable retained re-verification, must not be mergeable in pieces. Two contexts
would create a half-green state the ruleset would need to AND anyway. (Rejected alternative kept
on record: a second informational "Receipt · Published" context from `receipt-post-run.yml`; not
required by the ruleset, so it adds no gate strength.)

## 2. Behavior for stale / missing / failed / mismatched

| State | How it arises | What the check shows | Merge consequence |
|---|---|---|---|
| **success (green)** | approve+shadow pass; head unchanged since approval; receipt binds the exact candidate whose producer run was attempt 1 green | `completed/success`; annotations carry candidate/receipt/plan/publication/run | mergeable (subject to ruleset 23754541 review rules) |
| **missing** | Owner never dispatched approval; or dispatch failed before `approve` resolved outputs (no head known); or producer attempt 1 never went green (`receipt-post-run` refuses non-attempt-1, so nothing publishes) | no check run exists → merge box "Required checks have not passed" / pending, never assume success | blocked (fail-closed; `do_not_enforce_on_create=false` means only check runs created after activation count, so pre-cutover runs never satisfy it) |
| **stale** | PR head moved after the approval (force-push/new commit), or base `develop` advanced under `strict_required_status_checks_policy=true` | new head has NO check run (missing, pending) — the green check stays on the old head SHA and cannot transfer; a re-dispatch of approval on the moved PR produces `completed/failure` with annotation `stale: approved head <old> != live head <new> (replan + re-approval required)` | blocked until fresh CI run → fresh receipt → fresh approval |
| **failed** | approve job failed (verifier live() refusal, malformed outputs, wrong actor — fail closed inside the step), or shadow retained verification failed, or gate `if: always()` runs with any `needs` in `failure/timed_out/cancelled` | `completed/failure`; output.title states the stage (`approval failed` / `retained verification failed` / `chain incomplete`); summary links the failed workflow run | blocked (red) — explicit red instead of indefinite pending, because a dispatched Owner run always lands a terminal conclusion on the live head |
| **mismatched** | receipt/plan/candidate cross-check disagreement surfaces as: dispatched `pr_number` resolves to a PR whose head/base differ from the plan fixture; shadow input publication/plan not in protected Planning history; or gate condition d/e violated | `completed/failure` with annotation `mismatch: <field> <approved-value> != <live-value>`; if even the live head cannot be resolved (PR closed/deleted), NO check run is created and the lane records the run URL only (fail-closed as missing) | blocked |

Invariants preserved: no empty-string skip (R27-F6 — missing outputs fail the approve step before
`gate` ever reports success); `gate` never reads PR-controlled code (only the authenticated run
context + Planning + APIs); the check's green state is evidence of a durable, content-addressed
Planning fact, not of a transient runner result.

## 3. Ruleset JSON patch (activation belongs to the maintainer; q201 does NOT touch it)

Target: `PUT https://api.github.com/repos/mcpdev80/baseharbor/rulesets/25223521` (ruleset PUT is
whole-body; no `sha` precondition needed). Body derived from the LIVE object captured in §0:

```json
{
  "name": "develop - required checks",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [],
  "conditions": {
    "ref_name": { "include": ["refs/heads/develop"], "exclude": [] }
  },
  "rules": [
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "do_not_enforce_on_create": false,
        "required_status_checks": [
          { "context": "Receipt · Candidate Completion", "integration_id": 15368 }
        ]
      }
    }
  ]
}
```

Delta vs live: (i) `enforcement`: `disabled → active`; (ii) required_status_checks:
`"PR Selected Checks"` REMOVED (retirement at the gate level) and `"Receipt · Candidate
Completion"` added, both bound to `integration_id 15368`.

Retirement scope of legacy contexts:
- Only the ruleset binding changes. The legacy PRODUCER (`ci.yml` job `pr_selected_final` emitting
  `PR Selected Checks`) stays deployed and running — it becomes an informational check again
  (as it already effectively is while enforcement is disabled) — and is removed only in a LATER,
  separately reviewed product PR after the new path has qualified (retention window: ≥ 10
  consecutive merged PRs plus ≥ 1 rollback drill). Deleting it in the same step would destroy the
  rollback precondition (§4).
- The job name `PR · Receipt Shadow Consumption` inside `receipt-shadow.yml` (currently a
  candidate-invisible check on the dispatch run's SHA) must NOT be added to the ruleset; it stays
  informational. Recommend the implementation task rename it to `Receipt · Shadow (informational)`
  to keep context-name namespaces unambiguous.
- A pre-cutover snapshot file `docs/internal/review-protection/develop-required-checks.ruleset.json`
  must be updated by the implementation PR to contain BOTH bodies (pre = current with
  `enforcement: "disabled"` preserved verbatim from this capture, post = above), so the revert
  (and this lane's capture) never depends on chat history.

Suggested staging order for the maintainer (not an activation by this lane): deploy product
changes to develop → coordinator registration (TRUSTED_SOURCE + pins, §5 gap 2) → one informational
dispatch end-to-end on a throwaway PR → set ruleset `enforcement: "evaluate"` and observe merge-box
neutrality on live PRs for a soak period → final PUT body above (`active`).

## 4. Rollback

Rollback is EXCLUSIVELY the documented revert of the §3 patch. No product code, no Planning, no
workflow redeployment:

```
PUT /repos/mcpdev80/baseharbor/rulesets/25223521
{ … body of §3 with enforcement:"disabled"→"active" as it was BEFORE the cutover:
  {"name":"develop - required checks","target":"branch","enforcement":"active",
   "bypass_actors":[],
   "conditions":{"ref_name":{"include":["refs/heads/develop"],"exclude":[]}},
   "rules":[{"type":"required_status_checks","parameters":{
     "strict_required_status_checks_policy":true,"do_not_enforce_on_create":false,
     "required_status_checks":[{"context":"PR Selected Checks","integration_id":15368}]}}]}
```

(The pre-cutover live body had `enforcement:"disabled"`; the rollback target is the last-known-good
ACTIVE form above — the implementation PR stores both snapshots, and the operator picks per the
incident note. If only the activation itself must be undone without restoring legacy enforcement,
the same PUT with `"enforcement":"disabled"` reverts to the exact captured live state.)

Conditions for rollback validity:
- The legacy producer (`pr_selected_final` in ci.yml) must still be deployed — guaranteed by the
  §3 retention window; this is why legacy PRODUCER retirement is out of the rollback's scope.
- Effect: PRs that already merged under the receipt gate stay merged (linear history, no revert of
  commits); open PRs fall back to needing a green `PR Selected Checks`, which every push to a
  pull_request-active PR regenerates automatically.
- A rollback does NOT retire new-path receipts already published in Planning; those remain
  append-only durable evidence (no deletion, no rewrite).
- Post-rollback verification: `gh api repos/mcpdev80/baseharbor/rulesets/25223521` diff against the
  stored snapshot; one open PR must show `PR Selected Checks` as its required context.

## 5. Explicit unresolved rights and gaps

1. **Rights**: ruleset PUT/PATCH requires repo-admin (Owner token) — this lane had read-only API
   scope (`gh api` GET only) and performed zero mutations. `checks: write` for the future `gate`
   job is a workflow-permission expansion that itself ships through the normal PR gate —
   self-referential but bounded (the new job can mark its own qualifying PR red/green only,
   matching today's `PR Selected Checks` authority level).
2. **Pins/registration not final**: `TRUSTED_SOURCE: ''` (receipt-approval), reusable-workflow pin
   `f57b30ed48f19e62452ab793801a02ccd2658414` (shadow call), controller pins
   `e13f1570550f4b6b09f3727728293d91afbebf94` (post-run, x2), and the workflow's dormancy until a
   "CI-only default-branch registration" (workflows live on develop, dispatch reads them from
   default branch `main`). Every pin must be moved to the final integrated reviewed head by the
   coordinator at registration; while stale, the chain fails closed. Cutover §3 must not be
   applied before this registration is itself merged and dispatched clean.
3. **Pipeline is currently failing live**: `receipt-post-run.yml` "Publish Receipt to Planning"
   failed twice on 2026-10-29 (runs 40834168626, 40811856878; one skipped, 40835806321) and
   `receipt-approval.yml` has never run. Prerequisite: receipt publication must be green for a
   sustained window before the enforcement flip; the cause of those publish failures is NOT
   diagnosed in this lane (out of scope) and must be closed first.
4. **App-identity of REST-created check runs**: §0 grounds that pull_request and workflow_run
   check runs attribute to app 15368; that a REST `POST /check-runs` made with the Actions token
   also attributes to app 15368 (not the author's OAuth app) is the standard behavior assumed by
   this design but not yet witnessed in this repo. Registration must first create one
   informational check run via the gate on a throwaway PR and verify `.app.id == 15368` before
   the ruleset PUT; if the platform attributes otherwise, the design pivots to a workflow_run- or
   pull_request-triggered gate placement (documented alternative: the same `gate` job in a
   pull_request-targeted workflow that re-reads the published approval at its PR head).
5. **Strict policy × async approval churn**: with `strict_required_status_checks_policy=true`,
   every develop advance makes every approved-but-unmerged PR stale (head must re-integrate →
   new CI run → new receipt → new Owner dispatch). Cost is Owner time. Unresolved decision kept
   with Owner: keep `strict=true` (this design's baseline, matches current semantics) vs
   `strict=false` with the gate itself re-verifying base ancestry (would need the receipt to bind
   a base-integration proof; larger change).
6. **Attempt-1-only publication** (post-run hard refuses `run_attempt != 1`): a PR whose attempt 1
   CI failed and attempt 2 passed has NO receipt and can never get one without a fresh push.
   Unresolved: either relax to attempt-N publication with receipt re-keying (product task), or
   document "push again to re-produce attempt 1" as the operational answer.
7. **Human serialization**: the only trigger is a manual Owner `workflow_dispatch`; there is no
   queue, no SLA, and no auto-dispatch on receipt publication (deliberate — approval is the
   human decision). Blocked-PR waiting time is unbounded by design; flagged so the board can
   track Owner load, not hidden.
8. **Legacy text retirement**: `docs/DEVELOPMENT_GUIDELINES.md:127`, `docs/de/DEVELOPMENT_GUIDELINES.md:117`,
   `docs/internal/review-protection.md`, `scripts/PR_RUNTIME_REQUEST_INTERFACE.md:22` and
   `scripts/pr-required-final.py` still name `PR Selected Checks` as THE required gate. These are
   product docs/code and follow the retention window of §3; the ruleset patch does not and must
   not touch them, and this design does not edit them (READ-ONLY lane).
9. **Placement witness gap**: whether GitHub evaluates required checks against the PR head commit
   in ALL merge-box paths (merge queue would differ; this repo uses squash+linear, so head-SHA
   placement is the evaluated one). If a merge queue is ever introduced, re-derive §1 placement.
10. **Closed/deleted PRs**: dispatch on a closed PR cannot resolve a live head; the gate then
    creates nothing (missing = fail closed). Acceptable; documented so no one "fixes" it by
    creating checks on orphaned SHAs.

## repo-rule compliance

- Claim protocol honored by the coordinator (lane dispatched read-only; planning publishing by
  coordinator; q201 wrote ONLY `baseharbor-plan/evidence/r27-ci-replacement-2026-10-29/cutover-design.md`,
  working tree, no `git add/commit/push`, no product edits, no ruleset mutation).
- All factual claims above cite the command that produced them (§0); transient values (SHAs, run
  ids, enforcement states) are point-in-time reads of 2026-10-29 and must be re-read live before
  the cutover implementation task starts.
- No secrets, tokens or credentials appear in this document.

END q201-DONE
