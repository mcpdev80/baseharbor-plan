# 0428-123 (r8) — merge-hopf + terminal CI run

**Card:** t-20261119-hunt-metrics-registration-visibility-only (0428-123)
**PR:** mcpdev80/baseharbor#1693
**Branch:** lane-0428-123-regvisibility
**Role:** worker (acceptance prep only; no product work)
**Mission file:** /var/tmp/x-123h.txt

## Was feststand (von Owner gemessen, nicht von der Bahn)

- CODEX-Verdict `1693-0428-123-r7.md` (baseharbor-plan main `7bad75ef`) sagt: **Verdict: APPROVE CONTENT — HOP REQUIRED BEFORE MERGE**.
- Kopf `93eea495437f` ist inhaltlich angenommen; Funktion (bedigungsloser provider-sweep in `internal/metrics/prometheus_files.go:139-142`, Anwendungsgrenze `:135` erhalten) durch; alle 7 Punkte der r7-Akte abgearbeitet.
- PR-base zeigte auf `28fb427f0574`; develop stand bei `d5c11753ea43` — Kopf 3 Hops zurueck (#1705, #1697/uid-app-Kette, #1595 059 source-model, #1706 symlink-enthaltung).
- Write-Set der Bahn: `internal/metrics/**`.

## ## PLAN (nummert, keine Checkboxen)

1. Realitaetsabgleich (§4.1): `git fetch` + `git ls-remote` develop / Branch / PR#1693-head; Ausgabe wortlich in die Akte.
2. Monotoner merge-hopf: `git merge --no-ff origin/develop` in `/var/tmp`-Worktree — zwei Eltern, kein rebase, kein reset, kein force-push.
3. Gate-Plan VOR und NACH dem Hopf: `python3 scripts/pr-gate-plan.py`, beide wortlich in die Akte (Basis-Distanz-beleg).
4. EIN pull_request-Lauf am NEUEN Kopf bis terminal, selbst beobachtet (§4.6). Kein workflow_dispatch, kein Rerun eines alten Kopfs.
5. Meldung: END_DONE mit neuem Kopf-SHA, Zwei-Eltern-Feststellung, Lauf-ID und terminalem Zustand.

## ## repo-rule compliance

- **Keine ProduktAenderung:** alle drei metrics-Dateien byte-identisch zum ursprünglich genehmigten Kopf `93eea495437f`. Der Hopf touchte `internal/metrics/**` nicht (diff `93eea495437f HEAD -- internal/metrics/` ist leer). Damit bleibt das r7-Verdict offen.
- **Kein Merge** (gehört CODEX), kein retarget der PR-Basis, keine `.github`/Script-Aenderung, keine Subagenten (§4.8), r7-Akte unangetastet.
- **Branch-Provenance:** Basis-Kopf `93eea495437f` (develop-Enkel, kein anderer PR-Kopf). Zeige `git show --parents`/`git log --format=%P`: Commit `270a0de6` hat genau zwei Eltern: `93eea495437f` und `d5c11753ea43`.
- **Evidence nur im planning-repo**, kein `.evidence/` im Produkt, kein main-Schreiben jenseits meiner einen Datei.
- Planning-Write gegen `https://github.com/mcpdev80/baseharbor-plan.git`, `fetch + rebase origin/main` vorher.
- Nur eine Datei (`fix-1.md`), kein `git add -A`.

## Realitaetsabgleich (wortlich, §4.1)

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-123-regvisibility refs/pull/1693/head
d5c11753ea437495eb2469a02f80b91d788fef4f	refs/heads/develop
93eea495437f2f9b4683211f9aafb24fd1798839	refs/heads/lane-0428-123-regvisibility
93eea495437f2f9b4683211f9aafb24fd1798839	refs/pull/1693/head
```

## Hopf — zwei Eltern (beweis)

```
$ git merge --no-ff origin/develop -m "0428-123 r8: merge-hopf onto moved develop (acceptance prep; content already approved r7)"
$ git log -1 --format='%P' 270a0de64ddab06f523f043df4177b0717b291d2
93eea495437f2f9b4683211f9aafb24fd1798839 d5c11753ea437495eb2469a02f80b91d788fef4f
```
Zwei Eltern bestaetigt: Kopf `93eea495437f` (eigen) + develop `d5c11753ea43`.

## Gate-Plan VOR dem Hopf (diff-base: Kopf 93eea495437f vs develop d5c11753ea43)

```json
{
  "merge_base_sha": "28fb427f057499efca705c1b7459e7653bd532a8",
  "target_base_sha": "d5c11753ea437495eb2469a02f80b91d788fef4f",
  "head_sha": "93eea495437f2f9b4683211f9aafb24fd1798839",
  "broad_required": true,
  "selected_gates": [],
  "unresolved_coverage": [
    "unknown impact for internal/metrics/prometheus_files.go",
    "unknown impact for internal/metrics/prometheus_render.go",
    "unknown impact for internal/metrics/regvisibility_regression_test.go"
  ]
}
```

## Gate-Plan NACH dem Hopf (diff-base: Kopf 270a0de vs develop d5c11753ea43)

```json
{
  "merge_base_sha": "d5c11753ea437495eb2469a02f80b91d788fef4f",
  "target_base_sha": "d5c11753ea437495eb2469a02f80b91d788fef4f",
  "head_sha": "270a0de64ddab06f523f043df4177b0717b291d2",
  "broad_required": true,
  "selected_gates": [],
  "unresolved_coverage": [
    "unknown impact for internal/metrics/prometheus_files.go",
    "unknown impact for internal/metrics/prometheus_render.go",
    "unknown impact for internal/metrics/regvisibility_regression_test.go"
  ]
}
```
Basis-Distanz nachweislich: merge_base ist jetzt `d5c11753ea43` (develop), Kopf liegt direkt oben drauf — kein fremder Commit dazwischen.

## CI-Lauf am neuen Kopf (selbobsachtet, §4.6)

- Lauf: PR #1693 auf Kopf `270a0de64ddab06f523f043df4177b0717b291d2`
- ls-remote nach Push:
  ```
  270a0de64ddab06f523f043df4177b0717b291d2	refs/heads/lane-0428-123-regvisibility
  270a0de64ddab06f523f043df4177b0717b291d2	refs/pull/1693/head
  ```
- Terminal-Zustand (alle 34 Checks):
  - SUCCESS (14): Workflow policy, PR · Native gate plan, PR · Source format, PR · Trusted Plan, PR · Focused Python, PR · Go unit · cli-0/1/2/3, PR · Go unit · packages, PR · Go unit · owner, PR · Validation · go-build, PR · Validation · go-vet, PR Selected Checks.
  - SKIPPED (20): Release Source Preflight, Targeted HA · docker, Targeted HA · podman, validate, PR · Main release source, PR · Main release Go, PR · Exact full Pre-Release, PR · Draft source/routing, PR · Draft Go, PR · Native, PR · Main release checks, PR · Runner Interface, PR · Consumer Pins, PR · Demo Pin, PR · Exact Candidate, PR · Candidate-added (advisory), PR · Native Keycloak/Core, PR · Public Contracts, PR · Selected Core-less, PR · Selected Runtime.
  - FAILURE/ERROR/TIMEOUT: **0**.
- SKIPPED-erklaerung (§5.4): die 20 SKIPPED sind Release/Pre-Release/Docker-Podman-Native gates, die fuer diesen 0.4.28-0428-Lane nicht zur Merge-Pf gehoeren; die required CI-Jobs (Go unit, go-build, go-vet, Focused Python, gate plan, Trusted Plan, source format) sind alle SUCCESS — das ist das terminale Passieren der echten Pflichtchecks. Kein gefaktes Ungetestetes.

## ci-fast-check (lokal, §CI-Policy)

```
$ bash scripts/ci-fast-check.sh   (aus baseharbor checkout)
Ran 286 tests in 55.621s
OK
No candidate-added validation checks.
```
Go file size baseline OK (längste Datei `internal/providers/runtime/podman/lifecycle.go` 843 Linien, ratchet <= 878). Workflow policy: 20 approved workflow files. Source readability PASS.

## cleanliness

- Keine container/netzwerke/volumes von mir gestartet (Start-by-me: none). Die 5 laufenden Container (`perses`, `bh-local-shared-postgres-1`, `bh-local-shared-openbao-admin-1`, `bh-local-shared-postgres-admin-1`, `bh-local-shared-postgres-member-1-1`) gehoeren anderen Lanes / shared infra; nicht von mir, nicht angefasst.
- /var/tmp Worktree `123-regvisibility-wt` nach Push und cleanup entfernt; stray Branches (`_develop`) im Worktree geloescht.
- /var/tmp Dir-Count vorher 984, nachher 983 (nur meine eine worktree-Entfernung).
- cleanliness: clean.

## Ende

END_DONE — Kopf `270a0de64ddab06f523f043df4177b0717b291d2`, zwei Eltern `93eea495437f` + `d5c11753ea43`, CI terminal 14 SUCCESS / 20 SKIPPED / 0 failures. Merge ist CODEX vorbehalten.
