# CODEX-REVIEW 1396a — Secure Export round 2

- Mission: `coordinator/missions/codex-r1396a.txt`
- Role: CODEX-REVIEW (read-only; no PR action)
- Repository: `mcpdev80/baseharbor`
- PR: #1396, base `develop`
- Reviewed head: `0001ca02d19fe9edd69d79c94633377dc3f09260`
- Reviewed base: `f01d2fbdea6b93af6e06ca6297d04065b6acf701`
- Review date: 2026-11-06
- Verdict: **REJECT**

## Candidate and gate identity

`git ls-remote origin` reported `0001ca02d19fe9edd69d79c94633377dc3f09260`
for `refs/pull/1396/head`; the PR API reported the same exact head and base
`develop`. Remote `develop` was `f01d2fbdea6b93af6e06ca6297d04065b6acf701`;
`git merge-base --is-ancestor origin/develop origin/pr/1396` returned 0.
Hosted run `42147787627` was terminal `completed / success` at that exact head;
`PR Selected Checks` also completed successfully. Runtime-related jobs were
skipped by path selection.

Name-only diff from `origin/develop` to the candidate:

- `cmd/baha/commands.go`
- `cmd/baha/machine_coverage.go`
- `cmd/baha/secure_profile_export.go`
- `cmd/baha/secure_profile_export_test.go`
- `docs/cli/command-index.md`
- `docs/de/cli/command-index.md`
- `docs/de/reference/cli-machine-coverage.md`
- `docs/reference/cli-machine-coverage.md`
- `internal/applicationbackup/secureprofile.go`
- `internal/applicationbackup/secureprofile_test.go`

The reviewed write-set and registration line are present at the exact candidate.
The existing encryption primitive `internal/applicationbackup/crypto.go` is
unchanged (blob `52f1788b3b20339d65356ce0a3eeb3ac2a946c62` on both refs), as is
`internal/applicationbackup/archive.go` (blob
`e8abb7a66a61379da97424a4038fc8446897a6bd` on both refs). No changes were made
by this review; the live product worktree was left untouched.

## Production wiring source review

The registration at `cmd/baha/commands.go:251` adds
`secureProfileExportCommand(store)`. That command's `Run` calls
`executeSecureProfileExport`; the implementation resolves the application,
loads opt-in local credentials with `devaccess.Load`, calls
`applicationbackup.BuildExport`, and writes the resulting envelope. This is a
real production caller, and the round-1 adapter boundaries remain intact:
explicit local credential selection, no provider secrets or new device
identities, authenticated encryption through the existing crypto helper,
fail-closed empty/invalid/wrong-password/tamper/truncation behavior, and
no-overwrite output creation.

## Registration mutation and counterprobe

An isolated detached worktree at the exact candidate was created at
`/tmp/opencode/codex-r1396-mutant`. I removed only the registration line
`secureProfileExportCommand(store),`; the literal diff was one deleted line in
`cmd/baha/commands.go`.

With the registration removed, I ran:

```text
go test ./cmd/baha -run 'TestHumanCommandIndexTracksExactCommandMetadata|TestMachineDocumentationTracksRegistryAndCommandTree' -count=1
```

The mutant was red: `TestHumanCommandIndexTracksExactCommandMetadata` reported
drift in `docs/cli/command-index.md`, and
`TestMachineDocumentationTracksRegistryAndCommandTree` reported drift in
`docs/reference/cli-machine-coverage.md`. I restored the line; the same two
tests then passed (exit 0). The isolated worktree was clean after restoration.

## Blocking finding: claimed assembly cell does not exercise the command

The task handoff and the test comment describe
`TestSecureProfileExportWritesEncryptedFile` as a command-to-adapter production
E2E cell. The test body instead constructs its own manifest and entries, calls
`applicationbackup.BuildExport` directly, calls `writeSecureProfileExport`,
then decrypts the file. It never constructs `rootCommand`, invokes
`secureProfileExportCommand` or `executeSecureProfileExport`, resolves a test
application, or loads the local credentials through `devaccess.Load`.

Therefore the registration mutation's red signal proves that the generated
command documentation is kept in sync with the command registry; it does not
make the claimed export assembly cell red. A broken or bypassed command path
could leave the isolated adapter test green. The production wiring is present
by source inspection, but the required end-to-end cell is not demonstrated by
the committed test.

### Required correction recipe

Add a bounded command integration test in `cmd/baha` that invokes
`baha app secure-profile export` through the real root/command tree with a test
application store and eligible local developer credentials. Assert the output
file is created, decrypts only with the supplied password, contains the
selected credentials, and does not expose the password or plaintext in output.
Then remove only the registration line in an isolated worktree and show that
this invocation cell itself fails; restore the line and show the counterprobe
passes. Re-run the focused tests and the required hosted checks on the resulting
exact head. No product changes were made during this review.

## Repository-rule compliance

Read-only review only. No PR mutation, approval, merge, product edit, or change
to the candidate occurred. The source mutation was isolated and restored.

## Conclusion

The production command is registered and its source calls the secure export
adapter; the registration mutant and restored counterprobe are reproducible.
The required real assembly behavior is not exercised by the claimed E2E test,
whose body directly tests the adapter and file helper. **REJECT** until a
command-level integration cell demonstrates the production path and its
registration mutation discrimination.
