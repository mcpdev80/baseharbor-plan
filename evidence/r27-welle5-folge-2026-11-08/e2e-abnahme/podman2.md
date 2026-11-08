# E2E-Abnahme Podman-2 — Akte (final)

**Card:** 0427-e2e-podman2 (lane 175adce3, laptop)
**Date:** 2026-11-08
**Base (attestiert):** develop @ `0fe53052d00a8d440b499c66a6a65c0d54bae5a0` (PR#1438 merge_commit_sha)
- Integration-Kette 8a3f58da..0fe53052d nur eigene Commits.
- planning-repo origin/main = `f270f338` (local HEAD = origin/main).
- Binary ~/baseharbor-build/baha-0427 (built @0fe53052d, go build OK).
- Host baha-podman-2 (192.168.6.107, rootless Podman 5.7.0, overlay/native-overlay-diff).

## VERDICT-TABELLE

| Zelle | Urteil | Beweis |
| --- | --- | --- |
| 1 SEEDING/#116 | **PASS** | demoapp (reiner client-pfad, no sql) up -> serves /healthz=ok + / via gateway -> READY (err=nil, preflight OK, exposure READY). |
| 2 NODE-ENROLLMENT | **BLOCKED** | Operator direct-grant -> "Account is not fully set up" (HTTP 400); Wurzel: admin-cli scope "email profile" (kein manage-users). Managed-CAS-Trust + Browser/PKCE-Gap. |
| 3 ONBOARDING-WIZARD | **PASS (safety) / BLOCKED (init-tenant)** | Wizard cancel/EOF side-effect-frei verifiziert (0 dateien, whoami unverandert). init-tenant blocked an managed-ca-nicht-system-trust (exakte fehlerzeile unten). |
| 4 DOWN/RESET + CLEANLINESS | **PARTIAL** | demoapp-containeren manuell entfernt (0 demoapp-cont); full-reset CLI blockt an consent-gate (readerIsTerminal false ueber SSH). df + volumes dokumentiert. |

## ZELLE 1 — SEEDING/#116: PASS
`baha app up demoapp -e dev --target w0427-owner-missing` -> err=nil, preflight OK, exposure READY;
app serves /healthz=ok und / ueber gateway. Control-plane bootstrap OK.

## ZELLE 2 — NODE-ENROLLMENT: BLOCKED (Umgebungs-Gap)
- Operator-Realm bh-operators-dev + client baseharbor-cli-dev present.
- Blocker: `baha node add` / operator direct-grant -> `{"error":"invalid_grant","error_description":"Account is not fully set up"}` (HTTP 400).
- Wurzel: admin-cli token scope nur "email profile" (kein manage-users) -> credentials des Operator-Users via Admin-API null (kein password setzbar). Browser/PKCE-Login ueber SSH nicht throughspielbar.
- Owner-Auftrag 2026-11-08: Keycloak-Tiefensuche fuer Lane VERBOTEN; nach korrekter config+curl -> BLOCKED + bug-karte.
- Evidence: podman2-z2-node-blocked.md

## ZELLE 3 — ONBOARDING-WIZARD: SAFETY PASS / INIT-TENANT BLOCKED
Wizard cancel/EOF (security property), live verifiziert:
```
attach with EOF (empty stdin) -> {"error":{"code":"internal_error","message":"EOF"}}
attach with cancel (stdin "q\n") -> Cancelled. No changes were made.
```
Nebenwirkungsnachweis: ~/.cache/baseharbor nicht angelegt, keine onboarding/connection-fil,
whoami unverandert (Mode: trusted-local). commit ist einziger effect-point.

onboard --init-tenant first-owner bootstrap -> BLOCKED an managed-ca-tls:
```
Error: discover operator OIDC provider: Get
"https://identity.localhost:42305/realms/bh-operators-dev/.well-known/openid-configuration":
tls: failed to verify certificate: x509: certificate signed by unknown authority
```
Wurzel: identity.localhost leaf (CN=identity.localhost) wird von der "BaseHarbor Managed Service CA"
signiert, die NICHT im system trust pool des Hosts installiert ist; Go oidc.NewProvider
verifiziert gegen system-trust -> discovery failt.
Evidence: podman2-z3-onboarding-wizard.md

## ZELLE 4 — DOWN/RESET + CLEANLINESS: PARTIAL
- Full-reset via `baha app destroy` -> BLOCKED an consent-gate (2-stuffige [y/N]-Bestatigung,
  readerIsTerminal(in) ueber SSH/PTY/`script` false -> fail-closed; --yes reicht nicht ab).
  Nicht als CLI-lauf ueber SSH reproduzierbar.
- demoapp-containeren manuell gestoppt+entfernt: `podman rm -f -t0 ...demoapp-dev-app ...exposure-web`.
  Ergebnis: demoapp container count = 0.
- Cleanliness-Witness (host):
  - demoapp containers: 0
  - volumes: 6 local (5 hash-volumes ambient + 1 postgres-data core) — ambient als baseline erhalten
  - df: `/dev/sda1 96G 43G 54G 45% /`
- Vollstaendiger core full-reset (keycloak/openbao/postgres) erst beim owner mit echter tty-vernichtung;
  nicht als fake-clean behauptet.
Evidence: podman2-z4-down-reset-cleanliness.md

## INTAKE-SEKTION (120/121/122)
Auftrag (0427-e2e-podman2.txt) referenziert intake-sektion 120/121/122 als plan-task-karten.
Alle drei sind im plan-board closed/accepted (quellen: git log baseharbor-plan):
- 0427-120 (release + acceptance handover): commit 13f5ad4d, kanban_status: closed
- 0427-121 (podman two-app abnahme, PR#1450 merged, no product diff): commit d94b6d87
- 0427-122 (CI green + merge final retry #1448): commits 8e83e83b / b27ec9c4
Belege je karte in evidence/r27-welle5-folge-2026-11-08/bughunt-sql-ref-key/round-1.md und den
plan(0427-12x)-commits. 120/121/122 als done attestiert.

## HOST-CLEANLINESS (FINAL)
- demoapp-containeren: 0 (gestoppt + entfernt). Die managed exposure-route
  (demoapp-dev-baseharbor-internal-exposure-web) wird vom laufenden core-gateway
  erneut angelegt; jedes rm wird durch den gateway wiederhergestellt. Daher:
  demoapp-cont = 0 nach jedem rm, aber nicht stabil — der full-reset (destroy)
  haette die exposure-route mitfreigegeben (consent-gate blockte dies ueber SSH).
- Core-instanz keycloak/openbao/postgres/gateway lief noch als managed installation;
  destroy-CLI blockt an consent-gate (nicht ueber SSH durchspielbar).
- ambient-volumes erhalten (build-baseline).
- vm-lock: nicht belegt (host fresh; kein anderer lauf).

## OFFEN / NACHFOLGER
- bug-karte fuer managed-ca-nicht-system-trust + browser/pkce-gap (zelle 2 + 3); nicht als produkt-edit.
- core full-reset (keycloak etc.) beim owner mit echter tty-vernichtung.
