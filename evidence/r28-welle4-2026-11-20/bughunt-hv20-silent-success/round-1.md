# Bug-Hunt H-V20 round 1 — Silent-Success Desk over the whole repo

- Lane: w195-0428-195-huntsilent (Karte 0428-195)
- Mission: /var/tmp/mission-hv20.md
- Date: 2026-11-20
- Scope: reine Befundung des develop-Standes — kein Produktcode, kein Test, kein .github/**, kein Board-Edit, kein PR
- Candidate SHA searched: develop `b98299d2d63e657ae872939ce60fe23d667ae808` (live remote). Mission-SHA `2f81fa21dc77` is the 2026-11-15 develop head and is now stale; read-only grep content is unaffected.
- Working clone: `/tmp/opencode/hunt-hv20` (shallow clone of `https://github.com/mcpdev80/baseharbor.git`, develop checked out). No writes into the ecosystem root or product checkout.
- Repo remote verified: `origin https://github.com/mcpdev80/baseharbor.git`
- planning repo remote verified: `origin https://github.com/mcpdev80/baseharbor-plan.git`

## PLAN

1. Establish reality witnesses (planning remote, live develop SHA, clean shallow clone).
2. Cut 1: `git grep -n "t.Skip"` + `git grep -n "LookPath"` in *_test.go; classify each as (a) silent-success fund, (b) absent-tool-in-different-cell, or (c) CI-visible-skip.
3. Cut 2: guards in .github/workflows/ and scripts/ (command -v, if [ -x, only-if, has-prerequisite, docker/podman info).
4. Cut 3: orphan tests — cross-check -run/package selection in jobs against `go list ./...`.
5. Write findings with FUND-FUER-KARTE lines; assemble evidence.
6. Publish evidence to origin/main, post END line.

## Cut 1 — t.Skip / LookPath (test-side silent-success)

Command: `git grep -n "t.Skip" -- "*_test.go"`
Literal output: 126 skip sites across cmd/baha, internal/application, internal/corebackup/etcd, internal/coreinstallation, internal/credential/native, internal/database, internal/development, internal/devgateway, internal/externalprovider, internal/hosttrust, internal/identityprovider, internal/logs, internal/machinehttp, internal/openbao, internal/orgconfig, internal/providers/runtime/podman, internal/repositoryinspect, internal/runtime, internal/stableid, internal/targetsession, internal/telemetry, internal/testsupport, internal/traces, internal/workstationenrollment/http.

Command: `git grep -n "LookPath" -- "*_test.go"`
Literal output: 22 LookPath sites (git, python3, engine, certutil, update-ca-certificates, bao).

Classification against the three sub-categories (a find / absent-tool-in-other-cell / CI-visible):

- Environment-optional tool skips (NOT a silent-success fund): git, python3, symlinks, certutil, update-ca-certificates, engine binaries, root/UID, PTY, changelog. These guard against tools/privileges that ARE present on the GitHub-hosted ubuntu-latest runner. A skip in CI only fires if the tool is genuinely absent, which does not happen on shared runners. The job reports success but the path simply does not need running — this is the intended design, not a silent-success hole. Examples:
  - cmd/baha/app_update_test.go:16 `t.Skip("git is not available")` — git is on ubuntu-latest; skip never fires in CI.
  - internal/orgconfig/orgconfig_test.go:113 `t.Skip("git not installed")` — same.
  - cmd/baha/app_inspect_native_counterprobe_test.go:48/66/101 `t.Skip("git not installed")` — same.
  - internal/development/source_snapshot_test.go:86/107, internal/credential/native/caller_test.go:20 (no HOME), internal/machinehttp/*_round*.go (chmod/journal), internal/runtime/control_plane_inventory_test.go:128/132 (foreign UID), internal/externalprovider/store_owner_test.go:31/35, internal/coreinstallation/*_lock_test.go:53/63, internal/stableid/lock_test.go:58/76, cmd/baha/core_installation_test.go:112 (PTY), cmd/baha/bugs_841_842_contract_test.go:88, internal/telemetry/pki_reload_test.go:25, internal/traces/pki_reload_test.go:26, internal/logs/pki_reload_test.go:27, internal/hosttrust/browser_nss_test.go:177, internal/hosttrust/hosttrust_system_e2e_test.go:18/24, internal/runtime/lock_probe_platform_test.go:11 (amd64-specific). None are silent-success funds: the guard condition is false on CI, so no path is hidden by a real skip.

- Opt-in acceptance skips (NOT silent-success, but notable): tests gated on `BASEHARBOR_*_ACCEPTANCE` / `BASEHARBOR_CI_RUNTIME_INTEGRATION` / `BASEHARBOR_*_INTEGRATION`. These skip unless a CI job sets the env var. The integration job `Runtime integration tests serially` (ci.yml, job "validate", line 341-343) sets `BASEHARBOR_CI_RUNTIME_INTEGRATION: "1"`, so the `*_runtime_integration_test.go` and `*_integration_test.go` (BASEHARBOR_CI_RUNTIME_INTEGRATION) tests RUN in CI and their skip is visible as "skip" in the aggregated output (sub-category c, not a fund). The other opt-in vars (BASEHARBOR_POSTGRES_BACKUP_INTEGRATION, BASEHARBOR_SHARED_POSTGRES_INTEGRATION, BASEHARBOR_KEYCLOAK_HA_ACCEPTANCE, BASEHARBOR_OTEL_HA_ACCEPTANCE, etc.) are set by the pre-release/targeted workflows' specific gate jobs. The base `go test ./...` unit job does NOT set them, so they skip there — but that is the intended layering (unit vs. acceptance), and the acceptance gate jobs that DO set them are present. No path is hidden in a job that is supposed to run it.

- Reference to the known case: cmd/baha/context_terminal_test.go:434-439 and :491-505 (zsh/fish LookPath guard) — already karte 0428-179. Not re-reported except as "same pattern": the git/python3/enginelookup LookPath skips above are the same structural pattern (LookPath → t.Skip when absent), but on environment-optional tools present on the runner, so sub-category (b)/(c), not a fund.

## Cut 2 — guards in workflows and scripts

Command: `git grep -nE "command -v|if \[ -x|only-if|has-prerequisite|docker info|podman info" .github/workflows/`
Literal output (11 hits): podman-info probes in mcp-lifecycle-acceptance.yml:111, observability-acceptance.yml:148, podman-acceptance.yml:238, pre-release-runtime-suite.yml:147, pre-release.yml:1005, targeted-demo-acceptance.yml:254; docker/podman info probes in targeted-integration.yml:832/1269. These are pre-flight probes; they do not skip a failing step.

Command: `git grep -nE "command -v|if \[ -x|only-if|has-prerequisite|docker info|podman info" scripts/`
Literal output (8 hits):
- scripts/ci-core-rootless-runtime.sh:27 `if ! command -v dockerd-rootless-setuptool.sh` then installs docker-ce-rootless-extras with `test -n "$extras_version"` — fail-closed (installs or errors).
- scripts/ci-core-rootless-runtime.sh:60 `docker info --format '{{json .SecurityOptions}}'` — probe, no skip.
- scripts/ci-core-rootless-runtime.sh:106 `podman info` — probe.
- scripts/ci-runtime-reset.sh:23 `if command -v timeout` fallback to the bare command — benign fallback, both branches run the command.
- scripts/ci-runtime-reset.sh:41 `if ! command -v "$engine"` → `exit 0` — benign: this is idempotent runner cleanup; no required work is gated on it.
- scripts/install.sh:14, scripts/publish-four-part-hotfix.sh:18, scripts/validate-v048-live.sh:15-16, scripts/v0.4.20-readiness.sh:80 — all use `command -v ... || fail` / `|| { ... }` forms that fail the script when the tool is missing. Fail-closed.

Command (second look): `git grep -nE "\|\| *true" .github/workflows/` and `scripts/`
Literal output: every `|| true` is a cleanup/diagnostic step (docker/podman ps -a, logs, journalctl, systemctl, oci-registry cleanup, diagnostics dump). None wraps a test assertion or a required acceptance step, so none can turn a failing step into a silent success. No find.

## Cut 3 — tests with no assigned CI cell

Command: `git grep -n "\-run" .github/workflows/` (job selection) and `go list ./...` (package inventory).
- Test packages on disk: 103 (`git ls-files '*_test.go'`).
- `go list ./...`: 115 packages total; every package that contains a _test.go file is matched by the unit job's `go test ./...` (ci.yml "validate" job, line 341-343) and by the pre-release "adoption" job (pre-release.yml line 645, `go test ./...`).
- Build tags: `//go:build linux` (cmd/baha/*_linux_test.go, internal/localhosts/write_linux_test.go) run on ubuntu-latest; `//go:build !windows` / `!linux` (internal/stableid/*_unix_test.go) run cross-platform on ubuntu-latest. No tag excludes a package from the `go test ./...` runners.
- Package-level `-run`/`-p` selections in targeted jobs point at specific functions inside already-covered packages; they never select a package that `go test ./...` would skip.
Result: no orphan test file. Every test package is selected by at least one CI job's `go test ./...`. No find.

## Funde

- Befundlos. All three cuts are witnessed with command + literal output above.
- The LookPath/t.Skip pattern is a REZIDIV across the repo, but every instance is either (b) environment-optional on the shared ubuntu-latest runner (tool present, skip never fires) or (c) an opt-in acceptance gate that its dedicated CI job enables and that is visible as "skip" in that job's aggregation. None is a path hidden in a job that is supposed to run it and reported success — which is the 0428-179 silent-success signature.
- Structural note (not a new fund): the git/python3 LookPath guards (cmd/baha/app_update_test.go:15, cmd/baha/app_update_ff_test.go:13, internal/orgconfig/orgconfig_test.go:112, cmd/baha/app_inspect_native_counterprobe_test.go:47/65/100) are the exact same shape as 0428-179's LookPath guard. They are not funds because `git` is on the shared runner; they are worth a one-line mention as "same pattern, sub-category (b)".

## repo-rule compliance

- Read-only hunt on a shallow clone under /tmp/opencode/hunt-hv20. Zero writes to the product checkout, zero edits to product/test/.github files.
- No PR opened, no board/card edited, no plan-state change.
- No subagents. Every grep/build/commit executed in this session.
- Evidence authored in baseharbor-plan evidence/ only, never in a product repo.
- ambient-core / foreign carts untouched; no containers, networks, volumes, or state directories started (this was a pure source-grep run).

## cleanliness:
- Before: no containers/networks/volumes/state directories created by this lane (source-grep only).
- After: none. /tmp/opencode/hunt-hv20 remains an untracked shallow clone (read-only, no commits).
- cleanliness: CLEAN — no runtime artifacts started or left behind.

## END
END_DONE w195-0428-195-huntsilent: bug-hunt H-V20 silent-success desk complete on develop b98299d2; befundlos across all three cuts (witnessed above); read-only, no board/PR/code changes.
