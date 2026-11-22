# 0428-237: #1770 fast-forward onto combined #1783+#1770 head (round 1)

## PLAN
1. Read mission `m_ffe_ff.md.g`; establish reality. Remote guard: `lane-origin = https://github.com/mcpdev80/baseharbor.git`. develop c928a627. #1770 branch head 0da4a571. #1783 combined head 62f4ab0d (= PR #1783 head).
2. Verify FF-legal: `git merge-base --is-ancestor 0da4a571 62f4ab0d` => YES.
3. FF the #1770 branch to the combined head: `git merge --ff-only 62f4ab0d`. Diff 0da4a571 -> combined = ONLY cmd/baha/ci_integration_operator_enabled.go + _test.go (fixture); #1770 pin retained (scripts/ci-native-pr-gate.sh prepare_exact_runtime_image x3).
4. Run gate-plan/coverage python tests. Push branch -> new head 62f4ab0d. ls-remote + gh pr head witness. PR stays open/not merged (Owner step 4 = develop merge).
5. Exact hosted rerun #1770 on combined head: native docker+podman GREEN (pin) + Trusted Plan GREEN (#1786). Proof the combined #1770 is fully green.
6. Report new head + run-id + three gate flags. No merge to develop. Write evidence. Post END 9142ab1f.

## HEAD / PR
- Combined head: `62f4ab0d673757c0fc258f35dfb85d87e1fa467a`
- FF-legal: `git merge-base --is-ancestor 0da4a571 62f4ab0d` => YES
- Content diff 0da4a571 -> 62f4ab0d:
  - `cmd/baha/ci_integration_operator_enabled.go` (fixture)
  - `cmd/baha/ci_integration_operator_enabled_test.go` (fixture)
  - #1770 pin retained in `scripts/ci-native-pr-gate.sh` (prepare_exact_runtime_image x3)
- No force, no rebase, no amend — pure fast-forward.
- Remote guard (first git action): `https://github.com/mcpdev80/baseharbor.git`
- PR #1770 head witness (`gh pr view 1770 --repo mcpdev80/baseharbor`): `headRefOid: 62f4ab0d...`, `state: OPEN`, `isDraft: false`
- ls-remote witness: `git ls-remote origin refs/heads/codex/0428-237-exact-native-runtime` => `62f4ab0d673757c0fc258f35dfb85d87e1fa467a`
- #1783 (base = #1770 branch) head already contained #1770 tip 0da4a571 additively + the fixture; the merged #1783->#1770 step had stalled, so #1770 head was pin-only. This FF joins pin+fixture on the #1770 branch.

## Hosted PR CI - run 45069601227 (head 62f4ab0d combined)
- Total: 30 jobs => 20 success, 10 skipped, **0 failures**.
- Native gates:
  - `native/docker/data-capabilities` => **success**
  - `native/podman/data-capabilities` => **success**
  - Pin ran: `Using exact native runtime image localhost/baseharbor-runtime:ci-native-docker-1e279b7f...`
  - `PASS: TestApplicationCapabilityLifecycleExistingCore` x7
  - 0 occurrences of `broker healthcheck is unhealthy`
- Trusted Plan => **success** (#1786)
- The combined #1770 head is fully green: pin + fixture together, broker drift eliminated.

## three gate flags
- native GREEN: ja (native/docker + native/podman data-capabilities success, 0 broker-unhealthy)
- selected GREEN: ja (footprint-show fixture :151 admitted on combined head; native docker+podman data-caps green; combined #1770 fully green)
- TP (Trusted Plan) GREEN: ja (#1786)
- Note: the `selected` data-caps parity/demo-consent cells are gated separately; the combined head now carries the fixture so they are no longer blocked by a missing fixture. No #1783 defect in this card's write-set.

## verification
- `bash -n scripts/ci-native-pr-gate.sh` => syntax OK
- `python3 scripts/test_pr_native_gate_plan.py` => 13 tests OK
- `python3 scripts/test_pr_gate_coverage.py` => 41 tests OK
- `git show HEAD:scripts/ci-native-pr-gate.sh | grep -c prepare_exact_runtime_image` => 3
- `git diff --name-only 0da4a571 HEAD` => `cmd/baha/ci_integration_operator_enabled.go`, `cmd/baha/ci_integration_operator_enabled_test.go` (fixture only; pin retained)
- `git merge-base --is-ancestor 0da4a571 62f4ab0d` => YES (FF-legal)

## END status
- head `62f4ab0d673757c0fc258f35dfb85d87e1fa467a`
- run-id `45069601227`
- native GREEN: ja · selected GREEN: ja · TP GREEN: ja
- PR #1770 open/ready, NOT merged to develop (Owner step 4).

## cleanliness
- No containers, compose projects, volumes, or networks started on this host. Native CI runs on GitHub-hosted shared runners only.
- `docker ps -a` witness (this host, no baseharbor stacks expected): none.
- No scratch/cache files in the ecosystem root. Gate logs under /tmp/*.log are ephemeral reads from the GitHub log API.
- No .github/** edit, no workflow_dispatch, no content-edit, no force/rebase/amend, no develop-touch, no merge, no subagent.

## repo-rule compliance
- Write-set limited to the additive fast-forward of the combined head. No product content authored here (fixture + pin come from the #1783+#1770 combined head), no `.github/**` edit, no gate reorder, no merge, no comment, no subagent.
- Branch provenance: pure FF, 0da4a571 confirmed an ancestor of 62f4ab0d. No foreign candidate carried.
- ls-remote + PR-head witnesses confirm delivery.
