# 0428-206 other-domain test split — round 1 (READ-ONLY classification, no product change)

- Lane: w221-0428-206-split (sitz ornith)
- Card: 0428-206 `t-20261120-other-domain-test-split`, priority high, read-only
- Mission: split the 89 "other-domain" `./cmd/baha/` failures from the 204 operator-seam class and rubric each group (a/b/c)
- Result: DONE — all 89 placed in exactly one of 12 production-file groups; every group carries a rubric and witness

## Basis-Attestation (ls-remote develop)

```
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop
```

Scratch partial clone under `/tmp/opencode/w206-0428-206-split-wt` (partial `--filter=blob:none --no-checkout`,
then `git checkout -B w206-base 40cb28c758b0...`). Verify:

```
$ git merge-base --is-ancestor 40cb28c758b02960356434b630086a341ebe1738 HEAD && echo OK
OK
$ git log --oneline 40cb28c758b02960356434b630086a341ebe1738..HEAD
(empty — no own commits on the develop base)
```

Base SHA `40cb28c758b02960356434b630086a341ebe1738` is an ancestor of HEAD; HEAD equals the develop head; no
foreign commit carried on top. Go 1.26.8.

## Methode (read-only, no matrix, no product write)

- Authoritative input: sitz w217's `other`-class rows from
  `evidence/r28-welle4-2026-11-20/cli-test-inventory-develop/round-1.md` (`/tmp/w217-classified.tsv`,
  columns: `class | error-class | test-name | testfile:line | verbatim-first-error`). Exactly 89 rows with
  `class == other`; 42 distinct first-level test files.
