# r28 Welle 1 — 0428-091 Perses Tempo datasource: Round 3

Task: `t-20261114-r28-perses-tempo-source` (card 0428-091, PR #1610)
Recipe: `evidence/r28-welle1-2026-11-15/perses-tempo-source/act-luna-r2.md` (binding)
Base: `w091-0428-091` @ `4b222b1dd5b55ca0ff427f54663e235f25e984e1`
Candidate: `w091-0428-091` @ `7a2736ba58c6d0ba0f6c9375791c53e6920ba7d4` (new commit, no amend)
Branch owner: mission lane `mission-fix-tempo.md` (worker session), Coordinator dispatch `d4212c96-16b8-4fe3-a6ef-587d20c0e0d0`
PR #1610 stays draft; base `lane-0428-075-perses-seam`. No `.github/**` change. No merge, no `ready_for_review`, no force-push. No subagents used.

## 1. Plan (numbered, as executed)

1. Reproduce the finding at base `4b222b1dd`: constant `PersesTempoDatasourceKind = "TraceDatasource"`, flattened document, no native resource validation, no trace-query path. Confirmed in `internal/metrics/perses_tempo_datasource.go`.
2. Re-verify upstream truth for the pinned Perses release `v0.55.1`: native datasource plugin kind `TempoDatasource`, trace-query plugin kind `TempoTraceQuery`, REST resource envelope `Datasource` (`perses.dev/v1` group) with `metadata{name,project}` and `spec.plugin{kind,spec}`; Tempo's own search API is `GET /api/search?...&format=json&q=<traceql>`. The Go module route is unusable (`github.com/perses/perses@v0.55.1` needs go 1.27.3; this repo pins go 1.25.0 / toolchain go1.26.9), so the contract is witness data, not an import.
3. Emit the native envelope: `apiVersion: perses.dev/v1`, `kind: Datasource`, project-scoped metadata `baseharbor`/`baseharbor-tempo`, `spec.default: true`, `spec.plugin.kind: TempoDatasource` with `spec.plugin.spec.proxy.url` only (no `directUrl`) — the shape the accepted sibling adapter (PR #1608, Prometheus) uses.
4. Add native resource validation against a committed upstream contract witness (`internal/metrics/testdata/perses-tempo-datasource/perses-pin.json`, `go:embed`-ed as `PersesTempoPinSource` so validation is working-directory independent): `ValidatePersesTempoResource` and `ValidatePersesTempoTraceQuery` fail closed on a flattened document, a self-invented plugin kind, a wrong resource kind, a `directUrl` bypass, missing proxy/scope, or an incomplete witness.
5. Implement a real trace query: `queryPersesTempoTrace` performs an actual TraceQL spanset query (`{ .resource["service.name"] == "<app>" }`) against Tempo's `/api/search` over the authorized Tempo service-access client (`tempoProviderHTTPClient` → `serviceaccess.NewHTTPClientForPolicy`). Reachability is `verified` only from observed trace ids; a clean empty answer stays `unverified`; a transport/HTTP failure errors.
6. Keep the observation axes honest: `BuildPersesTempoDatasource` performs no live observation (always `unverified`) but still resolves the authorized source and fails closed on absent/external/unmaterialized/denied state; `buildVerifiedPersesTempoDatasource` additionally answers through the production client, so an injected script can neither paper over the production path nor verify against a listener the provider identity does not cover.
7. Rewrite the test cells (`perses_tempo_datasource_test.go` + new `perses_tempo_fixture_test.go`) and generate golden witnesses; delete the superseded flat golden `testdata/perses-tempo-datasource/tempo.json`, add `tempo-datasource.json` and `tempo-trace-query.json`.
8. Run the checks, commit as a new commit on `w091-0428-091`, push with explicit refspec with ls-remote witnesses, and write this akte.

## 2. Reproduction of the finding (before)

At `4b222b1dd` the adapter declared `PersesTempoDatasourceKind = "TraceDatasource"`, emitted a flat `{kind,name,owner,url}` document with no Perses resource envelope, performed no upstream-contract validation, and had no query path: reachability was asserted without an observation. Both round-1 and round-2 candidates kept that shape; Luna's round-2 verdict demanded the native `TempoDatasource` envelope, real resource validation and a real trace query. All three are fixed in the candidate.

## 3. What the candidate does

- `internal/metrics/perses_tempo_datasource.go` — adapter, native envelope build, real TraceQL query, verification paths, source resolution.
- `internal/metrics/perses_tempo_contract.go` — pinned upstream contract witness types, `go:embed` source, native validation (split to stay inside the 800-line source limit of `scripts/source-readability-audit.sh`; the split is a deviation, see §6).
- `internal/metrics/perses_tempo_errors.go` — the fail-closed verdict errors.
- `internal/testsupport/serviceissuer/issuer.go` — added `CertificateFor` so TLS fixtures can present certificates signed by the very test issuer that materializes the provider PKI (fixture support, not product code).
- goldens + witness under `internal/metrics/testdata/perses-tempo-datasource/`.

## 4. Tests and results (verbatim tails)

Commands (worktree `/var/tmp/w091-r3-wt`):

```
go build ./...                      # clean
go vet ./...                        # clean
gofmt -l cmd internal spec contracts # clean
bash scripts/source-readability-audit.sh
python3 scripts/validate-pr-gate-coverage.py
go test ./internal/metrics/ -count=1
go test ./internal/metrics/ ./internal/capability/ ./cmd/baha/ -run Perses -count=1
go test ./internal/traces/... ./internal/application/... ./internal/capability/... ./internal/serviceaccess/... -count=1
```

Results:

```
source readability: Go file size PASS (<= 800 lines ...), Function span PASS, Regression ratchet PASS
PR gate coverage catalog is valid
ok  github.com/mcpdev80/baseharbor/internal/metrics       0.195s
ok  github.com/mcpdev80/baseharbor/internal/capability    0.004s
ok  github.com/mcpdev80/baseharbor/cmd/baha               7.487s
ok  github.com/mcpdev80/baseharbor/internal/traces        0.025s
ok  github.com/mcpdev80/baseharbor/internal/application   6.761s
ok  github.com/mcpdev80/baseharbor/internal/serviceaccess 0.094s
```

Verbose Tempo cell list (`-run TestPersesTempoDatasource -v`), all PASS:

```
--- PASS: TestPersesTempoDatasourceNativeResourceShape
--- PASS: TestPersesTempoDatasourceValidateRejectsNonNativeResource (7 subtests: custom-plugin-kind,
    flattened-document, wrong-resource-kind, direct-url, no-proxy-url, missing-metadata, missing-project)
--- PASS: TestPersesTempoDatasourceRealTraceQueryAnswers
--- PASS: TestPersesTempoDatasourceVerifiedOnlyByRealQuery
--- PASS: TestPersesTempoDatasourceVerifyRequiresRealQuery
--- PASS: TestPersesTempoDatasourceVerifyUsesTheAuthorizedBoundary
--- PASS: TestPersesTempoDatasourceServiceAccessClientEnforcesTrust
--- PASS: TestPersesTempoDatasourceAbsentSourceFailClosed
--- PASS: TestPersesTempoDatasourceExternalSourceFailClosed
--- PASS: TestPersesTempoDatasourceMissingEndpointFailClosed
--- PASS: TestPersesTempoDatasourceDeniedPolicyFailClosed
--- PASS: TestPersesTempoDatasourceTracesUnselectedFailsClosed
--- PASS: TestPersesTempoDatasourceUnselectedPersesFailsClosed
--- PASS: TestPersesTempoDatasourceFailClosedWhenUnpinned
--- PASS: TestPersesTempoDatasourceNamesTempoOwner
--- PASS: TestPersesTempoDatasourceNoSecretInDescriptor
--- PASS: TestPersesTempoDatasourceGoldenFiles
ok  github.com/mcpdev80/baseharbor/internal/metrics       0.035s
```

Full-repo `go test ./internal/...`: only the pre-existing base-parity failures remain
(`internal/controlplaneruntime` and the `internal/database` integration cells require
`BASEHARBOR_TEST_DATABASE_URL`, Owner-triaged as non-candidate state in earlier rounds;
verified identical at base `4b222b1dd` in a throw-away worktree, e.g.
`--- FAIL: TestRunStartsTLSHealthReadinessAndProtectedAPI` fails the same way there).

## 5. CI mapping (recipe point: new tests must be covered by GitHub CI)

The new cells live in `internal/metrics` package tests and are executed by the existing
required jobs of workflow `ci.yml` (`PR · Draft Go · cli-*`, which run
`go test ./internal/...` with the go.mod toolchain). No new test files or naming scheme
outside the standard Go test layout, so no CI change is needed; the package is not
individually enumerated in `scripts/validate-pr-gate-coverage.py` (catalog validates:
"PR gate coverage catalog is valid"). No `.github/**` file was touched; if the integrator
wants `internal/metrics` enumerated as its own gate, that is an owner workflow change
(§6 finding F3).

## 6. Deviations and findings

- D1 (file split): the implementation grew past the 800-line source limit, so the contract
  witness/validation and the verdict errors moved to `perses_tempo_contract.go` and
  `perses_tempo_errors.go`. Pure organization; behavior identical; `source-readability-audit.sh` passes.
- D2 (test-support addition): `serviceissuer.Issuer.CertificateFor` (a few lines in
  `internal/testsupport`) lets fixtures present issuer-signed TLS identities. The alternative
  was hand-rolled self-signed CA fixtures that duplicate the trust chain and prove less. Flagged
  here because it slightly exceeds the recipe's file list.
- F1 (STATE, ownership boundary): `capability.TempoIntegration.SupportedScopes = {shared}`
  (`internal/capability/reference.go`), so an external Tempo placement is not resolvable from
  Core truth and the adapter's `ScopeExternal` fail-closed branch is unreachable from a manifest;
  `TestPersesTempoDatasourceExternalSourceFailClosed` asserts the placement contract refuses it
  and documents the reason. Owner of the descriptor: decide whether Tempo gains the external
  scope; the adapter already fails closed on it.
- F2 (STATE, identity pipeline): `traces.tempoAccessSpec` is `RequireClient: true` and the
  Caddy gateway renders `client_auth mode require_and_verify`, but the managed-local provider
  PKI on disk (`<provider>/service-access/pki`) contains only the server pair — no enrolled
  workload client identity — and `serviceaccess.NewHTTPClientForPolicy` only presents a client
  certificate when `policy.AuthenticationRequired && Authentication == mTLS`, which is false in
  the `dev` default. So the Core Tempo read path (`traces.tempoHTTPClient`) itself presents no
  client cert in dev; the adapter mirrors that exactly (`tempoProviderHTTPClient` keeps the
  resolved policy) and the gateway fixture mirrors the same wire behavior, so no cell can
  verify a path production could not take. A genuine dev-time mTLS read path needs the identity
  pipeline to enroll a client identity into the provider PKI (or BYOC vars) — out of this
  card's write set; recommend a follow-up card.
- F3 (CI enumeration): if release governance wants `internal/metrics` visible as a named gate
  rather than part of the `./internal/...` shard, that is a `.github/**`/catalog change for the
  owner (report only; not done here).

## 7. Delivery witnesses

- Before push: `git ls-remote origin refs/heads/w091-0428-091` → `4b222b1dd5b55ca0ff427f54663e235f25e984e1`
- New commit: `7a2736ba58c6d0ba0f6c9375791c53e6920ba7d4` (single commit on top of base;
  `git log 4b222b1dd..HEAD` lists only this lane's commit; `merge-base --is-ancestor` OK → fast-forward)
- Push: `git push origin HEAD:refs/heads/w091-0428-091` → `4b222b1dd..7a2736ba5  HEAD -> w091-0428-091`
- After push: `git ls-remote origin refs/heads/w091-0428-091` → `7a2736ba58c6d0ba0f6c9375791c53e6920ba7d4`
- PR #1610 head follows the branch automatically; still draft; no review actions taken.

## 8. Handoff

Candidate is ready for CODEX-REVIEW round 3 against `act-luna-r2.md`: native `TempoDatasource`
envelope emitted and validated against the pinned witness (point 1 and 2 of the recipe), real
TraceQL query path with verified-only-by-observation semantics (point 3), fail-closed negatives
with typed verdicts, goldens committed. Findings F1/F2 need owner eyes; they are boundaries of
other cards, not defects of this adapter.
