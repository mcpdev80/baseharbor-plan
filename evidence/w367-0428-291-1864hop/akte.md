# w367-0428-291-1864hop — Re-hop PR #1864 (card 0428-291) onto current develop + fresh exact-head CI

## Status: END_BLOCKED — ACCEPTED by Owner (2026-11-27T03:56:23Z); no further task until after the 284-transport (ticket #179)

## Diagnosis (accepted)
- Branch HEAD b9675cc0b carries TWO foreign merge commits by prior lane w358-0428-291-1864hop on top of the card fix c945b2fcb (author w333) → single-writer scope violation.
- HEAD unmerged into live develop ea5218d72 (merge-base c167fa5d; ~18 develop commits advanced); the last w358 merge also pulled 120 lines of 0428-344 catalog rows into scripts/pr-gate-coverage.json (off-write-set).
- Card blocker (w267 HOLD 7206173319 on b9675cc0): develop catalog row source.cmd_baha_app_init_runtime_permission_scope_test_go lacks runtime_specific:true → only Docker native gate runs; card requires BOTH native paths (card lines 59-69). Fix = baseline family #136/0428-359 landing the row. Product-side/Owner action, not a worker transport.
- Prior lane w358 already performed hop + fresh CI run 45907132239 (all required checks SUCCESS).

## Clean single-writer hop (built locally, NOT pushed — remains a handoff candidate)
- Fresh branch from live develop ea5218d72, apply ONLY the 3 card 0428-291 files (the exact develop-diff that exists in branch HEAD vs develop), canonical identity w367-0428-291-1864hop.
- Local commit e54077256b3e25b763d9c75ffd0daaaaa3067155 — 3 files changed, +208/-4, gofmt clean, go build ./cmd/baha exit 0, go vet ./cmd/baha exit 0, canonical author+committer w367-0428-291-1864hop.
- git log origin/develop..e54077256 lists ONLY this commit (single writer). NOT pushed; PR #1864 head still b9675cc0b.
- Patch snapshot at /tmp/card0428291.diff.
- A correct handoff: push e54077256 to the named branch w333-0428-291-capperms-fix as the single-writer hop head, then fresh exact-head Hosted CI watching BOTH native Docker + Podman gates.

## Evidence on plan main
- evidence/w367-0428-291-1864hop/akte.md (plan PR #177 squash-merged, on origin/main).

## END
END_BLOCKED w367-0428-291-1864hop: card 0428-291 PR #1864 hop — branch HEAD b9675cc0b not single-writer (two foreign w358 merge commits), unmerged into live develop ea5218d72; card blocker is baseline family #136/0428-359 catalog prerequisite (source.cmd_baha_app_init_runtime_permission_scope_test_go needs runtime_specific:true). Prior lane w358 already hop+CI run 45907132239. Clean single-writer hop built locally as e54077256 (not pushed); awaiting next task (post 284-transport, ticket #179). No containers started, no remote touched.
