# R27 CI cutover design — correction round (o218, evidence-only)

Task: t-20261029-r27-ci-cutover-design (v0.4.27). CORRECTION ROUND, evidence-only. No product write,
no planning write, no ruleset activation, no git in baseharbor-ecosystem. Reads:

- v1 candidate: `baseharbor-plan/evidence/r27-ci-replacement-2026-10-29/cutover-design.md` (lane q201)
- o215 findings: `baseharbor-plan/evidence/r27-ci-replacement-2026-10-29/shadow-preflight.md`
  (findings 1–4 with payloads)
- o216 patch draft: `baseharbor-plan/evidence/r27-ci-replacement-2026-10-29/ruleset-patch-preflight.md`

This file is the sole write of lane o218. It does NOT change §1–§5 of v1; it replaces the three
specific v1 assumptions the o215 payloads disprove and adds (2) the exact first real chain-run
sequence with the concrete live workflow_ids and (3) the exact evidence that must sit at the end of
the evidence file to make ruleset activation + Ready-sperre-off legal.

## PLAN

0. basics-check run; this task prompt read; scope: EVIDENCE-ONLY (no product, no planning, no git)
1. Read v1 (§1 head-SHA placement, §3 ruleset patch, §5 gap 5 strict-policy), o215 findings 1–4, o216 §1–§5
2. §A: map each o215-disproven assumption to the corrected statement, with the disproof payload
3. §B: exact first real chain-run sequence (Producer run 352609139 → Post-Run 397459764 → approval → shadow → gate)
4. §C: exact evidence-set required at the end of the evidence file for legality of activation + Ready-off
5. END line appended

## §A. Which v1 assumptions are replaced by the o215 findings (and by what)

o215 ran the real authenticated GitHub objects for the first time and proved three concrete facts
that contradict three explicit v1 statements. Each row: v1 claim → o215 disproof payload → corrected
statement. (Nothing in v1 §2, §4, or the "exactly one context" invariant is affected.)

### A1. base_ref-regex directive (v1 head-SHA placement rationale) — REPLACED

- **v1 claim (§1, lines 64–67):** the check run's `head_sha` is chosen "deliberately over placing it
  on candidate (the merge commit)": head SHA is read live from `gh api …/pulls/<N> --jq .head.sha`
  because merge refs are rewritten by GitHub whenever head or base moves.
