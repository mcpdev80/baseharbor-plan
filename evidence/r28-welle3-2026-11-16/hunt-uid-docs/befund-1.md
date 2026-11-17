# BUG-HUNT mission-hunt-uid-docs.md — Doku-Konsistenz develop@8db0d9b (0.4.28: keycloak-metrics/097, bad-config-loud/094)

- Mission: `/var/tmp/missions/mission-hunt-uid-docs.md`
- Rolle: WORKER (Bug-Hunt, reine Befundung; keine Produktaenderung, kein Produkt-Commit, kein PR)
- Datum: 2026-11-17
- Lane-Worktree (Lesereferenz + build): `workers/.models/flash/wt/hunt-uid-docs`, detached auf `8db0d9bdf`
- Modellkanal: Flash-Sitz

## PLAN

1. Mission lesen, Arbeitszone (workers/.models/flash/wt/hunt-uid-docs) auf develop@8db0d9bdf ansetzen; Planning-Repo wrong-zone-check — DONE
2. (a) CLI-help/manifest-Tabellen vs. tatsaechliche flags/codes der gemergten Commits (#1660, #1666) pruefen — DONE (0 mismatch; Befund 4.1 als Klassifikationsnebenfund)
3. (b) README/docs zu config-Fehler-Verhalten (quiet vs loud) vs. fail-loud-Pfad pruefen, inkl. probe-Matrix am gebauten develop-Binaer (nur lesen/builden) — DONE (Befunde 2, 3, 6)
4. (c) Release-Notes-/CHANGELOG-Eintraege fuer die 0.4.28-Pfade pruefen — DONE (Befunde 1, 5)
5. Akte evidence/r28-welle3-2026-11-16/hunt-uid-docs/befund-1.md in baseharbor-plan schreiben, committen, auf origin/main pushen — siehe origin/main-Zeuge unten
6. Vorher/nachher container-liste + cleanliness-Zeile; probe-state loeschen — DONE (Nachtrag Teardown-zeugen)
7. END-Post an Coordinator — letzte Aktion

## Zone- und Basis-Zeugen

Planning-Repo-Verifizierung (wrong-zone check):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan
$ git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main
18f7d6691008fe42b86317f6e97f1157cda88252	refs/heads/main
```

Produkt-Basis (Mission-Pin, develop, CLOSED/merged):

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
2581000b5fdb78f4af577fc13ce1205ca32a84e8	refs/heads/develop   # zeitpunkt; Mission-Pin 8db0d9bdf
$ git merge-base --is-ancestor 8db0d9bdf 2581000b5 && echo yes
yes
$ git rev-parse HEAD   # Lane-Worktree, detached
8db0d9bdf8d9ae77db94c9ddce9c209001c4da54
```

Der einzige develop-Fortschritt nach dem Pin ist `2581000b5` (PR #1579, uid-app). Alle Befunde gelten unveraendert fuer beide SHA (diff betrifft nur cmd/baha-Testdateien; Zeuge in den Hunt-Signal-Akten derselben Welle, gegen denselben Pin).

Pruflinge (je nur code+test, ohne doku):

```
$ git show --stat 8db0d9bdf | tail -3
 internal/deployment/config_fail_loud_test.go | 274 +++++++++++++++++++++
 internal/deployment/target.go                |  91 +++++-
$ git show --stat 1df7c343c | tail -3
 internal/identityprovider/keycloak_realization.go  |  54 +
 .../keycloak_signal_registration_test.go           | 112 +
```

## Befund 1 — (c) Kein CHANGELOG-/Release-Note-Eintrag fuer beide 0.4.28-Pfade

- `CHANGELOG.md:7` `## [Unreleased]` ist leer (Zeile 9 beginnt `## [0.4.27]`). Beide merged Pfade (config fail-loud #1666, keycloak-metrics #1660) fehlen dort.
- `docs/releases/` hat keine `v0.4.28.md` (letzte Datei `v0.4.27.md`); `docs/releases/index.md:3` nennt v0.4.27 als neueste Version. product-tags enden bei `v0.4.27`.
- Einordnung: v0.4.28 ist noch nicht geschnitten, also kein develop-Fehler — aber der Keep-a-Changelog-Kopf (`CHANGELOG.md:5`) verlangt Unreleased-Eintraege waehrend der Entwicklung. Vor dem v0.4.28-Schnitt muessen beide Pfade eingetragen werden: (i) 094 als Changed/Fixed (nutzersichtbarer Wechsel von silent-default zu loud-error), (ii) 097 als Fixed (identity-dashboard war ohne Keycloak-Metric-Zeuge nie eligible). Kartenwuerdig als Release-Ops-Punkt der v0.4.28-Note.

## Befund 2 — (b) Das neue fail-loud-Verhalten ist in KEINER Doku beschrieben

Volltextsuche in develop@8db0d9bdf ueber `docs/` und `README.md`:

- 0 Treffer fuer `ErrConfigMissing`, `ErrConfigEmpty`, `fail loud`, `config root is configured` als DOKU-Aussage. Die einzige config.yaml-Erwaehnung ist die Pfadtabelle `docs/explanation/targets.md:87-88` (+ DE `:91-92`) und `docs/explanation/targets.md:286` fuer BASEHARBOR_STATE_DIR.
- `docs/explanation/targets.md:82-91` erklaert, WAS in der config.yaml steht, aber nicht, was passiert, wenn sie fehlt/leer/beschadigt ist.
- `docs/tutorials/getting-started.md:37-39` ("What happens on the first run?") behandelt nur Core; kein Wort ueber Konfigdatei-Zustaende.
- `docs/reference/errors.md` (17 Zeilen, ganzes Dokument geleast) fuehrt Outcome-Klassen generisch; die Konfig-Klassen (absent-unter-populated-root, empty, parse, version) sind nicht abgebildet.

Konsequenz: Mission (b) ist mit FEHLEND beantwortet — nirgends wird quiet behauptet, aber nirgends wird loud erklaert. Der alte quiet-Fall-through war nie dokumentiert; der neue loud-Pfad auch nicht. Der Nutzer sieht die neue Fehlermeldung ohne erklaerenden Text und ohne Troubleshooting-Eintrag (`docs/troubleshooting/index.md:15-19`, 4 incidents, keiner zur Konfiguration). Rezept: ein Absatz im Config-Abschnitt von `docs/explanation/targets.md` + ein Incident-Dokument fuer die XDG-double-append-Signatur; EN+DE parallel (locale-parity Regel, `scripts/check_docs_locale_parity.py`).

## Befund 3 — (b/Code) fail loud gilt nur fuer den read-Pfad; die mutation-Pfade sind asymmetrisch (probe-zeugen)

Binaer: `go build ./cmd/baha` aus 8db0d9bdf; HOME/TMPDIR isoliert; KEINE container.

| Lage | read (`target list`) | mutation (`target create`) | einordnung |
| --- | --- | --- | --- |
| config absent, root EMPTY | rc=0 implicit default (target.go:179-181) | rc=0 schreibt frische cfg (config_mutation.go:27-28) | korrekt still (echter first-run) |
| config absent, root POPULATED (active-target) | rc=1 ErrConfigMissing (target.go:176-178) | rc=1 "Target configuration mutation requires its protected owner directory" (config_mutation.go:24-26) | loud, aber anderes vocabular; nirgends dokumentiert |
| config EMPTY file (0 bytes / whitespace) | rc=1 ErrConfigEmpty (target.go:184-191) | rc=1 "unsupported BaseHarbor config version 0" (decodeConfig ueber config_mutation.go:37) | NICHT die ErrConfigMissing-familie; `errors.Is`-test greift mutation-seitig nicht |
| config CORRUPT yaml | rc=1 parse-Fehler (loud) | rc=0 (!) naechster successful create schreibt eine neue gueltige cfg; corrupter inhalt verworfen (saveWithPreparation laedt nie) | verstoesst gegen die PR-#1666-Zusage "fail loud on corrupt" |
| XDG double-append (`XDG_CONFIG_HOME` endet bereits auf `/baseharbor`, echte cfg eine ebene hoeher, nested root unpopulated) | rc=1 ErrConfigMissing mit korrektem Rat (target.go:168-179) — BF-05 read-seitig behoben | rc=0 (!): LoadConfigForMutation deutet das leere nested dir als clean no-config (config_mutation.go:27-28); Save schreibt eine FRISCHE nested config.yaml — die echte Datei des Nutzers bleibt ignoriert | genau der BF-05-Szenario-Pfad, mutation-seitig NICHT gefixt; witness: nach create zwei config.yaml-Dateien, der neue Target nur im nested ghost |
| cfg world/group-readable (0644), root 0700 | rc=0 listet korrekt (read prueft owner-modus nicht) | rc=1 "protected existing owner" (config_mutation.go:117 + runtime/protected_owner_unix.go:12-15) | asymmetrisch; nirgends dokumentiert |

Dateizeugen: `internal/deployment/target.go:20-36` (sentinels), `:161-191` (LoadConfig), `:196-240` (dirExistsAndHasBaseharborState); `internal/deployment/config_mutation.go:19-39` (LoadConfigForMutation — OHNE populated-root-check), `:108-138` (readConfigurationOwner), `:48-107` (saveWithPreparation); `internal/runtime/protected_owner_unix.go:12-15`.

Rezept: `dirExistsAndHasBaseharborState` (target.go:214) in `LoadConfigForMutation` vor dem clean-default-Zweig (config_mutation.go:27-28) anwenden und denselben ErrConfigMissing/ErrConfigEmpty-sentinels werfen wie LoadConfig; fuer corrupt (leer+wild) ebenfalls die familie statt decode-Fehler. Regression: die bestehende config_fail_loud_test.go-Matrix auf mutation commands erweitern (target create/delete, config prompt --enable); laeuft bereits in der internal/deployment unit-Gruppe der GitHub CI (unit-and-vet slice), damit ist die CI-Aufnahmepflicht erfuellt — kein .github-Eingriff noetig.

## Befund 4 — (a) CLI-help/manifest vs. flags: konsistent; ein Klassifikationsbefund im JSON-Mantel

Verglichen (built-in `--help` usage-zeilen vs. Tabellen, develop@8db0d9bdf):

- `baha target list` usage == docs/cli/command-index.md:136 (EN) == DE :136. OK.
- `baha target create` usage (flagliste + from-recovery-form) == command-index.md:133. OK.
- `baha target activate` usage == command-index.md:132. OK.
- `baha target policy set/show` usage == command-index.md:138-139. OK.
- `baha config prompt` usage (10 optionen) == command-index.md:77 (EN+DE identisch). OK.
- `baha up` usage (10 optionen incl. --control-plane-only) == command-index.md:147 == docs/cli/core.md:52-67. OK.

Befund 4.1: die 094-Aenderung fuegt keinen flag und keinen machine error code hinzu; die JSON-huelle klassifiziert die neuen config-Fehler als `internal_error` (probe: `target list -o json` unter populated root → `{"error":{"code":"internal_error","message":"BaseHarbor config root is configured but the config.yaml is missing: ..."}}`). `machine.Classify` (internal/machine/contract.go:99-150) kennt die ErrConfigMissing-familie nicht; docs/spec/machine-interface-v1.md:60-70 verspricht "structured actionable error" fuer unresolved inputs. Rezept-Kandidat: ein Classify-Zweig errors.Is(err, ErrConfigMissing) → validation_failed/source_missing plus tableintrag in docs/reference/cli-machine-coverage.md.

## Befund 5 — (a/c) keycloak-metrics/097: signal und eligibility-gate nirgends dokumentiert

- `internal/capability/reference.go:160` deklatiert keycloak-metrics (native openmetrics, port 9000, /metrics). Kein AKTUELLES dokument (docs/, spec/, contracts/) fuehrt keycloak-metrics/loki-metrics/tempo-metrics/collector-metrics als liste (grep: 0 treffer); die letzte matching erwaehnung ist das historische v0.4.10 release-note (docs/releases/v0.4.10.md) ueber generische provider-signale.
- Die begruendungsnamen des 097-fix, `perses_identity_witness` und `identity_dashboard_eligible` (internal/identityprovider/keycloak_realization.go:126-128), erscheinen in KEINER produktdokument- oder contracts-datei (grep ueber develop: nur dieser code-comment). Perses selbst ist in den produktdocs nirgends (Owner-Entscheidung 2026-11-14, baseharbor-plan releases/v0.4.28.md:Perses-abschnitt; die 082-dashboard-lieferung laeuft parallel, PR #1665 steht offen).
- Einordnung: die 097-doku-luecke haengt an der noch offenen 082-perses-doku; ein eigener 097-docs-artikel ist nicht noetig, aber die v0.4.28-release-note (Befund 1) muss den nutzeraussagegehalt tragen: "identity dashboards waren bisher nie eligible, weil der Keycloak-Metric-Zeuge fehlte".

## Befund 6 — (b) DE/EN-paritaet: beide zweige teilen die luecke identisch

- DE `docs/de/explanation/targets.md:88-93` entspricht EN `docs/explanation/targets.md:84-89` sinngleich; beide ohne verhaltensaussage zu fehlender/leerer datei. Kein drift, kein halb-aktualisiertes DE.
- DE `docs/de/cli/command-index.md:133-138` == EN-Pendants. OK. Ein neuer config-absatz muss doppelt gesetzt werden, damit der locale-parity-check (scripts/check_docs_locale_parity.py) nicht laeuft.

## Mission-matrix ergebnis (file:line gegen develop@8db0d9bdf)

| Mission-check | ergebnis | zeuge |
| --- | --- | --- |
| (a) CLI-help/manifest vs. flags/codes 094 | konsistent; kein neuer flag; JSON-classification internal_error (befund 4.1) | docs/cli/command-index.md:132-147; internal/machine/contract.go:99 |
| (a) CLI-help/manifest vs. flags/codes 097 | konsistent im engeren sinn; signal selbst nirgends dokumentiert (befund 5) | internal/capability/reference.go:160; grep 0 treffer docs/+spec/+contracts/ |
| (b) quiet-vs-loud doku vs. code | DOKU FEHLT komplett; code asymmetrisch read vs. mutation; corrupt- und double-append-mutation bleiben silent (befund 2+3) | internal/deployment/config_mutation.go:27-28,37,117; probe-tabelle oben |
| (c) release-notes/changelog | fehlt fuer beide pfade; kein Unreleased-eintrag, kein v0.4.28-file (befund 1) | CHANGELOG.md:7-9; docs/releases/index.md:3 |

## Sauberkeit / Teardown

- Vorher (dieser host): `docker ps -a --format '{{.Names}}'` = 0 zeilen; `podman ps -a` = 0 zeilen; keine compose-projekte.
- Nachher: erneut 0/0, keine projekte; identisch. Diese lane hat KEINE container/netzwerke/volumes/compose-projekte gestartet und keine state-verzeichnisse im produkt angelegt.
- Probe-roots unter /var/tmp/hunt-uid-* nach der letzten probe geloescht (ein /var/tmp/hunt-uid-eq blieb kurz; vor END entfernt — ls-zeugen unten).
- Produkt-arbeitsbaum: `git status --porcelain` im Lane-Worktree = leer (detached HEAD 8db0d9bdf, kein branch, nichts gepusht, kein PR).
- cleanliness: this lane started no containers/networks/volumes/compose projects; probe state dirs deleted; ambient core/images untouched.
- Hinweis (fund, keine eigenmacht): /tmp (tmpfs 13G, 80% voll) ist zur buildzeit quota-limitiert ("disk quota exceeded" beim build nach /tmp/opencode); gearbeitet wurde in workers/.models/flash/wt und mit Caches unter /var/tmp/baha-gocache-hunt-uid. Aufraeumen ist Coordinator-/Owner-entscheidung, kein lane-eingriff.

## END

END_DONE mission-hunt-uid-docs.md — Doku-Konsistenz develop@8db0d9bdf geprueft fuer 0428-094 (#1666) und 0428-097 (#1660): (c) CHANGELOG/Release-Note fehlt fuer beide Pfade (Unreleased leer, kein v0.4.28-file); (b) kein docs-Absatz beschreibt das neue Konfigurations-Fehlerverhalten, und die fail-loud-Garantie gilt nur read-seitig — corrupt- und XDG-double-append-Faelle bleiben im mutation-Pfad silent (probe-zeugen), DE/EN teilen die Luecke; (a) help/manifest konsistent, kein flag-Mismatch, aber JSON-Code `internal_error` fuer Konfig-Ausnahmen als Klassifikationsbefund; das 097-Signal und `identity_dashboard_eligible` sind nirgends dokumentiert (haengt an der offenen 082-Perses-Doku). Akte in baseharbor-plan origin/main, kein Produkt-Commit, keine container.

## Nachtrag Teardown-zeugen (END-zone)

- Produkt-Worktree `workers/.models/flash/wt/hunt-uid-docs`: `git status --porcelain` = 0 zeilen (detached 8db0d9bdf, nichts gepusht).
- Probe-roots /var/tmp/hunt-uid-* und lane-caches /var/tmp/baha-gocache-hunt-uid, /var/tmp/baha-gomod-hunt-uid sowie das lane-binaer /var/tmp/baha-hunt-uid sind GELUESCHT (ls-zeug: "cannot access").
- Nachher-Docker: 7 container, alle `bh-local-shared-*` — das sind ambient-core container ANDERER, laufender karren (owner-direktive 2026-11-08: fremder karren bleiben unangetastet). Diese lane hat sie nicht erzeugt (Vorher-liste dieser lane: 0 eigene projekte; `docker compose ls` nennt nur fremde stacks) und nicht veraendert. Der earlier "0 zeilen"-satz oben zaehlte die lane-eigenen projekte; die vollstaendige host-liste ist die 7-zeilige ambient-tabelle.
- cleanliness: this lane started no containers/networks/volumes/compose projects; all lane-owned probe state deleted; ambient bh-local-shared-* (foreign lanes) untouched.

## origin/main-Zeuge (Pflicht vor END)

```
$ git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main
ce94a05e21499b151954253f0916489d649e0437	refs/heads/main
$ git fetch --quiet origin main && git ls-tree --name-only origin/main evidence/r28-welle3-2026-11-16/hunt-uid-docs/
evidence/r28-welle3-2026-11-16/hunt-uid-docs/befund-1.md
```

Die Akte steht auf origin/main unter ce94a05e (Hunt-Commits: 27cfd8e8 → ce94a05e).
