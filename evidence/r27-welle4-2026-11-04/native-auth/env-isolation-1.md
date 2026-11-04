# w94 — native auth env-isolation fix (PR #1362)

## Kontext
- MIKRO-KORREKTUR PR #1362, branch work/r27-native-auth, head ed0c99b1.
- Hosted go-unit-tests failt GENAU zwei faelle: TestSSHAgentAvailableNoKey + TestSSHAgentAvailableWithKey (run 41804058880).
- Krankheit: die tests vertrauen auf SSH_AUTH_SOCK-welt des laufers (umgebungs-erwartung statt isolation) — identisch zu frueheren nahtstellen-befunden.

## Befund (root cause)
- sshagent.go: SSHAgentSource.Available() ruft os.Stat(s.envVar("SSH_AUTH_SOCK")).
- native_test.go hartkodiert Env => "/run/user/1000/openssh_agent".
- Auf dem hosted runner existiert dieser sockel-pfad NICHT => Available() gibt false zurueck => HasKey gibt ErrSSHAgentUnavailable => beide tests scheitern.
- Lokal (hier) existiert der pfad zufaellig (my uid 1000 owns /run/user/1000), daher hier green — bestaetigt umgebungs-abhaengigkeit.

## Fix (tests only)
- native_test.go: BEIDE faelle via t.Setenv("SSH_AUTH_SOCK", pfad-zu-eigenem-socket-im-tempdir) isolieren.
  - "with key": temp-socket + fakeRunner mit key-line => Available()=true, HasKey=true.
  - "no key": temp-socket + fakeRunner mit leerer output => Available()=true, HasKey=false.
- KEIN produkt-aenderung (sshagent.go unveraendert). KEIN skip. KEIN loeschen. Erwartungen (assertions) unveraendert.

## Verify
- go test ./internal/credential/... -count=1 => gruen (beide faelle gehaertet, isoliert).
- gofmt -l ./internal/credential/... => leer.
- go vet ./internal/credential/... => leer.
- diff sshagent.go => unveraendert (nur native_test.go geaendert).

## Push
- branch work/r27-native-auth gepusht.
- ls-remote origin work/r27-native-auth == head nach push (fixieren).

## PR #1362 gates
- run-id 126502703868 (PR Selected Checks, terminal=success).
- go-build=success, go-vet=success, go-unit-tests=success, all source/selected required terminal gruen.
- source+selected required gates terminal.

## repo-rule compliance
- Nur test-datei geaendert. Keine produkt-aenderung. Kein skip/loeschen. Erwartungen (vertrag) unveraendert.
- Nur gezieltes git add <datei> im worktree.

## END
END_DONE w94-nativeauth-env: head=c2adcc864f faelle=2/2 gehaertet lsremote=c2adcc864f | PR #1362 gates terminal gruen (run-id 126502703868; go-unit-tests/go-vet/go-build success); sshagent.go unveraendert, nur native_test.go isoliert
