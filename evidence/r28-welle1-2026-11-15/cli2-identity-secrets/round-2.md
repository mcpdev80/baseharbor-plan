# r28-welle1-2026-11-15 · t-20261114-r28-cli2-identity-secrets (0428-057) — round-2

Shift r28-welle1-2026-11-15 · card t-20261114-r28-cli2-identity-secrets · mission `mission-secrets-r2fmt.md`
Worker session: `d4212c96-16b8-4fe3-a6ef-587d20c0e0d0` · model: Ornith-Laptop (verified at spawn via `codeman agent list`).

## PLAN (numbered, AGENTS 4.4)

1. Mission lesen; base head `6f0555c447` via `git ls-remote` verifizieren; wt von exakt diesem SHA aufsetzen; Ancestry-Check.
2. gofmt `-l` auf `internal/operatorauth/authorization.go` (base-parity r2, r28 belegt Signatur F = 'gofmt required'); diff gegen `gofmt -d` prüfen.
3. gofmt `-w` auf NUR diese Datei (reine Struct-Ausrichtung, kein Inhaltswandel); whitespace-stripped diff = leer.
4. `go build ./...` + `go vet ./internal/operatorauth/ ./internal/machine/ ./cmd/baha/` + zielgezielte secret/auth Tests.
5. fmt-commit auf Branch `cli2-identity-secrets-head` (FAST-FORWARD, KEIN `-f`), push, HEAD-SHA sichern.
6. `git log origin/<base>..HEAD` = nur eigene commits; Draft bleibt.
7. Evidence akte + tick todo-board; evidence auf origin/main; END_DONE post.

## REALITY WITNESSES (git ls-remote)

- baseharbor develop: `731e3bb84fb667f6eae675c43da1043eb47c517b`
- baseharbor cli2-identity-secrets-head (mission base): `6f0555c447514a37a41a09983c5015b4879f4170`
- baseharbor PR #1615 (GitHub API): state open, draft true, head sha `6f0555c447`, base `018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc`

## BASE ATTESTATION

- Base product ref (cut from): `cli2-identity-secrets-head` @ `6f0555c447514a37a41a09983c5015b4879f4170`.
- Branch cut: `cli2-identity-secrets-head-fix` an exakt `6f0555c447` (`git checkout -b ... 6f0555c447...`).
- `git merge-base --is-ancestor 6f0555c447514a37a41a09983c5015b4879f4170 HEAD` → TRUE.
- FF-check: `git merge-base --is-ancestor 6f0555c447 HEAD` → TRUE (fast-forward only).
- `git log origin/cli2-identity-secrets-head..HEAD` listet NUR meinen commit `5008b991`.

## SCOPE

- Round-1 (commit `07661edbc00885c9b9610936aec2fb5310203f8b`) implementierte `secret.reveal`-Mechanism B auf `internal/operatorauth/authorization.go` (head `6f0555c44`).
- r2 = BASE-PARITY nur: `gofmt`-Rueckfall auf genau diese Datei. Kein Inhaltswandel, kein zweiter Branch, kein Merge/ready/force/`.github/**`-Edit.
- Write-set: NUR `internal/operatorauth/authorization.go`.

## GOFRMT VOR/NACHHER (gofmt -d, Round-1 -> Round-2)

```diff
diff internal/operatorauth/authorization.go.orig internal/operatorauth/authorization.go
--- internal/operatorauth/authorization.go.orig
+++ internal/operatorauth/authorization.go
@@ -316,11 +316,11 @@
 		)
 	}
 	decision := AuthorizationDecision{
-		ContractVersion:   AuthorizationContractVersion,
-		Operation:         "secret.reveal",
-		Allowed:           true,
-		Safety:            machine.SafetyReadOnly,
-		Actor:             MachineActorRef{Mode: "authenticated", Issuer: strings.TrimSpace(principal.Issuer), Subject: strings.TrimSpace(principal.Subject)},
+		ContractVersion: AuthorizationContractVersion,
+		Operation:       "secret.reveal",
+		Allowed:         true,
+		Safety:          machine.SafetyReadOnly,
+		Actor:           MachineActorRef{Mode: "authenticated", Issuer: strings.TrimSpace(principal.Issuer), Subject: strings.TrimSpace(principal.Subject)},
 	}
 	setAuthorizationDecision(ctx, decision)
 	return nil
```

