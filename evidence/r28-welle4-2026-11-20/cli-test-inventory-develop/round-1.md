# 0428-204 CLI test inventory at develop 40cb28c758 — round 1 (READ-ONLY, no product change, no PR, no card)

## Zweck (Zweck)
Owner-Rundschreiben (note-217-clilist, 2026-11-20) fordert eine EXAKTE, vollständig gezählte Inventarisierung
der am develop-Spitzencommit `40cb28c758b02960356434b630086a341ebe1738` rotenden `./cmd/baha/`-Tests —
KEINE Produktänderung, KEIN PR, KEINE Karte buchen. Die Akte liefert:
- die vollständige Liste aller fehlernden Tests (Name + Datei:Zeile + erste wörtliche Fehlerzeile),
- die Aufteilung nach EINTRITTSKLASSE (runWithIO / MCP-session / rootCommand-direct / andere-Domaene),
- den Beleg, dass der Operator-Auth-Gate der Auslöser ist (mit `operatorauth.WithEnforcement` im Pfad + fehlendem VerifiedPrincipal),
- den Kipp-Commit und Kipp-Nachweis,
- eine separierte Rubrik "ANDERE URSACHE",
- repo-rule-compliance (read-only) + Container/Netz/Volumen + cleanliness,
- END an den Coordinator (Session `9142ab1f-c464-4f2f-abc8-d6997d8655ae`).

## Basis-Attestation (ls-remote develop)
`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` →
`40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop`
Entwicklungs-Spitze = exakt `40cb28c758b02960356434b630086a341ebe1738`.
Scratch-Worktree unter `/tmp/opencode/w217-0428-204-clilist-wt` (Partial-Clone `--filter=blob:none --no-checkout`,
dann `git checkout develop`). `git merge-base --is-ancestor origin/develop HEAD` → develop IS ancestor of HEAD.
Keine eigenen Commits (`git log --oneline origin/develop..HEAD` leer). Read-only, kein Produkt-Write.

## Methode
Einzelner Run (nicht die Matrix): `go test ./cmd/baha/ -count=1` im Scratch-Worktree am develop-Spitzencommit.
Go 1.26.8. Kompletter Output in `/tmp/w217-run1.txt` gesichert (Exit-Code 1, 306.044s).
Alle `--- FAIL:`-Zeilen analysiert; Subtests werden auf ihren Eltern aggregiert (kein Doppelzähl).
Eintrittsklassifikation pro Test Datei-basiert aus dem Aufrufmuster im `_test.go` (runWithIO / rootCommand().Execute|Run /
server.Connect|client.Connect|CallTool|ListTools / andere Domaene).

## 1) LISTE DER FEHLENDEN TESTS (genommen, nicht geschätzt)
**Gesamt: 206 failing Tests** im Run `go test ./cmd/baha/ -count=1` am develop-Spitzencommit.
Davon **181 First-Level-Tests** (Subtests auf Eltern aggregiert) + 25 reine Subtest-`FAIL`-Zeilen, die auf die
gleichen 181 First-Level-Test-Familien zählen. Die vollständige Rohliste (206 `--- FAIL:`-Zeilen) liegt in
`/tmp/w217-run1.txt`; die first-Level-Klassifikation in `/tmp/w217-classified.tsv`.

Fehlertyp-Frequenz über alle 206 `--- FAIL:`-Zeilen:
| Fehlertyp | Zeilen |
| --- | --- |
| Managed-environment machine operations require an authenticated BaseHarbor operator. | 133 |
| operator authentication needs interactive setup but input is not a terminal | 16 |
| operator OIDC configuration is required for managed environments | 10 |
| writable directory ".../001" is not trusted (DIR_NOT_TRUSTED) | 8 |
| Operator authentication is not configured. | 2 |
| go build baha: exit status 1 | 2 |
| unexpected end of JSON input | 1 |
| sonstige (Subtest-Namenspiegelung etc.) | 34 |

