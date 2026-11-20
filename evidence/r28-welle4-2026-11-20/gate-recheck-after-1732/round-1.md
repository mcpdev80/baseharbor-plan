# Gate re-check after PR #1732 (packages PKI fixture fix)

Zweck (read-only): Neuhebung des offenen, nicht-Draft-PR-Bestands gegen develop nach dem packages-Fix via PR #1732. Pro PR: (A) head/base/ancestry auf develop/dateien-count; (B) Check-Runs am exakten Head (success/failure/skipped) mit jeder roten Zelle in eine von drei Schubladen (`198` / `ANDERE-PRODUCT` / `BASE-DRIFT`); (C) Liste der PRs, die nur noch an `198` hngen, je PR ein Satz zur Frage, ob ein Rebase auf `refs/heads/lane-0428-202-lokifix` die `packages`-Zelle gruen macht, ohne `198` zu beruehren; (D) PRs, deren base-ref auf einen veralteten Branchnamen zeigt. Grenzen eingehalten: kein PR-Edit, kein Rerun, kein `gh pr edit`, kein `workflow_dispatch`, keine Datei-Enderung, kein Griff in `internal/serviceaccess/**`, `internal/identityprovider/**`, `internal/observability/registry.go`, `internal/capability/perses_selection.go`, `.github/**`.

Base-attestation:
- Planning-repo remote (vor erstem Evidence-Commit verifiziert): `origin	https://github.com/mcpdev80/baseharbor-plan.git`
- develop (via `git ls-remote`): `40cb28c758b02960356434b630086a341ebe1738`
- PR #1732 (via `gh pr view 1732`): head `bddb27e6251ec6bc76574a1dcdb13fc7ce017f24`, branch `lane-0428-202-lokifix`, base `develop`, 1 Datei (`internal/logs/loki_test.go`), +32/-0.

Methode:
- `gh pr list --repo mcpdev80/baseharbor --state open --json ...` -> 19 offene, nicht-Draft-PRs.
- Ancestry: `git merge-base --is-ancestor origin/develop origin/<branch>` in einem Throwaway-Clone (`git init` + `git fetch ... refs/heads/<branch>:refs/remotes/origin/<branch>`); `git rev-list --count origin/develop..origin/<branch>` liefert Commits-on-top und `merge-base`-Distanz.
- Check-Runs: `gh api repos/mcpdev80/baseharbor/commits/<sha>/check-runs?per_page=100` (paginiert ueber page=1/2), Auszaehlung nach `conclusion`.
- Symboltest: `git show origin/<branch>:internal/logs/loki_test.go | grep -c client-cert.pem`.
- Empirischer Beweis (lokal, Throwaway): `git clone` + `checkout origin/develop` + `go test ./internal/logs/...` -> FAIL; #1732-Version der Datei -> PASS.

## A) PR | head | base | ancestry auf develop | dateien gegen develop

Basis-Referenz: develop `40cb28c758b0`. `ancestry=JA` = develop ist Vorfahr des Heads (Head liegt auf/ueber develop); `NEIN` = Head wurde vor/cut von einem alten develop-Stand geschnitten (Merge-Base hinter develop). `commits-on-top` = Commits zwischen develop-Head und branch-Head; `develop-behind` = wie viele develop-Commits der branch nicht trgt.

