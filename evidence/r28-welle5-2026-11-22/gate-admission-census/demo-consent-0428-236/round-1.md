# 0428-236 round-1 — data-capabilities gate apply consent-retry: STOP (finding only)

Mission: `t-20261122-data-capabilities-gate-consent`, baseharbor-demo only. Core bleibt gesperrt, PR #1753 bleibt unberuehrt.

## PLAN

- (done) 1. ls-remote + pull des demo-repos (remote verified: `https://github.com/mcpdev80/baseharbor-demo.git`), develop-head abgeglichen, branch `lane-0428-236-gate-consent` in workers/0428-236-demogate-wt angelegt (Schnitt aus develop `5d1cf312`, base-attestation unten).
- (done) 2. Den apply-pfad des gates real ausgelesen (run.sh -> lib.sh -> new_edit.py chain) und mit dem BELEG-abgleich gefuehrt: der gemeldete fehler-pfad hat den consent-retry BEREITS; ein zweiter apply-pfad (fixture-consent.py) erkennt die refusal, fuehrt sie aber auf dem gemeldeten PTY-pfad nicht aus.
- (done) 3. Andockbarkeit ohne core-aenderung geprueft: NEIN — die einzige mechanik-freie route waere `--json`, die scheitert an der core gate-admission fail-closed (file:line unten). STOP-Kriterium getroffen: nichts umgebaut, keine product-datei in baseharbor-demo geaendert, kein PR eroffnet (PR gegen develop ohne aenderung ist sinnlos; die mission erlaubt nur die ANDOCKUNG, und die ist ohne core-aenderung nicht moeglich).
- (pending) 4. (entfaellt wegen STOP) — PR + hosted run nur bei successfullem andocken.
- (done) 5. Akte + END/QUESTION an coordinator 9142ab1f.

## Beweise (Messung, keine Behauptung)

### A0. Wo die mission-prämisive ("der gate nimmt diesen pfad nicht") sich wirklich bricht

- Der `run_consented`-wrapper (tests/lib.sh:182-184 -> tests/fixture-consent.py) wird im data-capabilities-gate NIRGENDWO aufgerufen: `grep -c "run_consented" tests/data-capabilities/run.sh` = 0; der einzige `$BAHA`-ruf in run.sh ist `status --verbose` (zeile 26, read-only). Der apply-pfad des gates laeuft stattdessen durch die Python-PTY-kette (run.sh:43 -> new_edit.py -> `apply_created_application`). Der consensus-retry existiert ALSO bereits auf einer anderen mechanik (PTY, capture_confirm_hash), nicht auf dem fixture-consent-pfad — das erklaert den scheinbaren widerspruch in der mission.

### A1. Der retry war zur Zeit des BELEG-laufs NICHT auf dem apply-pfad — und wurde NACH dem beleg durch echte PRs nachgeruestet (datiert)

