# w385-0428-078-pr1855fix — Diagnose zur realen Keycloak-Attributions-Fehlerklasse

LANE w385-0428-078-pr1650pre. KARTE 0428-078. REPO baseharbor. PR #1855. MISSION 2026-11-27.
CHECKPOINT-PFLICHT 2026-11-27T08:38:21Z (Ornith-laptop-Ausfall bis 2026-11-28 18:00 Europe/Berlin): ALLES wird gesichert, kein weiterer Push.

## Git identity (visible ansatz block)

- Card frontmatter owner (verbatim): `(lane w385-0428-078-pr1650pre)` — full owner value `w385-0428-078-pr1650pre`.
- Git user.name / user.email: `w385-0428-078-pr1650pre` / `w385-0428-078-pr1650pre@baseharbor.local`.
- Commit invocation: `git -c user.name=w385-0428-078-pr1650pre -c user.email=w385-0428-078-pr1650pre@baseharbor.local commit/merge ...`.
- Pre-push gate line: `git show -s --format=%an HEAD` must equal `w385-0428-078-pr1650pre` exactly.

## Hop head (develop absorb)

- Absorbed develop head `ea5218d72e263f21e79853b679af50074dab8c25` into PR #1855 via `git merge --no-commit --no-ff ea5218d7...`, committed as **a6ae9031c** (author + committer `w385-0428-078-pr1650pre`).
- `git log --oneline ea5218d7..a6ae9031c` lists only the merge commit `a6ae9031c` on top of develop (the ancestor test holds; no foreign commit carried on top of the new develop base).
- Branch provenance (against the exact base head you fetched, ea5218d7): `git merge-base --is-ancestor ea5218d7 a6ae9031c` => TRUE (develop is an ancestor of the hop head).
- `git diff origin/<base>...HEAD --name-only` scope: the absorb only added the 26 develop commits; the PR's own product/test deltas remain in the parent history (d18e4b367 and its 6 ancestor commits). No force, no rebase, no squash.

## The three failing tests — root-cause diagnosis (all in one CI job)

Single GitHub Actions run on the exact head: run **45911769054**, event `pull_request`, head_sha `d18e4b367940ad5ee36862dbda1eea2d7a605db0` (EXACT-HEAD MATCH). All failing tests live in the single CI job `PR · Go unit · packages` (job 140221639232), package `github.com/mcpdev80/baseharbor/internal/...`. Mission's earlier report of three distinct jobs (140221639553, 140228648981) is corrected here: they are all the one Go unit job.

Three distinct test failures, each a DIFFERENT root cause:

1) `keycloak_signal_attribution_test.go:74` — `TestKeycloakSignalRegistrationTargetProductionAttribution`.
   - Failing log line: `attribution root = "docker-dev", want the producer's state root "/tmp/TestKeycloakSignalRegistrationTargetProductionAttribution3197917589/001/targets/docker-dev"`.
   - Root cause: the producer regression test decodes the service token and asserts `filepath.Clean(decoded) == filepath.Clean(stateRoot)` — the FULL path. The producer (`keycloakSignalAttributedService`, `keycloak_realization.go:290-296`) emits `keycloak@<dirname>:9000` — the DIRECTORY NAME only. So `decoded == "docker-dev"` != the full state root.
   - STATUS: OPEN. This is the attribution-TOKEN-SHAPE conflict. The Coordinator ruled (2026-11-27T08:30:20Z) that the token FORM is a product/contract decision routed to Owner Queue (OQ-3); DEFAULT is Option 1 (directory-name, witness+contract authoritative) IF the two other witness tests still prove dotted-collision separation. Neither the producer token NOR the test expectation is changed until the decision lands.

