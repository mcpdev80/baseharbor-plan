# PLAN — 078-r2 chain (mission-identity-078-r2-chain)

Lane: lane-0428-078-perses-identity-on-resolver
Card: t-20261114-r28-perses-dashboard-identity
Date: 2026-11-16
Base attest: fd82668f1 (lane-0428-080-r28-perses-selection, #1590 r3, APPROVE CONTENT)
Candidate: c8430f826 (rebased onto fd82668f1)

## Steps

- Rebase commit c8430f826 from base 1781277d3 onto fd82668f1 via a new merge-commit against the r3 head (no force-push). Fresh branch verified by ls-remote before/after push; FF push on lane-0428-078-perses-identity-on-resolver. PR #1650 stays draft (isDraft checked before/after).
- Clean up duplicate identity-catalog API/key names present in my diff vs the old base: reconcile the new DashboardBackendKeycloak / "keycloak" const and the "identity-keycloak" catalog key + test references against the r3 DashboardBackendIdentity / keycloak-identity API. No content change, only name reconciliation against the moved base.
- Production status-result call-site: wire persesStatus in cmd/baha/app_status_result.go through the resolver so identity-keycloak is eligible only via EligibleFor with NonForgeableAvailable + per-backend keycloak signal (fail-closed). Positive test: real keycloak-metrics signal + target-auth; negative tests: unwired/forgeable/falsely-global -> fail-closed. STOP + file:line finding if the resolver surface (witness resolution + backend-signal collection) is missing — no own 080 resolver expansion.
- go build ./... ./cmd/..., go vet, gofmt -l; run ./internal/capability/... + targeted status/metrics tests. Watch the CI validate run to terminal (Eigenes-Run-Pflicht).
- refspec-push + ls-remote attest; keep PR #1650 draft. Write akte evidence/r28-welle2-2026-11-16/perses-dashboard-identity/on-resolver-round-2.md. origin/main witness + END post. Bring down any compose project started.
