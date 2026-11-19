# Bug-Hunt H-V9 — source-model + symlink- containment gegen die restliche Ansicht (reine befundung)

## Kontext
Schnitt: die frisch gemergte source-model- und symlink-flaeche des 0428-059 / #1706-merge auf develop.
Anlass: zwei aenderungen sind in den letzten zwei stunden auf develop gelandet, von keiner jagd beruehrt.
Quellen-SHA (develop): 97abbe1572a74170e3414448fe2dce843309c10a (gemessen `git ls-remote origin refs/heads/develop`).

Bezugscans:
- 15727ca88 = 0428-059 "extend app sources and unique components (source model slice)"
  cmd/baha/app_workspace_source_model.go (+tests), app_workspace.go, app_workspace_wizard.go,
  mcp_workspace_mutation.go, app_up_noop.go, app_core_requirement-umfeld,
  cmd/baha/machine_coverage.go +40 (handschriftliche Registrierung cliPresentationCommands, :133, lookup :88)
- 930df12a4 / merge 97abbe157 = #1706 "contain component paths across symlinks" (codex/0428-059-symlink-containment)

## PLAN

- planning-repo root attestieren (git -C .../baseharbor-plan rev-parse origin/main)
- census vorher (evidence-tree ls)
- S1: aufrufstellen der component-path-auflösung grep (EvalSymlinks / Clean / Rel / ResolvePath-artig)
  in cmd/baha/app_workspace_source_model.go, app_workspace.go, internal/application/* — prüfen, ob
  eine combination von Clean VOR Rel (oder umgekehrt) einen pfad wieder nach oben entkommen lässt;
  ein durchkommender '../' = fund mit datei:zeile.
- S2: 'unique components' vs registry/fussabdruck — wo wird uniqueness erzwungen, was passiert bei
  doppelter component-ref anderer version/quelle; entscheidender test (namensnennung + zeile);
  interpretation status-/desk-pfad.
- S3: cmd/baha/machine_coverage.go gegen die echte CLI — handchriftliche registrierung (:133) vs
  exportierter kommando-baum (root/kinder); human_documentation_test.go:101 und
  machine_documentation_test.go:57 gegen den generator; laufender vergleich; fehlt/kommando-im-baum.
- S4: mcp_workspace_mutation.go und app_workspace_wizard.go — benutzen beide denselben pfad-validierungs-
  helfer wie der source-model-zweig; zweite eigene validierung pro pfad = klassischer fund.
- befund-1.md schreiben (jeder fund: datei:zeile ODER testname+ausgang; SZENE je 'VERHALTEN KORREKT'/'BEFUND')
- befund committen + pushen, ls-remote origin/main witness
- census nachher + cleanliness-zeile

## Status

IN ARBEIT — alle vier szenen werden an diesem run bearbeitet.

## Befunde

### SZENE S1 — Symlink-enthaltung gegen das source-model

- (ausstehend — grep + interpretatioon folgt)

### SZENE S2 — 'unique components' vs registry/fussabdruck

- (ausstehend — test + interpretation folgt)

### SZENE S3 — machine_coverage.go gegen die echte CLI

- (ausstehend — vergleichslauf folgt)

### SZENE S4 — wizard- und mcp-pfade

- (ausstehend — validierungs-helfer-vergleich folgt)

## REPO-RULE COMPLIANCE

- reine befundung, KEINE produkt-aenderung: eingehalten
- KEIN branch, KEIN PR, KEIN merge: eingehalten
- KEIN .github/scripts/coordinator-aenderung: eingehalten
- KEIN subagent (§4.8): gehalten (eigene session)
- keine vm/container/netzwerk/volume: eingehalten — rein quellcode + lokale unit-laeufe
- evidence-only: /tmp/baseharbor-plan-x158v (kein Evidence-Tier im Produktzweig), nur eigene datei
- git -A vermieden: NUR meine datei git add
- /var/tmp/produktzweig vermieden: kein write nach /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan

## Cleanliness

vorher: keine container/netzwerke/volumes/state-verzeichnisse gestartet
nachher: keine container/netzwerke/volumes/state-verzeichnisse gestartet
