# CODEX-REVIEW 0427-176 r2 — PR #1507

ROLLE: REVIEW
URTEIL: KORREKTUR

## PLAN

1. Exakten PR-Head, PR-Basis, develop-Head und Hosted-Run unabhängig prüfen.
2. F1 alpha/beta-Unabhängigkeit und F2 same-key destroy-Fairness gegen den Produktions-Lockpfad prüfen.
3. F3 Dotfile-Erzeugung, Ziel-weiten Scan, Produktionsintegration und Testdeckung prüfen.
4. Urteil samt Korrekturrezept in Planning-Evidence publizieren.

## Stand und Zeugen

- PR #1507 head `425cf9d2a98edd04a8aab8bb10556109e71c378a`.
- GitHub PR API meldet base `develop` bei `b3a8042d18ea60f162a32a51df34a499cad6a237`; `git ls-remote` meldet aktuelles `develop` bei `942111d5a1c43f5257bf1627a966fa9e6c6f24bd`. Der Merge-base ist `b3a8042d18ea60f162a32a51df34a499cad6a237`; Candidate und aktuelles develop sind um je drei Commits auseinander. Die Behauptung „drift 0 / base 942111d5a“ ist daher aktuell nicht bestätigt.
- Run `42590829681` ist `completed/success` auf exakt `425cf9d2a98edd04a8aab8bb10556109e71c378a`. `PR Selected Checks`, go-unit-tests, build, vet, gofmt, destroy-retry Docker/Podman und die angezeigten ausgewählten Unit-/Dokumentationsjobs bestanden. Native Keycloak/Core, Consumer Pins, Demo Pin und mehrere weitere Jobs sind `skipped`; sie werden nicht als bestanden gezählt.
- Planning-Remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`.

## Delta-Bewertung

F1 ist durch `cmd/baha/application_lifecycle_lock_test.go:259-309` wesentlich belastbarer: alpha hält den per-App-Lock bis Test-Cleanup, beta muss innerhalb von drei Sekunden erwerben. Die behauptete target-weite Serialisierung würde damit scheitern.

F2 belegt jetzt gleiches deployment-ID-Keying: `cmd/baha/application_lifecycle_lock_test.go:318-395` lässt Up und Destroy dieselbe App-ID verwenden, prüft echte Lock-Contention vor Freigabe und bounded retry danach. Das erfüllt den beanstandeten Designnachweis für den same-key-Wettbewerb.

F3 ist weiterhin nicht nachgewiesen und im Produktionspfad nicht umgesetzt. `internal/stableid/lock.go:110-129` erzeugt das per-App-Dotfile unter dem kurzen target-weiten Lock; der Lock wird danach freigegeben, während das App-Dotfile bestehen bleibt. `deploymentsHaveAppLocks` steht bei `internal/stableid/lock.go:139-153`, ist aber außer in seiner Definition nur aus Tests aufgerufen; `git grep` zeigt keinen Produktionsaufruf. Der target-weite Produktionspfad in `cmd/baha/application_lifecycle_lock.go:75-79` nimmt weiter nur `coreinstallation.AcquireLifecycleLock`, das den Root-Lock erwirbt und keine App-Dotfiles scannt. Ein bereits laufender App-Lifecycle kann deshalb weiter mit einer target-weiten Mutation überlappen.

Auch `TestLocalAppLifecycleCannotOverlapTargetWideMutation` beweist diese Richtung nicht: `internal/stableid/lock_test.go:152` scannt das Dotfile, bevor die Testzeile 161 den target-weiten Lock nimmt; während des gehaltenen Locks wird nur ein neuer App-Erwerb blockiert. Der Test führt keinen Scan unter dem gehaltenen target-weiten Lock aus und prüft nicht, dass ein echter targetweiter Produktionsaufruf eine bereits laufende App abweist. Zusätzlich liefert `deploymentsHaveAppLocks` bei `ReadDir`-Fehlern `false` (`lock.go:141-143`), also würde ein integrierter Aufrufer einen Scanfehler als „keine aktive App“ interpretieren.

## Korrekturrezept

- Dateien: `internal/stableid/lock.go`, `internal/coreinstallation/lifecycle_lock.go` sowie die targetweiten Produktionsaufrufe, insbesondere `cmd/baha/application_lifecycle_lock.go` und die tatsächlichen Stop/Destroy/Target-Definitionspfade.
- Änderung: einen exportierten targetweiten Erwerbspfad bereitstellen, der den gemeinsamen `.installation.lock` hält, die App-Dotfiles scannt und bei vorhandenem App-Lifecycle oder Scanfehler fail-closed verweigert. Alle targetweiten Produktionsmutationen müssen diesen Pfad benutzen. Dotfile-Erzeugung und Scan müssen dieselbe kritische Sektion verwenden.
- Testanforderung: Produktionspfad-Regression, in der eine App den per-App-Lock hält und eine echte targetweite Mutation nicht beginnt; Gegenrichtung: während targetweiter Lock+Scan gehalten wird, kann keine neue App ihr Dotfile anlegen. Scanfehler muss verweigern. Die F1- und F2-Tests bleiben erhalten. Die Regressionen müssen im gehosteten Go-Unit-Job laufen.
- Stop-Kriterium: kein targetweiter Produktionsaufruf darf eine aktive App überlappen; kein Scanfehler darf als leerer Scan gelten; Run auf exaktem neuen Head terminal erfolgreich. Vor Abnahme muss außerdem PR-Basis beziehungsweise Develop-Drift aktualisiert und erneut sha-genau geprüft sein.

Der aktuelle grüne Run ersetzt weder den fehlenden Produktionsscan noch die nötige Aktualisierung gegen aktuelles develop. Kein Merge.

END 0427-176 r2 REVIEW: KORREKTUR — #1507 `425cf9d2a98edd04a8aab8bb10556109e71c378a`; die F3-Produktionsintegration und der echte Gegenrichtungsbeleg fehlen.
