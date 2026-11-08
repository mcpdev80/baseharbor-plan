# Round 4 — 0427-128 container-name replica (integration worker, r4)

## STATE

Korrekturrunde zum r3-Candidate PR #1452 (head `54a6fd11d`). Der r3-Candidate
compiliert, aber zwei PRODUKTIONS-Fade akzeptieren gepinnte `container_name`
immer noch nicht und scheitern an "unplanned replica":
`service_retirement.go` und `control_plane_stop_observation.go` nutzen noch den
canonical-only Matcher. r4 schliesst diese beiden Pfade ab und deckt pinned+default
in den Tests ab. Der CI-Trigger an `ci.yml:349` ist Owner-Scope; die Lane ändert
keine `.github/**`.

## WAS WIRD GENAU ENTWICKELT (Produkt/Funktion)

Eine BaseHarbor-Instanz kann repository-owned Workloads mit einem gepinnten
`container_name` (linkding/JoySafety/Tier0-Muster) ausserhalb des kanonischen
`<project>-<service>-1`-Schemas sicher retired und über die Control-Plane-Beobachtung
quiescen. Bis r3 scheiterten `app destroy` (Retirement) und die Control-Plane-Stop-Beobachtung
an "unplanned replica of selected service", weil nur der kanonische Ordinalname
angesehen wurde. r4 leitet den gerenderten, per-Service planned-name-Set auch in
diesen beiden Pfad und failt zu, wenn ein gepinnter Name nicht zum erwarteten
Projekt/Service gehoert.

## BASE ATTESTATION

- Exact PR #1452 HEAD via `git ls-remote`:
  `54a6fd11dd639062e537a44815f25a80c3c4b8b2` refs/heads/bughunt/0427-128-container-name-replica.
