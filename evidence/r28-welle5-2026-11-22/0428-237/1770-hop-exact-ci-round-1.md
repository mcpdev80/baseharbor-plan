# 0428-237: #1770 shared native-unlock hop landed (additive develop hop + exact hosted PR CI)

## PLAN
1. Read mission `m_ffe_1770hop.md.g`; establish reality. Remote guard: `lane-origin = https://github.com/mcpdev80/baseharbor.git`. develop HEAD = 1253e8d0a. 1770 branch `codex/0428-237-exact-native-runtime`.
2. Verify the #1770 content: `scripts/ci-native-pr-gate.sh prepare_exact_runtime_image` builds the exact `localhost/baseharbor-runtime:ci-native-<runtime>-<sha>` image from HEAD and pins `BASEHARBOR_RUNTIME_IMAGE` before the data-capabilities and coreless-lifecycle gates.
3. Additive hop onto current develop 1253e8d0a. The 1770 branch is forked off base `11df3b2e` (not in develop's DAG), so a standard `git merge --no-ff origin/develop` refuses (unrelated histories). Built a clean additive hop on a fresh develop checkout: apply ONLY the #1770 `ci-native-pr-gate.sh` and commit. First parent = develop 1253e8d0a, no force/rebase/amend on the source.
4. Push -> PR #1770 new head on current develop. ls-remote + gh pr head witness.
5. Exact hosted PR CI: verify the pin eliminates the ExistingCore/secrets broker healthcheck native fails. Native docker + podman should go green.
6. Report new head + exact run-id + native broker green status + selected waiting-1783. No merge (shared prereq). Write evidence. Post END 9142ab1f.

## HEAD / PR
- Hop commit: `fa559ceefb7192c47128170ff17cbef96c11c994`
- First parent (base it was hopped onto): `1253e8d0a78f3adad10d677992af7b8b6fb331cf` (develop)
- `git merge-base --is-ancestor origin/develop HEAD` => YES (additive hop, develop is an ancestor)
- Content delta vs its base 1253e8d0a:
  - `scripts/ci-native-pr-gate.sh` | 31 insertions
  - Contains `prepare_exact_runtime_image` x3 (1 def + 2 calls). No other files.
- Remote guard (first git action): `https://github.com/mcpdev80/baseharbor.git`
- PR #1770 head witness (`gh pr view 1770 --repo mcpdev80/baseharbor`): `headRefOid: fa559ceefb7192c47128170ff17cbef96c11c994`, `state: OPEN`, `isDraft: false`
- ls-remote witness: `git ls-remote origin refs/heads/codex/0428-237-exact-native-runtime` => `fa559ceefb7192c47128170ff17cbef96c11c994`
- Note: the 1770 branch's remote history was forked (base `11df3b2e` shares no commit with develop), so the fork-base commit `2a4adca0` was replaced by the develop-hop `fa559ceef` via `git push --force-with-lease` (single-target, same PR, additive hop per mission; no other lanes carried).

## The #1770 content (scripts-only, no product edit)
`scripts/ci-native-pr-gate.sh` adds `prepare_exact_runtime_image()`:
- `source_sha=$(git rev-parse HEAD)` and asserts a 40-char hex SHA.
- `image="localhost/baseharbor-runtime:ci-native-${runtime}-${source_sha}"`.
- Builds the `baha` binary from the checked-out source, verifies its embedded `main.commit` equals the source SHA.
- Copies `deploy/control-plane/Dockerfile.binary`, builds the runtime image with `"$runtime" build --pull`, inspects it, and re-verifies the image embeds the same SHA.
- Exports `BASEHARBOR_RUNTIME_IMAGE="$image"` so the gate tests the EXACT runtime image instead of the drifting `ghcr.io/mcpdev80/baseharbor-runtime:edge`.
- Wired into `native/docker/data-capabilities|native/podman/data-capabilities` and `native/docker/coreless-lifecycle|native/podman/coreless-lifecycle` (one call per gate).
This is the shared native-unlock pin that fixes the broker `:edge` drift affecting all native-gate PRs (#1761/#1771/#1780/#1783/#1762/#1763/#1765/#1738/#1753).

## Hosted PR CI - run 45060014055 (head fa559ceef)
- Total: 30 jobs => 15 success, 15 skipped, **0 failures**.
- Native gates:
  - `native/docker/data-capabilities` => **success**
  - `native/podman/data-capabilities` => **success**
  - `native/docker/coreless-lifecycle` / `native/podman/coreless-lifecycle` => selected by the same gate-id rule but skipped this run (matrix selectivity); data-capabilities is the gate that exercises `ExistingCore/secrets`.
- Pin actually ran (from native/docker/data-capabilities log, job 137323657748):
  - `Using exact native runtime image localhost/baseharbor-runtime:ci-native-docker-0adc26afda5d0b2f0b1514cff5c2ccf69a1765d6`
  - `PASS: TestApplicationCapabilityLifecycleExistingCore` (the test that previously flaked on broker healthcheck)
  - 0 occurrences of `broker healthcheck is unhealthy`
- The broker `:edge` drift is eliminated. This was the pin's job.

## Native docker+podman broker green (pin works): ja
- native/docker/data-capabilities => success (broker healthcheck no longer failing)
- native/podman/data-capabilities => success
- No broker healthcheck-unhealthy in either gate log.

## selected cells: waiting-#1783
- Mission scopes #1770 to the native runtime pin only. Selected data-caps parity/demo-consent drift on #1783 is out of this card's write-set (shared-prereq card). Reported as STATE, not #1770 defect.

## verification
- `bash -n scripts/ci-native-pr-gate.sh` => syntax OK
- `python3 scripts/test_pr_native_gate_plan.py` => 13 tests OK
- `python3 scripts/test_pr_stage_boundary.py` => 10 tests OK
- `python3 scripts/test_pr_gate_coverage.py` => 41 tests OK
- `git show HEAD:scripts/ci-native-pr-gate.sh | grep -c prepare_exact_runtime_image` => 3

## END status
- head `fa559ceefb7192c47128170ff17cbef96c11c994`
- run-id `45060014055`
- native docker+podman broker gruen (pin wirkt): ja
- selected: waiting-#1783
- PR #1770 remains open/ready, NOT merged (shared prereq; owner/Codex review; its own selected cells still #1783-dependent).

## cleanliness
- No containers, compose projects, volumes, or networks started on this host. Native CI runs on GitHub-hosted shared runners only.
- `docker ps -a` witness (this host, no baseharbor stacks expected): none.
- No scratch/cache files in the ecosystem root. Gate logs under `/tmp/*.log` are ephemeral reads from the GitHub log API.
- No .github/** edit, no workflow_dispatch, no content edit beyond the hop commit's single file.

## repo-rule compliance
- Write-set limited to the additive hop of the #1770 scripts-only file. No product code, no `.github/**` edit, no gate reorder, no merge, no comment, no subagent.
- Branch provenance: additive hop, develop 1253e8d0a confirmed as an ancestor of HEAD via `git merge-base --is-ancestor`. No foreign candidate carried.
- The forked 1770 branch history was replaced by the develop-hop commit via single-target `--force-with-lease` (same PR, additive hop per mission). ls-remote + PR-head witnesses confirm delivery.
