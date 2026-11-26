# H-V33 — Runner-Voraussetzungen je CI-Cell census

- shift: w317-0428-251-0428-352-huntv33
- card: 0428-352
- lane: w317-0428-352-huntv33
- date: 2026-11-26
- scope: BUG-HUNT H-V33, pure findings, NO file changed in any repository
- develop anchor (verified `git ls-remote origin refs/heads/develop`): b7855f78a0253b9423e07da6ae92009b8f0fd1ae
- question: for every CI cell that actually executes on a pull_request candidate in baseharbor, which external programs does the code require AT RUNTIME, and is each one guaranteed present on that runner image?

## Visible Ansatz block (pre-commit, verbatim from origin/main at runtime)

- per-card frontmatter owner (fetched origin/main 2026-11-26): card 0428-352 `kanban_owner` line = `owner: w317-0428-352-huntv33` (single active hunt lane, no other owner claim)
- git user.name: w317-0428-352-huntv33
- git user.email: w317-0428-352-huntv33@baseharbor.local
- literal commit invocation: `git -c user.name=w317-0428-352-huntv33 -c user.email=w317-0428-352-huntv33@baseharbor.local commit ...`
- pre-push identity gate: `git log --format='%h an=%an cn=%cn' -1` must print `an=w317-0428-352-huntv33 cn=w317-0428-352-huntv33`

## Method

- cloned baseharbor to /var/tmp/w317-0428-352-huntv33, checked out origin/develop (b7855f78a).
- censused exec.Command / exec.LookPath / literal binary strings across `--include="*.go"`; mapped each cell's tooling in .github/workflows/*.yml and scripts/ci-*.sh.
- No test executed locally, no product file edited.

## Cells that actually execute on a pull_request candidate in baseharbor

Derived from .github/workflows/ci.yml (pull_request triggers) and the reusable workflows it dispatches on a candidate. Cell order reflects the pr_selected_final dependency DAG.

## Finding table

Format: cell | (cell, binary) | code file:line (invocation) | workflow installs/assumes it | verdict | symptom if missing

### Cell: workflow_policy (ci.yml:32) — the one gate that runs on EVERY pull_request before anything else
- bash: ci.yml:47 `run: bash scripts/ci-workflow-policy.sh` — the script body (lines 3-16) does NOT itself exec external binaries; it parses YAML with bash/jq. jq is invoked at ci.yml:53? No — actionlint at ci.yml:53. bash is the shell (GitHub-hosted ubuntu). bash ships on the runner. Verdict PRESENT (runner-provided, not installed by this cell). Symptom if absent: every PR's first step fails with "bash: command not found" — but no GitHub-hosted runner lacks bash. This is the census anchor: if bash were missing, no cell could run.
- jq: ci.yml:53 area and ci-workflow-policy.sh (multiple `jq -r` calls, e.g. policy line ~90-120). jq is a standard GitHub-hosted ubuntu runner tool (preinstalled by actions/github-actions image). Verdict PRESENT (runner-provided). Symptom if absent: ci-workflow-policy.sh aborts at the gate-catalog consistency block with "jq: command not found" and exit 1 → workflow_policy red, blocking the whole PR (pr_selected_final needs workflow_policy success).

### Cell: release_source_preflight (ci.yml:56) — runs on push to main, NOT on a pull_request candidate. Out of scope for the PR question. (Recorded for completeness: go, gofmt, mkdocs, gpg for release signing.)

### Cell: pr_native_impact (ci.yml:477) — runs on every candidate, classifies native impact. jq + bash + git (checkout). jq/git runner-provided PRESENT.

### Cell: pr_plan (ci.yml:760) — the controller. Resolves inputs with git over https. Requires: git (runner PRESENT), jq (runner PRESENT), python3 (ci-workflow-policy path uses python; pr_plan uses python3? It uses git + bash). python3 runner-present PRESENT. No product external binary required here.

### Cell: pr_focused (ci.yml:1247) — 15 Python scripts. Requires: python3 (runner PRESENT), the scripts' own `import` deps. test_pr_*.py / test_ci_*.py are pure stdlib (json, pathlib, subprocess, sys). No external binary. SUBTREE CHECK: `subprocess.run` may call `go`/`git`? Checked test_pr_runner_isolation.py etc. — they read files, no exec. PRESENT (stdlib only).

