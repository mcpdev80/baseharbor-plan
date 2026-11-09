# v0.4.27 Target policy: CI recovery and admission foundation (2026-11-09)

## Scope
- Core issue: [baseharbor#1513](https://github.com/mcpdev80/baseharbor/issues/1513)
- Draft PR: [baseharbor#1514](https://github.com/mcpdev80/baseharbor/pull/1514)
- No release or merge authorization; do not mark 0427-023 or the policy work DONE.

## Confirmed CI evidence
- Previous exact-head Actions run [42608030907](https://github.com/mcpdev80/baseharbor/actions/runs/42608030907) failed.
- Observed error: Draft Go package selector included synthetic `./cmd/baha.test` and `./internal/*.test` package paths from `go list -test`.
- Observed error: `TestRunStartsTLSHealthReadinessAndProtectedAPI` lacked `BASEHARBOR_TEST_DATABASE_URL`.
- Commit [a82df08d](https://github.com/mcpdev80/baseharbor/commit/a82df08dcb9f2a96ea9479a77de559cc354f43bf) filters synthetic test packages, adds regression coverage and supplies PostgreSQL to Draft CI.
- Replacement Actions run [42610246646](https://github.com/mcpdev80/baseharbor/actions/runs/42610246646) was still `in_progress` at last inspection; no PASS claim.

## Policy foundation
- Commit [1fe4ee9d](https://github.com/mcpdev80/baseharbor/commit/1fe4ee9ddc0923c5dccfb1781f1beeabcf28947d) adds a Core-domain admission policy evaluator and negative/override regression tests in `internal/deployment`.
- Evidence fields are intentionally unexported: client-supplied branch, dirty, commit or approval flags must never manufacture trusted admission proof.
- No policy continues to preserve backward compatibility. A permissive development preset does not require provenance; a restrictive target fails closed without Core-owned evidence.
- **NOT COMPLETE:** evaluator is not yet wired to the real authorized Candidate ingress/apply path. Verified provenance and Core authorization must be obtained from existing trusted mechanisms before calling it. Full positive/negative runtime and API/MCP tests are outstanding.
- The `0427-023` remote delivery path remains separately open in PR #1473; no local dirty-snapshot delivery or READY acceptance is claimed.

## Next proof
Review source admission/consent implementation and add trusted evidence producer plus atomic Core-side gate ahead of any lifecycle state mutation. Then verify exact-head CI and independent Docker/Podman native E2E. Do not treat domain unit tests as deployment acceptance.
