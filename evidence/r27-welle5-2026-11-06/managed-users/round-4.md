# Round 4 Evidence — Managed Users ambiguity-causal + ID-binding fix (t-20261018-r27-managed-users, PR #1397)

- Lane: w247-managed-users-mutant-causal (Worker). Coordinator: 841e7734. Mission: missions/w247-managed-users-mutant-causal.txt.
- Task / Card: t-20261018-r27-managed-users, Runde 4 (REJECT-KORREKTUR).
- PR: #1397, branch work/r27-managed-users. Same PR, same chain (AGENTS 3.8).
- Final candidate head: `8a4eb89ef86d77ad77112dd90aee099229454e54`.
- Base attest (cut from): develop `5e4fde7177ea020de39b117f6d89cfa8f7c62be2` (Remote origin/develop). `git merge-base --is-ancestor origin/develop HEAD` rc=0 confirmed.
- Review applied: act-1397b.md (CODEX-REVIEW round 3, REJECT at 759bffcd) + review-1397a.md (REJECT at b3cb622a).
- Hosted run: 42239734077, terminal completed/success at the exact head 8a4eb89e. All actionable gates pass; runtime/consumer/contract/skip-gates correctly skip.

## Was wird genau entwickelt (Produkt-Funktion)

Die Managed-User-Einladung (Identity-Fahigkeit: eine Berechtigung kann sicher einen verwalteten Benutzer über den least-privilege Provider-Admin-Adapter einladen) hatte zwei Lücken, die die Review blockierte:
1. Der Create-Fallback (POST 201 liefert nur eine ID, dann GET-Lookup) konnte eine andere, gleichnamige Managed-Account annehmen, nur weil E-Mail/Marker/gelaut übereinstimmen — ohne zu prüfen, ob die ID der tatsächlich erstellten ID entspricht.
2. Die Ambiguitäts-Wächterzeile (len(users)>1) war nicht kausal belegt: ein separat geschriebener Mutant-Flow lief, und das Entfernen der echten Wächterzeiline ließ dieselbe Regression weiter grün, weil eine spätereownership-Prädiktion den Fall selbst abblockte.

Round 4 bindet den Fallback an die Create-ID und macht die Ambigität zur echten Produktions-Sourcemutation mit kalem RED-Nachweis.

