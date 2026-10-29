# Inventory Correction + PR Freshness Audit — o206

**Task:** r27 inventory correction + PR freshness audit (supports t-20261029-r27-ci-coverage-inventory + cutover)
**Lane:** o206 (ornith)
**Repo:** mcpdev80/baseharbor (base state), baseharbor-plan (this evidence file only)
**Date:** 2026-10-29
**Mode:** READ-ONLY everywhere except this evidence file. No git push/commit/merge performed.

## PLAN

1. PLAN 0: Track r27 inventory correction + PR freshness audit — DONE
2. PLAN 1: Read task note evidence/board-2026-10-29/prompts/o206.txt — DONE
3. PLAN 2: Re-query all three rulesets via the correct embedded-rules endpoint (GET /repos/mcpdev80/baseharbor/rulesets/{id}) — DONE
4. PLAN 3: Spot-check inventory sections 2-6 against live state (workflow files, PR Selected Checks producer, receipt-approval.yml TRUSTED_SOURCE, runners) — DONE
5. PLAN 4: Fetch origin, check #1200 and #1201 base drift vs origin/develop, then gh pr checks at current heads — DONE
6. PLAN 5: Compose inventory-correction.md with raw JSON quotes, corrections, and PR freshness verdict — DONE

## PART A — Rulesets re-verified with the correct endpoint

The inventory §1 claimed "All three rulesets return HTTP 404 for /rules endpoints ... contain zero rules ... empty shells." That conclusion is WRONG. The `/rules` sub-endpoint does not exist; rules are embedded in the ruleset object returned by `GET /repos/mcpdev80/baseharbor/rulesets/{id}`. The raw responses below are quoted verbatim from that endpoint.

### Ruleset 23754541 — "develop - integration branch" (target: branch, enforcement: disabled)

```json
{
  "_links": {
    "html": {"href": "https://github.com/mcpdev80/baseharbor/rules/23754541"},
    "self": {"href": "https://api.github.com/repos/mcpdev80/baseharbor/rulesets/23754541"}
  },
  "bypass_actors": [{"actor_id": 22537373, "actor_type": "User", "bypass_mode": "always"}],
  "conditions": {"ref_name": {"exclude": [], "include": ["refs/heads/develop"]}},
  "created_at": "2026-09-21T09:34:57.131+02:00",
  "current_user_can_bypass": "always",
  "enforcement": "disabled",
  "id": 23754541,
  "name": "develop - integration branch",
  "node_id": "RRS_lACqUmVwb3NpdG9yec5RGiQVzgFqdy0",
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {"type": "required_linear_history"},
    {
      "parameters": {
        "allowed_merge_methods": ["squash"],
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": true,
        "require_extra_approval_for_unattributed_changes": true,
        "require_last_push_approval": true,
        "required_approving_review_count": 1,
        "required_review_thread_resolution": true,
        "required_reviewers": []
      },
      "type": "pull_request"
    }
  ],
  "source": "mcpdev80/baseharbor",
  "source_type": "Repository",
  "target": "branch",
  "updated_at": "2026-10-28T14:49:36.901+01:00"
}
```

Rules present: `deletion`, `non_fast_forward`, `required_linear_history`, and a `pull_request` rule (squash-only, code-owner review required, 1 approving review, last-push approval, thread resolution, extra approval for unattributed changes). Enforcement: **disabled** (metadata object with real branch-protection + PR rules; not enforced on develop).

### Ruleset 25223521 — "develop - required checks" (target: branch, enforcement: disabled)

```json
{
  "_links": {
    "html": {"href": "https://github.com/mcpdev80/baseharbor/rules/25223521"},
    "self": {"href": "https://api.github.com/repos/mcpdev80/baseharbor/rulesets/25223521"}
  },
  "bypass_actors": [],
  "conditions": {"ref_name": {"exclude": [], "include": ["refs/heads/develop"]}},
  "created_at": "2026-10-16T09:13:12.673+02:00",
  "current_user_can_bypass": "never",
  "enforcement": "disabled",
  "id": 25223521,
  "name": "develop - required checks",
  "node_id": "RRS_lACqUmVwb3NpdG9yec5RGiQVzgGA4WE",
  "rules": [
    {
      "parameters": {
        "do_not_enforce_on_create": false,
        "required_status_checks": [{"context": "PR Selected Checks", "integration_id": 15368}],
        "strict_required_status_checks_policy": true
      },
      "type": "required_status_checks"
    }
  ],
  "source": "mcpdev80/baseharbor",
  "source_type": "Repository",
  "target": "branch",
  "updated_at": "2026-10-28T14:49:30.228+01:00"
}
```

