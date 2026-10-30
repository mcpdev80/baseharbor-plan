ROLLE: CODEX-REVIEW

## PLAN
1. erledigt: 0. Read dispatch and binding policies; record plan. Native TodoWrite unavailable.
2. erledigt: 1. Refresh product and Planning remote states and read the task and dossier.
3. erledigt: 2. Verify each of the five acceptance criteria against origin/develop artifacts.
4. erledigt: 3. Record exact verdict and recipe; update Planning only if acceptance is established and publication is safe.

## ROLLE: CODEX-REVIEW

Verdict: REQUEST_CHANGES. Product origin/develop bc0e4daeeda76663d181fbb6b6e46ec197142edc (HTTPS ls-remote verified); Planning fetched main 03efd9addab013f9bb1f847666f64ad782331858. Reviewed remote artifacts, not the worker's assertions.

1. MET: docs/DEVELOPMENT_GUIDELINES.md:38-45 states the permanent Standards First rule.
2. MET: all 11 contracts/service/v1/*.schema.json and the canonical provider and binding schema declare JSON Schema 2020-12; contracts/contracts_test.go:10-31 and :57-74 cover the dialect.
3. NOT MET as claimed: internal/capability/service_binding.go:40-65 implements name validation and service_binding_test.go tests the helper, but repository-wide search finds no production invocation of ValidateServiceBindingName. contracts/binding/v1/service-binding.schema.json:6 allows additionalProperties, and contracts/contracts_test.go:57-74 checks dialect only, not well-known output names. Documentation at spec/provider/v1/provider.proto:360-367 is present, but actual output-name enforcement and the specified contract-test guard are not demonstrated. Worker recipe: connect the validation to the actual binding output acceptance boundary and add behavioral tests for standard names, aliases and namespaced extensions at that boundary, plus a schema contract test matching the intended extension policy. Run focused contract and capability tests on exact candidate; stop for owner decision if the schema's open extension policy intentionally precludes enforcement.
4. MET as a policy statement: docs/decisions/0018-public-contract-namespace-and-compatibility.md:38-45 explicitly supersedes pre-freeze migration-preservation promises in ADR 0013, and :47-52 describes breaking pre-freeze namespace changes. This is not a claim of unconditional backward compatibility.
5. MET: docs/decisions/0013-standards-first-service-provider-contracts.md:47 separates runtime provider-instance state from catalog/distribution metadata; spec/provider/v1/provider.proto and contracts/provider/v1/provider-descriptor.schema.json define the respective boundaries.

No new product tests run for this read-only review; worker's exact-SHA tests are recorded in w390 but do not establish criterion 3. Task card has additional acceptance items and dependencies, including final pre-v0.5 review; no claim is made that those are complete. Stop acceptance until the enforcement gap is corrected or the owner resolves its intended contract, followed by independent exact-head review and relevant checks.

## repo-rule compliance
Read-only product review; no product modification or Planning status change. The owner marcel's active task remains in review. Coordinator reminders remain unresolved.

END rv390 DONE
