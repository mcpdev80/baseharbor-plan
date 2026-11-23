# BUG-HUNT FILLJOB H-P1 (Wizard-UX stream app-new/app-edit)

- sitz f0f6c8b4, lane w27-pr1627-0428-061-pull. FILLJOB (fellregel), keine produkt-aenderung. Reine Befundung der Wizard-UX gegen den aktuellen develop.
- Mission m_f0f_hunt.md.g: H-P1 (Wizard-UX: app-new/app-edit) gegen AKTUELLEN develop (rev-parse belegen, mind. b3df96348; Releasedesse = CLOSED/merged). Reine Befundung: vor-ort-pruefung der wizard-pfade (fehlerpfade, abbruch-zustaende, consent-harmonisierung mit fail-closed), belege datei:zeile. KEINE commits/aenderungen im produkt. STOPP-REGEL: sobald coordinator echte kartenarbeit ankindigt, befund abliefern, nichts neues starten.
- scope: nur lesende inspection (source read, build, named unit tests per test-runner-rule). keine docker/podman container, keine hosted CI (massstab bleibt ci; hier only lesende inspection).

## PLAN (nummeriert, keine checkboxen)

1. mission m_f0f_hunt.md.g lesen (first action, before git). board + evidence planen.
2. git remote guard (origin = github.com/mcpdev80), fetch origin develop, rev-parse verifizieren (>= b3df96348), docker BEFORE.
3. wizard source lesen: app_new_wizard.go, app_wizard_controller.go, app_edit.go, app_edit_apply.go, provider_change_confirmation.go, app_candidate_consent.go, application_provider_preferences.go (finishAppNewWizard), app_init_prompts.go (promptYesNo/promptLine/readPrompt), app_new.go (entry/tty guard).
4. fail-closed review: EOF handling, consent defaults (yes=no), candidate-confirm, provider-change-confirm, abort/aborted phases.
5. build cmd/baha + named unit tests (per test-runner-rule: NAMED -run, never bare go test ./cmd/baha/).
6. findings synthetisieren (severity + reproduktions-schritt), akte schreiben.
7. docker AFTER + cleanliness. END.

## BASE ATTESTATION

- develop HEAD (git ls-remote / rev-parse origin/develop): 826d498fc1ae9524112d07477a8809798d8272a7.
- >= b3df96348a9c56de00d67a060c9a5f0ddf6593d5: YES (git merge-base --is-ancestor b3df96348 origin/develop => exit 0).
- build: go build ./cmd/baha/ => exit 0 (go1.26.8 linux/amd64).
- named unit tests run (TestAppNewWizard|TestVerifyRuntimeBrokerBuildIdentity|TestRuntimeBroker|TestAppEdit|TestEditApply|TestClientConsent), skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication": ok (30.845s). no failures.
- read-only: no product commits, no edits. evidence only in baseharbor-plan.

## INSPECTION FOCUS

wizard entry/app-new: app_new.go (appNewCommand Run: len(args)==0 && noInput && readerIsTerminal guard; else deterministic headless), app_new_wizard.go (runAppNewWizard + loop + finalize via finishAppNewWizard in application_provider_preferences.go), app_wizard_controller.go (state machine), app_candidate_consent.go (--confirm-candidate).
app-new/edit harmonization: app_new_wizard.go run-mode, application_provider_preferences.go finishAppNewWizard (run mode chdir + executor + candidate-confirm prompt).
app-edit: app_edit.go (runAppEdit entry, driveAppEditWizard, driveAppEditNeeds, driveAppEditPreview), app_edit_apply.go (appEditApplyConfirmed, runAppEditCommand), provider_change_confirmation.go (readProviderImpactAcknowledgements, classifyProviderChangeConsent).
consent gate: internal/application/provider_change_consent.go (ValidateProviderChangeConsent/validateProviderConsent), app_candidate_consent.go (finalizeCandidateConsent constant-time).
prompts/abort: app_init_prompts.go (promptYesNo default, readPrompt EOF, appInitReaderIsTerminal).

## FINDINGS