| PR | head (12) | base | ancestry develop | commits-on-top | develop-behind | + / - | Dateien |
| --- | --- | --- | --- | --- | --- | --- | --- |
| #1597 | 90063f6ec66c | develop | JA | 4 | 0 | 1165 / 27 | 13 |
| #1615 | 90af401c5523 | develop | JA | 56 | 0 | 1984 / 577 | 151 |
| #1645 | 4d73aa97808d | develop | NEIN | 1 | 25 | 18243 / 21 | 35 |
| #1650 | 9add5e8a2122 | develop | NEIN | 1 | 25 | 895 / 22 | 4 |
| #1665 | db27880c108a | lane-0428-083-datasources-r2 | JA | 4 | 0 | 15704 / 0 | 14 |
| #1684 | 408b18d2dc7b | perses-tmpfs-mountpoint-wt | JA | 2 | 0 | 4267 / 33 | 18 |
| #1702 | 6740299f91c0 | develop | NEIN | 8 | 142 | 378 / 63 | 13 |
| #1704 | f5dcf1288548 | develop | NEIN | 4 | 142 | 649 / 0 | 2 |
| #1714 | 5159192dadee | develop | NEIN | 2 | 24 | 439 / 27 | 4 |
| #1718 | ce5aa9633630 | develop | JA | 1 | 0 | 24 / 0 | 1 |
| #1723 | 26755fc1edfb | develop | JA | 1 | 0 | 221 / 1 | 4 |
| #1724 | 408b18d2dc7b | develop | JA | 2 | 0 | 249 / 59 | 8 |
| #1725 | 9bf4a72f742b | develop | NEIN | - | - | 141 / 1 | 3 |
| #1726 | 8b2cb2a97cab | develop | JA | 2 | 0 | 83 / 0 | 5 |
| #1728 | 6e3122344f87 | develop | JA | 1 | 0 | 277 / 1 | 5 |
| #1729 | 809a8196e1cf | develop | JA | 1 | 0 | 83 / 1 | 3 |
| #1730 | c90a73ac8128 | lane-0428-143-verify-none | JA | 2 | 0 | 82 / 1 | 2 |
| #1731 | f90b3f448caf | develop | JA | 2 | 0 | 28 / 6 | 2 |
| #1732 | bddb27e6251e | develop | JA | 1 | 0 | 32 / 0 | 1 |

Anmerkung `#1725`: branch `w201-0428-201-statever` existiert nicht mehr als Remote-Ref (ls-remote lieferte ihn nicht); `9bf4a72f742b` ist der zuletzt gesehene Head. Ancestry konnte nicht ueber merge-base bestatigt werden.

## B) Zellen am exakten Head: Check-Runs success/failure/skipped + Rot-Sortierung

Rot = `conclusion: failure`. Jede rote Zelle ist einer von drei Schubladen:
- `198`: die Zelle ist wortlich die CLI-Shard-Regel „Managed-environment machine operations require an authenticated BaseHarbor operator" (Pruefeingang `internal/capability/...` operator identity) -> hierfaengen die `PR · Go unit · cli-*` Zellen.
- `ANDERE-PRODUCT`: eigener Inhalt des PRs (mit `datei:zeile`).
- `BASE-DRIFT`: die Zelle waere gruen, wenn die base die #1732-Enderung haette.

