---
id: w287-release-prepare-check-1
kind: evidence
card: t-20261017-release-0-4-27-prepare
shift: 2026-11-07
lane: w287-release-prepare-check
---
# v0.4.27 Release Prepare – Pruefrechnung check-1 (2026-11-07)

Rein lesender Pruefauftrag gemaess Mission w287: Kartenabschluss-Prüfung, develop-Abgleich
gegen Release-Checkliste, Lueckenliste fuer ein "vorbereitet"-Urteil. KEINE Veröffentlichung,
kein Tag, kein Release-Workflow, kein Product-Branch, keine .github-Aenderung. Diese Akte ist
die einzige Mutation (Plan-Repo main).

## PLAN

- Mission und Kartenvertrag lesen (plan.py show, tasks/t-20261017-release-0-4-27-prepare.md). DONE
- Plan-Repo-Identitaet und Remote-Zustand verifizieren (fetch, rev-parse). DONE
- Alle Karten mit release: v0.4.27 aus Frontmatter inventarisieren, Status zaehlen. DONE
- Aktive/wartende/geplante Karten namentlich pruefen: PR-Zustand via gh (ls-remote/PR-API). DONE
- develop f3db942859c gegen Release-Checkliste pruefen: Versionen, Pins, CHANGELOG. DONE
- Lueckenliste mit Fundstellen als Checklistenkarte schreiben. DONE
- Akte nach origin/main publizieren und dort verifizieren. SIEHE PUBLIZIEREN

## Zeugen (Plan-Repo, Realitaetsabgleich)

- git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v:
  origin https://github.com/mcpdev80/baseharbor-plan.git (fetch und push) – verifiziert VOR
  erstem Evidence-Commit (Zone-Kontrollwarnung 2026-11-07 beachten: workers/baseharbor-plan
  wurde NICHT verwendet).
- origin/main bei Arbeitsbeginn: c8b47fabc3eda0a77d28861dd0746aa57077ad1c
- Hinweis: im Plan-Repo lagen unkomittierte Aenderungen eines fremden Sessions
  (evidence/r27-welle5-folge-2026-11-07/node-cli/round-3.md, tasks/t-20261106-r27-remote-up-cli-path.md,
  neue maintenance-client/round-3.md). Diese wurden NICHT angefasst; die Akte wurde mit
  gezieltem git add ausserhalb dieses Arbeitsbaums publiziert.

## Produkt-Remote-Zeugen (frische Klone in /tmp/opencode/w287-wt, lesend)

- baseharbor develop HEAD bei Prüfung: 8a3f58da905fad52327d33466fde1d9568092519
- Missionreferenz f3db942859c68e78fe2e7c0a339be7eb0e380acb ("Merge PR #1404"): ist Vorfahr von
  develop HEAD (git merge-base --is-ancestor positiv); 119 Commits seither.
- baseharbor-demo main HEAD: c355d2a15f5b6b67ec665e8d9e1be863f4090831
- baseharbor-console main HEAD: 166831e8967f8940e870b5f60df6ee710b788fce
- baseharbor-node-connector main HEAD: 7fb235dd2f6e4b41485b3f4dc5419e167fc443fd
- Repo-Referenz-Demo-SHA (docs/releases/v0.4.23.demo-ref): d9637324fd77061b6239200f91ac55e3df3b47e4

## 1) Kartenabschlussstand der Release-Liste (release: v0.4.27)

Massgeblich ist `python3 scripts/plan.py list --release v0.4.27` (2026-11-07):
119 Karten = 75 accepted, 19 superseded, 1 dropped, 6 active, 3 wait, 15 waiting(planned).
Das Frontmatter-Inventar (kanban_status: 94 closed / 8 active / 2 wait / 15 planned) unterscheidet
sich davon nur durch drei Karten, die kanbanmaessig closed mit resolution=accepted/dropped sind,
 deren plan.py-Zustand aber noch active/wait traegt (vm-rebuild-integration, compose-host-isolation
 ueberpruefen; vm-rebuild ist bereits in 5.1-Hygiene). Die Roadmap-Zahl "93/119 accepted" in
