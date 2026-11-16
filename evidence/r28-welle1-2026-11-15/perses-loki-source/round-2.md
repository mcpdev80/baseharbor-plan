# 0428-086 — Perses Loki datasource source (round 2, luna-r1 correction)

- lane: lane-0428-086-perses-loki-source
- card: t-20261114-r28-perses-loki-source (0428-086)
- shift: welle2-086
- model: worker-ornith1.5-laptop (agentgateway)
- mission: /tmp/opencode/mission-fix-loki.md
- recipe: evidence/r28-welle1-2026-11-15/perses-loki-source/act-luna-r1.md (REQUEST CHANGES, candidate fdb4f84b47e)

## BASE ATTESTATION

- single-base lane-clone from the AKTUELLEN head of lane-0428-086-perses-loki-source
- base head (ls-remote origin): fdb4f84b47e4c98b1982de16983a994254917ef6 refs/heads/lane-0428-086-perses-loki-source
- base head verified against origin via `git ls-remote origin` BEFORE branch cut/commit
- planning repo attest: `git ls-remote origin main` = e28661a3e8d8bb800063447d5995f0b957c853e8 (refs/heads/main) — planning evidence live on origin/main
- detached HEAD committed ON the lane branch from the exact base head; base SHA fdb4f84b47e is an ancestor of the first commit

## BRANCH PROVENANCE (proof, not claim)

- branch: lane-0428-086-perses-loki-source, already existed on origin at fdb4f84b47e
- cut/committed FROM origin/lane-0428-086-perses-loki-source @ fdb4f84b47e
- base SHA fdb4f84b47e IS an ancestor of my first commit (verifier: `git merge-base --is-ancestor fdb4f84b47e4c98b1982de16983a994254917ef6 HEAD` -> 0)
- `git log --oneline origin/lane-0428-086-perses-loki-source..HEAD` lists ONLY my own commit (no foreign commit)
- exact base SHA in evidence before commit

## DEFECT REPRODUCED (round-1 head fdb4f84b47e)

- internal/logs/loki_datasource.go: LokiDatasourceNow returned only an internal status/target descriptor (LokiDatasource struct with PluginVersion/Target/Status/Reachable), not a Perses datasource resource
- QueryLoki accepted a caller-supplied *http.Client and endpoint string as authority: no binding to the authoritative Loki service-access policy/transport, so the claimed service-access TLS/authorization boundary was not enforced by this API
- the Loki plugin version was a mutable local const (LokiPluginVersion = "v0.6.0") with no seam pin; the seam PersesRelease only pins PrometheusPluginVersion
- ValidateLokiDatasourceSource was a separate, unused-by-builder check

## FIX SUMMARY (vs recipe act-luna-r1)

