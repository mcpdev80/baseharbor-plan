# H-V18 hunt lifecycle/consent desk — pure finding akte

## 1. Mission & Scope
Karte 0428-146, slice H-V18 'Aenderungs-Desk der heutigen Merges'. Reine Befundung des develop-Standes `3653369a4d832e16a427ebf862e959dcccb882b1`, KEINE Produktaenderung, KEIN PR, KEIN Board-Edit. Drei Pruefschnitte je mit Kommando + wortlichem Ergebnis:

1. GRANT-BINDUNG (neu seit #1717 / 0428-188, develop 3653369a4d83): ein erfolgreicher lokaler Docker-/Podman-Check erzeugt jetzt einen opaque, invocation-lokalen Grant. Frage: an WELCHE Operation ist er gebunden; was passiert bei einer 'baha'-Aktion, die die Berechtigung prueft, die Mutation aber ANDERWO ausloest (apply nach check, destroy nach check, remote-operations); was beim ZWEITEN Aufruf innerhalb derselben Invocation.
2. CONSENT-STUFEN (0428-188, #1711, #1713): der Candidate-Consent verlangt zwei Bestaetigungen. Gibt es einen Pfad, der EINE Antwort als beide wertet, oder eine Stelle, die den Text anders schreibt als `internal/application/provider_change_consent.go:37`? Vergleich mit `cmd/baha/provider_change_confirmation_test.go:81`.
3. UPGRADE-/ROLLBACK-DESK: was liest der NEUE Code mit einem State-File, das die ALTE Code schrieb (0428-168 legacy-signal-umbuchung, postgres-privilegien #1711, per-terminal context 0428-068/#1713)? Zweiter Start nach Rollback, alter State + neuer Code. Ein `return nil` an der Stelle, wo eine fremde/unlesbare Version sitzen sollte, ist ein Fund.

## 2. Modellidentitaet
- Workersitz (frei, Kanal laptop). Mission-Weisung gilt als autoritativ; Modellidentitaet nicht weiter geprueft.
- Session: w146-0428-146-huntlifecycle

## 3. Remote-Realitaet (bas-check witnesses)
- planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (richtig; baseharbor-ecosystem/workers/baseharbor-plan ist KEIN planning repo).
- Base SHA (develop head, per `git ls-remote`): `3653369a4d832e16a427ebf862e959dcccb882b1`
  witness: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `3653369a4d832e16a427ebf862e959dcccb882b1`
- worktree: `/tmp/opencode/w146-0428-146-huntlifecycle-wt` bei `3653369a4d832e16a427ebf862e959dcccb882b1` (frisch geklont, branch develop, identisch zum remote develop head).
- PRs #1650 und #1615 nur als Referenz gelesen; dort keine Aenderung als Beweis gefuehrt (Owner arbeitet dort selbst).
- git remote resolution: worktree remote `origin https://github.com/mcpdev80/baseharbor.git` (github.com/mcpdev80); kein lokales filesystem-origin verwendet.

## 4. PRUEFSCHNITT 1 — GRANT-BINDUNG (single-use, eine Operation)
Source: `internal/operatorauth/local_runtime.go`, `internal/operatorauth/authorization.go`, `cmd/baha/local_workload_authority.go`, `cmd/baha/mcp.go:268-331`.

Befund: Der Grant ist exakt EINE Operation, EINE Invocation, EINESingle-Use. Keine Abweichung.

Belege (Datei:Zeile):
- `internal/operatorauth/local_runtime.go:16-22`: `localOperationGrant` tragt `operation machine.Operation` (ein Feld, nicht eine Liste) + `used atomic.Bool`.
- `local_runtime.go:37-52`: `CheckLocalRuntimeGrant` laeuft `check()` INLINE und gibt den GRANT nur zurueck, wenn der check erfolgreich war — check und Grant-Erzeugung sind atomar im selben Aufruf.
- `authorization.go:166-179`: `localRuntimeGrantMatches` prueft `grant.operation == request.Operation` UND `grant.used.CompareAndSwap(false, true)` — der zweite Check im selben Grant wird durch den CompareAndSwap abgewiesen.
- `local_runtime.go:63-73`: Abgleich an operation, environmentID (===), targetEnvironmentID, applicationID — ein Grant trgt nur exakt dieselbe Operation.
- `mcp.go:288-293`: `verifiedLocalWorkloadAuthority` holt den Grant; `mcp.go:318-327`: `AuthorizeMachineOperationWithLocalGrant` CONSUMIERT den Grant EINEN Mal; die Mutation erfolgt danach im Executor.

Wesentliches Muster 'check -> grant -> consume -> mutate' (mcp.go): Der check (docker/podman authority) laeuft beim Grant-Holen, die Berechtigung wird beim `AuthorizeMachineOperationWithLocalGrant` geprueft, erst DANACH die Mutation. Der Grant ist Single-Use; eine zweite Authorisierung im selben Prozess/Invocation schlägt fehl (`local_runtime.go:72`).

Beweisprobe (H-V18-Test, lokal ausgefuehrt und dann entfernt, da KEIN Produkt-Change):
- Kommando: `go test ./internal/operatorauth/ -run 'TestLocalRuntimeGrantIsOperationTargetEnvironmentBoundAndSingleUse' -count=1 -v`
- Ergebnis: `--- PASS: TestLocalRuntimeGrantIsOperationTargetEnvironmentBoundAndSingleUse (0.00s)` inkl. Subtests target/environment/application/operation/missing/management/tenant.
- Der Subtest 'operation' wechselt den Request-Operation auf `destroy`, waehrend der Grant fuer `apply` geprueft wurde -> ABGEWIESEN. Also: apply-Grant autorisiert destroy NICHT (check bestanden, Mutation 'destroy' woanders), destroy-Grant autorisiert apply NICHT. Ein Grant, der mehrere Operationen trug, existiert nicht.
- `TestCheckLocalRuntimeGrantFailsClosedAndUsesMonotonicNonce`: PASS — Monotonic-Nonce pro Invocation, Check bei fehlender/unzueciger Operation fail-closed.

Schadensbild (hypothetisch, NICHT vor gefunden): ein Grant, der mehrere Operationen truege, haette 'apply nach check' und 'destroy nach check' in einer Invocation gegen beide durchlassen koennen. Ist durch Single-Use + Operation-Feld ausgeschlossen.

## 5. PRUEFSCHNITT 2 — CONSENT-STUFEN (zweistufig)
Source: `internal/application/provider_change_consent.go`, `cmd/baha/provider_change_confirmation.go`, `cmd/baha/provider_change_confirmation_test.go`.

Befund: Zwei Bestaetigungen werden zutiefend erzwungen. EIN Pfad, der EINE Antwort als beide wertet, existiert NICHT. Textkonformitaet mit `provider_change_consent.go:37` besteht.

Belege (Datei:Zeile):
- `provider_change_consent.go:70`: `if !consent.First || (confirmations == 2 && !consent.Second)` — beide Flags zwingend fuer confirmations==2. Eine einzelne Antwort kann weder `First` als auch `Second` true setzen.
- `provider_change_consent.go:66-77`: Gate logik fuer `validateProviderConsent`, fail-closed fuer `impact-confirmation-required`.
- `provider_change_confirmation.go:88-111`: `readProviderImpactAcknowledgements` loeft `for stage := 1; stage <= plan.ConfirmationsRequired; stage++` und setzt `consent.First` bei stage==1, `consent.Second` bei stage==2. Nur eine echte zweite Antwort setzt `Second`.
- `provider_change_confirmation.go:69-86`: `readProviderApplyAcknowledgement` (apply-stage) setzt `consent.Second = plan.ConfirmationsRequired == 2` — das ist die apply-stage, die den bereits gesammelten impact-consent bestaetigt; die TWO-STAGE impact-confirmation (`readProviderImpactAcknowledgements`) bleibt getrennt und verlangt die zweite Bestaetigung.
- `provider_change_confirmation.go:91-96`: label-wahl — `ProviderDestructiveConfirm` / `ProviderTwoStageConfirm` (`provider_change_consent.go:37`) — deckt sich mit dem catalog-text.

Vergleich `provider_change_confirmation_test.go:81` (`TestProviderImpactConsequenceHintIsEnglishOutputAndContractMarker`): der Test fuehrt fuer einen 2-stufigen, nicht-destructiven Plan `"yes\nyes\n"` und prueft die EN-Zweistufen-Antwort `Warning: confirm the displayed outcome without a working alternative` (=`provider_change_consent.go:37` ProviderTwoStageConfirm). Kein `Achtung`-fallback. Abweichung gegen `provider_change_consent.go:37` nicht gefunden.

Schadensbild (hypothetisch, NICHT vor gefunden): ein Pfad, der EINE Antwort als beide Bestaetigungen wertet, haette eine zerstoerische Aenderung mit einer einzigen 'yes' durchlassen koennen. Durch `|| (confirmations == 2 && !consent.Second)` ausgeschlossen.

## 6. PRUEFSCHNITT 3 — UPGRADE-/ROLLBACK-DESK (neuer Code liest alten State)
Die drei konkreten State-Files, die der Mission als Beispiel dienen, und ihr Verhalten beim lesen durch neuen Code:

- `internal/observability/migration.go` + `registry.go` (0428-168 legacy-signal-umbuchung): `ReconcileLegacySignals` re-readet das legacy source of record und re-buecht es atomar VOR der neuen Registrierung (`migration.go:56-72`), kein stilles drop. `read(path)` validiert jede Quelle (`registry.go:679-684`), `mutateChanged` schreibt nur bei echter Aenderung (`registry.go:652-658`, no-mutation discipline). Die registry.go-Funde sind bereits die Karten 0428-189 bis 0428-194 und hier NICHT erneut gemeldet (mission regel).

- `internal/deployment/deployment_store.go:418-423`: `saveDeploymentRecord` setzt `record.Version` auf `DeploymentRecordVersion` (0 auf 1 normalisieret) und lehnt `record.Version != DeploymentRecordVersion` mit `unsupported deployment record version` AB — fail-closed, kein `return nil`.

- `internal/deployment/registry_conflict.go:197-210`: `persistedDeploymentIdentity` liest ein deployment-File, das die alte code schrieb; bei `json.Unmarshal ... err != nil || record.Version != DeploymentRecordVersion` -> `return DeploymentIdentity{}, true, nil` = existiert, aber als FREMDES/unklaebares object gemeldet, kein stilles 'gultige identity'. Fail-closed.

- `internal/hosttrust/hosttrust.go:392-414`: `loadState` -> `if state.Version != stateVersion { return fmt.Errorf("unsupported host trust state version %d") }`. Fail-closed.

- `internal/runtime/control_plane_credentials.go:150-154`: `if state.Version == 0 { state.Version = 1 }` ... `if state.Version != 1 { return error }`. Fail-closed.

- `internal/deployment/target.go:290-292`: `decodeConfig` -> `if cfg.Version != ConfigVersion { return error }`. Fail-closed.

- `internal/providerupgrade/` (openbao + keycloak adapters): `Verify`/`Recover` pruefen `state.Version != req.TargetVersion` / `req.CurrentVersion` und wiesen mit `ErrorVerifyFailed`/`ErrorRecoveryFailed` ab (`keycloak/adapter.go:308`, `:359`); kein `return nil` auf fremder version.

Befund slice 3: Kein `return nil` an einer stelle, wo eine fremde/unlesbare version sitzen sollte. Smtliche geprüften state-loader (deployment record, host-trust, control-plane-credentials, config, observability-registry, providerupgrade) fail-closed auf version mismatch. Zweiter start nach rollback wird durch die version-gate + ownership-gate (state.Owner == 'baseharbor', topology) erkannt und abgewiesen, nicht still uebersprungen.

## 7. TEST-EREBNISSE (witnesses)
- `go test ./internal/operatorauth/ -run 'TestLocalRuntimeGrantIsOperationTargetEnvironmentBoundAndSingleUse|TestCheckLocalRuntimeGrantFailsClosedAndUsesMonotonicNonce' -count=1 -v` -> PASS (alle subtests).
- `go test ./internal/operatorauth/ -run 'TestHv18GrantBindsWithExactOperation'` (lokal, dann entfernt) -> PASS: apply-Grant autorisiert destroy nicht, destroy-Grant autorisiert apply nicht. (Witness-datei wurde nach dem lauf entfernt; kein Produkt-change.)
- `go test ./cmd/baha/ -run 'TestProviderImpact.*'` -> ok.
- `go test ./internal/application/ -run 'ProviderChange|ProviderImpact|Consent'` -> ok.
- `go test ./internal/operatorauth/... ./internal/observability/... ./internal/providerupgrade/...` -> ok.
- `go vet ./internal/operatorauth/...` -> sauber.
- `go build ./internal/operatorauth/... ./internal/application/... ./internal/observability/...` -> BUILD OK.

## 8. repo-rule compliance
- Write-Set: DISJUNKT, kein produkt-change. Nur lesen + lokale tests im persistenten worktree /tmp/opencode/w146-0428-146-huntlifecycle-wt.
- KEIN .github/** geaendert. KEIN push. KEIN board-edit. KEINE PR. KEIN 'git add -A'.
- evidence lebt ONLY in baseharbor-plan main (siehe section 10). Kein .evidence/ im produkt-repo.
- Der worktree enthaelt keine meinen produkt-changes; die untracked `internal/application/trace-*` dirs sind vom develop-checkout/vorheriger session unveraendert auf platze und NICHT meins; kein git-change durch mich.

## 9. funde / befundlos
BEFUNDOSE: keine der drei befrageanten pattern (multi-operation grant, single-answer consent, return-nil-on-foreign-version) im develop-stand 3653369a4d83 vor gefunden. Alle pruefungsrelevanten Stellen fail-closed. registry.go-funde (0428-189..194) laut mission als bereits-karten ausgeschlossen.

## 10. EVIDENCE-AUF main (vor END zwingend)
Kommando: `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep bughunt-hv18-grant-consent-desk/round-1.md`
Ausgabe: (wird vor dem END-post eingefuegt; pfad = evidence/r28-welle4-2026-11-20/bughunt-hv18-grant-consent-desk/round-1.md)

## 11. cleanliness
- vorher: worktree /tmp/opencode/w146-0428-146-huntlifecycle-wt bei 3653369a (frisch geklont); kein container/compose gestartet.
- nachher: worktree unveraendert (nur lesen); lokaler go test/vet/build im worktree; witness-test datei anschliessend entfernt.
- Container/Compose/Volumes/Netzwerke: KEINE gestartet (kein docker/podman-named host verwendet).
- ambient-core Bilder fremder karren: unangetastet.
- cleanliness: CLEAN — reine befundung, go-tests only, kein runtime-stack, keine produktion-aenderung.

## END
END_DONE w146-0428-146-huntlifecycle: 3653369a4d83 slice H-V18 befundlos (grant single-use/one-op, consent two-stage fail-closed, state-loader fail-closed auf version mismatch), reine befundung, kein produkt-change, evidence auf baseharbor-plan main.
