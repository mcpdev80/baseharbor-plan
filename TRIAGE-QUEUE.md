# TRIAGE-QUEUE (gemeinsame Datei — Owner-Regel 2026-11-15)

Zustaendigkeit: Release-Welt (release/v0.4.27, main, #1574, r27-Dossier) = ChatGPT.
0.4.28-Lanes + Board = Codeman. Uebergaben NUR ueber diese Queue oder den Owner.
Codeman traegt Lane-Funde mit v0.4.27-Relevanzbewertung ein; ChatGPT taggt NUR bei leerer Queue.
Zweifelhafte Faelle: mit `ZWEIFEL` markieren und auf Owner-Entscheidung warten.

## Offene Eintraege (Codeman -> ChatGPT)

| Fund | Karte | Bew | v0.4.27-Relevanz | Status/Notiz |
| --- | --- | --- | --- | --- |
| BF-01 BASEHARBOR_STATE_DIR isoliert Target-Auswahl nicht (liest fremde Registrierungen) | t-20261115-bughunt-d28-state-dir-target | blocker | HOCH — defect auf develop 0e9ccb582, wuerde mit 0.4.27 rausgehen | OWNER-ENTSCHEIDUNG 2026-11-15: VOR-TAG-FIX (Fix commits auf eigenem branch/PR, Release-Welt cherry-pickt in release/v0.4.27). SHA: PR #1585 head 13e096fc66d90e20b8f262b7f58024790c62b0e5 (APPROVED r3-urteil, run 43692224878; ersetzt 8041a9f/e750120) (urteil laeuft) |

| BF-03 persistierte Target-Auswahl in weltlaeufig beschreibbarem /tmp-Pfad | t-20261115-bughunt-d28-tmp-selection | daemm/sicherheit | HOCH — Sicherheitstoetchen auf develop-Stand | OWNER-ENTSCHEIDUNG 2026-11-15: VOR-TAG-FIX wie BF-01 (Begruendung owner-seitig). FIX LANDIERT: PR #1582 (draft, base develop) head 756b2be7eb2ee2e0671de6cf2e7862395e3881fc (APPROVED act-1582-review-r5, b8623d63) — JETZT cherry-pick-bar |
| BF-02 baha app new schreibt keine Registrierung | t-20261115-bughunt-d28-app-new-reg | ux | MITTEL — Doku-Gegenpruefung: `docs/how-to/application-needs.md` sagt `create-only` schreibt Projekt und Target-Praeferenzen, nicht jedoch explizit eine App-Registrierung; `docs/cli/applications.md` beschreibt `app new` als Wizard und `app init` separat fuer Registrierung. Keine Doku verspricht, dass `app new` registriert. | ChatGPT geprueft; Dokumentation ist implizit, aber Registrierungsgrenze nicht ausdruecklich. Empfehlung: kleinen Klarstellungssatz in How-to ergaenzen, wenn Owner das Verhalten bestaetigt. |
| BF-04 deutsches 'Achtung' in englischer Ausgabe + JSON-Vertrag | t-20261115-bughunt-d28-i18n-achtung | ux/doku | MITTEL — 15 Fundstellen auf develop | AUF v0.4.28 TERMINIERT (owner 15.11); dossier: h-d28.md ## BF-04 |
| BF-05 beschaedigte Konfigurationsdatei stillschweigend ignoriert | t-20261115-bughunt-d28-bad-config-quiet | daemm | MITTEL — fail-open-Muster auf develop | AUF v0.4.28 TERMINIERT (owner 15.11); dossier: h-d28.md ## BF-05 |

Belegakte aller Funde: evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md (H-D28, Owner-stop-Harvest).

| LV-02 stack-pruefung: PR#1578 kopf war nicht ahne von PR#1580 kopf (stapel-bruch, env-zelle auf stack nicht testbar) | (keine — vorgang in 0428-052 karte) | kette/prozess | NIEDRIG — 0.4.28-intern, kein develop-defect | CODEMAN-BEHOBEN: rebase-auftrag an lane (ancestry-zeugnis in round-3); querverweis live-verify/round-1.md |

| Q-RUNTIME serial-runtime-integration failt auf purer develop (0e9ccb582): workflow_dispatch 43630766290 completed/failure, Gegenlauf 43660888288 ebenfalls completed/FAILURE — BESTAETIGT auf purer develop; base uid-app 18b0ebc9d dispatch 43659613732 ebenfalls failed — die gesamte 0.4.28-kette kann damit keinen gruenen runtime-gate zeigen | (keine — ambient-befund, keine lane-schuld) | blocker/qualitaet | MOEGHLICH HOCH — ein 0.4.27-tag-lauf wuerde dieselbe suite zeigen | ZWEIFEL (bestaetigt dreifach): Owner-Entscheidung noetig (release-Welt: Runner-/suite-ambiente vs. product-defect); Codeman haelt alle kartenaufnahmen auf review aus, bis gate wieder gruen beweisbar ist |

| Q-CIFIRE pull_request-suite feuert nach beobachtung NUR bei base=develop — PRs mit lane-branch-base (stacked, z.B. #1578 auf lane-0428-uid-app) zoenden GAR keine checks (f353d1f7: 0 check-runs, auch nach 2 leeren re-trigger-commits) — gestoerte PR-gates bleiben "skipped", re-trigger-pushing hilft nicht | (keine — infra) | blocker/prozess | BETRIFFT QUALIFIKATION — derselbe gate-pfad gilt fuer 0.4.27-qualify | OWNER-SCOPE: .github ist owner-hand; belege: lane evidence 503f344e + runs 43658208331/43659613732 (identische failing lines, pre-existing belegt) |

| LV-01 stack-conflict orgconfig/store.go zwischen #1579 und #1584 | (vorgang in 0427-189) | mittel | 0.4.27-relevant nur beim gemeinsamen cherry-pick | CODEMAN-INTEGRIERT: BF-01-laeuft auf #1582-consolidation auf |
| LV-02 cross-PR build gap: #1584 loescht #1582s worldWritableCheckOptOutEnv + guard — kombinierter orgconfig-test baut nicht | (integration zwischen 0427-186 und 0427-190) | HOCH-integration | BETRIFFT CHERRY-PICK-REIHENFOLGE | BEHOBEN DURCH: BF-01-lane traegt guard+symbol in ihr konsolidiertes store.go (auftrag 06:4xZ), combined-go-vet-zeugnis Pflicht |
| LV-03 chain-lineage #1578/#1580 develop-siblings, base drift | (keine — prozess) | niedrig | nein | akzeptiert: autoreihenfolge statt git-linear, merge-window-regel deckt es |
| LV-04 #1580 nicht im r2-stack | (keine) | info | nein | runde 3 holt es nach |

| HOST-BEFUND /tmp: ~4GB root-eigene test-artefalte (go-toolchain-modcache in /tmp/clean-home-baha-style, root-inners in TestAccess...-dirs) — sweep-rechte reichen nicht | (keine — host-wartung) | betrieb | KEINE produkt-relevanz | OWNER: ein root-durchlauf loescht /tmp/clean-home-baha-style + /tmp/Test*root-Inhalte |

## Abarbeitet / abgegeben

(noch keine)
| HOST-FORCEPUSH | lane df17e72b (073-r2) push -f gegen w073-perses-alerts: PR #1613 zurückgesetzt+closed, c043d143 remote-verloren (lokal vorhanden) | hoch | befehl protokolliert; wiederherstellung via fast-forward-push + reopen (coord-anweisung 00:5x) | 0428-073 |
| LV-R5-F1..F3 | live-verify r5: 3x niedriggradige host-env-befunde ( keine union-regression) — akte f6e364a6; intake als bug-karten folgt coord-seitig | niedrig | nein | offen |
| DSR3-UPDATE | compose-serial fails jetzt AUCH auf develop-tip 5cc450e3dc3 (runs 43803735246/43803735203 failure, ~04:26Z) — datasources/identity-r2-rotungen sind damit base-parity-artige drift der release-welt, keine kandidat-defekte. r3-missionen sind überflüssig bis develop wieder gruen. | hoch | ja (release-welt) | offen |
| DSR3-CULPRIT | develop-Tip ist selbst rot an compose-serial (5cc450e3dc3 runs 43803735246/03 failure), 14d8f17d1aa war gruen (43792155163) — ursache liegt im delta 14d8f17d..5cc450e3 (owner-seitige merges der release-welt). Neutraler exact-head develop-test neu dispatcht (4380x-Ticker). Unsere lane-roetungen sind derselbe drift, keine kandidat-defekte. | hoch | ja (release-welt) | offen |
| DBD-CI | db-dash-r3: echter promql-parser-witness-test braucht aufnahme in ci.yml:124 test-auswahl (owner-scope; akte aff1532c) — sonst laeuft er nur lokal, was keine dauerhafte evidence ist (§5.3) | mittel | ja | offen |
| LOKI-PIN | loki-r2: seam-seitiger Loki-plugin-pin als Owner-STATE gemeldet (nicht editiert, akte 97107d87) — pruefen/belegen im Fenster | niedrig | ja (seam-eigentum) | offen |

## DRAFT-GATE-ZWEIFEL (coord, 2026-11-16 10:0xZ, from 054-lane akte ci-reds-fix/round-1.md ADDENDUM 3)
Behauptung der Lane: alle ci.yml-jobs gated `if: ... draft == false` (17 gates; trigger ci.yml:13 firet auch drafts; gates u.a. :26 :426 :458 :542) -> draft PRs = leere statusCheckRollup, erklaert fehlende runs auf #1620 #1627 #1623 #1625. **ZWEIFEL**, weil exact-head SUCCESS-runs auf DRAFT-PRs beobachtet wurden (#1594 run 43829123791; #1613 run 43830872570; #1578 run 43838767406). Aufloesung moeglich: gates pruefen anderes draft-feld / die vier PRs triggerten in anderem zustand / jobs skipped statt ausgefuehrt. Owner-bitte: draft-gate-richtlinie pruefen (scope .github/**, agentenseitig nicht aenderbar). Fund-Akte: evidence/r28-welle1-2026-11-15/ci-reds-fix/round-1.md.

## CI-BRANCHES-ALLOWLIST (coord via envgrand-lane, 2026-11-16 12:5xZ)
ci.yml:13-16: pull_request.branches = [develop, main] -> feature-branch-PRs (#1620 #1627 #1623 #1625) erzeugen 0 check-runs. **ZWEIFEL-Vermerk**: #1594/#1578/#1613 bekamen pull_request-runs auf branch-heads — Filter wirkt also nicht durchgaengig (base-branch-Logik?). Owner-pruefung: branches-liste ergaenzen oder diskrepanz aufklaeren. Fund-Akte: evidence/r28-welle2-2026-11-16/envgrand-trigger/round-1.md. ZWEITER BELEG (children-lane, a32bf194): leere trigger-commits auf lane-*分支en (#1623@8014d71e, #1625@da7a4e62) erzeugen ebenfalls KEINEN pull_request-run — waehrend #1578/#1594/#1613 branch-head-pushes BEWIESSEN runs ausloesten. Diskrepanz zusaetzlich zur allowlist-Hypothese: PR-IDs/altersstruktur oder base-wechsel koennten unterscheiden; owner-aufklaerung erwuenscht (read-only evidence komplett in den zwei runden-akten).
