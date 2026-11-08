# baha vm-lock claim/release + brownfield/wiederhol-pfade — H-D4 bug-hunt akte

- lane: mission-hunt-hd4 (session 594fd2f5)
- shift: r27-welle5-folge-2026-11-08
- host: baha-podman-2 (=192.168.6.206, baha-runner-podman-2, Podman 5.7.0, rootless) — baha-docker belegt (mission-hunt-hd3), baha-docker-2 net-pools erschopft, Owner-Freigabe: auf baha-podman-2 (free podman network space)
- vm-lock: baha-podman-2 OWN (594fd2f5, claimed 2026-11-08) -> RELEASED beim END
- produkt-stand: develop @ d30de3a4a176e073c8c1a9a0fc0b0ef06202b064 (git ls-remote origin develop)
- planning origin/main witness: cde090afa8622a2032b3579abffaf11f14267b3b (git ls-remote origin main)
- scope: KEIN produkt-code, KEIN PR, KEIN .github. Nur evidence (plan-repo) + vm selbst.
- obj: brownfield/wiederhol-pfade: zweites `baha up` auf bestehender app, `baha up` nach fehlerlauf (wiederhole denselben schritt), apply->abort->apply, target-wechsel (BASEHARBOR_TARGET) zwischen zweizielen mit geteiltem plan-read, status/list konsistenz nach jedem schritt.

## repo-rule compliance
- keine produkt-aenderungen, kein .github, kein PR, keine workflow-aktion.
- evidence liegt in baseharbor-plan (plan-repo), NICHT im produkt-repo.
- keine subagenten (owner-direktive 2026-11-04).
- binar vom develop-kopf d30de3a4a (go build), /tmp/hd4/baha auf host.

## PLAN
- host-attestation + binar vom develop-kopf (d30de3a4a) bauen + shippen (done)
- host-saturation befund: baha-docker-2 docker net-pools exhaustion -> baha-podman-2 (done)
- Core bootstrap hd4test-pm (podman): Core READY SQL+Secrets+Identity (done)
- first up hd4demo: app READY (pg verified, workload ready, exposure ready, dev URL) (done)
- szenario 2: zweites baha up (idempotence): "source unchanged", app READY (done)
- szenario 3/4: up nach SIGKILL-mid-workload -> DEGRADED, resume up -> READY (lock re-acquired) (done)
- szenario 5: target-wechsel BASEHARBOR_TARGET (hd4test-pm vs hd4test-pm2) aus spec: status/list konsistenz (done)
- funde nach schweklasse mit datei/befehlsgenauem repro, pos+neg (done)
- destroy apps + teardown (stop/remove mine containers/nets/vols), cleanliness, lock release (done)
- evidence publish + ls-remote origin/main (in Arbeit)

## base attestation
- planning origin/main SHA: cde090afa8622a2032b3579abffaf11f14267b3b (git ls-remote origin main)
- produkt develop HEAD: d30de3a4a176e073c8c1a9a0fc0b0ef06202b064 (git ls-remote origin develop)
- binar: go build d30de3a4a, /tmp/hd4/baha auf baha-podman-2

## BEFUNDE

