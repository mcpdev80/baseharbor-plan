# w343-0428-344-pagination — card 0428-344 (t-20261128-hunt48-runtime-pagination-contract)

Mission: `coordinator/missions/w343-0428-344-pagination.txt` (coordinator e6ca7696-b1f8-492d-b226-876b16925fc5)
Repo: mcpdev80/baseharbor, branch `w343-0428-344-pagination` against `develop`.

## Ansatz (visible block, owner directive)

- Card frontmatter owner VERBATIM (fetched at runtime from plan `origin/main`, commit
  `4c2ebb767` "claim: 0428-344 -> w343-0428-344-pagination"):
  `owner: w343-0428-344-pagination` (no `(lane X)` form → canonical identity = full owner value).
- git identity used (set per-worktree via `git config --worktree`, bare `git config` untouched):
  - `user.name = w343-0428-344-pagination`
  - `user.email = w343-0428-344-pagination@baseharbor.local`
- Commit invocation: worktree-scoped config is set, so plain `git commit` inside the worktree
  resolves to the canonical identity; every commit is additionally gated by
  `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` BEFORE the commit.
- Pre-push gate line (mechanical, before EVERY push):
  `git show -s --format=%an HEAD` must equal `w343-0428-344-pagination` exactly.

## Base attestation

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` →
  `5a37ddbd9a06dd44f6068d3266ff2ed853a84a74`
- Branch `w343-0428-344-pagination` created directly from that exact SHA
  (`git merge-base --is-ancestor 5a37ddbd9... HEAD` → OK, ANCESTRY-OK in transcript).
- Remote resolution (FIRST git action in worktree, `git remote -v`):
  `origin` and `lane-origin` both → `https://github.com/mcpdev80/baseharbor.git`. Only `lane-origin` used.
- `git diff origin/develop...HEAD --name-only` and `git log --oneline origin/develop..HEAD`:
  recorded below at PR time (must show only this lane's files/commits).

## Planning repo zone check (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`)

```text
baseharbor	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
baseharbor	https://github.com/mcpdev80/baseharbor.git (push)
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
upstream2	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
upstream2	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Correct zone (`/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, NOT `workers/baseharbor-plan`).
Evidence published via an isolated plan worktree + plan PR (main is protected).

## Contract decision (Owner decision 2026-11-25 on card: breaking contract changes allowed pre-v1.0)

Finding H-V48 BF-48-4: runtime API list endpoints have no pagination contract. Inventory of the
current runtime-facing list responses (develop `5a37ddbd9`):

- `GET /api/v1/apps/{app}/secrets` (`internal/applicationsecretapi/handler.go:60,66-78`) → `{"secrets":[...]}`, unbounded, no pagination fields.
- `GET /runtime/v1/capabilities` (`internal/applicationruntimeapi/handler.go:122-136`) → `{"capabilities":[...]}`, bounded by the built-in capability registry.
- Machine navigation list results `app.list` / `target.list` / `workspace.list` / `runtime.list`
  (`internal/machine/navigation.go`, read-models `internal/machinereadmodels/artifacts.go`) → full result arrays, no pagination fields.

Decision (minimal sufficient scope): declare an explicit bounded pagination contract as a shared
`pagination` metadata envelope emitted by every listed runtime list response:

- Request: optional query parameters `page` (default 1) and `page_size` (default and maximum 100, cap 100).
- Response gains a `pagination` object: `{ "page", "page_size", "total", "total_pages", "next_page" }`
  (`next_page` null on the last page) as a sibling of the item collection. Omitting the parameters
  returns the complete observation as one bounded default page (page 1, page_size = total) for the
  navigation results, or the first 100-item page for the HTTP endpoints.
- Invalid pagination parameters fail closed with the canonical `apierror` envelope `bad_request`.
- No backward-compatibility shim (pre-v1.0 Owner decision).

Final shape after implementation review: the contract is the single shared struct
`apierror.Pagination` (fields `page`, `page_size`, `total`, `total_pages`, `next_page`) plus
`apierror.PageParams` / `ParsePageParams` / `Paginate` in `internal/apierror`. Machine navigation
results (`machine.ApplicationListResult`, `TargetListResult`, `WorkspaceListResult`) and the read-model
`RuntimeListResult` carry it as a named `pagination` JSON field; `machine.PaginateMachineList` is the
single constructor for the default full-bounded-page shape. The read-model schema/golden artifacts are
regenerated from the Go types (contract test `TestMachineReadModelArtifactsDeriveFromActualCoreTypes`
stays green by derivation).

## PLAN

