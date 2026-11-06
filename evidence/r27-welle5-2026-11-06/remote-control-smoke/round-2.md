# w243 remote-control smoke — round 2: anmeldung JA, remote binding belegt, remote `up` = Produkt-Luecke

- Role: Worker (Lane w243); coordinator session `841e7734-b814-423e-9763-476643190dc7`.
- Mission: `coordinator/missions/w243-remote-control-r2.txt` (continuation of w240, see `round-1.md`). This file REPLACES the earlier first-pass revision of this lane (published at `b4700ff`), which recorded a pre-correction END_BLOCKED ("no serve / no reachable Core"). The owner Korrektur and the resatz directive redirected the Muster to `docs/tutorials/homelab.md`: Core (+ alle Container) auf VM baha-podman, dev host = nur CLI (this lane ran the CLI as dev-host-standin ON the VM, since a dev-host login is impossible — see Befund 6), Anmeldung VON der VM initiiert, Targetanlage auf der Core-Seite, Operation gegen das remote Target.
- Result: **DONE with disclosed Befunde.** Enrollment (`node add` + `node connect`) works via product paths; connector holds 8 live mTLS sessions; the Core↔connector binding path IS reachable through the serve-side machine API (`control-plane.status`, `plan`, `runtime.list` all succeeded against target node-01 — proof that the connector-backed execution plane lands). The tutorial §4 app lifecycle over the connector is blocked by a qualified product capability gate (`app_remote_lifecycle.go:34`, Befund 5) and the CLI-only ops miss tenancy/coreAuthority wiring (Befunde 3, 4). VM factory-clean at teardown (null witnesses at bottom).

## PLAN (numbered; mirrors the live board workers/todos/w243-remote-control-r2.json)

1. Read prior records (w240/w242 missions, round-1.md, AGENTS.md) — DONE
2. Secure old dev-host baha (backup `workers/w243-coord-backup/baha-old` + sha witness), replace with develop build — DONE (first-pass section below stays valid)
3. Develop single-control-plane landing check (`git log develop --grep single`) — DONE: message-grep negative; w242's git-log-S evidence (plan 3b7e5dc) proves single-default already landed; live topology witness `{version:1,ha:false}` confirms — blocker trigger NOT met
4. Rebuild VM Core clean from develop@78e78e66 (`baha-now`), serve reachable, tenant seeded — DONE
5. Core-side remote-target creation per homelab §3 + Anmeldung VON der VM (homelab §2/§3) — DONE (with `--target` Befund 1/2)
6. Connector persistent + 8 live sessions (`node connect`, then manual daemon — Befund systemd unit) — DONE
7. Tutorial §4 operations (plan / up / status) against connector target + doctor + serve-side machine API — DONE, witnesses below; `up` = capability gap (Befund 5)
8. OIDC/session reconciliation (Keycloak claims seeding) — DONE, disclosed
9. VM factory-clean teardown + null witnesses + lock release — DONE
10. Evidence rewrite, commit+push to baseharbor-plan origin/main, END post — DONE (this file)

## Step 4 — VM Core (host baha-podman, target podman-test)

Source: develop@78e78e66 (`baseharbor-plan` cache checkout, `go build` with GOCACHE under /var/tmp/opencode-w243 — no ecosystem-root pollution). Control plane single topology (topology.json `{version:1,ha:false}`), doctor witness at first-pass section (all OK incl. control-plane-ha satisfied=true).

Serve operator API + connector listener: `baha serve` with documented envs (`BASEHARBOR_API_DATABASE_URL`, `BASEHARBOR_API_OIDC_ISSUER`, `BASEHARBOR_API_OIDC_AUDIENCES`, `BASEHARBOR_API_TLS_CERT_FILE/KEY`, `BASEHARBOR_CONNECTOR_*` incl. `CONNECTOR_LISTEN_ADDR=0.0.0.0:9443`, `RUNTIME_OPERATIONS_DIR`). The API TLS cert needed URI SAN `spiffe://baseharbor/platform/core/podman-test` (connector `--core-identity` pin, connector_transport.go:42) AND DNS SANs; issued via the product's managed-local OpenBao PKI role `baseharbor-core` (`internal/openbao/service_csr.go:17`); IP SANs forbidden (`internal/serviceaccess/csr.go`). Hostname `baseharbor-core` -> VM IP via /etc/hosts (reverted at teardown). Disclosure: a second throwaway serve instance on 8445/9445 was probed for the app-node-01 naming variant and abandoned (connector enrollment against it 401 — its authority path unresolved); killed at teardown, zero listeners after.

