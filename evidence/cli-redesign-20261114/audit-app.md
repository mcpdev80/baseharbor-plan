# Audit: app command semantics (0428-044 · v0.4.28)

**Type:** Read-only audit (MERGE-FROST: no product changes). Evidence only in the planning repo.
**Author:** lane-0428-044-r28 (Worker) · Date: 2026-11-14
**Base SHA (develop):** `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`  (this equals `origin/develop` HEAD at fetch time)
**Planning base (origin/main) before commit:** `4c1444f81d59c76cfd7122b7dc83c827599d6b8b`
**Worktree used:** `/tmp/baha-audit-wt` (detached HEAD at `0e9ccb582`; an isolated read-only checkout, not a candidate branch)

This audit traces every app/init/plan/up/down/pull/status/logs/destroy/prune/urls/source branch and the data (env/secrets/services/tls/backup/restore) surface on `develop 0e9ccb582`, then compares each to the owner working brief (`evidence/cli-redesign-20261114/brief.md`), the proposed command map (`command-map.md`), and the static code-entry index (`code-entry-index.md`). Per-path result is `trifft` / `wicht ab` / `Konsistenzrisiko` with `file:line` witnesses. All witnesses were read from the checked-out source, not from the index's links.

## Method

- Checked out `develop 0e9ccb582` in an isolated read-only worktree `/tmp/baha-audit-wt`; `git rev-parse HEAD` == `0e9ccb582`.
- The code-entry-index header pins `cd77e20e`; that is the index's authoring snapshot, NOT the audit base. Every entry below was re-read on `0e9ccb582` and cross-checked against the index (line numbers shifted because `0e9ccb582` is newer than `cd77e20e`).
- Scope limited to `cmd/baha/` (CLI) + `internal/application/` intent, per task entry points. Runtime/pro realization (`internal/runtime/`, providers) is out of scope.
- No edits to any product file; no evidence written into the product repo.

## Registry: where app children live

- `appCommand` registers only 6 stable children: `new, workspace, init, create, list, manifest-show (show), plan, preflight` — `cmd/baha/app.go:21-37`.
- The full lifecycle/data surface is appended later by `configuredApplicationCommand` at `cmd/baha/commands.go:209-255`: `edit, footprint, inspect, apply, guided-backup, guided-restore, env, sql, cache, creds, secure-profile, logs, shell, exec, update, tls, status(+tls), doctor(+tls), down, stop, up, destroy, secret, runtime-identity, evidence, version, versions, prune`.
- Root shortcuts (`baha up/down/plan/logs/doctor/destroy/inspect/backup/restore/update`) route to the same cores via `cmd/baha/commands.go:40-166`. `up` → `runtimeUpCommandWithInputResolver` (`commands.go:80`, impl `app_input_resolver.go:520`); `down` → `appDownCommand` in a repo, else `controlPlaneDownCLI` (`commands.go:86-91`); `destroy` (whole installation) → `runtimeDestroyCommand` (`commands.go:99`); `plan` → `appPlan` (`commands.go:108-112`); `logs` → `appLogsCommand` (`commands.go:120`).

---

## 1. `baha app new` / `baha new` (greenfield)

- Entry: `appNewCommand` `cmd/baha/app_new.go:32`. Usage `baha app new [NAME] [--directory PARENT] [--stack ...|--stack-profile ...] [-e ENV] [--http] [--sql] [--cache] ... [--secrets] [--require-secret ...] [-o json]`.
- `baha new` is NOT a top-level command; it is only a wizard prompt (card entry point). The command map's `baha new → guided task selection` is therefore a *proposed* destination, not current behaviour. **wicht ab.**
- Guided path requires a terminal and refuses piped/no-input consent (`app_new.go:40-44`). Deterministic path: NAME + `--directory` + explicit flags, non-interactive.
- `--stack go|nextjs|python|quarkus` maps to an adapter ID (`developmentAdapterID`, `app_new.go:83`); `--stack-profile NAME` uses a reusable profile (`app_new.go:69-77`). `--stack` and `--stack-profile` are mutually exclusive (`app_new.go:52-71`). **trifft** brief.
- Next steps printed: `cd`, `baha app init --quick`, `baha up` (`app_new.go:139-142`). Aligns with brief's `new` = greenfield → init.
- Consistency risk: `--stack` accepts `go|nextjs|python|quarkus` in the Usage string (`app_new.go:36`) but `appNewOptions` parsing (`app_new.go:145+`) is the authority. The usage banner lists a stack set that must be validated against the adapter registry.

