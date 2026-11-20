# 0428-143 · Verification=none is ignored — evidence (round 1)

- Card: t-20261119-r28-app-source-verification-none-ignored (0428-143)
- Lane: w203-0428-143-vernone (session ornith)
- Release: v0.4.28
- Date: 2026-11-20

## PLAN

1. Reality check: read mission + card, confirm planning remote (baseharbor-plan) and product remote (lane-origin = https://github.com/mcpdev80/baseharbor.git); develop head = 40cb28c758b0
2. Measure fund-text on current develop and record witnesses
3. Create isolated worktree /tmp/opencode/lane-0428-143-wt from exact develop head (detached HEAD, no foreign commits)
4. Add the ObservabilityVerifyNone skip to the application-source loop in internal/metrics/prometheus_verify.go (same as provider loop)
5. Add uniform-semantics contract text at the single definition site internal/capability/integration_contract.go
6. Add CI-executed regression in internal/metrics (app source Verification=none not awaited)
7. gofmt + go vet clean; one squashed commit; focused go test both packages
8. Second befund: stale-emitted-target-after-same-ID-switch — covered or open?
9. Draft PR #1694 base develop, draft=false at handoff; hosted run at exact head (own terminal observation)
10. Publish evidence to baseharbor-plan main; compose sweep; END to coordinator

## Repo rule compliance

- Read baseharbor/AGENTS.md; implemented inside the card write-set only: internal/metrics/prometheus_verify.go (+ tests) and the single contract sentence in internal/capability/integration_contract.go.
- No touched files: internal/capability/perses_selection.go, internal/observability/registry.go, internal/identityprovider/**, internal/serviceaccess/**, internal/machine/**, internal/operatorauth/**, internal/metrics/perses_prometheus_datasource*.go, internal/application/perses_runtime.go, internal/metrics/prometheus_files.go, cmd/baha/app_status_result.go, internal/application/provider_registry.go, .github/**, cmd/baha/operator_test_fixture_test.go, cmd/baha/app_context.go.

## Reality witnesses

- Planning repo remote: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` -> origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)
- Product remote resolved: lane-origin = https://github.com/mcpdev80/baseharbor.git (NOT 'origin' which in shared checkouts can point at a local fs path; used only the github.com/mcpdev80 remote)
- develop head (measured via ls-remote): `git ls-remote lane-origin refs/heads/develop` -> 40cb28c758b02960356434b630086a341ebe1738
- Worktree /tmp/opencode/lane-0428-143-wt cut from 40cb28c758b0, detached HEAD, clean: `git merge-base --is-ancestor origin/develop HEAD` = YES; `git log --oneline origin/develop..HEAD` empty (no foreign commits)

## Fund-text (measured on current develop, witnesses)

- Card names prometheus_verify.go:153/174/185 on fac01c77. On current develop the same asymmetry holds:
  - internal/metrics/prometheus_verify.go (~line 251): provider loop carries `if source.Verification == capability.ObservabilityVerifyNone { continue }`
  - internal/metrics/prometheus_verify.go (~lines 252-261): application loop `for _, source := range applicationSources {` has NO equivalent guard
  - The application source prefix filter (`strings.HasPrefix(source.ID, applicationSourcePrefix)`) is present but the verification skip is not
- `ListApplicationMetrics` returns all app-class sources; a source with mode 'none' is excluded from exported ListMetrics but verifyProviderSourcesAt still waits for its 'up' sample
- Definition site: internal/capability/integration_contract.go:58 defines `ObservabilityVerifyNone ObservabilityVerificationMode = "none"` (card said :37; the type ObservabilityVerificationMode is :41, const value :58 — the definition site, on current develop)
- No second site documents this rule as contract text: integration_contract.go:242 only validates provider signals; prometheus_files.go skips for the exporter. The uniform semantics will be stated once, at the definition site.

## Acceptance mapping

1. Application loop gets the same ObservabilityVerifyNone skip as provider loop — no other behavior, no new config, no framework
2. Contract semantics stated at exactly one site (integration_contract.go definition site)
3. CI-executed regression in internal/metrics (package owns the verifier): app-class source with Verification=none is no longer awaited as required up sample; own falling test name; cite which CI job runs it
4. Second befund (stale emitted target after same-ID source switches to VerificationNone): checked separately below
5. Hosted run at the exact head, observed to terminal state, run-id + conclusion

## Second befund (open, out of write-set)

PR #1693 independent review reproduced a stale emitted target: when a same-ID
application-class source switches from a verified Verification mode to
`VerificationNone`, the previously emitted `application--<app>--<env>--<source>.json`
is not removed.

- Confirmed against current develop (40cb28c758b0), locked file:
  `internal/metrics/prometheus_files.go`. The exporter write loop skips
  `Verification==none` (line 146-147: `if source.Verification == capability.ObservabilityVerifyNone { continue }`),
  so no new file is written for the `none` source. The room-sweep at
  lines 122-144 only deletes `application--*` files when a *different* app source
  is present (`hasApplication`), and never on the application scope — so a
  same-ID source that switches to `none` while it is the only app source leaves
  its stale `application--*.json` behind. This is exactly the reviewer's finding
  (1693-0428-123-independent-review.md, file prometheus_files.go:113-117 at the
  1693 head).
- **Not addressed by this change.** My fix is confined to
  `internal/metrics/prometheus_verify.go` (stop waiting) and the single contract
  sentence; the stale-file deletion lives in the locked
  `internal/metrics/prometheus_files.go`, outside this card's write-set (4.3).
- Status: **OPEN**, file:line `internal/metrics/prometheus_files.go:146-147`
  (write loop) + `:122-144` (sweep condition). Per fund->karten-pflicht this
  stays with the coordinator (owner casts the card); not built here.

## END

END_DONE w203-0428-143-vernone: <head SHA> pr=<n> run=<id> evidence=<path on origin/main>
