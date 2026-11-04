# CODEX-REVIEW — PR #1362 native-auth, round 2

- Candidate: `a3eee132e3f2d1b65d7afee80efc3f9c0d166d6c` (verified exact SHA)
- PR base: `bb9bc0ef1b419e06e153c9b95bfef47b24347108` (develop ancestor)
- PR: OPEN, READY, mergeable; 7 changed files / +708 lines, all under `internal/credential/native/`, matching the reserved write set.
- Verdict: **REJECT**. No approval or merge.

## Seven SHA-exact checks

1. **Native-hit / no-interaction counterprobe — FAIL.** The package has no production caller: repository search outside `internal/credential/native` finds no `native.Broker` or import of the package. At `internal/credential/native/broker.go:59-67`, a hit returns `credential.Data{}`; no credential is provided to the consumer. `caller_test.go:93-110` verifies that test helper execution returns nil error and empty payload, but does not test that the real application skips its interactive auth path when the native source hits. Thus the required user-visible behavior is neither connected nor proven; the compile-time interface assertion (`broker.go:41-43`) alone is not a callable production integration.

2. **Native failure and secret-safe fallback — PARTIAL.** The source uses Git's stdin/stdout helper protocol and fails closed on missing/empty replies (`gitcredential.go:38-57`); execution errors redact stderr (`host.go:22-32`, `host.go:62-69`) and broker errors collapse to the documented absence result (`broker.go:59-70`). Tests cover missing helper and stderr sentinel. Because no product caller uses this broker, the required fallback behavior in the actual query path remains unproved.

3. **SSH environment isolation — PASS for configuration isolation.** Tests use `t.TempDir`, `t.Setenv("SSH_AUTH_SOCK", ...)` and a fake runner (`native_test.go:95-140`); Go restores the environment after each test. They no longer depend on or rewrite the user's real SSH configuration. The temp file is sufficient for the current `os.Stat` availability check; the fake runner isolates `ssh-add` behavior.

4. **No secret writes outside defined storage — PASS for this write set.** The seven changed files contain no credential persistence path. Git helper data is read from stdout and not written by this adapter; the temporary helper scripts in tests live under `t.TempDir`. The caller currently receives no payload, which is a functional deficiency noted above, not an unintended secret-file write.

5. **Card write set — PASS.** GitHub reports seven changed files, all new files under `internal/credential/native/`; this is within the task's `internal/credential/` reservation. No other task-owned paths are changed in the PR diff against its actual base.

6. **Package tests/build/gofmt/vet — PASS.** On the extracted exact candidate: `go test ./internal/credential/... -count=1`, `go build ./internal/credential/...`, `go vet ./internal/credential/...`, and `gofmt -l internal/credential` all completed successfully. Packages credential, credential/native and credential/openbao passed.

7. **Prior review recipes — PARTIAL.** The Git credential protocol is corrected (`gitcredential.go:44-57` and real-helper test in `caller_test.go:14-40`); stderr is dropped from returned command errors (`host.go:22-32`) with a sentinel regression (`caller_test.go:75-91`); SSH tests now isolate `SSH_AUTH_SOCK` (`native_test.go:95-140`). However, the core recipe to connect a callable path is not satisfied merely by implementing the interface: there is no production caller, and successful resolution returns empty `credential.Data`. Consequently the required no-interaction behavior on a real native hit is still unimplemented/unverified.

CI was terminal on this candidate at run `41834411858`: `go-build`, `go-unit-tests`, `go-vet`, source format, workflow policy and `PR Selected Checks` succeeded; unrelated/product gates were skipped. The run is green but does not close the production-call-path finding.

## REZEPT

- **Datei:** `baseharbor/internal/credential/native/broker.go` and the owning production credential-query caller; regression coverage in `baseharbor/internal/credential/native/caller_test.go` plus caller-level tests.
- **Änderung:** Wire the broker into the actual credential query flow before any interactive prompt. Carry the resolved credential only through the existing protected in-memory credential contract so downstream auth can use it; do not treat a boolean “found” signal with empty data as successful authentication. Preserve the fail-closed documented fallback when no native source resolves and keep secrets out of errors/logs.
- **Testanforderung:** Add an end-to-end caller counterprobe with a configured native hit that proves the helper is queried, the real prompt/interaction callback count remains zero, and the downstream operation receives the expected credential through the protected contract. Add the paired missing-source case proving the documented fallback occurs without secret leakage. Retain SSH tests using isolated `SSH_AUTH_SOCK` and assert the caller environment/configuration is unchanged after the test. Re-run package tests/build/vet/gofmt and required hosted gates on the new exact SHA.
- **Stop-Kriterium:** Stop/reject if native credentials are only detected but not consumed by the production query path, if a hit can still trigger interactive auth, if secrets escape through errors/logs or unapproved files, if SSH tests alter real user configuration, or if required checks are not terminal green for the reviewed SHA.

## Review boundary and END

Read-only review of exact candidate `a3eee132e3f2d1b65d7afee80efc3f9c0d166d6c`; no candidate changes, approval, or merge. `END_DONE codex-r1362b: verdict=REJECT open=production-call-path,native-hit-interaction | The adapter reports native hits but has no production caller and returns empty credential data.`
