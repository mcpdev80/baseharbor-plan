# 0428-221 red-eleven-desk hunt-1: what every open failing PR is missing

- Lane: `0428-221-huntred` (this session, `d1317318`)
- Task card: `0428-221` (BUG-HUNT, pure classification, no product change, no commit to baseharbor)
- Mission: `coordinator/missions/H-V38-red-eleven.md`
- Role: Worker, read-only. No product file changed, no commit to baseharbor, no PR action, no subagents, no bare `go test ./cmd/baha/`, no `git add -A`, no `git stash`.
- Evidence repo (remote -v verified BEFORE first evidence commit):
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)` (ONLY repo with github.com/mcpdev80)
- Evidence path (before END must be present on origin/main):
  `evidence/r28-welle4-2026-11-21/red-eleven-desk/hunt-1.md`
- Anchor: baseharbor develop `77c1e60f51b91003ac3ddc391008c15e4a713a5c` (witnessed via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`)

## PLAN (nummeriert, vor der ersten Aktion)

- Verify gh auth + evidence dir + baseharbor-plan remote is the ONLY github.com/mcpdev80 remote.
- Enumerate all open PRs (gh pr list --state open), then `gh pr checks <n>` for each; keep PRs with a `fail` line.
- For each failing PR record failing job name + job id; capture the three `gh run view` byte-sizes.
- Count distinct first-level `--- FAIL: Test` names per PR (strip subtests); list names, not sums.
- Ancestry axis: `merge-base --is-ancestor develop head` via the compare API; record behind-by size.
- Cross-check failing names against `evidence/r28-welle4-2026-11-21/*` for class (c) other-card.
- Write this table + cleanliness + repo-rule compliance.
- Push evidence to origin/main, verify path present, post END line.

## 1) Quantity: open PRs and which have a fail line

- Open PRs total: 26 (witnessed via `gh pr list --repo mcpdev80/baseharbor --state open --json number,title,headRefName`).
- PRs with at least one `fail` line in `gh pr checks <n>`: 7.
- PRs with NO fail (green, pending, or skipped): 1746 (skipping), 1745 (pass), 1742 (pass), 1741 (pass), 1740 (pass), 1739 (pass), 1738 (pass), 1737 (pass), 1736 (pass), 1725 (pending, not fail), 1627 (fail only on `Draft Go *` shard = pre-merge draft, not selected; `PR Selected Checks` = skipping), 1625 (no checks reported), 1623 (no checks reported), 1614 (pass/draft pass), 1588 (pass), 1585 (pass).
- Fail-line PRs analyzed below: 1596, 1597, 1620, 1645, 1650, 1665, 1723.

## 2) Failing job name + job id per PR (from `gh pr checks`)

- PR 1596 (0428-056 org-env reconciliation; head 6135e73a6e2c36e09637856412b94133b3743119):
  - `PR Selected Checks` job 136671011448 (run 44847161507)
  - `PR · Go unit · cli-0` job 136669672861, `cli-1` 136669672827, `cli-2` 136669672771, `cli-3` 136669672839, `packages` 136669672780
- PR 1597 (0428-076 perses db dashboards; head 90063f6ec66cf6d249181d803293f50064c44b8d):
  - `PR Selected Checks` job 136555658338 (run 44812791612)
  - `Draft Go` 136549693831/136549693806/136549693603/136549693598/136549694266; `Go unit` 136553627940/136553627999/136553628023/136553627991/136553627904
- PR 1620 (0428-067 per-reveal creds audit; head 28cb907dc0a678d1b5326df5203741c70cf84978):
  - `PR Selected Checks` job 136677834103 (run 44849270489)
  - `Go unit` cli-0 136676566364, cli-1 136676566433, cli-2 136676566418, cli-3 136676566440, packages 136676566379