Severity scale: S=security/fail-closed risk, H=behavior bug, M=UX clarity, L=minor/nit. Repro = exact reproduktions-schritt where applicable. All read-only; no change made.

### F1 [S] app-new run-mode: candidate-confirm prompt is fail-closed by default (VERIFIED GOOD, documented)
- app_new_wizard.go:249 -> application_provider_preferences.go:247: `promptYesNo(reader, out, "Bind this exact candidate and continue with its lifecycle?", false)` — default no. Without --confirm-candidate the repository apply fails closed before writing deployment state (app_candidate_consent.go:159 finalizeCandidateConsent returns nil on empty rawDigest; app_candidate_consent.go:154 missingCandidateConsentError).
- reproduce: non-interactive/EOF => readPrompt returns io.EOF (app_init_prompts.go:390 readPrompt: EOF is cancellation). The confirm prompt never reaches a yes; project files remain; guidance printed (application_provider_preferences.go:249).
- conclusion: fail-closed confirmed. No finding. (Worth stating for the harmonization audit.)

### F2 [S] provider-change-confirm two-stage + separate data-deletion + stale-plan binding (VERIFIED GOOD)
- provider_change_confirmation.go:88 readProviderImpactAcknowledgements: loops stages 1..ConfirmationsRequired; default answer != "y"/"yes" => consent.First/Second stay false (fail-closed). Destructive => extra DeleteData prompt, separate from plan confirm.
- provider_change_consent.go:52 ValidateProviderChangeConsent => validateProviderConsent: PlanID must match (stale-impact-consent), First (and Second when confirmations==2) required, DeleteData required when destructive; provider_change_consent.go:60 validateProviderConsentRequirements: Version==ProviderImpactVersion && planID!="" && 1<=confirmations<=2 else invalid-impact-plan.
- classifyProviderChangeConsent(provider_change_confirmation.go:126) maps code ownership/foreign-/*-missing => ErrorOwnershipAmbiguous/ErrorConflict/ErrorValidationFailed (runtime classification of a user-facing error, not a bypass).
- conclusion: fail-closed, explicit, harmonized. No finding.

### F3 [M] app-new run-mode candidate-confirm prompt is shown AFTER chdir into the new project root (clarity, not a fail-closed gap)
- application_provider_preferences.go:250-256: after os.Chdir(root) the first executor run fails with missingCandidateConsentError; the prompt "Bind this exact candidate and continue?" (line 249) then appears while cwd is the freshly created project. If the operator later cancels, guidance references `<root>` (249) which is still correct, but the prompt's working-directory context is the new (not-yet-applied) app.
- severity M (UX clarity): no consent gap, but the prompt fires post-chdir; if the terminal closes mid-prompt, the "Project files were created" path (257-260) is what remains.
- repro: app new in run-mode, no --confirm-candidate; after creation the run-mode executor returns missingCandidateConsentError; confirm prompt shown in new root.
- recommendation (Owner scope; not changed here): show the candidate-confirm prompt before/without chdir, or make the message explicit that cwd is the new app. file:line application_provider_preferences.go:249-256.

### F4 [M] app-new "run" mode confirmation prompt default is no (fail-closed) — but the create-only vs run distinction in mode selection has a soft default that could surprise
- app_new_wizard.go:289-305 appNewExecutionMode: default (empty) => "create-only"; "run" => run mode. This is explicit and the question text at app_new_wizard.go:179 differs for run ("continue into the separately authorized lifecycle?"). Fail-closed confirmed for both.
- severity M (UX): the label "After creation (create-only or run)" (app_new_wizard.go:290) is terse; no finding, documented as the harmonization baseline.

### F5 [L] app_edit driveAppEditNeeds: unknown-key feedback lists all commands; "space" toggle result is ignored (no error surfaced)
- app_edit.go:283 driveAppEditNeeds "space" case calls `next, _ := session.Controller.SelectNeed(ctx, "space")` and ignores `next`/err, then sets session.Controller = next. app_wizard_controller.go:371 SelectNeed returns (next, confirmed); app_capability_selection.go:101 Update returns (model, confirmed) — for "space" at a non-final cursor it toggles selected and returns confirmed=false (no confirmation needed). The editor keeps the session. Fine, but there is NO on-screen feedback that the toggle happened (contrast: "n/no/back" prints a hint, "provider ..." prints usage).
- severity L (UX clarity): a keypress that silently toggles with no visual ack. reproduce: app edit, needs screen, press space on a capability row, observe no status line.
- recommendation (Owner scope): echo a one-line status ("<kind> selected" / "<kind> deselected") or rely on the next preview. file:line app_edit.go:283.

### F6 [L] app_new guidedStackProfile org-default error path is terminal (no retry) — intended?
- app_new_wizard.go:485-491: if organizationDefaultStack("dev") returns a name not in catalog => returns fmt.Errorf(...) with no retry/exit. This aborts the wizard with a raw error (app_new_wizard.go:75 -> appNewAbortOnEOF only handles io.EOF, so a non-EOF error propagates as a hard failure with a stack-ish message).
- severity L: inconsistent error presentation vs the usageError style used elsewhere (app_new_wizard.go:248, 252, 531). An org-default that resolves to a missing stack is an edge case; worth a usageError hint for parity. file:line app_new_wizard.go:489.

### F7 [M] new-wizard run-mode: after project creation the lifecycle is invoked with a fresh executor call; on partial-failure a message is printed but the decision lock lifecycle is released twice (potential double-release)
- application_provider_preferences.go:219-226: `release := func(){ if creationUnlock != nil {...} }` then passed as `release` param; at line 250 in run mode `release()` is called explicitly BEFORE the executor, then `defer`red release() again. The deferred release is idempotent (creationUnlock set to nil after first call). Not a leak.
- severity M documented as reviewed-OK: idempotent, no double-mutation. No finding beyond confirmation.

## HARMONISATION SUMMARY (fail-closed parity app-new vs app-edit)

- EOF: both wizards fail-closed. app_new app_init_prompts.go:390 readPrompt (EOF => cancellation, even with buffered partial "yes"). app_edit app_edit.go:249-250 (readErr && key=="" => Step(appWizardEOF) => errAppWizardAbort).
- consent defaults: app_new promptYesNo false (fail-closed) at provider-confirm (app_new_wizard.go:181) and candidate-confirm (app_provider_preferences.go:247). app_edit provider-change-confirm default answer != y/yes => First/Second false (fail-closed).
- candidate binding: app_new --confirm-candidate constant-time compare (app_candidate_consent.go:159); app_edit has no --confirm-candidate (edit is a running-app reconcile, uses provider-change-confirm instead). Both fail closed without explicit consent.
- abort/aborted phase: both converge to errAppWizardAbort (app_wizard_controller.go:27/308-315) and never reach Execute; edit driveAppEditWizard loop re-enters on stale preview (phase != decided) just like app-new's loop (app_new_wizard.go:209-213).

## CLEANLINESS

- docker BEFORE (before inspection): empty (header only, 0 containers).
- docker AFTER (after inspection, at END): empty (header only, 0 containers).
- no docker/podman compose projects or containers started by this lane. No networks/volumes/state directories created. ambient shared infra (bh-p427 pods, baseharbor-pre-release-registry) not mine, untouched.
- no product commits, no edits, no scratch files in the ecosystem root. evidence only in baseharbor-plan.

## END

END_DONE w27-pr1627-0428-061-pull: H-P1 BUG-HUNT DONE (read-only). develop 826d498fc (>= b3df96348), build OK, named unit tests pass. NO product change. FINDINGS: F1 [S] confirm prompt fail-closed (verified good), F2 [S] provider-change-confirm two-stage/destructive/stale (verified good), F3 [M] run-mode candidate-confirm fires post-chdir (UX clarity), F4 [M] create-only/run soft default documented, F5 [L] app-edit space-toggle no on-screen ack, F6 [L] org-default missing-stack hard error vs usageError parity, F7 [M] double-release idempotent (verified good). Akte published baseharbor-plan origin/main. docker ps -a clean. STOPP-REGEL active: as soon as coordinator signals real card work, stop and hand off.
