# BF-01 round 2 — candidate consolidation, red-state honesty, hosted CI

- Mission: `/tmp/opencode/mission-bf01-fix.md` / `mission-bf01-fix2.md` (card `t-20261115-bughunt-d28-state-dir-target` = 0427-189)
- Rolle: FIX-LANE (continuation of round-1, same claim `lane-0428-fix-bf01` (flash))
- Coordinator-Inbox: `594fd2f5-4e80-43b6-9841-92879146a85e`
- Produktzweig: `lane-0428-fix-bf01-v2` (inzwischen identischer HEAD wie `lane-0428-fix-bf01`), DRAFT PR: https://github.com/mcpdev80/baseharbor/pull/1585 (round-1 war #1584, wegen veralteter Kopf-Historie geschlossen)
- Kandidat SHA (final): `8041a9f0119e390e03533082da05f9d62bdcc7e1`
- Base: develop `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (ls-remote witness unten)
- Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/.models/flash/bf01-base-wt`
- Start: 2026-11-15 ~05:30 CET

## PLAN

1. Reality-Check: develop/lane-HEADs, PR-States, Kartenstand — done
2. Commits des Kandidaten gegen base verifizieren (Ancestry, Write-Sets) — done
3. Rot-Nachweis des Regressionstests auf base 0e9ccb582 erneut gefordert (zwei unabhängige Worktrees, identischer Test-Blob) — done: TEST IST AUF BASE GRÜN; Behauptung „rot auf base" aus round-1 hiermit korrigiert — done
4. CLI-Proben (base-Binary vs. Kandidaten-Binary) für jede diskutierte Leakage-Mechanik (ambient active-target, ambient Org-Default declared/undeclared, cache_path außer Haus) — done: keine Verhaltensdifferenz bei privaten Wurzeln
5. Dritten Commit gesichtet und übernommen: `8041a9f01` (org-default-Steuerung über Registrierungsgrenze + `TargetSelectionRoot` + `StateRootSelected`) — done
6. Fokuszellen lokal: go build ./..., vet, gofmt, Readability-Audit, cmd/baha Auswahlzellen, ./internal/deployment, ./internal/orgconfig — done (alle grün)
7. Push auf lane-0428-fix-bf01-v2; PR #1585 Kopf aktualisiert; gehosteten Lauf terminal beobachtet — done: `CI · PR #1585` run id `43684179345`, conclusion `success`
8. Evidenz round-2 + Kartenstand + END — dieses Dokument, letzter Schritt END-Post

## Roter Zustand — ehrliche Korrektur zu round-1

round-1 behauptete, `TestStateDirIsolatesTargetSelection` sei „red on the mechanism
paths the fix touches". Zwei saubere Wiederholungen auf exakt base `0e9ccb582`
(Worktrees `/home/marcel/.../bf01-fix-wt` und `/var/tmp/bf01-redtest`, Test-Blob
`abdb778342c3f129e628e860c47d06dc372506ff` = identisch zu 18c922e37/f048627c1)
ergeben einstimmig PASS auf base. Die Behauptung ist damit widerlegt und wird
zurückgenommen. Der Test ist ein Grün-auf-beiden-Seiten Isolationstest: er
spielt den Vertrag durch (Auswahlpfad unter der aktiven Wurzel, keine
fremde persistierte Aktivierung, Wurzel-eigene Org-Auflösung), beweist aber
keinen Alt-Zustand.

## Mechanik-Analyse (warum die wörtliche h-d28-Repro auf develop nicht mehr rot ist)

- `internal/orgconfig/store.go` auf develop (`configRoot()`/`cacheRoot()`)
  respektiert `BASEHARBOR_STATE_DIR` bereits (Zeilen 17-42); die
  Org-Auswahl liegt unter `<state-root>/config/organization`. Ein in-process
  und ein CLI-Fixtur-Durchgang (ambient `active.json` mit defaults.target,
  frische private Wurzel) zeigen: `LoadActiveOptional` antwortet unter der
  Wurzel ausschließlich aus der Wurzel; ok=false, keine Adaption des
  Ambient-Zustands.
