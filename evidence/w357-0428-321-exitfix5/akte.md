# w357-0428-321-exitfix5 — 0428-321 / PR #1866 — END + disposition (2026-11-27)

- Head: 3702c09502203e82633d664690eac9484a370df9 (parents abeba2c1a + c167fa5d323), branch w334-0428-321-exitcodedocs, canonical w357 identity (4-field verified).
- Exact-head runs: 45906926997 (abeba2c1, pre-#1872) FAILURE; 45909111789 (3702c095) FAILURE.
- Independent coordinator log verification (job 140213421376 of 45909111789): Selected Runtime gates abort at fixture bootstrap —
  caddy `no upstreams available` (http.log.error), postgres `SSL error: unexpected eof while reading`, then
  `RuntimeError: guided up abort (first_rc=2); consent not completed` (tests/guided/drive.py:749).
  Plain `PR · Native · native/{docker,podman}/data-capabilities` jobs SUCCESS in the same run.
- Disposition: environment/runner-health defect on the Selected-Runtime fixture path, NOT attributable to the 0428-321 exit-code diff
  (no 137/143/130 signal; product runtime code never entered). PR comment: issuecomment-7205758779.
- Card state: blocked-external. No further retries until environment recovery; then fresh exact-head run + Codex review. No merge on 3702c095.
