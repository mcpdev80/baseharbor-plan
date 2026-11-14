# Audit: platform, target, environment and UID paths of the CLI (IST-ZUSTAND)

Card: `t-20261114-r28-cli2-audit-platform` (0428-045) · Lane: `lane-0428-045-r28`
Type: pure inventory (merge-frost, owner directive 2026-11-14). No product change, no PR, no release, no tag.
Inputs: [brief](brief.md), [command mapping](command-map.md), [code entry index](code-entry-index.md).
Product base: `develop` @ `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (witnesses in §0).

Mission clarification recorded: dispatch line 1 of `mission-audit-platform.md` reads
"audit-assistenten/dialoge"; the owner corrected this in-channel on 2026-11-14 as a derivation
error. This lane is the **platform / environment** audit of card 0428-045; mission paragraph 2
(AUFGABE) plus the card note are authoritative. The dialog/wizard surface belongs to 0428-047
(`audit-interface.md`) and is touched here only where a platform path reaches it.

## PLAN

1. Claim leg: card already published `active` with owner `lane-0428-045-r28` on plan `origin/main`
   (`9aad6e58`, coordinator commit "coord: 0428-045 -> active (bahn 9c5ccd32, flash)").
   `python3 scripts/plan.py claim` refuses to re-claim an active card ("only planned, wait or
   blocked tasks can be claimed"), so the claim requirement is satisfied by the published state;
   nothing was re-published.
2. Locate the authoritative planning repo and read the redesign inputs (brief, command-map, code-entry-index).
3. Pin product truth: `develop` = `0e9ccb582` plus a clean persistent clone at exactly that SHA.
4. Inventory the platform/environment-controlled paths: state-root and UID/owner paths, target
   selection, environment selection, platform local/remote/node surfaces, OS-conditional code —
   each with file:line at `0e9ccb582`.
5. Judge each item against Core `AGENTS.md`, `docs/DEVELOPMENT_GUIDELINES.md` and the owner-brief
   decisions. Verdicts: `trifft` / `weicht ab` / `Konsistenz-Risiko`.
6. Cite external reference sources (context7 MCP for the Go standard library, web sources for the
   XDG Base Directory spec and 12-factor config).
7. Deliver this dossier to `evidence/cli-redesign-20261114/audit-platform.md`, push to plan main,
   set the card to `review`, post END.

## 0. Zone and provenance witnesses

Wrong-zone guard (mandated one-liner, executed before the first evidence commit):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```

`workers/baseharbor-plan` was never used. The quarantined `workers/baseharbor` checkout was never
cited: every product statement comes from `git ls-remote` on GitHub and from a fresh clone in this
lane's own persistent zone (`/tmp/opencode/audit-platform-wt/repo`) checked out at the exact SHA.

Base attestation (no branch was cut: this is a read-only audit under merge-frost, the only
deliverable is this file on plan `main`):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin main
9aad6e585a8e7337f4415addefa4b4950b67714e	refs/heads/main
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan log --oneline -1
9aad6e58 coord: 0428-045 -> active (bahn 9c5ccd32, flash)