- **o215 disproof (finding 1, payloads lines 20–53):** the live producer/producer-of-post-run objects
  carry `base_ref: null` on BOTH the real PR producer (run 40833893562, PR #1199) and on every post-run
  (run 40885711304, sha 7a417d37). The post-run `workflow_run.head_sha` is a **merge commit**
  (7a417d37 = #1198 merge, parent d92c1654), never the PR head. The PR-Number regex in
  receipt-post-run.yml (lines 142–144, `refs/pull/([0-9]+)/merge`) is **empty** for PR-producer and
  merge-producer alike (base_ref null); `.pull_requests` is empty on the workflow_run object. PR-Number
  and candidate/base/head SHAs therefore come from the **trusted-pr-plan artifact**, not from any
  checkout of `refs/pull/N/head` and not from a live base_ref.
- **corrected statement:** the ruleset merge-gate still evaluates on the PR head commit (v1 §1 rationale
  — GitHub evaluates required checks on the PR head, confirmed by the `PR Selected Checks` runs sitting
  on head SHA `c03cdfb0…` — stays valid). BUT the *producer* no longer "reads head live from the PR API
  by base_ref"; the chain is driven entirely by (a) the authenticated `workflow_run.head_sha` = **merge
  commit** and (b) the **trusted-pr-plan.json artifact** (pr_number + candidate/base/head). The post-run
  workflow already does NOT checkout `refs/pull/N/head` (o215 finding 4, controller pins `dd8fb61d` at
  lines 86/219, Planning checkout `main` at line 227). So the corrected design binds the exact candidate
  by artifact content alone — `external_id`/`details_url`/annotations carry `candidate` (integration
  SHA), `receipt`, `plan`, `publication`, and `workflow_run.head_sha` (merge commit) — and by the already-
  proven approval chain (`receipt.sha == plan.candidate_sha == producer run head_sha` live, `retained`
  offline). The v1 "read head live from the PR API" step is **removed**; head is the PR head resolved at
  approval time by `receipt_verifier.resolve_pull` (the new `head` output, 40-hex, fail-closed), and the
  merge-gate check sits on that head. This is consistent with o215 finding 1a: producer `head_sha` is PR
  head `96a96362` on a live `pull_request` producer and the merge commit on develop-push — both are the
  authenticated runtime facts, not a manually read PR API value.

### A2. pr-plan.json artifact identity (v1 candidate-binding mechanism) — REPLACED

- **v1 claim (§1, lines 69–73, 83–89):** the EXACT candidate is bound to the check run by content that
  the `gate` job assembles from `needs.approve.outputs.{receipt,plan,candidate,publication}` plus a new
  `head` output; the approval chain already proved `receipt.sha == plan.candidate_sha`.
- **o215 disproof (finding 1, lines 57–78, 120–128):** candidate/base/head SHAs are read from
  **pr-plan.json** (the trusted-pr-plan artifact the producer uploads), **not** from a checkout ref and
  **not** from the workflow_run object (which exposes no PR payload and a merge-commit head). The PR
  number the Writer/Tasklink need comes from the artifact's `pr_number` (env `PR_NUMBER`, empty for a
  PR-producer unless the producer carries it). `RUN_ID = github.event.workflow_run.id` fetches that
  artifact. Every SHA used is the artifact's, and the workflow_run head_sha is the merge commit.
- **corrected statement:** the `gate` job's candidate binding no longer "assembles from approve outputs
  alone". It is two-source: (1) the **trusted-pr-plan.json artifact** supplies the canonical
  `pr_number` + `candidate` (integration SHA) + `base` + `head`; (2) the **live PR head at approval
  time** (`head` output from `resolve_pull`) is asserted equal to the approved head (gate condition d).
  The `external_id`/`details_url`/annotations therefore carry the artifact `candidate` (verified against
  `receipt_verifier.extract_facts`: `candidate_sha = integration_sha`), the merge-commit `workflow_run.head_sha`,
  and the `head` (PR head). A mismatch between artifact `head` and live PR head, or between artifact
  `pr_number` and the dispatched `pr_number`, is gate `failure` with annotation `mismatch: head
  <approved> != <live>` (v1 §2 mismatched row, kept). The v1 §1 "assemble from approve outputs" is
  narrowed to "assemble from **artifact facts** + the live-approved `head`", with the artifact as the
  source of truth for the exact candidate.

### A3. workflow_run.head_sha = merge-commit semantics (v1 §5 gap 5, strict policy) — REPLACED/SHARPENED

- **v1 claim (§5 gap 5, lines 227–232):** under `strict_required_status_checks_policy=true`, every
  develop advance makes every approved-but-unmerged PR stale (head must re-integrate → new CI run → new
  receipt → new Owner dispatch). Unresolved decision kept with Owner (strict=true vs strict=false).
- **o215 disproof (finding 1, lines 43–60; finding 2, lines 80–108):** the workflow_run head_sha is the
  merge commit (develop-HEAD), and `refs/pull/N/head` for closed/merged PRs #1198/#1199/#1202 **still
  exist** post-merge (`delete_branch_on_merge=null`, no auto-delete). PR #1199 is a **Squash-Merge**
  (`merge_commit_sha=null`), so its develop-HEAD is the squash SHA, not a second-parent merge commit.
- **corrected statement:** gap 5's "develop advance → stale" is now two distinct cases, both owned by
  the merge method, not one vague "Owner decision":
  - **Squash-Merge PRs** (e.g. #1199): develop-HEAD after merge ≠ PR head; the post-run workflow_run.head_sha
    is the squash SHA, the PR head `96a96362` is frozen on `refs/pull/1199/head`. Under strict policy the
    receipt on the old head is stale the moment develop advances; a fresh push → fresh attempt-1 CI → fresh
    receipt → fresh Owner dispatch. This is exactly v1's stated cost; the o215 data *confirms* squash is the
    live merge method, so the cost is real and applies to every Squash-Merge PR.
  - **Merge-commit / normal PRs**: `refs/pull/N/head` persists after merge (finding 2), so the head SHA the
    receipt binds does not detach from a rewritten ref; the only staleness trigger remains a new head commit
    before merge. The merge-commit workflow_run.head_sha does not bind the merge-gate check (that stays on
    the PR head), so the merge-commit semantics only affect the **candidate artifact binding** (which reads
    `head_sha` from the artifact + workflow_run, both = merge commit) — it does NOT move the evaluated commit.
  - **Correction to gap 5 resolution:** keep `strict=true` (baseline, current semantics, confirmed live). The
    alternative (strict=false + gate re-verifying base ancestry) still needs a base-integration proof and
    stays an unresolved decision — but the o215 data removes the "merge refs rewritten" worry as a *separate*
    argument: with `delete_branch_on_merge=null` the head ref does not detach, so the only real cost is the
    post-squash develop-advance staleness, which is intrinsic to squash+strict and is the Owner's to accept.

### A4. Minor correction — legacy producer run_id / attempt provenance

- **v1 claim (§1, line 71):** annotations carry "producer run id + attempt".
- **o215 correction (findings 1–3):** producer run id = the CI · Source & Quality run id
  (`workflow_id 352609139`, the CI producer); attempt = `run_attempt` from the producer's own run context
  (post-run hard refuses `run_attempt != 1`, so attempt is always 1 at publish; o215 finding 6). The
  post-run run id (`workflow_id 397459764`) is a **downstream** id carried in `external_id` for the post-run
  witness, not the producer id. Both ids belong in annotations, correctly labelled.

## §B. Exact first real chain-run sequence after #1206 + #1205 merges

Precondition (from v1 §5 gap 3, still open, gate before this sequence): `receipt-post-run.yml` publish
must be green for a sustained window (the two 2026-10-29 failures 40834168626 / 40811856878 must be
resolved) and the CI-only default-branch registration (TRUSTED_SOURCE populated, all pins at the final
integrated reviewed head) must be merged + dispatched clean. This sequence documents the **order and the
exact live ids**, not a green-run guarantee.

Live ids (from o215 findings + v1 §0):
- Producer workflow id `352609139` ("CI · Source & Quality", ci.yml, the `pull_request`/`push` producer
  emitting the trusted-pr-plan artifact and the legacy `PR Selected Checks`).
- Post-run workflow id `397459764` ("Receipt · Post-Run Writer", `on.workflow_run` of the producer,
  `run_attempt == 1` gate, publishes UNAPPROVED receipt to Planning).
- Approval chain controller pin `e13f1570550f4b6b09f3727728293d91afbebf94`; shadow reusable-workflow pin
  `f57b30ed48f19e62452ab793801a02ccd2658414`; final-check pin `b53632aa` (rv1206); controller pin
  `dd8fb61d614b59252c9d29121380b5893d006828`.

Sequence (each step keyed to the exact object that triggers it):

1. **#1205 and #1206 merge to develop** (Squash or merge-commit per the repo default
   `delete_branch_on_merge=null`, `allow_auto_merge=false`; see o215 finding 2). develop advances to the
   merge/squash SHA.
2. **Producer run 352609139 fires** on the develop-push (event=push, `workflow_run.head_sha` = the new
   develop merge/squash commit, `run_attempt=1`). It uploads the trusted-pr-plan artifact (pr_number +
   candidate/base/head) and runs the legacy `PR Selected Checks`. This is the only run whose artifact the
   rest of the chain consumes.
3. **Post-run run 397459764 fires** `on.workflow_run` of 352609139 **success** with `run_attempt == 1`.
   It reads `github.event.workflow_run.id` (= 397459764), downloads the trusted-pr-plan artifact
   (`gh api …/runs/<397459764>/artifacts`), resolves candidate/base/head **from pr-plan.json**, and runs
   `receipt_writer.py --publish` using `PLANNING_RECEIPT_WRITE_TOKEN` (must exist — o215 finding 3a: repo
   vars currently 0, so Owner must provision this secret before the chain is green). Publishes an
   UNAPPROVED receipt to Planning with `external_id="<candidate>:<publication>"` and the merge-commit
   `workflow_run.head_sha` in the annotations.
4. **Owner dispatches** `receipt-approval.yml` `workflow_dispatch` on the exact PR (`PR_NUMBER` from the
   artifact). `receipt_verifier.resolve_pull` resolves the live PR head → new `head` output (40-hex,
   fail-closed). The approve step runs live verification (`live()`), publishes a durable approved receipt,
   and emits `receipt/plan/candidate/publication/head` outputs. (Dormancy: `TRUSTED_SOURCE` must be
   populated at registration, else fail-closed — v1 §5 gap 2.)
5. **Shadow run** `receipt-shadow.yml@f57b30ed` executes job "PR · Receipt Shadow Consumption" at the exact
   publication commit (`b53632aa` final-check pin), running the offline retained verify (`retained()`),
   fail-closed on `wrong candidate SHA` / `plan candidate mismatch`.
6. **`gate` job** (`needs: [approve, shadow]`, `if: always()`) runs. It reads the **artifact** `candidate`
   + the live-approved `head`, asserts all four approve outputs present/well-formed (condition c), asserts
   live head == approved head and base develop-ancestry is current (condition d), asserts dispatched
   `pr_number` matches (condition e), and `needs.approve.result == success` (a) + `needs.shadow.result ==
   success` (b). On ALL: creates `POST /repos/mcpdev80/baseharbor/check-runs` with
   `name="Receipt · Candidate Completion"`, `head_sha=<live PR head>`, `status=completed`,
   `conclusion=success`, `external_id="<candidate>:<publication>"`, `details_url=<content-addressed
   publication blob>`, and per-fact annotations (receipt path, plan revision, exact integration SHA,
   durable publication commit, producer run 352609139 + attempt, post-run run 397459764, verdict rule).
   On any fail: `conclusion=failure` with the machine-checkable reason line from v1 §2.

Idempotence/rerun keyed by `(name, head_sha)` (v1 §1 lines 90–91): after a head move the new head gets a
fresh check run; the old head's check goes stale naturally. A post-merge merge-commit run_head does not
bind the gate check (that stays on the PR head) — the merge-commit sha only feeds the artifact binding
(A2).

## §C. Evidence that MUST sit at the end of the evidence file for legal activation + Ready-sperre-off

Before the maintainer runs the §3/§25223521 PUT (activation) and before the Ready card can be taken off
sperre, the evidence file must contain, each with its provenance command, all of the following. This is
the concrete replacement for v1's "activation belongs to the maintainer" hand-off:

1. **Chain-run proof (binding):** the accepted automatic skeleton's real first run — the producer run id
   `352609139`, the post-run run id `397459764` with `run_attempt == 1`, the trusted-pr-plan artifact
   download (pr_number + candidate/base/head), the UNAPPROVED receipt publication to Planning, the
   Owner approval dispatch, the retained shadow verify, and the `gate` check run `Receipt · Candidate
   Completion` on `external_id="<candidate>:<publication>"` — captured with commit-SHA, task-id, run-id,
   gate result, and the reviewer/Owner verdict. Artifact: `evidence/board-2026-10-29/scripts/chain-run.sh`
   (o216 §5).
2. **Exact-candidate proof:** `receipt.sha == plan.candidate_sha == producer run head_sha` live AND offline
   `retained()` at the publication revision, with the integration SHA resolving via
   `receipt_verifier.extract_facts` (`candidate_sha = integration_sha`). This closes A2/A1: the merge-commit
   workflow_run.head_sha and the artifact candidate must agree with the receipt.
3. **Three negative proofs:** each of the three bounded offline cases in `negative-proofs.sh` invoked in
   `retained` mode, asserting closed-fail on the isolated variable (candidate-mismatch, plan-mismatch,
   wrong head). Artifact: `evidence/board-2026-10-29/scripts/negative-proofs.sh` (o216 §5).
4. **Ruleset binding proof (Ready-sperre-off):** `gh api repos/mcpdev80/baseharbor/rulesets/25223521`
   live with `enforcement: "active"`, `required_status_checks` containing exactly
   `{"context": "Receipt · Candidate Completion", "integration_id": 15368}`, strict `true`,
   `do_not_enforce_on_create: false`, `bypass_actors: []`, `current_user_can_bypass: never` — i.e. the
   o216 §2 activation block with the context swapped to the new receipt context and legacy `PR Selected
   Checks` removed. Plus `gh pr checks <one merged develop PR>` showing the new context present and the
   legacy one absent, so the Ready card's merge-gate is demonstrably satisfied by the exact candidate.
5. **Rollback snapshot proof:** the stored pre-/post-cutover ruleset bodies (v1 §3/§4) both present, and a
   post-activation diff against §1 live JSON confirming no other field drifted (bypass_actors, strict,
   do_not_enforce_on_create carried verbatim).

Until (1)–(4) are present with their provenance commands and a written Owner/Reviewer verdict, the
activation PUT and the Ready-sperre-off are not legal — this evidence file is where that requirement is
now written down, not merely implied.

## repo-rule compliance

- Evidence-only correction round. No `gh api` write, no product write, no Planning write, no
  `workflow_dispatch`, no git anywhere in baseharbor-ecosystem. This file is the only write of lane o218.
- Every corrected statement (§A) cites the o215 finding + payload line that disproves the v1 claim; every
  live id (§B) cites its source (v1 §0 / o215). Point-in-time values (SHAs, run ids, enforcement states)
  are 2026-10-29 reads and must be re-read live before the cutover implementation task starts.
- No secrets, tokens, or credentials appear in this document.

END o218-DONE
