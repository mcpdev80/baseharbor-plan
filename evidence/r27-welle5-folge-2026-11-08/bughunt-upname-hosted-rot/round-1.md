# 0427-181 — TestUpNameResumesThroughCommandEntrypoint hosted rot

- Card: 0427-181 (task `t-20261109-0427-181-upname-entrypoint-hosted-rot`, kanban active, owner `lane-0427-181-impl`)
- Shift: r27-welle5-folge-2026-11-08 · Lane: w286 (session 594fd2f5-4e80-43b6-9841-92879146a85e)
- Repo pin: mcpdev80/baseharbor
- Base: develop `fea92f379e55bbe6e143a095d7c2e6c16e0b3a06` (exact SHA of the ref cut from)
- Planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY (NOT `workers/baseharbor-plan`)
- Planning origin/main HEAD at evidence write time: see `git ls-remote origin main` below

## PLAN

- Attest zone + base: worktree `/tmp/opencode/m181-wt` cut from `origin/develop fea92f379` (mission base), branch `w286-0427-181-upname-hosted`. Planning repo `origin/main` HEAD `b69cbccd` before my evidence commit.
- Diagnose root cause of the full-hosted-matrix failure.
- Implement hermetic test isolation in `cmd/baha` (`*_test.go` only).
- Local checks: build, vet, focused unit test, docker cleanliness.
- Hosted proof: green `go-unit-tests` group on a full matrix develop run with `--- PASS: TestUpNameResumesThroughCommandEntrypoint` present.
- Hygiene + terminal END.

## Repo-rule compliance

- Write-set restricted to `*_test.go` under `cmd/baha` (production code untouched; no justification needed).
- No `.github/**` edits, no workflow reruns, no `workflow_dispatch` by me beyond the required hosted proof run.
- No subagents (4.8): every step run inside this session.
- Evidence committed to the planning repo (origin/main), never to the product repo.
- One integration candidate branch `w286-0427-181-upname-hosted` cut from `fea92f379`; foreign commits never carried on top.

## Hosted proof

- (pending — push candidate, then hosted develop matrix run)

## END

- (pending)
