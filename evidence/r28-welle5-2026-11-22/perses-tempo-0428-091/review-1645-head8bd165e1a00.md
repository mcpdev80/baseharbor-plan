# PR #1645 exact-head independent review

## PLAN

1. Read the #1645 review tail and reconcile the exact scope, candidate, evidence destination, and coordinator handoff requirement.
2. Refresh GitHub refs and exact-head CI receipts; inspect the candidate diff and prior acceptance criteria read-only.
3. Write and validate SHA-specific review evidence in the specified Planning path; publish only that evidence to Planning origin/main.
4. Update the live board and post the final exact-head verdict and witnesses to the Coordinator.
5. Read the #1645 continuation and capture its terminal-run requirements and read-only limits.
6. Record run 45001605859 terminal status, exact-head match, failed count, packages job ID, and native data-capabilities execution state.
7. Finish and validate the SHA-specific review evidence, publish it to Planning origin/main, update the board, and post END.
8. Read the #1645 review continuation tail and capture its exact additional evidence requirements.
9. Reconcile terminal CI state and the runtime-coverage verdict for the exact head without triggering or rerunning workflows.
10. Update and validate the existing Planning review evidence, publish it to origin/main, update the board, and post END.

## Scope and candidate

Role: CODEX-REVIEW, independent read-only review. PR #1645 is open, ready (not draft), and based on `develop` at `acc343239681feb235a33cf00c8ea754c537291f`. The exact candidate is `8bd165e1a00d25972b55e5b50787091f0aee8f0a`, branch `w091-tempo-r5-fix`. Fresh remote witness: `acc343239681feb235a33cf00c8ea754c537291f refs/heads/develop` and `8bd165e1a00d25972b55e5b50787091f0aee8f0a refs/pull/1645/head`.

The additive hop is verified in GitHub commit metadata: merge commit `95ddbb1c38b0714bb8145a672433d453e9be49c0` has parents `326ca9005267c135feb31cdfde8ac69a3c17508e` (previous candidate) and `acc343239681feb235a33cf00c8ea754c537291f` (develop). Head commit `8bd165e1a00d25972b55e5b50787091f0aee8f0a` is a child of that merge and changes only `internal/metrics/perses_tempo_source_test.go` by one insertion and one deletion. The adapter commit remains present as exact commit `4d73aa97808d000d2f70eaa193f8dbfc14e817a7`.

## Review findings

The corrected test at `internal/metrics/perses_tempo_source_test.go:404-421` now resolves with `ResolveWithPolicy("dev", "cache", AuthenticationMTLS, EnvironmentPolicy{TrustedLocal: true})`. It reconciles TLS material and asserts that a development non-RequireClient gateway has no client certificate or key. This makes the test fixture's policy source explicit and preserves the policy-neutral behavior under test. The exact changed commit contains no product-code change. The test uses `t.TempDir()` for its files and an in-memory test issuer; no persistent resource is created. Static inspection of the target test file found no `t.Skip`, skip call, timeout change, or sleep.

The mission's full-base empty-diff condition is not met literally. GitHub's `develop...HEAD` comparison contains these `internal/serviceaccess/**` paths: `gateway_reader.go`, `http_gateway.go`, `perses_compose_realization.go`, `pki.go`, and `pki_projection_test.go`. Its non-test `internal/metrics/*.go` paths are `perses_tempo_contract.go`, `perses_tempo_datasource.go`, `perses_tempo_errors.go`, `perses_tempo_upstream.go`, and `perses_tempo_verify.go`. No `.github/scripts/**` path is changed. Those source changes belong to the retained Perses Tempo adapter commit in this feature PR; they are not changes in the one-line correction hop. The hop-only comparison `95ddbb1c38b0714bb8145a672433d453e9be49c0...8bd165e1a00d25972b55e5b50787091f0aee8f0a` contains only `internal/metrics/perses_tempo_source_test.go`.