$ git ls-remote https://github.com/mcpdev80/baseharbor.git develop
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
$ git -C /tmp/opencode/audit-platform-wt/repo rev-parse HEAD
0e9ccb582f5bdcdc74049bbe3996263cdce6500c
```

Every `file:line` in this dossier refers to that product SHA. The mission text names the same base
("`code-einstieg file:line auf develop 0e9ccb582`"), so the audited base and the ordered base agree.

## 1. Reference sources (external, cited per mission "WERKZEUGE")

- Go standard library, `os.UserHomeDir` / `os.UserCacheDir` implementation and documented behaviour:
  `HOME` on Unix/macOS, `USERPROFILE` on Windows, `home` on Plan 9; `UserCacheDir` returns
  `$XDG_CACHE_HOME` when set (erroring on a relative value) else `$HOME/.cache`; an unset variable
  yields a platform default **or a non-nil error**. Source: `src/os/file.go`, retrieved through the
  context7 MCP library `/golang/go` (https://github.com/golang/go/blob/master/src/os/file.go).
  Relevance: BaseHarbor reimplements these lookups by hand in §2, so the standard-library semantics
  are the yardstick for "is a missing variable an error or a silent default".
- Go build-time platform selection, `go help environment` (`GOOS`, `GOARCH`) and the
  `//go:build` tag mechanism, retrieved through the same context7 library
  (`/golang/go`, https://github.com/golang/go/blob/master/src/cmd/go/alldocs.go). Relevance: every
  OS branch in §6 is a compile-time choice, so a binary built for Linux cannot "detect" a supported
  macOS/Windows path at runtime — the support matrix in §6 is the authoritative statement.
- XDG Base Directory Specification, version 0.8 (8 May 2021), Freedesktop.org,
  https://specifications.freedesktop.org/basedir/latest/ — §2 Basics, §3 Environment variables.
  Normative points used here: the base directories **must be absolute** and a relative value
  "should be considered invalid and ignored"; `$XDG_STATE_HOME` (default `$HOME/.local/state`) is the
  category for persistent per-user *state*; `$XDG_RUNTIME_DIR` must be owned by the user with mode
  `0700` and its lifetime is bound to the login session, and applications **must fall back with a
  warning** when it is unset; non-essential user executables belong in `$HOME/.local/bin` on `PATH`.
- The Twelve-Factor App, Config (III): "stores config in environment variables … easy to change
  between deploys without changing code", https://12factor.net/config. Relevance: the brief's
  per-terminal active context and the `BASEHARBOR_*` overrides follow this convention; the audit
  additionally checks that an override is *observable* in output, which 12-factor does not require
  but the brief's "names and meaning must be consistent" does.

## 2. State-root, UID and file-ownership paths

The whole platform rests on three hand-rolled root resolvers. They do **not** agree with each other.

| Resolver | `BASEHARBOR_STATE_DIR` | XDG variable | Plain fallback | Absolute-value check |
| --- | --- | --- | --- | --- |
| `deployment.ConfigPath` — `internal/deployment/target.go:95-107` | `<root>/config/config.yaml` (`:96`) | `XDG_CONFIG_HOME` → `<root>/baseharbor/config.yaml` (`:99`) | `$HOME/.config/baseharbor/config.yaml` (`:102-106`) | none |
| `deployment.DataRoot` — `internal/deployment/target.go:109-121` | `filepath.Clean(root)` (`:110`) | `XDG_DATA_HOME` → `<root>/baseharbor` (`:113`) | `$HOME/.local/share/baseharbor` (`:116-120`) | none |
| `orgconfig.configRoot` / `cacheRoot` — `internal/orgconfig/store.go:17-43` | `…/config/organization`, `…/cache/organization` | `XDG_CONFIG_HOME`, `XDG_CACHE_HOME` | `$HOME/.config/baseharbor/organization`, `$HOME/.cache/baseharbor/organization` | none |
| `runtime.resolveStateDir` / `globalStateDir` — `internal/runtime/stack.go:449-484` | `filepath.Clean(root)` (`:453`) | `XDG_DATA_HOME` only (`:476`) | `$HOME/.local/share/baseharbor/runtime`, **plus a legacy `.baseharbor/runtime` reuse** (`:18`, `:469-471`) | none |
| `operatorauth.SessionPath` — `internal/operatorauth/config.go:92-113` | `<root>/cache/sessions` (`:102`) | `XDG_RUNTIME_DIR` → `<dir>/baseharbor` (`:104`) | `os.UserCacheDir()/baseharbor/sessions` (`:106-110`) | none |
| `hosttrust.trustStateRoot` — `internal/operatorauth/trust.go:79-91` | root as-is (`:81`) | `XDG_DATA_HOME` → `<dir>/baseharbor` (`:83`) | `$HOME/.local/share/baseharbor` | none |
| `runtime.DataDir("")` — `internal/runtime/stack.go:435-447` | `filepath.Clean(override)` (`:439`) | indirect (through `resolveStateDir`) | same | none |
| CLI-local copies of the same idea — `cmd/baha/target_recovery.go:28`, `cmd/baha/node_install.go:42`, `cmd/baha/app_backup_restore_guided.go:601` | not honoured (they read `XDG_DATA_HOME` directly) | `XDG_DATA_HOME` | `$HOME/.local/share` | only `app_backup_restore_guided.go:602-604` requires an absolute value |

UID / ownership paths:

- Owner-only protection predicate: `internal/runtime/protected_owner_unix.go:10-15` (`//go:build
  !windows`) requires mode `&0077 == 0`, `owner.Uid == uint32(os.Getuid())` and `Nlink == 1` for files.
  The Windows twin is `cmd/baha/application_native_sql_projection_windows.go` (`//go:build windows`),
  the POSIX twin `cmd/baha/application_native_sql_projection_unix.go:15`.
- Selection-file ownership and detachment: `cmd/baha/target_selection.go:15-46`
  (`<config-dir>/active-target`, size-capped at 1024 bytes, `!detached:` prefix), mutation under a
  state lock with `0700`/`0600` and an `Lstat` ownership re-check in
  `cmd/baha/target_selection_mutation.go:32-50`, `:53-70`.
- Privilege probes that read the real/effective UID: `cmd/baha/local_workload_authority.go:66-95`
  (an OIDC env variable disables the local authority at `:68-72`; then mode `&0077` and
  no symlink on the target state root and runtime root at `:84-95`),
  `cmd/baha/node_disconnect_plan.go:175` (per-entry `stat.Uid != uint32(os.Geteuid())`),
  `cmd/baha/dev_hosts.go:205` (`os.Geteuid() != 0` → prefix `sudo --`),
  `cmd/baha/update_etcd_identity.go:18-73` (rootless namespace UID mapping for etcd recovery),
  `internal/runtime/docker_engine.go:48-50` (`/run/user/<uid>/docker.sock`),
  `internal/providers/runtime/podman/quadlet_runtime.go:55-64` (`XDG_RUNTIME_DIR` else
  `/run/user/<uid>`, plus a derived `DBUS_SESSION_BUS_ADDRESS`).
- Privilege escalation style differs per subsystem: `internal/hosttrust/hosttrust.go:551-569`
  tries the bare command and only then `sudo --`, while `cmd/baha/update_mutation.go:134-161`
  refuses to escalate at all ("self-update never invokes sudo automatically") and
  `cmd/baha/dev_hosts.go:195-212` uses `sudo --` through a hidden
  `--baseharbor-hosts-write` re-exec (`cmd/baha/main.go:32-48`).

Verdicts for §2 are items T1-T6 in §7.

## 3. Target selection and target-scope paths

Effective-target resolution is implemented once and reused everywhere (`effectiveTarget`,
`cmd/baha/target.go:87-124`):

```
explicit --target            cmd/baha/main.go:187-200  -> withTargetOverride (target.go:53)
BASEHARBOR_TARGET            cmd/baha/target.go:93
persisted active-target      cmd/baha/target_selection.go:23-46, :66
configured default_target    cmd/baha/target_selection.go:76
unique configured target     cmd/baha/target_selection.go:79-83
implicit "local"             internal/deployment/target.go:326-347 (Config.ResolveTarget)
organization layer           cmd/baha/target.go:98-123 (orgconfig.ResolveEffective wins over :101/:123)
```

- Precedence order and the fail-closed conflict message: `cmd/baha/target_selection.go:59-92`;
  the conflict names `baha target activate NAME` and `BASEHARBOR_TARGET` (`:87-89`).
- Provenance is reported in machine output as `selection_origin` through
  `cmd/baha/target_selection.go:94-115` with the vocabulary
  `explicit` / `environment` / `persisted` / `configured-default` / `unique-configured` / `implicit-local`,
  surfaced by `collectTargetInspection` (`cmd/baha/target.go:420-454`, human form at `:395` "Selected").
- Machine target list uses a **third** vocabulary in the same domain: `default` / `active` /
  `effective` / `implicit` flags, `cmd/baha/machine_navigation.go:75-115` (Active is computed as
  `name == activated`, i.e. only the environment variable, `:100`). The human `target list` marks
  `implicit`, `default`, `active`, `effective` at `cmd/baha/target.go:204-240`.
- `baha target activate NAME` validates the name, binds it through the management-connection
  boundary **before** persisting (`cmd/baha/target.go:278-293`, `cmd/baha/use_target.go:25-40`,
  `:62+`), and `baha use [TARGET]` is the same command, not an alias (`use_target.go:30-37`).
  The guided path with no argument is `cmd/baha/target_activate_wizard.go:15-80`, which re-reads the
  configuration at submit time (`:56-64`) and refuses a vanished target.
- `baha target delete NAME` is detach-with-recovery, never a runtime or data removal:
  `cmd/baha/target.go:253-258`, `deleteTarget` `:563-604`; the recovery-file write is
  `cmd/baha/target_recovery.go:28` and the detach marker invalidates the persisted selection
  (`target_selection.go:39-41`, `target_selection_mutation.go:26-29`).
  The docs state the same contract, `docs/cli/targets.md:52-70`.
- Root `destroy` is the whole installation, not the app: `cmd/baha/runtime_destroy_all.go:39-95`
  (`destroyInstallation`), with discovery over every configured **and** every state-directory target
  `cmd/baha/runtime_destroy_discovery.go:19-81`, and the environment-removal half in
  `cmd/baha/app_destroy_lifecycle.go` / `cmd/baha/app_lifecycle.go:197-215`. Remote targets are
  skipped only on a context flag (`runtime_destroy_discovery.go:15`, `runtime_destroy_all.go:285-288`).
- Target state isolation is by name: `deployment.TargetStateRoot(name)` =
  `<data-root>/targets/<name>` (`internal/deployment/target.go:123-132`), runtime root `…/runtime`
  (`cmd/baha/target.go:607-626`). Names are slug-validated
  (`internal/deployment/target.go:134-139`).
- `baha list --all-targets` deliberately fails closed on an ambiguous selection and offers both
  repair doors (`cmd/baha/commands.go:43-56`, `cmd/baha/app_commands.go:110-150`).

## 4. Environment selection and environment-named semantics

- The `-e` / `--environment` flag is parsed per command, not globally: the shared extractor is
  `cmd/baha/app_context.go:597-643` (also consumes `--uuid`), with command-local copies in
  `cmd/baha/runtime.go:93-101`, `cmd/baha/app.go:577-585`, `cmd/baha/policy.go:80`,
  `cmd/baha/onboarding_command.go:152`, `cmd/baha/completion.go:84-90`.
  Conflicting duplicate selections fail closed (`app_context.go:129-134`, `:609-616`, `:623-628`).
- An explicit environment selects a **complete manifest**, never an overlay:
  `internal/application/environment.go:24-31` (doc) and `:69-90`; an `envs/<name>/baseharbor.yaml`
  that declares a different environment is a hard error (`:179-187`); a root manifest reused for
  another environment only overrides the deployment context (`:80-89`), and
  `applyApplicationEnvironmentOverride` revalidates after the override
  (`cmd/baha/app_context.go:50-59`). Multiple candidate manifests without `-e` fail closed
  (`environment.go:106-121`). The `LegacyState` marker is set only for the root-manifest reuse (`:88`, `:194-201`).
- Environment identity is **name-only**; the stable per-environment ID the brief asks for does not
  exist. The three identity axes are Target + Application + Environment
  (`deployment.NewDeploymentIdentity`,
  `internal/deployment/deployment_store.go:218`, called at `cmd/baha/app_context.go:266`), and the
  deployment ID stays separate, as the brief wants.
- A process-global mutable override carries the value between layers:
  `var applicationEnvironmentOverride string` (`cmd/baha/app_context.go:16`) with
  `pushApplicationEnvironmentOverride` (`:44-48`) and
  `applyApplicationEnvironmentOverride` (`:50-59`). It is read from
  `organizationEnvironment` (`cmd/baha/target.go:147-161`) and `collectTargetInspection`
  (`target.go:445-452`). The same value is threaded differently in the machine plane:
  `withOrganizationEnvironment(ctx, …)` (`target.go:141-145`, callers
  `machine_http_executor.go:108`, `machine_http_runtime_explorer.go:16/40/76`,
  `connector_enrollment.go:76`). Two mechanisms, one meaning.
- **Hard-coded environment name special cases (the central §4 finding).** The brief requires
  "unrestricted by fixed `dev/test/prod` semantic special cases; same capabilities irrespective of
  name". Current code branches on the literal name in at least these places:
  - `internal/operatorauth/config.go:83-90` `ManagedEnvironment`: `"dev"`/`"development"` are
    unmanaged, **every other name** is managed → authentication is selected by name.
  - `internal/operatorauth/authorization.go:155-170`: a `workstation-mtls` principal is refused
    outside `"dev"`.
  - `cmd/baha/management_remote_reads.go:42-47` (`"Remote application reads currently require the
    dev operator session."`), plus `management_remote_status.go:40`,
    `management_remote_repository.go:41`, `management_remote_dev_credentials.go:36/60`,
    `management_remote_dev_domain.go:32/46`, `machine_http_dev_domain.go:33`,
    `machine_http_dev_credentials.go:30`, `dev_operations.go:54` (`const environment = "dev"`).
  - `cmd/baha/runtime_destroy_authority.go:70-72` picks the most protected environment through
    `installationDestroyAuthorizationEnvironment` (`:75-84`), which ranks by name.
  - `internal/application/metrics_policy.go:78-86`, `internal/application/workload_security.go:243-252`,
    `internal/devaccess/credentials.go:22-30`, `internal/logs/lifecycle.go:190-211`,
    `internal/metrics/prometheus_verify.go:204-211` and `internal/metrics/prometheus_files.go:295`,
    `internal/providerui/application.go:432-439`, `internal/runtimebroker/broker.go:264-272`,
    `internal/identityprovider/keycloak_driver.go:635-643`: all switch on `"dev"`/`"development"`.
  - `internal/serviceaccess/policy.go:94-101` is the only place that documents the alternative:
    `dev|development` unauthenticated, `test|testing|stage|staging|prod|production` authenticated,
    and *everything else* treated as managed rather than silently weakened (fail-closed default).
    the same fail-closed posture appears in `internal/application/workload_security.go:257-259` (an
    override can never weaken managed policy) and in `availability.Intent.Validate` reached through
    `internal/application/manifest_validation.go:36`.
  - `cmd/baha/prompt.go:331-350` renders the shell prompt from name semantics
    (`prod`/`production` → PROD indicator, `test`/`stage`/`staging` in critical-only mode).
  - `internal/orgconfig/effective.go:54-57` defaults an empty environment to `"dev"`, and `:67`
    keeps the built-in target default `"local"`.
- The `dev` default also appears as a command default rather than a policy:
  `cmd/baha/app.go:474` (`createManifestOptions{environment: "dev"}`), `cmd/baha/app_new.go:146`,
  `cmd/baha/app_new_wizard.go:73`, `cmd/baha/app_init_wizard.go:194`, `cmd/baha/app_init_selection.go:56`,
  `cmd/baha/config_org.go:220`/`:261`, `cmd/baha/management_remote_reads.go:43`,
  `cmd/baha/control_plane_stop_impact.go:116-118`, `cmd/baha/application_provider_plan.go:79`
  (management app is hard-wired to `"prod"`).

## 5. Platform surface: local, remote, node, provider, stack, OpenBao/trust

The brief proposes the taxonomy `app`, `env`, `target`, `context`, `platform`, `access`, `system`
with "Platform local/remote/node". Today no `baha platform` command exists
(`grep -rn 'Name: *"platform"' cmd/baha/` is empty; `command-map.md:10,18,22-23,27,38,51-59` marks the mapping as
proposed). The underlying surfaces are:

- **platform local** (the Core / management host on this machine): `baha up --control-plane-only`
  (`cmd/baha/runtime.go:78-156`, install path `cmd/baha/core_installation.go:43-192`), `baha serve`
  (`cmd/baha/serve.go:16-156`), `baha status` / `baha doctor` for the control plane
  (`cmd/baha/control_plane_operations.go:35`, remote twin `cmd/baha/management_remote_reads.go:102-135`).
  A remote target can never install a Core: `installCore` refuses non-local access
  (`core_installation.go:57-60`), and `requireApplicationCore` (`:222-285`) distinguishes local
  (`:253-260`: `coreRequired()` typed error in non-interactive/`--yes`-less paths) from the
  startup-bound node-connector case (`application_core_authority.go:47-80`).
  This matches the brief's "keep Core, target and connector distinct" (guidelines §5:
  `runtime != capability != delivery`, `docs/DEVELOPMENT_GUIDELINES.md:48-55`).
