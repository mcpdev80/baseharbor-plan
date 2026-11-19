# CODEX-REVIEW — independent board-sweep cross-check

Date: 2026-11-19
Scope: read-only verification of the five stated sweep findings. This review changed no product code, task card, or PR. Product witnesses were fetched from `https://github.com/mcpdev80/baseharbor.git`; Planning was published from this separate clone after fetch/rebase of `origin/main`.

## 1. Closed cards and merge ancestry

Command:

```sh
git -C /var/tmp/codex-review-wave/baseharbor fetch origin develop
for s in 0234e9aa8 145f98b9c 8dccd4fe1; do
  printf '%s -> ' "$s"
  git -C /var/tmp/codex-review-wave/baseharbor merge-base --is-ancestor "$s" 7ee6f817dbff5a238bbc651315d6d76b3819fc91
  echo $?
done
```

Output:

```text
develop=7ee6f817dbff5a238bbc651315d6d76b3819fc91
0234e9aa8 -> 0
145f98b9c -> 0
8dccd4fe1 -> 0
```

All three supplied merge commits are ancestors of the named `develop` SHA. This independently supports the closed status for the three cards in scope.

**deckt sich**

## 2. Closed unmerged PRs and content presence

Command:

```sh
for n in 1603 1619 1610; do
  gh api "repos/mcpdev80/baseharbor/pulls/$n" --jq '{number,title,state,merged,draft,head:.head.sha,base:.base.ref,merge_commit_sha}'
done
for s in fed843492482b26572f093049a28e8bdcd19f777 fbffb965f72585b160d4fee7bcc6050287c10fc2 d57ab527524048bddc0af7bb08009edbb4d32033; do
  git -C /var/tmp/codex-review-wave/baseharbor merge-base --is-ancestor "$s" 7ee6f817dbff5a238bbc651315d6d76b3819fc91
  echo "ancestor_rc=$?"
done
```

Output:

```text
#1603 title="draft(0428-079): Perses-native messaging dashboard eligibility" state=closed merged=false draft=true head=fed843492482b26572f093049a28e8bdcd19f777 base=develop merge_commit_sha=null
#1619 title="0428-085 Perses log and trace views (consume 086/091 adapters, fail-closed)" state=closed merged=false draft=true head=fbffb965f72585b160d4fee7bcc6050287c10fc2 base=w091-0428-091 merge_commit_sha=b2515445b4cb386f6cdf68ca1b956410b4efd61f
#1610 title="0428-091 Connect Perses Tempo datasource" state=closed merged=false draft=true head=d57ab527524048bddc0af7bb08009edbb4d32033 base=lane-0428-075-perses-seam merge_commit_sha=aa69064a04c9e4cf02173986791965f9075a9997
ancestor_rc=1
ancestor_rc=1
ancestor_rc=1
```

Blob checks compared changed/scoped paths at each PR head with the named `develop` tree. For #1603, the GitHub PR-files list compared as `same=12 diff=10 missing=3`; the three missing paths in `develop` are `internal/metrics/perses_messaging.go`, `internal/metrics/perses_messaging_test.go`, and `internal/metrics/testdata/perses/rabbitmq-messaging.json`. The 10 differing blobs included `internal/capability/perses.go` and `internal/metrics/perses_contract_test.go`.

For #1619 and #1610, the PR-files API returned an empty list for #1619 and a repository-wide addition-shaped list for #1610, so I checked the task-relevant `internal/logs`, `internal/traces`, and `internal/metrics` trees directly. At #1619's head, `internal/logs/perses_log_views.go` and `internal/traces/perses_trace_views.go` are present while both are absent at `develop`. At #1610's head, `internal/metrics/perses_tempo_datasource.go` and `internal/metrics/perses_tempo_contract.go` are present while both are absent at `develop`. Scoped tree comparison found `17 diff / 28 missing / 0 same` paths for #1619 and `10 diff / 34 missing / 0 same` for #1610. Thus the relevant unmerged content is not in `develop`.

**deckt sich**

## 3. Draft status of the nine CLI2 PRs and affected card states

Command:

```sh
for n in 1578 1580 1595 1614 1620 1623 1625 1627 1591; do
  gh api "repos/mcpdev80/baseharbor/pulls/$n" --jq '"#\(.number) draft=\(.draft) title=\(.title)"'
done
```

Output:

```text
#1578 draft=true title=0428-051 uid-environment: durable non-secret env identity
#1580 draft=true title=0428-052: stable target UID (0428-052) -- DRAFT
#1595 draft=true title=0428-059: extend app sources and unique components (source model slice)
#1614 draft=true title=0428-062: unify app status + versions over the source-model read view
#1620 draft=true title=0428-067 fix(cmd/baha): per-reveal audit for `baha app creds --reveal`
#1623 draft=true title=0428-063: guided app logs/exec/urls over the status read view
#1625 draft=true title=0428-065 guided baha app export of selected local credentials
#1627 draft=true title=0428-055: baha env destroy (env-scoped identity removal)
#1591 draft=true title=0428-054 env-registry: app/target/node association on environment.json
```

