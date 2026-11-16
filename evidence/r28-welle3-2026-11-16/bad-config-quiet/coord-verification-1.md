# 0428-094 · coord-verification 1 (lane-end substitute, documented)

Lane 3059a081 delivered the batch18 Object-1 recipe in code but its END post never routed to the
coordinator inbox (post-routing defect, queue 148 pattern; lane pane shows it repeatedly declaring
"END posted" while the coordinator-side inbox has no such message since batch17).

## Recipe coverage (verified by coordinator against remote refs, 2026-11-16 23:4xZ)

- Luna batch18 recipe: LoadConfig integration case with `XDG_CONFIG_HOME=<temp>/.config/baseharbor`,
  intended config.yaml at that root, nested resolved path absent, assert `errors.Is(err, ErrConfigMissing)`.
- Candidate head `4f2906c6b` (diff vs fe00c7f18 = +28 lines, single test file):
  `internal/deployment/config_fail_loud_test.go:191/:209` implement exactly the double-append
  resolution (`ConfigPath() resolves to <root>/baseharbor/...`), the ErrConfigMissing assertion
  family is present at :35/:50-51 (matrix retained from round 2).
- PR #1666: draft=true, base=develop, head == `4f2906c6b` (gh-zeug).
- Exact-head pull_request run `43979087744`: completed SUCCESS (gh-zeug).

## Disposition

Card 0428-094 -> review (candidate + witnesses complete). This note stands in for the missing
worker akte round-3; no code claim is made here that is not backed by the cited remote evidence.
