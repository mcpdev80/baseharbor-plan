# 0428-285 — CI operator acceptance non-interactive in Light gates (baseharbor implementation)

- Lane: w111-0428-285-operatorfix
- Card: t-20261124-ci-operator-acceptance-nontty (0428-285), claimed w111-0428-285-operatorfix
- Repo: mcpdev80/baseharbor — baseharbor-ONLY. baseharbor-demo side moved to Codex lane w115 (card 0428-284) per owner scope-correction 2026-11-24.
- Model/session: flash worker session; every step ran inside this session (§4.8). No subagents; no other session contacted.

## Remote attestations (ls-remote witnesses)

- planning repo (wrong-zone guard): `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push).
- baseharbor develop (real URL): `f14fb87c8f5afd91168e4f174d620c9f00e6341e` (refs/heads/develop).
- baseharbor-demo develop: `c23bd9ac58919302ffad3a43f43afb1a34bfbc96`.

Witness (live): `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `f14fb87c8...`.

## Base attestation (before branch)

- Branch cut from develop `f14fb87c8f5afd91168e4f174d620c9f00e6341e`.
- `git merge-base --is-ancestor f14fb87c8 19ce34eff` => f14fb87c8 is an ancestor of the commit. Cutting from another PR head would be a scope violation; this is a clean develop head.

## Ground truth (run 45432650561, head f14fb87c8 = current develop; job logs 138587494655 policy, 138587494875 reconciliation)

The operator seam is fully wired on develop (`cmd/baha/main.go:144 WithEnforcementIfAbsent`, `:148 withCIIntegrationOperator`). Fixture `cmd/baha/ci_integration_operator_enabled.go` is identical on develop and #1815 (blob 693a06199). The demo pre-release workflow already seeds the operator contract (`BASEHARBOR_DEMO_OPERATOR_GATE="$GATE"`, `GATE="$GATE"`, `DEMO_ATOMIC_GATE=1`, `BASEHARBOR_TEST_RUNTIME`) at the acceptance invocation — so the demo seeding was NOT the gap.

Operator trace (`[ci-operator-testonly] decision=... command=...`) proves:
- `up --yes`, `up --confirm-candidate`, `up --confirm-candidate <digest>`, `app apply --json [--confirm-candidate <digest>]` all stamp the scoped operator (`decision=managed-local-gate`) — these already work via `cliLocalWorkloadOperation` (apply).
- The ONE real operator-admission gap: `decision=managed-local-gate-rejected: command-not-in-managed-workload-set: policy check -e dev`. `policy explain` and `config organization set` were admitted on the policy gate; `policy check` was not.
- connectivity/reconciliation gates fail inside the `run_consented` `up --confirm-candidate` consent handshake (not an operator-admission gap) — demo-side (w115).

## PLAN

1. Done — Read mission + card; claim t-20261124-ci-operator-acceptance-nontty (pushed claim to baseharbor-plan main).
2. Done — Verified planning-repo remote + real develop SHAs via ls-remote.
3. Done — Ground-truthed failing admission from run 45432650561 policy + reconciliation job logs.
4. Done — baseharbor fixture: added `ciIntegrationPolicyCheck` admission (canonical `policy check` forms stamp the scoped test-only operator on the policy gate; other NAME/flag/gate stay fail-closed) + locked `up --confirm-candidate`/`app apply --confirm-candidate` forms in a new regression test; updated 0428-250 negative test.
5. Done — Build (`go build -tags=baseharbor_ci_operator_testonly ./cmd/baha/`) + targeted tagged test run (`-run TestCIIntegration...`) PASS. Full package test not run (needs containers; Hosted-only rule).
6. Done — Committed cleanly (two fixture files only) on top of develop f14fb87c8.
7. Done — Fixed a corrupted branch ref (phantom 36d075fad -> clean 19ce34eff), force-pushed lane-0428-285-operatorfix, verified delivery.
8. Done — Opened PR #1827 (base develop, head lane-0428-285-operatorfix).
9. In progress — Hosted CI run 45445355381 observed in_progress (not yet terminal). Left running; no new trigger.
10. STOP-IMPLEMENT + HANDOFF (owner 2026-11-24): implementation frozen pending transfer to a Codex lane.

## Repo-rule compliance

- baseharbor write-set = fixture file + test only. `git diff f14fb87c8..19ce34eff --name-only` => exactly `cmd/baha/ci_integration_operator_enabled.go`, `cmd/baha/ci_integration_operator_enabled_test.go`. No `.github/**` edit (owner-scope).
- baseharbor-demo: NO edits. `scripts/report.sh` was edited then reverted (develop blob restored) per owner scope-correction; demo PR side is Codex lane w115.
- Hosted-only: no local product/unit suite run (no `go test ./cmd/baha/` bare package; only the build-tagged targeted `TestCIIntegration` forms). No containers, no compose, no VM.
- No subagents (§4.8); no other session contacted.
- Evidence lives only in baseharbor-plan under `evidence/`; nothing added to a product repo (no `.evidence/` directory; no main-branch writes in a product repo).
- Branch provenance: cut from develop head f14fb87c8 (ancestor verified); one integration candidate, one chain.

## cleanliness

- Read-only of host runtime: no containers/compose/networks/volumes started. No stack to bring down. Session shell pid witness: this lane shell PID. `docker ps -a` / `podman ps -a` diffs empty.
- Scratch: CI job logs under /tmp/w111-*.log. Worktree `/tmp/opencode/w111-0428-285-operatorfix-wt` only.

## END

END_DONE w111-0428-285-operatorfix: baseharbor implementation of card 0428-285 done on branch `lane-0428-285-operatorfix` (commit `19ce34effe5acdd08c4acae3986c40a76aaac0e9`, clean single commit on develop f14fb87c8), PR #1827 OPEN (base develop). Fixture gains `ciIntegrationPolicyCheck` (admits canonical `policy check` forms on the policy gate; fail-closed elsewhere) and a regression test locking `up --confirm-candidate`/`app apply --confirm-candidate` (WITH/WITHOUT digest) to the policy gate; 0428-250 negative test updated. Local build + targeted tagged `TestCIIntegration` pass. CI run 45445355381 observed in_progress (terminal outcome not yet recorded). baseharbor-demo side (test-cert login + empty-Acceptance-group-header) reverted out and reassigned to Codex lane w115 (card 0428-284) per owner scope-correction 2026-11-24 — w111 touched NO demo files in final state. Implementation frozen pending owner transfer to a Codex lane; no further pushes. Claim retained for coordinator to hand off.