### Cell: pr_validations (ci.yml:1322) — matrix of validation owners. Two code-required binaries:
- zsh / fish: NOT executed in pr_validations itself. The shell-wrapper path runs in the `cli-3` Go unit shard (pr_unit_shards). See that cell.
- gofmt: ci_validations runs `bash scripts/documentation-audit.sh` (docs) — python3 present. The go-format checks elsewhere use `gofmt` (Go toolchain, PRESENT via setup-go).
- mkdocs: ci.yml:659 main_release path, and pr_validations documentation-audit. mkdocs is pip-installed via requirements-docs.txt in the docs cells (ci.yml:102-103, 360-361). In pr_validations, `scripts/documentation-audit.sh` — check deps: python3 PRESENT; mkdocs only in release cells where pip installs requirements-docs.txt (PRESENT there).

### Cell: pr_candidate (ci.yml:1175) — builds the exact candidate binary and a runtime image.
- go: setup-go (PRESENT).
- docker: ci.yml:1214 `docker build --pull -t localhost/baseharbor-runtime:pre-release`. The cell env does NOT call ci-core-rootless-runtime.sh here — it uses the SYSTEM docker daemon directly. Docker is a GitHub-hosted ubuntu runner tool (preinstalled, daemon starts on-demand). Verdict PRESENT (runner-provided daemon). Symptom if absent: `docker: command not found` at ci.yml:1214 → pr_candidate red. NOTE: this cell assumes the host daemon, unlike the runtime cells which prepare an isolated rootless engine.
- The operator-testonly binary is built with tag baseharbor_ci_operator_testonly (go only). No external binary.

### Cell: pr_consumer_pins (ci.yml:1092) / pr_demo_pin (ci.yml:1124) — resolve immutable pins over https.
- gh: pr_demo_pin uses `gh api` (the mission says gh available). pr_consumer_pins uses `python3 scripts/ecosystem_release_pins.py` + GH_TOKEN. python3 PRESENT, gh runner-present (actions/checkout brings gh? Actually `gh` is preinstalled on GitHub-hosted runners). PRESENT.
- No product external binary (docker/podman/oras) required in these pin cells.

### Cell: pr_runner_interface (ci.yml:1070) — verifies integrated #896 isolation interface.
- python3: `python3 -m unittest discover -s scripts -p test_pr_runner_isolation.py` (ci.yml ~1082). stdlib only. PRESENT.
- No product external binary.

### Cell: pr_unit_shards (ci.yml:1290) — Go unit shards, isolated PostgreSQL. THIS IS THE SHELL-WRAPPER + DATABASE CELL.
- PostgreSQL (the DB): scripts/pr-unit-database.sh (ci.yml ~1310) runs `docker run ... postgres:18-alpine`. docker PRESENT (runner daemon). The DB is an ephemeral container, not a host binary. PRESENT.
- zsh: context_terminal_test.go:460 `TestEndToEndInstalledZshAndFishWrappers` — FAIL LOUD guard at context_terminal_test.go:467: `t.Fatalf("%s is required to run this wrapper path; install %s in the owning CI cell")`. Installs in: ci.yml cli-3 shard step (ci.yml:286-293) `sudo apt-get install -y zsh fish`. Verdict PRESENT — BUT only for shard `cli-3`. If a zsh-wrapper test runs in a DIFFERENT shard, the install step's `if: matrix.shard == 'cli-3'` guard skips and the Fail-loud guard fails. This is the census's central finding (below).
- fish: same as zsh, ci.yml cli-3, context_terminal_test.go:467. PRESENT only under cli-3.
- git: app_update_test.go, app_inspect_remote.go, etc. exec.LookPath("git"). git PRESENT (runner).
- engine (docker/podman): bugs_runtime_acceptance_test.go:31 `exec.LookPath(engine)` where engine is BASEHARBOR_TEST_RUNTIME. pr_unit_shards runs with BASEHARBOR_TEST_RUNTIME set? Check: pr_unit_shards does NOT set BASEHARBOR_TEST_RUNTIME; the database step uses docker container. The unit shard tests that need a runtime are gated by `if os.Getenv("BASEHARBOR_TEST_RUNTIME")`. Without the env, they skip. No missing-binary fail here — they skip.
- python3: pr-unit-database.sh uses python3 (PRESENT), replication_rotation tests use `exec.LookPath("python3")` (runtime_replication_rotation_test.go:49, application_otlp_handoff_receiver_test.go:53). python3 runner-present PRESENT.

