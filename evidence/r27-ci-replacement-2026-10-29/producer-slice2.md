# Producer slice 2: next public-contracts producer for the first automatic chain run

Lane o208. READ-ONLY analysis slice. No commits in baseharbor-plan; this evidence
file is the only write. Task prompt: `evidence/board-2026-10-29/prompts/o208.txt`.

## PLAN

1. Read `pr-gate-plan.py` and `pr-diff-base.py` first (task requirement) to learn
   the planner contract before simulating anything.
2. Map every shipped contract schema family against spec/docs and against the test
   coverage that currently exists in `contracts/*_test.go`.
3. Cross-check `git log --oneline -30 -- contracts/` on `origin/develop` and the
   open PRs (#1202 f60, #1160 dependabot) to avoid collision with f60/#1202 and
   in-flight r27 work.
4. Select the smallest genuinely-missing contracts slice and prove it is not a
   no-op by running the real Go `source-contracts` check on a scratch worktree of
   `origin/develop`.
5. Simulate `pr-gate-plan.py` locally on the scratch worktree for the candidate
   file set and capture the planner output.
6. Deliver the chosen slice, the exact reservation list, the planner output, and
   the branch-name suggestion.

## Chosen slice

Candidate file (new, test-only):

- `contracts/extension_trust_test.go`  (package `contracts_test`, repo root; Go
  discovers package-root `_test.go` files, so a sub-directory test would not be
  compiled — placement matters)

This PR adds behavioral coverage for the `extension/v1` contract family, which is
authoritative per `docs/spec/extension-artifact-trust-v1.md` (both
`extension-descriptor.schema.json` and `extension-trust.schema.json` are declared
the normative shipped schemas) but currently has **zero** behavioral schema
tests. The only existing contract coverage for it is the offline registry audit
(`contracts/registry_test.go`), which asserts JSON validity, `$id`/namespace
conformance and `$ref` resolution — never the trust or family semantics the spec
declares normative.

Why this is needed (real, not a no-op):

- Every other shipped contract family already has a behavioral schema test:
  `service`, `binding`, `machine`, `provider`, `provider-impact`,
  `provider-plan`, `connection-profile`, `footprint`. Only `extension/v1`
  (2 normative schemas) is unguarded.
- The schema and the Go validator (`internal/extension/metadata.go`) diverge in
  two places the new test catches: the descriptor schema requires
  `artifact.oci_reference` and `configuration_schema.dialect`, neither of which
  `Metadata.Validate()` enforces. A valid-by-Go-metadata descriptor is rejected
  by the schema (`required: missing properties: ["oci_reference"]` and later
  `["dialect"]`). The test ties the packaged schema to the real verifier so the
  schema cannot silently drift from the runtime contract.
- `TestExtensionDescriptorSchemaRejectsGoValidatorRejects` asserts the schema
  rejects an invalid extension id pattern and an out-of-enum family, closing the
  trust boundary at the public-contracts surface for the extension family.

No genuinely-missing slice was invented: the 10 service families listed in
`TestShippedServiceFamiliesHaveSchemas` plus the `vector` family added in #1199
already cover all 11 `service/v1` schemas, and #1199 is merged to
`origin/develop` (7a4debcc). f60's branch `work/r27-pin-o201-fwd` already carries
#1199, so this slice does not duplicate it.

## Exact reservation list (file paths)

- `contracts/extension_trust_test.go` (added by this slice; test-only)
- `contracts/extension/v1/extension-descriptor.schema.json` (read-only,
  authoritative subject)
- `contracts/extension/v1/extension-trust.schema.json` (read-only, authoritative
  subject)
- `internal/extension/metadata.go` (read-only, real validator under test)
- `internal/extension/trust.go` (read-only, `VerifyArtifact`/`Verify` trust model
  under test)

Planner planner output proving gate selection:

```
$ git worktree add -f /tmp/o208-scratch origin/develop   # 80d03122 ... #1201
$ # add contracts/extension_trust_test.go (package contracts_test)
$ git commit -m "test(extension/v1): behavioral trust + descriptor schema coverage"
$ # HEAD=e796918d1724aaa6c44f580c95bd665c221a4fca, develop=80d0312276aab8829deb80188aa9902ff0183b73
$ python3 scripts/pr-diff-base.py --repository /tmp/o208-scratch \
      --target-base 80d0312276aab8829deb80188aa9902ff0183b73 \
      --head e796918d1724aaa6c44f580c95bd665c221a4fca
$ GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop \
      python3 scripts/pr-gate-plan.py --diff <diff.json> \
      --requirements scripts/release-requirements.json \
      --mapping scripts/pr-gate-map-v1.json
{
  "broad_required": false,
  "coverage_status": "resolved",
  "head_sha": "e796918d1724aaa6c44f580c95bd665c221a4fca",
  "integration_sha": null,
  "mapping_schema": "baseharbor.pr-gate-plan/v1",
  "merge_base_sha": "80d0312276aab8829deb80188aa9902ff0183b73",
  "release": "v0.4.26",
  "reasons": [
    "contracts/extension_trust_test.go: contract"
  ],
  "schema": "baseharbor.pr-gate-plan/v1",
  "selected_gates": [
    "integration/static/public-contracts"
  ],
  "target_base_sha": "80d0312276aab8829deb80188aa9902ff0183b73",
  "unresolved_coverage": [],
  "required_validation_checks": [
    { "command": "go test ./internal/application/... ./contracts/...",
      "id": "source-contracts",
      "owner": "CI source / contracts" }
  ],
  "validation_contract": "Enforce all required_validation_checks independently of selected_gates; zero selected_gates is valid only when coverage_status is resolved. If unresolved, final check MUST fail closed; never treat as no checks or automatically run the complete release catalog."
}
```

Selected gate: `integration/static/public-contracts` (planner maps any
`contracts/*.json`/`*.go` change to this gate; `coverage_status: resolved`,
`broad_required: false`). The `source-contracts` check (`go test
./internal/application/... ./contracts/...`) passed on the scratch worktree:

```
ok  github.com/mcpdev80/baseharbor/internal/application   47.015s
ok  github.com/mcpdev80/baseharbor/contracts               0.389s
```

## Candidate branch name suggestion

`work/r27-producer-extension-contracts`

For a later lane to open the ordinary contributor PR that makes this chain's
`PR · Public Contracts` gate execute. Keep it test-only and repo-root
`contracts_test.go` placement (a sub-directory `_test.go` is not compiled into
the `contracts` package).

## repo-rule compliance

- Read-only analysis in baseharbor-plan; the scratch worktree lived in
  `/tmp` and was removed + pruned. No commit in baseharbor-plan.
- `pr-gate-plan.py` and `pr-diff-base.py` were read in full before simulation.
- Simulation ran on a scratch worktree of `origin/develop` (80d03122) with the
  authenticated runner context set (`GITHUB_REPOSITORY`/`GITHUB_BASE_REF`) exactly
  as CI provides it; no PR content was read for qualification.
- Collision check: #1202 (f60, ci publish token) and #1160 (dependabot) touch no
  contracts files; #1199 is already on develop and on f60's branch. This slice is
  disjoint from both.
- Go `source-contracts` check executed locally and passed; no CI gate claimed as
  green, only the local verification reproduced above.

o208-DONE
