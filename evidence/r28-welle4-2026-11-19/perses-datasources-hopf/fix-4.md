# 0428-083 fix-4 — runtime call site, mounts, container acceptance (mission-083-runtime-call-site.md)

Lane: `lane-0428-083-datasources-r2` · PR #1684 · mission tag `083-runtime-call-site`

Final head: `24cd5f4538fa8f9bc814fcd481143484742c3a14`
CI chain: `24cdb6e38…` (run 44567714956, success) → `2a112434a2b915ef38109caec06ef824c577169f`
(run 44570550143, failure = flaky `TestAdmissionBodyCompletesBeforeLifecycleWhileProgressRemainsObservable`
in internal/machinehttp, a package this PR never touches) → final `24cd5f4538fa8f9bc814fcd481143484742c3a14`
(run 44573407736, **success**, terminal; recorded below).

## Monotonicity / ancestry witnesses

- develop at final hopf: `c296086ca1e35ef3212d293afc94d7bebcd1690f` ([0428-086] Perses Loki datasource
  adapter, #1616). `git merge-base --is-ancestor c296086c HEAD` → OK (merge commit `24cd5f45`, no
  rebase, no force). Intermediate hopfs onto `859654861` and `1019190d` are merge commits in the chain.
- previous documented head `a9befb3127b26a8a0f622bcf686fb6bcbb9b9e6e`: `git merge-base --is-ancestor a9befb31 HEAD` → OK.
- `git merge-tree --write-tree origin/develop HEAD` → `99e851c834ff76bfec1ec297c78390912231d7da`,
  0 conflicted objects (clean tree).
- `git log --oneline origin/develop..HEAD` shows only this lane's own chain
  (2a112434, 24cdb6e3, b276977d, 3d0d551b, 683062f3, 7fc929b0, a9befb31, f0adef10, a4a9efee, ab693229, 8c713950).

## The gap and the grep chain

Before (mission step 2, on head a9befb31 / every earlier head):

    $ grep -rn "MaterializePersesPrometheusDatasourceAt" internal/ | grep internal/application/
    (empty)

The materializer existed but nothing at the apply boundary called it — that was the verdict's
"runtime consumer and mounts absent".

After (head 2a112434): the lifecycle calls it through the seam (internal/metrics imports
internal/application, so a direct edge back would be an import cycle; registration closes it):

- call site: `internal/application/runtime_postgres.go:140` → `ensurePersesDatasourceRuntime`
  (defined at `runtime_postgres.go:371`), inside `EnsureRuntime` BEFORE the compose render and
  the Perses start.
- seam registration: `internal/metrics/perses_datasource_lifecycle.go:71`
  (`RegisterPersesDatasourceMaterializer(materializePersesDatasourceForLifecycle)` from package init;
  `go list -deps ./cmd/baha | grep internal/metrics` confirms metrics is always in the CLI dependency
  graph, so the seam is installed in every baha binary).
- mount resolver seam: `internal/metrics/perses_datasource_lifecycle.go:108`
  (`persesDatasourceLifecycleMounts`), deselection remover + artifacts cleaner registered from init.
- `MaterializePersesPrometheusDatasourceAt` itself is invoked from the seam path
  `materializePersesDatasourceWithProject` → `BuildPersesPrometheusDatasourceAt` with the
  DEPLOYMENT root + namespace + resource project; no second path constant exists anywhere on the route.
- verify side: `CheckManagedRuntimeDefinition` renders through `RuntimeComposeYAMLForContextDir`
  (context dir) so verify compares against the written files; the Perses verify check fails closed
  ("not configured") for a selected-but-unprovisioned surface (`management_ui.go`, `datasourceProvisioned`).

## Mounts (mission part 2)

`internal/application/perses_runtime.go:99` resolves the pair through the registered resolver and
renders them only when artifacts are present (fail-closed — never mounts of missing paths):

    - ../providers/management-ui/perses/config.yaml:/etc/perses/config.yaml:ro
    - ../providers/management-ui/perses/provisioning:/etc/perses/provisioning:ro