- git-archäologie (baseharbor-demo, origin/develop history): der retry in `apply_created_application` (`--confirm-candidate` + `capture_provider_impact_candidate_hash`) kam erst mit PR #162 (merge f882382, 2026-11-16 10:16) und PR #163 (merge f23b6e0, 2026-11-16 11:52). Der provider-impact-zweig (zeile 346) existiert ab f882382.
- Der BELEG-lauf 44994268323 startete 2026-11-22T06:3xZ auf core PR #1753 head a40b7676; core ci.yml `:922` loest den demo-ref auf `heads/main` auf (gemessen: origin/main = 98e4d54, 2026-11-21). main enthaelt alle obigen retries ALLEIN durch die develop-merges — der demo-stand im beleg-lauf hatte den apply-retry also schoen. Das dokumentierte rot in jenem lauf erklaert sich durch die OTHER half: die `footprint show` admission auf dem data-capabilities gate, die genau PR #1753 aendert (cmd/baha/ci_integration_operator_enabled.go, footprint-fail-closed bis zu diesem PR). Das ist der Grund, warum PR #1753 Gruen werden sollte ohne irgendwelche demo-aenderung.
- Folgerung fuer die mission: ein demo-seitiger ANDOCK-Auftrag ist gegenstandslos, weil die mechanik laengst da ist UND das verbleibende defizit ausschliesslich in core liegt (PR #1753, gesperrt).

### A2. Undockbarkeit ohne core-aenderung — STOP-Beweis

### A. Der gemeldete fehler-pfad laeuft bereits durch den consent-retry

- BELEG run 44994268323 (core repo, PR #1753 head a40b7676), job 137122169353 `PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities) / Executed docker · data-capabilities`, log ~zeile 1686-1690: `Warning: Apply these changes? [y/N] y` → `Re-run with --confirm-candidate 3b332ee5…18597` → `Error: record deployment before mutation: candidate submission requires …`.
- Dieser transcript ist exakt der eingabestrom von `apply_created_application` (baseharbor-demo tests/guided/new_edit.py:338-357): erster `subprocess.run(argv=[BAHA,"app","apply"])`, dann `capture_confirm_hash(transcript)` (drive.py:80-93) und retry mit `[*argv, "--confirm-candidate", digest]` via `run_tty` (:355). Verifiziert durch direkte Messung: `capture_confirm_hash` auf den kopierten job-log-transcript liefert genau `3b332ee5c8c164e524c739488c1eb2b20c54c19d086ec2ddd10862edf6b18597`.
- Der gate ruft das: baseharbor-demo tests/data-capabilities/run.sh:43 -> tests/data-capabilities/new_edit.py (main) -> create_sql_removal_application (:57-71) -> `apply_created_application` (guided/new_edit.py:338). Der apply-pfad DES GATES hat den consent-retry also bereits; die mission-praemisse ("der gate nimmt diesen pfad nicht") ist fuer den PTY-apply-pfad widerlegt.
- Warum der retry im beleg-lauf nicht zur solution fuehrte statt dessen der FEHLER sichtbar blieb: der retry laeuft mit dem digest, aber der folgende `run_tty`-durchlauf endet erst in READY; das beobachtete rot stammt aus einem vorgelaagerten stand des gates — vgl. C (gate-admission), das in genau diesem PR #1753 gefixt wird (footprint show admission). Der core-consent-pfad selbst ist nicht der defekte teil.

### B. Der einzige apply-pfad OHNE retry ist fixture-consent.py — und der ist nicht der gate-apply-pfad

- baseharbor-demo tests/fixture-consent.py:36-73 (candidate_confirmation + set_candidate_confirmation) erkennt die refusal und haengt das flag an, aber nur fuer subprocess-pfade (non-PTY, `--json` erzwungen in :142-143). Benutzt von tests/lib.sh:182-184 (run_consented) und scripts/acceptance.sh:89 (destroy-cleanup). Der data-capabilities apply laeuft NICHT ueber diesen pfad, sondern ueber das PTY (A).

### C. Andocken ohne core-aenderung ist nicht moeglich (STOP-Beweis)

- Die einzige route, den PTY-apply auf den fixture-consent-retry zu ziehen, ist non-PTY `--json` — aber die core gate-admission ist fail-closed fuer `app apply`/`footprint show` auf dem data-capabilities gate: baseharbor cmd/baha/ci_integration_operator_enabled.go:118-148 (`command-not-in-managed-workload-set`, zeile ~180) laesst nur die aufgezaehlten canonical forms zu; genau das aendert PR #1753 (footprint show admission, zeilen 135-148 region) — und die mission sperrt core-aenderungen UND PR #1753.
- feature-detection wie tests/guided/drive.py:37 ist bereits implementiert und auf dem PTY-pfad aktiv; eine "ANDOCKUNG an den BESTEHENDEN consent-retry" ohne neue mechanik ist damit bereits realisiert — eine zusaetzliche anbindung waere doppelte mechanik und verletzt Regel 2 der mission.
- ZUSAETZLICH: das demo-repo kennt gar keinen getriggerten path fuer diesen pfad. `git grep -c "run_consented" -- tests/data-capabilities/` = 0 (grep ausgefuehrt: nur status/verbose); der gate hat keine apply-zeile. Das in der mission gemeinte andocken ist damit auch strukturell nicht moeglich: es gibt keinen apply-pfad in run.sh/lib.sh, der geaendert werden koennte.

## Basis-attestation (branch, unverandert gelassen)

- `git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/heads/develop` → `5d1cf312e18d06915db35c340bebe4e3d4f39d45` (gemessen vor branch-schnitt); branch `lane-0428-236-gate-consent` = exakt dieser SHA (lesend, kein content-commit).
- Working tree: `git status --porcelain` = 0 Aenderungen an versionierten dateien; ich habe in baseharbor-demo NICHTS geschrieben (kein PR, kein push — ls-remote bestaetigt 0 refs unter diesem branch-namen).

## repo-rule compliance

- Write set: keins genutzt (STOP vor any edit). Keine core-aenderung, keine PR-1753-aktion, kein broker, keine subagenten, kein merge/close/comment. Posten nur an coordinator.

## cleanliness

cleanliness: nothing started (this lane is read-only for 0428-236). Eigen pid 2993369. `docker ps -a` BEFORE = 0 entries; AFTER = 0 entries. Keine container/netzwerke/volumes; die worktree workers/0428-236-demogate-wt ist lesend (0 delta) und bleibt bis Coordinator-cleanup bestehen (kein product commit, therefore removal safe whenever).

END 0428-223-testctx BLOCKED (0428-236): STOP-Kriterium — consent-retry auf dem gate-apply-pfad bereits vorhanden (PTY route); andocken des fixture-consent-pfads ohne core-aenderung nicht moeglich (file:line oben); keine aenderung, kein PR. Candidate SHA: branch lane-0428-236-gate-consent = develop 5d1cf312 (unchanged). Uebergang zu 0428-231 korrekturronde PR #1761 wie befohlen.
