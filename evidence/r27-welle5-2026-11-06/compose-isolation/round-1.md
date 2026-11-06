# w205 compose host isolation — Round 2 (r27 compose-host-isolation)

- Lane: w205 (Worker). Coordinator: 841e7734
- Task card: t-20261105-r27-compose-host-isolation (Runde 2 design mandate: per-test fresh isolated Core, no shared live daemon)
- Candidate branch: work/r27-compose-isolation, head 3fcba08f6a5 — PR #1383 (the single integration candidate for the r27 chain)
- Mission file: coordinator/missions/w205-compose-isolation.txt

## PLAN (work plan, ticked as worked)

- Read mission + task card; confirm candidate branch work/r27-compose-isolation @ 3fcba08f (PR #1383) is the one integration candidate; restore local + own worktree to origin head.
- Base attestation: latest develop 512dcd72 (origin/develop 21d8d05) is ancestor of first commit 3fcba08f.
- Build candidate (go build -buildvcs=false ./cmd/baha); go vet; gofmt check.
- Red-first on baha-docker: run 4 tests against deliberately polluted shared state with isolation disabled -> expect >=1 cell RED; document failing log line.
- Clean-state green: run all 4 cells on baha-docker with BASEHARBOR_CI_RUNTIME_INTEGRATION=1; all PASS.
- Parallel independence: run 2 cells simultaneously on baha-docker; separate project names in ps; both PASS.
- Mutant: disable per-test isolation on baha-docker; at least one cell RED at the bootstrap-core gate; capture verbatim.
- Space phase: docker compose down each test project; ps -a free of lane names; df -l line into evidence.
- Commit evidence to baseharbor-plan evidence path; push; confirm path on origin/main via ls-tree; log lists ONLY my own commits.
- Final teardown: down all test projects on baha-docker; ps witness; END_DONE to 841e7734.

## Base attestation (provenance)

- origin/develop head: 21d8d05cf1acf04729077e05eb350fcd3bb018ed
- latest develop commit present as ancestor of candidate: 512dcd721ac3fb739bfd4cb0b990fd68d6794762 (git merge-base --is-ancestor rc=0)
- Candidate head cut from: 3fcba08f6a555df1143db846feb5464035adb4b4 (work/r27-compose-isolation, PR #1383)
- The branch is a long-lived integration candidate merged through multiple develops; its working base for this lane is the current candidate head, which carries latest develop as ancestor. No second branch invented.
- Evidence path (baseharbor-plan only, never a product repo): evidence/r27-welle5-2026-11-06/compose-isolation/round-1.md

## Repo-rule compliance

- Product repo (mcpdev80/baseharbor) never modified: no .github edits, no workflow_dispatch/reruns, no product writes. This lane only RUNS the candidate's tests via SSH on the named SSH host baha-docker and records transcripts.
- No subagents: every step executed in this session.
- No containers started on the coordinator/codeman host; all runtime work via SSH on baha-docker.
- One candidate per chain: continued on work/r27-compose-isolation / PR #1383.

## END status

- Pending (work in progress).
