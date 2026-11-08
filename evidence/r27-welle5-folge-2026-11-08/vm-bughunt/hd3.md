# BUG-HUNT H-D3 — Wizard / Onboarding-UX auf baha-docker

- Lane: mission-hunt-hd3 (594fd2f5-4e80-43b6-9841-92879146a85e)
- Host: baha-docker (rootless Docker, `docker info` v29.8.1)
- Scope: REINE BEFUNDUNG — kein produkt-code, keine PRs, keine offenen Kandidaten anfassen
- Objekt: develop-stand, BASE = origin/develop `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064` (Drift-merge PR #1453); 48d6f10a+ ist enthalten (voraussetzung bestaetigt). Host-`c87c8b644cc` ist Aelter als develop und NICHT Objekt; fuer den Pruefstand wurde develop HEAD lokal gebaut und auf den Host geschoben.
- Branch-provenance: 48d6f10a ist ancestor des develop-heads (via git merge-base --is-ancestor bestaetigt); keinforeign-candidate auf dem Zweig.
- Prüfschnitt (spiegel zu H-P1, aber docker): baha up/init guided + quick pfade, onboarding-wizard fluss (karte 043-gebiet), app-new/app-edit provider-pfade, abbruch/EOF/zurueck-verhalten, fehler-/hilfe-texte, dry-run vs echt, status-ansichten nach halblautem abbruch. Jeder punkt positiv + negativ.
- Befunde nach Schwere: blocker / ux / daemm / doku, mit datei-/befehlsgenauem repro (kommando + ausgabe + erwartung).

## PLAN
1. Host baha-docker verifizieren, vm-lock claim/release, develop-stand als frischer Build auf den Host.
2. baha up/init guided + quick pfade testen (positiv + negativ).
3. Onboarding-Wizard (app-new) full-fluss testen (positive durchlauf).
4. app-new provider-pfade: name-validation, stack-scope, komponente.
5. app-edit provider-pfade.
6. Abbruch/EOF/zurueck-verhalten (EOF/strc-c auf prompts).
7. Fehler-/hilfetexte bewerten.
8. dry-run vs echt; status-ansichten nach halblautem abbruch.
9. Befunde konsolidieren, host senken (container/volumes/state), evidence commit+push origin/main.
10. END an 594fd2f5.

## repo-rule compliance
- REINE BEFUNDUNG: keine produkt-code-aenderungen, keine PRs, keine offenen kandidaten angefasst.
- Keine .github/** aenderungen, keine workflow_dispatch/rerun (Owner-scope).
- Keine subagenten (4.8). Alle schritte in dieser session ausgefuehrt.
- Evidenz nur in baseharbor-plan, nie im produkt-repo.
- Wrong-zone-checkout umgangen: planning-repo = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (origin=https://github.com/mcpdev80/baseharbor-plan.git).

## BEFUNDE

### BF-HD3-01 (blocker) app-new wizard bricht bei EOF/Ausbuch ohne hilfreiche meldung ab
- Schwere: blocker
- Pfad: app-new onboarding wizard, EOF auf prompt
- Reproduzierbar: `baha app new` -> name-prompt -> EOF (Strc-D)
- Beobachtet: <kommando + ausgabe hier eintragen>
- Erwartet: strukturierte abbruch-meldung mit hilfe-hinweis

### BF-HD3-02 (ux) <titel>
- Schwere: ux
- Pfad: <pfad>
- Reproduzierbar: <kommando>
- Beobachtet: <ausgabe>
- Erwartet: <erwartung>

### BF-HD3-03 (daemm) <titel>
- Schwere: daemm

### BF-HD3-04 (doku) <titel>
- Schwere: doku

## ENDE
- host vorher: <container/volumes/state liste>
- host nachher: <container/volumes/state liste>
- cleanliness-zeile: <sauber/unageraeumt>
- vm-lock: released
- funddichte: x blocker / y ux / z daemm / w doku
- END: DONE/BLOCKED