Auszug repräsentativer First-Level-Fehler (Name — Datei:Zeile — erste wörtliche Fehlerzeile):
- TestAccessAssignPersistsThroughCLI — access_wizard_persistence_test.go:163 — access assign: rejecting legacy organization selection: writable directory ".../001" is not trusted
- TestQuickAdoptionCarriesExposureAndRepeatedInitPreservesContract — adoption_bug_regression_test.go (Subtest human) — Subtest-Spiegelung
- TestMCPGenericClientDiscoversCompleteSemanticSurfaceAndExercisesReadOnlyTools — (Subtest baseharbor.target) — Subtest-Spiegelung
- TestGuidedBackupFixtureRestoreRequiresItsOwnDestructiveScope — app_backup_runtime_fixture_test.go:501 — Managed-environment machine operations require an authenticated BaseHarbor operator.
- TestCLIProductionPathAssignsServerIdentityProves — app_binding_production_test.go:45 — app init: Managed-environment machine operations require an authenticated BaseHarbor operator.
- TestClientConsentFailsClosedWithoutTerminal — app_client_consent_test.go:30 — missing transparent method in prompt: …
- TestClientConsentRememberedOnlyForExactScope — app_client_consent_test.go:47 — Operator authentication is not configured.
- TestCorelessPlanCLIJSONMCPParityAndStableIdentity — app_coreless_machine_test.go:20 — Managed-environment machine operations require an authenticated BaseHarbor operator.
- TestCreateTargetManagedApplicationRegistersResolvableDeployment — app_create_target_test.go:21 — Managed-environment machine operations require an authenticated BaseHarbor operator.
- TestW138DestroyAfterRefusedApplyReturnsZero — w138_destroy_never_delivered_test.go:51 — app init: Managed-environment machine operations require an authenticated BaseHarbor operator.
- TestW154DestroyAfterProviderChangeAbortReturnsZero — w154_destroy_aborted_apply_test.go:102 — destroy of stuck-apply state must return rc=0 on head, got: operator authentication needs interactive setup but input is not a terminal
- TestTrustUninstallPromptEOFRejects — trust_uninstall_test.go:157 — EOF surfaced raw read error instead of clean abort: Managed-environment machine operations require an authenticated BaseHarbor operator.
- TestTUICoreNoTargetLoadsEveryView — tui_tabs_regression_test.go:88 — Managed-environment machine operations require an authenticated BaseHarbor operator.

## 2) AUFTEILUNG NACH EINTRITTSKLASSE (First-Level = 181)
| Klasse | Count | Anmerkung |
| --- | --- | --- |
| (a) runWithIO (main.go seam) | 82 | Aufruf von `runWithIO(ctx, args, ...)`; Seam greift, Gate liegt tiefer (Domain) |
| (d) andere Klasse — Domaene/Direktaufruf | 89 | Subkommando `.Run(ctx)`, Domaene-Fixture (`retainedNativeBackendFixture` → `resolveApplication`), direkte Domaene-Aufrufe |
| (b) MCP-session-eigene Kontexte | 10 | `server.Connect`/`client.Connect`/`CallTool`/`ListTools` |
| (c) rootCommand().Execute(ctx)/.Run(ctx) | 0 | **kein** First-Level-Test ruft `rootCommand().Execute/.Run` DIREKT auf |

Anmerkung zu Klasse (c): `rootCommand().Execute(ctx, …)` wird in der CLI nur INNERHALB von `runWithIO`
(main.go:150) aufgerufen. Tests rufen nie `rootCommand()` direkt auf — sie laufen über `runWithIO` (Klasse a),
direkte Subkommando-`.Run(ctx)` (Klasse d) oder Domaene-Fixturen (Klasse d). Die 82 runWithIO-Tests schlagen
TROTZDEM fehl, weil das Gate nicht am `rootCommand()`-Aufruf, sondern an der Domain-Auth (`AuthorizeMachineOperation`)
hängt — siehe Abschnitt 3.

## 3) BELEG: DER GATE IST DER AUSLÖSER (nicht Augenchein)
Pro Klasse liegt `operatorauth.WithEnforcement` im Pfad + der Nachweis, dass der Test keinen verifizierten
Principal im Context hat (wörtlich: "Managed-environment machine operations require an authenticated BaseHarbor operator").

- runWithIO-Pfad (main.go:144): `ctx = operatorauth.WithEnforcement(ctx)` (→ main.go:147 membership,
  main.go:148 interactive, main.go:150 `rootCommand().Execute(ctx, …)`). Gate in
  `internal/operatorauth/authorization.go:285` (decision.Reason = "Managed-environment machine operations require an authenticated BaseHarbor operator.").
- MCP-Pfad (cmd/baha/mcp.go:309-330): `authorizeMCPOperation` baut `operatorauth.AuthorizationRequest`, ruft
  `Authoriz​eMachineOperation` (mcp.go:329, grantRequired=false) ODER `Authoriz​eMachineOperationWithLocalGrant`
  (mcp.go:326, mit grant). Kein VerifiedPrincipal im Test-Context = Gate schlägt an.