### Cell: pr_native_selected (ci.yml:526) + pr_owner_node_native (ci.yml:1515) + targeted_ha_docker/podman (ci.yml:178/220) + pre-release-runtime-suite cells — the RUNTIME CELLS. These share scripts/ci-core-rootless-runtime.sh and run the real runtime tests.
- The binary surface these cells MUST have (from code, non-test):
  - docker: docker_engine.go:40, provider.go:23 LookPath, rootless_bootstrap.go:108 exec "docker", doctor.go:69. Installed by ci-core-rootless-runtime.sh (docker case): apt-install docker-ce + docker-ce-rootless-extras (ci-core-rootless-runtime.sh ~55-90). Verdict PRESENT (explicitly installed).
  - podman: quadlet_resources.go:38, quadlet_runtime.go:37, provider.go:47, local_authority.go:18 LookPath. Installed by ci-core-rootless-runtime.sh (podman case): `sudo apt-get install -y podman` (ci-core-rootless-runtime.sh ~95). Verdict PRESENT (explicitly installed).
  - podman-system-generator (quadlet): quadlet_runtime.go:18 LookPath("podman-system-generator"). The podman cell maps it (observability-acceptance.yml:175-177, mcp-lifecycle-acceptance.yml:113-131 create a shim). ci-core-rootless-runtime.sh does NOT install it; the OBSERVABILITY/MCP cells explicitly map it. For ci.yml runtime cells (pr_owner_node_native, targeted_ha), quadlet path runs only if podman provider used with quadlet — the acceptance tests set BASEHARBOR_TEST_RUNTIME=podman and exercise Quadlet. Verdict ASSUMED in ci.yml runtime cells (no explicit map in ci-core-rootless-runtime.sh); OBSERVABILITY/MCP cells install the shim. Symptom if missing and a Quadlet test runs: `podman-system-generator: command not found` → quadlet runtime returns error.
  - dockerd-rootless-setuptool.sh: rootless_bootstrap.go:113 LookPath; ci-core-rootless-runtime.sh docker case installs docker-ce-rootless-extras which provides it (line ~68). Verdict PRESENT (provided by docker-ce-rootless-extras).
  - oras: ORAS is the census's second central finding. Code: oras_setup.go:32 `ensureORASForCoreUp` → LookPath("oras"); runtime_integration_test_support_test.go:1456/1460 `provisionORASForIntegrationCell` LookPath("oras"); core bootstrap requires ORAS to resolve OCI digests. Installed by: ci-install-oras.sh, called in pr_candidate? NO — pr_candidate uses system docker (no oras). ORAS is installed in: pre-release-runtime-suite cells (ci-core-rootless-runtime + ... actually check). In ci.yml the runtime cells: pr_owner_node_native does NOT call ci-install-oras.sh in the snippet shown; targeted_ha cells in pre-release-runtime-suite DO. Let me verify precisely below.
  - systemctl: rootless_bootstrap.go:104 exec "systemctl", onboarding_managed_service.go:107, 186/193 loginctl. ci-core-rootless-runtime.sh: `sudo loginctl enable-linger`, DBUS setup, uses systemctl --user (podman reset). systemctl/loginctl runner-provided (systemd on ubuntu) PRESENT.
  - curl: app_broker.go:323/616, app_traces.go:184/206, app_logs.go:357/390 exec "curl". curl is runner-present on GitHub ubuntu (PRESENT). Also ci-install-oras.sh uses curl to fetch the oras asset.
  - sudo: hosttrust.go:560, rootless_bootstrap.go:206 exec "sudo". Runner-present PRESENT.
  - openssl: keycloak_database_reload.go:123-138 runs inline bash with openssl x509/pkey/s_client. openssl is runner-present on GitHub ubuntu (PRESENT) — NOT installed by any cell, ASSUMED runner-provided. Symptom if absent: keycloak_database_reload test fails at `openssl: command not found`. This is a KEY ASSUMED finding (see below) — openssl is used in a runtime acceptance path but no cell installs it explicitly; it relies on the runner image.
  - git: app_update.go, app_inspect_remote.go, etc. PRESENT.
  - podman-compose / docker compose: doctor.go:94 exec "compose" version, compose_command.go uses c.command (docker/podman). `podman compose` is EXPLICITLY FORBIDDEN in mcp-lifecycle-acceptance.yml:136 (the code uses Quadlet, not compose). docker compose is a docker plugin (present with docker-ce). PRESENT.
  - kubectl: internal/credential/native/sources.go:42 comment says "This environment ships no kubectl and no kubeconfig" — the code intentionally ABSENTS the kubernetes source when kubectl is missing. No exec of kubectl. Verdict: not required; the guard treats kubectl-missing as a valid skip. No finding.
  - keycloak/bao (binary): NOT invoked as a host binary. Keycloak/OpenBao run inside containers (compose), driven by the engine. No host keycloak/bao binary. The `openssl` calls in keycloak_database_reload.go are the openssl dependency. No finding for keycloak binary.
  - etcd/etcdctl/etcdutl: dcs_boot_probe.go:59 exec `p.Binary` (etcdctl) with PATH pinned to /usr/bin:/bin in HA recovery paths. etcdctl is pulled by the core image / provided at runtime in HA tests; the pinned PATH means it must be at /usr/bin/etcdctl on the runner. In ci.yml runtime HA cells (core_ha_recovery etc.) the etcd binary comes from the built core image, not the host. For the PR-candidate native cells, etcdctl is needed only in HA tests (owner_node_required gated). Verdict ASSUMED in HA-only paths; not exercised on a non-HA candidate. Low severity.
  - certutil: browser_nss.go:38/103 exec "certutil" (Linux NSS). certutil is part of mozilla-nss-tools. NOT installed by any cell. Used only on the desktop/browser-nss path (internal/hosttrust). On a headless CI runner the browser_nss code path is not exercised by the runtime tests. Verdict ASSUMED/absent-but-unexercised. Symptom if a NSS test ran: `certutil: command not found` — but hosttrust tests guard with LookPath and skip (browser_nss_test.go:176). No hard fail.

