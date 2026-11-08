# 0427-013 access-wizard — Korrekturrunde r6 (PR #1430)

Lane: flash mission-013-r6. Karte t-20261018-r27-access-wizard (0427-013),
Kandidatenbranch `work/r27-access-wizard`, PR #1430. Auftrag: blockierenden
r5-Befund beheben — `PersistActive` ersetzte die gesamte Profilmap durch das
Snapshot des aktiven Owners und loeschte damit Profile ANDERER owner, die beim
Laden bewusst uebergangen werden (act-1430-review-r5.md, origin/main).

## PLAN

1. Realitaetsabgleich: ls-remote develop + refs/pull/1430/head, Akt act-1430-review-r5.md aus baseharbor-plan origin/main gelesen.
2. Worktree /tmp/opencode/mission-013-r6-wt, Branch w/r27-access-wizard-r6 (lokal) auf PR-head bd5f2f108, Push auf den bestehenden Kandidatenbranch work/r27-access-wizard (kein zweiter Kandidat, AGENTS 3.8).
3. Befund reproben: temporarer CLI-Repro-Test vor Fix => FAIL "BUG: foreign-owner profile deleted by PersistActive" (bestaetigt Befund 1:1).
4. Fix internal/orgconfig/profiles.go PersistActive: Merge je owner-namespace statt Map-Replacement; fremde Owner-Zeilen bleiben unveraendert.
5. Regression cmd/baha/access_wizard_persistence_test.go: TestAccessAssignPreservesForeignOwnerProfile + TestAccessOffboardPreservesForeignOwnerProfile (rot ohne Fix, gruen mit Fix).
6. r3/r4-Pfade (cancel, fail-closed offboarding, multi-target) bleiben gruen; gezielte + breite Checks; lokale Basis-Rotation dokumentiert (siehe unten).
7. Drift-merge origin/develop (zuerst 1fe57f250, dann e39b00043), Push, PR #1430 aktualisiert.
8. CI auf exaktem head 9dd2f779fa terminal beobachten (4.6), ls-remote-Beleg.
9. Evidence round-6.md committen und auf origin/main publizieren.
10. END-Post + Karte auf review.

## Base attestation (PROOF)

- PR-head bei Schichtbeginn: `git ls-remote origin refs/pull/1430/head` =>
  `bd5f2f10838eeadb89bc121a3719427b2bc6c005  refs/pull/1430/head`.
- develop bei Schichtbeginn: `git ls-remote origin refs/heads/develop` =>
  `1fe57f25007413c710e049094c62bf71656b2aa2` (Mission tippte zuletzt f9e207ac0; develop war bereits weiter — 1fe57f250 enthaelt f9e207ac0).
- Branch `w/r27-access-wizard-r6` lokal aus PR-head bd5f2f108 (detached checkout, danach umbenannt); Arbeit wurde auf den bestehenden Kandidatenbranch gepusht (eine Kette, ein Kandidat).
- Drift-merges: `884ee818f` (merge 1fe57f250), `9dd2f779f` (merge e39b00043 = develop-tip bei Push). Ancestry-Zeugen:
  - `git merge-base --is-ancestor bd5f2f108 HEAD` => exit 0.
  - `git merge-base --is-ancestor 1fe57f250 refs/pull/1430/head` (Frisch-Fetch) => exit 0.
- Log-Zeilen bd5f2f108..HEAD vor dem letzten Drift-merge: eigene Commits sind `1c76570ae` (fix) und `884ee818f` (drift-merge); die uebrigen Eintraege sind die develop-Merge-Commits des Drift-merges selbst (Marcel Pfingstgraef = develop-Entwicklung, basisgewollt), kein fremder PR-Kandidat wird aufgegeben: Diff PR#1430 gegen develop enthaelt nur 19 Dateien der Karte + 2 Dateien der r6-Aenderung, keine .github/**.

## Befund-Repro VOR Fix (unabhaengig bestaetigt)

Temporaerer Test (production CLI-Pfad, aktiver owner `persist-acme`,
fremdes Profil `foreign` owner `other-installation` auf prod; assign alice yes):

```
--- FAIL: TestReproForeignOwnerProfileLostThroughCLI (00.00s)
    zz_repro_foreign_r6_test.go:32: BUG: foreign-owner profile deleted by PersistActive; profiles=2
```

Ursache exactly wie in der Akt: `ManagerFromActive` setzt owner aus
`state.Config.Organization` und `LoadProfiles` uebergeht fremde Zeilen
(internal/orgconfig/profiles.go:353); `PersistActive` ersetzte dann
`state.Config.Profiles` komplett durch `ProfileMap(manager.SnapshotProfiles())`
(internal/orgconfig/profiles.go:615-625).

## Aenderung

`internal/orgconfig/profiles.go` `PersistActive`: Merge statt Replace —
fremde Owner-Zeilen (`Owner != "" && Owner != manager.Owner`) werden aus dem
geladenen Dokument unveraendert in die geschriebene Map uebernommen; die
Snapshot-Zeilen des Managers (eigene + legacy-ownerlose) schreiben nur in ihr
(name,target)-Namespace. Bestehende Semantik fuer aktiven Owner bleibt
identisch (bestaetigt durch die un veraendert gruenen r3/r4-Tests).

