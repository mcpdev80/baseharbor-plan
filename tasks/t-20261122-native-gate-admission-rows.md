---
id: t-20261122-native-gate-admission-rows
card_number: "0428-230"
card_short_title: "native gate rows for"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: Owner (user-authorized CI coverage, PR 1756, includes ci-native-pr-gate.sh gate executor support)
kanban_status: review
kanban_lane: review
kanban_summary: ""
kanban_title: 0428-230 · native gate rows for
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1756]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/gate-admission-census/native-checks-catalog-recipe.md"]
---

- [ ] t-20261122-native-gate-admission-rows · native gate rows for env-destroy #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** Owner (user-authorized CI coverage, PR 1756, includes ci-native-pr-gate.sh gate executor support)  
    **PR:** [baseharbor#1756](https://github.com/mcpdev80/baseharbor/pull/1756)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/gate-admission-census/native-checks-catalog-recipe.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261122-native-checks-rows-operator-seam](t-20261122-native-checks-rows-operator-seam.md)  
**Owner:** Owner (user-authorized CI coverage, PR 1756, includes ci-native-pr-gate.sh gate executor support)  
**Priority:** not set  
**PRs:** [baseharbor#1756](https://github.com/mcpdev80/baseharbor/pull/1756)  
**Source:** 
<!-- /generated:links -->


## Why

A bug-hunt census (evidence/r28-welle5-2026-11-22/native-gate-admission/befund-1.md, plan 8ceac4228) measured that the
PR-level native gate selector never admits the environment-destroy components, so a PR that changes only those sources
gets `matrix={"include":[]}` from `PR · Native gate plan` (job 137070848046 on head 2f0f80786d8) while the actual test
execution happens only through the coreless application shards (`scripts/pr-gate-plan.py:1171`, `:1231`). The native
check row is therefore an admission gap, not an execution gap: the planner file itself exists at develop 8b9a8f50645
(`git ls-tree` = blob 4259fbf665) and no warning annotation was ever emitted.

## Findings to carry into the edit

- Selection loop is `scripts/validate-pr-gate-coverage.py:74-88` (function starts at line 66) and only reads rows from
  `coverage["native_checks"]` with `selection_scope == "focused"`.
- Eight components have `runtime_specific` or `required_test_names` but no `native_checks` row: the env-destroy
  integration test source (docker + podman), `runtime.podman-service-stop` and its test component (podman,
  TestSelectedStopAcceptsPinnedContainerName), and the six `cmd/baha/*runtime_test.go` application components
  (docker + podman).
- The catalog at develop 8b9a8f50645 and at head 2f0f80786d8 is byte-identical, so this is not caused by any open PR.

## Acceptance

- `scripts/pr-gate-coverage.json` gains `native_checks` rows that list the components above in `source_components`, so
  `PR · Native gate plan` selects at least one native check for a PR that only touches those paths.
- `scripts/test_pr_gate_coverage.py` (or the existing validator test group) asserts the new rows in hosted CI; no test
  may pass by being skipped.
- One follow-up PR CI run shows `Native gates selected: true` with the executed job ids recorded in this card's
  evidence.

## Owner scope

`scripts/**` is Owner-scope for lanes (AGENTS write bans): the edit is made by the Owner or by a lane explicitly
commissioned for it; lanes only re-run and witness.

Erweiterung des vertrags, gemessen an develop 1ff16925c4e: neben den acht bereits benannten komponenten fehlen auch die acht test-quellen von PR 1750 und die drei ci_integration_operator-quellen in den native_checks-zeilen - deshalb ist PR . Selected Runtime an den gehopften heads 5d47569f337 (#1750) und ce5cf8f3037 (#1753) weiterhin SKIPPED, obwohl PR 1755 gemergt ist. rezept und feldformen: evidence/r28-welle5-2026-11-22/gate-admission-census/native-checks-catalog-recipe.md. Karte 0428-234 ist als superseded in diese karte folded.

Measured at develop 1ff16925c4e: besides the eight named components, the eight PR 1750 test sources and the three ci_integration_operator sources also have no native_checks rows. That is why PR Selected Runtime is still skipped at the hopped heads 5d47569f337 (#1750) and ce5cf8f3037 (#1753) although PR 1755 merged. Recipe and field shapes: gate-admission-census/native-checks-catalog-recipe.md. Card 0428-234 is folded into this card as superseded.

Measured at develop 1ff16925c4e: besides the eight named components, the eight PR 1750 test sources and the three ci_integration_operator sources also have no native_checks rows. That is why PR Selected Runtime is still skipped at the hopped heads 5d47569f337 (#1750) and ce5cf8f3037 (#1753) although PR 1755 merged. Recipe: gate-admission-census/native-checks-catalog-recipe.md. Card 0428-234 folded in as superseded.

Measured at develop 1ff16925c4e: besides the eight named components, the eight PR 1750 test sources and the three ci_integration_operator sources also have no native_checks rows. That is why PR Selected Runtime is still skipped at the hopped heads 5d47569f337 (#1750) and ce5cf8f3037 (#1753) although PR 1755 merged. Recipe: gate-admission-census/native-checks-catalog-recipe.md. Card 0428-234 folded in as superseded.

Measured at develop 1ff16925c4e: besides the eight named components, the eight PR 1750 test sources and the three ci_integration_operator sources also have no native_checks rows. That is why PR Selected Runtime is still skipped at the hopped heads 5d47569f337 (#1750) and ce5cf8f3037 (#1753) although PR 1755 merged. Recipe: gate-admission-census/native-checks-catalog-recipe.md. Card 0428-234 folded in as superseded.

Measured at develop 1ff16925c4e: besides the eight named components, the eight PR 1750 test sources and the three ci_integration_operator sources also have no native_checks rows. That is why PR Selected Runtime is still skipped at the hopped heads 5d47569f337 (#1750) and ce5cf8f3037 (#1753) although PR 1755 merged. Recipe: gate-admission-census/native-checks-catalog-recipe.md. Card 0428-234 folded in as superseded.

Route berichtigt, mit zeugen: der trusted native planner steht bereits in develop (blob 4259fbf665 am base 1ff16925c4e, added_by eabe37d36, ancestor bestaetigt) und die drei Native-check-runs aus run 44986337450 tragen NULL annotationen - die hinweis ueber einen fehlenden planner ist nur der vom runner echoed script-quelltext mit unersetzter variable. Die basis-eigene selektor-logik auf den acht geaenderten pfaden von PR 1750 liefert byte-genau die leere matrix, und der zaehlbare grund ist: 0 von 8 pfaden haben eine components-zeile, native_checks traegt 6 zeilen. Diese karte heisst damit catalog rows for the existing planner, nicht establish the planner. Nach dem merge: hop plus native-gate-runs fuer PR 1750 und PR 1753, proof ist der ausgefuehrte Selected-Runtime-job.

Uebergabe an den owner: sie haben die native_checks-zeilen als PR 1756 in eigener regie uebernommen, einschliesslich der ausfuehrungs-unterstuetzung, die ci-native-pr-gate.sh fuer die exakten gates braucht. Grund und feldformen sind gemessen (blob 4259fbf665 am base, null annotationen, 0 von 8 pfaden mit components-zeile). Nach merge: ich hoppe #1750 und #1753 neu und melde die ausgefuehrten Selected-Runtime-jobs als acceptance-beweis.

Uebergabe an den owner: sie uebernehmen die native_checks-zeilen als PR 1756 in eigener regie, einschliesslich der ausfuehrungs-unterstuetzung die ci-native-pr-gate.sh fuer die exakten gates braucht. Grund und feldformen sind gemessen (blob 4259fbf665 am base, null annotationen, 0 von 8 pfaden mit components-zeile). Keine lane ist darauf angesetzt - dublette vermieden. Nach merge hoppe ich #1750 und #1753 neu und melde die ausgefuehrten Selected-Runtime-jobs als acceptance-beweis.

PR 1756 ist offen und reviewbar. Kopfumfang gemessen: funf dateien, alle scripts/**, +414 -8 (ci-native-pr-gate.sh +30-3, pr-gate-coverage.json +324, test_pr_gate_coverage.py +42, test_pre_release_runtime_reuse.py +10, validate-pr-gate-coverage.py +9-5). WICHTIG: der gemeldete head de141fe9 ist nicht der aktuelle - ls-remote refs/pull/1756/head = 6cec31ff6737d1b409e9c9e3b1f3597fa0cb686b, und dieser ist in unserem objektbestand der einzige head; alle pruefe und value werden auf 6cec31ff673 geschrieben. Gehosteter run 44989154812 ist unterwegs. Die resolver-inderung ist die von mir gemessene luecke: die podman-dedup-zeile entfernt jetzt kein podman-check mehr, wenn die component runtime_specific=true ist (validate-pr-gate-coverage.py, geaenderter block in resolve_native_checks). Independent exact-head review ist dispatcht; nach CI und verdict fuehrt CODEX-MERGE den merge aus, danach hoppe ich #1750 und #1753 neu.
