# round-4-developauthz — 0428-210 keep-develop-authorization on --all-targets app list

## Role / card / PR

- Rolle: Worker, Karte t-20261121-all-targets-config-loss (0428-210)
- PR: #1739, branch `0428-210-alltargets`, base `develop`, draft=false, open
- Korrekundrunde nach CODEX-REVIEW review-1.md ('Verdikt: REQUEST CHANGES')

## PLAN

1. eigenen baum + identitaet im baum (commit-author = 0428-210-authzkeep) -- erfuellt
2. develop-auth-block wiederhergestellt (authorizeMCPOperation dev fuer --all-targets; authorizeCurrentMCPContext fuer selected) -- erfuellt
3. ErrConfigMissing nur NACH autorisierung am inventar-lese-pfad toleriert (nur cmd/baha/app_commands.go, write-set eingehalten) -- erfuellt
4. gruen: app_list_all_targets_test.go (installiert + zerstoert) bleibt gruen -- erfuellt
5. negativer fall beweist abweisung mit operator-auth-fehler (literal 'Managed-environment machine operations require an authenticated BaseHarbor operator'), keine config-bypass -- erfuellt
6. push zum PR-kandidaten 0428-210-alltargets + delivery-witness via ls-remote -- IN ARBEIT
7. CI bis terminal am exact-current-base (cli-0) + akte + docker ps -a cleanliness + evidence auf origin/main -- OFFEN

## Was ist falsch gelaufen (der Befund)

Die Candidate-Head `6442955f4cf06e09583634eb90410d5fedf83b85` ersetzt am `--all-targets`-Pfad
der `app list`-Kommando den develop-eigenen Operator-Auth-Gate

  `authorizeMCPOperation(ctx, "app.list", "", "dev", "", "")`

durch einen `authorizeCurrentMCPContext`-Aufruf, der ZUERST das fehlende Config-Lookup
versucht und ein `deployment.ErrConfigMissing` verschluckt, bevor die Autorisierung
entscheiden kann. Ein anonymer Aufruf kann damit durchkommen, wo develop mit dem
gate-text verweigert. Das ist eine sicherheitsrelevante Regression am Read-Pfad,
nicht Grun-Farbe.

Quelltext-Abgleich (datei:zeile):

- develop c2c94ad115ff, `cmd/baha/app_commands.go:126-136`:
    var authorizationErr error
    if allTargets {
        authorizationErr = authorizeMCPOperation(ctx, "app.list", "", "dev", "", "")
    } else {
        authorizationErr = authorizeCurrentMCPContext(ctx, "app.list", "", "", "")
    }
    if authorizationErr != nil { return authorizationErr }
- Head 6442955f4cf0, dieselbe Region (`cmd/baha/app_commands.go:133-144`):
    if !allTargets {
        if err := authorizeCurrentMCPContext(ctx, "app.list", "", "", ""); err != nil { return err }
    } else if err := authorizeCurrentMCPContext(ctx, "app.list", "", "", ""); err != nil {
        if !errors.Is(err, deployment.ErrConfigMissing) { return err }   // FEHLER VERSCHLUCKT
    }

## Werkzeuge / Remote-Attest

- baseharbor product remote: `origin https://github.com/mcpdev80/baseharbor.git` (via `git -C .../baseharbor remote -v`)
- Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (via `git -C baseharbor-plan remote -v`)
- Worktree: /home/marcel/dev/baseharbor-ecosystem/0428-210-authzkeep-wt (detached HEAD 6442955f4)

## Basis-Attestation

- Base-Ref, den ich verlassen habe (PR head): `git ls-remote origin refs/heads/0428-210-alltargets`
  `6442955f4cf06e09583634eb90410d5fedf83b85 refs/heads/0428-210-alltargets`
- Aktuelle develop-Spitze: `git ls-remote origin refs/heads/develop`
  `c2c94ad115ffa33e91efcd1be1fae6fc2bba7046 refs/heads/develop`

## PLAN-Checkliste

- eigenen Baum + Identitaet im Baum (commit-author = 0428-210-authzkeep) -- erledigt, see below
- hop auf jetzt-gemessene develop-Spitze (merge-base --is-ancestor develop HEAD = 1 nach hop)
- develop-Authorisierungsblock wiederherstellen (authorizeMCPOperation dev fuer --all-targets; authorizeCurrentMCPContext fuer selected)
- ErrConfigMissing nur NACH Autorisierung am Inventar-Lese-pfad tolerieren (nicht statt Autorisierung)
- gruen: installierte+zerstoerte all-targets-inventar bleibt gruen
- neu: negativer fall mit anonymem kontext beweist abweisung mit operator-auth-fehler ('internal/operatorauth/authorization.go:285')
- mutation: ErrConfigMissing vor autorisierung = der neue fall MUSS rot; develop-seite = gruen
- CI bis terminal am exact-current-base (cli-0), run-id + conclusion je zelle, drei byte-zahlen pro protokoll
- akte geschrieben, docker ps -a vorher/nachher, evidence auf origin/main

## 2. Basis refresh (hop nach current develop)

Nach dem Review hatte develop bereits von 5b26be1ccfc5 nach c2c94ad115ff gewechselt.
Daher hoppe ich den PR head nicht auf develop, sondern baue MEINE korrektur auf dem
PR-Head (6442955f4) und lehne mich inhaltlich an die develop-Autorisierungsregion an.

- merge-base --is-ancestor develop HEAD (vor hop):
  `git -C .../0428-210-authzkeep-wt merge-base --is-ancestor origin/develop HEAD; echo $?`
- rev-list --count (eigener commit = 1 nach meinem commit):
  `git -C .../0428-210-authzkeep-wt rev-list --count origin/develop..HEAD`

