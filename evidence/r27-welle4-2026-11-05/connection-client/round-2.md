# r27 connection-client — round 2 evidence (lane w164)

- Task: t-20261018-r27-connection-client (RUNDE 2)
- Repo: baseharbor
- Branch: work/r27-connection-client (head f1f3551291c2e71d23741818f25c27e578db8680; develop anchor 24c7d0492f34e58c2a6be505ba80b8bdfb151cb7)
- Coordinator: f49a3303
- Review: baseharbor-plan/evidence/r27-welle4-2026-11-04/connection-client/review-1380a.md (VOLL gelesen; Baseline-Rot-Klage gegen PR #1380 VORBESTAND — identisch auf pristine develop, erledigt)
- Owner-Entscheidung Runde 2: Autoritaetspruefung in den SELBSTstaendigen grenz-pfad (coreinstallation/authority.go + ConnectionSelection.Resolve) im use-/activate-pfad drahten — OHNE resolvedApplication; issuer darf NICHT ueber resolveApplication kommen. Wenn issuer in diesem pfad nachweislich nur mit workload-Kontext existiert: END_BLOCKED mit exakter aufrufkette. resolveApplication/apply/plan/destroy NICHT aendern.

## PLAN

- Mission + review-1380a lesen; branch/head/ancestor确认; caches unter /tmp/opencode/w164
- Empirisch bestimmen: kann use/activate-pfad issuer ohne resolvedApplication aufrufen? (issuer-resolution, resolveManagementConnectionIssuer-Abhaengigkeiten, file:line-Material)
- Wenn issuer nachweislich workload-only: END_BLOCKED mit exakter use->?->issuer-kette; sonst ConnectionSelection.Resolve in use/activate-grenze via coreinstallation-authority drahten, keine app-context
- Echte CLI-tests: ausdrueckliche auswahl gewinnt, autoritaet erlaubt/verweigert, fail-closed; je mit wortlichem output + mutant-gegenprobe (leitung kappen -> test rot)
- go build ./..., go vet ./cmd/baha ./internal/coreinstallation -count=1 -race x20, gofmt -l leer
- ls-remote verbatim == head, ancestor rc=0 vs develop, name-only diff, un betroffene pfade blob-liste; Planning publish + END

## Empirische pruefung: issuer im use/activate-pfad

### Befund: use/activate hat KEINE resolvedApplication, KEINE issuer-aufloesung

- cmd/baha/use_target.go:19-27 (useTargetCommand.Run): delegiert an targetCommand().Children[activate].Run — kein issuer, kein resolvedApplication, kein coreinstallation.Load.
- cmd/baha/target.go:241-263 (activate Run): LoadConfig() + writePersistedTarget(NAME) — kein issuer, keine verbindung, keine autoritaet; keine resolvedApplication{}.
- cmd/baha/target_activate_wizard.go:15-69 (guidedTargetActivation): LoadConfig() + writePersistedTarget() —同上, keine resolvedApplication{}, kein issuer.
- resolvedApplication{} wird NUR gebaut in cmd/baha/app_context.go (resolvedRepositoryApplication:146, resolveRegisteredApplication:258, resolveIncompleteRegisteredApplication:406, app_new_wizard:236, app_input_resolver:123, application_restore_source:59). NICHT in target.go/target_activate_wizard.go/use_target.go.

### Befund: der einzige issuer-aufruf ist resolveManagementConnectionIssuer, und der braucht resolvedApplication + workload

- cmd/baha/application_service_issuer.go:89 resolveManagementConnectionIssuer(ctx, resolved resolvedApplication, workload bhruntime.RuntimeProvider) (serviceaccess.Issuer, error):
  - ruft resolveApplicationServiceIssuer(ctx, resolved, workload) (application_service_issuer.go:20) auf — baut issuer aus resolved.TargetStateRoot + bound Core runtime (openbao.NewServiceIssuer(provider, files)) — REIDET workload + resolvedApplication.
  - resolveApplicationServiceIssuer (application_service_issuer.go:20-79): uses resolved.TargetStateRoot, applicationCoreTarget(selected), resolveApplicationCoreRuntime(resolved, workload) — alle drei benoetigen eine aufgelste resolvedApplication + RuntimeProvider.
- Keiner der use/activate-pfade ruft resolveManagementConnectionIssuer, resolveApplicationServiceIssuer, resolveApplicationCoreRuntime oder applicationCoreTarget auf. verifyConnectionSelectionForTarget (use_target.go:112) ist NUR in der tests aufruf; bindExplicitSelectionToConnection (use_target.go:61) NUR in der tests.

### Schlussfolgerung (file:line belegt)

- Der use/activate-pfad kann die live management-connection autoritaet NICHT aufrufen, ohne eine resolvedApplication + workload zu erfinden. Der issuer existiert in diesem pfad nachweislich nur mit workload-Kontext (resolveManagementConnectionIssuer:89 -> resolveApplicationServiceIssuer:20 -> resolveApplicationCoreRuntime, alle resolvedApplication+RuntimeProvider). Owner-Entscheidung ("wenn der issuer in diesem pfad nachweislich nur mit workload-Kontext existiert ... dann und NUR dann: END_BLOCKED") ist erfuellt.

## END_BLOCKED

- END_BLOCKED w164-connection-r2: head=f1f3551291c2e71d23741818f25c27e578db8680; aufrufkette: use(use_target.go:19)->target activate.Run(target.go:241)/guidedTargetActivation(target_activate_wizard.go:15)->kein issuer; live-issuer NUR ueber resolveManagementConnectionIssuer(application_service_issuer.go:89)->resolveApplicationServiceIssuer(application_service_issuer.go:20)->resolveApplicationCoreRuntime, alle resolvedApplication+bhruntime.RuntimeProvider; use/activate baut resolvedApplication{} NIEMAL (app_context.go:146/258/406, app_new_wizard.go:236, app_input_resolver.go:123, application_restore_source.go:59); Owner-entscheidung (issuer workload-only => END_BLOCKED) erfuellt; NICHTS am produkt-pfad aendern; grenz-erweiterung als eigene entscheidungs-karte kardieren.
- ls-remote origin work/r27-connection-client: f1f3551291c2e71d23741818f25c27e578db8680 (verbatim == local head); ancestor rc=0: git merge-base --is-ancestor origin/develop HEAD -> no (develop 24c7d049 ist VOR dem branch, PR basierte auf e444ae11, drift listet 512dcd72/3b5974ca/1a84726d/c762022e/0476164a/24c7d049 — die baseline-drift ist VORBESTAND, kein zweiter branch)

## Workspace-hygiene

- .w152/ (baseharbor/.w152/mod/...): foreign module cache von lane w152 (mt. 4. Nov 23:34, nicht meins). Nicht geloscht (fremder Arbeitsstand, §5.6). Untracked, unangetastet. Kein scratch in der ecosystem-root von mir.
- /tmp/opencode/w164: meine caches (falls benoetigt), ausserhalb des produkt-repos.

## blob-liste der un betroffenen pfade (bestaetigt, keine aenderung)

- cmd/baha/use_target.go (nur gelesen)
- cmd/baha/target.go (nur gelesen)
- cmd/baha/target_activate_wizard.go (nur gelesen)
- cmd/baha/application_service_issuer.go (nur gelesen)
- cmd/baha/app_context.go (nur gelesen)
- internal/coreinstallation/authority.go (nur gelesen)
- internal/coreinstallation/selection.go (nur gelesen, auf branch vorhanden)
- resolveApplication/apply/plan/destroy-code: NICHT angefasst
