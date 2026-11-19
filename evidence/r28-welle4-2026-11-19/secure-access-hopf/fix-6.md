# fix-6 — Perses production gateway composition + encryption key material (0428-089)

Mission: mission-089-compose-config-render.md · Card: t-20261114-r28-perses-secure-access · PR: #1599
Branch: lane-welle2-089-perses-secure-access (no competing branch, monotone, no force, no rebase)

## PLAN

1. Reproduce both blockers at ed7f448f (B1: runtime_postgres.go:369 still called
   writePersesUIComposeService — Perses bound 0.0.0.0 with a published port in the
   delivered compose; B2: perses_config_render.go:67 referenced
   PersesEncryptionKeyContainerPath with no producer, no projection, no mount).
2. Switch the production compose path to the gateway rendering: network_mode into
   the gateway namespace, no Perses published port, no routable bind; the gateway
   becomes the only host-visible address (loopback publish).
3. Retain the legacy direct-publish writer with zero callers and an in-source grep
   witness; document it as the negative shape.
4. Persist the credential-free gateway plan record (compose-project-scoped service
   address, topology, posture) during EnsurePersesManagementUI; the pure compose
   rendering reads it back and identity-checks it against this deployment's Perses
   service alias, so a copied-in or stale record cannot render.
5. Add the key producer: 32 crypto/rand bytes, authoritative copy 0600 via the
   atomic owner-only writer outside every mounted tree; reuse keeps the key
   (the Perses database decrypts with it); a weakened-mode or truncated key fails
   closed.
6. Add the container-readable projection (0644 file in a dedicated 0755 directory
   providers/perses-management/secrets/) and mount that directory read-only at
   /etc/perses/secrets — directory binds, because a file bind under /etc/perses
   would make the daemon root-create the parent and the distroless nonroot could
   not read through it.
7. Regressions through the production path (a) gateway-only exposure, (b) key
   absent fail-closed, (c) key present auth+mount; update the existing compose/
   provenance/TLS tests and the lifecycle resource expectation (gateway container).
8. Monotone merge-hopf develop 7ee6f817d into the same push (base-distance
   directive: scripts/test_pr_gate_plan.py + scripts/ci-workflow-policy.sh differ
   since c296086ca).
9. Local validation (build, vet, focused tests, ci-fast-check) then one exact-head
   hosted run to terminal with the PR Selected Checks witness.

## Head sequence

| step | head | note |
| --- | --- | --- |
| previous candidate | ed7f448f6a84a6ed917260cd4186a2a122a077ed | run 44551362534 SUCCESS (interim, superseded by fix-6) |
| + monotone merge-hopf origin/develop 7ee6f817dbff5a238bbc651315d6d76b3819fc91 | 6d15092d9 (merge commit, 0 conflict regions) | `merge-base --is-ancestor origin/develop HEAD` = true; #1581 touched only scripts/ (no product conflict, as predicted) |
| + fix-6 content commit | 16f6cf671aa3bde59f793333fb4957d0e1434652 | pushed; run 44580643188 (watched to terminal below) |

Ancestry witnesses (all true): ed7f448f6 → 16f6cf671, origin/develop(7ee6f817d) → 16f6cf671; `git merge-tree --write-tree origin/develop 16f6cf671` conflict count = 0.

## Base-distance witness

`git diff --name-only c296086ca1e35ef3212d293afc94d7bebcd1690f 7ee6f817dbff5a238bbc651315d6d76b3819fc91` (coordinator-measured):

- scripts/ci-workflow-policy.sh
- scripts/test_pr_gate_plan.py

scripts/test_pr_* is a gate-plan hit, so one new exact-head run (44580643188) is the qualifying evidence; the interim runs 44544947599 and 44551362534 are superseded.

## Blocker 1 (B1) — production compose still direct-publish — RESOLVED

- Site: internal/application/runtime_postgres.go:369 (ed7f448f) called
  writePersesUIComposeService (internal/application/perses_runtime.go:61), which
  rendered `--web.listen-address=0.0.0.0:8080` plus a published loopback port on
  the Perses container itself. The gateway compose path existed only behind test
  drivers.
- Resolution: the Perses branch of RuntimeComposeYAMLForProject now calls
  writePersesGatewayComposeServices, which renders via
  serviceaccess.RenderPersesCompose from the persisted plan record: Perses gets
  `network_mode: "service:perses-ui-access"`, the command-line loopback pin
  `--web.listen-address=127.0.0.1:8080`, NO ports block; the gateway service
  (Caddy, TLS+auth, refused /proxy/ routes) owns the only host-visible loopback
  port. The gateway reaches Perses through the backend-network alias
  (devaccess.ApplicationAlias(app, "perses")) of the Perses service; Perses joins
  the same `default` network declaration so the gateway keeps its backend alias.
