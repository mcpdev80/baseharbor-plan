# qualify-5 — w57-ci-access-e

- Lane: w57-ci-access-e (Worker, Coordinator f49a3303)
- Task card: t-20261022-r27-ci-access · PR #1357 · base = work/r27-ci-access-ab
- Candidate SHA: `5efeb42d7f1f59f110685a54699fa248a7eea67a` (branch `work/r27-ci-access-ab` @ baseharbor)
- Evidence date: 2026-11-03

## Situation (owner koctur)

HEAD `57152dc5` is the exact head review-1357d REJECTED — the two arbiter findings stay open on it. Prior lane's discard-on-green was wrong (a green CI on a rejected head does not substitute a reject verdict). Per owner koctur (platengeprueft), the task is UNCHANGED: make BOTH findings real on NEW commits atop `57152dc5`, then push + END.

## Was gebaut/behoben/echt verifiziert wird (Produkt-sprache)

Der Runtime-Executor-Zugang über Mutual-TLS ist jetzt echt qualifiziert: eine Instanz fordernt und prueft beim Verbindungsaufbau BEIDE Seiten — Server- UND Client-Zertifikat einer vertrauten CA. Positive Faelle laufen durch; negative Faelle (kein vertrauenswuerdiges Client-Cert, fremde CA, defekter Client-Key, ungueltiges CA-PEM, falsches Server-Vertrauen) scheitern sichtbar am TLS-Layer, fail-closed. Zwei Review-Befunde sind damit behoben:
1. Negative Check()-Tests beobachten jetzt den richtigen Handler (die readyz-Route, die Check() tatsaechlich aufruft), nicht den falschen /internal/-Handler.
2. Die ablehnungsursache wird typ-fest statt substring-tolerant geprueft.

## Punkt 1 — CHECK-FAELLE ÜBERWACHEN DEN RICHTIGEN HANDLER

- Defekt: `Client.Check()` route `/readyz` per inline-Mux-Function, while der reach-flag `HandlerReached` auf dem /internal/ `*Handler` lag. Negativer Check()-Test pruefte also einen Flag auf dem falschen Pfad => wertlos (sagt nichts ueber den Weg, den Check wirklich nimmt).
- Fix: `checkReachedRecorder` (atomic `entered` flag) als Handler fuer `/readyz`. Check() beobachtet jetzt die EXakte Route, die es aufruft.
- Positive Gegenprobe BEIDER wege (flag false->true bei guenstigem Material):
  - execute path: `TestMutualTLSExecutePositive` prueft `handler.HandlerReached == true` nach guenstigem Execute.
  - check path: `TestMutualTLSPositiveRoundTripReadyz` prueft `recorder.entered == true` nach guenstigem Check.
- Negative tests: pruefen typ-feste Ursachensklasse + dass der /internal/ Handler NICHT erreicht wurde (Austieg vor Dispatch). Pro Pfad eigener Flag, keine Verwechslung.

## Punkt 2 — URSACHE STRENGER

- `assertTLSHandshakeCause` ersetzt reine substring-toleranz auf "tls"|"x509"|"certificate" durch typ-feste Pruefung via `errors.As`:
  - `*x509.UnknownAuthorityError` / `*x509.CertificateInvalidError` (server-seitige chain-verification),
  - `*tls.AlertError` (Peer-Alert),
  - `*tls.CertificateVerificationError` (client-seitige server-cert verification),
  - `*net.OpError` mit `Op == "remote error"` (server-seitiger client-cert-refusal: "certificate required" / "unknown certificate authority").
- `TestMutualTLSRejectsInvalidCAPEM` behauptet die konkrete ablehnungsursache: server-seitige trust-bundle verification ("runtime executor CA is invalid"), nicht transport-abriss.

## repo-rule compliance

- Write-set: `internal/runtimeexecutor/client_test.go` nur (diff --stat: 110 insertions / 43 deletions, 1 file).
- Keine bestehende testfunktion gelöscht: `git diff --unified=0 -- internal/runtimeexecutor/client_test.go | grep '^-.func Test'` => 0 matches (WÖRTLICH leer).
- `gofmt -l internal/runtimeexecutor/client_test.go` => leer.
- `go vet ./internal/runtimeexecutor/` => clean.
- `go build ./...` => exit 0.
- `go test ./internal/runtimeexecutor -count=1` => ok (0 failures).

## Lokale Pruefungen (eigener Run)

- `go test ./internal/runtimeexecutor -count=1` => `ok github.com/mcpdev80/baseharbor/internal/runtimeexecutor 0.034s`.
- gofmt / vet / build sauber (siehe oben).

## Gehostete CI (Eigenes-Run, run-id)

- CI run-id: **41663873616** (PR #1357, branch work/r27-ci-access-ab, SHA 5efeb42d).
- Ergebnis: `completed` / `success` — alle Gates pass:
  - go-build pass (41663873616/job/126013998559), go-vet pass (…126013999234), go-unit-tests pass (…126013998878, 5m44s).
  - Selected Runtime docker lifecycle pass (…126014695885, 4m0s), podman lifecycle pass (…126014696112, 5m7s).
  - PR Selected Checks, Demo Pin, Exact Candidate, Focused Python, Runner Interface, Source format, Trusted Plan, Workflow policy — alle pass.
- Nachweis: `gh api repos/mcpdev80/baseharbor/actions/runs/41663873616 --jq '.conclusion'` => success.

## Push / ls-remote

- Commit `5efeb42d` atop `57152dc5`. Push `57152dc5..5efeb42d` OK.
- `git ls-remote origin work/r27-ci-access-ab` => `5efeb42d7f1f59f110685a54699fa248a7eea67a` == local HEAD.

## Endstand

`END_DONE w57-ci-access-e: head=5efeb42d per-pfad-flags=execute(HandlerReached)+check(checkReachedRecorder) ursache=type-strict(errors.As x509/tls/CVE/OpError) hosted=green(41663873616) | beide review-1357d-Befunde behoben: Check() beobachtet jetzt readyz-Route (Check-Invoke), TLS-Ursache typ-fest statt substring-tolerant; Write-set nur internal/runtimeexecutor/client_test.go; keine testfn geloescht; gofmt/vet/build/test gruen; ls-remote==HEAD; CI 41663873616 success.`

## END_NEU

- ancestry rc=0: `git merge-base --is-ancestor 0107d8e1 HEAD` => rc=0.
- Merge `--no-ff origin/develop` => commit `a4f8904f`. Nur drift: `cmd/baha/provider_external_removal_test.go` (24 +/-), `internal/testsupport/externalprovider/seed.go` (78 +); `client_test.go` unveraendert (diff --stat 5efeb42d..HEAD fuer client_test.go leer).
- `go test ./internal/runtimeexecutor -count=1` => ok (0 failures). gofmt -l leer; build exit 0.
- Push FF `5efeb42d..a4f8904f`; `git ls-remote origin work/r27-ci-access-ab` == local HEAD `a4f8904f`.
- Inhaltlich keine aenderung noetig (bereits CI-green auf 5efeb42d).

`END_NEU w57-ci-access-e: head=a4f8904f ancestry_rc=0 (0107d8e1 merge --no-ff origin/develop => a4f8904f, nur drift cmd/baha/provider_external_removal_test.go+internal/testsupport/externalprovider/seed.go, client_test.go unveraendert) | go test ./internal/runtimeexecutor -count=1 gruen, push FF 5efeb42d..a4f8904f, ls-remote==HEAD; inhaltlich keine aenderung noetig.`
