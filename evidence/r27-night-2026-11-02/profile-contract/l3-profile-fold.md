# Evidence — l3-profile-fold lane (one-off doc fold)

- Task: `t-20261018-r27-profile-contract` (same PR #1324, fold finding)
- Lane: `l3-profile-fold` (worker, coordinator f49a3303)
- Product repo: `mcpdev80/baseharbor`, PR #1324, branch `work/r27-profile-contract`
- Evidence path: `baseharbor-plan/evidence/r27-night-2026-11-02/profile-contract/l3-profile-fold.md`

## PLAN (getickt)

1. [x] Worktree isoliert angelegt (`/tmp/opencode/l3-profile-fold-wt`, branch `work/r27-profile-contract`)
2. [x] Ist-Stand gelesen: `docs/(de)/spec/credential-access-v1.md` + `docs/(de)/spec/management-access-profiles-v1.md`, nav, cross-refs
3. [x] EN-Abschnitt "Management surface access profiles" in `docs/spec/credential-access-v1.md` ergänzt (keine Negation)
4. [x] DE-Abschnitt "Management-Zugriffs-Profile" sinngleich in `docs/de/spec/credential-access-v1.md` ergänzt
5. [x] Quelle `docs/(de)/spec/management-access-profiles-v1.md` mit `git rm` gelöscht
6. [x] Querverweise geprüft: kein nav/docs verwies auf den gelöschten Stem
7. [x] Checks: `go build ./...` rc=0, `go test ./contracts/managementaccess/v1` ok, `documentation-audit.sh` full PASS
8. [x] Commit `8b01eda5`, push+ls-remote verifiziert
9. [x] Regie-Änderung: KEINE CI-Auswertung (Owner-Kanal); END posten
10. [x] Planning-Handoff-Abschnitt aktualisiert, `plan.py check` 0 errors

## Was wird entwickelt (Produkt-/Funktions-Sprache)

Ein tragbares Management-Zugriffs-Profil wird fest in das zuständige Credential-/Zugangs-Eigentumsdokument eingespeist: Was ein nicht-geheimes Management-Profil, eine sensible Einmal-Geräte-Registrierung und ein explizit verschlüsseltes Credential-Export-Payload sind, was ihr Import darf und nicht darf, Storage-Trennung und die Abgrenzung zu `connection-profile/v1`. Keine Negation, kein Umbau drumherum.

## Was entwickelt wurde

- `docs/spec/credential-access-v1.md`: neuer normativer Abschnitt "Management surface access profiles" (ManagementAccessKind, fail-closed ImportCapability, StorageClass, ManagementAccessProfile, EncryptionDescriptor, callable path, relationship to connection-profile/v1, invariants).
- `docs/de/spec/credential-access-v1.md`: sinngleiches DE-Pendant.
- `docs/(de)/spec/management-access-profiles-v1.md`: gelöscht (`git rm`).
- Keine CI-Dateien (.github/**, pr-gate-plan.py, pr-check-runner.py) angefasst.

## Checks (lokal, eigen-Run)

- `go build ./...` → rc=0
- `TMPDIR=/tmp go test ./contracts/managementaccess/v1` → ok
- `bash scripts/documentation-audit.sh` → full PASS (Structure, Human-doc size, No legacy stubs, German scope, Internal evidence, ADR, Governance, Runtime docs, Task/domain IA, Podman release CI, Brand identity); `documentation-audit.sh` exit 0
- `python3 scripts/check_de_translation_integrity.py` → DE technical integrity PASS
- `python3 scripts/check_docs_locale_parity.py` → EN/DE page coverage OK
- `plan.py check` → 0 errors, 4 warnings (pre-existing, nicht meine)

## Ende / Terminalzustand

- Fold + Audit-Fix lokal: commit `8b01eda5` (Fold), `8f3ebff9` (Audit-Fix). Push+ls-remote verifiziert.
- Nach push bewegte sich der Shared-Branch weiter: Remote-HEAD ist `0db72d35` ("docs: restore credential profile example parity"), der dieselbe Audit-Parity löst. Shared PR-Kandidat — **kein Force-Push/History-Rewrite** (Owner-Regel).
- Terminal: PR #1324 `work/r27-profile-contract` @ `0db72d35`, base `develop`. Kein Merge/Release/Tag.
- Regie-Änderung (Owner-Direktiv): KEINE CI-Logs/Reruns/Auswertung; nach push+ls-remote sofort END posten.

## END

`END_DONE l3-profile-fold: head=0db72d35 | fold docs/(de)/spec/management-access-profiles-v1.md into docs/(de)/spec/credential-access-v1.md; audit+go tests pass; shared PR #1324 head=0db72d35 (remote advanced, nicht force-pushed); kein Merge/Release/Tag`
