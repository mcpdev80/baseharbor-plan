# PR #1357 Abschlussreview — codex-r1357n

ROLLE=REVIEW, kein Merge. **Urteil: ACCEPT-WITH-DEFERRAL** für den Runtime-Executor-Client-Slice. Reviewer Codex GPT-6 Luna. Geprüfter Commit `e86d39c0ea3e3c516500b87e4589135fbb50aa78`, tree `5d4cbd00b87e7b45ab822a82cc5923255e98ade0`; base/develop `2cadfcee8161ec087b6f50d80fb41428d414f9df` ist Vorfahr. PR #1357 OPEN/READY, mergeable, nicht gemergt. `git ls-remote` vor und nach den Mutationen bestätigt PR-Head `e86d39c0ea3e3c516500b87e4589135fbb50aa78` und develop `2cadfcee8161ec087b6f50d80fb41428d414f9df`. Mutationen blieben in isolierten SHA-genauen Scratch-Archiven; der Produkt-Worktree blieb sauber und unverändert.

## Matrix und Gegenproben

- Der Koordinatorvermerk in `baseharbor-plan/tasks/t-20261022-r27-ci-access.md` (2026-11-04, „Universum-Matrix-Praezisierung“) bestätigt die Load-Phase-Abgrenzung: 8 echte Dispatches plus 4 verweigerte Pfadkombinationen. Im Testcode sind vier konstruierbare Identitätsfälle mit je einem `wrappedCheck` und `wrappedExecute` abgedeckt; das ergibt `combinedPaths == 8`. Die defekten Client-Cert-/CA-Fälle scheitern dagegen vor einem Client-Aufbau. Ihre vier Null-Aufruf-Ausgänge (Readyz- und Execute-Flag für jede der zwei Fälle) werden separat mit konkreten Assertions geprüft und nicht in den Real-Call-Counter eingerechnet. Die Aufteilung ist im Matrixcode sichtbar, nicht nur im Kartenvermerk.
- Counter-Mutation auf dem exakten Head: einen realen `wrappedExecute`-Aufruf aus der ersten Fixture entfernt, Counter-Definition unverändert gelassen. `TestExecuteNeverReachedOnEveryNegativeInput` ging ROT mit `matrix N==M counter mismatch: expected 8 ... got 7`.
- Check-Counter-Gegenprobe: den ersten `wrappedCheck`-Zählerwrapper durch einen direkten `c.Check`-Aufruf ersetzt. Der TLS-Fehler blieb klassifiziert, aber das Matrix-Ende ging ROT mit erwartetem `N=7`.
- Vier unabhängige Load-Phase-Mutationen: in getrennten Archiven jeweils für Row 4 und Row 6 den Readyz-Recorder bzw. Execute-Recorder vor der Originalassertion auf „erreicht“ gesetzt. Jede Probe ging ROT an der passenden Assertion (`row 4`/`row 6`, Readyz/Execute). Die Konstruktor-Ladefehler selbst bleiben davon unberührt.
- Route-Miswire: `/readyz` und `/internal/` im gemeinsamen Testserver vertauscht. Der vollständige Paketlauf ging ROT, darunter `TestMutualTLSExecutePositive`, `TestMutualTLSRejectsMissingClientCertificate` und `TestMutualTLSPositiveRoundTripReadyz` mit den jeweiligen falschen Handlerantworten.

## Kandidat, Tests und Gates

- Gegenüber develop ändert der Kandidat nur `internal/runtimeexecutor/client_test.go` (+2007/0); `internal/runtimeexecutor/handler.go` ist byte-identisch. Keine bestehenden Tests gelöscht oder umbenannt; keine Produktions-Test-Hooks.
- `GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go test ./internal/runtimeexecutor -count=1 -timeout 8m`: PASS (`ok`, 0.081s). `GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go vet ./internal/runtimeexecutor`: PASS. `gofmt -l internal/runtimeexecutor`: keine Ausgabe. `git diff --check` gegen die exakte Basis: PASS.
- GitHub Actions Run [41763640650](https://github.com/mcpdev80/baseharbor/actions/runs/41763640650) auf exakt `e86d39c0` COMPLETED/SUCCESS. `PR Selected Checks`, Workflow policy, Source format, Trusted Plan, Runner Interface, Demo Pin, Focused Python, Exact Candidate, Go build/unit/vet und ausgewählte Docker-/Podman-Lifecycle-Jobs SUCCESS; bedingte und nicht ausgewählte Jobs SKIPPED. Kein Gate wurde umgangen.

## Deferral

Die angekündigte Worker-Evidence `qualify-14.md` ist im Workspace nicht vorhanden. Der technische Befund ist durch die hier reproduzierten Mutationen geprüft; die fehlende Datei ist nachzureichen, bevor die Evidence-Ablage als vollständig gilt. Andere Access-/Gate-Slices werden durch diesen Runtime-Executor-Test nicht neu qualifiziert und bleiben bei ihren jeweiligen Slice-Ownern.
