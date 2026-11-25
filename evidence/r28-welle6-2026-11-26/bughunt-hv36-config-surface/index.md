# Bug-Hunt slice H-V36: config/flag surface consistency

Pure finding. No product changes. Read-only analysis of the config/flag surface at the
exact develop anchor.

## Task
BaseHarbor BUG-HUNT SLICE H-V36: examine config/flag surface consistency on the CURRENT
develop tip - cobra flag definitions vs docs/reference/cli.md vs --help output ordering;
env var read sites vs docs (godot names actually referenced); defaults drift between
cmd/baha wiring and internal/ constructors. Read-only akte with per-row file:line
findings + proposed card lines.

## Anchor
- git ls-remote origin refs/heads/develop -> a87da7d179e08d43e8987885c38ab459ff1d887d
- Fresh blobless clone at workers/.models/ornith; checked out a87da7d179e08d43e8987885c38ab459ff1d887d (clean working tree, zero local commits).
- Base attestation: a87da7d179e08d43e8987885c38ab459ff1d887d is the checked-out HEAD.
- Remote guard: clone origin URL https://github.com/mcpdev80/baseharbor.git (verified via git remote -v).

## Method
- Built /tmp/baha-v36 from ./cmd/baha (go1.26.8, build clean).
- Captured --help output for root + subcommands and compared flag ordering, enums, usage strings.
- Extracted Usage strings vs parsed switch-case flags (cmd/baha/*.go, non-test) with /tmp/hv36_drift.py; remaining "missing" tokens are non-switch-parsed flags (--agents prefix, --cert-file/--key-file/--file prefix checks), not drift.
- Cross-checked env var read sites (os.Getenv) against docs/how-to/operator-api.md and docs/reference.

## Findings (per-row file:line)
1. config/flag surface is internally consistent at this anchor. No drift detected across the three axes.
2. --help flag ordering matches command-index.md and the Usage: string in every sampled command.
   - config prompt: docs/cli/command-index.md:94 == /tmp/baha-v36 config prompt --help (order + enums identical).
   - app env: --format dotenv|shell|json|yaml matches cmd/baha/app_env.go:21 and parseAppEnvArgs (app_env.go:50-64).
   - app new: --stack go|nextjs|python|quarkus matches cmd/baha/app_new.go:36; stacks validated via developmentAdapterID (app_new.go:285-307, registry-resolved).
   - app init capability flags order matches app new capability flags order (both --sql|--sql-instance ... --secrets|--require-secret).
3. --workload-source enum: compose|quadlet|kubernetes matches internal/repositoryinspect/workload_source.go:19-21 (WorkloadSourceCompose/Quadlet/Kubernetes).
4. --target global flag: both --target NAME and --target=NAME parsed (cmd/baha/main.go extractGlobalOutputOptions), verified live (status reports target-not-configured).
5. env var read sites vs docs: operator-api.md:10-70 env names (BASEHARBOR_RUNTIME_APP_NAME, BASEHARBOR_RUNTIME_EXECUTOR_MODE, BASEHARBOR_RUNTIME_OPERATIONS_DIR, BASEHARBOR_API_* match cmd/baha/serve.go:28-55 and :145-188). BASEHARBOR_RUNTIME_ENVIRONMENT read in serve.go:176, referenced in compose_render.go:165.
6. defaults: input TLS mode default "local" is set once in cmd/baha/app_input_resolver.go:327 (ClassDefault) and consumed consistently; no cmd/baha-vs-internal constructor drift observed in sampled paths.
7. Global options order (quiet/silent/verbose/plain/no-color/no-input/version) is stable across all commands (internal/cli/cli.go renderHelp).

## Proposed card lines (for coordinator triage)
- Card A (cosmetic, low value): the config/flag surface is currently consistent; a regression guard (golden --help snapshot in CI) would catch future drift. Requires .github/** change (Owner scope) -> report file:line, do not edit.
- No blocking drift card required at this anchor.

## Cleanliness
- No containers/compose started; read-only hunt. No docker/podman activity on host.
- Worktree /tmp/opencode/w167-0428-224-hunt-v36-wt (blobless clone at a87da7d).
- Build artifact /tmp/baha-v36 (temporary).
- gh clean: no orphans.

## END
w167-0428-224-hunt-v36 DONE - find count 0 (surface clean), 1 proposed guard card for coordinator.