- PR 1645 (perses/tempo .go->.go.txt rename; head 4d73aa97808d000d2f70eaa193f8dbfc14e817a7):
  - `PR Selected Checks` job 136562618719 (run 44814746593)
  - `Go unit` cli-0 136560143562, cli-1 136560143577, cli-2 136560143358, cli-3 136560143510, packages 136560143717
- PR 1650 (0428-078 wire perses identity-keycloak; head 28c18f02039f0957544146cf5d0db2a1561a4220):
  - `PR Selected Checks` job 136667750659 (run 44846209015)
  - `Go unit` cli-0 136666536022, cli-1 136666535981, cli-2 136666535996, cli-3 136666536069, packages 136666535997
  - `Selected Runtime (atomic/docker/identity)` docker·identity job 136666960147 (native, gated)
- PR 1665 (0428-082 native perses dashboard; head e84e434bc1b49ce43a1c48041312242c8a56a981):
  - main run 44867225115: `Go unit` cli-0 136733616159, cli-1 136733616117, cli-2 136733616216, cli-3 136733616219, owner 136733616169, packages 136733616174; `Native Keycloak/Core` docker 136733615993, podman 136733616062; `Runner Interface` 136733615999; `Validation` go-build 136733616083, cli-gofmt 136733616088, go-vet 136733616051, authority-package-tests 136733616089; `Focused Python` 136733615977; `Exact Candidate` 136733616020; `Native · native/docker/perses-runtime-smoke` 136733590613 (compile-timeout); `Native · native/podman/installation-destroy` 136580960436 (real test fail)
  - draft run 44820054935: `Draft Go` cli-0 136578314124, cli-1 136578314208, cli-2 136578314247, cli-3 136578313975, packages 136578314108
- PR 1723 (0428-199 --workload-port; head 26755fc1edfbde534986b501197a92f38842a0c1):
  - `PR Selected Checks` job 136472605316 (run 44788134959)
  - `Go unit` cli-0 136469561450, cli-1 136469561462, cli-2 136469561471, cli-3 136469561524, packages 136469561792
  - `Selected Runtime (atomic/docker/data-capabilities)` docker·data-capabilities 136470779149; `guided` 136470779213

## 3) Byte sizes of the three required paths (per mission step 2)

- The three mandated read paths are all ZERO bytes on every failing PR. This is the known "run log is not a valid zip" failure: `gh run view --job <id> --log`, `gh run view <run> --log-failed`, and `gh run view <run> --log` each return 0 bytes (exit 0), e.g. for PR 1596 run 44847161507:
  - A `--job 136671011448 --log`: 0 bytes
  - B `--log-failed` (run 44847161507): 0 bytes
  - C `--log` (run 44847161507): 0 bytes
- The aggregate-log path drops entire jobs; `--log` can deliver `failed to get run log: zip: not a valid zip file`. Byte counts below are recorded per job via the authenticated logs endpoint `GET /repos/mcpdev80/baseharbor/actions/jobs/{id}/logs` (curl, `Authorization: Bearer <gh token>`), which returns the raw per-job text log. Representative sizes (bytes):
  - PR 1596 cli-0: 97871; cli-1: 66914; cli-2: 63846; cli-3: 55973; packages: 34606
  - PR 1645 cli-0 (the one job whose `--log-failed` was non-empty earlier): 368850 in an isolated probe; the aggregated per-job endpoint here: 97872
  - PR 1665 native/installation-destroy 136580960436: 33963; perses-runtime-smoke 136733590613: 41605; Keycloak/docker 136733615993: 39427
- Raw logs saved under this lane's temp zone for reproduction (not committed to any product repo).

## 4) Counting: distinct first-level `--- FAIL: Test` names per PR (subtests stripped)

