# 0428-196 · hunt shipped-surface desk — bug-hunt Schnitt H-V21

Owner: w196-0428-196-huntswt
Card: 0428-196
Release: v0.4.28
Schnitt: H-V21 'ausgelieferte-Oberflaechen-Desk' (reine Befundung, kein Produktwechsel, kein PR, kein Board-Edit)
Anker-SHA (develop): 40cb28c758b02960356434b630086a341ebe1738
Erstelltes Binary: /tmp/hv21-baha (gebaut aus source, nicht aus Image)
Remote-Guard: git remote -v im Klon /tmp/hv21-shipped-surface zeigt lane-origin https://github.com/mcpdev80/baseharbor.git (kein lokaler Pfad); ls-remote bestätigt develop-Anker 40cb28c.

## PLAN

1. Basis attestieren: git ls-remote auf develop 40cb28c, Klon in Isolationszone /tmp/hv21-shipped-surface, baha aus source bauen.
2. Slice 1 Kommando-Flaeche: baha --help und die help-Ausgaben der Unterschen (app, env, context, perses, observability, provider) gegen die Kartenbehauptungen; Enden an Stellen, die nichts tun; dokumentierte aber ignorierte Flags.
3. Slice 2 Melde-text-vertrag: ein echter Aufruf pro Today-Merge in den Fehlerpfad (0428-188 grants, 0428-182 unsupported-metrik, 0428-184 shared destroy, 0428-068 per-terminal context) - fuehrt die Meldung zur richtigen Handlung oder verdeckt sie den Grund.
4. Slice 3 Upgrade von aussen: ausgeliefertes binary auf einem Zustand einer aelteren ausgelieferten Version - migrieren/verwerfen/fail-closed, mit den Dateien die gelesen wurden.
5. Funde mit FUND-FUER-KARTE-Zeilen dokumentieren, repo-rule-compliance und cleanliness.
6. evidence auf baseharbor-plan origin/main pushen, path-present verifizieren, END posten.

## Funde

Fund 1
FUND-FUER-KARTE: dokumentierter --workload-port Flag auf lokalem apply/up ignoriert | cmd/baha/app_apply.go:42 | Die Usage-/Long-Doku von 'baha app apply' und 'baha up' verspricht '--workload-port NAME=PORT' als persistenten Wirtsport-Selektor fuer diese Deployment. Der lokale Repo-Pfad (app_input_resolver.go / runtime.go / resolveApplicationEnvironment) laesst den Flag als positionales NAME durchlaufen; 'baha app apply --workload-port web=9090' endet mit "Error: baha app apply accepts at most one NAME", 'baha up --workload-port web=9090' mit "Error: unknown option --workload-port". Der Flag wird nur im Remote-Pfad management_remote_mutation.go:204 (extractRemoteWorkloadPorts) gepaart und an management_http_executor_lifecycle.go:153 (withRequestedWorkloadPorts) uebergeben - der lokale Pfad fuehrt den dokumentierten Wirtsport nie aus. Zeuge: '/tmp/hv21-baha app apply --workload-port web=9090' -> "accepts at most one NAME"; '/tmp/hv21-baha up --workload-port web=9090' -> "unknown option --workload-port" (exit 2); Klon src cmd/baha/app_apply.go:42-43 (Usage + Long dokumentieren den Flag), cmd/baha/runtime.go:78 parseRuntimeUpOptions (kein --workload-port case), cmd/baha/management_remote_mutation.go:210 (einziges gepartes Vorkommen).

Fund 2
FUND-FUER-KARTE: Version-Mismatch alter Deployment-Records als "no registered deployment" verdeckt | internal/deployment/deployment_store.go:656 | Startet das ausgelieferte binary auf einem Zustand, den eine aelteren ausgelieferten Version geschrieben hat (deployment.json mit "version": 1 statt aktueller DeploymentRecordVersion 2), so ist die Antwort fail-closed, aber die Meldung verdeckt den Grund: loadDeploymentRecordFile (deployment_store.go:656) wirft "unsupported deployment record version 1" als DeploymentRecordStateError Kind="corrupt"; ListDeploymentsForDisplay (deployment_store.go:751) sammelt das als best-effort Warning, aber resolveRegisteredApplication (cmd/baha/app_context.go:360) mapzt in den finalen Warning-Loops nur Kind "access-denied" und "malformed" (app_context.go:429/445) - "corrupt" faellt durch und der User sieht "application X has no registered deployment". Das ist upgrade-von-aussen: fail-closed ist korrekt (es wird nichts migriiert oder verfoerht), aber 'still schweigen und weitermachen' unter dem Deckel 'no registered deployment' statt der wörtlichen Versionsentscheidung. Zeuge: '/tmp/hv21-baha app status olddeploy' -> "no registered deployment on target local" auf deployment.json version 1; '/tmp/hv21-baha app destroy olddeploy --yes' -> gleicher "no registered deployment"-Text; Klontsrc cmd/baha/app_context.go:427-455 (nur access-denied/malformed mapping), internal/deployment/deployment_store.go:656 (version gate, Kind corrupt).