1. Read contract, hunt akte BF-48-4, claim verification (done — see above).
2. Base attestation + worktree + identity gates (done — see above).
3. Implement `internal/apierror/pagination.go`: `PageParams`, `Page`, `Pagination` envelope, query parsing + validation, apply/total helpers.
4. Implement `internal/apierror/pagination_test.go`: focused contract tests (defaults, cap, invalid → fail closed, last page, envelope JSON shape).
5. Wire `GET /api/v1/apps/{app}/secrets` (`applicationsecretapi`) to the contract + update its handler test expectations.
6. Wire `GET /runtime/v1/capabilities` (`applicationruntimeapi`) + update handler test expectations.
7. Wire machine navigation list results (`internal/machine/navigation.go`: app/workspace/target list results) + read-model regeneration check; contract test `contracts/machine_read_models_test.go` stays green via derived schema.
8. Documentation: `docs/spec/runtime-list-pagination-v1.md` (new normative spec), register it in `docs/spec/README.md`, `mkdocs.yml` and `mkdocs.de.yml` nav, DE nav entry links the canonical English page marked `EN` per STYLE_GUIDE (reference/spec pages need no translation; locale-parity script excludes `de/` and checks file-set parity → new file gets a DE stub link page only if the parity script requires it — verify by reading script, not guessing).
9. Test-route check: `source-contracts` CI check runs `go test ./internal/application/... ./contracts/...`; confirm whether `internal/apierror` and the touched handler packages are covered by the auto-discovered package CI; record route in evidence. No `.github/**` edits.
10. Local prechecks: `gofmt -l`, `go vet ./internal/apierror/... ./internal/applicationsecretapi/... ./internal/applicationruntimeapi/... ./internal/machine/...`, `go build ./...` (NO local tests).
11. Commit (identity-gated), push branch, open DRAFT PR against develop.
12. Watch own hosted CI run to terminal state; record FULL40 + run IDs; PR head comment.
13. Move PR to ready, handoff, evidence on origin/main, END.

## Candidate and CI

- Candidate commit: `969362e397a14d3f1e173697750386079aa4f5d2` (branch `w343-0428-344-pagination`).
- Identity gate: `git show -s --format='%h an=%an cn=%cn' HEAD` →
  `969362e39 an=w343-0428-344-pagination cn=w343-0428-344-pagination` (matches the card frontmatter
  owner value exactly; set via `git config --worktree`, `git var GIT_AUTHOR_IDENT`/`GIT_COMMITTER_IDENT`
  verified before the commit).
- Ancestry: `git merge-base --is-ancestor 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 HEAD` → OK.
- `git log --oneline origin/develop..HEAD` → exactly one line:
  `969362e39 feat(api): bounded pagination contract for runtime list endpoints (0428-344)` (own commit only).
- `git diff origin/develop...HEAD --name-only` → 19 files (see PR); no `.github/**`, no `cmd/baha`,
  no `docs/reference/cli.md`/`errors.md` (mission write-set respected).
- Delivery witness after push:
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/w343-0428-344-pagination` →
  `969362e397a14d3f1e173697750386079aa4f5d2	refs/heads/w343-0428-344-pagination`
- PR: https://github.com/mcpdev80/baseharbor/pull/1871 (DRAFT since creation; moved to ready at handoff).
- Local prechecks (non-test only): `go build ./...` OK, `go vet ./...` OK, `gofmt -l` clean,
  `bash scripts/documentation-audit.sh` PASS (EN/DE parity + DE technical integrity).
- Test route: new Go tests are package-discovered by the `go-unit-tests` fallback
  (`go test ./... -count=1`) and the contracts test runs via `source-contracts`
  (`go test ./internal/application/... ./contracts/...`). No `.github/**` change was needed.
- Hosted CI runs:
  - Run 1: 45884310220 (event `pull_request`, draft phase) → cancelled by the ready transition (concurrency).
  - Run 2: 45884566859 (event `pull_request`, `ready_for_review` on exact head 969362e39…) → FAILED
    `PR · Trusted Plan`: fail-loud catalog rule — changed `internal/**` sources have no row in
    `scripts/pr-gate-coverage.json`: "uncataloged source change, no declared runtime gate owner:
    internal/apierror/pagination.go (id source.internal_apierror_pagination_go): add this source with
    its surfaces to scripts/pr-gate-coverage.json, …". `scripts/pr-gate-coverage.json` is the shared
    base required-plan catalog (AGENTS "gate-catalog doctrine"; mission write-set excludes it) — this
    is the single allowed coordinator route case. The needed change: add one component row per changed
    source with surfaces pointing at the package-discovery validation (not the Docker/Podman
    data-capabilities example from the error message, which would bind heavyweight runtime gates to
    pure unit-test code):
    {"id": "source.internal_apierror_pagination_go", "path": "internal/apierror/pagination.go", "surfaces": ["source.package.integration.static.public.contracts"]} and the same for
    internal/apierror/pagination_test.go, internal/applicationruntimeapi/handler.go,
    internal/applicationruntimeapi/pagination_contract_test.go, internal/applicationsecretapi/handler.go,
    internal/applicationsecretapi/pagination_contract_test.go, internal/machine/navigation.go,
    internal/machine/pagination_contract_test.go, internal/machinehttp/source_transfer.go,
    internal/machinereadmodels/artifacts.go, internal/sourcetransfer/transfer.go.
    (Note: `internal/machinehttp/source_transfer.go` is listed but `machinehttp` has no existing
    package row; the same single row form applies.)
  - Run 3 (state): 45884719597 (event `pull_request`, second exact-head trigger via authorized
    close+reopen on the same head 969362e39…) — observed terminal below.

## Cleanliness

- No containers/compose projects started (pure Go + docs lane). `docker ps -a` before/after: n/a for this lane's host — tests run only in Hosted CI.
- Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/w343-0428-344-pagination-wt` (removed after END per coordinator policy).

## Handoff

- PR: (pending)
- Candidate SHA: (pending, FULL40)
- Run IDs: (pending)
- State: (pending)

END: (pending)