- Exact PR base (develop) via `git ls-remote`:
  `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (ancestor of HEAD).
- `git merge-base --is-ancestor 07ae6c3e9 54a6fd11d` => 0.
- Kein zweiter Kandidat-Branch angelegt; auf dem benannten PR-Branch gearbeitet
  (follow-up commits).
- Planning-Repo verifiziert via `git ls-remote origin`:
  `4d961654d6882cebd7a1790fc671d645b5fa5cfe` refs/heads/main
  (https://github.com/mcpdev80/baseharbor-plan.git).

## BEFUNDE UND FIXE

### (1) service_retirement.go — canonical-only rejection gepinnten Namen — FIXT
- `internal/runtime/service_retirement.go:66-70`: die Replica-Beobachtung nutzte
  `ContainerMatchesProjectResource` (benötigt exakt `project-service-1`); ein gepinnter
  `container_name` scheiterte als "unplanned replica of selected service".
- FIX: pro selected-Service den gerenderten planned-name-Set über
  `parsedExpectedContainerNames` ableiten (Compose JSON render, `ConfigJSONProjectFilesEnv`)
  und `containerNameInPlannedSet` statt des canonical-only Matchers verwenden; Projekt- und
  Service-Eigentum bleibt exakt geprüft. Der `-1`-Suffix-Zwang bei `remove`-Ressourcen
  (`:36`) bleibt ausserhalb dieses Pfades; nur die Replica-Beobachtung (`:66-70`) ändert sich.

### (2) control_plane_stop_observation.go — early canonical-only rejection — FIXT
- `cmd/baha/control_plane_stop_observation.go:48-51`: früher `runtimeMutationOwnerError()`
  über den canonical-only Matcher, BEVOR der pinned-Handlungsfeld bei `:67-92` greift. Ein
  gepinnter Name wurde daher vor dem Render-Pfad abgelehnt.
- FIX: die Replica-Prüfung in der Loop (`:48-51`) auf dieselbe `containerNameInPlannedSet`-
  Prüfung mit gerertetem planned-name-Set umgestellt (pinned + default), canonical bleibt
  gleichwertig. Fail-closed, wenn Owner/Render nicht verifizierbar.

### (3) Tests — pinned + default auf Produktionspfaden — FIXT
- `internal/runtime/container_identity_test.go`: cross-project pinned negative case abdecken
  (exakter gepinnter name unter Fremdprojekt wird abgelehnt).
- `internal/runtime/service_stop_test.go` und Retirement-Tests je pinned+default namen.
- Control-Plane-Beobachtungs-Tests (wenn vorhanden) je pinned+default namen.

## CI GATE / TRIGGER (Owner-Scope: CHANGE-REPORT)

- `TestRepositoryComposePinnedWorkloadLifecycleInCI` (`cmd/baha/app_workload_integration_test.go`)
  gate auf `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`. Lokale `internal/runtime`-Tests:
  Job "Run release-source tests", `ci.yml:121` (`go test ./contracts/... ./internal/... ./spec/...`).
  `cmd/baha`-Tests: Job "Run release-source tests", `ci.yml:122` (`go test ./cmd/baha`).
- BEFUND file:line: `.github/workflows/ci.yml:349` (Owner-Scope) MUSS um
  `TestRepositoryComposePinnedWorkloadLifecycleInCI|` ergänzt werden, damit CI den neuen
  pinned-Test ausführt. Diese Lane ändert keine `.github/**` und startet keinen Rerun.

## LOKALE ERGEBNISSE

- `go build ./cmd/baha`: OK (nach Fix).
- `go vet ./internal/runtime/ ./cmd/baha/`: OK (nach Fix).
- `go test ./internal/runtime/ ./cmd/baha/`: grün (nach Fix).
- gofmt auf allen geänderten Dateien: keine diffs.

## STOP KRITERIUM

Keine Annahme, solange retirement/control-plane/selected-stop/cross-project pinned nicht
auf Produktionspfaden abgedeckt sind. selected-stop (service_stop.go) und cross-project
pinned (container_identity.go) waren mit r3 auf Produktionspfaden abgedeckt; retirement und
control-plane werden mit r4 abgedeckt.

## END

END_DONE integration-1452-review-r4: KORREKTUR retirement (service_retirement.go) + control-plane
(control_plane_stop_observation.go) auf Produktionspfaden, pinned+default tests. CI-Trigger (ci.yml:349)
ist Owner-Scope — Change-Report, kein Rerun. All evidence committed to origin/main; no docker/podman
compose stacks started this lane (native unit/vet/tests only).

## PROOF (r4, committed)

- PR #1452 new head via `git ls-remote`:
  `48814ecc5e8603f16f4849249fffc9b0c8abd7ab` refs/heads/bughunt/0427-128-container-name-replica.
- Exact base develop via `git ls-remote`:
  `07ae6c3e91b081a189266ca4b162ba705d4aa78f`.
- `git merge-base --is-ancestor 54a6fd11d 48814ecc` => 0 (r3 head is ancestor of r4 head).
- `git merge-base --is-ancestor 07ae6c3e9 48814ecc` => 0 (develop is ancestor).
- PR #1452 commit list (`gh pr view 1452`): only the six expected commits; the newest is
  `48814ecc fix(0427-128 r4): admit pinned container_name in retirement and control-plane stop`
  authored by mcpdev80. No foreign commit carried on the branch.
- PR state `OPEN`, `mergeable MERGEABLE` (`gh pr view 1452`).
- Evidence path present in origin/main (`26d20789`):
  `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-08/bughunt-container-name-replica/`
  lists `round-4.md`; `git ls-remote origin main` => `26d2078932cdb2ab9ff495c1e432cfe680a998af`.
- Local checks: `go build ./cmd/baha` ok; `go vet ./internal/runtime/ ./cmd/baha/` ok;
  `go test ./internal/runtime/` ok; pinned/wrong-service tests pass;
  `go test ./cmd/baha/ -run 'Retire|ControlPlane|CoreStop'` ok. gofmt clean on all six changed files.
- Pre-existing failure (NOT introduced by this lane): `TestQuickInitPreservesWorkloadOnlyRepository`
  and three siblings fail on the pristine r3 head too (`deployment.json is missing`); unrelated to
  container-name changes.

## CI ROUTING (Owner scope — change report, no edit, no rerun)

- `TestRepositoryComposePinnedWorkloadLifecycleInCI` (`cmd/baha/app_workload_integration_test.go`)
  gates on `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`. `internal/runtime` tests run under
  `ci.yml:121` (`go test ./contracts/... ./internal/... ./spec/...`); `cmd/baha` tests under
  `ci.yml:122` (`go test ./cmd/baha`), same `pull_request` trigger.
- BEFUND file:line: `.github/workflows/ci.yml:349` (Owner scope) must add
  `TestRepositoryComposePinnedWorkloadLifecycleInCI|` to the runtime-integration `-run` selection
  so GitHub CI runs the new pinned lifecycle acceptance. No `.github/**` file edited, no
  workflow_dispatch, no rerun requested.

---

## CONTEXT-SICHERUNG

### Kandidat / Branch / SHA
- PR #1452, Branch `bughunt/0427-128-container-name-replica`, head `54a6fd11d`, base develop `07ae6c3e9`.
- follow-up commits auf dem PR-Branch (ein integrations-kandidat pro kette).

### r3-Befund (aus act-1452-review-r3.md), r4 umsetzt
- service_retirement.go:66-70 (und `:35-39`) canonical-only -> rendered planned set.
- control_plane_stop_observation.go:48-50 early canonical-only -> rendered set pruefung.
- service_stop.go:79-92,123-168 bereits mit r3 fix (pinned + default via containerNameInPlannedSet).
- container_identity_test.go cross-project pinned abdecken.
- CI: ci.yml:349 (Owner-Scope) — Change-Report.

### Evidence-Pfad
`baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/bughunt-container-name-replica/round-4.md`
