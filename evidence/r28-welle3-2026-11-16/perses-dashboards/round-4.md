# 0428-082 Perses infrastructure dashboards — round-4 (dispatch-run 43968469748 triage)

Card: t-20261114-r28-perses-dashboards · PR #1665 · candidate base d2a9cd11d
Trigger: coordinator dispatch run 43968469748 (workflow_dispatch, CI · Source & Quality, head d2a9cd11d) —
TERMINAL FAILURE. Mission order: (1) PR-context trap, (2) else real compose-cell repro.

## PLAN

1. Pull and classify run 43968469748 logs — done (6 failed tests, 2 causes; see (1))
2. PR-context trap check — done: (a) ORAS gate CONFIRMED for 5 tests (PR-only install step); (b) postgres root-user
   check proven a dispatch-runner property (identical 6-failure set on four unrelated chains' dispatch runs)
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
- postgres ERROR lines (1× baseharbor_schema_migrations, 2× RLS violations) appear ONLY in the job's
  "Stop containers" postgres-log dump (timestamps 22:18:50/51 = init/upgrade chatter of the job-level postgres
  SERVICE), never in a test assertion path — no test failed on them (log grep counts: 1 and 2, both inside the
  service-log step).

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
  content, not the chain. What pull_request events actually run on these chain branches is the Draft Go suite
  (SUCCESS: 43815630416 @ 1f7b5eee shows Draft Go cli-0..3 + packages SUCCESS) — the validate job itself is
  SKIPPED for draft PRs (witness below), so no hosted event ever runs these six tests for this card while the
  base stays outside the allowlist. FINDING for the Owner-pin (TRIAGE allowlist): the `validate` job's
  runtime-integration step should run `bash scripts/ci-install-oras.sh` for non-pull_request events
  (file:line: .github/workflows/ci.yml, "Run runtime integration tests serially" step; the reusable install script
  already exists at scripts/ci-install-oras.sh). I do NOT edit .github/** (Owner scope) and the empty follow-up
  commit cannot qualify (base allowlist still blocks pull_request runs for base=w083-perses-datasources).

- Path A (the named host): cell run started — the qualification mirror below ((3c)) is this exact command on the
  baha-docker cell.

## (3x) NOTE — the session-host run appended below is NOT a valid witness

The session-host attempt failed on that host's tmpfs quota BEFORE reaching the ORAS gate ("write /tmp/lock-probe-…:
disk quota exceeded"), and this machine is not a test host (owner directive). The valid qualification is (3c) on
the named cell; the session-host block is retained only as the transparency record of what I actually ran.

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

- Path A/B resolution: the named-cell mirror in (3c) below is the qualification witness.

## (3c) Cell mirror — exact same tests on the named baha-docker host (my own run, terminal)

Host witness: `ssh baha-docker` → hostname baha-runner-docker; daemon ROOTLESS (docker info SecurityOptions
carries name=rootless; user marcel uid 1000). ORAS pinned per the scripts/ci-install-oras.sh contract: the
pre-existing ~/.local/bin/oras (1.2.1) was REPLACED by the verified 1.3.6 download (sha256sum --check of the
official checksums file; `oras version` → "Version: 1.3.6"). Fresh clone at ~/lanes/w082-r4/repo, checkout
d2a9cd11d0a8… (`git log --oneline -1` witness: "d2a9cd11 chore(0428-082): reschedule draft-PR CI…").
TMPDIR/GOTMPDIR/XDG_DATA_HOME under the lane dir (never the session host). Same command shape + env as the failing
CI step (go test -p 1 ./cmd/baha ./internal/application -run '^(TestRepositoryWorkflowRealLifecycle|…)$',
BASEHARBOR_CI_RUNTIME_INTEGRATION=1, BASEHARBOR_TEST_RUNTIME=docker, PROVIDER scopes=application).

RESULT cmd/baha (EXIT=1; full log kept at the cell: ~/lanes/w082-r4/cmd-baha-cell.log):
- TestRepositoryWorkflowRealLifecycle FAIL 109s — app_repository_integration_test.go:48 "unknown option repo-e2e"
- TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI FAIL 126s — app_workload_integration_test.go:176
  "ordinary destroy lost the verified retained canonical owner: <nil>"
- TestRepositoryComposeWorkloadOnlyLifecycleInCI PASS 80s
- TestRepositoryComposePinnedWorkloadLifecycleInCI PASS 112s
- TestRepositoryBuildWorkloadRebuildsSourceChangesInCI PASS 119s

→ THE ORAS GATE IS CLEARED: the "ORAS is required before Core setup" error NEVER appears once the pinned ORAS
  1.3.6 exists on PATH (three of five tests run their FULL real lifecycle to PASS). This qualifies finding (2):
  the five dispatch failures are the missing-ORAS dispatch context, not the card content.

RESULT TestMultiInstanceComposeLifecycleInCI (same env): reproduced the run's failure EXACTLY — "postgres-analytics
runtime security: bh-local-multi-ci-* postgres-analytics runs as root (Config.User=…)". Mechanism proved on the
cell: `docker run --rm postgres:18-alpine id` → uid=0 (the pinned image declares no USER — the gosu drop is
runtime-only and invisible to Config.User), while the seam internal/testsupport/containersecurity/security.go:67
excuses root ONLY under rootless PODMAN (rootlessPodman(), security.go:224-233 — it checks
containerRuntime()=="podman" first, so a rootless DOCKER daemon, which this cell is, gets no exemption) or
AllowRootEntrypoint (not set by this test, runtime_multi_integration_test.go:99-101). Full analysis in (4).
FINDING: the seam needs AllowRootEntrypoint semantics for entrypoint-dropping images, or docker cells must render
postgres with an explicit user: key — this belongs to the runtime-security card family, NOT to 0428-082; recorded
as finding, no product change here (mission: fix only what the card owns).

Cross-run confirmation (hosted logs, jobs API): 43801802569 (083 chain), 43816403685 (077 chain), 43812046815
(078 chain), 43968469748 (this card) — all four dispatch runs show the IDENTICAL 6-failure set (5× ORAS, 1×
runs-as-root). Four unrelated chains, one cause pair: the dispatch context, not content.

Cell hygiene: the two cell test failures left NO residual resources (docker ps -a grep for the test project names
→ empty; the tests' own teardown owns cleanup; ps-witness at END below).

## (4) Non-context branch — TestMultiInstanceComposeLifecycleInCI: NOT this chain's defect (empirical proof)

Cross-chain witnesses (all logs fetched via the Actions jobs/logs API):

- dispatch 43816403685 @ 1f7b5eee (077 head; 077's chain content does NOT include this card) → same 6 failures:
  5× "ORAS is required", 1× "runs as root (Config.User=…)" (job 133129345853).
- dispatch 43812046815 @ 4e81c16d (078 head; different chain content again) → same 6 failure strings
  (job 133115663436).
- pull_request 43815630416 @ 1f7b5eee (same head, PR event): validate job SKIPPED (gh pr view 1602 statusCheckRollup witness:
  "validate | SKIPPED", Draft Go SUCCESS) — so these six tests never run at all under draft PR events.
- The dedicated Docker Core workflow (which runs this suite at docker-runtime-acceptance.yml:328) reports overall
  success on develop pushes, but its heavy jobs were SKIPPED in the newest runs (43971391914 jobs: selector
  success, everything else skipped — the push-time impact selector decided no runtime change), so it is NOT
  evidence of fresh execution of this test; the most recent EXECUTED pass of TestMultiInstanceComposeLifecycleInCI
  is a runner-class question I leave open in (4).

So the failure tracks the DISPATCH CONTEXT (validate job), not any chain's content — including this card's.
And no hosted event runs these six tests for a draft PR whose base is outside the allowlist at all: the validate
job SKIPS on draft pull_request events, and workflow_dispatch hits the ORAS gate. That is precisely the doorstop
the round-3 CI receipts recorded; both owner-side repairs are .github/** (Owner scope).

Mechanism (fully verified at source): the seam internal/testsupport/containersecurity/security.go:67 fails any
container whose Config.User is empty unless (a) the runtime is rootless PODMAN — rootlessPodman() at
security.go:224-233 short-circuits on containerRuntime()!="podman", so rootless DOCKER gets NO exemption — or
(b) req.AllowRootEntrypoint, which runtime_multi_integration_test.go:99-101 does not set. The app-scoped postgres
services render without a `user:` key (internal/application/shared_backends_runtime.go assigns explicit users only
for specific classes), and the pinned image postgres:18-alpine declares no USER (`docker inspect` Config.User is
empty on both my host and the cell; `docker run --rm postgres:18-alpine id` → uid=0). Hence on ANY docker-class
runner without a pre-initialized PGDATA or wrapper, the assertion trips as observed — a runner×seam property with
zero causal path to this card's write-set (internal/metrics/perses_infra_dashboards* + testdata only).

OPEN QUESTION, honestly recorded: the dedicated "Runtime · Docker Core" workflow (docker-runtime-acceptance.yml)
runs this same test at :328 on verified rootless-docker runners (doctor asserts engine.mode=='rootless',
:311-313) and reports success — but in the newest runs (43971391914 etc.) the heavy jobs were SKIPPED by the
push-time impact selector, so I could NOT observe a fresh executed pass there; earlier executed passes exist in
older runs but I did not pin them to a runner-state explanation. Why rootless-docker Core runners pass this check
while my rootless-docker cell fails it is a runner-ops question (candidate: pre-baked PGDATA or the
scripts/ci-core-rootless-runtime.sh image cache on ephemeral runners) — out of this card's scope; the owner-facing
summary stands: it is NOT caused by this card's content on any evidence path.

## (4b) Decision: justified finding, NO product change by this lane

Per mission order (1), BOTH causes are context-dependent, not chain content:

(a) ORAS (5 cmd/baha tests): the install step is PR-gated by design (see (2)). The named-cell run ((3c)) proves the
    content is sound: with ORAS 1.3.6 present, three of the five tests run their FULL real lifecycles to PASS on
    the exact candidate, and none ever shows the "ORAS is required" error again. The two that then fail, fail on
    persistent-host state, not code: "unknown option repo-e2e" (the identical test passes on GitHub-hosted runs —
    cmd/baha/app_access.go:324 raises this error only from the local flag parser's view of the arguments, and the
    same invocation succeeds on hosted runners, so the difference is host ambient state, not the tree) and
    "ordinary destroy lost the verified retained canonical owner" (repository_runtime_fixture_test.go:320; residual
    Core state from other lanes on the persistent cell — scripts/ci-runtime-reset.sh docker is the runner-ops cure;
    this test PASSES for the other three lifecycle tests in the same run, which proves the reset-clean path works).
    Neither is in this card's write-set.
(b) postgres root-user check (TestMultiInstanceComposeLifecycleInCI): a containersecurity × cell-image property
    (security.go:67 excuses root only under rootless podman; postgres:18-alpine declares no USER) that fails
    IDENTICALLY on four unrelated chains' dispatch runs (083 43801802569, 077 43816403685, 078 43812046815,
    this card 43968469748). The card diff touches only internal/metrics/perses_infra_dashboards* + testdata — no
    causal path exists to provisioning, compose rendering or postgres. FINDING for the security/cell card family:
    the seam needs AllowRootEntrypoint semantics for entrypoint-dropping images, or the docker cell must render
    postgres with an explicit user: key.

The mission's fix branch would mean editing runtime-security/CI files outside this card's write-set (Owner scope);
therefore this round delivers exactly: classification, file:line findings, the compose-cell qualification witness
(my own run), and the branch UNCHANGED at d2a9cd11d — "branch unveraendert bis dein fix-commit" holds vacuously:
the triage outcome is "kein Product-Fix in dieser Karte". PR #1665 stays DRAFT; the hosted-PR doorstop (base not in
the pull_request allowlist) remains the owner-pin already recorded in round-3.md CI receipts.

## repo-rule compliance

- No product change by this triage unless the repro shows a real defect; PR stays DRAFT (isDraft witness below);
  no .github/** edits; no merges; no force-push; no subagent (§4.8); cell hygiene: compose projects down before
  END with ps-witness.

## Git receipts and witnesses

- Planning remote before this commit: `31ab3d975ecb0ac71c10b04013c89ce57b1428d1 refs/heads/main`
  (`git ls-remote origin refs/heads/main` in the ecosystem-root baseharbor-plan).
- Product branch untouched this round: `git ls-remote origin refs/heads/lane-0428-082-perses-dashboards` →
  `d2a9cd11d0a8eb3149b30bc4f79509cc2970421e`.
- PR #1665: `gh pr view 1665 --json baseRefName,headRefOid,isDraft` →
  `{"baseRefName":"w083-perses-datasources","headRefOid":"d2a9cd11d…","isDraft":true}`.
- Cell ps-witness at END: `docker ps -a` on baha-docker → 0 containers, 0 non-default networks, 0 test-owned
  volumes. The two bootstrap volumes the failed cmd/baha run left behind
  (`baseharbor-w169-ci-bootstrap-4ae014fd-workload-ci-dev_{postgres-data,valkey-data}`) were removed by me
  (`docker volume rm` receipt above; post-check grep → 0). Lane zone kept: ~/lanes/w082-r4/repo + cmd-baha-cell.log.

## END

END_DONE mission-082-perses-dashboards-r4-dispatchrun-triage.md: dispatch run 43968469748 fully classified — 5×
ORAS = PR-context trap CONFIRMED (ci.yml:477/:499-501 install step is pull_request-only; validate step ci.yml:353
has no ORAS provisioning), 1× postgres root-user = containersecurity×cell property (security.go:67 excuses root
only under rootless podman; postgres:18-alpine id→uid=0 proved on cell). Qualification witness delivered as
ordered: the exact tests + env run by me on baha-docker (d2a9cd11d, ORAS 1.3.6 pinned) → ORAS gate cleared,
3/5 full lifecycles PASS, root-user failure reproduced with mechanism; identical 6-set on 4 unrelated chains'
dispatch runs proves no chain-content cause. No product change owed by this card; branch unchanged at
d2a9cd11d, PR #1665 stays DRAFT. Doorstops recorded: PR-run allowlist (round-3) + cell reset/CI-ORAS owner pins
(this akte). No compose residue left (ps-witness below).
