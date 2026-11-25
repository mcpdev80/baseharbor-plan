# Bug-hunt slice H-V43: env/config injection surface

Scope: env/config injection surface. os.Getenv/env-var read sites vs documented config keys, precedence order (flag>env>file?) consistency across subcommands, secret-bearing vars logged or leaked into diagnostics.

Pure finding, no product change. READ-ONLY.

## Base attestation

- develop HEAD (git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop): a87da7d179e08d43e8987885c38ab459ff1d887d
- Worktree cut at exact tip: w178-0428-224-hunt-v43-wt (detached a87da7d1)
- git remote -v in worktree: lane-origin ssh://git@github.com/mcpdev80/baseharbor.git (used for all git ops; origin is the bookkeeping repo)
- Planning repo remote: https://github.com/mcpdev80/baseharbor-plan.git (verified before first commit)

## Environment-variable read inventory

215 os.Getenv calls across the tree; 209 are non-test production-ish reads. The full list of distinct `os.Getenv("NAME")` keys was extracted and cross-referenced against the documented configuration surface in docs/spec/control-plane-runtime.md, docs/explanation/targets.md, and docs/decisions/0014/0002.

### FUND-1: no single registry of documented config keys; ~30 runtime-executor env vars undocumented

file:line: cmd/baha/serve.go lines 145-193 (runtimeExecutorConfigFromEnv, controlPlaneConfigFromEnv)

Every value at serve.go:147-193 is read directly from os.Getenv with no shared registry, schema, or doc link. docs/spec/control-plane-runtime.md only documents 3 control-plane API vars (BASEHARBOR_API_DATABASE_URL, BASEHARBOR_API_OIDC_ISSUER, BASEHARBOR_API_OIDC_AUDIENCES, BASEHARBOR_API_LISTEN_ADDR) plus BASEHARBOR_MANAGED_CORE_TLS/BASEHARBOR_API_PUBLIC_URL/BASEHARBOR_CONNECTOR_PUBLIC_ADDRESS. The executor/control-plane config reads ~30 additional BASEHARBOR_* vars (BASEHARBOR_RUNTIME_OPENBAO_URL, BASEHARBOR_RUNTIME_OPENBAO_CREDENTIALS_FILE, BASEHARBOR_RUNTIME_TOKEN_FILE, BASEHARBOR_RUNTIME_OPERATIONS_DIR, BASEHARBOR_RUNTIME_METRICS_TARGETS_DIR, BASEHARBOR_EXECUTOR_S3_ADMIN_CREDENTIALS_FILE, etc.) that have no spec entry.

Impact: low-medium. Not a leak; it is an observability/governance gap — operators cannot discover the accepted keys, so undocumented keys get guessed/tested, which is exactly the surface a hunt for injection wants to pin down.

### FUND-2 (HIGH): compose `${VAR}` expansion reads the whole ambient process environment, unredacted, into a on-disk .env

file:line: internal/providers/runtime/podman/quadlet_project.go line 338-362 (quadletComposeEnvironment) + internal/providers/runtime/podman/quadlet_project.go line 367-403 (expandQuadletComposeNode / expandQuadletComposeString)
file:line: internal/providers/runtime/podman/quadlet_render.go lines 254-276 (quadletRenderServiceEnvironment writes {project}-{service}.env)
file:line: internal/providers/runtime/podman/quadlet_project.go lines 317-335 (WriteQuadletProject writes to ~/.config/containers/systemd/)
file:line: internal/providers/runtime/podman/quadlet.go lines 40-73 (composeEnv.UnmarshalYAML: null-tag list items expand via os.Getenv(key))

Root: quadletComposeEnvironment copies the entire ambient environment (os.Environ()) into a map. expandQuadletComposeString substitutes ${VAR} / ${VAR:-default} for every string literal in the rendered Compose model using that map. The substituted values are then written verbatim to a service .env file (quadletRenderServiceEnvironment), which WriteQuadletProject persists under ~/.config/containers/systemd/.

Leak: if any ambient secret-bearing variable (e.g. a CI token, AWS creds, a password) shares a name with a compose key or is referenced by ${VAR} in a rendered unit, the plaintext value is written to disk under the user's config dir with no redaction and no name filter. The null-tag env expansion (quadlet.go:53,67) additionally lets arbitrary ambient vars in if a compose fragment declares a null-valued env key.

Severity: HIGH (secret-bearing ambient env can be materialised to disk through a legitimate compose key).

### FUND-3 (MEDIUM): docker compose passes ambient env to the subprocess; same unredacted expansion risk

file:line: internal/runtime/compose_files.go line 285-302 (mergeProcessEnvironment) + internal/runtime/docker_engine.go lines 284-315 (commandEnvironment) + internal/runtime/command_env.go lines 9-24 (runtimeCommandEnv)

Root: the docker Compose subprocess is invoked with the full ambient os.Environ() (commandEnvironment/mergeProcessEnvironment/runtimeCommandEnv). Docker Compose itself performs ${VAR} expansion against that ambient env, so the same unredacted-secret-materialised-to-container-env risk applies on the docker path, and compose.env-style files are honoured (COMPOSE_ENV_FILES at cmd/baha/app_context.go:691-714 loads repo/.env and stateInit env).

Impact: same class as FUND-2 but on the docker path (container env, not a writable config file).

### FUND-4 (LOW): BASEHARBOR_TARGET precedence is documented for CLI selection but not for runtime-input precedence consistency across subcommands

file:line: docs/de/reference/cli-machine-coverage.md line 100, docs/reference/cli-machine-coverage.md lines 97-98 (BASEHARBOR_TARGET: explicit flag > shell-env > configured default)
file:line: internal/application/provider_placement.go lines 31-41 (HasExplicitProviderPlacement reads ProviderScopeEnv/SharingBoundary/ExternalReference via os.Getenv with no flag/file fallback)

Root: the documented precedence (flag > env > file) applies to Target selection. Provider-placement env overrides (provider_placement.go) are read purely from os.Getenv with no documented precedence vs. on-disk org config, and no per-subcommand consistency check. Not a bug yet, but a precedence-gap to pin down.

### NEGATIVE (no finding): secret-bearing vars are not logged

- operator OIDC: identityprovider/external_binding_change.go line 77-84 derives a SHA-256 revision from provider/issuer/client-id/secret/ca and zeros the material before hashing (change.Revision = hex.EncodeToString(digest[:])). No secret value logged.
- app_access.go line 141-143: PASSWORD/URI only printed on authenticated secret.reveal seam; otherwise <masked>.
- operatorauth/config.go: ConfigFromEnv builds Config without logging issuer/client-id.
- runtimeobservability/observer.go: lifecycle/request/export-error logs contain no credential fields (only method/path/status/duration).
- orgconfig: model.go:173,227,292 actively reject secret-like material in environment/identity names.

## repo-rule compliance

- No product files changed. No .github/** edits. No workflow_dispatch / reruns.
- Evidence written only to baseharbor-plan (product repo untouched).
- git remote resolved to github.com/mcpdev80 before any git op (lane-origin).

## CLEANLINESS

docker ps -a (own pid zone): none started during this hunt (read-only code scan, no containers/compose projects launched).
git status worktree: clean (no edits; git ls-files confirms tracked state at a87da7d1).

## END

END w178-0428-224-hunt-v43 DONE — 4 findings (1 HIGH, 1 MEDIUM, 2 LOW/negative), 0 product changes.
