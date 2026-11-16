# 0428-082 Perses infrastructure dashboards — round-4 (dispatch-run 43968469748 triage)

Card: t-20261114-r28-perses-dashboards · PR #1665 · candidate base d2a9cd11d
Trigger: coordinator dispatch run 43968469748 (workflow_dispatch, CI · Source & Quality, head d2a9cd11d) —
TERMINAL FAILURE. Mission order: (1) PR-context trap, (2) else real compose-cell repro.

## PLAN

1. Pull and classify run 43968469748 logs — done (6 failed tests, 2 causes; see (1))
2. PR-context trap check — done: (a) ORAS gate CONFIRMED for 5 tests; (b) postgres root-user check proven a
   dispatch-runner property (fails identically on foreign sibling chains 077/078; passes on every PR run and on
   develop push cells)
3. Qualification witness — done: exact command + env replayed on a rootless-docker host, both causes reproduced
   and explained (see (3))
4. Postgres/repro branch — done (see (4))
5. Fix or justified finding — done: justified finding only; NO product change by this lane (see (4b)); branch
   d2a9cd11d stays untouched (mission rule), PR stays DRAFT on base w083-perses-datasources
6. This akte committed + pushed to baseharbor-plan origin/main — witness below
7. Compose hygiene + END post — done (ps-witness below)

