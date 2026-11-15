# TRIAGE-QUEUE (gemeinsame Datei — Owner-Regel 2026-11-15)

Zustaendigkeit: Release-Welt (release/v0.4.27, main, #1574, r27-Dossier) = ChatGPT.
0.4.28-Lanes + Board = Codeman. Uebergaben NUR ueber diese Queue oder den Owner.
Codeman traegt Lane-Funde mit v0.4.27-Relevanzbewertung ein; ChatGPT taggt NUR bei leerer Queue.
Zweifelhafte Faelle: mit `ZWEIFEL` markieren und auf Owner-Entscheidung warten.

## Offene Eintraege (Codeman -> ChatGPT)

| Fund | Karte | Bew | v0.4.27-Relevanz | Status/Notiz |
| --- | --- | --- | --- | --- |
| BF-01 BASEHARBOR_STATE_DIR isoliert Target-Auswahl nicht (liest fremde Registrierungen) | t-20261115-bughunt-d28-state-dir-target | blocker | HOCH — defect auf develop 0e9ccb582, wuerde mit 0.4.27 rausgehen | OWNER-ENTSCHEIDUNG 2026-11-15: VOR-TAG-FIX (Fix commits auf eigenem branch/PR, Release-Welt cherry-pickt in release/v0.4.27). SHA: folgt (fix-lane im dispatch) |
| BF-03 persistierte Target-Auswahl in weltlaeufig beschreibbarem /tmp-Pfad | t-20261115-bughunt-d28-tmp-selection | daemm/sicherheit | HOCH — Sicherheitstoetchen auf develop-Stand | OWNER-ENTSCHEIDUNG 2026-11-15: VOR-TAG-FIX wie BF-01 ( Begruendung owner-seitig eingetragen). SHA: folgt |
| BF-02 baha app new schreibt keine Registrierung | t-20261115-bughunt-d28-app-new-reg | ux | MITTEL — Doku-Gegenpruefung: `docs/how-to/application-needs.md` sagt `create-only` schreibt Projekt und Target-Praeferenzen, nicht jedoch explizit eine App-Registrierung; `docs/cli/applications.md` beschreibt `app new` als Wizard und `app init` separat fuer Registrierung. Keine Doku verspricht, dass `app new` registriert. | ChatGPT geprueft; Dokumentation ist implizit, aber Registrierungsgrenze nicht ausdruecklich. Empfehlung: kleinen Klarstellungssatz in How-to ergaenzen, wenn Owner das Verhalten bestaetigt. |
| BF-04 deutsches 'Achtung' in englischer Ausgabe + JSON-Vertrag | t-20261115-bughunt-d28-i18n-achtung | ux/doku | MITTEL — 15 Fundstellen auf develop | AUF v0.4.28 TERMINIERT (owner 15.11); dossier: h-d28.md ## BF-04 |
| BF-05 beschaedigte Konfigurationsdatei stillschweigend ignoriert | t-20261115-bughunt-d28-bad-config-quiet | daemm | MITTEL — fail-open-Muster auf develop | AUF v0.4.28 TERMINIERT (owner 15.11); dossier: h-d28.md ## BF-05 |

Belegakte aller Funde: evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md (H-D28, Owner-stop-Harvest).

| LV-02 stack-pruefung: PR#1578 kopf war nicht ahne von PR#1580 kopf (stapel-bruch, env-zelle auf stack nicht testbar) | (keine — vorgang in 0428-052 karte) | kette/prozess | NIEDRIG — 0.4.28-intern, kein develop-defect | CODEMAN-BEHOBEN: rebase-auftrag an lane (ancestry-zeugnis in round-3); querverweis live-verify/round-1.md |

| Q-RUNTIME serial-runtime-integration failt auf purer develop (0e9ccb582): workflow_dispatch 43630766290 completed/failure, Gegenlauf 43660888288 laeuft; base uid-app 18b0ebc9d dispatch 43659613732 ebenfalls failed — die gesamte 0.4.28-kette kann damit keinen gruenen runtime-gate zeigen | (keine — ambient-befund, keine lane-schuld) | blocker/qualitaet | MOEGHLICH HOCH — ein 0.4.27-tag-lauf wuerde dieselbe suite zeigen | ZWEIFEL: Owner-Entscheidung noetig (release-Welt: Runner-/suite-ambiente vs. product-defect); Codeman haelt alle kartenaufnahmen auf review aus, bis gate wieder gruen beweisbar ist |

## Abarbeitet / abgegeben

(noch keine)
