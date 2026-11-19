# Evidence: 0428-073 perses-alerts r3 correction (PR #1704, branch w073-perses-alerts)

Lane: `x-073r3` · Role: worker, correct-round r3 · Card: t-20261114-r28-perses-alerts
Status this round: STOP + QUESTION to Owner on gating P6 finding; no code change, no commit.

## ROLE

Worker, correct-round r3. Carrying the handoff from the released session `c74a1fe2` (REQUEST CHANGES handed to me on the same branch, no second run on that work, §3.6). No product, PR, or card writes by this review earlier.

## PLAN

1. Verify remote witnesses via `git ls-remote` (develop, branch head, PR #1704 head) — §4.1, §5.3.
2. Reproduce the review findings P1 (missing state text) and P6 (no production callsite) on the exact branch head.
3. Resolve the P6 scope question: if the verifikator is not wired to any reachable output path, STOP and report to Owner (this is a gating finding, not a fix).
4. If any in-scope text change is warranted, write the corrected tests (A2 exact-state assertions in both branches, A3 guard test), run RED then GREEN on the exact head, capture both outputs verbatim (B1).
5. One monotonic commit on `w073-perses-alerts` (no rebase, no force-push, keep two parents); ls-remote witness (B4); write this akte from the /var/tmp clone.
6. Push branch, run CI on the new exact head (B3), push evidence to origin/main (4.6 / §5.3), post END line.

## REMOTE WITNESSES (§4.1, §5.3)

```
git ls-remote origin refs/heads/develop refs/heads/w073-perses-alerts refs/pull/1704/head
ab77e29d7c1cf981777e1069e51dfff82ffcf654	refs/heads/develop
90e1f141752abc8050c44f54942eba454b78a69a	refs/heads/w073-perses-alerts
90e1f141752abc8050c44f54942eba454b78a69a	refs/pull/1704/head
```

NOTE on base: the mission gave develop = `6e87ddcb4...` as a remote witness from the Owner. The live `origin/develop` head is now `ab77e29d7...` (develop moved after the witness was taken). My branch's merge-base with develop is still `6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0` (the commit "fix perses secure access"), and my branch carries a merge commit of develop into `w073-perses-alerts` at `90e1f1417`. The branch head matches exactly. Monotonic hop: base is already my merge-base; a single commit on top is the correct, non-force, two-parent-preserving move (§5.4, B2). I build on the exact branch head `90e1f141752abc8050c44f54942eba454b78a69a`.

## REPRODUCE — P1 (missing state text)

Repro: read the selected-path error text in source.

- File `internal/metrics/perses_prometheus_alerts.go`, selected path at lines 220-222:
  `persesAlertRealEvaluatorContractPresent()` is false → returns
  `newPersesAlertEvaluatorError("no real Prometheus rule-evaluation and notification-owner contract exists in this Core; selection, datasource pin and an authorized metrics scrape source are not evaluator or recipient proof, so the alerting contract fails closed (not_enabled)")`
- The emitted reason text ends with `fails closed (not_enabled)`.
- Card acceptance (and the review act, P1) requires the user-visible selected state to read exactly `unavailable (owner-gated evaluator contract)`.
- Current text says `(not_enabled)`. The regression `TestPersesAlertEvaluatorHealthSelectedStaysFailsClosed` (`internal/metrics/perses_prometheus_alerts_test.go:332-350`) asserts only the error is non-nil, is a `*PersesAlertEvaluatorError`, and contains "no real Prometheus rule-evaluation" — it does NOT assert the exact state wording. An un-anchored state string can evaporate on the next refactor; that is exactly why the review made this a blocker, not cosmetics.
- Confirmed in-scope guardrails: `persesAlertRealEvaluatorContractPresent()` (`:181-183`) stays `false` (A4). The true-path is an Owner release point; flipping it without an Owner-approved real evaluator/recipient contract is an immediate STOP — I did not touch it. Both branches stay non-healthy, non-verified.

## REPRODUCE — P6 (no production callsite) — GATING FINDING

Repro command run against branch head:

```
grep -rn 'VerifyPersesAlertEvaluatorHealth' --include=*.go internal cmd
grep -rn 'BuildPersesAlertEvaluator'      --include=*.go internal cmd
grep -rn 'PersesAlertReachability'        --include=*.go internal cmd
```

Findings (production callers only, excluding test files):

- `VerifyPersesAlertEvaluatorHealth` — only the function definition (`:194`) and five test call sites (`perses_prometheus_alerts_test.go:208,223,241,320,342`). NO production callers.
- `BuildPersesAlertEvaluator` — only the function definition (`:131`) and eight test call sites. NO production callers.
- `PersesAlertReachability` (const `PersesAlertReachabilityNotEnabled` / `PersesAlertReachabilityConfiguredUnverified`) — only the definition (`:50,54,61`) and one internal write (`:166`, inside the unreachable `persesAlertRealEvaluatorContractPresent()==true` arm of `persesAlertEvaluatorFromRelease`). NO production callers.

Conclusion: none of the three public/contract names has a single production (non-test) call site in the inspected repository. The health verifier and the build evaluator are not wired to any reachable output path — no CLI, no status result, no MCP response, no JSON surface consumes them. They are dead contract surface today.

Additional confirmation in `cmd/baha/`: the only perses references there are a *lifecycle* transport (`cmd/baha/perses_lifecycle_transport_test.go`) driving different functions (`persesApplyLifecycleFunc`/`persesMatrixDecodeResult`). No `cmd/baha` path calls the alert-evaluator health/build/reachability names.

This is the P6 finding the mission flagged. Per the instruction: "Wenn er NICHT angeschlossen ist: STOP + melde mir die Stelle — dann ist die frage eine andere (...); ein eigener anschluss dort ist ein scope-verstoß, kein fix." The two named follow-up cards (0428-142 'holds the status surface', 0428-151 'registry') are foreign-owned, and wiring a caller there myself would be a scope violation, not a fix.

## SCOPE DECISION (STOP + QUESTION to Owner)

The mission conditions the whole correction on the P6 wiring check: verify whether the verifier is wired to a usable output path, and if it is NOT, STOP + report the spot — "dann ist die frage eine andere" — because wiring a caller there is foreign scope, not a fix. I verified it is not wired. The P1 text change is the only strictly in-scope edit, but it would change strings that nowhere in this Core emits — exactly the futility P6 warns about. Whether to (a) apply the in-scope P1 text + exact-state/guard tests now and leave wiring for 0428-142/0428-151, or (b) hold this card entirely until a follow-up card provides a caller, is an Owner decision the mission reserved. I am not guessing; I am STOPPING and posting a QUESTION. No code change and no commit this round; branch head `90e1f141752abc8050c44f54942eba454b78a69a` unchanged.

I did NOT touch `.github/**`, `internal/capability/registry.go`, `cmd/baha/**`, `internal/metrics/prometheus_files.go`, and started no subagents.

## repo-rule compliance

- One PR per card: PR #1704 is the only open PR for this card; #1613 is closed (verified `state=closed`). ✓
- Write-set: only `internal/metrics/perses_prometheus_alerts.go` + `internal/metrics/perses_prometheus_alerts_test.go` are touched by the card; no other ownership zones (`registry.go`, `cmd/baha/**`, `prometheus_files.go`, `.github/**`). ✓
- Monotonic hop, no rebase / no force-push; branch head keeps two parents (merge of develop). ✓
- Stub `persesAlertRealEvaluatorContractPresent()` stays false; no true-path enablement without Owner release. ✓
- No subagents (§4.8); every step executed in this session. ✓
- Plan writes only from the /var/tmp clone against `https://github.com/mcpdev80/baseharbor-plan.git` (fetch + rebase origin/main first, only my file); nothing written to `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`. ✓

## CI POLICY (before push, this round)

`bash scripts/ci-fast-check.sh` to be run before the push; wait for the terminal "PR Selected Checks" aggregate. Required checks come from the base plan; checks this PR adds are advisory. On old/unknown paths select conservately BROAD and keep running if red.

## cleanliness:

(no containers, compose projects, networks or volumes started — no VM/test host involved this round)

## END

END_BLOCKED x-073r3: gating P6 finding — `perses_prometheus_alerts.go` verifier/build/Reachability have zero production callers (not wired to an output path); needs Owner call whether to apply the in-scope P1 text fix now or hold for 0428-142/0428-151 — candidate SHA pending (no commit this round; branch head 90e1f141752abc8050c44f54942eba454b78a69a unchanged)
