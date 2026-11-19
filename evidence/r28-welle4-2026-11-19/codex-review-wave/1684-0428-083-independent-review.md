# Independent read-only review — PR #1684 / 0428-083

Reviewed 2026-11-19.

- Head: `738ed514b208239e02cb06968cc72bb808bc070c`
- Base at review: `7ee6f817dbff5a238bbc651315d6d76b3819fc91`; current `develop` had advanced to `558dc42d0c8c9d798fcdf5938be2ea14e432b754`.
- Exact-head run `44577713744` was terminal success for PR Selected Checks, but `PR · Selected Runtime` was skipped.
- No repository edit, PR comment, or merge was performed by this review.

## Findings

1. **The lifecycle resolver reads a different path from the production runtime.** Production `application.RuntimeFilesFor` (`internal/application/runtime_postgres.go:75-85`) sets the compose context to `store.Root/<app>/runtime`. The resolver registered by this PR (`internal/metrics/perses_datasource_lifecycle.go`) derives its projection root from the runtime directory as `<store.Root>/<app>/providers/management-ui/perses`. The materializer instead writes to `<store.Root>/applications/<resourceProject>/providers/management-ui/perses`. On the production layout these do not match, so the resolver reports the projection absent and Perses starts without the config/datasource mount. The test `TestPersesDatasourceLifecycleMountsResolveFromMaterializer` hardcodes an alternate `<state>/applications/<project>/runtime` layout rather than exercising `RuntimeFilesFor`; the container test mounts the materialized result directly and bypasses `RuntimeComposeYAMLForContextDir`. Test the actual `EnsureRuntime`/compose path for local and target layouts.

2. **The datasource endpoint is unreachable from the normal Perses container.** `ProviderEndpoint` (`internal/metrics/prometheus_render.go:25-40`) returns `https://127.0.0.1:<published-port>`, which the builder stores verbatim as `proxy.spec.url` (`perses_prometheus_datasource.go:218-242`). In the production Compose service, loopback refers to the Perses container itself, not host/Core Prometheus. The container test uses `docker run --network host` (`perses_prometheus_datasource_container_test.go:126-151`), masking this difference. Core Prometheus is also a separate service from the app Perses container. Provide an endpoint reachable from Perses on the production network, with matching TLS SAN/trust, and test it using an isolated bridge-network container through the rendered production Compose path.

3. **Production proxy TLS trust is missing.** `NewPersesGlobalDatasourceResource` sets no `proxy.spec.secret`, and the production materializer emits no proxy trust secret. The container test helper manually injects that reference and GlobalSecret (`perses_prometheus_datasource_container_test.go:118-124, 285-301`), so the witness exercises a repaired artifact, not production output. The managed endpoint uses the private BaseHarbor runtime CA; Perses will not trust TLS without a production-owned trust anchor/reference. Provision only the public CA material, safely reconcile and clean it up, and test the materialized artifacts verbatim.

4. **Runtime acceptance is still missing.** The exact-head `PR · Selected Runtime` gate was skipped. These production-path/runtime defects are not covered by the green Go unit/build/vet checks.

Unverified follow-up: the apply path sends `docker compose kill -s HUP perses` and immediately checks health while provisioning interval is 300 seconds. Confirm the signal semantics for the deployed Perses version before relying on that reload path.
