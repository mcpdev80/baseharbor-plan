# Bug-Hunt 174: permission-denied / invalid-arg masquerading as 'foreign installation'

- Shift: r27-welle5-folge-2026-11-08 · Lane mission-174-impl · Datum: 2026-11-09
- Ziel: drei Ergebnis-Klassen EXPLIZIT trennen bei Ziel-/Installations-Identity-Aufloesung: (1) unlesbar/Access-Denied = named access error mit Pfad + Reparatur-Hinweis, (2) ungültiger Name/Argument = usage error mit offending input, (3) nur echter fremder Eigentums-Hash = foreign installation. Regressionen pro Zweig in CI-erfassten Gruppen.
- Kandidat: branch `0427-174-permission-truth` von develop HEAD 20902f0a abgetrennt.
- Planning evidence base SHA (planning repo, ls-remote origin main): 170d25f54844f28189dc2d7375cd6996c98a2eea
- Planning task card: t-20261108-bughunt-permission-lies-foreign-install (kanban active). Fundakte: evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd6.md (BF-HD6-1 blocker + BF-HD6-2).
- Subagenten: keine (Owner directive 2026-11-04). Kein .github/**.

## PLAN

- Fundakte hd6.md, mission-174-impl.md und Referenzquellen (deployment_store.go, deployment_list.go, app_repository_identity.go, coreinstallation/installation.go) lesen
- Beide Funde gegen develop HEAD reproduzieren (permission-denied + empty-target)
- Fix implementieren: 3 Wege trennen (access-denied usage error foreign)
- Regressionen: fake permission-denied fixture ueber test-seam + empty-target fall
- CI-Bezug herstellen (welche gruppe fuehrt den test)
- go test + go vet + go build
- Zweig anlegen, commit, ls-remote witness, PR, evidence on origin/main
- Terminaler hosted CI-run, cleanliness, END

## Funde (reproduziert)

### Fund BF-HD6-1 (blocker, permission-denied -> false foreign)

- Klasse: host-state / permission-denied. Schwere: blocker.
- Beleg: `coreinstallation.Load(".../gfield0427/runtime")` -> `os.Lstat(installation.json)` -> `permission denied` (mod 600 root:root, marcel uid 1000 kann nicht lesen).
- Ursache (file:line): `internal/deployment/deployment_store.go:115` `installation, err := coreinstallation.Load(targetRoot)`; die `else if err != nil` ветка bei `deployment_store.go:137-143` wertet JEDEN `os.ErrNotExist`-auesseren Fehler als `ErrDeploymentOwnerForeign` (Zeile 142). `coreinstallation.Load` schlaegt mit `open .../installation.json: permission denied` fehl — VOR der Inhaltvalidierung (Lstat scheitert). Also reine host-seitische Permission-Einschrankung, NICHT Fremdeigentum.
- Trace: `VerifyDeploymentOwner target="gfield0427"` -> `Load err=open .../gfield0427/runtime/installation.json: permission denied installationID=""` -> `Error: ... foreign installation cannot own this deployment`.
- Positiv: `local`/`w0427docker` installation.json = marcel:marcel 600 -> VerifyDeploymentOwner OK. fail-closed owner-pruefung ist korrekt; nur die Klassifizierung des Lese-Fehlers ist der Bug.

### Fund BF-HD6-2 (empty-target -> usage error)

- Klasse: cli / invalid-target-name. Schwere: medium.
- Beleg: `ListDeployments("")` -> `TargetStateRoot("")` -> `ValidateTargetName("")` -> `invalid target name "": use lowercase letters, digits, dots or hyphens...`.
- file:line: `internal/deployment/target.go:132-138` (ValidateTargetName), `internal/deployment/deployment_store.go:661-668` (ListDeployments -> TargetStateRoot).
- Status: der `InvalidTargetName`-Fehler ist bereits ein usage error, der den offending input nennt. Er läuft ueber `verifyDeploymentOwnerAtSeam` (deployment_store.go:43-45) und wird dort direkt zurueckgegeben — er ERREICHT ErrDeploymentOwnerForeign NICHT. In `repositoryIdentityClaims` (cmd/baha/app_repository_identity.go:91-95) ist er also bereits korrekt als usage error. Die Karte verlangt, dies explizit zu sichern (Regression), damit kein kuenftiger Umweg den Fehler wieder als foreign neu klassifizieren kann.

## Fix-Design

- 3 Wege trennen in `VerifyDeploymentOwner` (deployment_store.go) UND `VerifyDeploymentOwnerAgainstOwner` (deployment_owner_loan.go):
  1. `coreinstallation.Load` fehlgeschlagen UND `os.ErrNotExist` -> `ErrDeploymentOwnerMissing` (unveraendert).
  2. `coreinstallation.Load` fehlgeschlagen UND Zugriffs-/Lese-Fehler (permission denied, open failure, stat failure) -> NEUE sentinel `ErrDeploymentOwnerAccessDenied` mit Pfad + Reparatur-Hinweis (Besitzer/rechte); NICHT foreign.
  3. Installation laedt, aber Inhalt ist ungueltig/fremd (Hash/Ziel/Symlink-Escape) -> `ErrDeploymentOwnerForeign` (unveraendert).
- Diskriminator: Ein OS-Level-Lese-/Zutrittsfehler auf der installation.json ist ein host-state access problem, kein owner-identity problem. Nur eine datei, die LAEDT aber INHALTLICH falsch ist, ist foreign.
- `ErrDeploymentOwnerAccessDenied` = `errors.New("deployment state directory for Target is not readable; the Core installation.json is not accessible to this user — check owner and permissions; ... before its state is loadable")`, mit dem fehlgeschlagenen fs.Error unwrapbar.
- `errIsAccessDenied(err)`: `errors.Is(err, os.ErrPermission)` OR (stat/open error && !errors.Is(err, os.ErrNotExist) && !errors.Is(err, os.ErrExist)).
- Access-denied muss fail-closed bleiben: kein loan-hook umgeht access-denied zu foreign.
- empty-target regression: sicherstellen, dass `ValidateTargetName`-fehler als usage error propagiert (keine aenderung an logik, nur test).

## Regressionen (Test -> Check -> Trigger)

- Test 1: `TestDeploymentOwnerAccessDeniedIsNotForeign` (internal/deployment/*_test.go): provision owner, chmod installation.json auf 0400 (unreadable for a non-root test user is not reliable in CI; use a test-seam that returns an os.ErrPermission from Load) -> VerifyDeploymentOwner returns ErrDeploymentOwnerAccessDenied, NOT ErrDeploymentOwnerForeign; DeploymentRecordState().Kind classifies as access-denied; save/load/list all surface access-denied; on-disk record bytes unchanged.
  - Test-seam: package-internal var `testLoadInstallationForOwner func(root string) (coreinstallation.State, error)` defaulting to `coreinstallation.Load`, so a test can deterministically return os.ErrPermission without depending on real file permissions (which are root-dependent in CI).
- Test 2: `TestDeploymentOwnerEmptyTargetUsageError` : `ListDeployments("")` returns InvalidTargetName usage error, not ErrDeploymentOwnerForeign; `ValidateTargetName("")` names the offending input.
- CI-Bezug: tests in `internal/deployment/` werden ausgefuehrt in der Gruppe "release-source-tests" (ci.yml Zeile 122: `go test ./contracts/... ./internal/... ./spec/...`) UND "go-unit-tests" (ci.yml: `go test ./...`). Beide CI-gruppen erfassen den path; kein .github-aenderung noetig.
  - Lernfall 163/172: ein permission-fehler ist NICHT abwesenheit; der test muss access-denied explizit gegen foreign abgrenzen, nicht nur "irgend ein error".

## Verified-against-developed-binary (Lernfall 162)

- hd6.md meldet fresh build 452be76c identisches verhalten -> kein stale binary. Hier: fix auf develop HEAD; build gegen 20902f0a; verifikation ueber go test matrix + eigener checker.

## Local verification

- `go test ./internal/deployment/... -run 'TestDeploymentOwner' -count=1` -> expect green incl. new tests
- `go test ./... ./contracts/... ./spec/...` (release-source subset)
- `go vet ./...`
- `go build -o /tmp/baha-174 ./cmd/baha`

## Branch provenance

- Base SHA (develop HEAD, ancestor of first commit): 20902f0a6ab016fd8fe6a501751e1becc5f334dd
- `git rev-list --parents -n1 <first-commit>` shows 20902f0a as sole parent; `git log` lists only my own commits.

## Repo-rule compliance

- Nur product-write-set: internal/deployment/deployment_store.go, internal/deployment/deployment_owner_loan.go, internal/deployment/*_test.go. Kein .github/**. Kein evidence-verzeichnis im product-repo.
- Evidence nur in baseharbor-plan (evidence/bughunt-permission-lies-foreign-install/round-1.md).

## CLEANLINESS

- Keine container/compose gestartet (pure Go unit test, keine runtime gates). git status working tree nach commit = clean.

## END

- Lane: mission-174-impl — PENDING (END erst nach terminalem hosted CI-run + origin/main evidence)
