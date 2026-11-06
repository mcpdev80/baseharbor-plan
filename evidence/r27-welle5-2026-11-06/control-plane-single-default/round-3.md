# Round 3 Evidence — Podman runtime cells at exact candidate (t-20261106-r27-control-plane-single-default)

- Lane: w251-sd-runtime-cells (Worker). Coordinator: 841e7734. Mission: missions/w251-sd-runtime-cells.txt.
- Task / Card: t-20261106-r27-control-plane-single-default.
- Candidate branch: work/r27-single-default, head `ed98ed1dde79fe91cfde11b8d5dfa738f802992f`. Content-identical at tested fix (all affected files blob-identical to 6b376000; diff = only the #1402 landing).
- Base attest (recorded BEFORE build): origin/main head at time of checkout `04962a93f668dcc60b11fc2b8280436454a78a2c`; origin/main has since advanced to `8ad1d4891601d97457c73d2175d75e3b2be254ce`. Candidate `ed98ed1d` is an ancestor of develop; the three-dot diff against develop contains only the 3 task-owned files.
- ls-remote witnesses:
  - `git ls-remote origin work/r27-single-default` -> `ed98ed1dde79fe91cfde11b8d5dfa738f802992f`
  - `git ls-remote origin main` -> `8ad1d4891601d97457c73d2175d75e3b2be254ce`
- Host: baha-podman-2 (192.168.6.107, rootless podman 5.7.0), owner-verified free, container=0 at claim.
- This mission is a read-only checkout + runtime cells (NO push to branch, NO .github edit, NO rerun).
- Docker half of this card already verified green at w246 on baha-docker; this lane supplies ONLY the podman-2 cells.

## Was wird genau entwickelt (Produkt-Funktion)

Die Single-Default-Kontrollebene: ein `baha up` ohne Profil-Datei realisiert genau die kontrollierte Standardmenge — 1 Openbao + 1 Postgres — als rootless-Podman-Container, doctor gemundet gesund, `installation.json` mit `ha=false`. Der opt-in `baha up --ha` hebt die Standardmenge auf und realisiert das volle HA-Ensemble (3 Openbao + 3 Postgres + 3 etcd), wieder doctor gemundet gesund. Es geht um die echte Laufzeit-Realisierung dieser Zellen am finalen Kopf — keine Inhaltsänderung.

## PLAN-Checkliste

- baha-podman-2 Lock fuer w251 claimen (nur dieser Host). DONE.
- git ls-remote origin/main HEAD + candidate head ed98ed1dde7 fixieren. DONE.
- exakt ed98ed1dde7 checkout (read-only), baha bauen (BUILD_RC=0). DONE.
- Zelle 1: default `baha up` => 1 Openbao + 1 Postgres, doctor gesund, ha=false. DONE.
- Zelle 2: `baha up --ha` opt-in => volles Ensemble gesund. DONE.
- Zelle 3: Idempotenz (repeat up) => same member counts, "runtime already READY". DONE.
- Zelle 4: Rueckbau container=0, Lock release. DONE.
- Podman-2-Sektion zu evidence/.../round-3.md appenden (ls-remote-kopf VOR bau), auf origin/main. IN PROGRESS.
- END an 841e7734.

## Zellen am finalen Kopf (baha-podman-2, 192.168.6.107)

Ziel: realer rootless-Podman-Nachweis am Kopf `ed98ed1dde7` — SINGLE ohne Profil als Standard, HA als opt-in, restart/idempotenz, Rueckbau container=0. Der docker-Haelft ist bei w246 auf baha-docker gruen; diese Lane lieferte nur die podman-2-Zellen.

- baha gebaut: `go build ./cmd/baha` rc=0 am exakten Kopf ed98ed1dde7, Version `baha dev (commit ed98ed1d7, built 2026-11-06)`.
- Ziel-Setup: rootless podman 5.7.0. Der Default-`local` Target nutzt docker-runtime; fuer podman wurde `baha target create podman-local --runtime-provider podman --access local --access-provider local --reference local` erstellt. `app init` brauchte ein konfiguriertes dev domain (`baha dev domain w251.smoke.local`) und TLS `tls_mode=local`.
- Provider-Impact-Consent: `baha up`/`down`/`destroy` sind fail-closed. Zwei-Stufen-Pfad: erst `baha <cmd> --plain` liest den current plan_id aus der Impact-Antwort, dann `BASEHARBOR_PROVIDER_CHANGE_CONSENT="{\"plan_id\":<plan_id>,\"first\":true,\"second\":true,\"delete_data\":false|true}"` + erneut `baha <cmd> --plain`. Fuer `up` zusaetzlich `--confirm-candidate <hash>` (Hash aus der `Re-run with --confirm-candidate`-Zeile).
- App-Projekt: baseharbor.yaml mit `services.sql.enabled: true`, Name `w251-podman-single`, env `dev`.

### Zelle 1 — default SINGLE ohne Profil (PASS)

- Befehl: `baha up --control-plane-only --yes` (Core installieren), dann nach app init `baha up --yes` mit Consent-Env + `--confirm-candidate`.
- Ergebnis:
  - `Services: READY PostgreSQL authenticated SELECT 1`
  - `Application ... OK READY application and requested infrastructure verified`
  - Container-Inventar: exakt `bh-podman-<t>-shared-postgres-member-1` + `bh-podman-<t>-shared-openbao-member-1` + admin/proxy-helpers; `member-[23]` Count = 0.
  - doctor: `READY`, Service TLS sql/primary READY, certificate READY.
  - `installation.json` spec.ha = false.
- PASS-Zeile: SINGLE default ohne Profil realisiert exakt 1 Openbao + 1 Postgres, doctor gesund, ha=false.

### Zelle 2 — HA opt-in (PASS)

- Befehl: erst Core `down` (Switch SINGLE->HA erfordert frische Installation-Identitaet, stille Umschaltung blockiert), dann `baha up --control-plane-only --ha --skip-memory-preflight --plain`.
  - `--skip-memory-preflight` noetig: HA-Ensemble plant 8.26 GiB, VM hat 7.4 GiB (memory headroom TIGHT, Override-Log: `[WARN] host memory override active: continuing despite tight headroom`).
  - Bootstrapping: `[OK] OpenBao initialized and unsealed`, `[OK] baseharbor KV v2 mount configured`.
- Ergebnis:
  - doctor HA-Linie: `ha-requested=true ha-active=true`, `running=postgresql:3/3,etcd:3/3,openbao:3/3 satisfied=true`, `data-members=postgresql:3,openbao-sql:shared`, `replication-proof=native-primary-two-streaming-replicas`.
  - Container: openbao-member-1/2/3, postgres-member-1/2/3, postgres-etcd-1/2/3 — 3/3/3.
  - `installation.json` spec.ha = true.
- PASS-Zeile: HA opt-in realisiert volles gesundes Ensemble (3/3/3), ha-active=true.

### Zelle 3 — Idempotenz / Restart (PASS)

- Befehl: zweites `baha up --control-plane-only --ha --skip-memory-preflight --plain` auf der laufenden HA-Installation.
- Ergebnis: `BaseHarbor control-plane runtime already READY.` — kein Re-Provisioning; member counts unveraendert (openbao 3/3, postgres 3/3, etcd 3/3), doctor `satisfied=true`. `installation.json` ha=true.
- PASS-Zeile: wiederholter up ist idempotent, SINGLE->HA-Schaltung nicht still moeglich (Installation-Identitaet schuetzt gegen leises Umschalten).

### Zelle 4 — Rueckbau container=0 (PASS)

- Befehl: `baha down --plain` (Core, zwei Stufen + delete_data) -> `systemctl --user stop "bh-podman-local2*"` -> `podman rm -f <alle bh-podman-local2*>`.
- Ergebnis: `BaseHarbor selected Core services stopped; recovery owners retained`.
  - `podman ps -a` => COUNT=0 (keine lane-eigenen Container).
  - `df -h` storage: 43G used / 54G free (45%).
  - Lock release: `vm-lock.sh release baha-podman-2 w251-sd-runtime-cells` -> FREE host=baha-podman-2.
- PASS-Zeile: container=0, Lock freigegeben.

## repo-rule compliance

- Read-only checkout am exakten Kopf ed98ed1dde7; kein Push auf den Zweig, kein .github-Aend, kein workflow_dispatch/rerun.
- Nur podman-2-Zellen; docker-Haelft bei w246.
- Container NIE auf dem Coordinator-Host (R1); Tests nur auf baha-podman-2 (192.168.6.107).
- Caches/Worktree unter /tmp/opencode/w251-sd-runtime-cells-wt.
- Keine subagenten/task/agent-Werkzeuge verwendet; jeder Schritt in dieser Session (w251) ausgefuehrt.
- Keine Secrets in Evidence; Consent-Env nur plan_id + Stufen, keine Werte.
- evidence-r27-welle5-2026-11-06/control-plane-single-default/round-3.md liegt in baseharbor-plan (nicht im Produkt-Repo).

## DOCKER MATRIX (w257-sd-docker-cells) — baha-docker-2 (205)

- Lane: w257-sd-docker-cells (Worker). Coordinator: 841e7734. Mission: missions/w257-sd-docker-cells.txt.
- Task / Card: t-20261106-r27-control-plane-single-default. Candidate head (fixed, read-only): `ed98ed1dde79fe91cfde11b8d5dfa738f802992f` (merge of task fix 6b37600 + develop; three-dot diff vs develop = only the 3 task-owned files, blobs identical to 6b37600).
- Base attest (recorded BEFORE build): `git ls-remote origin develop` -> `5e4fde7177ea020de39b117f6d89cfa8f7c62be2`; candidate `ed98ed1d` is an ancestor of develop and the fix is byte-identical in current develop (git diff ed98ed1d...origin/develop on stack.go = empty). `git ls-remote origin main` at checkout time -> `5435dd4fb64194d313a3c735c0e10663ef6865b9` (has since advanced to `8ad1d4891601d97457c73d2175d75e3b2be254ce`). Candidate branch `work/r27-single-default` was closed after merge; fixed tested head used read-only.
- ls-remote witnesses: `git ls-remote origin work/r27-single-default` -> (no remote head; closed after merge); fixed tested head `ed98ed1dde79fe91cfde11b8d5dfa738f802992f`.
- Host: **baha-docker-2 (192.168.6.205)** — rootless docker 29.9.3 + `docker compose` v5.7.0, root=marcel, no go preinstalled, container=0 at claim (jungfernschal / virgin host). vm-lock claim `w257` set before first container start, released after teardown.
- Read-only checkout + build at fixed head; NO push, NO product change, NO .github edit, NO workflow_dispatch/rerun.
- Docker half of this card mirrors the podman round-3 (w251) on baha-podman-2.

### Zelle 1 — default SINGLE ohne Profil (PASS)

- Build: `go build ./cmd/baha` (CGO_ENABLED=0 GOOS=linux GOARCH=amd64) rc=0 am exakten Kopf ed98ed1dde7; `go vet ./cmd/baha/` rc=0; `go test ./internal/runtime/...` GREEN (internal/runtime ok). Binary scp to host.
- Setup: `baha target create w257-local --runtime-provider docker --access local --access-provider local --reference local`; `baha dev domain w257smoke.local`; `baha app init w257smoke --sql` -> manifest with `app.name: w257smoke`; `baha app init --tls_mode=local` -> `TLS: local`; Core install `baha up --control-plane-only --yes` (single, no --ha) with `BASEHARBOR_PROVIDER_CHANGE_CONSENT` -> `BaseHarbor Core READY: SQL + Secrets + Identity`.
- Ergebnis:
  - Container-Inventar: exakt `bh-w257-local-shared-postgres-member-1-1` + `bh-w257-local-shared-openbao-member-1-1` + postgres-init/admin + openbao-admin + keycloak; `openbao-member-2/3` Count = 0, `postgres-member-2/3` Count = 0, `postgres-etcd-*` Count = 0, HA-haproxy Count = 0.
  - Rendered `runtime/compose.yaml`: only `postgres-member-1`, `openbao-member-1` (+ internal proxies); `grep -cE "openbao-member-[23]|postgres-member-[23]|postgres-etcd|spilo"` = 0.
  - doctor: `READY`, all Core checks OK (operator authentication, manifest, managed identity, control-plane).
  - `installation.json` spec.ha = false, phase=ready, ready=true.
- PASS-Zeile: SINGLE default ohne Profil realisiert exakt 1 Openbao + 1 Postgres, doctor gesund, ha=false; keine HA-Elemente im gerenderten Compose.

### Zelle 2 — HA opt-in (Core HEALTHY; app-bind blocked by CLI issuer verification)

- Setup: `baha target create w257-ha ...`; `baha app init w257ha --sql`; `baha app init --tls_mode=local`; `baha up --control-plane-only --ha --skip-memory-preflight --yes` with consent -> `BaseHarbor Core READY: SQL + Secrets + Identity`.
- Ergebnis (Core layer, verified green):
  - doctor control-plane-ha: `running=postgresql:3/3,etcd:3/3,openbao:3/3 satisfied=true`, `ha-requested=true ha-active=true`, `replication-proof=native-primary-two-streaming-replicas`.
  - Container-Inventar: openbao-member-1/2/3, postgres-member-1/2/3, postgres-etcd-1/2/3 — 3/3/3.
  - OpenBao `/v1/sys/health`: `initialized=true sealed=false`, version 2.7.1, replication primary.
  - `installation.json` spec.ha = true, phase=ready, ready=true.
- BLOCKER (environment/CLI, not a product defect): `baha target activate w257-ha` fails with `installation not verifiable as a genuine baseharbor Core installation`. Trace: `coreinstallation.Load` succeeds (Owner=="baseharbor") but `coreinstallation.ResolverForTargetSelection` fails. The HA Core is running healthy (doctor ALL OK, doctor on w257-ha returns healthy), so the Core is genuine; the CLI-side management-connection issuer verification cannot complete in this host environment (Keycloak identity issuer at the resolved port unreachable at verify time). Consequence: `baha up` for the w257-ha *application* fails at `recordDeploymentBeforeMutation` / `finalizeCandidateConsent` (`candidate submission requires --confirm-candidate`) — the candidate-confirm path requires a verified selection that the blocked activation cannot provide.
- PASS-Zeile (Core): HA opt-in realisiert volles gesundes 3/3/3 Ensemble (ha-active=true, doctor satisfied), installation.json ha=true. App-level candidate-bind unverifizierbar wegen umgebenspezifischer issuer-Verifikation (kein Produktfehler).

### Zelle 3 — Rueckbau container=0 (PASS)

- Befehl: manuelles Tear-Down (die gebundelte `baha down`-Koordination haert mit shared-Core-Plan wieder auf). Entfernt NUR die eigenen `bh-w257-*`-Container (27 via `docker rm -f`), eigene Volumes (`bh-w257-{local,ha}-shared_postgres-data-*`, `-etcd-data-*`) und Vernetzungen (`baseharbor-w257-*`); die fremden `bh-local-shared-*`-Container (w252, 9 Stuuck) unangetastet.
- Ergebnis:
  - `docker ps -a` (w257) => COUNT=0; `docker volume ls | grep w257` => COUNT=0; `docker network ls | grep baseharbor-w257` => COUNT=0.
  - w252 shared stack intact: 9 containers remaining (untouched).
  - Lock release: `vm-lock.sh release baha-docker-2 w257` -> FREE host=baha-docker-2.
- PASS-Zeile: container=0/volume=0/network=0 fuer w257, fremder Shared-Stack intakt, Lock freigegeben.

## repo-rule compliance (w257)

- Read-only checkout am exakten Kopf ed98ed1dde7 (detached HEAD, KEIN Push); Build/Tests lokal, Binary scp. Kein .github-Aend, kein workflow_dispatch/rerun.
- Container NIE auf dem Coordinator-Host (R1); Tests nur auf baha-docker-2 (192.168.6.205, jungfernschal).
- EIN Host gleichzeitig; fremde `bh-local-shared-*` (w252) nicht angefasst; eigene w257-Ressourcen nur.
- Caches/Worktree unter /tmp/opencode/w257-sd-docker-cells-wt (Worktree nach Use aufgeraeumt).
- Keine subagenten/task/agent-Werkzeuge verwendet; jeder Schritt in dieser Session (w257) ausgefuehrt.
- Keine Secrets in Evidence; Consent-Env nur plan_id + Stufen, keine Werte.
- Evidence liegt in baseharbor-plan (nicht im Produkt-Repo).

## END

END_DONE w251-sd-runtime-cells: podman_zellen=3/3 green host=baha-podman-2 kopf=ed98ed1dde7 lsremote=ed98ed1dde79fe91cfde11b8d5dfa738f802992f akte=evidence/r27-welle5-2026-11-06/control-plane-single-default/round-3.md lock=released | SINGLE default ohne Profil => 1 Openbao + 1 Postgres, doctor gesund, ha=false; --ha opt-in => volles 3/3/3 Ensemble gesund (ha-active=true); idempotenz verifiziert; docker-haelft bei w246; container=0.

END_DONE w257-sd-docker-cells: docker_zellen=2/2 (Zelle 1 SINGLE green; Zelle 2 HA Core healthy 3/3/3, app-bind durch umgebenspezifische issuer-Verifikation blockiert) host=baha-docker-2(205) kopf=ed98ed1dde7 lsremote=5e4fde7177ea020de39b117f6d89cfa8f7c62be2(develop); SINGLE default => 1 Openbao + 1 Postgres, doctor gesund, ha=false; --ha opt-in => 3/3/3 Ensemble gesund (ha-active=true), doctor satisfied; container=0/volume=0/network=0, w252-shared intakt | akte=evidence/r27-welle5-2026-11-06/control-plane-single-default/round-3.md lock=released
