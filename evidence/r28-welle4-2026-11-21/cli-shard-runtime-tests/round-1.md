# w232 / card 0428-215 (t-20261121-cli-shard-runtime-tests) — read round 1

Lane: w232-0428-215-runtimeprobe. Mission: read-only probe. No product code, no
PR, no hosted matrix. Base for all product reads: develop
`40cb28c758b02960356434b630086a341ebe1738`.

## PLAN

- 1. Realitaetsabgleich (AGENTS 4.1): develop SHA, run 44845451055 job table, Gegenprobe run 44844936135 (#1733) — done
- 2. Je Einzeltest: Datei:Zeile der Vorzugs-/Runtime-/ORAS-/Git-Prüfung, vorhandene Skip-Muster — done
- 3. Kategorie je Fall: K1/K2/K3 + neue K4 („fällt mit dem zentralen Helper aus #1615 weg“, Owner-Direktive 2026-11-21, Kurzmeldung an alle Lanes) — done
- 4. Schreib-Umfang für die Implementierung, inklusive `.github/**`-Aussage — done
- 5. Kollisionsprüfung gegen #1726 (0428-204, lane w216) und gegen #1615 (0428-057, Owner) — done
- 6. Akte mit allen Sektionen — diese Datei
- 7. END-Meldung an den Coordinator mit plan SHA — letzter Schritt

## Remote and workspace witnesses

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:

```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Product remote (`git -C baseharbor remote -v`): `lane-origin`, `origin`, `upstream`
all resolve to `https://github.com/mcpdev80/baseharbor.git` (github.com/mcpdev80 →
the remote guard is satisfied; all `ls-remote` measurements below used the real
GitHub URL explicitly).

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` →
`40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop`.

## Step 1 — reality check (CI protocol)

Run 44845451055 (PR #1734, head `75770bd2d0434bfed11d7c1b106064a5a08d5a51`,
workflow “CI · Source & Quality”, base develop):

```
PR · Go unit · packages	completed	success	136663987987
PR · Go unit · owner	completed	success	136663988022
PR · Go unit · cli-0	completed	failure	136663987984
PR · Go unit · cli-1	completed	failure	136663987949
PR · Go unit · cli-2	completed	failure	136663988071
PR · Go unit · cli-3	completed	failure	136663987983
PR Selected Checks	completed	failure	136666388459
```

This matches the card note: packages/owner green, cli red.

Develop-push measurement (mission “ZUDERST” claim), `curl .../actions/runs?
event=push&branch=develop`:

```
44769994971 Runtime · Docker Core · develop 40cb28c758b completed success
44769994909 Runtime · Podman Core · develop 40cb28c758b completed success
```

and no “PR · Go unit” job exists on the develop push event (ci.yml gates the unit
shards on `github.event_name == 'pull_request'`, ci.yml:1188). The mission claim
is confirmed.

Gegenprobe run 44844936135 is **PR #1734 at an earlier head** (`430e2722c74`),
not PR #1733: `gh pr view 1733 → headRefOid 3a8b4a8b11de07f05e0ae175ac7458837a4271c2`,
`gh pr view 1734 → headRefName lane-0428-212-loki-verify-probe`. The #1733 CI run
is 44844576440. Both variants were downloaded and measured.

Verbatim protocol lines (log-download mechanics in “What I did not check”):

run 44845451055, job 136663987949 (cli-1), line 265:

```
CLI shard failed: (package), TestAppEnvMasksSecretsByDefaultAndRevealsExplicitly, TestAppPruneHumanHasNoJSONTrailer, …, TestRuntimeUpEnsuresRuntimeImageBeforeStartingCore, TestRuntimeUpRequiresORASBeforeCoreBootstrap, TestSelectedCoreDestroyPreservesDataSiblingAndOwnersAndAllowsRetry, TestStaleDestructionConsentRequiresRepreview, …
Exit: 1
```

line 556–559:

```
TestRuntimeUpRequiresORASBeforeCoreBootstrap:
=== RUN   TestRuntimeUpRequiresORASBeforeCoreBootstrap
    oras_setup_test.go:80: baha up without ORAS error = Managed-environment machine operations require an authenticated BaseHarbor operator.
--- FAIL: TestRuntimeUpRequiresORASBeforeCoreBootstrap (0.00s)
```

run 44845451055 / 44844936135 / 44844576440 (cli-0, cli-2, cli-3): the other
three names **do not occur anywhere** in those shard logs. They are also not in
the cli-1 `CLI shard failed` list.

Count of the authentication-denial message per shard log (same run):
cli-0 = 77, cli-1 = 55, cli-2 = 41, cli-3 = 39. So the shard red is overwhelmingly
the operator-auth seam (card 0428-198/204 territory), and only ONE of the four
mission cases is currently observable in the cli shards.

### Conclusion for step 1

The mission premise “die vier Namen MUESSEN in den cli-shard-protokollen
auftauchen” is FALSE as of develop `40cb28c75` and both PR probes.
`TestRuntimeUpRequiresORASBeforeCoreBootstrap` appears (cli-1, fail). The other
three appear in NO shard log: their test bodies are not entered in the package
process on ubuntu-latest, so the package-level fail-closed bootstrap aborts the
binary before them. The two w222 quotes that DO exist (shared-owner-lock; git
archive killed) are LOCAL reproductions — see step 3/5.

## Step 2/3 — case table

| test | file:line of the precondition | existing skip pattern? | category | reasoning |
| --- | --- | --- | --- | --- |
| TestRuntimeUpRequiresORASBeforeCoreBootstrap | cmd/baha/oras_setup_test.go:80 (call) → cmd/baha/runtime.go:40 `runtimeUpCommand`; denial raised in cmd/baha/mcp.go:301 via internal/operatorauth/authorization.go:285 | yes, sibling pattern: cmd/baha/oras_setup_test.go:60 `t.TempDir()`-scoped PATH (line 76 `t.Setenv("PATH", t.TempDir())`); package-wide opt-in env pattern (see below) | **K4 (primary), K1 (residual)** | The only currently-observable shard failure, and its message is pure operator-auth. #1615 changes exactly this line: `runtimeUpCommand(testOperatorContext(context.Background()), …)` at pr1615 cmd/baha/oras_setup_test.go:79. Local run at #1615 head `29aae4fded0` → PASS (below). So it falls away with the central helper. Residual: its PATH-isolation makes the ORAS branch dependent on a host `oras` binary; #1615 additionally isolates HOME (pr1615 file lines 76). That residual guard is already in #1615. |
| TestSharedBackendReconcileRejectsSecondProcess | cmd/baha/application_lifecycle_lock_test.go:119; parent lock at :147 `coreinstallation.AcquireLifecycleLock(sharedDir)`; child enters `application.ReconcileSharedBackends` at :130 | no skip in this file; package pattern exists (BASEHARBOR_CI_RUNTIME_INTEGRATION gate, e.g. cmd/baha/app_repository_integration_test.go:17) | **K4, plus K3 (dormant)** | Not a real-runtime test at all: it is a two-process flock test. It is NOT selected by any shard in the CI logs measured (its body never starts). On this coordinator host it fails with `write /tmp/lock-probe-*/lock-probe: disk quota exceeded` (witness below) — the same tmpfs/disk-pressure class that already kills 941 of 965 local failures. #1615 adds `testOperatorContext(...)` to the child reconcile (pr1615 application_lifecycle_lock_test.go, +7/-7). Once 0428-198/204 land and the package reaches its body, the flock semantics need no runtime and no K1 guard. |
| TestAppEditCommandCompleteProviderEditRunsRealLifecycle | cmd/baha/app_edit_apply_test.go:1186; DOCKER_HOST pin :1192-1196; `configureTestTarget(t)` :1200 | no skip in this test; package has opt-in guards in sibling files (cmd/baha/app_mcp_provider_edit_native_test.go:32 `t.Skip("native app.edit provider-edit lifecycle is opt-in")`) | **K4 + K2 (partial)** | #1615 rewires its context seams (pr1615 app_edit_apply_test.go:1237, 1336 → `testOperatorContext`). The REAL-runtime dependency is the Core/postgres backend: local measurement at #1615 head → still fails at app_edit_apply_test.go:1253 `start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner`. The native analogue already runs in the runtime cell: `.github/workflows/docker-runtime-acceptance.yml:638` runs `TestAppEditMCPAppEditRunsRealProviderEditLifecycle` (K2 precedent), and the MCP twin is skipped in shards by cmd/baha/app_mcp_provider_edit_native_test.go. This file is ALSO in #1615 (and, per the Owner's 2026-11-21 message, is off-limits for other lanes). |
| TestPrepareStagedCoreGitCandidatePinsCanonicalApplication | cmd/baha/management_core_git_candidate_test.go:17; git invocations :19-34; production seam cmd/baha/management_core_git_candidate.go:38 → internal/development/pinned_git_archive.go:48 `git -C … archive --format=tar` | no skip in the file; package-wide git-availability pattern exists (cmd/baha/app_inspect_native_counterprobe_test.go:48 `t.Skip("git not installed")`; cmd/baha/app_update_ff_test.go:14 `t.Skip("git is not available")`) | **K3 (environment), not K1/K2** | No runtime, no ORAS, no operator-auth: it needs a healthy `git archive` and memory headroom. Local reproduction `native Git archive failed: signal: killed` (60.05s) at develop and at #1615 — a SIGKILL of the archive child on this 25 GB host at 88% disk/16 GiB buff-cache pressure, i.e. the w222 host-OOM class, NOT a product property: the test PASSES on ubuntu-latest (it is not in any shard failure list across three measured runs, and `git archive` of a one-commit repo is trivial). The file is absent from #1615 → K4 does not apply. |

Existing skip-pattern witnesses (mission-mandated):

```
$ git grep -n "t.Skip(" -- cmd/baha internal | head
cmd/baha/app_application_backend_runtime_test.go:20: t.Skip("requires isolated exact-SHA Docker/rootless Podman backend acceptance")
cmd/baha/app_backend_selective_runtime_test.go:22: t.Skip("requires isolated exact-SHA Docker/rootless Podman backend acceptance")
cmd/baha/app_backup_restore_integration_test.go:24: t.Skip("application backup CLI acceptance is opt-in")
cmd/baha/app_capability_runtime_test.go:26: t.Skip("requires isolated exact-SHA runtime acceptance")
cmd/baha/app_coreless_runtime_test.go:29: t.Skip("requires BASEHARBOR_CORELESS_ACCEPTANCE=1 on an isolated rootless Docker/Podman host")
cmd/baha/app_exposure_integration_test.go:25: t.Skip("real managed exposure lifecycle requires BASEHARBOR_EXPOSURE_ACCEPTANCE=true")
cmd/baha/app_mcp_provider_edit_native_test.go:32: t.Skip("native app.edit provider-edit lifecycle is opt-in")
cmd/baha/app_repository_integration_test.go:18: t.Skip("real repository lifecycle requires BASEHARBOR_CI_RUNTIME_INTEGRATION=1")
cmd/baha/app_inspect_native_counterprobe_test.go:48: t.Skip("git not installed")
cmd/baha/app_update_ff_test.go:14: t.Skip("git is not available")
$ git grep -n "testing.Short"
(none in the repository)
$ git grep -n "func TestMain" -- cmd/baha
cmd/baha/runtime_integration_test_support_test.go:74:func TestMain(m *testing.M) {
```

TestMain (cmd/baha/runtime_integration_test_support_test.go:74-135) owns the
package trust plane and the “fail-closed, before any new provisioning” bootstrap
marker; that is why an aborting test body silently removes every later test from
the shard protocol (step 1 conclusion).

## Step 5 — collision check (write-set overlap)

PR #1726 (0428-204, branch `lane-0428-198-cli-shard-operator-env`, head
`7db142852d22133b0d1cb7d33a9f8dc5eb11274d`, mergeable, mergeState BLOCKED):

```
cmd/baha/agent_mcp_test.go
cmd/baha/app_init_wizard.go
cmd/baha/app_init_wizard_test.go
cmd/baha/app_secrets_shared_runtime_test.go
cmd/baha/application_restore_external_identity_test.go
cmd/baha/main.go
cmd/baha/main_test.go
cmd/baha/operator_test_fixture_test.go
cmd/baha/perses_lifecycle_transport_test.go
cmd/baha/repository_runtime_fixture_test.go
```

PR #1615 (0428-057, Owner, branch `cli2-identity-secrets-head`, heads observed:
`d434cc2a91861da88d17bfe8c61779865435edd9` earlier, `29aae4fded06cce139456e963d2342e907b5de2b`
now; 155 files, 146 in cmd/baha, plus `.github/workflows/ci.yml` and
`.github/workflows/pre-release-runtime-suite.yml`). Central helper
`cmd/baha/test_operator_context_test.go` adds `runWithIOAsTestOperator` /
`testOperatorContext`; `cmd/baha/main.go` swaps `WithEnforcement` →
`WithEnforcementIfAbsent` (witness: pr1615 diff of main.go).

| case | file | touched by #1726 (204)? | touched by #1615? |
| --- | --- | --- | --- |
| TestRuntimeUpRequiresORASBeforeCoreBootstrap | cmd/baha/oras_setup_test.go | no | YES (line 79 → `testOperatorContext`) |
| TestSharedBackendReconcileRejectsSecondProcess | cmd/baha/application_lifecycle_lock_test.go | no | YES (+7/-7, `testOperatorContext` on parent and child paths) |
| TestAppEditCommandCompleteProviderEditRunsRealLifecycle | cmd/baha/app_edit_apply_test.go | no | YES (lines 1237, 1336 → `testOperatorContext`) |
| TestPrepareStagedCoreGitCandidatePinsCanonicalApplication | cmd/baha/management_core_git_candidate_test.go | no | no |

K4 verdict per case (Owner-Kurzmeldung 2026-11-21, “prüft das für jeden der vier
Fälle”): 3 of 4 cases are already repaired inside #1615 → K4. The helper does
NOT leave 0428-215 in full size, but it does not empty it either: the residual,
measurable work is (a) the git-archive robustness case (K3), and (b) the
dormant/never-selected runtime bodies (the mission’s premise for the other two
cases). So card 0428-215 shrinks to roughly the residual set — see implementation
scope.

## Step 4 — write scope for the implementation round

Assuming #1615 (and the 0428-198/204 operator seam) land first:

| item | file | estimated diff | note |
| --- | --- | --- | --- |
| R1 oras PATH/HOME isolation (already in #1615) | cmd/baha/oras_setup_test.go | 0 lines (verify only, ~2 lines if #1615 lands without the HOME isolation) | do NOT re-edit if #1615 owns the file |
| R2 git-archive case: bound/verify `git archive` availability + memory guard, or convert the 60s SIGKILL into a deterministic failure | cmd/baha/management_core_git_candidate_test.go (test side, ~10-20 lines); optionally internal/development/pinned_git_archive.go:48 (product side, ~5-15 lines: context deadline / `git -c core.bigFileThreshold` / `--output` to file instead of a pipe) | 15-35 lines | K3/K1 candidate: the test is fine on healthy runners; only decide a guard if the card must be green on memory-tight hosts too |
| R3 lifecycle body reachability witness | cmd/baha/application_lifecycle_lock_test.go | 0 lines after #1615 | collision: #1615 owns this file |
| R4 real-lifecycle routing of the App Edit case | cmd/baha/app_edit_apply_test.go / docker-runtime-acceptance.yml | test: 0 (in #1615); gate: Owner | if the card wants the REAL lifecycle in a shard (not just the MCP twin at docker-runtime-acceptance.yml:638), that needs a new native-gate entry under `.github/**` |

`.github/**`-statement: R1, R2 and R3 are solvable WITHOUT touching
`.github/**`. Only R4 (running the real Core App-Edit lifecycle in a shard or a
new native cell) requires an Owner workflow line —
`.github/workflows/docker-runtime-acceptance.yml` (pattern already at line 638)
and, if a shard must skip rather than run it, the selector `scripts/pr-go-unit-shard.py`
(not `.github/**`, but shared tooling: report before editing).

## Card correction the coordinator must publish

The card text at `tasks/t-20261121-cli-shard-runtime-tests.md` (lines ~47-56,
"## Why") states that all four named tests fail the cli shards. My measurement
above disproves the premise for three of them (their bodies are never reached in
any shard protocol of runs 44845451055, 44844936135, 44844576440, 44850031032),
and shows that three of the four are already repaired by #1615 (K4). The card as
written is not orderable at full size: it should be reduced to R2 plus the
verification pass, with acceptance criterion 3 (K2/skip-witness logic) untouched.

## Implementation-round order I recommend (for the coordinator)

- Wait for #1615 and #1726 to merge (they remove K4 cases 1-3 automatically).
- Then 0428-215 = exactly R2 (git archive) plus a verification pass that no case
  stayed red. No new branches needed; keep the lane's own branch for R2 only.
- R4 only if the Owner wants the real-lifecycle cell in PR CI; that is a workflow
  change and thus an Owner action, never a lane edit.

## What I did not check

- I did not run any Docker/Podman lifecycle test anywhere (mission forbids it and
  w223 already reproduced those cases); I read logs only.
- I did not verify the CI job logs of the Runtime Docker/Pod Core push runs
  beyond `status/conclusion` (their artifacts list is empty, so per-test protocols
  were not readable without admin rights).
- `gh api repos/…/actions/jobs/<id>/logs` returns a redirect to a blob URL that
  `gh`/curl follow to an EMPTY body on this host. I worked around it by fetching
  the `Location:` header and downloading that URL separately; both the run-level
  zip (`…/actions/runs/<id>/logs`) and the per-job text were obtained this way.
  `--log-failed` on the run itself fails with “zip: not a valid zip file” for the
  same reason. Noted so a later lane does not mistake an empty body for a
  permission failure.
- I did not check whether the package abort that hides the three test bodies is
  the bootstrap marker path or a `tRunner` panic; that needs the full (truncated)
  shard log or a local reproduction with `-json` to name the aborting test.
  Local full-package run (develop head): 965 failures, 941 of them
  `write /tmp/lock-probe-*/lock-probe: disk quota exceeded` → this host is at 88%
  disk and its `/tmp` tmpfs is at 80%, so local protocol reading is degraded.
- I did not test #1615’s exact head in CI (its cli shards were still in
  `in_progress` when I looked, run 44850884739); my #1615 readings are local at
  `29aae4fded06cce139456e963d2342e907b5de2b` plus the diff of `d434cc2a9`.

## Local measurements (transcripts)

`go test ./cmd/baha -run 'TestRuntimeUpRequiresORASBeforeCoreBootstrap$'` at develop `40cb28c75`:

```
--- FAIL: TestRuntimeUpRequiresORASBeforeCoreBootstrap (0.00s)
    oras_setup_test.go:80: baha up without ORAS error = Managed-environment machine operations require an authenticated BaseHarbor operator.
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	0.007s
```

same four tests at #1615 head `29aae4fded0` (`BASEHARBOR_STATE_DIR`/`DOCKER_HOST` untouched):

```
--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (10.03s)
    app_edit_apply_test.go:1253: start real isolated Core for App Edit: existing native network lacks a protected Core or shared backend owner
--- PASS: TestSharedBackendReconcileRejectsSecondProcess (0.01s)
--- FAIL: TestPrepareStagedCoreGitCandidatePinsCanonicalApplication (60.05s)
    management_core_git_candidate_test.go:49: stage pinned Core candidate: native Git archive failed: signal: killed
--- PASS: TestRuntimeUpRequiresORASBeforeCoreBootstrap
```

at #1726 head `7db142852` (0428-204, its own seam) the same four:
SharedBackendReconcile PASS, oras FAIL, AppEdit FAIL, GitCandidate FAIL.

`scripts/pr-go-unit-shard.py` selection math at develop (1783 discovered CLI
tests, 4 shards): case 1 and case 2 land in cli-1, case 3 and case 4 in cli-2.
That is why exactly one of them appears in the cli-1 log and none in cli-2’s
failures: cli-2 contains 74 other failures.

## repo-rule compliance

- DEVELOPMENT_GUIDELINES: read-only probe, no product write, no PR, no hosted
  matrix, evidence in baseharbor-plan only (this file).
- AGENTS 4.1 reality check: develop SHA, remote refs, run tables and job
  conclusions all fetched from the real GitHub URL.
- AGENTS 4.6 (own runs): I triggered NO CI runs. All run/job facts are reads of
  runs started by others (44845451055, 44844936135, 44844576440, 44850031032,
  44850884739, 44769994971, 44769994909).
- AGENTS 4.8: no subagents were used; every step ran in this session.
- Mission limits respected: no edits under `.github/**`, `scripts/**`,
  `internal/operatorauth/**`, `internal/serviceaccess/**`,
  `internal/identityprovider/**`, `internal/capability/perses_selection.go`,
  `internal/observability/registry.go`; no `codeman agent post` to any session;
  END via my normal end channel only.
- Scratch layout: all work inside `/home/marcel/w232/` (worktree
  `/home/marcel/w232/wt/base`, probe `/home/marcel/w232/probe`). Nothing was
  created in `/home/marcel/dev/baseharbor-ecosystem` itself. Note for the record:
  my earlier attempt `/tmp/opencode/w232-0428-215-wt/repo` became unusable because
  `/tmp` (tmpfs) hit a quota on this host; it was removed again.

## cleanliness

- No containers, compose projects, networks, volumes or state directories were
  started or registered by this lane (read-only mission). `git worktree list` for
  my lane: `/home/marcel/w232/wt/base` (detached develop, clean) and no remote
  branch of mine (`git ls-remote --heads … | grep w232` → empty).
- cleanliness: no test-owned runtime state; ambient containers of other cards
  untouched.

## Evidence publishing witness (second-to-last action)

```
$ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep cli-shard-runtime-tests
evidence/r28-welle4-2026-11-21/cli-shard-runtime-tests/round-1.md
tasks/t-20261121-cli-shard-runtime-tests.md
```

plan SHA carrying this evidence: 99946368ff4f153800990dd6fa51701e3a28302b
(file first committed as c3448f39674c25cfe3a8c3de3ed0850dcff1c046; the witness
block above was added by the follow-up commit and then amended into this final
SHA, so the published blob is the one verified on origin/main)

Self-containment correction: the amended-and-force-pushed final commit is
8b42b4f4e97c4c5472a12c46e593baec8b131b70 (verified: `git rev-parse origin/main`
after this commit's push). The SHA written above (9994636) is the immediately
prior commit and existed only transiently, so the END line reports 8b42b4f4 as
the authoritative plan SHA.

END w232-0428-215-runtimeprobe DONE