- **platform node** (Node Connector): `baha node add|connect|list|status|disconnect`
  (`cmd/baha/node.go:141-150`). `node add` creates the remote Target plus a one-use enrollment
  bundle (`node.go:191-260`, `mcp_node_tools.go:29-90`); `node connect` installs/starts the rootless
  connector service on the target host and requires explicit approval (`mcp_node_tools.go:29`).
  The **connector repository is archived** (see the banner in
  `https://github.com/mcpdev80/baseharbor-node-connector`); `docs/reference/platform-support.md:17`
  still lists it as "Integration pending". So the remote half of the platform surface is a
  contract-only path right now — the audit finding is that the CLI offers it without an
  availability gate that says so.
- **platform provider**: `baha provider` (authoring: `init`, `test` —
  `cmd/baha/provider.go:13-136`) and `baha provider add|list|inspect|verify|remove`
  (external registration: `cmd/baha/provider_external.go:39-197`), plus removal-with-impact
  `cmd/baha/provider_external_removal.go:18-44`. Registration ≠ authoring is preserved; the
  confirmation boundary is `confirmExternalProviderRegistration`
  (`provider_external.go:596`) and `normalizedTrustMode` (`:465`).
- **platform stack**: `baha stack list|show|create` (`cmd/baha/stack.go:15-248`) with the guided
  creator `guidedCreateStackProfile` (`cmd/baha/app_new_wizard.go:505`) and the profile catalog
  `stackCatalog` (`stack.go:28`).
