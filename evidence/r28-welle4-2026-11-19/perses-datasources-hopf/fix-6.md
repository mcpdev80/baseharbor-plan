# 0428-083 perses datasources — fix-6 (x-083r3, correction round on PR #1684)

Lane: x-083r3 · card t-20261114-r28-perses-datasources (0428-083)
PR: https://github.com/mcpdev80/baseharbor/pull/1684
Branch: lane-0428-083-datasources-r2 (only candidate)

## PLAN

1. Reality check: remotes, PR #1684 head, review dossier, card acceptance lines — done
2. Findings F1-F4 read and reproduced against head 738ed514b — done (file:line below)
3. Timeline probe on local docker (SIGHUP, GlobalSecret ca variant, SSRF connect-time guard) — done
4. F1: unify datasource-root derivation on the runtime-dir sibling; seams take (manifest, runtimeDir, namespace) — done
5. F2: provisioned endpoint = gateway service https://prometheus + compose extra_hosts host-gateway mapping — done
6. F3: trust anchor rides a provisioned GlobalSecret (caFile + serverName, public material); proxy.spec.secret is a NAME string; allowlisted trust dir — done
7. F4/reload: SIGHUP removed (kills the container); enable_watch IS the reload; live-API existence + proxy-health verify with bounded wait — done
8. Tests: lifecycle seams, goldens, runtime tests, container cell consumes materialized output — done
9. Container acceptance green on baha-docker — done (PASS, see witness)
10. Gate routing: coverage-catalog ownership declared for the datasource files — done
11. Hopf: merge --no-ff origin/develop (6e87ddcb), content-resolved, gate-plan before/after compared — done
12. One exact-head pull_request run watched to terminal — see "CI run" below
13. Evidence + END — this file

## F1 — datasource root: two layout formulas (independent review finding)

Repro: the lifecycle seam derived the root as `<deploymentRoot>/applications/<resourceProject>/providers/management-ui/perses`
(two-argument formula) while the compose render derived its mounts from the runtime projection dir;
for the local store layout (no namespace) the two disagree, so a provisioned datasource is mounted
from a path the writer never wrote.
File:line (before): internal/application/perses_runtime.go `datasourceLifecycleRoots(deploymentRoot, resourceProject)`;
internal/metrics/perses_datasource_lifecycle.go `datasourceLifecycleRoots` + `persesDatasourceProjectionRootForRuntime`;
internal/application/runtime_postgres.go `datasourceDeploymentRoot/files.ResourceProject` call site.
Fix: ONE application-side formula `PersesDatasourceRuntimeRoot(runtimeDir)` (the providers/management-ui/perses
sibling of RuntimeFiles.Dir); every seam signature is now `(manifest, runtimeDir, namespace)`; the
manifest-bound metrics entry derives through the same function. Removed: datasourceDeploymentRoot,
datasourceDeploymentBinding, the second metrics-side sibling formula.
Test: TestPersesDatasourceLifecycleMountsResolveFromMaterializer,
TestPersesDatasourceLifecycleSingleRootOnBothLayouts (writer==reader on both layouts), golden updates.

## F2 — endpoint not reachable from the Perses container

