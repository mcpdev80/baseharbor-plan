#!/usr/bin/env bash
# pilot-run.sh — DOKUMENT-SKRIPT des Positiv-Pfads (P3-Beweislauf, v0.4.27 Receipt-Kette).
#
# Ist-Zustand: Dieses Skript IST der Ablaufplan, keine Ausführung.
# Es wird vom Coordinator/Owner im Pilot-FALL explizit mit PILOT_RUN=yes ausgeführt.
# Ohne PILOT_RUN=yes gibt es nur die beabsichtigten Aktionen aus und beendet sich
# folgenlos mit 0 (DryRun-Guard; CODEMAN-START-Grenze "kein workflow_dispatch aus
# dieser Lane").
#
# Belegquelle: baseharbor-plan evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md
# Abschnitt 5 ("Run one ordinary contributor positive chain") und Task
# t-20261027-r27-shadow-run.md. Verifier-Interface: baseharbor scripts/receipt_verifier.py
# am finalen Kandidaten (Review-Kontext ad4d0f28, SHA kann durch f1/f2-Korrekturen
# fortschreiben — vor Pilot gegen den AKTUELLEN Kandidaten verifizieren).
#
# Platzhalter <...> sind bei Pilot zu verifizieren (siehe README-pr3-proof.md,
# "Platzhalter-Registrierung"). Keine erfundenen Gate-/Workflow-IDs.
set -euo pipefail

if [[ "${PILOT_RUN:-}" != "yes" ]]; then
  echo "DRYRUN — dieses Skript ist ein Doku-Skript. Keine Aktion ausgeführt."
  echo "Ausführung nur im autorisierten Pilot mit PILOT_RUN=yes und nach allen"
  echo "Vorbedingungen aus README-pr3-proof.md (Registration, Credential, Owner-Restart)."
  grep '^#>' "$0" | sed 's/^#> //'
  exit 0
fi

# ---------------------------------------------------------------------------
# Phase 0 — Vorbedingungen (jede individually; eine False => STOP, kein Pilot)
# ---------------------------------------------------------------------------
CANDIDATE_SHA="<FINALER-KANDIDATEN-SHA>"      # work/r27-correction-candidate HEAD, PR #1111 (inkl. f1/f2)
PRODUCT=mcpdev80/baseharbor
PLANNING=mcpdev80/baseharbor-plan
GATE=public-contracts                             # scripts/receipt_verifier.py: GATE, fest
PROD_WORKFLOW=.github/workflows/ci.yml            # Producer-Identität (receipt_verifier.py PRODUCT_WORKFLOW)
PROD_WORKFLOW_NAME="CI · Source & Quality"
POSTRUN_WORKFLOW=.github/workflows/receipt-post-run.yml
APPROVAL_WORKFLOW=.github/workflows/receipt-approval.yml
CONTRACT_PLAN_PATH=evidence/receipt-plans/public-contracts.json
CONTRACT_RECEIPT_DIR=evidence/receipts/public-contracts
PRODUCER_WORKFLOW_ID="<PLAZT-ci-workflow-id>"   # bei Pilot via 'gh api repos/$PRODUCT/actions/workflows' verifizieren
CI_ONLY_REGISTRATION="<PLAZT-registration-merge-sha>"  # Merge-SHA des CI-only default-main Registration-PRs

#> check: PR #1111 (oder Nachfolge-PR) gemäss Repo-Regeln akzeptiert, Kandidaten-SHA grün in Pflicht-CI
#> check: CI-only default-main Registration gemäss CODEMAN-START §2 auf main gelandet (TRUSTED_SOURCE pin gesetzt)
#> check: PLANNING_RECEIPT_WRITE_TOKEN provisioniert und nur im Vertrauens-Job lesbar (CODEMAN-START §2; Secret nie loggen)
#> check: Expliziter Owner-Restart liegt vor (Codeman-Pause sonst aktiv) — Owner-Entscheidung, nicht automatisierbar
git -C "$PRODUCT" cat-file -e "${CI_ONLY_REGISTRATION}^{commit}"
git -C "$PLANNING" pull --ff-only origin main

# ---------------------------------------------------------------------------
# Phase 1 — Ordinary contributor PR (echter Contributor, KEIN Owner-Handschuh)
# ---------------------------------------------------------------------------
#> hint: PR als normaler Contributor gegen develop; minimaler, CI-auswahlneutraler
#> hint: Eingriff (z.B. Docs), damit der public-contracts-Gate regulär läuft.
CONTRIB="<PLAZT-contributor-login>"            # ordinary contributor, nicht Owner
git -C "$PRODUCT" switch -c "pilot/r27-positive-<PLAZT-datum>" "origin/develop"
# ... minimaler Commit ...
git -C "$PRODUCT" push -u origin "pilot/r27-positive-<PLAZT-datum>"
gh pr create -R "$PRODUCT" --base develop --head pilot/r27-positive-<PLAZT:Datum> \
  --title "pilot(r27): ordinary contributor PR for receipt chain proof" --fill
PR="<PLAZT-pr-number>"                         # 'gh pr view --json number'
HEAD_SHA=$(gh pr view "$PR" -R "$PRODUCT" --json headRefOid -q .headRefOid)
CANDIDATE_SHA="$HEAD_SHA"                       # positiver Pfad: candidate == PR-head

