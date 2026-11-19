# Independent read-only review — PR #1599 / 0428-089

Review performed 2026-11-19 against the live pull request.

- Head: `97d88ffefa0c89281d0c1b776f47b46f4449123f`
- Base: `558dc42d0c8c9d798fcdf5938be2ea14e432b754` (`develop` at review time)
- PR state: open, merge state blocked.
- Exact-head run observed: `44582754552`, completed successfully after the initial review. Go shards, build/vet, docs checks and the required aggregate passed; runtime/native gates were skipped. No acceptance verdict or merge is given here.

## Findings

1. **Compose service creation is blocked by mutually exclusive network settings.** `internal/serviceaccess/perses_compose_realization.go:352-363` emits `network_mode: service:perses-ui-access` and also emits `networks`. The production caller in `internal/application/perses_runtime.go` supplies `plan.Spec.Networks = []string{"default"}`. Docker Compose does not allow `network_mode` and `networks` together for one service. The Perses service therefore cannot be created with this realization. The shared-namespace service should omit its own `networks` and use the gateway's network. Add a Compose-config or runtime test for the emitted model.

2. **Perses rejects this authentication configuration.** `internal/serviceaccess/perses_config_render.go:73-83` sets `security.enable_auth: true` and `authentication.providers.enable_native: false`, but no external provider is configured. In Perses v0.55.1, `Security.Verify()` rejects this exact combination with “impossible to enable auth if no authentication provider is setup”. Gateway mTLS authenticates the client certificate but does not mint or forward a Perses JWT. Configure a real Perses provider, or intentionally define and test a secure gateway-only boundary with Perses configured consistently. Upstream source: [Perses v0.55.1 security config](https://github.com/perses/perses/blob/v0.55.1/pkg/model/api/config/security.go).

The Compose incompatibility is documented in the [Docker Compose service reference](https://docs.docker.com/reference/compose-file/services/). This review made no repository edits, PR comments, or merge.
