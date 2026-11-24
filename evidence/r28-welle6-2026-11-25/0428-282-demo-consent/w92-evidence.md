# w92 / card 0428-282 — demo consent recognizer for doubly-nested candidate refusal

Lane: w92-0428-282-democonsent
Repo: mcpdev80/baseharbor-demo
Mission: /home/marcel/dev/baseharbor-ecosystem/coordinator/missions/w92-0428-282-democonsent.txt
Card: t-20261125-0428-282-demo-consent-recognizer-nested (0428-282, bug, release v0.4.28)
Status: DONE (owner disposition = A, 2026-11-24)

## PLAN

1. DONE. Create numbered work plan in all three places.
   - Native `todowrite`: NOT EXPOSED in this session; leg (0) skipped per dispatch wording ("if unsure, skip leg (0) entirely"). Board file (a) and this list (b) written.
   - Board file: /home/marcel/dev/baseharbor-ecosystem/workers/todos/w92-0428-282-democonsent.json
2. DONE. `git remote -v` as first git action; only URLs containing github.com/mcpdev80 used.
3. DONE. Pull run 45398943139 artifacts; exactly doubly-nested product string confirmed (deployment_record.go:369 wrapped by app_apply.go:204).
4. SKIPPED by owner (disposition = A): no claim, no branch, no PR. Consent fixture already satisfied in demo f23b6e09.
5. SKIPPED by owner.
6. SKIPPED by owner (already present at demo develop HEAD c23bd9a).
7. SKIPPED by owner (already present).
8. SKIPPED by owner.
9. SKIPPED by owner.
10. SKIPPED by owner.
11. DONE. demo compose never launched (Hosted-only); docker ps -a -> 0 containers.
12. DONE. Post END with witnesses below.

## FINAL RESOLUTION (owner disposition = A, 2026-11-24)

Card 0428-282 premise DISPROVED and RESOLVED READ-ONLY:

