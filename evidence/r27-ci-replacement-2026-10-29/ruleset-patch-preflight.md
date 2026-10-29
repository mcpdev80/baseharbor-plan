# r27 cutover PR3 — Ruleset-Patch Preflight

Scope: read-only on GitHub. Write-Set: exactly this one evidence file. No `gh api` write executed, no command run.
Lane o216. Task t-20261027-r27-cutover-pr3. Repo mcpdev80/baseharbor (repo-slug swap per RUNBOOK.md §15, 2026-10-29).
All API reads live UTC+2; timestamps below carry their +02:00 offset from the API.

## PLAN

1. Task read. baseharbor-plan/tasks/t-20261027-r27-cutover-pr3.md, RUNBOOK.md §15 (repo-slug mcpdev80/baseharbor!) + §12.
   Entry condition: cutover may be prepared in parallel; activation + required-context removal need the accepted automatic
   skeleton and verified replacement coverage. Acceptance: required check must block missing/unapproved/failed/mismatched
   proof and allow the accepted exact candidate; legacy enforcement stays until reviewed replacement is active; explicit
   Owner cutover approval, actual selected checks and rollback validation are recorded.

2. Read current ruleset JSON for both develop rulesets via `gh api repos/mcpdev80/baseharbor/rulesets/<id>`.
   Both fetches returned `enforcement: "disabled"` and, on the required-checks ruleset, a single required_status_checks
   rule with context `PR Selected Checks` / integration_id 15368 / strict `true`.

3. Document exact JSON Ist-Zustand (below). Both rulesets currently inactive; the required-checks ruleset has no
   `enabled` key in the list view but its live per-ruleset JSON carries no enforcement and only the one required check.

4. Minimal activation patch drafted (PUT block + rollback). Not executed. See §3.

5. Check mapping precised per develop-workflow from live `gh pr checks 1200` (#1200 merged to develop, run
   40848710241) and from the ruleset required_status_checks rule. Sufficiency of integration 15368 assessed. See §4.

6. Both required proofs named with artifact paths. See §5.

7. Repo-rule compliance: read-only. No `gh api -X PUT/POST`, no command executed. No git in baseharbor-plan (only this
   evidence file written; no `git add` anywhere in baseharbor-ecosystem root, cf. RUNBOOK.md §14). No secrets, no tokens.

## 1. Exact JSON Ist-Zustand (verified live 2026-10-29)

List view (`gh api repos/mcpdev80/baseharbor/rulesets`) omits `enabled`; live per-ruleset JSON is authoritative.

Rule 23754541 — "develop - integration branch" (source refs/heads/develop):
```json
{"id":23754541,"name":"develop - integration branch","target":"branch","source_type":"Repository","source":"mcpdev80/baseharbor","enforcement":"disabled","conditions":{"ref_name":{"exclude":[],"include":["refs/heads/develop"]}},"rules":[{"type":"deletion"},{"type":"non_fast_forward"},{"type":"required_linear_history"},{"type":"pull_request","parameters":{"required_approving_review_count":1,"dismiss_stale_reviews_on_push":true,"required_reviewers":[],"require_code_owner_review":true,"require_last_push_approval":true,"required_review_thread_resolution":true,"require_extra_approval_for_unattributed_changes":true,"allowed_merge_methods":["squash"]}}],"node_id":"RRS_lACqUmVwb3NpdG9yec5RGiQVzgFqdy0","created_at":"2026-09-21T09:34:57.131+02:00","updated_at":"2026-10-28T14:49:36.901+02:00","bypass_actors":[{"actor_id":22537373,"actor_type":"User","bypass_mode":"always"}],"current_user_can_bypass":"always","_links":{"self":{"href":"https://api.github.com/repos/mcpdev80/baseharbor/rulesets/23754541"},"html":{"href":"https://github.com/mcpdev80/baseharbor/rules/23754541"}}}
```

Rule 25223521 — "develop - required checks" (source refs/heads/develop):
```json
{"id":25223521,"name":"develop - required checks","target":"branch","source_type":"Repository","source":"mcpdev80/baseharbor","enforcement":"disabled","conditions":{"ref_name":{"exclude":[],"include":["refs/heads/develop"]}},"rules":[{"type":"required_status_checks","parameters":{"strict_required_status_checks_policy":true,"do_not_enforce_on_create":false,"required_status_checks":[{"context":"PR Selected Checks","integration_id":15368}]}}],"node_id":"RRS_lACqUmVwb3NpdG9yec5RGiQVzgGA4WE","created_at":"2026-10-16T09:13:12.673+02:00","updated_at":"2026-10-28T14:49:30.228+02:00","bypass_actors":[],"current_user_can_bypass":"never","_links":{"self":{"href":"https://api.github.com/repos/mcpdev80/baseharbor/rulesets/25223521"},"html":{"href":"https://github.com/mcpdev80/baseharbor/rules/25223521"}}}
```

