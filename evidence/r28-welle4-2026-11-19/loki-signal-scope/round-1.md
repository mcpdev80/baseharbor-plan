# t-20261120-r28-provider-signal-id-scope-inconsistency (0428-167) — round-1

**Verdict: END_DONE as refutation.** The bug described in the mission does not exist in the base lane HEAD of 0428-168. No production change was made. A regression test locking the invariant is filed. Seat held pending the corrected helper from 0428-168.

## PLAN

1. Reality check: fetch develop and the base lane, read the four named provider files and the registry read path.
2. Reproduction before solution: verify whether two Loki-using applications writing to the same shared registry would collapse to one source (the claimed overlap).
3. Decide scope: the four providers are already consistent; Loki was scoping-aware from introduction (v0.4.19, commit 6f444b63), while only Keycloak received ID scoping in 0428-1707 (b7cbc00f) and therefore carries the legacy migration. Loki needs no migration.
4. Lock the invariant with a CI-run regression test at the registry layer that owns RegisterProviderSignals/List.
5. Verify the test passes, the whole observability/logs/traces/telemetry/identityprovider packages pass, and the blob-pruefung is clean (only the two test files).
6. STOP per owner-meldefrist (2026-11-08): 0428-168 is under REQUEST-CHANGES and its generic helper migration.go is changing; do not start the Loki call-site work that depends on the corrected helper.
7. Write evidence, clean working tree, post END_DONE.

## Reality witnesses

