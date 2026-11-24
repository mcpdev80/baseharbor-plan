# 0428-284 CI test-certificate operator login (round 2)

## PLAN

- Inspect current baseharbor-demo and BaseHarbor `develop` login interfaces and existing demo IdP/env fixtures.
- Prove the available Keycloak X.509 and OIDC headless flow without changing BaseHarbor product authentication or authorization.
- Implement the certificate login only for the CI managed-policy test environment; preserve local behavior.
- Run local tests and the live test-issuer login, qualify the exact hosted PR head twice, merge, and hand off the remaining #1812 runtime qualification.

## Interface findings

- BaseHarbor `develop` supports the existing OIDC Authorization Code + PKCE login and `baha login --no-browser`; `cmd/baha/operator_auth.go:17-18` documents the existing CLI route.
- The auth-code-file hook at `internal/operatorauth/login.go:131-150` reads its file at lines 135-143 before printing the authorization URL at 145-150. A live IdP cannot return a code for the login-generated PKCE challenge before the harness receives that URL. No demo issuer/client/realm/certificate fixture was present in baseharbor-demo.
- Keycloak 26.8.0 can map a mutually authenticated X.509 certificate to an existing realm user in its X.509 browser flow. A live local proof showed the certificate mapped to `ci-test-operator`, Keycloak returned an authorization code to baha's loopback callback, and baha completed PKCE and verified the OIDC ID token. The existing `--no-browser` callback works, so no BaseHarbor source delta is needed.

## Implementation and evidence

- [PR #174](https://github.com/mcpdev80/baseharbor-demo/pull/174) merged into `develop` at `b41127723e523134a1c14ee3c36cf133237162ce`; source head was `b1e1a77bd0e2b0af7d9bf3cf9178be68cad0119f`.
- `tests/policy/run.sh` only provisions and logs in to a test issuer when `CI` is nonempty. The CI policy fixture uses managed `test`; local runs continue using `dev`. `tests/policy/operator-test-certificate.sh` creates an isolated Keycloak 26.8.0 realm, ephemeral CA/server/operator certificates, and an X.509 common-name mapping. The OIDC client is public with Standard Flow and PKCE S256; direct access grants and service accounts are disabled. Baha trusts the generated CA, while curl presents the test operator certificate to Keycloak and follows the code redirect to baha's loopback listener. An EXIT cleanup removes keys, CA data, and the IdP container. Trust-chain details are documented in `tests/policy/README.md`.
- No BaseHarbor product-auth or authorization code, user-facing login, consent check, `.github/**`, or `tests/mcp/**` change. The independent acceptance-reporting fix remains in [PR #173](https://github.com/mcpdev80/baseharbor-demo/pull/173), merged at `87f5b28dc6a3447092389eb7d2790b76a2958bba`.
- Local `python3 -m unittest discover -s tests -p test_fixture_consent.py -v`: 19 passed. `bash -n scripts/acceptance.sh scripts/report.sh tests/lib.sh tests/policy/run.sh tests/policy/operator-test-certificate.sh` and `git diff --check` passed.
- Hosted exact-head workflow run [45455975242](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45455975242) — success on `b1e1a77bd0e2b0af7d9bf3cf9178be68cad0119f`.
- Hosted exact-head witness run [45456155783](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45456155783) — success on the same SHA. Both used manual dispatch because the existing guided-consent workflow's pull-request filter selects `main` and the PR base is `develop`.
- A separate local `whoami` probe reached authorization and was denied because this isolated test identity has no tenant membership. The login itself succeeded; no tenant membership or authorization behavior was added or weakened. The probe is not a claim that the downstream operator authorization gate passed.

## Handoff

- The demo acceptance reporting and test-certificate login changes are delivered and sent to Maintainer review. No BaseHarbor-side change was needed; there is no product-auth delta to escalate.
- #1812 Docker and Podman Light runtime qualification was not run from this demo-only lane per the explicit instruction not to trigger BaseHarbor runtime suites. #1812 remains blocked until that separate runtime qualification is completed.
- The earlier PR #173 failure diagnosis remains: its old candidate run 45447956490 failed first at the stale assertion `tests/test_fixture_consent.py:56`; it was not caused by certificate code or a guided-consent regression.
