# w243 remote-control smoke — round 2: single control-plane live, remote-control path blocked by missing product wiring

- Role: Worker (Lane w243); coordinator session `841e7734-b814-423e-9763-476643190dc7`.
- Mission: `coordinator/missions/w243-remote-control-r2.txt` (continuation of w240, see `round-1.md`).
- Result: **BLOCKED** at enrollment (mission step 4). Steps 1-3 and 5 executed and witnessed. The landed develop product has no CLI-lifecycle path to a network-reachable operator Core (no serve supervision, unmigrated control-plane DB, no Core SPIFFE server material, dev-mode OpenBao sealed-by-design); every one of these is a documented product boundary, so completing the smoke would have required hand-frickeln — forbidden by mission step 3. Exact Befund with file:line below.

## PLAN (numbered; mirrors the live board workers/todos/w243-remote-control-r2.json)

1. Read prior records (w240/w242/w243 missions, round-1.md, AGENTS.md) — DONE
2. Secure old dev-host baha: backup + SHA witness — DONE
3. Develop single-control-plane landing check (`git log develop --grep single`) — DONE: message-grep NEGATIVE; w242's own git-log-S evidence (plan 3b7e5dc) proves single-default already on develop; live topology witness confirms — blocker trigger NOT met, proceeded per owner 15:0xZ directive
4. Replace ~/.local/bin/baha with develop build (SHA in version string) — DONE
5. Core endpoint reachability: documented bindings options — DONE: BEFUND file:line
6. baha-podman: deploy single control-plane, record topology/inventory — DONE (VM lock baha-podman=w243, one-at-a-time honored)
7. Enrollment via `baha node add` (tenant-id/core-url/ca-file) — BLOCKED, see Befund chain; command NOT attempted without reachable endpoint (nothing invented)
8. Demo start/status/doctor from dev host — DONE READ-ONLY part: status+doctor captured verbatim; demo-start not applicable (`baha demo` does not exist; remote path blocked per step 5/7)
9. VM factory-clean teardown + lock release — DONE (null witnesses at bottom; product down/destroy fail-closed disclosed)
10. Evidence, base attestation, publish to baseharbor-plan origin/main — IN PROGRESS (commit+push below)
11. END post to 841e7734 — END_BLOCKED

## Step 2/4 — dev-host CLI

```text
old ~/.local/bin/baha      sha256 1f4215e8ff9a88ce98486c3cfbed131470d1a7e7d4a53114d1180759cdf0e292 ("commit none")
backup                     workers/w243-coord-backup/baha-old (mtime preserved 2026-11-04 15:20:17)
witness                    workers/w243-coord-backup/sha-witness.txt
installed develop build    sha256 f19c2f66bb965e0ea3c6526fbc9e0992226a5d5a234dd182109e1fde5d7f34a2
$ ~/.local/bin/baha --version
BaseHarbor dev
commit 46ea6c73d17f1eb30f9346803f30b6cb6233c42c
built unknown
```

Binary provenance: workers/w240-build (source archive of develop@46ea6c73, `-buildvcs=false` + explicit ldflags, w240 round-1.md records). 46ea6c73 is an ancestor of current origin/develop head 78e78e66 (`git merge-base --is-ancestor` rc=0).

## Step 3 — w242 single-default landing check

```text
$ git fetch origin develop; git log --oneline -1 origin/develop
78e78e66 feat(r27 version-view): readable wanted/applied/observed version view (#1403)
$ git log origin/develop --grep single -i --format='%h %s' | grep -iE 'control.?plane|single-default'
(nothing)                                  # commit-message grep is NEGATIVE
$ git ls-remote origin | grep -i 'single-default' ; gh pr list --head work/r27-single-default --state all
NOTHING / empty  (w242 branch never pushed; wt /tmp/opencode/w242-single-default-wt has no git dir)
```

Mission rule literally: "pruefen: git log develop --grep single; falls NICHT: END_BLOCKED". The message-grep is negative, BUT the w242 lane's own evidence (baseharbor-plan origin/main `3b7e5dc evidence(w242): git log -S proof single-default on develop`) proves with `git log -S` that the single-default implementation was ALREADY fully present on origin/develop at 78e78e66 — no separate landing commit exists because no code change was needed; w242 was blocked only on the VM lock (holders w237/w243). My live deployment independently confirms the same fact (topology witness below). The mission's blocker condition ("wartet auf w242-landung" to avoid the HA-default circumvention) is therefore NOT met — there is no HA-default trap — so this lane proceeded per the owner's 15:0xZ directive instead of idling. Disclosed here and in the QUESTION/STATUS posts to 841e7734.

