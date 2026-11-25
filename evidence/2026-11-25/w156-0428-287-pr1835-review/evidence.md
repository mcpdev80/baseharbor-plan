# w156-0428-287-pr1835-review evidence

## PLAN

1. Refresh PR #1835 head, develop base, and current gate batch state.
2. Compare head commit author name with the owning lane on card 0428-287.
3. Record findings and blocked status in baseharbor-plan evidence.
4. Publish the evidence and post terminal coordinator status.

## Exact-head and owner identity

PR #1835 is open and unmerged at head `55d17d437cfced7ec648aa42c14cc529963b68b6`; its base is `develop` at `f7540e591609e0db6453e9b690fbb5d6686448a2`, also the current `develop` ref observed during this pass. The card `t-20261116-r28-bug-installation-reset-recovery` lists owning lane `w105-0428-279-audit`.

GitHub commit metadata for the exact head reports `.commit.author.name = w105` (`w105@baseharbor.local`). This does not equal the card owning lane `w105-0428-279-audit`. The identity check fails. No author metadata was changed.

## Native gate batch state

The previous PR CI run `45529689117` has exact-head `PR Selected Checks` success from GitHub Actions integration `15368`, but this does not satisfy the separately required native Docker and rootless Podman gates.

- Run `45571397690` is `workflow_dispatch`, completed/cancelled, with zero jobs. It is void and provides no gate evidence.
- Replacement run `45572854473` is also `workflow_dispatch` on the exact head and completed/cancelled. The run requested `ONLY_GATES: atomic/docker/guided,atomic/docker/lifecycle`; no Podman batch was run.
- The run's `Pre-Release Checks` check failed. Its log includes `AssertionError: source checks failed`. `Source · Qualified` logged `Source qualification did not pass: cancelled`. The Docker/Podman runtime result aggregators failed or cancelled, and no per-gate `Run runtime gate` evidence was produced.
- The batch-runner status file in the shared planning checkout records that run `45572854473` was stopped on owner direction before runtime jobs were created and holds further batches for a corrected exact head. This session did not modify that status file, dispatch, or rerun any workflow.

No native Docker or rootless Podman gate batch has terminal per-gate execution evidence qualifying this candidate. Merge remains withheld.

## Registration and scope

Registered this fresh decider pass in `workers/todos/w156-0428-287-pr1835-review.json`. The batch-runner lane `w136-pr1836-rowsreview` already has the Docker/Podman batch duty; this session did not duplicate its registration or contact it directly.

No product files were edited, no tests were run locally, no GitHub workflow was dispatched or rerun, and no merge was attempted. The earlier COMMENT review on #1835 remains the review event; this pass records updated identity and batch state for the coordinator.

Planning repository remote witness before evidence commit:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Cleanliness

Before snapshot ran as own process PID `164741`; `docker ps -a` output:

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

No Docker or Podman project was started.

After snapshot ran as own process PID `170497`; `docker ps -a` output:

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

## END

END_BLOCKED w156-0428-287-pr1835-review: merge withheld; head author `w105` mismatches card owner `w105-0428-279-audit`, and preservation assertion plus Podman proof are required on the new w157 head; current PR head 55d17d437cfced7ec648aa42c14cc529963b68b6.

## Origin main path witness

Exact output from `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/2026-11-25/w156-0428-287-pr1835-review/evidence.md`:

```text
From https://github.com/mcpdev80/baseharbor-plan
 * branch                main       -> FETCH_HEAD
evidence/2026-11-25/w156-0428-287-pr1835-review/evidence.md
```

## Owner precision recheck

Authenticated GitHub account via `gh api user --jq '.login'`: `mcpdev80`. The requested exact field query `gh api repos/mcpdev80/baseharbor/commits/55d17d437cfced7ec648aa42c14cc529963b68b6 --jq '.commit.author.name'` returned:

```text
w105
```

The card owner lane is still `w105-0428-279-audit`. The equality check compares `.commit.author.name` to that card-owner lane, and remains false. GitHub uploader `.author.login` was not used for the identity decision.

The refreshed PR is still open and unmerged at `55d17d437cfced7ec648aa42c14cc529963b68b6`; the w157 correction is not yet the PR head. The substantive acceptance hold remains the preservation assertion and Podman runtime proof on the new w157 head. Existing cancelled/void gate runs on `55d17d43` do not qualify that future head.
