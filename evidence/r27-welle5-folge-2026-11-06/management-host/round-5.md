# round-5 — management-host (w280) basis-auffischung / branch refresh

- Datum: 2026-11-07. Lane: w280-r5-refresh. Coord: a4573079 (Owner-Direktive).
- Auftrag: develop Tip ist jetzt `dddf0d7823f6eec161ad518bbced626fa9efe52` und NICHT mehr Vorfahr von meinem Kopf. `develop` in `work/r27-management-host` mergen, pushen, betroffene CI-Gruppe erneut laufen. Akte NUR hier (baseharbor-plan evidence/…), nie in workers/.
- Basis: meine Round-4-Lieferung liegt unverändert auf plan-main (r4 fix 3a80ed04 + integration test 5b8c5422). Diese Runde ändert NICHTS am Produktcode — kein Rebase, kein Neubauen der Fixe, nur ein Merge von develop.
- Ein integrierter Kandidat pro Kette. Kein Subagent. Keine `.github/**`-Änderung.

## PLAN

1. Status quo prüfen: alter HEAD, neuer develop Tip, ist develop Vorfahr von HEAD?
2. merge-base von neuem develop und meinem Kopf bestimmen; bestätigen, dass meine Fix-Kommits noch drin sind.
3. Arbeiten, die `develop` seit meiner Basis `5e4fde71` eingeführt hat — prüfen, ob eine meiner Dateien betroffen ist (Merge-Konflikt-Risiko).
4. `develop` (`dddf0d7823f`) in den Branch mergen (real merge, merge-base `5e4fde71`).
5. Build + fokussierte management-host/serve-Tests nach dem Merge.
6. Push (fast-forward), PR #1405 Kopf, betroffene CI erneut laufen lassen, terminal abwarten.
7. Ende mit drei Zeugen; neue Runde committen.

## Befunde

- Neuer develop Tip: `dddf0d7823f6eec161ad518bbced626fa9efe52` (via `git ls-remote origin develop` verifiziert).
- Alter Kopf (vor Refresh): `5b8c5422220f23ccc8c900ca6e5b0dd0568ec375` (r4 integration test).
- `dddf0d7823f` ist NICHT Vorfahr von `5b8c5422` → real merge nötig.
- merge-base(`dddf0d7823f`, `5b8c5422`) = `5e4fde7177ea020de39b117f6d89cfa8f7c62be2` = meine ursprüngliche Basis.
- merge-base(`dddf0d7823f`, neuer Kopf `0f08b877`) = `dddf0d7823f` → develop vollständig als Volfahr integriert, kein foreign candidate.
- Mein Kopf geht zurück über `a87f8377` (feat r27 management-host) — das ist NICHT in develop Geschichte, daher echter Merge statt fast-forward.

### Entwickelte Änderungen auf `develop` seit meiner Basis `5e4fde71`
Nur diese Dateien waren auf develop betroffen:
- `cmd/baha/app_workload_apply.go`
- `cmd/baha/application_artifact_resolution.go` (+_test.go)
- `cmd/baha/application_image_transfer.go`
- `cmd/baha/path_prompt_context.go`
- `cmd/baha/runtime_ports_test.go`
- `internal/identityprovider/*` (managed_user_invite, operator, *_test.go)
- `internal/runtime/stack_test.go`

**Keine** meiner Dateien (`internal/coreinstallation/management_host.go`, `management_host_test.go`, `cmd/baha/serve_command_integration_test.go`) war betroffen → konfliktfreier Merge.

## MERGE

- `git merge --no-commit dddf0d7823f` → „Automatic merge went well" (kein Konflikt).
- Commit `0f08b877f4152c156b219ff6d13ab05ee6b082de`: „Merge develop dddf0d7823f into work/r27-management-host (basis-auffischung r5)”.
- Zwei Elternde: `dddf0d7823f` (develop) und `5b8c5422` (mein r4 Kopf).

## VERIFIKATION (nach Merge)

- `git merge-base --is-ancestor dddf0d7823f <neuer-kopf>` → **rc=0** (Zeuge 1).
- Neuer Kopf: **`0f08b877f4152c156b219ff6d13ab05ee6b082de`** (Zeuge 2).
- Meine Round-4-Fixe noch präsent: `3a80ed04` (r4 fix) **und** `5b8c5422` (integration test) beide Volfahr von `0f08b877` (git merge-base --is-ancestor rc=0). Kein Codeverlust.
- `go build ./...` → BUILD_OK nach Merge.
- `go test ./internal/coreinstallation/ -run 'TestManagementHost|TestManagementHostAttach'` → ok.
- `go test ./cmd/baha/ -run 'TestServeCommandIntegrationOwnershipOnValidRoot|TestServeCommandManagementHost'` → ok.
- Branch-Provenanz (origin): `0f08b877 → 5b8c5422 → 3a80ed04 → 64d93e94 → a87f8377 → 5e4fde71 (develop) → ...`. Kein foreign Commit.

## PUSH + HOSTED CI (terminal)

- Push `5b8c5422..0f08b877` nach `refs/heads/work/r27-management-host` (fast-forward, kein --force).
- PR #1405 Kopf = `0f08b877`, state OPEN, not draft, MERGEABLE.
- Hosted CI: **Run-ID 42322027058**, Kopf `0f08b877`, Resultat **success**.
- 25 Checks: **15 SUCCESS, 10 SKIPPED, 0 FAIL**.
- SKIPPED: HA/docker, HA/podman, consumer/demo/exact-candidate/runtime/validate, public contracts (nicht auf dem Go-only Merge-Pfad).
- SUCCESS u.a.: workflow policy, trusted plan, source format, go-build, go-vet, cli-build, cli-vet, cli-gofmt, cli-package-tests, cli-guided-tests, authority-package-tests, source-contracts, go-unit-tests (läuft jetzt den integration regression cell mit).
- Keine `.github/**`-Änderung, kein workflow_dispatch/rerun.

## END

- Ende mit drei Zeugen an Coordinator `a4573079` gepostet:
  1. `git merge-base --is-ancestor dddf0d7823f 0f08b877` rc=0.
  2. Neuer Kopf `0f08b877f4152c156b219ff6d13ab05ee6b082de`.
  3. Gehosteter Run 42322027058 → success (25 checks, 0 fail).