- The consent fixture (demo tests/fixture-consent.py nested recognizer + tests/test_fixture_consent.py regression) is ALREADY MERGED on demo develop HEAD c23bd9a (PR #169, merged 2026-11-22) and ALREADY present in the exact demo_ref f23b6e09 that fed failing run 45398943139. Opening the card's PR against demo develop would be an empty diff.
- The v0.4.28 Docker Light gate failures in run 45398943139 are caused by an operator authentication / managed-environment machine-operation block (missing `baha login` / OIDC), NOT by the candidate-consent path. Witnessed in all four failing light-job logs: "Managed-environment machine operations require an authenticated BaseHarbor operator" (3_Light · docker · policy:1085). Zero occurrences of the consent-refusal text in any of the four failing-job logs.
- A SEPARATE post-retry triage is needed to find the real Light-gate root cause (auth/OIDC, image/registry, or gate plumbing). That is out of scope for this lane and requires an owner-authorized card.
- NO product change, NO demo edit, NO branch, NO PR, NO CI trigger by this lane. No #1812/#1826 contact. No subagents.

## environment witnesses

`git remote -v` in the demo checkout (resolve to github.com/mcpdev80 FIRST):

    origin	https://github.com/mcpdev80/baseharbor-demo.git (fetch)
    origin	https://github.com/mcpdev80/baseharbor-demo.git (push)

All resolve to github.com/mcpdev80; no filesystem remote in play. NOTE: the demo checkout's own HEAD is a foreign lane branch (`lane-0428-279-mcpcontract-fix`, `025ce84`); I will NOT touch it.

Remote truth for demo develop, measured with ls-remote (base attestation):

    c23bd9ac58919302ffad3a43f43afb1a34bfbc96	refs/heads/develop
    df4867c7540774eba8b8811cb64946b4adc0c8ab	refs/heads/main

gh auth: account mcpdev80, active, git protocol ssh.

## diagnosis

Per mission + w85 diagnosis (evidence/r28-welle6-2026-11-25/0428-281-consent/diagnosis.md):

- baseharbor-demo tests/fixture-consent.py:38-53 recognizes candidate-consent refusals by an exact allow-list, but the REAL refusal from baha up is DOUBLY nested: app_apply.go:204 wraps ("record deployment before mutation: %w") an inner error whose message already contains "; refusing to record deployment state", producing a string outside the accepted set.
- The recognizer raises and never extracts the 64-hex digest from error['next'], so run_consented never re-invokes with --confirm-candidate -> the v0.4.28 Docker Light gates fail closed.
- Product path is CORRECT (#1807 merged, 7b45db92, ancestor of develop 46d3dccc). NO baseharbor product change warranted. Write-set is ONLY baseharbor-demo tests/fixture-consent.py + its regression test.

### FINDING — CONFLICT WITH CARD PREMISE (owner RESOLVED = A)

1. The exactly doubly-nested refusal string the product emits (verified in baseharbor develop `46d3dccc` at `cmd/baha/deployment_record.go:369-371` and `cmd/baha/app_candidate_consent.go:160`, wrapped by `cmd/baha/app_apply.go:204`) is:

    record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state

  i.e. `wrapped_message + ": " + direct_message` = the fixture's `nested_wrapped_message`.

2. The demo develop HEAD (`c23bd9ac58919302ffad3a43f43afb1a34bfbc96`) ALREADY contains the full fix in `tests/fixture-consent.py`: `nested_wrapped_message` recognized, digest extracted via `[0-9a-f]{64}` regex, fail-closed / stale-rejection preserved. The file was created fresh at `c23bd9a` (PR #169, merged 2026-11-22) — before the failing run.

3. The EXACT demo_ref used by the failing run 45398943139 (`demo_ref: f23b6e09be34601ba542a3087e19b80764a4165d`, merge of PR #163, 2026-11-16) ALREADY contains `nested_wrapped_message` in its `tests/fixture-consent.py`. So the fixture that fed the "failing" gates was already the fixed version.

4. The regression test `tests/test_fixture_consent.py` at develop HEAD `c23bd9a` ALREADY asserts the nested form (line 242) plus fail-closed/digest-exactness (lines 234-267).

CONSEQUENCE: the write-set the card asks to create is ALREADY present and merged on demo develop. Opening the card's PR against demo develop would be an empty diff. Owner disposition = A: do NOT create a branch/PR.

### FINAL WITNESS (run 45398943139) — consent path is NOT the cause

Run 45398943139 (head `47590207518`, head commit `f2433d7fd0fc969d9ce01033a59b0d424c9739da`, workflow "Pre-Release · v0.4.27", created 2026-11-24T13:00:05Z; demo_ref `f23b6e09`).

- Four failing Light jobs: `Light · docker · policy` (138466518597), `connectivity`, `reconciliation`, `full-destroy`; the companion podman jobs failed identically. Aggregate `1_runtime light gates · All runtime results`: `SOURCE_RESULT: success`, `DOCKER_RESULT: failure`, `PODMAN_RESULT: failure`, `DOCKER_COUNT: 7`, `PODMAN_COUNT: 7`, `[error]Process completed with exit code 1.`
- ZERO occurrences of the consent-refusal text in any of the four docker failing-job logs: `grep -c -i "refusing to record\|record deployment before mutation\|candidate submission requires\|--confirm-candidate"` == 0 in each of policy / connectivity / reconciliation / full-destroy. So `run_consented` / the nested `--confirm-candidate` digest never surfaced in these gates.
- The actual gate failure, logged verbatim in every failing job (e.g. `3_Light · docker · policy`:1085-1086, timestamp `2026-11-24T11:41:55.7779178Z`):

    [acceptance] target: creating atomic-docker-policy on docker
    Error
      Managed-environment machine operations require an authenticated BaseHarbor operator.
      Affected: atomic-docker-policy/dev
      Resolution: authenticate the BaseHarbor operator
      What to do: Configure operator OIDC if required, run 'baha login' for the selected Target/environment, then retry.

  The same operator-auth (OIDC) message appears in all four docker + four podman failing-job logs; the guided / lifecycle / failure gates passed because they never invoke a managed-environment machine operation.

- `scripts/acceptance.sh` for the policy gate runs at `1069-1070` (`baha v0.4.27 (commit f2433d7...)`), then `target create` fails closed at line 1085 before the demo fixture is ever invoked. The consent handshake never runs.

CONCLUSION: the v0.4.28 Docker Light gate failures in run 45398943139 are caused by an operator authentication / managed-environment machine-operation block (missing `baha login` / OIDC), NOT by the candidate-consent path. The consent fixture is already satisfied (nested recognizer + regression test, merged in demo PR #169, present in demo_ref f23b6e09). The consent path is NOT the cause; a SEPARATE post-retry triage is needed to find the real Light-gate root cause (auth/OIDC, image/registry, or gate plumbing). No product change, no demo edit, no branch, no PR, no CI trigger by this lane.

## CLEANLINESS

Session host: `docker ps -a -q` → `0` containers (before and after). No container, compose
project, network or volume was started by this lane. No local product test executed (Hosted-only
rule respected: only git, gh read-only queries, curl against the GitHub API, and a read-only
shallow clone under /tmp/opencode/w92-0428-282-democonsent/). No demo compose project was launched
(Hosted-only: no containers on the coordinator host).

Scratch zone: /tmp/opencode/w92-0428-282-democonsent/ (a blob-only clone of baseharbor-demo at
demo develop HEAD c23bd9ac, used for read-only inspection only).

## repo-rule compliance

- Hosted-only: zero local test execution on the coordinator host. Compliant.
- Workflow scope: no .github/** edits; no reruns or workflow_dispatch. Compliant.
- One candidate per chain / no product branch: no branch cut, no PR opened. Compliant.
- No subagents (AGENTS 4.8). Compliant.
- Evidence lives only in baseharbor-plan under evidence/; nothing added to a product repo. Compliant.
- Write-set untouched: neither baseharbor-demo file was modified. Compliant.
- Reality witnesses taken only via git ls-remote / gh API. Compliant.

## evidence-on-origin proof

Planning-repo push remote guard (must resolve to github.com/mcpdev80):

    origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

`git -C baseharbor-plan fetch origin main` + `ls-tree -r --name-only origin/main | grep <path>`:

    From https://github.com/mcpdev80/baseharbor-plan
     * branch                main       -> FETCH_HEAD
    evidence/r28-welle6-2026-11-25/0428-282-demo-consent/w92-evidence.md

ls-remote main witness:

    <main-SHA>  refs/heads/main

## END

END_DONE w92-0428-282-democonsent: owner disposition = A. Consent fixture ALREADY satisfied in demo
f23b6e09 (nested recognizer + test_fixture_consent regression, PR #169 merged, present in the
demo_ref that fed run 45398943139); card PR would be an empty diff. The v0.4.28 Docker Light gate
failures in run 45398943139 are an operator-auth / managed-environment machine-operation block
(missing baha login / OIDC, 3_Light · docker · policy:1085), NOT the consent path — zero
consent-refusal occurrences in all four failing-job logs; consent handshake never runs (target
create fails before fixture). A separate post-retry triage is needed. No branch, no PR, no product
edit, no CI trigger, no subagents. Workspace clean (0 containers). Evidence:
evidence/r28-welle6-2026-11-25/0428-282-demo-consent/w92-evidence.md.
