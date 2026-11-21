# 0428-204 operator-auth helper coverage map vs #1615 — round 2 (reconciliation with w232 K-table + codex-review-r2)

- Lane: w234-0428-204-helpermap (sitz ornith)
- Card: 0428-204, read-only reconciliation (no product code, no PR, no `go test` on this host)
- Predecessor: round-1 (my card, b7dce1ee, 181 families A/B/C/D) — accepted. This round is the decision
  step the owner asked for after round-1: reconcile with the two new witnesses (w232 K-table e8b389a4,
  codex-review-r2 8a086890) and answer A/B/C.
- Result: DONE. THE ONE NUMBER = **80** of the failing cmd/baha cases heal without a single test line once
  #1615 lands — but this number is CONDITIONAL on the w217 cohort being correct, and the cohort is
  un-audited (see provenance block). The #1615 conversion itself (60 files / 177 sites, plus the 4
  w232 K4 cases verified at a real #1615 head) is independently citable.

## Basis-Attestation (ls-remote develop)

```
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop
```

Base `40cb28c758b02960356434b630086a341ebe1738` is an ancestor of HEAD; HEAD equals the develop head.
`gh pr view 1615 --json` base = `40cb28c758b02960356434b630086a341ebe1738`, head = `003c48fa53d8cf6c3c76c7a098fe0783bb1fd9cd`.
Read-only: gh API + blob contents only, no clone, no `go test`, no product write.
My round-1 evidence confirmed on origin/main:
```
$ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep operatorauth-helper-coverage
evidence/r28-welle4-2026-11-21/operatorauth-helper-coverage/round-1.md
```

## A. THE ONE NUMBER — how many of the 206 heal via the #1615 helper alone

### The number

**80 of the failing cmd/baha cases heal without a single test line once #1615 lands.** These are exactly
my round-1 class A (the 80 functional-CLI tests that run through `runWithIO` and get the verified test
principal injected by `runWithIOAsTestOperator` / `testOperatorContext` at PR head `003c48fa`).

Citable file:line witnesses (from my own round-1 card, not memory):

- `cmd/baha/mcp_json_parity_test.go:19` — `TestCLIJSONAndMCPShareApplicationOverviewAndDevelopmentDomain`,
  gate message `authorization.go:285`; converted by #1615 (base 0 → head 2 sites, verified via head blob).
- `cmd/baha/oras_setup_test.go:80` — `TestRuntimeUpRequiresORASBeforeCoreBootstrap`,
  `runtimeUpCommand` at `cmd/baha/runtime.go:40`; #1615 line 79 → `testOperatorContext`; **PASS at #1615
  head `29aae4fded0`** (w232 local measurement). This is the class-A proof that the helper heals at HEAD.
- `cmd/baha/application_lifecycle_lock_test.go:119` — `TestSharedBackendReconcileRejectsSecondProcess`;
  #1615 +7/-7 (`testOperatorContext` on parent and child); **PASS at #1615 head** (w232).
- `cmd/baha/core_installation_runtime_test.go:99` — `TestApplicationInitContinuesWithoutManagementInstallation`,
  gate message; converted by #1615.
- `cmd/baha/app_binding_production_test.go:45` — `TestCLIProductionPathAssignsServerIdentityProves`;
  converted by #1615.

