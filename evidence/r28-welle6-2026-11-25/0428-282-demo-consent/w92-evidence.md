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

## cleanliness

Baseline before any work, on the session host (pid TODO): `docker ps -a -q | wc -l` → TODO.

TODO — fill before END.

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