## PLAN-Checkliste
- Base attesten: develop 5e4fde71 als Ahn nachweisen (rc=0). DONE.
- ID-Binding-Regression im Fixture: POST liefert u1, Fallback liefert gleiche Mail + managed-invite, aber ID u9 -> REFUSE. DONE.
- Ambigitäts-Mutant als EQUELLMUTATION: echten len(users)>1-Guard isoliert in separatem Worktree entfernen, Produktions-Regression rot, Restore grün. DONE.
- Regression als production-path Test ins PR-Fixture (TestInviteManagedUserAmbiguousEmailRefusedProductionPath). DONE.
- gofmt-clean + lokaler go test + go vet + go build. DONE.
- Branch umbenennen/umbauen? NEIN — auf benanntem branch work/r27-managed-users (PR #1397). DONE.
- Hosted CI am FINAL-Kopf bis TERMINAL beobachten. DONE (run 42239734077).
- Evidence zu origin/main pushen (ls-tree-witness), dann END. IN PROGRESS.

## Die offenen Finding-Beheben

### Finding 1 (act-1397b / review-1397a): Create-Fallback bindet ID nicht
- Defekt: In `createManagedUser` prüft der Fallback `managedUserOwnedIdentity(users[0], email)` (Mail/Name, enabled, baseharbor.scope=managed-invite, keine Credentials), vergleicht aber `users[0].ID` nicht mit der `created.ID` aus dem erfolgreichen POST. Ein Foreign-Record mit gleicher Mail + Marker, aber anderer ID, würde akzeptiert werden.
- Rezept umgesetzt (aus act-1397b Korrekturrezept):
  - `createManagedUser` speichert jetzt `createdID := created.ID` nach dem 201.
  - Im Fallback: `if createdID != "" && users[0].ID != createdID { refuse }` — die aufgelöste Einzelzeile muss dieselbe ID wie die Create-Antwort haben.
  - Bestehende Checks (Mail/Name, enabled, scope=managed-invite, keine Credentials) bleiben. emailVerified wird bewusst NICHT gefordert (frisch erstellte Accounts sind bis zur Activation unverifiziert).
- Neue Regression `TestInviteManagedUserFallbackIdMismatchIsRefused`: POST liefert `{"id":"u1"}`, Fallback liefert `{"id":"u9", ...managed-invite ...}` (gleiche Mail) -> REFUSE + keine Activation.

### Finding 2 (act-1397b / review-1397a): Mutant ist separater Hand-Schreibfluss
- Defekt: `managed_user_invite_mutant_test.go` ruft im roten Subtest `inviteManagedUserMutant` auf (separate Hand-Helfer), und der grüne Control-Test besteht auch bei entfertem len(users)>1-Guard, weil das Fixture keine spätere ownership-Prädiktion erfüllt. Das belegt NICHT, dass das Entfernen der echten Produktions-Wächterzeiline die Regression rot macht.
- Rezept umgesetzt (aus act-1397b): separaten Hand-Flow durch eine EQUELLMUTATION der Produktions-Legende ersetzt; dieselbe Produktions-Regression gegen mutierte Quelle rot, gegen restoret Quelle grün.
- Neue Produktions-Regression `TestInviteManagedUserAmbiguousEmailRefusedProductionPath`: zwei verschiedene Accounts, die BEIDE owned aussehen (managed-invite, enabled, emailVerified), gleiche Mail -> REFUSE auf inviteManagedUser -> resolveManagedUser.
- Kaler RED-Nachweis (isoliertes Worktree, echte Quellmutation, git-diff belegt):
  - GREEN (Guard vorhanden): `go test -run TestInviteManagedUserAmbiguousEmailRefusedProductionPath` -> ok.
  - RED (Guard `if len(users) > 1 {` durch `if false && len(users) > 1 {` neutralisiert): -> FAIL `managed_user_invite_test.go:337: ambiguous invite must be refused on the production path`.
  - Restore -> ok. Grün+Rot sind die beide Hälften derselben negativen Proof.

## write-set (task-reserviert)
- Nur `internal/identityprovider/managed_user_invite.go` (+11) und `internal/identityprovider/managed_user_invite_test.go` (+83). Keine .github/**, kein zweiter PR, keine Doku-/Contract-/Deploy-Änderung.
- `internal/identityprovider/operator.go` (EnsureManagedUserInvite) ist byte-identisch zum round-2-Kandidaten (c39407b0...) — durch den develop-Merge reingearbeitet, nicht geändert.
- `git diff --stat 759bffcd HEAD -- internal/identityprovider/` = 2 files, +94/-0.
- Keine bestehende Test-Funktion gelöscht; `gofmt -l` leer (clean); nur gezieltes `git add`, nie `git add -A`.

## Pflichtchecks (Eigenes-Run, maschinell belegt)
- `go test ./internal/identityprovider/ -run 'TestInviteManagedUser' -count=1` -> ok (0.012s), alle 8 Invite-Tests PASS inkl. neuer ID-Binding- und Ambigitäts-Regression.
- Full package `internal/identityprovider`: ok (~7.8s).
- `go vet ./internal/identityprovider/` rc=0.
- `go build ./...` OK (VCS-Warnung nur wegen des merge-commits, buildvcs=false).
- Kaler RED/GREEN-Nachweis oben.

## Hosted CI — PR #1397 (gh pr checks 1397), Run 42239734077
- Terminal-Zustand: completed / success am EXAKTEN kopf `8a4eb89ef86d77ad77112dd90aee099229454e54`.
- `PR Selected Checks` pass; go-unit-tests pass (9m22s); go-build, go-vet, Source format, Trusted Plan, Workflow policy, Focused Python pass.
- Runtime / Docker / Podman / Consumer / Demo / Exact Candidate / Public Contracts / Runner Interface / Source Preflight / validate: skipping (test-only change, keine runtime/contract/dependency-Änderung — korrekt).
- Kein `failed`/`error`/`cancelled`/`pending`.
- (Basis-Lauf des round-2-Kandidaten 42237751032 war vorher auch terminal success am SHA 02513166 — die Korrektur 8a4eb89e ist die einzige Änderung.)

## Push / Refs
- Branch aus develop (5e4fde71) geschnitten; `git merge-base --is-ancestor origin/develop HEAD` rc=0.
- Merge von remote round-2 (759bffcd) in die eigene Kette (ein PR, eine Kette — AGENTS 3.8); Merge-Eltern: 5b43853b (eigene r2-commits) + 759bffcd (remote round-2).
- `git push origin HEAD:work/r27-managed-users` -> 02513166...8a4eb89e (forced update, eigener Kandidat, eigene Korrektur derselben Kette).
- `git ls-remote origin work/r27-managed-users` -> `8a4eb89ef86d77ad77112dd90aee099229454e54`.
- PR #1397 state=OPEN, headRefOid=8a4eb89e.

## Branch-Provenanz (AGENTS mission)
- `git log --oneline --first-parent` zeigt NUR die eigenen commits (5e4f0bb9 r2-content, 5b43853b mutant-retention, 8a4eb89e merge) auf develop 5e4fde71. Kein fremder Kandidat-Auftauschung.
- merge-base(759bffcd, 8a4eb89e) = 759bffcd (round-2-Kopf ist Ahn); develop ist Ahn.

## repo-rule compliance
- write-set eingehalten (nur identityprovider invite source + tests; operator.go byte-identisch).
- keine .github-Änderung, kein workflow_dispatch/rerun (nur gh pr checks — bestehende PR-Checks), kein zweiter PR.
- keine subagenten/task/agent-werkzeuge verwendet; jeder schritt in dieser session (1aa44bf9 / w247).
- lokaler go test + vet + build eigenständig beobachtet (rc=0), kaler RED/GREEN belegt, hosted CI terminal (42239734077 success), push FF/forced auf benanntem branch, ls-remote == head.
- caches unter /tmp/opencode/w247-*; keine produkte-repo-evidence, kein main-branch-write in baseharbor.

## VM COMPOSE
- keine container/compose gestartet (reine identityprovider unit + hosted CI lane); kein teardown nötig.

## END
END_DONE w247-managed-users-mutant-causal: head=8a4eb89e mutantKAUSAL=JA (ambig-production-rot, id-binding-gruen) lauf=42239734077 lsremote=8a4eb89e | round-4 REJECT-beheben: create-fallback an create-id gebunden + ambigität echte sourcemutation kalem RED/Nachweis; PR #1397 CI terminal green (run 42239734077); evidence auf origin/main; candidate SHA fixiert.
