# CODEX-REVIEW — Luna batch18

Date: 2026-11-17. Role: CODEX-REVIEW (Luna). Read-only review; no merge.

## Exact candidate and run witnesses

| Object | Candidate | PR / base | Run | Observed result |
| --- | --- | --- | --- | --- |
| 1 / 0428-094 | `fe00c7f180dc373d64a919e8aa74193a4db548bb` | Core #1666 / `develop`, OPEN DRAFT | `43958812007` | SUCCESS; draft jobs incl. Go packages and four CLI shards passed |
| 2 / 0428-082 | `d2a9cd11d0a8eb3149b30bc4f79509cc2970421e` | Core #1665 / `w083-perses-datasources`, OPEN DRAFT | `43968469748` | `workflow_dispatch`, FAILURE; unit/package tests passed, runtime integration step failed; other listed PR jobs skipped |
| 3 / 0428-099 | `86afbbebb7574b5c4bc1caeb098a4406e1e4a9e3` | Demo #164 / `develop`, OPEN DRAFT | `43963399114` | `workflow_dispatch`, SUCCESS; Guided consent regression job passed |

Remote PR heads, bases and draft states were checked as `mcpdev80`. The exact #1665 run is on its current head. In that run, `Run unit and package tests` passed, including `internal/metrics`; the separate `Run runtime integration tests serially` step failed. The round-4 evidence classifies its five ORAS setup failures and the postgres Config.User failure, and records the same failure set on unrelated chains. The replacement evidence includes the lane's exact-head cell replay with 3/5 lifecycle tests passing and the remaining two failing for cell state/argument reasons. This classification is accepted as evidence that the observed runtime failures do not implicate the dashboard diff; it does not substitute for the card's actual Prometheus-query acceptance point below.

## Verdicts

### Object 1 — #1666 / 0428-094: REQUEST CHANGES

The previous batch17 correction is otherwise present: an existing empty or whitespace-only file now returns `ErrConfigEmpty`; valid configuration still loads; and a missing file under a genuinely empty root retains the implicit default. The four-case `TestLoadConfigEndToEndXDGPath` exercises those behaviors at the ordinary path `XDG_CONFIG_HOME/baseharbor/config.yaml`.

The required end-to-end regression for the original XDG double-append case is still missing. In that case `XDG_CONFIG_HOME` itself already ends in `/baseharbor`, so `ConfigPath()` resolves a nested `/baseharbor/baseharbor/config.yaml` while the user's intended `config.yaml` is one directory above. `TestDirExistsAndHasBaseharborState` checks only the helper predicate for this sibling file; it never calls `LoadConfig()` with that XDG setup. The correction evidence says the matrix covers the real XDG resolution, but the source does not cover the reproduced mismatch end-to-end.

**Recipe:** add a `LoadConfig` integration case with `XDG_CONFIG_HOME=<temp>/.config/baseharbor`, place the intended `config.yaml` at that root, leave the nested resolved path absent, and assert `errors.Is(err, ErrConfigMissing)`. Retain the normal four-case matrix and the valid-config assertion. Run the affected deployment package check through an exact-head PR/draft Go run after the test correction.

### Object 2 — #1665 / 0428-082: REQUEST CHANGES

The batch17 content fixes are present in the exact candidate: the output uses the native Perses `Dashboard`/`Panel`/`TimeSeriesQuery` resource shapes; schema witnesses and a golden pin the serialized form; each panel's missing state follows its own query result; and unsupported node-exporter series were removed in favor of the scrape metadata series and actual BaseHarbor job/source labels. The unchanged 0428-080 selection files remain part of the declared dependency base rather than this card's new content. The live dispatch failure is credibly isolated from these content changes: workflow policy/source checks and the unit/package test step passed, including `internal/metrics`; the failure was in the distinct runtime integration step and was reproduced/classified in the round-4 evidence. The remaining skipped jobs are not counted as passed.

Two acceptance points remain unproven. First, exact-head source search found no production or non-test caller of `BuildPersesInfraDashboard` or `VerifyPersesInfraDashboard`; the only references are in the dashboard source and its tests. Thus the new live-query verifier is not reached from a product path. Second, the positive/negative query tests use `seriesScriptProbe` scripted answers. They prove per-panel state logic, but no artifact records a real query against the materialized Prometheus endpoint, as required by task 0428-082 (“Execute at least one real Prometheus query”). Upstream model fragments are pinned and checked, but the tests compare selected fragments and golden output rather than invoking the pinned upstream Perses validator.

**Qualification judgment:** the exact-head dispatch run plus the cell replay is sufficient to classify the unrelated runtime failures and to credit the passing exact-head source/unit tests. It is not sufficient to close the card's missing live-query/product-path acceptance. No rerun of the same unrelated six-test runtime set is requested solely to clear its diagnosed runner failures.

**Recipe:** connect the dashboard builder/verifier to the intended production verification path so it is actually exercised. Provide a reproducible witness at this candidate or its correction that issues at least one real `/api/v1/query` against a materialized Prometheus endpoint and records the returned scrape series and source scope. Validate the serialized resource with the pinned Perses schema/model validator (or an existing CI gate that performs that validation), rather than only substring checks against source excerpts. Route those focused checks through a durable CI/native gate; keep the already-passing dashboard unit coverage and 0428-080 tests intact. Obtain exact-head evidence for the new production path/schema validation; the existing unrelated runtime test failures need only be rerun if the chosen gate actually depends on them.

### Object 3 — Demo #164 / 0428-099: APPROVE CONTENT

The changed prompt matchers in `tests/guided/drive.py` and `tests/guided/new_edit.py` explicitly accept both `Achtung:` and `Warning:`. No matcher was narrowed to the new marker. `test_20_dual_match_accepts_achtung_and_warning_confirm_prompts` drives the post-rename Warning flow through the production consent flow to READY. The prior Achtung literal remains in the alternation, the legacy transcript fixtures retain Achtung examples, and the unrelated deletion-consent negative control remains unchanged. The exact-head Guided consent `workflow_dispatch` run passed with the regression suite. This is adequate for the requested dual-match consumer change; no Core files or workflow files were changed.

## Review limits and state

All three PRs remain OPEN and DRAFT. No GitHub approval, ready transition, candidate edit, or merge was made. The review did not alter product checkouts. The local demo checkout already contained untracked `.tools/` and Python `__pycache__` directories; they were left untouched.

## END

END_DONE mission-luna-batch18 — #1666 REQUEST CHANGES; #1665 REQUEST CHANGES; Demo #164 APPROVE CONTENT. Evidence distinguishes exact-head test successes from skipped checks and the unrelated runtime failure. No merge.