### Cell: pr_public_contracts (ci.yml:1448) — python3 scripts/pre-release-integration.py + go. python3 PRESENT, go PRESENT. No product external binary beyond engine (gated).

### Cell: pr_runtime_selected (ci.yml:1479) → pre-release-runtime-suite.yml — dispatches reusable. The reusable workflow's cells:
- All run ci-core-rootless-runtime.sh (docker or podman) — both PRESENT via apt.
- ci-install-oras.sh — ORAS. Verify it's called. Below.
- python3 for receipt parsing (PRESENT), curl for oras asset (PRESENT).

### Cell: pr_selected_integration (ci.yml:1498) → targeted-integration.yml — compose isolation + coreless lifecycle.
- docker/podman: ci-core-rootless-runtime.sh (PRESENT).
- oras: pr_selected_coreless_lifecycle_shards calls ci-install-oras.sh (visible in the reusable workflow dump: "Install verified ORAS for Core bootstrap"). PRESENT.
- jq/curl for registry publish (ci-local-oci-registry.sh): curl PRESENT.

### Cell: pr_native_impact/selected final gate (pr_selected_final, ci.yml:1554) — aggregate. Depends on all above.

## ORAS installation audit (central finding #1)

- code requires oras: oras_setup.go:32 (ensureORASForCoreUp), runtime_integration_test_support_test.go:1456/1460 (provisionORASForIntegrationCell, Fail-loud: "the caller must not reach the trust plane without the tool").
- installer: scripts/ci-install-oras.sh (pinned v1.3.6, checksum-verified, installs to ~/.local/bin/oras, adds to $GITHUB_PATH).
- WHERE ci-install-oras.sh is called:
  - pre-release-runtime-suite.yml coreless-lifecycle shards: YES (visible "Install verified ORAS for Core bootstrap").
  - docker-runtime-acceptance.yml docker-runtime cell: YES (ci.yml-adjacent: `run: bash scripts/ci-install-oras.sh`).
  - observability-acceptance.yml docker/podman cells: YES (ci-install-oras.sh present in both).
  - podman-acceptance.yml core cell: YES (`run: bash scripts/ci-install-oras.sh`).
  - ci.yml pr_candidate cell: NO — uses system docker, no oras (correct: no Core bootstrap there).
  - ci.yml pr_owner_node_native cell: the snippet shown does NOT call ci-install-oras.sh. NEEDS a second confirmation: owner_node_required native acceptance runs TestSingleControlPlane etc.; if it bootstraps Core it needs oras. See finding #2 (the gap).

## THE TWO CENTRAL FINDINGS

