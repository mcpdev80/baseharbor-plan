# w364-0428-321-1866rerun — coordinator-documented observation record (2026-11-27)

Mission: fresh Hosted attempt on exact head 3702c09502203e82633d664690eac9484a370df9 consuming repo pin 1a3c055cc0eef3f961722f12d843e33f6c1ca43e.
Observed (API): run 45916731635 executed with genuine 1a3 demo source; BOTH Docker + rootless-Podman data-capabilities gates FAILED again.
Root cause (owner-confirmed, w357 bootstrap findings refined): tests/guided/drive.py does not capture the nested consent refusal + digest (hash=False/prompt=False, no second up) - DEMO TEST-DRIVER defect, not product code of card 0428-321. Consent semantics must NOT be weakened.
Disposition: no further retries on this head; card 0428-321 blocked pending the owner-authorized separate Demo test-driver PR (nested-refusal parser + explicit digest retry) landing and a subsequent pin advance. Lane released after END.
