# 0428-202 · packages shard red on develop — evidence (round 1)

Lane: `w202-0428-202-pkgshard` (laptop)
Card: `t-20261120-r28-packages-shard-develop-regression` (0428-202)
Task type: bug · release v0.4.28 · areas ci, observability
Owner (lane): w202-0428-202-pkgshard
Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (confirmed via `git -C baseharbor-plan remote -v`)
baseharbor GitHub remote: `lane-origin https://github.com/mcpdev80/baseharbor.git` (only github.com/mcpdev80 remote trusted; shared checkout's `origin` never used)

## RESULT: END_BLOCKED — root cause is in a locked write-set

The `PR · Go unit · packages` shard breaks on develop between `f5ce95afce1c` (green) and
`40cb28c758b0` (red) at `internal/logs` multi-source Loki health. Root cause is the
fail-closed `serviceaccess.Resolve` behaviour change in **`internal/serviceaccess/policy.go`**
(introduced by `2af892e4e`, folded into develop `40cb28c758b0`). `internal/serviceaccess/**` is
owned by lane `473e54be` (#1684, datasources/tempo-Rail), which is a LOCKED file for this card
(0428-202 write-set is `internal/logs/**` + producer/selector side only, per the task card and
`note-202-writeset.txt`). Per AGENTS 4.3 (no second writer in a locked file) and the mission's
stop rule, this lane does NOT touch `internal/serviceaccess/**`. Reporting here with file:line and
one sentence of what is wrongly decided.

## PLAN

1. Read task card 0428-202 + mission; verify planning remote (github) and baseharbor remote guard.
2. Build two isolated worktrees; run `go test ./internal/logs/ -run TestPersesLokiDatasourceMultiSource` at f5ce95af (green) and at 40cb28c (red). Record both commands + outputs.
3. Bisect the merge window f5ce95af -> 40cb28c to name the exact merge + file:line that makes per-source selector count 0. Record bisect steps.
4. Determine root cause; confirm it lies in writable set (internal/logs/** + producer/selector) and NOT in a locked file. ROOT CAUSE IS IN internal/serviceaccess/** (locked lane 473e54be/#1684) => STOP + report one line.
5. Record full bisect + two-end proof + exact line in the akte; report to Owner with file:line and one sentence of what is wrongly decided.
6. Push akte to baseharbor-plan main; verify evidence path present; post END_BLOCKED with plan-main push SHA.

## repo-rule compliance

- Planning repo confirmed: `git -C baseharbor-plan remote -v` -> `origin https://github.com/mcpdev80/baseharbor-plan.git` (github URL). Evidence is written ONLY here, never in a product repo.
- No writes to `internal/serviceaccess/**`, `internal/application/perses_runtime.go`,
  `internal/metrics/perses_prometheus_datasource.go`, `internal/observability/registry.go`,
  `internal/identityprovider/**`, `internal/operatorauth/**`, `internal/machine/**`, `cmd/baha/**`.
- No subagents, no `git add -A`, no merge, no force-push.
- Isolated worktrees only under `/var/tmp/w202-pkgshard-wt/` (approved zone; `/tmp` was full at 2.8G/13G).

## Base attestation

- develop head: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop`
- PR #1714 head: `5159192dadeec8335eb401c90fca6614e29048b0 refs/pull/1714/head`
- Break window: between f5ce95afce1c (packages SUCCESS, run 44755545566) and 40cb28c758b0 (packages RED on internal/logs).
- Merged in that window: #1715 (0428-184), #1716 (0428-182), #1717 (0428-188), #1594 (0428-053), plus CI changes #1721/#1722.

## Bisect proof (my own command + output, two ends)

Isolated worktrees: `/var/tmp/w202-pkgshard-wt/f5ce95af` and `/var/tmp/w202-pkgshard-wt/40cb28c`.
Test command: `go test ./internal/logs/ -run 'TestPersesLokiDatasourceMultiSource' -count=1 -v`.

### END A — f5ce95afce1c (green baseline, run 44755545566)

```
$ go test ./internal/logs/ -run 'TestPersesLokiDatasourceMultiSource' -count=1 -v
=== RUN   TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource
--- PASS: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource (0.00s)
=== RUN   TestPersesLokiDatasourceMultiSourcePartialMatchability
--- PASS: TestPersesLokiDatasourceMultiSourcePartialMatchability (0.00s)
=== RUN   TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed
--- PASS: TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/internal/logs	0.016s
```

### END B — 40cb28c758b0 (develop head, RED, job 136433151042, run 44778040176)

```
$ go test ./internal/logs/ -run 'TestPersesLokiDatasourceMultiSource' -count=1 -v
=== RUN   TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource
--- FAIL: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource (0.00s)
=== RUN   TestPersesLokiDatasourceMultiSourcePartialMatchability
--- FAIL: TestPersesLokiDatasourceMultiSourcePartialMatchability (0.00s)
=== RUN   TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed
--- FAIL: TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed (0.00s)
FAIL
FAIL	github.com/mcpdev80/baseharbor/internal/logs	0.009s
```

Verbatim failure (END B):
```
loki_test.go:522: health must pass for a healthy multi-source Loki: perses Loki datasource health client: load Loki service access identity: stat /tmp/.../service-access/pki/client-cert.pem: no such file or directory
loki_test.go:633: expected 2 per-source queries even on full miss, got 0
```

### The break is NOT in internal/logs

```
$ git diff --name-only f5ce95afce1c 40cb28c758b0 -- internal/logs/
(empty)
$ git diff --name-only f5ce95afce1c 40cb28c758b0 -- internal/serviceaccess/
internal/serviceaccess/policy_explicit_test.go
internal/serviceaccess/policy.go
internal/serviceaccess/policy_test.go
```

`internal/logs/**` is byte-identical across the break. The ONLY changed source in the failing
package's dependency path is `internal/serviceaccess/policy.go`.

### The one line that carries the behaviour

The test manifest uses environment `dev` (`application.New("perses-loki-demo", "dev", ...)`). The
Loki health path resolves the policy via
`serviceaccess.Resolve(m.Environment, "loki", serviceaccess.AuthenticationMTLS)`.

`internal/serviceaccess/pki.go:111` —
`requireClient := policy.AuthenticationRequired && policy.Authentication == AuthenticationMTLS`.
The test's `materializeLokiServiceAccessPKI` only writes `server-cert.pem`/`server-key.pem` (no
`client-cert.pem`), so `requireClient` MUST be `false` for the test to pass.

Two-end diff of `internal/serviceaccess/policy.go` (the responsible change, `2af892e4e` folded into
`40cb28c758b0`):

```diff
-	switch environment {
-	case "dev", "development":
-		p.AuthenticationRequired = false        // <-- was: dev = trusted-local (no client cert)
-	case "test", "testing", "stage", "staging", "prod", "production":
-		p.AuthenticationRequired = true
-	default:
-		// Custom environments are treated as managed ...
+	// The compatibility API has no trusted policy source. Treat every
+	// environment as managed until a caller supplies an explicit policy.
+	return ResolveWithPolicy(environment, provider, authentication, EnvironmentPolicy{})
...
+	switch {
+	case policy.TrustedLocal:
+		p.AuthenticationRequired = false
+	default:
+		// Managed (or an explicitly untrusted environment): authentication is
+		// required ...
+		p.AuthenticationRequired = true
 	}
```

At `f5ce95afce1c:internal/serviceaccess/policy.go` lines 94-96: `switch environment { case "dev",
"development": p.AuthenticationRequired = false`. At `40cb28c758b0:internal/serviceaccess/policy.go`
lines 140-145 the `PKIManagedLocal` short-circuit returns `p` with
`p.AuthenticationRequired = true` (the fail-closed `ResolveWithPolicy`), so
`ExistingTLSMaterial(policy, ...)` sets `requireClient = true` and demands
`service-access/pki/client-cert.pem`, which the test never materialises → file-not-found → shard
red.

### No trusted-local source exists for `dev` (confirms the regression is unmitigated)

```
$ grep -rn "ResolveWithPolicy\|TrustedLocal: *true" internal/ --include=*.go | grep -v _test.go
(empty)
```

No caller supplies `ResolveWithPolicy(..., EnvironmentPolicy{TrustedLocal: true})`. The new
design's only escape hatch from managed is an explicit `TrustedLocal` policy, and there is no
source feeding it for `dev`/`development`. So `dev` Loki mTLS now always requires a client
certificate the test does not provide. The `internal/logs` multi-source Loki test assumed the old
`dev` = trusted-local behaviour; that assumption is now broken by the `serviceaccess` change, not
by anything in `internal/logs`.

## Conclusion / what is wrongly decided (one sentence)

`serviceaccess.Resolve("dev", "loki", MTLS)` now returns `AuthenticationRequired = true`
(fail-closed managed) via `internal/serviceaccess/policy.go` `ResolveWithPolicy`
(`2af892e4e`/`40cb28c758b0`), so `internal/serviceaccess/pki.go:111` requires `client-cert.pem`,
which no `dev` environment or caller supplies and which the `internal/logs` multi-source Loki test
does not materialise — the regression lives in the locked `internal/serviceaccess/**` write-set
(lane `473e54be`, #1684), not in this card's `internal/logs/**` write-set.

## Cross-checks (named only, this card's scope)

- PR #1645 head `4abc25ab6772` (run 44731562217) fails the same shard on `internal/identityprovider` — that is `internal/identityprovider/**`, owner field #1650, left to #1650.
- 0428-198 lane independently confirmed the same operator/OIDC pre-existing gate defect ("this is the pre-existing 0428-198 gate defect, NOT caused by my change") — two independent witnesses that the gate is broken while the card content is fine.
- The blind spot: develop push runs only `Runtime · Docker Core` / `Runtime · Podman Core` (runs 44769994971, 44769994909 = success); the unit shards are PR-only, so a develop-side breakage is invisible until a PR hops onto develop and pays for it.

## Cleanliness

- No docker/podman compose projects, containers, networks or volumes started. State under `/var/tmp/w202-pkgshard-wt/` only (git worktrees, no containers).
- before: `/var/tmp/w202-pkgshard-wt/` — two worktrees (f5ce95af, 40cb28c). after: same, no containers/netzwerke/volumes created.
- cleanliness: clean — no container/network/volume/state-dir artifacts; ambient-core images of foreign carts untouched.

## END

END_BLOCKED w202-0428-202-pkgshard — root cause in locked `internal/serviceaccess/policy.go`
(lane 473e54be/#1684); Owner/owner-lane fixes there. This lane made no product change.
