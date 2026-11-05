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
- CLI: cmd/baha/secure_profile_export.go (new), registered in app.go (app.go registration is the single shared CLI surface; verified no other slice owns it).
- Write-set is bounded to: internal/applicationbackup/secureprofile/{secureprofile.go,secureprofile_test.go}, cmd/baha/secure_profile_export.go (+ its test), plus the app.go registration line. Any need for a shared file outside this set => STOP+MELDEN with file:line.

## END
(continued next round)
