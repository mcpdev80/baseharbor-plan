## PLAN — w113-codec-r2 (t-20261018-r27-profile-codec round 2)

- Read mission + review-1363a fully; confirm candidate head 0eb8f231, base develop bb9bc0ef, PR #1363 draft
- Recipe 1: store.go bind every imported/exported record to canonical version + normative schema + installation/recipient/scope/trust as store input; reject before side effects; reject credential-bearing URLs / secret material in all serialized fields incl recipient/dest path
- Recipe 2: decode with unknown-field rejection (incl nested) OR lossless documented forward-compat; adversarial tests with real secret canary + unknown future field; assert no secret in export bytes
- Recipe 3: canonical container format + real import->export round-trip; pin field/record ordering in regression; golden follows canonical representation
- Recipe 4: transactional atomic write; partial-write leaves nothing behind; conflict-replace verifies previous record actually replaced (not just Replaced==1)
- Recipe 5: update docs/spec/credential-access-v1.md AND docs/de/spec/credential-access-v1.md so payload/envelope semantics + outer container schema match the implemented model exactly
- Recheck all seven probes (secret, unknown-field, bad-version, wrong-installation/recipient/scope, canonical round-trip, partial-write, conflict-replace) + package tests, build, vet, gofmt
- Local commit isolated branch; prepare exact-SHA handoff; keep draft; report gates as STATE not green without observed terminal run

## Results (round 2)

- Worktree started on develop; created isolated branch work/r27-profile-codec-rt2 at candidate head 0eb8f2316b602fe707f0d111c19429c1aac03e7a (base develop bb9bc0ef, PR #1363 draft). Confirmed the four codec/store files were the task write-set; all other diff vs develop is unrelated carried-over work.
- Recipe 1 + 2 (store.go): added ExpectedBinding input (installation_id/recipient_prefix/scope/trust_self_consistent) enforced in NewStore + Import before any write; every record validated against the normative record schema via canonical_schema.go (contracts.ReadSchema loader, no network); decodeContainer now fails closed on unknown top-level and nested fields (strictUnmarshal for struct + strictRecordKeys for record/nested objects); secret/credential scan on every serialized field incl dest_path and recipient (secretMarkers + isCredentialURL). ErrUnknownField, ErrSchema, ErrBinding, ErrSecretOnField added.
- Recipe 3: canonical outer container baseharbor.profile-container/v1 with fixed field/record order (regression TestCanonicalFieldOrder), real import->export round trip (TestCanonicalRoundTrip). New container.schema.json ($ref record schema, additionalProperties:false at container + record + nested objects).
- Recipe 4: Import commits with a single atomic os.WriteFile and cleans up on failure (partial-write leaves nothing); under ImportPolicyConflictReplace the previous record file for the identity is superseded after commit (filesContainingIdentities), so a replace leaves exactly one file and the committed contents reflect the new record (TestImportConflictReplaceVerifiesActualReplace).
- Recipe 5: EN + DE credential-access-v1 docs gained a "Portable container — payload vs envelope semantics" section documenting: container carries record + export envelope only (no ciphertext/secret), no-secret-in-export-bytes guarantee, canonical repeatable round trip, outer container schema, transactional atomic import with replace/supersede behavior.
- Seven probes covered by tests: secret canary (TestSecretCanaryProbe), unknown future field+secret (TestUnknownFutureFieldProbe), bad version (TestBadVersionProbe), wrong installation/scope (TestWrongInstallationScopeProbe), foreign credential recipient via schema (TestSchemaRejectsForeignRecipientProbe), canonical round trip (TestCanonicalRoundTrip), partial-write rollback (TestTransactionRollbackLeavesNoPartialWrite), conflict replace actual (TestImportConflictReplaceVerifiesActualReplace), export-secret-in-dest-path/recipient (TestExportRejectsSecretInDestPath / TestExportRejectsCredentialBearerRecipient).
- Local checks (all green, observed):
  - go build ./... : clean
  - go vet ./contracts/managementaccess/v1/ : clean
  - gofmt -l contracts/managementaccess/v1/ : clean
  - go test ./contracts/managementaccess/v1/ : ok (all package tests pass)
- Local commit f935fa1818479541a6a602012cc08788dcb53bbc on work/r27-profile-codec-rt2 (7 files, scoped write-set; no .github, no cmd/baha, no internal/delivery).
- PR #1363 kept DRAFT; no push, no workflow_dispatch, no rerun (owner .github field / Eigenes-Run-Pflicht: gates not claimed green without observed hosted run).

END at f49a3303:
END_DONE w113-codec-r2: head=f935fa1818 against 0eb8f231, probes 7/7 green locally, build/vet/gofmt/test clean | round-2 hardening complete; PR #1363 draft, coord to flip ready + run selected checks.

