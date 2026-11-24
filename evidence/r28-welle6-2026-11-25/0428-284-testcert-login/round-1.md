# 0428-284 acceptance reporting fix and certificate-login handoff (round 1)

## PLAN

- Diagnose PR #173 workflow run 45447956490, which failed on former head `8f706b7d2c0aad81287c0229868850e7157e2077`.
- Identify first failure and distinguish a reporting-test assertion failure from guided-consent or certificate-probe regression.
- Correct the reporting regression test and qualify the exact final source head with two hosted workflow executions.
- Merge only the independent acceptance-group concrete-failure-reporting fix; leave certificate login as an owner decision pending exact IdP inputs.

## PR #173 diagnosis

- PR: https://github.com/mcpdev80/baseharbor-demo/pull/173
- Final source head: `07a12287bf2c22717d9196d91d00217aba86cc12`.
- The initial failed run [45447956490](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45447956490) ran on `8f706b7d2c0aad81287c0229868850e7157e2077`. Its first failure was `tests/test_fixture_consent.py:56`, test `test_policy_gate_has_secret_safe_unexpected_error_diagnostic`, where an assertion still expected the previous diagnostic string `line=%s exit=%s command=%q`. The implementation now reports source file and line. This was a stale assertion, not a cert probe and not a guided-consent behavior regression.
- Corrected the assertion and ran the focused regression: `PYTHONPATH=tests python3 -m unittest test_fixture_consent.ConsentTests.test_policy_gate_has_secret_safe_unexpected_error_diagnostic -v` — passed. Shell syntax checks and `git diff --check` passed.
- Exact final head hosted runs [45448531969](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45448531969) and [45448729972](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45448729972) both succeeded on `07a12287bf2c22717d9196d91d00217aba86cc12`.
- Both successful runs were manual dispatches of the existing guided-consent workflow: its `pull_request` filter targets `main`, but this PR targets `develop`. No workflow files or branch protections were changed.
- PR merged to `develop` at `87f5b28dc6a3447092389eb7d2790b76a2958bba`; remote `develop` was verified at the same merge SHA.

## Scope and remaining owner decision

- Merged change is the demo acceptance-group reporting fix, including `scripts/acceptance.sh`, `scripts/report.sh`, `tests/lib.sh`, `tests/policy/run.sh`, and its regression test. It reports concrete file:line failure detail. No BaseHarbor product-auth, consent, or `.github/**` changes were made.
- The interactive-OIDC policy-gate failure remains open pending the owner test-certificate login ruling. Owner inputs requested: existing IdP issuer/client, test certificate and CA material, and the Keycloak X.509 flow mapping to the operator. The demo tree did not contain an existing realm/client/certificate fixture. No synthetic testonly route or new certificate mechanism was implemented.
- The PR body and Planning card preserve the auth issue as the single open certificate/auth escalation. Any product-auth grant/client-auth requirement must be returned to the owner with its exact source location before work proceeds.