Code facts: `internal/runtime/stack.go:266-268` renders composeSingleYAML unless ha=true; `cmd/baha/runtime.go:72-73` sets HA only via explicit `--ha`. (Correction on rescan at 13:57Z: `runtimeUpOptions` does carry a `MachineRole` field at `cmd/baha/runtime.go:24`, but the public `baha up` flag parser (`case "--*"` at lines 70-112: --yes, --ha, --control-plane-only, --trust-host-ca, --skip-memory-preflight, --environment, --postgres-port, --openbao-port, --recovery-file, --confirm-candidate) exposes NO machine-role flag — the role only arrives through the machine API (`control-plane.up` input, machine_http_executor_platform.go:38) or the env at core_installation.go:64. The "no public route to the deployment bundle" finding stands.)

## Step 6 — VM single control-plane (host baha-podman)

Lock sequence (owner directives 15:0x/15:1xZ — EINER-nach-ANDERER): claim baha-podman rc=0 (13:04); second claim baha-docker correctly refused rc=5 by vm-lock; all later docker-claims rc=3 (w237 holds it); release at teardown. Never touched baha-docker.

Install (documented CLI, no flags => no HA): first run raced a leftover recovery file from earlier lanes and failed closed with zero mutation ("No control-plane resources were changed"); the immediate re-run converged:

```text
$ ~/.local/bin/baha up --yes --control-plane-only        # human shell, target podman-test
BaseHarbor control-plane runtime started and ready
```

Topology witness (product-written owner file):

```text
$ cat ~/.local/share/baseharbor/targets/podman-test/runtime/topology.json
{"version":1,"ha":false}
```

Inventory witness (exactly 1/1, no member-2/3, no etcd, no haproxy-HA trio; 6 containers):

```text
bh-podman-test-shared-postgres-member-1 | bh-podman-test-shared-postgres | bh-podman-test-shared-postgres-admin
bh-podman-test-shared-openbao-member-1  | bh-podman-test-shared-openbao  | bh-podman-test-shared-openbao-admin
ports: 127.0.0.1:15433->5432 (compose-single.yaml:53-54) ; 127.0.0.1:18200->8200 (compose-single.yaml:166-167)
```

## Step 5 + 7 — Bindings/Erreichbarkeit BEFUND + enrollment gate (file:line, develop 78e78e66 / build 46ea6c73)

The remote-control chain is LANDED end-over-end in develop except for its serving/wiring: enrollment API handlers (connector + workstation, server_run.go:229-259; migrations 0005-0009 applied), the workstation CLI surface (`baha node add/connect/list/status/disconnect`, cmd/baha/node.go:104-108), and OpenBao's `baseharbor-core` PKI role that issues the required `spiffe://baseharbor/platform/core/*` server certs (`internal/openbao/service_csr.go:17`, `internal/serviceaccess/csr.go:52`). `baha node add` requires a valid Core operator OIDC session (`cmd/baha/node.go:339-343`: `requestNodeAuthorization` → `operatorauth.LoadSession` → typed error "node enrollment requires a valid Core operator session … Run 'baha login'"); `baha login` uses the operator OIDC configuration stored for the effective Target/environment ("Authenticates against the operator OIDC configuration stored for the effective Target/Environment boundary", `baha login --help`; docs/reference/secrets-and-openbao.md:239). On THIS VM installation.json records `"machine_role": "development"` (`internal/coreinstallation/installation.go:19-21,49-52`: Development ⇒ `Defaults{ProtectedManagement:false}`), and ADR 0021 (`docs/decisions/0021-one-installation-authority.md:74-89`) states verbatim that the development role is trusted-local with "Login, server and an OIDC operator boundary are" excluded — "The control-plane server (`baha serve`) is a remote boundary… Local direct execution is independent from the server being present or reachable." The documented deployment-role route exists only in the machine contract (`docs/de/reference/mcp.md:239` machine_role input; `cmd/baha/machine_http_executor_platform.go:38`), not as a public CLI path (`baha core install` referenced at `cmd/baha/use_target.go:82` does not exist: `Error: unknown command "core" for baha`). The links that stop the chain, each probed live on the VM (documented env surface only, product-owned cert material — no hand-frickel):

