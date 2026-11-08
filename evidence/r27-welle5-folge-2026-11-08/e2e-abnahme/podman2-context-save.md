# 0427-e2e-podman2 — Kontext-Sicherung (85%, Zwang-Sicherung 2026-11-08 ~02:20)

## TASK-SUMMARY
E2E-Abnahme des Integrations-Merge develop 0fe53052d (PR#1438) ALS REALER LAUF auf baha-podman-2.
Mission: /home/marcel/dev/baseharbor-ecosystem/coordinator/missions/0427-e2e-podman2.txt
4 Zellen: (1) SEEDING/#116, (2) NODE-ENROLLMENT, (3) ONBOARDING-WIZARD, (4) DOWN/RESET+cleanliness.
Evidence: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/e2e-abnahme/

## BASE-ATTESTATION (DONE)
develop @ 0fe53052d00a8d440b499c66a6a65c0d54bae5a0 (PR#1438 merge_commit_sha). Integration-Kette
8a3f58da..0fe53052d nur eigene Commits. planning-repo origin/main = ac857c33.
Binary ~/baseharbor-build/baha-0427 (built @0fe53052d, go build OK).

## HELFER / PROTOKOLL
- SSH: `ssh -o BatchMode=yes baha-podman-2 '<cmd>'` (Alias -> 192.168.6.107, rootless Podman 5.7.0).
- Keycloak admin (master): user=baseharbor-admin pass=b7d5c4145820f3d73f155cf213c362627517b7b155f2af314526e98464b8b440.
- Zelle-1-Ergebnis: demoapp (reiner client-pfad, no sql) up -> serves /healthz=ok + / via gateway -> PASS.
- demoapp containers 2026-11-08 gestoppt+entfernt (podman stop -t0; podman rm -f). Host ohne demoapp.
- config.yaml operator-auth issuer = https://identity.localhost:42305/realms/bh-operators-dev.

## ZELLE 1 (SEEDING/#116): PASS
control-plane bootstrap OK; demoapp reiner client-pfad up READY (err=nil, preflight OK, exposure READY).

## ZELLE 2 (NODE-ENROLLMENT): BLOCKED (Umgebungs-Gap) — evidence geschrieben
- Operator-Realm bh-operators-dev + client baseharbor-cli-dev present.
- Blocker: operator direct-grant -> "Account is not fully set up" (HTTP 400).
  Wurzel: admin-cli token scope nur "email profile" (kein manage-users) -> credentials null.
  + Browser/PKCE-Pflicht ueber SSH nicht durchspielbar.
- Owner-Auftrag 2026-11-08: Keycloak-Tiefensuche fuer Lane VERBOTEN; nach korrekter config+curl -> BLOCKED + bug-karte.
- Evidence: podman2-z2-node-blocked.md (geschrieben, kein checkbox).

## ZELLE 3 (ONBOARDING-WIZARD): OFFEN — BLOCKER erkannt
- baha onboard --init-tenant nutzt denselben operator login -> operator OIDC discovery.
- ISSUER-FEHLER (aktuell): "tls: failed to verify certificate: x509: certificate signed by unknown authority".
  URSACHE: BaseHarbor Managed Service CA ist NICHT im system trust pool des Hosts; Go oidc.NewProvider
  verifiziert gegen system-trust -> die identity.localhost leaf (CN=identity.localhost) wird abgelehnt.
- Das ist derselbe Umgebungs-Gap wie Zelle 2. ONBOARDING-WIZARD init-tenant braucht echtes operator login
  (browser/PKCE) -> nicht ueber SSH throughspielbar.
- WICHTIG: onboard hat auch NON-INIT-TENANT attach-pfad + WIZARD-CANCEL/EOF-schutz (keine nebenwirkungen).
  Zelle-3-Urteil fokussiert auf: wizard cancel/EOF bleibt nebenwirkungsfrei (sicherheits-property).

## ZELLE 4 (DOWN/RESET + CLEANLINESS): OFFEN
- destroy via CLI blockt an readerIsTerminal=false (SSH/script) + 2-stufige impact-confirmation; --yes reicht nicht.
- demoapp-containeren bereits manuell gestoppt+entfernt. Zelle 4 = full-reset + cleanliness-zeile.
- Endzustand required: container=0, volumes=0, df; ps-witness VOR END.

## INTAKE-SEKTION (120/121/122) — ALLE DONE
- 120: PASS. origin/main=ac857c33; develop@0fe53052d verifiziert; Integration-Kette nur eigene Commits;
  host fresh (0 container, overlay/native-overlay-diff); ambient-volumes als Build-Baseline.
- 121: PASS. Scope=Verifikation (no product-edit/PR/runner-vm-infra). Write-set isoliert.
- 122: PASS. Beweismittel=git ls-remote(origin/main) via HTTPS; evidence-pfad=baseharbor-plan/evidence/...; END->codeman 594fd2f5.

## VM-LOCK
- Kein vm-lock file belegt (host war fresh, 0 container). Lock nur durch laufenden Lauf; vor END nicht belegt.

## OFFENE ACTIONS / NEXT (prioritaet: zelle 2/3/4 urteile + intake ENDE)
1. Zelle 3: ONBOARDING-WIZARD urteil. Wizard cancel/EOF nebenwirkungsfrei verifizieren (security-property).
   init-tenant blockt an operator-issuer-TLS (managed-ca-nicht-system-trust) -> dokumentieren.
   try: operator boundary via env BASEHARBOR_OPERATOR_OIDC_ISSUER + session-datei; sonst BLOCKED mit fehlerzeile.
2. Zelle 4: destroy full-reset (Keycloak etc.) -> cleanliness-zeile (container=0, volumes=0, df).
   destroy-cli blockt an readerIsTerminal -> evtl. manuell (schon fuer demoapp gemacht).
3. Evidence komplettieren: alle 4 zellen urteile + cleanliness in podman2.md.
4. evidence auf origin/main pushen (git ls-remote origin/main vor push!).
5. END an codeman 594fd2f5-4e80-43b6-9841-92879146a85e:
   codeman agent post 594fd2f5-... "<END_DONE|END_BLOCKED> 0427-e2e-podman2: <1 line + sha>".

## WARNUNGEN
- END VOR Stop posten. evidence origin/main (nicht workers/baseharbor-plan!). kein subagent/produkt-edit/PR.
- evidence KEIN markdown-checkbox.
