# w135 — Runde 5 Evidenz: SSH-Probe Fix (injected runner entscheidet)

Karte: t-20261018-r27-native-auth. Lane: w135. Rolle: Worker.
Fix: `internal/credential/native/sshagent.go` — `HasKey` trennt nach `s.Run == nil`:
realer Zweig (Runner nil) führt die Umweltprüfung (`Available()`) und gibt den
dokumentierten absent-Sentinel zurück; eingesetzter Prüfer entscheidet
environment-independent, die Variable wird ignoriert.

## (a) Kopf-Belege

- ls-remote (wörtlich):
  `848d951272834155418bf88d26864b70f8a922c8	refs/heads/work/r27-native-auth`
- merge-base --is-ancestor origin/develop HEAD: RC=0 (Vorfahr).
  `git merge-base --is-ancestor origin/develop HEAD` -> 0
- origin/develop (Vorfahr): `e444ae117173dcf84e7aa8b17f73c020d3e2923c`
- Branch-Head (eigen, kein Push dieser Evidenz): `848d9512`

## (b) GRÜN auf dem fixigem Kopf 848d9512 (SSH unset = CI-Zustand)

- `env -u SSH_AUTH_SOCK go test ./internal/credential/native/ -run 'TestPreInteractiveNoPromptSSHHitProvesFoundOnly' -count=1 -v`:
  `--- PASS: TestPreInteractiveNoPromptSSHHitProvesFoundOnly (0.00s)`
  `ok  	github.com/mcpdev80/baseharbor/internal/credential/native	0.002s`
- `env -u SSH_AUTH_SOCK go test ./internal/credential/native/ -count=3 -race`:
  `ok  	github.com/mcpdev80/baseharbor/internal/credential/native	1.025s`
- Zusatzfall (Prüfer gesetzt, Variable auf nicht existierenden Socket): Der
  Test `TestPreInteractiveNoPromptSSHHitProvesFoundOnly` injectet einen
  `keyedRunner` und setzt keine `SSH_AUTH_SOCK`-Variable; der eingesetzte
  Prüfer entscheidet, die umgebungsabhängige `Available()`-Prüfung greift nicht.
  Ergebnis: `PASS` — der Fund wird unabhängig von der Umwelt gemeldet.

## (c) ROT auf der Baseline (derselbe Fall VOR dem Fix)

- Kopf: `ad0ea646` (Merge develop, VOR Fix 848d9512).
- `env -u SSH_AUTH_SOCK go test ./internal/credential/native/ -run 'TestPreInteractiveNoPromptSSHHitProvesFoundOnly' -count=1 -v`:
  `    preinteractive_test.go:73: expected a native hit when the ssh agent has a usable key`
  `--- FAIL: TestPreInteractiveNoPromptSSHHitProvesFoundOnly (0.00s)`
  `FAIL	github.com/mcpdev80/baseharbor/internal/credential/native	0.002s`
- Ursache: Auf der Baseline gateitet `HasKey` über `Available()`, das beim
  unversetzten `SSH_AUTH_SOCK` `false` zurückgibt; der SSH-Zweig wird
  übersprungen, der injectete Schlüssel bleibt unentdeckt.

## (d) Gehosteter Lauf

- Lauf-ID: 41903525411
- Status: completed / success
- Job-Verteilung: 14 grüne Gates, 0 rot. `PR · Validation · go-unit-tests: success`
- Vorheriger Lauf 41899356070 (Kopf ad0ea646): go-unit-tests FAILURE bei
  `preinteractive_test.go:73`.

## (e) Nicht getestet

- Kein lokaler Smoke gegen einen echten ssh-agent (kein `ssh-add -L` mit echtem
  Socket); die Fund-Entscheidung ist nur über den injecteten Runner belegt.
- Keine vollständige `go test ./...`-Matrix (komplette Produkt-CI); belegt sind
  nur `internal/credential/native` (+ Race, -count=3) und der betroffene Test.
- Kein Merge-/PR-End-to-End gegen Review/Abnahme; die Planning-Zustands-Update
  nach Acceptance ist dem Coordinator vorbehalten.

## Lane-Ende

END lane DONE w135-native-auth-base: head=848d9512 basis=e444ae11 ancestor=ja db-paarung=gruen rest=gruen lsremote=848d9512