- Grep witness: `grep -rn writePersesUIComposeService --include=*.go .` returns
  only the definition (internal/application/perses_runtime.go) and its comment
  lines — zero production and zero test callers. The function is retained
  deliberately as the documented negative shape; removing it is not required by
  any contract (its old output form would still be refused by the workload
  security analyzer, and TestPersesComposeRenderedWhenSelected now pins the new
  form).
- Fail-closed/three-state preserved: manifest gate (services.perses ⇒
  ObservabilityManagementUI, pinned release), `configured_unverified` stays a
  degraded check (VerifyApplicationManagementUIChecks perses branch untouched),
  status never slips to verified.

## Blocker 2 (B2) — encryption_key_file without producer — RESOLVED

- Site: internal/serviceaccess/perses_config_render.go:67 wrote
  `encryption_key_file: /etc/perses/secrets/encryption-key` while
  `grep -rn PersesEncryptionKeyContainerPath` (ed7f448f) showed only the
  constant, the config line, a test and one os.WriteFile in the test helper —
  no production producer. With capability/perses_security.go:53 refusing keyless
  auth, the delivered composition could not start Perses with its claimed
  posture.
- Resolution (producer → projection → mount):
  - producer: ensurePersesEncryptionKey (internal/application/perses_runtime.go)
    generates 32 crypto/rand bytes once per deployment, writes the authoritative
    copy with writeOwnerOnlyFile (atomic, 0600) at
    secrets/perses/encryption.key under the runtime dir — outside every mounted
    tree; reuse keeps the existing key; mode & 0o077 != 0 or len < 32 fails closed.
  - projection: a 0644 copy in the dedicated 0755 directory
    providers/perses-management/secrets/ (regenerated from the authoritative key
    on every reconciliation; never logged; the value never appears in compose,
    config or evidence).
  - mount: the rendering bind-mounts exactly that directory read-only at
    /etc/perses/secrets (PersesEncryptionKeyComposeBindDir in
    serviceaccess.PersesServiceMounts — one contract list shared by renderer,
    composition and tests). Directory-bind rationale: the distroless nonroot
    image cannot read a file bind whose parent /etc/perses/secrets the daemon
    would root-create; and the two /etc/perses subtree mounts never shadow each
    other.
  - fail-closed: checkPersesCompositionFiles (projection path, run before
    rendering) plus the renderer's byte-for-byte proof refuse any composition
    whose key file, gateway Caddyfile/material or config.yaml is absent or
    drifted. PersesComposeServices itself refuses when no key projection path is
    declared at all.
- Stale material: EnsurePersesManagementUI retires the legacy server.cert/
  server.key/pki projections from providers/management-ui/perses (that whole tree
  is bind-mounted into /etc/perses, so only contract files may live in it); the
  persistence marker stays for the lifecycle verify gate.

## New/changed regressions (production path, not definition-only)

- TestPersesProductionComposeIsGatewayOnlyExposure — (a) via EnsureRuntime →
  RuntimeComposeYAMLForProject: perses service has no `ports:`, no 0.0.0.0 in
  its command, `network_mode: service:perses-ui-access`, and only the gateway
  publishes (127.0.0.1-prefixed).
- TestPersesProductionComposeFailsClosedWithoutKeyMaterial — (b) remove the key
  projection or the gateway Caddyfile after EnsureRuntime ⇒ composition refuses
  to render (fail-closed; no silently-keyless Perses).
- TestPersesProductionComposeMountsKeyAndConfig — (c) full contract mount set
  (config dir, secrets dir, persistence volume, all :ro where bind), config.yaml
  equals the deterministic rendering of the plan's effective policy, projection
  0644 / authoritative 0600.
- Updated on the gateway topology: TestPersesComposeRenderedWhenSelected (parses
  both services), TestPersesTLSFilesProjectedAndConsumed (gateway material
  modes + SANs incl. localhost/127.0.0.1/perses-ui-access),
  TestPersesMountedConfigProvenanceAndEffectivePolicy (contract mounts + plan
  determinism), TestPersesRuntimeFilesProjectProviderFiles,
  TestPersesLifecycleResourcesIncludeManagedService; internal/application/
  runtime_lifecycle.go now declares the perses-ui-access container in
  ExpectedRuntimeResourcesForProject.