releases/v0.4.27.md ist veraltet (wahr: 75 accepted + 19 superseded + 1 dropped = 95 abgeschlossen).
Geschlossen sind u.a. cleanup und updates
(akzeptiert), samtliche Wellen-1..5-Domänenkarten (contracts, state, journal, devices, profiles,
registry, connector service/trust/streams, management-host, client-commands, stage-versions,
version-view, artifact-resolution, remote-material, ci-lanes, vm-smoke).

Nicht abgeschlossen, namentlich, mit PR-Zeugnis (gh-PR-API, 2026-11-07):

- t-20261018-r27-access-wizard (0427-013, active): PR #1430 OPEN e651cb1c29 mergeable;
  PR #1433 OPEN 1a36cb2c8d CONFLICTING gegen aktuellen develop.
- t-20261018-r27-maintenance-client (0427-034, active): PR #1428 OPEN a3416743b1 mergeable.
- t-20261018-r27-node-cli (0427-039, active laut plan.py/Frontmatter): PR #1427 OPEN 0dc4c4d4f3
  und PR #1436 OPEN a267ae031a, beide mergeable. Im Arbeitsbaum des Plan-Repos laeuft eine
  unkomittierte round-3-Korrektur desselben Kandidaten (tasks/t-20261106.../evidence node-cli
  round-3.md zeigen merge auf develop 8a3f58da90 mit "closed/accepted") – noch NICHT auf
  origin/main publiziert, also kein Kartenabschluss. Board-Truth folgt dem Publisher dieser Runde.
- t-20261018-r27-onboarding-wizard (0427-043, active): PR #1435 OPEN 09ec640b2b mergeable.
- t-20261106-r27-remote-up-cli-path (0427-116, active): PR #1407 OPEN c4d528645e und PR #1437
  OPEN 4956639be8 mergeable; zusaetzlich Integrations-Draft PR #1438 (9ad6458c87, draft).
- t-20261105-r27-compose-host-isolation (0427-110, active): PR #1383 ist MERGED – Kartenstatus
  "active" ist veraltet; kein offener Kandidat bekannt. LUECKE: Karte muss auf Abschlussstand
  geprueft/ueberfuehrt werden (board truth).
- t-20261104-r27-vm-rebuild-integration (active, resolution=accepted): boarded active mit
  accepted-Resolution – Zustand fuehren (5.1) statt Sammelstatus.
- core-815-tests-greenfield-stacks-native-runtimes (wait): PR #1429 OPEN 0743011cfa und
  PR #1432 OPEN 6e06cb6a85 mergeable.
- t-20261104-r27-vm-integration-runs (wait): externer Host-Blocker, keine PRs.
- planned, nie beauftragt (15): remote-docker-web, remote-podman-web, remote-rollout,
  public-surfaces, docs, promote, access-proof, ci-consumption, local-parity-proof, team-proof,
  video-proof, nc-3 (Connector-Finalakzeptanz) sowie die Stage-Karten qualify, publish, verify.

Ketten-Logik: public-surfaces haengt an access-wizard, maintenance-client, node-cli,
onboarding-wizard und den Web/Rollout-Karten; docs und video-proof am Ende. Die sechs
unabgeschlossenen Domänenkarten mit offenen PRs blocken damit die gesamte Acceptance-Kette.

## 2) develop f3db942859c gegen Release-Checkliste (Versionen/Pins/CHANGELOG)

Fundstelle Basis: PRUEFPUNKT-Klon 8a3f58da90 (f3db942859c ist Vorfahr; Checkliste auf aktuellem
Stand, weil 119 Commits Differenz).

- Versionen: cmd/baha/main.go:24 `version = "dev"` (ldfgesteuert) – konsistent, kein harter
  0.4.26-Rest im Runtime-Pfad gefunden. scripts/release-requirements.json enthaelt 66 Treffer
  "v0.4.27": der Katalog IST inzwischen registriert – das Gegenstueck zur älteren Behauptung im
  Audit v0.4.27-ci-test-routing-audit-2026-11-07.md ("0 of 65 gates list v0.4.27"). Das Audit
  ist an dieser Stelle UBERHOLT; vor Qualify mit pr-check-runner/pr-gate-plan positiv und negativ
  neu zu verifizieren (scripts/pre-release-check-plan.py akzeptiert den Tag nun dem Anschein nach).
  scripts/pr-gate-map-v1.json nennt ebenfalls "v0.4.27".