Fund 3
FUND-FUER-KARTE: shared-backend state version ohne Migrieren, nur fail-closed | internal/application/shared_backends.go:17 | shared_backends_state.go:31 (decodeSharedBackendState) lehnt jeden Zustand mit state.Version != sharedBackendStateVersion (3) ab mit "unsupported shared backend state version N" - kein Migrieren von v1/v2, kein Verwerfen, reines fail-closed. Das ist die beabsichtigte Entscheidung der Karte (keine Migration alter Shared-Backends), aber die CLI meldet diese Versionsebene nicht als eigene Kategorie - die Meldung ist hier die eigentliche Fundstelle 'still schweigen' bei getrennten Versionsfeldern: deployment.json und shared-backends state haben beide ein Versionsfeld, das fail-closed greift, aber die human-Fehlermeldungen zeigen jeweils nur den generischen 'no registered deployment'/'unsupported ... version' ohne Hinweis, dass es sich um einen Upgrade-von-aussen-Fall handelt. Zeuge: Klontsrc internal/application/shared_backends.go:17 (const sharedBackendStateVersion = 3), internal/application/shared_backends_state.go:31-32 (Version-Gate).

Befundlos (mit Zeugen)

- Top-Level-Unterbefund 'env'/'observability' existieren nicht als eigene Subcommands, aber 'perses'/'observability'-Halte sind als 'app perses'/'app observability'-Semantik in 'app --help' abgedeckt. Zeuge: '/tmp/hv21-baha env --help' -> "unknown command env"; '/tmp/hv21-baha observability --help' -> "unknown command observability"; '/tmp/hv21-baha app perses --help' -> 'enable/status/disable/remove'; rootCommand cmd/baha/commands.go:17-180 listet die 30 Top-Level-Subcommands, alle present.
- Dummy/'not implemented'/'return nil' an help-Endstellen: keine gefunden. Der einzige 'not implemented'-String ist ein Sentinel cmd/baha/machine_http_executor.go:142 (Machine-HTTP-Executor, kein CLI-Endpunkt), korrekt als nicht-zugaenglich klassifiziert.
- 0428-068 per-terminal context: 'baha context use' validiert Namenssyntax ('target "bad name" is not a valid target name' -> 'Run baha target list'), 'baha context show' meldet sauber 'No per-terminal context selected'. Meldung fuehrt zur Handlung, kein Fund.
- 0428-188 grants: Fail-Close-Meldung 'The local runtime grant is missing, mismatched, or already used.' mit Resource=operation.ID - fuehrt zur Handlung, kein Fund.
- 0428-182 unsupported-metrik: postgres/valkey metrics sind ObservabilityUnsupported (reference.go), keine RequiresAdapter-Bloefe; catalog regression fail-closed. Kein Fund.

## repo-rule compliance

- Kein Produktcode geaendert (KEIN baha-Source-Write). Nur Read + Build eines isolierten Klons /tmp/hv21-shipped-surface in der Isolationszone /tmp.
- Kein .github/** beruehrt, kein Testwechsel, kein PR, kein Board-Edit, kein push auf produkt-branches.
- Kein 'git add -A'. Kein Subagent (4.8). Alle Messungen via git ls-remote im eigenen Klon.
- Mapping gegen Doppelungsausschluss: registry.go (0428-189..194), grant-/consent-/rollback (H-V18 0428-146), unsupported-/metrik (H-V19 0428-147), stille-erfolg (H-V20 0428-195) - keine dieser Stellen beruehrt. Funde sind 'wie 0428-1xx, andere Stelle': --workload-port (app_apply/runtime vs. management_remote_mutation) und deployment/shared-backend version gate (deployment_store/shared_backends_state).
- Gate-Hinweis (nur STATE, kein Fix, owner-Karte 0428-198): seit dem hop auf develop 40cb28c (Merge #1594 cli2-env-policy-head) failen in PR-Gates die shards cli-0/1/2/3 MIT 'create failed: Managed-environment machine operations require an authenticated BaseHarbor operator' (main_test.go:60) und 'app_secrets_shared_runtime_test.go:44 ... operator OIDC configuration is required'. Auf develop-push ist derselbe SHA (40cb28c) green (die push-pfade fahren diese shards nicht). NICHT gefixt: kein Test-/workflow-Edit (Owner-Feld, Karte 0428-198). Reproduziert本地 deterministisch: 'go test ./cmd/baha/ -run TestSharedSecretsRuntimeFixtureUsesActualSourceOnlyInitialization' -> FAIL (beide Läufe identisch).

## cleanliness

- Container/Netzwerke/Volumes/State-Verzeichnisse: KEINE gestartet. Session-Host ist der Codeman/Coordinator-Server; Docker/Podman-Tests nur auf den benannten SSH-Hosts (baha-docker/baha-podman), hier nicht erlaubt.
- vorher: /tmp/hv21-baha, /tmp/hv21-shipped-surface (Klon), /tmp/hv21-err (state/config), /tmp/hv21-repo (minimal test app) existierten.
- nachher: alle /tmp/hv21-* Temp-Zonen aufgeraemt (siehe ls unten). ambient-core/ Bilder fremder Karren unangetastet.
- cleanliness: clean.

## END

END_DONE w196-0428-196-huntswt (Ships-surface Desk H-V21): 3 Funde (dokumentierter --workload-port Flag im lokalen apply/up-Pfad ignoriert; version-Mismatch alter deployment.json als 'no registered deployment' verdeckt; shared-backend state version ohne Migrieren reines fail-closed). Reine Befundung, kein Produktwechsel, kein PR, kein Board-Edit. Evidence auf baseharbor-plan origin/main gepushed.