Rules present: a single `required_status_checks` rule requiring context **"PR Selected Checks"** with **`integration_id: 15368`** (the receipt-approval integration) and strict policy. Enforcement: **disabled** (rule exists but is not yet enforced on develop — this is the intended pre-registration state; enforcement is flipped at final cutover).

### Ruleset 23754542 — "main - released source" (target: branch, enforcement: active)

```json
{
  "_links": {
    "html": {"href": "https://github.com/mcpdev80/baseharbor/rules/23754542"},
    "self": {"href": "https://api.github.com/repos/mcpdev80/baseharbor/rulesets/23754542"}
  },
  "bypass_actors": [],
  "conditions": {"ref_name": {"exclude": [], "include": ["refs/heads/main"]}},
  "created_at": "2026-09-21T09:34:57.599+02:00",
  "current_user_can_bypass": "never",
  "enforcement": "active",
  "id": 23754542,
  "name": "main - released source",
  "node_id": "RRS_lACqUmVwb3NpdG9yec5RGiQVzgFqdy4",
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {"type": "required_linear_history"},
    {
      "parameters": {
        "allowed_merge_methods": ["squash"],
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_extra_approval_for_unattributed_changes": true,
        "require_last_push_approval": false,
        "required_approving_review_count": 0,
        "required_review_thread_resolution": true,
        "required_reviewers": []
      },
      "type": "pull_request"
    }
  ],
  "source": "mcpdev80/baseharbor",
  "source_type": "Repository",
  "target": "branch",
  "updated_at": "2026-09-21T09:34:57.638+01:00"
}
```

Rules present: `deletion`, `non_fast_forward`, `required_linear_history`, and a `pull_request` rule (squash-only, extra approval for unattributed changes, thread resolution, 0 required approvers). Enforcement: **active**.

### Ruleset verdict (corrects inventory §1)

The three rulesets are NOT empty shells. Each carries real rules embedded in the object:

| ID | Name | Enforcement | Rules that actually exist |
|----|------|-------------|---------------------------|
| 23754541 | develop - integration branch | disabled | deletion, non_fast_forward, required_linear_history, pull_request (squash, code-owner review, 1 approver, last-push approval, thread resolution, unattributed extra approval) |
| 25223521 | develop - required checks | disabled | required_status_checks: **"PR Selected Checks"** (integration_id 15368), strict policy |
| 23754542 | main - released source | active | deletion, non_fast_forward, required_linear_history, pull_request (squash, unattributed extra approval, thread resolution, 0 approvers) |

Key corrections vs inventory §1:
- "Return HTTP 404 for /rules endpoints ... zero rules" is FALSE. There is no `/rules` sub-endpoint; `GET /repos/mcpdev80/baseharbor/rulesets/{id}` returns the full rule list inline (raw JSON above).
- The required-status-check rule **does exist**: context `PR Selected Checks`, integration_id `15368`, strict policy (ruleset 25223521). The "required checks" are enforced via this ruleset rule (when enforcement is flipped active), not purely "at the workflow level".
- The only accurate claim in §1 was `enforcement: disabled` on the two develop rulesets. That is a real pre-registration state: the rules are written and correct, they are simply not yet enforcing on develop. main ruleset 23754542 is `active` and is enforcing.
- `integration_id: 15368` is referenced but the separate `GET /repos/mcpdev80/baseharbor/integrations/15368` endpoint returned 404 in this read-only pass — the id is valid in the required_status_checks rule; its external identity endpoint is not publicly queryable under the current token scope.

## PART A — Spot-check of inventory sections 2-6 vs live state

### Section 2 (Workflow files, 22 total) — CONSISTENT
Live `GET /.github/workflows?ref=origin/develop` returns exactly the 22 workflow files listed in the inventory (artifact-gc, ci, docker-runtime-acceptance, host-trust-owned-e2e, mcp-lifecycle-acceptance, nextjs-greenfield-e2e, observability-acceptance, pages, podman-acceptance, pre-release-runtime-suite, pre-release, receipt-approval, receipt-post-run, receipt-shadow, release, renovate, runtime-broker, runtime-image, runtime-s3-acceptance, supplemental-release-validation, targeted-demo-acceptance, targeted-integration). No file added/removed.

