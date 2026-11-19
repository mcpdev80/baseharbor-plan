# fix-4 (r5) — 0428-123 regvisibility: explicit provider-file ownership + emitted-glob regression

- Card: t-20261119-hunt-metrics-registration-visibility-only (0428-123)
- PR: mcpdev80/baseharbor#1693 · zweig `lane-0428-123-regvisibility`
- Session: laptop worker session, Modell `worker-ornith1.5-laptop` über AgentGateway verifiziert.
- Review: CODEX-REVIEW REQUEST CHANGES r2 on exact head `97987af6954aca0318a16aef99b19c27dbee231a` (base `7ee6f817dbff5a238bbc651315d6d76b3819fc91`), akte `evidence/r28-welle4-2026-11-19/codex-review-wave/1693-0428-123-r2.md`.
- Evidence provenance: baseharbor-plan `origin/main` (https clone `/var/tmp/plan-123`, fetch+rebase vor Commit).
- Review-only: no code change, card update, or merge by the reviewer.

## Kopf-Folge (97987af6 → 57f49d78)

- 97987af6 (r4): disjoint app-target namespace + namespace reconciliation — bekam REQUEST CHANGES r2 (B2 foreign-provider preservation + B1 emitted-glob regression).
- 57f49d78 (r5, dieser Lauf): Commit `f85d4b0743a01c9662abcbe80ca308597f2f5c0c` + zweiter monotoner merge-hopf auf develop `558dc42d0c8c9d798fcdf5938be2ea14e432b754` (#1701 perses messaging, 18:xx). Run 44587260864.
- Basiswechsel-Zeuge: `git diff --name-only 7ee6f817 558dc42d` → `internal/metrics/perses_dashboards_messaging.go` + `perses_dashboards_messaging_test.go` + testdata. KEIN `scripts/test_pr_*`/`scripts/ci-workflow-policy.sh`, KEIN `.github/workflows`. Per base-abstands-regel also KEIN neuer lauf-pflicht-trigger durch den basiswechsel; der lauf unter 558dc42d ist der gültige kandidat.
- Warum der lauf auf 97987af6 nicht zaehlt: 97987af6 trug die UNFIXED version (b2/b1); die abnahme forderte eine korrektur. Der lauf ist die alte version.

## CI-Beweis (terminal)

- Run-ID: 44587260864, Event pull_request, SHA 57f49d7851c1e2a4d00726dd6ff455a2929b0506, Start 2026-11-19T18:23:21Z.
- Status terminal: **completed/success**. Aggregate `PR Selected Checks: success`.
- Pflicht-Jobs ausgefuehrt und gruen (kein SKIPPED unter Mandatory): go-build, go-vet (success), Go unit owner/packages/cli-0/1/2/3 (alle success), Workflow policy success, Trusted Plan success, Native gate plan success, Source format success, Focused Python success.
- `PR · Go unit · packages` fuehrt ALLE non-CLI Go packages ohne test-filter aus; `internal/metrics` erfolgreich. Die five `TestRegVisibility*`-tests haben kein build-constraint und rufen kein `t.Skip`, also wurden sie in diesem shard ausgefuehrt (nicht nur im tree present).
- Kein ORAS/trust-plane runner-precondition-fehler; HA/runtime-gates von ci-policy als skipped markiert (nicht ausgefallen).
- Provenance: `git merge-base --is-ancestor origin/develop 57f49d78` → rc=0; `git merge-base --is-ancestor f85d4b07 57f49d78` → rc=0; `git merge-tree --write-tree origin/develop 57f49d78` conflict-count=0. PR #1693 head=57f49d78, base=558dc42d, draft=false.

## Die fixes (datei:zeile)

### B2 — blocking — ownership of provider-prefixed files (prometheus_files.go)

- `syncProviderTargets` (:98) leitet jetzt `providerSources` aus den NON-app-quellen ab (`ownProviderNamespace := len(providerSources) > 0`).
- Die deletion-schleife (:131-150) loescht eine `provider--`/`provider-secure--`-datei nur, wenn (a) der sync provider-quellen EIGEN (`ownProviderNamespace`) UND (b) die datei einem aktuell ausgewaehlten provider-source entspricht (`providerSourcePresent(providerSources, name)`). Beim application-only-sync (`ownProviderNamespace == false`) wird der provider-namespace ueberhaupt NICHT angefasst — eine fremde `provider--foreign.json`/`provider-secure--foreign.json` bleibt byte-identisch.
- Damit ist der review-rezept erfullt: "make ownership of provider-prefixed files explicit so application-target reconciliation cannot delete foreign provider JSON; preserve stale-provider cleanup only for files the current sync can prove it owns." Kein viertes objekt nothendig — ownership wird durch die name-matching-gegen-current-sources ausgedrueckt.

### B1 — emitted-glob regression (prometheus_render.go + regvisibility_regression_test.go)

- `TestRegVisibilityProviderFileGlobClassification` ruft `prometheusConfig` auf (der vorherige test tat das nicht) und prueft fuer die slugs `provider` und `provider-secure`: die application-target-datei wird AUSCHLIESSLICH vom `baseharbor-applications`-job glob ausgewaehlt und NIEMAM vom `baseharbor-providers`-job; die echte `provider--<hash>.json`-datei wird vom `baseharbor-providers`-job, nicht vom applications-job, ausgewaehlt. Damit ist die prior-recipe-pflicht erfullt, die EMITTED PATTERNS auszuueben, nicht nur prefix-classification.

## Neue test-ids + gate

- `TestRegVisibilityApplicationNamedProviderIsDisjoint`, `TestRegVisibilityStaleApplicationTargetReconciledOnSync`, `TestRegVisibilityForeignProviderFileSurvivesApplicationReconciliation`, `TestRegVisibilityForeignProviderFilePreservedUnderProviderSync`, `TestRegVisibilityProviderFileGlobClassification` — alle gruen unter `go test ./internal/metrics -run "^TestRegVisibility"`.
- Gate: `go build ./...` rc=0, `go vet ./internal/metrics` rc=0, full metrics+observability package pass, `bash scripts/ci-fast-check.sh` → 280 tests OK, workflow policy PASS, source readability PASS, regression ratchet PASS.
- CI-Aufnahme: alle five tests laufen im existing `PR · Go unit · packages` shard (auto-discovered durch `go test ./...`), pull_request-trigger. Kein `.github/**`-change nothendig (owner-scope); kein change an `scripts/**`.

## Foreign-file before/after hashes (B2)

- `TestRegVisibilityForeignProviderFileSurvivesApplicationReconciliation`: seeds `provider--foreigndeadbeef.json` + `provider-secure--foreigncafed00d.json`, saved byte digests vor dem app-only-sync, asserted byte-identisch nachher.
- `TestRegVisibilityForeignProviderFilePreservedUnderProviderSync`: seeds `provider--foreigndeadbeef.json`, saved byte digest vor dem provider-sync mit einem anderen (owned) provider-source, asserted byte-identisch nachher.
- `fileDigest` hashet mit `sha256` + `base64.StdEncoding` (regression_test.go helpers); vor/nach-hash werden im test direkt verglichen, kein string-verbatim in der akte.

## ## PLAN (nummeriert, ohne markdown-checkboxen)

1. `git fetch origin --prune`; remote-truth selbst lesen (`git ls-remote origin refs/heads/develop`, `gh api pulls/1693`); akte r2 wortlich gelesen.
2. EIN monotoner merge-hopf `git merge --no-ff origin/develop` (kein rebase, kein force) auf den dann aktuellen develop (558dc42d); nachweise is-ancestor develop=0, is-ancestor r5-commit=0, merge-tree conflict-count=0.
3. B2 fix: `ownProviderNamespace` + name-matching-ownership in `syncProviderTargets` (prometheus_files.go).
4. B1 fix: `prometheusConfig`-regression gegen die emittierten job-globs.
5. Neue regression: fremde `provider--`/`provider-secure--`-datei seeden, byte-digest vor/nach, app-only-sync und provider-sync; `TestRegVisibilityProviderFileGlobClassification`.
6. `go build ./...`, `go vet ./internal/metrics`, `go test ./internal/metrics -run TestRegVisibility`, full metrics+observability, `bash scripts/ci-fast-check.sh` VOR push.
7. Push (draft=false); EIN exaktkopf-lauf 44587260864 bis terminal (completed/success, PR Selected Checks: success).
8. Evidence fix-4.md; karte erst NACH terminal-gruen auf review.

## ## repo-rule compliance

- Write-set: nur registry/target-naming path (internal/metrics/prometheus_files.go, internal/metrics/regvisibility_regression_test.go). Kein `.github/**`, kein `scripts/**`, kein `cmd/baha/**`, kein `internal/machine/**`, kein `docs/**`.
- Kein rebase/force/reset auf produkt-zweigen; monotoner merge-hopf; base attestet durch diff-zeuge (kein test_pr_* treffer).
- Kein subagenten (§4.8); kein merge durch mich (owner fuehrt die unabhaengige abnahme).
- CI-Aufnahme der neuen tests uebenden existing go-unit packages shard + pull_request-trigger; kein `.github/**`-change nothendig.
- PR/#1693: PR-basis bleibt die vertrags-lane (base 558dc42d = develop), kein gestapeltes pr.

## Host hygiene (cleanliness)

- Vorher: `docker ps` (keine baseharbor-compose container in diesem go-only lauf), `docker network ls`, `docker volume ls`.
- Nachher: dieselben drei listen; kein in diesem lauf erzeugter container/netzwerk/volume (reiner go build/test/commit/push + git).
- cleanliness: keine baseharbor-compose netzwerke/volumes/container in diesem lauf erzeugt; ambient-core/ unangetastet.
