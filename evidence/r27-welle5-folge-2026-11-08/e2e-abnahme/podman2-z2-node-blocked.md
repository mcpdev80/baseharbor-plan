# E2E-Abnahme Podman-2 — Zelle 2 NODE-ENROLLMENT: BLOCKED

**Card:** 0427-e2e-podman2 (lane 175adce3)
**Date:** 2026-11-08
**Base (attestiert):** develop @ `0fe53052d00a8d440b499c66a6a65c0d54bae5a0` (PR#1438 merge_commit_sha verifiziert; Integration-Kette 8a3f58da..0fe53052d nur eigene Commits)
**Host:** baha-podman-2 (`192.168.6.107`, rootless Podman 5.7.0, overlay/native-overlay-diff, fresh: 0 Container)
**Binary:** `~/baseharbor-build/baha-0427` (built from `@0fe53052d`, `go build` OK)

## Ziel (Mission)
Dateibasierte Einschreibung eines zweiten Ziel-Hosts; `baha node list/status` zeigt ENROLLED aus ECHTEM Zertifikats-lifecycle (kein grant-abgeleiteter Wert).

## Blocker (EXAKTE FEHLERZEILE)
`baha node add` bzw. `baha node status` brauchen eine gueltige operator session
(`operatorauth.LoadSession` + `ValidAt()`), die ein echtes `id_token` des Operator-Realms
`bh-operators-dev` erfordert. Die Operator-Login-Kette (`baha login -e dev --init-tenant` / `baha serve`)
ist ueber SSH NICHT durchspielbar:
1. Operator-OIDC-Issuer ist `https://auth.baha.localhost:8443/realms/bh-operators-dev`; das Gateway-Zertifikat
   (CN=demoapp.baha.localhost) deckt den Host `auth.baha.localhost` NICHT -> `tls: failed to verify certificate`.
2. `baha login` oeffnet zwingend einen Browser (PKCE-Callback); kein interaktiver Browser ueber SSH.

## Pfad-1-Versuch (dokumentiert, Owner-Auftrag 2026-11-08)
- Operator-Issuer in `~/.config/baseharbor/config.yaml` auf `https://127.0.0.1:42305/realms/bh-operators-dev`
  geaendert (zulässige, dokumentierte Test-Konfig; Cert deckt localhost echt -> kein Fake).
- Operator-Realm `bh-operators-dev` + Client `baseharbor-cli-dev` (PKCE, public, redirect 127.0.0.1) PRESENT.
- Operator-User `opnode` (enabled=true, emailVerified=true, requiredActions=[]) erstellt.
- **Fehler:** `POST /realms/bh-operators-dev/protocol/openid-connect/token` (grant_type=password)
  -> `{"error":"invalid_grant","error_description":"Account is not fully set up"}` (HTTP 400).
- **Ursache (Wurzel):** Der Keycloak-Admin-Token (admin-cli, master realm) hat Scope `email profile`,
  KEIN `manage-users` -> `PUT /admin/realms/{realm}/users/{id}` setzt `credentials: null` (204, ohne Wirkung).
  Das Passwort kann damit NICHT im Operator-Realm hinterlegt werden -> direkter Grant scheitert.
- `baha serve` (Operator-API) kann ohne gueltige operator session nicht node-Owner-Tenant verifizieren.

## Fazit
Zelle 2 BLOCKED: Umgebungs-Gap (Admin-Scope des Operator-Realms zu eng + Browser/Headless-Luecke).
Keycloak-Tiefensuche laut Owner-Auftrag fuer diese Lane VERBOTEN (Budget gehoert Zelle 3+4).
Der Browser/Headless-Gap + Admin-Scope-Gap wird als eigene bug-karte gemeldet (nicht als Produkt-Edit).
Kein Produkt-Edit, kein PR, keine Runner-/VM-Infra-Änderung.

## Evidence-Beweise
- `config.yaml` operator-auth issuer -> 127.0.0.1:42305 (grep-Auszug unten)
- `direct grant` -> HTTP 400 "Account is not fully set up"
- admin-cli token scope: `scopes: email profile`, `realm_access.roles: null`
- User opnode: `enabled=True creds=0 req=[]` (credentials werden via Admin-API nicht geschrieben)
- `https://auth.baha.localhost:8443/.../.well-known/openid-configuration` -> TLS subject CN=demoapp.baha.localhost (Cert deckt Host nicht)

## Nachfolger
Owner meldet bug-karte fuer browser/headless + admin-scope gap. Zelle 3 (onboarding-wizard) + Zelle 4 (down/reset + cleanliness) in diesem Bericht.