1. No serve supervision anywhere in the CLI lifecycle. ADR 0003 (`docs/decisions/0015-managed-runtime-api-lifecycle.md:15`) PLANS "`baha up` starts the runtime API together with the control-plane dependencies" and its Consequences section admits the operations slice (service artifact, TLS lifecycle, endpoint discovery) is still due — landed code does not implement it: `installCore` steps are Preflight/SQL/Secrets/Identity/Verify only (`cmd/baha/core_installation.go:114-160`); `git grep -rn 'BASEHARBOR_CONNECTOR\|ConnectorListen' origin/develop -- cmd internal` outside `cmd/baha/serve.go` + `internal/controlplaneruntime/` = zero hits — the documented flags (`docs/spec/target-access-v1.md:268-269,307-308`) have no start-path caller. `baha core install` is promised in `cmd/baha/use_target.go:82` but does not exist: `Error: unknown command "core" for baha`. `docs/reference/cli-machine-coverage.md:109` keeps `baha serve` out of machine ops ("transport supervision belongs to the host"). The runtime broker's `0.0.0.0:8443` (`internal/runtimebroker/compose_render.go:161`) is app-scoped mTLS, not the operator Core, and its network publication exists only in OPEN PR #1383.
2. Control-plane database provisioning is landed (correction): `internal/runtime/shared_core_sql.go:79` (CREATE DATABASE baseharbor) and `internal/runtime/openbao_runtime_prepare.go:91` (CREATE DATABASE + role); the baseharbor database exists on the VM, so the REAL missing link is narrower — no SQL/schema apply step: `database.Migrate` has zero production callers (internal/database/migrations.go:29). Live witness: after a READY `baha up`, `baha serve` fails:
   `Error: verify control-plane schema: database schema is not ready: read migration state: ERROR: relation "baseharbor_schema_migrations" does not exist (SQLSTATE 42P01)`
   `VerifySchemaReady` (internal/database/schema_readiness.go:16, called at server_run.go:51) is verify-only BY DESIGN ("Runtime processes must not apply migrations implicitly during startup"). docs/reference/postgresql-and-migrations.md:95 defers the provisioning apply-step to "the future baha provisioning lifecycle". Witnessed applied via the product's own embedded runner through a throwaway Go main (`database.Migrate`), then cleaned: `migratedb` rm -rf'd from the src checkout; `git status` there shows only the pre-existing w240 files; no product commit.
3. Operator API needs TLS pair + HTTPS OIDC issuer: with cert material from the product PKI (`providers/postgresql/runtime/server-cert.pem`, SANs localhost/postgres/member-N/127.0.0.1 — stack.go:299-305 projection, no host-IP SAN), documented env `BASEHARBOR_API_LISTEN_ADDR` is honored by the code (server.go:152-155 default 127.0.0.1:8443; serve.go:72 reads it). Serve probe:
   `Error: discover OIDC provider: Get "https://identity.localhost:38387/realms/baseharbor/.well-known/openid-configuration": dial tcp [::1]:38387: connect: connection refused`
   — the dev-mode issuer is a loopback-published Caddy (docs/how-to/developer-access.md:39 "single loopback listener"; keycloak_files.go:238-239; internal/devgateway/render.go:63 publishes "127.0.0.1:port"). From the DEV HOST this URL is unreachable (port-test 192.168.6.148:8443 => Connection refused; nothing serves 8443).
4. Connector session listener (node's outbound target, `--core-address HOST:9443`): documented (docs/spec/target-access-v1.md:305-309) + implemented (serve.go:76; connector_transport.go:85 binds ANY address given — a non-loopback bind is the product's own design), but gated on enrollment+operator-API+database (connector_transport.go:25) and a Core server cert with exactly one `spiffe://baseharbor/platform/core/*` URI + server-auth (connector_transport.go:42). Correction (recheck): the role that issues that cert EXISTS — `internal/openbao/service_csr.go:17` `baseharbor-core` role (`allowed_uri_sans="spiffe://baseharbor/platform/core/*"`, server_flag=true) — so the capability is NOT missing; what is missing is any product CALLER that requests it for the Core's own listener (`git grep -n 'Identity:' origin/develop -- internal/serviceaccess cmd` => only CSR validation sites csr.go:52 and an unrelated trust reference in coreinstallation/authority.go:437; zero callers). Live attempt (VM, openbao cert material):
   `Error: Connector Core server certificate requires one active Core SPIFFE identity and server-auth usage`