### BF-hd4-1 (brownfield/host, HOCH): "all predefined address pools have been fully subnetted" blockiert `baha up`/Core-bootstrap auf gesattigtem docker-host — kein baha-logic-bug, sondern docker-netz-pools erschopft
- schwereklasse: brownfield (hoch, blocker-faellig) — ein zweiter `baha up`/Core-bootstrap auf einem host mit erschopften docker-netz-pools bricht am netz-anlegungs-fehler, OHNE maschinenlesbaren recovery-hinweis; der user sieht "Core identity failed" bzw. "The application workload failed to start", aber nicht, dass netz-pools exhaust sind.
- repro (docker, baha-docker-2, hd4test frisches target):
  - `baha up --control-plane-only --yes`:
    ```
    [OK] OpenBao initialized and unsealed
    Error: Core identity failed: compose up -d --build --no-deps keycloak-1 keycloak-access:
    Network baseharbor-identity-core-hd4test Error Error response from daemon: all predefined address pools have been fully subnetted
    ```
  - zweite `baha up` auf bestehender app (workload-phasse):
    ```
    [START] Starting repository workload - creating workload network
    [FAIL] Starting repository workload - failed
    Error: Network baseharbor-dev-workload-hd4test-hd4demo-dev Error Error response from daemon: all predefined address pools have been fully subnetted
    ```
  - erwartet: netz (baseharbor-identity-core-<tgt> + -internal bzw. baseharbor-dev-workload-<tgt>-<app>-<env>) angelegt -> Core READY / app READY
  - befund: host baha-runner-docker-2 war von ambient/past-lane-netzen gesattigt (28 baseharbor-netze + weitere, fast alle /20 in 192.168.0.0/16 belegt; 172.18–172.29 komplett vergeben). Nur 192.168.240.0/20 war frei. Der fail-closed-zustand ist inhallich korrekt (docker daemon meldet exhaustion), ABER: (a) kein human recovery-hinweis auf netz-pools, (b) teilrealisierte installation (postgres+openbao up, keycloak stopped-but-owned) bleibt in DEGRADED ohne wiederherstellung-pfad. Positiv: fail-closed ohne halben core mit vertrauen.
  - gewicht: brownfield-hoch. Nachweisbar, dass es ein host-/docker-conditional ist (docker-bridge default pool + fixed /20 subnets erschopft), kein baha-logic-regression.
- note: docker host war rootless + slirp4netns; `/etc/docker/daemon.json` default-address-pool (172.40.0.0/16) zu fuegen half nicht zuverlässig (rootless daemon path); host-netz-infrastruktur nicht weiter veraendert (owner-scope, andere lanes).

### BF-hd4-2 (lock/claim/release, mittel): SIGKILL-mid-run verlaesst ein recording deployment; kernel lifecycle-lock loest sich sauber -> `baha up` resume korrekt — aber app destroy braucht destroy-time plan_id (kein app-plan plan_id)
- schwereklasse: lock/claim/release (mittel) — ein per SIGKILL abgebrochener `baha up` hinterlaesst die app in DEGRADED; der kernel-basierte lifecycle-lock (`.installation.lock`, `stableid.AcquireLifecycleLock` -> `unix.Flock(LOCK_EX|LOCK_NB)`) loest sich beim prozess-tod sofort, und ein erneuter `baha up` re-acquires das lock, rebuilt und bringt die app zurück zu READY.
- repro (podman, baha-podman-2, hd4demo2):
  1. `baha up ... --confirm-candidate <hash>` im hintergrund starten; ~20–40s warten (workload build laeuft), dann `kill -9 <baha-up-pid>`.
     - output abbruch:
       ```
       [START] Starting repository workload
       [WAIT] Starting repository workload - still working (10.4s)
       [WAIT] Starting repository workload - still working (20.4s)
       <SIGKILL> up procs: 0
       ```
  2. `baha status` danach:
     ```
     Application: DEGRADED  one or more managed capabilities, bindings or workload checks need attention
     Workload:     FAILED   workload service is not ready
     Workload:     FAILED   workload source changed since last verified build: app; run 'baha up' to rebuild
     Exposure:     FAILED   managed-exposure/open .../caddy/state.json: no such file or directory
     ```
  3. zweite `baha up` (mit passendem plan_id + confirm-hash):
     ```
     [START] Starting repository workload - rebuilt app
     [INFO] Starting repository workload - workload ready
     Application: OK  READY  application and requested infrastructure verified
     ```
  - erwartet: lock nach prozess-tod frei, resume clean
  - befund POSITIV: kernel-lock loest sich sauber (kein sticky lock, kein "resource temporarily unavailable" nach sauberem kill); resume up korrigiert DEGRADED -> READY. Positiv: deployment-state recovery funktioniert, lock-owner korrekt.
  - NEIV: nach einem ORPHANIERTEN `baha up` (ssh-connection close, prozess overlebt) bleibt der kernel-lock GEHALTEN — `baha up`/`baha status` melden "resource temporarily unavailable" und die app ist blockiert bis der orphan prozess extern gekillt wird (`pkill -9 -f "baha up"`). Das ist die praktische gefahr: ein hangernder run blockiert den target solange bis ein mensch/die coordinator-recovery den prozess beendigt.
  - app destroy needs the plan_id computed by the destroy run itself (provider_plan.impact.plan_id), nicht app plan's; app plan auf einer READY-app liefert provider_plan OHNE impact.subkey -> destroy consent env mit plan_id aus app plan schlägt fehl ("Provider-change consent must be one bounded JSON object"). Positiv: destroy flow selbst ist korrekt, nur die automation-vorbereitung (plan_id extraktion) war hier fehlerhaft.