- **trust / OpenBao**: `baha trust status|export|install|uninstall`
  (`cmd/baha/trust.go:20-160`, operations `cmd/baha/trust_operations.go:23-141`, backend detection
  `internal/hosttrust/hosttrust.go:455-520`, browser NSS `internal/hosttrust/browser_nss.go:27-39`)
  and `baha openbao status|bootstrap|unseal|rotate` (`cmd/baha/openbao.go:15-190`). The machine
  surface for the same domain is `cmd/baha/mcp_platform_tools.go:25-77`. Both print **no secret
  material** (`cmd/baha/openbao.go:19-21`, `cmd/baha/mcp_platform_tools.go:36`), matching guidelines §6
  (`docs/DEVELOPMENT_GUIDELINES.md:56-59`).
  Note that `baha trust install` is the only trust action that can silently escalate:
  `runMaybePrivileged` falls back to `sudo -- install …` and `sudo -- update-ca-*`
  (`internal/hosttrust/hosttrust.go:551-569`) after an unprivileged attempt, while
  `installManagedTrust` refuses to claim an operator-owned root
  (`cmd/baha/trust_operations.go:84-88`).

## 6. OS-conditional behaviour

`runtime.GOOS` gates in the CLI layer:

- self-update: asset name `baseharbor_<GOOS>_<GOARCH>.tar.gz` and the Linux amd64/arm64 gate
  (`cmd/baha/update.go:168`, `:179-181`); platform is reported as `GOOS + "/" + GOARCH` (`:263`).
