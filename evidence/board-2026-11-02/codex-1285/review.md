# PR #1285 — unabhängiges Codex-Review

ROLLE: REVIEW
Urteil: REJECT
Zeit: 2026-11-02T13:04:31Z
Reviewer: OpenAI Codex, unabhängige Session; Session-ID und genaue Modellkennung hier nicht verfügbar, kein Horde-Task zugewiesen.
Kandidat: 7489eecda856d2f0171653610a657a79ff71d6c7; develop: 9a93865a935624045e96a503da0a3a1c2f7d1559. `git ls-remote` bestätigte beide SHAs vor und nach Review. Vollständigen PR-Diff und Worker-Evidence rcptverfix/evidence.md gelesen; nur receipt_verifier.py und drei zugehörige Testdateien geändert.

## Blockierende Befunde und Rezept

1. Der Worker-Vertrag in rcptverfix/evidence.md fordert, dass ein nicht erforderlicher, dennoch ausgeführter und fehlgeschlagener Job blockiert. Der neue Code ignoriert solche Fehler ausdrücklich; `test_not_required_optional_failure_is_accepted` prüft das Gegenteil. Worker: Vertrag exakt umsetzen und eine Regression für optional-skipped versus optional-executed-failure ergänzen; keine fehlgeschlagenen ausgeführten Jobs grün rechnen.
2. Die behauptete Ableitung aus dem Trusted Plan ist unvollständig: `required_validation_checks` wird nicht geprüft; native Gates werden mit `"native" in g or "lifecycle" in g` erkannt, während der maßgebliche `scripts/pr-authenticated-results.py` die Präfixe `atomic/docker/`, `atomic/podman/`, `integration/docker/`, `integration/podman/` verwendet und zusätzlich Consumer-/Demo-Pins nach Abhängigkeiten fordert. Ein ausgewähltes `integration/docker/...` kann so Exact Candidate und Runner Interface umgehen; erforderliche Validierungsjobs und Consumer-Pins fehlen ebenfalls. Worker: dieselbe autoritative vollständige Gate- und Dependency-Ableitung verwenden, eindeutige Jobs prüfen und Regressionen für native Auswahl, fehlgeschlagene/fehlende Validierung sowie Consumer-/Demo-Dependencies hinzufügen.
3. `by_name = { ... }` überschreibt doppelte Jobnamen, obwohl die Fehlermeldung Mehrdeutigkeit zu blockieren behauptet; ein fehlgeschlagener erforderlicher Job kann durch einen gleichnamigen erfolgreichen verdeckt werden. Worker: pro erforderlichem Namen genau einen Job verlangen und beide Job-Reihenfolgen mit Duplikaten testen.

Nach Korrektur fokussierte Receipt-Tests und die tatsächlich erforderlichen CI-Gates für den neuen SHA nachweisen und erneutes unabhängiges Review einholen. GitHub meldet Kandidat BEHIND; vor Merge aktuelle Integration und strict required checks erneut qualifizieren. Bei unzureichender belegter Gate-Abdeckung stoppen.

## Weitere Evidenz

GitHub Actions Run 41447936075: PR Selected Checks SUCCESS für den Kandidaten, Job 125286728686, App 15368; Focused Python, receipt-execution-tests, pr-planner-tests, ci-executor-verifier-tests und ci-policy SUCCESS. Review-Threads leer. Grüne Tests widerlegen obige Vertragsverletzungen nicht. Kein Merge durchgeführt; develop blieb auf dem oben genannten SHA. Der behauptete pre-existing Planning-Testfehler wurde für dieses Urteil nicht unabhängig verifiziert.
