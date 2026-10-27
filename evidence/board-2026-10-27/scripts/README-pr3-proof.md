# README-pr3-proof — P3-Beweislauf (v0.4.27, automatische Receipt-Kette)

**Status: VORBEREITUNG (Lane p3a). Keine dieser Aktionen wurde aus dieser Lane ausgeführt.**
Die `.sh`-Dateien sind Doku-Skripte mit DryRun-Guard (`PILOT_RUN=yes` / `NEG_RUN=yes`
nötig für Ausführung); `capture-evidence.py` ist read-only ausführbar.

Bezugsdokumente: CODEMAN-START.md §5 (Maßstab für Positiv + 3 Negative),
Task `t-20261027-r27-shadow-run.md` (Abnahme), rv1-Review
`../rv1-review-ad4d0f28.md` (BF-W3-1 → f1, tasklink-Verdrahtung → f2).
Verifier-Interface referenziert Kandidaten `ad4d0f28`; **bei Pilot gegen den finalen
integrierten Kandidaten (nach f1/f2) prüfen** — f1/f2 können den SHA fortschreiben.

## Dateiinventar

| Datei | Zweck | Ausführbar in dieser Lane? |
|---|---|---|
| `pilot-run.sh` | Positiv-Pfad als Kommando-Folge (PR → Producer-Run → post-run → live → Owner-Dispatch → retained shadow → capture) | NEIN (Doku; DryRun zeigt nur Absicht) |
| `negatives.sh` | Die 3 kontrollierten Negative gegen den Produktions-Verifier mit exakten Fail-Erwartungen | NEIN (Doku; DryRun) |
| `capture-evidence.py` | gh-API/Git read-only → `../p3-positive-chain.json` (run_id, attempt, workflow_id, head/candidate/base_sha, receipt_path, introduction/approval/publication, rc je Check; keine Secrets) | JA (read-only, schreibt nur die Output-JSON) |
| `README-pr3-proof.md` | Dieses Dokument | — |

## Reihenfolge (strikt)

