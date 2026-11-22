ROLLE: CODEX-MERGE

## PLAN

1. Verify exact PR head/base, clean merge state, review evidence, run and authorization.
2. Merge PR #1714 once without force or protection bypass, only if all prechecks pass.
3. Verify and record the resulting develop SHA and merge commit.
4. Publish this merge evidence to baseharbor-plan origin/main and verify its remote path.
5. Post the coordinator END with the merge result and four prechecks.

Session marker: 1450c201

## Four prechecks

1. PASS. Before merge, `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1714/head` returned develop `1ff16925c4e141d732459a34ddf0b7f49128a214` and PR head `67495fde96837846d9d2b26e8db5ad93b7b7c988`. PR #1714 was OPEN, not draft, `mergeStateStatus=CLEAN`, and mergeable.
2. PASS. The exact-head review artifact is present on plan `origin/main` at `evidence/r28-welle5-2026-11-22/perses-valkey-gate-0428-183/review-1714-head67495fde968.md`; GitHub content SHA `142e111e48322f1d83aba7171646738a6f5eb81b` and its literal verdict is `VERDICT: APPROVE` for the exact candidate.
3. PASS. Exact-head run `44989324573` completed SUCCESS with zero failed jobs. Required `PR Selected Checks` job `137107855881` passed from Actions integration `15368`. `PR · Go unit · packages` job `137106741719` passed and its log includes `ok github.com/mcpdev80/baseharbor/internal/metrics 0.490s`; the Valkey regression and the three named unchanged tests ran in that package suite. There is no separate job named `internal/metrics-shard` in this run; internal/metrics was executed by the packages shard.
4. PASS. `/home/marcel/.config/baseharbor-coordinator/COST_CONTROL.md` mtime was `2026-11-22 06:35:23 +0100`; its owner clarification resumes this bounded PR sweep and authorizes qualified merges. The historical cost stop did not block this merge. The authority file was not edited.

## Live merge requirements

The live ruleset query showed `develop - integration branch` ruleset `23754541` disabled and `develop - required checks` ruleset `25223521` active, requiring `PR Selected Checks` from integration `15368`. That required check passed. No protection bypass was used. The merge used squash, matching the repository’s configured merge method.

## Merge result

`gh pr merge 1714 --repo mcpdev80/baseharbor --squash --match-head-commit 67495fde96837846d9d2b26e8db5ad93b7b7c988` completed successfully, guarded by the exact expected head.

GitHub reports PR #1714 MERGED at `2026-11-22T05:40:26Z`, merge commit `5ca8420c1814f25bea6404e55fd054c60746eae5`. Post-merge `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1714/head` returned:

    5ca8420c1814f25bea6404e55fd054c60746eae5 refs/heads/develop
    67495fde96837846d9d2b26e8db5ad93b7b7c988 refs/pull/1714/head

## Repo-rule compliance

One authorized merge only. No force, protection bypass, local test, product edit, workflow dispatch, PR comment, or subagent.

## Cleanliness

Before merge evidence publication: PID `2498165`; `docker ps -a` returned no containers. No containers or compose projects were started.

## END codex-rev2-1736 DONE

MERGED PR #1714 at candidate `67495fde96837846d9d2b26e8db5ad93b7b7c988`; new develop SHA and squash merge commit are both `5ca8420c1814f25bea6404e55fd054c60746eae5`. All four prechecks passed.

First evidence push witness from `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`:

    1cad97946bf194bb3500692d62ed8d349945acba refs/heads/main

Required fetched `origin/main` tree witness from `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 'review-17'`:

    evidence/r28-welle5-2026-11-22/ci-cells-shells/review-1754-head0975e671.md
    evidence/r28-welle5-2026-11-22/ci-cells-shells/review-1754-headacd8dd95.md
    evidence/r28-welle5-2026-11-22/coreless-validation/review-1736-head4c919fd6.md
    evidence/r28-welle5-2026-11-22/coreless-validation/review-1736-headfa527b439.md
    evidence/r28-welle5-2026-11-22/footprint-gate-admission/review-1753-head91f4e38795a.md
    evidence/r28-welle5-2026-11-22/footprint-gate-admission/review-1753-pending.md
    evidence/r28-welle5-2026-11-22/gate-admission-census/review-1756-head6cec31ff673.md
    evidence/r28-welle5-2026-11-22/oras-0428-229/review-1754-headacd8dd95.md
    evidence/r28-welle5-2026-11-22/perses-valkey-gate-0428-183/review-1714-head67495fde968.md
    evidence/r28-welle5-2026-11-22/perses-valkey-gate-0428-183/review-1714-headfc525970d41.md
    evidence/r28-welle5-2026-11-22/sourcepull-0428-061/review-1752-head719242df.md
    evidence/r28-welle5-2026-11-22/sourcepull-0428-061/review-1752-head7b3c6588.md
    evidence/r28-welle5-2026-11-22/sourcepull-0428-061/review-1752-head9140e0c8.md
    evidence/r28-welle5-2026-11-22/sourcepull-0428-061/review-1752-heada4adc29a.md
    evidence/r28-welle5-2026-11-22/sourcepull-0428-061/review-1752-heade7df5ab4.md
    evidence/r28-welle5-2026-11-22/testcontext-0428-223/review-1750-head17f471cd3fe.md
    evidence/r28-welle5-2026-11-22/testcontext-0428-223/review-1750-head5d47569f337.md
    evidence/r28-welle5-2026-11-22/valkey-gate-0428-183/review-1714-head277ff976395a.md
    evidence/r28-welle5-2026-11-22/workload-port-0428-199/review-1752-head34feb493480-contract061.md
    evidence/r28-welle5-2026-11-22/workload-port-0428-199/review-1752-head34feb493480.md
