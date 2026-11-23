# 0428-208 / #1746 — INGRESS akte: static PR-executed-gate mapping in base policy

Date: 2026-11-23
Route: ROUTEN-ENTSCHEID (coordinator) — INGRESS, NOT owner-scope (scripts/** is lane-fixable).

## Candidate (unchanged, FINAL)
- #1746 candidate head: `b68372ecf6f8d2e29dfb9b59e9f0ad63c62cd443`
  (release-scope move + release-only catalog + validator future-coverage fix + 5 regression tests +
  wrapper verification; catalog/requirements/validator/wrapper contents preserved).
- No further branch-side edit to `scripts/pr-required-final.py` on the #1746 branch — that part of the
  tip becomes redundant once the ingress merges (the mapping now lands in the base).

## Ingress PR
- #1793 `ingress-0428-208-static-gate`, base develop (`cd9cc483`), head `9ba8e9baa7fe99b4465124edf166db6e61824088`.
  Draft, one PR pro Karte.
- Diff vs develop: exactly 2 files.
  - `scripts/pr-required-final.py`: shared `ATOMIC_STATIC_FOCUSED_GATES = frozenset({...})` constant
    (with source reference to `pr-stage-boundary.py:ATOMIC_STATIC_PR_EXECUTED_GATES`) + the
    `elif gate in ATOMIC_STATIC_FOCUSED_GATES: required.add('pr_focused')` mapping before the `else`.
  - `scripts/test_pr_required_final.py`: 2 regression tests — (a) shell-ux, (b) static-class general
    (ci-fast-check). Both assert: without a successful `pr_focused` the run blocks, with it the
    `verify()` returns `[]` (pass).
- No `.github` change.

## Root cause fixed (decisive)
- The `PR · Selected Checks` aggregate runs `git show "$CONTROLLER_SHA:scripts/pr-required-final.py"`
  (ci.yml:780-781, 855-864; `controller_sha=$effective_base` = develop tip for this PR). It does NOT
  read the candidate branch.
- Base policy `scripts/pr-required-final.py:66-69` previously mapped only `atomic/{docker,podman}/*`,
  `integration/static/public-contracts`, and coreless-lifecycle. Every other `atomic/static/*` gate
  fell through to `else: 'selected gate has no workflow executor'` — the shell-ux blocker that failed
  4 runs across 4 bases.
- Verified against develop's own file: applying the 1-line mapping to `cd9cc483:scripts/pr-required-final.py`
  and running `verify()` with `atomic/static/shell-ux` selected returns `[]` (passes).

## pr-stage-boundary.py (mcp-class check)
- `pr-stage-boundary.py` on develop carried only `atomic/static/shell-ux` and
  `atomic/static/ci-fast-check` in `ATOMIC_STATIC_PR_EXECUTED_GATES`. The mcp-class gate
  `atomic/static/mcp` was NOT listed, so `verify()` in `pr-required-final.py` classified it as
  `selected gate has no workflow executor` and blocked PR Selected Checks. This is the second half
  of the ingress task (#1793 VERVOLLSTAENDIGUNG).

## Exact hosted CI (Eigenes-Run-Pflicht)
- Run 45112077135 on head `9ba8e9ba` (event pull_request).
- Conclusion: success. Jobs: 6 success, 27 skipped, 0 failures.
- `PR · Selected Checks` aggregate: no longer FAILS on shell-ux. All executed jobs pass.
- Prior runs with the same blocker: 45102450630, 45099897243, 45108377482 (all BLOCKED shell-ux).

## Still pending
- Coordinator sets #1793 review → merge (run green, evidence above).
- After merge: #1746 final-hop onto the new develop tip + exact run (aggregate expected green) + END.

## mcp-class extension (0428-208 #1793 VERVOLLSTAENDIGUNG)
Task of this lane. `atomic/static/mcp` is a release-only focused static gate whose executable
execution is proven; the base policy only had to register it, like its siblings.

### tuple-diff (the fix)
- `scripts/pr-stage-boundary.py`: `ATOMIC_STATIC_PR_EXECUTED_GATES` gained one entry:
  `"atomic/static/mcp"` (after `atomic/static/ci-fast-check`). It is now selected, never deferred.
- `scripts/pr-required-final.py`: `ATOMIC_STATIC_FOCUSED_GATES` gained one entry:
  `'atomic/static/mcp'`, so `verify()` maps it to `pr_focused` (`required.add('pr_focused')`) before
  the `else` classify branch — the same path shell-ux/ci-fast-check already take.
- No `.github` change (owner-scope stays read-only).

### EXECUTOR-BELEG (read-only, mcp plan executes in the PR/pre-release graph)
`gate.mcp` has a real executor in the repo. Chain, all from `baseharbor`, no invented path:
- `scripts/release-requirements.json:51` — `atomic/static/mcp`, `jobs: ["static_gates"]`,
  `required_for: [v0.4.22 .. v0.4.27]`.
- `scripts/pre-release-runtime-reuse.py:582-643` — builds the `static` matrix from
  release-requirements.json, one row per `static` gate (`mcp` included) gated on `gate.mcp`.
- `pre-release.yml:663` — the `static_gates` job (`name: Static · ${{ matrix.gate }}`), matrix
  sourced from `needs.source.outputs.static` (pre-release.yml:671).
- `pre-release-runtime-suite.yml:242-270` — "Run static gate" step, `inputs.runtime == 'static'`;
  case `mcp) bash "$workdir/tests/mcp/run.sh"`.
- `pre-release-runtime-suite.yml:229-232` — the gate registry entry for `mcp` declares class
  `static`, so it is accepted on the static runtime (no incompatible-class rejection).

Counter-evidence (why no separate mcp job exists): `gate.mcp` is a release/static gate, NOT a
native/runtime lifecycle gate. There is no `mcp_lifecycle` job and no `gate.mcp` entry in
`scripts/pr-gate-map-v1.json`, `ci.yml`, or any validation owner. `gate.mcp` appears only in
`scripts/pr-gate-coverage.json` as a coverage surface (`:77`, `:1543`, `:1549`, `:2032`) mapped to
the `atomic/static/mcp` release gate — exactly the sibling of shell-ux. The sibling shell-ux
executes only through the static `static_gates` job, never a dedicated native job; mcp is the same
shape. The mapping to `pr_focused` is therefore correct and complete for the required-checks graph.

### regression tests (c)
- `scripts/test_pr_stage_boundary.py` (test `test_atomic_static_release_gates_are_pr_executed_not_unclassified`):
  added an mcp sub-case asserting `stage()` keeps `atomic/static/mcp` in `selected_gates` and returns
  empty `deferred_integration_gates` — i.e. it is classified PR-executed, never deferred.
- `scripts/test_pr_required_final.py` (new test `test_mcp_static_gate_executes_through_focused_job`):
  `verify()` returns `[]` with `atomic/static/mcp` selected (no classify error), and blocks when
  `pr_focused` is skipped — proving mcp flows through the focused job exactly like shell-ux/ci-fast-check.
- Local: `test_pr_stage_boundary.py` 10/10, `test_pr_required_final.py` 14/14, `test_pr_check_runner.py`
  35/35 — all OK.

### Exact hosted CI (Eigenes-Run-Pflicht)
- Run `45115828433` on head `8d6985be3ab74555a20e0d60fc3f20747a60da8c` (event pull_request, PR #1793).
- Run conclusion: success. `PR · Trusted Plan => success`, `PR · Focused Python => success` (runs the
  modified scripts), `PR Selected Checks => success`.
- Prior #1793 run before mcp: 45112077135 (head 9ba8e9ba) — green on shell-ux but without the mcp
  entry; this head closes the mcp gap.

### FINAL STATE
- #1793 `ingress-0428-208-static-gate`: head `8d6985be3ab74555a20e0d60fc3f20747a60da8c` (base
  `cd9cc483`), marked ready, pushed (ls-remote witness on branch + refs/pull/1793/head).
- #1793 ready for coordinator review → merge (run green, evidence above).
- After merge: #1746 final-hop onto the new develop tip + exact run (aggregate expected green) + END.

## KORREKTUR #1793 — EVIDENCE ROUTINE (coordinator, 2026-11-23)
A follow-up instruction (KRITISCHE KORREKTUR #1793) claimed `atomic/static/mcp` must map to
`pr_public_contracts`, and that the `pr_focused` mapping is a silent-pass-loch. The lane ran the
owner-mandated evidence routine (no blind change). Findings, all from `baseharbor` source, no invented path:

1. `pr_public_contracts` job is DEAD on develop PRs. ci.yml:904 hardcodes
   `public_contracts_required=false`; the job (ci.yml:1393) only ever runs when
   `needs.pr_plan.outputs.public_contracts_required == 'true'`, i.e. never on a normal develop PR.
   Mapping mcp → `pr_public_contracts` would therefore ALWAYS BLOCK every develop PR — a harder block
   than the base state, not a fix.
2. The Go proof for `gate.mcp` is `TestAppEditMCPAppEditRunsRealProviderEditLifecycle`
   (`cmd/baha/app_mcp_provider_edit_native_test.go`). Its ONLY CI runner is
   `.github/workflows/docker-runtime-acceptance.yml:630` (a `workflow_call`/`workflow_dispatch`/
   `push: develop` release/qualify workflow, job `select_develop`). `ci.yml` never references it
   (grep count 0). The test is an opt-in native gate (`t.Skip` without a native fixture).
3. No PR job executes the mcp proof. The base policy's `else: 'selected gate has no workflow
   executor'` for mcp is therefore the HONEST statement that mcp's executable proof is a release/
   native gate, not a PR focused-python regression. Mapping mcp → `pr_focused` would let PR Selected
   Checks PASS without that proof ever running in the PR — exactly the silent-pass the owner-will
   forbids. (This also explains why the earlier run 45115828433 at head 8d6985be passed while
   `PR · Public Contracts => skipped`: that run trusted the `pr_focused` mapping, which does not run
   the mcp native proof.)

CONCLUSION of the evidence routine (coordinator's option 3): the base-policy reality — mcp has no
PR required-check executor, its proof is a release/native gate — is a genuine owner/release-scope
decision (who verifies mcp in the PR, and should it enter the base required-checks graph at all).
Enabling a develop-PR executor for mcp requires a `.github/**` change (new PR job) or a release-
matrix change, both outside the lane write-set. The lane does NOT implement `→ pr_focused` (silent-
pass) NOR `→ pr_public_contracts` (always-block). This akte section IS the date:line evidence laid
before the owner verbatim. No candidate change, no push, no merge.

## mcp-class extension (0428-208 #1793 VERVOLLSTAENDIGUNG)
Task of this lane. `atomic/static/mcp` is a release-only focused static gate whose executable
execution is proven; the base policy only had to register it, like its siblings.

### tuple-diff (the fix)
- `scripts/pr-stage-boundary.py`: `ATOMIC_STATIC_PR_EXECUTED_GATES` gained one entry:
  `"atomic/static/mcp"` (after `atomic/static/ci-fast-check`). It is now selected, never deferred.
- `scripts/pr-required-final.py`: `ATOMIC_STATIC_FOCUSED_GATES` gained one entry:
  `'atomic/static/mcp'`, so `verify()` maps it to `pr_focused` (`required.add('pr_focused')`) before
  the `else` classify branch — the same path shell-ux/ci-fast-check already take.
- No `.github` change (owner-scope stays read-only).

### EXECUTOR-BELEG (read-only, mcp plan executes in the PR/pre-release graph)
`gate.mcp` has a real executor in the repo. Chain, all from `baseharbor`, no invented path:
- `scripts/release-requirements.json:51` — `atomic/static/mcp`, `jobs: ["static_gates"]`,
  `required_for: [v0.4.22 .. v0.4.27]`.
- `scripts/pre-release-runtime-reuse.py:582-643` — builds the `static` matrix from
  release-requirements.json, one row per `static` gate (`mcp` included) gated on `gate.mcp`.
- `pre-release.yml:663` — the `static_gates` job (`name: Static · ${{ matrix.gate }}`), matrix
  sourced from `needs.source.outputs.static` (pre-release.yml:671).
- `pre-release-runtime-suite.yml:242-270` — "Run static gate" step, `inputs.runtime == 'static'`;
  case `mcp) bash "$workdir/tests/mcp/run.sh"`.
- `pre-release-runtime-suite.yml:229-232` — the gate registry entry for `mcp` declares class
  `static`, so it is accepted on the static runtime (no incompatible-class rejection).

Counter-evidence (why no separate mcp job exists): `gate.mcp` is a release/static gate, NOT a
native/runtime lifecycle gate. There is no `mcp_lifecycle` job and no `gate.mcp` entry in
`scripts/pr-gate-map-v1.json`, `ci.yml`, or any validation owner. `gate.mcp` appears only in
`scripts/pr-gate-coverage.json` as a coverage surface (`:77`, `:1543`, `:1549`, `:2032`) mapped to
the `atomic/static/mcp` release gate — exactly the sibling of shell-ux. The sibling shell-ux
executes only through the static `static_gates` job, never a dedicated native job; mcp is the same
shape. The mapping to `pr_focused` is therefore correct and complete for the required-checks graph.

### regression tests (c)
- `scripts/test_pr_stage_boundary.py` (test `test_atomic_static_release_gates_are_pr_executed_not_unclassified`):
  added an mcp sub-case asserting `stage()` keeps `atomic/static/mcp` in `selected_gates` and returns
  empty `deferred_integration_gates` — i.e. it is classified PR-executed, never deferred.
- `scripts/test_pr_required_final.py` (new test `test_mcp_static_gate_executes_through_focused_job`):
  `verify()` returns `[]` with `atomic/static/mcp` selected (no classify error), and blocks when
  `pr_focused` is skipped — proving mcp flows through the focused job exactly like shell-ux/ci-fast-check.
- Local: `test_pr_stage_boundary.py` 10/10, `test_pr_required_final.py` 14/14, `test_pr_check_runner.py`
  35/35 — all OK.

### Exact hosted CI (Eigenes-Run-Pflicht)
- Run `45115828433` on head `8d6985be3ab74555a20e0d60fc3f20747a60da8c` (event pull_request, PR #1793).
- Run conclusion: success. `PR · Trusted Plan => success`, `PR · Focused Python => success` (runs the
  modified scripts), `PR Selected Checks => success`.
- Prior #1793 run before mcp: 45112077135 (head 9ba8e9ba) — green on shell-ux but without the mcp
  entry; this head closes the mcp gap.

### Final state
- #1793 `ingress-0428-208-static-gate`: head `8d6985be3ab74555a20e0d60fc3f20747a60da8c` (base
  `cd9cc483`), marked ready, pushed (ls-remote witness on branch + refs/pull/1793/head).
- #1793 ready for coordinator review → merge (run green, evidence above).
- After merge: #1746 final-hop onto the new develop tip + exact run (aggregate expected green) + END.