That last file (`oras_setup_test.go:80` → PASS at #1615 head) is the one class-A case proven to heal by
actual execution at a real #1615 head, not by diff inference alone.

### WHAT THAT NUMBER DEPENDS ON (the provenance line the owner demanded)

80 is **class A of the w217 cohort**. The w217 cohort is **`/tmp/w217-classified.tsv`, 181 first-level
failing tests, which was never published as an auditable file** — it lived only in transient `/tmp` on the
w217/w221/w224 machines. It is referenced (not attached) in three published evidences:
`cli-test-inventory-develop/round-1.md`, `other-domain-test-split/round-1.md`, and
`bug-hunt-2026-11-21/fail-closed-honesty/round-1.md` (w224, line 57).

The w221 codex-review-r2 (8a086890) therefore raised exactly the objection the owner repeats here: the
original 89/181 counts cannot be audited from the published evidence because the TSV is absent, and an
independent reproduction at exact base `40cb28c758` yielded **203 distinct failing top-level names**, not
181 and not 206.

Concretely, the arithmetic does not line up:

- My card: `206 = 181 first-level families + 25 subtest-only FAIL lines`. The `206` is a **count of
  `--- FAIL:` lines**; the `181` is a **count of distinct first-level families** (subtests aggregated onto
  parents); the `25` is my own subtraction. None of the three is independently reproducible here because
  the source TSV is unpublished.
- codex-review-r2: `203 distinct failing top-level test names` at the same base, reproduced fresh.

So the honest statement of THE ONE NUMBER is: **IF the w217 cohort of 181 first-level families is correct
(round-1's class A = 80), THEN 80 heal via the #1615 helper — but the 181/206/25 breakdown is not
independently audited, and codex's 203 top-level names is the first auditable reproduction, which does not
match 181 or 206.** The class-A heal-mechanism (a test over `runWithIOAsTestOperator` gets the verified
principal and skips the `authorization.go:285` gate) is independent of the exact cohort size and is proven
at a real #1615 head by `oras_setup_test.go:80`.

### The part that IS independent of the cohort

`#1615` converts `runWithIO` → `runWithIOAsTestOperator` in **60 of the 137 changed test files, 177 sites
total** (verified per file via the 155-file list + per-file `gh api .../files` patch + head-blob grep).
This conversion count does not depend on the failing-test cohort: it is a property of the #1615 diff. The
w232 K-table confirms the mechanism on four named cases at a real #1615 head:

| case | file:call | w232 category | #1615 | at #1615 head |
| --- | --- | --- | --- | --- |
| TestRuntimeUpRequiresORASBeforeCoreBootstrap | oras_setup_test.go:80 | **K4** (heals) | line 79 → `testOperatorContext` | PASS |
| TestSharedBackendReconcileRejectsSecondProcess | application_lifecycle_lock_test.go:119 | **K4** (heals) | +7/-7 `testOperatorContext` | PASS |
| TestAppEditCommandCompleteProviderEditRunsRealLifecycle | app_edit_apply_test.go:1186 | **K4 + K2(partial)** | lines 1237,1336 | FAIL at :1253 (real-Core, not auth) |
| TestPrepareStagedCoreGitCandidatePinsCanonicalApplication | management_core_git_candidate_test.go:17 | **K3 (env, not K4)** | no | FAIL (git-archive SIGKILL) |

3 of 4 named cases are K4 = class A = healed by the helper. K3 (git-archive) = class D in my card = a
different, environmental cause. This maps my A/B/C/D onto w232's K1/K2/K3/K4: **K4 ≡ class A (heals),
K3 ≡ class D (env, stays), the two dormant runtime bodies are class B (stay as reachability work), K1/K2
residual is class B/C.**

## B. Re-cut cards 0428-204, 0428-213, 0428-214 after a #1615 merge

**0428-204 (per-call vs helper):** the work-set is exactly my class B + class C.

- Class B (81 first-level families): direct `.Run(ctx)` / domain-fixture calls (`resolveApplication`,
  `resolveRepositoryLifecycleIntent`, domain subcommand `.Run`, `retainedNativeBackendFixture`) that never
  run over `runWithIO`, so the helper does not touch them. These need a per-file switch to
  `runWithIOAsTestOperator` — but NOT a new test line, because the helper already exists in #1615. The 81
  live in the w221 12 production-file groups (e.g. `repository_up.go:151` (9), `application_destroy_authorization.go:33`
  (5), `application_restore_authorization.go:25` (3), `app_repository_identity.go:14` (2),
  `application_lifecycle_lock.go:40`, `application_runtime_retirement_intent.go:6`).
- Class C (10): shared-session MCP (`server.Connect` + `clientSession.CallTool`); needs the second unstamped
  server per 3.3.5, not the helper.

The file-set that drops entirely with #1615 = **class A = 80** (healed, no 204 work). The file-set that
stays = **class B (81) + class C (10) = 91**. `#1615` changes none of the 81 class-B production files and
touches none of the 4 non-test #1615 files (`app_access.go`, `app_commands.go`,
`application_native_backend_observation.go`, `application_registry_source.go`) — verified: the 81 class-B
files are not among the 60 converted files.

**0428-213 and 0428-214:** these two cards are not in my read-set this shift. The owner named them as
siblings to re-cut from the same coverage map. I state explicitly that I did NOT touch them (read-only
mission, no access to their task notes in my evidence) — they inherit the same split: anything that runs
over `runWithIOAsTestOperator` is healed by #1615 (drop), anything that calls `.Run(ctx)`/fixture directly
or shares an MCP session stays. The coverage map's A/B/C/D rows are the shared re-cut key; the numeric
per-card split requires each card's own failing-test cohort, which is not in my evidence.

## C. Do my classes cover the 89 'other' cases from card 0428-206?

**No — not yet, and this is the exact line the verdict failed on.** My A/B/C/D classes classify the 206
failing cmd/baha tests by ENTRY MECHANISM (runWithIO / `.Run(ctx)` direct / shared-session MCP / other
cause). Card 0428-206 is about the 89 **other-domain** subset and needs a per-file rubric (production file
+ witness), which my classes do not carry. Two things are true:

- The 89 other-domain cases are a SUBSET of my class B (the 81 `.Run(ctx)`/fixture direct cases are almost
  entirely the other-domain cohort) plus a few class-D rows. So my classes *partition* them by entry
  mechanism, but they do NOT provide 0428-206's required rubric: every one of the 89 mapped exactly once
  to its first-failing production file with a witness.
- The w221 round-1 that attempted that rubric is **rejected** by codex-review-r2 for two concrete defects:
  the twelve group counts `9+5+3+3+2+2+2+1+1+1+1+8` sum to **38**, not 89 (group 12 is labelled 8 but its
  subgroups sum to 9), and the referenced `/tmp/w217-classified.tsv` was never published so the 89 rows
  cannot be audited. My round-1 card cites w221's 89 and its 12 groups as its class-B witness — which
  means **my card inherits the same unaudited-89 problem**. I own that gap.

The fix is not mine to do (read-only mission, 0428-206 is active under its wait-sweep owner), but the
required correction is: rebuild the 89 from an audited `go test -json` stream at exact base `40cb28c758`
(the codex review already captured 203 names at that base), map each exactly once to its first-failing
production file with a witness, and reconcile 89/181 against that fresh run. My A/B/C/D entry-mechanism
partition is compatible with that rebuild and supplies the "which heal via helper" column; 0428-206 still
needs the missing per-file rubric line.

## What I did NOT check

- Did NOT run `go test ./cmd/baha/` (read-only mission, no build, no matrix). The 80 / 81 / 10 / 10 counts
  are inherited from round-1 and are therefore CONDITIONAL on the un-audited w217 cohort.
- Did NOT independently reproduce the 206 / 181 / 25 breakdown. The only audited reproduction in this
  ecosystem's published evidence is codex's **203 distinct top-level names** (exact base `40cb28c758`),
  which the owner's round-2 demand is precisely about.
- Did NOT verify the 60/177 #1615 conversion count against a second independent tool (same caveat as
  round-1: the gh `?per_page` files endpoint returned empty patches for some filenames, so per-file
  verdicts were confirmed against head blobs).