## 2. `baha app init` / `baha init` (brownfield)

- Entry: `appInitCommand` `cmd/baha/app.go:158`; the *registered* init is the input-resolver variant `appInitWithInputResolverCommand` (`commands.go:214`, usage rebuilt at `commands.go:215`). `baha init` root → same (`commands.go:40-42`).
- Deterministic contract: requires an explicit capability or workload selection (`hasExplicitInitContract`, `app.go:178-183`); `--quick` allows repository-only detection. Rejects multiple workload sources without an explicit one (`app.go:218-233`).
- Flags (from usage `commands.go:215`): `--agents`, `--quick`, `--json`, `--input NAME=VALUE`, `--hostname HOST`, `--tls acme|existing|local`, `--cert-dir DIR`, `--yes`, `[-e ENV]`, `--sql/--sql-instance`, `--cache/--cache-instance`, `--key-value/--key-value-instance`, `--document-db/--document-db-instance`, `--messaging-queue|pubsub|stream [--*-instance]`, `--s3/--s3-bucket`, `--secrets/--require-secret`, `--workload-component`, `--workload-source KIND:PATH`.
- Authored YAML omits `ApplicationID` (`m.ApplicationID = ""`, `app.go:256`) — **trifft** brief's statement "Current generated authored YAML omits ID". Brief wants `app.id` committed in versioned `baseharbor.yaml` at new/init — **nicht implementiert; Konsistenzrisiko** (brief item 14, coordination-required).
- Consistency risk: `--tls` accepted here but the index lists `--tls` only under `app init` generic clues; the resolver usage is authoritative.

## 3. `baha app create` (Core-managed source)

- Entry: `appCreateCommand` `cmd/baha/app_commands.go:23`. Usage `baha app create NAME [--environment ENV] [--sql|--sql-instance ...]...`.
- Local: `createTargetManagedApplication` (`app.go:40`) writes a `managed` deployment record with only Git/OCI source identity, no workstation paths (`app.go:106-114`), omits `ApplicationID` for remote (`app_commands.go:47`). Requires `app.create` authorization (`app.go:62`).
- Aligns with brief's `create` = managed/adopt, `app.create` domain op preserved. **trifft.**

## 4. `baha app list` / `baha list`

- Entry: `appListCommand` `cmd/baha/app_commands.go:106`; root `list` dispatches to `app list` (`commands.go:44-56`).
- Flags: `--all-targets`, `--json`, `--output`. Default fails closed when multiple Targets exist and no selection (`commands.go:47` long).
- Consistency: brief wants `-c` components throughout applicable commands; `list` has no `-c` (it lists deployments, not components). **keine Diskrepanz** (list is deployment-scoped).

## 5. `baha app plan` / `baha plan` / `baha app preflight`

- `appPlanCommand` `cmd/baha/app_commands.go:238`; root `plan` → `appPlan` (`commands.go:103-113`). `appPreflightCommand` `cmd/baha/app_commands.go:340`.
- plan flags: `--environment`, `--json`, `--output`, `--uuid` (remote rejects `--uuid`, `commands.go:256-260`). preflight flags: `--json`, `--output`, `--uuid`.
- plan renders operator access + provider impact + "No changes were made" — read-only. **trifft** brief's plan = read-only desired-state.
- Consistency risk: `--uuid` is a remote-only selector on plan/preflight/status; a workstation could pass it locally and be ignored/failed. Worth a note: not a fail-closed guard locally.

## 6. `baha app apply` / `baha up` (`--up`)