### BF-hd4-3 (status/list konsistenz, niedrig/mittel): `baha list` ohne BASEHARBOR_TARGET schliesst bei >1 target fail-closed; status target-skaliert konsistent
- schwereklasse: status/list (niedrig) — mehrere konfigurierte targets ohne umgebungs-var blockieren target-abhaengige befehle.
- repro (baha-podman-2, 2 targets hd4test-pm + hd4test-pm2):
  - `baha list` (keine BASEHARBOR_TARGET):
    ```
    Error: multiple deployment targets configured; choose one of: hd4test-pm, hd4test-pm2, w0427-owner-missing
    Next: Run baha target activate NAME, or set BASEHARBOR_TARGET=NAME ... Use baha target list to inspect available targets.
    ```
  - `baha target list` (kein env): LISTET alle 4 targets sauber (hd4test-pm, hd4test-pm2, local, w0427-owner-missing).
  - `BASEHARBOR_TARGET=hd4test-pm baha status --json` aus spec: `target: hd4test-pm | ready: True | state: running`.
  - `BASEHARBOR_TARGET=hd4test-pm2 baha status --json` aus spec: `target: hd4test-pm2 | ready: False | state: not_applied`.
  - erwartet: status spiegelt target-scoped zustand; list ohne env braucht target-wahl.
  - befund POSITIV: target-wechsel aus EINEM repo gibt konsistente, nicht-stale zustande zurueck (pm=running/ready, pm2=not_applied). `baha target list` ohne env working. Fail-closed von `baha list` bei >1 target ist intentional (owner-boundary: nicht raten, welcher target). Kein bug, dokumentiert als konsistenz-befund.

### BF-hd4-4 (wiederhol/idempotence, positiv): zweites `baha up` auf bestehender READY-app ist idempotent
- schwereklasse: wiedervorschlag (positiv) — app bereits ready, zweites `baha up`:
  ```
  [START] Starting repository workload - source unchanged
  [INFO] Starting repository workload - workload ready
  Application: OK  READY
  ```
  - befund POSITIV: "source unchanged" -> workload nicht neu gebaut, app bleibt READY, exit 0. Lock re-acquired clean. Positiver befund (kein regress).

## BEFUNDE GESAMT
- brownfield/host (hoch): 1 — netz-pools exhaustion, fail-closed ohne recovery-hinweis
- lock/claim/release (mittel): 1 — SIGKILL resume korrekt; ORPHANIERTER prozess blockiert lock bis externer kill
- status/list (niedrig): 1 — target-skaliert konsistent; list ohne env fail-closed intentional
- wiederhol/idempotence (positiv): 1 — zweites up idempotent
- fix: keiner (schreibgrenze = kein PR/produkt-aenderung). alle funde dokumentiert, kein produkt-code veraendert.

## END
END_DONE mission-hunt-hd4: bug-hunt abgeschlossen. 4 funde (1 brownfield-hoch netz-exhaustion, 1 lock-mittel orphan-block, 1 status/list-konsistenz, 1 idempotence-positiv) dokumentiert mit datei/befehlsgenauem repro. lock baha-podman-2 RELEASED, host besenrein (0 mine containers/nets/vols, ambient unangetastet, df 46%). binar d30de3a4a. evidence auf origin/main (cde090af). kein fix (schreibgrenze).
