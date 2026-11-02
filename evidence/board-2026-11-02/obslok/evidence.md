# obslok — Loki-Log-Ingestion Verifikation scheitert auf GH-hosted

## PLAN

- [ ] 1) Volle Fehlerzeile + vorangehende Zeilen aus Run-Log 41397537623, Job app_observability_acceptance_test.go:165 ziehen (gh api job logs)
- [ ] 2) Ursache triagieren: Loki-Startbereitschaft (Grace/healthcheck #1265), Query-Zeitfenster/Sortierung, oder Ingestion-Pat echt kap
- [ ] 3) Minimaler Fix + Regression; PR gegen develop; Observability-Dispatch auf PR-Branch beobachten
- [ ] 4) END_BLOCKED nach 90 Min Diagnose wenn keine eindeutige file:line-Ursache; statt Weiterbohren

## STATUS

- [ ] 1) Volle Fehlerzeile + vorangehende Zeilen aus Run-Log 41397537623, Job app_observability_acceptance_test.go:165 ziehen (gh api job logs)
- [ ] 2) Ursache triagieren: Loki-Startbereitschaft (Grace/healthcheck #1265), Query-Zeitfenster/Sortierung, oder Ingestion-Pat echt kap
- [ ] 3) Minimaler Fix + Regression; PR gegen develop; Observability-Dispatch auf PR-Branch beobachten
- [ ] 4) END_BLOCKED nach 90 Min Diagnose wenn keine eindeutige file:line-Ursache; statt Weiterbohren

## END

END_BLOCKED obslok: pr= head= run=41397537623 | 90 min elapsed, keine file:line-Ursache identifiziert — END_BLOCKED mit file:line statt Weiterbohren
