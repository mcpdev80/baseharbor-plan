# Audit: identity and access semantics (0428-046 / t-20261114-r28-cli2-audit-access)

- type: evidence (read-only audit)
- release: v0.4.28
- card: 0428-046
- task: t-20261114-r28-cli2-audit-access
- owner: lane-0428-046-r28
- produced: 2026-11-14 (shift 0428)
- candidate base: develop @ `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (product repo `mcpdev80/baseharbor`)
- evidence base: plan repo `origin/main` @ `6b34b1d96d583cb5407f0ca7d3b9c06c6b50c954`

## Scope and method

Read-only bestandsaufnahme of the current identity/access CLI surface on `develop @ 0e9ccb582`. No product edits were made (Merge-Frost). Sources: the owner working brief, command-map, and code-entry-index; the Core source tree checked out at `0e9ccb582`; Core `AGENTS.md` and `docs/DEVELOPMENT_GUIDELINES.md`. Every finding carries a `file:line` witness against the checked-out tree. The task note (card `0428-046`) and AGENTS 4.8 were followed: this session executed every step; no sub-agents were spawned.

Work plan recorded in the live board `workers/todos/mission-audit-access.md.json` (id/title/steps), the mission evidence `## PLAN` list below, and the task evidence.

## Summary of findings

- F1 (deviates / consent): `baha app creds ... --reveal` prints the real password and full connection URI in plaintext with only one consent gate and no audit write — violates brief "Reveal defaults masked; explicit --reveal" + guideline §6.
- F2 (deviates / audit): the identity/access mutation surface (`login`, `logout`, `whoami`, `access assign/offboard`, `user offboard`, `workstation new/revoke`, `onboard --invite/--import/--init-tenant`, `config organization`) writes no audit event. The audit registry is application-lifecycle-only.
- F3 (deviates / audit): the secret path itself is clean (never prints values), but the reveal surface (F1) and `app env --reveal` have no per-reveal audit; only set/list/delete are audited at the lifecycle layer.
- F4 (matches): `--init-tenant` correctly reuses the owner-bound OIDC+PKCE login transaction; the wizard never creates an independent admin.
- F5 (deviates / consistency): environment name still carries special cases (`dev` default; rank map `dev/development/test/staging/prod`); brief wants name-independent semantics.
- F6 (consistent / open): environment is addressed by name only (no per-environment UID); brief wants stable UIDs — not implemented yet.
- F7 (matches): `app creds --reveal` blocks JSON output (no credential leak via machine interface); plain-text path is the leak.
- F8 (matches / consistency): org-config is an org-level managed source (OCI/Git/local/system, immutable digest), never inline secrets; matches brief "provider registration ≠ authoring".
- F9 (matches): `whoami`/`login` fall back to `trusted-local` (no OIDC) for unmanaged envs; managed envs require a login session. Matches brief "no hardcoded dev rule, no account required when local access allows".
- F10 (matches): secrets are stored in the OpenBao-backed managed namespace, never in manifests/audit/output; set uses an input callback that keeps bytes out of DTOs.
- F11 (consistency risk): `onboard --import` redemption enforces one-use grant + symlink/public-ancestor refusal, but does not require an operator OIDC session on the developer workstation — intended by design, flagged for review.

## Per-command findings

### `baha access assign | access offboard`
- Command/flags: `baha access assign PERSON [--json]`, `baha access offboard PERSON [--json]` (children of root `access` group). Entry `access_wizard_command.go:34/109`; parse `output.go:17`.
- Authority/auth: folds every selection into the single production `orgconfig.Manager` via `loadAccessWizardAuthority` (fail-closed on incomplete config: `access_wizard_command.go:195-223`). Person is bound to the exact CLI subject via `validateAccessWizardPerson` before the authority is called (`access_wizard_command.go:254`).
- Audit: NONE. No `recordApplicationAudit`/`evidence.Append` call anywhere in `access_wizard_command.go`.
- Befund: AUTHORITY TREFFT / CONSENT TREFFT / AUDIT WICHT AB. A deliberate person→Target grant and its revocation are correctly authorized and fail-closed, but they leave no audit event. This is the single largest gap for the "present/missing audit" acceptance criterion.

### `baha user | user offboard`
- Entry `user_command.go:17/49`; `user offboard LOGIN [--yes]`.
- Auth: requires `openWorkstationAuthority` (locally owned Core host; OpenBao initialized/unsealed/owned; tenant bound) — `workstation_command.go:58-100`. `user offboard` disables Keycloak first, then revokes all stations with verify-at-each-step (`user_command.go:93-127`).
- Audit: NONE in `user_command.go` (line 94 only references the retained DB audit row, no new event).
- Befund: AUTHORITY TREFFT / AUDIT WICHT AB. Strong fail-closed ordering, no audit event.

