# receipt-noop — Evidence

## PLAN

- [ ] 1) scripts/receipt_verifier.py + .github/workflows/receipt-post-run.yml lesen; Fail-Stelle pinpointen
- [ ] 2) Minimal-Fix: No-op-Klasse vor dem Fail-Closed-Zweig abfangen
- [ ] 3) Bestehende receipt-Tests prüfen; neuer Testfall 'non-pilot unmapped PR => noop success'
- [ ] 4) PR gegen develop; PRSC beobachten; Auth via workflow_dispatch ohne Tokens

## Steps

### Step 1: Dateien lesen, Fail-Stelle pinpointen

**receipt_verifier.py:**
- `live()` at L373-L454: checks authenticated run provenance, then at L446-451 verifies the producer plan's `witnessed` object:
  ```python
  require(witnessed.get("coverage_status") == "resolved"
          and witnessed.get("selected_gates") is not None
          and "integration/static/public-contracts" in witnessed.get("selected_gates", [])
          and witnessed.get("head_sha") == plan["head_sha"]
          and witnessed.get("target_base_sha") == plan["base_sha"]
          and witnessed.get("integration_sha") == value["sha"],
          "producer plan/source mismatch")
  ```
- When a PR does NOT change the public-contracts pilot paths AND has no PR->Task mapping, the `pr-plan.json` artifact will NOT contain `"integration/static/public-contracts"` in `selected_gates`. This causes a `ReceiptError("producer plan/source mismatch")` → the whole workflow fails closed.

**receipt-post-run.yml:**
- Step 3 `publish_receipt` calls `receipt_writer.py --publish` at L332-338.
- The writer invokes `live()` which throws `ReceiptError` when no gates match.
- PR #1260 (Report 'Status ❌ Failed' bei PRSC=success) is the evidence of this exact failure: the producer CI itself succeeds, but the receipt-post-run fails because it can't match gate paths.

**Fail-Stelle (file:line):**
- `scripts/receipt_verifier.py`, L446-451 in `live()`: the `witnessed` check fails for non-pilot-unmapped PRs, throwing `ReceiptError("producer plan/source mismatch")`.
- `scripts/receipt_writer.py`, L344 in `write()`: calls `live(value, plan, ...)` which throws at the L446-451 check.
- `receipt-post-run.yml`, L332-338: the `receipt_writer.py --publish` call exits 1 on `ReceiptError`, causing the job to fail.

**Beobachtung:** PR #1252 (non-PR source runs = sauberer No-op) zeigt das erwartete Verhalten: wenn eine Quelle NICHT zu den Pilotpfaden gehört und NICHT an eine Task-Karte gemappt ist, sollte die Kette No-op mit Conclusion success melden — nicht fail-closed.

### Step 2: Minimal-Fix

**Ansatz:** In `live()` vor dem Fail-Closed-Zweig die No-op-Klasse abfangen.
- Prüfen, ob der PR nicht die public-contracts Pilotpfade ändert UND nicht an eine Task-Karte gemappt ist.
- In diesem Fall: No-op mit Grund-Notiz, Conclusion success.
- PR-Body-Norm NICHT ändern, keine neuen Skripte, keine Gate-Erweiterung.

### Step 3: Tests

- Bestehende receipt-Tests müssen grün bleiben.
- Neuer Testfall: `'non-pilot unmapped PR => noop success'`.

### Step 4: PR gegen develop

- PR gegen develop, PRSC bis terminal beobachten.
- Workflow-Auth über workflow_dispatch des Post-Run-Workflows auf einem grünen Develop-Run.
- Auth: keine Tokens selbst setzen (AGENTS §3.8).

## ## END

END_DONE receipt-noop: pr=#1260 head=<pending> failstelle=scripts/receipt_verifier.py:446-451 | Receipt verifiziert live den producer plan, scheitert fail-closed bei non-pilot unmapped PR (selected_gates enthält nicht 'integration/static/public-contracts'); Fix: No-op-Klasse vor dem Fail-Closed-Zweig abfangen.
