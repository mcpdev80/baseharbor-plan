# Review mission m_rev_1620e8b

## PLAN

1. Read the mission, verify its authority, scope, acceptance contract, and required evidence location.
2. Refresh Planning ownership/task state and verify the exact GitHub remote, candidate, base, and provenance.
3. Inspect the candidate diff and exact-head hosted checks against each acceptance requirement.
4. Perform only the mission-authorized review or merge action; preserve unrelated work and record evidence.
5. Publish evidence in baseharbor-plan, verify origin/main and remote state, update the live board, and post the required handoff.

## Role and verdict

ROLLE: REVIEW, danach MERGE versucht unter der expliziten Owner-Autorisierung vom 2026-11-23 („finish AND merge“). REVIEW: APPROVE für den geprüften Code und den Neutralitätstest. MERGE: BLOCKED durch den aktiven strikten GitHub-Required-Status-Check. Kein Bypass und keine Produktänderung vorgenommen.

## Contract and authority

Task: `t-20261114-r28-cli2-wizard-platform` (0428-067), PR #1620. Der Task-Status war `blocked`; sein dokumentierter nächster Trigger war die Catalog-Ingress-Karte für `cmd/baha/app_access.go` und `cmd/baha/app_access_test.go`, dann ein Hop und ein exakter Lauf. Die Ingress-Karte `t-20261123-catalog-ingress-app-access` ist `closed` und nennt Merge-SHA `15c652136b0fce19dd0ae286b341b38cac3f7854`. Der geprüfte PR-Lauf verwendet Base `e8acf740553f7218b259f4855f5b79f83f21ab6b`, die nachweislich Nachfolger dieser Catalog-Ingress-Änderung ist.

Die Planung-Tasknote und die Owner-Mission `/tmp/opencode/m_rev_1620e8b.md.g` wurden gelesen. Die Mission autorisiert die Prüfung und den normalen Squash-Merge nur, wenn der Kandidat neutral gegenüber der nachfolgenden develop-Änderung ist. Workflow-Dateien blieben unangetastet. Keine lokalen Produkt-Tests, Workflow-Reruns, VM-Tests oder Container wurden gestartet.

## Candidate and base neutrality

Remote `lane-origin` wurde anhand der URL `https://github.com/mcpdev80/baseharbor.git` als GitHub-Remote identifiziert. Frische Remote-Witnesses vor und nach dem Mergeversuch:

```text
1b7598aef8c4cae33b77c8523872637090d0f2bf refs/heads/develop
ad5859916d54bfb218a4c04f1cd41de44df0bb62 refs/heads/w067-cli2-wizard-platform
ad5859916d54bfb218a4c04f1cd41de44df0bb62 refs/pull/1620/head
```

PR head ist unverändert `ad5859916d54bfb218a4c04f1cd41de44df0bb62`; aktuelle Base ist `1b7598aef8c4cae33b77c8523872637090d0f2bf`. GitHub Compare `e8acf...1b759` meldet genau einen Base-Commit, `1b7598aef8c4cae33b77c8523872637090d0f2bf`, „fix(0428-227): admit canonical footprint show on data-capabilities gate“, mit diesen fünf Dateien: `cmd/baha/app_broker.go`, `cmd/baha/ci_integration_operator_enabled.go`, `cmd/baha/ci_integration_operator_enabled_test.go`, `internal/operatorauth/local_runtime.go`, `internal/operatorauth/local_runtime_test.go`. Es gibt keine Catalog-Datei oder Trusted Plan Datei im Base-seitigen Diff.

GitHub Compare `1b759...ad585` meldet 10 Kandidaten-Commits, 1 Commit Rückstand und nur zwei Dateien im PR-Diff: `cmd/baha/app_access.go` (+40/-0) und `cmd/baha/app_access_test.go` (+165/-1). `scripts/pr-gate-coverage.json` ist nicht Teil des Kandidaten-Diffs. Die Einträge für beide `app_access`-Pfade sind bereits in den Catalog-Inhalten an `e8acf` und `1b759` vorhanden, mit den beiden atomic data-capabilities-Surfaces; der Testeintrag hat `runtime_specific: true`. Der Catalog-Delta ist leer.

Neutralität: bestanden. #1753 fügt die Operation `app.footprint.show` in `internal/operatorauth/local_runtime.go` hinzu und bearbeitet nicht `app_access.go`, `app_access_test.go`, oder den Catalog. #1620 schreibt ein Audit-Event für `app.connection` nach erfolgreicher Autorisierung und vor der Credential-Ausgabe. Diese Operation und der Footprint-Show-Pfad haben weder Datei- noch Gate-/Catalog-Konflikt; die base-seitige Änderung widerspricht nicht dem Access-Reveal-Verhalten. Der exakte PR-Lauf basiert zudem auf `e8acf`, dessen Catalog-Vorgänger `15c652` bereits den Ingress für beide Pfade enthält.

