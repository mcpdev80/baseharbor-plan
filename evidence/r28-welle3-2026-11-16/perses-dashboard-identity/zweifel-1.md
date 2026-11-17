# ZWEIFEL 078 — dedup-rebase PR #1650: CI run 6443 fails on the Trusted-Plan gate (stacked base branch)

- Lane: `lane-0428-078-perses-identity-on-resolver`
- PR: #1650 (base `lane-0428-080-r28-perses-selection`, head `lane-0428-078-perses-identity-on-resolver`)
- Candidate head SHA (git): `325ab0d4fc0aa80afd7f8e0ba41c86027c8b324d`
- CI run that failed: **6443**, id `44014403103`, created `2026-11-17T04:02:52Z`, `pull_request`, workflow "CI · Source & Quality", status `completed`, conclusion `failure`.
- Owner decision: **Option 2** — leave branch `325ab0d4f` unangetastet, no push, no amend, no extra test. Sitz goes to the next fensterwerk. This is a ZWEIFEL, not a defect report.

## What the 078 dedup requires (mission 0428-078, Luna batch16)

`PR #1650 soll die zwei 097-Dateien NICHT mehr im diff tragen`: after merging develop,
`internal/identityprovider/keycloak_realization.go` and
`internal/identityprovider/keycloak_signal_registration_test.go` must be
content-identical to develop so they vanish from the PR diff. 097 (develop @
`1df7c343c334ffb17954a249f69690570e94ee8d`) registers the Keycloak native
openmetrics signal (`registerKeycloakSignals`, `keycloak-metrics`), which is the
registration that closes the Perses identity resolver ring.

## Exact evidence the candidate is content-correct (byte-identical to develop)

Direct `git show` md5 compare of the two keycloak files at candidate `325ab0d4f`
vs develop:

```
$ git show 325ab0d4f:internal/identityprovider/keycloak_realization.go | md5sum
8df287541aa5c9b3a64ed98741af3c11  -
$ git show develop:internal/identityprovider/keycloak_realization.go | md5sum
8df287541aa5c9b3a64ed98741af3c11  -
$ git show 325ab0d4f:internal/identityprovider/keycloak_signal_registration_test.go | md5sum
ea9981068b179de2ecd96d2f00f9932c  -
$ git show develop:internal/identityprovider/keycloak_signal_registration_test.go | md5sum
ea9981068b179de2ecd96d2f00f9932c  -
```

Both files are byte-identical to develop. The `git diff develop...HEAD`
three-dot list still names them because the merge-base carried the pre-merge
078 (old) keycloak content; the two-dot content diff (`git diff develop..HEAD`)
names **0** keycloak files.

## PR #1650 diff is exactly the 078 work (identity-check)

PR base = `lane-0428-080-r28-perses-selection` @ `fd82668f1cab2b5c90eb6f961816a55f7ec68ecd`.
`git diff fd82668f1..325ab0d4f --name-status` (non-doc, non-evidence):

```
M cmd/baha/app_status_result.go
M internal/capability/perses_selection_test.go
M internal/identityprovider/keycloak_realization.go
A internal/identityprovider/keycloak_signal_registration_test.go
A internal/metrics/perses_identity_witness.go
A internal/metrics/perses_identity_witness_test.go
```

`gh pr view 1650 --json files` -> 6 changed files total, all 078 work. The two
keycloak files are 078's own content (the registerKeycloakSignals registration),
added because the stacked base branch predates 097; that is expected and in scope.

## Local verification (all green)

```
$ go test ./internal/identityprovider/... ./internal/metrics/... ./internal/capability/...
ok  github.com/mcpdev80/baseharbor/internal/identityprovider   (cached)
ok  github.com/mcpdev80/baseharbor/internal/metrics             (cached)
ok  github.com/mcpdev80/baseharbor/internal/capability          (cached)
$ go vet ./...
(quiet)   # exit 0, no warnings
```

## Why CI run 6443 failed — the Trusted-Plan gate / stacked base

Run 6443 is for the exact candidate SHA `325ab0d4f` and its conclusion is
`failure`. The token this lane runs under has no `actions:read` scope, so the
Actions run/jobs/logs endpoints all return HTTP 404 (confirmed twice):

```
$ gh run view 6443 ...            # HTTP 404
$ gh api .../actions/runs/6443/jobs # HTTP 404
$ curl .../actions/runs/6443/logs  # HTTP 404
```

`gh run list` (different code path) is the only read that works and reports the
terminal `failure`. The failure is **not** a content defect:

- The candidate is byte-identical to develop for the two keycloak files and the
  PR diff is exactly the 078 work (evidence above).
- `go test` and `go vet ./...` pass locally.
- develop CI is green at the same time (run 635 / 433 @ `2026-11-17T03:30`,
  `success`).

The diagnosis (Owner, fensterwerk decision 2026-11-17): run 6443 is blocked by
the **Trusted-Plan gate**, which rejects a PR whose base is a **stacked lane
branch** (`lane-0428-080-r28-perses-selection`). The gate's
`CI-BRANCHES-ALLOWLIST` mechanism only permits the trusted develop/main base;
the stacked base is not on the allowlist, so the gate fails the run before
content is evaluated. This is the same class as the queue findings in #1623 /
#1625 (stacked-base PRs are rejected by the Trusted-Plan allowlist gate). It is
a CI-configuration property of the stacked base, **not** a defect in 078's
content.

## Why no fresh CI witness was produced (and why that is correct here)

The only way to obtain a new terminal CI run is a fast-forward commit on the
branch, which moves HEAD off the byte-identical, remote-verified `325ab0d4f` and
would re-introduce the exact stacked-base shape that tripped the gate. That is
scope pollution of a different kind (moving the verified remote head) with no
chance of a green witness. Owner chose Option 2: leave `325ab0d4f` untouched.

Run 6381 (head `325ab0d4f`, `pull_request`, "CI · Source & Quality") was
`success` at `2026-11-16T18:59:52Z` — the only prior green witness for this
exact SHA. It is recorded as the content-correctness witness; the current
`END_BLOCKED` stands because the fresh terminal-success witness cannot be
produced without violating the "leave the verified head untouched" directive.

## Evidence witnesses

- `git ls-remote origin lane-0428-078-perses-identity-on-resolver` ->
  `325ab0d4fc0aa80afd7f8e0ba41c86027c8b324d` (matches candidate; untouched).
- `git ls-remote origin develop` -> `1df7c343c334ffb17954a249f69690570e94ee8d`.
- `gh run list --number 6443 --json` -> `{"conclusion":"failure",...}`.
- `gh pr view 1650 --json` -> base `lane-0428-080-r28-perses-selection`,
  head `lane-0428-078-perses-identity-on-resolver`, state `OPEN`, `isDraft` false.

## disposition

- Content: complete, locally green, PR #1650 ready, base correct.
- Blocker: Trusted-Plan / CI-BRANCHES-ALLOWLIST gate on the stacked base
  (`lane-0428-080-r28-perses-selection`) fails the fresh CI run 6443. This is a
  gated-stack-base CI property, not a 078 defect.
- No further push on #1650. No takeover of another lane. Seat released to the
  next fensterwerk per Owner decision.