### Section 3 (PR Selected Checks producer) — CORRECT
`PR Selected Checks` is the `pr_selected_final` job (name override) in **ci.yml**, defined at ci.yml:808 (`name: PR Selected Checks`), a `pull_request` job on `ubuntu-latest` with `if: always() && github.event_name == 'pull_request' && github.base_ref == 'develop'`. It runs `scripts/pr-required-final.py` against authenticated results and is the job behind the `PR Selected Checks` required-status-check context in ruleset 25223521. The inventory's mapping of this context to the selected-checks producer is correct.

### Section 3 (receipt-approval.yml TRUSTED_SOURCE) — CURRENT VALUE CONFIRMED + o201 CHANGES IT
Live value on `origin/develop` (7a4debccc4e2fa5e78287e9b9388b0cb521d66e2): `TRUSTED_SOURCE: ''` (empty string, verifier fails closed). This matches the inventory's "pre-registration" framing.

The single commit of PR #1200 (`work/r27-pin-o201`, `5aaa38ec`) changes ONLY `.github/workflows/receipt-approval.yml`:
- `TRUSTED_SOURCE: ''` → `TRUSTED_SOURCE: 'b53632aaaee6067397c27000c229f34736ec2155'` (pins the reviewed receipt-approval/receipt_verifier blobs)
- shadow `uses: .../receipt-shadow.yml@f57b30ed...` → `...@b53632aaaee6067397c27000c229f34736ec2155` (the reviewed receipt-shadow carrying the R27-F6 publication input)

So on develop TRUSTED_SOURCE is empty (inventory correct for develop); o201 pins it to the reviewed b53632aa head. Inventory §7 says PLANNING_RECEIPT_WRITE_TOKEN exists — confirmed in both the inventory and live (used by receipt-approval.yml).

### Section 6 (Runners) — JSON IN INVENTORY UNVERIFIED LIVE; endpoints 404
The inventory §6 JSON (3 self-hosted runners: `baha-k3s-runner-01` id 25 k3s/kubernetes, `baha-runner-docker-2` id 23 docker, `baha-runner-podman-1` id 24 podman; all online, not busy) could NOT be re-verified live. Under the current token scope the runners list endpoint returns 404:
- `gh api repos/mcpdev80/baseharbor/runners` → 404
- `gh api mcpdev80/runners` → 404
- `gh api orgs/mcpdev80/orgs/runners` → 404

The token has scopes `gist, read:org, repo` — the runners list requires `admin:org`/`repo` runner read that is not present. The inventory's runner inventory is plausible and internally consistent with the workflow runner labels cited elsewhere (docker/runtime-acceptance on baha-runner-docker-2, podman on baha-runner-podman-1, k3s on baha-k3s-runner-01) but remains **UNVERIFIED** from this read-only lane. Flagged for a verifier with runner-list scope, not asserted.

## PART B — PR #1200 / #1201 freshness audit

### Base drift vs origin/develop
`git -C baseharbor fetch origin` succeeded. develop HEAD: `7a4debccc4e2fa5e78287e9b9388b0cb521d66e2`.

| PR | Head ref | HEAD SHA | merge-base(origin/develop, head) | develop is ancestor? | Commits ahead of develop |
|----|----------|----------|----------------------------------|----------------------|--------------------------|
| #1200 (work/r27-pin-o201) | origin/work/r27-pin-o201 | `5aaa38ece21c40ad10d2805bf0bc41fac3d695b8` | `7a4debccc4e2fa5e78287e9b9388b0cb521d66e2` | YES (fast-forward) | 1 |
| #1201 (work/r27-postrun-token-o203) | origin/work/r27-postrun-token-o203 | `de2312a06b234cde08943ce0329b83e01bd36fa3` | `7a4debccc4e2fa5e78287e9b9388b0cb521d66e2` | YES (fast-forward) | 1 |

Both PRs target **develop** as base, are **OPEN**, and each is exactly **1 commit ahead** of origin/develop with develop as a true ancestor (clean fast-forward). No local develop drift; both heads are fresh against current develop. Neither branch has diverged or fallen behind.

### gh pr checks at current heads