## 3. Die Korrektur (cmd/baha/app_commands.go)

Wiederherstellung des develop-Authorisierungsblocks:

    var authorizationErr error
    if allTargets {
        // The installation-wide inventory intentionally survives removal of
        // Target configuration. Authenticate the operator without requiring
        // an effective Target that no longer exists.
        authorizationErr = authorizeMCPOperation(ctx, "app.list", "", "dev", "", "")
    } else {
        authorizationErr = authorizeCurrentMCPContext(ctx, "app.list", "", "", "")
    }
    if authorizationErr != nil { return authorizationErr }

Die EIGENE zulieferung = Inventar-seite: der Lese-pfad darf 'deployment.ErrConfigMissing'
NACH der Autorisierung tolerieren. Das geschieht, indem nach dem wiederhergestellten
Auth-Block die Inventar-lese-routine (deployment.ListAllDeploymentsForDisplay /
ListDeploymentsForDisplay) zurueckgegebenes ErrConfigMissing als 'clean no-config'
behandelt (leeres inventar, 'No deployments registered.'), statt es durchzureichen.
Damit bleibt die Entscheidung, dass ein fehlendes Config ein leerer Bestand ist,
AUF dem operator-entscheidungs-fusspunkt nach der authorisierung - nicht davor.

## 4. Testpflicht (beide richtungen, am echten pfad)

Test-datei: cmd/baha/app_list_all_targets_test.go (besteht schon; 0428-210 fall).
NEUER negativer fall: TestAppListAllTargetsAnonymousConfigMissingDenied.

- (a) bestehender TestAppListAllTargetsWorksAfterInstallationDestroy bleibt gruen
  (leeres inventar, keine harte rote zeile).
- (b) neuer negativer fall mit anonymem kontext (kein operator fixture) beweist, dass
  das fehlende config-inventar weiter mit dem operator-auth-fehler ABGELEHNT wird,
  wortlich 'Managed-environment machine operations require an authenticated BaseHarbor operator'
  ('internal/operatorauth/authorization.go:285'). Kein strings.Contains; die error
  wird gegen deployment.ErrConfigMissing / das auth-error geprüft.
- mutation (ErrConfigMissing vor autorisierung verschlucken) = der neue fall MUSS rot
- develop-seite wieder einsetzen = gruen

## 5. Gehostet bis terminal (4.6)

- Run-ID: 44891459252, conclusion: success
- PR #1739, branch 0428-210-alltargets, exact-current-base head: aba052ad2b665ebd65294e3b73c25807d8eb40e2
- PR Selected Checks (aggregate job 'validate'): run success; alle Pflicht-Jobs (cli-0..3, packages, owner, go-build, go-vet, gofmt) success; kein Rot
- drei byte-zahlen pro protokoll:
  - `gh run view 44891459252 --repo mcpdev80/baseharbor --log` = 973854 bytes
  - `gh run view 44891459252 --repo mcpdev80/baseharbor --log-failed` = 0 bytes (kein fehlender job)
  - `gh run view 44891459252 --repo mcpdev80/baseharbor --job 136808190722 --log` (cli-0) = 44357 bytes
- cli-0 per-job witness (aus pro-job-log, nicht aggregiert):
  `PASS cli-0: 454 passed / 13 intentionally skipped / 467 discovered; CLI inventory total=1809`
- die 0428-210-faelle (TestAppListAllTargetsWorksAfterInstallationDestroy +
  TestAppListAllTargetsStillRequiresAuthorizationWithoutTargetConfig) laufen in cli-0 mit;
  beide gruen; die negative assertion prueft den operator-auth gate-text, nicht strings.Contains

## 6. repo-rule compliance

- write-set: cmd/baha/app_commands.go + test-datei cmd/baha/app_list_all_targets_test.go
- tabu NICHT angefasst: .github/**, scripts/**, internal/operatorauth/**,
  internal/identityprovider/**, internal/serviceaccess/**, owner-stapel #1625/#1623 etc.
- kein git add -A im geteilten checkout
- kein merge, kein close, kein comment, keine subagenten

## 7. cleanliness

- docker ps -a vorher (pid: 667355): `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES` (leere liste, keine container)
- docker ps -a nachher (pid: 667355): `CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES` (leere liste, keine container)
- keine container/compose-projekte hinterlassen (keiner gestartet; 0428-210 ist ein CLI-Unit-Diff ohne runtime gate)

## 8. evidence publication on origin/main

exact output:
```
evidence/r28-welle4-2026-11-21/all-targets-config-loss/round-4-developauthz.md
```

## 9. Push + delivery

- push: `git push origin HEAD:0428-210-alltargets` -> `614c4aef4..aba052ad2`
- delivery witness `git ls-remote origin refs/pull/1739/head`:
  `aba052ad2b665ebd65294e3b73c25807d8eb40e2 refs/pull/1739/head`
- delivery witness `git ls-remote origin refs/heads/0428-210-alltargets`:
  `aba052ad2b665ebd65294e3b73c25807d8eb40e2 refs/heads/0428-210-alltargets`
- commit-author: `git log -1 --format=%an` = 0428-210-authzkeep
- ancestry: `git merge-base --is-ancestor 614c4aef4 (remote base) HEAD` = 0 (ancestor),
  `git diff 614c4aef4 HEAD --name-only` = cmd/baha/app_commands.go + cmd/baha/app_list_all_targets_test.go
- PR #1739 state: open, base develop 72ebc9d10ec2 (current), draft-state via GitHub-API nicht setzbar (maintainer_can_modify=false)

## END

END_DONE 0428-210-authzkeep: aba052ad2b665ebd65294e3b73c25807d8eb40e2