0. **Vorbedingungen** (alle wahr, sonst kein Pilot): Owner-Restart erteilt; Kandidat
   (PR #1111 + f1/f2) unabhängig-reviewt und Pflicht-CI grün; CI-only
   default-main-Registration auf main gelandet (`TRUSTED_SOURCE`-Pin gesetzt,
   `receipt-approval.yml`/`receipt-post-run.yml` auf main registriert);
   `PLANNING_RECEIPT_WRITE_TOKEN` vom Owner provisioniert (nur im Vertrauens-Job
   sichtbar, niemals geloggt).
1. `pilot-run.sh` Phasen 1–4: ordinary contributor PR, automatischer Producer-Run
   (attempt 1), automatischer post-run-Publication, `live`-Verifikation rc=0.
2. Phase 5: **ausschließlich die Owner-Entscheidung** als
   `gh workflow run receipt-approval.yml --ref main -f pr_number=<PR>`. Approval,
   Receipt-Auto-Resolution, Publication, Task-Link: automatisch.
3. Phase 6: retained shadow consumption mit deaktiviertem API (`env -u GH_TOKEN …`),
   rc=0 als echter SUCCESS-Job im Nachlauf, nicht als skipped/echoed Job.
4. `capture-evidence.py --pr <PR> --post-run <id> --approval-run <id> …` →
   `p3-positive-chain.json`; Verweise/URLs im Task-Beleg verankern.
5. `negatives.sh` NEG-1, NEG-2, NEG-3a/3b gegen dieselbe production Pfad; jedes
   `expect_reject`-PASS dokumentieren, Original-Evidenz unverändert lassen.
6. Unabhängiges Review des finalen Kandidaten + dieses Belegs; erst danach
   Kartenschritt review→accepted (nur durch berechtigte Instanz).

## Stopp-Kriterien (sofort abbrechen, nicht umdeuten)

- Irgendein `STOP`-Zweig in `pilot-run.sh`/`negatives.sh` (retained rc≠0;
  post-run job skipped/geechoht/manuell replays; Transportfehler statt 404 in
  NEG-2; rc=0 oder Fremd-Meldung in einem Negativ; Planning-Stamm angefasst).
- Producer-Ereignis braucht einen Actions-Rerun oder einen Owner-Handschuh-PR statt
  ordinary contributor → Beweis nichtig, Kandidaten-/Setup-Fehler beheben, neu starten.
- Platzhalter lässt sich nicht eindeutig verifizieren (Workflow-ID, Registration-SHA,
  Contributor-Login) → Pilot nicht starten.
- f1/f2 ist noch nicht im Kandidaten integriert, oder rv1-Befunde sind am finalen SHA
  nicht reproduzierbar behoben → Realitätsabgleich zuerst.
- Deadline 2026-10-29T23:35:50Z ohne erreichbaren Automatik-Nachweis → gemäß
  CODEMAN-START §7 Infrastruktur-Ausbau stoppen und Blocker berichten.

## Was NICHT automatisiert werden darf

- Die Owner-Entscheidung (`gh workflow run` durch mcpdev80) — Der Dispatch selbst.
  Der Dispatcher kann nichts beschleunigen; Inputs `receipt_path`/`candidate_sha`/
  `plan_revision` füllt NIEMAND manuell (auto-resolved, sonst fail-closed).
- Manual evidence push / git am / patch-download / Replay eines post-run Jobs;
  ein lokaler Commit gilt nie als publiziert.
- Editieren echter approved Receipts oder Planning-Geschichte (auch nicht für
  Negative — Mirrors nur, siehe `negatives.sh`).
- Erfundene Gate-/Workflow-IDs; Alles `<PLAZT…>`-Felder müssen bei Pilot aus der
  Live-API/Git bewiesen werden.
- Kein Release/Tag/Deployment, kein Branch-Protection-Bypass, keine
  Full-CI-Wiederholung für unveränderte Commit-Sha.

## Platzhalter-Registrierung (bei Pilot zu verifizieren)

| Platzhalter | Beweismittel im Pilot |
|---|---|
| `<FINALER-KANDIDATEN-SHA>` | `gh pr view 1111 --json headRefOid` (nach f1/f2) |
| `<PLAZT-contributor-login>` | ordinary contributor Account (nicht mcpdev80) |
| `<PLAZT-pr-number>` | `gh pr create` Ausgabe |
| `<PLAZT-postrun-run-id>` | `gh run list --workflow receipt-post-run.yml` |
| `<PLAZT-ci-workflow-id>` | `gh api repos/mcpdev80/baseharbor/actions/workflows` |
| `<PLAZT-registration-merge-sha>` | Merge-SHA des CI-only main-Registration-PRs |
| `<PLAZT-andere-echte-40hex>` | beliebige echte, nicht zum Plan gehoerende Commit-SHA |
| `EXPECTED_PLANNING_HEAD` | `git -C "$PLANNING_LOCAL" rev-parse HEAD` vor Negativen |
| Job-Namen `PR · Public Contracts` / `PR · Trusted Plan` | `receipt_verifier.py` live() (ad4d0f28 :261/:267) |

## repo-rule compliance (Lane p3a)

- Write-Set ausschließlich `baseharbor-plan/evidence/board-2026-10-27/**`
  (disjunkt zu rv1 `rv1-review-ad4d0f28.md` und f1-Produktbranch); kein
  Produktcode, keine Workflow-Dateien, kein baseharbor-Schreibzugriff (read-only
  Inspektion von `ad4d0f28` Belegquellen).
- Kein `workflow_dispatch` ausgeführt; keine Secrets in JSON/Logs
  (`capture-evidence.py` schreibt nur oeffentliche API-/Git-Felder).
- Publiziert als ordinary pull → render+check → bundle-commit → push main
  (AGENTS baseharbor-plan: planning-direct-main, evidence-only).
