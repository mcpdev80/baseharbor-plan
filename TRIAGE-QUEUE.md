# TRIAGE-QUEUE (gemeinsame Datei — Owner-Regel 2026-11-15)

Zustaendigkeit: Release-Welt (release/v0.4.27, main, #1574, r27-Dossier) = ChatGPT.
0.4.28-Lanes + Board = Codeman. Uebergaben NUR ueber diese Queue oder den Owner.
Codeman traegt Lane-Funde mit v0.4.27-Relevanzbewertung ein; ChatGPT taggt NUR bei leerer Queue.
Zweifelhafte Faelle: mit `ZWEIFEL` markieren und auf Owner-Entscheidung warten.

## Offene Eintraege (Codeman -> ChatGPT)

| Fund | Karte | Bew | v0.4.27-Relevanz | Status/Notiz |
| --- | --- | --- | --- | --- |
| BF-01 BASEHARBOR_STATE_DIR isoliert Target-Auswahl nicht (liest fremde Registrierungen) | t-20261115-bughunt-d28-state-dir-target | blocker | HOCH — defect auf develop 0e9ccb582, wuerde mit 0.4.27 rausgehen | ZWEIFEL: fix pre-tag (Frost-Brechung noetig) oder post-tag in 0.4.28? Owner-Entscheidung |
| BF-03 persistierte Target-Auswahl in weltlaeufig beschreibbarem /tmp-Pfad | t-20261115-bughunt-d28-tmp-selection | daemm/sicherheit | HOCH — Sicherheitstoetchen auf develop-Stand | ZWEIFEL: wie BF-01, Owner-Entscheidung |
| BF-02 baha app new schreibt keine Registrierung | t-20261115-bughunt-d28-app-new-reg | ux | MITTEL — evtl. dokumentiertes Verhalten; Doku-Gegenpruefung durch Release-Welt erbeten | wartet Triage |
| BF-04 deutsches 'Achtung' in englischer Ausgabe + JSON-Vertrag | t-20261115-bughunt-d28-i18n-achtung | ux/doku | MITTEL — 15 Fundstellen auf develop | wartet Triage |
| BF-05 beschaedigte Konfigurationsdatei stillschweigend ignoriert | t-20261115-bughunt-d28-bad-config-quiet | daemm | MITTEL — fail-open-Muster auf develop | wartet Triage |

Belegakte aller Funde: evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md (H-D28, Owner-stop-Harvest).

## Abarbeitet / abgegeben

(noch keine)
