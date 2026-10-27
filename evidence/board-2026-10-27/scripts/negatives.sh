#!/usr/bin/env bash
# negatives.sh — DOKUMENT-SKRIPT der drei kontrollierten Negative (P3-Beweislauf).
#
# Ziel (CODEMAN-START §5): derselbe Produktions-Verifier-Pfad wie im Positivfall,
# mit kontrolliert defekten Eingaben/Fixtures. Erwartet wird die ANGESEQUENE
# Verweigerung (rc=1 + exakte Meldung), NICHT ein Netzwerk-/Tool-Fehler.
# Transportfehler, rc>1 oder falsche Meldung => STOP, Negativ gilt als NICHT belegt.
#
# Verifier: baseharbor scripts/receipt_verifier.py am FINAL-integrierten Kandidaten
# (Review-Kontext ad4d0f28; f1/f2 koennen den SHA fortschreiben — vor Pilot gegen
# dem aktuellen Kandidaten pruefen). Referenzierte Fail-Meldungen im Kandidaten
# ad4d0f28 verifiziert: live():230 'wrong candidate SHA', verify_file():311 'wrong
# receipt path', :312 'receipt does not match required candidate/plan', :315 'plan
# candidate mismatch', witness_failure():150 'run or resource not found' vs
# 'witness transport failure', retained():325 'original receipt was edited',
# :328 'receipt commit must introduce a new path', :331 'receipt must have exactly
# one approval edit and no later edits', :332 'approval commit mismatch'.
#
# Grenzen:
#  - Alle Mutationen in WEGWERF-Mirrors unter "$NEG_TMP" (mktemp -d).
#  - Echte approved Receipts und der Planning-Stamm bleiben unangetastet.
#  - Ohne NEG_RUN=yes: DryRun, keine Aktion.
set -euo pipefail

PLANNING_LOCAL="<PLAZT-lokaler-checkout-baseharbor-plan>"   # read-only Nutzung, Stamm unveraendert
PRODUCT_LOCAL="<PLAZT-lokaler-checkout-baseharbor>"         # Kandidaten-HEAD checkout
EXPECTED_PLANNING_HEAD=""   # bei Pilot: Planning-HEAD vor den Negativen erfassen

if [[ "${NEG_RUN:-}" != "yes" ]]; then
  echo "DRYRUN — Doku-Skript. Keine Aktion ausgeführt. Ausführung nur im autorisierten"
  echo "Pilot-Kontext mit NEG_RUN=yes (Vorbereitungsstufen siehe README-pr3-proof.md)."
  grep '^#>' "$0" | sed 's/^#> //'
  exit 0
fi

VERIFIER="$PRODUCT_LOCAL/scripts/receipt_verifier.py"
GATE=public-contracts
CHAIN_JSON="$(dirname "$0")/../p3-positive-chain.json"
PLAN_REVISION=$(jq -r .plan_revision "$CHAIN_JSON")
RECEIPT_PATH=$(jq -r .receipt_path "$CHAIN_JSON")
CANDIDATE_SHA=$(jq -r .candidate_sha "$CHAIN_JSON")
INTRODUCTION_COMMIT=$(jq -r .introduction_commit "$CHAIN_JSON")
WRONG_CANDIDATE="<PLAZT-andere-echte-40hex>"   # echte, NICHT zum Plan gehoerende SHA
NEG_TMP=$(mktemp -d)
trap 'rm -rf "$NEG_TMP"' EXIT
#> check: PLANNING_LOCAL/Product-Locations im Umgebungskonzept des Pilot gesetzt (read-only Nutzung)

mirror () {  # $1=name  -> Pfad des Frisch-Mirrors (Vollhistorie)
  local d="$NEG_TMP/$1"
  git clone -q --no-hardlinks "$PLANNING_LOCAL" "$d"
  echo "$d"
}

canon_edit () {  # $1=file  $2=python-dict-update-code (kanonische Neu-Serialisierung)
  python3 - "$1" "$2" <<'PYEOF'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1])
