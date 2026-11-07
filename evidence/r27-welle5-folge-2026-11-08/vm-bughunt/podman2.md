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

## BEFUNDE

### BF-1 (UX, blocker-faellig): app new endet mit widerspruechigem Exit "Created X" + "Error: installation must be restored"
- Schwereklasse: ux (hoch) — der wizarddruckt ERFOLG ("Created gfapp, Location: ~/gfapp, Stack: go, Validation: SATISFIED") UND GLEICHZEITIG EINE ERROR ("project created but Target preference registration incomplete: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable").
- Repro: `$B app new` interaktiv (name=gfapp, stack=Enter, mode=create-only, confirm=y) mit BASEHARBOR_TARGET=w268 auf baha-podman-2 (Coreless tenant target, keine Core-Installation vorhanden).
- Befund: Projekt-DATEIEN werden angelegt (baseharbor.yaml etc. existieren, inspect moeglich), aber der wizard verlaesst den prozess mit einem Zustand, der eine restoration verlangt — ohne dass ein wiederherstellungs-pfad fuer den user sichtbar ist. Exit-code nicht erfasst (probe-schnitt). Konsistenzproblem: erfolgsmeldung + fehler in EINEM aufruf.
- Minimal repro (produktseitig): Target ohne installierte Core-Installation (Coreless) + `baha app new`/`baha up` -> Error ErrDeploymentOwnerMissing (internal/deployment/deployment_store.go:25), abgefangen in cmd/baha/app_new_wizard.go appNewCreateFromWizardDecision -> finishAppNewWizard, der "Created X" bereits geschrieben hat.
- Offene frage: ist der app-stand nach diesem fehler usebar (manifest ist vorhanden) — d.h. der wizard hinterlaesst ein halbfertiges, aber prinzipiell valides projekt, ohne den user zu leiten. Gewicht:UX-hoch, ggf. blocker, wenn kein recovery-pfad.

### BF-2 (doku/ux, mittel): app init / status / doctor schlagen fehl mit "multiple deployment targets configured" fuer repo mit bestehendem baseharbor.yaml
- Repro: cd ~/demo (besteht, baseharbor.yaml vorhanden) -> `$B app init --quick` -> Error "multiple deployment targets configured". Auch `$B status` -> "Application identity has not been initialized" (benotigt interaktiven init). `$B inspect` funktioniert aber sauber.
- Ursache: selectedTargetName (cmd/baha/target_selection.go:84) faellt closed, wenn kein persisted/activated/default target UND >1 target in config (w268 + w0427-owner-missing + local). Der wizard kann den target nicht waehlen (kein interaktiver selector im new-flow), es faellt hard-closed.
- Befund: fuer ein repo mit bestehendem manifest gibt es KEINE nicht-interaktive rueckfalle, die den target akzeptiert; der user muss BASEHARBOR_TARGET setzen oder `baha use` — beides nicht aus der fehlermeldung ersichtlich. Gewicht: doku/ux-mittel.

### BF-3 (confirm-abort, NICHT belegt als bug): "n" bei "Create project files only [Y/n]" hinterlaesst kein projekt (korrekt)
- Verifiziert: wizard loop auf appWizardNo (phase->Needs), auf EOF -> abort -> "No changes were made", kein app-dir. frueherer schein-befund ("consentapp" trotz n) war ein testfehler (mein script sendete y).
- => consent-abort verhaelt sich korrekt; kein fund.

### BF-4 (brownfield, beobachtung): host ist voller brownfield-quadlet-state (110 .container/.scope files)
- ~/.config/containers/systemd/: 110 quadlet-dateien (baseharbor-* app-owned + bh-*shared* fuer w266s/w268/podman-local/podman-local2).
- systemd --user list-units: baseharbor-postgres*.service etc. als "generated" (from podman-user-generator), status "failed" (keine running container — clean teardown).
- Befund: baha inspect/status/doctor laufen in diesem umfeld OHNE fremde containern anzutasten (read-only beobachtet). KEIN produkt-befund, nur kontext-festhaltung fuer nachfolger.
- VM-hygiene: diese quadlet-state NICHT geloescht (bh-*shared* + fremde targets = read-only respekt, owner-scope).

## VM-HYGIENE / RECHNER-SÄUBERUNG (beweis)
- host: baha-podman-2 (rootless podman 5.7.0)
- vorher container: 0 (keine lane-eigenen running) ; nachher: 0
- bh*/w*/gfapp/ecapp/demo volumes: 0 (keine eigenen — die 5 local-driver volumes sind ambient-podman-state, nicht angefasst)
- netzwerke: 1 (podman bridge = basis, nicht angefasst)
- images: 6 (ambient-core, nicht angefasst; kein system prune)
- ~/.local/share/baseharbor*: keine state-zenisse von mir (observability/ nur ambient)
- test-app-dirs ~/gfapp ~/ecapp ~/demo ~/aborttest ~/decline ~/consentabort ~/gf ~/hf ~/create-only ~/y: alle entfernt
- /tmp-testreste: keine lane-eigenen (nur /tmp/opencode/baha-clone build + drive-helfer, host-seitig, nicht produkt)
- vm-lock baha-podman-2: RELEASED (FREE host=baha-podman-2, coordinator journal)
- cleanliness: 0 container, 0 volumes (mine), df 44%

## END
- END_BLOCKED 0427-003-podman2-bughunt: teilststand — wizard-exit-konsistenz (BF-1, ux-hoch) + target-resolution-doku (BF-2, doku-mittel) + brownfield-kontext (BF-4, beobachtung) dokumentiert; kein fix (schreibgrenze = kein PR/produkt-aenderung). vm-lock released, akte auf origin/main (commit aac4d0d2, ls-remote 50a4e175), rechner gesäubert (cleanliness: 0 container). nachfolger bearbeitet fund.
