# w92 / card 0428-282 — demo consent recognizer for doubly-nested candidate refusal

Lane: w92-0428-282-democonsent
Repo: mcpdev80/baseharbor-demo
Mission: /home/marcel/dev/baseharbor-ecosystem/coordinator/missions/w92-0428-282-democonsent.txt
Card: t-20261125-0428-282-demo-consent-recognizer-nested (0428-282, bug, release v0.4.28)
Status: active

## PLAN

1. DONE. Create numbered work plan in all three places.
   - Native `todowrite`: NOT EXPOSED in this session; leg (0) skipped per dispatch wording ("if unsure, skip leg (0) entirely"). Board file (a) and this list (b) written.
   - Board file: /home/marcel/dev/baseharbor-ecosystem/workers/todos/w92-0428-282-democonsent.json
2. IN PROGRESS. `git remote -v` as first git action; only URLs containing github.com/mcpdev80 used.
3. TODO. Pull FULL ci-operator.log/artifact from run 45398943139 for the exact doubly-nested refusal string and the emitted digest; resolve stale-vs-current.
4. TODO. Claim 0428-282 via scripts/plan.py claim + push; verify owner published.
5. TODO. Cut ONE branch off demo develop from an attested SHA (ancestor witness).
6. TODO. Fix tests/fixture-consent.py recognizer for doubly-nested refusal + extract digest + retry once.
7. TODO. Add regression test asserting nested recognized + fail-closed on stale/absent.
8. TODO. Wire test into GitHub CI covering its path; keep PR draft.
9. TODO. Open draft PR against demo develop; monitor exact-head required checks to terminal green.
10. TODO. After green + required reviews: merge demo consent PR (owner-authorized); record merge SHA + witness.
11. TODO. Bring down demo compose (docker ps -a before/after); publish evidence to planning origin/main.
12. TODO. Post END_DONE with PR number, head SHA, diff, run id + outcome, merge status, merge SHA + witness.

## environment witnesses

`git remote -v` in the demo checkout (resolve to github.com/mcpdev80 FIRST):

    origin	https://github.com/mcpdev80/baseharbor-demo.git (fetch)
    origin	https://github.com/mcpdev80/baseharbor-demo.git (push)

All resolve to github.com/mcpdev80; no filesystem remote in play. NOTE: the demo checkout's own HEAD is a foreign lane branch (`lane-0428-279-mcpcontract-fix`, `025ce84`); I will NOT touch it — I cut a dedicated worktree off demo develop for this lane.

Remote truth for demo develop, measured with ls-remote (base attestation):

    c23bd9ac58919302ffad3a43f43afb1a34bfbc96	refs/heads/develop  <-- branch cut here
    df4867c7540774eba8b8811cb64946b4adc0c8ab	refs/heads/main

gh auth: account mcpdev80, active, git protocol ssh.

## diagnosis

Per mission + w85 diagnosis (evidence/r28-welle6-2026-11-25/0428-281-consent/diagnosis.md):