value = json.loads(p.read_bytes())
exec(sys.argv[2], {"value": value})
p.write_bytes((json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=True) + "\n").encode())
PYEOF
}

expect_reject () {  # $1=label $2=rc $3=output $4...=erlaubte Meldungs-Muster
  local label="$1" rc="$2" out="$3"; shift 3
  if grep -q 'witness transport failure\|GitHub operation failed\|operation not permitted' <<<"$out"; then
    echo "STOP [$label]: Transport-/Tool-Fehler statt Verweigerung — Negativ NICHT belegt"; exit 1
  fi
  if [[ "$rc" -eq 0 ]]; then echo "STOP [$label]: Verifier hat NICHT abgelehnt (rc=0)"; exit 1; fi
  if [[ "$rc" -gt 1 ]]; then echo "STOP [$label]: rc=$rc — Argument-/Crash-Fehler statt Verweigerung"; exit 1; fi
  local m
  for m in "$@"; do grep -q "$m" <<<"$out" && { echo "PASS [$label]: rc=1 mit '$m'"; return; }; done
  echo "STOP [$label]: rc=1 aber Meldung passt zu keinem erwarteten Muster:"; echo "$out"; exit 1
}

# ---------------------------------------------------------------------------
# NEG-1 — wrong candidate SHA (mutationsfrei: Argument gegen echte Evidenz)
# ---------------------------------------------------------------------------
#> Der Verifier wird gegen die UNVERAENDERTEN published Evidence mit einem
#> Kandidaten aufgerufen, der nicht der Receipt-Kandidat ist.
#> Erwartung (retained/verify_file Pfad): rc=1 'receipt does not match required
#> candidate/plan'. Eine gefaelschte Receipt-gegen-Plan-Variante wuerde 'wrong
#> candidate SHA' (live) bzw. 'plan candidate mismatch' liefern — beide als
#> derselbe Defekt akzeptiert; jede andere Meldung => STOP.
OUT=$(python3 "$VERIFIER" retained --planning "$PLANNING_LOCAL" \
  --revision "$PLAN_REVISION" --receipt "$RECEIPT_PATH" \
  --candidate "$WRONG_CANDIDATE" --plan "$PLAN_REVISION" 2>&1); RC=$?
expect_reject "NEG-1 wrong candidate SHA" "$RC" "$OUT" \
  'receipt does not match required candidate/plan' 'wrong candidate SHA' 'plan candidate mismatch'

# ---------------------------------------------------------------------------
# NEG-2 — genuinely missing run ID (Live-Pfad, echte API gegen toten Run)
# ---------------------------------------------------------------------------
#> Mirror auf Introduction-Revision (unapproved — Bedingung von live()), dann
#> run.id auf garantiert nie existenten Wert 9000000001; Dateiname MITRAEND in
#> 9000000001-1.json umbenennen (path_for leitet den Pfad aus run.id ab — ohne
#> Rename käme nur 'wrong receipt path', ein unbewiesener Pfad).
#> Erwartung: rc=1 mit 'run or resource not found' (echter HTTP-404).
#> STOP-Bedingung: 'witness transport failure' => Netzwerk-Outage ist KEIN
#> Missing-run-Nachweis (CODEMAN-START §5).
M2=$(mirror neg2)
git -C "$M2" checkout -q "$INTRODUCTION_COMMIT"
canon_edit "$M2/$RECEIPT_PATH" 'value["run"] = {"id": 9000000001, "attempt": 1}'
mkdir -p "$M2/evidence/receipts/$GATE"
mv "$M2/$RECEIPT_PATH" "$M2/evidence/receipts/$GATE/9000000001-1.json"
git -C "$M2" add -A && git -C "$M2" commit -qm "neg2: dead run id (controlled, throwaway mirror)"
OUT=$(python3 "$VERIFIER" live --planning "$M2" --product "$PRODUCT_LOCAL" \
  --revision "$(git -C "$M2" rev-parse HEAD)" \
  --receipt "evidence/receipts/$GATE/9000000001-1.json" \
  --candidate "$CANDIDATE_SHA" --plan "$PLAN_REVISION" 2>&1); RC=$?
