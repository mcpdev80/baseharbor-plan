# 0428-110 fix-1 — mutation paths now fail loud (corrupt config + XDG double-append)

- Mission: `/var/tmp/missions/mission-110-mutation-loud.md`
- Karte: t-20261117-hunt-uid-docs-110 (0428-110), Claim: worker-flash (mission-110-mutation-loud), publiziert 2026-11-17
- Branch/Candidate: `lane-0428-110-mutation-loud` @ `1d01ea16c003adffa0dfd529282417956560e2a4`, PR #1682 (READY) gegen develop
- Rolle: WORKER (Fix-Lane)

## PLAN

1. ls-remote develop als erste Aktion + Planning-Repo wrong-zone check — DONE
2. Isoliertes tmp worktree + branch lane-0428-110-mutation-loud ab develop@bcae1e8c — DONE
3. Reproduktion beider silent-pfade am gebauten develop-Binaer (log-zeilen unten) — DONE
4. Fix: LoadConfigForMutation prueft wie der read-pfad; Save-Routen refusen overwrite/ghost — DONE
5. Regressionen unit (internal/deployment) + production command entrance (cmd/baha) — DONE
6. build/vet/gofmt + affected tests, readability audit — DONE
7. Push (refspec), PR #1682 READY auf develop — DONE
8. Eigener exact-head CI run bis terminal — laeuft, Run 44060840263 (Witness unten)
9. Akte + END — dieses Dokument