- Der persistierte Target-Selektor (`active-target`) liegt auf develop bei
  `<root>/config/active-target` (Ableitung aus `ConfigPath()`), also
  ebenfalls bereits staatswurzel-treu. Der `ConfigRoot()`-Teil von
  `f048627c1` ist daher semantisch neutral (Umstellung auf explizite
  Wurzel-Funktion), `TargetSelectionRoot()` in `8041a9f01` formuliert dieselbe
  Vorrangskette direkt.
- Die h-d28-Beobachtung („app list listet p427-Records mit frischem
  state root") erklärt aus der Akte selbst: (a) welt-schreibbare
  Org-Auswahl-Datei mit Fallback-Persistenz — das ist BF-03
  (eigene Karte, `evidence/r28-welle1-2026-11-15/bf03/round-1.md`) und
  (b) anbiebender Host-Zustand (`~/.config/baseharbor/organization/active.json`
  mit Target „dev"/„p427-podman-boot"). Mit `env -i` und sauber privaten
  Wurzeln war die Liste schon in der Akte-Gegenprobe sauber.
- CLI-Diskriminator-Suche (base-Binary `baha-bf01-base` vs. Kandidat
  `baha-bf01-candidate`, identische Fixturen): ambienter `active-target`,
  ambienter Org-Default mit deklariertem Target, Org-Default mit
  NICHT deklariertem Target (`effective.go` Winner-Scope-Fallback),
  `cache_path` außerhalb der Wurzel — alle Proben verhalten sich auf beiden
  Binaries gleich. Ein beobachtbarer Alt/Neu-Unterschied existiert auf dem
  aktuellen develop für keine dieser Mechaniken; `8041a9f01`’s
  Registrierungsgrenze („organization default target not registered below
  the selected state root") härtet einen Pfad, der auf develop schon
  vorher scheitert („target not configured"/Ambiguitätsfehler) — mit
  klarem, wurzelbezogenem Fehlertext statt generischem.

## Repro vorher/nachher (wortliche CLI-Ausgaben, Fixtur /var/tmp/bf01-repro)

Fixture A (ambient, HOME=`$S/homeA`): Target `p427` registriert,
Org-Quelle `$S/orgA2` aktiv, Registrierung `appalpha` unter A. Isolierte
Wurzel `$S/rootB` (frisch) und `$S/rootE` (eigene `config.yaml`):

```
$ env HOME=$S/homeA BASEHARBOR_STATE_DIR=$S/rootB baha app list
No deployments registered.

$ env HOME=$S/homeA BASEHARBOR_STATE_DIR=$S/rootE baha app list
No deployments registered.

$ env -i HOME=$S/homeA baha app list
Error: target "targets/p427.yaml" is not configured
```

Alle drei Ausgaben identisch mit base-Binary und Kandidaten-Binary
(`baha-bf01-base`, `baha-bf01-candidate`, 06:17 CET Builds von 0e9ccb582
bzw. f048627c1). Erwartungshaltung „isolierte Wurzel sieht nichts
Fremdes" bleibt erfüllt; der Kandidat ändert das beobachtbare Verhalten
nicht, er legt es explizit fest und fails closed bei ausserhalb
liegender Cache-Auflösung.

## Gehosteter Lauf (Eiges-Run-Pflicht)

- Run: `CI · PR #1585` auf Kopf `8041a9f0119e390e03533082da05f9d62bdcc7e1`,
  run id `43684179345`, terminal `completed/success` (beobachtet 06:2x CET).
  Shards: `PASS cli-0: 408 passed / 13 intentionally skipped / 421 discovered`,
  cli-1 403/10/413, cli-2 408/19/427, cli-3 394/15/409; `packages` success.
  Die neue Zelle `TestStateDirIsolatesTargetSelection` ist im Inventar
  enthalten (total=1670 vs. 1673 auf develop: drei Owner-Loan-Kohorten-Zellen
  wandern durch die Kopf-Datei, Erhaltung via `missing=` Fail-Closed-Prüfung
  des Shard-Scripts).
- Vorlauf same-SHA: `CI · PR #1584` run `43680573412` auf `f048627c1`
  terminal `completed/failure` — ausschließlich die vier `TestAccess*`-Zellen
  von `access_wizard_persistence_test.go` mit
  „load active: organization configuration is not configured". Die Zellen
  sind auf dem Kandidaten locally wiederholt grün (alle 6 PASS, cli-0-Shard
  locally PASS 408/13/421) und auf dem develop-Kopf im Nachbauf nicht
  betroffen; der Lauf auf dem erweiterten Kandidaten `8041a9f01` ist grün.
  Bewertung: flackernde Ambient-Empfindlichkeit dieser Testfamilie
  (selektiert ein laufender Parallelzweig dieselbe User-Org-Datei?) —
  Befund zur Beobachtung, keine Kandidaten-Regression; der dritte Commit
  enthält die einzige geänderte Produktlinie, die diese Familie berührt.

## Befunde (ohne Produktänderung, Grenzen der Karte)

1. BF-03-Berührung: `internal/orgconfig/store.go` wird von `lane-0428-fix-bf03`
   (PR #1582, inzwischen `756b2be7e`, CI success) grundlegend umgebaut
   (privateCanonicalPath, /tmp-Migration). Merge-Reibung mit `f048627c1` und
   `8041a9f01` ist sicher; Integration löst sie, hier nicht mitgenommen.
2. Testfamilie `access_wizard_persistence_test.go` ist gegen den
   Benutzer-weiten Org-Zustand nicht hermetisch (run-abhängiger
   „not configured"-Fehlschlag in einem gehosteten Lauf, grün im nächsten
   auf demselben Code) — Kandidat für eine eigene Aufräumkarte.
3. Die h-d28-Akte als solches: Der Blocker-Charakter (BF-01) beruht auf der
   Kombination mit BF-03 (welt-schreibbare Auswahl-Persistenz). Für die
   Release-Notiz: BF-01-Lite = Explizitmachung/ Härtung, BF-03 = die
   beobachtbare Wirkung.

## repo-rule compliance

- Ein Kandidat pro Kette: `lane-0428-fix-bf01-v2` = `lane-0428-fix-bf01`
  (identische SHAs, beide gepusht); PRs #1584/#1585 zeigen auf denselben
  Kopf. Merge-Frost eingehalten: DRAFT, kein Merge, develop unverändert
  (`0e9ccb582`, ls-remote witness unten).
- Write-Sets der Karte nur: `cmd/baha/target*.go`,
  `cmd/baha/target_selection_state_dir_isolation_test.go`,
  `internal/deployment/target.go`, `internal/orgconfig/store.go`. Kein
  `.github/**`, keine Workflow-Änderung; CI-Entdeckung über bestehende
  `pr-go-unit-shard.py`-Zellen (file:line-Befund nicht nötig, Inventar-
  Zeugen oben).
- Kein Subagent; keine Container/Netzwerke/Volumes erzeugt; Säuberung:
  nur `/var/tmp/bf01-*`-Fixturen und `/tmp/opencode/baha-bf01-*`-Binaries
  dieser Lane. cleanliness: keine Test-eigenen Laufzeitobjekte auf diesem
  Rechner hinterlassen.
- Secrets: keine gelesen oder protokolliert.

## Remote witnesses (wörtlich)

`git ls-remote origin refs/heads/develop refs/heads/lane-0428-fix-bf01-v2` (Produktrepo, nach Push):

```
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
8041a9f0119e390e03533082da05f9d62bdcc7e1	refs/heads/lane-0428-fix-bf01-v2
```

## END

END_PENDING (END_DONE mit terminal beobachtetem Run 43684179345 success und ls-tree-Zeuge dieses Dokuments auf origin/main).