expect_reject "NEG-2 missing run id" "$RC" "$OUT" 'run or resource not found'

# ---------------------------------------------------------------------------
# NEG-3 — edited fixture / edited history (retained-Pfad)
# ---------------------------------------------------------------------------
#> 3a "edited history": auf dem echten approved Stand ein ZWEITER Receipt-Edit
#>     (approved.at geändert) in eigenem Commit. Erwartung rc=1
#>     'receipt must have exactly one approval edit and no later edits'
#>     (alternativ 'approval commit mismatch', je nach Edit-Punkt).
M3A=$(mirror neg3a)
canon_edit "$M3A/$RECEIPT_PATH" 'value["approved"]["at"] = "2026-01-01T00:00:00Z"'
git -C "$M3A" add -A && git -C "$M3A" commit -qm "neg3a: post-approval receipt edit (controlled, throwaway mirror)"
OUT=$(python3 "$VERIFIER" retained --planning "$M3A" \
  --revision "$(git -C "$M3A" rev-parse HEAD)" --receipt "$RECEIPT_PATH" \
  --candidate "$CANDIDATE_SHA" --plan "$PLAN_REVISION" 2>&1); RC=$?
expect_reject "NEG-3a edited receipt history" "$RC" "$OUT" \
  'receipt must have exactly one approval edit and no later edits' 'approval commit mismatch'

#> 3b "edited fixture": der Introduction-Commit wird byte-seitig verfremdet (amend,
#>     eine Leerzeile/Space zusaetzlich — Blob != kanonische Unapproved-Bytes) und die
#>     approved-Zeile im echten approved-Stand auf diesen verfremdeten Commit gezeigt.
#>     Erwartung rc=1 'original receipt was edited' (retained():325); bei anderer
#>     Historie-Setzung alternativ 'receipt commit must introduce a new path' (:328).
M3B=$(mirror neg3b)
git -C "$M3B" checkout -q "$INTRODUCTION_COMMIT"
printf ' ' >> "$M3B/$RECEIPT_PATH"
git -C "$M3B" commit -qam "neg3b: byte-edited introduction fixture (controlled, throwaway mirror)"
FAKE_ORIGINAL=$(git -C "$M3B" rev-parse HEAD)
git -C "$M3B" checkout -q "$PLAN_REVISION"
canon_edit "$M3B/$RECEIPT_PATH" "value['approved']['receipt_commit'] = '$FAKE_ORIGINAL'"
git -C "$M3B" add -A && git -C "$M3B" commit -qm "neg3b: approval bound to edited introduction (controlled fixture)"
OUT=$(python3 "$VERIFIER" retained --planning "$M3B" \
  --revision "$(git -C "$M3B" rev-parse HEAD)" --receipt "$RECEIPT_PATH" \
  --candidate "$CANDIDATE_SHA" --plan "$PLAN_REVISION" 2>&1); RC=$?
expect_reject "NEG-3b edited fixture" "$RC" "$OUT" \
  'original receipt was edited' 'receipt commit must introduce a new path'

# ---------------------------------------------------------------------------
# Abschluss-Kontrolle: echte Evidenz unveraendert
# ---------------------------------------------------------------------------
if [[ -n "$(git -C "$PLANNING_LOCAL" status --porcelain)" ]] || \
   [[ "$(git -C "$PLANNING_LOCAL" rev-parse HEAD)" != "$EXPECTED_PLANNING_HEAD" ]]; then
  echo "STOP: Planning-Stamm wurde angefasst/verschoben — Negative verletzen die Grenze"; exit 1
fi
echo "NEG DONE: alle drei Negative produktion-pfadig belegt; Original-Evidenz unveraendert"