### `baha workstation new | list | revoke`
- Entry `workstation_command.go:21`. `new`/`revoke` require the same managed authority; `revoke` verifies the new revoked state after writing (`workstation_command.go:313-321`).
- Audit: NONE.
- Befund: AUTHORITY TREFFT / AUDIT WICHT AB.

### `baha onboard --invite | --import | --init-tenant`
- Dispatch `onboarding_command.go:30-39`; `--init-tenant` reuses `operatorLoginCommand().Run` (same OIDC+PKCE+tenant transaction) `onboarding_command.go:191-192`; tenant bootstrap `onboarding_initial_tenant.go:19-66`.
- Auth: `--invite` creates a Keycloak user + one-use workstation invitation, temporary password, changed at first login (`onboarding_invite_command.go:100-163`). `--init-tenant` is restricted to the locally owned Core after real OIDC login (`onboarding_initial_tenant.go:14-18`). `--import` redeems the private one-use invite with one-use-grant + symlink/public-ancestor refusals (`onboarding_import_command.go:29-...`).
- Audit: NONE across the three modes.
- Befund: `--init-tenant` and `--import` behave per brief. `--init-tenant` correctly never stands up an independent admin (`onboarding_initial_tenant.go:14-18`). `--import` redemption requires no operator OIDC session on the workstation (design intent; flag for review). No audit events for any onboard mode.

### `baha login | logout | whoami`
- Group `operatorLoginCommand/logout/whoami` registered at root `commands.go:161-163`.
- Auth: unmanaged env → `trusted-local` (no OIDC required); managed env requires a verified OIDC session (`operator_auth.go:42-51`, `operator_operations.go:25-52`, `operator_auth_status.go:28-58`).
- Audit: NONE for login/logout/whoami.
- Befund: AUTHORITY TREFFT per brief (no hardcoded `dev` rule, local access allowed when unmanaged). No audit.

### `baha config organization`
- Entry `config_org.go:28`; subcommands `set|show|check|update`.
- Auth: org config is an org-level managed source (OCI/Git/local/system) with immutable digest, resolves references only, never stores plaintext secrets (`source.go:57-264`, `model.go:66-271`).
- Befund: TREFFT / consistent with brief "external provider registration is not provider authoring". This is an org/`platform` concern, not per-user identity.

### `baha app secret` (set/list/delete)
- Entry `app_secret.go:21`; mutations `secret_operations.go:21-91`.
- Secrets live in the OpenBao-backed managed namespace; set uses an input callback keeping bytes out of DTOs and zeroes them (`secret_operations.go:44-61`). Never printed in manifests/logs/audit/normal output.
- Befund: TREFFT. Secret value handling matches guideline §6. The bypass risk is only the reveal surface (F1), not the store.

### `baha app creds --reveal` — THE BYPASS
- Entry `app_access.go:96` (`baha app creds postgres|valkey [INSTANCE] [--app NAME] [--reveal]`).
- `--reveal` prints the real password + URI: `fmt.Fprintf(out, "PASSWORD=%s\nURI=%s\n", binding.Password, binding.URI)` at `app_access.go:129` (plain-text path only; JSON path is blocked at `app_access.go:116-118`).
- Authorization runs once, pre-reveal, in `resolveAccessBinding` (`app_access.go:215-245`): `authorizeApplicationOperation(ctx, "app.connection", resolved)` then `ResolveServiceBinding` reads the owner-only bindings file (`internal/application/access.go:27-90`). There is NO second consent gate for `--reveal`, no privileged-user re-check, and NO audit write (`grep recordApplicationAudit app_access.go` = none).
- Befund: WICHT AB / TREFFT-NICHT. The brief says reveal is masked by default and shown only with explicit `--reveal`; here the default is already masked, but the explicit reveal prints the plaintext secret through the human terminal with no second confirmation, no per-reveal audit, and no re-check that the caller is the owner on the owned Core. This is the clearest secret-exposure deviation in the slice. Guideline §6 ("secrets never enter normal machine output") is met for list/store but the reveal path is a terminal-only exception that is neither gated nor audited.

### `baha app env --reveal`
- Entry `app_env.go:17`; `inspectApplicationEnvironment` masks non-public fields by default (`app_env.go:108-130`) and unmasking with `--reveal` (`app_env.go:32-36`).
- Audit: NONE (`grep recordApplicationAudit environment_operations.go` = none).
- Befund: consistent with the brief's "Reveal defaults masked; explicit --reveal". Same audit gap as F2.

