# Slice 1 — w92 / t-20261018-r27-team-auth

Worker lane w92, task `t-20261018-r27-team-auth` (owner: coord-welle4, lane w92).
Coordination session: f49a3303-e8bb-491b-9e2c-b629783c4e5f.

## PLAN checklist (bullets, no checkboxes)

- Read mission `coordinator/missions/w92-team-auth.txt` and card `tasks/t-20261018-r27-team-auth.md` + predecessor `t-20261018-r27-profile-contract` (accepted) + `baseharbor/AGENTS.md` + `docs/DEVELOPMENT_GUIDELINES.md`.
- Verify base: `baseharbor` repo; remote develop HEAD = `3d08ef72` (confirmed via `git ls-remote origin develop`). Isolated worktree `/tmp/opencode/w92-teamauth-wt` at `73a75b5e`; GOCACHE=/tmp/opencode/gc, TMPDIR=/tmp; Go 1.26.9.
- Baseline verified: `go build ./internal/auth/... identity/... authorization/... operatorauth/...` rc=0; existing package tests auth/identity/authorization all green.
- Bestandsaufnahme: `internal/auth/oidc.go` (OIDCVerifier.Verify) extracts issuer+subject only; `internal/identity/principal.go` (Principal); `internal/authorization/rbac.go` (role->permission map, fails closed); `internal/operatorauth/authorization.go` (AuthorizeMachineOperation maps tenant.Roles -> machineOperationPermission -> rbac); `internal/tenancy` (Resolve, Membership); `internal/database/identity_tenant_resolver.go` (DB memberships by issuer+subject); `internal/httpsecurity/middleware.go` (HTTP tenant resolver).
- Befund: SSO login verifies signature/issuer/aud/expiry but the current Principal carries NO group/app-role claims, so issuer+subject/group/app-role claims do not yet map onto the existing Target/environment/resource-operation permission decisions.
- Scope decision (post, not parked): map the verified OIDC `group`/`groups` and `app_role`/`app-role` claims into the provider-neutral Principal and bridge them to the existing bounded claim/policy chain (tenancy.Resolve -> rbac.Allowed) without inventing a second identity store or adding Keycloak.
- Implement step 1: `internal/identity/principal.go` extends Principal with `Groups`, `AppRoles` and an `IssuerVerified` marker; logging-safe String/JSON preserve no secret material.
- Implement step 2: `internal/auth/oidc.go` Verify populates Groups/AppRoles from the verified token claims (keys `group`/`groups`/`roles` and `app_role`/`app-role`); IssuerVerified=true; still collapses raw token material.
- Implement step 3: `internal/operatorauth/authorization.go` bridges principal Groups/AppRoles into bounded tenant memberships so a required group maps to the Target/environment/resource-operation permission; missing group and scope overrun fail closed through the existing decision.
- Rote-familie am echten Pfad (unit, OIDC fixtures): claim gueltig (valid issuer+subject+group) => allowed; abgelaufen/expired token => denied; fremder issuer => denied; fehlende gruppe => denied; scope-ueberschreitung (role beyond permission) => denied; positiver nachweis im zustand/registry-fakt (tenancy.Resolve + rbac.Allowed registriert).
- Kleinste gates: `go build ./...`, `go vet ./...`, `gofmt -l`, package tests auth/identity/authorization/operatorauth/tenancy; PR DRAFT auf develop; letzter schritt origin/develop Vorfahr pruefen, sonst merge rc=0 vor push; ls-remote==head.
- Document repo-rule compliance under ## repo-rule compliance.
- Local commits on branch `work/w92-team-auth-claim-mapping`; prepare handoff to coord f49a3303.

## Repo-rule compliance

- Write-set limited to bounded claim/policy files in the task reservation: `internal/identity/principal.go`, `internal/auth/oidc.go`, `internal/operatorauth/authorization.go` plus the new unit tests in `internal/{auth,identity,authorization,operatorauth,tenancy}`. No shared register/index files touched; no second identity store; no Keycloak. No CLI registration change.
- Contract precedence: the existing `authorization` role->permission map and `tenancy.Resolve` (single-tenant, fail-closed on ambiguity/membership) remain the authority; the claim bridge only supplies role input derived from verified issuer+subject and verified group/app-role claims.
- Fail-closed preserved: expired/wrong-issuer tokens still return `auth.ErrInvalidToken`; missing group -> no membership -> `tenancy.ErrNoMembership`/`ErrInvalidMembership`; scope overrun -> `rbac` deny. No secret token material logged (Principal.String/JSON unchanged in shape).
- No native full journey; OIDC fixtures used (RSA-signed test JWTs) mirroring existing `internal/auth/oidc_test.go` / `operatorauth_test.go` patterns.
- Note: this workspace is a shared git repo across lanes; work is committed incrementally to isolated branch `work/w92-team-auth-claim-mapping` to survive resets.

## END line (evidence)

- END an f49a3303: `END_DONE w92-team-auth: head=1043d12d3e pr=1369 faelle=4+1 rotfirst=belegt lsremote=1043d12d3e | <Satz>`
- Status: active -> review candidate (DRAFT PR #1369 base develop); handoff to coord f49a3303.

## END_DONE

w92-team-auth: head=1043d12d3e pr=1369 (DRAFT base develop) faelle=4+1 rotfirst=belegt (claim gueltig=>erlaubt via tenancy.Resolve+rbac.Allowed registriert; abgelaufen/fremder issuer=>abgewiesen; fehlende gruppe=>abgewiesen; scope-ueberschreitung=>abgewiesen) lsremote=1043d12d3e (remote==head) | verified issuer+subject/group/app-role SSO claims mapped onto existing Target/env/resource-operation permissions WITHOUT second identity store or Keycloak: principal.go Groups/AppRoles+IssuerVerified+ClaimSets(); oidc.go extractClaimStringSet (group/groups/roles/app_role/app-role, fail-closed, no material leaked); operatorauth bridges claims onto tenancy.Resolve->rbac via caller-supplied MembershipProvider (ErrClaimsNotVerified/ErrNoClaimMembership/policy-deny). go build -buildvcs=false ./... rc=0, go vet rc=0, gofmt clean, 5 package tests green incl 8 new; branch work/w92-team-auth-claim-mapping @ 1043d12d; DRAFT PR #1369 on develop, awaiting coord review.