- apply: `appApplyCommand` `cmd/baha/app_apply.go:38`; lifecycle `runApplicationApplyLifecycle` `app_apply.go:104`. Lifecycle order: admission policy → target lifecycle lock → `requireResolvedApplicationCore` → provider-authorization/retirement → **candidate confirmation** (`promptConfirmCandidateSubmission`, `app_apply.go:184`) → record-before-mutation → broker materialize → preflight → converge → verify → audit. Flags: `--skip-memory-preflight`, `--confirm-candidate <digest>`, `--workload-port NAME=PORT`, `--yes` (implicit via assume-yes).
- **`--up` NOT implemented.** Brief (item 2) asserts "`--up` invokes the same app-up operation". Grep for `--up` across `cmd/baha/*.go` returns nothing. `baha up` is a *root command*, not a flag. `app up` flags: `--yes/-y`, `--skip-memory-preflight` (`app_up.go:18-36`). Root `up` → `runtimeUpCommandWithInputResolver` (`app_input_resolver.go:520`); options `--yes/-y, --ha, --control-plane-only, --trust-host-ca, --skip-memory-preflight, -e/--environment, --postgres-port, --openbao-port, --recovery-file, --confirm-candidate` (`runtime.go:78-137`). **wicht ab (brief) / Konsistenzrisiko (flag exists in map intent, not in code).**
- `up` reuses the SAME apply lifecycle core (`executeApplicationUpLifecycle` → `app_up_lifecycle.go:35`), which calls `runApplicationApplyLifecycle`. So `baha up` == `app apply` semantics (brief's intent is met by reuse), but the literal `--up` flag does not exist.
- Consistency risk: root `up` supports `--ha/--control-plane-only/--postgres-port/--openbao-port/--recovery-file/--trust-host-ca` (management Core bootstrap); `app up` does NOT. A user running `baha up --ha` in a repo bootstraps Core; `baha app up --ha` fails unknown-option. This asymmetry is real and worth flagging for the taxonomy review.
- Candidate submission bound only on explicit `--confirm-candidate` with the exact printed hash; else fails closed (`app_apply.go:43-60`). **trifft** brief consent model.

## 7. `baha app down` / `baha app stop` / `baha destroy`

- `appDownCommand` `cmd/baha/app_lifecycle.go:21` — built by reusing `appStopCommand`'s command struct with `Name = "down"` (`app_lifecycle.go:21-26`). `appStopCommand` `app_lifecycle.go:35` reuses `appDestroyCommand`'s struct with `Name = "stop"`, sets `applicationStopModeKey` context flag (`app_lifecycle.go:42-46`). So the chain is `down → stop → destroy` (one struct, three names).
- `appDestroyCommand` `app_lifecycle.go:197`; usage `baha app destroy [NAME] [--uuid DEPLOYMENT-ID] [--yes]`. `executeApplicationDestroyLifecycle` `app_lifecycle.go:271`. Non-full-reset (`stop`) = retire runtime, preserve data, retain owner; full-reset = remove state, audit.
- Root `destroy` (`commands.go:94-101`) → `runtimeDestroyCommand` = WHOLE INSTALLATION (apps + providers + Core services + config/state), `--all` kept as compatibility alias (`runtime_destroy_all.go:51,87`). `--delete-data` flag also on root destroy (`runtime_destroy_all.go:87`).
- **Konsistenzrisiko:** brief (item 15) says `target delete` detaches/recovery, `target remove` retains; `root destroy` = whole installation. Current code: `baha destroy` (root) = whole installation with `--data`/`--delete-data`; `app destroy` = app removal. `target` remove vs delete is a *target*-namespace concern, not audited here (outside app slice). No conflict found in the app slice.
- Consistency risk: `--uuid` on `app destroy` is documented as the only unambiguous identity on a poisoned registry (`app_lifecycle.go:201-204`, card 0427-175). Good.

## 8. `baha app prune`

- Entry: `appPruneCommand` `cmd/baha/app_prune.go:39`; `executeApplicationPrune` `app_prune.go:78`; `executeApplicationPruneResolved` `app_prune.go:104`.
- Usage: `baha app prune <name>` (exactly one positional; refuses 0 or >1; refuses unknown flags). Flags: only `--json`/`--output` via `parseReadOutputArgs`.
- Narrow fail-closed guard (`deletionGuard`, `app_prune.go:238`): refuses when source present (recoverable) or record has applied-intent snapshot (real deployment). Resolves by exact NAME naming each match on ambiguity (`resolvePruneByName`, `app_prune.go:326`).
- MCP path pins `authorizedIdentity` and re-validates on-disk identity before delete → fail-closed on same-name drift (`app_prune.go:405-445`); test seam `pruneDriftHook` (internal only, `app_prune.go:311`).
- **trifft** brief's `prune` = `app setup prune`; implementation is a registry-only dangling-record remover. Semantic match is strong.

## 9. `baha app status` / `baha app show` / `baha app version` / `baha app versions`

- `appStatusCommand` `cmd/baha/app_observe.go:203`; TLS-wrapped `appStatusCommandWithTLS` `cmd/baha/app_tls.go:280`. Usage `baha app status [NAME] [-o json]`. Renders Application/Access/Management UIs/Runtime/Service TLS/TLS sections; exit error only when not ready with failures (`applicationStatusCommandError`, `app_observe.go:247`).
- **`baha app show` = `appManifestShowCommand`** (`cmd/baha/app_commands.go:222`), prints `resolved.Manifest.AuthoredYAML()`. The command map lists `baha app show → app status` (`command-map.md:101`). **wicht ab** in the sense of different output: `show` prints the authored manifest YAML; `status` prints runtime readiness. Both exist as distinct leaves. The map conflates them.
- `appVersionCommand` `cmd/baha/app_version_view.go:24` = `baha app version` (single app resolved version view); `appVersionsCommand` `cmd/baha/app_versions_command.go:19` = `baha app versions` (list across all-targets). Map: `version → status/source list`, `versions → list --all-targets/app status`. **trifft** (versions = all-targets inventory).

## 10. `baha app urls` / `baha app logs`

- The map proposes `baha open → app urls` (`command-map.md:20`) and `baha app urls`. Current code has **no `baha app urls` leaf**. URL resolution lives in `publicApplicationAccessURLs` (`cmd/baha/app_access_urls.go:33`) and `applicationAccessURLs` (`app_access_urls.go:14`) — used by status/doctor, not a dedicated command. **wicht ab (new/missing leaf).**
- `baha app logs` → `appLogsCommand` `cmd/baha/app_access.go:139`; root `logs` → same (`commands.go:115-122`). Flags: `[SERVICE] --follow --app NAME`. Normalizes workload logs stdout/stderr to stdout (`app_access.go:163-165`). **trifft.**

## 11. `baha app exec` / `baha app shell`

- `appExecCommand` `cmd/baha/app_access.go:192`, usage `baha app exec SERVICE COMMAND [ARG...] [--app NAME]`. `appShellCommand` `app_access.go:170`, usage `baha app shell SERVICE [--app NAME]`. Both `resolveWorkloadAccess` + `compose.RunProjectFilesEnv`. Flags: `--app`. **trifft** brief's `app exec -c backend` shell / `--cmd` — **wicht ab**: current exec takes `SERVICE COMMAND [ARG...]` positionally, not `-c/--cmd`. The brief's `-c`/`--cmd` is a *proposed* refinement, not current.

## 12. `baha app source` / workspace

- `baha app workspace` → `appWorkspaceCommand` `cmd/baha/app_workspace.go:16`; subcommands `init/map/show/resolve/status/update` (`app_workspace.go:31-38`); `update` = `appWorkspaceUpdateCommand` `cmd/baha/app_workspace_git.go:51`.
- Map: `baha app workspace → app source`, `baha app workspace update → baha app pull` (`command-map.md:24,151`). **Konsistenzrisiko / wicht ab:** `app workspace update` fast-forwards *mapped multi-repo* sources (`app_workspace_git.go:51-90`); `baha app update` (`cmd/baha/app_update.go:44`) fast-forwards the *single app's Git repo* with pre-update backup policy. These are two different surfaces the map collapses to one `app pull`. `app update` flags: `--check`, `--backup-password-file FILE`, `--no-backup` (`app_update.go:148-173`); durable-state (SQL/secrets) requires a recovery point or explicit `--no-backup` (`app_update.go:105-117`).
- Workspace identity stays in `.baseharbor/sources.yaml`; checkout paths in XDG, never Application Intent (`app_workspace.go:21`). **trifft** brief's "App source is a Git repo/local/OCI; pull impacts whole repo, preview of shared impacts".

## 13. `baha app env` (data)

- Entry: `appEnvCommand` `cmd/baha/app_env.go:17`; usage `baha app env [NAME] [--format dotenv|shell|json|yaml] [--reveal] [--path]`.
- Credential-bearing service URLs masked by default; `--reveal` prints real values; `--path` prints only the dotenv path. `maskRuntimeSecrets` (`app_env.go:108`) masks all non-public fields; public set is a fixed allow-list (`isPublicRuntimeEnvironmentField`, `app_env.go:116`) — **new fields fail closed**. `--path` and `--reveal` cannot combine (`app_env.go:75-77`).
- **trifft** brief item 10 (`app data env` app variables; reveal defaults masked; `--reveal` shows selected/all). Current env only has a single global `--reveal` (not per-value selection) — minor divergence, acceptable.

## 14. `baha app creds` / `services`

- Entry: `appCredsCommand` `cmd/baha/app_access.go:96`; usage `baha app creds postgres|valkey [INSTANCE] [--app NAME] [--reveal]`.
- Map proposes `baha app creds → app data services` and `baha app data services` (complete bound service connection data incl. credentials) (`command-map.md:110,113`). **Konsistenzrisiko:** current `creds` is a *console-ish* connection-metadata command for `postgres|valkey` only (SQL + Valkey instances), not the full "bound service connection data incl. all credentials" surface. `--reveal` in JSON is explicitly rejected (`app_access.go:116-118`: "JSON connection metadata never reveals credentials"). Brief wants a richer `app data services` — **wicht ab (partial coverage).**

## 15. `baha app sql` / `cache`

- `appPSQLCommand` `cmd/baha/app_access.go:17` (`baha app sql [INSTANCE] [--app NAME]`); `appRedisCommand` `app_access.go:57` (`baha app cache [INSTANCE] [--app NAME]`). Both `resolveAccessBinding` + `requireManagedClientConsent` before opening the console. **trifft** brief's `app data sql`/`cache` (retained as access consoles).

## 16. `baha app secret` (incl. set/list/delete/tls-set, runtime-identity)

- Entry: `appSecretCommand` `cmd/baha/app_secret.go:21`; children `set/list/delete` (`app_secret.go:30-167`) + `tls-set` (`app_secret_tls.go:26`); `runtime-identity` group `cmd/baha/app_runtime_identity.go:13`.
- `set` usage `baha app secret set [NAME] KEY [--stdin | --file PATH]`. Values never accepted as args or printed; interactive echo-disabled; `--stdin`/`--file` deterministic; `--no-input` requires an input source (`readSecretSetValueInteractive`, `app_secret.go:229-243`). `delete` previews without `--yes` (`app_secret.go:133-166`).
- `list` returns only key names (`app_secret.go:93-126`). OpenBao protection: values stored in isolated scope, never returned. **trifft** brief item 11 (`app data secrets` arbitrary type; list supports single named selection + reveal; OpenBao protection/audit). Divergence: current list shows only names, no single-name reveal (`--reveal` on list not implemented) — brief wanted `app secret` single named selection and reveal; **Konsistenzrisiko**.
- `runtime-identity` set/list/rotate/revoke (`app_runtime_identity.go`) map to `app data secrets identity` per the map. **trifft.**

## 17. `baha app tls` / `app data tls`

- Entry: `appTLSCommand` `cmd/baha/app_tls.go:103`; usage `baha app tls [NAME] [--check] [-o json]`; `update` subcommand reuses the same struct (`app_tls.go:280`). Status section renders TLS mode (existing/acme/local), certificate expiry, update-available. **trifft** brief's `app data tls` guided.

## 18. `baha app backup` / `restore`

- Entry: `appBackupCommand` `cmd/baha/app_backup_restore.go:26`; `appRestoreCommand` `app_backup_restore.go:38`. `executeApplicationBackupLifecycle` `app_backup_restore.go:50`.
- backup usage `baha app backup [NAME] --password-file FILE [--output FILE] [--include-state CLASS] [--exclude-state CLASS]`. restore usage `baha app restore BACKUP [NAME] --password-file FILE`. Backup requires an encrypted recovery unit; restore validates+decrypts before mutation, reconstructs ephemeral identities, restores durable state with workload stopped, then final status/doctor. **trifft** brief's `backup/restore distinct from selectable encrypted export`.

## 19. `baha app data export` / `secure-profile` / `evidence`

- `secureProfileExportCommand` `cmd/baha/secure_profile_export.go:26` (`baha app secure-profile [--export]`); `appEvidenceCommand` `cmd/baha/app_evidence.go:17` (`baha app evidence`, flags `--environment,--json,--output,--uuid`). Map: `secure-profile → app data export`, `evidence → app data export`. **Konsistenzrisiko:** two separate export-ish leaves (`secure-profile` = encrypted export; `evidence` = evidence collect) both loosely map to `app data export`; not clearly distinguishable from the brief.

## 20. Root vs app consistency (overall)

- Root `up` carries management-Core bootstrap flags (`--ha`, `--control-plane-only`, `--postgres-port`, `--openbao-port`, `--recovery-file`, `--trust-host-ca`) that `app up` does **not** — real asymmetry for the taxonomy review.
- Output convention is uniform: `--json`, `-o json|--output json|--output human`, `-ojson` via `parseReadOutputArgs` (`cmd/baha/output.go:16+`). **trifft** brief's "clear short English CLI; `--no-input` never blocks".
- Authorization: every mutation checks `authorizeApplicationOperation`/`authorizeMCPOperation` with a domain op (`app.create`, `app.connection`, `app.prune`, `destroy`, `apply`). Consent (`--yes`) is layered on top, never a substitute. **trifft** brief item 16 (plan→preflight→apply→verify; consent is not an extra reveal password).
- Secret protection: no plaintext in manifests (AuthoredYAML omits ID), masked creds, `--reveal` gated, OpenBao isolation, `zeroBytes`, terminal echo-off. **trifft** brief item 11/16.

## Gaps / risks summary

1. **`--up` flag absent** (`wicht ab`): brief item 2 — `--up` invokes app-up. Not in code anywhere.
2. **`baha app urls` leaf absent** (`wicht ab`): brief item 10 + map `open → app urls`; URL logic exists but no dedicated command.
3. **`app show` ≠ `app status`** (`Konsistenzrisiko` in map): `command-map.md:101` maps `app show → app status`; `show` prints authored YAML (`app_commands.go:222`), `status` prints readiness. Both exist.
4. **`app exec` positional, not `-c/--cmd`** (`wicht ab`): brief item 10. Current `exec SERVICE COMMAND [ARG...]` (`app_access.go:192`).
5. **`app workspace update` vs `app update` collapsed to one `app pull`** (`Konsistenzrisiko`): two distinct surfaces (`app_workspace_git.go:51` multi-repo vs `app_update.go:44` single-app w/ backup policy).
6. **`app creds` ≠ full `app data services`** (`Konsistenzrisiko`): only `postgres|valkey` connection metadata; JSON never reveals; no per-value reveal.
7. **`app secret list` no single-name reveal** (`Konsistenzrisiko`): brief item 11 wanted named selection + reveal.
8. **`baha new` not a top-level command** (`wicht ab`): only a wizard prompt; map's `new → guided selection` is proposed.
9. **`app.id` not committed** (`Konsistenzrisiko`, coordination-required): brief item 14 — authored YAML omits ID (`app.go:256`); wants portable versioned ID.

## AGENTS.md / guidelines compliance

- Read-only audit; no product file edited; no evidence in the product repo. No `.evidence/` directory, no main-branch writes, no subagents (4.8), no `git add -A`. Worktree isolated under `/tmp`. No Docker/Podman started (not a smoke-test mission). No `.github/**` touched. No CI reruns triggered.
- Branch provenance: audit used an isolated detached-HEAD worktree at `0e9ccb582`, not a branch; no candidate branch was cut. Planning base `origin/main = 4c1444f8` re-verified immediately before commit.

## Evidence witness (plan main, pre-commit)

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree --name-only origin/main evidence/cli-redesign-20261114/
brief.md
cleanup28-r1
code-entry-index.md
command-map.md
```
(No `audit-app.md` yet on `origin/main`; this audit is the first commit there.)

## END

lane 0428-044-r28 · audit COMPLETE (read-only, MERGE-FROST honored) · candidate evidence: `evidence/cli-redesign-20261114/audit-app.md` on plan main · my commits: `9b025693` (audit) + `97be908e` (frontmatter/evidence-link); base `9aad6e58` is an ancestor · card left `active` (evidence-only deliverable, no PR — mission forbids a PR and the schema's `review` requires a `prs` entry) · evidence blob on origin/main: `efe44ff31b0759520c122a88b089af9135f09f97`.

## repo-rule compliance

Read-only audit; zero product edits; no evidence written into the product repo (no `.evidence/`, no main-branch writes in baseharbor); no subagents (§4.8); no `git add -A`; isolated read-only worktree `/tmp/baha-audit-wt` at `0e9ccb582` (detached HEAD, not a candidate branch) now removed; no Docker/Podman started; no `.github/**` touched; no CI reruns. Base `origin/main` re-verified immediately before each commit.

## END_DONE

lane 0428-044-r28 · END_DONE · audit-app.md · candidate SHA 9b025693 (plan main); 97be908e frontmatter · card active (evidence-only, no PR) · END per dispatch to 594fd2f5.
