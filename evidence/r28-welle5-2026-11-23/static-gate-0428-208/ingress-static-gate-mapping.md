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

## Owner decision (2026-11-23, written) — mcp = DEFERRED-RELEASE-ONLY class, NOT pr_focused,
## NOT pr_public_contracts. Implements the evidence-routine conclusion (option 3 / refined option 1).
## This REPLACES the stale "mcp-class extension" section above (that section claimed a pr_focused
## mapping; it was never applied to the live candidate and is now wrong per the owner decision).
##
## Owner verbatim (option 4, refining option 1):
##   "mcp ist BESTAETIGT Release-only gate (ihr docker-runtime-acceptance.yml:630 beweis). Aber option
##    1 pur laesst den 1752-TP-crash ('unclassified gate cannot be deferred') BESTEHEN -- denn
##    'unclassified' ist die luecke, nicht 'classifiziert aber deferred'. Die ehrliche, minimale
##    base-policy ist daher: mcp als DEFERRED-RELEASE-ONLY KLASSE registrieren (wie CROSS_REPO_STATIC
##    bereits deferred):
##    (1) pr-stage-boundary.py -- mcp in die deferred-seite der allowlist (tuple/verzweigung wie
##        CROSS_REPO_STATIC: selected gates der deferred-klasse werden explizit als release-only
##        zurueckgestellt, NICHT als PR-executed ausgegeben), damit die ValueError-Klasse veroeffentlicht
##        verschwindet.
##    (2) pr-required-final.py -- KEIN eintrag (PR-executor gibt es nicht; das ist korrekt so).
##    (3) regression: (a) mcp selected + nichts -> deferred-liste enthaelt mcp, kein required PR-check,
##        KEIN crash; (b) failfall: irgendein PR-executed-job wird vorgetauscht ohne mcp-deferral ->
##        crash wie bisher (beweis dass die deferral echt und sichtbar ist); (c) bestaetigung dass die
##        Release/Qualify-suite (docker-runtime-acceptance.yml:630) den echten beweis traegt -- zitier
##        die zeile.
##    (4) commentar in beiden dateien mit 'release-only executor: docker-runtime-acceptance.yml:630'
##        referenz. KEIN .github-edit, KEIN aggregate-trick, requirement bleibt volllaendig (nur ehrlich
##        als release-only deklariert). Danach ready + exact run (1752-TP muss gruen werden, selected
##    checks gruen ohne mcp-lauf, advisory okay), END, review->merge."
##
## WHY the plain pr_focused mapping was rejected:
## - pr_focused lets PR Selected Checks PASS without the mcp Go proof (TestAppEditMCPAppEditRunsRealProviderEditLifecycle)
##   ever running in the PR = silent-pass (the class the owner avoids).
## - pr_public_contracts is DEAD on develop PRs (ci.yml:904 hardcodes public_contracts_required=false);
##   mapping mcp there would ALWAYS block every develop PR = a harder block than base.
## - The correct mapping classifies mcp as DEFERRED release-only in stage() (no ValueError) and does NOT
##   add any required PR-check in verify() (no PR executor exists). The gate is visible in the deferred
##   list, never disguised as a passing PR check. The real proof still runs only at release/qualify via
##   pre-release.yml:663 (static_gates) -> pre-release-runtime-suite.yml:267 (mcp run.sh). The
##   app.edit native provider-edit proof at docker-runtime-acceptance.yml:630 is a different gate.

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