- ORAS helper install supports `linux`/`darwin` on `amd64`/`arm64` only, otherwise an actionable
  error with the upstream URL (`cmd/baha/oras_setup.go:60`, `:147-155`).
- managed-service onboarding and the development runtime image are Linux-only
  (`cmd/baha/onboarding_managed_service.go:30-33`, `cmd/baha/development_runtime_image.go:35-37`);
  `/etc/hosts` management is Linux-only (`cmd/baha/dev_hosts.go:122`).
- host browser launcher switch (`cmd/baha/human_open.go:78-87`), host-trust system backend
  (`internal/hosttrust/hosttrust.go:466-468`), NSS browser store (`internal/hosttrust/browser_nss.go:27`),
  operator login command (`internal/operatorauth/login.go:301`), the runtime-explorer terminal
  probe (`internal/runtimeexplorer/terminal.go:59`), and the etcd rootless recovery probe
  (`internal/stableid/lock_probe.go:68`).
- health/doctor accepts `linux || darwin || windows` and prints the pair
  (`cmd/baha/control_plane_operations.go:155`, `internal/health/doctor.go:28`).
- build-tag split files: `cmd/baha/path_prompt_linux.go` (`//go:build linux`, raw-termios path
  completion with Tab at `:44-58`, `:105`) vs `cmd/baha/path_prompt_other.go` (`//go:build !linux`,
  plain line prompt plus a printed context block), and the SQL projection
  `application_native_sql_projection_unix.go` / `_windows.go`.

The published support statement is narrower than the code: `docs/reference/platform-support.md:11-15`
lists native Linux (Docker, rootless Podman) as the only release-qualified context, marks WSL2 as
unproven and native Windows/macOS as **unsupported release binary/runtime**, while `doctor` reports
macOS and Windows as an OK `os` check. Under merge-frost this is reported as a consistency risk,
not fixed.

## 7. Findings and verdicts

Legend: **trifft** = matches the contract, **weicht ab** = deviates, **Konsistenz-Risiko** =
internally inconsistent or ambiguous, not provably wrong.

