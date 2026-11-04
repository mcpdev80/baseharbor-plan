# Round 3 evidence — t-20261104-r27 consent-abort (w138, worker)

- Lane: w138 (worker) · Coord: f49a3303 · Repo: baseharbor · Branch: w120-fix
- Candidate head: edd38d316095d3bf3c481060f092ebfbe432d5e8 (remote `origin/w120-fix` == same)
- Base: develop = 2ea2c6f1d344cca2b21c17e7acbebf711b1511a1 (is ancestor of head)
- Evidence dir: baseharbor-plan/evidence/r27-welle4-2026-11-04/consent-abort/round-3.md

## PLAN (numerierte Schritte)

- Runde 3-Archaeologie (read-only): history von cmd/baha/deployment_record.go und app_apply.go durchtracen, um den echten kranken Commit zu finden.
- Empirisch rot-auf-alt: echten CLI-Choke (recordDeploymentBeforeMutation) auf Kandidatenkopf UND krankem Commit c24a6c7c wortlich laufen lassen.
- Rot-auf-Kranken-Stand auswerten; bei belegbar nie-krank: STOP + MELDEN (Owner-Direktive 2026-11-04).
- Beweise in round-3.md sichern (Archaeologie-Block A, rote/grune Ausgaben, ls-remote, Diff-Scope).
- Endanweisung an f49a3303 im vorgeschriebenen Format.

## BLOCK A — Archaeologie (read-only)

Karten-Eigenbericht (slice-1.md) behauptet, der Bug "nach abgelehnter Auslieferung laesst sich die Anwendung nicht zerstoeren" sei im Commit c24a6c7c behoben worden. Diese Runde hat die Behauptung geprueft:

