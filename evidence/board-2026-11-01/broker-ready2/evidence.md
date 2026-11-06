# Evidence: broker-ready2 — Runtime-Broker readiness fix

## PLAN

  - Step 1: Locate: compose/Startpfad des runtime-broker in scripts/ + internal/providers/ (grep /readyz, healthcheck, EXPOSE, Startcommand)
  - Step 2: Minimal-Fix: start_period der Healthcheck-Konfiguration von 2s auf 30s erhöhen — gibt OpenBao und Broker genug Zeit zur Initialisierung vor dem ersten Healthcheck-Attempt
  - Step 3: Lokaler Beweislauf: broker starten, /readyz messen (Vorher/Nachher in Evidence)
  - Step 4: PR gegen develop 'fix(runtime-broker): make readiness reachable', PRSC terminal beobachten
  - Step 5: Karte via plan.py new, Claim, Merge und Planning-Update

## Lane Status

END_DONE broker-ready2: <pending>