Therefore the stated criterion “empty `develop...HEAD` diff” conflicts with the same review instruction to retain adapter commit `4d73aa97` and with this card's adapter write-set. I cannot mark that literal criterion satisfied. Repair recipe: if this review is intended to judge only the correction hop, scope the non-test check to `95ddbb1c38b0714bb8145a672433d453e9be49c0...HEAD` and retain the existing adapter commit; rerun the exact-head package check if the candidate changes. If emptiness against develop is mandatory for the entire PR, the candidate must be narrowed, which conflicts with the required adapter commit and card goal; resolve that acceptance-scope conflict before changing product files. No test/source correction is indicated by the current correction commit itself.

## Hosted CI and test routing

Exact PR-triggered run `45001605859` for head `8bd165e1a00d25972b55e5b50787091f0aee8f0a` completed `success` at 2026-11-22 08:16:07 UTC after 5m02s; trigger was `synchronize`; failed jobs: 0. It had 30 jobs: 15 success and 15 skipped. `PR Selected Checks` check run `137145341525` completed success. `PR · Go unit · packages` job `137144258716` completed success, replacing the prior packages failure `137127343932` on old head `326ca900526`. The exact test is in the package run's normal Go test discovery; the hosted package log reports `ok github.com/mcpdev80/baseharbor/internal/metrics 1.261s`.

The Trusted Plan output recorded these annotations: “Incremental PR checks: previous source/base ancestry not proven; reused validations=0; reused runtime gates=0” and “No narrow mapping: conservative checks selected.” No prior validations or runtime gates were reused.

`PR · Native gate plan` job `137144213067` succeeded. The native selection result was `NATIVE_REQUIRED: false`, `NATIVE_RESULT: skipped`; `PR · Selected Runtime` check `137144260959` and `PR · Native · ${{ matrix.id }}` check `137144260109` were skipped. The native matrix had no data-capabilities row. This is a selection outcome, not an executed native runtime proof.

## Runtime coverage verdict

Runtime coverage: native data-capabilities not required for the reviewed change. The correction-hop diff changes only `internal/metrics/perses_tempo_source_test.go`. On the trusted base, `scripts/validate-pr-gate-coverage.py:66-83` resolves native checks from changed source-component paths and each check's `source_components`; `scripts/pr-gate-coverage.json:3056-3076` lists the Docker data-capabilities row's components, all under `cmd/baha`, and the test path is not a component path or listed source component. The Podman row at `scripts/pr-gate-coverage.json:3077-3097` has the same component mapping. `scripts/release-requirements.json` lists supported releases through v0.4.27 and its data-capabilities requirement rows at lines 248 onward and 608 onward; v0.4.28 is absent from that base catalog. Therefore the missing native row is correct for this test-only correction and is not a coverage gap for this changed path. The skipped row must not be reported as runtime execution evidence.

## Verdict

REQUEST_CHANGES — the corrected test and exact-head selected checks pass, but the explicitly required empty `develop...HEAD` non-test diff is false because the same candidate retains the adapter's service-access and metrics implementation. The review can be completed as APPROVE only after the acceptance scope is clarified to assess the one-line hop delta, or after the full-base diff condition is otherwise reconciled; the native data-capabilities row is not required for the correction path.

## Repo-rule compliance

Read-only review only. No product files changed, no PR review/comment/merge/close action was issued, no workflow rerun was triggered, and no product tests were run locally. Planning evidence is stored only in the canonical `baseharbor-plan` repository. Canonical Planning remote line: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

## cleanliness

Before review, PID 3322430 ran `docker ps -a --no-trunc`; output contained only the column header and no containers. After review, PID 3329378 ran `docker ps -a --no-trunc`; output contained only the column header and no containers. No compose project was started. The Planning validator `python3 scripts/plan.py check` completed with 0 errors and 10 pre-existing dependency warnings.

END codex-rev-1747 DONE — REQUEST_CHANGES on exact head `8bd165e1a00d25972b55e5b50787091f0aee8f0a`; runtime-coverage verdict: native data-capabilities not required for the test-only correction; run `45001605859`, failed jobs 0, packages job `137144258716`; `develop...HEAD` non-test diff is not empty; Planning remote `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

## Planning path witness

The required fetch and tree lookup returned exactly:

```text
From https://github.com/mcpdev80/baseharbor-plan
 * branch                main       -> FETCH_HEAD
evidence/r28-welle5-2026-11-22/perses-tempo-0428-091/review-1645-head8bd165e1a00.md
```
