# Round 1 — Secure Export (t-20261018-r27-secure-export), Lane w204

State: active (implementation round)

## PLAN
- Base attestation: develop=3d8fc207 recorded as ancestor of first commit.
- Record predecessor-drift findings (round-1.md) verbatim.
- Decide faithful write-set bounded by the card (adapter/tests + reuse crypto.go via existing API).
- Implement `internal/applicationbackup/secureprofile` adapter (encrypt/decrypt via crypto.go; explicit selection; fail-closed; no remote secrets / fresh identities by default).
- Wire into `contracts/managementaccess/v1` `CredentialExport` contract (existing authority).
- CLI `baha secure-profile export` (sibling of `app backup`), password via --password-file (never argv).
- Positive/negative regressions: empty/unselected->fail-closed, unreadable w/o password, readable w/ password, wrong-password deterministic RED + mutant GREEN probe.
- go test/vet/build; push work/r27-secure-export; hosted TERMINAL gate; ls-remote witness.

## Predecessor drift (verbatim findings, per coordinator)
- develop HEAD = 3d8fc207deabc2840bcfd888f46d2394cc5a7d36 (ls-remote == this).
- Branch work/r27-secure-export created by THIS lane (did not exist before).
- t-20261018-r27-profile-codec (#1363) "connection/profile codec/store" was NOT delivered on develop: no such module exists on origin/develop. internal/application/store.go exists instead (belongs to t-20261018-r27-public-surfaces, per that task's own ownership note: "Punkt 7 ... liegt ... auf t-20261018-r27-public-surfaces").
- t-20261018-r27-protected-credentials (#1385) reports an OpenBao managed-credential path (SetManagedCredentialIfAbsent) + internal/credential/broker.go + FilePreparedMaterialStore. On develop:
  - internal/credential/broker.go is a ROTATION/MANAGED-CREDENTIAL Broker: Resolve(ctx, ref, scope) (Data{Payload map[string][]byte, Expires *time.Time}). It is NOT a local credential export API.
  - internal/credential/prepared_material.go: PreparedMaterialStore (Load/Save/Clear keyed by rotation keys via validateRotationKey). NOT a local export API.
  - Neither is consumed by any production code on develop (no non-test callers of PreparedMaterialStore/FilePreparedMaterialStore/Resolve found).
- internal/applicationbackup/archive.go + archive_test.go DO exist on develop: generic BACKUP archive (Build/Open over PayloadEntry{Name,Data}), owned by backup-restore (core-315 / podman-backup-guided-runtime). Mission says reuse crypto.go only via existing API, not migrate crypto.
- The normative "encrypted local credential payload" contract IS present on develop: contracts/managementaccess/v1 defines CredentialExport kind + EncryptionDescriptor (algorithm aes-256-gcm, encrypted bool, nonce) with fail-closed ValidateKindEnforcement (nonce = 12 bytes / 16 base64url chars). Store (transactional import) + ExportToContainer exist but have NO production callers (standalone-adapter gap).
- devaccess/credentials.go: local dev-access credentials (username/password) persisted at <target-root>/developer-access/<env>/credentials.env; Enable()==true only for dev/development. devaccess/rebind.go: LocalCredentialStore interface + Recovery.
- credential/native/gitcredential.go: GitCredentialSource reuses the git credential helper; never surfaces secret; fails closed with ErrGitCredentialUnavailable when absent.

## Write-set decision (bounded by card + predecessor interfaces)
- New package: internal/applicationbackup/secureprofile (adapter + tests). Reuses internal/applicationbackup/crypto.go encryptPayload/decryptPayload through the SAME package via a thin wrapper (no crypto migration; no edit of crypto.go).
- Bind into existing contracts/managementaccess/v1 CredentialExport contract (existing authority) — no new shared write (that belongs to t-20261018-r27-public-surfaces).
- PRODUCTION WIRING DEFERRED: public-surfaces task vermerk (2026-11-04) states the callable production consumer of contracts/managementaccess/v1 is DIESER task's (public-surfaces') ownership, "nicht der Kodierungsfremden Karte" = not this adapter card. So NO CLI command wiring in this card; no edit of cmd/baha/commands.go (public-surfaces shared registration).
- BOUNDED WRITE-SET = internal/applicationbackup/secureprofile/{secureprofile.go,secureprofile_test.go} only. Any need for a shared file outside this set (commands.go, app.go, managementaccess contract edits) => STOP+MELDEN with file:line. The adapter exposes a full public callable API so public-surfaces can wire it (zusammenbau durch echten Pfad) without this card touching the shared surface.

## Round-2 progress (implementation complete, local gates green)
- Adapter written at internal/applicationbackup/secureprofile.go (package applicationbackup, reuses crypto.go encryptPayload/decryptPayload through the existing same-package API — no crypto migration, no edit of crypto.go).
- Fail-closed: BuildExport rejects empty selection (ErrEmptySelection), incomplete manifest (ErrInvalidExportManifest), empty password (ErrEmptyExportPassword), traversal/invalid entry names; OpenExport rejects wrong password / tampered ciphertext / truncated envelope via authenticated decryption before any plaintext.
- 11 tests pass locally with -race: empty/incomplete/empty-password/traversal fail-closed; unreadable without password; round-trip readable with password; wrong-password fails closed; tolerant-mutant RED probe (TestExportTolerantMutantFailsRed); tamper/truncation fail-closed; tampered schema version. No regression to the existing applicationbackup suite.
- gofmt clean, go vet clean, full `go build ./...` clean.
- Pushed work/r27-secure-export to origin; ls-remote witness: 4668a59347d9c1811995165c3384f8be3ed65a03 == local head. Base develop 3d8fc207 confirmed ancestor of the commit; single own commit.
- NEXT: PR to develop to trigger hosted terminal gate. The CI workflow (.github/**) is Owner scope — do not edit workflow files or trigger workflow_dispatch; report a failing check as STATE (check name + failing log line) and stop there.

## Round-2 progress (implementation complete, local gates green)
- Adapter written at internal/applicationbackup/secureprofile.go (package applicationbackup, reuses crypto.go encryptPayload/decryptPayload through the existing same-package API — no crypto migration, no edit of crypto.go).
- Fail-closed: BuildExport rejects empty selection (ErrEmptySelection), incomplete manifest (ErrInvalidExportManifest), empty password (ErrEmptyExportPassword), traversal/invalid entry names; OpenExport rejects wrong password / tampered ciphertext / truncated envelope via authenticated decryption before any plaintext.
- 11 tests pass locally with -race: empty/incomplete/empty-password/traversal fail-closed; unreadable without password; round-trip readable with password; wrong-password fails closed; tolerant-mutant RED probe (TestExportTolerantMutantFailsRed); tamper/truncation fail-closed. No regression to the existing applicationbackup suite.
- gofmt clean, go vet clean, full `go build ./...` clean.
- Pushed work/r27-secure-export to origin; ls-remote witness: 4668a59347d9c1811995165c3384f8be3ed65a03 == local head. Base develop 3d8fc207 confirmed ancestor of the commit; single own commit.
- PR #1396 opened against develop (event base 3d8fc207).

## Round-3: hosted gate (CI receipt)
- PR: https://github.com/mcpdev80/baseharbor/pull/1396 (base develop 3d8fc207, head work/r27-secure-export 4668a593).
- Hosted CI run 42132046377 TERMINAL = success.
- Job breakdown (all applicable gates):
  - PR Selected Checks: success
  - PR · Validation · go-build: success
  - PR · Validation · go-unit-tests: success  (full `go test ./...`, covers this adapter)
  - PR · Validation · go-vet: success
  - PR · Source format: success
  - PR · Trusted Plan: success  (CI immutable-input base policy verified; base 3d8fc207 is ancestor of 4668a593)
  - Workflow policy: success
  - PR · Selected Runtime: skipped (runtime_required=false for a pure Go adapter; no runtime provider files touched) — correctly skipped, not a failure
  - PR · Exact Candidate: skipped (requires runtime_required==true AND owner-authored PR; this is a bot-authored adapter PR) — correctly skipped
- BASE ATTESTATION: branch cut from origin/develop 3d8fc207deabc2840bcfd888f46d2394cc5a7d36 (ls-remote at cut == this); 3d8fc207 is an ancestor of commit 4668a59347d9c1811995165c3384f8be3ed65a03; single own commit. develop has since moved to 21d8d05c (other lanes); irrelevant to this PR's event base.
- Write-set verified bounded to internal/applicationbackup/secureprofile.go (+ its test) and the PR; no edit of crypto.go, no .github file, no other slice's files, no shared CLI registration (commands.go owned by t-20261018-r27-public-surfaces).

## END
(continued next round)