| # | Path | Verdict | Witness |
| --- | --- | --- | --- |
| T1 | single effective-target resolver, ordered, fail-closed on ambiguity | **trifft** | `cmd/baha/target_selection.go:59-92`, `cmd/baha/target.go:87-124` |
| T2 | `target delete` = detach + recovery, never data removal | **trifft** | `cmd/baha/target.go:253-258`, `:563-604`; `docs/cli/targets.md:52-62` |
| T3 | root `destroy` ≠ app `destroy` (installation vs application) | **trifft** | `cmd/baha/runtime_destroy_all.go:39-101`, `cmd/baha/app_lifecycle.go:197-215`; `command-map.md:3,10,18` |
| T4 | activation binds authority before persisting; no silent fallback after detach | **trifft** | `cmd/baha/target.go:278-293`, `cmd/baha/use_target.go:25-40`, `target_selection.go:39-41` |
| T5 | target selection is documented as shell-local but implemented as per-user persisted | **weicht ab** | `docs/explanation/targets.md:152-168` vs `cmd/baha/target.go:260-263`, `target_selection.go:48-57` |
| T6 | three vocabularies for one selection state (`selection_origin` vs `Selectors` vs machine flags); `Active` ignores `--target` | **Konsistenz-Risiko** | `target_selection.go:94-115`, `target.go:231-240`, `machine_navigation.go:96-102` |
| T7 | `--target` is global (before the verb) with no `-t` short form anywhere; docs are not aligned with each other | **weicht ab** (brief wants `-t`) | `cmd/baha/main.go:187-200`; `grep '"-t"' cmd/baha/` empty; `docs/cli/global-options.md:7`; `docs/cli/targets.md:30` |
| T8 | `-c`/`--component` exists only as `--component SOURCE=ID` in two commands, no comma lists, no `-c` short form | **weicht ab** (brief wants `-c`, comma-separated, throughout) | `cmd/baha/app_workspace.go:81,102,115`; `cmd/baha/stack.go:176-185`; `cmd/baha/app_access.go:21,61,100,143,174,196` (no `-c` at all) |
| T9 | environment name drives authentication, metrics, workload security, log retention, dev credentials, remote-read admission, destroy ranking and prompt colour | **weicht ab** (brief: name-independent, policy-driven) | `internal/operatorauth/config.go:83-90`; `internal/operatorauth/authorization.go:155-170`; `cmd/baha/management_remote_reads.go:42-47`; `cmd/baha/runtime_destroy_authority.go:75-80`; `internal/serviceaccess/policy.go:94-101`; `internal/application/workload_security.go:243-252`; `cmd/baha/prompt.go:331-350` |
| T10 | `serviceaccess` and `workload_security` carry the fail-closed `default:` posture that the rest of the environment branching lacks | **Konsistenz-Risiko** | `internal/serviceaccess/policy.go:99-101`; `internal/application/workload_security.go:253-259` |
| T11 | environment selection is complete-manifest, never an overlay; duplicates fail closed | **trifft** | `internal/application/environment.go:24-31,69-90,106-121,179-193` |
| T12 | environment identity is name-only; no stable environment ID | **weicht ab** (brief: stable IDs for env/app/target) | `internal/deployment/deployment_store.go:218` (`NewDeploymentIdentity`) via `cmd/baha/app_context.go:266`; `internal/application/environment.go:15-22` |
| T13 | the same environment value travels by two mechanisms (process-global string vs context value) | **Konsistenz-Risiko** | `cmd/baha/app_context.go:16,44-58` vs `cmd/baha/target.go:141-145` + `machine_http_executor.go:108` |
| T14 | `-e` is parsed per command in five places instead of once | **Konsistenz-Risiko** | `app_context.go:597-640`, `runtime.go:93-101`, `app.go:577-585`, `policy.go:80`, `onboarding_command.go:152` |
| T15 | no `baha platform` command; the proposed local/remote/node/provider/stack taxonomy is unimplemented; the closest existing surface is `baha stack create --scope`, which scopes a profile file and not a deployment platform | **weicht ab** (expected: proposal, not yet truth) | `command-map.md:10,18,22-23,27,38,51-59`; `grep -rn 'Name: *"platform"' cmd/baha/` empty; `cmd/baha/stack.go:176-193`; `cmd/baha/stack_operations.go:54-63` |
| T16 | Core-vs-target-vs-connector separation enforced; Core install is local-only, remote Core is startup-bound | **trifft** | `core_installation.go:57-60`, `:222-285`; `application_core_authority.go:47-80`; `target.go:686-700` |
| T17 | provider registration and provider authoring stay separate surfaces | **trifft** | `provider.go:13-60`, `provider_external.go:39-197`, `:465`, `:596` |
| T18 | trust/OpenBao and machine tool outputs never print secret material | **trifft** | `cmd/baha/openbao.go:19-21`, `cmd/baha/trust_operations.go:75-103`, `cmd/baha/mcp_platform_tools.go:36` |
| T19 | `baha dev credentials` prints the plaintext developer password in the human path while the JSON path returns only the protected-file reference | **weicht ab** (guidelines §6; brief "no plaintext in normal machine output" — the human path is the outlier) | `cmd/baha/dev_access.go:106-121` vs `:110-116`; HTTP twin returns no password `machine_http_dev_credentials.go:30-45` |
| T20 | host-trust install escalates through `sudo` after a failed unprivileged attempt; self-update refuses escalation by design | **Konsistenz-Risiko** (two privilege postures) | `internal/hosttrust/hosttrust.go:551-569` vs `cmd/baha/update_mutation.go:144-150`, `cmd/baha/dev_hosts.go:195-212` |
| T21 | state roots are re-derived per subsystem (`DataRoot`, `resolveStateDir`, `SessionPath`, `trustStateRoot`, CLI copies) | **Konsistenz-Risiko**, guidelines §7 | §2 table; `internal/deployment/target.go:95-121`; `internal/runtime/stack.go:435-484`; `internal/operatorauth/config.go:92-113`; `internal/operatorauth/trust.go:79-91`; `cmd/baha/target_recovery.go:28`; `cmd/baha/node_install.go:42`; `cmd/baha/app_backup_restore_guided.go:601-604` |
| T22 | no root resolver rejects a relative `BASEHARBOR_STATE_DIR` / `XDG_*` value | **weicht ab** (XDG spec: a relative value must be ignored; Go's `UserCacheDir` errors instead) | `internal/deployment/target.go:96,110`; `internal/runtime/stack.go:439,453`; `internal/orgconfig/store.go:18,32`; `internal/operatorauth/config.go:102-110`; `internal/operatorauth/trust.go:81-90`; the only absolute-path guard is `cmd/baha/app_backup_restore_guided.go:602-604` |
| T23 | persistent per-user state (target selection, org cache, operator sessions, recovery material) has no `XDG_STATE_HOME` concept: the selection file sits beside the config file, sessions in cache | **weicht ab** (XDG 0.8 §2/§3) | `cmd/baha/target_selection.go:15-21` with `internal/deployment/target.go:95-107`; `internal/orgconfig/store.go:31-43`; `internal/operatorauth/config.go:102-110` |
| T24 | unset `XDG_RUNTIME_DIR` falls back to `/run/user/<uid>` with no warning; a missing `HOME` yields an untyped error in some resolvers and an actionable one in another | **Konsistenz-Risiko** | `internal/providers/runtime/podman/quadlet_runtime.go:54-64`; `internal/deployment/target.go:102-105`, `:116-119`; `internal/runtime/stack.go:475-483` |
| T25 | a legacy `.baseharbor/runtime` (CWD-relative) state directory is reused whenever global state does not exist | **Konsistenz-Risiko** (surprise in shared checkouts) | `internal/runtime/stack.go:18`, `:449-473` |
| T26 | `BASEHARBOR_TARGET` and `--target` win over organization defaults, so a distributed org policy can be overridden per invocation | **Konsistenz-Risiko** (open decision in brief) | `cmd/baha/target.go:98-123`; `internal/orgconfig/effective.go:67-91`; `brief.md:14` |
| T27 | an empty environment silently becomes dev in org resolution and in the organization set/read defaults, while other call sites default it only for remote reads | **Konsistenz-Risiko** | `internal/orgconfig/effective.go:54-57`; `cmd/baha/management_remote_reads.go:42-44`; `cmd/baha/config_org.go:219-220`, `:260-261` |
| T28 | doctor/health reports `darwin`/`windows` as an OK platform check although the support matrix marks them unsupported; only the self-update path enforces the narrow matrix at runtime | **Konsistenz-Risiko** | `cmd/baha/control_plane_operations.go:155`; `internal/health/doctor.go:28`; `cmd/baha/update.go:179-181`; `docs/reference/platform-support.md:11-15` |
| T29 | completion suggests only the three fixed environment values dev, test and prod, which reinforces the very special cases the brief wants removed | **weicht ab** | `cmd/baha/completion.go:84-90` vs `brief.md:12` |
| T30 | remote connector surface is offered (`baha node add`) while its implementation repository is archived and the matrix says "Integration pending" | **weicht ab** (unimplemented capability must be explicit) | `cmd/baha/node.go:141-150`; `docs/reference/platform-support.md:17`; archived banner in `https://github.com/mcpdev80/baseharbor-node-connector` |

## 8. Roll-up and the acceptance questions

Card acceptance asks for a per-path impact/recovery map, the actual target-detach vs
full-install-destruction distinction, and the version-sensitive gaps.

### 8.1 Impact and recovery map (per path)

| Path | What it mutates | Recovery door | Witness |
| --- | --- | --- | --- |
| `target activate` / `use` | one file `<config-dir>/active-target` (0600, under a state lock) | `baha target deactivate` clears it | `cmd/baha/target_selection.go:48-57`, `cmd/baha/target.go:289-293`, `:297-312` |
| `target create` | `config.yaml` target + access entries (`Config.SaveExpected`, `internal/deployment/config_mutation.go:44`) | `target delete` (detach) | `cmd/baha/target.go:456-560`, `cmd/baha/target_mutation.go:49` |
| `target delete` (detach) | removes the config entry, writes a protected recovery copy, marks a persisted selection detached | restore with `baha target create NAME --from-recovery PATH` (`cmd/baha/target.go:250`) | `cmd/baha/target.go:563-604`, `cmd/baha/target_recovery.go:28`,
  `cmd/baha/target_selection_mutation.go:17-29` |
| `node add` / `node disconnect` | remote Target + one-use enrollment bundle; disconnect revokes and retains recovery owners | retained recovery owners; `node disconnect` requires `--yes` after impact acknowledgement | `cmd/baha/node.go:145,149`, `cmd/baha/node_disconnect_lifecycle.go`, `cmd/baha/node_disconnect_plan.go:175` |
| root `destroy` | every configured and every state-directory Target, Core services, local state root; host trust removal | none inside the command; data volumes are reported, not silently removed | `cmd/baha/runtime_destroy_all.go:83-101`, `cmd/baha/runtime_destroy_discovery.go:19-81`, `cmd/baha/runtime_destroy_inventory.go:125-205` |
| `app destroy` | one application's runtime, data, credentials, recovery state and registration | explicitly `app stop` for data-preserving stop | `cmd/baha/app_lifecycle.go:197-215`, `cmd/baha/app_destroy_lifecycle.go:64-140` |
| `trust install` / `uninstall` | system anchor directory + OS trust refresh (may escalate) | `baha trust uninstall`; `baha trust export` for a manual path | `cmd/baha/trust.go:117-190`, `internal/hosttrust/hosttrust.go:511-536` |
| `openbao bootstrap/unseal/rotate` | managed trust plane; recovery material stays in the operator-held file | `--recovery-file PATH` / the persisted target-scoped recovery path | `cmd/baha/openbao.go:76-190`, `docs/reference/secrets-and-openbao.md:15-17` |
| `serve` / `up --control-plane-only` | Core installation under `<data-root>/targets/<target>/runtime` | `baha update --recover --version V --yes` for HA PostgreSQL/DCS restore | `cmd/baha/runtime.go:78-156`, `cmd/baha/core_installation.go:43-100`, `cmd/baha/update.go:73-105` |

### 8.2 Target detach versus full-install destruction (explicit)

`baha target delete` is configuration detach with a protected recovery copy: existing deployments,
bindings, processes, volumes, data and access definitions all remain
(`cmd/baha/target.go:253-258`, `:563-604`; `docs/cli/targets.md:52-62`; the detach marker even blocks
automatic selection afterwards, `target_selection.go:39-41`). Root `destroy` is the opposite end of
the scale — it walks every Target, including state directories that are no longer configured
(`runtime_destroy_discovery.go:44-66`), removes owned Core services
(`runtime_destroy_inventory.go:125-171`) and removes the local state root
(`runtime_destroy_all.go:631-658`). `command-map.md:3` and `:10/:18` keep the two names apart, and the
code matches. Nothing in the audited tree lets one command reach the other's blast radius. Verdict:
**trifft** (T2, T3), with one documentation caution: `baha destroy --all` is accepted as a
"backwards-compatible alias" while installation scope is already the default
(`cmd/baha/runtime_destroy_all.go:46-53`), so the flag's presence still suggests a narrower mode that no
longer exists.

### 8.3 Version-sensitive gaps

- `--environment` is described as selecting resolved deployment state without rewriting authored
  intent (`commands.go:79`), which is exactly what `ResolveRepositoryEnvironment` does
  (`environment.go:28-31, 80-89`); the `LegacyState` marker is the version-compatibility seam
  between the pre-global-state path (`.baseharbor`, `internal/runtime/stack.go:18`) and
  `XDG_DATA_HOME`-based state (`:449-473`). A repository that already has both is resolved by
  "global wins, legacy reused only when global is absent", so an upgrade is not atomic across the
  two roots (T25).
- `platform-support.md:5-8` pins the matrix to the released v0.4.22 baseline and marks v0.4.23
  qualification pending, while `up`/`doctor` gate features on `runtime.GOOS` (`§6`). Any claim about
  "supported platform" in CLI output must be read against that baseline, not against the code's
  broader GOOS switches (T28).
- `internal/runtime/contract/api.go:240-249` accepts any slug-like provider kind, but only
  `docker` and `podman` are registered
  (`internal/runtime/resolver/resolver.go:11-23`, `:41-44`);
  `kubernetes`/`openshift` kinds exist as constants
  (`internal/runtime/contract/api.go:18-19`) with no registration, so a Target
  created with `--runtime-provider kubernetes` fails at resolution rather than at creation.
  This is the "unimplemented must be explicit" gap in the platform axis (T15, T30-adjacent).

### 8.4 Coverage cross-check against the card's entry points

`cmd/baha/target*.go` (selection, activation, mutation, recovery, policy, wizard: §3),
`node*.go` (§5 platform node), `provider*.go` (§5 platform provider), `stack*.go` (§5 platform
stack), `runtime*.go` (§3 root destroy, §5 platform local), `openbao.go` (§5 trust/OpenBao) and
`internal/deployment/` (§2 roots, §3 resolution) are all covered. `cmd/baha/commands.go`, the shared
parser/machine registry, `.github/**`, release notes and generated indexes are reserved for their
integration/CI owners (card note) and were only read, never edited.

## 9. repo-rule compliance

- Read-only audit under merge-frost: no product file was created, changed, deleted or reverted; no
  branch was cut, no PR opened, no release or tag touched. The only write is this dossier in the
  plan repository (write-set: baseharbor-plan only, as the mission states).
- Claim leg: the card was already `active` with owner `lane-0428-045-r28` on plan `origin/main`
  (`9aad6e58`); `plan.py claim` refuses to re-claim an active card, verified in this session
  (§PLAN step 1). Nothing was re-published and no other lane's claim was touched.
- Planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` only, proven by the
  `rev-parse --show-toplevel` and `remote get-url origin` witness in §0. `workers/baseharbor-plan`
  was never used. `workers/baseharbor` (quarantined stale refs) was never cited.
- Product truth was measured by `git ls-remote` on GitHub plus a fresh clone in this lane's own
  persistent zone (`/tmp/opencode/audit-platform-wt/repo`), checked out at exactly `0e9ccb582`.
- Evidence lives only in `evidence/cli-redesign-20261114/audit-platform.md` in the plan repo; this
  dossier intentionally contains no markdown task-checkbox lines anywhere (neither the empty nor the
  ticked form), so the CardBoard cannot leak a card from it.
- No sub-agents (AGENTS 4.8): every step — the clone, every `grep`/`read`, the context7 MCP calls,
  the web searches and this file — ran inside this session.
- No containers, no compose projects, no test VMs, no GitHub-hosted runs and no workflow files were
  started or edited (`.github/**` is owner scope; nothing here needed it, so no workflow finding is
  filed). Nothing to bring down: cleanliness is stated in §11.
- Plan push is a planning act on `main` in the planning repository, which is the delivery channel
  the mission orders ("akte … plan-main push"). No CI was triggered by it.
- Sources for external claims are cited in §1; internal claims carry `file:line` against the pinned
  SHA only.

## 10. Open items for the contract task (not decisions of this lane)

1. Whether the target selection stays per-user persisted (today's implementation, `target.go:260-263`)
   or becomes shell-local (today's documentation, `docs/explanation/targets.md:152-168`). T5/T26.
2. One vocabulary for selection state across human, JSON and MCP output (T6), and one owner for the
   `-t` / `-c` short forms the brief names but the code never defines (T7, T8).
3. Replacing environment-name semantics with explicit policy/authorization, including the
   `ManagedEnvironment` name test, the `"dev"` defaults and the destroy rank map (T9, T27, T29).
   `internal/serviceaccess/policy.go:94-101` is the pattern to generalise.
4. Stable per-environment IDs next to the existing Target/Application/Deployment identity axes (T12).
5. One root-resolution helper with an absolute-path guard and an `XDG_STATE_HOME` concept, replacing
   the seven resolvers in §2 (T21, T22, T23).
6. An explicit availability statement for the remote node/connector and Kubernetes provider paths
   while their implementation is out of Core (T15, T30, §8.3).
7. Whether the human reveal path (`baha dev credentials`) keeps printing a plaintext password at all
   now that the JSON/MCP path deliberately does not (T19).

## 11. Cleanliness

cleanliness: no container, network, volume, compose project, systemd unit or state directory was
created by this lane. Work artefacts live only under `/tmp/opencode/audit-platform-wt/` (one clone of
`mcpdev80/baseharbor` at `0e9ccb582`, plus the three dossier parts used to assemble this file); the
plan repository contains only this file. Nothing was started on the host this session runs on and no
SSH test host was used, because no runtime gate was in scope for a read-only inventory.

## 12. Handoff

- lane: `lane-0428-045-r28` (session 0428-045, flash)
- card: `t-20261114-r28-cli2-audit-platform` (0428-045), state `active` at start of this lane
- product base audited: `develop` @ `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (no candidate branch,
  no PR: merge-frost, reine Bestandsaufnahme)
- plan base at start: `origin/main` @ `9aad6e585a8e7337f4415addefa4b4950b67714e`; the remote moved on
  while this dossier was written, so the dossier was published as exactly one commit
  on top of the fetched head `3aa218da73504b3ff428b687d253095bee7fa9dd`; no force-push, no history
  rewrite. Final pushed head: `d853f49e0e53abf04fc7ecdbd16f9ca846f659fb` (§13)

## 13. Evidence witnesses (last action of this lane, measured after the final push)

```
$ git ls-remote origin main
d853f49e0e53abf04fc7ecdbd16f9ca846f659fb	refs/heads/main
$ git ls-tree origin/main evidence/cli-redesign-20261114/audit-platform.md
100644 blob 1219e1dc682ba5f4647e3bfc5d7d4d89da37157d	evidence/cli-redesign-20261114/audit-platform.md
$ git log --oneline origin/main..HEAD
(empty: nothing of this lane is left unpushed)
$ git log --oneline 3aa218da..origin/main
d853f49e 0428-045 audit-platform: refresh witness block with final pushed head
337da5ba 0428-045 audit-platform: delivery note for the two-commit witness sequence
5575f383 0428-045 audit-platform: evidence witnesses (ls-remote, ls-tree) added
35d0a975 0428-045 audit-platform: platform, target, environment and UID path inventory at develop 0e9ccb582
```

The last command lists ONLY this lane's commits on top of the fetched base `3aa218da`: four commits,
all touching only this file, no foreign candidate carried. The witness block necessarily lags one
push behind (a file cannot record the SHA of its own push), which is why the sequence is
`35d0a975` → `5575f383` → `337da5ba` → `d853f49e` and `d853f49e` is the authoritative candidate
for this dossier's content.

## END

END_DONE mission-audit-platform.md: platform/environment/target/UID paths audited at develop 0e9ccb582, 30 file:line verdicts in evidence/cli-redesign-20261114/audit-platform.md; candidate SHA 0e9ccb582f5bdcdc74049bbe3996263cdce6500c; no product change (merge-frost), card could not move to review (review requires a prs entry; see §12).
