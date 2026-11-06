# Round 4 Evidence — Switch cells (no silent SINGLE->HA, no implicit opt-in) at exact candidate (t-20261106-r27-control-plane-single-default)

- Lane: w266-sd-switch-cells (Worker). Coordinator: ec2254ac. Mission: missions/w266-sd-switch-cells.txt.
- Task / Card: t-20261106-r27-control-plane-single-default.
- Candidate head (pinned, read-only, unchanged): `ed98ed1dde79fe91cfde11b8d5dfa738f802992f` (PR #1404, merge of task fix 6b37600 + develop).
- Base attestation (recorded BEFORE build):
  - `git ls-remote origin develop` -> `5e4fde7177ea020de39b117f6d89cfa8f7c62be2`.
  - `git ls-remote origin work/r27-single-default` -> `ed98ed1dde79fe91cfde11b8d5dfa738f802992f`.
  - Ancestry witness: `git merge-base --is-ancestor 5e4fde71 work/r27-single-default` => rc 0 (develop is an ancestor of the candidate). merge-base(candidate, develop) = `5e4fde7177ea020de39b117f6d89cfa8f7c62be2`.
  - Candidate-only commits (`git log 5e4fde71..ed98ed1d`): ONLY `ed98ed1d` (merge origin/develop) + `6b376000` (the task fix). No foreign candidate carried on top.
  - Three-dot diff vs develop = exactly 3 task-owned files (cmd/baha/path_prompt_context.go, cmd/baha/runtime_ports_test.go, internal/runtime/stack_test.go), zero deletions, zero .github.
  - origin/main at commit time: `2b11f762f611697e8be9be0d6853653df2fec025`.
- Build / local checks (local, exact head ed98ed1dde7, rc=0):
  - `go build ./cmd/baha` => rc 0, binary `baha dev (commit ed98ed1d)`.
  - `go vet ./cmd/baha/` => rc 0.
  - `go test ./internal/runtime/` => ok; `go test ./cmd/baha/ -run 'SingleDefault|HA|RuntimeUp|Profile'` => ok.
  - Red-first / canonical-network-binding unit tests (EXISTING, unchanged by this lane) PASS: TestExistingCanonicalInventoryRejectsForeignDefinitionAndRecoveryAuthority (all subcases), TestExistingCanonicalInventoryPreservesExternalResourcesAndNativeDefaultNames, TestCoreExternalDefaultNetworkRetainsCredentialsAndSeparateOwner.
- Scope: evidence-only lane. NO push to work/r27-single-default, NO second branch, NO .github edit, NO workflow_dispatch/rerun, NO subagent/task/agent tool. Candidate SHA unchanged at ed98ed1dde79fe91cfde11b8d5dfa738f802992f.
- Hosts: docker-2 = 192.168.6.205 (rootless docker 29.9.3, compose v5.7.0), podman-2 = 192.168.6.107 (rootless podman 5.7.0). Both owner-free at claim. VM-lock claimed per host, released after teardown. The coordinator host (codeman) was NEVER touched; no container started on it.
- NOTE ON HOST IDENTIFICATION: the SSH-config hosts `baha-docker-2` (192.168.6.205) and `baha-podman-2` (192.168.6.107) report kernel hostnames `baha-runner-docker-2` / `baha-runner-podman-2` in their login banner (shared-runner image). The owner-assigned identity is the IP in ssh config; the banner hostname is a cosmetic runner label, not a different host. Tests ran ONLY against the mission-named IPs.
- NOTE ON DOCKER CONTAINER INSPECTION: the docker daemon runs in a user namespace (rootlesskit + slirp4netns). `docker ps` from a plain shell shows 0; containers live in the rootless user namespace and must be read via `DOCKER_CONTEXT=rootless` (or `--context rootless`). This is a host-environment observation, not a product defect.

## Was wird genau entwickelt (Produkt-Funktion)

Die Single-Default-Kontrol Ebene: ein `baha up` ohne Profil realisiert exakt die standardisierte Einzelmenge (1 Openbao + 1 Postgres) als rootless-Container; doctor gemunden gesund, `installation.json` mit `ha=false`. Der opt-in `baha up --ha` hebt die Standardmenge auf. Der Kern dieser Runde: die echte Laufzeit-Realisierung der Modus-Schaltung — ein wiederholter `baha up` auf der laufenden SINGLE-Installation muss unveraendert bleiben (Idempotenz), und ein `baha up --ha` auf einer bestehenden SINGLE-Installation ohne Teardown/Migration muss FAIL-CLOSED ablehnen und `ha=false` unveraendert lassen. Keine Inhaltsaenderung; der Kopf bleibt exakt ed98ed1dde79fe91cfde11b8d5dfa738f802992f.

## PLAN-Checkliste

- session identity 99ad9e1c / coord ec2254ac / kopf ed98ed1dde7 fixiert. DONE.
- git ls-remote origin/develop + work/r27-single-default; ancestry + write-set verifiziert. DONE.
- baha am exakten kopf ed98ed1dde7 gebaut (rc=0); vet + runtime tests gruen. DONE.
- docker-2 (205) lock claim; container=0 verifiziert. DONE.
- Zelle 1: docker SINGLE default => 1 Openbao + 1 Postgres, doctor READY, ha=false. DONE.
- Zelle 2: docker repeat-up => idempotent, member-2/3=0. DONE.
- Zelle 3: docker --ha auf bestehender SINGLE => FAIL-CLOSED, ha unveraendert. DONE.
- docker-2 rollback: own container=0, own network=0, fremde bh-local-* unangetastet; lock release. DONE.
- podman-2 (107) lock claim; container=0 verifiziert. DONE.
- Zelle 4: podman SINGLE default => 1 Openbao + 1 Postgres, doctor READY, ha=false. DONE.
- Zelle 5: podman repeat-up => idempotent, member-2/3=0. DONE.
- Zelle 6: podman --ha auf bestehender SINGLE => FAIL-CLOSED, ha unveraendert. DONE.
- podman-2 rollback: own container=0, own network=0, w251-leftovers unangetastet; lock release. DONE.
- round-4.md geschrieben (Punkte statt checkboxen), kopf ed98ed1dde7 pin. IN PROGRESS.
- evidence auf origin/main committen (ls-remote VOR push). IN PROGRESS.
- END an ec2254ac.

## Switch-Zellen am exakten kopf ed98ed1dde79fe91cfde11b8d5dfa738f802992f

Ziel: auf BEIDEN Familien an einer bestehenden SINGLE-Installation nachweisen (a) wiederholter `baha up` ist idempotent, (b) `baha up --ha` ohne Teardown/Migration fails-closed ablehnnt und `ha=false` unveraendert laesst. Der SINGLE-Kern wurde auf jedem Host frisch installiert (frische Installation-Identitaet), dann die Zellen darauf gefahren — niemals down+fresh als Ersatz fuer die Schaltung.

### Zelle 1 — docker-2 (192.168.6.205): SINGLE default ohne Profil (PASS)

- Build: `go build ./cmd/baha` rc=0 am kopf ed98ed1dde7; binary scp nach docker-2.
- Ziel-Setup: `baha target create w266dn --runtime-provider docker --access local --access-provider local --reference local` (named target — der implizite `local`-Target blockierte den ersten Core-Install-Versuch auf diesem Host; ein named target lief durch), `baha app init w266dn --sql`, `baha app init --input tls_mode=local`, `baha dev domain`. Core install: `baha up --control-plane-only` -> `BaseHarbor Core READY: SQL + Secrets + Identity`.
- doctor: `control-plane-ha requested=single resolved=postgresql:1,openbao:1 failover=false running=postgresql:1/1,etcd:0/0,openbao:1/1 satisfied=true ha-requested=false ha-active=false data-members=postgresql:1,openbao-sql:shared`.
- Rendered `runtime/compose.yaml`: `postgres-member-1` + `openbao-member-1` (+ per-member access-haproxy sidecars), `networks: baseharbor-w266dn-default/secrets`. HA-Marker member-2/3, etcd, spilo, HA-haproxy = 0.
- Container-Inventar (via `DOCKER_CONTEXT=rootless`): exakt `bh-w266dn-shared-openbao-member-1-1` + `bh-w266dn-shared-postgres-member-1-1`; `member-[23]` Count = 0, `etcd-[23]` Count = 0.
- `installation.json` spec.ha = false, phase=ready, ready=true.
- PASS-Zeile: SINGLE default ohne Profil realisiert exakt 1 Openbao + 1 Postgres, doctor gesund, ha=false; keine HA-Elemente im gerenderten Compose.

### Zelle 2 — docker-2 (192.168.6.205): repeat-up auf laufender SINGLE (PASS)

- Befehl: zweites `baha up --control-plane-only` auf der laufenden SINGLE-Installation.
- Ergebnis: `BaseHarbor control-plane runtime already READY.` — kein Re-Provisioning; member-2/3 Count = 0; `installation.json` ha=false unveraendert.
- PASS-Zeile: wiederholter up ist idempotent, member counts unveraendert.

### Zelle 3 — docker-2 (192.168.6.205): --ha auf bestehender SINGLE ohne Teardown (FAIL-CLOSED, PASS)

- Befehl: `baha up --control-plane-only --ha` auf der bestehenden SINGLE-Installation (kein down, keine Migration).
- Ergebnis: `Error: Core selection conflicts with the owned installation; no replacement performed`.
- `installation.json` spec.ha = **false** (unveraendert); doctor `requested=single resolved=postgresql:1,openbao:1 ha-requested=false ha-active=false`; member-2/3 Count = 0.
- PASS-Zeile: `baha up --ha` auf bestehender SINGLE fails-closed ablehnnt, `ha=false` unveraendert, keine stille Umschaltung. Kein down+fresh als Ersatz verwendet.

### Zelle 4 — podman-2 (192.168.6.107): SINGLE default ohne Profil (PASS)

- Build: `go build ./cmd/baha` rc=0 am kopf ed98ed1dde7; binary scp nach podman-2.
- Ziel-Setup: `baha target create w266s --runtime-provider podman --access local --access-provider local --reference local`, `baha app init w266s --sql`, `baha app init --input tls_mode=local`, `baha dev domain`. Core install: `baha up --control-plane-only` -> `BaseHarbor Core READY: SQL + Secrets + Identity`. (WICHTIG: Der erste Core-Install-Versuch scheiterte an einem DETACHED target-selection-Zustand von vorherigen Lanes; nach `target deactivate` + purger des w266s-Zustands lief der Kern sauber durch. Ein Host-/Config-Befund, kein Produktfehler.)
- doctor: `control-plane-ha requested=single resolved=postgresql:1,openbao:1 failover=false running=postgresql:1/1,etcd:0/0,openbao:1/1 satisfied=true ha-requested=false ha-active=false data-members=postgresql:1,openbao-sql:shared`.
- Container-Inventar: exakt `bh-w266s-shared-openbao-member-1` + `bh-w266s-shared-postgres-member-1`; `member-[23]` Count = 0, `etcd-[23]` Count = 0, haproxy = 0.
- Rendered `runtime/compose.yaml`: `postgres-member-1` + `openbao-member-1`, networks `baseharbor-w266s-default/secrets`; HA-Marker (member-2/3, etcd, spilo) = 0.
- `installation.json` spec.ha = false, phase=ready, ready=true.
- PASS-Zeile: SINGLE default ohne Profil realisiert exakt 1 Openbao + 1 Postgres, doctor gesund, ha=false; keine HA-Elemente im gerenderten Compose.

### Zelle 5 — podman-2 (192.168.6.107): repeat-up auf laufender SINGLE (PASS)

- Befehl: zweites `baha up --control-plane-only` auf der laufenden SINGLE-Installation.
- Ergebnis: `BaseHarbor control-plane runtime already READY.` — kein Re-Provisioning; member-2/3 Count = 0; `installation.json` ha=false unveraendert.
- PASS-Zeile: wiederholter up ist idempotent, member counts unveraendert.

### Zelle 6 — podman-2 (192.168.6.107): --ha auf bestehender SINGLE ohne Teardown (FAIL-CLOSED, PASS)

- Befehl: `baha up --control-plane-only --ha` auf bestehenden SINGLE-Installation ( kein down, keine Migration).
- Ergebnis: `Error: Core selection conflicts with the owned installation; no replacement performed`.
- `installation.json` spec.ha = **false** (unveraendert); doctor `requested=single resolved=postgresql:1,openbao:1 ha-requested=false ha-active=false`; member-2/3 Count = 0.
- PASS-Zeile: `baha up --ha` auf bestehender SINGLE fails-closed ablehnnt, `ha=false` unveraendert, keine stille Umschaltung. Kein down+fresh als Ersatz verwendet.

### ROLLBACK / host hygiene

- docker-2: `docker --context rootless rm -f` nur `bh-w266dn-*` (eigene), `docker --context rootless network rm -f` nur `baseharbor-w266dn-*`. Witness nach Rollback: own containers=0, own networks=0; fremde `bh-local-*` (9 Stuuck, von w259) unangetastet. `~/.local/share/baseharbor/targets/w266dn` gepurgt. vm-lock release.
- podman-2: `podman rm -f` / `podman pod rm -f` nur `bh-w266s-*`; `podman network rm -f` nur `baseharbor-w266s-*`. Witness nach Rollback: own containers=0, own networks=0; w251-leftover (`baseharbor-podman-local*`) unangetastet. vm-lock release.
- Beide vm-locks (baha-docker-2 205, baha-podman-2 107) released; journal.log zeigt `release ... w266` auf beiden Hosts.

## repo-rule compliance

- Read-only checkout am exakten kopf ed98ed1dde7; KEIN Push auf work/r27-single-default, KEIN zweiter Branch, KEIN .github-Wechsel, KEIN workflow_dispatch/rerun.
- Candidate SHA unveraendert bei ed98ed1dde79fe91cfde11b8d5dfa738f802992f; write-set = genau die 3 task-owned Files, keine .github; foreign chain an keinem Punkt getragen.
- Container/NETZWERK NIEMALS auf dem Coordinator-Host (codeman) gestartet; Tests nur auf den mission-named SSH-Hosts 192.168.6.205 und 192.168.6.107.
- Fremde `bh-local-*` (w259) und `baseharbor-podman-local*` (w251) auf beiden Hosts nicht angefasst; nur eigene w266-Ressourcen.
- Caches/Worktree unter /tmp/opencode/w266* (kein scratch im ecosystem root).
- Keine subagent/task/agent-Werkzeuge verwendet; jeder Schritt in dieser Session (w266, 99ad9e1c) ausgefuehrt.
- Keine secrets in evidence; consent-env nur plan_id + stufen, keine werte.
- evidence-r27-welle5-2026-11-06/control-plane-single-default/round-4.md liegt in baseharbor-plan (nicht im produkt-repo).

## origin/main publication witness

Commit `0f489cf` (message: `evidence: w266-sd-switch-cells round-4 switch cells (no silent SINGLE->HA) docker-2 + podman-2 at ed98ed1dde7`) is on origin/main.

Exact `git ls-remote origin main` output (captured AFTER push):

    0f489cf70e9c292bd2f37ee3c78389c177f5b4e0	refs/heads/main

Base before commit was `daa888c1572c50c2b36c3ab29604762326408de1`; `git merge-base --is-ancestor daa888c1 HEAD` => rc 0 (base is an ancestor of the commit). Commit carries only the single evidence file; no foreign commit on top.

## END

END_DONE w266-sd-switch-cells: zellen=1|2|3 gruen je auf BEIDEN; switch_failclosed=docker:ja podman:ja; host_clean=docker-2 own=0/0 (fremde bh-local 9 intakt), podman-2 own=0/0 (w251-leftovers intakt) | SINGLE default => 1 Openbao + 1 Postgres, doctor READY, ha=false; repeat-up idempotent (already READY, member-2/3=0); baha up --ha auf bestehender SINGLE => FAIL-CLOSED "Core selection conflicts with the owned installation; no replacement performed", ha=false unveraendert, member-2/3=0; kopf=ed98ed1dde79fe91cfde11b8d5dfa738f802992f lsremote=ed98ed1dde79fe91cfde11b8d5dfa738f802992f develop=5e4fde7177ea020de39b117f6d89cfa8f7c62be2 origin/main=2b11f762f611697e8be9be0d6853653df2fec025 | akte=evidence/r27-welle5-2026-11-06/control-plane-single-default/round-4.md