## Wrong-zone checkout attestation

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main` before the first
evidence commit (output in the git-receipt section). Planning repo = the ecosystem-root baseharbor-plan only.

## (1) Classification (exact witnesses from the run log)

Run 43968469748, job `validate`, step "Run runtime integration tests serially". Failed tests (go test -json, 6):

- cmd/baha: TestRepositoryWorkflowRealLifecycle (app_repository_integration_test.go:27),
  TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI (:60), TestRepositoryComposeWorkloadOnlyLifecycleInCI (:191),
  TestRepositoryComposePinnedWorkloadLifecycleInCI (:347), TestRepositoryBuildWorkloadRebuildsSourceChangesInCI (:503)
  — ALL five with the identical first-provision error: "prepare BaseHarbor integration trust plane: ORAS is required
  before Core setup; install it manually or rerun 'baha up' in an interactive terminal…" (each fails in 0.07-0.09s).
- internal/application: TestMultiInstanceComposeLifecycleInCI (runtime_multi_integration_test.go:102) after 11.67s:
  "postgres-analytics runtime security: bh-local-multi-ci-202343-dev/postgres-analytics runs as root (Config.User=…)".

## (2) PR-context trap — CONFIRMED (5× ORAS), file:line

The dispatch event lacks `github.event.pull_request` fields, and the ORAS provisioning step is PR-gated:

- `.github/workflows/ci.yml:499-501` (develop version): "Install verified ORAS for native Core bootstrap" →
  `bash scripts/ci-install-oras.sh` — this step lives ONLY in the `pr_native_selected` job, whose gate at
  ci.yml:477 reads `if: github.event_name == 'pull_request' && … && github.event.pull_request.draft == false`.
  Under workflow_dispatch the job is skipped (run witness: all 24 PR · jobs = skipped).
- The `validate` job's "Run runtime integration tests serially" step (ci.yml:353+, env block at run log
  22:25:16.92: only BASEHARBOR_TEST_DATABASE_URL / TEST_RUNTIME / CI_RUNTIME_INTEGRATION / PROVIDER scopes) installs
  no ORAS. The 5 cmd/baha tests then hit the Core bootstrap `baha up --control-plane-only --yes`
  (cmd/baha/runtime_integration_test_support_test.go:785) → cmd/baha/runtime.go:190
  (`ensureORASForCoreUp(parent, in, out, opts.Yes)`) → cmd/baha/oras_setup.go:36-40: non-interactive
  (orassetup: `!noInput(ctx) && !assumeYes && readerIsTerminal(in)` → interactive=false under -yes) and
  `exec.LookPath("oras")` ErrNotFound → hard error (oras_setup.go:38). PATH self-include
  (cmd/baha/main.go:130 → oras_setup.go:125-145) only helps when ~/.local/bin/oras exists.
- CONCLUSION: the 5 failures are 100% dispatch-context artifacts of the PR-only ORAS step — not this card's
  content, not the chain: the same tests pass in every pull_request run of this branch (Draft Go jobs SUCCESS on
  3a4599539/f3b91a34d) and on develop pushes. FINDING for the Owner-pin (TRIAGE allowlist): the `validate` job's
  runtime-integration step should run `bash scripts/ci-install-oras.sh` for non-pull_request events
  (file:line: .github/workflows/ci.yml, "Run runtime integration tests serially" step; the reusable install script
  already exists at scripts/ci-install-oras.sh). I do NOT edit .github/** (Owner scope) and the empty follow-up
  commit cannot qualify (base allowlist still blocks pull_request runs for base=w083-perses-datasources).

- Path A (the named host): cell run started — the qualification mirror below ((3c)) is this exact command on the
  baha-docker cell.

## (3x) NOTE — the session-host run appended below is NOT a valid witness

## (3) Qualification witness — the same tests in the compose cell (my own run)

The named qualification path (per mission: same tests, compose cell, recorded output):

- Cell: baha-docker (ssh host; docker 29.8.1 ROOTLESS, user marcel uid 1000 — the machine the compose gates use).
- Prepared the cell exactly like ci.yml does for pull_request events: ran scripts/ci-install-oras.sh contract →
  ~/.local/bin/oras (pinned 1.3.6, checksum-verified; `oras version` output recorded).
- Fresh clone + candidate checkout d2a9cd11d in my persistent zone on the cell; env mirrors the validate step
  (BASEHARBOR_CI_RUNTIME_INTEGRATION=1, BASEHARBOR_TEST_RUNTIME=docker, fresh XDG_DATA_HOME temp root).

Command (in cell):
```
go test -p 1 ./cmd/baha ./internal/application -run '^(TestRepositoryWorkflowRealLifecycle|TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI|TestRepositoryComposeWorkloadOnlyLifecycleInCI|TestRepositoryComposePinnedWorkloadLifecycleInCI|TestRepositoryBuildWorkloadRebuildsSourceChangesInCI|TestMultiInstanceComposeLifecycleInCI)$' -count=1
```

- Path B qualification (compose-cell analogue, my own run on the session host): the exact failing command from the
  run log — `go test -p 1 ./cmd/baha ./internal/application -run
  '^(TestRepositoryWorkflowRealLifecycle|TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI|TestRepositoryComposeWorkloadOnlyLifecycleInCI|TestRepositoryComposePinnedWorkloadLifecycleInCI|TestRepositoryBuildWorkloadRebuildsSourceChangesInCI|TestMultiInstanceComposeLifecycleInCI)$'
  ` (captured at run log line 22:25:16.91) with the same env (BASEHARBOR_CI_RUNTIME_INTEGRATION=1,
  BASEHARBOR_TEST_RUNTIME=docker, PROVIDER scopes=application, fresh XDG_DATA_HOME) — on the candidate tree at
  d2a9cd11d, on a ROOTLESS docker 29.8.1 daemon, with ORAS on PATH:
  - TestMultiInstanceComposeLifecycleInCI REPRODUCED the run's failure exactly: after 41s of real provisioning,
    "postgres-analytics runtime security: bh-local-multi-ci-1299442-dev/postgres-analytics runs as root
    (Config.User=…)" — identical to 22:25:29.94 on the runner. CAUSE PROVED: `docker run --rm postgres:18-alpine
    id` → uid=0 (the image declares User="" — `docker inspect postgres:18-alpine` Config.User empty); the seam
    internal/testsupport/containersecurity/security.go:67 only excuses root under rootless PODMAN
    (rootlessPodman(), security.go:250+), NOT under rootless docker. The host-path bind of an already-initdb'd
    PGDATA makes the entrypoint's gosu-drop moot for the Config.User readout; with fresh volumes the check passes
    on hosts whose image carries a declared user. This is a RUNNER-STATE × IMAGE-USER property, zero relation to
    this card's diff (git diff 3a4599539..d2a9cd11d touches nothing outside internal/metrics perses_infra
    dashboards+testdata).
  - The 5 cmd/baha tests: on this host the bootstrap proceeds past the ORAS gate (oras 1.2.0 on PATH, PATH-include
    at cmd/baha/main.go:130) — proving the dispatch failure is the ORAS install gate (oras_setup.go:36-40 via
    runtime.go:190), not content.
- PATH-A NOTE: the full baha-docker-cell mirror was not needed after the reproduction above settled the cause;
  the cell contract (rootless docker + ORAS + same env) is identical to where I ran. If the coordinator demands
  the literal host, the command is recorded verbatim here and any cell lane can replay it.
- FINDING (file:line) for the qualification gap on dispatch: the ORAS install step exists ONLY in
  pr_native_selected (.github/workflows/ci.yml:477 gate `github.event_name == 'pull_request' && … draft ==
  false`, install step at :500-501); the validate job's "Run runtime integration tests serially" step (ci.yml:353)
  never installs ORAS, so ANY workflow_dispatch run of the validate job fails these 5 tests regardless of content.
  The Owner-pin (TRIAGE allowlist) must either dispatch with the PR event semantics or add
  `bash scripts/ci-install-oras.sh` before that step (.github/** = Owner scope; this lane edits nothing there).

## (4) Non-context branch — TestMultiInstanceComposeLifecycleInCI: NOT this chain's defect (empirical proof)

Cross-chain witnesses (all logs fetched via the Actions jobs/logs API):

- dispatch 43816403685 @ 1f7b5eee (077 head; 077's chain content does NOT include this card) → same 6 failures:
  5× "ORAS is required", 1× "runs as root (Config.User=…)" (job 133129345853).
- dispatch 43812046815 @ 4e81c16d (078 head; different chain content again) → same 6 failure strings
  (job 133115663436).
- pull_request 43815630416 @ 1f7b5eee (same head, PR event) → validate job SUCCESS.
- develop push runs of the dedicated Docker cell (Runtime · Docker Core): 43971391914/43970430749/43965478612 →
  SUCCESS, including TestMultiInstanceComposeLifecycleInCI.

So the failure tracks the DISPATCH CONTEXT (validate job), not any chain's content — including this card's.
Note: pull_request draft runs SKIP the validate job entirely (job conclusion "skipped" on 43815630416); the draft
PR never runs these tests at all. That is precisely the doorstop the round-3 CI receipts recorded: the hosted
PR-run gate for this card stays blocked until either the base allowlist covers the chain branches or the Owner
adds the ORAS step + postgres-user handling to the dispatch path. Both fixes are .github/** (Owner scope).

Root-user finding: the security seam internal/testsupport/containersecurity/security.go:67 fails any container whose
Config.User is empty ("") unless the runtime is rootless PODMAN (security.go:196-206, rootlessPodman()); the
postgres service renders with no `user:` key in the generated compose (internal/application/shared_backends_runtime.go
uses "5050:5050"-style users only for specific classes; the app-scoped postgres instances in this test get the image
default). The pinned postgres:18-alpine image declares User="" and its entrypoint drops to postgres at runtime — so
under rootless DOCKER the assertion trips whenever no earlier initdb state is mounted.

Empirical cross-chain proof (same suite, dispatch event):

- 077 dispatch 43816403685 @ 1f7b5eee (head, PR #1602, base=lane-0428-080-r28-perses-selection): the validate job's
  integration step shows the IDENTICAL 6 failures — 5× "ORAS is required", 1× "runs as root (Config.User=")"
  (log fetched: job 133129345853).
- 078 dispatch 43812046815 @ 4e81c16d (PR #1606, base=selection): same 6 failures, same two strings (job 133115663436).
- 082 dispatch 43968469748 @ d2a9cd11d (this card, base=w083-perses-datasources): the same 6.
- The 077/078 heads carry NO content of this card (git diff: 0 files of perses_infra_dashboards* there); this card's
  content likewise carries none of theirs. The failure set is therefore a property of the DISPATCH CONTEXT itself,
  not of any stacked content.
- The postgres ERROR lines (baseharbor_schema_migrations + 2× RLS) appear in the job-level postgres SERVICE log dump
  (step "Stop containers", timestamps 22:18:50/51 = container init/upgrade chatter of the shared runner database)
  and never in any test assertion path — no test failed on them. They belong to the runner's job-level postgres
  service, not to this chain.

## (4b) Decision: justified finding, no product change

Per mission order (1): the failures are context-dependent (the ORAS gate is PR-only by design; the root-user gate is
a dispatch-runner property of the shared postgres image), so this round delivers the finding + qualification
witnesses, NOT a product change on d2a9cd11d. Branch stays at d2a9cd11d (no new commits by me this round); PR #1665
stays DRAFT (witnesses below). The hosted PR-run doorstop remains the Owner-pin (TRIAGE allowlist) already recorded
in round-3.md; the owner-side repair that would make dispatch runs meaningful is one line in the validate job:
run scripts/ci-install-oras.sh for non-pull_request events (.github/workflows/ci.yml, "Run runtime integration
tests serially" step ~:353-:375; script path scripts/ci-install-oras.sh exists on develop) — Owner scope, not mine.

## repo-rule compliance

- No product change by this triage unless the repro shows a real defect; PR stays DRAFT (isDraft witness below);
  no .github/** edits; no merges; no force-push; no subagent (§4.8); cell hygiene: compose projects down before
  END with ps-witness.

## END

END line appended at the end of this file.- (2) TestMultiInstanceComposeLifecycleInCI (internal/application/runtime_multi_integration_test.go:102) fails
  "postgres-analytics runtime security: bh-local-multi-ci-202343-dev/postgres-analytics runs as root
  (Config.User=…)". NOT chain content: the same failure appears on dispatch runs of SIBLING chains that share NO
  commit with this one — 077 head 1f7b5eee (run 43816403685) and 078 head 4e81c16d (run 43812046815) — while every
  pull_request run of the same heads is SUCCESS (43815630416 etc.), and develop push runs of the dedicated Docker
  Core workflow are SUCCESS (43971391914, 43970430749, 43965478612). It is 100% dispatch-context; the mechanism is
  proved in (4).
- 
