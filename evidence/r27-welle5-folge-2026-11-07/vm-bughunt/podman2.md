# baha podman2 — hand-festival UX-bughunt (card core-815)

- lane: 0427-003-podman2-bughunt (session 486b2d02, laptop)
- date: 2026-11-07 UTC
- host: baha-podman-2 (=192.168.6.107, baha-runner-podman-2) — rootless podman 5.7.0, no docker, linger=no
- task: OWNER-DIREKTIVE 2026-11-07 ABEND: hand-festival auf echtem podman (rootless). User-Erfaltung komplett durchspielen. NUR baha-podman-2.
- scope: NEUAUFBAU/rauchprobe w283 erledigt. Jetzt INTERAKTIVES UX-Durchspielen: greenfield + brownfield + wizards + maintenance.
- SCHREIBGRENZE: KEINE produkt-aenderungen, KEIN PR. Nur evidence-dateien (plan-repo) + vm selbst (container/ima anlegen/loeschen auf host).

## repo-rule compliance
- keine produkt-aenderungen, kein .github, kein PR, keine workflow-aktion.
- evidence liegt in baseharbor-plan (plan-repo), NICHT im produkt-repo.
- keine subagenten (owner-direktive 2026-11-04).
- binar vom develop-kopf 8a3f58d (go build), NICHT aus PRs/zweigen.

## PLAN

- 1 host-attestation + binar vom develop-kopf bauen (done)
- 2 greenfield: fresh homedir -> baha init -> app new wizard KOMPLETT interaktiv (back/cancel/EOF) -> up -> status -> logs/inspect -> down -> reset, alle verwirrungen notieren
- 3 brownfield: snapshot container/ima -> quadlet/systemd-units + fremder containern -> init/up/status/down + wizards, nichts loeschen (read-only)
- 4 wizards: access-wizard, onboarding-wizard, maintenance-fluss interaktiv (yes/no/abort/weiter/zurueck)
- 5 befehle summieren, funde je klasse, vm aufräumen (down), vm-lock release, evidence publish + ls-remote
- 6 END an 594fd2f5

## base attestation
- origin/main SHA: 7423a1191df700a48267d5df970e1ba305b89ecc (git ls-remote origin main)
- produkt develop HEAD (testquelle): 8a3f58da905fad52327d33466fde1d9568092519 (baha build-quelle, NICHT branch-cut — dies ist ein bughunt, kein PR)
- kein PR/branch-cut noetig (schreibgrenze = kein PR)

## befehle gesamt
- (waehrend arbeit)

## funde gesamt
- blocker: 0
- ux: 0
- clone: 0
- doku: 0

## END
- (steht am ende)
