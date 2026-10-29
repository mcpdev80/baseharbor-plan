# Producer PR 2: ordinary contributor PR for the first automatic chain run

Lane o209. Implemented the ordinary contributor PR (PR only, NOT merged). Task
prompt: `evidence/board-2026-10-29/prompts/o209.txt`. Evidence follows
producer-slice2.md (o208's exact slice) and producer-slice2.md's candidate
branch `work/r27-producer-extension-contracts`.

## PLAN

1. Read o209.txt, producer-slice2.md, baseharbor/AGENTS.md and
   baseharbor/docs/DEVELOPMENT_GUIDELINES.md.
2. Confirm the o209-BLOCKED guard: fetch origin, verify develop HEAD
   (f95b3446), grep `origin/develop:contracts/contracts_test.go` for the
   extension family. Result: NO extension match on develop, so the slice is a
   genuine addition, not a no-op.
3. `git worktree add` a new branch `work/r27-producer-extension-contracts` from
   origin/develop at /home/marcel/dev/baseharbor-ecosystem/worktrees/o209.
4. Implement exactly o208's selected file `contracts/extension_trust_test.go`
   (package `contracts_test`, repo root). Added three tests:
   - `TestExtensionV1SchemasResolveAndValidate`: a valid extension trust document
     validates against the packaged descriptor + trust schemas (2020-12, `$ref`
     resolved from the packaged registry), tying schema to the real verifier.
   - `TestExtensionDescriptorSchemaRejectsGoValidatorDivergence`: a descriptor
     valid under `extension.Metadata.Validate()` (missing `artifact.oci_reference`
     and `configuration_schema.dialect`) is rejected by the schema, proving the
     frozen-family guard cannot miss the family.
   - `TestExtensionDescriptorSchemaRejectsInvalidIdAndFamily`: schema rejects
     invalid extension id patterns and out-of-enum families.
5. `go mod tidy` to move `github.com/google/jsonschema-go` (already direct in
   develop production code) and re-classify already-direct modules to a clean
   direct require. No other files touched.
6. Run locally: `go test ./contracts/ -run TestExtension -count=1`; then
   `go test ./contracts/... -count=1`; `go vet ./contracts/...`;
   `bash scripts/source-readability-audit.sh`.
7. One coherent commit; push; open PR #1203 to develop. Do NOT merge, do NOT
   touch CI files, no git in baseharbor-plan.
8. Write this evidence file.

## Implementation

File: `contracts/extension_trust_test.go` (package `contracts_test`, repo root;
Go compiles package-root `_test.go` files, a sub-directory `_test.go` would not
be compiled into the `contracts` package).

Tests exercise `internal/extension/metadata.go` (`Metadata.Validate`) and
`internal/extension/trust.go` (`VerifyArtifact`) as the real validator/trust
model under test; read-only authoritative subjects `contracts/extension/v1/*.schema.json`.

Local verification:

```
$ cd worktree && go test ./contracts/ -run TestExtension -count=1
=== RUN   TestExtensionV1SchemasResolveAndValidate
--- PASS: TestExtensionV1SchemasResolveAndValidate (0.01s)
=== RUN   TestExtensionDescriptorSchemaRejectsGoValidatorDivergence
--- PASS: TestExtensionDescriptorSchemaRejectsGoValidatorDivergence (0.00s)
=== RUN   TestExtensionDescriptorSchemaRejectsInvalidIdAndFamily
--- PASS: TestExtensionDescriptorSchemaRejectsInvalidIdAndFamily (0.00s)
ok  	github.com/mcpdev80/baseharbor/contracts	0.016s

$ go test ./contracts/... -count=1
ok  	github.com/mcpdev80/baseharbor/contracts	0.330s

$ go vet ./contracts/...
(no output)

$ bash scripts/source-readability-audit.sh
Source readability
Go file size       PASS (<= 800 lines or no worse than explicit baseline)
Function span      PASS (<= 200 lines or no worse than explicit baseline)
Regression ratchet PASS (new/worsened violations fail closed)
```

The divergent fixture in `TestExtensionDescriptorSchemaRejectsGoValidatorDivergence`
passes `extension.Metadata.Validate()` (valid OCI reference) yet is rejected by
the packaged schema for missing `artifact.oci_reference`/`configuration_schema.dialect`
— the schema's `required` enforces what the Go validator never does.

## Git / PR

- Worktree: `/home/marcel/dev/baseharbor-ecosystem/worktrees/o209` (branch
  `work/r27-producer-extension-contracts`, created from origin/develop f95b3446).
- Commit: `a2da4174 test(extensions/v1): behavioral trust + descriptor schema coverage`
- Head SHA: `a2da41742a738a276a6c2fdd60cb63da87892d99`
- PR: #1203 `https://github.com/mcpdev80/baseharbor/pull/1203` (state OPEN,
  MERGEABLE, base develop). NOT merged.

Files changed: `contracts/extension_trust_test.go` (added), `go.mod`, `go.sum`.
go.mod/go.sum change is `go mod tidy` re-classifying already-direct modules
(jsonschema-go is already a direct dependency of develop production code) to a
clean direct require; no module versions changed, no other files touched.

## repo-rule compliance

- Test-only slice exactly matching producer-slice2.md's selected file; no other
  product files. No CI files touched.
- `go mod tidy` required by the test; jsonschema-go already direct in develop
  (cmd/baha/mcp_application_authoring.go, contracts/*, internal/machinereadmodels/*).
  Diff is re-classification + require-block re-sort; no version changes.
- Local `go test ./contracts/...`, `go vet ./contracts/...` and
  source-readability-audit.sh executed and passed. No CI gate claimed green;
  only the local verification reproduced above.
- PR #1203 opened to develop, not merged, awaiting main registration per
  task prompt. No git activity in baseharbor-plan.

o209-DONE
