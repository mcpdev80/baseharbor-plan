# H-V25 — duplicate-and-superseded desk · round-1

Mission (from `/var/tmp/m229.txt`): for **every** open PR in `mcpdev80/baseharbor` determine
(a) whether it content-wise contains another open PR (duplicate),
(b) whether it is superseded by another PR (its files already there, `git cherry` / patch-id),
or (c) whether it sits on a stale base branch that has long since merged into develop (base-ref wrong).
Pure finding only. No product change, no PR close, no matrix. Decision on close/supersede stays with Owner.

## lane identity / branch provenance

- Product repo checked: `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor`
- `git -C baseharbor remote -v` → `origin  git@github.com:mcpdev80/baseharbor.git (fetch/push)` — real GitHub remote.
- Planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, `origin → https://github.com/mcpdev80/baseharbor-plan.git`.
- develop head (verified `git ls-remote` reachable via origin): `40cb28c758b02960356434b630086a341ebe1738`.
- This lane starts nothing, touches no product files, closes nothing. No containers, no compose, no runners.

## method (1)

1. `gh pr list --repo mcpdev80/baseharbor --state open --limit 60 --json number,title,headRefName,baseRefName,isDraft,headRefOid` → 30 entries (full open set).
2. `git fetch origin "+refs/pull/*/head:refs/remotes/origin/pr/*"` (PR heads) + `git fetch origin develop`.
3. per PR: file list = `gh pr view N --json files`; patch-id = `gh pr diff N | git patch-id --stable` (matches the mission's `git diff <base>...pr/N` intent; `gh pr diff` uses the PR's recorded base).
4. per PR: `git merge-base --is-ancestor origin/develop origin/pr/N` → `NO` = base older than develop.
5. file-set overlaps and subset/containment computed in `workers/.models/laptop/overlap.py` from a per-PR file TSV.

## tabelle (PR | dateien | patch-id | base-ancestor? | befund)

