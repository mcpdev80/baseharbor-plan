# Producer PR #1203 fix round C (o213)

Lane o213. Round C on PR #1203 (branch work/r27-producer-extension-contracts,
candidate head b9ebc475, forward of a2da4174 -> 7c798147 -> b9ebc475). Task
prompt: `evidence/board-2026-10-29/prompts/o213.txt`. Task:
`baseharbor-plan/tasks/t-20261029-r27-ci-producer.md`. Review input:
`evidence/board-2026-10-29/codex-rv1203.md` (RV1203 + RV1203B, VERDICT
REQUEST_CHANGES, 2 findings). Fix lineage:
`evidence/r27-ci-replacement-2026-10-29/producer-pr2-fix.md` (o211 round B).

## PLAN

1. Read dispatch, codex-rv1203.md (RV1203 + RV1203B) and producer-pr2-fix.md.
   Re-attach worktrees/o209 on origin/work/r27-producer-extension-contracts and
   fast-forward to the current remote head 7c798147 (a2da4174..7c798147); confirm
   the only develop-vs-HEAD change is contracts/extension_trust_test.go (138 +,
   no go.mod/go.sum).
2. PART 1 (decide first, cheap): assess whether a GENUINE uncovered
   PROFILE-contract behavior exists under contracts/profile* or the profile
   schemas in contracts/ + spec/. Test: do current profile tests exercise
   required-field negatives per field and schema-validation failures, or is one
   clearly missing (structure compared against extension_trust_test.go)?
3. PART 1 verdict: NO genuine uncovered profile slice (see PART-1 decision + proof
   and the profile coverage map at the end). Do not pad. Deliver the coverage map
   and recommend the owner-approved scope wording (extension family allowed),
   which producer-slice2 already established. Keep the branch as-is meanwhile.
4. PART 2 (always): fix contracts/extension_trust_test.go per RV1203B:
   (a) split the artifact + dialect double-removal at the old lines 43-54 into
   two single-field negatives, each asserting its named constraint; (b) assert
   baseline validity inside the second test too; (c) correct the 'Go validator
   divergence' comment to match the code (the Go validator is no longer invoked;
   the tests exercise only the packaged jsonschema-go schema).
5. PART 2 correction detail: confirmed via the schema JSON that
   `configuration_schema` is NOT a top-level required field of the extension
   descriptor; only its nested `dialect` is required when the object is present.
   So the correct single-field `dialect` negative is an empty
   `configuration_schema` object (`{}`), not an absent one; the absent-object
   case was verified to pass and was not shipped as a negative.
6. TESTS: go vet ./contracts/, go build ./..., full `go test ./contracts/ -count=1`
   (isolated GOPATH/GOCACHE under /tmp), and focused
   `-run '^TestExtension' -v`. Commit forward only (no force), push, confirm new
   head and green exact-head PR Selected Checks.

## PART-1 decision: no genuine uncovered PROFILE-contract slice

Decision: NO genuine uncovered profile-contract behavior exists; do not pad a
profile test. The dispatch's honest-gap test is passed and the result is
documented below and in the profile coverage map.

Proof:

- The only shipped "profile" JSON-schema contract is
  `contracts/connection-profile/v1/profile.schema.json` (top-level required:
  version, name, core, trust, targets; nested core: installation_id, url;
  trust: ca_pem, sha256; targets[]: name, tenant_id, runtime_provider). It is
  covered by a real behavioral test:
  `TestConnectionProfileSchemaRejectsAuthorityAndLocalState` in
  `contracts/v0425_contracts_test.go:88`. That test asserts the canonical
  transport-shape passes, rejects forbidden extra properties
  (additionalProperties:false), rejects an insecure `http://` core URL, and
  rejects a non-`const` version. Every other shipped family
  (service, binding, machine, provider, provider-impact, provider-plan,
  footprint) already carries a behavioral schema-validation test.
- The dispatch framed PART 1 around the word "profile"; the task's original scope
  wording ("small real profile-contract slice") would therefore point at
  connection-profile, which is already guarded. There is no uncovered
  profile-contract slice to qualify, and no service/development/binding/provider
  family is in the reservation this round owns.
