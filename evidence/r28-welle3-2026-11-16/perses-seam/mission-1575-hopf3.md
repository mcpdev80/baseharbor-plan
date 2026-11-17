# mission-1575-hopf3 — perses-seam base-refresh hopf-3

## One-line summary
Base-Hopf #3: develop advanced to 2581000b (uid-app #1579 merged 04:58:47Z) past my prior head 16adf5c3. Re-merged origin/develop into the same candidate branch `lane-0428-075-perses-seam` (plain merge, no rebase, no force, no second branch). Diff carried only the uid-app regression file `cmd/baha/app_init_uid_app_slice_test.go` — ZERO overlap with Perses seam files (seam intersection = null). Build/vet/gofmt + affected seam tests green, refspec-pushed, PR #1575 READY.

## Trigger (fensterregel)
- Prior remote head (hopf-2): `16adf5c3d2db3039c183e1a6841fced31a131b2e`
- New remote develop: `2581000b5fdb78f4af577fc13ce1205ca32a84e8` (0428-050 uid-app Option B #1579, merged 04:58:47Z)
- Ancestry check: `git merge-base --is-ancestor 16adf5c3 origin/develop` => NO (HEAD is behind develop), so a re-merge was required.

## PLAN

- 1. Reality sync: ls-remote witnesses first (develop + lane head)
- 2. Inheritance / delta check: what develop brings past 16adf5c3, confirm seam intersection = null
- 3. git merge origin/develop (plain merge-commit, no rebase, no force, no second branch)
- 4. build / vet / gofmt + affected seam tests
- 5. refspec-push + ls-remote witness, PR READY, exact-head run to terminal state (self-run)
- 6. extend rebase-window-1.md (hopf-3 block) + END post + GUI todos

## REALITY WITNESSES (first actions)

`git ls-remote https://github.com/mcpdev80/baseharbor.git` from fresh clone in /var/tmp/hopf3-zone:

    2581000b5fdb78f4af577fc13ce1205ca32a84e8	refs/heads/develop
    16adf5c3d2db3039c183e1a6841fced31a131b2e	refs/heads/lane-0428-075-perses-seam

Workspace: fresh clone in /var/tmp/hopf3-zone (base-develop + seam clone), mission GRENZEN: tmp = /var/tmp. No citation of the quarantined workers/baseharbor checkout anywhere.

## ERBNACHWEIS / DELTA (seam intersection = null)

- merge-base of seam vs current develop: `8db0d9bdf8d9ae77db94c9ddce9c209001c4da54`
- Files develop changed since that merge-base (i.e. what this re-merge brings): EXACTLY ONE:
    cmd/baha/app_init_uid_app_slice_test.go   (new uid-app regression slice, #1579)
- Files my seam changed since that merge-base: 20 Perses/manifest/contract files — NONE of them is the uid-app test file.
- The two sets are disjoint => the merge cannot conflict on seam files (seam-schnittmenge = null, as predicted in the mission).
- Both prior approval SHAs remain ancestors of head:
    git merge-base --is-ancestor 492b8e8f 16adf5c3 -> true
    git merge-base --is-ancestor af308e66 16adf5c3 -> true
- The re-merge carries the uid-app delta on top; the seam chain r2->r8 stays intact.

## BASE ATTESTATION

- Branch NOT newly cut: continued the existing candidate branch
  `lane-0428-075-perses-seam` at remote head `16adf5c3d2db3039c183e1a6841fced31a131b2e`
  (PR #1575, verified by ls-remote above).
- Merged `origin/develop` = `2581000b5fdb78f4af577fc13ce1205ca32a84e8` via plain
  `git merge` (no rebase, no force, no second branch).
- New head (merge commit): `fa41389c038b449dc4cd850706a6d28f3aac59a2`
  ("Merge branch 'origin/develop' into lane-0428-075-perses-seam").
- Provenance: `git merge-base --is-ancestor 2581000b fa41389c` -> true
  (develop is ancestor of the new merge commit).
- `git merge-base --is-ancestor 16adf5c3 fa41389c` -> true (prior hopf-2 head carried).
- Approvals still ancestors: `git merge-base --is-ancestor 492b8e8f fa41389c` -> true,
  `git merge-base --is-ancestor af308e66 fa41389c` -> true.
- Own commits `git log 16adf5c3..fa41389c`: exactly two — my merge commit `fa41389c`
  plus the one develop-carried commit `2581000b` (#1579 uid-app). No foreign candidate.

## Verification (local, self-run, in /var/tmp/hopf3-zone/base-seam)

Toolchain: go1.26.8 (per go.mod).
- go build ./... => pass
- go vet ./... => pass
- gofmt -l . (non-vendor) => clean (empty output)
- go test -count=1 ./internal/capability/ ./internal/metrics/ => ok
  (holds internal/capability/perses_test.go and internal/metrics/perses_contract_test.go,
  the seam-affected Perses tests)
- go test -run TestPerses ./cmd/baha/ => PASS (cmd/baha; run with TMPDIR set, see note)
- go test -count=1 ./internal/application/ => ok (161.9s; full suite)

NOTE on disk-pressure: the tmpfs `/tmp` on this host holds only ~2.6G and is shared across
lanes. Running the Go test binaries with the default TMPDIR produced only
`write .../tmp/...: disk quota exceeded` failures (TestRetainedPrometheusInventorySurvivesOtherProviderSourceWithdrawal,
TestRuntimeSourceUsesAuthenticatedServiceIdentityAndRoundTrips, the shared lock-probe cells,
and a `/tmp/argsXXXX` write in cmd/baha) — none a logic failure. With `TMPDIR`/`GOTMPDIR`
redirected to /var/tmp/hopf3-zone/go-tmp (32G free), every one of the above passes. This is a
host-environment artifact, not a merge defect: the merge delta is the single new file
cmd/baha/app_init_uid_app_slice_test.go, which touches no seam logic.

## Push (refspec)

- git push origin HEAD:lane-0428-075-perses-seam
  push witness (fast-forward): 16adf5c3..fa41389c
- Remote verify (ls-remote, before/after):
    before: 16adf5c3d2db3039c183e1a6841fced31a131b2e	refs/heads/lane-0428-075-perses-seam
    after:  fa41389c038b449dc4cd850706a6d28f3aac59a2	refs/heads/lane-0428-075-perses-seam
    after:  fa41389c038b449dc4cd850706a6d28f3aac59a2	refs/pull/1575/head  (via `gh pr view 1575`, live)
- Base freshness on remote: `git merge-base --is-ancestor 2581000b fa41389c` -> true.

## PR #1575 status (terminal CI)

- gh pr view 1575 => state=OPEN, mergeable=MERGEABLE, head=lane-0428-075-perses-seam,
  headRefOid=fa41389c038b449dc4cd850706a6d28f3aac59a2, base=develop.
- Exact-head CI run (self-observed to terminal): run #6451, GitHub Actions run
  44023379363 (pull_request event, commit fa41389c, created 2026-11-17T05:20:13Z):
  `gh run view 44023379363 --json status,conclusion` -> completed/success (updated
  2026-11-17T05:29:24Z). All ran jobs success; remaining jobs skipped by diff-scope gating
  (no fail, no pending). This was the auto-triggered run on push — no workflow_dispatch or
  rerun triggered (GRENZEN: no .github/**; Owner scope).

## repo-rule compliance

- No .github/** edits, no merge-force, no rebase, no second branch, no subagent (§4.8).
- Work confined to the mission-named branch `lane-0428-075-perses-seam` (one candidate per chain, AGENTS 3.8).
- Evidence lives only in baseharbor-plan under evidence/r28-welle3-2026-11-16/perses-seam/.
- Planning-repo witness: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main` => e6ebc365f1bd97ebccc7cebc1950cd5df17afc1e (the real planning repo, not workers/baseharbor-plan).
- No containers/networks/compose left by this lane (cleanliness: no docker/podman projects started; ps-witness in rebase-window-1.md hopf-3 block).

## END line
END_DONE mission-1575-hopf3.md: PR #1575 hopf-3 — merged develop@2581000b (uid-app #1579), seam intersection null, candidate <new head> pushed, run <run-id> completed/success, READY.