- Method: per-job logs fetched via the authenticated jobs/{id}/logs endpoint; `grep` for `--- FAIL:`, strip the timestamp prefix and any `/subtest`, `sort -u` at first level.
- PR 1596: 197 distinct first-level names
- PR 1597: 197 distinct first-level names
- PR 1620: 197 distinct first-level names
- PR 1645: 198 distinct first-level names (the extra is `TestPersesTempoDatasourceSharedBackendGatewayStaysPolicyNeutral`, added by the .go->.go.txt rename)
- PR 1650: 197 distinct first-level names
- PR 1723: 197 distinct first-level names
- PR 1665: 1 real first-level test fail — `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` — from `Native · native/podman/installation-destroy` (job 136580960436). The 1665 `Go unit`/Keycloak/perses-runtime jobs are compile-rootless-runtime timeouts (`[error]The operation was canceled`), not test failures.
- The 197-name set is IDENTICAL across 1596/1597/1620/1650/1723 (diff of 1596 vs 1597 = empty). These are the entire `cmd/baha` Go-unit shard failing as a block.

## 5) Ancestry axis (mission step 4): develop NOT an ancestor of head = class (b)

- Witnessed develop head: `77c1e60f51b91003ac3ddc391008c15e4a713a5c`.
- Anchor used by prior `other-domain-test-split` evidence: older develop `40cb28c758b02960356434b630086a341ebe1738`; current develop `77c1e60` is ahead of it.
- `gh api .../compare/<develop>...<head>` status for every failing PR is `diverged` (develop is NOT an ancestor of head; the head branched off an older develop), except PR 1665 = `behind` (purely older, ahead_by 0). behind_by (commits of develop not in head = the `git rev-list --count <head>..<develop>` proxy):
  - PR 1596: behind=166
  - PR 1597: behind=166
  - PR 1620: behind=166
  - PR 1645: behind=191 (most diverged)
  - PR 1650: behind=166
  - PR 1665: behind=1
  - PR 1723: behind=166
- Verdict: every failing run applies to a STALE develop snapshot, far behind the witnessed head. `merge-base --is-ancestor develop head` = NO for all seven.

## 6) Protocol classification (a real defect / b stale base / c other-card)

