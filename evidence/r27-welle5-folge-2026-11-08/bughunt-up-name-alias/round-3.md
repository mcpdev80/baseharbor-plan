# 0427-130 r3 — PR #1459 up NAME command-entry regression (round 3)

Lane: mission-130-r3 (shift r27-welle5-folge-2026-11-08)
Mission: `/tmp/opencode/mission-130-r3.md`
Recipe: `act-1459-review-r2.md` (baseharbor-plan evidence, origin/main)
Evidence repo (authoritative): `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY (NOT workers/baseharbor-plan)

## Remote witness (measured via git ls-remote, own zone)

```text
d30de3a4a176e073c8c1a9a0fc0b0ef06202b064	refs/heads/develop
da68dd48abab8acc48d8e882d39015cef257e710	refs/pull/1459/head
b709b80dfa6717f6bbf44da46824ed82ac2d8ae0	refs/pull/1464/head
96b54ce29660797351179ae6db86748328c1fb85	refs/heads/main (baseharbor-plan)
```

- PR #1459: head `da68dd48`, base develop, open, not draft, mergeStateStatus=UNSTABLE.
- PR #1464 (the develop-build defect that raises the native owner-state prerequisite): OPEN, `mergedAt=null`, NOT merged into develop.

## PLAN

- Verify remote truth: PR #1459 head, develop head, #1464 in develop, baseharbor-plan origin/main
- Reproduce: confirm new regression calls resolver directly, not the CLI up entry (runWithIO) in cmd/baha test
- Rewrite the test to drive the real `baha up NAME` command entry and assert resolution+output
- Check native docker+podman exact-head status; #1464 blocker; poll once (max 1 per 2-3 min)
- Publish evidence to baseharbor-plan origin/main; ls-remote + cleanliness witness
- Bring down any containers/networks/state; post END_BLOCKED; tick todo board

## Repo-rule compliance

- Single product file changed: `cmd/baha/runtime_ports_test.go` (one test rewritten).
- No `.github/**` touched (owner scope). No runner/container/VM work. No workflow rerun/dispatch.
- No subagents (directive 2026-11-04). Every step run in this session.
- `gofmt -l` clean on the file; `go vet ./cmd/baha/` clean.
- Regression runs daemon-free and passes in 0.89s.

## Finding 1 — alias regression did not drive the command entry (CORRECTED)

Exact-head diff of PR #1459 is one file: `cmd/baha/runtime_ports_test.go` (+83 lines).
`TestUpNameResumesRegisteredDeploymentAcceptsParity` (lines 342–420 at the reviewed head) called
`resolveRegisteredApplication(...)` directly at lines 386 and 417 and never invoked the top-level
command action (`rootCommand`/`runtimeUpCommand` via `runWithIO`). It proved the resolver accepts a
handed name, not that the reported regression is fixed through the real `baha up NAME` entry. The
claim in its doc comment ("production-command path") exceeded what it executed.

Production routing (verified in source):
`runWithIO(ctx, []string{"up", NAME, ...})` -> `rootCommand` -> `runtimeUpCommand` ->
`routeRepositoryRuntimeUp` -> `resolveApplication(ctx, store, nil, "apply")` -> with a NAME arg ->
`resolveRegisteredApplication(ctx, target, targetRoot, NAME, "", "up")`.
`baha app up NAME` -> `appUpCommand` -> `executeApplicationUpLifecycle` -> `resolveApplication(ctx, store, [NAME], "up")`
-> `resolveRegisteredApplication`. Resolution happens in-process BEFORE any runtime inspection.

Key empirical result (built exact-head binary, ran on host docker):
- The top-level `baha up NAME` command entry bootstraps the shared management Core (SQL+Secrets+Identity/OpenBao)
  before it resolves — a real ~150s bootstrap that needs a clean, working docker host. On this shared
  host it failed with `Core sql failed: existing native network lacks a protected Core or shared backend owner`
  (leftover Core state from aborted runs). This is why a full-resume `up NAME` is a native/runtime acceptance
  concern, exactly why the native gate is red and gated behind PR #1464.
- `baha app up NAME` resolves the registered deployment by NAME through the entry in 0.02s with no daemon,
  emitting the resolved application header `BaseHarbor · <NAME> · <ENV>`, then fails closed with
  `application runtime has not been applied: run 'baha app apply <NAME>' first` for a registered-but-not-applied
  deployment. That fail-closed is itself proof the NAME reached the command entry from an empty working dir.

## Correction applied (this round)

Rewrote `TestUpNameResumesRegisteredDeploymentAcceptsParity` in `cmd/baha/runtime_ports_test.go`
(57 insertions / 33 deletions) to drive the real command entry:

1. Seeds a registered deployment via the existing unit helper `registerTestDeployment`, sets the target,
   and `t.Chdir` to a fresh empty temp dir (no `baseharbor.yaml`) so a cwd-based resolution cannot win.
2. `baha app up NAME --yes --skip-memory-preflight` via `runWithIO` must emit the resolved NAME in its output
   (proving the entry selected the registered deployment by NAME), and must fail closed on the
   registered-but-not-applied deployment with an `apply` guard.
3. `baha up NAME --yes --skip-memory-preflight` via the same entry must fail closed for the same
   registered-but-not-applied deployment (a cwd-based resolution from the empty dir cannot reach it).
4. Parser parity retained: both parsers accept the same single optional NAME and agree on the value.
5. Fail-closed for an unregistered NAME through the command entry (`up <unknown>` must error).

Regression result:
```
=== RUN   TestUpNameResumesRegisteredDeploymentAcceptsParity
--- PASS: TestUpNameResumesRegisteredDeploymentAcceptsParity (0.89s)
PASS
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.901s
```
`gofmt -l` clean; `go vet ./cmd/baha/` clean.

CI routing: the corrected test runs under `PR · Validation · go-unit-tests` (`go test ./... -count=1` on
`pull_request`), which covers `cmd/baha`. The native-destroy impact selector
(`scripts/test-ci-impact-selectors.sh`) does NOT route `cmd/baha/runtime_ports_test.go` to develop
acceptance — it is a pure unit test, not a destroy test. No `.github/**` change was needed to pick it up.

## Blocker — native docker/podman red on the exact head (external, owner domain)

Failing checks on exact head `da68dd48` (hosted run `42466626445`, `pull_request`):
- `PR · Native destroy retry · docker` (job `128687668677`): FAILURE, exit code 1.
- `PR · Native destroy retry · podman` (job `128687668659`): FAILURE, exit code 1.
- `PR Selected Checks` (job `128689852189`): FAILURE.

Exact failing test/log (docker job, `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry`):
- `installation_destroy_native_test.go:43` ->
  `missing deployment state for installation-retry-native/installation-retry/dev [97be702f-fadc-40bc-8657-5e07378b2daa]: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable`

This is exactly the defect PR #1464 raises: its diff adds `installCore(...)` bootstrap +
`coreBootstrapFixtureConsent(t, ctx)` to establish the authoritative installation owner before `app apply`
in that same test. The failure is a develop-build owner-state prerequisite, unrelated to the `up NAME`
alias change, and outside this lane's write-set.

#1464 status after polling (max 1 poll per 2–3 min per directive): 15+ polls across the shift,
`grep "#1464"` in develop log = 0, develop head `d30de3a4` unchanged, PR #1464 OPEN (`mergedAt=null`,
itself currently failing native CI). This is an external owner blocker; the lane cannot land #1464 or
green the native gate without it.

## Prepared handoff for successor lane (the rest, once #1464 lands)

When #1464 is merged into develop:
1. Cut/clean the PR #1459 candidate branch off the current develop head `d30de3a4` (or the new develop
   head after the #1464 merge), show the base SHA as an ancestor of the first commit, and confirm
   `git log --oneline <branch>` lists ONLY the lane's own commits.
2. Re-apply this corrected `cmd/baha/runtime_ports_test.go` to the fresh candidate (verify it still passes
   daemon-free, ~1s).
3. `gh pr ready 1459`; run the native docker + podman jobs on the exact head AND `PR Selected Checks`
   until all three are green on the exact SHA (this is the only gate that counts). A passing `go-unit-tests`
   is not a substitute for the executed native jobs.
4. Record run-ids / job names / PASS lines here; `git ls-remote` both the candidate head and baseharbor-plan
   origin/main; confirm evidence path present on origin/main before posting END.

## END

END_BLOCKED 0427-130-r3 — CLI-entry regression CORRECTED and PASS 0.89s daemon-free in isolation
(`cmd/baha/runtime_ports_test.go`, drives the real entry via `runWithIO`: `app up NAME` resolves the
registered deployment by NAME, `up NAME` + unknown NAME fail closed; runs under go-unit-tests, not routed
to native selector). Native docker+podman red on exact head `da68dd48` is PR #1464's develop-build
defect (owner domain, not this lane's write-set); #1464 NOT merged into develop after 15+ polls.
Handoff prepared above for the successor lane to finish once #1464 lands. No green-fabrication, no rerun-spam,
no `.github/**` edit, no runner/container/VM work. Cleanliness: no containers/networks/volumes/state
started by this lane remain (docker pruned; /tmp demo dirs removed). Evidence to publish to baseharbor-plan origin/main.