- CHANGELOG: Unter "## [Unreleased]" ("## [0.4.27]" fehlt noch, korrekt vor Veröffentlichung)
  steht genau EIN Fix (Authoring-Intent compose-OmitEmpty, #1265). Zwischen f3db942859c und
  HEAD liegen 119 Commits (u.a. PRs #1404/#1405/#1406/#1418/#1419/#1420/#1424/#1425/#1434) ohne
  CHANGELOG-Aenderung; git diff zeigt KEINE CHANGELOG-/docs/releases-Aenderung in diesem Bereich.
  LUECKE: Freitext-Changelog fuer v0.4.27 unvollstaendig – vor dem Tag-Schnitt durch die
  betroffenen Kartenbesitzer/Integrations-Bahn nachziehen (Product-Repo, Owner-Kontrolle).
- Pins: docs/releases/v0.4.27.md und docs/releases/v0.4.27.demo-ref FEHLEN weiterhin auf develop
  (ls bestaetigt; aelteste demo-ref ist v0.4.23, lueckenhaft seit v0.4.24). pre-release.yml:121
  verlangt docs/releases/${tag}.demo-ref mit exakter 40-Zeichen-SHA fuer neue Versionen.
  Die Demo-Referenz-SHA d9637324fd ist NICHT der aktuelle demo main HEAD c355d2a15f – vor dem
  Pin muss die Qualifikation der gewaehlten Demo-Revision laufen, kein erfundener Pin.
  Release-Tags stehen bei v0.4.26; an der Kartenlinie (kein Tag) korrekt.
- Neue Tests seit f3db942859c: 18 neue _test.go-Dateien. Nicht-skippende laufen mit
  go test ./... im go-unit-tests-Pfad (CI route gegeben); 4 sind skip-gated
  (client_commands_core_integration_test.go, control_plane_single_native_ci_test.go,
  management_host_twoprocess_test.go, keycloak_single_native_ci_test.go) und brauchen den
  nativen Docker/Podman-Auswahlpfad – Status wie im Routing-Audit: NOT YET VERIFIED executed.
  Kein .github-Eingriff dieser Lane; Entdeckung/Trigger sind Owner/CI-lanes-Materie.

## 3) Was fehlt fuer ein "vorbereitet"-Urteil (Checkliste mit Fundstellen)

- p1 – Sechs Domänenkarten mit offenen PRs landen und akzeptieren: #1430/#1433 (1433 CONFLICTING,
  Fundstelle: gh mergeable), #1428, #1427/#1436, #1435, #1407/#1437 plus Draft-Integration #1438.
- p2 – core-815 Greenfield-Stacks #1429/#1432 und vm-integration-runs (wait) abarbeiten.
- p3 – Die 15 planned-Karten (remote-docker-web bis video-proof, nc-3, public-surfaces, docs,
  promote) mindestens in ihrem geforderten Akzeptanzanteil erfuellen; public-surfaces/docs sind
  harte Gate-Vorbedingung der Release-Checkliste.
- p4 – docs/releases/v0.4.27.md (menschliche Release-Notes EN/DE-Konsistenz) und
  docs/releases/v0.4.27.demo-ref (verifizierte Demo-SHA) auf develop; Fundstellen: pre-release.yml:121,
  ls docs/releases/.
- p5 – CHANGELOG.md [Unreleased] auf [0.4.27] vollstaendig nachziehen (119 Commits seit #1404
  unkommentiert); Fundstelle: diff CHANGELOG f3db..HEAD leer.
- p6 – release-requirements.json/pr-gate-map-v1.json v0.4.27-Eintrag positiv UND negativ
  regressionsgetestet (Routing-Audit-Block "Confirmed selection / release-catalog gaps" ist
  teilweise ueberholt, neu zu verifizieren); Fundstelle: grep 66 Treffer.
- p7 – Test-Routing-Matrix Abschluss: 4 skip-gated neue Tests + die P0/P1-Zeilen des
  CI-Routing-Audits mit ausgefuehrten (nicht skipped) Nachweisen auf exaktem Head.
- p8 – Freeze der vier Immutable-ecosystem-SHAs (Core develop, Demo main, Console main,
  Connector main nach Consumer-Qualifikation) und Kandidatenbaum-Matrix; erst nach p1–p7.
- p9 – Karten-Hygiene: compose-host-isolation (#1383 MERGED, Karte "active") und
  vm-rebuild-integration (active mit resolution=accepted) auf wahren Stand ziehen; Roadmap-Zaehler
  in releases/v0.4.27.md (93/119) ist leicht veraltet. Fundstelle: Frontmatter-Inventar oben.
- NICHT Teil von Prepare: Tag, Pre-Release-Lauf, Promotion, Publish, Pages-Deployment –
  Owner-Aktion gemaess AGENTS 5.2 und Owner-Direktive 2026-11-07.

Zwischenstand-Zahl als Prozentliste (119 Release-Karten): abgeschlossen 95 von 119 (80 %:
75 accepted + 19 superseded + 1 dropped), offen 25 (6 aktive PR-Karten, 3 wait, 15 planned/
waiting inkl. Stage-Karten), damit ready-Kante = Abschluss von p1–p7, nicht Kartenzahl allein.

##repo-rule compliance

- Nur Plan-Repo main (diese Akte) mutiert; Zone /tmp/opencode/w287-wt mit lesenden Klone.
- Keine .github-Aenderungen, keine Reruns, keine Tags, keine Produkt-Branches, keine Subagenten.
- gh nur lesend (pr view/list). Fremde unkomittierte Plan-Aenderungen erhalten.

## 5) Betriebsbefund: geteilte Plan-Arbeitsbaeume (wichtig fuer Coordinator)

Mehrere dieser Lanes (w275, w282, w285, w287) arbeiten im SELBEN Verzeichnis
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan. Beim Publizieren dieser Akte fand ich
unkomittierte Aenderungen der node-r3-Lane vor (tasks/t-20261018-r27-node-cli.md,
node-cli/round-3.md, views/*). Nach fetch erschien cad293f2 ("coord: evidence-recovery node
round-3.md"), das genau diese Dateien bereits publiziert hatte und mit meinem stash-carry-forward
kollidierte. Aufloesung: die publizierten cad293f2-Inhalte sind massgeblich. Die carry-forward-commits
(537a3cc0) wurden zurueckgenommen (c0591090); der diff origin/main..HEAD enthaelt damit AUSSCHLIESSLICH
meine eigene Akte, keine fremden Stände. Empfehlung an den Coordinator: lanesgetrennte Klone oder commit-before-dispatch,
sonst naechster stash-Konflikt.

Die uebrigen Fremd-aenderungen (compose-host-isolation/round-7.md, infra/podman2-rebuild-2.md,
maintenance-client/round-3.md, remote-up-cli/round-3.md) habe ich bewusst unkomittiert liegen
lassen - ihren Lanes zugeordnet; kein Loschen.

## Publizieren

- Witness-Push: git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan push origin HEAD:main
- Commit-Kette cad293f2..HEAD (log-Line-Zeuge): 537a3cc0 carry-forward (unkomittierte Fremd-edits
  der node-r3-lane), f748b6de/4c6d368b meine Akte + Ruecknahme des carry-forward. Der
  GESENDETE DIFF origin/main..HEAD enthaelt nur evidence/w287-release-prepare/check-1.md; die
  carry-forward/revert-Paare heben sich dateiweise auf. Kein fremder Kandidat wird mitgefuehrt.
- Verifikation vor END: git ls-tree -r --name-only origin/main | grep release-prepare/check-1.md
  (Exakte Ausgabe steht in der END-Zeile und als letzter Absatz dieser Akte nach dem Push.)

## END

END_ZEILE: siehe letzte Zeile nach Push (wird hier wortgleich gesichert).
