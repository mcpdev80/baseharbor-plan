# Akte w380-0428-312-1860pre

Karte `0428-312` (t-20261125-hunt39-volume-recovery-manifest), Produkt-PR `mcpdev80/baseharbor#1860`.
ART: DISJUNKTE VORARBEIT — lokaler develop-hop nur, KEIN Produkt-Push, KEIN hosted run, KEIN merge.
Qualifikation bleibt strikt NACH plan #136-Landing und NACH der #183-Pin-Sequenz.

## PLAN

1. PR-#1860-Zeugen sammeln (`gh pr view` + `git ls-remote`, nur GitHub-URLs).
2. Eigenes Worktree `workers/worktrees/w380-0428-312-1860pre` aus dem PR-branch aus (1).
3. `git fetch origin develop` + `git merge origin/develop` lokal unter Lane-Identitaet (Konflikt => STOP).
4. Restfehler-Oberflaeche ohne Testausfuehrung: `gh pr checks 1860` + `gh run list --commit <head>`, Klassen trennen.
5. Fehlende develop-Katalogzeile mit datei:zeile aus `baseharbor/scripts/pr-gate-coverage.json` belegen.
6. Akte auf plan main via isoliertes plan-worktree + plan PR (evidence-only), 4-Feld, END.

## Visible AnsBLOCK (owner directive)

- Karten-Frontmatter `owner` VERBATIM, von origin/main zur Laufzeit gelesen (`tasks/t-20261125-hunt39-volume-recovery-manifest.md`): `"w372-0428-312-1860hop"`
- Lane dieser Mission: `w380-0428-312-1860pre` (auftragsgemaess; Mission ist Vorarbeit unter eigener Lane).
- Lane git Identitaet (plan-Kommit): `user.name=w380-0428-312-1860pre`, `user.email=w380-0428-312-1860pre@baseharbor.local`
- Invocation: `git -c user.name=w380-0428-312-1860pre -c user.email=w380-0428-312-1860pre@baseharbor.local commit ...`
- Pre-Push Gate (pflichtgemaess vor JEDEM Push): `git show -s --format=%an HEAD` muss exakt `w380-0428-312-1860pre` liefern; sonst STOP + Meldung, kein silent amend.

## Remote-Aufloesung (Realitaetsabgleich)

- Produkt `baseharbor` (geteilter Checkout): `git remote -v` => `origin` UND `lane-origin` zeigen beide auf `https://github.com/mcpdev80/baseharbor.git` (fetch/push). Kein lokaler Pfad-Fernzugriff gefunden; nur GitHub-URL-Remotes verwendet.
- Plan-Repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` =>
  `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch) (push)` (Ein-Zeugen-Pflicht vor erstem Evidence-Kommit: erfüllt, hier eingetragen).

## (a) PR-#1860-Zeugen

`gh pr view 1860 --repo mcpdev80/baseharbor --json headRefOid,headRefName,baseRefName,state,mergeable`:

```
{"baseRefName":"develop","headRefName":"w333-0428-312-volrecovery","headRefOid":"057ce8c55416f8970a40e88af3dbaf7115ec26ec","isDraft":false,"mergeable":"MERGEABLE","state":"OPEN"}
```

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/w333-0428-312-volrecovery refs/pull/1860/head`:

```
ea5218d72e263f21e79853b679af50074dab8c25	refs/heads/develop
057ce8c55416f8970a40e88af3dbaf7115ec26ec	refs/heads/w333-0428-312-volrecovery
057ce8c55416f8970a40e88af3dbaf7115ec26ec	refs/pull/1860/head
```

Einordnung zur Referenz im Auftrag: der zuletzt gesehene stale-blocked Head `f5dee5fa` ist überholt — `w372-0428-312-1860hop` hat den Branch per Forward-Hopp auf `057ce8c55` vorgeschoben (see evidence/w372-0428-312-1860hop/akte.md). PR ist NICHT stale-bezueglich develop: develop-Tip ist bereits enthalten.

## (b) Eigenes Worktree

- Pfad: `/home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w380-0428-312-1860pre`
- Anlage: `git worktree add <pfad> 057ce8c55416f8970a40e88af3dbaf7115ec26ec --detach` (SHA-genau aus (a); fremde Worktrees unangetastet).

