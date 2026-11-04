# ROLLE: CODEX-REVIEW — connector PR #21

**Verdikt: ACCEPT.** Review-only; no merge was performed in this mission.

## Exact candidate and diff

- PR: [mcpdev80/baseharbor-node-connector#21](https://github.com/mcpdev80/baseharbor-node-connector/pull/21)
- Base `main`: `346e5ae77ffa929e771ecf1b1322b78fb65bc165`
- Reviewed head: `e3afb49a8f28c3d970b12bca4745a0a500cb0f0f`
- PR is open, ready (not draft), mergeable; `main` is an ancestor of the head.
- `git ls-remote origin refs/heads/main refs/heads/work/r27-test-wire-helper`:

```
346e5ae77ffa929e771ecf1b1322b78fb65bc165 refs/heads/main
e3afb49a8f28c3d970b12bca4745a0a500cb0f0f refs/heads/work/r27-test-wire-helper
```

`git diff --name-status origin/main..HEAD` is exactly:

```
A internal/connector/testwire_smoke_test.go
A internal/targetaccess/testwire.go
```

There are no modifications to existing files. New-file blobs: `internal/targetaccess/testwire.go` = `4e9782e39adabce875a5dfaeef78c7a90666a353`; `internal/connector/testwire_smoke_test.go` = `e130a31f659c3ab02f8b9c1a61c1bfb4678a71df`.

## Existing trust/session blob identities

For each existing trust/session-related file in `internal/connector` and `internal/targetaccess` (including certificate bootstrap/install and production OpenSession call paths), the following literal Git blob IDs match between base `346e5ae77ffa929e771ecf1b1322b78fb65bc165` and head `e3afb49a8f28c3d970b12bca4745a0a500cb0f0f`:

| Existing file | Base blob | Head blob |
| --- | --- | --- |
| `internal/connector/outbound.go` | `cdec0402f69c90ab73432ea74e5d27eca9799ca1` | `cdec0402f69c90ab73432ea74e5d27eca9799ca1` |
| `internal/connector/outbound_pool.go` | `b5cd880d73ccbb3bf37268df688067617a2cfad0` | `b5cd880d73ccbb3bf37268df688067617a2cfad0` |
| `internal/connector/outbound_pool_test.go` | `fea4a6da5b3cee5ef33d8738f43b292f9ee8ea6b` | `fea4a6da5b3cee5ef33d8738f43b292f9ee8ea6b` |
| `internal/connector/outbound_test.go` | `8576f5a260128bab5186f4c71701bbbda2619912` | `8576f5a260128bab5186f4c71701bbbda2619912` |
| `internal/connector/target_access_session.go` | `9945b2f223a317b867b494bdc8b240760feb5844` | `9945b2f223a317b867b494bdc8b240760feb5844` |
| `internal/connector/target_access_session_test.go` | `b332cf6de90e27c09c1f830a80f9ac063d95e170` | `b332cf6de90e27c09c1f830a80f9ac063d95e170` |
| `internal/targetaccess/bootstrap.go` | `83668d3141b19d69fac9ba786129864581555873` | `83668d3141b19d69fac9ba786129864581555873` |
| `internal/targetaccess/bootstrap_test.go` | `d92da75496ad82dbf3b5f293a08327bdd300b80e` | `d92da75496ad82dbf3b5f293a08327bdd300b80e` |
| `internal/targetaccess/bootstrap_tls_test.go` | `3c522a5f2bd54316c1cd7c9a3e03088761b517c7` | `3c522a5f2bd54316c1cd7c9a3e03088761b517c7` |
| `internal/targetaccess/install.go` | `fc96bfbe18346fcaf250a6300e0bfe32f8c0b6b9` | `fc96bfbe18346fcaf250a6300e0bfe32f8c0b6b9` |
| `internal/targetaccess/install_test.go` | `efe787eef6c2df4225165cb11580ea36252a35f8` | `efe787eef6c2df4225165cb11580ea36252a35f8` |
| `internal/targetaccess/security.go` | `3019e806700e47cae88cb80bab3e66de563c71de` | `3019e806700e47cae88cb80bab3e66de563c71de` |
| `internal/targetaccess/security_test.go` | `c82e0a7f25de1fc30267b385c9b5488efaad9c32` | `c82e0a7f25de1fc30267b385c9b5488efaad9c32` |
| `internal/targetaccess/session.go` | `cba4c3e7821916bc517d0167a1b720817e9662df` | `cba4c3e7821916bc517d0167a1b720817e9662df` |
| `internal/targetaccess/session_dispatch_test.go` | `6301ef2ec632042da8dd82e1cb02420b28fcfdbb` | `6301ef2ec632042da8dd82e1cb02420b28fcfdbb` |
| `internal/targetaccess/session_test.go` | `eacd8f35ead3c3e39b86e2d989619122d5e2acde` | `eacd8f35ead3c3e39b86e2d989619122d5e2acde` |
| `internal/targetaccess/session_trust.go` | `34ddde35812253e460c4b10ec1d4e3a9d8169f29` | `34ddde35812253e460c4b10ec1d4e3a9d8169f29` |
| `internal/targetaccess/session_trust_test.go` | `821f85f6a7453b69cb8b82bacc7a99df387542b0` | `821f85f6a7453b69cb8b82bacc7a99df387542b0` |

The remaining files in the complete `internal/targetaccess` package, all `internal/nodeservice` files, and the connector stream handler are also byte-identical; literal base/head blob pairs:

```
internal/nodeservice/nodeservice.go | e72bb29256d88235bd7d92c266560dec5858f387 | e72bb29256d88235bd7d92c266560dec5858f387
internal/nodeservice/nodeservice_test.go | 7e557daf858ce9325f5a89d10d3bbaa6e4047a77 | 7e557daf858ce9325f5a89d10d3bbaa6e4047a77
internal/nodeservice/reenroll.go | ab2217d8b8e50925bc725736247531191aff3613 | ab2217d8b8e50925bc725736247531191aff3613
internal/nodeservice/systemd.go | 797e53eff2044a87e4e00ad99063d06a4ca006c9 | 797e53eff2044a87e4e00ad99063d06a4ca006c9
internal/targetaccess/admission.go | 9933ae9b68aca2d8223d722caa570b523d070404 | 9933ae9b68aca2d8223d722caa570b523d070404
internal/targetaccess/admission_lock_linux.go | 83f393e6be357e2f2161b791693500795e98d3a1 | 83f393e6be357e2f2161b791693500795e98d3a1
internal/targetaccess/admission_lock_unsupported.go | d76eec88a0582a6003f7d3eb5b04781e2dc2b4c8 | d76eec88a0582a6003f7d3eb5b04781e2dc2b4c8
internal/targetaccess/admission_test.go | 5beb398cc078120afcd54de0623ed3146f3d0427 | 5beb398cc078120afcd54de0623ed3146f3d0427
internal/targetaccess/bundle.go | e50f9a00b8d19f6709471e1773ce987c6e4e9730 | e50f9a00b8d19f6709471e1773ce987c6e4e9730
internal/targetaccess/bundle_test.go | edee840a002bc8a77374d6313c7f2a21e4b3963b | edee840a002bc8a77374d6313c7f2a21e4b3963b
internal/targetaccess/canonical/source-lock.json | c3f93431214e81211909a7f107427cce1fea0e67 | c3f93431214e81211909a7f107427cce1fea0e67
internal/targetaccess/canonical/wire.golden.json | 78954e5642b108c2f387b6b6aef60d4bdcf622de | 78954e5642b108c2f387b6b6aef60d4bdcf622de
internal/targetaccess/canonical/wire.schema.json | f7bd63dba5575dac085cd1f8cdc2e0ac66fc07e4 | f7bd63dba5575dac085cd1f8cdc2e0ac66fc07e4
internal/targetaccess/canonical_wire.go | 334ff3c553f13088960a014553197097f4979b63 | 334ff3c553f13088960a014553197097f4979b63
internal/targetaccess/canonical_wire_test.go | e41ff81689acec52d29f889e20ec84bd375dfb22 | e41ff81689acec52d29f889e20ec84bd375dfb22
internal/targetaccess/contract.go | f7c553c807cf0d20e132a54192e9e7aef35b1504 | f7c553c807cf0d20e132a54192e9e7aef35b1504
internal/targetaccess/contract_test.go | 83e2927f114cdf4d642e1b786587b589e926c9ef | 83e2927f114cdf4d642e1b786587b589e926c9ef
internal/targetaccess/enrollment.go | e6e5366253fd4034606fbaad8ae44d6da8f44db1 | e6e5366253fd4034606fbaad8ae44d6da8f44db1
internal/targetaccess/enrollment_test.go | 05219e82b0eb2cc38a9c178e4812815d21048798 | 05219e82b0eb2cc38a9c178e4812815d21048798
internal/targetaccess/negotiation.go | dd33d73fd8985f4fc43bbce0eef698cb2ca2687d | dd33d73fd8985f4fc43bbce0eef698cb2ca2687d
internal/targetaccess/payloads.go | 3e93420385c98497cc2da549cfdaa2e59a591133 | 3e93420385c98497cc2da549cfdaa2e59a591133
internal/targetaccess/quadlet_completion_wire_test.go | 42e623702d607d4cb0e2f6efa860c04af97e542f | 42e623702d607d4cb0e2f6efa860c04af97e542f
internal/targetaccess/streams.go | aba4709aac15f67a1a7487c6752c02a5a6c8894b | aba4709aac15f67a1a7487c6752c02a5a6c8894b
internal/targetaccess/streams_test.go | ad3624ac0a90b0de0ab3c450f6f412be7284f86c | ad3624ac0a90b0de0ab3c450f6f412be7284f86c
internal/connector/target_access_stream.go | abb5aef88e579f4ff32f5b547be7448c2516d0fb | abb5aef88e579f4ff32f5b547be7448c2516d0fb
```

## Helper isolation and smoke

`rg -n 'NewHandshakePair' --glob '*.go' .` finds only the constructor declaration and documentation in `internal/targetaccess/testwire.go` and one consumer: `internal/connector/testwire_smoke_test.go:28`. Thus the helper is imported only by the test package; no product call site uses it.

The smoke exercises `NewHandshakePair`, `net.Pipe`, both real `targetaccess.OpenSession` roles, peer identity negotiation, and an actual `Request` frame written by the client and read by the server. There is no `t.Skip` in either new file.

Own targeted run:

```
$ go test ./internal/connector -run '^TestServeLogStreamHandshakeWireRoundTrip$' -count=1 -v
=== RUN   TestServeLogStreamHandshakeWireRoundTrip
    testwire_smoke_test.go:123: wire round-trip OK: request "req-wire-1" over real mTLS line, rc=0
--- PASS: TestServeLogStreamHandshakeWireRoundTrip (0.09s)
PASS
ok   github.com/mcpdev80/baseharbor-node-connector/internal/connector 0.094s
```

## Hosted checks

Both runs are terminal-success on the exact head:

- [CI · Node Connector Quality, run 41934807383](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41934807383): `completed/success`; PR check `Test · Vet · Build` passed.
- [Connector Source Conformance, run 41934807440](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/41934807440): `completed/success`; `source` passed. Two unrelated native matrix jobs were skipped by workflow selection; the required test/build/vet/source checks passed.

## Verdict

The exact diff adds only the exported test-wire helper and its external-package smoke test. All existing trust/session/certificate and session-call-path blobs listed above are byte-identical to `main`; only the smoke test consumes `NewHandshakePair`. The real mTLS/frame smoke passes locally, and both hosted runs are terminal-success on the exact candidate. **ACCEPT.**
