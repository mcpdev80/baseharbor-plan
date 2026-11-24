# #1812 prerequisite dependency map (round 1)

Lane: w94-0428-249-1812depcmap (READ-ONLY DESK)
Mission: coordinator/missions/w94-0428-249-1812depcmap.txt
Date: 2026-11-24

## PLAN

- Step 1: Fetch reality SHAs — DONE (`git ls-remote`: baseharbor develop `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2`, baseharbor-demo develop `c23bd9ac58919302ffad3a43f43afb1a34bfbc96`).
- Step 2: Verify antecedent 1 (consent handshake, card 0428-282) — DONE (see "Antecedent 1").
- Step 3: Verify antecedent 2 (MCP/operator-auth class in the #1812 Light harness) — DONE (see "Antecedent 2").
- Step 4: Verify antecedent 3 (annotation #171 / demo PR #171) — DONE (see "Antecedent 3").
- Step 5: Verify antecedent 4 (#1825 testonly build tag, merged 46d3dccc) — DONE (see "Antecedent 4").
- Step 6: Read #1812 PR state + gate history — DONE (see "Base and candidate attestation" + gate evidence).
- Step 7: Synthesize DAG + ordered merge sequence + exact demo_ref + single next action — DONE (see "Dependency DAG" and "Ordered merge sequence").
- Step 8: Write this evidence file — DONE.
- Step 9: Commit+push atomically, prove on origin/main — IN PROGRESS (see "Evidence delivery witness").
- Step 10: Report inline + END post — PENDING.

## Planning repo remote witness (wrong-zone check)

    git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
    origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin	https://github.com/mcpdev80/baseharbor-plan.git (push)

## Base and candidate attestation (reality witnesses)

All remote truth measured with `git ls-remote <real-url>` and `gh api` (never the quarantined workers/baseharbor checkout refs):

- baseharbor develop: `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2`
  (witness: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`).
  This SHA is itself the merge commit of PR #1825 (`fix(0428-249): build baha-ci-operator-testonly artifact with its build tag`, mergedAt 2026-11-24T12:43:08Z — mergeCommit oid equals develop tip, verified via `gh pr view 1825`).
- baseharbor-demo develop: `c23bd9ac58919302ffad3a43f43afb1a34bfbc96`
  (witness: `git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/heads/develop`).
- PR #1812 (`gh pr view 1812`): OPEN, non-draft, base develop, head branch `lane-0428-249-runtime-image-fix`, head SHA `47590207518ce9501f1b1bbb115d72d64a206d14`, mergeable MERGEABLE. Its single commit is on top of develop (w90 ledger: run 45398943139 gate plan logged "Candidate contains the checked develop tip 46d3dccc...", i.e. current develop is an ancestor of the #1812 head — no rebase strictly required for content, see next-action line).
- Latest #1812 gate evidence: run 45398943139 (workflow_dispatch, head 47590207, completed failure). Docker Light family executed 7 gates: guided/lifecycle/failure PASS; policy/connectivity/reconciliation/full-destroy FAIL (w90 ledger, evidence/r28-welle6-2026-11-25/1812-docker-light-ledger/round-1.md). The Podman Light family was NOT executed (`ONLY_GATES` selected `atomic/docker/*` only, `light_podman_execute_count=0`).
- The gate run pinned demo_ref `f23b6e09be34601ba542a3087e19b80764a4165d` (the v0.4.27 pin at develop 46d3dccc; `git show 46d3dccc:docs/releases/v0.4.27.demo-ref`). develop ALSO carries `docs/releases/v0.4.28.demo-ref` = `c23bd9ac...` (current demo develop).

## Antecedent 1 — CONSENT handshake (card 0428-282)

Verdict (corrected against direct code inspection — this REFINES the w92/w85 mission premise): the doubly-nested recognizer is ALREADY MERGED and present in EVERY relevant demo ref. Demo commit `42852efa` (branch `fix/fixture-consent-nested-up-error`, PR #138, MERGED 2026-11-14) is an ancestor of `f23b6e09` (the v0.4.27 pin, `git merge-base --is-ancestor` → true) and of demo develop `c23bd9ac`; the current form was completed by `604c0d7 fix(demo): accept exact wrapped candidate refusal` (2026-11-15). All three refs' `tests/fixture-consent.py` accept the set {direct, single-wrapped, doubly-nested `record deployment before mutation: X: X`}. The failing string from the gates is EXACTLY in that set (see quoted line below). w92's dedicated 0428-282 PR was NOT found open on demo at desk time (newest demo PRs = #171/#170). If w92's PR merges, it is content-equivalent or a no-op for these gates; **antecedent 1 as stated does NOT explain the 4 red gates on 45398943139 and should NOT be treated as a #1812 prerequisite** — flag this to the coordinator as a mapping correction.

Exact failure string the fix must match, quoted verbatim from run 45398943139 job 138466518674 (reconciliation; identical in policy/connectivity/full-destroy jobs):

    Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state

The `next:` hint carries the digest, e.g. (policy job): `Re-run with --confirm-candidate 89c24dd7118e7994507ab6d0173cf5a7b183f8d27eac143d9118924cad57a5ed to acknowledge this exact submission.`

Comparison of recognizers (all verified by direct `git show <ref>:tests/fixture-consent.py`):
- demo develop `c23bd9ac` and run-pinned `f23b6e09`: identical three-variant set {direct, wrapped, doubly-nested} (develop:44-46).
- 42852efa (#138) built {direct, wrapped+wrapped} — same effective set; 604c0d7 finalized it.
- `run_consented` (tests/lib harness) routes the failing ops THROUGH this wrapper (tests/reconciliation/run.sh:9,20,35; tests/connectivity/run.sh:15,34,73; tests/full-destroy/run.sh:12; scripts/acceptance.sh:93), and wrapper.py strips no output — so the digest extraction + `--confirm-candidate` re-run machinery IS engaged for these gates.

Open residual (documented uncertainty): the consent lines at 13:13:10 in the full-destroy job come AFTER the 13:13:08 operator-auth cleanup failure; the in-gate consent refusal was visibly RE-TRIED (second `baha up` at 13:13:10), so whether the consent re-run itself terminates the gate green once operator-auth is fixed cannot be proven from logs alone — only the next exact-head gate run can. If it still fails closed there, the consent-wrapper's digest currency (stale-after-retry question from w85) is the first suspect, not the recognizer set.

Gates formerly attributed to antecedent 1: reconciliation, connectivity, full-destroy (+ policy consent phase) — RECLASSIFIED: they fail on the consent line surfacing inside phases driven by the missing operator authentication (antecedent 2), with the recognizer already in place. Confirmed: NO baseharbor product change needed — the digest hint survives wrapping product-side (#1807 merged as 7b45db92, ancestor of 46d3dccc; w85 diagnosis in evidence/r28-welle6-2026-11-25/0428-281-consent/diagnosis.md).

## Antecedent 2 — MCP-OPERATOR-AUTH class in the Light harness

Verified independently from run 45398943139 logs (the earlier "all four gates = consent only" claim in the w90 ledger is INCOMPLETE):

- policy (job 138466518597): `baha policy check -e dev` fails with
  `Error: operator authentication needs interactive setup but input is not a terminal`
  (log at 13:11:50, then `policy gate unexpected ERR: line=48 exit=2 command=tee "$ARTIFACT_DIR/policy-check.txt"`).
  Demo file:line: `tests/policy/run.sh:48-49` — `$BAHA policy check -e dev | tee ...` is invoked with piped stdout/stdin, non-interactive, without operator auth.
- full-destroy (job 138466518939): `Error` + `Managed-environment machine operations require an authenticated BaseHarbor operator.` / `Configure operator OIDC if required, run 'baha login' for the selected Target/environment, then retry.` at 13:13:08, after the destroy itself had succeeded — this fires in the cleanup/diagnostics preparation, and the job then fails `RESULT FAIL` at 13:13:08.75 (the LATER consent lines at 13:13:10 are a second up-retry, see below).
- reconciliation and connectivity: consent line only (operator-auth string count = 0 in their logs).

Does the harness have the SAME missing operator-auth seed as w80 #1826 / w93 triage? PARTLY: the atomic Light harness auto-provisions the target (`scripts/acceptance.sh:53-58` runs `baha target create ... --provider ... --access local-docker ...` successfully — "target: ready" in every gate log), but it NEVER authenticates an operator (`baha login` / testonly CI-operator credential appears in no harness file; `grep -rn "login|operator" scripts/` → nothing). The product-side testonly seed EXISTS and is the existing provisioning mechanism: `BASEHARBOR_PREBUILT_BINARY=$RUNNER_TEMP/pre-release-candidate/baha-ci-operator-testonly` is handed to the harness by the workflow (pre-release-runtime-suite.yml "Run runtime gate" env block), and #1825/46d3dccc made that artifact actually built WITH the `baseharbor_ci_operator_testonly` tag. The gap is demo-side: `tests/policy/run.sh` (line ~48) and the full-destroy cleanup path invoke commands that require an AUTHENTICATED operator without using that seeded identity.

Classification: this is a SEPARATE demo authorization beyond the consent PR (a second demo harness PR for the policy/full-destroy operator-auth path, card 0428-250 family — its sibling `lane-0428-250-demo-operator-root` PR #170 is open but covers ONLY `tests/config-matrix/run.sh` root naming, NOT policy/full-destroy). Flagged as pending owner authorization.

## Antecedent 3 — ANNOTATION (demo PR #171, card 0428-279; product PR #1826)

- demo PR #171 (`lane-0428-279-mcpcontract-fix`, head `025ce84`): removes `baseharbor.app.pull` from the destructive set in `tests/mcp/run.sh` (plus adds perses tools) and carries unrelated guided drive-matcher edits in tests/guided/*. State OPEN, mergeStateStatus CONFLICTING/DIRTY — needs conflict resolution against demo develop before it can merge.
- baseharbor PR #1826 (OPEN, head `6589a37b`): re-pins `docs/releases/v0.4.28.demo-ref` from `c23bd9ac` to `025ce84`. Its latest dispatch run 45413604588 fails on EXACTLY this one line (`Static · mcp / Executed static · mcp`, "incorrect MCP safety annotations: baseharbor.app.pull", #1826 body) — i.e. the demo-side removal landing on the pinned ref fixes that failure.
- Relevance to #1812's 14 Light gates: NOT DIRECTLY relevant — the mcp gate is a STATIC gate, not a Docker/Podman Light gate. But #1812's qualification rerun inherits the release demo_ref, and the release v0.4.28 pin should carry the annotation fix so the accompanying static gates don't stay red in the same suite. Note: #1826's run shows #1812's candidate family did NOT fail on this annotation path.

## Antecedent 4 — TAG (#1825 operator testonly -tags binary, merged 46d3dccc)

- Verified MERGED at 2026-11-24T12:43:08Z with mergeCommit `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2` = current develop tip.
- Evidence it works on the latest head: run 45398943139 (head 47590207, AFTER the merge) — every gate log shows `baha-ci-operator-testonly` present and the version gate passing; #1812's own targets (runtime image reload, steps 14/15) succeeded in all 7 executed jobs. The residual failures are consent/auth text, not operator-auth admission. CONFIRMED: operator-auth admission now passes (matches w81 ledger).

## Dependency DAG

    #1825 (merged, develop 46d3dccc) ──► operator-auth admission OK for every later rerun   [done]
    #1807 (merged, product digest-hint path) ──► no product change needed for consent        [done]
    demo consent-recognizer: ALREADY on develop + on the run-pinned f23b6e09 (via #138/604c0d7, merged Nov-14/15)
        └─► NOT a #1812 prerequisite; w92's card-0428-282 PR is content-equivalent for these gates
    demo operator-auth harness fix (policy + full-destroy cleanup; 0428-250 family)   [NOT YET AUTHORIZED] ◄── PRIMARY blocker
        └─► unblocks policy (direct auth error) + full-destroy (auth error in cleanup) and, per residual above,
            is the most-plausible driver of the consent lines in reconciliation/connectivity phases
    demo #171 (app.pull destructive-set removal)  [open, CONFLICTING — needs rebase]
        └─► unblocks static mcp gate; #1826 re-pin consumes it (release pin, not #1812 blocker)
    #1812 rerun = f(develop 46d3dccc+, demo_ref = consent + operator-auth fixes merged to demo develop)

## Ordered merge sequence (for #1812 qualification)

1. demo operator-auth harness PR (policy + full-destroy; 0428-250 family) → merge to baseharbor-demo develop. **PENDING OWNER AUTHORIZATION** — no such PR exists yet; #170 (open) covers ONLY `tests/config-matrix/run.sh` root naming, NOT policy/full-destroy. This is the ONE substantive blocker.
2. demo consent PR (card 0428-282, w92) → merge to demo develop (owner-authorized by the w92 mission; optional for #1812 — recognizer already on develop; merges for the regression test and pin hygiene).
3. demo #171 → resolve conflicts against demo develop, then merge (needed for the static mcp gate and the release pin; not a Light-gate blocker for #1812).
4. baseharbor #1826 → merge after #171 lands (it re-pins v0.4.28.demo-ref to #171's head; re-pin to the final demo develop tip if steps merge out of order).
5. #1812 qualification rerun on head 47590207 (develop 46d3dccc is already an ancestor; rebase only if develop moved).

Exact demo_ref #1812 must pin after prerequisites: the final baseharbor-demo develop SHA containing the operator-auth harness fix (step 1) — and, if it merged, the 0428-282 commit. As of this desk no such tip exists; today's demo develop `c23bd9ac` already satisfies the CONSENT-recognizer condition (doubly-nested form accepted, and so does the currently-pinned `f23b6e09`) but NOT the operator-auth condition.

## Single next #1812 action (once prerequisites merge)

Keep or rebase head 47590207 (develop 46d3dccc is already an ancestor; rebase only if develop moved) and dispatch the Pre-Release Runtime suite on the exact head with demo_ref = final demo-develop SHA containing the operator-auth fix; run the Docker Light gates first to green, then the Podman Light gates (never executed in 45398943139 — `ONLY_GATES` selected docker only).

## Pending owner decisions

- Operator-auth demo harness fix (policy run.sh non-interactive auth + full-destroy cleanup auth): no card/PR authorized beyond #170's config-matrix scope — needs owner authorization (this is the "separate demo authorization beyond the consent PR" the mission asked to classify).
- #171 conflict resolution (mergeStateStatus CONFLICTING) and its interleaving with the consent PR in demo tests/guided/* (both touch drive.py) — sequencing decision.

## Gates table (summary)

| antecedent | repo | PR/card | state | gates it unblocks | authorized? |
| --- | --- | --- | --- | --- | --- |
| consent handshake (nested recognizer) | baseharbor-demo | card 0428-282 (w92 PR) — recognizer content ALREADY merged via #138/604c0d7 | on develop AND on run-pinned f23b6e09; dedicated PR not yet seen open | formally none new (reclassification: not the blocker for the 4 red gates) | yes (owner-authorized in w92 mission) |
| operator-auth harness seed | baseharbor-demo | 0428-250 family (#170 open = config-matrix only) | no PR covers policy/full-destroy | docker policy (direct), full-destroy (cleanup); most-plausible driver of the consent-phase fails in reconciliation/connectivity | NO — pending owner decision |
| app.pull annotation set | baseharbor-demo + baseharbor | demo #171 / core #1826 | #171 open CONFLICTING; #1826 open, fails only on static mcp | static/mcp gate (not a Light gate) | covered by card 0428-279 |
| testonly -tags binary | baseharbor | #1825 | MERGED at develop tip 46d3dccc | operator-auth admission in all gates (done) | done |

## cleanliness

Read-only desk: no product-repo writes, no branches/PRs/CI actions (only `gh` reads and `git ls-remote`/read-only clones into /tmp/opencode/w94-map). No containers or compose projects started; nothing to bring down. `docker ps -a` untouched on this host.

## repo-rule compliance

- Hosted-only: zero local test execution. Read-only desktop: no edits/PR/merge/CI triggers on #1812 or chain. No subagents (§4.8). No other session contacted. Evidence only in baseharbor-plan. Real remote URLs only (workers/baseharbor never cited). Compliant.

## Evidence delivery witness

Command run as second-to-last action (output verbatim):

    $ git -C baseharbor-plan fetch origin main && git ls-tree -r --name-only origin/main | grep evidence/r28-welle6-2026-11-25/1812-prerequisite-map
    From https://github.com/mcpdev80/baseharbor-plan
     * branch                main       -> FETCH_HEAD
    evidence/r28-welle6-2026-11-25/1812-prerequisite-map/round-1.md

Evidence commit: 76a6c39fcbacb7b969b85766376102b44b61282a, pushed 4d5b8f8dc..76a6c39fc HEAD -> main to https://github.com/mcpdev80/baseharbor-plan.git.

## END

END_DONE w94-0428-249-1812depcmap: prerequisite map done — develop 46d3dccc, demo develop c23bd9ac; consent recognizer ALREADY on develop and run-pinned f23b6e09 (#138/604c0d7 merged) so card-0428-282 is not the Light-gate blocker; primary blocker is the UNAUTHORIZED demo operator-auth harness fix (policy run.sh non-interactive auth + full-destroy cleanup auth, 0428-250 family); #1825 admission confirmed; #171/#1826 affect static/mcp only; next action = rerun #1812 gates (head 47590207, docker then podman) on demo_ref = demo develop tip containing the operator-auth fix; candidate SHA for chain unchanged 47590207518ce9501f1b1bbb115d72d64a206d14