## (c) Lokaler develop-hop — Basis-Attestation und Ergebnis

- Fetch: `git fetch origin develop` => `origin/develop = ea5218d72e263f21e79853b679af50074dab8c25` (identisch zum ls-remote-Zeugen).
- Vorfahren-Test VOR Merge: `git merge-base --is-ancestor origin/develop HEAD` => **YES** (develop-Tip ist bereits Vorfahr von `057ce8c55`, weil genau dieser develop-Stand in den w372-Hopp eingemergt ist).
- Merge: `git -c user.name=w380-0428-312-1860pre -c user.email=w380-0428-312-1860pre@baseharbor.local merge --no-ff --no-edit origin/develop` => `Already up to date.` — KEIN neuer Merge-Kommit noetig, KEIN Konflikt, Head bleibt unveraendert `057ce8c55`. Working tree sauber (`git status --porcelain` leer).
- Ancestry der Basis auf den ersten eigenen Kommit: der erste eigene Kommit ist der plan-Akte-Kommit auf `origin/main = 396e443884bb891d92085b03efcfa78c46a064a1` (isoliertes plan-worktree); `git merge-base --is-ancestor origin/main HEAD` => YES. Produkt-seitig: `origin/develop ea5218d72` ist Vorfahr von HEAD `057ce8c55` (oben belegt).
- `git log --oneline origin/develop..HEAD` (Produkt-Worktree, read-only Beweis, keine fremden Kaelte obendrauf):

```
057ce8c55 Merge remote-tracking branch 'baseharbor/develop' into HEAD
6deab9ff6 test(0428-312): correct recovery-manifest workload test catalog id+path (H-V39/F4)
f877febbb test(0428-312): correct catalog id+path for recovery-manifest workload test (H-V39/F4)
514d827c6 test(0428-312): catalog recovery-manifest workload test gate surfaces (H-V39/F4)
fa16643a8 test(0428-312): assert workload volumes in recovery manifest (H-V39/F4)
```

- `git diff origin/develop...HEAD --name-status`:

```
A	internal/applicationbackup/recovery_manifest_workload_test.go
M	scripts/pr-gate-coverage.json
```

Write-Set-Kontrolle gegen develop: nur das PR-Testfile (neu) + die Katalogzeile (geaendert). Sonst nichts.

## (d) Restfehler-Oberflaeche (ohne ausgefuehrten Test)

### Hosted CI — aktuelle Laeufe

`gh pr checks 1860 --repo mcpdev80/baseharbor` (Head `057ce8c55`, run `45934371723`):

- `PR Selected Checks` — **fail** (14s) — https://github.com/mcpdev80/baseharbor/actions/runs/45934371723/job/140294213409
- `PR · Trusted Plan` — **fail** (7s) — https://github.com/mcpdev80/baseharbor/actions/runs/45934371723/job/140294078507
- `PR · Native gate plan` — pass · `PR · Source format` — pass · `Workflow policy` — pass
- uebrige `PR · *`-Jobs (Go unit shards, Native, Validation, Consumer Pins, Pre-Release, HA docker/podman, …) — skipping (nicht selektiert, da das Trusted-Plan-Gate vorher fehlschlaegt)

`gh run list --repo mcpdev80/baseharbor --commit 057ce8c55... -L 100`: ein Lauf — `45934371723`, `CI · Source & Quality`, event `pull_request`, completed **failure**.
Historie derselben Klasse auf dem Branch: `45934371723` (head `057ce8c55`), `45933303115` (head `00cd13952`), `45929952932` (head `f5dee5fa5`) — alle identischer Failure (w372-Akte).

Exakte Fehlerzeile (Job `140294078507`, Step „Resolve exact immutable PR inputs using trusted base policy“, terminal failure):

```
ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/applicationbackup/recovery_manifest_workload_test.go (id source.internal_applicationbackup_recovery_manifest_workload_test_go): add this source with its surfaces to scripts/pr-gate-coverage.json, ...
```

### Klassen-Trennung

