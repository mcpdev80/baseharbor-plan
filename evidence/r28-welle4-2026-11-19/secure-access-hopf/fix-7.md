# fix-7 — carrier move to serviceaccess + compose validity (B1) + auth posture (B2) (0428-089)

Mission: mission-089-compose-config-render.md · Card: t-20261114-r28-perses-secure-access · PR: #1599
Branch: lane-welle2-089-perses-secure-access (monotone, no rebase, no force, no second branch, lane never merges)

traeger-verschiebung: capability -> serviceaccess, begruendung: 0428-084 ist gemergt/abgenommen, deployment-feld gehoert nicht in eine sicherheits-postur

## PLAN

1. Restore internal/capability/perses_security.go byte-identical to its state at ed7f448f6 (the merged 0428-084 contract surface): zero diff for the capability files, proven by `git diff` witness below.
2. Move ServiceAddress + EncryptionKeyFile onto the serviceaccess carrier: PersesGatewayPlan, PersesGatewayPlanRecord (persisted gateway-plan.json) and PersesGatewayRequirements.ServiceAddress; PersesComposeServices falls back to plan.EncryptionKeyFile.
3. RenderPersesConfig gains the service address as a parameter (2-arg); every call site and every test that touched the capability struct is converted to the plan carrier — no posture file edit.
4. B1 (coordinator variant A, B forbidden): the Perses service renders `network_mode: "service:perses-ui-access"` EXCLUSIVELY — the `networks:` block is removed from that branch (Docker Compose forbids network_mode AND networks on one service). The backend-network alias rides the gateway service's first network via spec.NetworkAliases, which EnsurePersesManagementUI sets from plan.ServiceAddress (deployment-scoped producer; the contract-level BuildPersesGateway stays alias-free). The shared classification (perses_gateway.go upstream-form decision) is untouched — verified by a persisted-plan witness in the new test.
5. B1 validation: a REAL validator replaces string comparison — `docker compose config -q` against the rendered stack where the CLI exists (the hosted runners have it; the test skips that half with a log line where it does not), plus a YAML-parsed network_mode-XOR-networks rule on every host, plus alias-location (gateway yes / Perses no), loopback-pin retention, and Caddyfile reverse_proxy-to-alias witnesses.
6. B2: enable_auth: true with every provider disabled has no login path (Perses server verification refuses that shape). The rendering now states the ACTIVE native provider under the security block (Perses schema: security.authentication.providers.enable_native — a top-level authentication key with only `providers` and no oidc/oauth is not the schema SecurityConfig consumes). The posture "no unauthenticated exposure" (capability/internal/capability/perses_security.go (AuthenticationEnabled-required rule)) survives: auth stays ON; native users live in the encrypted database behind encryption_key_file.
7. B2 validation against the REAL parser shape, not a string: the regression unmarshals the mounted config.yaml and requires doc.security.enable_auth==true, security.encryption_key_file == PersesEncryptionKeyContainerPath, security.authentication.providers.enable_native==true, and NO top-level authentication key.
8. The 0428-143 Verification=none contract question is NOT touched (not this card's contract).
9. One monotone candidate, one exact-hosted-head run to terminal (§4.6).

## Carrier witnesses (capability -> serviceaccess)

- `git diff 97d88ffef --name-only | grep internal/capability` → `internal/capability/perses_security.go` ONLY (the 13 added field lines removed).
- `git ls-tree 97d88ffef` vs new head: perses_security.go + perses_security_test.go blob identity restored (diff vs ed7f448f6 state = empty; the two fields ServiceAddress/EncryptionKeyFile are gone from the posture struct).
- carrier fields now: internal/serviceaccess/perses_gateway.go (PersesGatewayPlan.ServiceAddress :134, PersesGatewayRequirements.ServiceAddress, PersesGatewayPlanRecord.ServiceAddress/EncryptionKeyFile), persisted/read in perses_compose_realization.go, set in internal/application/perses_management_ui.go (:332) and perses_runtime.go (record write at EnsurePersesManagementUI).

## compose validierung (B1) — with file:line

- Defect (measured at 97d88ffef): internal/serviceaccess/perses_compose_realization.go wrote `network_mode: "service:<gateway>"` AND, for len(plan.Spec.Networks)>0, a `networks:` block — Docker Compose forbids the pair (https://docs.docker.com/reference/compose-file/services/), so `docker compose up` fails on the delivered stack; the string-compare unit tests let it through.
- Fix: networks: block removed from the shared branch (perses_compose_realization.go, fix-7 comment at the branch); alias registration moved to the gateway service: internal/application/perses_runtime.go EnsurePersesManagementUI sets plan.Spec.Networks=["default"] and plan.Spec.NetworkAliases=[plan.ServiceAddress] before persisting the record; HTTPGatewayComposeService (internal/serviceaccess/http_gateway.go :422-452, the `i == 0` branch) emits them under the gateway's first network. The gateway's upstream still names the alias host (BuildPersesGateway unchanged; sharedNetwork stays true — coordinator's variant-B prohibition honored).
- Fail-closed in BOTH directions: alias resolves from OTHER containers to the GATEWAY namespace (perses_gateway.go:114-121 documents exactly this); Perses itself binds namespace-loopback only (command pin), and the /proxy/ route stays refused by the gateway Caddyfile; a peer dialing bh-dev-<name>-perses:8080 reaches the gateway, which 404s/refuses — Perses never answers on a routable interface.
- New tests: TestPersesComposeValidatesUnderRealToolchain (docker compose config -q + yaml rule + shared-topology witness), TestPersesComposeAliasLivesOnGatewayNotPerses (alias on gateway / none on Perses / loopback pin kept / Caddyfile reverse_proxy to alias). Gate: Go unit · packages shard (./internal/application).

## auth-postur (B2) — with file:line

- Defect: internal/serviceaccess/perses_config_render.go rendered `security.enable_auth: true` plus `authentication: providers: enable_native: false` — enable_auth with zero active providers has no login path; server verification refuses the pattern.
- Upstream schema proof (perses/perses v0.55.0, fetched from the pinned release tag): `pkg/model/api/config/config.go` Config has fields Security/Database/... — NO top-level `authentication`; `pkg/model/api/config/security.go` Security carries `Authentication AuthenticationConfig \`yaml:"authentication,omitempty"\``; `pkg/model/api/config/authentication.go` AuthenticationConfig.Providers is `AuthenticationProviders` with `EnableNative bool \`yaml:"enable_native"\``. So the schema-consumed path is security.authentication.providers.enable_native; the `authentication:` key at document level was parsed nowhere (or failed strict validation) and `enable_native: false` left zero providers active under enable_auth — the refused no-login-path shape.
- Fix: perses_config_render.go now emits `  authentication:\n    providers:\n      enable_native: true` INSIDE the security block (91). Chosen posture: enable_auth ON + native provider activated (coordinator option 2), NOT auth-off — so the capability AuthenticationEnabled rule survives; the gateway (mTLS/bearer) remains the operator boundary; the native account store is encrypted with the key material from fix-6.
- Validation at the real parser shape (not string): TestPersesRenderedConfigAuthenticationProviderIsValid unmarshals the mounted config.yaml (production path via EnsureRuntime) and asserts the nested security.authentication.providers.enable_native==true shape and absence of a top-level authentication key.

## Head sequence (monotone)

| step | head | note |
| --- | --- | --- |
| fix-6 candidate (qualifying) | 97d88ffefa0c89281d0c1b776f47b46f4449123f | run 44582754552 SUCCESS (21 executed) — superseded by fix-7 per the review |
| + fix-7 content (carrier move + B1 + B2 + regressions) | 2048612cf3cfd1a23745fa52ad703d1742023bfd | run 44593538443 on this head CANCELLED by the concurrency group when the comment-only follow-up pushed |
| + comment-only witness commit | 8c5b6b95486632c4fcbd95d847a36167b56b502c | exact-head run 44594142616: completed SUCCESS, 21 executed / 0 failed, "PR Selected Checks" success, candidate_advisory_required="false", PR mergeStateStatus CLEAN, draft=false. Superseded by the required base hopf below (develop moved after the push). |
| + monotone merge-hopf origin/develop 223cb97a9d652a4672257cabbadf12e2b41ed9cd (0428-148-docs squash-merge, other world) | e435527348587d6246b0af600c6bd82717ce9c32 | merge commit, 0 conflicts; `git merge-base --is-ancestor origin/develop HEAD` = true; base diff 558dc42d0..223cb97a9 touches ONLY docs/de/how-to/observability.md + docs/how-to/observability.md (one line each) — no CI-half files, no overlap with this lane's write-set. exact-head run under watch: 44598112016 — terminal result recorded below. |

## Branch witnesses (AGENTS 5.3)

- `git ls-remote origin refs/heads/lane-welle2-089-perses-secure-access` → `e435527348587d6246b0af600c6bd82717ce9c32  refs/heads/lane-welle2-089-perses-secure-access` (at the hopf push; before it `8c5b6b95486632c4fcbd95d847a36167b56b502c`).
- `git ls-remote origin refs/heads/develop` → `223cb97a9d652a4672257cabbadf12e2b41ed9cd` (coordinator-measured; ancestor of the branch head after the hopf).
- New exact-head run after this change: 44594142616 → superseded; qualifying run 44598112016 on e43552734 (conclusion recorded by the follow-up commit of this file). Runtime gates remain SKIPPED per the owner wire (114(a) ORAS install) — not a failure of this candidate.

Ancestry: origin/develop(558dc42d0) → both heads true; ed7f448f6 → both true; no rebase, no force; develop did not move during this window (ls-remote 558dc42d0 at push time; the existing hopf 97d88ffef already carried it, so no new hopf was due).

## Local validation (all before the push)

- go build ./... clean; go vet ./internal/application ./internal/serviceaccess ./internal/capability ./cmd/baha clean.
- go test ./internal/serviceaccess -count=1 → ok; ./internal/application -count=1 → ok; ./internal/capability → ok; ./cmd/baha -run '^Test(Perses|AppPerses)' → ok.
- new fix-7 tests FAIL on pre-fix-7 content (stash witness) and pass after — they reproduce the reviewed defects.
- bash scripts/ci-fast-check.sh → 280 python tests OK, "No candidate-added validation checks", source-readability PASS.
- gofmt -l clean.

## repo-rule compliance

- Traeger question: applied as decided (capability files zero-diff; carrier in serviceaccess). The capability/perses.go PersesConfiguredStatusNow addition was NOT part of the three locked hunks and stays (it is 0428-089's own fail-closed status work from fix-1/2, referenced by cmd/baha tests of this card).
- One PR per card, monotone commits on lane-welle2-089-perses-secure-access, draft=false; no merges by the lane; no subagents (§4.8).
- .github/** and scripts/** untouched (Owner scope).
- Docker: the compose-validating test invokes only `docker compose config -q` on a temp-dir file (pure validation, zero containers/networks/volumes); hosted CI runners have the CLI; where absent the rule check still runs via YAML.
- Host cleanliness: this lane created no containers, networks, volumes or state directories; the foreign perses-proto/deny/probe set remains reported-only, untouched.
- Secret protection: the encryption key value never appears in compose, config, records or this evidence; only paths/modes are stated.
