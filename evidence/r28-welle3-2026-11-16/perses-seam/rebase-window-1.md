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
  (observed pending→running at push; per GRENZEN this lane never triggers
  workflow_dispatch or reruns and does not edit .github/**; the run's terminal
  outcome belongs to the watchers/next window — READY is kept).

## repo-rule compliance

- No .github/** edits, no merge, no force-push, no rebase, no subagents (§4.8).
- Work confined to the mission-named branch `lane-0428-075-perses-seam` (one candidate per chain).
- Evidence lives only in baseharbor-plan under evidence/r28-welle3-2026-11-16/perses-seam/.
- Planning-repo witness: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main`
  → 3709109959a1fbca0a1b0b6a7fffdf6e8ee41c06 (the real planning repo, not workers/baseharbor-plan).

END_DONE mission-1575-seam-rebase.md: PR #1575 refreshed on develop@e6cce9c73, inheritance of 492b8e8f+af308e66 proven, candidate 8aa9574d7b1a049b3132e091bf546c49b65d1411 pushed fast-forward.