ls-remote (run 2026-11-20, from /home/marcel/dev/baseharbor-ecosystem/workers, origin = https://github.com/mcpdev80/baseharbor.git):

```
$ git ls-remote origin refs/heads/develop
f61ef0f4991cae88727c02b731d862bf395d8984	refs/heads/develop
$ git ls-remote origin refs/heads/lane-0428-168-signal-id-migration
0d1568ec4dc8c92c4d2721fb374ecd9d086d0d4c	refs/heads/lane-0428-168-signal-id-migration
```

Base lane head moved during this shift: the mission named `983152b9763b521222fb766df71209626e82362e`; the current remote head is `0d1568ec4dc8c92c4d2721fb374ecd9d086d0d4c` (the 0428-168 corrections are landing). `git log -1 --format=%H %P` of the base lane:

```
0d1568ec4dc8c92c4d2721fb374ecd9d086d0d4c 514691368474075eac0e97b5e2e7c5b6c7930fa4
```

## What the evidence shows (refutation)

The mission claims four providers build their Perses signal identity but two carry the project and two do not: `keycloak:`+project, `tempo:`+project, `opentelemetry-collector:`+project present, and a literal `loki-metrics` without project at internal/logs/realization.go:233.

Measured against the base lane HEAD (983152b9), all four are scoping-aware:

- internal/identityprovider/keycloak_realization.go:135 `registrationID := "keycloak:" + r.files.Project`
- internal/traces/tempo.go:404 `ID: "tempo:" + p.Project`
- internal/telemetry/realization.go:178 `ObservationID: "opentelemetry-collector:" + files.Project`
- internal/logs/realization.go:238 `ID: "loki:" + placement.Project`

There is no project-less literal Loki ID anywhere in internal/. The only `loki-metrics` literals are the runtime-signal *name* inside `signals["loki-metrics"] = ...` (a map key, the Perses signal name in capability/reference.go:132) and the registration ID line — which already carries `+ placement.Project`.

Registry semantics confirm the overlap cannot happen with distinct scoping IDs: RegisterProviderSignals (internal/observability/registry.go, mutate) replaces by exact (ID, provider) pair; List filters on exact source.ID. Two scoping IDs => two distinct sources.

Root-cause for the divergence: Loki was scoping-aware from its introduction (v0.4.19, commit 6f444b63 "make shipped service/provider boundaries runtime-neutral"). Keycloak received ID scoping only in 0428-1707 (b7cbc00f), which is why Keycloak carries the legacy migration (migration.go ReconcileLegacySignals) and Loki does not. The base lane HEAD differs from origin/develop by exactly the completed Keycloak migration work (keycloak_legacy_migration_test.go, migration.go, read_signals_test_helper.go); the Loki registration path is byte-identical between base lane and develop.

## What I took from the 0428-168 verdict P3

P3 (from the 0428-168 REQUEST-CHANGES verdict) says the worker writes only the Loki call-site in internal/logs/realization.go:233 plus Loki tests, and that the call-site hangs off the helper form that 0428-168 r2 delivers. I have NOT written that call-site change, because the bug it would fix does not exist (refutation above) AND the helper migration.go is changing under me right now. Per the stop directive I will not start that work or rebase onto the moving base. Any re-evaluation of scope for my branch must wait until the corrected helper from 0428-168 is on a stable base.

## CI coverage for the filed test

My two new files are test-only and live in packages the CI unit shard enumerates:

- internal/observability/loki_signal_scope_regression_test.go -> internal/observability package
- internal/logs/loki_signal_scope_regression_test.go -> internal/logs package

scripts/pr-go-unit-shard.py (--mode packages) runs `go list ./...` and `go test -count=1 ./...` for every non-CLI package with no filter, so both packages are covered by the generic Go unit CI with no .github/** change required. The tests assert at the registry layer that owns RegisterProviderSignals/List and the private registerProviderSignals call site, so a real regression of the Loki ID is caught here.

## Verification run

```
$ go version
go1.26.8 linux/amd64   (go.mod toolchain go1.26.9)
$ go test -count=1 ./internal/observability/ ./internal/logs/ ./internal/traces/ ./internal/telemetry/ ./internal/identityprovider/
ok  internal/observability
ok  internal/logs
ok  internal/traces
ok  internal/telemetry
ok  internal/identityprovider
$ go build ./...          # exit 0
$ go test ./internal/observability/ -run 'Loki'   # both Loki tests PASS
$ git diff --name-only 983152b9763b -- internal/identityprovider internal/traces internal/telemetry internal/logs internal/observability
# empty: no production file touched by me
```

## repo-rule compliance

- Evidence written ONLY in baseharbor-plan (the planning repo at /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan), never in a product repo. No .evidence/ directory, no main-branch writes. origin/main fetched before write (4ca50e06).
- No .github/**, no scripts, no product production change authored by me.
- No subagents used. No VM/container/compose/network/volume started. Session-local runtime only.
- Branch provenance: no branch was cut; no PR was opened; nothing was pushed. All reads were via git ls-remote / a fresh clone under /tmp/opencode (x167-wt, base168). The workers/baseharbor quarantined checkout was never cited.
- Scope boundaries honored: no write to internal/runtime/project.go (0428-166), no merge, no rerun.

## cleanliness:

Started: a fresh read-only clone of the base lane at /tmp/opencode/base168 (git clone --branch lane-0428-168-signal-id-migration), a scratch clone at /tmp/opencode/x167-wt, and a bookkeeping clone at /tmp/opencode/x167-wt. No containers, no compose projects, no networks, no volumes, no STATE directories persisted. Ambient-core images of foreign cards untouched. Working tree of base168 restored to base HEAD via `git checkout --` after the base lane advanced; only the two untracked test files remain. No ephemeral test artifacts left behind.
```
$ cd /tmp/opencode/base168 && git status --short
?? internal/logs/loki_signal_scope_regression_test.go
?? internal/observability/loki_signal_scope_regression_test.go
```

## END

END_DONE. Nothing pushed (no branch cut, no PR). PR status: n/a. At their current seat the 0428-167 lane has authored a refutation (the Loki scoping bug does not exist in base lane HEAD) and a CI-locked regression test; the Loki call-site migration that the original task envisioned is deferred until the corrected migration helper from 0428-168 lands on a stable base. Next round of 0428-167 gets a fresh lane on the freed seat and must re-check scope against the corrected helper before deciding whether the Loki call-site change is still needed.