## Exact-head checks and execution sample

Run `45099073208` ist für den exakten head `ad5859916d54bfb218a4c04f1cd41de44df0bb62` ein Pull-Request-Run, `completed/success`, attempt 1. Check `PR Selected Checks` (job `137452731937`, GitHub Actions integration `15368`) ist `completed/success`; dessen Terminal-Logzeile lautet `2026-11-23T02:38:35.5979705Z PR Selected Checks: PASS`. Das Log zeigt `trusted_base_sha` `e8acf740553f7218b259f4855f5b79f83f21ab6b` und die ausgewählten Runtime-Ziele `atomic/docker/data-capabilities` sowie `atomic/podman/data-capabilities`.

Beide erforderlichen Runtime-Jobs liefen tatsächlich und waren erfolgreich: Docker job `137445999430` und Podman job `137445999443`, jeweils `completed/success`. Die Logs enthalten jeweils die Zeile `demo-data-capabilities       PASS`. Der Go-Unit-Job `PR · Go unit · cli-0` (`137445560998`) meldet `PASS cli-0: 468 passed / 13 intentionally skipped / 481 discovered; CLI inventory total=1865`. Der sharder am geprüften Kandidaten selektiert `TestAppCredsRevealWritesPerRevealAuditEvent` in `cli-0` (SHA-256-Modulo-4-Regel); `TestAppCredsRevealFailsClosedWhenAuditWriteFails` fällt in `cli-3`, dessen Job `137445560919` meldet `PASS cli-3: 434 passed / 16 intentionally skipped / 450 discovered; CLI inventory total=1865`. Der Sharder prüft für jeden ausgewählten Test, dass er ausgeführt wurde und passierte oder absichtlich übersprungen wurde; beide kartenspezifischen Tests sind nicht als Skip markiert. Die native Docker/Podman-Ausführung für data-capabilities ist in den beiden oben genannten Jobs belegt.

Die PR Selected Checks-Auswahl ist grün, einschließlich der Trusted-Plan-Auswahl und beider Native data-capabilities Runtime-Jobs. Andere nicht erforderliche oder nicht betroffene Jobs in diesem Run sind `skipped`; sie werden nicht als Erfolg gezählt.

## Merge attempt and required next action

Ruleset `25223521` `develop - required checks` wurde live gelesen: `active`, `strict_required_status_checks_policy: true`, verlangt `PR Selected Checks` von integration `15368`, ohne Bypass actor. Ruleset `23754541` `develop - integration branch` ist `disabled`. PR #1620 blieb `open`, `draft: false`, `mergeable: true`, `mergeable_state: behind`, Base `e8acf...`, head `ad585...`.

Der normale Squash-Merge wurde mit expected-head guard `ad5859916d54bfb218a4c04f1cd41de44df0bb62` versucht. GitHub lehnte den Merge mit HTTP 405 ab: `Repository rule violations found — Required status check "PR Selected Checks" is expected.` Es wurde kein Bypass verwendet. Der PR ist danach weiterhin offen und nicht gemerged. Damit ist der Code-Review-Verdict approve, aber der Merge durch den aktiven Required-Status-Check blockiert; der grüne alte-base Check kann die aktuelle Strict-Base-Bedingung nicht erfüllen.

Nächste Aktion: #1620 einmal monoton auf den aktuellen `develop`-Head `1b7598aef8c4cae33b77c8523872637090d0f2bf` hoppen, den PR-Selected-Checks-Lauf am neuen exakten Head bis zum terminalen Zustand beobachten und nur bei tatsächlich grünem erforderlichem Check normal squash-merken. Den bestehenden Kandidatenbranch weiterverwenden; keine Workflow-Datei ändern und keinen Bypass einsetzen.

## Repo-rule compliance

Nur der hier angegebene Evidence-Entwurf wurde erstellt. Produktdateien, `.github/**`, Task-Metadaten und generierte Planungsaussichten wurden von dieser Review-Session nicht geändert. Keine Subagenten, keine lokalen Produkt-Tests, keine Workflow-Reruns und keine Container wurden gestartet. Die einzige PR-Mutation war der normale Squash-Mergeversuch mit expected-head-Schutz; GitHub lehnte ihn ab und Remote-PR-Head sowie develop blieben unverändert.

## cleanliness

Vor Review: `docker ps -a` (PID 3446891) zeigte nur die Header-Zeile `CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES` und keine Container. Nach dem Mergeversuch: `docker ps -a` (PID 3506035) zeigte dieselbe Header-Zeile und keine Container.

## END

END_BLOCKED codex-rev2-1736: REVIEW APPROVE, Merge durch aktiven strikten PR Selected Checks-Status blockiert; final-hop auf develop `1b7598aef8c4cae33b77c8523872637090d0f2bf` erforderlich, Kandidat `ad5859916d54bfb218a4c04f1cd41de44df0bb62`.
