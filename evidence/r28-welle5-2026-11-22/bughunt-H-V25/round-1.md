# H-V25 bug-hunt app-footprint 3-surface consistency - round-1 akte

Sitz `w21-pr1702-0428-bughunt-hv25`. Bug-hunt H-V25, owner-order, REINE BEFUNDUNG, develop-stand, KEINE aenderung/commit/push/subagent.

Auftrag: app-footprint 3-flaechen consistency desk. Fuer denselben footprint vergleichen die menschliche, die -o json und die MCP-ausgabe feld-fuer-feld. Nach dem 245-fix (Unused) pruefen ob WEITERE felder divergieren (z.B. counts vs ids, status-namen, fehlende felder).

GRENZE: cmd/baha footprint show menschen-branch + json + mcp-tool; NUR lesen, kein edit (245 ist fertig, 237/231 nicht astasten).

## PLAN

- plan in board-file + ## PLAN in akte
- develop fetchen (refs/heads/develop), HEAD-sha in akte; NUR lesen (git show/grep/rg, ggf. read-only durchgang)
- surface A human: cmd/baha app footprint show presenter - positiver+negativer fall, datei:zeile
- surface B json: app footprint show -o json - positiver+negativer fall, datei:zeile
- surface C mcp: baseharbor.app.footprint.show tool output - positiver+negativer fall, datei:zeile
- feld-fuer-feld vergleich human vs json vs mcp fuer denselben footprint; divergenzen pruefen (counts vs ids, status-namen, fehlende felder); klassifizieren ECHTER DEFECT / doku-luecke / kein-befund
- kartenwuerdige funde mit mindest-rezept in akte (Owner giesst karte, Fund->Karte-pflicht bei ihm); KEIN edit/commit/push/subagent; cleanliness; 9142ab1f posten
- END: develop-head, fundbilanz, je fund datei:zeile, cleanliness

## Befunde

develop HEAD: 62784eff7befadfaa8a08fc21eaffbd4e3cc8962 (git ls-remote origin refs/heads/develop)

Desk: app-footprint 3-flaechen consistency, feld-fuer-feld fuer denselben Footprint.
Surface A = human presenter (cmd/baha/app_footprint_presenter.go:22 renderAppFootprint)
Surface B = JSON (cmd/baha/app_footprint_show.go:55-72 appFootprintShowContext JSON=true -> json.Marshal(view.Footprint))
Surface C = MCP (cmd/baha/app_registration_921.go:70 registerMCPFootprintShowTool -> appMachineFootprintJSON -> appFootprintShowContext(JSON=true) -> json.Marshal; MCP unmarshals into application.Footprint)

### Befund B1: JSON (B) und MCP (C) sind byte-identisch fuer denselben Footprint — KEIN DEFECT, positive Befund
- appMachineFootprintJSON (cmd/baha/app_machine_adapters.go:242-248) ruft appFootprintShowContext mit JSON=true -> bytes.Clone(json.Marshal(view.Footprint))
- registerMCPFootprintShowTool (cmd/baha/app_registration_921.go:85-96) ruft appMachineFootprintJSON und unmarshaled in application.Footprint, gibt struct zurueck -> identische Felder, identische Werte
- Rundtrip marshal->unmarshal verliert keine Felder (Struktur ist stable; ProviderScope/ProviderOwnership sind string basierte Typen, registry.go:18/26)
- Reproduzierbar (positiv): resolve footprint -> JSON bytes == MCP struct serialisiert; (negativ): keine divergenz zwischen B und C
- Klassifizierung: KEIN DEFECT. Nach 245-fix (Unused) ist die machine-seitige oberflaeche konsistent.

### Befund B2: Human presenter (A) ist BY-DESIGN ein kuratierte SUBSET der Footprint-Struktur — KEIN DEFECT, positive Befund
- Footprint-Struktur (internal/application/footprint.go:115-124): Version, Target, ApplicationID, Requirements, Existing, Additional, Unused, Core, Complete
- renderAppFootprint (cmd/baha/app_footprint_presenter.go:22-78) rendert: Target, Realizations-counts, Core, Resolution, Existing/Additional (InstanceID/State/RAM/Containers/Dependencies), unbound Requirements, Unused. Explizit dokumentiert "It neither resolves providers nor assumes resources" (footprint.go presenter:16-20).
- Bewusst WEGGELASSEN aus human: Version, ApplicationID, Scope, Ownership, Shared, Consumers, Ancillary; Requirements nur unbound (details).
- Der 245-fix (B3 H-V22) hat genau die machine-seitige divergenz (Unused) gefixt; human==json parity test TestAppFootprintShowSameAuthorityHumanAndJSON (app_footprint_show_test.go:46) + TestAppFootprintShowHumanAndJSONAgreeOnUnused (0428-245) pruefen die machine-oberflaeche; human ist presentation-layer, kein contract
- Klassifizierung: KEIN DEFECT. Human ist praesentation; JSON/MCP sind contract; die divergenz ist intentional (individuelle Evidenz nur; keine Totalen).

