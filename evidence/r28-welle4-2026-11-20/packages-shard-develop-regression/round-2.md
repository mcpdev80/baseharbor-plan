# 0428-202 · packages shard red on develop — evidence (round 2)

Lane: `w207-0428-202-lokifix` (ornith)
Card: `t-20261120-r28-packages-shard-develop-regression` (0428-202)
Task type: bug · release v0.4.28 · areas ci, observability
Owner (lane): w207-0428-202-lokifix

Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (confirmed via `git -C baseharbor-plan remote -v`)
baseharbor GitHub remote: `origin https://github.com/mcpdev80/baseharbor.git` (only github.com/mcpdev80 remote trusted; this worktree's `origin` and `lane-origin` both resolve to that URL)
Evidence path: `baseharbor-plan/evidence/r28-welle4-2026-11-20/packages-shard-develop-regression/round-2.md`

## RESULT: END_DONE — fix committed, PR #1732, packages shard GREEN

The earlier lane `w202-0428-202-pkgshard` (round-1.md) concluded END_BLOCKED: it located the
failing file and read-only bisected the break to `internal/serviceaccess/policy.go`, then stopped on
the locked write-set. This lane re-read the task card `note-202-lokifix.txt` (card 0428-202, r28),
which states the diagnosis up front: **the bug is NOT `policy.go` — it is a missing client keypair in
the `internal/logs` test fixture**, which is in the writable set.

Read-only re-verification (develop head `40cb28c758b0`, CI job 136526893242 of run 44805066271)
confirms the note exactly:

- Failing cell: `PR · Go unit · packages`. The three tests are
  `TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource` (loki_test.go:522),
  `TestPersesLokiDatasourceMultiSourcePartialMatchability` (loki_test.go:586),
  `TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed` (loki_test.go:633, "expected 2
  per-source queries even on full miss, got 0").
- Verbatim cause: `perses Loki datasource health client: load Loki service access identity: stat
  /tmp/<test>/001/providers/loki/shared/service-access/pki/client-cert.pem: no such file or directory`.
- The culprit: helper `materializeLokiServiceAccessPKI` (internal/logs/loki_test.go:434) writes only
  `ca.pem`, `server-cert.pem`, `server-key.pem` to `filepath.Join(files.Dir,'service-access','pki')`;
  no `client-cert.pem` / `client-key.pem` is ever written.
- The consuming side: `lokiDatasourceHTTPClient` (internal/logs/loki_datasource.go:394-401) calls
  `serviceaccess.Resolve(m.Environment,'loki', AuthenticationMTLS)` (passes) and then
  `serviceaccess.ExistingTLSMaterial(...)` which requires the client material.
- Producer-side layout it must match: `internal/serviceaccess/pki.go:485`
  (`ClientCertificate: filepath.Join(dir,'client-cert.pem')`) — a locked file, out of scope.

## PLAN

1. Read mission + note-202-lokifix.txt; confirm card scope and locked write-set.
2. Attest remote base (origin/develop = 40cb28c758b0) via `git ls-remote`; pick only the github.com/mcpdev80 remote.
3. Cut isolated worktree at develop head (`/tmp/w207-lokifix-wt`); reproduce the three failing tests against develop.
4. Confirm root cause: `materializeLokiServiceAccessPKI` writes ca/server keys only, no client pair.
5. Add ECDSA P256 client cert (ExtKeyUsageClientAuth, 0600) signed by the same test CA, as
   client-cert.pem + client-key.pem in the same pki dir; confirm the capture server loads its server
   cert from the same dir (one shared trust chain, no handshake change).
6. Gate: `go test ./internal/logs/ -run TestPersesLokiDatasourceMultiSource -count=1` (before/after witness).
7. Full: `go test ./internal/logs/ -count=1` (loki_consumer_assertion_test.go path, no new failures) + `go vet`.
8. Commit only internal/logs/*.go in the named branch `lane-0428-202-lokifix`.
9. `gh pr create` (no --draft) on develop base; record that cli-0..3 red = pre-existing 0428-198/owner gate, packages = my fix.
10. Watch hosted CI run to terminal; record PR#, head SHA, base, run-id, conclusion per cell.
11. Write akte; verify evidence path present on origin/main; post END with plan-main SHA.

## repo-rule compliance

- Planning repo confirmed: `git -C baseharbor-plan remote -v` -> `origin https://github.com/mcpdev80/baseharbor-plan.git` (github URL). Evidence written ONLY here, never in a product repo. No `.evidence/` directory anywhere.
- Write-set: `internal/logs/loki_test.go` ONLY. Diff `git diff origin/develop...HEAD --name-only` = `internal/logs/loki_test.go` (one file). `git log --oneline origin/develop..HEAD` lists only my commit `bddb27e62`.
- Locked write-set NOT touched: `internal/serviceaccess/**`, `internal/observability/registry.go`, `internal/capability/perses_selection.go`, `internal/identityprovider/**`, `.github/**`, `go.mod`, `go.sum`.
- Branch provenance: cut from `origin/develop`, `git merge-base --is-ancestor 40cb28c758b02960356434b630086a341ebe1738 HEAD` = YES. base attestation: `git ls-remote origin refs/heads/develop` -> `40cb28c758b0...` (ancestor of first commit).
- No subagents. No `git add -A`. No merge, no force-push. No workflow edits, no `workflow_dispatch`/reruns.
- Isolated worktree only under `/tmp/w207-lokifix-wt`.

## Base attestation

- develop head: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop`
- Branch `lane-0428-202-lokifix` delivered head: `git ls-remote origin refs/heads/lane-0428-202-lokifix` -> `bddb27e6251ec6bc76574a1dcdb13fc7ce017f24 refs/heads/lane-0428-202-lokifix`
- `git merge-base --is-ancestor 40cb28c758b0... HEAD` -> YES (develop is an ancestor of my first commit).
- `git diff origin/develop...HEAD --name-only` -> `internal/logs/loki_test.go`
- `git log --oneline origin/develop..HEAD` -> only `bddb27e62 test(loki): materialize mTLS client keypair in test PKI fixture`

## Fix

`internal/logs/loki_test.go`, inside `materializeLokiServiceAccessPKI`, after the server-key write:
generate a second ECDSA P256 key, build an `x509.Certificate` with `KeyUsage: DigitalSignature|KeyEncipherment`,
`ExtKeyUsage: [ExtKeyUsageClientAuth]`, signed by the same throwaway test CA (`ca`/`caKey`), and write
`client-cert.pem` (CERTIFICATE PEM) + `client-key.pem` (PKCS#8 PRIVATE KEY PEM), both `0600`, to the same
`service-access/pki` directory. The same `dir` is passed to `recordingQueryCaptureServer` (loki_test.go:392),
which loads `server-cert.pem`/`server-key.pem` — unchanged, so the capture server still validates against
the CA and the health client presents the matching client cert: one shared trust chain.

## PROOF (own command + output, before/after, single command)

Command: `go test ./internal/logs/ -run 'TestPersesLokiDatasourceMultiSource' -count=1`

BEFORE (clean develop, HEAD 40cb28c75, worktree /tmp/w207-lokifix-wt):
```
--- FAIL: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource (0.00s)
    loki_test.go:522: health must pass for a healthy multi-source Loki: perses Loki datasource health client: load Loki service access identity: stat /tmp/TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource3894536791/001/providers/loki/shared/service-access/pki/client-cert.pem: no such file or directory
--- FAIL: TestPersesLokiDatasourceMultiSourcePartialMatchability (0.00s)
    loki_test.go:586: health must pass when at least one source is verified: perses Loki datasource health client: load Loki service access identity: stat /tmp/.../client-cert.pem: no such file or directory
--- FAIL: TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed (0.00s)
    loki_test.go:633: expected 2 per-source queries even on full miss, got 0
FAIL
FAIL	github.com/mcpdev80/baseharbor/internal/logs	0.008s
```

AFTER (HEAD bddb27e62):
```
ok  	github.com/mcpdev80/baseharbor/internal/logs	0.017s
```

Full package + vet (HEAD bddb27e62):
```
$ go test ./internal/logs/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/logs	0.210s
$ go vet ./internal/logs/
# (no output -> clean)
```

The narrow gate + full package + vet are green. The only new failures anywhere are the `cmd/baha`
CLI shards (see below), which are pre-existing and out of scope.

## Hosted CI run (terminal state, 4.6)

- PR: #1732 `fix(0428-202): materialize mTLS client keypair in internal/logs Loki PKI fixture`
  `https://github.com/mcpdev80/baseharbor/pull/1732`
- base: develop `40cb28c758b0` (via `gh api .../pulls/1732 --jq .base.sha`)
- head: `bddb27e6251ec6bc76574a1dcdb13fc7ce017f24`
- run id: **44818799733** (CI · Source & Quality), watched to terminal `conclusion: failure`
- Per cell:
  - `PR · Go unit · packages` -> **SUCCESS** (executed on exact head bddb27e62, this is the fix).
  - `PR · Go unit · owner` -> SUCCESS.
  - `PR · Validation · go-build` -> SUCCESS. `PR · Validation · go-vet` -> SUCCESS.
  - `PR · Go unit · cli-0` -> FAILURE. `cli-1` -> FAILURE. `cli-2` -> FAILURE. `cli-3` -> FAILURE.
  - `PR · Native gate plan` -> SUCCESS. `PR · Trusted Plan` -> SUCCESS. `PR · Source format` -> SUCCESS. `PR · Workflow policy` -> SUCCESS.
  - All release/native/ha/draft/pre-release cells -> SKIPPED (not merge-relevant for this card).

### Why cli-0..3 RED is this card's non-issue

The four CLI shards fail on the exact same pre-existing gate. Verbatim from job 136574098755 (cli-0):
```
main_test.go:60: create failed: Managed-environment machine operations require an authenticated BaseHarbor operator.
```
and `FAIL github.com/mcpdev80/baseharbor/cmd/baha`. This is the locked `internal/identityprovider/**`
operator-auth pre-existing gate defect (owner field #1628/#1594, the same 0428-198 operator/OIDC gate
reported by the 0428-198 lane). Confirmed it fails identically on clean develop:
```
$ git stash  (worktree clean at 40cb28c75)
$ go test ./cmd/baha/ -run 'TestMCPRegistrationCIInProcess' -count=1
--- FAIL: TestMCPRegistrationCIInProcessDiscoverAndInvoke (0.05s)
    registration_ci_readiness_test.go:118: ... authentication_failed ... Managed-environment machine operations require an authenticated BaseHarbor operator.
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	0.059s
$ git stash pop
```
So: **cli-red = 0428-198 (locked identityprovider gate), packages = my fix (green).** No second CI
matrix run is warranted — the CLI failure is unchanged from develop and out of this card's write-set.

## Cleanliness

- No docker/podman compose projects, containers, networks or volumes started. State under `/tmp/w207-lokifix-wt/` only (git worktree, no containers).
- before: `/tmp/w207-lokifix-wt/` — clean develop worktree. after: same worktree with one committed change + a `/tmp/cli0.log` CI-log capture.
- cleanliness: clean — no container/network/volume/state-dir artifacts; ambient-core images of foreign carts untouched.

## END

END_DONE w207-0428-202-lokifix — internal/logs Loki PKI fixture now materializes the mTLS client keypair;
PR #1732 (base develop 40cb28c758b0, head bddb27e62) packages shard GREEN; cli-0..3 red = pre-existing
locked identityprovider operator-auth gate (#1628/#1594), out of scope. No product change outside
internal/logs/loki_test.go.
