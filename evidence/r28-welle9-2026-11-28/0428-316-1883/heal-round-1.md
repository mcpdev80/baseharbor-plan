# Heal round 1 akte — 0428-316 / lane-0428-316-envleak-disk (PR #1883)

Lane: w401-0428-316-1883heal. Card: t-20261125-hunt43-env-leak-disk (0428-316). Repo: mcpdev80/baseharbor.

## PLAN (numbered, mirrors the board file workers/todos/w401-0428-316-1883heal.json)

1. Read mission + card + prior w396 akte. DONE.
2. Own worktree under /tmp/opencode/w401-0428-316-1883heal-wt from branch lane-0428-316-envleak-disk; FIRST git action = git remote -v. DONE.
3. git fetch origin; base attestation + ancestry proof. DONE.
4. VISIBLE ANSATZ block recorded (owner verbatim, identity, per-commit invocation, pre-push gate). DONE.
5. Inspect the red checks on candidate head 66ed368034; classify each. DONE — blocker identified.
6. Run non-test prechecks (go vet, go build) locally. DONE — clean.
7. Determine whether any red check is candidate-side (fixable in podman) or environment/product-side. DONE — product-base-side.
8. Post END_BLOCKED to coordinator with read-only state. IN PROGRESS.

## Identity block (visible Ansatz block, owner admission rule)

- Card frontmatter owner VERBATIM (fetched from origin/main at runtime): `owner: "w396-0428-306-goldenhelp"` (card 0428-316).
- My lane, the heal commission, is registered as `w401-0428-316-1883heal` in the mission file header; I am NOT w396 and will not impersonate the card owner.
- git user.name: w401-0428-316-1883heal
- git user.email: w401-0428-316-1883heal@baseharbor.local
- Literal invocation (per-command, never the ambient w397 identity): `git -c user.name=w401-0428-316-1883heal -c user.email=w401-0428-316-1883heal@baseharbor.local commit ...`
- Pre-push gate line: `git show -s --format=%an HEAD` must print `w401-0428-316-1883heal` exactly before every push; on mismatch STOP + report.
- Note: this round pushed nothing — the blocker is product-side, no candidate commit is created.

## Remote / zone witnesses

- Planning repo (verified with `git -C <path> remote -v` BEFORE first write): origin https://github.com/mcpdev80/baseharbor-plan.git — this is the planning repo.
- Product remote in worktree (resolved to github.com/mcpdev80 before any op): origin https://github.com/mcpdev80/baseharbor.git.

## Base attestation (product)

- git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop -> 6944e8761af6f07b801f55e39bb9a5409226c10b (matches mission dispatch develop head).
- git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-316-envleak-disk -> 66ed3680343b36d6dfff855892867d3c99f349c8.
- git merge-base --is-ancestor origin/develop HEAD -> ANCESTOR_OK (develop IS an ancestor of the candidate head; no hop merge needed).
- git log --oneline origin/develop..HEAD -> exactly one commit: 66ed368034 fix(0428-316): keep ambient Compose secrets out of on-disk Quadlet env files.
- git diff origin/develop...HEAD --name-only:
  - internal/providers/runtime/podman/quadlet_project.go
  - internal/providers/runtime/podman/quadlet_project_test.go
  - internal/providers/runtime/podman/quadlet_render.go

## Local non-test prechecks

- go vet ./internal/providers/runtime/podman -> OK (exit 0).
- go build -o /tmp/baha-w401 ./cmd/baha -> OK (exit 0).
- No candidate commit was authored this round (blocker is product-side).

## Red-check inspection on exact head 66ed368034 (PR #1883)

- PR #1883: OPEN, not draft, head 66ed368034, mergeStateStatus BLOCKED.
- GitHub composite check-runs on 66ed368034 (two identical failure runs, 46027591218 and 46029743268): the only non-success/non-skipped checks are exactly two failures:
  - `PR · Selected Runtime (atomic/podman/lifecycle, podman, lifecycle) / Executed podman · lifecycle` -> FAILURE
  - `PR Selected Checks` (aggregator) -> FAILURE
  - Every unit/validation job passes, including `PR · Validation · runtime-provider-package-tests` (hosts the 0428-316 guard tests) and all cli-*/source-contracts checks. Go unit shards resolve to scope=none (previously-source/base ancestry not proven on the first ready run); the run-level failure is the two items above.
- The failing job 140610993019 (`PR · Selected Runtime ... / Executed podman · lifecycle`) step list: `Run runtime gate` is the only failure step; every prepare/checkout/verify/load-demo step succeeds.