Repro (measured): the app compose and the provider compose are separate projects; the "prometheus"
gateway DNS alias lives on the provider access/publish networks only, so the Perses app container
cannot route it; the host-loopback URL (https://127.0.0.1:<port>) names the container's OWN loopback.
File:line (before): internal/metrics/prometheus_render.go `ProviderEndpoint` (host form) consumed by
internal/metrics/perses_prometheus_datasource.go build.
Fix: the provisioned endpoint is `https://prometheus` (`ProviderNetworkEndpoint`/`ProviderNetworkEndpointHost`)
plus the compose `extra_hosts: "prometheus:host-gateway"` mapping on the app Perses service
(internal/application/perses_runtime.go splice into the gateway rendering — 0428-089 topology preserved);
the rendered config carries `datasource.proxy.allowed_networks: ["127.0.0.0/8","::1/128"]` because the
pinned SSRF guard checks the resolved IP at connect time (measured on v0.55.1). Build context split:
runtime (provisioned, in-network form) vs host-probe (verify path, published loopback) — see
`buildPersesPrometheusDatasourceContextual(..., buildContextRuntime|buildContextHostProbe)`.
IPv6 URLs are bracket-normalized (measured failure: `https://invalid IP:port` rejected by the loader).
Test: TestPersesPrometheusDatasourceRuntimeProvisioning (url + secret reference), goldens.

## F3 — trust anchor absent from the provisioned datasource

Repro: the materialized GlobalDatasource carried no TLS trust for the mTLS gateway; the old container
test asserted an inline tlsConfig which the pinned schema rejects (cue disjunction) — and the loader
error (measured on baha-docker) `json: cannot unmarshal object into Go value of type string` proved
`proxy.spec.secret` is a NAME string, not a SecretSelector object; any caFile reference additionally
requires `security.secret_file_allowed_directories` (measured: "file references in secrets are disabled").
File:line (before): internal/metrics/perses_prometheus_datasource_runtime.go `NewPersesGlobalDatasourceResource`
(no secret), `PersesDatasourceConfig` (no security block).
Fix: GlobalDatasource references `proxy.spec.secret: "baseharbor-prometheus-tls"`; a GlobalSecret is
provisioned beside it (`spec.tlsConfig.caFile=/etc/perses/datasource-trust/baseharbor-runtime-ca.pem`,
`serverName: prometheus`, public material only — no secret VALUE in artifacts, fail-closed teardown
covers it); the config allowlists the dedicated trust dir; the public CA bundle is projected from the
provider tree and mounted with the datasource pair.
Test: goldens (globaldatasource.json, config.yaml), TestPersesPrometheusDatasourceContainerLoadsProvisionedDatasource
negative TLS check (untrusted CA -> proxy refuses, "certificate signed by unknown authority").

## F4/timeline — SIGHUP reload kills Perses; health checked against dead/wrong target

Repro (measured, perses v0.55.1 distroless): `docker kill --signal HUP` stops the container (exit 129;
async.NewSignalListener takes SIGINT/SIGTERM only); verify then queried a host-recomputed endpoint
against a dead server. Additionally the verify path used the Prometheus endpoint instead of the
deployment's own Perses surface.
File:line (before): cmd/baha/app_apply_lifecycle.go `reloadPersesProvisioning` (`op.Run(...,"kill","-HUP","1")`);
internal/metrics/perses_prometheus_datasource.go `verifyPersesPrometheusDatasourceHealthAt` (endpoint).
Fix: provisioning config `enable_watch: true` (new in v0.55 #4136) IS the reload; the distroless image
has no shell/CLI, so no in-container nudge exists or is needed; the apply boundary then fail-closed
VERIFIES: materialized identity from the provisioning file, live existence via
`GET <perses management URL from runtime.env>/api/provisioning/globaldatasources/<name>` with a bounded
watcher-window wait, then health THROUGH the Perses datasource proxy
(`GET <proxy>/datasource/http/api/v1/query?query=up`).
Test: container acceptance proves the watcher path end-to-end (rewrite on host -> reconcile -> proxy
query answered by the fake); unit regressions on the verify chain. The acceptance cell reads the
live datasource through `/api/v1/globaldatasources/<name>` (works on the pinned build — the cell is
the live-witness for the route); the 404-on-not-loaded state drives the bounded wait.

## Gate routing (CI gate never ran on this path)

Repro: the 15 changed runtime files fell into the planner catch-alls
(`application-implementation-unresolved`, final `unknown impact`); `pr-selected-runtime-matrix.py`
derives `required = bool(supported atomic/*)` from the plan's selected gates, so the docker
observability gate skipped on every exact-head run (witnessed: job "PR · Selected Runtime" SKIPPED
while "Targeted HA · docker"/runtime cells never scheduled in runs 44631856770/44633719086).
Fix: ownership declared in scripts/pr-gate-coverage.json (the sole authority for PR runtime-gate
selection) for exactly the datasource files this card changes — the internal/application render/
lifecycle route, cmd/baha/app_apply_lifecycle.go, the metrics datasource files + testdata witnesses;
unit surfaces for the regression tests. No new gate ids, no planner-logic or workflow edits
(scripts/pr-gate-plan.py and .github/** untouched — Owner scope).
Checks: validate-pr-gate-coverage.py PASS; ci-workflow-policy.sh PASS.
Before/after gate plan (same planner, per H3 comparison):
BEFORE hopf (diff 7ee6f817..738ed514): coverage unresolved, selected [atomic/docker/observability], 15 unresolved entries.
AFTER hopf+fix (diff 6e87ddcb..d0801226): coverage unresolved (catch-alls remain for untouched sibling files - unchanged planner), selected [atomic/docker/observability], 17 unresolved entries.
Required-gates delta on THIS card's files: the coverage-catalog entry now declares the observability
pair for them (before: "No declared runtime gate owner" for all 15; after: none of the 15 in the
unowned list) — the exact-head run below shows whether the runtime cells schedule.

## Hopf (coordinator directive, develop 6e87ddcb)

H1: `git merge --no-ff origin/develop` at 78f9bd2f; two parents
`7e12a52efd0610f42765a6597a7ed5ce6c79902b 6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0`;
`git merge-base --is-ancestor origin/develop HEAD` = 0. develop commit time 2026-11-19T21:04:21+01:00.
H2: conflicts resolved by CONTENT (not side): internal/application/perses_runtime.go,
runtime_lifecycle.go, runtime_postgres.go — the 0428-089 gateway topology (writePersesGateway
ComposeServices + plan provenance) is kept as the production render; the datasource mounts and the
host mapping splice INTO the gateway rendering (fail-closed on a missing perses block/volumes list);
RuntimeComposeYAMLForProject gains the RuntimeFiles form; the context-dir form stays for seam tests.
No conflict touched scripts/pr-gate-plan.py, .github/** or scripts/test_pr_* — no STOP needed.
H3: gate-plan local comparison above.
H5: ls-remote witness inside this file (below), ancestry + parents lines in this section.

## Own-branch witness

```
$ git ls-remote origin refs/heads/lane-0428-083-datasources-r2
d0801226e8535eff63450761bb226681024c9c4c	refs/heads/lane-0428-083-datasources-r2
$ git show -s --format=%cI origin/develop
2026-11-19T21:04:21+01:00
$ git merge-base --is-ancestor origin/develop HEAD; echo $?
0
$ git log -1 --format=%P 78f9bd2f
7e12a52efd0610f42765a6597a7ed5ce6c79902b 6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0
```

## Docker container acceptance (baha-docker)

```
$ ssh baha-docker  (rootless docker 29.8.1, image persesdev/perses:v0.55.1)
=== RUN   TestPersesPrometheusDatasourceContainerLoadsProvisionedDatasource
--- PASS: TestPersesPrometheusDatasourceContainerLoadsProvisionedDatasource (13.09s)
```
The cell consumes the MATERIALIZED output (config with enable_watch + loopback range + trust-dir
allowlist, GlobalDatasource with the secret NAME, provisioned GlobalSecret, mounted bundle); the one
cell-side change rewrites the proxy URL to the container-reachable endpoint address. Negative TLS:
`tls: bad certificate` recorded — proxy refuses an untrusted anchor. Loader error witness (fixed by
this round): `cannot unmarshal object into Go value of type string` + `file references in secrets
are disabled` (pinned behavior evidence for F3).

## CI run (exact head)

(run recorded after terminal state; see END post — run 44646620311, pull_request, head d0801226e8535eff63450761bb226681024c9c4c)

## repo-rule compliance

- One candidate branch; merges INTO the lane are develop-only with two parents (78f9bd2f); no rebase/force; lane never merged anything else.
- `.github/**`, `scripts/pr-gate-plan.py`, `scripts/test_pr_*` untouched (gate routing went through scripts/pr-gate-coverage.json, the catalog file with existing same-PR validation policy — planner logic untouched).
- internal/capability/registry.go, cmd/baha/app_status_result.go untouched.
- Docker tests NOT run on this host; the container acceptance ran on baha-docker via named SSH host only. The local `go test ./...` runs skip the docker-gated cells (BASEHARBOR_PERSES_DATASOURCE_CONTAINER_ACCEPTANCE unset).
- No subagents used.
- Plan repo: own evidence file only, cloned fresh, `git add <file>`, rebase before push.
- develop moved again during this window (bbc937c8). The current head d0801226 is 0-behind? — measured: `git merge-base --is-ancestor origin/develop HEAD` returned 0 against 6e87ddcb (the hopf target in the directive); develop later advanced to bbc937c8 — recorded here, next hopf belongs to the coordinator's directive window.
- cmd/baha known host-dependent test failures (TestRuntimeUpRequiresORASBeforeCoreBootstrap, TestPrepareStagedCoreGitCandidatePinsCanonicalApplication, TestAppEditCommandCompleteProviderEditRunsRealLifecycle, guided-fixture timeouts) reproduce IDENTICALLY on the plain develop control worktree 6e87ddcb — environment (ORAS/runtime presence), not this diff.
- Language: product/functional wording; English technical terms kept.

## cleanliness

Before: local host had probe containers from the timeline probe (removed earlier); baha-docker had
probe containers baha-perses-ds-* and cell leftovers.
After: `docker ps -aq --filter name=baha-perses-ds` on both hosts: empty; cell network removed;
`baha-perses-ds-*` count 0 on baha-docker and this host; ambient bh-local-shared-* (foreign cores)
untouched.
cleanliness: clean — no lane-owned containers, networks, volumes or state dirs remain on this host or baha-docker.
