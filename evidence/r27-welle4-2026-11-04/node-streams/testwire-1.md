# w155 — Test-wire helper for t-20261105-r27-test-wire-helper (RUNDE 1)

**Lane:** w155 (Worker) · **Coordinator:** f49a3303 (Qwen Flash)
**Card:** t-20261105-r27-test-wire-helper · **Release:** v0.4.27
**Repo:** baseharbor-node-connector · **Branch:** work/r27-test-wire-helper (cut from origin/main 346e5ae)
**Evidence path:** baseharbor-plan/evidence/r27-welle4-2026-11-04/node-streams/testwire-1.md
**PR:** #21 https://github.com/mcpdev80/baseharbor-node-connector/pull/21

## PLAN

- Read mission + full card (plan.py show). Card state was `ready` (unassigned); Owner directive assigned the lane in the mission text.
- Cut branch work/r27-test-wire-helper from real origin/main (346e5ae); verified origin/main SHA via ls-remote before branch cut.
- Confirm existing newTestCA/newTestLeaf ceremony lives only in _test.go (package-internal, unimportable) and that OpenSession uses TLSFiles + Hello.
- Design exported HandshakePair helper in NEW internal/targetaccess/testwire.go that wraps the ceremony behind an exported call; no production file touched.
- Write connector-package smoke test importing the helper and round-tripping one frame over a real net.Pipe mTLS line (red-before-green proof).
- Local checks: go vet ./..., go build ./..., gofmt -l, go test ./...
- Verify blob-identical: git diff --name-only origin/main..HEAD lists only the new file + test; product API and OpenSession unchanged.
- Push branch, open PR #21 to main; run hosted CI to terminal; record Run-IDs + status; publish board + END_DONE to coordinator.

## WAS WIRD ENTWICKELT

A cross-package test wire: the mTLS handshake ceremony that lives sealed inside `internal/targetaccess` `_test.go` files is now exported behind one exported call (`targetaccess.NewHandshakePair`), so package-external tests (the connector package) can build a real CA+leaf pair and drive the real `OpenSession` ServeLogStream handshake chain end-to-end. This is pure test infrastructure — no product API change, no `OpenSession` change.

## BRANCH PROVENANCE (proof)

- ls-remote origin before branch cut (main): `346e5ae77ffa929e771ecf1b1322b78fb65bc165  refs/heads/main`
- Branch cut: `git checkout -b work/r27-test-wire-helper origin/main` → tracks origin/main at 346e5ae.
- `git log --oneline origin/main -1`: `346e5ae r27: harden connector trust rotation, revocation and reconnect (#20)`
- `git merge-base --is-ancestor origin/main HEAD` → YES (346e5ae is an ancestor of HEAD).
- `git log --oneline origin/main..HEAD` lists ONLY my commit: `e3afb49 ...`
- Remote head after push: `e3afb49a8f28c3d970b12bca4745a0a500cb0f0f`
- No foreign candidate carried on top; one integration candidate per chain.

## REPO-RULE COMPLIANCE

- Only TWO new Go files added (internal/targetaccess/testwire.go + internal/connector/testwire_smoke_test.go); zero existing files changed.
- Existing trust/session/cert files left blob-identical (git diff --name-only origin/main..HEAD lists only my two new files).
- Product API surface unchanged; OpenSession untouched; helper named/documented as test infra only.
- No .github/ edits, no workflow_dispatch, no runner work (runs triggered via PR, not by me).
- No subagents — all steps executed in this session.

## HOW THE CIRCUMVENTED THE _test.go SEAL

The ceremony (newTestCA/newTestLeaf) stayed byte-identical inside _test.go. A NEW non-test file (testwire.go) holds the exported `NewHandshakePair` + shared `newTestLeafMaterial`, which reproduces the ceremony in a compiled (non-_test) file so it can be imported package-externally. Key correctness fix during dev: both leaf sides of the pair must share ONE CA (generated once in NewHandshakePair), otherwise each side's trust bundle points at a different CA and the handshake fails. Leaf serials are made distinct from the CA (serial 1) so the chain satisfies RFC 5280 uniqueness that Go 1.26's x509 verifier enforces.

## EVIDENCE

### smoke test output (local)
```
=== RUN   TestServeLogStreamHandshakeWireRoundTrip
    testwire_smoke_test.go:123: wire round-trip OK: request "req-wire-1" over real mTLS line, rc=0
--- PASS   TestServeLogStreamHandshakeWireRoundTrip (0.21s)
ok  	github.com/mcpdev80/baseharbor-node-connector/internal/connector	0.225s
```
Red-before-green: the exported helper is what makes this connector-package test compile and pass; without it the ceremony stays sealed in _test.go.

### local checks
- `gofmt -l .` → empty (clean)
- `go build ./...` → OK
- `go vet ./...` → OK
- `go test ./...` → all packages green (internal/targetaccess 15.1s, internal/connector 0.247s, etc.)

### blob-identical proof
```
$ git diff --name-only origin/main..HEAD
internal/connector/testwire_smoke_test.go
internal/targetaccess/testwire.go
```
Exactly two new files; no product file touched.

### hosted CI to terminal
- Run #55 "CI · Node Connector Quality" — conclusion **success** (Test/Vet/Build, ID 126940475424). https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41934807383
- Run #200 "Connector Source Conformance" — conclusion **success** (source + actual encrypted transport jobs, ID 126940474477). https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41934807440
- Both triggered via pull_request (PR #21) on GitHub-hosted shared runners; no rerun/dispatch issued by this lane.

## END

END_DONE w155-testwire: head=e3afb49a8f blob=<trusted dateien identisch belegt: diff --name-only origin/main..HEAD = nur 2 neue Go-Dateien> smoke=<frame rc0> lauf=<#55 success + #200 success> lsremote=<e3afb49a8f> | Exported NewHandshakePair hinter dem bestehenden newTestCA/newTestLeaf-Zeremonie; Connector-Smoke-Test rundertourt ein Frame ueber die echte mTLS-Leitung; kein Produktfileveraenderung; CI gruen.

✅ TASK COMPLETE — END_DONE sent to coordinator f49a3303.
