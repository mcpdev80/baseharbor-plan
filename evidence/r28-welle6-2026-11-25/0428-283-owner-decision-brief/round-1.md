# 0428-283 — Consolidated owner-decision brief: #1812 / #1826 CI operator-auth (read-only desk)

- Lane: w101-0428-283-ownerbrief
- Mission: coordinator/missions/w101-0428-283-ownerbrief.txt
- Date: 2026-11-24
- Scope: READ-ONLY synthesis. No edits/PR/merge/CI-trigger/rebase; no branch touched; no subagents (§4.8); no other session contacted.

## PLAN

- Fetch reality SHAs via git ls-remote (baseharbor develop, baseharbor-demo develop) and verify planning-repo remote — DONE
- Read all nine listed evidence files plus w81 0428-249 round-3 — DONE (0428-283-operator-fix-proposal/round-1.md appeared between listing and read; all ten sources now folded in)
- Re-measure run 45398943139 per-gate first in-gate failures from the job logs (gh api actions/jobs/<id>/logs, saved under /tmp/runlogs/w101) — DONE
- Verify mechanism claims against current develop f14fb87c8 source (workflow steps, ci_integration_operator_enabled.go, authorization.go, local_workload_authority.go, login/operator_auth_boundary.go, demo harnesses) — DONE
- Write this brief with the corrected fact, A/B/C verdicts, recommendation, downstream sequence — DONE
- Commit + push atomically with targeted git add, prove presence on origin/main, post END — IN PROGRESS

## Reality witnesses (measured this session)

