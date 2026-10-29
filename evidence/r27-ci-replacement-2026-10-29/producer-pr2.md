# Producer PR #1203 fix round (o211)

Lane o211. Fix round on PR #1203 (branch work/r27-producer-extension-contracts,
candidate head a2da4174). Task prompt:
`evidence/board-2026-10-29/prompts/o211.txt`. Task:
`baseharbor-plan/tasks/t-20261029-r27-ci-producer.md`. Review input:
`evidence/board-2026-10-29/codex-rv1203.md` (VERDICT REQUEST_CHANGES, 2 findings).

## Deviation from task scope (FIX 3)

Dispatch FIX 3 offered two paths: prefer a profile slice if one genuinely exists
and is uncovered, otherwise keep the extension slice. Inspecting `contracts/`:
`contracts/connection-profile/v1/profile.schema.json` is a shipped normative
contract with an existing behavioural test
(`TestConnectionProfileSchemaRejectsAuthorityAndLocalState` in
`contracts/v0425_contracts_test.go`). Every other shipped family (service,
binding, machine, provider, provider-impact, provider-plan, footprint,
connection-profile) already has behavioural coverage; only `extension/v1`
(the 2 schemas under test here) was unguarded.

Decision: the connection-profile slice is already covered, so there is no
uncovered profile slice to qualify. The extension/v1 slice remains the correct
and genuinely-missing target. The original candidate's extension tests are kept,
fixed to the codex recipe, and stripped of the go.mod/go.sum promotion that was
blocking the planner. No scope deviation from the authoritative task contract
beyond reverting the candidate's accidental dependency promotion.

## PLAN

1. Read `codex-rv1203.md`, task note and producer-slice2 evidence.
2. Re-attach the existing branch in worktrees/o211 (origin/work/r27-producer-extension-contracts,
   head a2da4174) without recreating it.
3. FIX 1 (blocking): the diff carried go.mod/go.sum edits that promoted indirect
   deps (go-jose, jsonschema-go, oauth2, mongo-driver) to direct, which the
   planner reads as unknown module impact -> coverage-unresolved.
   `git checkout origin/develop -- go.mod go.sum` restored develop's module graph;
   confirmed the test still compiles+passes with `jsonschema-go` as an indirect
   dependency (it already is a direct import of the test package, resolved through
   the contracts registry, so no promotion is needed).
4. FIX 2: rewrote `contracts/extension_trust_test.go` so each case derives from a
   schema-valid baseline descriptor (asserts pass once), then mutates exactly one
   field per negative case and asserts the schema names that constraint. Fixed the
   misleading comment at old line 79 claiming a frozen-family guard: the new tests
   validate the descriptor schema's id pattern and family enum, they do not
   invoke the trusted-document family guard.
5. FIX 2 fixture correction: the descriptor id pattern is
   `^[a-z0-9][a-z0-9._-]*/[a-z0-9][a-z0-9._-]*$`, which permits internal dashes,
   so the original `trailing-dash/x-` fixture passed. Replaced with ids that
   actually violate the pattern (uppercase segment, leading dash in each segment).
6. Verified: `go vet ./contracts/`, `go build ./...`, full
   `go test ./contracts/ -count=1` and the focused `-run '^TestExtension'`.
7. Committed forward (no force), pushed; verified PR #1203 selected checks green.

## Repo-rule compliance

- Work confined to worktrees/o211; no edits in baseharbor-plan, no git in
  baseharbor-plan.
- go.mod/go.sum restored to develop's graph and committed clean; the post-fix
  diff of HEAD vs origin/develop contains only .github workflows,
  `contracts/extension_trust_test.go` and two `scripts/` receipt tests. No module
  graph change is shipped, so the planner's impact question no longer applies.
- Test compiled and run with the module graph of origin/develop
  (f95b3446) in an isolated GOPATH/GOCACHE under /tmp; no promotion of indirect
  dependencies.
- No merge, no self-approval, no PR edit. CI selection left to the repo's
  planner; the exact-head PR Selected Checks composite gate is the required
  verifier and it is green.

## Fix 1 (blocking CI / go.mod impact)