Legend: `dev-ancest` = "is origin/develop an ancestor of the PR head?" — `YES` means the PR already incorporates develop; `NO` means the PR head does not contain develop (stale base / pre-#1594 work).

| PR | base | #files | stable patch-id (sha1) | dev-ancest | befund |
|---|---|---|---|---|---|
| 1734 | develop | 1 | d00847f19fd8c59a292c3e687962e33686f0beb2 | YES | dev-synced; touches `internal/logs/loki_test.go` — see 1732 (same file, DIFFERENT patch → not a dup) |
| 1733 | develop | 2 | ddb427a22e4073d41d5b234cbba9c3e343ac29cb | YES | dev-synced; `perses_management_ui.{go,test}` |
| 1732 | develop | 1 | c5161717889b4b733009d992aa5b386763db96af | YES | dev-synced; `internal/logs/loki_test.go` — same file as 1734 but a completely different change (mTLS client keypair fixture). **NOT a duplicate of 1734.** |
| 1731 | develop | 2 | 4c727b074673362d9e6c2195851a92333ecea791 | YES | dev-synced; `cmd/baha/context_terminal_test.go` + `.github/workflows/ci.yml`. Still **open** (mergedAt null) though 1731's own test files are also carried in the large 1615 batch. Not a dup: different intent, distinct patch-id, and `.github` change is Owner scope. |
| 1730 | lane-0428-143-verify-none | 2 | 18fa4c09664f720efa522050fc63420fa3719337 | YES | **STACKED, not dup/supersede.** Body: "STACK: base #1729 (0428-143, head 809a8196e1cf)". `origin/pr/1729` IS an ancestor of `origin/pr/1730` (`git merge-base --is-ancestor`). 1730's 2 files are a subset of 1729's 3 files by construction — 0428-203 is the intended follow-up on 0428-143. |
| 1729 | develop | 3 | 833cfb88d8739ec5e545b69b7efa50296c1c30b4 | YES | dev-synced base of 1730. `internal/capability/integration_contract.go`, `prometheus_verify.go`, `prometheus_verify_workload_only_test.go` |
| 1728 | develop | 5 | c0253bdb2b1a93838870989efdd0d27b5a2cb81e | YES | dev-synced; 0428-200 deployment-version-mismatch |
| 1726 | develop | 9 | 2348eaf17cfb2ad4bc2d74af94d4eca4a76035ed | YES | dev-synced; CLI operator-identity + shared-runtime fixtures |
| 1725 | develop | 3 | 484c197e72d6e07d392c010e638798768b1d3299 | YES | dev-synced; 0428-201 shared backend state version |
| 1724 | develop | 8 | c66d6c609031bd05811235fd62fc7e964434ed10 | YES | dev-synced; 0428-177 perses runtime regression |
| 1723 | develop | 4 | 7c7d284f976f5a7880b76e72de5dda63482787fc | YES | dev-synced; 0428-199 `--workload-port` |
| 1718 | develop | 1 | 293adca6963e34e0a5a4388bd854a40f64d8cf7b | YES | dev-synced; `cmd/baha/context_terminal_test.go` — shares this file with 1731 (see 1731) |
| 1714 | develop | 4 | 66705526966a78185e30497be5b9a587c43ef0b6 | **NO** | **STALE (c).** merge-base `f5ce95afce1cfec053dd7717ed05e89bfe153535`; develop is 24 commits ahead. Perses valkey dashboards. |
| 1704 | develop | 2 | d8287c699ec14b82c004fed5fd2ac5cddc71b881 | **NO** | **STALE (c).** merge-base `28fb427f057499efca705c1b7459e7653bd532a8`; develop 142 commits ahead. 0428-073 r28 Perses alerts. |
| 1702 | develop | 13 | 90481538b284700fe7e51c5db296649e3db18dd2 | **NO** | **STALE (c).** merge-base `28fb427f057499efca705c1b7459e7653bd532a8`; develop 142 commits ahead. 0428-142 perses status-witness. |
| 1684 | perses-tmpfs-mountpoint-wt | 18 | defddd65031202bb8ac71eb9992154d428190d97 | YES | dev-synced (develop is ancestor). Base branch is a scratch WT (`perses-tmpfs-mountpoint-wt`), not develop — a stack base. See note: 1684 shares `perses_runtime.go`+`runtime_postgres.go` with 1724. |
| 1665 | lane-0428-083-datasources-r2 | 14 | eb88410e6d98059b630aa87c5ade27d848e02a1e | YES | dev-synced; stacked base `lane-0428-083-datasources-r2` (0428-082 perses dashboard). |
| 1650 | develop | 6 | 6ee094fd41dd31bef4147a88cb05c91f1f53a73f | YES | dev-synced; 0428-078 Perses identity-keycloak resolver |
| 1645 | develop | 35 | 1f3b3b8042330b8704e12998bbace9660bb34a61 | **NO** | **STALE (c).** merge-base `96f2ae11a25a508998c44a9854ef17f8fa15c112`; develop 25 commits ahead. 0428-091 r28 rename .go→.go.txt witnesses. |
| 1627 | develop | 9 | 42e63d293406d293469fabe112536701c2f23f87 | **NO** | **STALE (c), draft.** merge-base `5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3`; develop 311 commits ahead. 0428-055 env destroy. |
| 1625 | cli2-identity-secrets-head | 8 | 0fc06eddc191e19c93711ac588b89035674c8f3f | **NO** | **STALE (c), draft.** base is `cli2-identity-secrets-head` (a stack base). merge-base `ae2d022c8dc92c012cd0ed9d5eb2aefa7d5f6101`; develop 317 commits ahead. 0428-065 app export. |
| 1623 | cli2-identity-secrets-head | 20 | a41014d936191e2e104e42807bd49f9748fba2b3 | **NO** | **STALE (c), draft.** base `cli2-identity-secrets-head`. merge-base `ae2d022c8dc92c012cd0ed9d5eb2aefa7d5f6101`; develop 317 ahead. 0428-063 app interact. |
| 1620 | develop | 2 | e4b957da0d1c4e536c0844e79dfa7c1468a4fa6a | **NO** | **STALE (c), draft.** merge-base `5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3`; develop 311 ahead. 0428-067 creds audit. |
| 1615 | develop | 100 | a16d888e11601784a7a10273e51059caffddae95 | YES | dev-synced; huge 0428-057 reveal batch (base = develop). Shares `machine_coverage.go` etc. with the cli2 stack (1623/1625/1627) — see overlap note. |
| 1614 | develop | 55 | acae96a8de8cbbfe37b321e7a876624b65e1edf9 | **NO** | **STALE (c), draft.** merge-base `ae0602e02882619dea151dc82d62b98b72481566`; develop 319 ahead. 0428-062 app-status unification. |
| 1597 | develop | 13 | 77005dcdf72601b0f352d0060bfb74bac490ee95 | YES | dev-synced; 0428-078 perses dashboards (carries `app_status_result.go`, `app_perses_cli_test.go` — see overlap note) |
| 1596 | develop | 4 | 5b55fd4a4a432ea84f6dbf32b15b4a25b09cce6b | **NO** | **STALE (c).** merge-base `4d14741ee9485b7e0c346fa873ed59f637e71b68`; develop 316 ahead. 0428 org-env reconcile. |
| 1588 | develop | 7 | 7f1a412b48f605ade776043dc476d09e3dbf13c2 | **NO** | **STALE (c), draft.** merge-base `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`; develop 562 ahead. 0427-186 target policy presets. |
| 1587 | develop | 9 | 8202a280cb8f9a9d555f253c1b790a343ce3a67c | **NO** | **STALE (c), draft.** merge-base `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`; develop 562 ahead. r28 operator-API runbook. |
| 1585 | develop | 6 | e6176c83caee15a139fac044e523f1a95315f223 | YES | dev-synced; 0428 fix-bf01 target selection |

## counts (3)

- Open PRs analysed: **30**
- `dev-ancest = YES` (PR already incorporates develop, base not stale): **18** → 1734, 1733, 1732, 1731, 1730, 1729, 1728, 1726, 1725, 1724, 1723, 1718, 1684, 1665, 1650, 1615, 1597, 1585
- `dev-ancest = NO` (base older than develop → **stale**, case (c)): **12** → 1714, 1704, 1702, 1645, 1627, 1625, 1623, 1620, 1614, 1596, 1588, 1587
  - Of those 12, drafts: 1627, 1625, 1623, 1620, 1614, 1588, 1587 (7 drafts); non-drafts: 1714, 1704, 1702, 1645, 1596 (5).
  - Base branch is a non-develop stack base for: 1625, 1623 (both `cli2-identity-secrets-head`).

## duplicate / superseded analysis (2)

**No duplicate found.** Two PRs share the identical patch-id only if the diff is byte-identical. All 30 PRs have a **distinct** stable patch-id (see `workers/.models/laptop/pids.sh` output reproduced below). Two PRs share an *identical file-set* (`1732 == 1734`, both only `internal/logs/loki_test.go`) — this is a same-path coincidence, not a duplicate: the two diffs are unrelated (`1732` adds an mTLS client keypair fixture; `1734` rewrites the fail-closed probe witness with two subtests). Confirmed: different patch-ids, divergent change content.

**No supersession found.** No PR's complete change-set is already contained in another open PR. The only subset relation is `1730 ⊂ 1729` (2 of 1730's files ⊂ 1729's 3 files) — but this is the documented stack (1730's body says "STACK: base #1729"; `origin/pr/1729` is a real ancestor of `origin/pr/1730`). It is an intended dependent PR, not a superseded one.

