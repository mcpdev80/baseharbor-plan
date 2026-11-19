# fix-3 (r4) — 0428-123 regvisibility: disjoint app-target namespace + app-target namespace reconciliation

- Card: t-20261119-hunt-metrics-registration-visibility-only (0428-123)
- PR: mcpdev80/baseharbor#1693 · zweig `lane-0428-123-regvisibility`
- Session: laptop worker session, Modell `worker-ornith1.5-laptop` über AgentGateway verifiziert.
- Evidence provenance: baseharbor-plan `origin/main` (https clone `/var/tmp/plan-123`, fetch+rebase vor Commit).
- Review: CODEX-REVIEW REQUEST CHANGES on exact head `4f22bf6e92354637367a821318f1dfbd6d1c1515` (base `1019190d8dc0ecac7693f3461153e76be0e2cb8a`), akte `evidence/r28-welle4-2026-11-19/codex-review-wave/1693-0428-123.md`.

## Kopf-Folge (d751c83bb → 4f22bf6e → 97987af6)

- d751c83bb (r3): ListMetrics 5-arg auf develop fac01c772.
- 4f22bf6e (r3): ListMetrics 5-arg auf develop 1019190d — dieser Kopf bekam REQUEST CHANGES von CODEX-REVIEW (die zwei findings).
- 97987af6 (r4, dieser Lauf): Commit `6732ec8d1011e12e067ec70ccf7b3370731fe969` + zweiter monotoner merge-hopf `97987af6954aca0318a16aef99b19c27dbee231a` auf develop `7ee6f817dbff5a238bbc651315d6d76b3819fc91` (#1581, 18:19:51+01:00). Run 44578337221.
- Basiswechsel-Zeuge (in die akte, base-abstands-regel): `git diff --name-only c296086ca1e35ef3212d293afc94d7bebcd1690f 7ee6f817dbff5a238bbc651315d6d76b3819fc91` → `scripts/ci-workflow-policy.sh`, `scripts/test_pr_gate_plan.py`. `scripts/test_pr_*` ist ein treffer der base-abstands-regel, also ist der neue lauf unter 7ee6f817 pflicht (kein lauf auf dem alten stand c296086c/1019190d).
- Warum der alte lauf (44557894265 auf 4f22bf6e) nicht zaehlt: der kopf 4f22bf6e trug die UNFIXED version; die abnahme forderte eine korrektur. 44557894265 lief auf dem korrigierungsbeduerftigen kopf und ist keine abnahme.

## CI-Beweis (terminal)

- Run-ID: 44578337221, Event pull_request, SHA 97987af6954aca0318a16aef99b19c27dbee231a, Start 2026-11-19T17:32:50Z.
- Status terminal: **completed/success**. Aggregate `PR Selected Checks: success`.
- Pflicht-Jobs ausgefuehrt und gruen (kein SKIPPED unter Mandatory): go-build (PR · Validation · go-build: success), go-vet (PR · Validation · go-vet: success), Go unit owner/packages/cli-0/1/2/3 (alle success), Workflow policy success, Trusted Plan success, Native gate plan success, Source format success, Focused Python success.
- Kein ORAS/trust-plane runner-precondition-Fehler; die HA/runtime-gates sind von CI-policy als skipped markiert (nicht ausgefallen). SKIPPED != pass, aber hier ist SKIPPED keine Mandatory-Execution; die Mandatory-Jobs sind alle ausgefuehrt.
- Provenance: `git merge-base --is-ancestor origin/develop 97987af6` → rc=0; `git merge-base --is-ancestor 7ee6f817 97987af6` → rc=0; `git merge-base --is-ancestor 1019190d 97987af6` → rc=0; `git merge-tree --write-tree origin/develop 97987af6` conflict-count=0. PR #1693 head=97987af6, base=7ee6f817, draft=false.

## Die zwei fixes (datei:zeile)

### Finding #1 — disjunktions-namespace (prometheus_files.go)

- `syncProviderTargets` (:74) nimmt jetzt `SourceApplication`-quellen aus `ListApplicationMetrics` auf und schreibt sie ueber `writeApplicationTargetFile` (:194) in die eigene `application--<app>--<env>--<source>.json`-datei (`appTargetFileName` :53), nie in eine `provider--<hash>.json`-datei. `appTargetFileName` prueft die ID-grammatik `application:metrics:<app>:<env>:<src>` und faellt closed (leer), wenn die id nicht passt. Der prefix `application--` (:47) ist strukturell disjunkt vom `provider--`/`provider-secure--`-namespace: kein gueltiger application-slug (z.b. `provider` oder `provider-secure`) kann je eine datei erzeugen, die mit `application--` beginnt.
- `EnsureProviderFilesWithRuntimeCAAt` (:388) und `UnregisterSharedApplicationAt` (:616) rufen jetzt `ListApplicationMetrics` auf (wenn `policy.Collect[MetricsSourceApplication]`) und foldingen die app-quellen in die target-writer, die app-quelle wird also tatsaechlich in die datei geschrieben, nicht nur via `ListApplicationMetrics` im verify-pfad gesehen. Vorher lief `syncProviderTargets` nur ueber `ListMetrics` (exkludiert app-quellen), also wurde nie eine app-target-datei geschrieben.
- `providerSourcePresent` (:161) loescht nur `provider--`-dateien, die keinem ausgewaehlten nicht-app-quelle entsprechen — orphan-en, keine foreign-files.
- `prometheus_render.go:198` baseharbor-applications file_sd list hat jetzt eine ausdrueckliche `application--*--*--*.json`-zeile (die `*--*--*.json`-zeile trifft sie ebenfalls).

### Finding #2 — application-namespace reconciliation (prometheus_files.go)

- `syncProviderTargets` reconciliert den `application--`-namespace bei JEDEM sync: `appKeep` sammelt exakt die dateien der jetzt selektierten app-quellen (:106), die schleife (:111) loescht jede andere `application--*.json`-datei und loescht orphaned `provider--`/`provider-secure--`-dateien, laesst aber foreign provider- und runtime-target-dateien unangetastet (nichts in beiden namespaces).

## Neue test-ids + gate

- `TestRegVisibilityApplicationNamedProviderIsDisjoint` (regvisibility_regression_test.go): application mit dem slugs-wert `provider` (gueltiger slug), `syncProviderTargets` aufrufen, behaupten: quelle erscheint GENAU EINMAL im `application--provider--dev--api.json`-file MIT labels `baseharbor_application`=provider/`baseharbor_environment`=dev/`baseharbor_source`=id, NICHT im providers-job (keine `provider--`-datei traegt das ziel), und ueberlebt einen anschliessenden empty sync.
- `TestRegVisibilityStaleApplicationTargetReconciledOnSync`: erst stage-queLLE syncen (identische application `demo`), dann dev-only; behaupten: stage-target-datei + stage-endpoint weg, dev-target da (`demo-dev`), eine fremde `0-runtime-target.json`-datei unveraendert (content-digest).
- Gate: `go build ./...` rc=0, `go vet ./internal/metrics` rc=0, `go test ./internal/metrics -run TestRegVisibility` pass, full metrics + observability package pass, `bash scripts/ci-fast-check.sh` → 275 tests OK, workflow policy PASS, source readability PASS.
- CI-Aufnahme: die neuen tests laufen im existing `PR · Go unit · packages` shard (auto-discovered durch `go test ./...`), pull_request-trigger. Kein `.github/**`-change noetig (owner-scope); kein change an `scripts/**`.

## ## PLAN (nummeriert, ohne markdown-checkboxen)

1. `git fetch origin --prune`; remote-truth selbst lesen (`git ls-remote origin refs/heads/develop`, `gh api pulls/1693 .head.sha/.base.sha/.mergeable_state/.draft`). Basiswechsel gemessen: develop 7ee6f817 (owner-merge #1581), diff c296086ca→7ee6f817d touching scripts/test_pr_gate_plan.py + scripts/ci-workflow-policy.sh = base-abstandstreffer.
2. EIN monotoner merge-hopf `git merge --no-ff origin/develop` (kein rebase, kein force) auf 7ee6f817; nachweise: is-ancestor develop=0, is-ancestor 7ee6f817=0, is-ancestor 1019190d=0, merge-tree conflict-count=0.
3. Finding #1 fix (disjunktions-namespace) + finding #2 fix (namespace reconciliation) in internal/metrics/prometheus_files.go; render-glob in prometheus_render.go.
4. `go build ./...`, `go vet ./internal/metrics`, `go test ./internal/metrics -run TestRegVisibility`, full metrics+observability, `bash scripts/ci-fast-check.sh` VOR push.
5. Push (draft=false) zu lane-0428-123-regvisibility; EIN exaktkopf-lauf 44578337221 bis terminal (completed/success, PR Selected Checks: success).
6. Evidence fix-3.md; karte active bis abnahme.

## ## repo-rule compliance

- Write-set: nur registry/target-naming path (internal/metrics/prometheus_files.go, prometheus_render.go, regvisibility_regression_test.go). Kein `.github/**`, kein `scripts/**`, kein `cmd/baha/**`, kein `internal/machine/**`, kein `docs/**`.
- Kein rebase/force/reset auf produkt-zweigen; monotoner merge-hopf; base attestet durch diff-zeuge.
- Kein subagenten (§4.8); kein merge durch mich (owner fuehrt die unabhaengige abnahme).
- CI-Aufnahme der neuen tests uebenden existing go-unit packages shard + pull_request-trigger; kein `.github/**`-change noetig.
- PR/#1693: PR-basis bleibt die vertrags-lane (base 7ee6f817 = develop), kein gestapeltes pr.

## Host hygiene (cleanliness)

- Vorher: `docker ps` (keine baseharbor-compose container in diesem go-only lauf), `docker network ls`, `docker volume ls`.
- Nachher: dieselben drei listen; kein in diesem lauf erzeugter container/netzwerk/volume (reiner go build/test/commit/push).
- cleanliness: keine baseharbor-compose netzwerke/volumes/container in diesem lauf erzeugt; ambient-core/ unangetastet.