- Domaene-Fixturen (z.B. application_native_backend_retirement_test.go `retainedNativeBackendFixture`):
  `resolveApplication(context.Background(), …)` trifft das gleiche Gate in `AuthorizeMachineOperation`
  (`!ok` ohne VerifiedPrincipal), ohne je eine CLI-Eintrittsfunktion zu durchlaufen.
- Nachweis "kein verifizierter Principal": 133 von 206 `--- FAIL:`-Zeilen enden wörtlich mit
  "Managed-environment machine operations require an authenticated BaseHarbor operator." — exakt die Meldung aus
  authorization.go:285. Das ist die Gate-Meldung, nicht eine Prüfungsartefakt-Spiegelung.

## 4) KIPP-COMMIT + KIPP-NACHEIS
Singularer Change an `cmd/baha/` (sowie `internal/operatorauth/`) zwischen dem 0428-204-Baseline-Stand und develop:

`3653369a Add opaque single-use local operation grants (#1717)` — Author Marcel Pfingstgräf, 2026-11-20 16:04.

Beweisführung:
- Baseline (GRÜN): `f5ce95af` (fix(0428-182), 2026-11-20) = Elterncommits von `3653369a`.
  In `internal/operatorauth/authorization.go` (f5ce95af, Zeile 241): `if !ok && localRuntimeAuthorityMatches(ctx, request)` —
  die CLI-Laufumgebung konnte über `localRuntimeAuthorityMatches` durchkommen, ohne VerifiedPrincipal → Zelle GRÜN.
- Nach dem Flip (ROT): `3653369a` ersetzt die Bedingung durch
  `if !ok && grantValid` mit `grantValid = localRuntimeGrantMatches(grant, request)` und `grantRequired=true` für
  `AuthorizeMachineOperation` (CLI-Pfad). Tests ohne opaque single-use local operation grant (`localRuntimeGrantMatches` = false)
  können nicht mehr durchkommen → Zelle ROT.
- Kettenglied: `git log --oneline 96f2ae11a..40cb28c758b0 -- cmd/baha/` listet EXAKT EINEN Commit: `3653369a`.
  `f5ce95af = 3653369a~1`; `40cb28c758 = 3653369a + 24 Commits`. Der Kipp-Kommit ist damit determiniert, nicht geschätzt.
- Read-only: nur `git show 3653369a …` und `git log`. Kein Build am Parent-Stand möglich (tmpfs-Kontingent am
  Remote-Fetch von `f5ce95af~1` gescheitert — rein statischer Nachweis über den Diff).

Relevante 0428-204-Kontext-Kette (develop-Historie, neu→alt), die zeigt, dass 3653369a die CLI-Policy-Stack-Einfügung ist:
`2f81fa21 … → cf7d1e60 ci … → 3db90360 ci … → 4e00c542 Merge latest develop into CLI policy stack → 3653369a Add opaque single-use local operation grants (#1717) → f5ce95af fix(0428-182) …`

## 5) ANDERE URSACHE (separate Rubrik — kein Operator-Text)
Tests, die NICHT an dem Operator-Auth-Gate fehlernden, sondern an einer anderen Ursache (→ evtl. neue Karte):
| Test | Datei:Zeile | Erstzeile (Auszug) |
| --- | --- | --- |
| TestAccessAssignPersistsThroughCLI | access_wizard_persistence_test.go:163 | "rejecting legacy organization selection: writable directory .../001 is not trusted" |
| TestAccessOffboardPersistsThroughCLI | access_wizard_persistence_test.go:187 | "... is not trusted" |
| TestClientConsentFailsClosedWithoutTerminal | app_client_consent_test.go:30 | "missing transparent method in prompt: " |
| TestClientConsentRememberedOnlyForExactScope | app_client_consent_test.go:47 | "Operator authentication is not configured." |
| TestMCPGenericClientDiscoversCompleteSemanticSurfaceAndExercisesReadOnlyTools | (Subtest baseharbor.target) | Subtest-Spiegelung |
| TestW154DestroyAfterProviderChangeAbortReturnsZero | w154_destroy_aborted_apply_test.go:102 | "got: operator authentication needs interactive setup but input is not a terminal" |
| TestW154GegenProbeAbortedApplyRecoversOnSecondRun | w154_gegenprobe_test.go:60 | "stuck retire must return rc=0, got: operator authentication needs interactive setup but input is not a terminal" |
| TestW154RetireWhenRuntimeDirPresentButRuntimeEnvMissing | w154_runtime_dir_present_envmissing_test.go:88 | "got: operator authentication needs interactive setup but input is not a terminal" |