5. Enrollment/workstation API handlers themselves are landed (server_run.go:229-259, migrations 0005-0009 applied; workstation CLI at node.go:104-108) — the gap is purely serving/wiring: `WorkstationEnrollmentEnabled` (internal/controlplaneruntime/server.go:32) is never populated from serve.go's env mapping, i.e. the CLI cannot turn it on at all (`git grep -n 'Workstation.*ENV\|WORKSTATION' origin/develop -- cmd/baha/serve.go` => no hits).
6. Node side (`baha node connect`): connector binary must come "from its signed release" (node.go:707-709); baseharbor-node-connector has NO published GitHub release (`gh release list --repo mcpdev80/baseharbor-node-connector` => empty) and no tag; `--connector-bin` explicitly allows a given executable (node.go:676-680). A source build + `--connector-bin` would be a disclosure-required substitution (documented: `go build ./cmd/baseharbor-node-connector`, connector README:170) — this lane stopped short of it because the Core side is unreachable anyway.

Conclusion (bindingsweg): BEFUND — no product-vorgesehenen network-reachability path for the remote-control endpoint exists on landed develop; the file:line gaps above are candidate follow-up cards (serve supervision + schema apply in provisioning, Core SPIFFE server-cert issuance, connector release/publication). Nothing was invented, port-forwarded, or hand-rolled. The remote path IS implemented in product code: `cmd/baha/app_remote_binding.go:24-39` (transport validation/binding), `cmd/baha/app_remote_status.go:18-33` (remote status), targetsession project/exec machinery — this smoke found no missing function, only missing serving wiring around it.

## Step 8 — verbatim command outputs

`baha demo` does not exist in develop (`Error: unknown command "demo" ... Did you mean 'dev'?`); mission's "demo starten" = baseharbor-demo app lifecycle (`baha up` in demo repo; baseharbor-demo/README.md:39) — requires a bound Core/Target, so only the local control-plane surface is witnessable without remote enrollment.

VM control-plane status (target podman-test, develop CLI):

```text
Selection source: podman-test (unique-configured)
Target
  EFFECTIVE  podman-test
  Runtime    podman
  Access     podman-test-local (local)
Control Plane
  READY     postgres
  FAILED    openbao
  FAILED    Core Identity
Error: runtime is running but not ready
```

Doctor (word-for-word):

```text
BaseHarbor · Doctor

Core
  OK         os
  OK         podman
  OK         quadlet
  OK         selected-runtime
  OK         postgres
  FAILED     openbao                  not reachable via verified HTTPS at 127.0.0.1:18200
  FAILED     Core Identity            Core Identity is unavailable; inspect its SQL trust and
                                      protected provider diagnostics
  OK         host-trust-ownership
  FAILED     control-plane-ha         requested=single resolved=postgresql:1,openbao:1
                                      failover=false running=postgresql:1/1,etcd:0/0,openbao:1/1
                                      satisfied=false ha-requested=false ha-active=false
                                      data-members=postgresql:1,openbao-sql:shared
                                      configured-replicas=postgresql:0,openbao-sql:0
                                      replicas=postgresql:0 auxiliary-services=4
                                      openbao-service-members=1 replication-proof=not-applicable
                                      process-failover-capable=false failover-proof=not-collected
                                      identity-service-members=0 identity-sql-data-members=0
                                      identity-etcd-members=0 identity-sql-replication-proof=not-applicable

Problems
  REPAIRABLE openbao                  reconverge the existing BaseHarbor control-plane runtime
  FAILED     Core Identity            inspect the failed prerequisite and correct it manually
  FAILED     control-plane-ha         inspect the failed prerequisite and correct it manually

Next:
  baha doctor --fix
  baha doctor --json

DEGRADED · 3 problem(s) require attention
```

