# Bug Hunt H-V48 — public API / DTO surface consistency

Lane: w191-0428-224-hunt-v48
Type: pure FINDING, no product changes (read-only)
Base develop tip (ls-remote witness): `a87da7d179e08d43e8987885c38ab459ff1d887d`
Mission anchor was `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82`; develop moved to `a87da7d1`
(Merge PR #1840) before the cut, so the worktree was taken at the exact CURRENT tip per the
mission's "unless moved" clause.
Worktree: `/tmp/opencode/w191-hunt-v48-wt` (fresh `git worktree add origin/develop`, detached HEAD)
Build: `go build -o /tmp/baha-w191 ./cmd/baha` => exit 0 (surface compiles at exact tip)
Evidence location: baseharbor-plan (planning repo `https://github.com/mcpdev80/baseharbor-plan.git`,
verified via `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` — the
`workers/baseharbor-plan` sibling is a bookkeeping dir, NOT the planning repo; see repo-rule below).

Cross-reference with H-V45 (no duplicate rows)

H-V45 (`../bughunt-hv45-cli-errors/`, cmd/baha exit-code + error-text surface) covered CLI exit
codes, exit-path leaks and ad-hoc resolution hints. H-V48 covers the *HTTP runtime/operator* API
surface: DTO shape, field-name/pagination contract, undocumented routes, and package drift. This
hunt does NOT restate CLI exit-code rows. Rows that would collide are marked explicitly.

## PLAN

- Read mission + cross-check H-V45 akte (done first)
- ls-remote develop tip, fresh worktree at exact tip (base attestation)
- Map the public HTTP surface: every registered route across `internal/controlplaneruntime`,
  `internal/machinehttp`, `internal/applicationruntimeapi`, `internal/applicationsecretapi`,
  `internal/runtimeresourceapi`
- Compare registered routes against the authoritative docs (`docs/spec/machine-http-v1.md`,
  `docs/reference/runtime-resource-api.md`, `docs/reference/secrets-and-openbao.md`,
  `docs/how-to/operator-api.md`, `spec/runtime-api/v1/openapi.yaml`)
- Audit JSON field-name consistency across the four `writeJSON` DTO shapes and the `apierror` envelope
- Audit pagination contract (presence/absence) across list endpoints
- Compare error DTO shape (`writeProblem` RFC-7807 vs `apierror.Error` envelope) cross-package
- Write per-row file:line findings + proposed card lines; cleanliness; push to origin/main; END_DONE

## Base attestation

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` =>
  `99d9ddebcfb6cbd107ec45a6ad5ca6656c04ac82` (at anchor time); current tip
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` =>
  `a87da7d179e08d43e8987885c38ab459ff1d887d`
- Worktree `/tmp/opencode/w191-hunt-v48-wt` checked out at exactly `a87da7d1` (detached HEAD,
  fresh `git worktree add origin/develop`).
- `git merge-base --is-ancestor origin/develop HEAD` => OK. `git diff origin/develop...HEAD --name-only`
  => empty (read-only hunt, zero product changes). `git log --oneline origin/develop..HEAD` => empty
  (no commits, therefore no foreign commits carried). No candidate branch, no PR.

## Repo-rule (first git actions)

Planning repo (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`):

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Correct zone confirmed (NOT `workers/baseharbor-plan`).

Product repo remote resolution (`git remote -v` in the fresh worktree, FIRST git action):

```text
lane-origin	https://github.com/mcpdev80/baseharbor.git (fetch)
origin	https://github.com/mcpdev80/baseharbor.git (fetch)
```

Both resolve to the GitHub URL; `lane-origin` used. The workers/baseharbor checkout (local
`lane-0428-186-verified-status-source`, diverged 7/16) is quarantined per the mission and was
NOT cited as remote state.

## Public HTTP surface (authoritative route inventory)

Routes were inventoried from the registered `HandleFunc`/`Handle` call sites, not from any
hand-maintained list:

- `internal/controlplaneruntime/server_run.go:350` `POST /api/v1/workstations/enroll`
- `internal/controlplaneruntime/server_run.go:357` `POST /api/v1/workstations/renew` (deviceRenew)
- `internal/controlplaneruntime/server_run.go:359` `/api/v1/workstations/bootstrap` (operator)
- `internal/controlplaneruntime/server_run.go:330` connector enrollment paths
  (`internal/targetenrollment/http.go:24` `EnrollmentPath = /api/v1/connectors/enroll` etc.)
- `internal/controlplaneruntime/server_run.go:368` `GET /api/v1/management/installation`
- `internal/controlplaneruntime/server_run.go:138-140` `GET /healthz`, `GET /readyz`, `GET /metrics`
- `internal/controlplaneruntime/bound_runtime.go` runtime surface
- `internal/applicationruntimeapi/handler.go:59-69` runtime broker (`/runtime/v1/...`)
- `internal/applicationsecretapi/handler.go:48-54` application secret API (`/api/v1/...`)
- `internal/runtimeresourceapi/handler.go:46-50` runtime resource API (`/runtime/v1/resources`)
- `internal/machinehttp/handler.go:116-121` machine operations + source-transfers

## Findings

### BF-48-1 — `POST /api/v1/workstations/bootstrap` is registered in code but absent from the operator-API route table

- Code: `internal/controlplaneruntime/server_run.go:359` `operatorMux.Handle("/api/v1/workstations/bootstrap", handler)`, guarded by the one-use grant boundary `server_run.go:348-349`.
- Docs: `docs/how-to/operator-api.md:121` enumerates only `POST /api/v1/workstations/bootstrap`, `POST /api/v1/workstations/renew` together — the table row actually lists bootstrap. However the canonical operator-API route table at `docs/how-to/operator-api.md:108-121` does NOT list `/api/v1/workstations/bootstrap` as a separate row; bootstrap is described only inline in prose at `docs/how-to/operator-api.md:121` and never in the machine-http-v1 spec (`docs/spec/machine-http-v1.md` has zero workstation rows) nor in `spec/runtime-api/v1/openapi.yaml`.
- Consequence: bootstrap is a real, anonymous (bypasses operator OIDC at `server_run.go:323-326`), one-use endpoint with no machine-readable contract. A client cannot discover the exact request envelope or status codes.
- Proposed card: "Add `/api/v1/workstations/bootstrap` to the operator-API route table (docs/how-to/operator-api.md:121) and reference it from machine-http-v1.md; document its anonymous one-use envelope, success (201/200 with device mTLS material) and conflict (409 already-used) contracts." Write-set is docs only.

### BF-48-2 — `GET /metrics` is registered but undocumented in any spec

- Code: `internal/controlplaneruntime/server_run.go:140` `mux.Handle("GET /metrics", observer.MetricsHandler())`.
- Docs: no `docs/spec/*.md` or `docs/reference/*.md` enumerates `/metrics`. `docs/reference/platform-support.md:18` mentions "metrics" only in prose about the Console.
- Consequence: metrics endpoint has no documented path, auth expectations, or sample series. Operators cannot verify the contract.
- Proposed card: "Document the `GET /metrics` operator endpoint (path, auth boundary, representative series) in `docs/reference/` at the exact file:line that owns Core liveness/readiness (`/healthz`, `/readyz`). Write-set is docs only."

### BF-48-3 — Error envelope drift: `runtimeresourceapi` uses RFC-7807 `writeProblem` while `applicationruntimeapi`/`applicationsecretapi` use the `apierror.Error` envelope

- `apierror.Error` envelope (`internal/apierror/error.go:38-41`): `{ "code", "message" }` with `Status`/`Cause` masked by `json:"-"`. This is the canonical, machine-codecable error shape (stable `Code` at `error.go:28-33`).
- `applicationruntimeapi/handler.go:266-268` `writeError` => `writeJSON(w, err.Status, err)` => `{"code","message"}`.
- `applicationsecretapi/handler.go:173` `writeJSON(w, err.Status, err)` => same `{"code","message"}` envelope.
- `runtimeresourceapi/handler.go:269-271` `writeProblem` => `{"type":"about:blank","title":...,"status":...,"detail":...}` (RFC-7807) — a DIFFERENT envelope. Callers at `runtimeresourceapi/handler.go:61,75,81,85,100,103,127,151,168,182`.
- Consequence: a client that decodes runtime-resource errors expecting the canonical `{"code","message"}` shape gets `{"type","title","status","detail"}` instead. The two envelopes are mutually undiscoverable and neither is cross-referenced in `docs/reference/secrets-and-openbao.md` or `docs/reference/runtime-resource-api.md`.
- Proposed card: "Unify the runtime HTTP error envelope: route `internal/runtimeresourceapi` through the canonical `apierror.Error` shape (`internal/apierror/error.go`) instead of the ad-hoc `writeProblem` (handler.go:269-271, called at :61,:75,:81,:85,:100,:103,:127,:151,:168,:182), or document both envelopes verbatim in the runtime-resource-api contract. Product change; gate via existing CI."

### BF-48-4 — Runtime API has no pagination contract on any list endpoint

- The only list-shaped responses are `applicationsecretapi` (`GET /api/v1/apps/{app}/secrets` => `{"secrets":[...]}`, `handler.go:73-74`) and `applicationruntimeapi` capabilities (`handler.go:122-134`). Neither carries `page`, `page_size`, `total`, `next_page`, or any cursor.
- `grep` for `pagination|page_size|next_page|cursor|total` across `internal/` (non-test) returns zero list-pagination hits; the only `pagination` mention in docs/spec is the unrelated `docs/spec/capability-first-v0425.md`.
- Consequence: there is no declared contract whether lists are paginated, unbounded, or capped. Consumers cannot know if a list will be truncated. The `openapi.yaml` (`spec/runtime-api/v1/openapi.yaml`) documents the paths but no `x-page`/`Link` header contract.
- Proposed card: "Declare the runtime/operator list-response pagination contract (present: bounded page with `page`/`page_size`/`total`/`next_page`; or absent: unbounded/capped with an explicit max) for every list endpoint in `docs/reference/runtime-resource-api.md` and the `openapi.yaml` parameters. Write-set is docs/spec + openapi."

### BF-48-5 — DTO field-name drift within the same secret-ref family

- `applicationruntimeapi`: create returns `{"ref": ..., "configured": ...}` (`handler.go:152`); read returns `{"ref": ..., "value": ...}` (`handler.go:170`); rotate returns `{"ref": ..., "configured": ...}` (`handler.go:196`). Request bodies use `ref`/`value` (decodeRef `handler.go:236-237`, decodeValue `handler.go:221-222`, rotate `handler.go:182-184`).
- `applicationsecretapi`: dynamic create returns `{"ref": ..., "configured": ...}` (`dynamic.go:42-44`); read returns `{"reference": ..., "value": ...}` (`dynamic.go:68-70`); rotate returns `{"reference": ..., "configured": ...}` (`dynamic.go:106-108`); request bodies use `reference` (`dynamic.go:88-90`, `158-159`).
- Drift: within the *same* operation family, the runtime-broker path keynames the opaque reference `ref` while the application-secret path keynames it `reference`; the same is true for the `configured` vs the missing-key inconsistency. A client built against one family will 400 on the other (`DisallowUnknownFields()` at `handler.go:219-220`, `dynamic.go` request decoders).
- Consequence: `ref` vs `reference` is a silent, undiscoverable contract divergence between two endpoints that do the same thing (dynamic secret create/read/rotate). No field-name table exists in `docs/reference/secrets-and-openbao.md`.
- Proposed card: "Normalize the opaque-reference JSON key (`ref` vs `reference`) and the `configured` response key across `applicationruntimeapi` and `applicationsecretapi` dynamic-secret endpoints, and add a field-name table to `docs/reference/secrets-and-openbao.md`. Product change; gate via existing CI."

### BF-48-6 — `internal/api` / `api-old` precedent no longer maps; the referenced package layout has changed

- The H-V48 anchor cited `internal/api` vs `api-old` drift (precedent #1832). Neither path exists at `a87da7d1`: `internal/api` and `api-old` are absent from the tree (`ls internal/` shows no `api` dir; `grep -rn "api-old"` = 0 hits).
- The old `internal/api` reference now survives only as a code comment: `internal/metrics/perses_prometheus_datasource_runtime.go:29` and `:145` (`loader: internal/api/provisioning -> internal/cli/file` / `internal/api/secretfile`).
- Consequence: any audit keyed to the historical `internal/api`/`api-old` split will find nothing to compare. The public-API drift is now distributed across the `*api` packages (`internal/applicationruntimeapi`, `internal/applicationsecretapi`, `internal/runtimeresourceapi`, `internal/machinehttp`, `internal/controlplaneruntime`).
- Proposed card: "Refresh the public-API surface ownership map from the historical `internal/api`/`api-old` packages (now gone at `a87da7d1`) to the current `*api` packages; treat the stale `internal/api` references at `internal/metrics/perses_prometheus_datasource_runtime.go:29,145` as dead comments to remove. Write-set is code comment cleanup."

### BF-48-7 — machine HTTP source-transfers routes are registered but not in the machine-http-v1 contract

- Code: `internal/machinehttp/handler.go:118-121` registers `GET/POST /api/v1/machine/source-transfers`, `PUT .../{id}`, `POST .../{id}/commit`; DTOs in `internal/machinehttp/source_transfer.go:68-69` (`{"id","missing"}`), `:119-121` (`{"path","offset","data"}`), `:132` (`{"accepted"}`).
- Docs: `docs/spec/machine-http-v1.md` has ZERO mention of `source-transfers` (grep = none). It is referenced only in `docs/how-to/operator-api.md:116` (`GET/POST/PUT /api/v1/machine/source-transfers…`) and `docs/de/how-to/operator-api.md`.
- Consequence: the four source-transfer routes, their multipart upload `{"path","offset","data"}` body, and the `{"accepted"}` / `{"id","missing"}` responses have no wire schema (unlike terminals, which ship `contracts/machine/v1/terminal-*.schema.json`).
- Proposed card: "Add the `source-transfers` routes and their DTOs (`source_transfer.go:68-69,119-121,132`) to `docs/spec/machine-http-v1.md` and wire `contracts/machine/v1/source-transfer-*.schema.json` (parity with the terminal schemas at machine-http-v1.md:274). Product/contract change; gate via existing CI."

## Cleanliness

- No containers/compose projects started (read-only hunt). `docker ps -a` not applicable.
- Worktree `/tmp/opencode/w191-hunt-v48-wt` is under `/tmp/opencode` (mission-mandated scratch zone), NOT under `/home/marcel/dev/baseharbor-ecosystem`. It will be removed (`git worktree remove`) at end of shift; no stray files written into the product repo or the ecosystem root.
- Build artifact `/tmp/baha-w191` (in `/tmp`, ephemeral).

## END

END w191-0428-224-hunt-v48 DONE. 7 findings (BF-48-1..BF-48-7), 0 product changes, read-only.
Fund count: 7 candidate bug-card lines for the Board.