Tenant seeded: `7b37b9e2-2f1f-4a11-9c9a-9f4f1b5f1a11` ("BaseHarbor Platform"). Operator identity `baseharbor-operator` (subject bc0e7daf-…) with realm membership `editor` in that tenant.

## Step 5 — Anmeldung (homelab §3 target create + §2 login + node add/connect)

Canonical clean-slate flow (final state, verbatim):

```text
$ baha-now --target podman-test target list   # pre: only local + podman-test
$ python3 /tmp/authzsession.py podman-test dev
session saved via product SaveSession: /run/user/1000/baseharbor/operator-podman-test-dev.json | groups: ['editor', …] roles: ['editor', …]
$ baha-now --target podman-test node add node-01 \
    --runtime podman --tenant-id 7b37b9e2-2f1f-4a11-9c9a-9f4f1b5f1a11 \
    --core-url https://baseharbor-core:8443 --core-address baseharbor-core:9443 \
    --ca-file /tmp/w243-core/service-ca.pem --environment dev
Node node-01 prepared as Target node-01.
Enrollment file: /home/marcel/.local/share/baseharbor/node-enrollment/node-01.json
Copy this one owner-only file to the remote host, then run: baha node connect <file>
$ baha-now node connect ~/.local/share/baseharbor/node-enrollment/node-01.json \
    --connector-bin /home/marcel/.local/bin/baseharbor-node-connector
Node node-01 connected as Target node-01.
Connector service: baseharbor-node-connector.service
$ ss -tn state established | grep -c ':9443'
8
$ baha-now node status node-01
Target  node-01
Node    node-01
Runtime podman
State   ENROLLED
Expires 2026-11-07T18:18:09Z
```

What `node add` created (Core side, product path, cmd/baha/node.go:155-175): Target `node-01` (tenant-id set, access `node-node-01` → provider baseharbor-node-connector, reference node-01), access row, one-use enrollment grant in `connector_enrollment_grants` (TTL 600 s), node row in `connector_nodes`, bundle file 0600. `node connect` consumed the staged bootstrap authorization and enrolled the node cert (8 ESTABLISHED sessions; keepalive loop restarted the daemon on cert expiry during the long lane — a persistence workaround, see Befund 3).

Naming deviation, disclosed: the tutorial names the Target `app-node-01` (§3 lines 52-56). The product's default naming is target == node name (`node add node-01` → Target node-01, `node.go` opts.TargetID defaults to NodeID at :131-132). Forcing `app-node-01` via `node add --target app-node-01` is broken both ways (Befunde 1+2), and a post-hoc rename breaks the connector cert because the SPIFFE URI encodes target_id (`spiffe://baseharbor/platform/connectors/<tenant>/<target>/<node>`) — sessions only dial with a matching `--target-id`. The final demo therefore uses the canonical flow with Target node-01. A parallel `target create app-node-01 …` (product path, worked verbatim: "Target app-node-01 created") plus enrollment against a second serve demonstrated the target/node split, but that variant's connector enrollment 401s on the throwaway authority (documented above) — the node-01==app-node shape is the witness that stands.

## Step 7 — operations against the connector target (homelab §4 shape: `baha --target node-01 plan|up|status`)

CLI, dev-host-standin, verbatim (fresh session, DB env = Core authority):

```text
$ baha-now --target node-01 plan           # in /tmp/w243-demo (version:1, app demo/dev, services.sql: true)
Plan for demo (dev)
Operator access: trusted-local · READY · trusted-local
1. ensure database.sql:default - ensure SQL capability resource default
2. verify database.sql:default - verify application-facing SQL access for default
Core: not-required; additional providers: 2; unused providers retained: 0
Achtung: review the concrete consequences and required acknowledgements below.
$ baha-now --target node-01 up --yes       # + BASEHARBOR_PROVIDER_CHANGE_CONSENT (product env, provider_change_context.go:21)
Error
  Selected remote Application requires provider lifecycle adapters that are not yet qualified.
What to do
  Keep this deployment pending until its complete remote provider and workload contracts are supported.
$ baha-now --target node-01 status
Selection source: node-01 (explicit)
BaseHarbor · node-01
Target
  EFFECTIVE  node-01
  Runtime    podman
  Access     node-node-01 (baseharbor-node-connector)
Control Plane
  NOT DEPLOYED
$ baha-now --target node-01 doctor         # with node-01/dev session (external-oidc boundary)
BaseHarbor · Doctor
Core
  OK         os / podman / quadlet / host-trust-ownership
  FAILED     target-access            baseharbor-node-connector unavailable: Remote Target is
                                      outside the authenticated tenant.
  FAILED     control-plane-ha         real Core provider topology unavailable: stat
                                      ~/.local/share/baseharbor/targets/node-01/runtime/compose.yaml: no such file or directory
```

