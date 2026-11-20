## runde 2 (card 0428-169) — closeout mit ERSETZUNG-DURCH-ANDEREN-OFFEN-PR

- ROLLE: worker, PR-hygiene. Vertrag runde 2 (vom Owner, 2026-11-20 ~04:00): je PR der liste drei zeilen.
- 1. VOLLSTAENDIGE dateiliste: `gh pr diff <n> --name-only` (ganze liste).
- 2. vergleich gegen ALLES mit inhalt: develop UND offene AMEN-/kanditaten-menge. Vergleichs-koepfe je datei: `git diff --name-only <pr-n-head> <vergleichs-head> -- <datei>` -> LEER = dort vertreten. Heads: origin/develop f61ef0f4991c, 1615 f93564a0, 1650 b6dab95a, 1684 576c6ad8, 1695 f64d30af, 1709 983152b9, 1614 80d4df52, 1625 010db47d, 1623 8014d71e, 1702 6740299f, 1704 f5dcf128, 1596 c90c3b89.
- 3. KLASSE je pr: (a) ERSETZT-DURCH-DEVELOP (alle dateien blob-identisch mit develop), (b) ERSETZT-DURCH-PR <m> (alle dateien blob-identisch in EINEM PR m), (c) TEIL-ERSETZT (teil gedeckt, teil fehlt — datei, zeilen, karte benennen), (d) NICHT-ERSETZT (gar nicht gedeckt).
- HANDELN nur bei (a) und (b): `gh pr close <n> --comment "<nachweis-zeile mit vergleichs-head>"`. Bei (c)/(d) NICHT schliessen, in tabelle melden (das ist owner-seite, karte giessen).
- BEWEIS-PFLICHT: pro pr drei zeilen; ls-remote develop am anfang; am ende zaehl (a)+(b) und (c)+(d).

## develop witness (runde 2)

