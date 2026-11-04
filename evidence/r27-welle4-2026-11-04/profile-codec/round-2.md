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

## Push + remote proof (coordinator plattenbefund remedy)

Coordinator plattenbefund: candidate existed only locally (head f935fa18 on NO remote ref; evidence said "no push" on a NEW branch work/r27-profile-codec-rt2; head without remote proof does not count). Fix per instructions: bring the branch onto the PROPOSED candidate branch work/r27-profile-codec (one candidate per chain, PR #1363 stays single candidate), merge develop, push, verify ls-remote==head verbatim.

- Branch: work/r27-profile-codec-rt2 (base candidate head 0eb8f231). Merge develop first so the candidate sits on the newest develop.
- Merge: `git merge --no-edit origin/develop` -> 35baed6c (only .github/workflows/ci.yml + scripts/pr-unit-database.sh + scripts/test_pr_unit_database_route.py landed from develop — the repo's own CI update; my 7 product/doc files byte-identical to f935fa18, verified).
- Push (one candidate per chain): `git push origin work/r27-profile-codec-rt2:work/r27-profile-codec`
  - Output: `0eb8f231..35baed6c  work/r27-profile-codec-rt2 -> work/r27-profile-codec` (GitHub dependabot footer only; no gate run by me).
- develop remote is now ecbb88545f96473986f8f41394cffce58b97d2df (not the 2a43984a named in plattenbefund — coordinator view was stale; fetch confirmed ecbb88545f).
- ls-remote == HEAD verbatim:
  - command: `git ls-remote origin work/r27-profile-codec develop`
  - output:
    ```
    ecbb88545f96473986f8f41394cffce58b97d2df	refs/heads/develop
    35baed6c2d139f22a685d01ea56e1d9b36e3934f	refs/heads/work/r27-profile-codec
    ```
  - local HEAD: `35baed6c2d139f22a685d01ea56e1d9b36e3934f` (candidate branch remote ref matches head).
- PR #1363 remains DRAFT (coordinator flips to ready + runs hosted selected checks). No self-approval, no rule bypass.

## Seven local probes (command + output, observed)

- command: `cd baseharbor && GOCACHE=/tmp/codex-rt2-gocache go test ./contracts/managementaccess/v1/ -v 2>&1 | grep -E "^--- (PASS|FAIL)"`
  - result: 68 PASS / 0 FAIL, including the seven round-2 probes: TestSecretCanaryProbe, TestUnknownFutureFieldProbe, TestBadVersionProbe, TestWrongInstallationScopeProbe, TestSchemaRejectsForeignRecipientProbe, TestCanonicalRoundTrip, TestTransactionRollbackLeavesNoPartialWrite, TestImportConflictReplaceVerifiesActualReplace, TestExportRejectsSecretInDestPath, TestExportRejectsCredentialBearerRecipient (full list in round-2.md).
- `go build ./...` : clean
- `go vet ./contracts/managementaccess/v1/` : clean
- `gofmt -l contracts/managementaccess/v1/` : clean (empty)
- `go test ./contracts/managementaccess/v1/` : ok

END at f49a3303:
END_DONE w113-codec-r2: head=35baed6c29 == ls-remote 35baed6c29 on work/r27-profile-codec (PR #1363), probes 7/7 green locally | candidate pushed to the single proposed branch, merged develop; coord flips PR ready + runs hosted selected checks.