Serve-side machine API (`POST /api/v1/machine/executions`, bearer id_token from the product session file, TLS at :8443) — this is the bindingsweg PROOF (serve binds pool + coreAuthority + tenancy, machine_http_executor.go:33-45, application_core_authority.go:26-35):

```text
control-plane.status   -> state: succeeded | installation phase: ready
plan (demo/node-01)    -> state: succeeded | actions: ensure/verify database.sql:default
runtime.list node-01   -> state: succeeded | remote resources: 8  (container inventory VIA connector)
apply (consent input)  -> state: failed | capability_missing "…not yet qualified"  (Befund 5, same gate via API)
```

`runtime.list` succeeding with 8 remote resources through the connector is the end-to-end remote-control proof requested: Core-side machine API → bound connector session pool → node runtime, tenant-checked.

## Step 8 — OIDC reconciliation (disclosed, NOT product behavior)

The managed Keycloak user carried NO `groups`/`roles` claims, so the CLI membership resolver (`identity_tenant_resolver.go:95-130`, claim roles ∩ `memberships.role`) found nothing and tenancy stayed unresolved. Reconciled via Keycloak admin REST (admin token `baseharbor-admin`@master, client uuid b4de4632-b6bd-4d9c-b8e4-8daff4992b5a): `groups`+`roles` protocol mappers, editor group/role, directAccessGrants, redirectUris widened to `http://127.0.0.1:*` (product callback 127.0.0.1:19899/callback preserved). The DB membership row (tenant 7b37b9e2…, role editor, external identity 9d1c2f4e…) was seeded via SQL — disclosure: no product CLI path writes `memberships`/`external_identities` at 78e78e66 (grep: only resolver + migrations). Operator password rotated during probing (stored /tmp/w243-oppw, deleted at teardown). All Keycloak mapper/role/group deltas REVERTED before teardown (delete mapper/role/group 204×6, directAccessGrants=false, redirectUris restored).

## Befunde (file:line, develop@78e78e66)

1. `cmd/baha/node.go:143-146` — `node add --target NAME` against a pre-existing connector Target fails "node add must run against a local Core authority Target": the gate checks the EFFECTIVE target's AccessProvider, but the target it means (the local Core) is `effectiveTarget` under override; when `--target` names the REMOTE target, the same call self-rejects. Witness: run with existing app-node-01 → that error verbatim.
2. `cmd/baha/node.go:155-165` — with `--target` absent, `createTargetDefinition` silently creates the Target, then any later step failing rolls it back ("target \"app-node-01\" is not configured" after a silent create+rollback when e.g. the grant request fails). Net effect: the `--target` flag of `node add` is unusable in both postures; only default naming works. (Follow-up card candidate.)
3. systemd-user unit `baseharbor-node-connector.service` created by `node connect` fails on start: `detect runtime: selected enrolled runtime is unavailable` — ProtectSystem=strict sandbox breaks the rootless-podman probe (PATH/XDG/DBUS drop-ins do not fix). Product `node connect` itself works (bundle → ENROLLED). Workaround realized for persistence: manual run of the same connector binary with the unit's ExecStart flags + `--bootstrap-*` consuming the connect-STAGED (unconsumed) `bootstrap.authorization.json`; keepalive loop during the lane. Follow-up card candidate.
4. CLI `doctor --target <connector-target>` FAILS target-access even with a correct tenant-scoped session and tenant-id on the Target: `cmd/baha/runtime_explorer_machine.go:55-57` requires `tenancy.FromContext` == target.TenantID, but the CLI authorization path `cmd/baha/mcp.go:68` (`authorizeCurrentMCPContext("control-plane.doctor","","","")`) never attaches tenancy to the context (only the principal). The serve HTTP path does (`httpsecurity/middleware.go:54-60` ResolveTenant). Same gate makes `baha --target node-01 status` work only because status skips the connector explorer; the app-scope gate `application_core_authority.go:61-65` additionally needs the ctx coreAuthority, which only `newInstallationMachineExecutor` (serve) sets — CLI never does. This is the bindingsweg BEFUND half: product path for CLI-only remote app ops is not wired; the documented MCP/HTTP surface works.
5. `cmd/baha/app_remote_lifecycle.go:28-38` — remote workload qualification gate rejects ANY manifest that uses shared backends (`HasSharedBackends`, internal/application/shared_backends.go:139-140), i.e. the only service shape the manifest schema accepts at this revision (services.sql capability). Consequence: tutorial §4 `up` on a connector target can never succeed for an SQL app at 78e78e66 — capability gap, disclosed rather than hacked around (verified identically via CLI, MCP stdio, and HTTP API: `capability_missing "…not yet qualified"`).
6. `internal/devgateway/render.go:63` — dev-mode identity gateway publishes `127.0.0.1:%d:%d` (loopback-only). The issuer `https://identity.localhost:34885/realms/baseharbor` is therefore unreachable from a real dev host; a genuine dev-host `baha login` cannot complete against this VM topology (login binds a loopback callback anyway). Hence dev-host-standin execution on the VM; the remote-control CHAIN (Core API on VM, connector outbound sessions, remote operations) is host-independent and its witnesses carry over verbatim.
7. Connector binary source build (disclosed): baseharbor-node-connector has no published release; built from source @7fb235dd and fed via `--connector-bin` (node.go:676-680 allows it explicitly).

