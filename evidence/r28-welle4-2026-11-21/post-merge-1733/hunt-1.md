# Post-merge-desk zu #1733 (0428-211, Lane 0428-211-huntmerge)

ROLLE: Worker, BUG-HUNT. Reine Befundung, KEINE Produkt-aenderung, KEIN Commit an baseharbor, KEINE PR-Aktion.

L: 0428-211-huntmerge | SLICE: H-V32 | KARTE: 0428-211 (Perses anonymous denial names next command)

## BASIS-ATTESTATION
- develop head auf dem ich misst: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
  => 72ebc9d10ec247f24853af579655fd95c387214b  refs/heads/develop (gemessen 2026-11-21)
- #1733-Merge ist ancestor des aktuellen develop:
  `git merge-base --is-ancestor 44b55ea4bc66e0139dc147df10f925079ab1b27d origin/develop` => OK (YES)
- Realer baseharbor-remote (erste git-Aktion): `git remote -v`
  => origin https://github.com/mcpdev80/baseharbor.git (fetch/push). Kein LOCAL-FS-Remote, kein lane-origin in diesem Checkout.
- Plan-remote (erste Evidence-Quelle): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`
  => origin https://github.com/mcpdev80/baseharbor-plan.git
- Arbeitszone: /tmp/opencode/huntmerge-wt (frischer Clone, kein geteilter plan-checkout).

## 1. WAS #1733 INHALTLICH BRACHTE
- Merge-Comment: `44b55ea4 Merge pull request #1733 from mcpdev80/w226-0428-211-persesmsg` (Marcel Pfingstgraef, 2026-11-21 10:34:10 +0100)
  parents: f7c4bfa22589c7be3e605ceff769ada5fec4100f (develop vorher) + 3aec8701e497e583861babc227b509ddbd86398c (PR-Branchkopf)
- Der einzige inhaltliche Commit des PRs: 3a8b4a8b "perses: name next command on anonymous operator-auth denial"
  (committer lv4-verify <worker@baseharbor.local>). Zwei Merge-Commits im Branch waren nur Origin-Pull-Resyncs.
- Aenderungen auf develop (diff f7c4bfa2..3aec8701, also der PR-Inhalt):
  - internal/application/perses_management_ui.go | 1 Zeile geaendert (+1/-1)
  - internal/application/perses_management_ui_test.go | 28 Zeilen neu (+28)

## 2. PERSSES-VERWEIGERUNGSMELDUNG AM MERGED-STAND
- Datei im produkt-branch (develop), erzeugende Stelle:
  internal/application/perses_management_ui.go:96, in EvaluatePersesOperatorAccess() (Zeile 86),
  Arm !authenticated||principal==nil||!princip.IssuerVerified, ReasonCode "operator_authentication_required".
- Wortlaut (merged develop):
  "The optional Perses management surface requires a verified operator identity; an anonymous request is never admitted. Log in with 'baha login' for the selected Target/environment, then retry the same request."
- Vorher (f7c4bfa2) war nur der Missing-Precondition-Teil drin ("...never admitted."), kein Next-Command/Path.
- PR-Aenderung: Suffix angehaengt: "Log in with 'baha login' for the selected Target/environment, then retry the same request."
- Erfuellt sie die Karte? JA fuer den Wortschlssel der Karte: die Nennung von 'baha login' (Aktion) + 'for the selected Target/environment' (Path) + 'verified operator identity' (missing precondition). Error-Code und Fail-closed-Effekt unveraendert (ErrPersesOwnershipUnknown), der PR war explizit "No change to the error code or the fail-closed enforcement".
- Die Karte verlangte laut Commit-Message das Muster von cmd/baha/mcp.go:301 (machine.Error.Next: "run 'baha login' for the selected Target/environment, then retry.") => die perses_management_ui-Meldungues folgt dem gleichen Sprachmuster (Aktion + Target/Environment-Path + "retry").

## 3. NACHFOLGE-SUCHE: PRUFT EIN FALL DIE MELDUNG?
- `git grep -n "operator_authentication_required" origin/develop -- cmd internal` findet die Pruefung/Referenz
  an internal/application/perses_management_ui.go:95 (Setzung) UND internal/application/perses_management_ui_test.go:127-131.
- Der neue Fall: internal/application/perses_management_ui_test.go:116-145
  TestEvaluatePersesAnonymousDenialNamesNextCommand(t). Er bindet die Actionabilitaet der anonymous denial
  an den Wortlaut: fordert contains(decision.Reason,"baha login"), contains(...,"verified operator identity"),
  contains(...,"for the selected Target/environment"); err==ErrPersesOwnershipUnknown; ReasonCode=="operator_authentication_required".
- CI-Zelle/Job: der Fall laeuft in Job "Release Source Preflight" (workflow .github/workflows/ci.yml),
  Step "Run release-source tests" (ci.yml:123), Lauf ueber `go test ./contracts/... ./internal/... ./spec/...`.
  `internal/application` ist dort inkludiert => der neue Test wird in dieser CI-Zelle ausgefuehrt.
