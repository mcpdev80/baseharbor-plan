## PLAN (round 5 — branch correction for 0428-142 perses backend-witness renderer)

1. Read the mission correction (`/var/tmp/ans2.txt`) and record the numbered plan before Git.
2. Verify `2b1fdcc` is a clean fast-forward of the PR head `e21b5c5` (content unchanged; only the branch target differs).
3. Resolve remotes (`origin` = github.com/mcpdev80), force-push `2b1fdcc` to the PR branch `lane-0428-142-statuswitness`, prove `gh pr view 1702 --json headRefOid = 2b1fdcc`, no second PR.
4. Monitor the new hosted CI run on `2b1fdcc` to terminal (run-id + conclusion per shard, §4.6).
5. Classify the failing shards as inherited (operator-auth class #1615 + shared-runner PKI fixture), proven by identical failures on the old head.
6. Publish round-5-hopfix.md to baseharbor-plan origin/main (verified path); clean host; report END to coordinator.

## Review metadata

- Session: Ornit worker, lane 0428-142-hopfix.
- Model: worker-ornith1.5 (providerID agentgateway). Backend: not exposed.
- Time: 2026-11-21, UTC.
- Candidate head (corrected, on PR branch): `2b1fdcc06d9e07de583fea5140e020597bd2a18d`.
- Previous PR head (before correction): `e21b5c528923ddd610b8c5e709ff0d61294c211e`.
- develop base head: `40cb28c758b02960356434b630086a341ebe1738` (via `git ls-remote origin refs/heads/develop`).
- Accepted prior candidate (carries the renderer): `3f7600ded0d98902ec689543fa29ad4fdc0d3e6e`.

## Remote attestation (BEFORE first push)

```text
origin  https://github.com/mcpdev80/baseharbor.git (fetch)
origin  https://github.com/mcpdev80/baseharbor.git (push)
```

## Root cause and the correction

PR #1702 (`headRefName = lane-0428-142-statuswitness`, base develop, draft=false) carried the entire Perses witness feature but the hop left `renderPersesBackendWitness` defined (perses_lifecycle.go:314) and never called, so the human `perses status` face drifted from the machine face. The fix restores the one dropped call in `persesStatusCommand` (perses_lifecycle.go:93).

Round-4 delivered that exact fix on a dedicated lane branch `lane-0428-142-perses-status-backend-witness` (commit `2b1fdcc`). The owner's correction (2026-11-21) states the content is correct but the branch is wrong: one card, one PR. `2b1fdcc` sits directly on the PR head `e21b5c5` (its parent is `e21b5c5`), so it is a clean fast-forward — only the branch target changes, the candidate is byte-identical.

Fast-forward proof:

```text
git merge-base --is-ancestor e21b5c528923ddd610b8c5e709ff0d61294c211e 2b1fdcc06d9e07de583fea5140e020597bd2a18d -> 0 (ancestor)
git rev-parse 2b1fdcc^ -> e21b5c528923ddd610b8c5e709ff0d61294c211e
git diff --name-only origin/pr/1702 2b1fdcc06d9e07de583fea5140e020597bd2a18d
  cmd/baha/app_status_result_test.go
  cmd/baha/perses_lifecycle.go
```

Push and delivery:

```text
To https://github.com/mcpdev80/baseharbor.git
   e21b5c5..2b1fdcc  2b1fdcc06d9e07de583fea5140e020597bd2a18d -> lane-0428-142-statuswitness
```

ls-remote delivery witness:

```text
2b1fdcc06d9e07de583fea5140e020597bd2a18d	refs/heads/lane-0428-142-statuswitness
```

PR #1702 headRefOid after the push (PR follows the branch, no retarget, no second PR):

```text
{"headRefName":"lane-0428-142-statuswitness","headRefOid":"2b1fdcc06d9e07de583fea5140e020597bd2a18d"}
```

## CI state (run-id + conclusion per shard, §4.6)

New head `2b1fdcc`: CI run `44865751734` event=pull_request, head `2b1fdcc06d9e`, completed/failure at 2026-11-21T04:24 UTC.

Success shards: Native gate plan, Workflow policy, Source format, Trusted Plan, Focused Python, go-build, go-vet, cli-gofmt, owner.
Skipped (advisory / gated): Targeted HA docker/podman, Main release Go, Draft source/routing/go, Exact Pre-Release, Release Source Preflight, Native, validate, Candidate-added (advisory), Demo Pin, Native Keycloak/Core, Runner Interface, Consumer Pins, Exact Candidate.
Failed shards: PR · Go unit · cli-0, cli-1, cli-2, cli-3, packages.

Old head `e21b5c5` (pre-correction): CI run `44850246247` completed/failure, same five failing shards. This is the identity of the failing set.

## Inherited-failure classification

**cli-0..3 — operator-auth class (#1615).** The four failing CLI-invoking witness tests and the rest of the cli-shards fail with one error:

```text
app_perses_cli_test.go:284: baha status --json failed: operator authentication needs interactive setup but input is not a terminal
```

This is the inherited operator-auth boundary (managed environment, interactive CIDR gate). It fails identically on the old head `e21b5c5` (run 44850246247). The success of the class on a different head (`run 44854729670 cli-0..3 SUCCESS`) proves the class is fixable/environment-dependent, not a per-candidate defect; it does not certify this candidate.

**packages — shared-runner PKI fixture.** The packages shard fails on exactly three tests, identical on both heads:

```text
loki_test.go:522: perses Loki datasource health client: load Loki service access identity: stat .../providers/loki/shared/service-access/pki/client-cert.pem: no such file or directory
```

`TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource`, `TestPersesLokiDatasourceMultiSourcePartialMatchability`, `TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed` — all in `loki_test.go`, a file this change does not touch. Same three fail on old head run 44850246247.

**My change introduces zero regressions.** `2b1fdcc` differs from `e21b5c5` only by:
- `perses_lifecycle.go`: the restored `renderPersesBackendWitness(out, result.BackendWitness)` call.
- `app_status_result_test.go`: two new focused tests (`TestPersesStatusWitnessHumanFaceRendersBackendWitness`, `TestPersesStatusWitnessRendersBackendWitnessDirectly`).

Neither new test appears in the failing set; the failing set is byte-identical between the two heads.

## Evidence: focused tests (local, bypassing operator-auth boundary)

Three pure-unit witness tests + one direct-renderer test that do not hit the CLI operator-auth boundary:

```text
--- PASS: TestPersesStatusWitnessConfiguredWhenResolved (0.00s)
--- PASS: TestPersesStatusWitnessUnreachableWhenDeclaredNotResolved (0.00s)
--- PASS: TestPersesStatusWitnessUnreachableIsNotTheManifestFlag (0.00s)
--- PASS: TestPersesStatusWitnessRendersBackendWitnessDirectly (0.00s)
```

The direct-renderer test is a valid regression guard: it fails without the renderer call (removed the call, test failed) and passes with it (exit 0). go build / go vet / gofmt clean on `2b1fdcc`.

## repo-rule compliance

- Write-set: exactly the three card files (`perses_lifecycle.go`, `app_status_result_test.go`; `app_status_result.go` unchanged vs PR head, present on the PR). No change to internal/operatorauth/**, internal/observability/registry.go, internal/capability/perses_selection.go, internal/identityprovider/**, internal/serviceaccess/**, the #1615/#1625/#1623 stack, .github/**, or runner infrastructure.
- One integration candidate per chain: the single PR #1702 / PR branch `lane-0428-142-statuswitness`. No second PR opened; the old dedicated lane branch is not a PR.
- Subagents: none used. Every step executed in this session.
- No .github/** edits, no workflow reruns/workflow_dispatch, no runner repair.
- No Docker/Podman containers or compose projects started; nothing to tear down.
- Evidence written only to baseharbor-plan (origin/main), never in the product repo.
- Workspace: worktree under /tmp/opencode/0428-142-hopfix-wt; caches under /home/marcel/.go-build-cache; no scratch in the ecosystem root.

## cleanliness

- No containers/volumes/compose projects started on this host. `docker ps -a` witness: nothing started this lane (pre/post identical).
- CI job log downloads under /tmp/opencode/0428-142-hopfix-jobs/ (transient).

## END

END_DONE 0428-142-hopfix: re-pointed the one-line renderer fix to the PR branch lane-0428-142-statuswitness (2b1fdcc, fast-forward of e21b5c5, byte-identical candidate), PR #1702 headRefOid = 2b1fdcc, no second PR. CI run 44865751734 terminal/failure = inherited class only (cli-0..3 operator-auth + packages Loki PKI fixture), identical to old head run 44850246247; owner/go-build/go-vet/go-gofmt SUCCESS. Evidence round-5-hopfix.md published to baseharbor-plan origin/main.
