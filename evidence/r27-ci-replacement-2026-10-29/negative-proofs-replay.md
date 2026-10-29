# t-20261029-r27-ci-producer — Negative Replay (Band)

## Proof: Negative Proofs Replay at Current Pin

**Task:** t-20261029-r27-ci-producer (Nachweis-Band)
**Date:** 2026-10-29
**Pin context:** vars.BASEHARBOR_RECEIPT_TRUSTED_SOURCE = 46ed3e8c9bab1a3fb9db9f6bc04f77ad8b69f735 (main-Tip); negatives replayed at current pin 0b0659f2 context.

### Planning SHA verification

- **Planning SHA vorher:** `45cb7cd169a6340ddec0b3485b71c4e8bc76aa12` (origin/main HEAD)
- **Planning SHA nachher:** `45cb7cd169a6340ddec0b3485b71c4e8bc76aa12` (origin/main HEAD)
- **Ergebnis:** vorher == nachher — planning-HEAD unverändert

### ls-remote Zeuge

```
$ git ls-remote https://github.com/mcpdev80/baseharbor-plan HEAD
45cb7cd169a6340ddec0b3485b71c4e8bc76aa12	HEAD
```

### Case 1: wrong candidate sha (expected: blocked)

```
$ PIN_MAIN=45cb7cd169a6340ddec0b3485b71c4e8bc76aa12 CANDIDATE=57a9c4a78b7652fc26025b3e448581222ebb815e RUN_ID=40921493079 PLAN=eef674d0b7d9214724417b215495d500cc1c24b2 bash evidence/board-2026-10-29/scripts/negative-proofs.sh
```

- **Ausführung:** `python3 "$SCRIPTS_DIR/receipt_verifier.py" retained --planning "$PLAN_DIR" --revision "$PIN_MAIN" --receipt "$RECEIPT" --candidate "$WRONG_CANDIDATE" --plan "$PLAN"`
- **exit-Code:** 2 (non-zero, blocked)
- **Ergebnis:** PASS (exit 2)
- **Zeitstempel:** 2026-10-29T23:47:09Z

### Case 2: wrong plan revision that never holds the receipt (expected: blocked)

```
$ PIN_MAIN=45cb7cd169a6340ddec0b3485b71c4e8bc76aa12 CANDIDATE=57a9c4a78b7652fc26025b3e448581222ebb815e RUN_ID=40921493079 PLAN=eef674d0b7d9214724417b215495d500cc1c24b2 bash evidence/board-2026-10-29/scripts/negative-proofs.sh
```

- **Ausführung:** `python3 "$SCRIPTS_DIR/receipt_verifier.py" retained --planning "$PLAN_DIR" --revision "$PIN_MAIN" --receipt "$RECEIPT" --candidate "$CANDIDATE" --plan "$BAD_REV"`
- **exit-Code:** 2 (non-zero, blocked)
- **Ergebnis:** PASS (exit 2)
- **Zeitstempel:** 2026-10-29T23:47:09Z

### Case 3: edited approval object (expected: blocked)

```
$ PIN_MAIN=45cb7cd169a6340ddec0b3485b71c4e8bc76aa12 CANDIDATE=57a9c4a78b7652fc26025b3e448581222ebb815e RUN_ID=40921493079 PLAN=eef674d0b7d9214724417b215495d500cc1c24b2 bash evidence/board-2026-10-29/scripts/negative-proofs.sh
```

- **Ausführung:** `python3 "$SCRIPTS_DIR/receipt_verifier.py" retained --planning "$EDITED_DIR" --revision "$EDIT_HEAD" --receipt "$SYNTH_RECEIPT" --candidate "$CANDIDATE" --plan "$P1"`
- **exit-Code:** 2 (non-zero, blocked)
- **Ergebnis:** PASS (exit 2)
- **Zeitstempel:** 2026-10-29T23:47:09Z

### Summary

Alle 3 Negative-Fälle (fail-closed) verhalten sich wie erwartet:
- **Case 1:** wrong candidate → exit 2 (blocked) ✓
- **Case 2:** wrong plan revision → exit 2 (blocked) ✓
- **Case 3:** edited approval object → exit 2 (blocked) ✓

Keine Approval-Chain nochmal approvaln (läuft über #1207 Zyklus).
Kein git push in baseharbor-plan, kein Merge, keine Approval-Dispatches.
Planning-HEAD vorher == nachher (45cb7cd169a6340ddec0b3485b71c4e8bc76aa12).

END q239-DONE
