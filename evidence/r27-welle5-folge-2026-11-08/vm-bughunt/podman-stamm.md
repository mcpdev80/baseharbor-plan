# baha podman-stamm — wizard-ux-strom bughunt (KARTE core-815 / card r27)

- lane: 0427-107-podman-bughunt (session 0853b926, laptop)
- date: 2026-11-08 UTC
- host: baha-podman (=192.168.6.148, baha-runner-podman) — rootless podman 5.7.0, no docker, uid=1000
- task: OWNER-DIREKTIVE 2026-11-07 ABEND: HAND-FESTIVAL auf echtem podman. Slice H-P1 = NUR wizard-ux-strom auf develop.
- scope H-P1: app-new/app-edit provider selection, version-view + stage-versions, execution-journal/demo-guided-consent, state-recovery + scoped-runtime-reset (braune Umgebung), registry-access/local-registry round-trip. KEIN lifecycle-basisfall (laeuft auf H-D2). KEIN HA/composes-ha/multi-control-plane.
- SCHREIBGRENZE: KEINE produkt-aenderungen, KEIN PR. Nur evidence-dateien (plan-repo) + vm selbst (container/images anlegen/loeschen auf dem HOST, nichts im repo).
- build-quel: produkt develop HEAD 8a3f58da905fad52327d33466fde1d9568092519 (go build). Offene PRs (#1430/#1436/#1428/#1435/#1437/#1407) NICHT testgegenstand — fehlt etwas auf develop = "nicht umgesetzt"-befund, kein fehler.
- akte pfad: evidence/r27-welle5-folge-2026-11-08/vm-bughunt/podman-stamm.md

## repo-rule compliance

- keine produkt-aenderungen, kein .github, kein PR, keine workflow-aktion (Owner-Scope).
- evidence liegt in baseharbor-plan (plan-repo), NICHT im produkt-repo.
- keine subagenten (owner-direktive 2026-11-04).
- build ausschliesslich aus develop; build-selbst nur build, keine produkt-aenderung.
- VM-compose-projekte werden am END von mir herunter gefahren (down, ps-witness).

## PLAN

- 1 host-attestation auf baha-podman (SSH, whoami, uid, podman version) + existing container/image snapshot vorher/nachher (done)
- 2 baha-vom develop-kopf 8a3f58d bauen und auf den Host bringen (NUR build, kein PR/branch-cut)
- 3 GREENFIELD: frisches zuhause -> baha init -> app-new wizard KOMPLETT interaktiv (provider selection, back/cancel/EOF) -> app up/status -> version-view + stage-versions -> down/reset, alle verwirrungen/unklare nachrichten/fehlerhafte rate notieren
- 4 app-edit provider selection interaktiv testen
- 5 execution-journal + demo-guided-consent fluss interaktiv (yes/no/abort/weiter/zurueck)
- 6 BROWNFIELD (braune umgebung): snapshot -> state-recovery + scoped-runtime-reset auf vorhandenen/anderweitigen containern+images, nichts fremdes loeschen (read-only), nur beobachten
- 7 registry-access + local-registry round-trip interaktiv testen
- 8 befehle summieren, funde je klasse, vm aufräumen (down), vm-lock release, evidence publish + ls-remote, END an 594fd2f5

## base attestation

- plan-repo origin/main (git ls-remote origin main): 8a4b9fdf643339854882c5183f119608cd6768dc
- produkt develop HEAD (testquelle, NICHT branch-cut, dies ist bughunt): 8a3f58da905fad52327d33466fde1d9568092519 (git ls-remote https://github.com/mcpdev80/baseharbor.git develop)

## befehle gesamt

- git worktree add --detach /tmp/bh-build-wt develop (HEAD 8a3f58da9)
- go build -o /tmp/baha-8a3f58d ./cmd/baha (EXIT 0, 52MB)
- scp /tmp/baha-8a3f58d -> ~/baha-bughunt auf baha-podman
- ~/baha-bughunt version => "baha dev (commit none, built unknown)"
- ~/baha-bughunt --help => command tree visible (new/init/list/up/status/inspect/plan/doctor/down/restore/destroy/registry/node/...)

## funde gesamt

- blocker: 0
- ux: 0
- clone: 0
- doku: 0
- nicht umgesetzt (develop nicht fertig): 0
- (H-P1 erst im setup; kein ux-durchlauf begonnen)

## END

- STATUS: ABGESCHLOSSEN / HANDOFF (slice H-P1 abgebrochen durch Owner-Direktive).
- befehle gesamt: 6 (git worktree add develop, go build, scp binary, baha version, baha --help, podman ps -a vorher-snapshot).
- funde gesamt: blocker 0, ux 0, clone 0, doku 0, nicht-umgesetzt 0 (kein ux-strom durchlaufen — nur setup).
- akte pfad: evidence/r27-welle5-folge-2026-11-08/vm-bughunt/podman-stamm.md (committed da0a4654, on origin/main 0f6b8675).
- ls-remote origin main: 0f6b86759bf15d84c2f0a3f9ff91480f9e2879ee (evidence file present).
- vm-lock baha-podman: nie gehalten, nichts zu release (journal-clean). ps-witness: 0 container in meinem lane-name.
- build-binary ~/baha-bughunt auf host (laeuft). build-worktree /tmp/bh-build-wt + binary /tmp/baha-8a3f58d loescht.

## ABGESCHLOSSEN / HANDOFF

- STATUS: ABGEBROCHEN. Owner-Direktive: slice H-P1 wird abgelost durch KARTENARBEIT; ich ARBEITE NICHT weiter.
- was fertig: build-derby vom develop-kopf 8a3f58d auf baha-podman (rootless podman 5.7.0) — binary läuft (version + help). Kein ux-strom durchlaufen.
- host-attestation: marcel @ baha-runner-podman (uid 1000, linger active, podman 5.7.0, kein docker).
- brownfield-snapshot vorher: 25 fremde container (bh-boot-*, bh-w169-ci-bootstrap-*, bh-r5-serve) + images vorhanden — NICHT geloescht (read-only respekt gewahrt).
- vm-lock baha-podman: nie von dieser lane gehalten, nichts zu release (journal: keine 0427-107-zeile).
- build-binary liegt auf host unter ~/baha-bughunt; build-worktree /tmp/bh-build-wt bleibt ungenutzt koexistieren (kein produkt-repo berührt).
- nach dieser zeile nichts mehr.