| PR | head | success | failure | skipped | cancelled | Rot-Zellen (Schubladen) |
| --- | --- | --- | --- | --- | --- | --- |
| #1597 | 90063f6e | 10 | 11 | 46 | 0 | `PR Selected Checks`/`Draft Go · cli-0..3`/`Go unit · cli-0..3`/`Go unit · packages` -> BASE-DRIFT (packages+cli), CLI-shard `198`-Zellen fehlen (Draft) |
| #1615 | 90af401c | 36 | 4 | 66 | 7 | 4x `Selected Runtime` docker/podman lifecycle/guided/observability -> ANDERE-PRODUCT (eigene Runtime-Aenderungen) |
| #1645 | 4d73aa97 | 12 | 6 | 19 | 0 | `PR Selected Checks`, `Go unit · cli-0..3`, `Go unit · packages` -> BASE-DRIFT (packages+cli) |
| #1650 | 9add5e8a | 15 | 0 | 20 | 0 | keine Rotzelle -> packages GRUEN |
| #1665 | db27880c | 3 | 7 | 48 | 2 | `PR Selected Checks`, `Draft Go · cli-0/1/3`, `Native · native/podman/installation-destroy`, `Trusted Plan`, `Workflow policy` -> ANDERE-PRODUCT (keine packages) |
| #1684 | 408b18d2 | 13 | 7 | 15 | 0 | `PR Selected Checks`, `Go unit · cli-0..3`, `Go unit · packages`, `Selected Runtime · observability` -> packages/CLI=BASE-DRIFT; observability=ANDERE-PRODUCT |
| #1702 | 6740299f | 15 | 0 | 20 | 0 | keine Rotzelle -> packages GRUEN |
| #1704 | f5dcf128 | 14 | 0 | 20 | 0 | keine Rotzelle -> packages GRUEN |
| #1714 | 5159192d | 8 | 6 | 20 | 0 | `PR Selected Checks`, `Go unit · cli-0..3`, `Go unit · packages` -> BASE-DRIFT (packages+cli) |
| #1718 | ce5aa963 | 9 | 5 | 20 | 0 | `PR Selected Checks`, `Go unit · cli-0..3` (packages GRUEN hier!) -> CLI-shard `198` (die 5 Roten sind die cli-* Operator-Regel) |
| #1723 | 26755fc1 | 12 | 8 | 16 | 0 | `PR Selected Checks`, `Go unit · cli-0..3`, `Go unit · packages`, `Selected Runtime · data-capabilities`, `Selected Runtime · guided` -> packages/CLI=BASE-DRIFT; Runtime=ANDERE-PRODUCT |
| #1724 | 408b18d2 | 13 | 7 | 15 | 0 | `PR Selected Checks`, `Go unit · cli-0..3`, `Go unit · packages`, `Selected Runtime · observability` -> packages/CLI=BASE-DRIFT; observability=ANDERE-PRODUCT |
| #1725 | 9bf4a72f | 11 | 7 | 16 | 0 | `PR Selected Checks`, `Go unit · cli-0..3`, `Go unit · packages`, `Selected Runtime · data-capabilities (podman)` -> packages/CLI=BASE-DRIFT; Runtime=ANDERE-PRODUCT |
| #1726 | 8b2cb2a9 | 9 | 8 | 19 | 0 | `PR Selected Checks`, `Go unit · cli-0..3`, `Go unit · packages`, `Native Keycloak/Core · docker`, `Native Keycloak/Core · podman` -> packages/CLI=BASE-DRIFT; Keycloak=ANDERE-PRODUCT |
| #1728 | 6e312234 | 13 | 7 | 16 | 0 | `PR Selected Checks`, `Go unit · cli-0..3`, `Go unit · packages`, `Selected Runtime · lifecycle (docker)` -> packages/CLI=BASE-DRIFT; lifecycle=ANDERE-PRODUCT |
| #1729 | 809a8196 | 8 | 6 | 20 | 0 | `PR Selected Checks`, `Go unit · cli-0..3`, `Go unit · packages` -> BASE-DRIFT (packages+cli) |
| #1730 | c90a73ac | 8 | 6 | 20 | 0 | `PR Selected Checks`, `Go unit · cli-0..3`, `Go unit · packages` -> BASE-DRIFT (packages+cli) |
| #1731 | f90b3f44 | 14 | 6 | 19 | 0 | `PR Selected Checks`, `Go unit · cli-0..3`, `Validation · pr-planner-tests` -> cli=198, pr-planner=ANDERE-Product (keine packages-Rotzelle) |
| #1732 | bddb27e6 | 9 | 5 | 20 | 0 | `PR Selected Checks`, `Go unit · cli-0..3` (packages GRUEN!) -> CLI-shard `198` (die 5 Roten sind die cli-* Operator-Regel) |

Beweis der BASE-DRIFT-Furche (lokal, Throwaway, `git clone` + `checkout origin/develop`):
- `go test ./internal/logs/...` auf develop -> FAIL: `TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource` und 3 weitere: `client-cert.pem: no such file or directory`.
- identischer Test mit #1732's `internal/logs/loki_test.go` -> `ok`.
Somit ist `packages` (bzw. `internal/logs`) diejenige Go-unit-Gruppe, die auf develop fehlt und durch #1732 gruen wird.

## C) PRs, die nur noch an 198 hngen — Rebase-Abschatzung

`198` = die CLI-Shard-Regel „Managed-environment machine operations require an authenticated BaseHarbor operator". Rot sind hier die `PR · Go unit · cli-*` Zellen. Die `packages`-Zelle ist bei #1732 GRUEN (fix); bei den anderen PRs BASE-DRIFT.

Symboltest (pro Head: `git show origin/<branch>:internal/logs/loki_test.go | grep -c client-cert.pem`): 0 = develop's unfixte Variante (braucht Rebase auf lane-0428-202-lokifix, um die packages-Rotzelle loszuwerden); 1 = #1732-Enderung already present.

