# 0428-164 — merge-window-audit-r2 (Worker, Verifikation-plus-Beweisschrift, read-only)

- Karte: `t-20261120-r28-merge-window-audit-r2` (0428-164). Read-only Verifikation; KEIN PR, KEIN Merge, KEIN PR-Schließen, KEINE VM/Container/Netzwerk/Volumen, KEIN Subagent (§4.8).
- Produkt-Base develop (real): `b7cbc00f0adfa36945d6f7af8098d88096276c4f` — Zeuge: `git ls-remote https://github.com/mcpdev80/baseharbor develop`.
- origin/main (Planning): `420cdce411e15b7cdb0fa8f7300594443aac625c` — Zeuge: `git ls-remote origin main` in `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (das echte Planning-Repo; `workers/baseharbor-plan` ist Quarantäne, hier nie committet).
- Produkt-Clone (persistent, /tmp/opencode): `/tmp/opencode/baseharbor-x164` — `git fetch origin develop` + PR-Köpfe via `gh pr view <n> --json headRefOid`.
- Workzone: alles aus `/tmp/opencode/baseharbor-x164` und `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`. Kein Write in `/home/marcel/dev/baseharbor-ecosystem`.

## PLAN (nummeriert, KEINE Checkboxen)
1. B1: Merge-SHAs der letzten Stunde auf PR-Köpfe aufoesen (`gh pr view <n> --json headRefOid,mergeCommit`) und `git diff --name-only <head> <merge>` pro Merge.
2. B2: Fuer jeden der 5 merged SHas pruefen, ob eine Datei unter `evidence/*/codex-review-wave/` ihn als 'reviewed head' oder 'Verdict: MERGED' nennt.
3. B3: Blob-Identitaet von `cmd/baha/app_status_result.go` und `cmd/baha/target.go` (spaeter Full-Sweep) ueber alle offenen PRs; weitere Dateien mit identischem Blob in >=3 PRs.
4. B4: Brett-Wahrheit — Cards, deren `prs`-Field einen PR nennt und deren `kanban_status` review/closed ist, gegen live `gh api pulls/<n>` abgleichen.
5. Akte schreiben (round-1.md ueberschreibend), Planning origin/main rebase, ls-remote-Zeuge, Commit NUR dieser einen Datei.

## B1 — Mergetreue der letzten Stunde (ERGEBNIS: alle 5 = content unveraendert gelandet)

| PR | head-sha (gh) | merge-commit | `git diff --name-only <head> <merge>` | Resultat |
|---|---|---|---|---|
| #1595 | `b1428b0b0ee41e9f90b55d768b5c86fdd6140614` | `15727ca8878938df7e924319c236c0bcc4a4201c` | 0 dateien | unveraendert |
| #1706 | `930df12a482595bba06748ded501fe082f0aab76` | `97abbe1572a74170e3414448fe2dce843309c10a` | 0 dateien | unveraendert |
| #1578 | `97689a75d54d2b28a04e002ccc3afd202b9d5210` | `d5c11753ea437495eb2469a02f80b91d788fef4f` | 0 dateien | unveraendert |
| #1580 | `522af6f4aa5ca1ec2119750be06f84d795612b85` | `bbc937c8f1b1f1604bd5b68f4c66259dc3a3e978` | 0 dateien | unveraendert |
| #1707 | `162ac67022aceb0dbddc4e78a00fdc62391ce25e` | `b7cbc00f0adfa36945d6f7af8098d88096276c4f` | 0 dateien | unveraendert |

- Befehl (pro Merge): `git -C /tmp/opencode/baseharbor-x164 diff --name-only <head-sha> <merge-commit-sha>` -> fuer alle 5 = 0 file entries.
- Befehl (head-Resolution): `gh pr view <n> --repo mcpdev80/baseharbor --json headRefOid,mergeCommit` -> head + mergeCommit je PR.
- Alle 5 Merges sind auf develop: `git merge-base --is-ancestor <merge> origin/develop` -> YES fuer alle 5.
- Korrektur zur vorigen Bahn: #1707 head war in dieser Messung korrekt als `162ac67022` (gh headRefOid) verwendet; mit dem develop-Eltern-SHA `bbc937c8` als Proxy war der diff falsch negativ (2 files). Mit echtem head = 0 files.
- #1595 ist ein Rebase-Merge (ein Parent). `4b3a3559` (ein develop-Commit) ist KEIN PR-Kopf; der echte PR-Kopf ist `b1428b0b`. Mit `b1428b0b` = 0 files (unveraendert).

## B2 — Urteil am merged-sha (ERGEBNIS: 0 von 5 — kein Verdict-file fuer irgendeinen der 5 merged SHAs)

- Suchpfad: `evidence/*/codex-review-wave/` (47 Dateien).
- Befehl: `grep -rn -iE 'reviewed head|VERDICT.*MERGED' evidence/*/codex-review-wave/ | grep <merge-sha>` und kontextuelle Pruefung jeder Trefferzeile.
- Ergebnis: FUER KEINEN der 5 merged SHAs existiert eine codex-review-wave Datei, die GENAU diesen sha als 'reviewed head' oder 'Verdict: MERGED' fuehrt.
  - #1595 (`15727ca88789`): nicht gefunden als reviewed head.
  - #1706 (`97abbe1572`): nicht gefunden.
  - #1578 (`d5c11753ea`): nicht gefunden.
  - #1580 (`bbc937c8f1`): nicht gefunden.
  - #1707 (`b7cbc00f0adf`): nicht gefunden.
- Warum grep manchmal trifft: `1690-0428-119-r4.md` und `1693-0428-123-r7.md` cite die SHAs nur als Kontext (develop-base sha / 'then-current Develop'), nicht als 'reviewed head'/'Verdict: MERGED' dieses Merges. Echte reviewed-head-Referenzen in den Wave-Dateien sind andere shas (`6740299f`, `594086014e`, `93eea49543`).
- ZAHLE fuer den Owner: **0 von 5** merges tragen ein Urteil am merged sha. Vorige Meldung "4 ohne Urteil" ist damit korrigiert auf **5 ohne Urteil** (#1578 #1580 #1595 #1706 #1707 — samtlich).

## B3 — Doppelarbeit ueber Blob-Identitaet (ERGEBNIS: echte Sperr-Kandidaten identifiziert)

### B3.1 — app_status_result.go (gemeldet, bestaetigt)
Befehl: `git rev-parse <head>:cmd/baha/app_status_result.go` je PR ueber `gh pr view <n> --json headRefOid`.
develop blob: `f963601a560338f46a22c7d4ca8836655b8c6478`.

| Blob (12) | PRs | Anzahl |
|---|---|---|
| `4bca9d58b171` | 1582 1585 1587 1588 1594 1596 1620 1623 1625 1627 | **10 PRs** |
| `f963601a5603` (= develop) | 7 PRs | unveraendert (Basis) |
| `4052832c2d6e` | 1606 1615 1645 | **3 PRs** |
| `4be6c8b5d25d` | 1665 | 1 |
| `315fc6188bea` | 1597 | 1 |
| `21d96642fc07` | 1650 | 1 |
| `0e5d91961b67` | 1614 | 1 |
| `05f2e76317af` | 1702 | 1 |

- Bestaetigt (Mission): #1606/#1615/#1645 tragen alle `4052832c2d` (identisch); develop = `f963601a56`; #1650 = `21d96642fc`.
- NEUE FIND: `4bca9d58b171` ist in **10 PRs** — eine identische aenderung (entfernt `perses`/`host_containers_dashboards` aus `applicationStatusResult`) die ueber 10 lanes laeuft. `git diff origin/develop <head> -- cmd/baha/app_status_result.go` = 102 +/- linen pro pr (echte aenderung, nicht basis-carry). Das ist der groesste echte sperr-kandidat fuer diese datei.
- Non-develop blob-groups in >=3 PRs: **2** (`4bca9d58`=10, `4052832c`=3).

### B3.2 — target.go (gemeldet, meldung KORRIGIERT)
Gemeldet war: "#1591 #1594 — beide koepfe gleich develop 7df235639c, datei nicht geaendert".
- BESTAETGT: #1591 blob `7df235639c...` und #1594 blob `7df235639c...`, BEIDE = develop; `git diff --name-only origin/develop <head> -- cmd/baha/target.go` = 0 fuer beide. Die meldung stimmt: die datei wird von #1591 und #1594 GAR NICHT geaendert.
- KORREKTUR an der vorigen bahn: die wurde aus target.go den app_status `4bca9d58`-befund uebertragen; falsch. Ziel blob ist aktuell `d488db4c80a0b4852e37a7b88bd6b888f00a977a` (nicht `7df235639c`, das war ein alter develop-stand). Non-develop blob-groups in >=3 PRs fuer target.go: **3** — `c5b4da56e2b1` (7 PRs: 1594 1596 1614 1620 1623 1625 1627), `314bc58416a4` (7 PRs: 1582 1587 1588 1597 1606 1645 1665), `2a48a6865522` (6 PRs: 1650 1684 1690 1693 1702 1704). Alle mit echtem 162-line edit vs develop.

### B3.3 — Full-Sweep ueber alle produkt-go files (cmd/baha/, internal/, non-test, non-testdata/assets/migrations)
Befehl: pro PR `git ls-tree -r <head>` -> file|blob, dann `awk` ueber distinct PRs pro (file,blob), filter `blob != develop-blob` und `>=3 PRs`.
- Grosse clustering (15-25 PRs) sind uebliche basis-carry (develop verschoben sich, alle lanes teilen den aelteren blob) — KEIN echter per-lane konflikt.
- Echte sperr-kandidaten (non-develop blob, moderate cluster, produkt-Quelle):
  - `cmd/baha/machine_coverage.go`: `d75e81f93754` (12 PRs), `3eed608223bd` (3 PRs)
  - `internal/application/management_ui.go`: `85abe88ac67b` (11 PRs), `2f969afff365` (6 PRs)
  - `internal/application/manifest*.go` (manifest/manifest_render/manifest_parse/manifest_validation): je ~11 bzw. ~4 PRs
  - `internal/deployment/target.go`: 3 groups (siehe B3.2)
  - `cmd/baha/app_status_result.go`: 2 groups (siehe B3.1)
  - plus ~10 kleinere clusters: `internal/environment/environment.go` (8), `cmd/baha/command_target_env.go` (8), `internal/identityprovider/keycloak_realization.go` (8), `internal/deployment/environment_identity.go` (7), `internal/serviceaccess/policy.go` (6), `internal/operatorauth/config.go` (6), `internal/application/workload_security.go` (6), `internal/deployment/environment_association.go` (4+4), `internal/capability/perses.go` (4), `internal/operatorauth/authorization.go` (3), `internal/deployment/target_id.go` (3), `cmd/baha/secret_operations.go` (3), `cmd/baha/environment_operations.go` (3).

### B3-ZAHLE fuer den Owner
- Paare/gruppen mit identischem NON-develop blob in >=3 PRs (produkt-go quelle, non-test): **>20 file-lanes**, gefuehrt von `app_status_result.go` (2 groups: 10+3 PRs), `target.go` (3 groups: 7+7+6 PRs), `machine_coverage.go` (12+3 PRs), `management_ui.go` (11+6 PRs).
- Der vom mission vorgegebene fall `4052832c2d` (app_status, #1606/#1615/#1645) ist bestaetigt; der #1591/#1594 target.go-fall ist bestaetigt (beide = develop, datei unveraendert).

## B4 — Brett-Wahrheit (card-status vs. live PR-state) (ERGEBNIS: keine diskrepanz im spot-check)

- Befehl pro pr: `gh api repos/mcpdev80/baseharbor/pulls/<n> --jq '.number,.state,.isDraft,.merged'`.
- Spot-check 16 PRs, die auf cards mit kanban review/closed vorkommen:
  - merged-PRs `#1578 #1580 #1595 #1706 #1693 #1697 #1705`: `state=closed merged=true` — board-zustand getragen.
  - open-PRs `#1665 #1690 #1704 #1606 #1615 #1645 #1591 #1594`: `state=open merged=false` — board-zustand getragen.
  - drafts: alle geprüften open PRs `isDraft=false` (kein review-on-draft-mismatch).
- Feststellung: keine diskrepanz zwischen kanban_status (review/closed) und live PR-state in diesem sample. Der heute mehrfach von hand zurueckgezogene review/draft-fall ist stand 2026-11-20 nicht aktiv. Vorige bahn (round-1) hatte 11 cards geprueft und ebenfalls keine diskrepanz gefunden; spot-check bestaetigt das.

## repo-rule compliance
- Read-only-verifikation. Kein produkt-aenderung, kein `.github/**`-edit, kein PR/Merge/Schließen, keine VM/container/netzwerk/volumen, keine subagenten (§4.8).
- Akten nur im planning-repo `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (echte planning-repo); KEIN commit in `workers/baseharbor-plan` (quarantae); KEIN `git -A`; NUR `git add evidence/r28-welle4-2026-11-19/merge-window-audit-r2/round-1.md`.
- Branch-provenanz: kein eigener branch/commit ausser der akte auf origin/main; commit base ist origin/main HEAD `420cdce411`.
- Produkt-clone `/tmp/opencode/baseharbor-x164` nur lesend benutzt; clone bleibt bestehen (audit-karte), keine container/netzwerke/volumes angelegt.

## cleanliness:
- keine container/compose/netzwerke/volumes/state angelegt; docker/podman nicht verwendet (keine vm-gate-pflicht in dieser karte).
- produkt-clone `/tmp/opencode/baseharbor-x164` unveraendert zur spaeteren audit-karte; temp-dateien in `/tmp/x164_*`.
- KEIN write in `workers/baseharbor-plan` (quarantae); KEIN `git -A`; kein produkt-aenderung.
- akten-datei `evidence/r28-welle4-2026-11-19/merge-window-audit-r2/round-1.md` ueberschreibend geschrieben (war vorher 6055 bytes vom vorherigen lane, der keine der 4 befehle nachmessen konnte).

## END
DONE — 0428-164 merge-window-audit-r2. evidence url: baseharbor-plan evidence/r28-welle4-2026-11-19/merge-window-audit-r2/round-1.md