### Environment UID and name special cases
- Default environment is `"dev"` in many places (`onboarding_command.go:142`, `onboarding_import_command.go:226`, `tui_remote.go:31`, `serve_operator_oidc.go:39`, ...).
- Destroy-authorization picks the most protected registered environment via a rank map: `ranks := map[string]int{"dev":0,"development":0,"test":1,"staging":2,"stage":2,"prod":3,"production":3}` (`runtime_destroy_authority.go:76`).
- Befund: WICHT AB vs brief "environment names unrestricted by fixed dev/test/prod semantic special cases". The rank map hard-codes the very semantics the brief wants removed; it is used only for destroy authorization (favor the most protected), which is defensible, but the pervasive `"dev"` default and the rank map are still name-semantic special cases. Environment is addressed by name only (no stable per-environment UID): `resolveApplicationEnvironment` uses `selection.Manifest.Environment` (`app_context.go:110-...`); stable UIDs (brief) are not implemented.

### `app pull` / `--up` naming
- `code-entry-index.md`/`command-map.md` reference `baha app pull` and `--up` (proposed).
- In the checked-out tree `app pull` does not exist; source update is `baha app update` (`app_update.go:44`), and `--up` appears nowhere (`grep --up` = none).
- Befund: CONSISTENCY RISK / naming gap. The proposed `app pull`/`--up` mapping is not yet realized; current source uses `app update`. Do not treat `app pull --up` as current behavior.

## Trust/consistency risks

- The identity/access mutation surface (assign/offboard/offboard/workstation/onboard/login/logout/whoami/org) writes no audit event, while the audit registry (`recordApplicationAudit` + `internal/evidence`, 10 call sites in `cmd/baha`) is application-lifecycle-only (`app_apply.go`, `app_lifecycle.go`, `app_update.go`, `app_backup_metadata.go`, `app_doctor_repair.go`, `application_restore_metadata.go`, `app_runtime_retirement.go`, `app_remote_lifecycle.go`, `repository_up.go`). This is the headline finding.
- The single most severe secret-exposure path is `baha app creds --reveal` (F1): plaintext password + full URI, one gate, no audit.

## Repo-rule compliance

- Read-only: no product file was created, changed, deleted or reverted. Merge-Frost respected.
- No plan-repo product writes outside this akte; this file is the only addition in the evidence dir for this slice.
- No sub-agents (AGENTS 4.8). All sources measured from the checked-out tree at `0e9ccb582`.
- VM/runner/CI: none invoked. No containers, no GitHub-hosted runs.
- Stray artifact observed in the evidence dir this shift: `evidence/cli-redesign-20261114/cleanup28-r1/round-1.md` (created 2026-11-14 20:53, not owned by this lane). Left untouched; reported here for the coordinator to attribute.

## Evidence witnesses (checked-out tree @ 0e9ccb582)

- plan repo origin/main head: `6b34b1d96d583cb5407f0ca7d3b9c06c6b50c954`
- product develop head: `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`
- `access_wizard_command.go:34,109,254` — authority + person binding; no audit
- `user_command.go:17,49,93-127` — fail-closed offboard; no audit
- `workstation_command.go:21,58-100,313-321` — managed authority; no audit
- `onboarding_command.go:30-39,142,191-192`; `onboarding_initial_tenant.go:14-66` — --init-tenant reuses login, local Core only
- `onboarding_invite_command.go:100-163`; `onboarding_import_command.go:29` — invite/import redemption
- `operator_auth.go:42-51,140-141`; `operator_operations.go:25-52`; `operator_auth_status.go:28-58` — trusted-local vs managed
- `config_org.go:28`; `internal/orgconfig/source.go:57-264`; `model.go:66-271` — org config, no inline secrets
- `app_secret.go:21`; `secret_operations.go:21-91` — managed namespace, no value leak
- `app_access.go:96,116-118,129,215-245`; `internal/application/access.go:27-90` — `--reveal` plaintext password/URI, one gate, no audit
- `app_env.go:17,32-36,108-130` — mask/default reveal, no audit
- `runtime_destroy_authority.go:76` — env rank map (name special case)
- `onboarding_command.go:142` — default env `dev`
- `commands.go:161-163` — login/logout/whoami group; `commands.go:229-245` — flat app data (no `app data` group); `app_update.go:44` — current update command (no `app pull`/`--up`)
- audit registry call sites: 10 files in `cmd/baha`, application-lifecycle only

## PLAN (work list)

- Read mission + brief/command-map/code-entry-index; verify plan repo remote (origin/main = 6b34b1d9)
- Confirm card 0428-046 state=active, owner lane-0428-046-r28; claim not needed (active)
- Clone baseharbor to /tmp and check out develop@0e9ccb582 for source tracing
- Audit access identity commands: access/onboard/user/workstation/grants/org + auth, secrets reveal/audit, env UID + name special cases
- Per-command findings (matches/deviates/consistency-risk) with file:line witnesses
- Write akte evidence/cli-redesign-20261114/audit-access.md; ls-tree witness
- Push plan main; publish card to review; END via send

## END

- lane: lane-0428-046-r28
- status: DONE (audit complete; akte written, ready for review handoff)
- candidate SHA: develop @ 0e9ccb582f5bdcdc74049bbe3996263cdce6500c
- note: read-only audit, no product changes; card to be moved to review by coordinator.
