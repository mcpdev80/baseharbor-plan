# BUG-HUNT 913 — Befund: Befehls- und Doku-Drift der v0.4.28 Releasedesse

Lane: hunt-cmddrift. Mission: /var/tmp/missions/mission-hunt-cmddrift.md.
Datum: 2026-11-17. Reine Befundung, keine Produktänderungen, kein .github/**.

## PLAN

- Objekt: baseharbor develop 62eaea2c8c5b29f73db03ae9b3e7efaf772e4458 (gemergte v0.4.28 Releasedesse)
- Worktree + binary build von exakt diesem SHA
- Schnitt (a): Cobra-Kommando-Baum (help-getrieben) gegen docs/cli/command-index.md (EN und DE)
- Schnitt (b): --help-Ausgaben und Doku-Beispiele trocken gegen die reale binary geprüft
- Schnitt (c): Flag-Namen-Drift EN vs DE Doku
- Befund-Datei in baseharbor-plan, push auf origin/main, Sauberkeit, END

## Basis-Attestation

- Plan-Repo-Verifikation (wrong-zone check): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
- Produkt-Basis: `git ls-remote origin refs/heads/develop` → `62eaea2c8c5b29f73db03ae9b3e7efaf772e4458 refs/heads/develop`; Worktree/Build exakt auf diesem SHA (detached).
- Kein Produkt-Branch, kein PR: Hunt ist reine Befundung; das einzige Artifact ist diese Datei in baseharbor-plan.
- Beweismittel-Logik: alle CLI-Zeugen stammen aus `./baha …` (built from 62eaea2c8) in leeren/bekannten Testverzeichnissen; dieses Host-Verzeichnis (coordinator/codeman server) hat keinen container runtime orchestration Zugang, daher brechen runtime-pflichtige Beispiele dort mit "container runtime orchestration not found" ab — das ist Umgebung, kein Produktbefund, und wird nicht als Befund gewertet.

## Schnitt (a): Cobra-Baum vs generierte Kommando-Referenz

Methode: Vollständiger Help-Walk über `baha … --help` (Usage-Klammern + Commands-Sektionen, Depth ≤ 3), verglichen mit `docs/cli/command-index.md` (154 Einträge), `docs/de/cli/command-index.md` und `baha agent describe -o json` (`cli_coverage`, 155 Einträge).

- Index ↔ Coverage Deckung: identisch (nur Wurzel `baha` in coverage, korrekt). EN-Index == DE-Index in Befehlspfaden, Kurzbeschreibung und Syntax-Spalten (0 Unterschiede).
- Befund A1 (gering, Dokumentation): Die 13 Kontext-Shorthands auf Root-Ebene (`baha new|init|list|inspect|backup|restore|up|down|plan|logs|status|doctor|update`) erscheinen NICHT in der Gruppen-Liste von `baha --help`, solange kein `baseharbor.yaml` im Verzeichnisbaum gefunden wird; erst in einer Application-Repository wechselt die Hilfe auf die "Application"-Gruppe und zeigt sie. `docs/cli/core.md:31` sagt das ("Inside a repository…"), aber `docs/cli/command-index.md` und `global-options`-Einführung kennzeichnen diese 13 Einträge nicht als repository-abhängig sichtbar. Ein User außerhalb eines Repos sieht 13 dokumentierte Befehle nicht im --help. Repro: leeres Verzeichnis, `baha --help | grep -E 'init|up|down|plan'` → nur "Get started"-Einträge.
- Befund A2 (neutralisiert, Hinweis): Die Help-Generierung rendert für Alias-Pfade (`baha workspace …`) die Usage-Zeile des kanonischen Baums (`baha app workspace …`), weil `normalizeWorkspaceHelp` nur `command.Usage` ersetzt, nicht `child.Usage` (cmd/baha/human_workspace.go:20-24). Praktische Folge: Fehlermeldungen sagen "baha app workspace does not accept…", obwohl `baha workspace` geroutet wurde. Kein Doku-Widerspruch, aber --help-vs-Doku-Inkongruenz im Kopierfluss. Datei: cmd/baha/human_workspace.go:20-24.
- Kein fehlender und kein veralterter Eintrag im Index gegen den realen Baum: alle 154 Index-Einträge lösen gegen die binary auf korrekte Kommandos auf; alle realen, nicht-versteckten Pfade (inkl. `baha app versions`, `baha config organization check/set/show/update`, `baha dev credentials|domain|hosts|cleanup`) sind im Index.
- Verstecktes Kommando `baha prompt` (cmd/baha/prompt.go:264-266, Hidden:true) ist in docs/cli/shell-ux.md:25,41 und docs/de/cli/shell-ux.md:3,31 als nutzbar dokumentiert (`baha prompt`), fehlt aber in command-index UND machine coverage — konsistent mit Hidden-Semantik, aber für Kopierbarkeit ein Dokumentations-Gap: es existiert kein Index-/Coverage-Eintrag, der versteckte-but-documented Befehle führt. Niederwertig.

## Schnitt (b): --help vs Doku-Beispiele, trockener Durchlauf gegen die reale binary

Methode: alle 396 eindeutigen `baha …`-Vorkommen in docs/cli + docs/de/cli extrahiert, jedes Kommando-Pfad gegen `<cmd> --help` aufgelöst (0 unbekannte Pfade), dann Flags/Ausgangscodes für Root-Beispiele, EN+DE-Beispielblöcke und DE-spezifische Pfad-Zitierende einzeln ausgeführt.

- Befund B1 (Doku-Fehler, EN+DE identisch): Syntax-Eintrag `baha down [options]` (docs/cli/command-index.md:88, docs/de/cli/command-index.md:88) suggeriert Optionen; die binary lehnt jede ab: `baha down --yes` → rc=2 "Error: down does not accept --yes … --yes does not provide them." Repro: `baha down --yes </dev/null; echo $?` → 2 mit usage-Fehler. Konsistenzproblem zwischen Syntax-Spalte und tatsächlichem Flag-Verhalten; korrekt wäre `baha down` ohne [options] (mit Hinweis auf die Pflichtbestätigungen interaktiv).
- Befund B2 (Doku-Lücke, EN+DE): `baha up -e dev` wird in docs/cli/core.md:120 und docs/de/cli/core.md:71 ohne --yes gezeigt; in der Praxis ist der erste `up` eines Repositorys ein Init-Schritt, der ohne `--yes` (defaults) oder explizite Auswahl abbricht ("Next: Run 'baha up --yes' … or run 'baha app init' interactively"). Repro (leeres Verzeichnis): rc=2. Die Doku-Behauptung "startet Umgebung dev" ist so nicht kopierbar lauffähig.
- Befund B3 (Doku-Lücke): `baha plan -e dev` (docs/cli/core.md:120, docs/de/cli/core.md:71) wird als Umgebungs-Wähler gezeigt; real akzeptiert `baha plan` nur `[NAME] [-o json|--output json]` (Usage aus --help), die `-e/--environment`-Form wird als Application-NAME interpretiert: `baha plan dev` → rc=2 "application \"dev\" has no registered deployment on target …". Repro wie gezeigt. Entweder Usage-Doku korrigieren oder -e durchreichen.
- Befund B4 (Doku-Lücke, gering): `baha init my-app` in docs/cli/core.md ("Initialize … including required Core setup", Tutorial-Pfad) endet non-interaktiv rc=2 "deterministic app init requires an explicit capability or workload selection"; `baha init NAME` ist in keiner Usage-Syntax aufgeführt (command-index.md:68 listet nur --agents/--quick/--input/--yes). Positional-NAME wird toleriert, aber ohne Capability-Auswahl nie lauffähig. Repro: `baha init my-app </dev/null; echo $?` → 2.
- Alle übrigen trockenen Beispiele (`baha up --yes`, `baha init --quick`, `baha destroy --yes`, `baha new application NAME --stack … [--http --sql --cache]`, `baha backup`, `baha restore`, `baha logs`, `baha open --print`, `baha tui --json`, `baha version`, `baha whoami`, `baha login`, `baha completion bash`, `baha agent describe`, `baha mcp serve --help`, `baha config organization show|check`, `baha target list|policy show`, `baha node list|status`, `baha provider list`, `baha stack list|show go`, `baha app *`-Familie inkl. `app init`, `app plan`, `app preflight`, `app status`, `app env --format json`, `app secure-profile export`, `trust status`, `dev hosts`, `connections`, `connect`, `user offboard`, `workspace map/show/init/resolve/status/update`) lösen und parsen fehlerfrei gegen die binary. Die 2 "unknown-path"-Treffer aus 396 Doku-Vorkommen (`baha promote`, `baha app secure-profile import`) sind ausdrückliche Negativ-Nennungen ("There is no … command", docs/how-to/local-remote-team-workflow.md:76,91) — kein Befund.

## Schnitt (c): Flag-Namen-Drift DE/EN-Doku

- Mengenprüfung: alle 158 eindeutigen `--flag`-Vorkommen in docs/cli/** sind identisch in docs/de/cli/** (0 EN-only, 0 DE-only); Kurzbeschreibung- und Syntax-Spalten des command-index sind zeichengleich zwischen EN und DE (0 Unterschiede, DE-Header erklärt das selbst).
- Befund C1 (DE-only Behauptung, Kopier-Drift): docs/de/cli/core.md:52,54 zeigt `baha up --control-plane-only --yes` und `baha up --control-plane-only --ha --yes` in einem expliziten DE-Textblock ("Control-Plane-Topologie", docs/de/cli/core.md:44-46) und behauptet in docs/de/cli/core.md:51, ohne Repository sei das "der explizite Core-only-Pfad"; der identische EN-Block (docs/cli/core.md:44-56) trägt dieselben Beispiele. Die Flag-Namen stimmen mit der binary überein — kein Namens-Drift, aber: KEIN EN/DE-Doku-Dokument zeigt `baha up` OHNE Repository als gültig für Standard-Application-Ablauf, während `baha up --control-plane-only` nur in DE-Tutorial homelab.md:18 (EN homelab.md:18 identisch) als Core-only-Pfad benannt wird. Für den Hunt-Schnitt "flag-namen-drift de/en" gilt: kein Befund — Flag-Namen sind in DE und EN deckungsgleich.

## Zusammenfassung der Befunde

- A1 Root-Hilfe zeigt 13 dokumentierte Shorthand-Befehle außerhalb eines Repositorys nicht (Doku-Kennzeichnung fehlt) — docs/cli/command-index.md, docs/cli/core.md:31
- A2 Alias-Hilfe rendert kanonische Usage-Zeile (`baha workspace … --help` zeigt `baha app workspace …`) — cmd/baha/human_workspace.go:20-24 (Hinweis, kein Doku-Widerspruch)
- B1 `baha down [options]` Syntax-Eintrag vs. "accepts keine Optionen" — docs/cli/command-index.md:88 / docs/de/cli/command-index.md:88
- B2 `baha up -e dev` Beispiel ohne Init-Vorbedingung kopierbar nicht lauffähig — docs/cli/core.md:120 / docs/de/cli/core.md:71
- B3 `baha plan -e dev` Beispiel: -e wird als Application-NAME gelesen — docs/cli/core.md:120 / docs/de/cli/core.md:71
- B4 `baha init <NAME>`-Beispiel endet non-interaktiv in Pflichtabbruch; Positional nicht in Usage — docs/cli/core.md (init-Abschnitt)
- C-Befunde: keine (Flag-Namen DE==EN, 158/158 deckungsgleich)
- Index-vs-Baum und Index-vs-Coverage: konsistent, keine fehlenden/veralterten Einträge
- Verstecktes `baha prompt` ist in shell-ux dokumentiert, aber nirgends im index/coverage (niederwertig)

Jeder Befund braucht eine Bug-Karte (Fund→Karte-Pflicht); die Kartennummern setzt der Coordinator, diese Akte bleibt der Evidence-Ort.

## repo-rule compliance

- Reine Befundung: keine Produkt-Commits, kein PR, keine .github/**-Änderung, keine gehosteten Läufe ausgelöst (nur gelesene ls-remote-Zeugen und lokale dry-run-Aufrufe der binary).
- Sprache: Produkt-/Funktionsaussagen deutsch, Fachwörter (container, target, flag, help, compose, worktree) englisch gelassen.
- Evidence nur in baseharbor-plan (evidence/r28-welle4-2026-11-17/hunt-cmddrift/), keine Checkboxes in dieser Datei.

## Zeugen

- `git ls-remote origin refs/heads/develop` → 62eaea2c8c5b29f73db03ae9b3e7efaf772e4458 (baseharbor)
- `baha version` → "baha dev (commit none, built unknown)"; Binary gebaut mit go1.26.8 aus dem SHA-Worktree `git rev-parse HEAD` → 62eaea2c8c5b29f73db03ae9b3e7efaf772e4458
- rc-Zeugen: down --yes rc=2; init my-app rc=2; plan -e dev rc=2; up -e dev rc=2 (leeres Verzeichnis); workspace directory rc=2 usage-Fehler "baha app workspace does not accept positional arguments"
- Help-Walk: 154 Index-Pfade, alle auflösbar; 0 unknown command paths aus 396 Doku-Vorkommen (2 davon ausdrückliche Negativ-Nennungen)

## cleanliness

- Keine containers/netzwerke/volumes/compose projects von dieser Lane gestartet; `docker ps`/`docker compose ls` zeigen nur ambient core/ Projekte anderer Lanes (unangetastet).
- Lane-Arbeitsverzeichnis /home/marcel/dev/baseharbor-ecosystem/work/hunt-cmddrift-wt (worktree+binary+caches) wird nach dieser Akte entfernt; temporäre Testverzeichnisse unter /tmp/opencode/chkdrift und /tmp/opencode/empty-repo ebenfalls.
- Hinweis an Coordinator: /tmp ist zu 80% voll (tmpfs 13G/11G), das Root-Dateisystem zu 97%; der erste Worktree-Ansatz unter /tmp/opencode scheiterte an "disk quota exceeded" (cgo). Kein Lane-eigenes Aufräumproblem, aber Betriebsbefund.

END hunt-cmddrift DONE