- Lokaler Run bestaetigt (Test Runner Rule, nur -run mit Name):
  `go test ./internal/application/ -count=1 -run "TestEvaluatePersesAnonymousDenialNamesNextCommand" -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` => ok github.com/mcpdev80/baseharbor/internal/application 0.008s
- ci-fast-check (ci POLICY): gofmt ok, source-readability ok, workflow policy 20 approved files, 295 tests OK.

## 4. NEBENWIRKUNGS-DESK (FAN-IN-REBASE-LISTE FENSTER, #1733 IS GEMERGT)
Alle offenen PRs, die in derselben Region aendern (cmd/baha/*, internal/application/*, internal/metrics/* perses).
Diff gegen develop via `gh pr diff --name-only`.

- #1745 lane-0428-083-datasources-r2 "Connect Perses Prometheus datasource" (perses-RUNTIME-Region):
  internal/application/management_ui.go, perses_datasource_*.go, perses_runtime.go, runtime_contract.go, runtime_postgres.go; internal/metrics/perses_prometheus_datasource*.go (14 Pfade).
- #1741 lane-0428-218-mcp-operator-seam "prove MCP operator-auth seam" (operator-auth-Region): cmd/baha/mcp_operator_seam_test.go.
- #1739 0428-210-alltargets "tolerate missing config for --all-targets" (cmd/baha): cmd/baha/app_commands.go, app_list_all_targets_test.go.
- #1738 lane-0428-214-destroystamp: cmd/baha/core_installation_runtime_test.go.
- #1737 lane-0428-213-trust-uninstall-false-green: cmd/baha/trust_uninstall_test.go.
- #1736 codex/env-destroy-gate-routing: scripts/pr-*.py (CI, keine Produkt-Region).
- #1728 w200-0428-200-verrmask-2 (internal/deployment): cmd/baha/app_context.go, internal/deployment/*.go.
- #1725 w201-0428-201-statever (internal/application): internal/application/shared_backends*.go.
- #1730 lane-0428-203-stale-target: internal/capability/integration_contract.go, internal/metrics/*.go.
- #1729 lane-0428-143-verify-none: internal/capability/integration_contract.go, internal/metrics/prometheus_verify*.go.
- #1704 w073-perses-alerts, #1702 lane-0428-142-statuswitness, #1665 lane-0428-082-perses-dashboards, #1650 lane-0428-078-perses-identity-on-resolver: weitere perses/metrics-Karten im Fenster (keine Aenderung an perses_management_ui.go).

Beobachtung (reine Befundung): #1745 greift direkt in die perses-RUNTIME-Region ein, die EvaluatePersesOperatorAccess/
perses_management_ui.go nahe liegt; das ist die aktive Fan-In-Nachfolge desselben Kartenumfelds (0428-083/076 perses).
Keine Handlung erforderlich; nur die Rebase-Liste fuer das Fenster dokumentiert.

## CLEANLINESS
- docker ps -a BEFORE (pid witness $$=623932):
  CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES  (leer)
- docker ps -a AFTER (pid witness 623932):
  CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES  (leer)
- Keine Container/Compose-Projekte gestartet (reine Lese-Akte, kein Produkt-Change). Sauber uebergeben.
- Kein 'go test ./cmd/baha/' ohne -run (Run-Regel eingehalten); nur gezielter -run.
- Kein 'git add -A' im geteichten checkout; kein Commit an baseharbor; keine PR-Aktion; keine Subagenten.

## REPO-RULE COMPLIANCE
- KEINE Produktdatei aendern (nur lesen/git grep/lokal -run).
- KEIN Commit an baseharbor; KEIN push an baseharbor.
- KEINE .github/**-Aenderung, KEINE workflow_dispatch/Rerun (Owner scope).
- KEINE Subagenten (4.8); jeder Schritt in dieser Session.
- Kein nacktes 'go test ./cmd/baha/'; nur '-run <Name>' mit skip-Form.
- Kein 'git add -A' im geteichten plan-checkout.
- Kein 'codeman agent post' in die Owner-Session; END ueber idle/watcher mit plan-sha.
- Evidenz lebt in baseharbor-plan/evidence/... (nicht in einem Produkt-Repo).

## PLAN
1. Mission lesen + plan-remote + baseharbor-remote verifizieren (done)
2. #1733 inhaltlich: develop-log merge-comment + git show pro eingebrachtem commit; gaendernte Dateien (done)
3. Perses-Verweigerungsmeldung am merged-stand: produkt-datei, woertleche meldung, erzeugende Stelle; nennt sie die geforderte aktion (done)
4. Nachfolge-suche: Fall der meldung prueft + CI-zelle/job-name (done)
5. Nebenwirkung-desk: andere offene PRs in derselben region (fan-in-rebase-liste) (done)
6. Akte + cleanliness + repo-rule compliance (done)
7. Evidence auf origin/main verifizieren + END posten (in Arbeit)