- baseharbor-demo tests/fixture-consent.py:38-53 recognizes candidate-consent refusals by an exact allow-list, but the REAL refusal from baha up is DOUBLY nested: app_apply.go:204 wraps ("record deployment before mutation: %w") an inner error whose message already contains "; refusing to record deployment state", producing a string outside the accepted set.
- The recognizer raises and never extracts the 64-hex digest from error['next'], so run_consented never re-invokes with --confirm-candidate -> the v0.4.28 Docker Light gates fail closed.
- Product path is CORRECT (#1807 merged, 7b45db92, ancestor of develop 46d3dccc). NO baseharbor product change warranted. Write-set is ONLY baseharbor-demo tests/fixture-consent.py + its regression test.

### FINDING — CONFLICT WITH CARD PREMISE (blocks implementation)

I could NOT proceed to edit because the card's premise is contradicted by current source:

1. The exact doubly-nested refusal string the product emits (verified in baseharbor develop `46d3dccc` at `cmd/baha/deployment_record.go:369-371` and `cmd/baha/app_candidate_consent.go:160`, wrapped by `cmd/baha/app_apply.go:204`) is:
   ```
   record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state
   ```
   i.e. `wrapped_message + ": " + direct_message` = the fixture's `nested_wrapped_message`.

2. The demo develop HEAD (`c23bd9ac58919302ffad3a43f43afb1a34bfbc96`, base of THIS card's requested branch) ALREADY contains the full fix in `tests/fixture-consent.py`:
   - `nested_wrapped_message` recognized (line matching the exact doubly-nested product string).
   - digest extracted via `[0-9a-f]{64}` regex.
   - fail-closed / stale-rejection preserved (unchanged).
   - the file was created fresh at `c23bd9a` (PR #169, merged 2026-11-22) — before the failing run.

3. The EXACT demo_ref used by the failing run 45398943139 (`demo_ref: f23b6e09be34601ba542a3087e19b80764a4165d`, merge of PR #163, 2026-11-16) ALREADY contains `nested_wrapped_message` in its `tests/fixture-consent.py`. So the fixture that fed the "failing" gates was already the fixed version.

4. The regression test `tests/test_fixture_consent.py` at develop HEAD `c23bd9a` ALREADY asserts the nested form (line 242: `nested["error"]["message"] = "record deployment before mutation: " + direct + ": " + direct`) plus fail-closed/digest-exactness (lines 234-267).

CONSEQUENCE: the write-set the card asks me to create ("recognizer matches doubly-nested + extract digest + retry once + regression test") is ALREADY present and merged on demo develop. There is no unfixed gap in the two files. Opening the card's PR against demo develop would therefore be an empty diff. This is exactly the kind of "product path already correct" situation that w85 flagged and the card's own acceptance implies must be reconciled with the owner before editing.

I did NOT edit either file, did NOT cut a branch, did NOT open a PR. Standing by for an owner scope decision (see QUESTION line posted to coordinator).

## CLEANLINESS

Session host (pid unknown at this turn): `docker ps -a -q` → `0` containers. No container, compose
project, network or volume was started by this lane. No local product test executed (Hosted-only
rule respected: only git, gh read-only queries, curl against the GitHub API, and a read-only
shallow clone under /tmp/opencode/w92-0428-282-democonsent/). No demo compose project was launched
(Hosted-only: no containers on the coordinator host).

Scratch zone: /tmp/opencode/w92-0428-282-democonsent/ (a blob-only clone of baseharbor-demo at
demo develop HEAD c23bd9ac, used for read-only inspection only).

## repo-rule compliance (so far)

- Hosted-only: zero local test execution on the coordinator host. Compliant.
- Workflow scope: no .github/** edits; no reruns or workflow_dispatch. Compliant.
- One candidate per chain / no product branch: no branch cut, no PR opened (pending scope decision).
- No subagents (AGENTS 4.8). Compliant.
- Evidence lives only in baseharbor-plan under evidence/; nothing added to a product repo. Compliant.
- Write-set untouched: neither baseharbor-demo file was modified. Compliant.
- Reality witnesses taken only via git ls-remote / gh API. Compliant.

## BLOCK STATUS

Lane is BLOCKED pending an Owner scope decision (QUESTION posted to coordinator, ticket
00d66002). Rationale: the card's write-set (demo tests/fixture-consent.py double-nested recognizer +
digest extraction + regression test) is ALREADY MERGED on demo develop HEAD c23bd9a (PR #169,
2026-11-22) and was ALREADY present in the exact demo_ref f23b6e09 that fed failing run
45398943139 (2026-11-24T13:00Z). Opening the card's PR against demo develop is therefore an empty
diff. No branch cut, no PR, no product edit, no local test. See ## diagnosis FINDINGS for the full
witness set.

## repo-rule compliance

- Hosted-only: zero local test execution on the coordinator host. Compliant (to verify).
- Workflow scope: no .github/** edits (Owner scope); no reruns or workflow_dispatch. Compliant.
- One candidate per chain: ONE branch off demo develop, ONE PR. Compliant (to verify).
- No subagents (AGENTS 4.8). Compliant.
- Evidence lives only in baseharbor-plan under evidence/; nothing added to a product repo. Compliant.
- Write-set ONLY: baseharbor-demo tests/fixture-consent.py + regression test. No product change, no other repo, no demo PR #171/#1826/#1812 contact. Compliant.

## evidence-on-origin proof

TODO — paste planning-repo push-remote guard, ls-tree grep output, ls-remote main witness before END.

## END

TODO — filled as final action.