# ---------------------------------------------------------------------------
# Phase 2 — Producer-Run (automatisch durch pull_request; kein dispatchen)
# ---------------------------------------------------------------------------
#> erwarteter Run: Workflow "CI · Source & Quality" (ci.yml), event pull_request,
#> attempt 1, head_sha == HEAD_SHA, conclusion success, Job public-contracts PASS
RUN_ID=$(gh run list -R "$PRODUCT" --workflow ci.yml --branch "refs/pull/$PR/merge" \
  --json databaseNumber,status,conclusion -q '.[0].databaseNumber')
gh run watch "$RUN_ID" -R "$PRODUCT" --exit-status
#> Erwartung attempt==1: ein Actions-Rerun ist KEIN neuer authentischer Versuch
#> (receipt_verifier.py live(): "pilot requires a fresh run, not an Actions rerun").
ATTEMPT=1

# ---------------------------------------------------------------------------
# Phase 3 — Automatischer post-run (receipt-post-run.yml via workflow_run)
# ---------------------------------------------------------------------------
#> erwartet: successful job in "Receipt · Post-Run Writer" auf dem selben Produkt-Repo,
#> automatisch via workflow_run (kein Dispatch); publiziert nur ueber den trusted Pfad.
#> schreibt in PLANNING:
#>   - plan fixture + receipt unter evidence/receipts/public-contracts/<run>-<attempt>.json (unapproved)
#>   - task->receipt Evidence-Referenz (receipt_tasklink; rv1-Hinweis: --pr-number
#>     Verdrahtigung mit dem finalen Kandidaten verifizieren)
#> STOP-Kriterium: post-run job skipped/echoed/manuell replays => kein Beweis (CODEMAN-START §5)
POSTRUN_RUN_ID="<PLAZT-postrun-run-id>"  # bei Pilot: gh run list --workflow receipt-post-run.yml
gh run watch "$POSTRUN_RUN_ID" -R "$PRODUCT" --exit-status
git -C "$PLANNING" pull --ff-only origin main
PLAN_REVISION=$(git -C "$PLANNING" rev-parse HEAD)
RECEIPT_PATH=$(ls "$PLANNING/$CONTRACT_RECEIPT_DIR"/ | tail -n1 | sed "s|^|$CONTRACT_RECEIPT_DIR/|")

# ---------------------------------------------------------------------------
# Phase 4 — Live-Verifikation vor der Owner-Entscheidung (nur Beweis, keine Aktion)
# ---------------------------------------------------------------------------
#> Erwartung: rc=0, Ausgabe "checked: public-contracts"
python3 "$PRODUCT/scripts/receipt_verifier.py" live \
  --planning "$PLANNING" \
  --product "$PRODUCT" \
  --revision "$(git -C "$PLANNING" rev-parse origin/main)" \
  --receipt "$RECEIPT_PATH" \
  --candidate "$CANDIDATE_SHA" \
  --plan "$(git -C "$PLANNING" rev-parse origin/main)"

# ---------------------------------------------------------------------------
# Phase 5 — Owner-Entscheidung (DER einzige manuelle Akt im ganzen Pfad)
# ---------------------------------------------------------------------------
#> Der/die Owner (mcpdev80) dispatcht selbst:
gh workflow run "$APPROVAL_WORKFLOW" -R "$PRODUCT" --ref main -f pr_number="$PR"
#> NICHTS weiter ist manuell: receipt_path, candidate_sha, plan_revision und alle
#> Commits werden vom Verifier aus dem PR-Reference AUTO-aufgeloest
#> (approve_pr/resolve_evidence; ein Mensch fuellt keine Receipt-Inputs).
#> Job-Ausgaben (Beleg fuer capture-evidence.py):
#>   approved: <receipt path>
#>   introduction: <commit, der den Receipt einfuehrt>
#>   approval: <Approval-Commit>
#>   publication: <FF-veroeffentlichter Planning-Commit>

# ---------------------------------------------------------------------------
# Phase 6 — Retained shadow consumption (API AUS, echter Erfolg, automatisch)
# ---------------------------------------------------------------------------
#> Erwartung: rc=0, "checked: public-contracts" — OHNE Netzwerk, mit vollem Git-Verlauf
#> (CODEMAN-START §5: positives retained case with origin API access forbidden).
set +e
env -u GH_TOKEN -u GITHUB_TOKEN \
  PATH="/usr/bin:/bin" \
  python3 "$PRODUCT/scripts/receipt_verifier.py" retained \
  --planning "$PLANNING" \
  --revision "$(git -C "$PLANNING" rev-parse origin/main)" \
  --receipt "$RECEIPT_PATH" \
  --candidate "$CANDIDATE_SHA" \
  --plan "$PLAN_REVISION"
RETAINED_RC=$?
set -e
[[ $RETAINED_RC -eq 0 ]] || { echo "STOP: retained shadow fehlgeschlagen (rc=$RETAINED_RC)"; exit 1; }

# ---------------------------------------------------------------------------
# Phase 7 — Evidence-Capture (nur oeffentliche Felder, JSON)
# ---------------------------------------------------------------------------
python3 "$(dirname "$0")/capture-evidence.py" --pr "$PR" \
  --output "$(dirname "$0")/../p3-positive-chain.json"
echo "pilot phase done — siehe README-pr3-proof.md fuer Review/Abnahme"
