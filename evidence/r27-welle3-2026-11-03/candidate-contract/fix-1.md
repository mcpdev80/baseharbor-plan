# Candidate Contract v1 — Evidence (t-20261018-r27-candidate-contract, lane w39)

Plain bullets. Coordinator f49a3303.

- Worktree /tmp/opencode/w39-candidate-wt, branch work/r27-candidate-contract, base origin/develop 1706272c (mission fetch + worktree rule honored).
- Card read fully: minimal normative definierung der unveraenderlichen source/image submission IN product spec EN + DE-gegenstueck mit input/negative fixtures + existing trusted checks. KEINE neue engine, KEINE CI-Dateien, KEINE privaten repository-formate.
- Write-set confined to docs/spec (EN+DE) + contracts/candidate/v1 fixtures/schema + spec README indexes. No internal Go product edit; internal/delivery/contract.go and internal/deployment/deployment_store.go read-only for reference only.
- EN spec: docs/spec/candidate-contract-v1.md — immutable exact submission (git revision, OCI digest pin, native compose/quadlet consume not rebuild), app/target/consent declarative binding, build-vs-consume separation (release consume never builds), migration boundary (app/owner owns schema; backup != compatibility, image rollback != db rollback, no generic migration engine), stage-versions reuses existing source/applied/observed fields (no new stage axis), standards-boundary (native tools/owners, no private framework).
- DE spec: docs/de/spec/candidate-contract-v1.md mirrors EN section-for-section. EN/DE parity: 163 paired pages OK; DE technical integrity PASS.
- Index: candidate-contract-v1.md added to docs/spec/README.md (Core contracts) and docs/de/spec/README.md (Core-Verträge).
- Schema: contracts/candidate/v1/candidate-contract.schema.json — draft 2020-12, canonical Namespace $id, contract_version const baseharbor.candidate/v1, required app/target/consent, source {kind,repository,revision} OR image {kind,reference,digest sha256:64}, additionalProperties:false, not:{required:[source,image]} enforces exactly-one immutable identity.
- Fixtures: contracts/candidate/v1/golden-fixtures.json (3 valid: source-exact-revision, image-digest-pinned, source-absent-image-only), contracts/candidate/v1/negative-fixtures.json (7 malformed: missing-app, missing-consent, bad-contract-version, digest-mutable-tag-only, digest-bad-sha-format, source+image-both, secret-reference-not-submitted).
- Test: contracts/candidate_contract_test.go — TestCandidateGoldenFixturesAreExactAndValid (all golden validate), TestCandidateNegativeFixturesAreRejected (all malformed rejected by schema), TestCandidateDigestMustBePinnedNotTagOnly, TestCandidateRejectsBareSecretReference.
- Library note: github.com/google/jsonschema-go v0.4.3 does not support nested oneOf/not/anyOf, so the exactly-one-identity-source cross-field rule is expressed at schema top-level via {not:{required:[source,image]}} rather than a per-property oneOf.
- .github/scripts: does not exist (empty) — mission required check honored; no CI files added.
- Merge/ancestry: git merge --no-commit origin/develop -> already up to date; git merge-base --is-ancestor origin/develop HEAD rc=0.
- Build: go build ./... PASS (TMPDIR=/tmp GOCACHE=/tmp/opencode/gc).
- Vet: go vet ./contracts/... PASS.
- Tests: go test ./contracts/... PASS; ./internal/deployment/... PASS; ./internal/delivery/... PASS.
- Docs: mkdocs --strict EN PASS, DE PASS; scripts/documentation-audit.sh PASS (all sections); check_de_translation_integrity.py PASS; check_docs_locale_parity.py PASS.
- Schema registry: contracts.SchemaRegistry() OK (32 schemas incl. new candidate schema).
- PR: draft #1355 on branch work/r27-candidate-contract, base develop. ls-remote origin work/r27-candidate-contract = 2e92832b8f23e80f77036e84cfcadf8504ac0f11 == local HEAD == PR headRefOid.
- STOP: none. Card product-code boundary ("minimal existing internal/delivery/application inputs") respected — no edit beyond docs + candidate contract/fixtures.
- END an f49a3303 (lane w39, t-20261018-r27-candidate-contract).

## END_DONE