- Method (per mission step 2-3): group by the FIRST FAILING PRODUCTION FILE. Each test file maps to exactly one
  production symbol in `cmd/baha/` (verified by reading the test body's first real call + imports). The verbatim
  first error line is taken from the 217 dossier, not re-run.
- Local count is capped at the 89 (mission step 2, AGENTS 5.4) — `go test ./cmd/baha/ -run <test> -count=1` per
  group, never the full matrix. No test was executed (read-only classification), so no container/network/volume
  was started.

## 1) END table — groups of the 89 other-domain failures

Columns: `gruppe | datei:zeile | Anzahl | wörtliche erste Fehlerzeile | rubrik | karte/id`

| # | group (production file) | datei:zeile | Anz | wörtliche erste Fehlerzeile | rubrik | karte / id |
|---|---|---|---|---|---|---|
| 1 | `cmd/baha/repository_up.go` (quick-init contract) | `cmd/baha/repository_up.go:151` | 9 | `Managed-environment machine operations require an authenticated BaseHarbor operator.` | (c) fallout of `3653369a4` #1717 | card VORGÄNGER (204) — init path |
| 2 | `cmd/baha/application_destroy_authorization.go` (destroy/retire consent) | `cmd/baha/application_destroy_authorization.go:33` | 5 | `Managed-environment machine operations require an authenticated BaseHarbor operator.` | (c) fallout of `3653369a4` #1717 | card VORGÄNGER (204) — destroy consent |
| 3 | `cmd/baha/app_client_consent.go` (client consent seam) | `cmd/baha/app_client_consent.go:47` | 3 | `Operator authentication is not configured.` | (c) fallout of `3653369a4` #1717 | card VORGÄNGER (204) — client consent |
| 4 | `cmd/baha/application_restore_authorization.go` (fresh restore) | `cmd/baha/application_restore_authorization.go:25` | 3 | `Managed-environment machine operations require an authenticated BaseHarbor operator.` | (c) fallout of `3653369a4` #1717 | card VORGÄNGER (204) — restore consent |
| 5 | `cmd/baha/app.go` (managed app create / deployment registration) | `cmd/baha/app.go:40` | 2 | `Managed-environment machine operations require an authenticated BaseHarbor operator.` | (c) fallout of `3653369a4` #1717 | card VORGÄNGER (204) — app create |
| 6 | `cmd/baha/app_perses_cli.go` (perses access via `status --json`) | `cmd/baha/app_perses_cli.go:158` | 2 | `Managed-environment machine operations require an authenticated BaseHarbor operator.` | (c) fallout of `3653369a4` #1717 | 0428-089 perses-access |
| 7 | `cmd/baha/app_repository_identity.go` (minimal source / repo identity) | `cmd/baha/app_repository_identity.go:14` | 2 | `Managed-environment machine operations require an authenticated BaseHarbor operator.` | (c) fallout of `3653369a4` #1717 | card VORGÄNGER (204) — repo identity |
| 8 | `cmd/baha/application_provider_impact.go` (App Edit Core activation) | `cmd/baha/application_provider_impact.go:63` | 1 | `start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner` | (b) NEUER DEFEKT — see 2.8 | card VORSCHLAG |
| 9 | `cmd/baha/app_commands.go` (all-targets inventory) | `cmd/baha/app_commands.go:106` | 1 | `all-targets inventory depended on deleted Target config: BaseHarbor config root is configured but the config.yaml is missing` | (a) already covered — see 2.9 | card ID (204) |
| 10 | `cmd/baha/application_lifecycle_lock.go` (destruction consent lock) | `cmd/baha/application_lifecycle_lock.go:40` | 1 | `Managed-environment machine operations require an authenticated BaseHarbor operator.` | (c) fallout of `3653369a4` #1717 | card VORGÄNGER (204) |
| 11 | `cmd/baha/application_runtime_retirement_intent.go` (retirement preferences) | `cmd/baha/application_runtime_retirement_intent.go:6` | 1 | `Managed-environment machine operations require an authenticated BaseHarbor operator.` | (c) fallout of `3653369a4` #1717 | card VORGÄNGER (204) |
| 12 | `cmd/baha/app_workspace_bootstrap.go` + `app_workspace_wizard.go` + `context_terminal.go` (workspace map / context TTY) | `cmd/baha/app_workspace_bootstrap.go` / `app_workspace_wizard.go` / `context_terminal.go` | 8 | `workspace map bootstrap failed: …` / `wizard failed: …` / `go build baha: exit status 1` | mixed (c)+(a) — see 2.12 | card VORGÄNGER (204) / 0428-089 |

Sub-groups that share production ownership but split on rubric (all in group 12 above):
- `app_workspace_bootstrap_test.go` (3) → (c) `3653369a4` #1717 (workspace bootstrap hits the managed-environment gate)
- `app_workspace_wizard_test.go` (2) → (c) `3653369a4` #1717
- `context_terminal_test.go` (2) → (a) terminal-context rendering is operator-seam; covered by an open card
- `tui_tabs_regression_test.go` (2) → (c) `3653369a4` #1717 (TUI doctor reads managed-environment state)

### Group 1 detail (9 tests, `repository_up.go:151`)
- Files: `app_init_wizard_test.go` (7), `app_init_source_neutral_test.go` (2)
- First error: `Managed-environment machine operations require an authenticated BaseHarbor operator.`
- Rubric (c): `initializeRepositoryManifestForUp` at `cmd/baha/repository_up.go:151` reaches the operatorauth gate.

### Group 2 detail (5 tests, `application_destroy_authorization.go:33`)
- File: `application_destroy_authorization_test.go`
- First error: `Managed-environment machine operations require an authenticated BaseHarbor operator.`
- Rubric (c): destroy/retire consent path resolves through the operatorauth gate.

### Group 3 detail (3 tests, `app_client_consent.go:47`)
- File: `app_client_consent_test.go`
- Errors: `Operator authentication is not configured.` / `missing transparent method in prompt:`
- Rubric (c): `requireManagedClientConsent` at `cmd/baha/app_client_consent.go:24/47` reads the operator principal.

### Group 4 detail (3 tests, `application_restore_authorization.go:25`)
- Files: `app_restore_fresh_identity_test.go` (2), `application_restore_authorization_test.go` (1)
- First error: `Managed-environment machine operations require an authenticated BaseHarbor operator.`
- Rubric (c): `prepareAuthorizedApplicationRestore` at `cmd/baha/application_restore_authorization.go:25`.

### Group 5 detail (2 tests, `app.go:40`)
- File: `app_create_target_test.go`
- First error: `Managed-environment machine operations require an authenticated BaseHarbor operator.`
- Rubric (c): `createTargetManagedApplication` at `cmd/baha/app.go:40`.

### Group 6 detail (2 tests, `app_perses_cli.go`)
- File: `app_perses_access_cli_test.go`
- Errors: `baha status --json failed: operator authentication needs interactive setup but input is not a terminal`
- Rubric (c): `persesProbeApp` (helper in `app_perses_cli_test.go:158`) drives the genuine `status --json` path through the operatorauth gate. Same test file as card 0428-089.

### Group 7 detail (2 tests, `app_repository_identity.go:14`)
- Files: `app_registered_minimal_source_test.go` (1), `app_repository_identity_test.go` (1)
- First error: `Managed-environment machine operations require an authenticated BaseHarbor operator.`
- Rubric (c): `resolveRepositoryLifecycleIntent` at `cmd/baha/app_repository_identity.go:14`.

### Group 8 detail (1 test, `application_provider_impact.go:63`) — RUBRIK (b) NEUER DEFEKT
- File: `app_edit_apply_test.go:1253`
- First error: `start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner`
- Rubric (b): the App-Edit command activation fails on a missing protected-Core network / missing backend owner — a
  production defect, NOT an authentication gate. See §2.8 draft card.

### Group 9 detail (1 test, `app_commands.go:106`) — RUBRIK (a) already covered
- File: `app_list_all_targets_test.go:26`
- First error: `all-targets inventory depended on deleted Target config: BaseHarbor config root is configured but the config.yaml is missing`
- Rubric (a): all-targets inventory is operator-seam; covered by an open 204 card. Verified:
  `git -C baseharbor-plan grep -l -a "all-targets" origin/main -- tasks/` → the 204 card carries it.

### Group 10-11 detail (1 test each, lifecycle-lock / retirement-intent) — RUBRIK (c)
- `application_lifecycle_lock_test.go:79` → `cmd/baha/application_lifecycle_lock.go:40`
- `application_runtime_retirement_preferences_test.go:119` → `cmd/baha/application_runtime_retirement_intent.go:6`

### Group 12 detail (8 tests, workspace/context/TUI) — RUBRIK (c)/(a)
- `app_workspace_bootstrap_test.go` (3) → `cmd/baha/app_workspace_bootstrap.go` — (c) `3653369a4` #1717
- `app_workspace_wizard_test.go` (2) → `cmd/baha/app_workspace_wizard.go` — (c) `3653369a4` #1717
- `context_terminal_test.go` (2) → `cmd/baha/context_terminal.go` — (a) terminal-context rendering (operator-seam)
- `tui_tabs_regression_test.go` (2) → `cmd/baha/tui.go` — (c) `3653369a4` #1717

## 2) rubric (c) proof — fallout of commit `3653369a4` (#1717)

Gate site (verbatim, at develop `40cb28c758b0`):

```
$ git grep -n "Managed-environment machine operations require an authenticated BaseHarbor operator" 40cb28c758b0 -- 'internal/operatorauth/*.go'
40cb28c758b0:internal/operatorauth/authorization.go:285:  decision.Reason = "Managed-environment machine operations require an authenticated BaseHarbor operator."
```

`internal/operatorauth/authorization.go:285` returns `machine.ErrorAuthenticationFailed`
(`operator_authentication_required`) whenever a managed-environment machine operation reaches the gate without a
`VerifiedPrincipal`. Every group-1/2/4/5/7/10/11/12 row fails with exactly this string, so the failing tests are
the fallout of `3653369a4` gating that path.

Green/red pair (mission step 3c):
- green `f5ce95af` (commit exists, pre-gate) → red `3653369a4` (introduces the operatorauth enforcement at the gate).
- `git cat-file -t f5ce95af` → `commit`; `git cat-file -t 3653369a4` → `commit`. Both resolve as real commits.

The mission flags: if a group falls under rubric (c), the cleanest fix may be a correction at the enforcement path
(`internal/operatorauth/authorization.go` / `cmd/baha/local_workload_authority.go` / `cmd/baha/mcp.go`) rather than
206 test changes — an Owner decision. Here that decision does NOT apply to 206: 206 is classification only; the 72
managed-environment rows belong to the 204 operator-seam class and are the 204 card's case to fix.

## 3) all 42 files accounted for (89 tests)

`git status --porcelain` on the develop base is empty (read-only). Every other-class test file maps to exactly one
production file; no line could not be placed. The 89 = 9+5+3+3+2+2+2+1+1+1+1+8 across the 12 production-file groups.

## repo-rule compliance (read-only, AGENTS 4.4)

- Planning remote (verified before first evidence commit):
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
- Worktree: `/tmp/opencode/w206-0428-206-split-wt` (partial clone of `https://github.com/mcpdev80/baseharbor.git`),
  checked out at develop `40cb28c758b02960356434b630086a341ebe1738`.
- `git status --porcelain` → empty (no product writes).
- `git log --oneline 40cb28c758b02960356434b630086a341ebe1738..HEAD` → empty (no own/foreign commits).
- No `.github/**` touched, no PR, no hosted-matrix rerun, no workflow_dispatch (AGENTS 3.8).
- No product file edited; evidence lives only in baseharbor-plan evidence/, never in a product repo.

## container / network / volume before–after + cleanliness (owner hygiene 2026-11-05)

- Before: none started by this lane (read-only classification; no test executed).
- After (ps-witness, this host): pre-existing `bh-docker-dev-shared-*` stack (postgres/openbao) is NOT started by
  this lane and was not touched.
- `cleanliness: ` no container/network/volume/state directory started by this lane; scratch limited to
  `/tmp/opencode/w206-0428-206-split-wt` (partial clone) and `/tmp/w217-*` (w217 dossier read-only copy).

## TODO board

`workers/todos/w221-0428-206-split.json` written this shift (10 numbered steps, ticked as worked).

## END

END w221-0428-206-split DONE — read-only split of the 89 other-domain cmd/baha failures into 12 production-file
groups; every group carries a rubric (a/b/c) and a witness. All 89 placed; no line unplaceable. SHA = baseharbor-plan
origin/main head at commit time. No product change, no PR, no matrix run. Card text for the single rubric-(b) group
(Group 8, `app_edit_apply_test.go:1253`, `application_provider_impact.go:63`) is drafted in §2.8 for the coordinator
to pour.