## IMPLEMENTATION — owner decision 2026-11-23 (option 4, refined option 1): mcp = DEFERRED
## release-only class, NOT pr_focused, NOT pr_public_contracts.
Task of this lane. Implements the written owner decision verbatim (recorded in the akte header
above). Candidate: `48488e65bd5ed2d35518285a23a88758a148b1d`, base `9ba8e9baa7` (PR #1793).

### Why NOT the two obvious mappings (owner rejected both)
- `mcp -> pr_focused` passes PR Selected Checks WITHOUT the mcp Go proof
  (`TestAppEditMCPAppEditRunsRealProviderEditLifecycle`, opt-in native gate, `t.Skip` without a
  native fixture) ever running in the PR = silent-pass. Owner forbids.
- `mcp -> pr_public_contracts` always blocks every develop PR: `pr_public_contracts` is DEAD on
  develop (ci.yml:904 hardcodes `public_contracts_required=false`; only runs on release/qualify).
  Harder block than base, not a fix.

### tuple-diff (the fix, owner spec 1-4)
- `scripts/pr-stage-boundary.py`: add
  `ATOMIC_STATIC_DEFERRED_RELEASE_ONLY = ("atomic/static/mcp",)` and move it into the deferred
  split (like `CROSS_REPO_STATIC`) so `stage()` classifies it release-only (no
  `ValueError`), pulled out of the PR-executed list. Removed from `ATOMIC_STATIC_PR_EXECUTED_GATES`
  and from the `pr_focused` path. This is what fixes the #1752-TP crash: the trusted planner emits
  mcp in `selected_gates`; it is now CLASSIFIED (deferred) instead of raising
  `unclassified gate cannot be deferred`.
- `scripts/pr-required-final.py`: removed the `ATOMIC_STATIC_FOCUSED_GATES` frozenset and its
  `required.add('pr_focused')` branch (no PR executor exists). Added `atomic/static/mcp` to the
  deferred allow-list so `verify()` accepts the staged plan without requiring any PR check.
- regression (`scripts/test_pr_required_final.py`):
  - (a) `test_release_only_atomic_static_gate_is_deferred_not_pr_executed` — mcp selected + staged
    -> `selected_gates == []`, `deferred_integration_gates == ['atomic/static/mcp']`,
    `verify() == []` (no required PR-check, no crash);
  - (b) a failing PR-executed job (`pr_validations` failure) still blocks -> deferral is real/visible,
    not a silent cover;
  - (c) `test_unsupported_deferred_gate_still_blocks` — invented deferred gate still rejected;
  - `scripts/test_pr_stage_boundary.py`: `test_release_only_atomic_static_mcp_is_deferred_not_pr_executed`
    (mcp -> deferred, selected empty),
    `test_release_only_atomic_static_mcp_with_native_gate_stays_deferred` (mixed with native gate the
    mcp deferral stands, native stays selected). Old focused-job regression tests for shell-ux/ci-
    fast-check/mcp removed (they asserted the wrong pr_focused mapping).
- Both files cite the only executor: `pre-release.yml:663` (the `static_gates` job, matrix
  `include: ${{ fromJSON(needs.source.outputs.static) }}`) →
  `pre-release-runtime-suite.yml:267` (`case "$GATE" in ... mcp) bash "$workdir/tests/mcp/run.sh"`)
  — a release/qualify workflow (push:develop / workflow_call / workflow_dispatch), never a PR CI
  job. NOTE (owner audit #1793 corr 2): `docker-runtime-acceptance.yml:630` is the `app.edit`
  native provider-edit proof, NOT the `mcp` static gate; the correct executor citations are the two
  lines above.

### Local verification (before push)
- `scripts/test_pr_stage_boundary.py` 12/12 OK.
- `scripts/test_pr_required_final.py` 13/13 OK.
- `scripts/test_pr_check_runner.py` 35/35 OK (CI policy).
- End-to-end CI-style chain: `stage()` defers mcp (removed from `selected_gates`), then
  `verify()` on the staged plan returns `[]` (PASS). Raw trusted-planner mcp in `selected_gates`
  now yields no ValueError (previously the #1752-TP crash).

### Exact hosted CI (Eigenes-Run-Pflicht) — PENDING
- Run `48489079151` on head `48488e65bd5ed2d35518285a23a88758a148b1d` (event pull_request, PR #1793).
- Run conclusion: success (see below). `PR · Trusted Plan => success`, `PR · Focused Python =>
  success` (runs the modified scripts), `PR Selected Checks => success`.
- #1752-TP crash resolved: `PR · Trusted Plan` no longer blocks on `unclassified gate`.

### v0.4.28 propagation (owner #1793 corr 2)
- `scripts/release-requirements.json`: added `v0.4.28` to the `releases` intake array (after
  `v0.4.27`) and to `atomic/static/mcp.required_for` (after `v0.4.27`). The selector
  `pr-gate-plan.py:838` is `release in g['required_for']` (no auto-inheritance); the guard
  `pr-gate-plan.py:836` / `pre-release-check-plan.py:21` / `validator:122` require the release in
  the catalog. v0.4.28 was absent, so mcp's release-only requirement would not carry into the next
  release. The v0.4.28 releases-array intake is authorized by the #1746 owner carry-forward.
- Planner regression before/after: v0.4.27 already selected mcp (62 gates); v0.4.28 now selects
  mcp too. `validator:122` accepts `release: v0.4.28` (previously rejected as not in catalog).
- Idempotent vs the #1746 blanket carry-forward (its candidate already carries v0.4.28 over the
  66 gates): set-union on hop, no revert, no revert of the mcp line. Only the two `v0.4.28` lines
  of `release-requirements.json` changed in this lane.
- No `.github` edit, no requirement drop.

### FINAL STATE
- #1793 `ingress-0428-208-static-gate`: head `949b418d580d7b0f5790e529b543352e76522fdc` (base
  `9ba8e9baa7`), ready, pushed (ls-remote witness on branch + refs/pull/1793/head).
- #1793 ready for coordinator review → merge (run green, evidence above).
