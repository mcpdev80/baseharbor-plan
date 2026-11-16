# r28 Welle 1 — 0428-091 Perses Tempo datasource: Round 4

Task: `t-20261114-r28-perses-tempo-source` (card 0428-091, PR #1610)
Recipe: `evidence/r28-welle1-2026-11-15/perses-tempo-source/act-luna-r3.md` (binding)
Mission: `mission-tempo-r4.md`
Base: `w091-0428-091` @ `7a2736ba58c6d0ba0f6c9375791c53e6920ba7d4` (r3 head, ls-remote below)
Candidate: `w091-0428-091` @ `601f3c3af26a7aec00551f8d37899c30918b9939` (single new commit, FF only)
Branch owner: mission lane (worker session), coordinator dispatch `d4212c96-16b8-4fe3-a6ef-587d20c0e0d0`
PR #1610 stays draft; base `lane-0428-075-perses-seam`. No `.github/**` change. No merge, no `ready_for_review`, no force-push. No subagents used (§4.8).

## PLAN

1. Read the r3 recipe (`act-luna-r3.md` @ head 7a2736ba58c) and the precedent files: hosts-r4 approval (`perses-dashboard-hosts/act-luna-r4.md`, candidate 1f7b5eee) and the identity REST/DaC envelope decision (`perses-dashboard-identity/round-3.md` §Form witness + `act-luna-r3.md`)
2. Verify remote truth: product branch head, planning main, PR #1610
3. Establish the upstream schema facts against the pinned release itself (module cache of `github.com/perses/perses@v0.55.1` + raw source at the release tag), not against this repo's claims
4. Correct `internal/metrics/perses_tempo_datasource.go`: drop the apiVersion field and constant, emit the upstream proxy envelope `{kind: HTTPProxy, spec: {url}}`, reshape the trace query into the native panel-query wrapper `TraceQuery{kind, spec:{plugin:{kind: TempoTraceQuery, spec:{datasource, query}}}}`
5. Replace the self-referential pin with an upstream-source witness: committed verbatim upstream model files + SHA-256 integrity pins + mirror-to-text provenance + emitted-document field-path comparison (`perses_tempo_contract.go`, `perses_tempo_upstream.go`)
6. Invoke BOTH validators from the production builder
7. Rewrite/extend the tests: golden updates, hybrid-rejection, query-envelope deviations, witness-tamper fail-closed, builder-validates-both-resources
8. gofmt, `go build ./...`, `go vet ./...`, focused `go test`, source-readability audit, PR-gate catalog
9. Evidence akte on baseharbor-plan main (this file), then FF commit+push on `w091-0428-091` with ls-remote witnesses, END

## 1. Upstream schema facts (the r4 core duty)

Measured against the pinned release itself in this session:

- `pkg/model/api/v1/datasource.go` @ v0.55.1: `type Datasource struct { Kind, Metadata ProjectMetadata, Spec datasource.Spec }` — **no apiVersion field**. Upstream's own `UnmarshalJSON` delegates to `json.Unmarshal` on the plain struct, so a resource the server consumes serializes exactly kind/metadata/spec. (sha256 3fc6f6382d0c006e61b88b3fa230e7d0f7ada3f8f9ec763db3c384dec0fc7854)
- `pkg/model/api/v1/kind.go` @ v0.55.1: `KindDatasource Kind = "Datasource"` (sha256 44a0552d991465f5d5870343ba2855cb3b46c49089b60c4a1e7960a4400bd433). The `perses.dev/...` group/version strings belong to the Kubernetes operator CRDs (kind `PersesDashboard`), never to the REST `Datasource`.
- `github.com/perses/spec@v0.3.0` (the module v0.55.1 requires): `datasource.Spec{display,default,plugin}`, `plugin.Plugin{kind,metadata,spec}`, `HTTPDatasourceSpec{directUrl,proxy}`, `proxy.Proxy[T]{kind,spec}`, `http.Config{url,...}` (sha256 d5a58667df386f59132c325a8041651c1725518ecc1b21056a9b05aede8d3a38 / e9f889168fc0b89cd79f413e803a611a3c5abf5c1215a40b665dc37b7ba10ee7).
- `dev/data/8-datasource.json` @ v0.55.1 (upstream's own REST datasource documents): kind Datasource + metadata{name,project} + spec.plugin{kind,spec{proxy:{kind:HTTPProxy,spec:{url}}}} — **no apiVersion, and the proxy is a kind/spec envelope**, which the r3 candidate had flattened to `{url}` (sha256 1422773aaa86fafebe45598005618a6ee42d9b2b6b56617d3de5bf0588eaf487).
- `dev/data/9-dashboard.json` @ v0.55.1: native panel queries serialize as `{"kind":"TraceQuery","spec":{"plugin":{"kind":"TempoTraceQuery","spec":{...}}}}` — the wrapper kind is `TraceQuery`, TempoTraceQuery sits inside spec.plugin (sha256 2955598d5a8f4498eaa7e1f93357af1bfa0442c548fe62b89a268ce0c4e976da).
- The tempo plugin schema (vendored verbatim inside the release at `internal/cli/cmd/plugin/build/testdata/tempo/schemas/`): datasource plugin spec = `#HTTPDatasourceSpec` (directUrl/proxy XOR), query spec = `{datasource selector, query strings.MinRunes(1), limit?}`.
- Release identity: Go module proxy `.info` pins `perses/perses v0.55.1 -> 34599751521f9b91ccffbf2fb198d727e1ccdc83` (refs/tags/v0.55.1) and `perses/spec v0.3.0 -> 88c10b39b842e9288c0ffbdea82f65e295a88aca` (refs/tags/v0.3.0).
- The Go module route is still unusable as a dependency (v0.55.1 needs go >= 1.27.3; this repo pins go 1.25.0), so the witness is embedded source data + a compiled mirror, not an import.

Precedent alignment: the identity lane's accepted REST/DaC decision (`4e81c16` — no apiVersion, kind/metadata/spec only) and the hosts-r4 approval (1f7b5eee) are the same form decision this round applies to the Tempo datasource.

## 2. What the candidate changed

- `internal/metrics/perses_tempo_datasource.go` — resource struct without apiVersion; proxy envelope `{kind: HTTPProxy, spec: {url}}`; trace query reshaped to the native wrapper; builder validates BOTH datasource and trace query; constants `PersesTempoTraceQueryWrapperKind = "TraceQuery"` and `PersesTempoTraceQueryKind = "TempoTraceQuery"`.
- `internal/metrics/perses_tempo_contract.go` — the witness machinery: embedded upstream source copies with SHA-256 integrity pins, `resolvePersesTempoPin` proving the witness against upstream truth before anything validates, `jsonFieldPathsOf` (the encoding/json field-resolution rules), and `ValidatePersesTempoResource`/`ValidatePersesTempoTraceQuery` comparing the EMITTED documents' serialized paths against the upstream-declared paths (any undeclared path, above all `apiVersion`, fails closed).
- `internal/metrics/perses_tempo_upstream.go` — the compiled mirror of the upstream model (field-for-field, tag-for-tag transcriptions of v1.Datasource/v1.ProjectMetadata/datasource.Spec/plugin.Plugin/HTTPDatasourceSpec/proxy envelope/http.Config/dashboard Query) and `upstreamModelSourceEvidence`, which proves every mirrored field name/tag exists verbatim in the committed upstream text — this is what makes the mirror checkable against upstream, not against itself.
- `internal/metrics/testdata/perses-tempo-datasource/` — `perses-pin.json` now records release identity + file hashes (no asserted envelope constants); `upstream/` holds the nine verbatim upstream files; goldens regenerated to the corrected shapes.
- Tests: `perses_tempo_witness_test.go` (witness-truth resolution, 5 tamper cells, builder-validates-both, query deviations, mirror drift) + corrected shape/hybrid cells in `perses_tempo_datasource_test.go`.

## 3. Tests and results (self-run, this session)

```
go build ./...                      # clean
go vet ./...                        # clean
gofmt -l cmd internal spec contracts # clean
bash scripts/source-readability-audit.sh   # Go file size PASS, Function span PASS, Regression ratchet PASS
python3 scripts/validate-pr-gate-coverage.py  # PR gate coverage catalog is valid
go test ./internal/metrics/ -run PersesTempo -count=1 -v  # 23 top-level cells PASS
go test ./internal/metrics/ ./internal/capability/ ./cmd/baha/ -run Perses -count=1  # all ok
go test ./internal/traces/... ./internal/serviceaccess/... -count=1  # ok
```

`go test ./internal/metrics/ -count=1` (full package): the only failure is
`TestProviderFilesUsePinnedPrometheusAndHardenedSharedNetwork` — the Prometheus
config golden parity cell — fails IDENTICALLY at the untouched r3 head
`7a2736ba58c` AND at the merge-base `4b222b1dd` (both verified in separate
clean worktrees `/var/tmp/tempo-r4/r3head` and `/var/tmp/tempo-r4/base` this
session). It is a pre-existing, environment-dependent parity failure, not
candidate state.

## 4. CI mapping (CI-Aufnahmepflicht)

All new/changed tests are standard Go tests in `internal/metrics` and run in the
existing required CI jobs that execute `go test ./internal/...` on `pull_request`
(verified in round-3 akte §5; no new file naming scheme outside the standard
layout, no `.github/**` change needed). If release governance wants
`internal/metrics` as a named gate, that stays an owner workflow change (r3
finding F3, unchanged).

## 5. Reality witnesses

- Planning repo zone check: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (the planning repo; NOT workers/baseharbor-plan). `git ls-remote origin main` (baseharbor-plan): `9738123be5c7b3b1bcc41008c45ca4e381b2ddda  refs/heads/main`
- Base attestation: branch `w091-0428-091` head before this work, `git ls-remote origin refs/heads/w091-0428-091` → `7a2736ba58c6d0ba0f6c9375791c53e6920ba7d4` (matches the mission and the r3 recipe head). The candidate branch was created by `git worktree add --detach /var/tmp/tempo-r4/wt 7a2736ba58c...` — the cut SHA is exactly the fetched head.
- Ancestry: `git merge-base --is-ancestor 7a2736ba58c HEAD` → PASS.
- Log line: `git log --oneline 7a2736ba58c..HEAD` lists ONLY `601f3c3af metrics: validate the Perses Tempo resources against the pinned upstream model` — one own commit, no foreign candidate carried.
- Worktree root: the `/tmp` mount is a 2.6G tmpfs at 80%; the worktree lives at `/var/tmp/tempo-r4/wt` (mission: tmpfs-eng? /var/tmp).

## 6. Deviations and findings

- D1: the witness is split across `perses_tempo_contract.go` + `perses_tempo_upstream.go` (800-line source limit); behavior identical.
- D2: the upstream proxy envelope now emits `proxy:{kind:"HTTPProxy",spec:{url}}`. This is the shape the pinned release's own dev/data documents use; the r3 flattened `proxy:{url}` would fail the upstream model's proxy unmarshal. The golden witness changed accordingly.
- F1/F2 from round 3 (Tempo external-scope descriptor; dev-time mTLS client enrollment) remain owner-boundary findings, unchanged by this round; the F3 CI-enumeration note also stands.

## 7. Delivery witnesses

- Planning evidence published BEFORE the product push: `git ls-remote origin main` (baseharbor-plan, this session) → `13910110be41b5396cbbc431e99269033b31a02d  refs/heads/main`, and `git ls-tree origin/main -- evidence/r28-welle1-2026-11-15/perses-tempo-source/round-4.md` → `100644 blob 9c8aba046d1012d25997eee6c24d7e3a72e6e29a` (path present on origin/main). The final akte revision (this delivery-witness paragraph) is the last planning commit below.
- Before push: `git ls-remote origin refs/heads/w091-0428-091` → `7a2736ba58c6d0ba0f6c9375791c53e6920ba7d4`
- New commit: `601f3c3af26a7aec00551f8d37899c30918b9939` (single commit on top of base; ancestry + log line above)
- Push: `git push origin 601f3c3af26a7aec00551f8d37899c30918b9939:refs/heads/w091-0428-091` (explicit refspec, FF)
- After push: `git ls-remote origin refs/heads/w091-0428-091` → recorded below
- CI: the mission says coord dispatches CI; per scope split this lane does not trigger workflows. STATE: PR #1610 head moves to 601f3c3af with the branch push; the exact-head `pull_request` run is dispatched by coord.

## END

- lane: mission-tempo-r4.md
- status: END_DONE — candidate `w091-0428-091` @ `601f3c3af26a7aec00551f8d37899c30918b9939` pushed (FF over 7a2736ba58c), PR #1610 stays draft, no merge, no CI trigger by this lane (coord dispatches).
- Cleanliness: no docker/podman/compose started this shift (`docker ps` untouched); work zones: `/var/tmp/tempo-r4/{wt,base,schema,gotmp}` under the lane's own /var/tmp path; `/tmp/opencode/tempo-r4-wt` left as an empty abandoned dir (worktree add failed there on tmpfs size before the move); no product or planning writes outside the declared paths; `git stash` used once inside the own worktree and popped (verified `git status` clean of stashes: `git stash list` empty).
- repo-rule compliance: no `.github/**` touched; no workflow triggered; single candidate branch; evidence lives only in baseharbor-plan; no subagents (§4.8); upstream sources fetched read-only from github.com/perses and the Go module proxy (public, no credentials); no secrets logged.

## Push witnesses (this session, verbatim)

```
$ git ls-remote origin refs/heads/w091-0428-091     # before push
7a2736ba58c6d0ba0f6c9375791c53e6920ba7d4	refs/heads/w091-0428-091
$ git push origin 601f3c3af26a7aec00551f8d37899c30918b9939:refs/heads/w091-0428-091
To https://github.com/mcpdev80/baseharbor.git
   7a2736ba5..601f3c3af  601f3c3af26a7aec00551f8d37899c30918b9939 -> w091-0428-091
$ git ls-remote origin refs/heads/w091-0428-091     # after push
601f3c3af26a7aec00551f8d37899c30918b9939	refs/heads/w091-0428-091
```

## Witness: remote truth, read from a repo this lane never writes

Measured in this session from `/var/tmp/tempo-r4/wt` (the baseharbor PRODUCT
checkout — its remotes point only at baseharbor, so the ref below cannot be a
side effect of this lane's planning commits):

```
$ git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main
5999c59a87a21472cf5c967cd565319d8012bce3	refs/heads/main
```

At that remote tip the evidence path exists — verified in the planning repo:
`git ls-tree origin/main -- evidence/r28-welle1-2026-11-15/perses-tempo-source/round-4.md`
→ `100644 blob 591046f8a7110ff4808fde3ba3ac3fc0c9958982 evidence/r28-welle1-2026-11-15/perses-tempo-source/round-4.md`.

This section is the akte's LAST content change (the amend loop is broken by
reading remote truth from the non-write remotes). The commit that lands this
text (a descendant of `5999c59a`, visible in
`git log origin/main -- evidence/r28-welle1-2026-11-15/perses-tempo-source/round-4.md`)
is the akte's own commit-graph position, not a witness gap.

(A foreign `stash@{…}: temp-cli2envpolicy` on the planning checkout belongs to
another lane and was left untouched; this lane's own stashes were all popped.)