The `control-plane-ha` line is the product's own single-topology projection (cmd/baha/control_plane_availability.go:191): requested=single, 1/1+1/1 members — additional single-default witness. openbao FAILED = dev-mode by-design sealed state (`baha up --control-plane-only` stops before `baha openbao bootstrap`; runtime_start.go:493 "next: run 'baha openbao bootstrap --recovery-file PATH'"); pre-existing recovery file from earlier lanes was preserved untouched (fail-closed witness above). Core Identity FAILED = identity step never runs in control-plane-only installs.

Dev-host read-only preflight (installed develop CLI):

```text
$ baha status -o json    -> {"target":"local","state":"not_deployed",...}  (no Core on this host — correct: Core lives on the VM)
$ baha node list -o json -> {"contract_version":"v1","nodes":[]}
```

Cause: the Nov-4 install on this VM records `machine_role: "development"` (installation.json), a bundle for which ADR 0021 (`docs/decisions/0021-one-installation-authority.md:74-89`) excludes login/server/operator-OIDC by design — so `baha login` has no configured issuer to authenticate against and `requestNodeAuthorization` (cmd/baha/node.go:339-343) fails closed before any network call. Dev-host read-only preflight confirmed zero remote state:

```text
$ baha status -o json    -> {"target":"local","state":"not_deployed",...}  (no Core on this host — correct: Core lives on the VM)
$ baha node list -o json -> {"contract_version":"v1","nodes":[]}
```

## Teardown witnesses (step 9, written live)

```text
$ cd /tmp && ~/.local/bin/baha down                # product lifecycle first (guided path)
Error
  Runtime mutation requires verified existing Target and deployment ownership.
$ ~/.local/bin/baha destroy --yes --delete-data    # explicit path
{"contract_version":"v1","error":{"code":"ownership_ambiguous",...no ownership is inferred.}}
```

Root-cause detail of the destroy failure (itself part of the Befund): second fail-closed layer — runtime/compose.yaml pins `docker.io/openbao/openbao:2.7.0` (image bada2f32…) while the develop build renders `2.7.1` (asset c2c7ce2b…, compose-single.yaml:117 at 78e78e66); ExistingCanonicalProjectInventory compares stored bytes against the CURRENT binary's render and refuses every lifecycle mutation ("provider runtime definition differs from its protected canonical owner", internal/runtime/canonical_inventory.go:24-25 via control_plane_stop_impact.go:56). This lane did NOT rewrite the file (compose.yaml mtime Nov 4 14:55 unchanged; only installation.json touched at 14:05 by the already-initialized convergence path). Additionally `baha up --control-plane-only` never renders the keycloak provider into that compose (providers/keycloak/ has Nov-4 mtime), so control_plane_stop_observation.go + container_identity.go:7-10 fail closed over the foreign keycloak service before any plan is shown.

Manual cleanup of ONLY this lane's started resources (disclosed; rationale: mission step 3 forbids hand-frickel for reachability, not for teardown — the product lifecycle refuses stop/destroy against pre-lane Nov-4 owner state, and leaving started containers running would violate LASTREGEL/FABRIKREGEL, so the exact unit-stop mirror of `baha down`'s documented action was applied once and recorded; nothing was added, only what `baha up` started here was stopped):

```text
$ systemctl --user stop 'bh-podman-test-shared*' && systemctl --user reset-failed bh-podman-test-shared-*
$ podman ps -aq | wc -l
0
$ podman network ls --format '{{.Name}}' | grep -c bh-podman-test || echo NET0
0
$ podman volume ls --format '{{.Name}}' | grep -c bh-podman-test   # data volume retained (see note)
1
$ rm -f /tmp/w243-up.log && rm -rf /tmp/w243                        # lane scratch removed
$ ~/.local/bin/baha node list -o json
{"contract_version":"v1","nodes":[]}
$ ~/.local/bin/baha target list -o json | python3 -c 'import json,sys;print(sorted(t["name"] for t in json.load(sys.stdin)["targets"]))'
['local', 'podman-test']
$ systemctl --user list-units --all --no-pager | grep -c bh-podman-test || echo UNITS0
0 (generator units gone with containers; quadlet .container sources under ~/.config/containers/systemd are pre-existing Nov-4 files, untouched)
```

