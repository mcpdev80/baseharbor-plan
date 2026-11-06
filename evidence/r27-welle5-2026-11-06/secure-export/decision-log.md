# r27 secure-export — decision log

Round 2 (w204, t-20261018-r27-secure-export).

## KOORD-B decision 2026-11-06 (explicit release)

The `cmd/baha/commands.go` wiring is fixed to this card's write-set window.
Precedent 1395a: an adapter without a production caller is dead code, no
acceptance value. Release explicitly granted: the single registration line in
`commands.go` is this card's write-set window for this card — no other edit in
that file.

Mandatory gates the worker satisfied before END:

1. develop current — merged. ls-remote witness
   21d8d05cf1acf04729077e05eb350fcd3bb018ed;
   `git merge-base --is-ancestor 21d8d05c HEAD` rc=0.
2. Real assembly cell — `baha app secure-profile export` resolves the target
   app, collects the opt-in local developer credentials
   (devaccess.Load), and encrypts through the real
   `applicationbackup.BuildExport`; the round-trip cell
   (TestSecureProfileExportWritesEncryptedFile) exercises command -> adapter and
   fails if the ciphertext does not decrypt back to the secret with the correct
   password.
3. Adapter-isolation test — the command calls the in-package BuildExport/OpenExport
   API; removing the binding (see mutant) flips the cell RED.
4. Mutant (registration line out => RED) — concretely demonstrated:
   `sed -i '/secureProfileExportCommand(store),/d' cmd/baha/commands.go` removes
   the command from the tree; `go test ./cmd/baha/ -run
   'TestHumanCommandIndexTracksExactCommandMetadata|TestMachineDocumentationTracksRegistryAndCommandTree|TestMachineCoverageCIRealTreeAndJSONClassification'`
   goes RED (machine documentation drift in
   docs/cli/command-index.md and docs/reference/cli-machine-coverage.md).
   Restore (cp backup) => counter-probe GREEN (rc=0). Command reappears in
   `baha app --help` and the committed HEAD keeps the line.
5. Hosted terminal on the new head — run 42146087866, conclusion success.

After this: END, no further back-and-forth. Merge and merge approval remain the
Coordinator / Codex-MERGE / Owner channel, not this worker.

## Basis refresh 2026-11-06 (KOORD-ZURUECK)

develop moved to f01d2fbdea6b93af6e06ca6297d04065b6acf701 (stage-versions merge),
no longer an ancestor of head 179b91b1 (precedence-truth gate: registry-r2 was
rejected for exactly this). One step: merged current develop into the branch.
ls-remote develop before merge: f01d2fbdea6b93af6e06ca6297d04065b6acf701.
Merge commit 0001ca02 (ort, no conflict; commands.go untouched by develop, line
intact). `git merge-base --is-ancestor f01d2fb HEAD` rc=0. Targeted
`git add` of the merged files; ls-tree confirms
internal/deployment/stage_versions.go, internal/deployment/stage_versions_matrix_test.go,
internal/deployment/deployment_store.go, cmd/baha/deployment_record.go,
cmd/baha/stage_versions_lifecycle_test.go tracked at new HEAD.
New head 0001ca02d19fe9edd69d79c94633377dc3f09260 == ls-remote verbatim.
CI run 42147787627 (pull_request) = success on the new head (all executed jobs
green; runtime/pin gates skipped).