**#1200 (run 40839765984):**
| Context | Status |
|---------|--------|
| Workflow policy | pass (25s) |
| PR Selected Checks | pass (11s) |
| PR · Focused Python | pass (2m3s) |
| PR · Validation · ci-executor-verifier-tests | pass (15s) |
| PR · Validation · ci-actionlint | pass (20s) |
| PR · Validation · ci-policy | pass (14s) |
| PR · Validation · pr-planner-tests | pass (1m43s) |
| PR · Validation · receipt-execution-tests | pass (32s) |
| PR · Trusted Plan | pass (7s) |
| Release Source Preflight | skipping |
| PR · Consumer Pins | skipping |
| PR · Demo Pin | skipping |
| PR · Exact Candidate | skipping |
| PR · Public Contracts | skipping |
| PR · Runner Interface | skipping |
| PR · Selected Runtime | skipping |
| Targeted HA · docker | skipping |
| Targeted HA · podman | skipping |
| validate | skipping |

**#1201 (run 40842267051):**
| Context | Status |
|---------|--------|
| Workflow policy | pass (27s) |
| PR Selected Checks | pass (11s) |
| PR · Focused Python | pass (2m12s) |
| PR · Validation · ci-policy | pass (15s) |
| PR · Validation · ci-actionlint | pass (22s) |
| PR · Validation · ci-executor-verifier-tests | pass (15s) |
| PR · Validation · pr-planner-tests | pass (1m35s) |
| PR · Validation · receipt-execution-tests | pass (29s) |
| PR · Trusted Plan | pass (7s) |
| Release Source Preflight | skipping |
| PR · Consumer Pins | skipping |
| PR · Demo Pin | skipping |
| PR · Exact Candidate | skipping |
| PR · Public Contracts | skipping |
| PR · Runner Interface | skipping |
| PR · Selected Runtime | skipping |
| Targeted HA · docker | skipping |
| Targeted HA · podman | skipping |
| validate | skipping |

Both heads: all armed required contexts pass, none red. The remaining contexts are `skipping` because they are gated behind runtime-selection/public-contract gates that these CI-only, non-runtime branches do not qualify for — expected, not a defect.

### Verdict: sync-commit or rerun needed AFTER merges?
No sync-commit and no `gh run rerun --failed` needed at present — there is nothing red to rerun, and both heads are already current against develop (clean fast-forwards, 1 commit each).

After the pending merges, a fresh run will be triggered automatically on the merge commit (the workflows fire on `pull_request`/`push`), so:
- **#1200 (receipt-approval.yml only):** the merge re-runs ci.yml + receipt-approval on the merged develop. Because o201 flips `TRUSTED_SOURCE` from `''` to `b53632a...` and repins the receipt-shadow ref, the receipt-approval + receipt-shadow jobs that previously failed-closed on the empty source will now execute against reviewed bytes. If any later commit re-introduces the empty pin or the shadow ref no longer carries the R27-F6 publication input, a `gh run rerun --failed` on the merge run would be the Frischkur (RUNBOOK §8). Currently not required.
- **#1201 (receipt-post-run.yml + test_receipt_postrun.py):** the merge adds `PLANNING_RECEIPT_WRITE_TOKEN` to the publish-step env (root cause 40834168626) plus a test asserting that env key. If the publish step still fails closed post-merge (e.g. a later commit drops the env key again), a `gh run rerun --failed` on the merge run is the correct Frischkur. Currently not required.

Neither action should be performed now. Both remain pending the actual merges and their resulting merge-commit runs.

## Corrections summary
- inventory §1 "empty shells / zero rules / 404 / no rules to enforce" → **FALSE**. All three rulesets carry real embedded rules (raw JSON above). Only the accurate sub-claim holds: the two develop rulesets are `enforcement: disabled` (intended pre-registration state); main 23754542 is `active`.
- required-status-check rule confirmed present: `PR Selected Checks` + `integration_id: 15368` (ruleset 25223521).
- TRUSTED_SOURCE on develop is `''` (inventory correct for develop); o201 pins it to `b53632a...`.
- Runners (§6) JSON: **UNVERIFIED live** (runner-list endpoint 404 under current token scope). Flagged, not asserted.
- #1200/#1201: both fresh (1 fast-forward commit ahead of origin/develop), all required contexts pass, no sync/rerun needed now.

## o206-DONE
