# 0428-125 · Runtime-metrics target-file key binds the environment (fix-1)

Card: t-20261119-hunt-metrics-target-env-key-asymmetry (hunt-918 Befund 7, MEDIUM).
Akte source: evidence/r28-welle4-2026-11-19/hunt-metrics/befund-1.md, Befund 7.
Lane: mission-targetenvkey.md (opencode flash session e409b9b1-7003-41cd-a3ea-ea61f075f7a5).
Candidate: branch lane-0428-125-target-env-key, commit 4fcb2b35d1182e7b639a8dc18f5cccf33ea8564f, PR https://github.com/mcpdev80/baseharbor/pull/1694 (base develop).

## PLAN

1. done — Read mission, hunt akte Befund 7, task card and repo rules.
2. done — Claim card via scripts/plan.py, publish claim (baseharbor-plan commit c2028da4 on main).
3. done — Reality check: ls-remote develop = ec592fd3852328439ae9de8763c816ae9dd88dcc; branch cut from it (attestation below).
4. done — Locate key computation and group label (file:line below).
5. done — Red regression with two environments on one shared targets dir (fails at base, red witness below).
6. done — Fix: one documented key formula including environment at ONE place (file:line below); legacy keys not renamed silently (acceptance reasoned below).
7. done — No overlap with excluded paths 124/123/121/122/119r3 (verified against each sibling lane's write-set below).
8. done — Monotonous hop: build, vet, race test, internal/... full unit suite, source-readability audit; pushed coherent candidate.
9. in progress — Observe the exact-head CI run on 4fcb2b35d to terminal state (recorded below before END).
10. done — Evidence written and pushed to origin/main before END post.

## Base attestation (branch provenance is proof)

ls-remote witness, product repo mcpdev80/baseharbor, measured at work start (fresh clone zone /tmp/targetenvkey-wt-clone/src, worktree /var/tmp/mission-targetenvkey-wt/wt):

    ec592fd3852328439ae9de8763c816ae9dd88dcc	refs/heads/develop

Branch cut: `git checkout -b lane-0428-125-target-env-key ec592fd3852328439ae9de8763c816ae9dd88dcc`.
Ancestor test: `git merge-base --is-ancestor ec592fd3852328439ae9de8763c816ae9dd88dcc HEAD` → OK (exit 0).
Log-line check: `git log --oneline ec592fd38..4fcb2b35d` lists exactly one commit —

    4fcb2b35 fix(0428-125): bind environment into the runtime-metrics target file key and resource id

— my own. No foreign candidate is carried on top. Planning-repo toplevel witness (`git rev-parse --show-toplevel` in /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (the correct planning repo, not the workers/ bookkeeping directory).

## Findings (file:line at base ec592fd38)

- Key computation, environment omitted: `internal/metrics/runtime_source.go:206-209` — `runtimeTargetFileName` = `sha256(application, callerService, resourceName)`, consumed by `targetPath` at `:202-204`; same tuple-only sum also produced the resource id at `:211-214`.
- Group label, environment present: `internal/metrics/runtime_source.go:134-146` — writeTarget stores `baseharbor_environment: e.environment`.
- Read-time assertion: `internal/metrics/runtime_source.go:185-192` — readTarget compares `baseharbor_environment` and fails hard with `runtime metrics target ownership mismatch` (Execute propagates it as a terminal error at `:60`).
- Shared-directory reachability: broker mounts one global targets dir `/var/lib/baseharbor/runtime-metrics` (`internal/runtimebroker/compose_render.go:202,243`), while per-deployment volumes are named per application+environment (`internal/application/metrics_policy.go:112-119`, used at `internal/metrics/prometheus_shared.go:236`), so the collision lives on the broker path.

## Fix

Single key formula, defined at exactly one place: `runtimeTargetFileName` in `internal/metrics/runtime_source.go` (fix commit), now `sha256(environment, application, callerService, resourceName)` with a doc comment stating the rule. `runtimeMetricsResourceID` no longer carries its own sum — the id is derived from the file key at that same place (strip `runtime-`/`.json` prefix/suffix, prefix `res-metrics-`), so file key and resource id can never diverge again. Both are executor methods; the environment is the executor's own field, which is exactly the value writeTarget stamps and readTarget asserts.

`runtime.delete` moves from deleting the environment-less legacy path (which never matched a file written under the new key) to deleting the caller's own environment file; the dev delete no longer can remove, and no longer silently leaves ambiguous, another environment's file.

## Bestand: migration vs acceptance (reasoned, not silent)

Decision: explicit acceptance of orphaned legacy files; NO in-product rename migration. Reasons:

- Legacy environment-less files are already unreachable for reads at the fix base: any file whose label carries an environment passes the readTarget identity check only when the label matches the executor, and the collision scenario in Befund 7 means such files are contentwise identical (port/path) — a rename cannot tell which environment owned a colliding file, so a faithful migration is information-theoretically impossible on the shared broker directory.
- Nothing outside this package references the key or id format: the only consumers of the runtime-metrics file name are `targetPath` call sites in `runtime_source.go` itself; the Prometheus file-sd glob (`prometheus_render.go:196-204`, `/etc/prometheus/runtime-targets/%d/*.json`) is pattern-based, and the `runtime-sources.json` snapshot (`internal/metrics/runtime_source_snapshot.go:19-24`) stores `observability.MetricsSource` metadata, not target-file paths or resource ids (verified by grep at base: `res-metrics-` and `"runtime-" +` occur only in `internal/metrics/runtime_source.go`; sibling `internal/runtimebroker/*` "runtime-*" strings are compose service/volume/secret names, not target files).
- Consequence is fail-closed and self-healing: after upgrade, an existing source's `runtime.get` reports not-found/mismatch exactly as Befund 7 already did under contention, and the next `runtime.create` in that deployment rewrites the target under the new environment-bound key. Stale legacy files keep their old labels; Prometheus may scrape a stale-but-valid target until a create or delete replaces it, which is the pre-existing lifecycle, not a new failure mode.
- If the release note wants a cleanup, a follow-up could delete files that fail the label check on create; deliberately out of this card's write-set.

The key format change is therefore a documented breaking change for runtime-metrics state on shared broker volumes (recorded here and in the PR); no silent rename happens.

## Red regression at base, green at candidate

Test: `internal/metrics/runtime_source_envkey_0428_125_test.go` — `TestRuntimeSourceSeparatesTargetFilesPerEnvironment`. Two executors (`dev`, `prod`) on ONE shared temp targets dir; the same (application, callerService, resourceName) tuple; asserts distinct file keys, distinct resource ids, two entries on disk, dev `runtime.get` still succeeds after the unrelated prod create (the Befund 7 failure), and dev `runtime.delete` removes only the dev file.

Red witness at base (before fix, same test file):

    --- FAIL: TestRuntimeSourceSeparatesTargetFilesPerEnvironment (0.00s)
        runtime_source_envkey_0428_125_test.go:53: environment key asymmetry: dev and prod share target file "/tmp/.../runtime-1c7ae398633cdd94eb20deb3.json"
    FAIL	github.com/mcpdev80/baseharbor/internal/metrics	0.005s

Green at candidate: `--- PASS: TestRuntimeSourceSeparatesTargetFilesPerEnvironment` (see run block).

## Checks (local monotonous hop, candidate 4fcb2b35d)

Toolchain: go1.26.8 linux/amd64 (go.mod declares go 1.25.0 / toolchain go1.26.9; local toolchain 1.26.8 is what this host has, identical to prior lanes' practice this shift — noted as STATE, not silenced).

- `go build ./internal/metrics/` → ok; `go vet ./internal/metrics/` → clean.
- `go test ./internal/metrics/ -run TestRuntimeSource -count=1 -race` → ok 1.020s (all three runtime-source tests green).
- `go test ./internal/metrics/ -count=1` → ok 0.173s.
- `go test ./internal/runtimeoperation/ ./internal/runtimeresourceapi/ ./internal/runtimebroker/ -count=1` → all ok.
- `go test ./internal/controlplaneruntime/ -count=1` → 1 FAIL: `TestRunStartsTLSHealthReadinessAndProtectedAPI` — `server_integration_test.go:33` is a `t.Fatal("testumgebung nicht hergestellt: BASEHARBOR_TEST_DATABASE_URL fehlt")`: the test hard-fails without a live Postgres DSN. Environmental prerequisite of the host, reproduces bit-identically at base ec592fd38 (verified by stashing my diff and re-running); NOT caused by this change. This is also a pre-existing fail-closed pattern finding (it fails instead of skipping without its service) — out of this card's write-set, reported here only. CI provides the DB in its service containers.
- `go test ./internal/...` (full unit sweep at candidate, GOCACHE/GOTMPDIR under /var/tmp/mission-targetenvkey-wt): every package ok except `internal/controlplaneruntime`, which fails ONLY on the pre-existing `BASEHARBOR_TEST_DATABASE_URL fehlt` host-prerequisite pattern above; CI executes those tests with its isolated PostgreSQL and they pass (run block).
- `bash scripts/source-readability-audit.sh` → PASS (size/span/ratchet).

## CI integration of the new test

The test is a plain in-package Go unit test auto-discovered by `go test ./internal/metrics/`; it needs no env or service containers. Selection is by the `go-unit-tests` group (`scripts/pr-gate-plan.py:1580`, command `go test ./... -count=1`) of workflow `CI · Source & Quality` (`pr-required-checks`), which triggered automatically on this PR against develop and reports the `PR · Go unit · *` job family (run witness below). The run's `PR · Native gate plan` job (gate-selection plan) completed SUCCESS for this head SHA, i.e. the selector accepted the candidate's paths. No `.github/**` change was needed; nothing to request from the Owner. Test binding: normal (auto-discovered) — no `REQUIRED_CLIENT_TESTS` or selector-file entry exists for `internal/metrics` beyond the package sweep, and none was added. The selector itself cannot be re-run off-runner: `python3 scripts/pr-gate-plan.py` refuses without `GITHUB_REPOSITORY`/`GITHUB_BASE_REF` ("refusing to qualify without authenticated runner context") — documented, not worked around.

## Hosted runs (Eigenes-Run-Pflicht)

Run observed by this session to terminal state:
- Workflow: `CI · Source & Quality` (`.github/workflows/ci.yml`, `pr-required-checks`), triggered automatically by PR #1694 against develop. Run ID `44457185039` (https://github.com/mcpdev80/baseharbor/actions/runs/44457185039), headSha `4fcb2b35d1182e7b639a8dc18f5cccf33ea8564f` (exact candidate).
- Terminal: `status=completed conclusion=success`. 14 jobs success, 19 skipped by the path selector (release/HA/native/draft jobs — not required for an `internal/metrics` change), 0 failing. Required selection for this change: go-vet, go-build, Focused Python, Native gate plan, Trusted Plan, Source format, Workflow policy and the full `PR · Go unit` family — all SUCCESS.
- New-test witness inside the run (job `PR · Go unit · packages`, step "Execute selected Go tests with isolated PostgreSQL"): `ok  	github.com/mcpdev80/baseharbor/internal/metrics	0.391s` — the package containing `TestRuntimeSourceSeparatesTargetFilesPerEnvironment` executed green on GitHub-hosted runners.
- No rerun, no workflow_dispatch, no `.github/**` touch was needed or made.

Local full `go test ./internal/...` sweep at candidate: only `internal/controlplaneruntime` DB-gated tests fail on the `BASEHARBOR_TEST_DATABASE_URL fehlt` pre-existing host-prerequisite pattern (identical at base); CI runs them with the isolated PostgreSQL service and they pass there.

## Scope discipline (excluded paths)

`git diff --name-only ec592fd38..4fcb2b35d` = only `internal/metrics/runtime_source.go` and the new test file. Verified against the sibling lanes' remote diffs at base: 0428-123 (lane-0428-123-regvisibility) touches `prometheus_verify.go`, `observability/registry.go`, new test; 0428-122 (lane-0428-appclass-writer) touches `internal/logs/*`, `application/runtime_observability.go`, `observability/registry.go`; the env-filter lane (d9d70a98) touches `internal/logs/*`, `observability/registry.go`, `prometheus.go` et al. No file overlap with any of them; my change set is disjoint. 0428-124's composition-blindness path is untouched (no change in realization/composition code).

## repo-rule compliance

- One PR for one card; single candidate branch; no second branch invented (remote ls-remote shows lane-0428-125-target-env-key absent before push, created once at 4fcb2b35d).
- Claim published via plan.py before any product edit (c2028da4).
- No `.github/**` edits, no merges, no force-push, no subagents, no containers or compose projects started on this host (all tests are pure-Go unit tests on temp dirs; VM hosts not needed and not touched).
- Scratch confined to /var/tmp/mission-targetenvkey-wt and /tmp/targetenvkey-wt-clone; no new paths in the ecosystem root.
- Language: identifiers and comments in English; the card's German terms (environment, targets dir) kept as system names.

## Deviations and notes

- The session named "0428-125-" in the pool IS this session (agent list shows self:true); no duplicate lane exists or was started.
- Two runtimeSource helpers now take the executor receiver; call-site churn is confined to runtime_source.go (3 call sites) — intentional to keep ONE place for the formula per the card's acceptance.
- Sibling cards this shift (all branch from the same develop head ec592fd38): #1690 (0428-119), #1691 (0428-121), #1692 (0428-122), #1693 (0428-123). Their diffs (gh pr diff --name-only at 2026-11-19) touch `internal/metrics/prometheus.go`, `prometheus_verify.go`, `realization.go` and new test files — never `runtime_source.go`. My write-set (`runtime_source.go` + one new `runtime_source_*_test.go`) is file-disjoint from all of them; fan-out merge order is a coordinator decision.
- While the full local `./internal/...` sweep ran, unrelated sibling-lane test processes on this host created scratch dirs (`internal/application/prune-*`, `trace-*` runtime.env files) inside my worktree. They contained only generated per-test state; I removed them from my worktree so my candidate stayed clean. Flagged for the coordinator because those lanes' hygiene (scratch inside a product worktree, mission rule: tmp /var/tmp) may need attention.
- The mission's suggested name for the evidence akte is `fix-1.md` under `evidence/r28-welle4-2026-11-19/target-env-key/` — used exactly.

END_DONE mission-targetenvkey.md: 0428-125 fix published — candidate `4fcb2b35d1182e7b639a8dc18f5cccf33ea8564f` on `lane-0428-125-target-env-key`, PR #1694, red→green regression `TestRuntimeSourceSeparatesTargetFilesPerEnvironment`, exact-head CI run 44457185039 terminal SUCCESS.

## Evidence-on-origin/main witness

Run as second-to-last action, before the END post:
<!-- EVIDENCE-PUSH-BLOCK -->