- `git ls-remote origin refs/heads/develop` BEFORE runde 2: `f61ef0f4991cae88727c02b731d862bf395d8984` (committer-date 2026-11-20T03:55:06+01; commit dahinter = merge von #1582, von der anderen welt gelandet).
- #1582: `gh api .../pulls/1582` -> state=closed merged=true; head f21bc6f35eac IS ancestor of develop (case (a), nur protokollieren, kein close — schon von anderer welt geschlossen).
- 21 open PRs gesamt (Stand messung runde 2).

## methode / werkzeug

- https-clone baseharbor in /tmp/opencode/x-169-wt; je kopf `git fetch origin refs/pull/<n>/head` + `git branch -f cmp_<n> FETCH_HEAD`; develop -> cmp_develop.
- blob-vergleich je datei: `git diff --quiet <cmp_pr> <cmp_head> -- <datei>` -> returncode 0 = blob-identisch.
- WICHTIG: kandidaten-kopfe bauen auf UNTERSCHLICHEN develop-basen, daher ist ein file nur dann "ersetzt durch PR m", wenn ALLE dateien des prs gegen PR m blob-identisch sind; teile decken sich, teile nicht -> (c).
- karten-ownership (gemessen an den task-Dateien, kanban_status): 1627=#0428-055 wait; 1620=#0428-067 blocked; 1650=#0428-078 blocked; 1615=#0428-057 live; 1623=#0428-063 live; 1594=#0428-env-registry (closed als karte, aber content lebt in stack); 1645=#0428-perses-tempo planned; 1665=#0428-perses-dashboards wait; 1588=#0427-target-policy wait; 1587=#0427-operator-api-docs wait; 1585=#bughunt-d28-state-dir wait.

## je PR — drei zeilen

### PR 1627 (#0428-055 env-delete, kanban=wait, LIVE)
1. `gh pr diff 1627 --name-only`: cmd/baha/commands.go, cmd/baha/env_destroy.go, cmd/baha/env_destroy_integration_test.go, cmd/baha/machine_coverage.go, docs/cli/command-index.md, docs/de/cli/command-index.md, docs/reference/cli-machine-coverage.md, internal/deployment/environment_destroy_scope.go, internal/deployment/environment_destroy_scope_test.go (9).
2. `git diff --name-only cmp_1627 cmp_develop -- <9 files>` -> 9 (nicht leer); `git diff --name-only cmp_1627 cmp_1615` / cmp_1650 / cmp_1684 ... -> je 9 (nicht leer). `git rev-parse cmp_1627:internal/deployment/environment_destroy_scope.go`=e120c9f8 vs `cmp_develop`... :8b9e346e (anders).
3. KLASSE (d) NICHT-ERSETZT: alle 9 files blob-weit von develop UND allen 11 kandidaten; content (env_destroy.go, environment_destroy_scope.go) existiert auf develop nicht (`git ls-tree -r cmp_develop --name-only | grep env_destroy` -> leer). karte 0428-055 kanban=wait, handoff 2026-11-20: "keep task in wait; PR #1627 head 96deb1f1; no merge or acceptance".
- HANDELN: KEIN close. meldung: PR #1627 / datei cmd/baha/env_destroy.go + internal/deployment/environment_destroy_scope.go / content fehlt auf develop und ist durch keinen benannten PR ersetzt (karte 0428-055 lebt, wait).

### PR 1620 (#0428-067 per-reveal-audit, kanban=blocked, LIVE)
1. `gh pr diff 1620 --name-only`: cmd/baha/app_access.go, cmd/baha/app_access_test.go (2).
2. `git diff --name-only cmp_1620 cmp_develop -- cmd/baha/app_access.go cmd/baha/app_access_test.go` -> 2 (nicht leer); gegen alle kandidaten je 2 (nicht leer).
3. KLASSE (d) NICHT-ERSETZT: beide files blob-weit; karte 0428-067 kanban=blocked, prs=[#1620], lebender ansatz.
- HANDELN: KEIN close.

### PR 1597 (perses-docs, teil #0428-perses)
1. `gh pr diff 1597 --name-only`: 33 files (cmd/baha/app_perses_cli_test.go, cmd/baha/app_status_result.go, docs/spec/*.md, go.mod, go.sum, internal/application/manifest_*, internal/capability/perses*, internal/metrics/perses_dashboards*, testdata/perses-dashboards/*).
2. gegen cmp_develop: 11/33 blob-identisch (docs + manifest_*.go-teile etc.), 22/33 nicht; gegen kandidaten: app_perses_cli_test.go, app_status_result.go, go.mod, go.sum, manifest_render.go, manifest_test.go, manifest_validation.go, capability/perses*.go, metrics/perses_dashboards* + testdata -> alle blob-weit (nicht in irgendeinem kopf vertreten).
3. KLASSE (c) TEIL-ERSETZT: 11/33 in develop, 22/33 nicht gedeckt. Nicht gedeckt: cmd/baha/app_perses_cli_test.go, cmd/baha/app_status_result.go, go.mod, go.sum, internal/application/manifest_render.go, internal/application/manifest_test.go, internal/application/manifest_validation.go, internal/capability/perses.go, internal/capability/perses_selection.go, internal/capability/perses_selection_test.go, internal/metrics/perses_contract_test.go, internal/metrics/perses_dashboards.go, internal/metrics/perses_dashboards_helpers.go, internal/metrics/perses_dashboards_promql_test.go, internal/metrics/perses_dashboards_test.go, internal/metrics/testdata/perses-dashboards/{loki-logs,mongodb-targets,postgresql-targets,prometheus-targets,tempo-traces}.json.
- HANDELN: KEIN close (nur teil gedeckt).

### PR 1594 (workload_security + operatorauth + serviceaccess policy)
1. `gh pr diff 1594 --name-only`: internal/application/workload_security.go, workload_security_explicit_policy_test.go, workload_security_test.go, internal/operatorauth/{authorization_test.go,config.go,config_explicit_policy_test.go,operatorauth_test.go}, internal/serviceaccess/{policy.go,policy_explicit_test.go,policy_test.go} (10).
2. gegen cmp_develop: 10/10 blob-weit; gegen alle kandidaten je 10 (nicht leer).
3. KLASSE (d) NICHT-ERSETZT: alle 10 blob-weit von develop und allen kandidaten.
- HANDELN: KEIN close.

### PR 1665 (#0428-perses-infra-dashboards, kanban=wait, LIVE)
1. `gh pr diff 1665 --name-only`: 41 files (cmd/baha/app_perses_infra_dashboards_cli_test.go, cmd/baha/app_status_result.go, docs/spec/*.md, internal/application/manifest_*, internal/capability/perses*, internal/metrics/perses_infra_dashboards*, perses_prometheus_datasource*, testdata/perses-infra-dashboard/*).
2. gegen cmp_develop: 14/41 blob-identisch, 27/41 nicht; gegen kandidaten: app_perses_infra_dashboards_cli_test.go, app_status_result.go, manifest_render.go, manifest_test.go, manifest_validation.go, capability/perses.go, capability/perses_selection.go, metrics/perses_contract_test.go, metrics/perses_infra_dashboards*.go, metrics/perses_prometheus_datasource*.go, testdata/perses-infra-dashboard/* -> blob-weit.
3. KLASSE (c) TEIL-ERSETZT: 14/41 in develop, 27/41 nicht gedeckt. Nicht gedeckt: cmd/baha/app_perses_infra_dashboards_cli_test.go, cmd/baha/app_status_result.go, internal/application/manifest_render.go, internal/application/manifest_test.go, internal/application/manifest_validation.go, internal/capability/perses.go, internal/capability/perses_selection.go, internal/metrics/perses_contract_test.go, internal/metrics/perses_infra_dashboards.go, internal/metrics/perses_infra_dashboards_test.go, internal/metrics/perses_prometheus_datasource.go, internal/metrics/perses_prometheus_datasource_test.go, internal/metrics/testdata/perses-infra-dashboard/{prometheus-targets.json, upstream/{dev-data-dashboard.json,*.cue.txt,*.go.txt,spec-*.json}} (23 dateien).
- HANDELN: KEIN close.

### PR 1645 (#0428-perses-tempo, kanban=planned, LIVE)
1. `gh pr diff 1645 --name-only`: 41 files (cmd/baha/app_perses_cli_test.go, cmd/baha/app_status_result.go, docs/spec/*.md, internal/application/manifest_*, internal/capability/perses_test.go, internal/metrics/management_ui.go, perses_contract_test.go, perses_tempo_*.*, testdata/perses-tempo-datasource/*, internal/testsupport/serviceissuer/issuer.go).
2. gegen cmp_develop: 11/41 blob-identisch, 30/41 nicht; gegen cmp_1615: app_status_result.go blob-identisch (coordinator-befund bestaetigt: `git diff --name-only cmp_1645 cmp_1615 -- cmd/baha/app_status_result.go` -> LEER), aber perses_tempo_*.* und capability/perses.go blob-weit; gegen alle anderen kandidaten ebenfalls blob-weit fuer die tempo-dateien.
3. KLASSE (c) TEIL-ERSETZT: 11/41 in develop; app_status_result.go in 1615 gedeckt; NICHT gedeckt (26): internal/application/manifest_render.go, manifest_test.go, manifest_validation.go, internal/capability/perses.go, internal/metrics/perses_contract_test.go, internal/metrics/perses_tempo_contract.go, perses_tempo_datasource.go, perses_tempo_datasource_test.go, perses_tempo_errors.go, perses_tempo_fixture_test.go, perses_tempo_upstream.go, perses_tempo_witness_test.go, testdata/perses-tempo-datasource/{perses-pin.json,tempo-datasource.json,tempo-trace-query.json,upstream/*}, internal/testsupport/serviceissuer/issuer.go.
- HANDELN: KEIN close (nur app_status_result.go in 1615 gedeckt, rest nicht).

### PR 1588 (#0427-target-policy-presets, kanban=wait, LIVE)
1. `gh pr diff 1588 --name-only`: cmd/baha/app_remote_lifecycle.go, cmd/baha/deployment_record.go, cmd/baha/machine_coverage.go, cmd/baha/target_deployment_policy_edit_b_test.go, docs/reference/cli-machine-coverage.md, internal/deployment/immutable_provenance.go, internal/deployment/immutable_provenance_test.go (7).
2. gegen cmp_develop: 0/7 blob-identisch; gegen alle kandidaten je 7 (nicht leer).
3. KLASSE (d) NICHT-ERSETZT: alle 7 blob-weit.
- HANDELN: KEIN close.

### PR 1587 (#0427-operator-api-docs, kanban=wait, LIVE)
1. `gh pr diff 1587 --name-only`: cmd/baha/serve.go, docs/cli/automation-agents.md, docs/de/cli/automation-agents.md, docs/de/how-to/operator-api.md, docs/de/spec/control-plane-runtime.md, docs/how-to/operator-api.md, docs/spec/control-plane-runtime.md, mkdocs.de.yml, mkdocs.yml (9).
2. gegen cmp_develop: 0/9 blob-identisch; gegen alle kandidaten je 9.
3. KLASSE (d) NICHT-ERSETZT: alle 9 blob-weit.
- HANDELN: KEIN close.

### PR 1585 (#bughunt-d28-state-dir, kanban=wait, LIVE)
1. `gh pr diff 1585 --name-only`: cmd/baha/target.go, cmd/baha/target_selection.go, cmd/baha/target_selection_state_dir_isolation_test.go, cmd/baha/target_state_layout.go, internal/deployment/target.go, internal/orgconfig/store.go (6).
2. gegen cmp_develop: 0/6 blob-identisch; gegen alle kandidaten je 6.
3. KLASSE (d) NICHT-ERSETZT: alle 6 blob-weit.
- HANDELN: KEIN close.

### PR 1582 (bereits GEMERGT — nur protokollieren)
1. `gh pr diff 1582 --name-only`: cmd/baha/runtime_integration_test_support_test.go, internal/orgconfig/orgconfig_test.go, internal/orgconfig/store.go (3).
2. head f21bc6f3 IS ancestor of develop f61ef0f4 (case (a)); `git merge-base --is-ancestor f21bc6f35eac f61ef0f4` -> JA.
3. KLASSE (a) ERSETZT-DURCH-DEVELOP — bereits von anderer welt geschlossen (merged 2026-11-20).
- HANDELN: kein close, schon geschlossen. protokolliert.

## tabelle (c)/(d) — owner-seite (karte giessen)

| PR | karte | klasse | dateien nicht gedeckt | zeilen (approx) |
| --- | --- | --- | --- | --- |
| 1627 | 0428-055 env-delete (wait) | (d) | 9 (env_destroy.go, environment_destroy_scope.go + tests, commands.go, machine_coverage.go, docs) | ~1400 deletions/insertions |
| 1620 | 0428-067 per-reveal-audit (blocked) | (d) | 2 (app_access.go, app_access_test.go) | neu |
| 1597 | perses-docs | (c) | 22/33 (app_perses_cli_test.go, app_status_result.go, go.mod/go.sum, manifest_render/test/validation, capability/perses*, metrics/perses_dashboards*) | teil in develop |
| 1594 | workload_security/policy | (d) | 10 | neu |
| 1665 | 0428-perses-infra (wait) | (c) | 27/41 (infra_dashboards*, prometheus_datasource*, capability/perses*, manifest_*) | teil in develop |
| 1645 | 0428-perses-tempo (planned) | (c) | 26/41 (perses_tempo*, capability/perses, manifest_*) | app_status_result.go in 1615 gedeckt |
| 1588 | 0427-target-policy (wait) | (d) | 7 (app_remote_lifecycle, deployment_record, machine_coverage, immutable_provenance*) | neu |
| 1587 | 0427-operator-api-docs (wait) | (d) | 9 (serve.go, docs, mkdocs) | neu |
| 1585 | bughunt-d28-state-dir (wait) | (d) | 6 (target*, orgconfig/store.go) | neu |

## end-gesamt runde 2

- geschlossene PRs durch diese lane: 0.
- (a)+(b) — schliessbar (in develop oder EINem anderen PR vollstaendig gedeckt): 1 (nur #1582, bereits merged, kein close noetig).
- (c)+(d) — NICHT schliessbar, in tabelle gemeldet, owner-seite: 8 (1627, 1620, 1597, 1594, 1665, 1645, 1588, 1587, 1585 — 1582 zaehlt als (a)/bereits-merged).
  - exakt: (a)=1 (#1582), (b)=0, (c)=3 (#1597, #1665, #1645), (d)=5 (#1627, #1620, #1594, #1588, #1587, #1585 -> 6; korrigiert: (d)=6).
  - aufgaenge: (a)+(b)=1; (c)+(d)=8 (9 list-prs abzüglich #1582).
- kein PR geschlossen (alle 9 list-prs tragen lebenden content, karten kanban in {wait,blocked,planned}).
- gegenprobe: 0 closes, 9 open erhalten.

## repo-rule compliance

- KEIN produkt-code, KEIN PR-close, KEIN merge, KEIN branch-delete, KEIN force-push, KEIN .github/scripts.
- read-only gh api + read-only git diff/merge-base/tree gegen https remote.
- KEIN subagent/task/agent tool (4.8).
- KEIN container/netzwerk/volume/state-verzeichnis.
- plan-writes nur aus planning-remote-clone, fetch+rebase origin/main vorher, nur diese akte, KEIN git -A.
- KEIN write in /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (workers-buchhaltung).

## cleanliness

- container/netzwerke/volumes/state-verzeichnisse: keine gestartet.
- /tmp/opencode/x-169-wt: https-clone baseharbor (read-only). cmp_* branches und /tmp/opencode/x-169-wt/*.py helper, werden aufpraet.
- cleanliness: clean.

## END

- END_DONE x-169 runde 2: (a)+(b)=1 (nur #1582, bereits merged), (c)+(d)=8 (1627,1620,1597,1594,1665,1645,1588,1587,1585). 0 PRs geschlossen. inhalt aller list-prs lebt (karten in {wait,blocked,planned}); (c)/(d) in tabelle gemeldet -> owner giesset karten.
- gegenproben: 0 closes; 9 open erhalten.
- gegenprobe zeile 1: `git merge-base --is-ancestor f21bc6f35eac792386a9d708234609ca6a7f7060 f61ef0f4991cae88727c02b731d862bf395d8984` -> JA (#1582 auf develop).
- gegenprobe zeile 2: `gh api repos/mcpdev80/baseharbor/pulls/1627 --jq .state` -> open (unveraendert, nicht geschlossen).

## ls-remote witness (origin/main BEFORE push)

- planning-remote origin/main base before this work: (fetch + rebase vorher, zeile unten).