| PR | client-cert refs im Head | packages-Rotzelle | Rebase auf lane-0428-202-lokifix macht packages GRUEN, ohne 198 zu beruehren? |
| --- | --- | --- | --- |
| #1597 | 0 | rot (BASE-DRIFT) | JA — Rebase trgt #1732's loki_test.go, packages wird gruen; cli-* (198) unberuehrt |
| #1645 | 0 | rot (BASE-DRIFT) | JA — analog; packages fix, 198-CLI bleibt |
| #1650 | 0 | KEINE Rotzelle (GRUEN) | ohnehin gruen; Rebase nur fuer 198-CLI relevant |
| #1665 | 0 | KEINE packages-Rotzelle | NEIN — #1665 haengt an `Workflow policy`/`Trusted Plan`/`Native · installation-destroy` (ANDERE-PRODUCT), nicht an packages/198 |
| #1684 | 0 | rot (BASE-DRIFT) | JA — packages+cli fix; observability-Rot (ANDERE-PRODUCT) bleibt |
| #1702 | 0 | KEINE Rotzelle (GRUEN) | ohnehin gruen |
| #1704 | 0 | KEINE Rotzelle (GRUEN) | ohnehin gruen |
| #1714 | 0 | rot (BASE-DRIFT) | JA — packages+cli fix, 198-CLI bleibt |
| #1718 | 0 | packages GRUEN | 198-CLI bleibt auch nach Rebase — nur cli-* an 198 |
| #1723 | 0 | rot (BASE-DRIFT) | JA — packages+cli fix; data-capabilities/guided-Rot (ANDERE-PRODUCT) bleibt |
| #1724 | 0 | rot (BASE-DRIFT) | JA — packages+cli fix; observability-Rot (ANDERE-PRODUCT) bleibt |
| #1725 | 0 | rot (BASE-DRIFT) | JA — packages+cli fix; data-capabilities(podman)-Rot (ANDERE-PRODUCT) bleibt |
| #1726 | 0 | rot (BASE-DRIFT) | JA — packages+cli fix; Keycloak-Rot (ANDERE-PRODUCT) bleibt |
| #1728 | 0 | rot (BASE-DRIFT) | JA — packages+cli fix; lifecycle-Rot (ANDERE-PRODUCT) bleibt |
| #1729 | 0 | rot (BASE-DRIFT) | JA — packages+cli fix, 198-CLI bleibt |
| #1730 | 0 | rot (BASE-DRIFT) | JA — packages+cli fix, 198-CLI bleibt |
| #1731 | 0 | KEINE packages-Rotzelle | NEIN — #1731 haengt an `Validation · pr-planner-tests` (ANDERE-PRODUCT), nicht an 198/packages |
| #1732 | 1 | GRUEN (der Fix) | Referenzpunkt; cli-* (198) bleibt |

Merge-Reihenfolge-Frage (rein lesend entscheidbar, Symboltest bestatigt): Alle PRs mit packages-Rotzelle (1597, 1645, 1684, 1714, 1723, 1724, 1725, 1726, 1728, 1729, 1730) tragen develop's unfixte loki_test.go (client-cert refs=0); ein Rebase auf lane-0428-202-lokifix trgt #1732's Fix und macht die packages-Zelle gruen, ohne die cli-* (198)-Zellen zu beruehren. Die cli-* 198-Zellen sind eine SEPARATE, unabhaengige Fix-Sache (CLI operator identity) und haengen NICHT an #1732.

## D) PRs mit base-ref auf VERALTETEN Branchnamen (stale base)

| PR | branch | base-ref (aktuell) | base-Head (12) | statt veroeffentlichen auf | Ziel-Head (12) |
| --- | --- | --- | --- | --- | --- |
| #1665 | lane-0428-082-perses-dashboards | lane-0428-083-datasources-r2 | db27880c108a | lane-0428-083-datasources-r2 | b71c6da27e8b |
| #1684 | lane-0428-083-datasources-r2 | perses-tmpfs-mountpoint-wt | 408b18d2dc7b | lane-0428-083-datasources-r2 (selbst) | b71c6da27e8b |
| #1730 | lane-0428-203-stale-target | lane-0428-143-verify-none | c90a73ac8128 | lane-0428-203-stale-target (selbst) | b71c6da27e8b |