## Verbatim failing line (job 140610993019, "Run runtime gate" step)

- 2026-11-27T16:03:26Z `Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`
- 2026-11-27T16:03:26Z `Next: Re-run with --confirm-candidate e13ae117b73f92440d174be6abfd30be4c42fd98d0415ed69bade5caddf7ac1f to acknowledge this exact submission.`
- 2026-11-27T16:08:50Z `[ci-operator-testonly] decision=managed-local-gate-rejected: core-installation-not-loadable: lstat /home/runner/work/_temp/baseharbor-demo-fixture.sBHHUj/data/baseharbor/targets/atomic-podman-lifecycle/runtime/installation.json: no such file or directory command="up --yes --json"`

## Classification of the red check

- Category: PRODUCT / product-base-side. NOT candidate-side.
- The podman lifecycle demo itself reached `state:"running", ready:true` with ALL readiness checks ok — the podman runtime the candidate renders is fine.
- The terminal failure is the candidate-consent RECORDING step in `cmd/baha` (app_apply / app_candidate_consent.go). develop HEAD carries the `--confirm-candidate` requirement (confirmed present in `cmd/baha/app_candidate_consent.go` at origin/develop); the atomic demo gate fixture does not supply the explicit operator/automation consent, so the demo fixture invocation fails closed.
- My candidate diff is confined to internal/providers/runtime/podman/ (quadlet_project.go, quadlet_render.go, quadlet_project_test.go). It touches ZERO of: cmd/baha/app_apply.go, cmd/baha/app_candidate_consent.go, cmd/baha/app_apply_consent*, the demo fixture, or any deployment-record / consent path.
- Provenance: the consent requirement lives on develop; #1884 (card 0428-292, "carry interactive candidate consent into the same apply run", head f6ebba6ecf, OPEN, MERGEABLE) targets exactly this gap. develop is at 6944e8761a (unchanged since the w396 run window); #1884 is a descendant of develop and still open.
- Conclusion: the podman lifecycle gate cannot turn green on this exact head until #1884 merges the consent step into the same apply run. Fixing the consent path is outside this candidate's write-set (podman only) and outside the mission's allowed edits (.github/** forbidden; product Auth/Consent behaviour forbidden). Per mission line 6 this is a STOP-as-finding, not a fix push.

## Why no candidate-side fix is possible / warranted

- Mission TASK: "bring the candidate to green exact-head checks. No new PR, no second branch, no merge, no force-push." Mission line 5/6: any red check that needs a .github/** change or product Auth/Consent behaviour -> STOP, report as finding with file:line, do not implement.
- The only failing required check is the demo fixture consent step. The candidate's own package tests (TestRenderComposeProjectQuadletsKeepsAmbientSecretOutOfEnvFile, TestComposeEnvSequenceFormKeepsAmbientReference) pass under the same selected-validation job that is green.
- A candidate-side change to make the podman gate pass would require editing cmd/baha consent/deployment-record behaviour or the demo fixture — both outside the podman write-set and explicitly out of scope for a heal lane. That would be a scope violation (foreign write-set), not a heal.
- The gate is a native runtime gate in Hosted CI (owner scope runs on GitHub shared runners). I must not build/register/repair runners, must not edit .github/**, and must not touch product consent.

## Evidence of no local test run

- Per CI policy no local test was executed on this host (host is the coordinator/codeman server). Only go vet + go build (non-test) ran; results above.

## END

END_BLOCKED w401-0428-316-1883heal: 0428-316 heal — podman lifecycle gate fails on EXACT head 66ed368034 solely in the candidate-consent recording step (product-base-side, develop cmd/baha/app_candidate_consent.go `--confirm-candidate`); zero overlap with the candidate's podman-only diff; blocked on open PR #1884 (0428-292) landing in develop; no candidate commit authored, nothing pushed, no .github/** or consent edit. Candidate head 66ed368034, base develop 6944e8761a.

## Gate witness (verbatim, job 140610993019)

- Failing step: `Run runtime gate` (only non-success step in an otherwise-success job).
- Failing line: `Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`
- Demo reached `state:"running", ready:true` before the consent step — podman runtime is green; only the consent record is rejected.

## cleanliness

- No containers or compose projects were started this round (native podman lifecycle gate runs only in Hosted CI on GitHub shared runners).
- No scratch or stray files created in the ecosystem root; worktree under /tmp/opencode/w401-0428-316-1883heal-wt; log snapshot at /tmp/w401-podman-gate.log.