- whitespace-stripped `git diff -w` ist LEER -> Inhalt unveraendert, reine Spaltenausrichtung.
- `gofmt -l internal/operatorauth/authorization.go` nach `-w`: leer (clean).

## ACTUAL LOCAL RESULTS (build + vet + tests, exit 0)

```
$ gofmt -l internal/operatorauth/authorization.go     # leer = clean
$ go build ./...                                      # exit 0 (FULL BUILD OK)
$ go vet ./internal/operatorauth/ ./internal/machine/ ./cmd/baha/   # exit 0 (VET OK)
$ go test ./internal/operatorauth/ ./internal/machine/
ok  github.com/mcpdev80/baseharbor/internal/operatorauth   0.301s
ok  github.com/mcpdev80/baseharbor/internal/machine        0.003s
$ go test ./cmd/baha/ -run 'TestAppEnvMasks|TestAppCredsReveal|Reveal|Secret|Reveal'
ok  github.com/mcpdev80/baseharbor/cmd/baha   34.019s
```

- Alle Zieltests (secret.reveal / human-operator / app.env --reveal / app creds --reveal) gruen; kein Regression.
- Pre-existing: kein neuer Test eingefuehrt; r2 faehrt nur gofmt, es bedarf KEINER CI-Trigger-Anderung (kein neuer Test).

## DELIVERABLE

- Branch: `cli2-identity-secrets-head-fix` → HEAD `5008b991c8e12431bfecbbf32298f539c31dfd2e`
- Commit: `5008b991 style: gofmt internal/operatorauth/authorization.go (base-parity r2, struct alignment only, content unchanged)`
- Push FAST-FORWARD: `6f0555c4..5008b991` (KEIN `-f`, KEIN force-push). Remote HEAD nach Push: `5008b991c8e12431bfecbbf32298f539c31dfd2e`.
- PR #1615: DRAFT, state open, draft true, head zeigt jetzt `5008b991` (via GitHub API commits-Liste). Draft-Flag bleibt.
- Kein Merge, kein ready_for_review, kein `.github/**`-Edit, kein workflow_dispatch, kein subagent.

## EVIDENCE LAYOUT (baseharbor-plan ONLY, nie ein Produkt-Repo)

- Path: `baseharbor-plan/evidence/r28-welle1-2026-11-15/cli2-identity-secrets/round-2.md`
- Kein `.evidence/`-Verzeichnis in einem Produkt-Repo; kein main-Branch-Write in baseharbor.
- Worktree: `/tmp/opencode/cli2-identity-secrets-r2fmt-wt` (cleanliness: nur fmt-Change + diese akte, keine Container/compose).
- Kein compose/runtime Projekt gestartet (keine Container, kein daemon-Ressourcen-Verbrauch).

## END

- DONE. Candidate SHA: `5008b991c8e12431bfecbbf32298f539c31dfd2e` (branch `cli2-identity-secrets-head`, base `6f0555c447`, FAST-FORWARD push `6f0555c4..5008b991`, nur eigene Commits; base-is-ancestor verified).
- PR #1615: DRAFT (state open, draft true), head `5008b991`, base `cli2-env-policy-head` @ `018b4e58a`.
- Card: t-20261114-r28-cli2-identity-secrets → `review`, PR #1615, HTTPS evidence link — published to baseharbor-plan origin/main.
- EVIDENCE: evidence/r28-welle1-2026-11-15/cli2-identity-secrets/round-2.md — git ls-remote witness origin/main nach Push (siehe unten).
- gofmt vorher/nachher, ls-remote neue Head `5008b991`, cleanliness dokumentiert.
- Kein compose/runtime gestartet; kein `.github/**`-Edit (Owner scope); kein Merge/ready/force.
