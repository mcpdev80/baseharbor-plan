# w156-0428-287-pr1835-review evidence

## PLAN

1. Refresh PR #1835 head, develop base, and current gate batch state.
2. Compare head commit author name with the owning lane on card 0428-287.
3. Record findings and blocked status in baseharbor-plan evidence.
4. Publish the evidence and post terminal coordinator status.
5. Hand off the future w158 identity recheck and w157 substantive gate review to the successor flow; preserve the hold.

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

END_BLOCKED w156-0428-287-pr1835-review: identity mismatch confirmed by exact Git author field; await w158 corrected audit for frontmatter re-check, and preserve the substantive new-head gates; PR head 55d17d437cfced7ec648aa42c14cc529963b68b6.

## Origin main path witness

Exact output from `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/2026-11-25/w156-0428-287-pr1835-review/evidence.md`:

```text
From https://github.com/mcpdev80/baseharbor-plan
 * branch                main       -> FETCH_HEAD
evidence/2026-11-25/w156-0428-287-pr1835-review/evidence.md
```

Exact output from the path check after the fresh frontmatter identity recheck (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/2026-11-25/w156-0428-287-pr1835-review/evidence.md`):

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

Exact output from the post-precision-publication path check (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/2026-11-25/w156-0428-287-pr1835-review/evidence.md`):

```text
From https://github.com/mcpdev80/baseharbor-plan
 * branch                main       -> FETCH_HEAD
evidence/2026-11-25/w156-0428-287-pr1835-review/evidence.md
```

## Owner policy update

Owner policy confirms the identity criterion is exact equality between `.commit.author.name` and the card-owner lane. The `gh api` value `w105` differs from frontmatter owner `w105-0428-279-audit`; the identity hold remains valid. The invalid #1835 OK audit line is routed for correction to fresh lane w158 (`8fcb8357`). Preserve this hold until that corrected audit lands, then re-check the exact author field against the card frontmatter.

The substantive hold also remains: the corrected preservation assertion and Podman proof must apply to the new w157 head. No new head or corrected audit was reviewed in this update.

Owner policy reminder: exact Git author-name equality must be used at every merge decision. The owner reports live PR #1839 has head author `w124` despite a `w153` branch; that case reinforces checking `.commit.author.name` against the card frontmatter lane rather than inferring identity from branch or uploader.

## Fresh frontmatter identity recheck

The current remote card file `tasks/t-20261116-r28-bug-installation-reset-recovery.md` has frontmatter `owner: w105-0428-279-audit`. Fresh `gh api` reads authenticated as `mcpdev80`, report PR #1835 head `55d17d437cfced7ec648aa42c14cc529963b68b6`, and return `.commit.author.name = w105` for that exact head. Exact equality is false; the identity hold is preserved. This comparison uses the card frontmatter owner, not a summary or GitHub uploader login.

Exact output from the post-policy-update path check (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/2026-11-25/w156-0428-287-pr1835-review/evidence.md`):

```text
From https://github.com/mcpdev80/baseharbor-plan
 * branch                main       -> FETCH_HEAD
evidence/2026-11-25/w156-0428-287-pr1835-review/evidence.md
```

## Lane succession and closeout

Owner confirms w156's #1835 review duty is succeeded by the w136/w182 flow. The recorded verdict remains blocked: identity exact-match failed, and preservation plus Podman evidence remain required on the new w157 head. The successor flow owns any later recheck against the card frontmatter and new-head gate evidence. This closes w156's duty only; it does not accept or merge #1835.

END_DONE w156-0428-287-pr1835-review: review verdict and blocker evidence published; follow-up handed to w136/w182; PR #1835 remains blocked pending corrected identity audit and substantive gates.