Overlap evidence (pairs sharing ≥1 file, ≥2 files):

| pair | shared files | read |
|---|---|---|
| 1729 & 1730 | `integration_contract.go`, `prometheus_verify_workload_only_test.go` | 1730 stacked on 1729 (0428-203 on 0428-143) — intended, not dup/supersede |
| 1732 & 1734 | `internal/logs/loki_test.go` | same path, unrelated content — not a dup |

Single-file coincidences (ignored, same file touched by different unrelated PRs): 1718/1731 (`context_terminal_test.go`), 1597/1650/1702/1614/1615 (`app_status_result.go`), 1588/1623/1625/1627/1614 (`machine_coverage.go`), etc. These are normal overlaps across a busy trunk, not duplicate or supersession.

## vorschlaege (ENTSCHEIDUNG IMBEI BEHIR — this akte closes/supersedes NOTHING)

Recommendation only; the Owner decides.

1. **Case (c) — stale base, the dominant finding (12 PRs).** All 12 are built on a base that no longer reflects develop. For non-draft PRs (1714, 1704, 1702, 1645, 1596) the actionable fix is a **retarget/rebase onto the current develop** (or the correct card base per `depends_on`) — a maintainer/owner action, not a worker write. For the 7 drafts (1627, 1625, 1623, 1620, 1614, 1588, 1587) the usual move is to leave for the owner to rebase or close as stale; drafts rarely block a release.
2. **Base is a non-develop stack for 1625, 1623** (`cli2-identity-secrets-head`): the correct base-ref per `depends_on` would be that lane's head, not develop. `gh pr view`/baseharbor-plan card `prs:` field is the source of truth; I did not edit cards.
3. **No duplicate / no supersede** to act on. No close, no supersede booking.
4. **1731 carries a `.github/workflows/ci.yml` change** (Owner scope) — reported here as STATE; the Owner edits `.github/**`. Do not rerun via this lane.

## repo-rule compliance

- Pure finding: **no** product file written, no `gh pr close`/`gh pr edit`, no retarget, no comment on any PR, **no** edit to baseharbor-plan cards, **no** `.github/**` edit, **no** workflow_dispatch, **no** runner/build/VM.
- No subagents/agents spawned (4.8). Every step run inside this session.
- Only the real GitHub remote `origin (git@github.com:mcpdev80/baseharbor.git)` touched; no `lane-origin`, no local-fs remote.
- No containers/compose started (cleanliness: none).
- Evidence written only into the planning repo (`baseharbor-plan`), never into the product repo.

## cleanliness

- Started nothing: no containers, no compose projects, no runners, no VMs.
- Scratch under `/tmp/opencode/w229-*` (TSV, pids, overlap script) — ephemeral, not committed.
- Working helper scripts in `workers/.models/laptop/` (`analyze-pr.sh`, `pids.sh`, `collect-files.sh`, `overlap.py`) — not committed to any product repo; not part of the planning evidence (only the akte below is).
- No orphaned state to bring down.

## evidence path (to be verified on origin/main before END)

`evidence/bug-hunt-2026-11-21/duplicate-superseded-desk/round-1.md` in `baseharbor-plan` (origin → https://github.com/mcpdev80/baseharbor-plan.git)

## END

END w229-0428-204-huntdup DONE — finding delivered, no action taken, decision with Owner.
