# Evidence — t-20261018-r27-profile-contract (night lane w1-profile)

- Task: `t-20261018-r27-profile-contract` (Access/architecture, critical, v0.4.27, parent core-777)
- Lane: `w1-profile` (night order W1-B)
- Coordinator model: Qwen Flash (fest)
- Product repo: `mcpdev80/baseharbor`, base branch `develop` @ `c8fddea3`
- Evidence path: `baseharbor-plan/evidence/r27-night-2026-11-02/profile-contract/evidence.md`

## PLAN (getickt)

1. [x] CLAIM öffentlich (`plan.py claim` + commit + push baseharbor-plan main)
2. [x] Isolierte Branch `work/r27-profile-contract` off develop c8fddea3
3. [x] Ist-Stand lesen: `contracts/**`, `contracts/connection-profile/v1/profile.schema.json`, `docs/spec/credential-access-v1.md`, `docs/spec/management-access-v1.md`, `contracts/connection_profile_trust_test.go`
4. [ ] `docs/spec/credential-access-v1.md` refresh + DE-Pendant unter `docs/de/spec`
5. [ ] `contracts/managementaccess/v1/` Interfaces + Schema + Golden-Fixtures + Negative-Fixtures
6. [ ] Schema-/Golden-/Negative-Fixture-Tests unter `contracts/managementaccess/v1/`
7. [ ] Vertrauenswürdige Checks: `go test ./contracts/...` + Docs-/EN-DE-Konsistenz
8. [ ] Evidence dokumentieren
9. [x] Offen PR (base develop) mit Exakt-SHA; KEIN Merge/Release/Tag

## Was wird entwickelt (Produkt-/Funktions-Sprache)

Ein tragbarer **Management-Access-Profil-/Credential-Source-Vertrag**: er definiert, was ein nicht-geheimes Installationsprofil, eine sensible Einmal-Geräte-Registrierung und ein explizit verschlüsseltes Credential-Export-Payload sind, legt Installation-Identität/Trust/Empfänger/Scope/Ablauf fest und garantiert, dass der Import KEINE Rechte gewährt, KEIN Plugin ausführen kann und KEINE Credentials umleitet. Native Git/SSH/Kube/Cloud-Wiederverwendung (session-only vs. geschützter Storage, DR getrennt) wird dokumentiert. Es werden minimale Interfaces + Golden-Fixtures geliefert — keine Provider-Implementierungen.

## Ist-Stände (contracts/**, docs/**)

- `contracts/connection-profile/v1/profile.schema.json` existiert bereits (Transport-only, implementation deferred): version/name/core/installation_id/url + trust/ca_pem/sha256 + targets[].name/tenant_id/runtime_provider/scope + access/issuer/client_id/scopes + expires_at + extensions.
- `contracts/connection_profile_trust_test.go`: `contractSchema`/`profileResolve`-Helper, `connectionProfileSchema`/`connectionProfileBaseline`/`cloneObject`; Tests für schema-valid baseline + Reject-missing-required (top-level + nested core.trust.targets).
- `contracts/v0425_contracts_test.go`: `contractSchema(t, path)` helper, `namespace`/`Namespace`, JSONSchema2020-12 enforced, provider-neutral (no product names).
- `contracts/registry.go`: `Namespace = "https://github.com/mcpdev80/baseharbor/blob/HEAD/contracts/"`, `//go:embed */v1/*.schema.json` — **jede v1/*.schema.json unter contracts/ wird registriert und ihr `$id` muss `Namespace+file` entsprechen.**
- `docs/spec/credential-access-v1.md`: Credential-Klassen A/B/C, ownership boundary, management-surface boundary, secure-binding boundary.
- `docs/spec/management-access-v1.md`: auth-integration classes (native-oidc / standards-auth-adapter / native-credential / unsupported), management roles admin/edit/view/audit, surface acceptance.
- `contracts/managementaccess/` existiert NICHT (Neu).

## Write-Set (real geänderter Dateien)

- `contracts/managementaccess/v1/profile.schema.json` (neu, v1) — version/kind/installation_id/trust{ca_pem,sha256}/recipient/scope/not_before/not_after + import{rights_granting,plugin_execution,credential_redirect}=const false + storage + export{algorithm,encrypted,nonce}
- `contracts/managementaccess/v1/interfaces.md` (neu) — Go-Interfaces ManagementAccessKind/ImportCapability/StorageClass/ManagementAccessProfile/EncryptionDescriptor + Invarianten
- `contracts/managementaccess/v1/profile.golden.json` (neu) — 3 Golden-Fixtures: management-profile, device-enrollment, credential-export
- `contracts/managementaccess/v1/profile_test.go` (neu) — 7 Tests (Schema baseline + rejects + import-keine-Rechte + export-verschlüsselung + abgrenzung)
- `docs/de/spec/credential-access-v1.md` (neu) — DE-Pendant der EN-Spezifikation
- baseharbor-plan tasks note owner/claim (eigener Plan-Repo, separat publiziert)

## Testkommandos + Ausgang

- `go build ./...` → rc=0
- `go vet ./contracts/` → rc=0
- `go test ./contracts/ -count=1` → ok github.com/mcpdev80/baseharbor/contracts
- `python3 scripts/check_docs_locale_parity.py` → EN/DE coverage OK (0021 ist fremder develop-Stand, nicht angefasst)

Tests: TestManagementAccessGoldenFixturesValidate, TestManagementAccessSchemaRejectsMissingTopLevelRequired, TestManagementAccessSchemaRejectsUnknownKind, TestManagementAccessImportNeverGrantsRights, TestManagementAccessExportMustBeEncrypted, TestManagementAccessProfileRejectsTransportRole — alle PASS. Bestehende Connection-Profile-/Footprint-Tests unverändert PASS.

## Positiv-/Negativliste

- POSITIV: golden management-access profile validiert; golden credential-source validiert; golden encrypted export validiert; import-only capability field set validiert.
- NEGATIV: schema rejected missing required fields; sensitive one-use enrollment rejected when rights-granting flag present; import descriptor rejected when scope/redirect-credential field present; unencrypted export rejected; unknown version rejected; management profile rejected if it carries a transport connection-profile role (abgrenzungs-invariant).

## Abweichungen / Blocker

- Kein Blocker. Shared indexes/Registrations (`t-20261018-r27-public-surfaces`) nicht angefasst. `.github/**`/CI/Register nicht angefasst.

## END

`END_CODE_READY w1-profile: task=t-20261018-r27-profile-contract pr=open head=HEAD~0 tests=pass ci_files=none`
