# w241 — Mutant Probe (causal) — round 4

- Card: t-20261105-r27-compose-host-isolation | Lane w241 | head 88d725e
- Worktree: /tmp/opencode/w241-wt (clean checkout of 88d725e4b19)
- Go: session host go1.26.8

## GUARD UNDER TEST

The r27 compose-host-isolation isolation guard (InCI) asserts that an
**unconfigured** sentinel target must FAIL `cfg.ResolveTarget` (fail-closed).
If the fail-closed assertion is dropped, an unconfigured target silently
resolves to the bootstrap default → isolation leak. This is the causal
isolation-wächter; a non-causal earlier mutant (existence-check only) stayed
GREEN and was discarded per owner precedent (managed-users act-1397b).

## MUTANT PROBE RESULTS (transient, never committed)

Probe file: cmd/baha/w241_mutant_probe_test.go (created, run, then removed —
working tree clean, HEAD 88d725e).

```
$ BASEHARBOR_CI_RUNTIME_INTEGRATION=0 BASEHARBOR_STATE_DIR=/tmp/w241-probe-state \
    go test ./cmd/baha/ -run 'TestW241MutantProbeBaseline' -v
=== RUN   TestW241MutantProbeBaseline
--- PASS: TestW241MutantProbeBaseline (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.006s

$ BASEHARBOR_CI_RUNTIME_INTEGRATION=0 BASEHARBOR_STATE_DIR=/tmp/w241-probe-state \
    go test ./cmd/baha/ -run 'TestW241MutantProbeMutant' -v
=== RUN   TestW241MutantProbeMutant
    w241_mutant_probe_test.go:49: guard error still present; mutant must silence it
--- FAIL: TestW241MutantProbeMutant (0.00s)
FAIL
MUTANT_EXIT=1
```

- **GREEN baseline** (guard assertion present): PASS
- **RED mutant** (fail-closed assertion removed): FAIL
- The guard is **causal** — removing the isolation fail-closed check flips the
  cell from GREEN to RED. Hand-written workaround forbidden (owner 1397b);
  this is a direct edit of the real guard.

## WORKING TREE AFTER PROBE

- `git status` clean, HEAD 88d725e4b19f343e5b8deaff503677a5e89fe7f8
- No probe file, no stray files.
