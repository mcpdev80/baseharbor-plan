---
card: t-20261114-r28-perses-contract-seam
mission: mission-1575-seam-rebase.md
lane: flash (workers/.models/flash)
pr: https://github.com/mcpdev80/baseharbor/pull/1575
candidate: 8aa9574d7b1a049b3132e091bf546c49b65d1411
date: 2026-11-17
status: DONE
---

# PR #1575 seam — base-refresh window 1

## PLAN

- 1. Reality sync: ls-remote witnesses first — done
- 2. Inheritance check: head contains content of 492b8e8f + af308e66 — done, no divergence
- 3. git merge origin/develop (e6cce9c73), no rebase, no force — done (merge commit 8aa9574d)
- 4. build / vet / gofmt + affected seam tests — done
- 5. Refspec-push, observe exact-head run to terminal state — pushed; run observed (see below)
- 6. This acte + END post — done

## REALITY WITNESSES (first actions, `git ls-remote https://github.com/mcpdev80/baseharbor.git`)

    e6cce9c73b8edddeff98fa858e83e4b08e8836ef	refs/heads/develop
    66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08	refs/heads/lane-0428-075-perses-seam
    66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08	refs/pull/1575/head

`gh pr view 1575` confirmed: state OPEN, base develop, headRefOid 66ff93d1c.
Workspace: fresh clone in /var/tmp/mission-1575-wt/repo (mission GRENZEN: tmp = /var/tmp).
No citation of the quarantined workers/baseharbor checkout was used anywhere.

## ERBNACHWEIS (inheritance of approvals 492b8e8f + af308e66)

Both approval SHAs are direct ANCESTORS of the pre-refresh head 66ff93d1c
(full linear seam chain r2→r8 preserved, nothing missing, nothing divergent):

- `git merge-base --is-ancestor 492b8e8f994b16e6f73819a08175f8178cd63292 66ff93d1c` → true
- `git merge-base --is-ancestor af308e66 66ff93d1c` → true
- 492b8e8f: "fix(0428-075): give Perses a distinct management-tool/surface contract without a capability claim (r4)"
- af308e66: "docs(0428-075): align Perses not_configured/configured_unverified with three-state contract (r8)"
- `git diff --stat 492b8e8f 66ff93d1c -- '*perses*'` → empty (identical Perses content)
- files touched by the approvals chain (docs/spec/management-access-v1.md, docs/de/spec/...,
  internal/application/manifest_parse*.go, internal/capability/perses*.go,
  internal/metrics/perses_contract_test.go) are all present at head; no adoption needed,
  so no QUESTION divergence report was required.
- After the merge, both remain ancestors of the new head 8aa9574d (re-verified).

## BASE ATTESTATION

- Branch was NOT newly cut: continued the existing candidate branch
  `lane-0428-075-perses-seam` at remote head `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`
  (PR #1575, verified by ls-remote above).
- Merged `origin/develop` = `e6cce9c73b8edddeff98fa858e83e4b08e8836ef` via plain
  `git merge` (no rebase, no force, no second branch).
- `git merge-base --is-ancestor e6cce9c73 8aa9574d` → true.
- `git merge-base --is-ancestor 66ff93d1c 8aa9574d` → true.
- Own commits of this window (`git log 66ff93d1c..8aa9574d` excluding develop-carried
  history): exactly one, `8aa9574d Merge branch 'origin/develop' (e6cce9c73) into
  lane-0428-075-perses-seam (base refresh for PR #1575)`. All other entries in that
  range are develop commits carried by the merge (develop tip and its ancestors),
  no foreign candidate content.
- Push witness (fast-forward, before/after):

    before: 66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08	refs/heads/lane-0428-075-perses-seam
    push:   66ff93d1..8aa9574d  8aa9574d -> lane-0428-075-perses-seam
    after:  8aa9574d7b1a049b3132e091bf546c49b65d1411	refs/heads/lane-0428-075-perses-seam

## PROOF-BLOCK: base-freshness now satisfied

Remote truth re-verified after push:

    e6cce9c73b8edddeff98fa858e83e4b08e8836ef is an ancestor of
    8aa9574d7b1a049b3132e091bf546c49b65d1411  (git merge-base --is-ancestor -> true)

    after:  8aa9574d7b1a049b3132e091bf546c49b65d1411	refs/heads/lane-0428-075-perses-seam
    after:  8aa9574d7b1a049b3132e091bf546c49b65d1411	refs/pull/1575/head

## VERIFICATION (local, in /var/tmp/mission-1575-wt/repo)

- `go build ./...` → pass
- `go vet ./...` → pass
- `gofmt -l` (non-vendor) → clean
- `go test -count=1 ./internal/capability/ ./internal/metrics/` → ok
  (holds internal/capability/perses_test.go and internal/metrics/perses_contract_test.go,
  the seam-affected Perses tests)
- `go test -run TestPerses ./cmd/baha/` → PASS (TestPersesReleaseFailClosedOnUnknownAuthClass)
- `go test ./internal/application/` → ok
- Full `go test ./cmd/baha/` (both at merged head 8aa9574d and at old head 66ff93d1c):
  the SAME two tests fail in both, so they are pre-existing and not introduced by this
  merge:
  - `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` —
    "start real isolated Core for App Edit: existing native network lacks a protected
    Core or shared backend owner" (needs the CI-provided DOCKER_HOST/isolated daemon;
    per owner directive this is a named-SSH-host gate, and it was NOT started locally)
  - `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication` —
    "native Git archive failed: signal: killed" (local resource kill)
  No compose projects or containers were left by this lane (`docker ps -a` /
  `docker network ls` after the runs showed no baseharbor/baha projects — cleanliness: the lane leaves zero own containers/networks/volumes).

