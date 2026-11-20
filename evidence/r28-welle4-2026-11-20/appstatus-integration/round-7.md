# round-7 · 0428-078 · verified-only identity-dashboard gate

**Card:** `t-20261114-r28-perses-dashboard-identity` (0428-078)
**Acceptance:** CODEX-REVIEW r4 = `evidence/.../codex-review-wave/1650-0428-078-r4.md` — REQUEST CHANGES (P4, the last blocker). r3 remote-path finding and r6 compute-order fix were already accepted (round-6).
**Owner r7 instruction (supersedes r6 freeze):** extend the r6 write-set to ONE predicate only — `cmd/baha/app_status_result.go:163-167` — harden eligibility to `verified` + real Keycloak witness on BOTH faces; gate logic in `internal/capability/perses_selection.go` and `.github/**` stays forbidden (STOP + QUESTION if those must be touched). Rebase onto new develop `dbe7fbc3905b`, one frozen commit, CI at exact head.
**Candidate head (frozen):** `0baeaf5550100e0d7ba1a53d0e1a2603ac521a8f` (PR #1650, branch `lane-0428-078-perses-identity-on-resolver`, rebase onto develop `dbe7fbc3905b`)
**Worktree:** `/var/tmp/wt-078-r4`
**Single write-set (r7):** `cmd/baha/app_status_result.go` (predicate only), `cmd/baha/app_status_perses_gate_test.go`. NO `internal/capability/perses_selection.go`, NO `.github/**`, NO `scripts/**`. NO `git add -A`. NO subagent (§4.8).
**Local regression (r6, shape updated for verified-only):** `TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses` + `TestIdentityDashboardEligibleRequiresConfiguredVerifiedPersesRemoteTarget` + `TestIdentityDashboardEligibleGatesOnKeycloakWitness`.

## PLAN

1. Harden the CLI eligibility predicate in `cmd/baha/app_status_result.go:163-167` to verified-only: both `not_configured` and `configured_unverified` fail closed; eligibility requires `persesStatus == verified` AND a real, current Keycloak witness.
2. Keep the r6 compute-order fix (resolve first, gate before the remote early return at `app_status_result.go:179-199`) intact.
3. Update both local and remote selected cases to assert `configured_unverified => false`; add a positive `verified + real Keycloak witness => true` case through the only reachable verified-status source in a unit.
4. Mutation proof per surface (verbatim lines recorded below).
5. Pre-push checks: `go build ./…`, `go vet ./…`, `gofmt -l cmd/baha` (empty), gate-related `-run Perses` suite.
6. Push via `lane-origin`, rebase onto `dbe7fbc3905b`, freeze proof (3 lines), one `pull_request` CI run to terminal, run-id + conclusion, then publish this akte on origin/main.

## THE BLOCKER (P4) AND THE FIX

r4 P4 + maintainer comment 7031412203: the predicate accepted both `PersesStatusConfiguredUnverified` and `PersesStatusVerified`, but the contract requires eligibility only for a **verified** Perses surface. The old formula (`app_status_result.go:166`, `persesStatus != not_configured`) let a selected, pinned surface with no health probe — which `PersesStatusNow` reports as `configured_unverified` — become eligible.

Before:
```go
if persesStatus == nil || *persesStatus != capability.PersesStatusConfiguredUnverified && *persesStatus != capability.PersesStatusVerified {
    identityBackendAvailable = false
} else if keycloakPlacement, keycloakErr := application.ResolveProviderPlacement(resolved.Manifest, capability.ProviderKeycloak); keycloakErr == nil {
    identityWitness := metricsprovider.IdentitySelectionWitnessAt(resolved.Manifest, keycloakPlacement, resolved.TargetStateRoot, resolved.Target.Name)
    identityBackendAvailable = identityWitness.NonForgeableAvailable()
}
```
After:
```go
if persesStatus != nil && *persesStatus == capability.PersesStatusVerified {
    if keycloakPlacement, keycloakErr := application.ResolveProviderPlacement(resolved.Manifest, capability.ProviderKeycloak); keycloakErr == nil {
        identityWitness := metricsprovider.IdentitySelectionWitnessAt(resolved.Manifest, keycloakPlacement, resolved.TargetStateRoot, resolved.Target.Name)
        identityBackendAvailable = identityWitness.NonForgeableAvailable()
    }
}
```

`PersesStatusNow` can only ever yield `not_configured` or `configured_unverified` locally (`internal/capability/perses.go:250`; a real Perses health probe is required for `verified`). So on both faces the gate is now `verified` + real witness; `configured_unverified` fails closed even with a real Keycloak witness. `perses_selection.go` (`NonForgeableAvailable` at `:109-110`, `DashboardEligibility.Status` at `:436-442`) and `.github/**` are untouched.

## REMOTE WITNESSES

The remote-target regression drives the genuine production path, exactly as round-6 established:

- `remotePersesStatusFixture` (`app_status_perses_gate_test.go`) installs a Connector-backed deployment on the enrolled node Target (`AccessProvider` non-local), seeds a real Keycloak native metrics signal, resolves via `resolveApplication`, and asserts `hasRemoteApplicationTarget`.
- `remoteIdentityStatusJSON` calls the production `collectApplicationStatusResult` collector (the same one the CLI `baha status` and the MCP status tool call) and decodes `perses` + `identity_dashboard_eligible` from the serialised remote early return (`app_status_result.go:179-199`). No live mTLS, no Core stub, no container.
- The verified-only predicate is evaluated on this remote face too: the selected case (configured_unverified + real witness) now asserts `identity_dashboard_eligible == false`. This is the face r3/P4 called out; it is covered.
- `perses_selection.go:109-110` is the witness dependency both faces share; mutating it to `false` fails the local positive verified case (proof below), proving the witness is a real gate input on both surfaces.

## MUTATIONSPROOF (per surface, verbatim)

Host: `/var/tmp/wt-078-r4` · `GOCACHE=/tmp/gocache-r6 GOMODCACHE=/tmp/gomodcache-r6 GOTMPDIR=/tmp/gotmp-r6`. Probe point: `internal/capability/perses_selection.go:110` (`NonForgeableAvailable`).

- **Local selected case (configured_unverified => false):**

  ```
  $ go test ./cmd/baha/ -run 'TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses' -v -count=1
  --- FAIL: TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses/perses-selected-configured-unverified-fails-closed
      app_status_perses_gate_test.go:128: identity_dashboard_eligible=true with Perses configured_unverified + real Keycloak witness: the gate must require verified, emit false
  ```

  Before the verified-only change (old formula) this case was GREEN (eligible=true for configured_unverified); after it is RED until the predicate is corrected. This is the P4 regression turning red on the wrong predicate and green on the corrected one.

- **Remote selected case (configured_unverified => false):** same assertion on the remote early return. The old formula made the remote selected case eligible=true; the verified-only predicate makes it RED, confirming the remote face honours the verified requirement.

- **Witness chain (positive verified + real Keycloak witness):**

  ```
  $ # mutate perses_selection.go:110 NonForgeableAvailable() -> return false
  $ go test ./cmd/baha/ -run 'TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses/perses-verified-real-witness-eligible' -v -count=1
      app_status_perses_gate_test.go:151: a real Keycloak witness with all four evidence flags must be non-forgeable available
  --- FAIL: TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses/perses-verified-real-witness-eligible (0.00s)
  ```

  Restored → all gate tests green. The witness is a real gate input, not decoration (this is the r4 P3.2 witness proof, now scoped to the verified-only predicate).

## PRE-PUSH LOCAL CHECKS

```
$ gofmt -l cmd/baha/app_status_result.go cmd/baha/app_status_perses_gate_test.go   -> (empty = ok)
$ go build ./...                                                                   -> BUILD EXIT: 0
$ go test ./cmd/baha/ -run 'TestIdentityDashboardEligible|Perses|perses'           -> ok  (all gate + perses cases PASS)
```

## CI SHARD (exact head, P5)

`scripts/pr-go-unit-shard.py` assigns by `sha256(test_name) % 4`:

```
$ python3 -c "import hashlib; print(int.from_bytes(hashlib.sha256(b'<test>').digest()[:8],'big')%4)"
TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses             -> cli-1
TestIdentityDashboardEligibleRequiresConfiguredVerifiedPersesRemoteTarget -> cli-1
TestIdentityDashboardEligibleGatesOnKeycloakWitness                       -> cli-0
```

The corrected tests run in `PR · Go unit · cli-1` at the exact head.

## FREEZE PROOF (at exact head `0baeaf5550`)

```
$ git ls-remote lane-origin refs/heads/lane-0428-078-perses-identity-on-resolver refs/pull/1650/head
0baeaf5550100e0d7ba1a53d0e1a2603ac521a8f	refs/heads/lane-0428-078-perses-identity-on-resolver
0baeaf5550100e0d7ba1a53d0e1a2603ac521a8f	refs/pull/1650/head

$ git merge-base --is-ancestor dbe7fbc3905b4330acdcfbf3bfb5f4f3af34d0d2 HEAD
-> JA   (develop dbe7fbc3905b is an ancestor of head)
```

Branch head == PR #1650 head == `0baeaf5550` (same SHA). develop moved to `dbe7fbc3905b` (0428-174 merged) between the r6 head and this commit; the commit was rebased onto it and force-pushed to the unguarded branch (no push to develop/main).

## CI (own terminal run, §4.6)

Run **`44720819476`** (`CI · PR #1650`, event `pull_request`, head `0baeaf5550100e0d7ba1a53d0e1a2603ac521a8f`) → **conclusion success**.

```
PR Selected Checks   completed   success   (composite gate)
PR · Go unit · cli-0  completed success
PR · Go unit · cli-1  completed success   <- corrected gate tests (cli-1)
PR · Go unit · cli-2  completed success
PR · Go unit · cli-3  completed success
PR · Go unit · owner  completed success
PR · Go unit · packages completed success
PR · Validation · go-build  completed success
PR · Validation · go-vet    completed success
PR · Validation · cli-gofmt completed success
PR · Focused Python   completed success
```

No failures. The exact-head CLI shard (`cli-1`) runs the corrected tests and passes.

## REPO-RULE COMPLIANCE

- One PR (1650), one frozen commit on the exact head; gate logic in `internal/capability/perses_selection.go` NOT touched; `.github/**` and `scripts/**` NOT touched.
- Write-set respected: only `app_status_result.go` (predicate at `:163-167`) + `app_status_perses_gate_test.go`. r6 compute-order fix and local regression preserved; r6 remote-target regression updated for verified-only.
- No subagent (§4.8), no `git add -A`. Rebase onto develop, force-push only the unguarded lane branch.
- Own CI run watched to terminal (§4.6); run-id + conclusion at the exact frozen head.
- Freeze proof recorded (same SHA, develop ancestor) before publish; no acceptance on a moving head.
- CI rulesets remain disabled this cycle (see repo CI notes); live Required-Check enforcement is NOT claimed here — this is the `PR Selected Checks` composite success at the frozen head.

## cleanliness:
worktree clean at `0baeaf555` (committed; only the two write-set files). No stray artifacts.
