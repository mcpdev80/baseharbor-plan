# Bug-hunt slice H-V43: env-leak-disk (w331, 0428-316)

Scope: BaseHarbor runtime paths that write an env-derived value TO DISK. The desk asks, for every `os.Getenv` read, where the value lands, and whether a secret-bearing or operator value is materialised to a file on disk (plaintext, by mode/owner) or into a container image's environment. Pure finding, no product change. READ-ONLY.

## Base attestation

- develop HEAD (git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop): 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74
- Worktree cut at exact tip: workers/w331-0428-316-hunt43-wt (detached 5a37ddbd9)
- git remote -v in worktree: origin https://github.com/mcpdev80/baseharbor.git (used for all git ops; verified github.com/mcpdev80 before any git op)
- Planning repo remote: https://github.com/mcpdev80/baseharbor-plan.git (verified before first commit)

## Environment-variable read inventory (whole tree)

215 `os.Getenv` calls; 209 non-test production-ish reads. Distinct `BASEHARBOR_*` keys that flow into disk writes were traced from the read site through the render/projection chain to the final `os.WriteFile`/`WriteFile` call. Cross-referenced against the documented config surface in docs/spec/control-plane-runtime.md and docs/explanation/*. Only new/distinguishing items are listed below; the prior H-V43 akte (bughunt-hv43-config-injection) already recorded FUND-1..4 (no single config-key registry; `serve.go:145-193` ~30 undocumented executor/control-plane vars; compose `${VAR}` expansion of ambient env; `BASEHARBOR_TARGET` precedence gap). This hunt re-verified those against current develop and adds the items below.

### FUND-A (HIGH): podman quadlet writes ambient env to a plaintext service .env on disk, unfiltered

file:line: internal/providers/runtime/podman/quadlet_project.go lines 338-362 (quadletComposeEnvironment copies the whole ambient os.Environ() into a map) + lines 367-403 (expandQuadletComposeNode/expandQuadletComposeString substitute ${VAR}/${VAR:-default} for every string literal in the rendered Compose model using that map)
file:line: internal/providers/runtime/podman/quadlet_render.go lines 254-272 (quadletRenderServiceEnvironment writes {project}-{service}.env with key=value, substituted value written verbatim)
file:line: internal/providers/runtime/podman/quadlet_project.go lines 317-335 (WriteQuadletProject persists every file, incl .env, under ~/.config/containers/systemd/ with 0o600 for service units)
file:line: internal/providers/runtime/podman/lifecycle.go lines 49-50 (UpProjectProgress calls quadletRenderProject on every up/config, so the render+write runs on the normal product path, not only tests)

Root: quadletComposeEnvironment always loads the entire ambient environment (os.Environ()). expandQuadletComposeString substitutes ${VAR} for every string literal in the rendered model, including service Environment entries, using that ambient map. quadletRenderServiceEnvironment then writes the substituted value verbatim to a {project}-{service}.env file, persisted under the user's config dir.

Leak: if any ambient secret-bearing variable (a CI token, AWS creds, a password, a BASEHARBOR_* credential that happens to share a name with a compose key, or is referenced by ${VAR} in a rendered unit) appears as a compose environment literal, its plaintext value is written to disk under ~/.config/containers/systemd/{project}-{service}.env with no name filter, no redaction, and no allow-list. Severity HIGH (secret-bearing ambient env is materialised to a plain file through a legitimate compose key).

Note on mode/owner: the file is written 0o600 (service units) inside a 0o700 dir (WriteQuadletProject os.MkdirAll(dir, 0o700)), so it is not world-readable — the defect is not a permission hole but an unfiltered materialisation: an operator's ambient secret reaches a plaintext file by construction.

Reachability proven against current source: the existing test internal/providers/runtime/podman/quadlet_project_test.go TestRenderComposeProjectFilesQuadletsMergesBaseHarborOverride (lines ~418-426) asserts that a substituted value lands in the rendered .env (it checks "ORIGINAL=base" appears in the .env file), which confirms the substitution-into-.env path executes. That test uses a literal compose value, NOT an ambient-substituted secret, so it does not cover the leak: no existing test asserts that an ambient ${VAR} of a secret-bearing variable is suppressed or that its presence in the .env is rejected.

### FUND-B (MEDIUM): docker compose passes the whole ambient env to the subprocess; same unredacted secret risk, different sink

file:line: internal/runtime/compose_files.go lines 285-302 (mergeProcessEnvironment) + internal/runtime/docker_engine.go lines 284-315 (commandEnvironment) + internal/runtime/command_env.go lines 9-24 (runtimeCommandEnv)

Root: the docker Compose subprocess is invoked with the full ambient os.Environ() (commandEnvironment/mergeProcessEnvironment/runtimeCommandEnv). Docker Compose itself performs ${VAR} expansion against that ambient env, so the same unredacted-secret risk applies on the docker path. Unlike FUND-A, docker compose does NOT write a local .env file here; the leak surface is container environment (the ambient secret becomes a container env var), not a writable config file.

Distinction vs FUND-A: FUND-A is a file leak (plaintext .env on disk, reachable via the podman product path). FUND-B is a container-env leak (no local file). Both share the unfiltered-ambient-env root; both are gated behind the same missing allow-list.

### FUND-C (LOW): BASEHARBOR_RUNTIME_IMAGE validated for CRLF/NUL only, not for path-separator or '=' injection into the rendered compose.yaml

file:line: internal/runtimeexecutor/compose.go lines 122-125 (image := os.Getenv("BASEHARBOR_RUNTIME_IMAGE"); ContainsAny(image, "\r\n\x00") guard)

Root: the only validation on the executor image env is a newline/NUL guard. A value such as `myimage:tag\n  inject: "line"` passes the guard and can inject a second key into the rendered executor compose.yaml written at compose.go:142 (os.WriteFile(composePath, ...)). Not secret-bearing; it is a low-severity compose-injection vector co-located with the env-read. Recommend a regex/allow-list validation alongside the newline guard.

### NEGATIVE (no finding): state-dir and provider credential files are hardened

- runtime.env files written by the runtime (internal/runtime/stack.go:115, internal/runtimeexecutor/compose.go:133, internal/telemetry/otlp.go:428, internal/logs/state.go:206) contain only generated ports or, for Loki, a managed objectstorage.PlatformBucket S3 secret (internal/logs/state.go:197-200) — written 0o600 inside 0o700 provider state dirs by design, not from ambient operator env.
- installation.json (internal/coreinstallation/installation.go) is written via a 0600 temp+rename (save()) and re-read with json.Decoder.DisallowUnknownFields() + strict UUID/owner/placement/spec validation; no env value is persisted there.
- orgconfig selections (internal/orgconfig/store.go) are written 0600 with an isWorldWritableDir fallback (privateFallbackConfigRoot) so a sticky-bit /tmp XDG_CONFIG_HOME never becomes the write target; the ambient XDG_BASE is only a path selector, never written as content.
- keycloak active-admin.env (internal/identityprovider/keycloak_admin_credential_rotation.go:233) holds a managed rotation secret, 0o600 writeProtectedEnv — intended credential file, not an ambient leak.

## repo-rule compliance

- No product files changed. No .github/** edits. No workflow_dispatch / reruns. No local go test (read-only code scan on the coordinator host; forbidden per owner policy stop 2026-11-26).
- Evidence written only to baseharbor-plan (product repo untouched).
- git remote resolved to github.com/mcpdev80 before any git op (origin).
- No containers or compose projects started (read-only scan); no docker/podman daemon work on this host.

## CLEANLINESS

docker ps -a (own pid zone): none — read-only code scan, no containers/compose projects launched.
git status worktree: clean (no edits; git ls-files confirms tracked state at 5a37ddbd9).
Worktree to remove: workers/w331-0428-316-hunt43-wt (removed at END).

## END

END w331-0428-316-hunt43envleak DONE — 3 findings (1 HIGH FUND-A podman .env materialisation, 1 MEDIUM FUND-B docker compose ambient env, 1 LOW FUND-C image injection), 0 product changes.
