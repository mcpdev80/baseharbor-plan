# w150-codex-1835-review evidence

## PLAN

1. Read the mission and applicable repository instructions; establish exact review scope.
2. Inspect candidate provenance, PR diff, checks, and independent review evidence.
3. Record findings and required evidence in the planning repo; verify exact-head state.
4. Commit and publish evidence, then report terminal status.

## Mission and scope

Mission: independent review only of mcpdev80/baseharbor PR #1835. Candidate head `55d17d437cfced7ec648aa42c14cc529963b68b6`; base `develop` at `f7540e591609e0db6453e9b690fbb5d6686448a2`. PR remains open and unmerged. No product files, workflows, CI runs, or local tests were changed or executed.

Planning repository remote witness, captured before this evidence commit:

```text
origin\thttps://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin\thttps://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Candidate diff and review

GitHub reports these exact changed paths:

- `cmd/baha/application_destroy_authorization.go`
- `cmd/baha/w287_destroy_after_failed_apply_test.go`
- `scripts/pr-gate-coverage.json`

The production change gates incomplete-inventory recovery on an unready deployment whose runtime Compose or env file is missing. The ordinary operation authorization and provider intent revalidation still happen before this fallback. The resulting plan is destructive and still passes through current-scope consent validation. No auth or consent weakening was found.

The exact-head changes resolve the two reported CLI regressions by retaining the complete plan for clean-but-missing runtime deployments, allowing stale parent acknowledgements to be rejected and child provider plans to retain Target scope. The CI trusted-plan log selected full Go scope after a conservative broad fallback because previous source/base ancestry was not proven. Hosted Go shards passed: CLI-2 job `138921722157` (481 passed, 24 intentionally skipped, 505 discovered) and CLI-3 job `138921721957` (456 passed, 17 intentionally skipped, 473 discovered). Other CLI Go shards and hosted validation jobs also completed successfully.

Exact-head check run `45529689117` completed. `PR Selected Checks`, check-run `138929655449`, concluded success from GitHub Actions integration `15368` for exact head `55d17d437cfced7ec648aa42c14cc529963b68b6`. Docker `data-capabilities` check `138922340276` passed. Native Podman coverage did not run: `Targeted HA · podman` and `PR · Native` were skipped. No separate rootless Podman qualification evidence for this behavior was found.

The new regression test's comment says a Core-owned shared SQL backend is present and preserved. However, `httpsAdoptionFixture` only writes a temporary Compose file. The test constructs a deployment record, then asserts deployment record removal and authored manifest preservation; it does not establish or inspect shared/foreign provider inventory after destroy. This does not prove the card's preservation requirement.

No exact-head failing CI result was found. The existing hosted CLI shard coverage is green, but the card's rootless Podman acceptance is unproven and the new regression does not assert shared/foreign preservation.

## Review action and verdict

Posted GitHub COMMENT review `6053834810` on exact head `55d17d437cfced7ec648aa42c14cc529963b68b6`, recording the two acceptance gaps and hosted check evidence. Review event was COMMENT only.

Verdict: not fully accepted; do not merge until shared/foreign preservation is asserted or covered by equivalent exact evidence, and valid rootless Podman evidence is attached. No merge was attempted. Merge SHA: none. Develop tip at review: `f7540e591609e0db6453e9b690fbb5d6686448a2`.

## Cleanliness

Before snapshot ran as own process PID `4108996`; `docker ps -a` output:

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

After snapshot ran as own process PID `4158483`; `docker ps -a` output:

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

No Docker/Podman project was started.

## END

END_BLOCKED w150-codex-1835-review: PR #1835 not accepted; shared/foreign preservation assertion and rootless Podman evidence missing; candidate 55d17d437cfced7ec648aa42c14cc529963b68b6.

## Origin main path witness

Exact output from `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/2026-11-25/w150-codex-1835-review/evidence.md`:

```text
From https://github.com/mcpdev80/baseharbor-plan
 * branch                main       -> FETCH_HEAD
evidence/2026-11-25/w150-codex-1835-review/evidence.md
```