`cmd/baha/access_wizard_persistence_test.go`: zwei neue Production-CLI-
Regressionen (assign + offboard) mit seeded foreign-owner-Profil; laden den
aktiven Stand neu und verlangen, dass das fremde Profil vollstaendig
(Name/Target/Owner/Scope/Revision/Operations) erhalten bleibt. Rot ohne den
Fix (Zeuge oben plus gezielter stash-Vergleich: beide neuen Tests FAIL
"foreign-owner profile ... must survive the write"), gruen mit Fix.

CI-Aufnahme: die neuen Tests laufen automatisch im bestehenden Job
`PR · Validation · go-unit-tests` (`go test ./cmd/baha`, Trigger: PR ready +
Push auf PR-head; ci.yml:122) — keine Workflow-Aenderung noetig, kein
.github/**-Antrag.

## Lokale Basis-Rotation (Coordinator-Entscheid 2026-11-08, dokumentiert)

Ein breites `go test ./cmd/baha` auf diesem Host zeigt 14-16 FAILS vom Muster
`incomplete deployment state for docker-dev// [...]: deployment.json is
missing: file does not exist` (app_init_*/app_backup_*/app_edit-Tests) sowie
Einzelfaelle `provider "postgresql" ... not found` — environment-Rotation
(lokale State-Verzeichnisse fehlen), KEIN Bezug zu access-wizard/orgconfig.
1:1-Nachweis: gleiches `go test ./cmd/baha -count=1` auf Basis 884ee818f
(ohne den r6-Fix) gegen Head 9dd2f779f-1 => FAIL-Listen differenzfrei
("IDENTICAL-1:1", 16/16 Zeilen identisch). Entsprechend Coordinator-Entscheid
ist das Abnahmetor die gehostete CI (provisionierte Umgebung), nicht der
Local run. Bekannte Basis-Karte 0427-132: Develop-Runtime-Cells rot durch
PR#1448 — falls der PR-Validation-Lauf genau `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndrierung`
(installation_destroy_native_test.go:43, missing deployment state) zeigt, ist
es die Basis, nicht dieser Diff; bisher zeigt der lauf dieses Muster nicht.

## Reviews, Checks, Kandidat
- Fokussiert: `go test ./cmd/baha -run TestAccess` PASS; `go test ./internal/orgconfig/... ./internal/accesswizard/...` PASS (r3 cancel, r4 fail-closed offboarding, multi-target-Persistenz unveraendert gruen).
- `go build ./...` PASS, `gofmt -l` leer fuer die beiden Aenderungsdateien, `go vet` (orgconfig/accesswizard/cmd-Build) sauber.
- Kandidat: PR #1430 head = `9dd2f779fa2445257d4f7f3c99a43b1245493818`
  (`git ls-remote origin refs/heads/work/r27-access-wizard` Zeuge:
  bd5f2f108... -> push -> 9dd2f779f...).
- CI (4.6, selbst beobachtet bis terminal): Run `42438784031` auf exaktem
  head `9dd2f779fa2445257d4f7f3c99a43b1245493818` => `completed / success`.
  Alle erforderlichen Jobs gruen (go-build, go-unit-tests, go-vet,
  wizard-registration-tests, PR Selected Checks, source format, docs,
  documentation-audit); Runtime-Jobs skipped (kein betroffener Pfad). Der
  destroy-retry-Basisfehler der Karte 0427-132 erschien im Lauf nicht.
  CI-Aufnahme der neuen Tests: `go-unit-tests` fuehrt `scripts/pr-unit-database.sh`
  => `go test ./... -count=1` (gh-hosted runner, PostgreSQL-Fixture), also
  laufen beide neuen Regressionen automatisch in diesem Job; Trigger: PR-ready
  und jeder Push auf den PR-head. Kein .github/**-Wechsel noetig.

## repo-rule compliance

- Keine .github/**-Aenderung; keine workflow_dispatch/Reruns durch diese Lane (nur PR-Push auf bestehendem Kandidaten, normaler Check-Trigger).
- Ein Kandidat pro Kette: Arbeit auf work/r27-access-wizard (PR #1430), kein Extra-Branch auf origin; lokaler Arbeitsbranch nur Durchlaufposten.
- Keine Subagenten (4.8); keine Container/compose-Projekte gestartet (kein VM-Teil in diesem Auftrag; ps-Zeuge: nichts zu holen).
- Evidence nur in baseharbor-plan; Zonen-Check: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` => `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, Remote https://github.com/mcpdev80/baseharbor-plan.git. Produkte-Checkout: /home/marcel/dev/baseharbor-ecosystem/baseharbor (workers/baseharbor nur ls-remote-Quelle via dessen Remote, nie als Remote-Zustands-Zeig zitiert).
- Write-Set exakt wie im Rezept genannt: internal/orgconfig/profiles.go + cmd/baha/access_wizard_persistence_test.go.
