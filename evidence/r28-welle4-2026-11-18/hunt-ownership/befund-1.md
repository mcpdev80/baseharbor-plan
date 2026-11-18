# BUG-HUNT 916 — runtime ownership / impact-consent staleness

Mission: /var/tmp/missions/mission-hunt-ownership.md
Lane: hunt-ownership (bug-hunt, pure findings, no product change)
Object: merged content on baseharbor develop at 8dccd4fe1a52bbcc61c67f7809079f33b8040d64 (verified via `git ls-remote origin develop`; fresh clone HEAD == 8dccd4fe1).
Worktree: /tmp/opencode/hunt-ownership-wt (fresh clone of origin/develop, no product edits).
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` → /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan; `git remote get-url origin` → https://github.com/mcpdev80/baseharbor-plan.git.
origin/main at evidence start: 528f3cc5753f9b2c20e802e37faef2226b68c16d (fetched, before my commit). My evidence commit is cut directly on top of that origin/main tip; other lanes' uncommitted work in the planning checkout (tasks/, views/, evidence/app-env-recovery-flags) was left untouched.
CI context of the mission trigger: PR #1663 run 44407750981 reported `stale-impact-consent` after an unverifiable ownership state. This hunt examines the mechanism on merged develop, not that PR.

## PLAN

1. Verify remotes (baseharbor develop HEAD 8dccd4fe1, baseharbor-plan origin/main), fresh clone at /tmp/opencode/hunt-ownership-wt. — done
2. Create this evidence file with ## PLAN + base attestation. — done
3. Slice (a): trace where ownership-state is classified "unverifiable" and what marks impact-consent stale (file:line). — done
4. Slice (b): tabulate add/remove/re-add race windows where states remain without error. — done
5. Slice (c): enumerate untested combinations (re-add after failed remove) across test suites. — done
6. Run focused unit tests on ownership/consent paths (no containers per R1), record results. — done
7. Write findings, cleanliness line, commit evidence on top of origin/main and push. — in progress
8. Verify evidence path present on origin/main, END post to coordinator. — pending

All paths are relative to the develop checkout at 8dccd4fe1.

## Slice A — code-path walk: "unverifiable" ownership → stale impact consent

### A.1 Where ownership/state is classified unverifiable

Two distinct layers, and only one of them feeds the consent digest:

Layer 1 — projection defaults (no runtime observation available at all):
- `cmd/baha/app_core_requirement.go:126-128` — `if existing[instance.ID] { fact.State = application.ProviderUnverifiable }` ("Registry presence is not a live or stopped-state observation"). Any registry-known instance whose adapter produced no observation defaults to unverifiable.
- `cmd/baha/app_core_requirement.go:130-132` — `OwnershipExternal` instances are always `ProviderUnverifiable` with empty dependencies.
- `cmd/baha/app_core_requirement.go:165-170` — the target storage/broker module is `ProviderUnverifiable` when `retainedBroker` (some dependent fact is not `ProviderNewRequired`) but no live observation exists.
- `cmd/baha/application_shared_backend_projection.go:23-26` — same retained-but-unobserved pattern for shared PostgreSQL/Valkey modules.
- `cmd/baha/application_shared_sql_observation.go:11-33` (`observeReusedCoreSQLState`) — a shared logical SQL module reusing the Core owner is unverifiable unless the owner fact is exactly well-shaped: `selected == nil` (13), root resolve error (17), inventory mismatch (20-22), fact-shape violations incl. `Containers.Value == nil` / not "measured" (24), running-with-zero-containers (27-28), and any state that is neither Running nor StoppedOwned (30-31).
- `cmd/baha/application_provider_container_observation.go:11-51` (`observeCanonicalProviderContainers`) — the actual ownership-checked classifier: duplicate wanted resource (16), no wanted resources (22), a container resource matching more than one real container = ambiguous (41-42), partially healthy/starting (47-48). Running requires ALL wanted containers running+healthy.
- `cmd/baha/application_broker_observation.go:67-68` and `cmd/baha/application_identity_observation.go:80-81` — "running but one-shot initializer completion unverifiable" → `ProviderUnverifiable`.
- `cmd/baha/application_broker_dependency.go:100`, `cmd/baha/application_management_dependency.go:50` — same default for broker/management ancillaries.
- Note the fail-open direction in these observers: every adapter loader/inspect/list error path silently `return`s (`application_broker_observation.go:20-38`, `application_shared_backend_observation.go:16-29`), leaving the Layer-1 default `ProviderUnverifiable` without any recorded reason.

Layer 2 — union retirement decision:
- `internal/application/provider_union.go:164-168` — `action = "preserve"; reason = "runtime ownership/state is unverifiable"; p.Complete = false` whenever `!observed || (!verifiedState && !externalReference) || fact.Target != snapshot.Target || fact.Dependencies == nil ||` app-scoped instance with no known owner. `verifiedState` is only Running/StoppedOwned/NewRequired (line 160); `unverifiable` deliberately never is.
- `internal/application/provider_union.go:139` + `173-180` — default reason "inventory or ownership is not verified"; a later unknown fact retroactively downgrades already-planned `stop`/`remove-runtime` to `preserve` ("incomplete Target inventory").

### A.2 What "unverifiable" changes in the impact plan

- `internal/application/provider_change_plan.go:121-149` — `describeProviderChange`: `observedRealization` (292-298) is known only when `Realization.Verified && Evidence != ""`; `known = known && observed && fact.InventoryComplete && …` (140). `ProviderImpactObservation.Revision` is carried into `p.Revision` (43).
- `provider_change_plan.go:97-100` — `!p.Complete || p.Destructive` forces `Attention = "Achtung"` and `ConfirmationsRequired = 2`.
- `provider_change_plan.go:101-117` — PlanID = sha256 over `impactDigestInput`, which includes (per `internal/application/provider_change_digest.go:12-45`): the full `capability.Registry`, the per-instance `structure{Target, State, Core, Dependencies, Ancillary, OwnerReference}` map built from `s.Facts`, the consumer union (`Required`, `ReleasedBindings`, `ConsumerActivity`, requirement resolutions), and `snapshot.Ancillary`.

### A.3 Where `stale-impact-consent` is raised

- Identity rule: `internal/application/provider_change_consent.go:66-68` — `consent.PlanID != planID` → `stale-impact-consent`. `ValidateProviderChangeConsent` (52-57) also yields `invalid-impact-plan` on version/planID/confirmations defects (59-64).
- Post-consent re-plan comparison (the mechanism behind the CI failure signature):
  - `cmd/baha/application_provider_authorization.go:51-59` — after consent is granted, the plan is rebuilt (`buildResolvedApplicationPlan`) and `current.ProviderPlan.Impact.PlanID != plan.ProviderPlan.Impact.PlanID` → `stale-impact-consent` with the diagnostic line "authorization mismatch: provider-plan-id-after-revalidation" (57).
  - `cmd/baha/app_runtime_retirement.go:125-130` — same re-plan comparison for runtime retirement (`app down`/`destroy` non-reset).
  - `cmd/baha/app_apply_result.go:82-106` — `authorizeConfirmedApplicationEdit`: current plan missing (`95`) or authorization-surface divergence → stale / fresh consent.
  - `internal/application/external_provider_scope.go:245,267,283,290,298` — registry digest recheck inside the flock for external provider removal.
  - Machine path: `cmd/baha/app_machine_adapters.go:206-214` — `plan.PlanID != view.PlanRevision` → `conflict`; `stale-impact-consent`/`invalid-impact-plan` → `conflict`, confirmation codes → `approval_required`.
- Intent-level stale signals that share the same code: `application_provider_authorization.go:70,76,88,116` (source identity / manifest / target drift) and `target_definition_change.go:75`, `node_disconnect_client.go:190`, `control_plane_stop*.go`, `runtime_destroy_all.go:162`.

### A.4 The chain the CI failure signature describes

1. A provider instance is registered but its runtime observation is unavailable/ambiguous/failed → state `ProviderUnverifiable` (A.1).
2. Union: `preserve` + `p.Complete = false` (provider_union.go:164-168); plan: `ConfirmationsRequired = 2`, `Attention` set (provider_change_plan.go:90-100).
3. `Complete=false` and the fact `State` are both inside the PlanID digest (provider_change_digest.go:23,44). `observation.Revision` rides in `p.Revision` (provider_change_plan.go:43) and is a sha over live facts + file revisions (application_provider_impact_observation.go:56-68).
4. User/MCP acknowledges; the engine replans at `application_provider_authorization.go:51`. Any flip between `unverifiable` and a verified state (or a changed `Revision`) between plan and revalidation yields a different PlanID → `stale-impact-consent` at :59.

### A.5 Findings (slice A)

- **A-F1 (by design, but a real livelock surface).** The consent identity intentionally hashes volatile *observation* state, not just intent. A provider whose observation is intermittently unverifiable (a starting container, an ambiguous match, a transient `ps`/`inspect` error folded into the default per the `return`-on-error paths in A.1) makes the plan oscillate: the interactive flow acknowledges plan P1, the post-consent revalidation computes P2, and apply refuses with `stale-impact-consent` forever while flapping continues. Bounded only by retry luck, not by any stabilization rule. The digest does exclude RAM/container *counters* (provider_change_digest.go:73-78) and countdown samples (provider_change_digest.go:68-82) — the exclusion is deliberate and narrow; the `State` field itself remains digest input.
- **A-F2 (observation error absorption).** All observation adapters swallow loader/inspect/list errors and silently fall back to `ProviderUnverifiable` (e.g. `application_broker_observation.go:20-38`), so the reason a consent goes stale is never recorded or surfaced; the CLI only prints plan-id mismatch. Diagnosis of a `stale-impact-consent` failure cannot distinguish "state genuinely changed" from "docker/podman inspect errored twice in a row".
- **A-F3 (inconsistent unverifiable treatment in the external-reference lane).** `provider_union.go:164` lets exactly `OwnershipExternal + ScopeExternal + State == ProviderUnverifiable` count as a verified external reference, while `application_provider_container_observation.go` can only reach `ProviderUnverifiable` for such instances through the Layer-1 defaults. A *registered-but-changed* external instance (identity mismatch) is reported unverifiable by `application_external_receiver_change.go:110` yet is not distinguishable from a genuine BYO reference in the digest — both land as `State=unverifiable`; consent equivalence cannot see a registration swap without the registry digest change.
- **A-F4 (lock-free read windows).** See slice B: the plan/proposal side observes state outside the per-application lifecycle lock, which is the structural amplifier of A-F1.

## Slice B — race windows in add/remove/re-add (states that can remain without an error)

Lock architecture: mutations take a per-application `flock` (`.app_installation.lock`) or target-wide `.installation.lock` with a bounded 15s retry (`cmd/baha/application_lifecycle_lock.go:37-134`). The plan/proposal chain — `buildResolvedApplicationPlan` → `observeApplicationProviderFacts` (direct `docker/podman ps`, registry `Load()`) — runs **without** that lock on all three call sites: `cmd/baha/app_commands.go:320`, `cmd/baha/machine_http_executor_read.go:165`, `cmd/baha/mcp_tools.go:160`. Registry file reads are lock-free (`internal/capability/registry.go:447-464`); only `Update` takes the `.lock` flock (`registry.go:466-494`). Deployment records are saved by rename (`internal/deployment/deployment_store.go:595`) with no cross-process serialization for already-claimed identities (`:383-393`).

| # | Window | Mechanism (file:line) | End state if it hits | Error surfaced |
| --- | --- | --- | --- | --- |
| B1 | plan vs. post-consent revalidation | concurrent mutation by another actor changes registry/observation between `application_provider_authorization.go:22` (plan) and `:51` (replan) | apply refused `stale-impact-consent`, nothing mutated | yes (fail-closed) |
| B2 | read-side torn observation | `ps` succeeds at `application_broker_observation.go:35` while the app's containers are mid-restart → Running→Unverifiable flip inside the digest | B1 outcome; consent never stabilizes while flip persists | yes, but undiagnosable (A-F2) |
| B3 | retirement interrupted after `recordPendingApplicationRuntimeRetirement` | record `Observed.State = "retiring"` + `previous_intent` persisted (`application_runtime_retirement_record.go:41-53`); process killed before `recordVerifiedApplicationRuntimeRetirement` (`app_runtime_retirement.go:168-172`) | deployment stuck in "retiring" until the next retry completes verification; retry re-plans and re-consents | none until verify fails; state is durable |
| B4 | `retireRuntimePreservingData` partial teardown | workload containers destroyed (`app_runtime_retirement.go:155-159`), then a provider retirement adapter fails mid-way (`application_provider_retirement.go:79-140` returns error at any step) | workload gone, provider runtime partially retired, pending record "retiring", provider bindings partially released — all tolerated/retried on next run | partial: error returned, state intentionally retained |
| B5 | re-add racing same file paths | `app up` plan built while a concurrent destroy releases references (`ReleaseApplicationProviderReferencesAt`, `app_runtime_retirement.go:164`); up is lock-holding but its *plan display* was lock-free | union computed from stale registry → apply fails `stale-impact-consent` (B1) OR, if state settles identically, succeeds while displaying a plan that described resources that were already gone — the plan-vs-replan digest equality is the only guard | yes / no (if hashes coincidentally equal) |
| B6 | lock-free registry read | `RegistryStore.Load()` at `internal/capability/registry.go:447-464` (no flock, not atomic-rename-documented) concurrent with a `Save` inside another process's `Update` | rare: reader sees a torn/old registry; decode errors fail closed (good), a *stale* read passes silently into the digest and is caught at revalidation (B1) or not at all | no for the stale-read case |
| B7 | `verifyOwnershipWhenNoDeploymentRecord` | between `LoadDeploymentRecord` fail and the identity/proof check (`app_runtime_retirement.go:22-61`), a first apply by another session creates the record | destroy takes the never-delivered cleanup path against a now-live deployment, or (vice-versa) real deployment treated as never-delivered — the `VerifyNeverDeliveredProof` (:57) narrows but cannot close this without a lock | partially — proof catches most cases |
| B8 | concurrent identical first-claims | `SaveDeploymentRecord` registry-write-lock only guards *new* claims (`deployment_store.go:383-405`) | duplicate double-claim is structurally prevented for new identities; re-saves of claimed identities are lock-free and last-writer-wins by rename | none (by design) |

Worst tabulated outcome: **B3/B4 are the only windows where a state can legitimately "stay" without an error** — a persistent `retiring` record or a partially-retired provider set that a later re-add must resolve. Everything else is caught fail-closed by the plan-vs-replan PlanID comparison (B1/B5) — which is exactly what makes A-F1/B2 produce repeated, seemingly random `stale-impact-consent` instead of progress.

## Slice C — test coverage gaps (combinations with NO test)

Existing coverage baseline: unit tests for consent identity/staleness (`internal/application/provider_change_consent_test.go:23`, `provider_change_plan_test.go:175`, `external_provider_scope_test.go:83`), unverifiable-classification units (`cmd/baha/application_provider_container_observation_test.go`, `application_shared_sql_observation_test.go`), retirement-record units (`application_runtime_retirement_record_test.go`, `application_retired_owner_chain_test.go`), and plan-vs-replan tests (`app_machine_adapters_test.go:66 TestAppMachineAdaptersStalePlanConsentAndCancellation`, `app_edit_apply_test.go:160 TestAppEditApplyStalePlanAndWrongConsentWriteNothing`). add/remove/re-add exists as *runtime acceptance* suites: `TestSelectiveBackendRuntimeAddRemoveReAdd` (cmd/baha/app_backend_selective_runtime_test.go:20), `TestSelectiveIdentityRuntimeAddRemoveReAdd` (app_identity_selective_runtime_test.go:26), `TestSelectiveSecretsRuntimeAddRemoveReAdd` (app_secrets_selective_runtime_test.go:22) — all gated behind `BASEHARBOR_*_ACCEPTANCE` env (`t.Skip` when unset; wired only into `.github/workflows/targeted-integration.yml`, i.e. native-gate runs, not plain unit CI).

Gaps (combinatorial, checked against test names/flows in cmd/baha and internal):
- **C1.** re-add (up/apply) after a *failed/interrupted* remove that left a `retiring` deployment record — no unit or CI test drives `recordPending…` followed by a failed retirement and then an `add`; only the success→verify path is unit-tested (`application_runtime_retirement_record_test.go:15`).
- **C2.** add/remove/re-add at the *consent* level in one session: nothing asserts that after remove-consent and re-add the replayed acknowledgement yields `stale-impact-consent` (as PR #1663's CI run hit). The `app up` after `app down` path with a *reused* consent object has no test; `TestAppEditApplyStalePlanAndWrongConsentWriteNothing` covers edit-plan staleness only.
- **C3.** no test pins the oscillation contract of A-F1: a fact flapping `unverifiable ↔ running` between plan and post-consent revalidation (B2) — no unit simulates the digest flip. The revalidation comparison in `application_provider_authorization.go:55-59` is covered only by "changed state" fixtures, not by "same state, second observation errored" fixtures.
- **C4.** the error-absorption default of A-F2 is untested: no test asserts which of the `return`s in `observeBrokerProviderFacts`/`observeSharedBackendProviderFacts` produced the `ProviderUnverifiable` classification (there is nothing to assert — the reason is not modeled).
- **C5.** external-reference vs. unverifiable-native discrimination (A-F3): `provider_union_external_reference_test.go` covers the happy external lane; no test covers a *changed* external registration identity landing with the same digest shape as the unverifiable default.
- **C6.** no coverage that the plan/proposal read path runs concurrently with a mutation (B1/B5/B6): zero tests exercise plan-then-mutate-then-revalidate interleavings; `TestAppMachineAdaptersStalePlanConsentAndCancellation` simulates revision skew by construction, not by real concurrency.

## Unit test runs (static + unit only, no containers — R1 respected)

- `go test ./internal/application/ -count=1` → `ok 0.178s` (fast subset `-run 'TestDescribeProviderChanges|TestProviderChange|…'`), plus full package `ok 8.523s`.
- `go test ./cmd/baha/ -run 'TestRetirementRecord|TestDetectDamagedDeploymentState|TestRetainedOwnershipBand|TestCorelessDecision|TestCapabilityRemoval|TestAppEditApplyStalePlan|TestTargetDefinitionRejectsUnproven' -count=1` → `ok 0.129s` (compiled with GOCACHE/GOTMPDIR in /tmp because `/` on this coordinator host was at 100% — 648M free; note for the Owner: `go env GOCACHE` = /var/tmp/go-cache sits on the full root filesystem).
- Runtime acceptance suites (`BASEHARBOR_BACKEND_LIFECYCLE_ACCEPTANCE=1` etc.) were NOT run — they need native runtimes on the named SSH hosts, out of scope for this static hunt.

## Incidental findings (not in the mission slices, documented only, no changes)

- **I1 (defect, recommend a card).** `cmd/baha/app_edit_apply.go:372-376`:
  ```go
  if changeErr == nil && result.Status != "complete" {
      if true {
          fmt.Printf("DIAG_EXEC result.Status=%v outcomes=%d result=%+v\n", …)
      }
  ```
  A leftover debug print (`if true`) on the production `app edit` mutation path, writing a full `ProviderChangeResult` dump to the process stdout (bypassing the `out` writer, so it corrupts `--json`/machine output streams). Merge archaeology suggests it came from a diagnosis session and was committed to develop. This should be removed and regression-tested.
- **I2 (docs).** `docs/internal/v0.4.25-provider-mutation-coverage.md:522-544` documents the unverifiable↔consent relationship for native gates, but the oscillation/livelock surface (A-F1) and the lock-free read windows (slice B) are not described anywhere; a mechanism note in `docs/explanation/providers.md` would help future hunts.

## Cleanliness

- No containers/compose projects/networks/volumes were started on any host (static + unit tests only, R1). `docker ps` / `podman ps` not invoked; nothing to bring down.
- Scratch worktree: /tmp/opencode/hunt-ownership-wt (clone; safe to remove). Temporary Go build caches (/tmp/opencode/hunt-ownership-gocache, …-gotmp) were created and deleted in the same step.
- No product-repo commits; baseharbor develop untouched (`git ls-remote` witnesses at top and END).
- cleanliness: no lane-owned compose projects, no stray files in /home/marcel/dev/baseharbor-ecosystem; only evidence in baseharbor-plan.

## Evidence publishing witnesses

- `git ls-tree -r --name-only origin/main | grep hunt-ownership` → `evidence/r28-welle4-2026-11-18/hunt-ownership/befund-1.md` (present on origin/main).
- `git merge-base --is-ancestor 528f3cc5753f9b2c20e802e37faef2226b68c16d HEAD` → true; my evidence commit `caf52415` sits directly on top of the fetched origin/main tip `528f3cc5` with only other lanes' published evidence commits between them (`git log 528f3cc5..HEAD` lists no foreign candidate branches).
- Product-repo truth witness at END: `git ls-remote origin develop` → `8dccd4fe1a52bbcc61c67f7809079f33b8040d64` (unchanged), and the fresh clone's working tree carries 9 untracked scratch artifacts from the `go test` runs only (no tracked modification; nothing was committed or pushed to baseharbor).

END: pending (see END line after this section)

## END

END_DONE mission-hunt-ownership.md: BUG-HUNT 916 befund-1 published (evidence commit caf52415 on baseharbor-plan origin/main); findings: unverifiable-ownership chain (provider_union.go:164-168 → digest → stale-impact-consent at application_provider_authorization.go:59), 8 race windows (B3/B4 = persistent `retiring` state), 6 coverage gaps, plus defect I1 (`if true` DIAG_EXEC stdout leak at app_edit_apply.go:372-376). No product change.

