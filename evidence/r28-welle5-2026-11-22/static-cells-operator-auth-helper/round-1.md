# 0428-231 round-1 — exported operator-auth helper, fan-out of the five sites (variant A)

Stand nach Coordinator-Antwort (ans231.md.g: variant A, citation des Auftragstexts zurückgenommen,Owner-Anordnung der helper-route; Freigabe für genau eine neue Datei in internal/operatorauth).

## PLAN

- (done) 1. Basis neu abgeglichen: ls-remote develop = `52a3c5446f41a1dd8678d99875e4cb1eee67874c` (#1756 gemergt, wie gemeldet); Branch lane-0428-231-static-auth-helper auf develop, base-behind=0. Anmerkung: der Branch-ref existierte lokal im workers/-bookkeeping-repo (Unfall aus der Vorrunde, leer); bereinigt, die echte Lane-Zone ist workers/0428-231-authhelper-wt.
- (done) 2. Fundstellen vollständig ausgelesen und Verhaltensgleichheit gesichert (if-absent vs. force, principal-Argumente): see 'hilfe' section
- (done) 3. Neue Datei internal/operatorauth/test_operator.go (nur diese eine Datei + keine interface/typ-Aenderungen): exports TestOperatorPrincipal, ReadGrantingMembershipProvider, WithVerifiedTestOperator (if-absent-Semantik wie bisher), WithVerifiedTestOperatorForce (force-Semantik wie bisher)
- (done) 4. Fan-out der fünf Dateien, kein Verhaltenswechsel (assert-Pfad identisch); Provider-Definition aus app_env_test.go entfernt
- (done) 5. build/vet/test-compile lokal sauber; bash scripts/ci-fast-check.sh OK (302 tests, 'Workflow policy PASS', OK); commit 5794874302f, push ohne force, PR #1761 (draft) gegen develop; delivery-witness ls-remote branch = 5794874302f; run 44994765677 terminal completed SUCCESS, failed 0
- (done) 6. Akte umgeschrieben auf diesen Stand (diese Datei), ## PLAN behalten
- (pending) 7. END post aan 9142ab1f

## hilfe: welche der fünf Dateien rufen jetzt den helper auf

- `cmd/baha/test_operator_context_test.go` — `testOperatorContext` ist jetzt `return operatorauth.WithVerifiedTestOperator(ctx)` (if-absent Semantik erhalten; Principal-Logik nach PrincipalFromContext unverändert).
- `cmd/baha/app_env_test.go` — die lokale `readGrantingMembershipProvider`-Definition (:51-58 alt) ist ENTFERNT und durch `operatorauth.ReadGrantingMembershipProvider` ersetzt; `runWithIOAndOperator` behält sein EXPLIZITES principal-Argument (ein Force-Helper würde die verschiedenen Test-identitäten überschreiben —文档 in der Datei), nutzt aber den geteilten Provider.
- `cmd/baha/app_export_command_test.go` — beide Stellen (:377, :400 alt) rufen `operatorauth.ReadGrantingMembershipProvider` statt des lokalen Typs.
- `cmd/baha/installation_destroy_native_test.go` — :47 nutzt den geteilten Provider (eigene operator-Principal bleibt, wie zuvor).
- `cmd/baha/target_definition_change_test.go` — ruft unverändert `testOperatorContext`, das jetzt DER EINEN helper-Route folgt (Zeile 41 mit explizitem WithVerifiedPrincipal-Override danach, Semantik erhalten).

Diff-stat (`git diff --stat develop..HEAD`):

```
 cmd/baha/app_env_test.go                     | 20 +++++++-------------
 cmd/baha/app_export_command_test.go          |  4 ++--
 cmd/baha/installation_destroy_native_test.go |  2 +-
 cmd/baha/test_operator_context_test.go       | 13 +------------
```
plus neu: `internal/operatorauth/test_operator.go` (72 Zeilen, einzige neue Datei; `git diff develop...HEAD --name-only` listet exakt diese 5 Pfade).

## Provenance + witnesses

- `git merge-base --is-ancestor 52a3c5446f41 HEAD` → yes (develop 52a3c544 = Ancestor des ersten Commits 5794874302f).
- `git log --oneline origin/develop..HEAD` → genau EIN commit (5794874302f, meiner).
- `git diff origin/develop...HEAD --name-only` → die 5 Dateien oben; KEINE .github/**, KEINE scripts/**.
- Remote: `git remote -v` → `origin https://github.com/mcpdev80/baseharbor.git`; push `52a3c544..579487430 refs/heads/lane-0428-231-static-auth-helper`; `git ls-remote … refs/heads/lane-0428-231-static-auth-helper` = `5794874302f197d0d4ec76d7c2743ba2bfd4288d`; PR #1761 draft=true gegen develop.

## Gehosteter run

- run `44994765677` (pull_request, head 5794874302f): **completed SUCCESS**, failed jobs **0**.
- Draft-Pfad-Sichtbarkeit: `PR · Validation · ${{ matrix.check }}` 137123317416 skipped, `PR · Native · ${{ matrix.id }}` 137123317510 skipped, `PR · Selected Runtime` 137123318152 skipped — bei einem draft PR laufen die selected-checks nicht; der draft-schalter liegt beim Handoff (review-Regel), ich habe ihn nicht umgestellt.

## Checks lokal (kein Ersatz für hosted, nur Vorprüfung)

- `go build ./...` ok; `go vet ./cmd/baha ./internal/operatorauth` ok; `go test -run XXX_NONE -count=1 ./cmd/baha ./internal/operatorauth` = compile-only, keine lifecycle containers; `bash scripts/ci-fast-check.sh` → 'Ran 302 tests … OK' (unittest-suite, keine cmd/baha package tests).

## repo-rule compliance

- Write set: internal/operatorauth/** (genau eine neue Datei — durch die Owner-Direktive in dieser mission für GENAU diese Datei gehoben) + die fünf cmd/baha test-Dateien. Keine product-sematik, keine interface-erweiterung (der Provider nutzt das BESTEHENDE MembershipProvider-Interface), keine .github/**-, keine scripts/**-Änderung. Keine aktion auf PR #1746. Kein merge/close/ready-schalten; PR bleibt draft bis Handoff. Keine subagenten; keine lokalen test-runs als beweis (hosted run ist der beweis). Posten nur an coordinator 9142ab1f.

## cleanliness

cleanliness: nothing started. Eigen pid 2928572. `docker ps -a` BEFORE = 0 entries; AFTER = 0 entries. Keine container/netzwerke/volumes; scratch `/var/tmp/go-cache-0428-231` (cache, bleibt unter /var/tmp); worktree workers/0428-231-authhelper-wt ist meine Lane-Zone.

END 0428-223-testctx DONE (branch lane-0428-231-static-auth-helper, head 5794874302f, base-behind=0, PR #1761, run 44994765677 completed SUCCESS, failed 0, cleanliness: nothing started)
