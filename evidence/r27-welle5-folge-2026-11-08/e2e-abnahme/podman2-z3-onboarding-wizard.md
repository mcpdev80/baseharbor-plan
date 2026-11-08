# E2E-Abnahme Podman-2 — Zelle 3 ONBOARDING-WIZARD

**Card:** 0427-e2e-podman2 (lane 175adce3)
**Date:** 2026-11-08
**Base (attestiert):** develop @ `0fe53052d00a8d440b499c66a6a65c0d54bae5a0` (PR#1438 merge_commit_sha)
**Host:** baha-podman-2 (192.168.6.107, rootless Podman 5.7.0)
**Binary:** ~/baseharbor-build/baha-0427 (built @0fe53052d)

## Ziel (Mission)
Onboarding-Wizard: Gefueter ablauf neuer user/org -> instanz, bundle-import, back/cancel/EOF
keine nebenwirkungen. `baha onboard --init-tenant` + wizard cancel/EOF pruefen (sicherheits-property).

## Ergebnis: WIZARD-CANCEL/EOF SAFETY — PASS; INIT-TENANT BLOCKED (umgebungs-gap)

### 3a Wizard cancel/EOF side-effect-frei — PASS (verifiziert)
Produktionsschnitt (cmd/baha/onboarding.go): Back/cancel/EOF abortet vor Commit; Commit ist der
einige Effect-Point. `onboard` fangt `onboardingwizard.ErrCancel` und gibt
`"Cancelled. No changes were made."` aus; EOF liefert `{"error":{"code":"internal_error","message":"EOF"}}`.

Live-Test auf host (stdin ueber SSH geleitet):

```
=== onboard attach with EOF (empty stdin) ===
What do you want to do?
  > attach - connect this workstation to an existing installation
    import - join with a device bundle or team profile you received
    owner - initialize or verify Core operator and tenant with OIDC
    remove - remove only this workstation's local connection (nothing remote changes)
Choice [attach]: {"contract_version":"v1","error":{"code":"internal_error","message":"EOF"}}
--- EOF EXIT:0 ---

=== onboard attach with cancel (stdin "q\\n") ===
Choice [attach]: Cancelled. No changes were made.
--- CANCEL EXIT:0 ---
```

Nebenwirkungsnachweis (keine dateien angelegt):
- `~/.cache/baseharbor/` existiert nicht (kein onboarding/connection-store).
- `find ~/.cache/baseharbor ~/.local/share/baseharbor -iname "*onboard*" -o -iname "*connection*"` -> leer.
- `whoami -e dev --target w0427-owner-missing` -> `Mode: trusted-local / Identity: local-operator` (unverandert).

Fazit: wizard cancel/EOF bleibt side-effect-frei; commit ist tatsaechlich der einzige Effect-Point.
Dies ist die eigentliche Sicherheits-eigenschaft der Zelle — bestanden.

### 3b onboard --init-tenant BLOCKED (umgebungs-gap, nicht reproduzierbar ueber SSH)
`baha onboard --init-tenant -e dev --target w0427-owner-missing --no-input`:
```
Error: discover operator OIDC provider: Get
"https://identity.localhost:42305/realms/bh-operators-dev/.well-known/openid-configuration":
tls: failed to verify certificate: x509: certificate signed by unknown authority
```
Wurzel: Operator-OIDC-Issuer = `https://identity.localhost:42305/realms/bh-operators-dev`.
Das leaf (CN=identity.localhost) wird von der **BaseHarbor Managed Service CA** signiert
(issuer=CN=BaseHarbor Managed Service CA, verifiziert via `openssl s_client`).
Diese Managed CA ist NICHT im system trust pool des Hosts installiert:
`/etc/ssl/certs`, `/etc/pki/ca-trust/extracted/pem`, `/usr/local/share/ca-certificates` enthalten
keine baseharbor-managed cert; `update-ca-trust` anchors leer. Go `oidc.NewProvider` verifiziert
gegen den system trust pool -> die signierte CA wird nicht anerkannt -> discovery failt.

Das ist derselbe Umgebungs-gap wie Zelle 2 (managed-ca-nicht-system-trust + browser/PKCE-pflicht).
Init-tenant ist der first-owner bootstrap, der ein echtes operator OIDC-login + PKCE-browser-callback
braucht — ueber SSH/PTY nicht throughspielbar.

## Fazit Zelle 3
- Wizard cancel/EOF safety (security property): PASS, live verifiziert, side-effect-frei nachgewiesen.
- onboard --init-tenant first-owner bootstrap: BLOCKED an managed-ca-tls (exakte fehlerzeile oben).
  Nicht reproduzierbar/umgehbbar ueber SSH; Keycloak-/CA-tiefensuche laut Owner-Auftrag fuer Lane VERBOTEN.
- Bug-karte fuer managed-ca-not-in-system-trust + browser/PKCE-gap wird (nicht als produkt-edit) gemeldet.