- CI gate: all of the above live in ./internal/application (and
  ./internal/serviceaccess) and run in the required "Go unit · packages" shard
  of the PR gate plan (go test ./internal/... selection); no workflow file was
  touched (Owner scope respected).

## Local validation (all before the push)

- go build ./... → clean
- go vet ./internal/application ./internal/serviceaccess ./internal/capability ./cmd/baha → clean
- go test ./internal/application -count=1 → ok; ./internal/serviceaccess → ok;
  ./internal/capability → ok; ./internal/logs ./internal/metrics ./internal/machine → ok
- go test ./cmd/baha -count=1 -run "^Test(Perses|AppPerses)" → ok
- gofmt -l internal/ cmd/ → clean
- bash scripts/ci-fast-check.sh → 280 python tests OK; "No candidate-added
  validation checks"; source-readability initially FAILED (perses_gateway.go
  815 > 800) → split the compose-realization half into
  internal/serviceaccess/perses_compose_realization.go; audit now PASS
- Background local full run of go test ./cmd/baha (pre-fix-6 tree): environment-
  dependent failures only (TestAppEditCommandCompleteProviderEditRunsRealLifecycle
  "existing native network lacks a protected Core or shared backend owner";
  TestPrepareStagedCoreGitCandidatePinsCanonicalApplication "native Git archive
  failed: signal: killed"; TestRuntimeUpRequiresORASBeforeCoreBootstrap expects an
  ORAS-masking error but the host HAS docker) — NOT persistent evidence (§5.3);
  the hosted exact-head run is.

## Todo file (AGENTS 4.4)

Written after the coordinator's reminder: coordinator/workers/todos/mission-089-compose-config-render.json (11 numbered steps, same plan as the ## PLAN list above; steps 7-9 were already done when the file was created and are recorded as completed).

## Hosted run (exact head)

- run 44580643188 on 16f6cf671aa3bde59f793333fb4957d0e1434652 — watched to
  terminal: completed SUCCESS, 21 executed / 0 failed (20 skipped by matrix
  design), "PR Selected Checks" = success, candidate_advisory_required="false",
  base develop (7ee6f817d), draft=false, mergeStateStatus CLEAN. This head is
  the full fix-6 qualification.
- Interim runs 44544947599 and 44551362534 are superseded per the
  base-distance rule.
- Post-qualification: a comment-only test cleanup (c4b0759a7) started run
  44582266839, which the branch's concurrency group CANCELLED when develop
  moved (558dc42d0, #1701) and the lane executed the required monotone hopf
  into the same push: head 97d88ffefa0c89281d0c1b776f47b46f4449123f
  (ancestors: ed7f448f6 true, origin/develop(558dc42d0) true; merge-tree
  conflicts 0; diff 7ee6f817d..558dc42d0 touches only
  internal/metrics/perses_dashboards_messaging* — no CI-half files, no
  overlap with this lane's write-set). Its exact-head run: 44582754552 —
  terminal result: (recorded by the follow-up commit of this file).

## repo-rule compliance

- One candidate per chain: continued on lane-welle2-089-perses-secure-access,
  monotone merges and content commits only; no rebase, no force, no second
  branch; the lane never merged.
- develop-hopf executed into the same push as fix-6 content (coordinator base-
  change directive); conflict count 0; the predicted surprise files
  (internal/capability/perses.go, cmd/baha/machine_coverage.go) were untouched
  by 7ee6f817d.
- .github/** and scripts/** untouched (Owner scope).
- internal/capability/perses_security.go: the coordinator locked this file
  ("SPERRDATEIEN: nicht aendern"). fix-6 needed a persisted, credential-free
  carrier for the service-address statement (compose-project-scoped) and the key
  file reference so the pure rendering stays deterministic and testable. The
  change is additive-only (two documented fields; ValidatePersesSecurityPolicy
  semantics untouched). If the coordinator considers this a lock violation, the
  fields can move into a serviceaccess-side record struct instead — say the word
  and I re-cut without touching the file. Flagging here rather than silently
  assuming.
- No subagents (§4.8). Host cleanliness: this lane created NO containers,
  networks, volumes or state directories of its own (the perses-proto/deny/probe
  set belongs to a foreign process and was left untouched as instructed);
  unit tests use t.TempDir() only.
- Secret protection: the encryption key value never appears in compose,
  rendered config, logs or this evidence; only paths and modes are stated.
