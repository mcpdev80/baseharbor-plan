# REVIEW.md — Review-B (read-only review of #1242 and #1243)

**ROLE:** REVIEW (read-only). No product edits. No merge.
**Model:** Qwen Flash (via AgentGateway). **Session:** local review lane (baseharbor-ecosystem/workers/.models/ornith).
**Time (UTC):** 2026-11-01 ~00:45Z (GitHub-hosted run timestamps) / review completed 2026-11-01.
**Basis:** `gh pr diff` gen-accurate diffs, `gh pr checks`, `gh api` run/job logs, source reads of the consent gate and the CI coverage gate.

Witnesses:
- #1242 head SHA `f392273e89b98d8520a686c0c0465fdc93aa26fb`; CI run `41251305646` (job `124685607590`).
- #1243 head SHA `878a21247996244d55769b3a1a3c7fdb47d53147`; CI run `41257223807` (job `124703362045`).
- main head `e92e20588c5737f566e29d47bbd08a9bcaed19d3`.

---

## PR #1242 — fix(observability-acceptance): plan→apply consent guard
**Verdict: {APPROVE-WARTEND-GREEN}**

Scope (gen-accurate, `gh pr diff #1242`): one file, `cmd/baha/app_observability_acceptance_test.go`.
- Before: `runWithIO(ctx, ["app","apply"])` with no consent → fails with `impact-confirmation-required`.
- After: builds the real impact plan, asserts `plan.ProviderPlan.Impact != nil`, constructs consent with the **actual** `impact.ConfirmationsRequired` (`First: true`, `Second: ConfirmationsRequired==2`, `DeleteData: false`), validates it through the **shared** `ValidateProviderChangeConsent` (the §2.7 gate), and threads it via `withProviderChangeConsent` into the apply. Renames the `status`-phase `resolved` locals (no behavioral change).

§2.7 correctness (witnessed in source):
- `internal/application/provider_change_consent.go:12-36` — validation requires plan ID match, `First` always, `Second` when `ConfirmationsRequired==2`, and `DeleteData` only when `Destructive`. The test's consent construction mirrors this exactly and passes for a create/apply (`DeleteData:false`, `Destructive:false` path).
- `provider_change_types.go:168-178` (`ProviderImpactPlan`) + `:182-187` (`ProviderChangeConsent`) — struct fields match what the test reads/sets.
- `provider_change_plan.go:66-74` — `ConfirmationsRequired=2` on alternative-less/unknown/destructive; the test reads the live value rather than hard-coding, so it cannot drift from the gate.
- **NOT a circumvention:** the consent is constructed against the real computed `impact`/`PlanID`/`ConfirmationsRequired` and validated by the real validator before apply. There is no blind `---` force-over-deletion; the only destructive path is the test's teardown `app destroy --yes`, which is a separate, pre-authorized cleanup code path. No product code touched.

Repo rules: read-only review, no product edits, no merge. ✅

---

## PR #1243 — ci(gh-dispatch2): run broker + s3 acceptance on GitHub-hosted
**Verdict: {CHANGES: integration gate requires native runtime qualification — not mergeable as-is}**

Scope (gen-accurate, `gh pr diff #1243`): two files, only `runs-on` lines:
- `.github/workflows/runtime-broker.yml`: `runs-on: [self-hosted, Linux, X64, baseharbor, docker]` → `runs-on: ubuntu-latest` (acceptance job, line 27; performance job, line 233).
- `.github/workflows/runtime-s3-acceptance.yml`: same swap (line 12).
- No test/logic change → **no coverage gap** possible; the mission's "Dauer-SKIP deckt Coverage"-concern does not apply. No permanent SKIP introduced (verified: no `skip`/`CLEAN`/`enabled:false` in either workflow).

CI status: the `PR Selected Checks` integration gate fails with:
`BLOCKED: coverage-unresolved: workflow execution/cleanup/evidence impact requires native qualification: .github/workflows/runtime-broker.yml; ... runtime-s3-acceptance.yml`
(witnessed in CI run `41257223807` / job `124703362045`).

Root cause (authoritative, `scripts/pr-gate-plan.py:1515-1519`): any change under `.github/workflows/` is classified `runtime-workflow-unresolved` and **requires native qualification** — a required, fail-closed gate, not a skippable optional check. The integration runner therefore blocks on GitHub-hosted (self-hosted `baseharbor` runners are what qualify this). The `coverage-unresolved` label here means "native runtime qualification not performed", not "coverage hidden by permanent skip".

Verdict rationale: The change is legitimate and well-scoped, but it does **not** pass the integration gate. This is a required-gate BLOCK (not a cosmetic skip), so the candidate is not acceptable yet.

Repo rules: read-only review, no product edits, no merge. ✅ (reviewer compliance only)

---

## END
END_DONE review-B: #1242=APPROVE-WARTEND-GREEN #1243=CHANGES:integration-gate-requires-native-qualification
