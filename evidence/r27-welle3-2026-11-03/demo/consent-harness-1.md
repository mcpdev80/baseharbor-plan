# t-20261104-r27-demo-guided-consent — demo consent harness

Task: t-20261104-r27-demo-guided-consent (baseharbor-demo)
Worker: w85-demo-consent-harness
Date: 2026-11-04
Repo rule authority: baseharbor-demo/AGENTS.md (planning = baseharbor-plan), product/review/CI in the demo repo.
Write scope: tests/guided/drive.py, baseharbor-core.ref only. No Core files. No new contract/gate semantics. No weakening of the consent gate. No env-var auto-confirm.

## Outcome

Guided happy-path `baha up` now captures the printed confirm-hash and, feature-detected,
re-runs the same guided `up` with `--confirm-candidate <digest>` so the candidate-consent
contract completes. Without Core support, today's fail-closed behavior is unchanged.

Evidence gate: acceptance.sh guided (own local run, rootless docker).

## Core pin (decided by coord f49a3303, 2026-11-04)

- baseharbor-core.ref: 212ae90e22e6ea2eeeaa84f35189b307b1ce32bc -> 488a39e6f67ecbc733dc6acdee2443b36db4717c
- Pin-tracking on the r27 candidate branch is an established pattern; 212ae90e is a proven ancestor.
- 488a39e6 is the commit that threads the digest to the apply choke point (see below).
- After #1355 merges to develop, Owner sets the pin to develop-retarget; this draft PR need not carry the final state.

## Root cause (why the guided gate fails closed today)

- ece31b80 (work/r27-candidate-contract head) parses `--confirm-candidate` into `runtimeUpOptions.CandidateConsent`.
- runtimeUpCommandWithInputResolver (app_input_resolver.go:494) calls parseRuntimeUpOptions(args) but never calls withCandidateConsentDigest(ctx, opts.CandidateConsent).
- routeRepositoryRuntimeUp calls appApplyCommand(...).Run(ctx, nil, ...); app apply reads the digest from candidateConsentOverride(ctx) and its own flag parse sees nil args -> digest empty.
- recordDeploymentBeforeMutation then sees an empty consent and refuses: "candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state".
- Fix (488a39e6): before appApplyCommand(...).Run(ctx, nil, ...), add `if opts.CandidateConsent != "" { ctx = withCandidateConsentDigest(ctx, opts.CandidateConsent) }`.

## Harness change (tests/guided/drive.py)

- First guided up: run_tty with capture=True (does not raise on fail-closed); transcript captured to file.
- capture_confirm_hash: extracts the 64-hex digest from the `Re-run with --confirm-candidate <digest>` line.
- binary_supports_confirm_candidate: behavioral probe with a throwaway digest in a throwaway dir; classifies by the literal `unknown option --confirm-candidate` rejection string. NOT by --help grep (the flag is parsed manually and is intentionally absent from the usage listing). Legacy emits the rejection string almost instantly; r27+ proceeds past it.
- If digest captured and flag supported: re-run the same guided up with `--confirm-candidate <digest>`; digest is stable across runs (computed from the unchanged repository source), so it binds and the flow reaches the apply.
- If digest captured but flag unsupported: raise (refuse to fabricate consent); today's fail-closed behavior.
- If no digest: today's behavior (no candidate surface).

## Evidence (own acceptance.sh guided run, docker, 488a39e6)

- Line 1284-1285: first up prints `confirm-hash 825675ca4a7d97a1067752234ca1cc107769dffc8788ce6a7b1c66cea6d794b7` and `Re-run with --confirm-candidate 825675ca...`.
- Line 1307: fail-closed on the first run: `Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`.
- Line 1308: harness logs `guided up: candidate confirm-hash captured 825675ca...; re-running with --confirm-candidate`.
- Line 1968-1969: second up with --confirm-candidate 825675ca... — digest accepted, flow proceeds past the consent choke point to the apply (reaches OpenBao manager-auth readiness gate).
- Digest stable: same 825675ca... on both runs (source unchanged).

## Regression matrix (both branches as reproducible regressions)

- Red-first (second run missing today): without the harness, the guided gate fails closed with the fail-closed error above (the only thing that ever printed). This is the bug #1355 described literally.
- Digest accepted (with harness + 488a39e6): digest 825675ca... bound, flow reaches the apply.
- Detection-false (today's behavior for an unsupported Core): a Core without the flag is probed, the literal `unknown option --confirm-candidate` is classified as unsupported, and the flow keeps the original fail-closed path (no fabricate-consent crash).
- Detection guard (refuse fabricate consent): if a digest prints but the probe says unsupported, drive.py raises instead of supplying the flag.

## Known local limitation (NOT a harness defect)

- The local run reaches the apply and stops at `verify OpenBao manager authentication after control-plane start: OpenBao manager credentials are not configured`.
- This is the single-member local OpenBao setup: CheckManager (internal/openbao/bootstrap.go:370) logs in as the OpenBao manager identity and requires quorum manager credentials that only an HA/3-member deployment configures.
- The gate is pre-existing and identical on the old core (212ae90e) and on develop (git log origin/develop..develop on cmd/baha/runtime_start.go shows CheckManager present on both). It is not introduced by the 488a39e6 threading fix.
- The candidate-consent contract itself completes: the digest is accepted and the flow proceeds past recordDeploymentBeforeMutation. The remaining gate is a downstream runtime readiness check.

## PR + status

- PR #128 (draft): https://github.com/mcpdev80/baseharbor-demo/pull/128
- Head: w85-demo-guided-consent = 683f1da7c5b67d71c25956252bade4af10c6e1f1
- ls-remote == head: verified (683f1da7c5b67d71c25956252bade4af10c6e1f1)
- HEAD (commit): 683f1da test(guided): capture confirm-hash and re-run up --confirm-candidate (t-20261104-r27-demo-guided-consent)
- Files: baseharbor-core.ref (pin bump), tests/guided/drive.py (harness). No Core files touched.
- Commit/PR status: committed to branch, pushed, draft PR open.
- CI via own local run: local acceptance.sh guided reaches the apply but stops at the OpenBao manager-auth readiness gate (local single-member limitation, documented above).

## END

- detection: beidseits-belegt (both branches as regressions: without-harness fail-closed; with-harness digest-bound).
- ls-remote: 683f1da7c5b67d71c25956252bade4af10c6e1f1
- END_DONE