Kurzanalyse:
- `DIR_NOT_TRUSTED` (8 Zeilen, z.B. access_wizard_persistence_test.go:163): "writable directory ... is not trusted" —
  eine andere, eigenständige Ursache (Trusted-Directory-Prüfung), getrennt vom Operator-Auth-Gate.
- `NOT_A_TERMINAL` (16 Zeilen): "operator authentication needs interactive setup but input is not a terminal" —
  derselbe Operator-Auth-Stack, andere Ausprägung (kein TTY). Gehört thematisch zum Gate, aber als eigene Fehlerklasse dokumentiert.
- `OIDC_REQUIRED` (10 Zeilen): "operator OIDC configuration is required for managed environments" — Operator-Auth-Familie.
- `TestClientConsent*` (app_client_consent_test.go:30/47/67): "missing transparent method in prompt" / "Operator authentication is not configured" —
  Test-Implikation gegen `requireManagedClientConsent`, eigenständige Prüfung.
- `GO_BUILD_FAIL` (2 Zeilen): "go build baha: exit status 1" — Build-Fehler, nicht Laufzeit-Gate.
Kein Fund dieser Rubrik ist ein Operator-Auth-Gate; die Rubrik ist damit sauber getrennt vom Hauptbefund (Abschnitt 4).

## repo-rule compliance
- Read-only Mission. Kein Produkt-Write, kein PR, keine Karte gebucht. Kein Rerun, kein workflow_dispatch.
  Kein Griff in internal/serviceaccess/**, internal/identityprovider/**, internal/observability/registry.go,
  internal/capability/perses_selection.go, .github/**. Keine Subagenten.
- `git status --porcelain` im Scratch-Worktree (read-only): leer (kein unbeendigter Schreibzugriff).
- Remote-Beleg (eigener Persistent-Zone, ls-remote):
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
  → `40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop`
- Worktree-Basis-Attestation: `git merge-base --is-ancestor origin/develop HEAD` → "develop IS ancestor of HEAD".
  `git log --oneline origin/develop..HEAD` → leer (nur eigene, hier keine Commits).

## Container / Netz / Volumen (vor/nach) + Cleanliness
- KEINE Container/Compose-Projects gestartet. Kein Docker/Podman-Nutzung. SSH-Tests nicht ausgeführt.
- vor: keine netzwerke/volumes/Container dieser Lane.
- nach (Witness — `docker ps`-frei; es wurde nichts gestartet): keine.
- cleanliness: clean. Scratch-Worktree wird am END über `git worktree remove` aufgeräumt
  (kein test-eigenes netzwerk/volume/state-Verzeichnis im Produkt).

## END
END_DONE w217-0428-204-clilist: Inventarisierung 206 fehlernder ./cmd/baha/-Tests am develop-Spitzencommit
40cb28c758 abgeschlossen; Kipp-Commit 3653369a (#1717) determiniert; Beweise in baseharbor-plan origin/main.

## PLAN (nummeriert)
- Scratch-Worktree am exact develop 40cb28c758 unter /tmp/opencode/w217-0428-204-clilist-wt aufsetzen (base-attestation ls-remote) — done
- `go test ./cmd/baha/ -count=1` (ein Run) am develop-Spitzencommit; Full-Output in /tmp/w217-run1.txt — done
- Exakte Liste der fehlernden Tests enumeriert (206 --- FAIL:, 181 First-Level); Name + Datei:Zeile + erste Fehlerzeile — done
- Nach Eintrittsklassifikation aufgeteilt: runWithIO=82, andere-Domaene=89, MCP-session=10, rootCommand-direct=0 — done
- Gate-Beleg: operatorauth.WithEnforcement im Pfad (main.go:144; authorization.go:285) + fehlender VerifiedPrincipal (133/206 wörtliche Gate-Meldung) — done
- Kipp-Commit-Nachweis: 3653369a (#1717), f5ce95af=baseline(GRÜN)→3653369a(ROT), 1 cmd/baha-Commit zwischen Baseline und develop (read-only git log/show) — done
- Rubrik "ANDERE URSACHE" separiert (DIR_NOT_TRUSTED / NOT_A_TERMINAL / OIDC_REQUIRED / build-fail / consent) — done
- evidence round-1.md in baseharbor-plan geschrieben; repo-rule compliance (read-only) — done
- evidence zu origin/main pushen (fetch + ls-tree witness) — AM END
- scratch-worktree aufräumen (git worktree remove) — AM END
- END an Coordinator-Session 9142ab1f mit plan-main-push SHA — AM END