- File/change: internal/logs/loki_datasource.go (rewritten)
  - BuildPersesLokiDatasource now produces the native Perses LokiDatasource resource (Kind = "LokiDatasource", spec.plugin.kind = LokiDatasource) via a Go-struct-first realization that marshals to the Perses-native datasource/document format (same pattern as internal/metrics/perses_prometheus_datasource.go and the lane's internal/metrics/perses_tempo_datasource.go). The structs are the source of truth; the committed golden witness is their marshalling. No go:embed of datasource JSON.
  - Binds, fail-closed, to the AUTHORITATIVE, manifest-resolved Loki service-access path:
    - capability.ValidatePersesRelease(release) — pinned release that validates
    - observability management UI + Perses selected in the manifest (m.Services.ObservabilityManagementUI && m.Services.Perses) — no datasource for an unselected surface
    - ExistingProviderFiles(m) + ProviderEndpoint(files) — materialized Loki query-api endpoint over the runtime TLS boundary; a missing endpoint propagates as an error, never a fabricated empty URL
    - readRuntimeLogSourceSnapshot (new internal/logs/runtime_log_source_snapshot.go) — the retained, owner-protected runtime log-source snapshot of THIS provider (project/scope/owner validated); missing/denied/foreign-owned source propagates as an error
    - lokiDatasourceHTTPClient — the seam's managed Loki query client bound to serviceaccess.Resolve("loki", MTLS) + ExistingTLSMaterial + NewHTTPClientForPolicy; a caller-supplied client is never the authority
  - "verified" reachability requires a REAL Loki query over the service-access TLS client (BuildPersesLokiDatasourceWithProbe + VerifyPersesLokiDatasourceHealth); pin validation alone never passes
  - Removed the old LokiDatasourceNow/QueryLoki/LokiDatasourceOwner/LokiQuery public API and the obsolete internal/logs/loki_datasource_test.go
  - No secret material (mTLS, CA, key, token) is materialized into the descriptor or returned from the client
- File/change: internal/logs/runtime_log_source_snapshot.go (new) — owner-protected Loki log-source snapshot reader mirroring the metrics runtime-sources contract
- File/change: internal/logs/loki_test.go (rewritten) — native-resource + owner + no-capability-claim + no-secret + fail-closed (unselected/absent-provider/absent-source/foreign-owned/absent-endpoint) + verify-fail-closed + real-query + golden + reachability-unverified cells
- File/change: internal/logs/testdata/perses-loki-datasource/loki.json (new golden witness)
- scope: command only; nothing rebuilt around it. The seam pin remains an Owner finding (below).

## TESTS / BUILD / VET (witnesses)

```
$ gofmt -l internal/logs/loki_datasource.go internal/logs/loki_test.go internal/logs/runtime_log_source_snapshot.go
(empty = clean)
$ go build ./...
(no output)
$ go vet ./...
(no output)
$ go test ./internal/logs/
ok  	github.com/mcpdev80/baseharbor/internal/logs	0.029s
$ go test ./internal/logs/ -run TestPersesLoki -v
--- PASS: TestPersesLokiDatasourceEmitsNativeResource
--- PASS: TestPersesLokiDatasourceNamesLokiOwner
--- PASS: TestPersesLokiDatasourceNoCapabilityClaim
--- PASS: TestPersesLokiDatasourceNoSecretInDescriptor
--- PASS: TestPersesLokiDatasourceFailClosedWhenUnselected
--- PASS: TestPersesLokiDatasourceFailClosedWhenProviderAbsent
--- PASS: TestPersesLokiDatasourceFailClosedWhenSourceAbsent
--- PASS: TestPersesLokiDatasourceFailClosedWhenForeignOwned
--- PASS: TestPersesLokiDatasourceFailClosedWhenEndpointAbsent
--- PASS: TestPersesLokiDatasourceVerifyFailsClosedWithoutProbe
--- PASS: TestPersesLokiDatasourceVerifyNeverReportsHealthy
--- PASS: TestPersesLokiDatasourceVerifyBindsServiceAccessClient
--- PASS: TestPersesLokiDatasourceGoldenFiles
--- PASS: TestPersesLokiDatasourceReachabilityUnverified
```

- All existing logs tests still pass (no regression from removing the obsolete loki_datasource_test.go).

## CI COVERAGE (Owner directive 2026-11-07)

- changed/new paths: internal/logs/*.go + internal/logs/testdata/*.json
- CI job that runs it: `.github/workflows/ci.yml` "Test" job, `go test ./...` (runs `./contracts/... ./internal/... ./spec/...`), trigger `pull_request` on paths including `**.go` — my draft PR #1616 fires this. My new tests run under that group.
- second coverage: `.github/workflows/targeted-integration.yml` "Shared provider unit and contract verification" job runs `go test ./...` + `go vet ./...`, `workflow_dispatch` by coordinator.
- No `.github/**` change was needed or made (Owner scope). No test is VM-only or local-only; every new test runs under the CI unit group above.

## EVIDENCE COMMITTED TO origin/main

- `git ls-remote origin main` before push: (see above)
- evidence committed to planning repo; commit on origin/main after push: 97107d87423dce243f335bae071d0040a6fc4627
- ls-remote origin main after evidence push: 97107d87423dce243f335bae071d0040a6fc4627 (refs/heads/main)

## PUSH WITNESSES

```
$ git ls-remote origin refs/heads/lane-0428-086-perses-loki-source
787fe6ca363e9154c77284c98414cd00b5c5ac00	refs/heads/lane-0428-086-perses-loki-source
$ git log --oneline origin/lane-0428-086-perses-loki-source..HEAD
787fe6ca3 fix(0428-086): emit native Perses LokiDatasource bound to service-access path (luna-r1)
```

- Exactly one commit on the branch, mine only (no foreign commit). Base fdb4f84b47e is an ancestor.

## SCOPE / STOP NOTES

- Seam pin (capability/perses.go PersesRelease.LokiPluginVersion) is OUT OF SCOPE (Owner seam file). The recipe says move the pin into the seam-owned PersesRelease contract through the coordinator/Owner. Owner decision (2026-11-16): add field `LokiPluginVersion string` to capability/perses.go PersesRelease (PersesRelease struct) and set it in PersesDefaultRelease (~perses.go:151) to the pinned Loki plugin version ("v0.6.0"); then this adapter reads the pin back from the seam instead of the local const in internal/logs/loki_datasource.go. Reported as STATE for the Owner; NOT edited.
- No merge, no ready_for_review, no force-push, no release. PR #1616 stays draft, base lane-0428-075-perses-seam unchanged.
- No containers/compose started this lane; nothing to bring down. Host-local writes: worktree under /tmp/opencode/w086loki only.

## repo-rule compliance

- Write-set: ONLY internal/logs/loki_datasource.go, internal/logs/loki_test.go, internal/logs/runtime_log_source_snapshot.go, internal/logs/testdata/perses-loki-datasource/loki.json; removed internal/logs/loki_datasource_test.go. No seam, no shared catalog, no .github/**. No merge / ready_for_review / force-push below base.
- No subagents (§4.8); all work in this session.
- Single base; branch provenance verified via git ls-remote + merge-base ancestor check.

## END status

- PR: https://github.com/mcpdev80/baseharbor/pull/1616 (DRAFT, isDraft=true, base lane-0428-075-perses-seam)
- head SHA: 787fe6ca363e9154c77284c98414cd00b5c5ac00
- NOT ready_for_review, NOT merged ✓
