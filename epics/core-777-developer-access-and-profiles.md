---
id: core-777
title: Make developer access and profiles portable
status: open
release: v0.4.27
parent: v0.4.27
sources: ["mcpdev80/baseharbor#777"]
---
# core-777 · Make developer access and profiles portable

Source: [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777) (labels kind/feature, area/dx, area/compatibility). Parent: [v0.4.27](../releases/v0.4.27.md) work area 2. Final acceptance: #174 (v0.4.31). Contract freeze: #175. Related: #408, #613, #743, #399, #61, #102.

This note condenses the source's explanatory prose and keeps **every acceptance criterion and normative rule**. The full original text, including examples and rationale, is in the [source snapshot](../migration/source-snapshot/baseharbor/777.json). No executable tasks are cut yet: cut them before implementation.

## Release assignment (2026-10-10)

Execution belongs to v0.4.27 (#874), work area 2. Contract definitions (portable profile import/export schema, boundaries and authority) were to be specified under v0.4.25 (#872) first. Console UX/functional proof is v0.4.28 (#875). The source's "two sessions" wording is superseded by the task-PR model (see [decision](../decisions/2026-10-15-task-prs-supersede-shared-release-prs.md)). Older mentions of v0.4.22/v0.4.25 scope in the source are historical.

## Goal

Freeze one simple, standards-first developer access and credential-portability model before v0.5. BaseHarbor works locally without a BaseHarbor login; existing native authentication is always preferred; BaseHarbor-managed credentials are an opt-in convenience/security feature. Principle: **as little as possible, as much as necessary — native standards first.** Also define portable developer-profile export/import and its boundary to application backup/restore and platform disaster recovery.

## Normative rules (condensed)

- **UX:** prefer automatic discovery and reuse; one sensible default; ask only when BaseHarbor cannot infer safely; hide advanced controls until needed; never repeat known information or credential entry while safe reusable access exists; guided flows for setup, import, access changes, removal and recovery; wizards show only the current decision; destructive operations show impact and default to the narrowest safe action; machine surfaces expose the same semantics without prompts; errors give one concrete next action. Happy paths: Dev Local `clone → baha app init → baha up`; Dev Remote `receive bundle → baha import <bundle> → baha up`; shared/team `receive connection profile → import → authenticate when policy requires → work`.
- **Local development needs no login** to init/inspect apps, use Docker/Podman, local K3s with working access, existing Git checkouts and auth, or local managed providers. Login only where developer or Target policy requires it (Console, protected test/prod Targets, central credentials, remote org control planes, approval/audit).
- **Workspace location:** BaseHarbor-created clones default to `~/baseharbor/repos/<host>/<owner-or-group>/<repository>`; existing repositories stay where they are; developer-local paths stay out of portable intent; internal state uses XDG locations; #613 stays the Git/workspace authority.
- **Native authentication first:** Git (credential helpers, GCM/platform stores, SSH agent, `~/.ssh/config`, configured HTTPS auth, client certs) — "if normal git works, BaseHarbor does not ask again"; Kubernetes (`KUBECONFIG`, `~/.kube/config`, contexts, exec plugins, OIDC, client certs); cloud provider chains (AWS, Azure, Google). No second credential model.
- **Minimal credential choice:** no questionnaire; if native auth succeeds, continue silently. Otherwise ask the minimum, then only "Store securely for future use? [Yes] [No]". *No* = session only: not in Git, portable intent or OpenBao; temporary files only in a protected per-user runtime directory with owner-only permissions, removed after use; prefer memory/stdin/agents. *Yes* = BaseHarbor-managed protected state; OpenBao is the authoritative durable store where managed secrets exist; portable state holds references only; runtime files/env are projections (#743); reuse without prompts; rotation/revocation without rewriting intent. No OpenBao details in the normal prompt.
- **Credential classes:** username/password, bearer/API/PAT, SSH key (+passphrase), client cert/key + CA, repository/registry robot credentials, external OIDC/OAuth client material. MFA/TOTP/passkeys belong to the human IdP session; machine identities (AppRole/workload identity) stay distinct.
- **Ownership:** local deployments may keep managed credentials in the local OpenBao boundary (exportable/backup-eligible per rules). For remote control planes, target-side secrets stay on the target; a normal profile export must not download remote secrets; other machines reconnect via standard Target access; remote platform DR is separate. "Secrets live where they are needed. Profile portability must not become accidental secret replication."
- **Profile export/import:** versioned, provider-neutral (`baha export` / `baha import <bundle>`, naming per #603). Default export: non-secret profile state only (repository/source definitions, workspace mappings, movable Target definitions, contexts, non-secret trust/config references, credential references, schema metadata); never passwords/tokens/keys, OpenBao root/recovery/unseal material, runtime bearer tokens, short-lived mTLS identities or remote secrets. Opt-in secure export of eligible local durable credentials: encrypted, authenticated, strong KDF, passphrase never in argv/logs, integrity-protected and versioned, no plaintext intermediate, validate before mutation, import writes back into the protected store, explicit fail-closed conflicts, never show secret values. UX: "Include securely stored local credentials? [Yes] [No]".
- **Multi-device:** independent local machines each have their own runtime, OpenBao state and workspace; export/import only to move managed local state; existing native auth on the destination is reused, not overwritten. Shared remote targets keep credentials centralized; each machine needs only its own access identity.
- **Export/import ≠ backup/restore ≠ platform DR:** profile portability, application recovery (#399/#61) and control-plane recovery are distinct; they may share encrypted archive primitives but never become one "backup everything".
- **Recoverability:** secure local credentials participate in the local recovery strategy; OpenBao data and recovery/seal material are separate assets; recovery material is never embedded beside the only backup; restore verifies usability; short-lived identities are regenerated; unrecoverable external credentials are reported explicitly.
- **Console:** same credential-source model as CLI/JSON/MCP; no Console-only credential database; non-secret config → declarative/profile state, secrets → protected/OpenBao state.
- **Repository/artifact consumers** (Git, OCI registries, Harbor/Quay/GHCR, Artifactory/Nexus, Helm, Maven/npm/PyPI/raw) reuse the same credential-source semantics; this freezes the boundary, not every integration.
- **Security:** no secrets in intent, Git, logs/status/doctor/evidence; no persistence for session-only; native mechanisms first; never weaken TLS/auth to avoid a prompt; no remote secrets copied by default; no BaseHarbor account for local work; managed credentials have explicit ownership/scope/rotation/revocation; imported bundles are untrusted until validated.
- **Parity:** one domain model for credential source, persistence choice, ownership, exportability, import result/conflict and secret-safe diagnostics; MCP never receives raw secrets because the human CLI can prompt; secret-taking operations use safe input channels and sensitivity metadata.
- **Team onboarding with external corporate SSO (2026-10-06, consolidates #803):** an administrator configures the team destination once; a colleague receives a non-secret Target reference/profile, reuses native access, signs in through the corporate IdP only when needed. No repeated issuer/client-ID/OpenBao questionnaire, shared admin token, mandatory managed Keycloak or BaseHarbor user directory. Attaching to an existing Target and administrator bootstrap are separate; attach never creates a second OpenBao/Keycloak. Semantics to settle: external OIDC as a complete path; trusted-local limited to the established boundary (an environment label cannot grant it); verified issuer+subject and stable group/app-role claims map to the existing policy model (SSO login alone grants nothing); distinct permissions for read/log, deploy/change, secret use/write, reveal, destroy and platform admin (JIT/break-glass stay #100); native kube auth, operator authorization and OpenBao permissions stay separate; the correct secret store is resolved through authoritative remote placement with no local/default fallback; no human OpenBao manager/root/AppRole credential is distributed; private store reachability without unprotected ingress; two machines refer to one stable destination with bounded conflict handling; Target references are versioned, trust-verified and cannot redirect credentials or run untrusted plugins; bounded session staleness and revocation; default export never copies remote secrets. Review finding at the time: the principal projection lacked group/role claims, dev classification was environment-based and bootstrap defaulted to managed Keycloak — to be resolved and proven; #769/#770 are foundations, not proof.
- **Managed Identity administration (2026-10-06):** teams may administer BaseHarbor access through the managed Identity provider (Keycloak reference) without external SSO: select/invite a user, assign a team/organization access profile for Targets/operations/scopes/environments, provide a minimal onboarding profile, change/revoke access within the installation boundary. Reuse #608/#609 role recommendations; profile assignment is not itself a grant. Path: CLI/Console/MCP/management HTTP → shared Core authn/authz/policy/audit → Identity provider management adapter → provider's native admin API (Keycloak Admin REST with least privilege). Not part of the Application Runtime REST API. The IdP stays authoritative for accounts, credentials, MFA and sessions; BaseHarbor manages only its own access relationships. Creation is explicit and idempotent; ambiguity fails closed; removal removes only owned grants. Minimal workflow belongs here; advanced governance stays #100.
- **Independent installations per security boundary (2026-10-06):** Dev and Prod are independent installations; no global authority, Baha-to-Baha traffic, federation or sync. A Target is runtime provider + access reference + scope; a management connection identifies the responsible Core. One installation may own several admitted Targets. Each managed deployment has one authoritative Core owner; local client metadata is cache. No implicit Dev→Prod trust, no store fallback across installations, clients never bypass Core to the node connector, a registered Target is not automatically authorized, profiles create neither reachability nor access.
- **Guided removal and offboarding:** small wizards that show impact and default to the least destructive option for BaseHarbor access removal, managed user disable/delete (only where BaseHarbor owns the account), Dev Remote device revocation, local connection/profile removal ("this workstation only" vs "revoke remotely and remove locally"), unused enrollment revocation and grant removal. Back/cancel never mutates; authorization and object state are revalidated at submit time.
- **Kubernetes boundary:** namespace-first by default; cluster-wide is a broader explicit scope; a namespace name alone is not a security boundary. Real Kubernetes bootstrap/runtime stays #102 (v0.7) and #320 (v0.8).
- **Dev Local vs Dev Remote (2026-10-06):** Dev Local runs Core and runtime on the workstation, zero ceremony. Dev Remote: the workstation is a client of a remote Core. Trusted Dev Remote onboarding is `baha import dev-remote.baha`, after which ordinary commands need no login, CA setup or repeated credentials while the device identity is valid. The enrollment bundle may contain Core endpoint/identity, pinned trust, one scoped (preferably mTLS) device identity, minimal scope and expiry/rotation/revocation metadata; never root/recovery/unseal material, provider admin credentials, remote app secrets or unrestricted host credentials; it is sensitive input. Each workstation gets its own revocable identity. The trusted mode must be explicitly issued by the installation, never inferred from an environment named `dev`. Shared/team/Test/Prod keep user/session flows.
- **v0.4.24 Core/Node/CLI handoff (2026-10-09):** test the final shipped commands and identities from #837/#846/#849; do not reimplement their transport or upgrade code.
- **Superseded section:** the source's "Core capability consistency" section ("Core = SQL + Secrets + Identity; Identity is a Core capability, not optional") conflicts with the later binding #872 correction in #155/#427 (2026-10-11: no unconditional SQL/Secrets/Identity bundle; footprint follows requested capabilities). The later correction wins; see [decision](../decisions/2026-10-15-capability-footprint-supersedes-fixed-core.md). Confirm when cutting tasks.

## Acceptance

### Developer UX
- Every normal onboarding/offboarding flow has a documented happy path with the minimum possible number of human decisions.
- No wizard asks for information already discoverable from the selected installation, profile, native toolchain or current state.
- Advanced authentication, trust and provider details are progressively disclosed rather than shown by default.
- Repeated daily developer operations do not require repeated login/credential prompts while valid reusable access exists.
- Dev Local and trusted Dev Remote remain materially simpler than shared/Test/Prod operation.
- CLI wording and Console flows optimize for developer intent first, implementation detail second.

### Frictionless local development
- Clean local Docker/Podman developer journey works without `baha login`.
- Existing Git credential helper authentication is reused without extra prompts.
- Existing SSH-agent/config authentication is reused without extra prompts.
- Existing local repository can be adopted without moving it.
- BaseHarbor-created clone defaults to `~/baseharbor/repos/<host>/<owner-or-group>/<repo>`.

### Runtime/target standards first
- Existing kubeconfig/context works without creating duplicate BaseHarbor credentials.
- Kubernetes exec/OIDC/client-cert authentication can remain authoritative.
- Architecture allows cloud-native credential chains without requiring a BaseHarbor-specific cloud login contract.
- Native access failure produces actionable guidance before offering managed storage.

### Temporary credentials
- Session-only credential is not persisted in Git, portable intent or OpenBao.
- Temporary secret files, if unavoidable, are owner-only and cleaned up.
- Normal output/logs do not expose the credential.

### Secure credentials
- Secure choice persists eligible credential material in the authoritative protected/OpenBao store.
- Future operations can reuse it without repeated credential prompts.
- Only references/non-secret metadata enter declarative/profile state.
- Rotation/revocation preserves the same repository/target logical reference.
- Secure local credentials are recoverable through the supported recovery model.

### Export/import
- Default export contains no secret values.
- Secure credential export requires explicit opt-in.
- Secret-bearing export is encrypted, authenticated and versioned.
- Import validates before mutation.
- Import restores secret material into the protected destination store.
- Conflicts are explicit and fail closed.
- Remote target secrets are not silently exported.
- Multi-device local setup can be recreated without requiring manual BaseHarbor state surgery.

### Lifecycle boundaries
- Developer profile export/import is documented separately from #399 Application Recovery Unit.
- Platform disaster recovery is not conflated with profile export.
- Short-lived runtime identities are regenerated rather than treated as portable developer credentials where appropriate.
- Recovery/seal material is handled separately from ordinary exported secrets.

### UX
- Existing authentication success causes no credential questionnaire.
- When input is required, the normal persistence choice is no more complex than secure-for-future-use vs session-only.
- Advanced authentication types/options appear only when needed.
- Human wording follows "as little as possible, as much as necessary."

### Cross-surface
- CLI/JSON/MCP/Console consume the same credential-source semantics.
- Machine surfaces remain secret-safe.
- No Console-only credential database or CLI-only credential behavior exists.

### Team onboarding and external SSO
- Local Docker/Podman works without login while shared remote dev denies anonymous/forged trusted-local access.
- New team member attaches the configured Target and uses external corporate SSO without managed Keycloak or per-user provider setup.
- Authenticated nonmember is denied; mapped developer cannot access another team/prod, reveal secrets or administer providers without permission.
- Wrong issuer/tenant/audience, missing/overage claims and expired sessions fail closed with actionable output.
- Same app on local and remote Targets uses different secret values correctly; no cross-target fallback or profile secret replication.
- Private secret-store access works through the supported access path without distributing manager credentials.
- Two clients observe one remote deployment/provider identity and safe conflicting-update behavior.
- Offboarding respects documented expiry/revalidation/revocation bounds.
- CLI/JSON/MCP/HTTP share decisions and actor attribution; onboarding is separate from bootstrap.
- Pre-freeze Core/HTTP/contract-fixture evidence is explicitly separated from real Kubernetes lifecycle implementation/acceptance in #102 (v0.7) and #320 (v0.8).

### Managed Identity administration
- A team using the existing BaseHarbor-managed Identity service can create/invite a colleague, assign an access profile and onboard them without external SSO.
- Profiles reuse organization/team configuration and support one or multiple Targets with explicit operation/scope/environment permissions.
- Account activation/password/MFA stays with the authentication service; no copied administrator token or second user database is needed.
- Provider management capabilities/permissions are checked before mutation; unsupported administration is actionable.
- Repeated onboarding is idempotent; ambiguous existing identities are rejected.
- Non-admin users cannot create users or grant/revoke access; profile tampering/import cannot elevate permissions.
- CLI/JSON/MCP/HTTP share Core authorization and provider-adapter behavior; Console has no independent identity/access store.
- Management operations are excluded from the Application Runtime REST API.
- Onboarding profile/reference contains no default secret/session export; any enrollment capability has the stated lifetime/recipient/replay protections.
- Access change/revocation is verified against effective permissions and documented stale-session bounds; unrelated identity/provider resources survive.
- General account/business-user administration for other applications remains out of scope.

### Guided removal and offboarding
- An operator can remove only BaseHarbor access without deleting the underlying managed Identity user.
- Managed-user deletion is a separate explicit guided action with impact review and permission check.
- A Dev Remote workstation can be revoked independently without affecting other workstations or remote application/platform state.
- Local connection removal cannot accidentally delete or revoke the remote installation.
- The wizard distinguishes local cleanup, remote device revocation and unused enrollment revocation.
- Back/cancel and failed authorization/state revalidation produce no partial destructive mutation.

### Topology and authority
- Topology documents independent local/Dev/Prod authorities, their admitted Targets, identity ownership and explicit secret-store placement.
- One installation supports multiple admitted Targets without one mandatory Core per Target; Target and management connection remain distinct.
- Two authorized workstations connected to the same installation observe one authoritative deployment/provider state and the same permitted Target references, with bounded conflict handling.
- Dev and Prod need no Baha-to-Baha traffic, registry/user/grant synchronization, shared administrator credential or Dev-owned dependency.
- The client connects directly to the selected authorized Core; network isolation is not bypassed by forwarding, profile import or cached metadata.
- Managed-Identity onboarding completes through account invitation/activation, scoped profile assignment and minimal profile import without external SSO, duplicate user storage or developer OpenBao setup.
- Anonymous shared-Dev access and environment-label-based trusted-local escalation are denied.
- Target listing and all operations enforce the selected installation's identity and operation/resource scope; Dev identities/sessions/profiles cannot implicitly authorize Prod.
- Copied/tampered profiles, equal local aliases and stale client metadata do not create grants or redirect credentials to an untrusted installation.
- Wrong/unavailable remote store fails explicitly; no cross-installation store fallback or default remote-secret export occurs.
- Grant/revoke is verified independently in each boundary, including documented stale-session bounds; no global offboarding guarantee is presented.
- Standalone local Docker/Podman use still works without remote services or login; native kube/Git/cloud authentication remains first-class.
- Namespace-first and explicit cluster-wide scopes are covered by contract fixtures and linked Kubernetes requirements, without claiming completed Kubernetes runtime acceptance.
- CLI/JSON/MCP/management HTTP and Console share Core policy, actor attribution and provider adapters; no independent Console identity/access store or Application Runtime management route is introduced.

### Dev Local and Dev Remote
- Dev Local works without login, onboarding bundle or remote Core.
- A fresh authorized workstation can connect to a trusted Dev Remote Core by importing one enrollment bundle and can immediately perform permitted operations without interactive login.
- Import validates Core destination/trust and bundle integrity before persisting or using credential material.
- The imported device identity is bounded, auditable, renewable and individually revocable.
- Two independently enrolled workstations can use the same Dev Remote Core and observe one authoritative remote state.
- Revoking workstation A does not revoke workstation B.
- No Core/OpenBao recovery/root material, provider administrator credential or remote application secret is included in the enrollment bundle.
- Secret-bearing import material is never emitted into logs, evidence, normal machine output or portable Application Intent.
- Trusted Dev Remote cannot be selected merely by naming an environment `dev`; it requires explicit installation policy/enrollment.
- Shared-team/Test/Prod onboarding continues to use authenticated user/session flows and does not inherit this trusted-device shortcut.

### v0.4.24 handoff
- Import/enrollment binds the local developer device to one explicitly selected management Core without treating that Core as a deployment Target. `baha use` selects the intended context; application placement remains a separate Target decision with deterministic explicit-argument precedence.
- A portable developer profile/enrollment bundle holds only Core/Target references, scope, public trust anchors and revocable device credentials as explicitly permitted; never exports OpenBao unseal keys, Keycloak provider-admin credentials, live SQL backups, etcd DCS snapshots or Patroni state.
- Local Dev remains usable without BaseHarbor login. Dev Remote uses Core-authorized device enrollment, scoped mTLS and optional organization OIDC; reconnect/renew/revoke/offboard follow the existing #846 Node/Target-access contracts, not a duplicate credential engine.
- Test a revoked/expired/imported-into-wrong-Core profile, foreign installation and multi-Core selection as negatives; fail closed with a secret-safe reason and concrete next action.
- Separate export/import for developer convenience from service backup/restore and disaster recovery. Provider recovery in #837/#845/#847/#848 remains installation-owned and requires independent verification; profile import is not a substitute.
- Human wizard, noninteractive CLI, JSON and MCP expose the same resolved authority, ownership, allowed next action and remediation. Console consumption does not introduce a second management authority.

### Team/access profile wizard (comment 2026-10-05)
- An authorized administrator creates a scoped team/access profile through name → Target multi-selection → rights → review, without provider/OpenBao configuration questions.
- Small, large and duplicate-name Target lists remain usable; search, keyboard selection, pagination and preserved selections are demonstrated.
- Effective rights per selected Target, installation identity and namespace/cluster-wide scope are clear before confirmation.
- Back/cancel, empty/no-match/denied/offline states and stale selection conflicts have actionable behavior and no unintended mutation.
- Profile creation, identity/group assignment and connection-profile export remain distinct; file import cannot confer server-side rights.
- Dev profile creation cannot enumerate or grant Prod access through another independent installation.
- Suggested roles/presets are understandable defaults, not a second identity directory or mandatory provider-specific role scheme.
- CLI and Console demonstrate the same wizard semantics; JSON/MCP execute the equivalent validated operation without prompts.

## Pre-freeze rule

Blocker for #174 semantic acceptance and #175 contract freeze. The v0.5 baseline must not freeze: login required for local development; BaseHarbor replacing Git/SSH/kubeconfig/cloud auth; profile export equal to application backup; remote secrets copied to developer machines by default; unrecoverable secure local credentials; product-specific repository credential models. Frozen rule: native standards first → work without login when safe → ask only when necessary → developer chooses temporary vs secure → secure means reusable, protected and recoverable → secrets stay at their ownership boundary.