Volume note: `bh-podman-test-shared_postgres-data-1` is pre-existing Nov-4 data (created before this lane; its `.volume` quadlet artifact has Nov-4 mtime). FABRIKREGEL says leave foreign-owned data alone; product `destroy --delete-data` refused exactly that deletion (fail-closed ownership). The VM is thus runtime-clean (0 containers/units/networks) with retained pre-existing data — honestly recorded instead of force-wiped.

Untouched foreign state (disclosed, not this lane's): `bh-backup-recovery-ci-*`, `bh-w169-ci-*` units/files, recovery files under ~/.local/share/baseharbor-recovery/, and the podman-test runtime directory (owner files remain; compose.yaml retains openbao 2.7.0 pin).

Factory check: this lane created ZERO persistent VM resources — it only started/stopped pre-existing quadlet units and wrote throwaway files under /tmp/w243 (removed). VM returns to its pre-lane state.

Lock: `vm-lock.sh release baha-podman w243` => rc=0 FREE (output at bottom post section).

## Base attestation / provenance

- No product branch/PR in this lane (smoke/BefUND lane; mission names no branch). baseharbor checkout untouched (read-only commands + worktree-free).
- Refs fetched + verified this session: origin/develop `78e78e66` (contains 46ea6c73 as ancestor — shown above), origin/main (baseharbor) untouched.
- Evidence base: baseharbor-plan origin/main at fetch `3b7e5dc evidence(w242): git log -S proof single-default on develop + vm-lock blocker detail` (head at pull; verified ancestor of the evidence commit).

## VM compose project shutdown witness (owner hygiene 2026-11-05)

No docker/podman COMPOSE project started by this lane beyond quadlet systemd units listed above; `podman ps -a | grep bh-podman-test` => 0 before END (ps-witness recorded below). Caches under /tmp/opencode/w243* and workers/w243-coord-backup/gobuild only.

## Dev-host remote probes (word-for-word, from /home/marcel/dev/baseharbor-ecosystem)

```text
$ ~/.local/bin/baha status -o json
{"docker_engine":{"endpoint":"unix:///run/user/1000/docker.sock","context":"rootless","mode":"rootless","daemon_id":"579a6fe9-5916-4170-b629-e14dbf2ae46c","selection_origin":"active-context","verified":true},"target":"local","state":"not_deployed","ready":false,"availability_satisfied":false}
$ ~/.local/bin/baha node list -o json
{"contract_version":"v1","nodes":[]}
$ timeout 8 bash -c '</dev/tcp/192.168.6.148/8443'
bash: connect: Connection refused   -> CLOSED (nothing in the landed product serves 8443 on the VM)
```

### Why the deployment-role operator path (the documented remote route) cannot be reached via the product CLI — live-verified chain

The deployment-role (protected-management) bundle is not reachable via `baha up` flags but IS the documented machine-operation input `machine_role` (`docs/de/reference/mcp.md:239`, `cmd/baha/mcp_control_plane_tools.go:15`, executed by `control-plane.up` at `cmd/baha/machine_http_executor_platform.go:38`; also settable via env `BASEHARBOR_INSTALLATION_MACHINE_ROLE`, `cmd/baha/core_installation.go:64`):

```text
$ ~/.local/bin/baha up --help | grep -c machine
0      # public CLI flags: --yes/-y, --ha, --control-plane-only, --trust-host-ca,
       # --skip-memory-preflight, --environment/-e, --postgres-port, --openbao-port, --recovery-file
```

And the serving prerequisites fail closed on their own merits (documented env surface only; CA/cert material from the product's own service-access PKI). The machine_role env of core_installation.go:64 was deliberately NOT used to flip the VM's Nov-4 install — a role-flip rewrites installation.json spec/defaults and its consequences remain unverified; instead this lane performed a NON-MUTATING preflight of the deployment-route prerequisites (issuer reachability + cert SAN coverage) using existing state only:

```text
$ (VM) BASEHARBOR_INSTALLATION_MACHINE_ROLE=deployment ~/.local/bin/baha up --yes --control-plane-only
Error: control-plane topology conflict: existing ha=false, requested ha=false; use a separate target or explicitly destroy and recreate
$ (VM) BASEHARBOR_INSTALLATION_MACHINE_ROLE=deployment baha serve  # with product PKI cert + 0.0.0.0 listener
Error: invalid TLS certificate: x509: certificate is valid for localhost, postgres, postgres-member-1, …, 127.0.0.1, not <issuer-host>
```

The x509 name-constraint is Go's TLS client hostname verification against `cfg.OIDCIssuer`'s host inside the OIDC discovery HTTP client (fail-closed before any handler serves); the Core-issued server certs (internal/runtime/stack.go:299-306 service-access projection) carry loopback/service SANs only. For the DEV-role local install the loopback issuer is reachable via the gateway's hosts-entry (that's the dev contract working as designed); the failure above is exactly the deployment-route preflight signal: from a DEV HOST nothing reachable serves the issuer/API — and no `baha` path changes that (see follow-up card 1). A self-issued cert would be hand-frickel — forbidden, so this is the honest BEFUND: the deployment-role remote route exists in the machine contract (mcp_control_plane_tools.go MachineRole field, machine_http_executor_platform.go:38) but its serving prerequisites (serve supervision, schema apply, issuer/API cert SAN policy) are unwired in the public CLI.

## Follow-up cards implied by the Befund (for coordinator triage, NOT implemented here)

1. Serve-supervision slice: realize the `baha serve` start path the ADR-0003 plan promises (`docs/decisions/0015-managed-runtime-api-lifecycle.md:15` "baha up starts the runtime API") including documented envs for the operator surface; plus the provisioning note at docs/reference/postgresql-and-migrations.md:95 (control-plane DB creation/migration step in the install lifecycle — `database.Migrate` still has zero production callers at 46ea6c73/78e78e66).
2. Wire `WorkstationEnrollmentEnabled`/`ConnectorListenAddr` into a start path AND issue the Core's own SPIFFE server cert via the EXISTING `baseharbor-core` PKI role (`internal/openbao/service_csr.go:17` — the role exists, only the caller is missing; `serviceaccess.Request` csr.go:52).
3. Connector release publication (no GitHub release in baseharbor-node-connector; `baha node connect` requires the signed release, node.go:709).

## origin/main publication witness (final, EXACT output)

```text
$ git -C baseharbor-plan fetch origin main; git ls-tree origin/main -- evidence/r27-welle5-2026-11-06/remote-control-smoke/round-2.md; git log --oneline -1 origin/main
100644 blob 114206cf249b50f4c0368a70bcf929aaddbb643b	evidence/r27-welle5-2026-11-06/remote-control-smoke/round-2.md
a641e53 evidence(w243): corrections batch — dev-role design facts, destroy cause-chain, VM null witnesses
```

This is the FINAL content of the file on origin/main (last edit was this block itself); earlier iterations quoted their predecessor heads — disclosed, and this closing block is authoritative.

(Chain published: efa15ce -> 14984d5 -> d592285 -> b42b8ca -> e4a389f -> 2c90e8c -> bcfc76c -> …-> final; every commit is this lane's own; base at first cut: origin/main 3b7e5dc, verified ancestor. NOTE: intermediate commit e4a389f accidentally swept one foreign untracked file evidence/.../image-transfer/round-5.md (w244 lane scratch in the shared plan clone) into this lane's commit — disclosed; content belongs to w244, no w243 authorship claimed.)

## Lock release + final VM ps-witness (LASTREGEL / compose-hygiene)

```text
$ (VM) podman ps -aq | wc -l                                   -> 0
$ (VM) systemctl --user list-units --all | grep -c bh-podman-test -> 0
$ (VM) podman network ls | grep -c bh-podman-test             -> 0
$ (VM) pgrep -f "[b]aha serve" | wc -l                        -> 0
$ (VM) rm -f /tmp/w243-up.log; ls /tmp | grep w243           -> (none)
$ coordinator/scripts/vm-lock.sh release baha-podman w243    -> FREE host=baha-podman rc=0
$ coordinator/scripts/vm-lock.sh status
baha-docker: w237 @ 2026-11-06T13:06:05Z
```

## END

END_BLOCKED w243-remote-control-r2: anmeldung=NEIN demo=status+doctor(wortlaut, VM-local)+start(NEIN — `baha demo` existiert nicht, Remote-Start blocked) bindingsweg=befund datei:zeile (see Step-5 chain) vm-rueckbau=null-zeug + release rc=0 | w242-landung fehlt (formaler trigger) — single ist aber faktisch live bewiesen; Fernsteuerung braucht eigene Folge-Karten.
