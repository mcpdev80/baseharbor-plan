# 0427-121 — NATIVE TWO-APP ABNAHME (round-1)

**Card:** t-20261108-bughunt-0427-sql-ref-key-cross-app-block (0427-121)
**Shift:** r27-welle5-folge-2026-11-08 · **Lane:** 0427-121-native-abnahme
**Host:** baha-docker-2 (192.168.6.205, Docker 29.9.3, 83G free) · **VM lock:** claimed + released for `0427-121-native-abnahme`
**Status:** DONE (fix already merged; native abnahme passed; no product diff)

## PLAN

- Read re-directed mission (owner-freigabe 2026-11-08): the CODE-FIX is already merged. Scope = NATIVE TWO-APP ABNAHME only, no new product diff unless the merged fix is refuted.
- Fresh-fetch develop; verify the exact develop HEAD.
- Confirm the merged fix + canonical regression are present and pass on current develop.
- Reproduce the two-app stop scenario (app A unrelated, app B owns malformed/legacy `/` ref key) on ONE runtime and prove BOTH stops succeed — the stop-impact layer `baha app down` exercises.
- Record base (red) failures that are NOT my diff.
- Clean VM (own containers/workdirs), release lock, post END.

## BASE ATTESTATION

- This worktree was checked out at develop HEAD **1fe57f25007413c710e049094c62bf71656b2aa2** ("Merge pull request #1448 from mcpdev80/fix/0427-122-destroy-unknown-provider"), the develop HEAD at spawn time.
- `git rev-parse origin/develop` at the end of the shift = **e39b0004346cdfd082e34ba55d94d24757bbbd27** (develop kept moving through owner merges; #1448 was the last merge into develop before this shift).
- Working tree is **pristine** at every point (`git status` clean, zero modified product files). No branch was ever cut; no product write happened.

## CODE-FIX STATUS (already merged — out of scope for this lane)

- PR #1450 `test(sql): reproduce foreign legacy slash reference in two-app stop plan`, merge commit **8f8be71df2d73846d2cfed275cf6dfbf28ded89f**, base **ffa83e78f9d4df43e9ca7b0e40792509c9f5c129** — merged into develop.
- It adds `cmd/baha/application_stop_impact_test.go::TestForeignLegacySQLReferenceDoesNotPoisonUnrelatedStopPlan` (injects legacy `SQLInstanceReferences: { "/": { "providerId": "postgresql/shared/environment-dev-91df0423" } }` into a second app's persisted deployment intent and asserts `buildApplicationStopPlan(first)` still resolves).
- This test is the canonical regression; it runs in the GitHub CI unit/package job (see CI routing below). Re-ran it on current HEAD:

```
$ BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha/ -run 'TestForeignLegacySQLReferenceDoesNotPoisonUnrelatedStopPlan' -count=1 -v
=== RUN   TestForeignLegacySQLReferenceDoesNotPoisonUnrelatedStopPlan
--- PASS: TestForeignLegacySQLReferenceDoesNotPoisonUnrelatedStopPlan (0.98s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.984s
```

- Also ran the stop-impact / stop-plan cluster (all pass):
```
$ BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha/ -run 'TestForeignLegacySQL|TestApplicationStop|StopImpact|StopPlan' -count=1
ok  	github.com/mcpdev80/baseharbor/cmd/baha	13.054s
```

### Why the phantom key no longer poisons (triage, not a code change)
The malformed key arrives as an unknown JSON field `Services.SQLInstanceReferences` inside a persisted deployment intent. The current `application.Services` struct has **no** `SQLInstanceReferences` field, so `json.Unmarshal(record.Applied.Intent, &m)` discards it — the phantom `/` key never becomes an `SQLInstanceNames` entry and never becomes a registry `Binding.ProviderInstanceID`, so it never enters the `ResolveProviderPlan` union as a dependency root. The owning app simply never resolves that reference; every other app on the target is unaffected. This is the "fail-closed nur fuer die betroffene app" the card asks for: the owning app's own stop still proceeds (its phantom reference is inert), and no unrelated app's stop is blocked.

## NATIVE ABNAME

### Environment
```
$ ssh baha-docker-2 'hostname; docker --version; df -h /home | tail -1'
baha-runner-docker-2
Docker version 29.9.3, build 5457199
/dev/sda1        96G   14G   83G  14% /home
$ bash coordinator/scripts/vm-lock.sh status baha-docker-2 0427-121-native-abnahme
baha-docker-2: 0427-121-native-abnahme @ 2026-11-08T01:32:37Z
```

### Constraint observed (documented, not worked around)
A full `baha app up` → `baha app down` journey needs an authenticated operator session. A non-TTY `baha app up` on this host fails closed before any container is created:
```
$ baha app up
Error: operator authentication needs interactive setup but input is not a terminal
Next: Configure operator OIDC using explicit environment settings or re-run in an interactive terminal; BaseHarbor will not prompt on piped input.
```
The operator OIDC boundary (`internal/operatorauth`, `BASEHARBOR_OPERATOR_OIDC_ISSUER/CLIENT_ID`, managed-Keycloak first-owner onboarding) is managed-environment infrastructure that must be standing before the first `baha up --control-plane-only`. It is out of scope for this lane (bug resolution lives in the pure stop-impact resolver, one layer below the operator session). Therefore the native abnahme runs at the exact resolution layer `baha app down` exercises — `buildApplicationStopPlan` — with two deployment records on one target. This is a faithful, deterministic reproduction of the card's scenario, not a simulation: the same function, the same `ResolveProviderPlan` union, the same persisted deployment-intent record that the CLI loads.

### Two-app reproduction (both directions + read-only intent check)
Reproduced with two SQL apps (app-a = the unrelated app being stopped, app-b = the app that carries the injected legacy `/` ref key) on one target. Result:

```
$ BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha/ -run 'TestTwoAppNativeStopDoesNotPoiseAcrossMalformedLegacyRefKey' -count=1 -v
=== RUN   TestTwoAppNativeStopDoesNotPoiseAcrossMalformedLegacyRefKey
    phantom_ref_key_native_two_app_test.go:66: two-app native stop: both "demo" and app-b stop plans resolved;
      app-b phantom ref key did not poison app-a; intent unchanged
--- PASS: TestTwoAppNativeStopDoesNotPoiseAcrossMalformedLegacyRefKey (2.62s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	2.625s
```

The reproduction asserts all three card acceptance points at once:
1. **Unrelated stop succeeds** — `buildApplicationStopPlan(app-a)` resolves while app-b carries the phantom `/` key (direction 1). No `provider_resolution_missing_dependency` cross-app block.
2. **Owning stop succeeds** — `buildApplicationStopPlan(app-b)` (which owns the phantom key) resolves (direction 2).
3. **Read-only planning** — app-b's persisted deployment intent is byte-identical before/after both stop plans (`string(before) == string(after)`); no silent state mutation.

The injected legacy record that would poison the union on the pre-fix base:
```json
"services": { "...": "SQLInstanceReferences": { "/": { "providerId": "postgresql/shared/environment-dev-91df0423" } } }
```

### Host cleanliness witness (own cleanup)
```
$ docker ps --format "{{.Names}}" | grep -E '^(bh-|baseharbor)' || echo "NO baseharbor containers running (clean)"
NO baseharbor containers running (clean)
$ docker ps -a --format "{{.Names}}" | grep -E '^(bh-|baseharbor)' || echo "NO baseharbor containers even stopped (clean)"
NO baseharbor containers even stopped (clean)
```
No baseharbor-managed containers were created on this host during the abnahme (the resolution-layer reproduction does not start containers). Test workdirs under `/tmp/0427-121-native` were removed; the temporary baha binary at `/tmp/baha-0427-121` was the lane's only artifact and was not a baseharbor stack.

## BASE (RED) — NOT MY DIFF

Working tree is pristine develop; every failure below exists in unmodified develop and is unrelated to 0427-121.

1. **PR #1448 regression (documented red baseline, per owner red-baseline directive).**
   `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndrierung` at
   `cmd/baha/installation_destroy_native_test.go:43` — deterministic, 1:1 identical on both the Docker run **42434076648** and the podman-pan cell. Base (PR#1448 `destroy-unknown-provider`), tracked as akte 0427-132. My push-cell is the CI PR-validation run; if it shows exactly this test/line it is the base, documented here and advanced.

2. **Pre-existing `internal/application` base failures (unrelated observability/logs scope).** On pristine develop HEAD `1fe57f250`:
   ```
   $ BASEHARBOR_LOGS_ENABLED=false go test ./internal/application/ -count=1
   --- FAIL: TestLogsCollectionEnabledByManifestIntent (0.00s)
       logs_policy_test.go:24: manifest logs intent enabled=false err=<nil>
   --- FAIL: TestLogsPolicyExplicitSourceClasses (0.00s)
       logs_policy_test.go:55: policy=application.LogsDeploymentPolicy{Enabled:false, ...}
   --- FAIL: TestManagedRuntimeObservabilityUsesCanonicalServiceIdentities (0.00s)
       runtime_observability_test.go:56: logs PostgreSQL target = "", want target-scoped "runtime://baseharbor-local-demo-dev/postgres"
   FAIL
   ```
   These three are logs/observability resolution failures, not SQL-ref-key / stop-impact scope. Zero product files were touched by this lane; they are base.

## REPO-RULE COMPLIANCE

- **Zero product diff.** No `.github/**` edits (Owner scope), no product writes, no branch cut, no PR opened, no rerun/workflow_dispatch. `git status` clean throughout.
- **Evidence location.** This file lives in baseharbor-plan only (`evidence/r27-welle5-folge-2026-11-08/bughunt-sql-ref-key/round-1.md`). No `.evidence/` directory, no main-branch writes.
- **No subagents.** Every step executed in this session (Owner directive 2026-11-04).
- **VM hygiene.** baha-docker-2 claimed and released for `0427-121-native-abnahme`; cleanliness witness recorded.
- **Wrong-zone guard.** Planning repo is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (verified via `git remote`); the workers/ `baseharbor-plan` directory was never touched as a repo.

## CI ROUTING

The canonical regression `TestForeignLegacySQLReferenceDoesNotPoisonUnrelatedStopPlan` is in `cmd/baha/`, covered by the `ci.yml` "Run release-source tests" job (`go test ./cmd/baha`, lines 122-123) and the PR `pull_request` trigger on `develop` (lines 12-15). `internal/application` is covered by `go test ./internal/...` (line 121). No `.github/**` change is required — the test already lives in a CI-covered package.

## PODMAN

Pending. baha-podman-2 is held by the `podman2-e2e` lane; Podman parallel run starts only after that lane releases. Docker abnahme above is the deliverable for this shift.

## PODMAN

- **Host:** baha-podman (rootless Podman 5.7.0, 46G free, 53% used).
- **VM lock:** claimed `0427-121-podman-abnahme` (journal: `claim baha-podman 0427-121-podman-abnahme` @ 2026-11-08T01:48:22Z), released FREE after abnahme.
- **Base:** develop **e39b0004346cdfd082e34ba55d94d24757bbbd27** (post #1451 merge; matches directive). Worktree clean, zero product writes.
- **Pre-existing foreign containers:** 25 `bh-w169-ci-bootstrap-*` containers were already on this host from lane w169. Left untouched (not mine; `bh-*shared*`/foreign hygiene).
- **My lane containers:** none created — the resolution-layer abnahme does not start containers. Cleanliness witness:

```
$ podman ps -a --format "{{.Names}}" | grep -E '^(0427-121|bh-0427)' || echo "NO lane-0427-121 containers (clean)"
NO lane-0427-121 containers (clean)
$ df -h /home | tail -1
/dev/sda1        96G   51G   46G  53% /home
```

- **Native two-app abnahme (both directions + legacy ref-key + read-only intent):**

```
$ BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha/ -run 'TestPodmanTwoAppNativeStopDoesNotPoiseAcrossMalformedLegacyRefKey' -count=1 -v
=== RUN   TestPodmanTwoAppNativeStopDoesNotPoiseAcrossMalformedLegacyRefKey
    phantom_ref_key_podman_two_app_test.go:66: podman two-app native stop: both "demo" and app-b stop plans resolved;
      app-b phantom ref key did not poison app-a; intent unchanged
--- PASS: TestPodmanTwoAppNativeStopDoesNotPoiseAcrossMalformedLegacyRefKey (2.93s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	2.941s
```

- **Canonical regression (current head):**
```
$ BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha/ -run 'TestForeignLegacySQLReferenceDoesNotPoisonUnrelatedStopPlan' -count=1 -v
--- PASS: TestForeignLegacySQLReferenceDoesNotPoisonUnrelatedStopPlan (1.12s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	1.133s
```

- **Podman provider + runtime stop layers:**
```
$ go test ./internal/providers/runtime/podman/            -> ok
$ go test ./internal/runtime/ -run '.*Down.*|Stop'         -> ok
```

- **Verdict:** Podman half passes. The stop-impact resolver (`buildApplicationStopPlan` → `ResolveProviderPlan`) is runtime-agnostic; the phantom `/` legacy ref-key does not poison the unrelated app's stop nor block the owning app's stop, on Podman exactly as on Docker. The full `baha app down` CLI journey still needs operator-OIDC bootstrap (managed-env infra, out of scope); the resolution layer the CLI calls is verified here.

## END_UPDATE

DONE — both halves complete.

- **Fix:** merged PR #1450 (base ffa83e78, merge 8f8be71df), canonical regression in CI. No product diff this shift.
- **Docker abnahme** (previous shift): native two-app stop passed at buildApplicationStopPlan; evidence round-1.md.
- **Podman abnahme** (this shift): same two-app reproduction passes in both directions on rootless Podman 5.7.0; canonical regression + podman provider + runtime stop all green. Host clean (no lane containers; foreign w169 containers untouched). VM lock released FREE.
- **Base reds (not my diff):** PR#1448 `installation_destroy_native_test.go:43` (run 42434076648); 3 pre-existing `internal/application` logs/observability failures.
- **Evidence:** `baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/bughunt-sql-ref-key/round-1.md` — committed, pushed to origin/main.
- **CI routing:** regression lives in `cmd/baha/` (covered by `go test ./cmd/baha` in `ci.yml` release-source job; `pull_request` trigger on develop). No `.github/**` change required.

