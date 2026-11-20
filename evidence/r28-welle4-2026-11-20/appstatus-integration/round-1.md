# 0428-078 — app_status integration (round 1)

Card `t-20261114-r28-perses-dashboard-identity` (0428-078), lane
`lane-0428-078-appstatus-integration` (integration work), then retargeted onto
`lane-0428-078-perses-identity-on-resolver` (PR #1650's branch). Role: worker.
Evidence owner: this lane; no product write outside baseharbor-plan.

## Realities / witnesses

- `git ls-remote origin refs/heads/develop` -> `ec02d5faad2499c8bf5ed08ce2ae1f5aac25d80f`
  (live, read at END).
- `git ls-remote origin refs/heads/lane-0428-078-perses-identity-on-resolver` -> `82bac3fab7c28d3765c189dc12f32ac65b06a9d2`
  (my final head, live).
- PR #1606: `state=CLOSED`, draft=true.
- PR #1650: `state=OPEN`, draft=false, base=develop.
- `origin/main` (baseharbor-plan) at `6fb95011b5c2` when the akte was opened.

### Three diffs of `cmd/baha/app_status_result.go` (all read against the exact
blob hashes; develop blob `f963601a560338f46a22c7d4ca8836655b8c6478`)

1. Winner #1650 (`022c454ce482`) vs loser #1606 (`4e81c16ddcf7`) — differs.
   `#1650` ADDS the `IdentityDashboardEligible` field (`cmd/baha/app_status_result.go`
   ~L39-45) and the non-forgeable witness call
   `metricsprovider.IdentitySelectionWitnessAt(...).NonForgeableAvailable()`
   (`cmd/baha/app_status_result.go` ~L159-162) plus both struct-return sites
   (`cmd/baha/app_status_result.go` ~L169, ~L275). `#1606` strips them.
2. `#1650` (`022c454c`) vs develop (`f963601`) — differs. `#1650` keeps
   `HostContainersDashboards` AND adds `IdentityDashboardEligible`.
3. `#1606` (`4e81c16d`) vs develop (`f963601`) — differs. `#1606` removes both
   `HostContainersDashboards` and `IdentityDashboardEligible`.

## Decision (with reason, not preference)

Winner is PR #1650. The card contract (Goal + Acceptance: "Deliver
identity-provider panels only for verified current Keycloak metrics; do not
rely on obsolete SPI assumptions") demands a non-forgeable identity-dashboard
eligibility gate. #1650 implements exactly that: `IdentityDashboardEligible`
derived from a real Keycloak native metrics signal via
`IdentitySelectionWitnessAt(...).NonForgeableAvailable()`, fail-closed on
missing signal, unselected provider, or non-BaseHarbor-owned placement.

Loser #1606 additionally STRIPS `IdentityDashboardEligible` (and, on its own
older base, `HostContainersDashboards`); its blob `4052832c` carries nothing
unique to the card. The stripped host-containers body is already represented
upstream (card 0428-077 / #1602 carries `HostContainersDashboards` and the
CLI test `TestBahaStatusHostContainersDashboardsExposesUnavailable`), so #1606
would duplicate an existing version.

## Loser closed

`gh pr close 1606` with a comment pointing at PR #1650 and this akte. Live
state: CLOSED (witness above).

## Winner retargeted (linear rebase, Owner directive 2026-11-20)

The #1650 head `022c454c` is a merge commit whose first-parent spine carries
unrelated #0428-075/#0428-080 releases and is based on a develop version that
precedes card 0428-077/#1602 — pushing it onto current develop would revert
~22k lines of current develop. The correct, provably-correct linear head on
current develop is: current develop + the card's own
`cmd/baha/app_status_result.go` change + the single dependency file it needs.

Final head: `82bac3fab7c28d3765c189dc12f32ac65b06a9d2`, first-parent chain is
exactly:

- `de77b3b2` fix(0428-078): land IdentityDashboardEligible witness on develop
- `82bac3fa` fix(0428-078): add IdentityDashboardEligible + keep
  HostContainersDashboards

`origin/develop` (`ec02d5fa`) is the sole base; `git merge-base --is-ancestor
origin/develop HEAD` -> OK.

