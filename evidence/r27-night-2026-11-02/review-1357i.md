# PR #1357 completion review — e9c9e826

ROLLE=REVIEW; no merge. **Verdict: REJECT.** Task `t-20261022-r27-ci-access`. Reviewer: Codex GPT-6 Luna (configured model `gpt-6-luna`), fresh Luna-channel run. Review target: `e9c9e826725e6001088f18bacd7e5a8598cac4c7`, tree `92bf7c0a34709ae9516b5282c3c6cbccb60f0228`; base `develop` `0107d8e1530ff3469048022d7035a2a472dbda34`, confirmed ancestor. PR remained OPEN/CLEAN and head/base matched GitHub API both before and after review. SSH `git ls-remote` was unavailable because `/etc/ssh/ssh_config.d/20-systemd-ssh-proxy.conf` has invalid ownership; GitHub refs API supplied the independent before/after head and base observations. Candidate object and working tree were not changed.

## Matrix universe and coverage

The requested universe is the two public client operations (`Check`, `Execute`) crossed with six failure phases: no client certificate, self-signed client certificate, client certificate from a foreign CA, malformed client certificate, wrong server CA, and malformed client CA rejected during `NewClient` load. This is 12 operation/case rows; each handshake row must observe both the `/readyz` recorder and execute handler, and the load-phase row must establish that neither route was called.

| Failure case | Check row | Execute row |
| --- | --- | --- |
| No client certificate | Present (`TestMutualTLSRejectsMissingClientCertificate`) | Missing |
| Self-signed client certificate | Present (`TestMutualTLSRejectsSelfSignedClientCert`) | Missing |
| Foreign client CA | Present (`TestMutualTLSRejectsForeignClientCA`) | Present only in the combined foreign-CA test; route recorder is not rechecked after Execute |
| Malformed client certificate | Missing; the test corrupts only the private key | Missing |
| Wrong server CA | Present (`TestMutualTLSRejectsWrongServerCA`) | Missing |
| Malformed client CA / load phase | Constructor failure and zero-route assertions present; no `Check` or `Execute` can be issued after failed construction | Constructor failure and zero-route assertions present; no `Check` or `Execute` can be issued after failed construction |

The reported 12-row matrix is therefore not demonstrated. Only Check-handshake negatives cover the certificate/CA cases; Execute has one foreign-client-CA attempt, and the malformed-cert case is actually a malformed-key case. The combined Check/Execute foreign-CA test verifies the execute handler remains untouched but does not re-read the readyz recorder after Execute.

## Findings

1. **The required 12 operation/case rows are incomplete.** `internal/runtimeexecutor/client_test.go:611-905, 916-992, 994-1107` has Check negatives for missing, self-signed, foreign-CA and wrong-server-CA cases, while the only negative Execute is a foreign-CA request (`:981-990`). The tests do not provide two route assertions for every matrix row. Add the missing Execute cases and a route-specific readyz/execute assertion pair for each row; retain exact TLS/load error expectations. Required test: `go test ./internal/runtimeexecutor -run 'TestMutualTLS(Rejects|Execute)' -count=1` must exercise all 12 rows and fail if either route is reached on any negative. Stop if any row cannot distinguish a handshake refusal from a client-load failure.

2. **The “broken certificate” row corrupts the private key instead.** `client_test.go:798-837` and `:994-1065` write an intact client certificate and corrupt only the PEM private-key body. This proves key-load failure, not malformed certificate handling. Add a distinct malformed-certificate fixture with an otherwise valid key and assert `NewClient` fails before any recorder invocation; account for it separately in both operation rows, documenting that neither method is callable after constructor failure. Required test: a named malformed-client-certificate load-phase test must fail if `NewClient` accepts the certificate or any route recorder is touched. Stop if the fixture does not isolate certificate parsing from key parsing.

3. **The candidate exceeds the mission write-set with a production handler change.** The PR changes `internal/runtimeexecutor/handler.go:24-30,50-51` to add and update `Handler.HandlerReached`, although the mission declares `client_test.go` as the write-set. Keep route counters in test-only wrapper handlers and remove the production field/import/write. Required test: the focused runtimeexecutor package suite must pass with no diff to `handler.go`, while the negative Execute tests still detect handler entry. Stop if the test cannot observe the execute route without changing product code.

## Mutation control, test and hosted evidence

- Independent mutation control, in a fresh `/tmp` archive at the exact candidate: changed the test server's `ClientAuth` from `tls.RequireAndVerifyClientCert` to `tls.RequestClientCert`; `TestMutualTLSRejectsMissingClientCertificate` failed as expected (`expected a TLS/handshake/verification error, got nil`, exit 1). Mutation was confined to the temporary archive.
- Required command in a clean archive of the exact candidate: `GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go test ./internal/runtimeexecutor -count=1 -timeout 8m` — PASS (`0.062s`).
- Hosted run `41688014380` completed SUCCESS on the exact head. `PR Selected Checks` SUCCESS; source format, trusted plan, runner interface, demo pin, exact candidate, focused Python, Go build, Go unit tests, Go vet, Docker lifecycle and Podman lifecycle gates SUCCESS. Conditional jobs were SKIPPED. No CI gate was bypassed.
- PR diff against `develop`: `internal/runtimeexecutor/client_test.go` (+1378) and `internal/runtimeexecutor/handler.go` (+6); zero deletions. The latter is outside the mission write-set.
- The broader access slices remain deferred to their respective owners: profile-contract, profile-codec, native-auth, protected-credentials, secure-export, device-enrollment, device-lifecycle, connection-client, access-profiles, managed-users, team-auth, access-wizard and onboarding-wizard. This review does not claim those slices qualified.

## REZEPT

Finding-1 | internal/runtimeexecutor/client_test.go:611-1107 | Add the missing Check/Execute cases for all six failure inputs and assert both route flags for each operation row, rechecking readyz after Execute | `TestMutualTLS...` matrix tests prove all 12 rows reject and both route counters stay false | Stop if a row conflates load failure and handshake rejection or either route is unobserved
Finding-2 | internal/runtimeexecutor/client_test.go:798-837,994-1065 | Replace the mislabeled broken-key fixture with a separate malformed-certificate fixture using a valid key; keep broken-key coverage separate | Named malformed-cert load-phase test proves `NewClient` rejects the certificate and no handler runs | Stop if invalid certificate bytes are not the cause of constructor failure
Finding-3 | internal/runtimeexecutor/handler.go:24-30,50-51 | Remove production `HandlerReached` instrumentation and count execute-route entry in a test-only wrapper in `client_test.go` | `go test ./internal/runtimeexecutor -count=1` passes with negative Execute route assertions and no `handler.go` diff | Stop if the test requires a product-code test hook