- Root cause (all six Go-unit PRs): the 197 `cmd/baha` tests fail at the operator-auth gate, not at their own assertions. Witnessed verbatim in the logs: `authentication_failed` ... `"message":"Managed-environment machine operations require an authenticated BaseHarbor operator."` and `needs interactive setup but input is not a terminal`. This is ONE shared root cause, not seven separate defects.
- Class (b) for all six Go-unit PRs (1596, 1597, 1620, 1645, 1650, 1723): the run applies to a stale develop snapshot (behind 166-191 commits), the entire `cmd/baha` shard fails together at the shared operator-auth gate, and the same names fail identically on every PR. `develop` is not an ancestor of the head. This matches the `0428-206 other-domain-test-split` card, which already inventoried the neutral production path as 97/117 operator-auth-gate failures, and the `0428-213 trust-uninstall-false-green` card (PR #1737), which fixes the same class of gate-backed test.
- Class (b) for PR 1665 too: its one real test fail (`TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry`) and its Keycloak/perses-runtime timeouts are the same stale-base + runtime-gate effect (behind 1; rootless-runtime compile timeout on GitHub-hosted shared runners). Not a distinct product defect.
- No class (c) hit: none of the failing names belongs to a DIFFERENT fan-out as a distinct defect. The nearest other-card hits are the cards that OWN the operator-auth root cause (0428-206, 0428-213, PR #1737) — i.e. these names are the shared gate signature, not a mis-attributed case. The `TestTrustUninstallPromptEOFAbortsCleanly` hit in `trust-uninstall-false-green/` and `other-domain-test-split/` is the same gate root, not a separate fan-out defect.
- Class (a) real defects found: 0. The kitchen-cook-reckoner's "11 red" resolves to stale-base shard-failures, not seven distinct product defects.

## 7) Table (PR | failing jobs | first-level names | class a/b/c | rev-list/behind size)

| PR | failing job name(s) | distinct first-level `--- FAIL:` names | class | behind (stale) / head |
| --- | --- | --- | --- | --- |
| 1596 | Selected Checks 136671011448; Go unit cli-0..3, packages | 197 (cmd/baha shard, identical set) | b (stale base) | behind 166 / 6135e73a |
| 1597 | Selected Checks 136555658338; Go unit cli-0..3, packages | 197 (same set) | b (stale base) | behind 166 / 90063f6e |
| 1620 | Selected Checks 136677834103; Go unit cli-0..3, packages | 197 (same set) | b (stale base) | behind 166 / 28cb907d |
| 1645 | Selected Checks 136562618719; Go unit cli-0..3, packages | 198 (same set + TestPersesTempoDatasourceSharedBackendGatewayStaysPolicyNeutral) | b (stale base) | behind 191 / 4d73aa97 |
| 1650 | Selected Checks 136667750659; Go unit cli-0..3, packages; docker/identity 136666960147 | 197 (same set) | b (stale base) | behind 166 / 28c18f02 |
| 1665 | Selected Checks 136733763054; Go unit 136733616159..16174; Native Keycloak 136733615993; Runner Interface 136733615999; Validation go-build/cli-gofmt/go-vet/authority-package-tests; Focused Python 136733615977; Exact Candidate 136733616020; Native perses-runtime-smoke 136733590613 (timeout); Native podman installation-destroy 136580960436 (1 real test) | 1 real: TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry; rest compile/rootless-timeouts | b (stale base + runtime gate) | behind 1 / e84e434b |
| 1723 | Selected Checks 136472605316; Go unit cli-0..3, packages; Selected Runtime docker data-capabilities 136470779149 / guided 136470779213 | 197 (same set) | b (stale base) | behind 166 / 26755fc1 |

- Shared root-cause line (verbatim, from PR 1596 cli-0 log, `--- FAIL` context): `Managed-environment machine operations require an authenticated BaseHarbor operator.` / `authentication_failed`.
- First-level names are identical across the six Go-unit PRs (diff 1596 vs 1597 = empty); full names for PR 1596 are in the reproduction logs under this lane's temp zone.

## ## PLAN (wiederholt, Board-Referenz)

1. Verify gh auth, evidence dir, baseharbor-plan remote.
2. Enumerate open PRs and `gh pr checks` per PR; keep `fail` PRs.
3. Capture failing job name + id; three-path byte sizes.
4. Count distinct first-level FAIL names; list them.
5. Ancestry axis (compare API behind_by).
6. Cross-check against other-card evidence for class (c).
7. Write table + cleanliness + repo-rule.
8. Push to origin/main, verify path present, END line.

## cleanliness

- No containers, compose projects, docker, or podman started. This is a pure read-only desk: `gh` + `curl` against the GitHub REST logs API + `git ls-remote` against the witnessed develop head.
- `docker ps -a` before: N/A (no daemon interaction this lane).
- `docker ps -a` after: N/A (no daemon interaction this lane).
- Cleanliness: clean. No test containers/networks/volumes/state left behind. No ambient-`bh-*` stack touched. No changes to /home/marcel/dev/baseharbor-ecosystem itself; all fetches wrote to this lane's temp zone only.

## repo-rule compliance

- BUG-HUNT scope, pure classification: no product file changed, no commit to baseharbor, no PR opened/edited/closed, no rerun/workflow_dispatch, no subagents (4.8), no bare `go test ./cmd/baha/`, no `git add -A`, no `git stash` in the shared plan checkout.
- Remote guard: the only github.com/mcpdev80 remote used is `https://github.com/mcpdev80/baseharbor.git` (verified via `git ls-remote` / `gh`), never an unresolved name.
- Evidence stays ONLY in baseharbor-plan; no .evidence/ dir, no product-repo writes.
- Runners are GitHub-hosted shared runners; nothing built/registered/repaired.
