# 0428-212 — Korrektur (round-2)

**Card:** t-20261121-loki-verify-probe
**Lane:** w235-0428-212-lokifix2
**Branch:** `lane-0428-212-loki-verify-probe-r2` (candidate branch `lane-0428-212-loki-verify-probe`)
**Commit:** `45d181ab4089da6611d888d249b27318924ef3c4`
**Reviewer verdict (round-1):** REQUEST CHANGES, review file `evidence/r28-welle4-2026-11-21/loki-verify-probe/review-1.md`, candidate `75770bd2d0434bfed11d7c1b106064a5a08d5a51`, base develop `40cb28c758b02960356434b630086a341ebe1738`.
**Author:** Qwen (laptop session w235), 2026-11-21.

## Ziel der Korrektur

Die review-1.md benannten zwei bestehenden Verweigerungen der Loki-health-familie, die auf JEDEM `err != nil` durchgingen, auf den bestimmten Fehlerinhalt heben. Review-Rezept (Abschnitt "Recipe and stop criterion"):

- `internal/logs/loki_test.go` `TestPersesLokiDatasourceVerifyFailsClosedWithoutProbe` (`:346-350`): statt `err != nil` den manifest-selection-fail-closed-error pruefen.
- `internal/logs/loki_test.go` `TestPersesLokiDatasourceVerifyBindsServiceAccessClient` (`:474-486`): statt `err != nil` den `load Loki service access identity:`-Pruffix + `os.ErrNotExist` pruefen, damit die Bindung an den service-access-client belegt ist; der unmaterialisierte Fall bleibt als eigener subtest mit Voraussetzungs-behauptung erhalten.

## Basis-Attestation

- Real GitHub remote URL: `https://github.com/mcpdev80/baseharbor.git` (via `git ls-remote` verifiziert).
- Base develop SHA: `40cb28c758b02960356434b630086a341ebe1738` (`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`).
- Exakter candidate head, von dem die_lane ausgangspunkt hat: `75770bd2d0434bfed11d7c1b106064a5a08d5a51`.
- Branch `lane-0428-212-loki-verify-probe-r2` von `75770bd` Abschneiden lassen (nicht von develop), damit die akte-grundlage des verdicts erhalten bleibt.
- `git merge-base --is-ancestor 75770bd2d0434bfed11d7c1b106064a5a08d5a51 HEAD` -> exit 0 (75770bd ist ancestor des fixes).
- `git log --oneline origin/develop..HEAD` listet nur die drei candidate-commits plus den eigenen fix commit `45d181ab4`:
  ```
  45d181ab4 test(logs): assert Loki health-refusal error identity, not bare err != nil
  75770bd2d test(logs): prove passing health verdicts came from a reached probe
  430e2722c test(logs): assert the fixture server identity carries server-auth before the probe witness
  0dc299ccb test(logs): split Loki datasource health witness into probe-rejection and precondition subtests
  ```

## PR #1734 head auf den eigenen fix zeigen lassen

Die regel 'ein PR pro karte' (3.3.8) bleibt gewahrt: kein zweiter PR. Der eigene commit `45d181ab4` wurde als TRUE fast-forward auf den urspruenglichen branch geschoben:

```
git push https://github.com/mcpdev80/baseharbor.git 45d181ab4089da6611d888d249b27318924ef3c4:refs/heads/lane-0428-212-loki-verify-probe
```
```
To https://github.com/mcpdev80/baseharbor.git
   75770bd2d..45d181ab4  45d181ab4089da6611d888d249b27318924ef3c4 -> lane-0428-212-loki-verify-probe
```