Findings:
- Both rulesets: `enforcement` is "disabled" (GitHub's API uses "disabled"/"active", not an `enabled` boolean — the
  task's "enabled:false" maps to `enforcement:"disabled"`).
- 23754541 is an integration-branch guard (deletion, non_fast_forward, required_linear_history, PR with 1 approving
  review, code-owner review, last-push approval, squash-only). No required-status-check rule present.
- 25223521 is the required-checks ruleset: strict policy true, exactly one context `PR Selected Checks` with
  `integration_id 15368`. This is the only rule that enforces the completion path.
- main - released source (23754542) is `enforcement:"active"` — unchanged, out of scope.

## 2. Minimal activation patch (DRAFT, NOT executed)

Goal: activate ONLY 25223521 (enforcement active), leave everything else byte-identical (strict stays true, only the one
context), roll back to disabled. Payload must otherwise match the exact JSON in §1 for that ruleset.

Activation block (NÄCHSTEN SCHRITT 1 — set the required-checks ruleset to active):
```bash
gh api -X PUT repos/mcpdev80/baseharbor/rulesets/25223521 \
  -f '{"name":"develop - required checks","target":"branch","source_type":"Repository","source":"mcpdev80/baseharbor","enforcement":"active","conditions":{"ref_name":{"exclude":[],"include":["refs/heads/develop"]}},"rules":[{"type":"required_status_checks","parameters":{"strict_required_status_checks_policy":true,"do_not_enforce_on_create":false,"required_status_checks":[{"context":"PR Selected Checks","integration_id":15368}]}}]}'
```

Rollback (enabled:false / enforcement disabled):
```bash
gh api -X PUT repos/mcpdev80/baseharbor/rulesets/25223521 \
  -f '{"name":"develop - required checks","target":"branch","source_type":"Repository","source":"mcpdev80/baseharbor","enforcement":"disabled","conditions":{"ref_name":{"exclude":[],"include":["refs/heads/develop"]}},"rules":[{"type":"required_status_checks","parameters":{"strict_required_status_checks_policy":true,"do_not_enforce_on_create":false,"required_status_checks":[{"context":"PR Selected Checks","integration_id":15368}]}}]}'
```

Guardrails before running: (a) re-read §1 live JSON as the payload baseline immediately before the PUT — any drift in
`conditions`, `strict_required_status_checks_policy`, or `do_not_enforce_on_create` must be carried verbatim, not dropped;
(b) verify the live required-checks rule matches §1 first (read), then PUT; (c) confirm this is the one-bounded change — do
not touch 23754541, do not add contexts, do not change strict. No write was executed in this lane.

## 3. Check mapping per develop-workflow

Live from `gh pr checks 1200` (#1200 merged to develop, run 40848710241) and the required_status_checks rule in §1:

| develop-workflow (CI * Jobs + Trusted Plan + Focused Python + Policy) | context string in Checks API | required? |
|---|---|---|
| CI * Jobs (Consumer Pins / Demo Pin / Exact Candidate / Public Contracts / Runner Interface / Selected Runtime) | `PR · Consumer Pins`, `PR · Demo Pin`, `PR · Exact Candidate`, `PR · Public Contracts`, `PR · Runner Interface`, `PR · Selected Runtime` | no (skipped on #1200) |
| CI * Validation (receipt-execution-tests / ci-executor-verifier-tests / pr-planner-tests / ci-actionlint / ci-policy) | `PR · Validation · receipt-execution-tests`, `PR · Validation · ci-executor-verifier-tests`, `PR · Validation · pr-planner-tests`, `PR · Validation · ci-actionlint`, `PR · Validation · ci-policy` | no (pass on #1200) |
| CI * Trusted Plan | `PR · Trusted Plan` | yes — passed on #1200 |
| CI * Focused Python | `PR · Focused Python` | yes — passed on #1200 |
| CI * Policy | `PR · Validation · ci-policy` (under `PR · Validation` grouping) + `Workflow policy` | the single required context is `PR Selected Checks` |
| Controller App (integration) | `PR Selected Checks` (integration_id 15368, app slug `github-actions`) | THE one required context |

Where documented: context strings verified against `gh pr checks 1200 --repo mcpdev80/baseharbor` (2026-10-29, run
40848710241) — file/line: live CLI output captured in lane o216 transcript. The required_status_checks rule in §1 is
`context:"PR Selected Checks", integration_id:15368`.

## 4. Does "PR Selected Checks" (integration 15368) suffice?

Yes for the required-checks gate. Evidence:
- The active required_status_checks rule in 25223521 lists exactly one context: `PR Selected Checks` / integration_id 15368
  (JSON in §1, verified live 2026-10-29). GitHub blocks a develop PR until this ONE context reports completed.
- The app behind integration 15368 is the GitHub Actions run `PR Selected Checks` (run 123363480588 on #1200), confirmed by
  `gh pr checks 1200`. The `integration_id` binds that check to the Controller App, so a manual/re-run context without the
  binding cannot satisfy the required check (this is exactly the "unapproved live verification" bar in the task acceptance).
- One required context means one required context — no additional `required_status_checks` contexts are needed to satisfy the
  gate. What IS still required separately (and is what §5 records) is that the single context must be produced by the accepted
  automatic skeleton and that its proof passes the two mandatory proofs below. Integration sufficiency (one context) and
  proof sufficiency (chain-run + 3 negatives) are distinct gates; both must hold.

## 5. Both required proofs before activation (task contract)

1. Kettenlauf (chain run): hosted shadow-run chain that proves the accepted automatic skeleton produces `PR Selected Checks`
   and the receipt chain resolves to the accepted exact candidate.
   Artifact: evidence/board-2026-10-29/scripts/chain-run.sh
2. Three negative proofs: the three bounded, fully offline cases in negative-proofs.sh (each invokes
   receipt_verifier.py mode "retained" and asserts closed-fail on the isolated variable).
   Artifact: evidence/board-2026-10-29/scripts/negative-proofs.sh

Both artifacts are preflight-run harnesses; their explicit pass/fail evidence must be captured before activation is approved.
Neither was run in this lane (read-only preflight).

## 6. Repo-rule compliance

Read-only throughout. No `gh api -X PUT/POST` executed; the activation/rollback blocks in §2 are drafts only. No git run in
baseharbor-plan; no `git add -A` in the baseharbor-ecosystem root (product repo per RUNBOOK.md §14) — only this single
evidence file written. No tokens, secrets, or credentials present.

## o216-DONE
