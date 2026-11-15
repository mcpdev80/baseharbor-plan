# PR #1575 Review R6

## PLAN

1. Verify exact PR #1575 r6 head/base ancestry, candidate commit log, live PR state, and specified hosted run.
2. Trace Perses pin validation into public status JSON and verify exactly the three allowed states.
3. Verify parsed JSON equals configured_unverified without health evidence and compare #1577 documentation wording.
4. Record SHA-specific verdict and any #1577 re-verdict impact, validate and publish evidence, verify origin/main, and post END.

## Candidate and provenance

Role: CODEX-REVIEW r6; no merge. Planning repository identity verified before this evidence commit:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Fresh product clone: `/tmp/opencode/mission-rev1575-r6-wt`. Exact product remote witness from `git ls-remote origin refs/heads/develop refs/pull/1575/head`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
28492bd12419f2c2e02048e07bfb92d09bb9735f	refs/pull/1575/head
```

PR #1575 is OPEN and DRAFT, base `develop`, branch `lane-0428-075-perses-seam`, exact head `28492bd12419f2c2e02048e07bfb92d09bb9735f`. `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c 28492bd12419f2c2e02048e07bfb92d09bb9735f` succeeded. The exact base-to-head log contains six commits on this candidate chain:

```text
28492bd12419f2c2e02048e07bfb92d09bb9735f mcpdev80 <dev@pfingstgraef.eu> fmt(0428-075): gofmt perses.go constants
181872c90a6e87b853e83198fbe87f198119ae23 mcpdev80 <dev@pfingstgraef.eu> fix(0428-075): expose Perses three-state contract in public status JSON (r5)
792c921cbcdb87158aa9abfbd28e2f266a44af5a mcpdev80 <dev@pfingstgraef.eu> ci(0428-075): re-trigger hosted CI for exact head c195a9a (r4)
c195a9a2049253accdf57a082e6eb33fc36ec7dd lane-0428-075-perses-seam <lane-0428-075-perses-seam@baseharbor.dev> test(0428-075): execute the genuine baha status path for the Perses seam + unknown-owner fail-closed (r3)
dc670bfd4d32baf29afde0e4b021bfdb63f4e0be mcpdev80 <dev@pfingstgraef.eu> fix(0428-075): ground Perses seam in manifest truth, fail-closed + unverified reachability
61f76fa18897d4a0709c09c27ae67e1ded8dba20 lane-0428-075-perses-seam <lane-0428-075-perses-seam@baseharbor.dev> feat(0428-075): define optional Perses provider seam (fail-closed)
```

The log contains only the named #1575 candidate chain; no #1577 head is carried. Relative to `develop`, 18 files changed and `git diff --check` is clean.

## Hosted run

Exact `gh run view 43656464247 --repo mcpdev80/baseharbor --json databaseId,status,conclusion,event,headSha,workflowName` output:

```json
{"conclusion":"success","databaseId":43656464247,"event":"pull_request","headSha":"28492bd12419f2c2e02048e07bfb92d09bb9735f","status":"completed","workflowName":"CI · Source & Quality"}
```

The run is on the exact candidate head. Active jobs `PR · Draft Go · cli-0`, `cli-1`, `cli-2`, `cli-3`, `packages`, and `PR · Draft source and routing` all concluded success. Draft selection skipped the remaining jobs. No failing check was observed; no rerun or workflow dispatch was initiated.

## R5 recipe review

### Public state and pin-validation path — present for local status results

`internal/capability/perses.go:146-164` defines the exact public vocabulary `not_configured`, `configured_unverified`, and `verified`. `PersesStatusNow` at `:176-195` returns `not_configured` for an unselected surface or invalid pin; for selected + valid `PersesDefaultRelease`, `ValidatePersesRelease` at `:97-106` validates the compiled version/image/auth class and `PersesStatusNow` returns `configured_unverified`. This function contains no runtime probe and never returns `verified`; its comments require a real health path before that state.

For local application status, `cmd/baha/app_status_result.go:158-162` derives the state from manifest selection, and `:235-248` assigns it to the public JSON field `Perses` (`json:"perses,omitempty"`). `baha status` in an application repository routes to the same app status command (`cmd/baha/status_command.go:17-20`); `baha app status --json` serializes the same `applicationStatusResult` (`cmd/baha/app_observe.go:203-220`). Thus both local entry points expose the state.

### Exact JSON assertion — present for root `baha status`, missing for app JSON

`TestBahaStatusPersesConfiguredUnverifiedPositive` uses the parsed output of selected Perses without a Perses health probe and asserts exact equality to `configured_unverified` (`cmd/baha/app_perses_cli_test.go:106-124,427-440`). The unselected case positively asserts `not_configured` (`:442-460`). The local selected fixture has no Perses runtime health path.

The test that separately executes `baha app status --json` only compares `management_ui` entries to root status; it does not assert `appReport.Perses` (`cmd/baha/app_perses_cli_test.go:279-307`). The implementation shares the result struct, but direct equality coverage for the `app status` JSON field should be added to that test.

### Public JSON omission on remote-target status — blocking

`Perses` is tagged `omitempty` (`cmd/baha/app_status_result.go:38`). Before the local state computation at `:162`, `collectApplicationStatusResult` returns early for a remote application target (`:137-141`) without setting `Perses`. Therefore the public JSON omits the field on this status path instead of returning one of the three contract values. The code comment at `:158-162` says the field is exposed on every runtime face, and the mission requires the field in public status JSON. Set `Perses` from the resolved manifest before the remote-target return and add parsed JSON assertions for the remote-target status case, preserving fail-closed behavior.

## PR #1577 wording cross-check

Fresh `git ls-remote` and `gh pr view` show PR #1577 is OPEN/DRAFT at `29dba54dddb02f48568c571e9ce37f671d21e6aa`, branch `0428-092-perses-boundary`, base `develop`. Its docs do not contain the three machine-state names. The English release note says selected-but-unprovisioned Perses is `unsupported` “never as configured” (`docs/releases/v0.4.28.md:15`); the German release note says the equivalent “nicht als konfiguriert” (`docs/de/releases/v0.4.28.md:13`). The English reference says `unsupported` rather than “configured” (`docs/reference/releases.md:31`); the German reference has the same mismatch (`docs/de/reference/releases.md:30`). These statements are not word-for-word consistent with the #1575 contract `configured_unverified` for selected + valid pin and no health proof.

There is also an internal wording conflict in the #1575 candidate itself: `docs/spec/management-access-v1.md:41-43` says selected-but-unprovisioned MUST be `unsupported` / “not configured,” while `:50-61` says selected + valid pin with no health probe is `configured_unverified`. Align the former requirement with the explicit three-state semantics and update the #1577 English and German release/reference wording to use the same three state names and meanings. `.github/**` is not involved and was not edited.

## Verdict and correction recipe

REJECT exact candidate `28492bd12419f2c2e02048e07bfb92d09bb9735f`. The local public status path now exposes the three-state field, pin validation alone maps only to `configured_unverified`, and a positive parsed-JSON equality assertion exists for selected Perses without a health proof. Blocking gaps: remote-target status omits the `perses` field; `app status --json` lacks direct equality coverage; PR #1577 wording is stale and conflicts with the exact state meanings, as does the earlier bullet in #1575's management-access spec.

Correction recipe: populate the field before the remote-target early return; assert parsed `app status --json` equals `configured_unverified` for the selected no-health fixture; reconcile `management-access-v1.md` and PR #1577 English/German release and reference statements to exactly `not_configured`, `configured_unverified`, and `verified`, with `verified` requiring a real health path. Keep #1577 WAIT. No #1577 re-verdict is warranted on its unchanged current head; after its docs change lands on the candidate, review the new exact SHA before acceptance. This r6 rejection does not authorize merge.

## repo-rule compliance

Read-only review from a fresh product clone; no local tests, product edits, PR updates, CI reruns, workflow edits, merges, containers, or VM actions. Evidence is stored only in the actual planning repository. The quarantined stale-ref product checkout was not used. Evidence contains no markdown checkbox lines.

Exact cross-PR witness from `git ls-remote origin refs/heads/develop refs/pull/1575/head refs/pull/1577/head`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
28492bd12419f2c2e02048e07bfb92d09bb9735f	refs/pull/1575/head
29dba54dddb02f48568c571e9ce37f671d21e6aa	refs/pull/1577/head
```

Exact `gh pr view 1577 --repo mcpdev80/baseharbor --json number,state,isDraft,headRefName,headRefOid,baseRefName` output:

```json
{"baseRefName":"develop","headRefName":"0428-092-perses-boundary","headRefOid":"29dba54dddb02f48568c571e9ce37f671d21e6aa","isDraft":true,"number":1577,"state":"OPEN"}
```

## Planning validation STATE

Planning validation could not complete because existing unrelated task metadata has source URLs where `plan.py` requires `repo#number` references. `python3 scripts/plan.py render && python3 scripts/plan.py check` stopped in render at `scripts/plan.py:883` with `ValueError: not enough values to unpack (expected 2, got 1)`. Running `python3 scripts/plan.py check` separately reached the same failure in `cmd_check -> validate -> check_generated_blocks -> links_block -> short_ref`. The offending `sources` entries are at line 19 of `tasks/t-20261115-bughunt-d28-app-new-reg.md`, `tasks/t-20261115-bughunt-d28-bad-config-quiet.md`, `tasks/t-20261115-bughunt-d28-i18n-achtung.md`, `tasks/t-20261115-bughunt-d28-state-dir-target.md`, and `tasks/t-20261115-bughunt-d28-tmp-selection.md`; each contains the URL `https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md` without a `#` reference. These files are outside this review's write scope and were not changed. The evidence itself passes `git diff --check` and the no-checkbox scan.


END mission-rev1575-r6.md DONE — REJECT candidate 28492bd12419f2c2e02048e07bfb92d09bb9735f.

Exact `origin/main` witness immediately before evidence publication:

```text
69d68d29164eea6e618e4b48a60d82793b7992e2	refs/heads/main
```
