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
- docker/podman/compose test stacks: NONE started this shift — nothing to bring DOWN (ps-witness: bh-* containers are pre-existing shared-host services, not mine)
- evidence origin/main: de0c9201

## REVIEW CORRECTION (hopf-4r, reviewer -> this lane)
- Review finding: process history (Luna/REQUEST_CHANGES/r2/PR-iteration) in source text
  of internal/capability/perses.go (~L47) and internal/metrics/perses_contract_test.go
  violated docs/DEVELOPMENT_GUIDELINES.md (history lives in akte/PR-text, not code).
- Correction: removed the historical narrative, kept the technical justification
  (what the contract/schnitt guarantees, why). NO functional change, NO test-logic change.
- New head: 87b287259a1d6f13fa255877558a5d027078a0b1
  (commit docs(0428-075): drop process history from perses seam comments).
- Verified: go build/vet/gofmt clean; ./internal/capability, ./internal/metrics,
  ./cmd/baha -run Perses|Status|Seam all PASS (TMPDIR=/var/tmp/opencode/hopf4-wt/tmp).
- refspec-pushed f24041a6..87b28725 -> lane-0428-075-perses-seam (remote 87b28725).
- Previous exact-head run 44026509996 superseded by new head (comment-only change;
  affected suites re-run green locally — no lost evidence).
- rebase-window-1.md hopf-4 block appended; evidence on origin/main blob 2c15df07.
- END_DONE mission-1575-hopf4: PR #1575 seam-schnittmenge null verifiziert; review
  correction applied (process history removed, tech justification kept); candidate
  87b287259a1d6f13fa255877558a5d027078a0b1 pushed; READY.

## REVIEW-FIX-1 (coord clarification 2026-11-17, PR #1575)
- Coord: card acceptance requires BOTH — (A) fail-closed validation AND (B) lossless
  serialization for the valid case.
- (A) manifest_validation.go validateObservabilityUIPreference: added fail-closed check —
  perses=true without observability.management_ui returns an error (no still-nil path).
- (B) manifest_render.go: unchanged guard (perses stays inside management_ui block);
  invalid (true,ohne) never serializes because validation rejects it.
- (C) manifest_test.go: three regression cases, no existing assertion weakened —
  (true,ohne)=>error, (true,true)=>lossless round-trip, (false,ohne)=>ignored baseline.
- New head: 9fc771859415fa44145720ff5079851943b2c020
  (commit fix(0428-075): fail-closed perses without management_ui; lossless round-trip).
- Verified: go build/vet/gofmt clean; ./internal/application full PASS (137.7s);
  ./internal/capability + ./internal/metrics Perses PASS.
- refspec-pushed 87b28725..9fc77185 -> lane-0428-075-perses-seam (remote 9fc77185).
- Exact-head run 44029539129 -> completed/success (all checks pass incl. Exact Candidate,
  Go unit cli-0..3, owner, packages, runtime lifecycle, source format, docs/pages).
  Previous run 44026509996 superseded. No workflow_dispatch/rerun (GRENZEN: no .github/**).
- rebase-window-1.md review-fix-1 block appended.
- END_DONE mission-1575-hopf4: PR #1575 — fail-closed validation + lossless serialization;
  candidate 9fc771859415fa44145720ff5079851943b2c020 pushed, run 44029539129 completed/success, READY.
