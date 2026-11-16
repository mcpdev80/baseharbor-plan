# CODEX-REVIEW — PR #1608

**ROLLE: REVIEW**  
**Task:** `t-20261114-r28-perses-datasources`  
**Candidate:** `c77c76870dc0245d7f7e6be4caf13b562435dd6e`  
**Exact-head CI:** run `43794449582`, COMPLETED SUCCESS, exact SHA; `./internal/metrics` passed.  
**Scope:** base is seam branch at `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`; approved seam head was `492b8e8f994b16e6f73819a08175f8178cd63292`. `66ff93d` is the merge of that seam and develop `14d8f17`; `492..66ff` is develop-sync content, while the merge’s delta over develop parent is the 20-file seam. PR-authored files are the datasource implementation, test, and golden. `git diff --check` clean.

## Verdict: REQUEST CHANGES

`internal/metrics/perses_prometheus_datasource.go` documents that pin validation alone must not pass health verification, but `VerifyPersesPrometheusDatasourceHealth` returns success for a valid pinned release without a live health/query probe. The test currently expects that success. In addition, the builder suppresses errors from `persesPrometheusDatasourceURL` and can return a default datasource with empty config and nil error. This does not meet the task’s requirement for an authorized existing Prometheus source and an actual query, and can misrepresent unavailable/denied configuration as usable.

## Recipe

- **File/change:** `internal/metrics/perses_prometheus_datasource.go`; propagate missing, denied, and invalid source errors; do not report verified/healthy based on pin validation alone. Tie construction to a selected/authorized manifest source and require the real health/query result before success.
- **Tests:** replace the nil-on-pinned-only expectation; cover absent/unselected/denied source, bad URL, and a real query/health success path, asserting the exact query and TLS/CA/credential handling. Validate the emitted datasource shape against pinned Perses v0.55.1, not only the local model. Ensure package CI selects these tests.
- **Stop:** stop if no authorized Prometheus source or runnable health/query path exists; report unavailable instead of manufacturing a successful default.

Read-only review; no merge performed.