Targets are the constants `PersesDatasourceContainerConfigPath` / `PersesDatasourceContainerProvisioningPath`
(one source of truth, shared with the materialized config's `provisioning.folders`). The container test
mounts byte-identical sources (absolute host paths of the SAME materializer output, same `:ro` targets).

## Container runtime acceptance (mission part 3)

Test: `TestPersesPrometheusDatasourceContainerLoadsProvisionedDatasource`
(`internal/metrics/perses_prometheus_datasource_container_test.go`, docker-gated by
`BASEHARBOR_PERSES_DATASOURCE_CONTAINER_ACCEPTANCE=1`).

Local exact-tree results (host docker daemon, pinned `docker.io/persesdev/perses:v0.55.1` =
`application.PersesUIImage`):

    BASEHARBOR_PERSES_DATASOURCE_CONTAINER_ACCEPTANCE=1 go test ./internal/metrics \
      -run TestPersesPrometheusDatasourceContainerLoadsProvisionedDatasource -count=1
    ok  github.com/mcpdev80/baseharbor/internal/metrics  9.8s   (on 24cdb6e3)
    ok  github.com/mcpdev80/baseharbor/internal/metrics  13.3s  (on 2a112434)
    ok  github.com/mcpdev80/baseharbor/internal/metrics  12.1s  (on final head 24cd5f45)

It proves, against the RUNNING pinned image started with exactly the two materializer mounts:
1. LOADED — `GET /api/v1/globaldatasources/baseharbor-prometheus` returns the provisioned
   GlobalDatasource (kind asserted).
2. QUERY/PROXY — `POST /proxy/globaldatasources/baseharbor-prometheus/api/v1/query` round-trips
   through TLS to the fake Prometheus and the fake records the proxied `up` query.
3. TLS fail-closed — replacing the GlobalSecret trust anchor (`spec.tlsConfig.ca`) with an
   unrelated CA makes the proxy refuse with "certificate signed by unknown authority" while the
   datasource itself stays loaded.

Perses v0.55 facts the cell encodes (measured against the pinned image + perses/spec cue schemas):
- proxy TLS trust rides `proxy.spec.secret` → a `GlobalSecret` with `spec.tlsConfig.ca`; an inline
  `tlsConfig` in the datasource spec fails the cue disjunction ("field not allowed").
- the datasource-proxy SSRF guard denies loopback by default; it is reopened ONLY inside the test
  cell's config (`datasource.proxy.allowed_networks: ["127.0.0.0/8"]`). The production deployment
  never needs this (provider and Perses share the compose network there).
- the plugin archive extraction into `/etc/perses/plugins` works without extra mounts.

Additional product hardening this round (self-review of the materializer): re-materialization now
clears stale regular files from the provisioning folder before writing (the loader loads EVERY file,
so a leftover datasource of a previous generation under a different endpoint could otherwise load
beside the current one). Regression: `TestPersesDatasourceLifecycleRematerializeClearsStaleResource`
(commit `2a112434`).

## CI (exact-head, §4.6)

- Run `44567714956` (head `24cdb6e3`, pull_request): completed, conclusion **success**.
  `candidate_advisory_required = "false"`, `runtime_required = "false"`.
- Run `44570550143` (head `2a112434`): completed, conclusion failure — the ONLY failing cells were
  `PR · Go unit · packages` and the aggregate. Cause: `internal/machinehttp`
  `TestAdmissionBodyCompletesBeforeLifecycleWhileProgressRemainsObservable` flake ("admission blocked
  behind lifecycle: … context deadline exceeded", 2s client timeout under CI runner load). This PR
  touches nothing in internal/machine* (verified via `git diff --name-only` and `gh pr diff 1684
  --name-only`); the identical run succeeded one commit earlier and on the final head. Local
  reproduction: the test passes in isolation (0.01s) and the whole package passes 3× locally (33s).
  Not a product defect of this card; reporting as an observation only.
- Run `44573407736` (head `24cd5f45`, the FINAL head): completed, conclusion **success**.
  Executed cells: Workflow policy, PR · Native gate plan, PR · Trusted Plan, PR · Source format,
  PR · Validation · go-vet, PR · Validation · go-build, PR · Focused Python, PR · Go unit ·
  packages/cli-0/cli-1/cli-2/cli-3, and **PR Selected Checks = success (the aggregate)**.
  Inputs visible in the aggregate step: `candidate_advisory_required: "false"` and
  `runtime_required: "false"`; `PR · Candidate-added checks (advisory)` accordingly skipped.
  No required validation for this diff's coverage fell out of the required plan beyond the
  runtime-gate mapping finding below.

### Finding (owner-scope, NOT edited): 'PR · Selected Runtime' skip condition

The mission demands the runtime cell actually EXECUTE in CI; if the gate stays skipped, report the
skip condition. On base `85965486`/`1019190d` the skip chain is:

- `.github/workflows/ci.yml:973` — the `PR · Selected Runtime` job runs only when
  `needs.pr_plan.outputs.runtime_required == 'true'`.
- `.github/workflows/ci.yml:851-852` — `runtime_required` is the `required` flag of
  `scripts/pr-selected-runtime-matrix.py` over the pr_plan output.
- `scripts/pr-selected-runtime-matrix.py` line ~14/22-25 — `required` is true only when the plan's
  `selected_gates` contain a `*/runtime/gate` entry.
- `scripts/pr-gate-plan.py` (~795-810 + the WIZARD_COMPONENTS/exact-path maps): this PR's changed
  paths (`internal/application/runtime_postgres.go`, `management_ui.go`, `perses_runtime.go`,
  `runtime_lifecycle.go`, `internal/metrics/perses_*`, `cmd/baha/app_apply_lifecycle.go`) land in
  "unknown impact"/"needs targeted qualification" (no narrow mapping → `coverage_status:
  unresolved`, `broad_required: true`) — so Go-unit/vet/build execute as the conservative selection
  but NO native runtime gate is mapped, and `PR · Selected Runtime` is skipped. Observed values in
  run 44567714956: `runtime_required: "false"`, `candidate_advisory_required: "false"`.
  A runtime-gate mapping for Perses datasource paths is owner scope (scripts/**).

Host witness precedent (088-r3): the container acceptance ran to PASS on this session host with
observed output above; the cell is CI-executable via the opt-in env once a gate mapping exists.

## Focused checks (mission step 3, on final tree)

- `go test ./internal/metrics ./internal/application -run Perses -count=1` → ok / ok
- `go build ./...` → ok; `go vet ./internal/metrics ./internal/application ./cmd/baha` → clean
- `gofmt -l internal cmd` → clean
- `bash scripts/source-readability-audit.sh` → PASS (file size, function span, regression ratchet)
- container acceptance as above. No full `./...` run (per mission).

## PLAN

1. §4.1 real-state check: fetch --prune, task note, PR state, develop head from ls-remote — done
2. gap proof (grep chain before): internal/application empty — done (see above)
3. part 1 apply-boundary call site via cycle-free seams + registration from metrics init — done
4. part 2 read-only compose mounts from the materializer path formula, fail-closed — done
5. part 3 docker-gated container acceptance: LOADED + proxy query + TLS fail-closed — done (green locally)
6. stale-generation hardening + regression test — done (2a112434)
7. focused checks (unit Perses, build, vet, gofmt, readability) — done
8. hopf onto 859654861 and 1019190d as merge commits — done
9. push with ancestor witness on a9befb31 — done (a9befb31..2a112434 fast-forward push)
10. exact-head CI watch to terminal + finding for the runtime-gate skip — done
11. evidence fix-4.md in /var/tmp/plan-083-clone, push origin/main, END post — done last

## repo-rule compliance

- No `.github/**` or `scripts/**` edits (the runtime-gate mapping gap is reported as a finding with
  file:line instead). No subagents (§4.8). One lane, one PR (#1684), draft=false unchanged.
- No merge, no `gh pr ready`, no force-push; hopfs are merge commits only, ancestry preserved
  (witnesses above). Forbidden files untouched: `internal/machine/contract.go`,
  `internal/metrics/perses_contract_test.go`, `internal/observability/environment.go`,
  `internal/logs/render.go`, `internal/telemetry/otlp_payload.go`,
  `internal/metrics/perses_dashboards_hosts.go`, 077/121 territory.
- Secret protection: the acceptance writes only PUBLIC CA material into the GlobalSecret resource
  (trust anchor), never a secret value; no credentials logged.
- Fail-closed contract preserved end to end (deselect → teardown; build error → projection removed;
  missing artifacts → no mounts; unprovisioned selected surface → verify error).
- Plan/evidence-only writes live in this clone (`/var/tmp/plan-083-clone`), never in the product repo,
  never in the shared plan copy.

## Handoff

- Final candidate head `24cd5f4538fa8f9bc814fcd481143484742c3a14` on
  `refs/heads/lane-0428-083-datasources-r2`, PR #1684 open (non-draft), base develop@c296086c monotone.
- Run `44573407736` (exact final head): **success**, terminal (all required cells + PR Selected Checks
  aggregate). The intermediate failure (run 44570550143) was the internal/machinehttp flake documented
  in the CI section — no lane change caused it beyond the hopf push.
- Luna review should re-check: the seam design (atomic.Pointer registrations in
  internal/application/perses_runtime.go + runtime_postgres.go, init in perses_datasource_lifecycle.go),
  the mounts being resolver-derived (no constant duplication), and the container cell's opt-in gate
  until an owner runtime-gate mapping exists.
- Mission-name note for the coordinator: this mission was delivered on the existing lane branch
  `lane-0428-083-datasources-r2` / PR #1684 per the window-hopf/monotonicity directives; no remote
  branch or PR named `lane-083-runtime-call-site` exists (`git ls-remote origin` shows nothing for it).
  If a different base was intended, that is a coordinator decision — this lane preserved all rules.
- entblockt durch #1592 (the historical blocker; resolved — its code is in develop and consumed here).

cleanliness: before = ambient `docker ps -a` shows the 7 `bh-local-shared-*` containers only (plus
transient `Created` stubs from the earlier daemon flakiness); all prototype containers/networks/volumes
(proto-*, deny-*, p3xx/p4xx/p5xx, c4x, t-echo, probe-*, baha-perses-ds-*, proto-net*/n4x/n5x,
proto-perses-db) were removed during the session; after = `docker ps -a` lists only the ambient
bh-local-shared-* set, `docker network ls` only bridge/host/none/baseharbor-local-*, no baha-perses-ds
leftover, host helper processes (fake prom listeners) stopped, /tmp/opencode prototype dirs removed.
Ambient bh-local-shared-* untouched per owner directive.