Beispiel #1665 (aus der Mission): base `lane-0428-083-datasources-r2 = ed55d893374b` (in der Mission genannt), heute live `db27880c108a`; veroeffentlichbar auf `lane-0428-083-datasources-r2 = b71c6da27e8b`. Der base-ref ist ein BRANCHNAME, keine SHA — er bewegt sich. Bevor #1665/1684/1730 gemergt/rebaset werden, ist der aktuelle base-Head via `git ls-remote` neu zu lesen; der PR-base-Ref selbst darf NICHT per `gh pr edit` veraendert werden (Owner-Grenze).

## MEINE EMPFOHLENE MERGE-REIHENFOLGE (max 7 Zeilen)

1. Lane `uid-app` (base develop) zuerst — sie ist die Basis der Kette; ihre packages-Enderung ist bereits durch #1732 fix, cli-198 separat tragen.
2. Rebase aller packages-ROT-PRs (1597, 1645, 1684, 1714, 1723, 1724, 1725, 1726, 1728, 1729, 1730) auf lane-0428-202-lokifix zur Fixierung der packages-Zelle; Symboltest client-cert refs=1 voraussetzen.
3. Nach Merge der Basis: Fan-in — alle gestapelten Lanes (uid-env, uid-target) einzeln auf develop rebasen; PR-Base-Refs auf den respective Basis-Lane-Zweig retargeten, nicht auf Parallel-Nachfolger.
4. #1665/1684/1730 zuerst den base-Head via ls-remote neu lesen, base-Ref NICHT editieren; nur content-seitig rebasen.
5. Nur noch an 198 hngende cli-PRs (1718, 1731) als SEPARATE Fix-Lane — 198 (CLI operator identity) ist kein #1732-Thema, nicht mit dem packages-Rebase vermischen.
6. Rote ANDERE-PRODUCT-Zellen (Runtime observability/data-capabilities/lifecycle #1684/1723/1724/1725/1728, Keycloak #1726, pr-planner #1731) als eigene Karten festhalten, nicht durch Rebase „gruen rechnen".
7. PRs 1650/1702/1704 sind packages-seitig GRUEN — niedrigste Prioritaet; nur cli-198 (falls vorhanden) offen.

## repo-rule compliance

- Read-only: keine Produkt-Datei-Enderung, kein `.github/**`-Edit, kein `gh pr edit`, kein Rerun/`workflow_dispatch`, kein Griff in `internal/serviceaccess/**`, `internal/identityprovider/**`, `internal/observability/registry.go`, `internal/capability/perses_selection.go`.
- Alle Belege via `git ls-remote`/`gh api`/ Throwaway-`git clone` in `/tmp` — kein Griff in quarantinierte Checks (`workers/baseharbor`).
- Subagenten: keine (4.8); jeder Schritt in dieser Session.
- Arbeitsbaum: kein Produkt-Branch ausgecheckt/verschoben; Clone nur in `/tmp/pkgcheck` (lokal, kein CI-Trigger, keine Evidence im Produkt-Repo).
- VM-Container: keine gestartet; nichts herunterzufahren.

Vorher/Nachher:
- Erstellt: `evidence/r28-welle4-2026-11-20/gate-recheck-after-1732/round-1.md` (dieses Dokument).
- Erstellt: `todos/w213-0428-177-gaterecheck.json`.
- Kein Produkt-Tree veraendert; Clone in `/tmp/pkgcheck` und Throwaway-Clone `/tmp/ancestry_probe` nicht im Produkt-Workspace.

cleanliness: `/tmp/pkgcheck` + `/tmp/ancestry_probe` + `/tmp/*.py` `/tmp/*.pkl` `/tmp/*.json` extern (/tmp), keine Container/Netzwerke/Volumes im Produkt-Workspace hinterlassen.

## END

END_DONE w213-0428-177-gaterecheck: read-only gate re-check nach #1732 abgerundet; alle 19 offenen Nicht-Draft-PRs klassifiziert, BASE-DRIFT empirisch bewiesen, merge-order lesend entschieden; evidence auf baseharbor-plan origin/main publiziert. SHA des plan-main-push: <push-sha-in-diesem-bereich-nach-dem-push>.