### Befund B3 (doku-luecke, low): Status-label divergiert zwischen human und JSON/MCP — status-namen NICHT zentral definiert
- Human presenter (cmd/baha/app_footprint_presenter.go:75-84 writeAppFootprintResource): maps ProviderStoppedOwned -> "stopped/owned (not running)", ProviderRunning -> "reused/running", ProviderNewRequired -> "new", default "unverified".
- JSON/MCP (internal/application/footprint.go:23-29): ProviderStoppedOwned -> "stopped-but-owned", ProviderRunning -> "running", ProviderNewRequired -> "newly-required", ProviderUnverifiable -> "unverifiable", ProviderForeign -> "foreign".
- Fuer denselben Footprint: human "- db: reused/running; ..." vs JSON "state":"running". Das ist ein LABELING-SWITCH (praesentation vs. canonical enum), kein Datenverlust (die ProviderState ist in beiden uebertragen; human nur um-benannt).
- Minimal-rezept (kartenwuerdig, owner giesst karte): zentral human-readable label map in einer const/funktion (z.B. renderProviderStateLabel) fuer app_footprint_presenter.go; dokumentieren dass canonical enum != human label. Optional: human-zeile canonical state in parens anhaengen ("- db: reused/running (running)"). Scope: cmd/baha/app_footprint_presenter.go + test.
- Klassifizierung: doku/luecke (labeling-inkonsistenz); kein data defect (ProviderState uebertragen).

### Befund B4 (doku-luecke, low): ProviderScope/Ownership/Consumers/Shared/Ancillary NICHT im human presenter — BY-DESIGN
- ProviderFootprint (internal/application/footprint.go:99-113) tragt Scope, Ownership, Shared, Consumers, Ancillary; JSON/MCP reporten sie; human presenter (cmd/baha/app_footprint_presenter.go:75-96 writeAppFootprintResource) rendert nur InstanceID/State/RAM/Containers/Dependencies.
- BY-DESIGN (human presenter dokumentiert "no assumed totals"); KEIN data defect.
- Klassifizierung: doku-luecke / intentional.

## Fundbilanz

- Echte Dekte: 0 (keine data-divergenz; JSON und MCP byte-identisch, human BY-DESIGN kuratiertes subset)
- Doku-luecke: 2 (B3 status-labeling-switch; B4 scope/ownership/shared/consumers/ancillary nicht human)
- Kein-befund: 3 (B1 JSON==MCP; B2 human curated subset intentional; B4 intentional)
- Gesamtflaeche: 4 Befunde; 0 card-worthy data defects; B3/B4 als doku-luecke dokumentiert (Fund->Karte-pflicht bei owner)

## Fundbilanz

(anzahl echte dekte / doku / null - to be filled)

## cleanliness

(nichts geaendert; keine eigenen container/volumes/state angelegt; ambient-core fremder lanes untouched)

## END w21-pr1702-0428-bughunt-hv25 DONE

- develop HEAD (witness): 62784eff7befadfaa8a08fc21eaffbd4e3cc8962 (git ls-remote origin refs/heads/develop)
- 4 Befunde; read-only desk audit; KEIN edit/commit/push/subagent; 237/231 nicht astasten; 245 ist fertig
- B1 (kein-befund): JSON (B) und MCP (C) byte-identisch fuer denselben Footprint; appMachineFootprintJSON cmd/baha/app_machine_adapters.go:242 -> appFootprintShowContext(JSON=true); registerMCPFootprintShowTool cmd/baha/app_registration_921.go:70-96; Rundtrip marshal->unmarshal verliert keine Felder (ProviderScope/Ownership string, registry.go:18/26)
- B2 (kein-befund): human presenter BY-DESIGN kuratiertes subset (footprint.go:115-124 Struktur); human==json parity test app_footprint_show_test.go:46 + 0428-245 agree-on-unused pruefen machine-oberflaeche
- B3 (doku-luecke/low): status-labeling-switch human "reused/running" vs canonical enum "running" (footprint.go:23-29 vs app_footprint_presenter.go:75-84); minimal-rezept in akte
- B4 (doku-luecke/low): ProviderScope/Ownership/Shared/Consumers/Ancillary (footprint.go:99-113) nicht human presenter; intentional
- 0 card-worthy data defects; B3/B4 doku-luecke (Fund->Karte-pflicht bei owner)
- keine eigenen container/volumes/state angelegt; ambient-core fremder lanes untouched