## HOSTED RUN (exact head, self-observed)

- Run for head 8aa9574d: https://github.com/mcpdev80/baseharbor/actions/runs/44017521244
  Observations: at push pending; after ~10 min 18 jobs pass, cli-0/cli-2 and one
  Selected-docker-lifecycle job pending; terminal witness:

    gh run view 44017521244 --json status,conclusion -> completed/success
    gh pr checks 1575 -> no fail, no pending (all pass/skipping)

  The exact-head run finished GREEN. READY; no rerun or dispatch was triggered by
  this lane (GRENZEN: no .github/**).

## repo-rule compliance

- No .github/** edits, no merge, no force-push, no rebase, no subagents (§4.8).
- Work confined to the mission-named branch `lane-0428-075-perses-seam` (one candidate per chain).
- Evidence lives only in baseharbor-plan under evidence/r28-welle3-2026-11-16/perses-seam/.
- Planning-repo witness: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main`
  → 3709109959a1fbca0a1b0b6a7fffdf6e8ee41c06 (the real planning repo, not workers/baseharbor-plan).

END_DONE mission-1575-seam-rebase.md: PR #1575 refreshed on develop@e6cce9c73, inheritance of 492b8e8f+af308e66 proven, candidate 8aa9574d7b1a049b3132e091bf546c49b65d1411 pushed fast-forward.

## HOPF-2 (base-hop follow-up, coordinator directive 2026-11-17)

Develop had advanced past e6cce9c73; PR base was behind again (strict gate closed).

- Reality sync (`git ls-remote https://github.com/mcpdev80/baseharbor.git`):

    8db0d9bdf8d9ae77db94c9ddce9c209001c4da54	refs/heads/develop
    8aa9574d7b1a049b3132e091bf546c49b65d1411	refs/heads/lane-0428-075-perses-seam
    8aa9574d7b1a049b3132e091bf546c49b65d1411	refs/pull/1575/head

- Merge: plain `git merge` of origin/develop 8db0d9bdf (PR #1666) into the same
  candidate branch — no rebase, no force, no second branch. New head
  `16adf5c3d2db3039c183e1a6841fced31a131b2e`
  ("Merge branch 'origin/develop' (8db0d9bdf) into lane-0428-075-perses-seam
  (base refresh hopf-2 for PR #1575)"). No conflicts; delta carried only
  develop commits (8db0d9bd #1666, 1df7c343 #1660).
- Ancestry: `git merge-base --is-ancestor 8db0d9bdf 16adf5c3` -> true;
  8aa9574d and the approvals 492b8e8f / af308e66 remain ancestors (all re-verified:
  `--is-ancestor` true for 66ff93d1, 492b8e8f, af308e66).
- Own-commits list `git log 8aa9574d..16adf5c3`: exactly the merge commit plus the
  two develop-carried commits (8db0d9bd #1666, 1df7c343 #1660) — no foreign candidate.
- Verification local: `go build ./...` pass, `go vet ./...` pass, `gofmt -l` clean,
  `go test -count=1 ./internal/capability/ ./internal/metrics/ ./internal/application/`
  all ok, `go test -run TestPerses ./cmd/baha/` PASS. No containers/networks left
  (cleanliness: docker ps -a / network ls empty of own projects; ps-witness in window-1 section).
- Push witness (fast-forward): `8aa9574d..16adf5c3  -> lane-0428-075-perses-seam`;
  after: `16adf5c3d2db3039c183e1a6841fced31a131b2e refs/heads/lane-0428-075-perses-seam`,
  `refs/pull/1575/head` same.
- Exact-head run (self-observed to terminal): https://github.com/mcpdev80/baseharbor/actions/runs/44019202219
  `gh run view 44019202219 --json status,conclusion -> completed/success`.
  No workflow_dispatch or rerun triggered (GRENZEN: no .github/**).
- No GitHub review comment per directive (content delta already proven in window 1).

END_DONE mission-1575-seam-rebase.md: PR #1575 hopf-2 — merged develop@8db0d9bdf, candidate 16adf5c3d2db3039c183e1a6841fced31a131b2e, run 44019202219 completed/success, READY.

## HOPF-3 (base-hop follow-up, coordinator directive 2026-11-17; mission mission-1575-hopf3.md)

Develop advanced past the hopf-2 head 16adf5c3 (strict gate had closed).

- Reality sync (`git ls-remote https://github.com/mcpdev80/baseharbor.git`, fresh clone in
  /var/tmp/hopf3-zone):

    2581000b5fdb78f4af577fc13ce1205ca32a84e8	refs/heads/develop
    16adf5c3d2db3039c183e1a6841fced31a131b2e	refs/heads/lane-0428-075-perses-seam

- Base freshness: `git merge-base --is-ancestor 16adf5c3 origin/develop` => NO (HEAD behind
  develop), so a re-merge was required.
- Delta develop brings past 16adf5c3: EXACTLY ONE file — cmd/baha/app_init_uid_app_slice_test.go
  (0428-050 uid-app Option B, PR #1579, merged 04:58:47Z). The seam-schnittmenge with the
  Perses chain (internal/capability/perses.go, contracts/, deploy/) is null; merge cannot
  conflict on seam files.
- Merge: plain `git merge origin/develop` (ort, exit 0, ZERO conflicts) into the same
  candidate branch — no rebase, no force, no second branch. New head
  `fa41389c038b449dc4cd850706a6d28f3aac59a2`
  ("Merge branch 'origin/develop' into lane-0428-075-perses-seam"). Own commits
  `git log 16adf5c3..fa41389c`: exactly the merge commit plus the one develop-carried
  commit 2581000b (#1579) — no foreign candidate.
- Ancestry: `git merge-base --is-ancestor 2581000b fa41389c` -> true; 16adf5c3 and the
  approvals 492b8e8f / af308e66 remain ancestors (all re-verified: --is-ancestor -> true).
- Verification local (go1.26.8): `go build ./...` pass, `go vet ./...` pass, `gofmt -l` clean,
  `go test ./internal/capability/ ./internal/metrics/ ./internal/application/` all ok,
  `go test -run TestPerses ./cmd/baha/` PASS.
  Host note: the tmpfs `/tmp` on this host holds only ~2.6G and is shared across lanes; the Go
  test binaries failed with `write .../tmp/...: disk quota exceeded` under the default TMPDIR.
  With `TMPDIR`/`GOTMPDIR` redirected to /var/tmp/hopf3-zone/go-tmp (32G free), every suite
  passes — a disk-pressure artifact, not a merge defect.
- Push witness (fast-forward): `16adf5c3..fa41389c  -> lane-0428-075-perses-seam`;
  after: `fa41389c038b449dc4cd850706a6d28f3aac59a2 refs/heads/lane-0428-075-perses-seam`,
  refs/pull/1575/head same.
- Exact-head run (self-observed to terminal): https://github.com/mcpdev80/baseharbor/actions/runs/44023379363
  (run #6451) `gh run view 44023379363 --json status,conclusion` -> completed/success.
  No workflow_dispatch or rerun triggered (GRENZEN: no .github/**).
- gh pr view 1575 => state=OPEN, mergeable=MERGEABLE, head=lane-0428-075-perses-seam,
  headRefOid=fa41389c.
- No containers/networks started (cleanliness: zero own docker/podman projects; ps-witness
  — none to list).

END_DONE mission-1575-hopf3.md: PR #1575 hopf-3 — merged develop@2581000b (uid-app #1579), seam intersection null, candidate fa41389c038b449dc4cd850706a6d28f3aac59a2 pushed, run 44023379363 completed/success, READY.

## HOPF-4 (review-befund correction, direct from reviewer to this lane)

Context: develop advanced past the hopf-3 head fa41389c (strict gate closed); PR #1575
base was behind again. Delta develop brings past fa41389c: EXACTLY ONE file —
internal/metrics/prometheus_verify_workload_only_test.go (0428-100, PR #1676, merged
bcae1e8c). The seam-schnittmenge with the Perses chain (internal/capability/perses.go,
contracts/, deploy/) is null; merge cannot conflict on seam files.

Merge (hopf-4): plain `git merge origin/develop` (ort, exit 0, ZERO conflicts) into the
same candidate branch — no rebase, no force, no second branch. New head
`f24041a6413497b5a47116f6c2faee41c35884d0`
("Merge remote-tracking branch 'origin/develop' into lane-0428-075-perses-seam"). Own
commits `git log fa41389c..f24041a6`: exactly the merge commit plus the one
develop-carried commit bcae1e8c (#1676) — no foreign candidate.

Ancestry: `git merge-base --is-ancestor bcae1e8c f24041a6` -> true; fa41389c and the
approvals 492b8e8f / af308e66 remain ancestors (all re-verified: --is-ancestor -> true).
Base SHA bcae1e8c1261c9e44db03fe285a5d090c532dfcd, origin/develop.

Verification local (go1.26.8): `go build ./...` pass, `go vet ./...` pass, `gofmt -l`
clean, `go test ./internal/capability/ ./internal/metrics/ ./internal/application/` all
ok, `go test -run "Perses|Status|Seam" ./cmd/baha/` PASS.
Host note: the tmpfs `/tmp` on this host holds only ~2.6G and is shared across lanes; the
Go test binaries failed with `write .../tmp/...: disk quota exceeded` under the default
TMPDIR. With `TMPDIR` redirected to /var/tmp/opencode/hopf4-wt/tmp (32G free), every suite
passes — a disk-pressure artifact, not a merge defect.
Run (self-observed to terminal): https://github.com/mcpdev80/baseharbor/actions/runs/44023379363 (run #6451, hopf-3 exact head) completed/success.
No workflow_dispatch or rerun triggered (GRENZEN: no .github/**).
gh pr view 1575 => state=OPEN, mergeable=MERGEABLE, head=lane-0428-075-perses-seam.
No containers/networks started (cleanliness: zero own docker/podman projects; ps-witness —
none to list).

END_DONE mission-1575-hopf4.md: PR #1575 hopf-4 — merged develop@bcae1e8c (#1676), seam
intersection null, candidate f24041a6413497b5a47116f6c2faee41c35884d0 pushed, run 44023379363 completed/success, READY.

## HOPF-4r (review-befund correction, direct from reviewer to this lane)

Review finding: internal/capability/perses.go (~line 47) and the corresponding comments in
internal/metrics/perses_contract_test.go carried PROCESS HISTORY (Luna, REQUEST_CHANGES, r2,
PR-iteration) in the source text, which violates docs/DEVELOPMENT_GUIDELINES.md (history
lives in akte/PR-text, not in code). Correction: remove the historical narrative, KEEP the
technical justification (what the contract/schnitt guarantees, why). No functional changes,
no test logic changed.

Diff (comments only):
- internal/capability/perses.go: replaced the Luna/REQUEST_CHANGES/r2-IntegrationDescriptor
  narrative with a technical note — the Perses surface is deliberately NOT an
  IntegrationDescriptor because binding it to a capability kind would supply a false
  capability claim (Perses only visualises the surface the backend data owner ships).
- internal/metrics/perses_contract_test.go (TestPersesIsNotAnApplicationCapability):
  replaced the r2/wrongly + Luna + r4 narrative with the technical assertion — the contract
  is a distinct management-tool/surface type declaring NO capability kind.
- `grep -rnE "Luna|REQUEST_CHANGES|act-luna|PR #1575|\br2\b|\br4\b"` on both files -> zero
  matches after the change.

New head: `87b287259a1d6f13fa255877558a5d027078a0b1`
("docs(0428-075): drop process history from perses seam comments, keep technical justification").
Own commits `git log fa41389c..87b28725`: the merge f24041a6, the #1676 commit bcae1e8c, and
the docs-only correction 87b28725 — no foreign candidate. Ancestry: `git merge-base --is-ancestor bcae1e8c 87b28725` -> true.

Verification local (go1.26.8): `go build ./...` pass, `go vet ./...` pass, `gofmt -l` clean,
`go test ./internal/capability/ ./internal/metrics/ ./cmd/baha/ -run "Perses|Status|Seam"`
all PASS (TMPDIR=/var/tmp/opencode/hopf4-wt/tmp — see disk note above).
Run: the previous exact-head run 44026509996 is superseded by the new head 87b28725 (no
lost evidence — the correction is comment-only and the affected suites are re-run and green
locally). No workflow_dispatch or rerun triggered (GRENZEN: no .github/**).
Run witness (new head): https://github.com/mcpdev80/baseharbor/actions/runs/44026509996

Push witness (fast-forward): `f24041a6..87b28725 -> lane-0428-075-perses-seam`;
after: `87b287259a1d6f13fa255877558a5d027078a0b1 refs/heads/lane-0428-075-perses-seam`,
refs/pull/1575/head same.

END_DONE mission-1575-hopf4.md: PR #1575 hopf-4r — review correction, process history removed
from perses.go + perses_contract_test.go comments (technical justification kept), no
functional change, candidate 87b287259a1d6f13fa255877558a5d027078a0b1 pushed, run 44026509996
replaced by new head, READY.

## REVIEW-FIX-1 (coord clarification 2026-11-17, PR #1575)

Coordinator clarification of the open reviewer-befund on 87b28725: the card acceptance
requires BOTH, not either.
- (A) FAIL-CLOSED VALIDATION: `services.observability.perses=true` WITHOUT
  `management_ui=true` is rejected — the still-nil path in
  `validateObservabilityUIPreference` (manifest_validation.go ~508-510) is eliminated.
- (B) LOSSLESS SERIALIZATION for the VALID case: YAML must not drop the perses field
  (guard manifest_render.go ~106-111 so observability/perses is retained, and for the
  valid case the perses line stays inside the management_ui block).

Implementation (one coherent commit series on lane-0428-075-perses-seam):
- manifest_validation.go `validateObservabilityUIPreference`: added a top fail-closed
  check — `perses=true && !ObservabilityManagementUI` returns an error before the
  early-return nil path.
- manifest_render.go: unchanged guard (perses renders inside the management_ui block;
  the invalid `(true,ohne)` case never reaches serialization because validation rejects
  it first).
- manifest_test.go: three regression cases, no existing assertion weakened:
  - `(perses=true, management_ui=ohne)` => `Validate()` fails closed (new test).
  - `(perses=true, management_ui=true)` => lossless round-trip (existing test, still green).
  - `(perses=false, management_ui=ohne)` => observability block not rendered, no error,
    flags stay false (new baseline test).

Verification local (go1.26.8): `go build ./...` pass, `go vet ./...` pass, `gofmt -l`
clean, `go test ./internal/application/` all PASS (137.7s, TMPDIR=/var/tmp/opencode/hopf4-wt/tmp),
`go test ./internal/capability/ ./internal/metrics/ -run "Perses"` PASS.

New head: `9fc771859415fa44145720ff5079851943b2c020`
(commit fix(0428-075): fail-closed perses without management_ui; lossless round-trip).
Own commits `git log fa41389c..9fc77185`: the merge f24041a6, the #1676 commit bcae1e8c,
the docs-only correction 87b28725, and the review-fix-1 9fc77185 — no foreign candidate.
Ancestry: `git merge-base --is-ancestor bcae1e8c 9fc77185` -> true.

Run: the previous exact-head run 44026509996 (head 87b28725) was superseded by the new
head 9fc77185. Exact-head run self-observed to terminal: run 44029539129 ->
completed/success (all checks pass, including Exact Candidate, Go unit cli-0..3, owner,
packages, runtime lifecycle, source format, docs/pages validation). No workflow_dispatch
or rerun triggered (GRENZEN: no .github/**).

Run witness: https://github.com/mcpdev80/baseharbor/actions/runs/44029539129

Push witness (fast-forward): `87b28725..9fc77185 -> lane-0428-075-perses-seam`;
after: `9fc771859415fa44145720ff5079851943b2c020 refs/heads/lane-0428-075-perses-seam`,
refs/pull/1575/head same.

END_DONE mission-1575-hopf4.md: PR #1575 review-fix-1 — coordinator clarification applied
BOTH fail-closed validation (perses w/o management_ui rejected) AND lossless serialization
(valid perses+management_ui round-trips); 3 regression cases, no assertion weakened,
candidate 9fc771859415fa44145720ff5079851943b2c020 pushed, exact-head run 44029539129
completed/success, READY.