2) `identity_dashboard_witness_test.go:144` — `TestIdentityDashboardWitnessPositiveMatchesConcreteTarget`.
   - Failing log line: `the witness must be non-forgeably available for the concrete matching Target, got {SelectionConfirmed:true MetricPresent:false MetricCurrent:false TargetAuthorized:true Available:false}`.
   - Diagnosis: `MetricPresent:false` means the witness source loop filters the seed source OUT before the attribution check. The seed registers a correct shared-placement record (ID `keycloak:<installation project>`, Network = the witness's own network, descriptor = `KeycloakIntegration` so Mode/Protocol/Path/Verification match the reference). The witness's descriptor-match guard at `identity_dashboard_witness.go:205-209` (`source.Mode != expectedSignal.Mode || Protocol || Path || Verification`) is the most likely filter, OR the network equality guard at line 214. Both must be traced to a concrete assertion; the source is present in ListAll but dropped.
   - STATUS: OPEN. Under diagnosis (do NOT guess a product delta; token form frozen per OQ-3).

3) `identity_dashboard_witness_test.go:445` — `TestIdentityDashboardWitnessRootAttributionResolvers` (direct unit test of `keycloakRecordTargetRoot`).
   - This is the clearest REAL witness defect: the colliding-project case (`project = TargetInstallationProject("a-b")`, root = dottedRoot, witnessName "a.b"`) must return `""` (fail closed) but the witness returns the witnessed root.
   - Root cause candidate: `keycloakProjectNamesTarget` (`identity_dashboard_witness.go:430-452`) line 438 checks `project == TargetInstallationProject(targetName)` — for targetName "a.b" it computes `TargetInstallationProject("a.b")`, but the record carries `TargetInstallationProject("a-b")`, which differ, so it falls through to the `bh-` prefix branch and matches on `projectTokenFor("a.b") == "a-b"` (dots-to-hyphens) => returns TRUE. The injective binding is supposed to come from the attribution token, but the test record's token `keycloak@a.b:9000` ALSO encodes the dotted root, so the token guard at line 401 passes too. The witness therefore does NOT reject a record whose production project belongs to a DIFFERENT (colliding) Target.
   - This is a genuine per-Target binding gap IN THE WITNESS (production code), independent of the producer token-shape question. It must be fixed by making `keycloakRecordTargetRoot` require the record's project to name the SPECIFIC witnessed target (not just a colliding one) — OR by tightening the token to be unambiguous — WITHOUT changing the producer token FORM (still frozen pending OQ-3).
   - STATUS: OPEN. Diagnosis complete; fix must respect the frozen token FORM.

## What is frozen (Owner/Coordinator ruling 2026-11-27T08:30:20Z)

- Producer token FORM (`keycloak@<dirname>:9000` vs `<uri-encoded full path>`) — DO NOT CHANGE until OQ-3 decision.
- Producer regression test expectation at `keycloak_signal_attribution_test.go:73` — DO NOT CHANGE until OQ-3 decision.
- No guessed product delta: neither the witness nor the producer is edited based on a guessed token shape.

## OPEN — next hand (not continued here, laptop down)

1. Confirm which witness guard drops the seed in failure #2 (trace Mode vs network equality at `identity_dashboard_witness.go:205-209` vs `214`).
2. Confirm failure #3 fix path that respects the frozen token FORM: tighten `keycloakProjectNamesTarget`/`keycloakRecordTargetRoot` so a colliding-Target project fails closed, without touching the producer token grammar.
3. When OQ-3 lands (default Option 1 = directory-name): re-verify failures #1, #2, #3 all pass on the directory-name token; if #1 still fails because the test expects the full path under Option 1, the test expectation itself is the over-broad part and belongs to the Owner/contract decision, not a worker guess.

## Cleanliness

- No docker/podman containers started. `docker ps -a` witness: no w385 containers.
- Product worktree `workers/worktrees/w385-0428-078-pr1855fix` detached HEAD `a6ae9031c`, working tree clean after hop commit.

## END

`END_BLOCKED w385-0428-078-pr1650pre: Laptop down (checkpoint 08:38:21Z). Hop committed a6ae9031c (absorb develop ea5218d7, lane identity an+cn). Three failing tests ALL in CI job PR · Go unit · packages / run 45911769054 on exact head d18e4b367 — corrected from earlier "three jobs" report. #1 keycloak_signal_attribution_test.go:74 = token-shape conflict (producer emits dirname, test wants full path) FROZEN for OQ-3. #2 witness TestIdentityDashboardWitnessPositiveMatchesConcreteTarget:144 MetricPresent:false = seed source dropped by witness guard (Mode/network) — trace pending. #3 witness keycloakRecordTargetRoot colliding-project case returns wrong root = REAL witness per-Target binding gap, fix must respect frozen token FORM. No product change made (frozen). Next: trace guard #2, design frozen-form-compatible witness fix #3, await OQ-3 on token form.`