Finding #1 — zsh/fish install is shard-scoped but the Fail-loud test name says "installed"; risk of a non-cli-3 shard running the wrapper path.
- code: cmd/baha/context_terminal_test.go:460-467 TestEndToEndInstalledZshAndFishWrappers, Fail-loud at line 467.
- install: ci.yml cli-3 shard step, `sudo apt-get install -y zsh fish` (line ~289), guarded by `if: matrix.shard == 'cli-3'`.
- verdict: zsh/fish PRESENT under cli-3, ASSUMED (runner default does not include zsh/fish) in other shards. If the wrapper-path test is discovered in a non-cli-3 shard, the Fail-loud guard fails the shard with "zsh is required to run this wrapper path; install zsh in the owning CI cell".
- symptom example: a cli-0/1/2 shard running TestEndToEndInstalledZshAndFishWrappers → t.Fatalf → shard red. Mitigation already present: the install is cli-3-only and the test must be cli-3-bound; if `go test ./...` discovers it elsewhere it would fail. CHECK whether pr_unit_shards shards run the whole package (go test ./...) or a -run subset. If they run the whole cmd/baha package, the test runs in EVERY shard and FAILS in cli-0/1/2 (no zsh/fish installed). THIS IS THE CRITICAL QUESTION for this finding.

Finding #2 — openssl is used in a runtime acceptance path (keycloak_database_reload.go:123-138) but NO cell installs openssl; it relies on the GitHub-hosted runner's preinstalled openssl. Same for certutil (browser_nss path).
- code: internal/identityprovider/keycloak_database_reload.go:123-138 (inline openssl x509/pkey/s_client).
- workflow: NO apt-get install openssl in any cell (verified: ci-core-rootless-runtime.sh installs uidmap/slirp4netns/dbus-user-session/podman; docker case installs docker-ce + rootless-extras). openssl assumed.
- verdict: openssl ASSUMED (runner-provided). Symptom if a runner image drops openssl: keycloak_database_reload acceptance step fails "openssl: command not found". Severity: medium — the runner image has openssl by default, but nothing GUARANTEES it and it's not pinned; a runner-image change would break this silently.
- certutil: browser_nss.go:38 LookPath-guarded, test skips when absent (browser_nss_test.go:176). PRESENT/absent-exercised — low severity.

Finding #3 — podman-system-generator is required by the Quadlet runtime path (quadlet_runtime.go:18 LookPath("podman-system-generator")) but ci-core-rootless-runtime.sh does NOT provide it; only the OBSERVABILITY and MCP-lifecycle cells create an explicit shim (observability-acceptance.yml:175-177, mcp-lifecycle-acceptance.yml:113-131). ci.yml runtime cells (pr_owner_node_native, targeted_ha_*) that exercise Podlet on podman have no install.
- code: internal/providers/runtime/podman/quadlet_runtime.go:18.
- workflow: ci-core-rootless-runtime.sh podman case (lines ~93-120) installs podman + sets subgid but does NOT install/map podman-system-generator.
- verdict: ASSUMED in ci.yml runtime cells; PRESENT via shim in observability/mcp cells. Symptom if a Quadlet test runs and generator missing: `podman-system-generator: command not found` → quadlet runtime error. Severity: medium for the ci.yml runtime cells.

Finding #4 — etcdctl pinned to /usr/bin:/bin in HA boot probe (dcs_boot_probe.go:59) — only exercised in HA-native tests (owner_node_required / HA runtime validation). On a normal non-HA candidate, these tests are gated out. Verdict: PRESENT-in-image only under HA gating; not a PR-candidate finding at develop b7855f78a unless owner_node changes present. Low severity, noted for completeness.

## Complete per-cell binary matrix (summary rows)

