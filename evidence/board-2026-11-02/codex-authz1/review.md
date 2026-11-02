# Independent review: codex-authz1

ROLLE: CODEX-REVIEW
VERDICT: REQUEST_CHANGES

Reviewed PR #1272 head `be022b55d80d897af7a843d48e8b5ef008cd4c68` against base `640846e1d9d8df2b52c726a21cf5ad06206c51d6`. Reviewer: Codex, independent review session; no product changes. `git fetch` of `refs/pull/1272/head` over HTTPS yielded the reviewed SHA. `git ls-remote` confirmed the same head and base. Diff contains only `CHANGELOG.md`, `internal/application/manifest.go` and `cmd/baha/mcp_application_authoring_test.go`.

## Finding and recipe

- `cmd/baha/mcp_application_authoring_test.go:153`: The added test exercises a valid `baseharbor.app.adopt` request without Compose, but has no negative case demonstrating that an actually required intent field remains rejected by schema validation. The assigned contract explicitly requires both directions. Add a negative case through the same MCP schema-validation path, omitting an established required field and asserting rejection specifically for that missing field, rather than a later business-logic failure. Retain the successful no-Compose case and existing validation. Run the focused authoring tests, demonstrate the negative case fails if the relevant schema requirement is removed, and obtain the checks required for the changed candidate. Stop and request renewed independent review if the candidate changes; do not merge or accept while any required CI gate is red or unresolved.

## Other observations

- `internal/application/manifest.go:153`: `json:"compose,omitempty"` makes the string optional in JSON schema and omitted on JSON serialization when empty. The manual YAML parser (`internal/application/manifest_parse.go:306-310`) still stores a supplied `compose:` value; omitted value is the Go empty string, not a nil pointer. Existing `internal/application/v0425_contract_test.go:430` checks a supplied value. No other `Workload.Compose` production consumer was found beyond parsing; runtime `Compose` fields found in search are different structures.
- The positive regression invokes `baseharbor.app.adopt`, not `baseharbor.author` named in the assignment. Confirm with the focused tests that the same generated intent schema is exercised; add direct coverage for `baseharbor.author` if it is a separate route/schema.
- Run [41405869847](https://github.com/mcpdev80/baseharbor/actions/runs/41405869847) is completed on the exact head; all non-skipped jobs except `PR Selected Checks` succeeded. The aggregate failed with `coverage-unresolved: mixed registration/execution source needs independent diff review: cmd/baha/mcp_application_authoring_test.go`. This review requests changes and does not make the required check green. No CI bypass is authorized.
- The candidate was read-only reviewed; no local tests or product changes were performed. Remote refs were checked before the review and should be refreshed at acceptance.
