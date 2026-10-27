# p3a — P3-Beweislauf-VORBEREITUNG (Skripte, kein Produktcode, kein Betrieb)

**Lane:** p3a (flash) · **Datum:** 2026-10-27 · **Scope:** nur
`baseharbor-plan/evidence/board-2026-10-27/scripts/**` (disjunkt zu rv1/f1)

## PLAN

(Von plan.py akzeptierte Nummerierung; [x]=erledigt.)

1. [x] Realitätsabgleich: basics-check, baseharbor-plan main ordinary pull
      (22c31a8 = rv1-Verdikt), Kandidat ad4d0f28 + rv1-Befunde gelesen
1. [x] Verifier-/Workflow-Interface am Kandidaten ad4d0f28 verifiziert
      (modes live/approve/retained, Fail-Meldungen mit file:line, Job-Namen,
      path_for, workflow_dispatch-Inputs)
1. [x] pilot-run.sh — Positiv-Pfad als Doku-Skript mit DryRun-Guard,
      Platzhaltern und "Inputs automatisch, manuell nur Owner-Entscheidung"
1. [x] negatives.sh — 3 kontrollierte Negative mit exakten Fail-Erwartungen
      (NEG-2 inkl. path_for-bedingtem Run-id-Rename; Transportfehler => STOP)
1. [x] capture-evidence.py — gh/Git read-only -> JSON (run_id, attempt,
      workflow_id, head/candidate/base_sha, receipt_path, introduction/
      approval/publication, rc je Check, keine Secrets); Smoke-Test ok
1. [x] README-pr3-proof.md — Reihenfolge, Stopp-Kriterien, Nicht-Automatisierung,
      Platzhalter-Registrierung
1. [x] Syntax-Checks: bash -n + DryRun beider .sh, py_compile + Mock-Smoke .py
1. [x] repo-rule compliance dokumentiert; render + check; bundle-commit; push main

## Dateien

- `scripts/pilot-run.sh` (neu) — 7 Phasen des Positiv-Pfads; DryRun ohne PILOT_RUN=yes
- `scripts/negatives.sh` (neu) — NEG-1/2/3a/3b in Wegwerf-Mirrors, expect_reject-Matrix
- `scripts/capture-evidence.py` (neu) — Evidence-Capture, Smoke-geprüft mit Mock-API
- `scripts/README-pr3-proof.md` (neu) — Reihenfolge + Stopp + Grenzen + Platzhalter

## Verifizierte Kandidaten-Referenzen (ad4d0f28, read-only)

- `receipt_verifier.py`: GATE public-contracts; main() modes/args; live() :230
  'wrong candidate SHA', :233 'wrong run/attempt'; verify_file :311/:312/:315;
  retained :325/:328/:331/:332; witness_failure :150 unterscheidet
  'run or resource not found' vs 'witness transport failure'; Job-Namen :261/:267
  ('PR · Public Contracts', 'PR · Trusted Plan'); path_for :101 leitet Receipt-Pfad
  aus run.id ab (für NEG-2 berücksichtigt).
- `receipt-approval.yml`: workflow_dispatch Input nur `pr_number`; Owner-context-Gate;
  approve-Ausgaben approved/introduction/approval/publication; TRUSTED_SOURCE '' bis
  Registration (fail-closed).
- rv1-Verdikt: BF-W3-1 (f1, publish-Kontrollfluss) + tasklink f2-Hinweis — in
  README/Doku-Skripten als "finalen Kandidaten pruefen" vermerkt; keine
  Gate-Erfindungen.

## Smoke-Beleg (dieser Lane, lokal, ohne Netzwerk)

- `bash -n` + DryRun: pilot-run.sh rc=0, negatives.sh rc=0 (keine Aktionen).
- `py_compile` capture-evidence.py ok; Mock-Smoke gegen Wegwerf-Git-Mirror:
  introduction/approval/publication/receipt_path/plan_revision korrekt, alle
  Checks pass=true.

## repo-rule compliance

- Write-Set: ausschließlich neue Dateien unter
  `evidence/board-2026-10-27/scripts/` + diese Evidence-Datei; baseharbor nur
  read-only inspiziert (git show ad4d0f28:…); kein workflow_dispatch ausgeführt;
  keine Secrets erfasst; Publication als ordinary pull → render+check →
  bundle-commit → push main gemaess baseharbor-plan/AGENTS.md.
- Konfliktvermerk: rv1/f1/Fix-Lanes schreiben nicht in dieses Verzeichnis;
  disjunktes Write-Set bestaetigt (git ls-tree HEAD vor Anlage geprueft).

## Grenzen dieser Vorbereitung (bewusst offen)

- Job-/Run-IDs, Workflow-IDs, Registration-SHA, Contributor-Login bleiben
  `<PLAZT…>` — bei Pilot aus Live-API/Git zu beweisen (README-Tabelle).
- NEG-3b-Historie-Setzung ist fixture-abhaengig; Meldungs-Erwartungen fix,
  Aufbau bei Pilot gegen finalen Kandidaten reproduzieren.
- Kein Merge/Acceptance/Release aus dieser Lane; Kartenstatus obliegt Coordinator.

END P3A-DONE FILES=5