Planning repo (wrong-zone check), `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:

    origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin	https://github.com/mcpdev80/baseharbor-plan.git (push)

    $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
    f14fb87c8f5afd91168e4f174d620c9f00e6341e	refs/heads/develop
    $ git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/heads/develop
    c23bd9ac58919302ffad3a43f43afb1a34bfbc96	refs/heads/develop

Product source read via a fresh blobless clone in the session scratch zone (/tmp/opencode/w101-desk/bh, HEAD = f14fb87c8); demo via `git show f23b6e09:...` / `c23bd9ac:...` in the demo checkout (read-only). Run logs re-fetched read-only via `gh api repos/mcpdev80/baseharbor/actions/jobs/<id>/logs` into /tmp/runlogs/w101.

## Sources synthesized (all present)

serial-execution-runbook, 0428-283-operator-inventory, 0428-283-operator-fix-proposal, 0428-283-fallback-applicability, 0428-284-postretry-triage, 1812-operatorauth-commonality, 1812-prerequisite-map, 1812-docker-light-ledger, 0428-281-consent/diagnosis (all under evidence/r28-welle6-2026-11-25/), plus w81 round-3 (evidence/r28-welle6-2026-11-24/w81-0428-249-1812gates/round-3.md). No source was missing; 0428-283-operator-fix-proposal/round-1.md landed at 16:20 while this desk was reading and is included.

## 1. THE FACT — run 45398943139, per gate (log-authoritative)

Head `47590207518ce9501f1b1bbb115d72d64a206d14` (branch `lane-0428-249-runtime-image-fix`, i.e. it CARRIES #1825's tagged binary), demo_ref `f23b6e09`, workflow "Pre-Release · v0.4.27", ONLY_GATES = 7 atomic/docker Light gates.

Target-create SUCCEEDED in every gate: each log shows `[acceptance] target: creating atomic-docker-<gate> on docker` immediately followed by `[acceptance] target: ready` (policy.log:1073-1074, conn.log:1073-1074, recon.log:1073-1074, destroy.log:1073-1074, re-verified this session from the job-log endpoints). The guided bootstrap `up` then reached `[phase] guided up: READY reached; returning to acceptance gate` in all seven gates. All seven gates EXECUTED (w90 ledger); 3 PASS (guided, lifecycle, failure), 4 FAIL (policy, connectivity, reconciliation, full-destroy).

First IN-GATE failure (after the consented `up` returned READY):

| gate | job id | first in-gate failure | class |
| --- | --- | --- | --- |
| policy | 138466518597 | `Error: operator authentication needs interactive setup but input is not a terminal` at `baha policy check -e dev` (log 1822; `policy gate unexpected ERR: line=48`), preceded at 13:09:34 by a benign first-attempt consent refusal inside the guided PTY flow that the drive.py second `up --confirm-candidate` resolved | operator-admission gap (missing gate-scoped admission for `policy check`) |
| connectivity | 138466518757 | gate exit 1 at 13:13:36 immediately after `run_consented "$BAHA" up --yes` started the companion workload (run.sh:34; log 1838-1861); companion containers reached READY; zero operator-auth strings; the run.sh:52 `connect` step is NOT reached | consent/classification interplay inside `run_consented` on the companion `up --yes` (operator-auth NOT the cause) |
| reconciliation | 138466518674 | gate exit 1 at 13:14:01 immediately after the second `run_consented "$BAHA" app apply` (run.sh:20, the MISSING->CREATE phase after `remove_managed_service_for_reconcile`); apply output ends OK, no third apply in trace, no error string | consent/classification interplay inside `run_consented` on `app apply` (operator-auth NOT the cause) |
| full-destroy | 138466518939 | `Error: Managed-environment machine operations require an authenticated BaseHarbor operator. Affected: /dev` (log 1837-1855) raised INSIDE the consented `run_consented "$BAHA" destroy --all --yes` after `{"destroyed":true}`; trace shows `command="app list --all-targets"` and `command="destroy --all ... --json"` then REJECTED `target-resolution-failed: target "atomic-docker-full-destroy" is not configured` — the self-inflicted no-effective-Target form (app_commands.go:126-138 with target "") is not admitted | operator-admission gap (gate-scoped literal admits `app list --all-targets` WITH a resolvable target, not the post-destroy empty-target re-invocation) |

Reconciliation of w92 vs the owner's raw-log correction: w92's claim that `target create` fails before the fixture (w92-evidence.md:92) is DISPROVED for run 45398943139 — w92 read stale/prior-attempt job text (its quoted timestamp 11:41:55 predates this run's 13:08 gate window, and its "zero consent strings" claim contradicts the consent errors at log line 1474 of every gate). The owner's correction is right for POLICY and FULL-DESTROY: create succeeded, the gate ran, failure is in-gate and operator-auth-class. But the synthesis against current source refines it further: connectivity and reconciliation are NOT operator-auth failures at all (zero auth strings in their logs); they fail inside the consent handshake on admitted commands. #1826 (static/mcp) IS a pure operator-auth failure: untagged plain binary + unsatisfiable env contract, failing at `target create mcp-static` (inventory round-1.md:109, fix-proposal round-1.md:68-83).

## 2. Mechanism options

(A) Build the `baseharbor_ci_operator_testonly`-tagged binary for the static/mcp path.
- Site: `.github/workflows/pre-release-runtime-suite.yml` static gate step, plain artifact/`go build` branch at :271-277 (runtime gate step already uses the testonly binary at :313-319, GOFLAGS :304).
- Coverage: this changes ONLY the static/mcp (and other static gates') binary. The Light gates already run the tagged binary at head 475902075 (ci-operator trace lines in every gate log). So (A) helps #1826 only, and it is NOT sufficient there either: even tagged, `ciIntegrationManagedLocalGateReason` (cmd/baha/ci_integration_operator_enabled.go:96-103) rejects `runtime=static` (hard-wired `docker|podman` at :102) and `mcp-static != atomic-<runtime>-<gate>` (fix-proposal round-1.md:126-149).
- Fail-closed risk: LOW by itself (the seam is tag-gated and env-gated, release binaries unaffected) — w95 grades it "Required prerequisite; does not weaken" (fix-proposal :313-315).

(B) Seed the managed-local operator env/target contract (ci_integration_operator_enabled.go:96-103: `BASEHARBOR_DEMO_OPERATOR_GATE` == `GATE`, `BASEHARBOR_TEST_RUNTIME` in {docker,podman}, target `atomic-<runtime>-<gate>`, AccessProvider local, no tenant).
- For Light: ALREADY fully seeded by the workflow for every runtime gate (pre-release-runtime-suite.yml :312/:322; inventory round-1.md:102-108) — every executed command shows `decision=managed-local-gate`. There is nothing left to "seed"; what fails in policy/full-destroy is the COMMAND admission list, not the env contract. In (B)'s w95 sense — extending the admission for the static contract — it would need a static-runtime case: that is the narrow product-contract widening (`:102`), which w95 grades STOP-WORTHY: it stamps a synthetic verified operator on a host with no verified runtime and no OIDC principal (fix-proposal :316; fallback-applicability :97).
- Verdict for static: Light covered (already), static NOT covered; making static covered via B1 weakens the boundary narrowly and must be an explicit owner decision.

(C) Engage the trusted-local fallback (w93 cited `internal/operatorauth/authorization.go:247`) non-interactively in CI.
- This path NO LONGER EXISTS as a fail-open. #1821 (commit 05ef48536, on develop) removed the dead trusted-local arm; at f14fb87c8 authorization.go:276-283 carries the explicit comment "No trusted-local fail-open here, by design ... do not reintroduce an `!ManagedEnvironment(...)` arm"; :285-295 denies `operator_authentication_required` whenever no principal and no grant. `ManagedEnvironment` (config.go:89-91/110-111) fails closed for EVERY name. w93's "verdict (c) N/A — dev is trusted-local" (1812-operatorauth-commonality :39-54) was measured against the OLD base 46d3dccc1 and the demo Core pin 08755645 and is superseded.
- Why it "does not already apply": it cannot — and the non-interactive substitute IS (B)'s synthetic operator (fallback-applicability :150-153). The `input is not a terminal` error (cmd/baha/operator_auth_boundary.go:122-124, inside `ensureOperatorAuthForBoundary`, reached from authorizeMCPOperation mcp.go:324) is exactly what happens when the seam does not stamp a principal: no `!ok` escape exists, so the boundary tries interactive OIDC setup on piped stdin.
- Re-engaging any name-based fail-open would be a general weakening. Reject.

## 3. Recommendation

Split the two problems; no single change honestly clears both:

1. #1812 Docker Light (and later Podman): the operator seam itself WORKS on the tagged binary (this run proves it). Fix the two residual command-level admissions in baseharbor product `cmd/baha/ci_integration_operator_enabled.go`, mirroring the existing gate-scoped literals (:198-210): admit the exact `policy check -e dev` form on `gate == "policy"` (log evidence: policy trace line `decision=managed-local-gate-rejected: command-not-in-managed-workload-set: policy check -e dev`), and admit the exact self-inflicted no-effective-Target forms (`app list --all-targets` / `destroy --all ... --json` with empty target) on `gate == "full-destroy"` after installation destroy. Separately finish the 0428-282 retry/digest-currency investigation for connectivity + reconciliation, whose logs prove consent-class exits, not operator-auth (this session: conn.log:1838-1861, recon.log:2058-2098) — do not paper them with admissions.
2. #1826 static/mcp: combination A + B2 (+ explicitly-authorized narrow B1). A = use `baha-ci-operator-testonly` (or add the GOFLAGS tag) in the static gate step (owner-scope .github); B2 = demo harness exports the operator env and a canonical target (baseharbor-demo); B1 = one NEW static-only admission case, kept distinct from the docker/podman branch. If the owner will not accept B1's narrow boundary widening, the honest alternative is genuine non-interactive operator config or keeping atomic/static/mcp out of the operator seam by documented policy — never a name-based fail-open (C).

Authorization count: realistically THREE owner decisions, not one: (i) the baseharbor admissions for policy/full-destroy — product code, normal PR; (ii) the static-gate build switch — owner-scope `.github/**`; (iii) the narrow B1 static-runtime product-contract admission — security-relevant; B2 demo changes ride a demo-repo PR. The "single operator-provisioning fix" premise in the runbook (§0 prereq) must be corrected accordingly.

Repo/file footprint: baseharbor `cmd/baha/ci_integration_operator_enabled.go` (+ its test), baseharbor `.github/workflows/pre-release-runtime-suite.yml` (owner), baseharbor-demo `tests/mcp/new-edit-static.py` (+ `tests/init/run.sh`, `tests/shell-ux/run.sh` for the same class).

## 4. Downstream sequence once merged (from serial-execution-runbook round-1)

Once the prerequisite fix(es) merge to develop producing new SHA X, the chain runs strictly serially: rebase #1812 (`lane-0428-249-runtime-image-fix`, base 46d3dccc1) onto X preserving #1823's deny-override content (grep-verify secret_operations.go L58/61/81/171/217 and secret_audit_test.go L195/241/310 post-rebase), force-push with ls-remote witness, then requalify on the exact head with two owner-required runs — Docker Light first (7 atomic/docker gates, tag v0.4.27, demo_ref = the demo tip carrying the fixes), Podman family only after Docker is terminal-green. After #1812 merges, #1819 (`w54-0428-181-export`) rebases and merges (its merge activates the 0428-278 perses coverage rows), then #1820 is cut FRESH from current develop carrying ONLY the 0428-271 regression (`cmd/baha/app_broker_compat_test.go:76-81`) — never the contaminated `28803d11` head; #1818 (`lane-0428-078-cf-fix`) resets from the VOID'd `20fc1cb7` to the canonical `8e2c50c1`, applies the owner-C retarget (persesDashboardProvisionForLifecycle seam + `TestPersesKeycloakDashboardQueriesSelectRealProviderLabels` at cmd/baha/perses_dashboards_test.go:766) and may only `--confirm-candidate` after #1819 is merged. All four stay DRAFT until handoff; no 0.4.28 merge before the 0.4.27 tag.

## repo-rule compliance

- Read-only desk: zero product/demo edits, no branch, no PR, no merge, no rerun/workflow_dispatch (failing runs 45398943139 and 45413604588 were only READ via gh api), no local product tests (Hosted-only), no VM use, no subagents (§4.8), no other session contacted.
- Remote truth only via `git ls-remote` of the real GitHub URLs and fresh clones in the session scratch zone; workers/baseharbor never cited.
- Evidence lives only in baseharbor-plan under evidence/ (this file).

## cleanliness

- No containers, compose projects, networks, volumes or state directories started on this host. `docker ps -a` before/after this session's work: identical (only pre-existing ambient entries from other lanes; this lane added none). Session shell pid witness: parent of these commands (this desk ran only git/gh/sed/grep).
- Scratch: /tmp/opencode/w101-desk (blobless clones of baseharbor + baseharbor-demo), /tmp/runlogs/w101 (job logs). Nothing in /home/marcel/dev/baseharbor-ecosystem outside this evidence file.

## Evidence delivery witness

Command run as second-to-last action (output verbatim):

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle6-2026-11-25/0428-283-owner-decision-brief
    From https://github.com/mcpdev80/baseharbor-plan
     * branch                main       -> FETCH_HEAD
    evidence/r28-welle6-2026-11-25/0428-283-owner-decision-brief/round-1.md

Push delivery: d9e27750e..90ee6b3ab main -> main (evidence commit 90ee6b3ab). Untracked foreign directory evidence/r28-welle6-2026-11-25/1818-true-scope/ exists in this shared checkout and was NOT touched or committed by this lane (reported here so its owner can commit it).

## END

END_DONE w101-0428-283-ownerbrief: consolidated owner brief delivered — corrected fact (target-create succeeds; policy+full-destroy fail on missing command admissions, connectivity+reconciliation on consent interplay; static/mcp = untagged binary + unsatisfiable contract), recommendation = product admissions for Light + A/B2/narrow-B1 combination for static, three owner decisions not one.