The current Planning notes map these PRs to cards as follows:

```text
#1578 t-20261114-r28-cli2-uid-environment: wait
#1580 t-20261114-r28-cli2-uid-target: review
#1595 t-20261114-r28-cli2-source-model: review
#1614 t-20261114-r28-cli2-app-status: review
#1620 t-20261114-r28-cli2-wizard-platform: review
#1623 t-20261114-r28-cli2-app-interact: review
#1625 t-20261114-r28-cli2-app-export: review
#1627 t-20261114-r28-cli2-env-delete: review
#1591 t-20261114-r28-cli2-env-registry: wait
```

Draft PRs are not review candidates under §5.2. Therefore the seven cards currently in `review` cannot remain there on the strength of these PRs; they must move back to `active` only if implementation is still active, otherwise to the appropriate non-review state (normally `planned`). The two `wait` cards are not made `review` by these drafts; keep `wait` only while their recorded wait conditions remain true. This establishes the mismatch, while the exact next status for each of the seven depends on whether its work is still active.

**deckt sich**

## 4. #1615 trigger coverage and exact-head run

Command:

```sh
gh api repos/mcpdev80/baseharbor/pulls/1615 --jq '{draft,mergeable,mergeable_state,head:.head.sha,base:.base.ref,base_sha:.base.sha}'
git -C /var/tmp/codex-review-wave/baseharbor show 7ee6f817dbff5a238bbc651315d6d76b3819fc91:.github/workflows/ci.yml | nl -ba | sed -n '12,19p'
gh run list --repo mcpdev80/baseharbor --commit f93564a0d707983bfe6a8b59375c1c1c914d7827 --json databaseId,status,conclusion,name,event,headSha --limit 100
gh api repos/mcpdev80/baseharbor/commits/f93564a0d707983bfe6a8b59375c1c1c914d7827/check-runs --jq '.check_runs[] | [.name,.status,.conclusion,.head_sha] | @tsv'
```

Output:

```text
{"draft":false,"mergeable":true,"mergeable_state":"clean","head":"f93564a0d707983bfe6a8b59375c1c1c914d7827","base":"cli2-env-policy-head","base_sha":"5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3"}
 12  pull_request:
 13    types: [opened, synchronize, reopened, ready_for_review, converted_to_draft]
 14    branches:
 15      - develop
 16      - main
 17      # Stacked development PRs target a lane-* branch and receive the same PR CI.
 18      - 'lane-*'
gh run list output: []
check-runs output: []
```

The base branch is `cli2-env-policy-head`, not `develop`, `main`, or `lane-*`. The stated `pull_request.branches` filter excludes this base. The PR is non-draft and GitHub reports `mergeable=true`, `mergeable_state=clean`, but neither the Actions run query nor the commit check-runs endpoint shows a run/check on the exact head SHA.

**deckt sich**

## 5. #1616 merge and content on current develop

Command:

```sh
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-086-perses-loki-source
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1616/head
gh api repos/mcpdev80/baseharbor/pulls/1616 --jq '{state,merged,merged_at,head:.head.sha,merge_commit_sha}'
git -C /var/tmp/codex-review-wave/baseharbor merge-base --is-ancestor c296086ca1e35ef3212d293afc94d7bebcd1690f 7ee6f817dbff5a238bbc651315d6d76b3819fc91; echo $?
```

Output:

```text
(branch query returned no line)
7042ee612430b472ba16cdaffbec0684e78686f6 refs/pull/1616/head
{"state":"closed","merged":true,"merged_at":"2026-11-19T16:53:19Z","head":"7042ee612430b472ba16cdaffbec0684e78686f6","merge_commit_sha":"c296086ca1e35ef3212d293afc94d7bebcd1690f"}
0
```

Blob IDs at PR head and `develop`:

```text
internal/logs/loki_datasource.go | 952b86e1ebc15dca13574acc0f59f1c2d88e3d7f | 952b86e1ebc15dca13574acc0f59f1c2d88e3d7f | SAME
internal/logs/loki_test.go | ce86670b42151f2c96117ae763688085a506bdb7 | ce86670b42151f2c96117ae763688085a506bdb7 | SAME
internal/logs/runtime_log_source_snapshot.go | 94fb565797a44f4cd75045537c83befd1bef6bc9 | 94fb565797a44f4cd75045537c83befd1bef6bc9 | SAME
internal/logs/testdata/perses-loki-datasource/loki.json | 2da53f1bf69a75eeb84d47480f6c4ed0e22e9ec8 | 2da53f1bf69a75eeb84d47480f6c4ed0e22e9ec8 | SAME
```

The source branch is absent, the pull ref preserves the head, the merge commit is an ancestor of current `develop`, and all four requested blobs match. The `accepted` conclusion for this merge holds on these requested witnesses.

**deckt sich**
