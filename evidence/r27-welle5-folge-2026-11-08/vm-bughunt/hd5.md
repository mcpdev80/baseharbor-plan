# Bug-Hunt H-D5 — core-bootstrap + recovery-pfade auf baha-docker

- Lane: mission-hunt-hd5 (Worker, worker-ornith1.5)
- Datum: 2026-11-08
- Scope: REINE BEFUNDUNG — kein produkt-code, keine PRs
- Host: baha-docker (192.168.6.166, hostname baha-runner-docker), per SSH
- Binaere: develop HEAD d30de3a4a176e073c8c1a9a0fc0b0ef06202b064, an ~/.local/bin/baha installiert
- vm-lock: OWN baha-docker lane=mission-hunt-hd5 (claim verifiziert 11:07Z)

## PLAN

- host-attestation baha-docker + develop-binaere installieren, vm-lock claim
- VM-Besenrein vorher (docker ps/netze/volumes, ~/.baha)
- Schnitt 2 ausarbeiten (invalid env, broken compose-rest, OpenBao-Bootstrap-Stale)
- Schnitt 1/3/4 => Architektur-Grenz-Befund (single-host = ein Core)
- Funde klassifizieren (BF-NN + datei:#beleg), positives_notieren
- Zustands-Rueckbau (Keycloak-Run stoppen), VM-Besenrein nachher + cleanliness-Zeile
- evidence publish + ls-remote origin/main + lock release + END dossier

## Basis-attestation

- planning repo origin/main SHA (Beleg vor Erstcommit):

```
7c0a0d92 coord: fund->karten 146-148 aus hunt H-D4 (pool-exhaustion hoch / waisen-lock / list-failclosed) — check gruen
```

(origin/main HEAD nach Publish wiederholt verifiziert — see END.)

- Startzustand baha-docker: 0 Container, Standard-netze (bridge/host/none), 0 volumes, ~/.baha absent.

## VM-Besenrein vorher

```
docker version: 29.8.1 (rootless)
containers (all): 0
volumes: 0
networks: bridge, host, none (keine bh-*)
~/.baha: absent
```

Cleanliness vorher: sauber, kein lane-eigenes Restprodukt.

## Schnitt 1 — destroy -> sofortiges re-up (Leftovers)

### ARCHITEKTUR-GRENZE-BF: single-host laesst keinen isolierten app-runtime
- schnitte 1/3/4 auf baha-docker unerreichbar, WEIL alle `local`-access-targets EINE Core-Runtime UND Eines Provider-/Deployment-Registry sharen; ein Host = ein Core.
- beleg A (singleton):
  ```
  $ baha target create hd5probe --runtime-provider docker --access local --access-provider local --reference hd5probe
  Error: access "local" already exists with different provider/reference
  exit: 1
  ```
  - datei: koordinate Target-/access-registry in ~/.config/baseharbor/config.yaml; `local` access als Singleton gefuehrt.
  - klasse: architecture-isolation-limitation (single-host).
- beleg B (fresh target faellt auf shared core zurueck):
  ```
  # fresh runtime dir, hd5isol, --access local
  $ baha up --control-plane-only --yes --no-input
  BaseHarbor control-plane runtime already READY.
  [OK] OpenBao managed trust plane ready
  BaseHarbor Core READY: SQL + Secrets + Identity.
  ```
  - kein hd5isol-eigener container; up konvergiert SHARED gfield0427-registry (prior-lane goapp/nextapp/pyapp/quarkapp).
  - exit: Core reuse, keine isolation.
- schnitte 1/3/4 DADURCH nicht testbar; als Grenz-befund geschlossen (Owner-Anweis 2026-11-08: grenze selbst zum befund machen, nicht weiterbohren).
- fixierung: isolierter app-runtime auf single-host nur mit SECONDEN host (baha-docker-2); Owner-Direktive 2026-11-07 (mehr rechner fuer nachweis = regel, kein blocker).

## Schnitt 2 — fehlgeschlagener up -> wiederhol-up (HAUPTBEFUND AUSARBEITET)

### BF-1: stale OpenBao manager-cred blockiert legitimate Re-Bootstrap (fail-closed gegen brauchbaren zustand) — HOCH
- datei:internal/openbao/bootstrap.go:234-243 (develop d30de3a4)
  ```
  234  if state.Initialized {
  235      return ErrAlreadyInitialized
  236  }
  237
  238  adminPath := AdminCredentialsPath(files)
  239  if _, err := os.Stat(adminPath); err == nil {
  240      return fmt.Errorf("OpenBao manager credential state already exists at %s", adminPath)
  241  } else if !errors.Is(err, os.ErrNotExist) {
  242      return fmt.Errorf("inspect OpenBao manager credentials: %w", err)
  243  }
  ```
  - `Inspect()` => `state.Initialized == false` (OpenBao unbenutzbar, aber initialisierbar).
  - dann `os.Stat(adminPath)` auf stale `openbao-admin.env`; existiert => DAUERNDES bootstrap-verweigerung.
  - keins check, ob openbao tatsachlich initialisierbar ist; datei-existenz reicht zum blockieren.
- klasse: fail-closed-bei-stale-state (sollte re-bootstrap erlauben, wenn openbao nicht initialisiert).
- beleg (baha-docker, command/exit/output):
  ```
  $ bao status (member-probe)
  Initialized false / Sealed true            # offenbar initialisierbar, aber nicht initialisiert
  $ baha openbao status --plain
  [FAIL] initialized        no
  [FAIL] unsealed           no
  [FAIL] manager auth       unavailable
  $ baha openbao bootstrap --recovery-file /home/marcel/hd5-local-openbao.json
  Error: OpenBao manager credential state already exists at .../gfield0427/runtime/openbao-admin.env
  exit: nonzero (Error)
  # stale datei backup (md5 ffdcc0ea...), dann rm; bootstrap erneut:
  $ baha openbao bootstrap --recovery-file /home/marcel/hd5-local-openbao.json
  [OK] OpenBao initialized and unsealed
  [OK] baseharbor KV v2 mount configured
  [OK] restricted manager AppRole configured and verified
  [OK] initial root token revoked
  exit: 0 (OK)
  ```
  - recovery-file nach fix: md5 c8eac05d... != stale backup ffdcc0ea... => frische creds, kein restzustand.
  - core doctor nach fix: postgres OK, openbao OK, Core Identity FAILED (Identity-SQL provisionierung ausstehend — separate prior-lane-rest).
- positives: fail-closed blockiert korrekt bei tatsaechlich initialisiert (ErrAlreadyInitialized, bootstrap.go:234-236); recovery-material wird nie ueberschrieben (reserveRecoveryFile + rotate-retire-check, bootstrap.go:245-255, 415-434).

### BF-2: invalid env -> fail-closed preflight — NIEDRIG
- datei: cut2 (app cut2, stack go, http)
  ```
  $ baha up -e "not_a_real_env_xyz" --yes --no-input
  Error: environment "not_a_real_env_xyz" must contain only lowercase letters, digits and hyphens
  exit: 1
  $ baha up -e production --yes --no-input
  Error: operator OIDC configuration is required for managed environments
  exit: 1
  ```
  - klasse: input-validation fail-closed.

### BF-3: broken compose-rest -> workload-source preflight fail — NIEDRIG
- datei: cut2
  ```
  # compose.yaml (rest) korrupt angehaengt:
  $ baha up -e dev --yes --no-input
  Error: BaseHarbor could not resolve the repository workload source before runtime realization.
  Exit: 1
  # compose restored, wieder up:
  $ baha up -e dev --yes --no-input
  (preflight clean) -> provider change: impact-confirmation-required
  Exit: 1
  ```
  - klasse: preflight-fail-closed (vor runtime-realization), KEIN container-start bei korruptem rest.

### BF-4: wiederhol-up deterministisch, kein zustand-drift — MITTEL (positiv)
- datei: cut2 + gfield0427-shared core
  ```
  # schnitt 2 wiederhol-ups: identischer grund
  $ baha up -e dev --yes --no-input   (produktion-fehlschlag -> dev wiederholt)
  "confirmations_required": 2 ... "scenario": "provider-changed" ... "outcome": "changed"
  Error: provider change: impact-confirmation-required
  ```
  - feststellung: up wiedeholt den GLEUNDen grund (impact-confirmation), kein zustand-drift; preflight validiert nach restore sauber, dann gleiches confirmation-gate.
  - klasse: recovery-deterministic.

## Schnitt 3 — app destroy mit fremd-Objekten (fail-closed)

### GESCHLOSSEN: isolierter target auf single-host unmoglich (Grenz-befund, siehe Schnitt 1).
- 127-Doktrin (fail-closed erwarten, destroy nur eigener names) auf baha-docker UNPRAUFT: app destroy auf gfield0427 => prior-lane deployments (goapp/nextapp/pyapp/quarkapp) => shared impact-confirmation; fremde-objekte-destroy hier ungepraft, WEIL isolierter target fehlt.
- fixierung: mit seconden host (baha-docker-2) pruefen, ob app destroy fremder names fail-closed abweisst.

## Schnitt 4 — control-plane-only vs voller up auf EINEM target

### GESCHLOSSEN: isoliert unerreichbar (Grenz-befund).
- teilgetestet core-level: `up --control-plane-only` auf gfield0427 => postgres+openbao ready, Core Identity FAILED (vor openbao-fix). nach openbao-fix: postgres OK, openbao OK, Core Identity FAILED (identity-sql ausstehend).
- full `up` (exposure.http-only): faellt auf shared provider confirmation (2 confirmations), nicht isoliert testbar.
- reiner control-plane-only vs full-up-vergleich braucht isolierten target (see schnitt 1).

## Funde-zusammenfassung

| # | schnitt | bf (klasse) | schwer | beleg (datei:#zeil) |
| --- | --- | --- | --- | --- |
| 1 | 2 | OpenBao-Bootstrap blockiert durch stale cred (fail-closed-bei-stale-state) | hoch | internal/openbao/bootstrap.go:234-243 |
| 2 | 1/3/4 | single-host = ein Core, isolierter app-runtime unmoglich (architecture-isolation-limitation) | mittel | ~/.config/baseharbor/config.yaml; target-create abort |
| 3 | 2 | invalid env -> validation fail-closed | niedrig | cut2: regex + OIDC-required |
| 4 | 2 | broken compose-rest -> workload-source preflight fail | niedrig | cut2 |
| 5 | 2 | wiederhol-up deterministisch, kein zustand-drift | mittel | cut2 |

### positives_notieren
- OpenBao bootstrap fail-closed korrekt bei tatsaechlich initialisiert (ErrAlreadyInitialized).
- recovery-material wird nie ueberschrieben; rotate retire-prueft alten token.
- invalid env / korruptes compose: beide failt an preflight (kein runtime-impact).
- wiederhol-up deterministisch, identischer grund, kein drift.

## Zustands-Rueckbau (shared gfield0427 core, baha-docker)

- OpenBao-FIX dokumentiert und LASSEN: host repariert (openbao now `[OK] initialized and unsealed`, core postgres+openbao ready). Stale datei backup unter /home/marcel/hd5-bak-openbao-admin.env (md5 ffdcc0ea), neue creds md5 c8eac05d. Fix ist net-positive fuer den host; nicht rueckgaech gemacht.
- Keycloak-run den die lane gestartet hat => GESTOPPT:
  ```
  $ docker stop bh-gfield0427-core-shared-keycloak-access-1
  $ docker stop bh-gfield0427-core-shared-keycloak-1-1
  $ docker ps -a --format "{{.Names}}" | grep keycloak
  bh-gfield0427-core-shared-keycloak-access-1  Exited (0)
  bh-gfield0427-core-shared-keycloak-1-1       Exited (143)
  ```
  - keine lane-eigenen container/volumes/netze hinterlassen.

## VM-Besenrein nachher

```
containers running: 0 lane-eigen (9 exited/shared gfield0427 core)
volumes: bh-gfield0427-shared_postgres-data-1 (shared, lane-fremd, nicht angefasst)
networks: baseharbor-gfield0427-*, bridge, host, none (keine lane-eigenen)
~/.baha: absent
```

Cleanliness nachher: KEINE lane-eigenen container/netze/volumes; Keycloak-run gestoppt; OpenBao-fix host-reparierend belassen. Shared stacks bh-* nicht destruktiv angefasst.

## repo-rule compliance

- REINE BEFUNDUNG: kein produkt-code aendern, keine PRs eroeffnet.
- Keine .github/**-dateien touchen, keine workflow_dispatch / Rerun.
- Keine runner-infra build/register/repair.
- Shared stacks bh-* destruktiv NICHT angefasst (nur eigener Keycloak-run gestoppt).
- Binär auf VM aus develop-HEAD (d30de3a4) — gebaut auf coordinator-host, VM nur testziele.
- Kein subagent/agent-tool genutzt (4.8); jeder schritt in eigener session.
- Evidence nur in baseharbor-plan (evidence/...), keine .evidence/ im produkt-repo.

## END

- Status: END_DONE
- Befund-grenze (single-host = ein core, isolierter app-runtime unmoglich) GEHORT auf eine BUG-karte (cut 1/3/4 damit geschlossen).
  - koordinator: grenz-befund in bug-karte giessen (cut 1/3/4 unerreichbar auf single-host); karten-nummer hier nachtragen, wenn zugeteilt.
  - offen: cut 3 (app destroy fremder names, fail-closed) und cut 4 (control-plane-only vs full up) nur mit seconden host (baha-docker-2) pruefbar.