Before: candidate diff vs develop included go.mod (+18/-...) and go.sum (+103
-...) changes that demoted mongo-driver/xdg-go/youmark from indirect and added
go.sum h1 lines for go-jose, jsonschema-go, oauth2, mongo-driver, etc. The
planner diagnostic at run 40857674413 was
`BLOCKED: coverage-unresolved: unknown impact for go.mod; unknown impact for
go.sum`.
Fix: `git checkout origin/develop -- go.mod go.sum`. The contracts test only
imports `github.com/google/jsonschema-go/jsonschema`, which develop already lists
as `// indirect`; the build resolves it through the contracts registry without
promotion.
Verify: `git diff origin/develop -- go.mod go.sum` is empty after checkout;
`go test ./contracts/ -count=1 -run '^TestExtension'` passes with develop's
graph.

## Fix 2 (test correctness)

`contracts/extension_trust_test.go` rewritten from 176 lines of mostly no-op
schema plumbing to two behavioural tests:

- `TestExtensionDescriptorSchemaRejectsGoValidatorDivergence`: builds a
  schema-valid baseline (id `example.com/org.example-extension`, family
  `provider`, oci_reference + dialect present), asserts it passes once, then
  removes `artifact.oci_reference` and `configuration_schema.dialect` and asserts
  the packaged schema rejects it. The Go `Metadata.Validate()` fixture comment is
  corrected: the test now shows the schema, not the Go validator, enforces these
  required fields.
- `TestExtensionDescriptorSchemaRejectsInvalidIdAndFamily`: one valid baseline,
  then per-iteration mutation of exactly `id` (4 invalid id patterns) and exactly
  `family` (3 out-of-enum values), each asserting the schema names the failing
  constraint.

The old line-79 claim that the test "prevents a frozen-family guard from missing
a family" was false; the extension descriptor schema has no such guard and the
test never calls `internal/extension` trust verification. Comment removed.

Verify:
```
$ GOPATH=/tmp/o211-gopath GOCACHE=/tmp/o211-gocache go test ./contracts/ -count=1 -run '^TestExtension' -v
=== RUN   TestExtensionDescriptorSchemaRejectsGoValidatorDivergence
--- PASS: TestExtensionDescriptorSchemaRejectsGoValidatorDivergence (0.00s)
=== RUN   TestExtensionDescriptorSchemaRejectsInvalidIdAndFamily
--- PASS: TestExtensionDescriptorSchemaRejectsInvalidIdAndFamily (0.00s)
PASS
```

## Fix 3 (slice selection)

`contracts/connection-profile/v1/profile.schema.json` exists and is already
covered by `TestConnectionProfileSchemaRejectsAuthorityAndLocalState`; no uncovered
profile slice exists to qualify. extension/v1 remains the genuinely-missing slice.

## Verification

Isolated (`GOPATH=/tmp/o211-gopath GOCACHE=/tmp/o211-gocache`):
```
go vet ./contracts/                      # clean
go build ./...                           # clean
go test ./contracts/ -count=1            # ok contracts 0.390s
go test ./contracts/ -count=1 -run '^TestExtension' -v   # 2 PASS
```

## CI / PR #1203

Branch work/r27-producer-extension-contracts, new head
`7c798147b955018f8d900a39d54d18d9296b79e0` (commit
`test(extension/v1): baseline+negative schema coverage`, pushed a2da4174..7c798147).
No force-push; a2da4174 preserved. Exact-head checks at 7c798147:

```
completed/success  PR · Public Contracts       (id 123402814880)
completed/success  PR · Validation · source-contracts
completed/success  PR · Focused Python
completed/success  PR · Trusted Plan
completed/success  PR · Demo Pin
completed/success  Workflow policy
completed/success  PR Selected Checks         composite gate
```
PR State OPEN, MERGEABLE. The previously-blocking go.mod/go.sum impact is
resolved; PR Selected Checks is green at the new head.

## Evidence

- New head: 7c798147b955018f8d900a39d54d18d9296b79e0
- PR: https://github.com/mcpdev80/baseharbor/pull/1203
- Review: evidence/board-2026-10-29/codex-rv1203.md
- Slice rationale: baseharbor-plan/evidence/r27-ci-replacement-2026-10-29/producer-slice2.md

o211-DONE