Files changed vs develop (exact write-set, no other develop file touched):

- `cmd/baha/app_status_result.go` — union of both Perses faces:
  `HostContainersDashboards` (develop's 0428-077 face, preserved) plus
  `IdentityDashboardEligible` (winner #1650 witness). Both struct returns
  populate both fields.
- `internal/metrics/perses_identity_witness.go` (added) — `IdentitySelectionWitnessAt`,
  depends only on develop symbols (`application.HasIdentity`,
  `capability.IdentitySelectionWitness`, `observability.List`,
  `NonForgeableAvailable`).
- `internal/metrics/perses_identity_witness_test.go` (added) — unit tests for
  the witness (eligible-when-real-signal, fail-closed without signal / not
  selected / external placement).
- `observability.List` call adapted to the develop HEAD signature (threaded
  `requestedEnvironment=""`), which does not change semantics (no
  environment filter on the Keycloak-native-signal check).

`git diff origin/develop -- cmd/baha/app_status_result.go` is the union diff
documented under "Decision" above.

## Gate plan + CI (executed, not claimed)

Gate plan (`scripts/pr-gate-plan.py --diff <pr-diff-base JSON>`, simulated
runner context `GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop`,
the guard fails closed when the authenticated context is genuinely unknown):

- `go build ./cmd/baha` (cli-build)
- `go vet ./cmd/baha` (cli-vet)
- `go test ./cmd/baha -run '^TestGuided'` (cli-guided-tests)
- `go test ./internal/application/... ./contracts/...` (source-contracts)

Local pre-run against head `82bac3fa` (all PASS):
`go build ./...`, `go vet ./cmd/baha`, `go test ./internal/metrics/...`,
`go test ./internal/application/... ./contracts/...`,
`go test ./cmd/baha -run '^TestGuided'` (38s),
`go test ./cmd/baha -run 'Perses|Identity|Status'` (34s),
`go test ./cmd/baha -run 'TestBahaStatusHostContainersDashboardsExposesUnavailable'`.

CI run 6710 (dbId 44662988741), head `82bac3fa`, event=pull_request,
conclusion=success (authoritative `gh run list` witness;
`https://github.com/mcpdev80/baseharbor/actions/runs/44662988741`).
Previously-failing `PR · Go unit · cli-2` (`TestBahaStatusHostContainersDashboardsExposesUnavailable`)
now passes on this head.

Note on the earlier run 6704 @ `bf9ff590`: it failed `PR · Go unit · cli-2`
because the head dropped `HostContainersDashboards` from the CLI struct while
develop's `TestBahaStatusHostContainersDashboardsExposesUnavailable` still
asserts that face. That is the winner/#1650-vs-develop conflict at
`cmd/baha/app_status_result.go`; resolved here by keeping both faces (the
union), not by dropping develop's face.

## repo-rule compliance

- Evidence lives ONLY in baseharbor-plan (`evidence/r28-welle4-2026-11-20/appstatus-integration/round-1.md`);
  no `.evidence/` directory, no product-repo writes, no main-branch writes.
- Evidence committed from `/var/tmp/x078-plan` (NOT the quarantined
  `workers/baseharbor-plan`). `git add` restricted to the single akte file
  (never `git add -A` in plan worktrees).
- No `.github/**` edit, no `workflow_dispatch`, no runner repair, no
  merge, no subagent.
- Pushes to my own unprotected lane branch only, all with
  `--force-with-lease`; no force-push on develop/main.
- No subagents (§4.8); every step ran in this session.
- No Docker/Podman compose projects started (no host-VM test named).

## cleanliness

- No containers, networks, volumes, or state directories created. No
  `baha` runtime fixtures left in the clone (`baha` binary and
  `internal/application/*/runtime/` test scratch removed before commit; only
  the 3 card files were added to baseharbor-plan).
- Before/after: before — nothing committed; after — one akte file added to
  baseharbor-plan origin/main.
- cleanliness: clean. No orphaned runtimes; nothing to bring down.

## END

END_DONE — 0428-078 resolved: winner PR #1650 (head `82bac3fa`), loser PR #1606
CLOSED, CI run 6710 success.