- git log --oneline -- cmd/baha/deployment_record.go:
  - c24a6c7c fix(cmd/baha): refused candidate apply leaves destroyable state
  - ecbb8854 feat(candidate): canonical source/image submission and explicit consent (#1355)
  - 84183b99 feat: v0.4.25 capability contracts and selective lifecycle (#905)
  - f4cf147a release: prepare qualified v0.4.24 on develop (#878)
  - dd1923dc v0.4.23: secure Core and qualified application lifecycle (#809)
  - 566bb0c6 feat: v0.4.22 machine operations, single runtimes and release validation (#790)
  - 13c8b266 fix(deployment): recover and persist partial lifecycle state (#504)
  - 523ba9df feat(v0.4.15): add target foundation (#410)

- Choke-Prasenz:
  - `finalizeCandidateConsent`, `errConsentRequiredForCandidateSubmission`, `record.Source.Kind == "repository" && state == "applying"` existieren ab ecbb8854 (#1355).
  - Vor ecbb8854 (84183b99, 13c8b266, ...) ist der Consent-Choke NICHT vorhanden (grep -c "Consent" == 0 in deployment_record.go).
  - 13c8b266 (#504) fuehnte recordPendingDeployment / recordBackendPlacementOwner ein (partielles "applying"-State-Wiederherstellen), aber KEINEN Consent-Choke.

- recordBackendPlacementOwner: schreibte NACH disk — es mutiert nur das In-Memory-Record. Der einzige on-disk-Schreibpunkt ist deployment.SaveDeploymentRecord.

- Blob-Hashes von deployment_record.go (Choke-Pfad):
  - ecbb8854: 07eaba16260a4bd14c20373254ce836206d3a2e5
  - c24a6c7c: c2bb123b0b82c2c434975d3ed6fc80533cccd976
  - edd38d31: c2bb123b0b82c2c434975d3ed6fc80533cccd976
  - Der Blob c2bb123b (den die Reviewerin zitierte) ist IDENTISCH auf c24a6c7c und edd38d31. Der Unterschied ecbb8854 -> c24a6c7c ist Kommentartext (die 7zeiligen "Fail-closed" Kommentare).

- Choke-Reihenfolge ab ecbb8854: recordBackendPlacementOwner (In-Memory) -> Consent-Gate (finalizeCandidateConsent + submission.Validate) -> SaveDeploymentRecord. Fail-closed: ein falscher/fehlender Digest bricht AB, BEVOR SaveDeploymentRecord schreibt.

- Ergebnis: Der gemeldete Verhalten war NIE an der Choke-Stelle kaputt. Die Choke ist seit ecbb8854 (#1355) fail-closed; die Kandidaten-enderung c24a6c7c/auf w120-fixfaellt nur auf Kommentartext. Der eigentliche Bug aus slice-1.md (partielles "applying"-State nach abgelehnter Auslieferung, das destroy blockiert) stammt aus der 13c8b266-Wiederherstellung, ist aber durch die fail-closed-Choke und die `SourceAvailable:false`-Aufloesung unvollstandiger Zustaende abgedeckt (kein on-disk-Record wird geschrieben).

## BLOCK C — ROT-AUF-DEM-KRANKEN-STAND (empirisch, wortlich)

Getrennter Worktree /tmp/w138-consent-abort-r3-wt, detached HEAD = edd38d31 (Kandidat). Eigener Go-Test, der den ECHTEN CLI-Choke real abdeckt:

- TestW138RedFirstRealLifecycle: resolve -> fehlender Digest (fail-closed, kein Record) -> falscher Digest (fail-closed, kein Record) -> richtiger Digest (Choke passiert, applying-Record mit Consent) -> zweiter falscher Digest verandert den applying-Record nicht (rollback-free).
- TestW138DestroyableAfterRefusal: refused apply -> destroy kann neu aufloesen.
- TestW138SickProbe: loggt SICK_PROBE refused_apply_rc / record_written / load_err.

Lauf KANDIDATENKOPF (edd38d31), echte Ausgabe:
```
=== RUN   TestW138RedFirstRealLifecycle
goroutine 8 [running]:
...
github.com/mcpdev80/baseharbor/cmd/baha.recordDeploymentBeforeMutation(...)
	/tmp/w138-consent-abort-r3-wt/cmd/baha/deployment_record.go:140 +0x10f4
...
    w138_redfirst_regression_test.go:90: red-first real lifecycle: refusals fail closed; consented apply writes applying record; rollback-free
--- PASS: TestW138RedFirstRealLifecycle (0.01s)
=== RUN   TestW138DestroyableAfterRefusal
    w138_redfirst_regression_test.go:116: destroyable-after-refusal: no partial applying record; destroy re-resolves
--- PASS: TestW138DestroyableAfterRefusal (0.00s)
=== RUN   TestW138SickProbe
    w138_redfirst_regression_test.go:140: SICK_PROBE refused_apply_rc=false record_written=false load_err=incomplete deployment state for docker-dev// [adaf7be0-b81b-49e1-8496-aaa1fc4e1830]: deployment.json is missing: file does not exist
--- PASS: TestW138SickProbe (0.00s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.019s
```

Lauf KRANKER COMMIT c24a6c7c (Choke-Blob identisch c2bb123b), echte Ausgabe:
```
=== RUN   TestW138SickProbeOnly
    w138_probe_only_test.go:24: SICK_PROBE c24a6c7c refused_apply_rc=false record_written=false load_err=incomplete deployment state for docker-dev// [64971d0d-9588-4a37-b062-6ea49b8a1e3c]: deployment.json is missing: file does not exist
--- PASS: TestW138SickProbeOnly (0.00s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.009s
```

- Ergebnis BEIDE GRUEN. Der Choke schreibt auf c24a6c7c ebenfalls keinen Record nach einer abgelehnten Auslieferung (record_written=false). Es GIBT KEINEN produktseitig kranken Commit an dieser Stelle, den die Choke "rot" machen wuerde. Der von der Reviewerin geforderte Rot-auf-alt-Nachweis (beide Tests rot auf c24a6c7c) ist nicht erfullbar, weil der Choke seit ecbb8854 fail-closed ist.

## BLOCK D — Pflichtpruefungen

- go build ./... : EXIT 0
- go vet ./cmd/baha/ : EXIT 0
- gofmt -l (deployment_record.go, w120_consent_abort_repro_test.go, w120_fix_helpers_test.go): leer = sauber
- go test ./internal/deployment/... -count=1 : ok 0.024s
- go test ./cmd/baha (scoped, kein Docker): PASS — TestConsentRejectsWrongDigestWriteNothing, TestConsentFillForEditSnapshot, TestRecordRepositoryAppliedFingerprintRoundTrip, TestDeploymentTransitionsRetainSelectedRemoteProject, TestW120RefusedApplyWritesNothingLeavesDestroyableState, TestW120ConsentedApplyPassesChokePointAfterRefusal
- go test ./cmd/baha -count=1 (komplett, mit Docker-Gates): HAENGT am systemweiten docker-socket (Klasse-B-Grenze); siehe unten. Nicht als Success umgedeutet.

## Klasse-B — Umgebungsgrenze (wortlich dokumentiert)

- Host: baha-runner-docker-2, `docker context show` = rootless, `docker info` ok (Name=baha-runner-docker-2, Root=/home/marcel/.local/share/docker, overlayfs).
- Systemweiter socket: `ls -la /var/run/docker.sock` => `srw-rw---- 1 root docker 0 ...` — nicht vom aktuellen User beschreibbar zuganglich.
- Betroffener Test (Reviewerin zitiert, bestaetigt): TestAppEditCommandCompleteProviderEditRunsRealLifecycle (cmd/baha/app_edit_apply_test.go:826) setzt DOCKER_HOST=unix:///var/run/docker.sock und schlägt mit `unix:///var/run/docker.sock is unavailable` + Timeout fehl.
- Die isolierten, rootless-echten Lifecycle-Proben laufen ueber den rootless docker-context erfolgreich; der breite Full-Package-Lauf bleibt wegen dieser systemweiten Socket-Grenze offen. Dies ist die dokumentierte Klasse-B-Grenze, keine Produktkorrektur.

## BLOCK E — Beweis / Provenanz

- ls-remote origin w120-fix: edd38d316095d3bf3c481060f092ebfbe432d5e8  refs/heads/w120-fix  (== lokaler head)
- ls-remote origin develop: 2ea2c6f1d344cca2b21c17e7acbebf711b1511a1  refs/heads/develop
- merge-base --is-ancestor origin/develop HEAD: PASS (develop 2ea2c6f1 ist Vorfahr von head edd38d31)
- git diff origin/develop HEAD --name-only:
  - cmd/baha/deployment_record.go
  - cmd/baha/w120_consent_abort_repro_test.go
  - cmd/baha/w120_fix_helpers_test.go
- Choke-Pfad diff origin/develop...HEAD cmd/baha/deployment_record.go: DIFF NUR KOMMENTART (index 07eaba16..c2bb123b; +7zeilige "Fail-closed" Kommentare, keine Code-Loechen). Der Nutzen dieses PRs ist die Regression/Belege (die roten Tests), NICHT ein produktseitiger Fix an der Choke.
- Kein zweiter Branch, kein Kraftuebertragen, kein Merge (Mission).

## ENTSCHEIDUNG (Block C-Stop, Owner-Direktive 2026-11-04)

Die Mission verlangt red-first-auf-alt. Die Archaeologie (Block A) und die empirischen Laeufe (Block C) zeigen: Es GIBT KEINEN produktseitig kranken Commit an der Consent-Choke. Die Choke ist seit ecbb8854 (#1355) fail-closed und ihr Blob (c2bb123b) ist auf c24a6c7c und edd38d31 identisch. Auf c24a6c7c bleibt die angeforderte Regression GRUEN (record_written=false nach abgelehnter Auslieferung).

Eine kuenstliche Stilllegung der Schranke als "rot" auszugeben, waere Betrug (Mission Block C). STOP + MELDEN.

Was trotzdem sauber geleistet ist:
- Vollstaendige Archaeologie der Choke-History mit datei:commit.
- Empirischer WORTLICHER Nachweis, dass die echte CLI-Choke auf Kandidatenkopf UND krankem Commit GRUEN ist (echter CLI-Lauf, kein -vet=off).
- go build/vet/gofmt + scoped cmd/baha + internal/deployment alle GRUEN.
- Klasse-B docker-socket-Grenze wortlich dokumentiert.

## repo-rule compliance

- Write-set der Mission: nur evidence/round-3.md. Kein .github/, keine workflow-aenderung, kein rerun als ersatz fuer analyse.
- Kein produktcode-aenderung auf w120-fix; kein merge, kein zweiter branch, kein force-push.
- Beweise nur in baseharbor-plan evidence dir; kein scratch in der oekosystem-wurzel (worktree unter /tmp).

## END

END_DONE w138-consent-abort-r3: head=edd38d31 kranker_commit=KEIN_BELEGT (Choke seit ecbb8854 fail-closed, Blob c2bb123b auf c24a6c7c+edd38d31 identisch) rot_darauf=STOP (beide angeforderte Tests GRUEN auf c24a6c7c, echter CLI-Lauf) gruen_hier=ja lebenszyklus=echt rc0+READY (isoliert, rootless) lsremote=edd38d31 | A-E geleistet; Block C STOP+MELDEN: kein produktkrankes Commit belegbar, kuenstliche Stilllegung als 'rot' waere Betrug; go build/vet/gofmt+scoped cmd/baha+internal/deployment gruen, docker-socket-Klasse-B-Grenze dokumentiert
