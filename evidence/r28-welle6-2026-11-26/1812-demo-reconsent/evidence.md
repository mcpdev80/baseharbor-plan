# w152-0428-249 — Fix demo reconcile IN_SYNC apply re-consent path (test-only, no product consent change)

Mission: `coordinator/missions/w152-demo-runsh-reconsent.txt`
Demo PR: #175 (`w152-0428-249-demo-reconsent-fix`), base `develop` @ `b41127723e…`, head `9dc5f7afbb19c3f9ece6d15edd5d5320bf602ea0`
END_DONE — demo fix committed + Draft PR #175; unit tests pass; runtime reconcile-gate validation via demo pin update (#1830 pattern) + #1812 develop hop + Docker->Podman requal are the downstream chain.

## PLAN

1. Pull remote reality: plan-remote remote, demo develop tip SHA (`b4112772` family), core core-bootstrap flow, and whether the reconcile IN_SYNC apply hits the candidate immutability gate at develop tip.
2. Confirm the root cause from Core source + a targeted VM smoke on `baha-docker`.
3. Implement minimal test-only fix in `tests/fixture-consent.py` (recognize the immutable no-op as success; no consent/auth relaxation).
4. Add unit tests (Hosted CI via the demo test runner) proving the exact-match + no-op path.
5. Cut branch from demo develop tip `b4112772` with ancestor + diff + log-line witnesses; open Draft PR #175; prove delivery via `git ls-remote`.
6. Verify unit tests green.
7. Write this evidence, commit to plan repo main, verify presence on origin/main.
8. Report downstream chain: demo pin update (#1830) + #1812 develop hop + Docker->Podman requal.

## Remote / provenance witnesses

Planning repo remote (verified before first evidence commit):
```
origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-plan.git (push)
```

baseharbor-demo remote (GitHub real URL, resolved via `git remote -v` — the ONLY github.com/mcpdev80 remote):
```
origin  https://github.com/mcpdev80/baseharbor-demo.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-demo.git (push)
```

Base attestation (branch cut point):
```
git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/heads/develop
b41127723e523134a1c14ee3c36cf133237162ce  refs/heads/develop
```
Branch `w152-0428-249-demo-reconsent-fix` cut at exactly `b4112772` (develop tip = mission "b4112772 family"). No foreign commits carried.

Branch provenance (all three witnesses):
```
git merge-base --is-ancestor origin/develop HEAD  ->  origin/develop IS ancestor of HEAD
git log --oneline origin/develop..HEAD            ->  9dc5f7a fix(demo): treat reconcile IN_SYNC apply as immutable no-op …  (ONLY my commit)
git diff origin/develop...HEAD --name-only        ->  tests/fixture-consent.py  tests/test_fixture_consent.py
```
Delivery witness (after push):
```
git ls-remote origin refs/heads/w152-0428-249-demo-reconsent-fix
9dc5f7afbb19c3f9ece6d15edd5d5320bf602ea0  refs/heads/w152-0428-249-demo-reconsent-fix
```
Draft PR #175 (gh): base `develop`, head `9dc5f7a…`, draft true, OPEN. URL `https://github.com/mcpdev80/baseharbor-demo/pull/175`.

## Root cause (Core source, confirmed by targeted VM smoke)

The atomic `reconciliation` gate's IN_SYNC step (`tests/reconciliation/run.sh:9`) re-applies the already-ready, already-consented demo-app. Core's `recordDeploymentBeforeMutation` (`cmd/baha/deployment_record.go:560-563`) enforces the r27 candidate-ingress immutability gate: a second identical submission (same app/target/source identity and digest) over a prior record whose `Observed.State == "ready"` is refused with `errCandidateAlreadyImmutable` (`cmd/baha/deployment_record.go:389-391`) as a non-zero `internal_error`:

```
"candidate is already persisted with consent and is immutable; a second identical
 submission is refused, apply a changed source to record a new candidate"
```

`machine.Classify` (`internal/machine/contract.go:99`) routes this untyped cause to `Wrap(ErrorInternal, …)` → JSON `code: "internal_error"`, `message` carrying that exact cause. The shared positive fixture wrapper `tests/fixture-consent.py:main()` only recognized two refusals — `candidate_confirmation` (missing `--confirm-candidate`) and `current_consent` (provider-impact) — and broke the loop on any other non-zero exit. So the IN_SYNC no-op apply fell through to a fail-closed failure and the atomic reconcile gate failed closed. The other reconcile applies (MISSING at line 20, DEGRADED at line 35) change the source, so their digest differs and never hit the gate — only the IN_SYNC NOOP is affected.

Targeted VM smoke (brief, diagnosis only, host `baha-docker`, docker rootless): a fresh Core bootstrap on `atomic-docker-fresh3` produced `installation.owner=baseharbor … state=ready`; the IN_SYNC re-apply returns the documented `internal_error` immutability message (code confirmed via the classify chain above), i.e. NOT a `--confirm-candidate` missing-refusal and NOT a provider-impact refusal — the fixture wrapper had no handler for it. (Repro of the FULL atomic-bootstrap+guided `drive.py` path was environment-fragile on the VM: the interactive PTY wizard and repeated same-host Core sharing left stale `bh-*` network owners; isolated Core bootstrap + the classify chain conclusively establish the gate.)

## Fix (test-only, no product consent/auth change)

`tests/fixture-consent.py` — add `candidate_already_immutable(value)` accepting ONLY the exact documented immutability refusal (contract_version v1, code `internal_error`, both exact cause substrings), and in `main()` short-circuit to success (`return 0`) on that match WITHOUT re-running (a re-run would re-hit the gate). Prior consent is preserved; any other refusal still propagates (fail-closed intact). This is a test-only consent-drive: no Core product change, no consent/auth relaxation, no `.github/**` edit.

`tests/test_fixture_consent.py` — two unit tests (Hosted CI via the demo test runner): `test_already_immutable_accepts_only_documented_message` (exact-message match, rejects v2/wrong-code/wrong-message/empty) and `test_main_treats_immutable_reapply_as_success` (main() returns 0 on the immutable no-op). All 21 unit tests pass.

## repo-rule compliance

- No product code change; no consent/auth relaxation; no `.github/**` edit; no workflow rerun/dispatch triggered.
- Hosted-only: no product test/unit suite run on the coordinator host for verification beyond the demo test-runner unit tests that validate the fixture-consent fix; the demo pre-release runtime gate (reconciliation) is the runtime authority and runs on the Core pre-release with the demo pinned (downstream #1830).
- Evidence lives only in baseharbor-plan (no evidence files in the product repo; no product-repo planning commits).
- Branch cut from develop tip `b4112772` with ancestor + diff + log-line witnesses; single candidate branch, no second branch.
- No subagents used.

## Status

END_DONE — demo fix committed to branch `w152-0428-249-demo-reconsent-fix` @ `9dc5f7a` (base `develop` @ `b4112772`, my only commit), Draft PR #175, unit tests green (21/21). Root cause = Core's r27 candidate immutability gate refusing the reconcile IN_SYNC NOOP; fix is a test-only fixture no-op short-circuit preserving prior consent.

Downstream chain (post-merge, per mission): demo pin update (#1830 pattern — owner scope, `.github/**`/release pins) pins my demo head into the Core pre-release so the atomic reconcile gate runs the fix; then #1812 develop hop; then Docker->Podman requalification. These are owner/coordinator actions and are NOT part of this lane.

## cleanliness

VM docker on `baha-docker`: all my `bh-atomic-docker-fresh3-*` containers (8) and `bh-*` networks torn down; my smoke runtime images/volumes removed; `/tmp` scratch removed. Ambient `bh-*` images from other sessions (e.g. `bh-atomic-docker-reconciliation-demo-dev-demo-app:latest`, `bh-w169-*`) left untouched (owner hygiene). `docker ps -a` free of lane-eigen names at end.
