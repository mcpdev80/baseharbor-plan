# CLI2 command contract — round 1 (0428-049 / t-20261114-r28-cli2-contract)

**Type:** Reviewed command contract (specification for the implementation packages). No product runtime change in this file.
**Author:** `lane-cli2-contract-r28` · Date: 2026-11-14
**Release:** v0.4.28 · Card: `0428-049`
**Base product (`origin/develop`):** `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (verified: fresh clone `git show 0e9ccb582:<path>` reproduces every witness)
**Base plan (`origin/main`):** `3aa218da73504b3ff428b687d253095bee7fa9dd`
**Inputs:** owner working brief `evidence/cli-redesign-20261114/brief.md`, proposed mapping `command-map.md`, static code-entry index `code-entry-index.md`, and the four completed audits `audit-access.md`, `audit-app.md`, `audit-interface.md`, `audit-wizards.md`.

> Scope note. This task specifies the command contract for the following implementation packages. It does **not** implement the runtime. The contract is a normative baseline: the implementation cards (application lifecycle / interaction / export / status, context-shell, source-model, uid-*, wizard-platform, compat-shim) consume it verbatim. Where a proposed name is not yet on `develop`, this file states the proposed destination; where it is, this file pins the current grammar at `0e9ccb582` so the destination can be reconciled against reality.

---

## 1. Conventions and authority

- **English CLI UX.** All human-facing command names, summaries, flag long-forms, and failure messages are English. The untranslated machine attention token `Achtung` (currently interpolated into ≥12 prompt strings at e.g. `cmd/baha/provider_change_confirmation.go:42,82,84,104`) is replaced by `Warning:` throughout every implementation package that touches it. This is a machine-facing value change; it is contract- and schema-visible (see §8).
- **One semantic core, many surfaces.** CLI, JSON (`-o json`), MCP (`baha mcp serve`) and HTTP share the same lifecycle semantics (`DEVELOPMENT_GUIDELINES.md §9`; Core `AGENTS.md` "Work and verify"). No surface may bypass policy, ownership, reconciliation, preflight or verification. Human-only sensitive reveal is deliberately excluded from ordinary machine output.
- **Fail-closed by construction.** Every mutation follows `plan → preflight → apply → verify`. Consent (`--yes`) is layered on top and never substitutes consequence/deletion consent.
- **Verdicts.** `trifft` (matches), `wicht ab` (deviates from the proposed destination), `Konsistenz-Risiko` (internal inconsistency or open risk), `offen` (unresolved owner decision).

## 2. Top-level taxonomy

Owner brief proposes: `app`, `env`, `target`, `context`, `platform`, `access`, `system`. This task fixes the grammar; it does not remove the currently registered groups. The current `develop` tree (root `baha`, `cmd/baha/commands.go:33-166`) registers `init, list, inspect, backup, restore, up, down, destroy, plan, logs, status, doctor, provider, stack, workspace, target, use, node, onboard, workstation, user, dev, config, shell-init, prompt, policy, access, agent, mcp, serve, app, connect, disconnect, connections, openbao, trust, login, logout, whoami, update, version, tui, completion` plus a root `new` chooser. The contract groups them as follows:

| Group | Owner | Current leaves | Proposed destination |
| --- | --- | --- | --- |
| `app` | application lifecycle/interaction/export/status | `new, workspace, init, create, list, show, edit, footprint, inspect, apply, plan, preflight, prune, backup, restore, env, sql, cache, creds, secure-profile, logs, shell, exec, update, tls, status, doctor, down, stop, up, destroy, secret, runtime-identity, evidence, version, versions` | consolidated under `app data …` for the data surface (§7) |
| `env` | uid-environment (proposed) | *not a current leaf* — environments addressed by `-e/--environment` only | new group; stable identity model §6 |
| `target` | deployment targets | `list, show, policy, create, delete, activate, deactivate` | `delete` = detach/recovery (§5); new `remove` keeps data (§5) |
| `context` | context-shell | `use` (+ root `target activate/deactivate`) | `use`, `clear`; per-terminal active context |
| `platform` | platform/stack/provider/secrets | `provider, author, stack, node, organization, secrets, local, remote` | `platform provider|author|stack|node|organization|secrets|local` (§4) |
| `access` | identity/access | `assign, offboard` (+ root `login, logout, whoami, workstation, user, onboard, grant`) | `access user|workstation|grant|login|logout|whoami|onboard` (§9) |
| `system` | core/system | `version, tui, completion, shell, prompt, domain, credentials, hosts, cleanup, agent, mcp, trust, destroy, update` | `system version|tui|completion|shell|trust|destroy|update|agent|mcp` (§10) |

## 3. Stable, shared flags

Brief line 8: `-t` target, `-e` environment, `-c` one or comma-separated components "throughout applicable commands. Names and meaning must be consistent."

| Flag | Meaning | Scope | Current state at `0e9ccb582` | Contract |
| --- | --- | --- | --- | --- |
| `--target NAME` / `-t NAME` | override Target resolution | global, stripped before dispatch (`cmd/baha/main.go:187`) | only long form exists; **no `-t`** exists | introduce `-t` shorthand for `--target` on every command that accepts a Target; keep `--target` canonical |
| `-e ENV` / `--environment ENV` | resolve deployment state | applicable lifecycle/data commands | accepted together where present; absent on read group (`baha app status`, `baha app plan` reach env only positionally) | `-e/--environment` consistent across all `app` lifecycle/data leaves |
| `-c COMPONENT` / `--component` | one or comma-separated components | applicable commands | three different names (`--component`, `--workload-component`); no `-c`, no comma-lists | unify to `-c`/`--component` = one or comma-separated component identities |
| `--yes` / `-y` | deterministic approval | mutation leaves | 58 long-form sites; 16 files also carry `-y`; completion advertises `-y` even where the parser rejects it | accept `--yes`/`-y` where implemented; completion must not advertise a shorthand the parser rejects |
| `--json` / `-o json` | structured output | read/mutation leaves | five accepted spellings (`--json, -o json, --output json, -ojson, --output=json`); some leaves accept it without advertising it | uniform format vocabulary: `human`, `json`; unknown value → typed usage error |
| `--no-input` / `--non-interactive` | never prompt | global | sets `NonInteractive`; enforced at ~81 hand-written sites | contract satisfied by discipline today; implementation introduces a central gate (§5.3) |
| `-q/--quiet/--silent` | concise output | global | honoured | retained |
| `-v/--verbose` | diagnostic output | global | honoured | retained |
| `--agents` | documentation-only init mode | `init` | correctly fenced | retained |

## 4. `platform` group

| Command | Destination | Owner | Consequence / rule |
| --- | --- | --- | --- |
| `platform stack` | `list, show, create` | platform | Stack Profiles; `create` takes `--component ID:ROLE:STACK` |
| `platform provider` | `add, list, inspect, show, verify, remove` | platform | external registration; **not** provider authoring (brief line 15) |
| `platform author` | `init, test` | platform | create minimal skeleton / run conformance; authoring ≠ authorizing a runtime provider |
| `platform node` | `add, connect, list, status, disconnect` | platform | remote Docker/Podman enrollment, one-use bundle |
| `platform organization` | `set, show, check, update` | platform | org-level managed source (OCI/Git/local/system), immutable digest, never inline secrets |
| `platform secrets` | `status, bootstrap, unseal, rotate` | platform | OpenBao control-plane |
| `platform local` | `up, down, serve, doctor, status` | platform | local control-plane surface (brief proposes `platform local up/down/serve/status/doctor`) |
| `platform remote` | `connect` | platform | remote Core connect |
| `platform destroy` | — | system | **whole installation**, not app destroy (brief line 15). Root `destroy` is the canonical location; `platform destroy` is the group-shorthand destination. |

## 5. `target` group

| Command | Destination | Owner | Consequence / rule |
| --- | --- | --- | --- |
| `target list` / `target show` / `target policy` | current names | target | `delete` = detach/recovery; `--json` supported |
| `target new` | `target create` | target | guided local target (runtime → scope → default); `--from-recovery` preserved |
| **`target remove`** | **new** | target | **retains runtime and data**; the intended meaning of "detach without destroying runtime/data" is `remove`, not `delete` (brief line 15) |
| `target delete` | `target remove` | target | `delete` detaches configuration, preserves data (current `delete` semantics); kept as the recovery alias |
| `target activate` / `target deactivate` | `context use` / `context clear` | context | persist/clear the active deployment target; fail-closed on concurrent change |

Decision rule: environment `test`/`prod` application operations must fail closed without a valid Target/Environment OIDC operator boundary (Core `security-invariants.md`); `dev` remains trusted-local where configured. This name-semantic special-casing is **open** — the brief wants name-independent semantics (brief line 12). Contract: keep the fail-closed guarantee; resolve the name-semantic question with the owner before implementation (see §11).

## 6. `env` group and identity model (owner-decided)

Owner brief line 12: environment names are unrestricted by fixed `dev/test/prod` semantic special cases; same capabilities irrespective of name, behaviour follows explicit policy/authorization. Brief line 13: environments, apps and targets each have stable IDs; deployment IDs remain separate.

- **Stable identities.** `environment` (one per Target), `app` (system identity per ADR 0017: the `(application_id, environment)` pair), `target` (Core-side UUID; workstation alias is separate), each carry a stable ID. Deployment IDs remain distinct from all three.
- **Shared environments, many apps.** An environment is shared by multiple apps and multiple nodes/future clusters; an app may live in multiple environments. Distinguish environment/target/app identity; no implicit shared data/credentials.
- **Name independence.** Environment create/edit/delete is guided; protected edit/delete require authentication + authorization as configured. Delete previews environment-scoped deployments and consequences; choose `Keep data` (default) or `Delete data`, explicit final consent, no forced prior per-app detach. Unknown ownership/impact fails closed.
- **`app.id` in the committed contract (brief line 14, OPEN).** Owner wants a **non-secret `app.id` committed in versioned `baseharbor.yaml`**, generated at new/init, reused by another checkout/Core, no manual UUID request, historical ID preserved, conflicts rejected. Current `develop` deliberately **omits** the authored `ApplicationID` (`app.go:256`) and the `(application_id, environment)` pair is the system identity per ADR 0017. **Decision required** (see §11): adopt a portable committed `app.id` with migration + reject-conflict, coordinated with Core and Git authority; or keep the current ADR 0017 identity.

## 7. `app data` group

Owner brief line 11. Consolidate the data surface under a new `app data …` group. `sql`/`cache` are retained as access consoles; backup/restore are distinct from the selectable encrypted export.

| Command | Destination | Owner | Consequence / rule |
| --- | --- | --- | --- |
| `app data env` | `app env` | app-data | app variables; reveal defaults masked; `--reveal` shows selected or all authorized values (brief wants per-value selection; current is a single global `--reveal`) |
| `app data secrets` | `app secret` | app-data | app-managed secrets with optional arbitrary type; list supports single named selection + reveal; OpenBao protection + audit on all access paths; no plaintext in manifests/audit/normal output |
| `app data services` | `app creds` (+ `app sql`, `app cache`) | app-data | **complete** bound-service connection data incl. credentials; current `creds` covers `postgres|valkey` connection metadata only (brief wants a richer surface) |
| `app data tls` | `app tls` | app-data | guided certificate management; `update` subcommand |
| `app data backup` | `app backup` | app-data | one encrypted recovery unit; `--password-file` only (never plaintext password) |
| `app data restore` | `app restore` | app-data | validates/decrypts before mutation; durable-state restore with workload stopped |
| `app data export` | `app secure-profile` | app-data | selectable encrypted export; clearly distinct from `app data backup`/`restore` and from `app evidence` (evidence collection) |
| `app data secrets identity` | `app runtime-identity` | app-data | set/list/rotate/revoke; "without changing any stored baseharbor:// secret references"; never grants operator API access |

Reveal contract (brief line 11): reveal defaults masked; explicit `--reveal` shows selected or all authorized values. **Known current deviation (audit-access F1):** `baha app creds --reveal` prints the real password + full connection URI with only one consent gate and **no audit write**; the JSON path is correctly blocked. The implementation package must add per-reveal audit + (recommended) a second consent gate; the contract fixes masked-by-default + explicit `--reveal` as the rule.

## 8. Output and error formats

- **Format vocabulary:** exactly two formats, `human` and `json`; any other value → typed usage error `unsupported output format` (`cmd/baha/output.go:31`).
- **Accepted spellings:** `--json`, `-o json`, `--output json`, `-ojson`, `--output=json` — all five reach 72 call sites. `-o` doubles as output **destination** in `baha trust export` (documented as a known exception).
- **Machine error envelope** (`internal/machine/contract.go`): `ResultError{contract_version="v1", error{code,message,cause,retryable,next,resource,remediation_class,details}}` with 21 stable codes; printed on stderr only when JSON was requested.
- **Human error rendering** (`cmd/baha/main.go:217`): Error / Affected / Resolution / What to do blocks; keeps `Next:` for usage/actionable errors.
- **Streaming exceptions:** `logs`, `exec`, `shell`, `sql`, `cache` are excluded from the machine surface by design (raw streams can carry secrets).
- **Exit codes (currently undocumented, fix in the implementation's doc contract):** success `0`; usage error `2`; runtime failure `1`; SIGINT/first cancellation `130`; SIGTERM/second signal `143`. These are correct and stable in code (`internal/cli/cli.go:82-91`, `cmd/baha/main.go`) but ship on no reference page — the implementation package must document them.
- **Version marker.** The machine surface carries `ContractVersion = "v1"`; the human surface carries none. A compat shim (separate card) bridges an unversioned human syntax against the versioned contract.

## 9. `access` group (identity / access)

| Command | Destination | Owner | Consequence / rule |
| --- | --- | --- | --- |
| `access user` | `user` | access | `user list`, `user offboard LOGIN [--yes]` (disable Keycloak, revoke all stations, verify-at-each-step) |
| `access workstation` | `workstation` | access | `new`, `list`, `revoke NAME` (asks once, then verifies revocation) |
| `access grant` | `access` | access | `assign PERSON [--json]` / `offboard PERSON [--json]` (folds into single production policy authority; atomic all-or-nothing) |
| `access login` / `logout` / `whoami` | root | access | unmanaged env → `trusted-local` (no OIDC); managed env requires a verified OIDC session |
| `access onboard` | `onboard` | access | `--invite`, `--import`, `--init-tenant`; `--init-tenant` reuses the owner-bound OIDC+PKCE login transaction, never creates an independent admin |

**Audit finding (carried):** the identity/access mutation surface writes **no audit event**; the audit registry (`recordApplicationAudit` + `internal/evidence`) is application-lifecycle-only. The implementation package must add audit events for `access`, `onboard`, `login/logout/whoami`, `user/offboard`, `workstation`, and org-config changes. Reveal paths (`app creds --reveal`, `app env --reveal`) also need per-reveal audit.

## 10. `system` group

| Command | Destination | Owner | Consequence / rule |
| --- | --- | --- | --- |
| `system version` | `version` | system | build version, commit, built date; `-o json` |
| `system tui` | `tui` | system | interactive status dashboard; refuses `--plain`/`--no-input`/non-TTY with an actionable redirect |
| `system shell` | `shell-init`, `completion`, `prompt` | system | bash/zsh/fish completion and shell integration; read-only, deterministic |
| `system trust` | `trust` | system | `status, export, install, uninstall`; installs only the public managed-local CA |
| `system destroy` | `destroy` | system | **whole installation**; two acknowledgements + separate data-deletion consent; `--all` compatibility alias; preserves app sources and external infra |
| `system update` | `update` | system | inspect/update BaseHarbor/Core; immutable image identities + verified recovery points |
| `system agent` / `system mcp` | `agent`, `mcp` | system | `agent describe` publishes the machine-coverage table; `mcp serve` runs the stdio server |

## 11. Unresolved owner decisions (contract must resolve before implementation)

These are open by design. The contract states the question and the safe default; it does **not** invent behaviour.

1. **`app.id` in the committed contract (brief line 14).** Adopt a portable non-secret `app.id` committed in versioned `baseharbor.yaml` (generated at new/init, reused, historical ID preserved, conflicts rejected) coordinated with Core + Git authority; or keep the ADR 0017 `(application_id, environment)` system identity. **Safe default:** if adopted, migrate existing stores and reject conflicts; do not silently weaken the ADR 0017 identity.
2. **`-t` and `-c` shorthand.** Introduce `-t` for `--target` and `-c` for `--component` as the brief requires, or relax the brief wording. **Safe default:** introduce them; keep `--target`/`--component` canonical long-forms.
3. **Environment name semantics (brief line 12).** Keep the fail-closed `test`/`prod` boundary but drop the name-semantic special cases (completion hard-coded `{dev,test,prod}`, destroy-authorization rank map `dev|development…prod`, default `"dev"` in 20+ places, deployment-preset vocabulary `development/test/staging/production`). **Safe default:** behaviour follows explicit policy/authorization, not the name; the fail-closed guarantee is retained.
4. **`app exec` grammar (brief line 10).** `-c backend` shell / `--cmd command`. Current `app exec SERVICE COMMAND [ARG...]` is positional. **Safe default:** adopt `-c/--component` for the workload selector and `--cmd` for the command, preserving positional compatibility during a documented compatibility period.
5. **`app pull` / `--up` naming (brief line 2).** Current source uses `app update` (`cmd/baha/app_update.go:44`); `--up` does not exist; `app workspace update` (multi-repo fast-forward) and `app update` (single-app Git + backup policy) are two distinct surfaces the map collapses to one `app pull`. **Safe default:** `app pull` = source update with whole-repo preview of shared impacts; keep `app update`'s backup policy; distinguish workspace-source vs app-source update.
6. **`Achtung` marker replacement (audit-interface 5.6).** Machine-facing English replacement for the untranslated German token. **Safe default:** replace with `Warning:`; this is contract- and schema-visible.
7. **`app show` vs `app status` (audit-app item 3).** `show` prints the authored manifest YAML; `status` prints runtime readiness. **Safe default:** keep both as distinct leaves; the map conflates them.
8. **`--no-input` central gate (audit-interface 3.1).** Contract satisfied today by discipline (~81 sites). **Safe default:** introduce a central gate so a forgotten prompt fails closed rather than blocks.
9. **HTTP stream bindings vs MCP exclusion (audit-interface 7).** HTTP catalogue exposes `logs`/`exec`/`terminal_*` streams that MCP excludes. **Safe default:** resolve the parity gap; do not ship a machine client that sees an endpoint with no MCP tool.
10. **Arrow-key navigation in wizards (audit-wizards 5.4).** Enter/Tab present; arrows absent. **Safe default:** decide whether arrows are in scope; Enter/Tab already satisfy the brief.

## 12. Migration and testing matrix (for the implementation cards)

Every old leaf/flag maps to a destination; no fixed dev semantics remain; the five seams (app lifecycle, uid-*, context-shell, platform, access) and migration/testing are explicit below.

| Old leaf / flag | Destination | Migration note |
| --- | --- | --- |
| `baha new` | `new` chooser → `app setup new` / `target new` / `platform stack new` / `platform author init` / `app setup init` | wizard prompt retained as card entry point |
| `baha app apply` / `baha up` | `app up` (`--up` alias resolves to the same app-up operation) | `baha up` root keeps management-Core bootstrap flags; `app up` does not |
| `baha app workspace …` | `app source …` (new group) | `workspace` kept as alias during compatibility |
| `baha app init` / `baha init` | `app setup init` (`init`/`setup new` greenfield vs `setup init` brownfield) | `--agents` mode fenced |
| `baha app creds` | `app data services` | richer surface; audit + per-reveal gate |
| `baha app secret …` | `app data secrets …` | add single-name reveal |
| `baha app env` | `app data env` | per-value reveal selection |
| `baha app tls` | `app data tls` | — |
| `baha app backup/restore` | `app data backup` / `app data restore` | distinct from `app data export` |
| `baha app secure-profile` | `app data export` | clearly distinct from evidence |
| `baha app runtime-identity …` | `app data secrets identity …` | — |
| `baha target create/delete` | `target new` / `target delete` (+ new `target remove`) | `remove` retains data |
| `baha target activate/deactivate` | `context use` / `context clear` | — |
| `baha login/logout/whoami` | `access login/logout/whoami` | — |
| `baha access` | `access grant` | — |
| `baha onboard` | `access onboard` | — |
| `baha workstation/user` | `access workstation` / `access user` | — |
| `baha provider/stack/node/openbao/config organization/policy/dev/agent/mcp` | `platform …` / `system …` | per §4/§10 |
| `baha destroy` | `system destroy` (whole installation) | — |
| `baha app destroy` | `app setup destroy` | app removal |

## 13. Repo boundaries and handoff

- **Reserved for other owners.** `cmd/baha/commands.go` (root tree), the shared parser/machine registry, `.github/**` (CI), release notes and generated indexes. This contract states the grammar; the implementation cards wire it, coordinate shared writes through the coordinator, and do not edit another worker's reserved files concurrently.
- **No Console/Node Connector public-repo implementation** in this release.
- **One task/branch/PR per worker.** This lane owns only this contract + this akte; no product change.
- **Review/acceptance.** Owner accepts the exact contract or records a blocker (§11); every old leaf/flag and sensitive/remote behaviour has an agreed destination, no fixed dev semantics; five independent implementation seams and migration/testing matrix explicit.
- **Evidence.** This file and the akte `contract/round-1.md` live only in the planning repo. No `.evidence/` directory anywhere; no main-branch writes in the product repo.