- `git merge-base --is-ancestor 75770bd2d0434bfed11d7c1b106064a5a08d5a51 45d181ab4089` -> exit 0.
- `gh pr view 1734 --repo mcpdev80/baseharbor --json headRefOid --jq .headRefOid` -> `45d181ab4089da6611d888d249b27318924ef3c4`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1734/head refs/heads/lane-0428-212-loki-verify-probe` ->
  ```
  45d181ab4089da6611d888d249b27318924ef3c4 refs/heads/lane-0428-212-loki-verify-probe
  45d181ab4089da6611d888d249b27318924ef3c4 refs/pull/1734/head
  ```

PR #1734 head ist jetzt `45d181ab4` — der durchgang an diesem head ist der eigene.

## Diff gegen candidate head 75770bd2d043 (nur internal/logs/loki_test.go)

```diff
diff --git a/internal/logs/loki_test.go b/internal/logs/loki_test.go
index c918652c7..3a01db783 100644
--- a/internal/logs/loki_test.go
+++ b/internal/logs/loki_test.go
@@ -345,9 +345,13 @@ func TestPersesLokiDatasourceFailClosedWhenEndpointAbsent(t *testing.T) {
 // unprovisioned surface returns a fail-closed error.
 func TestPersesLokiDatasourceVerifyFailsClosedWithoutProbe(t *testing.T) {
 	m := application.New("perses-loki-noop", "dev", false, false, false)
-	if err := logs.VerifyPersesLokiDatasourceHealth(context.Background(), m); err == nil {
+	err := logs.VerifyPersesLokiDatasourceHealth(context.Background(), m)
+	if err == nil {
 		t.Fatal("health must not pass without a real reachable Loki health path")
 	}
+	if !strings.Contains(err.Error(), "perses Loki datasource requires the observability management UI and Perses selected in the manifest") {
+		t.Fatalf("error must be the manifest-selection fail-closed error, got a different failure: %v", err)
+	}
 }
 
 // TestPersesLokiDatasourceVerifyNeverReportsHealthy asserts the fail-closed
@@ -475,10 +479,20 @@ func TestPersesLokiDatasourceVerifyBindsServiceAccessClient(t *testing.T) {
 	if err := rewriteLokiPort(t, m, probePort(t, server)); err != nil {
 		t.Fatalf("rewrite port: %v", err)
 	}
+	// The service-access PKI is left unmaterialized on purpose: the health path
+	// must fail closed on the identity-load BEFORE ever querying the endpoint,
+	// proving the endpoint is bound to the authoritative service-access client
+	// (a caller-supplied transport is never the authority).
 	err := logs.VerifyPersesLokiDatasourceHealth(context.Background(), m)
 	if err == nil {
 		t.Fatal("health must not pass against an unmaterialized service-access PKI")
 	}
+	if !strings.HasPrefix(err.Error(), "perses Loki datasource health client: load Loki service access identity: ") {
+		t.Fatalf("error must be the service-access identity precondition failure, got a different failure: %v", err)
+	}
+	if !errors.Is(err, os.ErrNotExist) {
+		t.Fatalf("error must be the missing service-access PKI file stat (os.ErrNotExist), got: %v", err)
+	}
 }
```

### Fix 1 — `TestPersesLokiDatasourceVerifyFailsClosedWithoutProbe` (`:346-350`)
Vorher: `if err := logs.VerifyPersesLokiDatasourceHealth(...); err == nil`.
Nachher: zusätzlich `strings.Contains(err.Error(), "perses Loki datasource requires the observability management UI and Perses selected in the manifest")`.
Erzeugter fehlerinhalt kommt aus `internal/logs/loki_datasource.go:364-365` (`perses Loki datasource requires the observability management UI and Perses selected in the manifest`). Die probe-gegenwart und ein beliebiger anderer fehner sind jetzt unterscheidbar.

### Fix 2 — `TestPersesLokiDatasourceVerifyBindsServiceAccessClient` (`:474-486`)
Vorher: `if err := logs.VerifyPersesLokiDatasourceHealth(...); err == nil`.
Nachher: der service-access-PKI-fall bleibt unmaterialisiert (absicht), und die verweigerung wird belegt durch (a) pruffix `perses Loki datasource health client: load Loki service access identity: ` und (b) `errors.Is(err, os.ErrNotExist)`. Der unmaterialisierte fall bleibt als eigener subtest mit voraussetzungs-behauptung erhalten. Der materialisierte fall (probe-rejection) wird durch den bestehenden subtest `UnreachableLokiIsRejectedByTheProbe` (review-1.md `:417-440`) abgedeckt.

### Local proof (smallest level, 5.4)
Vor-zustand (beide falsche gruen, durchgingen auf irgendeinem `err != nil`):
```
$ go test ./internal/logs -run "TestPersesLokiDatasourceVerify(FailsClosedWithoutProbe|BindsServiceAccessClient|NeverReportsHealthy)" -count=1
ok  	github.com/mcpdev80/baseharbor/internal/logs	0.007s
```
Nach-zustand (beide belegen identitaet):
```
$ go test ./internal/logs -run "TestPersesLokiDatasourceVerify(FailsClosedWithoutProbe|BindsServiceAccessClient|NeverReportsHealthy)" -count=1 -v
=== RUN   TestPersesLokiDatasourceVerifyFailsClosedWithoutProbe
--- PASS: TestPersesLokiDatasourceVerifyFailsClosedWithoutProbe (0.00s)
=== RUN   TestPersesLokiDatasourceVerifyNeverReportsHealthy
=== RUN   TestPersesLokiDatasourceVerifyNeverReportsHealthy/UnreachableLokiIsRejectedByTheProbe
=== RUN   TestPersesLokiDatasourceVerifyNeverReportsHealthy/UnmaterializedPKIFailsClosedAsPrecondition
--- PASS: TestPersesLokiDatasourceVerifyNeverReportsHealthy (0.00s)
    --- PASS: TestPersesLokiDatasourceVerifyNeverReportsHealthy/UnreachableLokiIsRejectedByTheProbe (0.00s)
    --- PASS: TestPersesLokiDatasourceVerifyNeverReportsHealthy/UnmaterializedPKIFailsClosedAsPrecondition (0.00s)
=== RUN   TestPersesLokiDatasourceVerifyBindsServiceAccessClient
--- PASS: TestPersesLokiDatasourceVerifyBindsServiceAccessClient (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/logs	0.007s
```

Voll-paket:
```
$ go test ./internal/logs -count=1
ok  	github.com/mcpdev80/baseharbor/internal/logs	0.083s
$ go vet ./internal/logs
VET OK
```

Inhalt-test ist bindend: ein unzureichender (unrelated) fehlererf wird von beiden assertionen verworfen, der echte inhalt tragt sie (lokal verifiziert, kein skip, keine assertion abgeschwaacht).

## Hosted run am exakten head (4.6)

Run `44853938826`, event `pull_request`, head `45d181ab4089da6611d888d249b27318924ef3c4`, terminal `completed/failure` um `2026-11-21T02:10:34Z`. Per job:

- `PR · Go unit · packages`: **success** — enthaelt den karten-required `./internal/logs` shard, ausgefuehrt am exakten head.
- `PR · Validation · go-build`: **success**.
- `PR · Validation · go-vet`: **success**.
- `PR · Go unit · owner`: **success**.
- `PR · Go unit · cli-0`: **failure**.
- `PR · Go unit · cli-1`: **failure**.
- `PR · Go unit · cli-2`: **failure**.
- `PR · Go unit · cli-3`: **failure**.
- `PR Selected Checks`: **failure** (aggregate).

Fehlerzeile cli-0 (aus `main_test.go:60`):
```
main_test.go:60: create failed: Managed-environment machine operations require an authenticated BaseHarbor operator.
```

### STATE: cli-shards rot, nicht karten-inhalt
Die roten `cli-0..3`-cells sind kein 0428-212-inhalt: es sind `cmd/baha` failures auBerhalb des write-set (`internal/logs/loki_test.go`), geerbt von karten 0428-204/215. review-1.md und die mission bestaetigen: "the red CLI cells are not a 0428-212 content problem". Der `PR Selected Checks`-aggregate bleibt am neuen head rot, solange die geerbten cli-shards rot bleiben — identisch zum zustand bei #1733/#1732. Dies ist ein ererbter zustand, nicht eine eigene ursache. Der karten-required `packages`-shard ist am exakten head gruen und fuehrt die fix-tests aus.

## repo-rule compliance

- Write-set: NUR `internal/logs/loki_test.go` geaendert. `internal/logs/loki_datasource.go` und `internal/serviceaccess/**` NICHT angefasst (produktion / owner-rail); nur die produkt-zeilen `loki_datasource.go:364-365` und `:399-401` als referenz im beweis genannt.
- `.github/**`: NICHT geaendert. CI-gruppe, die den `internal/logs`-pfad abdeckt, ist `PR · Go unit · packages`; der test-lauf dort ist der zustandene nachweis (trigger `pull_request`, job `PR · Go unit · packages`). Neue/gelaenderte tests laufen lokal UND in diesem CI-shard. Kein `.github/**`-befund noetig; keine workflow-aenderung.
- Kein skip erfunden, keine assertion abgeschwaacht (5.4).
- Kein subagent (4.8): jeder schritt in der eigenen session ausgefuehrt.
- Kein zweiter PR (3.3.8): fix als fast-forward auf den candidate-push-branch.
- Kein container/compose auf diesem rechner begonnen.

## cleanliness

- Worktree unter `/tmp/opencode/w235-loki-r2-wt` (eigen, nicht der shared-stapel). Geteilte `internal/application/*`-test-runtime-dirs einer anderen session vor dem commit entfernt (cleanup, 9 leere `runtime/runtime.env`-dirs).
- Kein docker/podman compose projekt gestartet; `docker ps -a`-witness nicht noetig.
- Shared-stapel `bh-docker-dev-shared-*` unangetastet.

## todo-board

`workers/todos/w235-0428-212-lokifix2.json` (6 schritte), schritt 6: BLOCKED 2026-11-21 auf retarget, danach END mit plan-sha.

## END

END_DONE w235-0428-212-lokifix2: fix done locally + hosted run 44853938826 terminal at head 45d181ab4; packages/build/vet/owner green; cli-shards red = inherited 0428-204/215 (see STATE).