## First-pass section (pre-correction attempt, retained as history)

The following was written BEFORE the owner Korrektur (Muster shift to homelab.md) and is retained verbatim where still true: dev-host CLI secured and replaced (`~/.local/bin/baha`, old sha256 1f4215e8…, backup `workers/w243-coord-backup/baha-old`, develop build sha256 f19c2f66…, `commit 46ea6c73…`, ancestor of origin/develop 78e78e66 per `git merge-base --is-ancestor` rc=0); the first-pass conclusion "no serve supervision / unreachable Core => END_BLOCKED" is SUPERSEDED: serve IS the documented path (it just has no CLI-lifecycle supervision; this lane started it manually, disclosed). Step 3 landing-check reasoning (message-grep negative but `git log -S` proof in plan 3b7e5dc) stands. `baha demo` does not exist; "demo starten" = app lifecycle in a demo repo (done: /tmp/w243-demo, app `demo`, deployment records under `~/.local/share/baseharbor/targets/node-01/deployments/`).

## Teardown witnesses (step 9, null, written live)

```text
$ podman ps -aq | wc -l          -> 0
$ ss -ltn | grep -cE ':(8443|9443|8444|8445|9445)'  -> 0
$ pgrep -fa 'baseharbor|baha'    -> 0
$ ls ~/.local/share/baseharbor*  -> 0 entries (removed via PRODUCT path: baha destroy --all with two
  explicit acknowledgements + data-deletion consent (plan 77e51c82…, BASEHARBOR_PROVIDER_CHANGE_CONSENT);
  output: "REMOVED xdg-data / REMOVED xdg-config / BaseHarbor-managed installation state was permanently removed",
  PRESERVED host-CA-untracked anchor /usr/local/share/ca-certificates/baseharbor-3363a99a89c3a822.crt (ownership not verified))
$ grep -c baseharbor /etc/hosts  -> 0   (lane additions reverted)
$ ls ~/.config/systemd/user | grep -c baseharbor -> 0 (unit disabled+removed; drop-in dir removed)
connector state dir / node-enrollment / nodes -> 0 (product teardown removed; connector_nodes/grants rows gone with the DB)
VM /tmp lane throwaways deleted; /tmp/w243 + /tmp/w243-quadlet-quarantine are FOREIGN artifacts (untouched)
dev-host: zero containers throughout the lane (podman ps -q | wc -l = 0, docker ps -q | wc -l = 0); dev-host baha left at develop stand per mission (backup stays)
vm-lock: claim baha-podman w243 @18:22:34Z, released as last action (journal witness in END post thread)
```

## Base attestation

Product source: baseharbor develop@78e78e66 (`git -C baseharbor log -1 --format=%H`) + connector source 7fb235dd (build disclosures above). No product repo was modified by this lane; every file:line quoted resolves in `git show 78e78e66:<path>`.
