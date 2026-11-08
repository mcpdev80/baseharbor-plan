# 0427-e2e-podman2 — Kontext-Sicherung (78%, 2026-11-08 ~02:10)

## TASK-SUMMARY
E2E-Abnahme des Integrations-Merge develop 0fe53052d (PR#1438) ALS REALER LAUF auf baha-podman-2.
Mission: /home/marcel/dev/baseharbor-ecosystem/coordinator/missions/0427-e2e-podman2.txt
4 Zellen: (1) SEEDING/#116, (2) NODE-ENROLLMENT, (3) ONBOARDING-WIZARD, (4) DOWN/RESET+cleanliness.
Evidence: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/e2e-abnahme/

## BASE-ATTESTATION
develop @ 0fe53052d00a8d440b499c66a6a65c0d54bae5a0 (PR#1438 merge_commit_sha). Integration-Kette
8a3f58da..0fe53052d nur eigene Commits. planning-repo origin/main = ac857c33.
Binary ~/baseharbor-build/baha-0427 (built @0fe53052d, go build OK).

## HELFER / PROTOKOLL
- SSH: `ssh -o BatchMode=yes baha-podman-2 '<cmd>'` (Alias -> 192.168.6.107, host= baha-runner-podman-2, rootless Podman 5.7.0).
- baha PTY-Fahrer: /tmp/pty_confirm.py (sendet "y\n" pro "[y/N]: "-Prompt) —上传 nach baha-podman-2:/tmp/pty_confirm.py.
- Keycloak admin (master): user=baseharbor-admin pass=b7d5c4145820f3d73f155cf213c362627517b7b155f2af314526e98464b8b440
  -> token curl. KEYCLOAK_BOOTSTRAP admin same creds (env KC_BOOTSTRAP_ADMIN_*).
- Zelle-1-Ergebnis: demoapp (reiner client-pfad, no sql) up -> app serves /healthz=ok + / via gateway -> PASS.
  demoapp destroy blockt an 2-stufiger impact-confirmation ([y/N] x2); --yes reicht NICHT.
- config.yaml operator-auth issuer -> https://127.0.0.1:42305/realms/bh-operators-dev (test-konfig).

## ZELLE 1 (SEEDING/#116): PASS
control-plane bootstrap OK; demoapp reiner client-pfad up READY (err=nil, preflight OK, exposure READY, serves /healthz).

## ZELLE 2 (NODE-ENROLLMENT): BLOCKED (Umgebungs-Gap)
- Operator-Realm bh-operators-dev + client baseharbor-cli-dev present.
- Blocker: operator direct-grant -> "Account is not fully set up" (HTTP 400).
  Wurzel: admin-cli token scope nur "email profile" (kein manage-users) -> credentials des Operator-Users
  via Admin-API null (kann kein password gesetzt werden). + Browser/PKCE-Pflicht ueber SSH nicht durchspielbar.
- Owner-Auftrag 2026-11-08: Keycloak-Tiefensuche fuer Lane VERBOTEN; nach korrekter config+curl -> BLOCKED + bug-karte.
- Evidence: evidence/r27-welle5-folge-2026-11-08/e2e-abnahme/podman2-z2-node-blocked.md (geschrieben).

## ZELLE 3 (ONBOARDING-WIZARD): OFFEN (naechster Schritt)
Gefueter ablauf neuer user/org -> instanz, bundle-import, back/cancel/EOF ohne nebenwirkungen.
`baha onboard --init-tenant` nutzt denselben operator login -> gleicher browser/PKCE-gap.
ABER: onboard hat auch non-init-tenant attach-pfad + wizard-cancel/EOF-schutz (keine nebenwirkungen).
Test: onboard --init-tenant (blockt evtl.), wizard cancel/EOF pruefen (muss nebenwirkungsfrei sein).

## ZELLE 4 (DOWN/RESET + CLEANLINESS): OFFEN
destroy loescht alles eigene incl. Keycloak (bugkarte 122). Host besenrein: container=0, volumes=0, df.
Cleanup: alle compose/containers OWN -> down (ps-witness) VOR END.
Baseline vorher: 0 container; ambient volumes pre-existing (24e436ff etc.).

## INTAKE-SEKTION (120/121/122) — STAND
- 120: PASS. origin/main=ac857c33; develop@0fe53052d verifiziert; Integration-Kette nur eigene Commits;
  host fresh (0 container, overlay/native-overlay-diff); ambient-volumes als Build-Baseline.
- 121: PASS. Scope=Verifikation (no product-edit/PR/runner-vm-infra). Write-set isoliert.
- 122: PASS. Beweismittel=git ls-remote(origin/main) via HTTPS; evidence-pfad=baseharbor-plan/evidence/...; END->codeman 594fd2f5.

## OFFENE ACTIONS / NEXT
1. Destroy demoapp sauber beenden (2 confirmations via pty_confirm.py) — container runtern.
2. Zelle 3: onboard wizard abspielen (cancel/EOF nebenwirkungsfrei), bundle-import.
3. Zelle 4: destroy full-reset (Keycloak etc. weg), cleanliness-zeile (container=0, volumes=0, df).
4. Evidence komplettieren (alle 4 zellen urteile + cleanliness).
5. evidence auf origin/main pushen (ls-remote vor push!).
6. END an codeman 594fd2f5-4e80-43b6-9841-92879146a85e mit je-karte-urteil + cleanliness-zeile.
   FORMAT: codeman agent post 594fd2f5-... "<END_DONE|END_BLOCKED> 0427-e2e-podman2: <1 line + sha>".

## WARNUNGEN (nicht vergessen)
- END VOR Stop posten. vm-lock release. evidence origin/main (nicht workers/baseharbor-plan!).
- Kein subagent. Kein produkt-edit. Kein PR/runner-vm-infra. evidence KEIN markdown-checkbox.