## Zone- und Basis-Zeugen

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop   # erste Aktion
bcae1e8c1261c9e44db03fe285a5d090c532dfcd	refs/heads/develop   # = Mission-Pin
```

Base attestation: branch geschnitten aus exakt `bcae1e8c1261c9e44db03fe285a5d090c532dfcd` (Vor-Rebase-Kopf `8e089dc47`, ancestor-Test yes). Nach dem Fetch von develop (62eaea2c8, #1604 + #1679 gemergt) sauber gerebased; `git merge-base --is-ancestor 62eaea2c8 HEAD` = yes. `git log --oneline origin/develop..HEAD` listet GENAU einen Commit: `1d01ea16c fix(0428-110): fail loud on mutation paths for corrupt config and XDG double-append` — kein artfremder Commit im Kandidaten.

## Reproduktion der silent-pfade (develop@bcae1e8c, gebautes Binaer, nur tmp-state, keine container)

Probe (identisch zur Befund-3-Matrix der Hunt-Akte, Zeile fur Zeile reproduziert):

| Fall | read `target list` | mutation `target create` | Dateizeuge develop-Code |
| --- | --- | --- | --- |
| corrupt yaml (mode 0600) | rc=1 parse-Fehler (loud) | rc=1 parse-Fehler, ABER: Save der naechsten Route ueberschreibt still (unit-Probe: LoadConfigForMutation err!=nil -> SaveExpected(nil) schreibt fresh cfg, Datei ersetzt) | config_mutation.go:24-38 Liest raw, aber Save-Pfad laedt nie |
| corrupt yaml (mode 0644, world-readable) | rc=1 parse-Fehler (loud) | rc=1 "protected existing owner" — OHNE decode; Save expected=nil schreibt FRISCHE cfg ueber den corrupten owner (unit-Probe: save err=nil, datei-now=fresh config) | readConfigurationOwner:117 rejected mode; save compare=false ueberspringt |
| empty file | rc=1 ErrConfigEmpty | rc=1 "unsupported config version 0" — fremde familie; Save expected=nil ersetzt still (unit-Probe: err=nil, datei-now=fresh cfg) | config_mutation.go:37 decodeConfig(raw) |
| XDG double-append (XDG_CONFIG_HOME endet auf /baseharbor, nested root unpopulated) | rc=1 ErrConfigMissing mit hint | **rc=0**, ghost-config.yaml wird EINENEbene hoeher ignoriert und nested neu angelegt: `find` zeigt baseharbor/baseharbor/config.yaml + baseharbor/config.yaml, user-cfg unveraendert, target NUR im ghost sichtbar (target list zeigt ihn nicht) | config_mutation.go:27-28 clean-default ohne populated-root/ghost-pruefung |
| populated root (active-target), cfg absent | rc=1 ErrConfigMissing | rc=0: schreibt frische cfg ueber die active-state-root hinweg | dito |

Konsole-zeugen (Auszug) vor dem Fix:

```
$ BASEHARBOR_STATE_DIR=...X target create ghost ...   # XDG double-append
Target ghost created (runtime docker, access local via local)
rc=0
$ find X -name config.yaml
X/baseharbor/baseharbor/config.yaml     # ghost, neu
X/baseharbor/config.yaml               # echt, ignoriert
```

## Fix

Write-Set: `internal/deployment/target.go`, `internal/deployment/config_mutation.go` (plus 2 neue Testdateien).

- `LoadConfigForMutation` prueft die geladene config auf dieselbe Weise wie `LoadConfig`: gleicher ErrConfigMissing/ErrConfigEmpty-sentinels, populated-root (`dirExistsAndHasBaseharborState`) und ghost-root (`configGhostRoot`) vor dem clean-default-Zweig; corrupt/leer owner geben die familie statt decode-Fehler (cause bleibt gewrappt sichtbar).
- `Config.Save` (read+overwrite-Route, z.B. `config prompt`): prueft einen EXISTENTEN owner zuerst per LoadConfig — ueberschreibt ihn nie ungelesen.
- `saveWithPreparation`: ghost-ablehnung VOR jedem MkdirAll/create (sonst waere das Layout nach root-Erzeugung nicht unterscheidbar); regularer existing-owner wird nie als acknowledged-absent bypassen (Lstat-regular-Check, CAS und bare route).
- XDG-double-append-Fall explizit konservativ: ablehnen + Hinweis (beide roots + Korrekturweg im Fehlerbild), KEIN silent dedupe/merge — wie in der Mission verlangt.
- Erste aktion auf einem sauberen Rechner (root existiert noch nirgends, kein ghost) bleibt der stille first-run-Pfad (rc=0, create + prompt getestet).
- Bestehende 0428-094-assertions (config_fail_loud_test.go) unveraendert gelassen — sie laufen alle weiter gruen (27 PASS der config-/load-/save-Gruppe).

Nach dem Fix (dasselbe Binaer-Kommando-Set): alle fälle rc=1 mit familie-fehler + hint; ghost-root nie angelegt (find-zeuge); user-config byte-identisch erhalten; first-run weiterhin rc=0.

## Regressionen

- `internal/deployment/config_mutation_fail_loud_test.go`: corrupt/empty/populated/ghost/clean-first-run auf `LoadConfigForMutation`, SaveExpected- und SaveExpectedPreservingTarget-Weigerung gegenueber corruptem owner ohne overwrite, read-path familie + hint parity.
- `cmd/baha/config_mutation_fail_loud_command_test.go`: `target create` (corrupt + double-append) und `target activate` ueber `targetCommand().Execute`, `config prompt` ueber `runWithIO` — jeweils der production command entrance (derselbe cli.Execute-command-tree-pfad, den das binary nimmt). Anmerkung: der target-create-pfad durch `runWithIO` wuerde auf den CI-hosts den owned-core readiness-schritt (connectivity probe) VOR dem config-load ausfuehren und mit runtime-unavailable gegen die family-assertion laufen; `Execute` umgeht den globalen bootstrap, praezedenzgleich zu `target_definition_native_test.go:74`.
- CI-Aufnahme: laeuft in der GitHub CI "Run release-source tests" (`go test ./internal/... ./spec/...` + `go test ./cmd/baha`) auf jedem PR — kein .github/** Eingriff noetig (Befund-Rezept der Hunt-Akte).

## Checks (lokal, isolated HOME; /tmp ist auf diesem host quota-limitiert — TMPDIR/GOCACHE unter /var/tmp)

- `go build ./...` ok, `go vet ./...` ok, `gofmt -l` leer
- `bash scripts/source-readability-audit.sh`: PASS (size/span/ratchet)
- `go test ./internal/deployment` (full, count=1): ok
- `go test ./cmd/baha -run 'TestTargetCreate|TestTargetActivateFailsLoud|TestConfigPrompt'`: alle PASS
- `go test ./cmd/baha -run 'Target|Config|Node|Prompt|Recovery|Onboard|Init'` (broad, count=1): ok (413s)
- `go test ./internal/application`: ok
- Pre-existing environment failures on this coordinator host, identical on the baseline (stash-Vergleich): `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` und `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication` brauchen docker/git-netz; diese Lane hat keine container gestartet (s. Sauberkeit).

## CI

- Run 44060840263 "CI · Source & Quality", headSha 1d01ea16c003adffa0dfd529282417956560e2a4, TERMINAL: completed, conclusion=success (beobachtet von dieser Lane bis zum Endzustand, 2026-11-17). Alle required Jobs gruen; die schweren runtime-Matrix-Jobs sind bei PRs skipped (selektiver Pfad nach CI-Regel der Repo-AGENTS).
## Sauberkeit

- Vorher/Nachher (dieser host, lane-eigene Projekte): `docker ps -a --format '{{.Names}}'` ohne die ambient-Zeilen = 0 zeilen; `docker compose ls` zeigt nur `bh-local-shared` (fremder karren, ambient-core container anderer lanes, owner-direktive 2026-11-08: unangetastet). Diese Lane hat KEINEN container/netzwerk/volume/compose gestartet. PS-Witness als letzte Aktion: Vorher identisch (0 lane-eigene), Nachher 0 — ps-zeuge im Transcript dieses turns.
- Lane-state: alle probe-roots (mission-110-{A..Z,EXP,RC,PG,V-*,MC*}) und fake-HOMEs sind GELUESCHT; uebrig: /var/tmp/mission-110-wt (Kandidat-worktree, bis Merge-Aufraeumen) + /var/tmp/mission-110-{tmp,gocache,gomod} (lane-Caches).
- Produkt-Arbeitsbaum /home/marcel/dev/baseharbor-ecosystem/baseharbor: unveraendert (nur fetch + worktree-add), kein Commit dort.
- cleanliness: this lane started no containers/networks/volumes/compose projects; all probe state under /var/tmp is owned by this lane and cleaned except the candidate worktree.

## Hinweise (fund, keine eigenmacht)

- **Laufzeit-Selbsttest der Test-Assertions (diese Lane, negative Pilotlaeufe):**
  - Family/check-Entfernung in `LoadConfigForMutation` (decode-family + populated/ghost): `TestTargetCreateFailsLoudOnCorruptConfig`, `TestLoadConfigForMutationCorruptFailsLoud`, `TestLoadConfigForMutationMissingUnderPopulatedRootFailsLoud`, `TestLoadConfigForMutationXDGGhostRootFailsLoudAndNeverWrites` → `--- FAIL` (Ghost-Write rc=0, user-cfg ignoriert).
  - Ghost-Zweig-Entfernung (root-absent branch, `if false`): `TestTargetCreateFailsLoudOnXDGDoubleAppend` → `--- FAIL` (create rc=0, ghost-config.yaml in der nested dir angelegt).
  - Save-route ghost-Zweig-Entfernung: der create-ghost-test bleibt gruen, weil die create-Sequenz (Load + SaveExpected) den Ghost zuerst im load-Zweig trifft — die CAS-Pruefung in saveWithPreparation ist die zweite Verteidigungslinie, kein Alleingang.
  Damit ist keine der neuen Assertions ein Papiertiger. Die leere-file- und save-route-assertions pruefen andere Code-Pfade (`readConfigurationOwner` mode-Check, `Config.Save` probe, `saveWithPreparation` CAS) und bleiben in den Piloten an — die Pfad-Trennung ist damit nachgewiesen.
- Die Host-Umgebung dieses coordinators teilt `~/.config/baseharbor` (entholt .installation.lock + organization/ von anderen lanes); Tests, die HOME nicht isolieren, erben dort ein populated-root ohne config.yaml und schlagen auf develop BASE vor — environment-Artefakt, kein Produktdefekt (baseline-Stash-Zeuge).
- Flaky-Kandidat (Befund fuer eine spaetere Karte, auferhalb dieses write-sets): `readConfigurationOwner` in LoadConfigForMutation lehnt eine EXISTENTE, aber nicht protected owner-datei (mode&0077 != 0) mit der generischen "protected existing owner" melodie ab, statt der config-familie — asymmetrisch zum read-pfad, der solche dateien liest. Diese Lane andert security.go/readConfigurationOwner bewusst nicht (Mission-GRENZE: security.go unveraendert).
- Die 094-Doku-Luecke (Befund 2: kein docs-Absatz fuer das neue Verhalten) bleibt offen und ist NICHT Teil dieses Fixes (Mission write-set); sie braucht eine eigene docs-Karte.

## origin/main-Zeuge (Pflicht, zweite-letzte Aktion)

```
$ git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main
ec8c38f451b80d2ceb005d1cb631222d1f701eb2	refs/heads/main
$ git ls-tree --name-only origin/main evidence/r28-welle3-2026-11-16/hunt-uid-docs-110/
evidence/r28-welle3-2026-11-16/hunt-uid-docs-110/fix-1.md
```

Die Akte steht auf origin/main unter ec8c38f4 (Commits: 5602c082 → 12a5886d → fc195b5f → ec8c38f4).

## END

END_DONE mission-110-mutation-loud.md — 0428-110: beide silent-pfade (corrupt config, XDG double-append) auf mutationspfaden reproduziert und gefixt: LoadConfigForMutation + Save-Routen pruefen die geladene config wie der read-pfad, werfen ErrConfigMissing/ErrConfigEmpty-familie loud, ghost-root wird konservativ abgelehnt (hint, kein dedupe), corrupter owner nie ueberschrieben; 094-assertions intact; regressionen unit + production entrance; build/vet/gofmt/affected tests gruen; Kandidat 1d01ea16c003adffa0dfd529282417956560e2a4 auf lane-0428-110-mutation-loud, PR #1682 READY gegen develop; Run 44060840263 exact-head TERMINAL SUCCESS (completed/success, von dieser Lane beobachtet).