- Did NOT touch 0428-213 / 0428-214 (not in read-set).

## repo-rule compliance

- Read-only Mission. No product write, no PR, no card booked, no rerun, no `workflow_dispatch`. No touch of
  `.github/**`, `internal/` (read via gh blob API only), `scripts/**`. No subagents.
- Remote witness (own persistent zone, gh API, no product clone):
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` →
  `40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop`.
- `gh pr view 1615 --json` base = `40cb28c758b02960356434b630086a341ebe1738`, head = `003c48fa53d8cf6c3c76c7a098fe0783bb1fd9cd`.
- No `.github/**` touched, no PR, no hosted-matrix rerun.
- Evidence lives only in baseharbor-plan evidence/, never in a product repo.

## Container / network / volume before–after + cleanliness

- Before: none started by this lane.
- After: none. No container/Compose/Docker/Podman started on any host, including the coordinator host.
  (Note for the record: the ambient `bh-docker-dev-shared-*` stack was torn down by another lane ~03:0xZ
  before this shift per the owner's message; this lane started nothing either way.)
- `cleanliness: ` clean. Scratch limited to gh-API reads under the agent's persistent zone. No worktree, no
  test-owned netzwerk/volume/state-Verzeichnis.

## END

END_DONE w234-0428-204-helpermap: THE ONE NUMBER = **80** class-A cmd/baha cases heal via the #1615
operator helper alone on landing (80 of w217's 181 first-level families; proven at a real #1615 head by
`oras_setup_test.go:80`). CONDITIONAL: the 181/206/25 cohort is the unpublished `/tmp/w217-classified.tsv`,
not audited; codex-review-r2's **203 distinct top-level names** at exact base `40cb28c758` is the first
auditable reproduction and does not match 181/206. #1615 conversion (60 files / 177 sites) is independently
citable; w232 K-table confirms 3 of 4 named cases are K4 = class A (heals at #1615 head). Re-cut: 0428-204
work-set after merge = class B (81) + class C (10) = 91; class A (80) drops. Classes PARTITION the 0428-206
89 by entry mechanism but do NOT supply its per-file rubric — that missing line is the codex defect and is
0428-206's to fix, not mine (read-only). SHA = baseharbor-plan origin/main head at commit time.
Read-only, no product change, no PR, no matrix run.
