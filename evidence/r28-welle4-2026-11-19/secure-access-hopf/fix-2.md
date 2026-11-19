# 0428-089 fix-2 — Perses compose config render (mission-089)

Lane: 089-compose-config-render · Card: t-20261114-r28-perses-secure-access · PR: #1599
Branch (reality witness, see below): `lane-welle2-089-perses-secure-access` (PR #1599 head) · Starting head: 31adf08fa1d0dc77f3698dad23bde3654d2f5967
Final candidate head: 233be0af2bba691fed7bd99655fb78a7515e2a0f (pushed; exact-head run 44535875227 SUCCESS, see Handoff)
Worktree: /var/tmp/mission-1599-wt (this lane's persistent zone, branch review-hopf-1599)
Planning clone: /var/tmp/m089-plan-clone (remote: https://github.com/mcpdev80/baseharbor-plan.git) — this file is committed and pushed from there; no git action was taken in the shared plan working copy.

Note on the branch name in the mission: the mission names `lane-0428-089-secure-access`; `git ls-remote` shows no such ref. The real candidate branch of PR #1599 is `lane-welle2-089-perses-secure-access` at exactly the mission's head 31adf08fa. Same chain, one candidate — I continue that branch (the mission's "EXACTLY ONE CANDIDATE PER CHAIN" rule is satisfied by the branch the PR actually carries; the name in the mission is stale).

## PLAN

1. [x] Reality check: fetch --prune, plan.py show t-20261114-r28-perses-secure-access, task-note + PR #1599 body/comments, develop vs head (merge-base ancestor + merge-tree counting)
   - Done. Witnesses in "Reality check" below.
2. [x] Hop develop onto the candidate (monotone merge commits, no force) — three window switches handled: f518e859d, 3b634232f/#1602 5a68196a1, 859654861.
3. [x] Prove the gap: file:line showing PersesComposeServices sets --config=/etc/perses/config.yaml but no volume/mount is rendered anywhere
   - Done; witnesses in "Gap proof" below.
4. [x] Implement fix: render deterministic config from validated policy, mount read-only into Perses, reference-only credentials; fix the loopback-upstream blocker
5. [x] Test (i): rendered-runtime statement about mounted config path AND effective policy
6. [x] Test (ii): integration test for gateway reachability, auth enforcement, Perses NOT directly visible on the host
7. [x] Focused checks: go test ./internal/serviceaccess -run Perses -v, go test ./internal/serviceaccess ./internal/application, go build ./..., go vet, gofmt -l ., source-readability-audit.sh
8. [x] Push with ancestor witness onto 31adf08fa, draft=false held, exact-head run 44535875227 to terminal SUCCESS
9. [x] This evidence file on origin/main before END
10. [x] Host left besenrein (no lane-owned containers/networks/volumes; 7 ambient bh-local-shared-* untouched)

## Reality check (§4.1)

- `git fetch origin --prune`; develop chain (all linear, per coordinator windows): da76c5cf9 → e1dc2cf61 (#1691) → f518e859d (#1682) → 3b634232f (#1592, 0428-088 merged 12:58:23Z) → 5a68196a1 (#1602, 0428-077 merged 13:25:17Z) → bcd0e29ca → 859654861 (CI base-owned required checks, owner-CI work, no product content). `git merge-base --is-ancestor e1dc2cf61 origin/develop` -> true at every step.
- Hop 1 (develop f518e859d onto 31adf08fa): commit 98746df95f9f7bfe82dd520815e1ba1c27aca197, first parent 31adf08fa (monotone, no force). merge-tree: exit 0, tree 81a41770ecfb9064efa396f9db233b4e4e18d854, 0 conflicts. 110-territory check: `internal/deployment/config_mutation.go` + test are byte-identical in my hop tree (sha256 10dd53fb… / c995f87f…); my write-set touches zero files under internal/deployment — no stop needed.
- My fix commits: aa7c899a4 (config renderer + read-only mount + topology, 4 files, foreign-file count 0) and b216bbb31 (topology model + tests, 5 files, all Perses).
- Hop 2 (develop 5a68196a1…3b634232f side): commit 9f5b116552431e7830a77954333117ab6e041c20. From here `internal/application/perses_runtime.go` (088 content) is in my base — no fork. merge-base --is-ancestor after hop: true.
- Hop 3 (develop 85965486154284d4ae7974573f504002335d4523): final candidate 233be0af2bba691fed7bd99655fb78a7515e2a0f, first parent b216bbb31, monotone merge, no force. `git merge-base --is-ancestor origin/develop 233be0af2` -> true. `git merge-tree --write-tree origin/develop 233be0af2` -> exit 0, tree 246f26c450adc5db018b3a23c7efb3a592e49421, 0 conflicted files. The 077 develop files (`internal/metrics/perses_dashboards_hosts.go`, `internal/logs/render.go`, `internal/telemetry/otlp_payload.go`) are untouched by my commits: `git diff b216bbb31 HEAD -- internal/serviceaccess/perses_gateway.go` is empty (hop touched none of my content files; all Perses files byte-identical from b216bbb31 to HEAD).
- Remote truth (git ls-remote origin): develop 695ad54944734e9976fe9cc1dbae117482677dc6 at evidence time (later window movement, not on my chain); lane-welle2-089-perses-secure-access = 233be0af2 (my push landed: `31adf08fa..233be0af2` fast-forward). `gh pr view 1599`: state OPEN, draft false, headRefOid 233be0af2.
- Task note: `plan.py show t-20261114-r28-perses-secure-access` -> state active; depends contract-seam (accepted), perses-runtime (accepted, merged via #1592). The 0428-084 Ruhend-files (cmd/baha/perses_lifecycle*.go, contracts/machine/v1/control.golden.json, internal/machine/contract.go, cli docs) exist on the stack; my diff touches none of them.

## Gap proof (error being fixed)

The Perses service definition set the `--config` flag, but no mount fed it (file:line both sides, at head 31adf08fa):

- flag side: `internal/serviceaccess/perses_gateway.go:267` rendered `- --config=/etc/perses/config.yaml` (plus :268 `--web.listen-address=127.0.0.1:8080`) into the service's `command:`.
- mount side: the same function rendered only `tmpfs: /tmp` (:257-258) and deliberately no `ports:` (:259-261); there was **no `volumes:` block at all**. `HTTPGatewayComposeService` (`internal/serviceaccess/http_gateway.go:367`) renders only the gateway service, never the Perses service. Across the whole repo, `PersesComposeServices` had exactly one caller (`internal/serviceaccess/perses_gateway_test.go:200`) and **no realization or renderer emitted a `/etc/perses/config.yaml` mount anywhere** — `grep -rn "etc/perses/config" --include='*.go'` hit only line 267. Witness on the pinned image: `docker inspect persesdev/perses:v0.55.1 --format '{{join .Config.Cmd " "}}'` -> `--config=/etc/perses/config.yaml --log.level=error` while the distroless image ships no such file, so Perses falls back to the compiled defaults: `security.enable_auth: false` — the exact anonymous exposure the contract forbids. The rendered plan/policy was never applied.
- loopback-upstream blocker: `BuildPersesGateway` hard-coded `UpstreamBindAddress = "127.0.0.1"` (`perses_gateway.go:132`) while the gateway spec upstream is `http://perses:8080` (`internal/application/perses_management_ui.go:310`); a loopback bind in the Perses container's own namespace is unreachable from a separate gateway container.
- product truth: no compose realization anywhere called `PersesComposeServices` at 31adf08fa (the 088 runtime landed in develop later, mid-window), so the config producer this fix adds is new and leak-free in the write-set: it materializes deterministically from the validated policy and is mounted read-only.

## Config provenance chain (policy → renderer → mount → container path), at candidate 233be0af2

- Policy: `internal/application/perses_management_ui.go:300-315` `PersesGatewayPlanFor` folds Target knowledge (`PersesProxySSRFDenyNetworks`, `:300-308`) into the effective posture and hands it to `serviceaccess.BuildPersesGateway` (`:316`). The fail-closed gate is `internal/capability/perses_security.go:120-145` `ValidatePersesSecurityPolicy`, re-checked by every later step.
- Renderer: `internal/serviceaccess/perses_config_render.go` `RenderPersesConfig` — validates first (`:48-50`), refuses a routable-literal bind (`:51-59`), then emits YAML keyed by the upstream v0.55 schema: `security.enable_auth`, `security.encryption_key_file` (file reference only, `PersesEncryptionKeyContainerPath` :31-36 — no secret value interpolated, never logged), `security.readonly`, `security.authentication.providers.enable_native: false`, `datasource.disable_local`, `datasource.proxy.{deny_private_networks,denied_networks,allowed_networks,allowed_hosts}`, `datasource.proxy.http.allowed_schemes`, `database.file.folder` (tmpfs path), `provisioning.folders`. Lists are deduplicated + sorted; bare addresses normalized to CIDR, so the rendering is deterministic.
- Materialization: `internal/application/perses_runtime.go` `EnsurePersesManagementUI` renders `capability.DefaultPersesSecurityPolicy()` through `serviceaccess.RenderPersesConfig` and projects the bytes with `writeUIRuntimeProjection` (0644, the managed-UI pattern). `PersesConfigHostPath` (same file, :30-38) names the host file the compose mount must feed.
- Mount: `internal/application/perses_runtime.go:99` renders `./providers/management-ui/perses/config.yaml:/etc/perses:ro` (read-only).
- Container path: `internal/application/perses_runtime.go:92` renders `--config=/etc/perses/config.yaml`, matching `serviceaccess.PersesConfigContainerPath` — flag, mount and rendered bytes provably agree.
- Gateway-adapter path (second consumer): `serviceaccess.PersesComposeServices` (`internal/serviceaccess/perses_gateway.go`) refuses to render without a registered `PersesConfigRenderer` (`:370-375`), then `validatePersesRenderedConfig` (`:420-440`) re-renders the policy, reads the declared host file and fails closed on drift, absence or a phantom path.
- Runtime proof: `TestPersesMountedConfigProvenanceAndEffectivePolicy` (genuine `EnsureRuntime` path) asserts the mounted file == `RenderPersesConfig(policy)` == what the command line names.

## Gateway topology: upstream reachability fixed

`BuildPersesGateway` no longer hard-codes `127.0.0.1` (`perses_gateway.go:150-193`): it parses the upstream host, distinguishes a service address from a literal, and records the topology in `PersesGatewayPlan.SharedGatewayNetwork` (new field). In the default shared-namespace form Perses binds `127.0.0.1` and the rendered Perses service carries `network_mode: "service:<gateway>"`, so the gateway reaches the loopback of the namespace it joined while Compose cannot publish a port of a container with no own networks (no host-visible Perses endpoint). In the namespace-local form (loopback-literal upstream matching the bind) the rendering publishes neither network_mode nor ports. Mismatched pairs, routable-literal binds and stranding loopback upstreams fail closed. `--web.listen-address` renders from the plan's verified bind (`PersesComposeServices`), so flag, file and topology can never disagree. The 088 single-container runtime path in develop keeps its own topology (see Scope notes); this card only wired the config mount there.

## Tests

- `internal/serviceaccess/perses_config_render_test.go` — `TestRenderPersesConfigIsDeterministicAndCredentialFree`; `TestRenderPersesConfigFailsClosedForInvalidPosture`; `TestPersesComposeServicesProvenanceFailClosed` (no producer, drifted file, unmaterialized path, phantom renderer — every refusal exercised).
- `internal/serviceaccess/perses_gateway_integration_test.go` — `TestPersesGatewayReachabilityAuthAndHostInvisibility` (isolated, in-process): upstream bound loopback-only through a namespace-local listener; the gateway front terminates TLS with `RequireAndVerifyClientCert` semantics using genuine `EnsureHTTPGateway` material from the same authority; subtests prove reachability through the shared namespace (`network_mode`-equivalent resolver: service name -> bound loopback), anonymous refusal, proxy prefix 404, and the rendered Perses block has no `ports:`/`expose:` and carries `network_mode: "service:perses-ui-access"` — Perses never host-visible.
- `internal/application/perses_config_provenance_test.go` — `TestPersesMountedConfigProvenanceAndEffectivePolicy` (rendered-runtime statement: mounted path + effective policy on the production `EnsureRuntime` path); `TestPersesRuntimeFilesRequireConfigProducerFailClosed`.
- CI routing: all three files are plain Go tests in `./internal/serviceaccess` / `./internal/application`; the run's `PR · Go unit · packages` cell executes them on every PR push (both packages ok in run 44535875227). No `.github/**` change was needed; none was made.

## Scope notes (honest limits)

- The recipe's "bind Perses on its private Compose interface" is implemented for the gateway-adapter rendering (shared network namespace, above). The 088 single-container runtime path merged into develop renders Perses with `0.0.0.0` + a published loopback host port; a published port stays reachable from other containers on the host, so that path does not yet enforce "only the gateway reaches Perses". Rewriting develop's merged 088 rendering is outside this card's correction; flagged here, not silently expanded.
- The compose daemon journey (containers) is smoke/validation material owned by the window's VM/gate lanes; this lane's durable proof is the three CI-executed test files above. No containers were started on the coordinator host (inspect = metadata only).

## Candidate log (31adf08fa..HEAD lists only my commits + develop hop content)

`git log --oneline 31adf08fa1d0dc77f3698dad23bde3654d2f5967..233be0af2bba691fed7bd99655fb78a7515e2a0f`: my content commits aa7c899a4 and b216bbb31, my monotone hop commits 98746df95, 9f5b11655, 233be0af2; everything else in that list is develop's own merged history arriving as hop parents. My commits' file deltas contain zero foreign files (per-commit `git diff --name-only` lists above). `git merge-base --is-ancestor 31adf08fa HEAD` -> true.

## repo-rule compliance

- Fail-closed everywhere: no registered config producer, drifted/unmaterialized/phantom rendering, anonymous or keyless posture, routable-literal bind, mismatched upstream/bind pair, missing issuer or TLS — each refusal is exercised by a test.
- Secrets: encryption key referenced by file only; no credential value in the rendered YAML, manifests, logs or assertions.
- runtime != capability != delivery preserved: provider realization lives in serviceaccess/application; no capability claim changed; `internal/capability/perses_security.go` gained only the documented `BindAddress` field (4 added lines, 0 removed — the field the renderer and plan cross-check).
- Ownership respected: `.github/**`, `scripts/**` untouched; 077's develop files untouched (byte-proof above); 0428-121 envfilter and 0428-084 Ruhend files untouched; no evidence or operational text in the product repo.
- One candidate per chain: everything landed on `lane-welle2-089-perses-secure-access`; no second branch (no new refs on origin; ls-remote witnesses above).
- Evidence discipline: this file committed and pushed from the isolated clone /var/tmp/m089-plan-clone against https://github.com/mcpdev80/baseharbor-plan.git; zero git actions in the shared plan working copy.

## Cleanliness

- Before (`docker ps -a` at session start): exactly the 7 ambient `bh-local-shared-*` containers of other karren; after: identical set, nothing added. This lane started no container, network or volume on the coordinator host; the integration test is in-process Go. No `docker pull`, no compose project of mine exists to tear down.
- cleanliness: no lane-owned containers/networks/volumes/state directories remain on any host I touched.

## Handoff

- Candidate: 233be0af2bba691fed7bd99655fb78a7515e2a0f on `lane-welle2-089-perses-secure-access`, PR #1599 (open, draft=false), base develop 85965486154284d4ae7974573f504002335d4523.
- Exact-head run: 44535875227, watched to terminal (`gh run watch`, exit 0): completed/success; 41 jobs, 23 executed all success, 18 skipped. Aggregate `PR Selected Checks` = SUCCESS. New base-owned line `candidate_advisory_required` = "false" (the candidate-added advisory check is skipped for this diff — no candidate-added validation outside the required plan). The `PR · Selected…` matrix cells are skipped (no runtime gate was selected for a pure renderer/adapter diff with passing unit coverage — no native runtime risk path changed).
- Local focused checks (this worktree, HEAD 233be0af2): `go build ./...` clean; `go vet` clean; `gofmt -l .` empty; `bash scripts/source-readability-audit.sh` PASS (size/function/ratchet); `go test ./internal/serviceaccess -run Perses -count=1 -v` = 14 top-level Perses tests PASS; `go test ./internal/serviceaccess ./internal/application ./internal/capability -count=1` all ok. No full ./... run (per mission).
- Reviewer: Codex Luna re-review against the REQUEST-CHANGES recipe in evidence/r28-welle4-2026-11-19/codex-review-wave/1599-0428-089.md.

## Zero-reach witness (mission branch name)

`git ls-remote origin refs/heads/lane-0428-089-secure-access` -> empty (ref does not exist on mcpdev80/baseharbor; before AND after my push). Product diff at candidate contains 0 occurrences of that string. One candidate only: `lane-welle2-089-perses-secure-access` = 233be0af2 (ls-remote witnesses in Reality check and Handoff).

## END

END_DONE mission-089-compose-config-render.md: deterministic policy renderer + read-only mount + reachable, non-host-visible Perses landed on candidate 233be0af2 (PR #1599, draft=false); exact-head run 44535875227 SUCCESS with PR Selected Checks = SUCCESS and candidate_advisory_required=false; evidence on origin/main.
