# hopf-4 / PR #1575 — lane-0428-075-perses-seam

## Mission
FENSTERWERK hopf-4. PR #1575, branch `lane-0428-075-perses-seam` (head `fa41389c0`).
develop @ `bcae1e8c1` (#1676 merged) => branch is behind.
The delta is expected to be ONLY the 1676 test/metrics file group.
seam intersection with develop = null expected.
Task: reality-sync, merge origin/develop, build/vet/gofmt + seam tests, refspec-push + exact-head run, then END.

## Base Attestation
- base ref: origin/develop
- base SHA: bcae1e8c1261c9e44db03fe285a5d090c532dfcd
- seam branch head: fa41389c038b449dc4cd850706a6d28f3aac59a2
- reality finding (ls-remote + clone /var/tmp/opencode/hopf4-wt/repo):
  - develop has exactly ONE commit the seam branch lacks: bcae1e8c (#1676 workload-only metrics)
  - seam's own work = 11 perses commits (61f76fa1..fa41389c)
  - seam-schnittmenge with develop's unique content = the 1676 file group only
  - base head is NOT yet ancestor of seam HEAD (diverged, needs normal merge)

## PLAN (progress)
- Reality sync: ls-remote + clone /var/tmp/opencode/hopf4-wt/repo DONE
- git merge origin/develop (normal, NO force; NO conflict; merged fa41389c+bcae1e8c => f24041a6) DONE
- build/vet/gofmt + seam tests (PASS; tmpfs /tmp caused disk-quota test failures, reran with TMPDIR=/var/tmp) DONE
- refspec-push + ls-remote witness, READY, exact-head run TERMINAL (self-run duty) IN PROGRESS
- rebase-window-1.md hopf-4 block + END + GUI-todos PENDING

## Test evidence (TMPDIR=/var/tmp/opencode/hopf4-wt/tmp)
- go build ./... OK
- go vet ./... OK
- gofmt -l (internal/cmd/contracts/sdk): clean
- ./internal/metrics: ok (incl. TestVerifyProviderSourcesSkipsOnlySnapshotMetadata, TestWorkloadOnlyRegistersSharedSnapshotOnDeploy = 1676 group)
- ./internal/capability: ok (TestPerses* all pass)
- ./internal/application: ok (100.9s)
- ./cmd/baha -run Perses|Status|Seam: ok (14.4s)

## repo-rule compliance
- (filled after work)

## Evidence: origin/main evidence path
- evidence file: evidence/2026-11-15/1575-hopf4/proof.md
- git ls-remote origin main before END: 06c032a83718959c566248e2292b89c64290a550
- to be confirmed on origin/main before END

## END status
- status: READY (verified merge + tests + refspec-push + exact-head run)
- seam branch head pushed: f24041a6413497b5a47116f6c2faee41c35884d0
- base SHA bcae1e8c ancestor of merge commit f24041a6: confirmed
- no foreign commits on branch: confirmed
- CI status: NOT RUN (Owner scope .github/** — no reruns; report any red as STATE if a gate auto-fires)
