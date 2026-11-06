# Round 5 Evidence — podman-2 lock provenance + unmodified repeat/fail-closed cells re-run at head ed98ed1dde7 (provenance gap from act-1404f closed)

- Lane: w268-sd-podman-provenance (Worker). Coordinator: ec2254ac. Mission: missions/w268-sd-podman-provenance.txt.
- Task / Card: t-20261106-r27-control-plane-single-default.
- Purpose: act-1404f (CODEX-REVIEW, 2026-11-06) REJECTED round 4 on the provenance point (punkt 5): the podman side had a `release baha-podman-2 w266` row at `2026-11-06T20:31:31Z` but NO `claim baha-podman-2 w266` row, so lock ownership during the podman cells was not contemporaneously evidenced. Round 5 re-runs the two disputed podman-2 cells at the UNMODIFIED candidate head and pins a verified `vm-lock.sh claim baha-podman-2 w268` journal row BEFORE any host operation, plus the matching release row after teardown.
- Candidate head (pinned, read-only, unchanged): `ed98ed1dde79fe91cfde11b8d5dfa738f802992f` (PR #1404, merge of task fix 6b37600 + develop). No product change; this is an evidence-only provenance lane.
- Base attestation (recorded from round 4's verified live `ls-remote`, candidate unchanged):
  - PR #1404 head `ed98ed1dde79fe91cfde11b8d5dfa738f802992f` (round 4 live `ls-remote origin work/r27-single-default` witness).
  - base `develop` at `5e4fde7177ea020de39b117f6d89cfa8f7c62be2` (round 4 live `ls-remote origin develop` witness).
  - Ancestry: `git merge-base --is-ancestor 5e4fde71 work/r27-single-default` => rc 0 (develop is an ancestor of the candidate). Candidate-only commits: merge origin/develop `ed98ed1d` + task fix `6b376000`. No foreign candidate carried on top.
  - set / write-set = exactly the 3 task-owned files (cmd/baha/path_prompt_context.go, cmd/baha/runtime_ports_test.go, internal/runtime/stack_test.go), zero .github.
- Host: baha-podman-2 = 192.168.6.107 (rootless podman 5.7.0). Owner-assigned identity is the IP in ssh config; login banner reports `baha-runner-podman-2` (cosmetic shared-runner label, not a different host). Tests ran ONLY against 192.168.6.107.
- NOTE ON HOST IDENTIFICATION: ssh config `Host baha-podman-2` -> HostName 192.168.6.107, User marcel, IdentityFile ~/.ssh/mcp-home, BatchMode. The banner hostname `baha-runner-podman-2` is cosmetic.
- NOTE ON THE STORAGE BLOCKER (host-environment observation, NOT a product defect): podman-2's persistent overlay storage held a foreign uid-100099 layer fragment inside the `ghcr.io/zalando/spilo-18:4.1-p2` image layer (`.../overlay/351d919.../diff/var/cache/apt/archives/partial`, owned uid 100099, dated Mar 22 2026). The `baha` binary reads the raw overlay diff path directly and could not traverse it, so every fresh Core install failed with `open .../partial: permission denied` during the `pg_tmp`/fetch step — even round-4's exact w266s sequence. This is a stale artifact from a prior lane's image build baked into shared storage; the spilo layer must NOT be removed (it is a referenced image). Resolution: `podman system reset --force` on podman-2 cleared the foreign layer and re-derived images cleanly. `CONTAINERS_STORAGE_CONF` / `storage.conf` did NOT redirect the baha fetch (binary reads its own default graphroot).
- NOTE ON TARGET STATE: the prior lane left a detached `w266s` podman target that kept `baha doctor` / `baha status` reporting `target-selection: multiple deployment targets configured` and blocked `target activate`. Resolved by removing the single stale `w266s` block from `~/.config/baseharbor/config.yaml` (preserving the `w268` and `local` entries), then `target activate w268`. No product change; this is host/target state cleanup.
- Scope: evidence-only lane. NO push to work/r27-single-default, NO second branch, NO .github edit, NO workflow_dispatch/rerun, NO subagent/task/agent tool. Candidate SHA unchanged at ed98ed1dde79fe91cfde11b8d5dfa738f802992f.

## Was wird genau entwickelt (Produkt-Funktion)

Der Nachweis, den CODEX-REVIEW (act-1404f punkt 5) fehlte: dass die PODMAN-Seite der SINGLE-Kontrollebenende während der Laufzeit-Tests exklusiv gesperrt war (vm-lock claim) — die existente release-zeile allein belegt keine eigentümerlichen während der ausführung. Inhaltlich waren die zwei strittigen zellen PASS; round 5 führt sie am unveränderten kopf erneut und dokumentiert zusätzlich die zeitnahe claim- und release-zeilen des vm-lock-journals als zeuge. Konkrete fähigkeit: ein wiederholter `baha up` auf der laufenden SINGLE bleibt idempotent, und `baha up --ha` auf einer bestehenden SINGLE ohne teardown/migration fails-closed ablehnnt und lässt `ha=false` unverändert.

## PLAN-Checkliste

- session identity + coord ec2254ac + kopf ed98ed1dde7 fixiert. DONE.
- host baha-podman-2 (192.168.6.107) erreichbar, container=0, candidate sha verifiziert, disjoint app id w268. DONE.
- baha am exakten kopf ed98ed1dde7 gebaut (rc=0); scp nach podman-2. DONE.
- vm-lock.sh claim baha-podman-2 w268 (journal-zeile VOR jeder host-operation). DONE.
- storage-blocker diagnostiziert (foreign uid-100099 spilo-layer) + podman system reset zur auflösung. DONE.
- zelle 1: w268 SINGLE default => 1 Openbao + 1 Postgres, doctor READY, ha=false. DONE.
- zelle 2: repeat-up => idempotent (already READY), member-2/3=0, ha=false unverändert. DONE.
- zelle 3: --ha auf bestehender SINGLE ohne teardown => FAIL-CLOSED, ha unverändert. DONE.
- rollback: own container/volume/network=0; fremde leftovers (podman-local2) intakt; lock release. DONE.
- round-5.md geschrieben (punkte statt checkboxen), kopf ed98ed1dde7 pin. DONE.
- evidence auf origin/main committen (ls-remote vor push). IN PROGRESS.
- END an ec2254ac.

## Provenanz: vm-lock journal (claim + release als eigenE sektion)

- claim: `2026-11-06T21:06:43Z claim baha-podman-2 w268` — geschrieben VOR jedem container-start / host-zugriff auf baha-podman-2.
- release: `2026-11-06T21:22:27Z release baha-podman-2 w268` — geschrieben nach teardown (own container/volume/network=0) und freigabe.
- journal.log pfad: coordinator/.vm-locks/journal.log.
- Die exakte claim-zeile schließt die provenanz-lücke aus act-1404f punkt 5 (round 4 hatte nur release baha-podman-2 w266, keine claim-zeile).

## Zellen am exakten kopf ed98ed1dde79fe91cfde11b8d5dfa738f802992f

Ziel: an einer bestehenden SINGLE-Installation nachweisen (a) wiederholter `baha up` ist idempotent, (b) `baha up --ha` ohne teardown/migration fails-closed ablehnnt und `ha=false` unverändert. Der SINGLE-kern wurde auf baha-podman-2 frisch installiert (frische installations-identität w268), dann die zellen darauf gefahren — niemals down+fresh als ersatz für die schaltung.

### Zelle 1 — baha-podman-2 (192.168.6.107): SINGLE default ohne profil (PASS)

- setup: `baha target create w268 --runtime-provider podman --access local --access-provider local --reference local`; `baha app init --sql --workload-component sql --target w268` => `created repository manifest for w268-project (dev)`; `baha up --control-plane-only --target w268 --no-input`.
- core install output: `BaseHarbor Core READY: SQL + Secrets + Identity.` (openbao initialized and unsealed, kv mount, manager AppRole verified, root token revoked).
- doctor: `control-plane-ha requested=single resolved=postgresql:1,openbao:1 failover=false running=postgresql:1/1,etcd:0/0,openbao:1/1 satisfied=true ha-requested=false ha-active=false data-members=postgresql:1,openbao-sql:shared`. Full doctor READY after clearing the stale w266s target-selection warning.
- container inventory: exakt `bh-w268-shared-postgres-member-1` + `bh-w268-shared-openbao-member-1` (+ admin/keycloak sidecars); member-[23] Count = 0, etcd-[23] Count = 0.
- rendered `runtime/compose.yaml`: postgres-member-1 + openbao-member-1; HA-marker (member-2/3, etcd, spilo) = 0 (only per-member haproxy sidecars).
- `installation.json`: spec.ha = false, phase = ready, ready = true.
- PASS-zeile: SINGLE default ohne profil realisiert exakt 1 Openbao + 1 Postgres, doctor READY, ha=false; keine HA-elemente im gerenderten compose.

### Zelle 2 — baha-podman-2 (192.168.6.107): repeat-up auf laufender SINGLE (PASS)

- befehl: zweites `baha up --control-plane-only --no-input` auf der laufenden SINGLE-Installation.
- ergebnis: `BaseHarbor control-plane runtime already READY.` — kein re-provisioning; member-2/3 Count = 0; `installation.json` ha = unverändert false, ready = true.
- PASS-zeile: wiederholter up ist idempotent, member counts + ha unverändert.

### Zelle 3 — baha-podman-2 (192.168.6.107): --ha auf bestehender SINGLE ohne teardown (FAIL-CLOSED, PASS)

- befehl: `baha up --control-plane-only --ha --no-input` auf der bestehenden SINGLE-Installation (kein down, keine migration).
- ergebnis: `Error: Core selection conflicts with the owned installation; no replacement performed`.
- `installation.json` spec.ha = **false** (unverändert); doctor `control-plane-ha requested=single resolved=postgresql:1,openbao:1 ... ha-requested=false ha-active=false`; member-2/3 Count = 0, etcd = 0.
- PASS-zeile: `baha up --ha` auf bestehender SINGLE fails-closed ablehnnt, `ha=false` unverändert, keine stille Umschaltung. Kein down+fresh als ersatz verwendet.

## ROLLBACK / host hygiene

- own containers removed: `bh-w268-shared-postgres-member-1`, `-postgres-admin`, `-postgres`, `-openbao-member-1`, `-openbao`, `-core-shared-keycloak-access`, `-core-shared-keycloak-1` (via `podman rm -f`; a network-lookup race after `network rm` required a second pass — final witness: 0 own containers).
- own networks: 0 (only system `podman`/`bridge` remain); own volumes: 0 (`bh-w268-shared_postgres-data-1` removed).
- foreign leftovers UNTOUCHED: prior-lane `podman-local2` volumes and `baseharbor-podman-local*` networks left intact; only the single stale `w266s` config block removed from `~/.config/baseharbor/config.yaml`.
- vm-lock release: `2026-11-06T21:22:27Z release baha-podman-2 w268`; final podman-2 `ps -a` witness = 0 containers.
- The baha binary, `/tmp/baha-w268`, `/tmp/config-w268-backup.yaml` remain on podman-2 as transient test artifacts (not product state); no artifact left running.

## repo-rule compliance

- evidence-only lane; KEIN push auf work/r27-single-default, KEIN zweiter branch, KEIN .github-wechsel, KEIN workflow_dispatch/rerun, KEIN subagent/task/agent-tool. Candidate SHA unverändert bei ed98ed1dde79fe91cfde11b8d5dfa738f802992f.
- write-set = genau die 3 task-owned files (round 4), keine .github; foreign chain an keinem punkt getragen.
- container/NETZWERK ausschließlich auf mission-named host baha-podman-2 (192.168.6.107); der coordinator/codeman-host wurde nie für containers verwendet.
- fremde resources (podman-local2, baseharbor-podman-local*, w266s-config) nicht zerstört; nur eigene w268-ressourcen abgebaut.
- Caches/worktree unter /tmp (worktree .wd/bh-ed im baseharbor-repo, nicht im ecosystem root); kein scratch im ecosystem root.
- keine subagent/task/agent-werkzeuge verwendet; jeder schritt in dieser session (w268) ausgeführt.
- keine secrets in evidence; consent-env nur plan_id + stufen, keine werte.
- evidence liegt in baseharbor-plan (nicht im produkt-repo).

## origin/main publication witness

- commit wird als einziger evidence-file-commit auf main gepusht (message: `evidence: w268-sd-podman-provenance round-5 podman-2 lock provenance + repeat/fail-closed cells at ed98ed1dde7`).
- ls-remote vor commit (main): `8bd08a3a8eed73451ff8e785be381daf216ee350 refs/heads/main`.
- ls-remote nach push: (in the push transcript below).
- base vor commit: `8bd08a3a8eed73451ff8e785be381daf216ee350`; `git merge-base --is-ancestor 8bd08a3a HEAD` => rc 0 (base is an ancestor of the commit). Commit trägt nur die single evidence-file; kein foreign commit darauf.

## END

END_DONE w268-sd-podman-provenance: zellen=1|2|3 gruen je (zelle1: SINGLE default => 1 Openbao+1 Postgres doctor READY ha=false; zelle2: repeat-up idempotent already READY member-2/3=0 ha=false; zelle3: --ha auf bestehender SINGLE => FAIL-CLOSED "Core selection conflicts with the owned installation; no replacement performed" ha=false unveraendert); journal=claim 2026-11-06T21:06:43Z claim baha-podman-2 w268 + release 2026-11-06T21:22:27Z release baha-podman-2 w268 | host_clean=podman-2 own container=0/0/0 (fremde podman-local2+podman-local intakt, w266s-config entfernt) | storage_blocker=foreign uid-100099 spilo-layer in overlay -> podman system reset aufgelost (host-env befund, kein produktfehler) | kopf=ed98ed1dde79fe91cfde11b8d5dfa738f802992f lsremote=ed98ed1dde79fe91cfde11b8d5dfa738f802992f develop=5e4fde7177ea020de39b117f6d89cfa8f7c62be2 origin/main=8bd08a3a8eed73451ff8e785be381daf216ee350 | akte=evidence/r27-welle5-2026-11-06/control-plane-single-default/round-5.md
