# baha docker vm-lock claim/release — H-D4 bug-hunt akte

- lane: mission-hunt-hd4 (session 594fd2f5)
- shift: r27-welle5-folge-2026-11-08
- host: baha-docker-2 (=192.168.6.205, baha-runner-docker-2, Docker 29.9.3, rootless) — baha-docker belegt (mission-hunt-hd3), Owner-Freigabe: auf baha-docker-2 arbeiten, gleiche docker-schnitt
- vm-lock: baha-docker-2 OWN (594fd2f5, claimed 2026-11-08T09:45:29Z)
- produkt-stand: develop @ d30de3a4a176e073c8c1a9a0fc0b0ef06202b064 (git ls-remote origin develop)
- planning origin/main witness: 4e5af4a453d7df4dd27bc4eee058dde2414006bb (git ls-remote origin main)
- scope: KEIN produkt-code, KEIN PR, KEIN .github. Nur evidence (plan-repo) + vm selbst (container/volum/netz anlegen/loeschen).
- obj: brownfield/wiederhol-pfade auf baha-docker: zweites `baha up` auf bestehender app, `baha up` nach fehlerlauf (wiederhole denselben schritt), apply->abort->apply, target-wechsel (BASEHARBOR_TARGET) zwischen zweizielen mit geteiltem plan-read, status/list konsistenz nach jedem schritt.

## repo-rule compliance
- keine produkt-aenderungen, kein .github, kein PR, keine workflow-aktion.
- evidence liegt in baseharbor-plan (plan-repo), NICHT im produkt-repo.
- keine subagenten (owner-direktive 2026-11-04).
- binar vom develop-kopf d30de3a4a (go build).

## PLAN

- host-attestation + binar vom develop-kopf (d30de3a4a) bauen + auf host shippen (done)
- isoliertes app (hd4demo) + ziel-target angelegt; up/lifecycle-lock/candidate-consent code studiert (done)
- szenario 1: erste `baha up` auf bestehendem Core -> impact- + candidate-consent-gate abgebildet (done)
- szenario 0: hd4test-core bootstrap -> SQL+OpenBao ok, keycloak-netz subnetted (host-saturation finding) (done)
- szenario 1b: erste `baha up` auf hd4test -> teilrecorded deployment (DEGRADED), status/list konsistenz ok (done)
- szenario 1c: resume `baha up` -> preflight voll ok, workload-start failt -> image/build getestet (ok) (done)
- szenario 2: zweites `baha up` auf bestehender app (idempotence) — offen
- szenario 3: `baha up` nach fehlerlauf (denselben schritt wiederholen) — offen
- szenario 4: apply -> abort -> apply (interrupt, retry) — offen
- szenario 5: target-wechsel (BASEHARBOR_TARGET) zwischen zweizielen mit geteiltem plan-read — offen
- funde nach schwereklassen mit datei/befehlsgenauem repro (kommando+ausgabe+erwartung), positiv+negativ — offen
- host besenrein (destroy + down + cleanliness-zeile + ps-witness), vm-lock release, evidence publish + ls-remote origin/main, END — offen

## base attestation
- planning origin/main SHA: 4e5af4a453d7df4dd27bc4eee058dde2414006bb (git ls-remote origin main)
- produkt develop HEAD: d30de3a4a176e073c8c1a9a0fc0b0ef06202b064 (git ls-remote origin develop)
- binar: go build d30de3a4a, /tmp/hd4/baha auf baha-docker-2

## befehle gesamt
- (waehrend arbeit)

## funde gesamt
- blocker: (offen)
- host/brownfield: 1 (keycloak netz subnetted)
- lock/claim/release: (offen)
- status/list: (offen)
- doku/ux: (offen)

## BEFUNDE

### BF-hd4-1 (host/brownfield, mittel): Core-Identity (Keycloak) kann auf gesattigtem host KEIN netz anlegen — "all predefined address pools have been fully subnetted"
- schwereklasse: host-brownfield (mittel) — die management-core bootstrap-sequenz bricht am ende (openbao/SQL ok, keycloak-netz fehlt), ohne sichtbaren recovery-pfad fuer den user
- repro: `baha up --control-plane-only --yes` auf baha-docker-2 (hd4test, frisches target)
  - ausgabe (exakt):
    ```
    BaseHarbor control-plane runtime started
    [OK] OpenBao initialized and unsealed
    ...
    Error: Core identity failed: compose up -d --build --no-deps keycloak-1 keycloak-access: Network baseharbor-identity-core-hd4test Creating
    Network baseharbor-identity-core-hd4test-internal Creating
    Network baseharbor-identity-core-hd4test Error Error response from daemon: all predefined address pools have been fully subnetted
    network:identity-consumer failed to create network baseharbor-identity-core-hd4test: Error response from daemon: all predefined address pools have been fully subnetted
    ```
  - erwartet: keycloak-netz (baseharbor-identity-core-hd4test + -internal) angelegt -> Core READY
  - befund: postgres + openbao werden realisiert; keycloak scheitert an erschopften docker-adr-pools des WIRTLICH gesattigten hosts (40+ bh-w169/266/268/286-netze von anderen lanes). Der error ist inhaltlich korrekt (docker daemon), ABER: der user bekommt "Core identity failed" OHNE hinweis, dass ein netz-subnetting-konflikt der grund ist, und OHNE recovery-pfad. Die teilrealisierte installation (postgres+openbao running, keycloak stopped-but-owned) bleibt in einem zustand, in dem ein zweites `up` das keycloak-netz NICHT erneut anlegt (besteht ja "stopped-but-owned") — status zeigt DEGRADED.
  - gewicht: brownfield-mittel. Positiv: der fail-closed-zustand ist sauber (kein halber core mit vertrauen). Negativ: kein maschinenlesbarer/human recovery-hinweis auf netz-pools; recoverfaehigkeit nach diesem fehler ungetestet.

## END
(steht am ende der arbeit)
