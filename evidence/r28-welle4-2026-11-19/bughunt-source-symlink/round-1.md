# Bug-Hunt H-V9 — source-model + symlink-containment gegen die restliche Ansicht (reine befundung)

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
- S1 grep: component-path-auflösung (EvalSymlinks/Clean/Rel/ResolvePath-artig) + Clean-before-Rel escape-check
- S2 unique-components: uniqueness-enforcement + doppelt-ref anderer version/quelle, entscheidender test
- S3 machine_coverage.go registrierung (:133) vs exportierter kommando-baum, laufender vergleich
- S4 mcp_workspace_mutation.go + app_workspace_wizard.go validierungs-helfer-vergleich
- befund-1.md schreiben + committen/pushen origin/main, census nachher + cleanliness
- END + akte (leslich, kein produkt-write)

## Status

END_DONE — alle vier szenen geprüft, kein bug-fund (alle VERHALTEN KORREKT), evidence published.

## Befunde

### SZENE S1 — Symlink-enthaltung gegen das source-model
VERHALTEN KORREKT. Jede component-path-auflösung läuft über development.ResolveWorkspace -> resolveContainedWorkspaceDirectory (internal/development/source.go:510-552). Fünf production-aufrufstellen auflösen das modell: cmd/baha/app_workspace.go:297, cmd/baha/app_workspace_wizard.go:88, cmd/baha/app_up_noop.go:192, cmd/baha/mcp_tools.go:117, cmd/baha/machine_http_executor_read.go:143. Keine aufrufstelle macht ein bares filepath.Clean+filepath.Rel ohne die shared containment-function. escape-check: source.go:526 lexical Rel-prüfung ('..'-prefix), source.go:529/533 filepath.EvalSymlinks auf root und candidate, source.go:540 zweite Rel-prüfung auf den kanonischen pfaden. Ein durchkommender '../' ist ausgeschlossen. zeuge: TestResolveWorkspaceRejectsSubpathSymlinkEscapes (internal/development/source_model_test.go:176) läuft für SourceLocal und SourceRepository, exit ok.

### SZENE S2 — 'unique components' vs registry/fussabdruck
VERHALTEN KORREKT. uniqueness wird erzwungen in SourceModel.Validate: internal/development/source.go:174-176 ('component %q is mapped more than once'), je application, je eigene quelle. zwei apps mit derselben component aber anderer version/quelle bleiben pro application scope; der footprint wird je component/<name>/source-identity.json keygeted (cmd/baha/app_up_noop.go:196-217), also application-lokal, kein globaler kollisionspfad. zeuge: TestSourceModelAllowsOptionalUniqueComponents (internal/development/source_model_test.go:21), exit ok.

### SZENE S3 — machine_coverage.go gegen die echte cli
VERHALTEN KORREKT. Die handschriftliche registrierung (:95 cliMachineOperations, :133 cliPresentationCommands, :189 cliExcludedCommands) trackt den exportierten kommando-baum; der test TestMachineDocumentationTracksRegistryAndCommandTree (cmd/baha/machine_documentation_test.go:48) schlägt bei jedem fehlenden eintrag an ('unclassified product command'). negativer beweis geführt: 'operator.identity' aus cliMachineOperations entfernt -> test schlägt fehl (machine_documentation_test.go:48); revert -> test grün. Jede leaf im baum ist in einer der drei maps klassifiziert.

### SZENE S4 — wizard- und mcp-pfade
VERHALTEN KORREKT. app_workspace_wizard.go:87-91 ruft model.Validate() und development.ResolveWorkspace(...) auf — dieselbe shared containment-function wie der source-model-zweig; ein escapender subpath schlägt hier fehl (line 89 return err). mcp_workspace_mutation.go registriert workspace.init/map über initializeApplicationWorkspace / mapApplicationWorkspace in cmd/baha/workspace_mutation.go:21 bzw :38; beide schreiben das quelle-modell über WriteSourceModel (Validate durch WriteSourceModel) bzw. LoadSourceModel und erlauben keine zweite eigenvalidierung — eine zweite eigene pfad-validierung pro pfad existiert nicht.

## REPO-RULE COMPLIANCE

- reine befundung, KEINE produkt-aenderung: eingehalten
- KEIN branch, KEIN PR, KEIN merge: eingehalten
- KEIN .github/scripts/coordinator-aenderung: eingehalten
- KEIN subagent (§4.8): gehalten (eigene session)
- keine vm/container/netzwerk/volume: eingehalten — rein quellcode + lokale unit-laeufe
- evidence-only: /tmp (kein Evidence-Tier im Produktzweig), nur eigene datei
- git -A vermieden: NUR meine datei git add
- /var/tmp/produktzweig vermieden: kein write nach /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan

## Cleanliness

vorher: keine container/netzwerke/volumes/state-verzeichnisse gestartet
nachher: keine container/netzwerke/volumes/state-verzeichnisse gestartet — /tmp/baseharbor-x158v und /tmp/baseharbor-plan-x158v nach ende entfernt

## Witnesses

- origin/main (planning) beim commit: e8e810e67844404179088642e0e6927d1130e37d
- origin/main (planning) nach push: e99aad94d8c6f73a4c9295d8b79df9e26021ff5a (commit e99aad94, round-1.md, nur meine datei)
- origin/develop (baseharbor, quelle): 97abbe1572a74170e3414448fe2dce843309c10a
- lokaler unit-lauf: go test ./internal/development/ und ./cmd/baha/ -run TestMachineDocumentationTracksRegistryAndCommandTree, TestHumanCommandIndexTracksExactCommandMetadata -> ok
- keine product-container, keine vm/netzwerk/volume gestartet