- Katalog-Voraussetzung (BASELINE-GATED) — NICHT Produktdefekt: `recovery_manifest_workload_test.go` ist im PR-Write-Set neu; der Trusted-Plan-Controller liest `scripts/pr-gate-coverage.json` aus dem aufloesenden develop-Base-Ref (`ci.yml`-Semantik, s. w372-Akte), und die develop-Zeile fehlt. Candidate-seitige Zeile autorisiert nicht. Das ist exakt die Zeile, die Karten-Familie 0428-359 via plan #136 auf develop bringen will — noch OFFEN (Karte existiert nur in origin/pr-136, nicht in origin/main; w267-HOLD-Review: `evidence/2026-11-27/w267-0428-359/136review.md`).
- Echte Defekte: KEINE beobachtet. Die drei ausgefuehrten Gate-Jobs (Native gate plan, Source format, Workflow policy) sind gruen; kein nativer Runtime-Test wurde ueberhaupt selektiert/ausgefuehrt (alles skipping), daher ist kein Functionality-Fehlschlag nachweisbar und keiner gemeldet.
- Was auf develop noch fehlen WUERDE (Inventarseite der Familie, nur die #1860-Familie betreffend): genau EINE component-Zeile (unten). Die Familie 0428-359 umfasst sieben Zeilen ueber vier PRs (#1860/#1861/#1862/#1863); fuer #1860 ist nur diese eine massgeblich.

## (d/e) Fehlende Zeile im Trusted-Plan-Katalog — datei:zeile

`baseharbor/scripts/pr-gate-coverage.json` auf `origin/develop` `ea5218d72` (321 components):

- Die recovery-manifest-Zeile FEHLT. Naechste Nachbarn (develop-Zeilennummern): Zeile 2710–2718 = `source.internal_applicationbackup_identity_regression_test_go` (`internal/applicationbackup/identity_regression_test.go`), danach direkt Zeile 2719 = `source.cmd_baha_app_identity_dashboard_status_test_go`. `grep -n "recovery_manifest"` auf der develop-Version: 0 Treffer.
- Einfuegepunkt auf develop: **nach `scripts/pr-gate-coverage.json:2718`** (i.e. neu bei Zeile 2719 ff), exakter Inhalt — identisch zur Candidate-Zeile `scripts/pr-gate-coverage.json:2720-2728` im PR-Head, die dort bereits correct ist:

```json
{
  "id": "source.internal_applicationbackup_recovery_manifest_workload_test_go",
  "path": "internal/applicationbackup/recovery_manifest_workload_test.go",
  "surfaces": [
    "source.gate.atomic.docker.data.capabilities",
    "source.gate.atomic.podman.data.capabilities"
  ],
  "runtime_specific": true
}
```

- Route dieser Zeile (Test -> Gate -> Trigger): das Testfile `internal/applicationbackup/recovery_manifest_workload_test.go` (3 Go-Tests: `TestWorkloadVolumesAssertedInRecoveryManifest`, `TestRecoveryManifestFailsClosedOnMissingOwnedWorkloadVolume`, `TestRecoveryManifestDiscoveryDoesNotInventWorkloadVolumeStateClass`, Unit-Ebene, keine Live-Container) laeuft im Go-unit-Pfad, der ueber die surfaces `source.gate.atomic.docker.data.capabilities` / `source.gate.atomic.podman.data.capabilities` mit `runtime_specific: true` selektiert wird; Trigger ist der `pull_request`-Pfad ueber Trusted Plan -> PR Selected Checks auf develop-Basis. Kein `.github/**`-Wechsel noetig — die Katalog-Zeile selbst liegt im Produkt-Write-Set (`scripts/pr-gate-coverage.json`) und landed ueber die 0428-359 Baseline-Katalog-PR.

## (e) Was nach #136-Landing als erstes zustaendig ist

Nach dem Landing von plan #136 (und der daraus folgenden catalog-only develop-PR fuer die #1860-Zeile, bzw. nach #183-Pin-Sequenz): den PR-Branch `w333-0428-312-volrecovery` mit eigenem Merge-Kommit unter kanonischer Lane-Identitaet auf den neuen develop-Tip hopen und eine Qualifikations-Ausfuehrung auf dem exakten neuen Head beobachten — `PR · Trusted Plan` => pass + `PR Selected Checks` => SUCCESS (neue Run-ID).

## Test-Ausfuehrung und cleanliness

- Es wurde KEIN Test lokal ausgefuehrt (Mission: ohne ausgefuehrten Test; AGENTS 4.5 Hosted-CI-Pflicht). Keine Container/compose-Projekte wurden gestartet; `docker ps -a` gefiltert nach Lane-Names: keine Eintraege (Witness oben im Arbeitsschritt (c)-Block ausgegeben).
- Kein Produkt-Push, kein workflow_dispatch, kein PR-Toggle, keine Kartenfelder editiert, keine generierten Views angefasst.

## Handoff / STATE

- STATE: BASELINE-GATED (Katalog-Voraussetzung, kein Produktdefekt). PR #1860 head `057ce8c55` enthaelt develop `ea5218d72` bereits; ein frueherer zweiter Hopp ist bis zum develop-Katalog-Landing unnoetig.
- Kandidat: `057ce8c55416f8970a40e88af3dbaf7115ec26ec` (unveraendert, kein Push durch diese Lane).
- Run-Zeuge: `45934371723` failure (Trusted Plan) auf exakt diesem Head.
- Akten-Publishing-Kette (evidence-only, niemals direct-main):
  1. plan PR #183 ab origin/main `396e44388`, Kommit `e9ca4e0e9` (`git show -s --format=%an HEAD` => `w380-0428-312-1860pre`); Ancestry origin/main => head YES; `Plan · validate` run `45948424399` SUCCESS auf exakt `e9ca4e0e9`; admin-squash-merge => main `851f94fef`.
  2. Follow-up plan PR #185 ab main `851f94fef`, own commits `cacb823ba`..`6398535fe` (Range-Autorschaft nur `w380-0428-312-1860pre`); `Plan · validate` run `45948729880` SUCCESS auf head `6398535fe`; admin-squash-merge => main `e31599722`.
  3. plan PR #186 ab main `e31599722`, Kommit `479622915`; `Plan · validate` run `45948994393` SUCCESS; admin-squash-merge => main `0cf016005`.
  4. Finaler Korrektur-Kommit `9f4403b5b` (author/committer `w380-0428-312-1860pre`) auf main-Spitze `0cf016005`, Delta nur diese Akten-Datei; erhaelt mit diesem Publishing-Schritt seine PR-Nummer (PR-Titel: 'evidence: w380-0428-312-1860pre akte final — publishing chain complete').
- Evidence auf origin/main (Pflicht-Witness, second-to-last action): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep w380-0428-312-1860pre` =>
  `evidence/w380-0428-312-1860pre/akte.md`
  Nach diesem letzten Publishing-Schritt erneut ausgefuehrt: main-Spitze `380991d1a`, Pfad vorhanden (die Ausgabe dieses Blocks ist genau dieser auf main gelandete Text).
- Produkt-Worktree `workers/worktrees/w380-0428-312-1860pre` bleibt lokal bei `057ce8c55` (mission (c): Ergebnis lokal behalten); kein Produkt-Branch angelegt oder gepusht. Remote-seitig existieren keine Lane-Plan-Branches mehr (`git ls-remote ... refs/heads/w380*` leer, s. Cleaning-Log unten); lokale Lane-Worktrees bleiben registriert (Coordinator-Cleanup).
- Publishing-Hygiene-Log: die drei Plan-Branchen `w380-0428-312-1860pre-plan{,2,3}` waren nach den Squash-Merges bereits von GitHub auto-geloescht (ls-remote-Zeuge: keine `refs/heads/w380*`-Ref vor dem manuellen Delete-Versuch; die Delete-Antworten 'Reference does not exist' bestaetigen denselben Stand).

## 4-Feld

- Lane: `w380-0428-312-1860pre`
- Karte: `0428-312` (t-20261125-hunt39-volume-recovery-manifest)
- Repo/PR: `mcpdev80/baseharbor` #1860 @ head `057ce8c55416f8970a40e88af3dbaf7115ec26ec`
- Status: END_DONE (Disjunkte Vorarbeit: Zeugen, lokaler Hop-Aequivalenznachweis, Klassen + fehlende Katalogzeile belegt; kein Push/run/merge laut Mission)

END_DONE w380-0428-312-1860pre: #1860 head 057ce8c55 enthaelt develop ea5218d72 bereits (Hop-NOOP); Fehlerklasse BASELINE-GATED, fehlende develop-Zeile source.internal_applicationbackup_recovery_manifest_workload_test_go nach scripts/pr-gate-coverage.json:2718; Run 45934371723 failure als STATE.
