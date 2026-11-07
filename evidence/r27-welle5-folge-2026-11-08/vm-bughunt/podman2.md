# baha podman2 — hand-festival UX-bughunt (card core-815)

- lane: 0427-003-podman2-bughunt (session 486b2d02, laptop)
- date: 2026-11-08 UTC (focus run)
- host: baha-podman-2 (=192.168.6.107, baha-runner-podman-2) — rootless podman 5.7.0, no docker, linger=no
- task: OWNER-DIREKTIVE 2026-11-07 ABEND: hand-festival auf echtem podman (rootless). User-Erfaltung komplett durchspielen. NUR baha-podman-2.
- scope heute: (B) brownfield quadlet/unit-neighbors + (C) UX native-auth + device-enrollment/lifecycle, destroy-after-aborted + consent-abort, snapshot-change-guard, profile/team-floors/managed-users.
- SCHREIBGRENZE: KEINE produkt-aenderungen, KEIN PR. Nur evidence-dateien (plan-repo) + vm selbst (container/ima anlegen/loeschen auf host, read-only respekt bei fremdem quellen).

## repo-rule compliance
- keine produkt-aenderungen, kein .github, kein PR, keine workflow-aktion.
- evidence liegt in baseharbor-plan (plan-repo), NICHT im produkt-repo.
- keine subagenten (owner-direktive 2026-11-04).
- binar vom develop-kopf 8a3f58d (go build), NICHT aus PRs/zweigen.

## PLAN

- host-attestation + binar vom develop-kopf (8a3f58d) bauen (done)
- brownfield: snapshot container/ima -> fremdes quadlet/systemd-unit + containern anlegen (read-only respekt) -> baha init/up/status/inspect beobachten, nichts loeschen
- UX: native-auth wizard, device-enrollment/lifecycle wizard (develop-stand), destroy-after-aborted + consent-abort (abbruch -> loeschbarer zustand), snapshot-change-guard
- profile/team-floors / managed-users ux (develop stand)
- befehle summieren, funde je klasse, vm aufrumen (down), vm-lock release, evidence publish + ls-remote
- END an 594fd2f5

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