- The genuinely uncovered slice in scope this round is the SECOND normative schema
  of the already-authorized extension/v1 family,
  `contracts/extension/v1/extension-trust.schema.json`, which ships with zero
  behavioral Go coverage (its `extensionSchema` helper is defined but never
  invoked). That is an extension-family contract, not a profile contract; it is
  addressed by PART 2's correction of the extension test, not by a new profile
  test. Adding a profile required-field-negative test on top of the existing
  connection-profile test would duplicate coverage of an already-guarded schema
  and is padding, not a real gap.
- The extension family is the authoritatively authorized slice per
  producer-slice2.md (normative per docs/spec/extension-artifact-trust-v1.md,
  zero prior behavioral coverage, disjoint from f60/#1202 and merged #1199). The
  scope deviation from the literal "profile" wording of the task is already
  owner-approved there; this round does not re-litigate it, it corrects the
  extension test to the RV1203B recipe.

Recommendation to owner: keep the scope wording as "extension/v1 contract family
allowed" (as producer-slice2 established) rather than "profile-contract slice";
connection-profile is already covered and is not the unguarded surface.

## PART-2 correction: extension_trust_test.go per RV1203B

RV1203B asked to: (a) split the artifact + dialect double-removal into two
single-field negatives each asserting its named constraint; (b) assert baseline
validity inside the second test; (c) correct the 'Go validator divergence'
comment when the Go validator is no longer invoked.

Applied:

- Split the old combined `missing` negative into two single-field negatives in
  `TestExtensionDescriptorSchemaRejectsGoValidatorDivergence`:
  - `missingArtifact` removes `artifact.oci_reference` (configuration_schema left
    empty, rest of descriptor intact) and asserts rejection naming
    `artifact.oci_reference`.
  - `missingDialect` leaves `artifact.oci_reference` present and sets
    `configuration_schema` to `{}` and asserts rejection naming
    `configuration_schema.dialect`. (Verified: the descriptor does not require
    `configuration_schema` itself at the top level, only `dialect` when present;
    an absent object is schema-valid and is not claimed as a negative.)
  - Each mutation is the only change from the asserted-valid baseline, so each
    negative fails only on its intended constraint.
- Second test `TestExtensionDescriptorSchemaRejectsInvalidIdAndFamily`: added a
  `resolved.Validate(base)` baseline assertion inside the test (it previously
  relied on the baseline defined in the preceding test). Each loop mutates exactly
  one field per iteration (id, then family) and names the failing constraint.
- Comment correction: the old doc comment claimed the test "prevents a
  frozen-family guard from missing a family" (removed in round B) and the inline
  claim referred to "Go validator divergence"; the Go metadata validator
  (`internal/extension/metadata.go` `Metadata.Validate()`) is no longer invoked by
  either test, so the inline language now describes only the packaged
  jsonschema-go schema, matching the code exactly. Doc comment restated to match
  the two single-field loops.

No go.mod/go.sum edits shipped; the only develop-vs-HEAD change in this commit is
contracts/extension_trust_test.go.

## repo-rule compliance

- Forward commits only, no force; a2da4174 and 7c798147 preserved. Branch
  work/r27-producer-extension-contracts, tree worktrees/o209.
- Isolated verification only (GOPATH=/tmp/o213-gopath GOCACHE=/tmp/o213-gocache).
  No CI gate claimed as green from the sandbox; exact-head CI verified separately
  via `gh pr checks` at the new head.
- PART-1 is read-only analysis; no product test added for the already-covered
  connection-profile slice, so no padding.
- Evidence written in baseharbor-plan only (this file). No planning-metadata edit
  made by this lane; task state/merge/acceptance remain the Maintainer's.

## Verification

Isolated (GOPATH=/tmp/o213-gopath GOCACHE=/tmp/o213-gocache):
```
$ go vet ./contracts/                            # clean (no output)
$ go build ./...                                 # clean
$ go test ./contracts/ -count=1
ok  github.com/mcpdev80/baseharbor/contracts  0.307s
$ go test ./contracts/ -count=1 -run '^TestExtension' -v
=== RUN   TestExtensionDescriptorSchemaRejectsGoValidatorDivergence
--- PASS: TestExtensionDescriptorSchemaRejectsGoValidatorDivergence (0.00s)
=== RUN   TestExtensionDescriptorSchemaRejectsInvalidIdAndFamily
--- PASS: TestExtensionDescriptorSchemaRejectsInvalidIdAndFamily (0.00s)
PASS
```

## CI / PR #1203 at new head

Branch work/r27-producer-extension-contracts, new head
b9ebc475694ba9a2324161ff388d19a2b7f774c5 (commit
`test(extension/v1): single-field required-field negatives + baseline per test`),
pushed 7c798147..b9ebc475, no force. PR State OPEN, MERGEABLE. Exact-head checks
at b9ebc475 (run 40863460054):
```
completed/success  PR · PR Selected Checks         composite gate
completed/success  PR · Public Contracts
completed/success  PR · Validation · source-contracts
completed/success  PR · Trusted Plan
completed/success  PR · Demo Pin
completed/success  PR · Focused Python
completed/success  Workflow policy
```
Skip-only gates (Targeted HA · docker / podman, Runner Interface, Consumer Pins,
Exact Candidate, Selected Runtime, Release Source Preflight, validate) are skips,
not failures. PR Selected Checks is green at the new head; go.mod/go.sum impact
from earlier rounds stays resolved (only the test file changes).

## Profile coverage map

Shipped contract schema families under contracts/ and their behavioral-coverage
status (schema Validate pass/fail; structural-only `$schema`/registry audits
noted separately):

- connection-profile/v1/profile.schema.json
  -> contracts/v0425_contracts_test.go:TestConnectionProfileSchemaRejectsAuthorityAndLocalState
  (PASS: positive shape + forbidden-extra-property + insecure-URL + non-const-version
  negatives). GENUINELY COVERED. (Required-field removal negatives per field are
  not asserted, but the schema is guarded; not an uncovered slice.)
- extension/v1/extension-descriptor.schema.json
  -> contracts/extension_trust_test.go:TestExtensionDescriptorSchemaRejectsGoValidatorDivergence
  + TestExtensionDescriptorSchemaRejectsInvalidIdAndFamily (PASS after round C). COVERED.
- extension/v1/extension-trust.schema.json
  -> no behavioral test yet; `extensionSchema` helper defined but uninvoked.
  UNCOVERED (the genuinely-uncorrectable slice; owner decision needed to expand
  scope beyond the descriptor, see recommendation). Not padded.
- provider-plan/v1/plan.schema.json
  -> contracts/v0425_contracts_test.go:TestProviderPlanSchemaEnforcesDataPreservation. COVERED.
- provider-impact/v1/{impact,consent,result}.schema.json
  -> contracts/provider_impact_test.go:TestProviderImpactMachineSchemasAndSharedFixtures. COVERED.
- provider-impact/v1/{scope,scope-result}.schema.json
  -> contracts/provider_impact_scope_test.go:TestProviderImpactScopeOfflineMachineContract. COVERED.
- machine/v1/{control,read-models,terminal-event,terminal-input}.schema.json
  -> contracts/machine_control_test.go, contracts/machine_read_models_test.go. COVERED.
- targetaccess/v1/wire.schema.json
  -> contracts/{targetaccess_wire_test,compose_phase_wire_test,quadlet_completion_wire_test}.go. COVERED.
- footprint/v1/footprint.schema.json
  -> contracts/v0425_contracts_test.go:TestFootprintSchemaMatchesDomainFixtures. COVERED.
- service/v1/* (11 families), binding/v1, provider/v1, development/v1/*
  -> structural only: contracts/contracts_test.go
  (TestServiceSchemasUseJSONSchema202012AndStayProviderNeutral,
  TestShippedServiceFamiliesHaveSchemas, TestProviderAndBindingSchemasUseJSONSchema202012).
  NOT covered by a behavioral Validate test; out of this round's reserved scope.
- conformance/provider/v1/profile.json -> not a `.schema.json`, not embedded;
  no behavioral test warranted.

Profile-contract conclusion: connection-profile (the only shipped "profile"
schema) is genuinely covered; there is no uncovered profile-contract slice to
qualify this round. The unguarded surface is extension/v1/extension-trust, an
extension-family contract. Recommend the owner-approved scope wording
"extension/v1 contract family allowed" rather than "profile-contract slice".

o213-SCOPE-QUESTION