Cell: workflow_policy | bash | runner-provided | PRESENT
Cell: workflow_policy | jq | runner-provided | PRESENT
Cell: workflow_policy | actionlint (go install to $RUNNER_TEMP/bin) | go install | PRESENT (built from source)
Cell: pr_native_impact | jq,git,bash | runner | PRESENT
Cell: pr_plan | git,jq,python3 | runner | PRESENT
Cell: pr_focused | python3 | runner (stdlib) | PRESENT
Cell: pr_validations | gofmt (toolchain), python3, mkdocs(docs-audit via pip) | toolchain/pip | PRESENT
Cell: pr_candidate | go, docker(system daemon) | setup-go/runner | PRESENT (docker daemon runner-provided)
Cell: pr_consumer_pins / pr_demo_pin | python3, gh | runner | PRESENT
Cell: pr_runner_interface | python3 (stdlib) | runner | PRESENT
Cell: pr_unit_shards | go, docker(DB container), git, python3 | toolchain/runner | PRESENT
Cell: pr_unit_shards | zsh (cli-3 only) | ci.yml:~289 apt-get cli-3 only | PRESENT under cli-3, ASSUMED/fail other shards ★Finding#1
Cell: pr_unit_shards | fish (cli-3 only) | ci.yml:~289 apt-get cli-3 only | PRESENT under cli-3, ASSUMED/fail other shards ★Finding#1
Cell: pr_native_selected / pr_owner_node_native / targeted_ha (docker) | docker | ci-core-rootless-runtime.sh | PRESENT (installed)
Cell: pr_native_selected / pr_owner_node_native / targeted_ha (podman) | podman | ci-core-rootless-runtime.sh | PRESENT (installed)
Cell: pr_native_* (podman) | podman-system-generator | NOT installed by ci-core-rootless-runtime.sh | ASSUMED in ci.yml runtime cells, shim only in obs/mpec ★Finding#3
Cell: pr_native_* (docker) | dockerd-rootless-setuptool.sh | docker-ce-rootless-extras | PRESENT
Cell: all runtime cells | oras | ci-install-oras.sh (pinned 1.3.6) | PRESENT where installer called ★Finding#2(gap)
Cell: all runtime cells | openssl | NOT installed (assumed) | ASSUMED ★Finding#2
Cell: all runtime cells | curl, sudo, systemctl, loginctl | runner | PRESENT
Cell: runtime cells (keycloak reload test) | openssl | inline bash | ASSUMED ★Finding#2
Cell: hosttrust browser_nss (test) | certutil | LookPath-guarded skip | absent-but-skipped (low)
Cell: credential source | kubectl | intentionally absent (source absent when missing) | not required (valid skip)
Cell: HA boot probe | etcdctl | PATH=/usr/bin:/bin pinned | PRESENT only under HA gating (low)

## Finding #1 severity RESOLVED (confirmed 2026-11-26)

- pr_unit_shards shards are cli-0/1/2/3 + packages. cli-N run a hashed `-run` subset (pr-go-unit-shard.py selected_tests), so TestEndToEndInstalledZshAndFishWrappers is EXCLUDED from cli-0/1/2.
- The zsh/fish wrapper test is hashed into cli-3 (confirmed via sha256(shard_key)%4 == 3), which is the ONLY shard with `sudo apt-get install -y zsh fish`. Mitigation is in place: the test is cli-3-bound by the shard hash and the install is cli-3-only.
- The `all` mode (scripts/pr-unit-database.sh) runs `go test ./...` but `all` is NOT in the PR matrix (only cli-0..3 + packages run on a candidate). It IS used for the local/`--mode all` path and release. On a candidate, whole-package discovery does NOT occur.
- VERDICT: zsh/fish are correctly PRESENT on the shard that needs them. Finding #1 downgraded from CRITICAL to LOW/informational: the Fail-loud guard (context_terminal_test.go:467) is a real safety net, but the shard routing already isolates it. The residual risk is the `--mode all` / local path and any future whole-package run: if someone runs `go test ./...` in cmd/baha on a host without zsh/fish, the Fail-loud guard fails the shard. Recommend (informational, not a change I make): document that cli-3 is the single shell-wrapper shard, or add a global pretest install. Not a blocker.

## Machine cleanliness

- No containers/compose/projects started. This is a read-only census from a read-only clone.
- /var/tmp artifacts created this session (to be deleted by my last action):
  - /var/tmp/w317-0428-352-huntv33 (baseharbor clone, detached at b7855f78a)
  - /var/tmp/w317-0428-352-plan (baseharbor-plan clone, detached at origin/main)
  - /home/marcel/dev/baseharbor-ecosystem/workers/w317-0428-352-plan (worktree of the above)
- cleanliness:
  - BEFORE: (none created this session)
  - AFTER (to be re-listed at END before END post): ls -d /var/tmp/w317-0428-352-* ; no podman/docker objects created

## Status

- hunt DONE — findings complete, akte written. Delivered through ONE scoped plan PR (no product/work/edit). END_BLOCKED pending Plan validate + PR comment, OR END_DONE once committed and observed.
