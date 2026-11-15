# PR #1575 Review R7

## PLAN

1. Verify exact PR #1575 r7 head/base ancestry, candidate commit log, PR state, and specified pull_request run.
2. Review the diff from 28492bd12 and confirm Perses status is populated before remote-target early return.
3. Verify parsed app status JSON equals configured_unverified without health evidence and compare #1577 wording.
4. Record exact-SHA verdict and correction recipe, validate and publish evidence, verify origin/main, and post END.


## Candidate and provenance

Role: CODEX-REVIEW r7; no merge. Planning repository root was verified before this evidence commit:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

Fresh product clone: `/tmp/opencode/mission-rev1575-r7-wt`. Exact product witness from `git ls-remote origin refs/heads/develop refs/pull/1575/head refs/pull/1577/head`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
a5a5abedc3f9b5f72a2ff3819ed847293869eea9	refs/pull/1575/head
29dba54dddb02f48568c571e9ce37f671d21e6aa	refs/pull/1577/head
```

PR #1575 is OPEN and DRAFT, base `develop`, branch `lane-0428-075-perses-seam`, exact head `a5a5abedc3f9b5f72a2ff3819ed847293869eea9`. `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c a5a5abedc3f9b5f72a2ff3819ed847293869eea9` succeeded. The base-to-head log contains only this candidate chain; no #1577 head is carried:

```text
a5a5abedc3f9b5f72a2ff3819ed847293869eea9 mcpdev80 <dev@pfingstgraef.eu> fix(0428-075): set Perses field before remote-target early return (r7)
28492bd12419f2c2e02048e07bfb92d09bb9735f mcpdev80 <dev@pfingstgraef.eu> fmt(0428-075): gofmt perses.go constants
181872c90a6e87b853e83198fbe87f198119ae23 mcpdev80 <dev@pfingstgraef.eu> fix(0428-075): expose Perses three-state contract in public status JSON (r5)
792c921cbcdb87158aa9abfbd28e2f266a44af5a mcpdev80 <dev@pfingstgraef.eu> ci(0428-075): re-trigger hosted CI for exact head c195a9a (r4)
c195a9a2049253accdf57a082e6eb33fc36ec7dd lane-0428-075-perses-seam <lane-0428-075-perses-seam@baseharbor.dev> test(0428-075): execute the genuine baha status path for the Perses seam + unknown-owner fail-closed (r3)
dc670bfd4d32baf29afde0e4b021bfdb63f4e0be mcpdev80 <dev@pfingstgraef.eu> fix(0428-075): ground Perses seam in manifest truth, fail-closed + unverified reachability
61f76fa18897d4a0709c09c27ae67e1ded8dba20 lane-0428-075-perses-seam <lane-0428-075-perses-seam@baseharbor.dev> feat(0428-075): define optional Perses provider seam (fail-closed)
```

The r7 diff from `28492bd12419f2c2e02048e07bfb92d09bb9735f` changes only `cmd/baha/app_status_result.go`, `cmd/baha/app_perses_cli_test.go`, and `docs/spec/management-access-v1.md` (15 insertions, 8 deletions). `git diff --check` is clean.

## Pull-request run

Exact `gh run view 43659466298 --repo mcpdev80/baseharbor --json databaseId,status,conclusion,event,headSha,workflowName` output:

```json
{"conclusion":"success","databaseId":43659466298,"event":"pull_request","headSha":"a5a5abedc3f9b5f72a2ff3819ed847293869eea9","status":"completed","workflowName":"CI · Source & Quality"}
```

The run is on the exact r7 head. Active pull-request jobs `PR · Draft source and routing`, `PR · Draft Go · cli-0`, `cli-1`, `cli-2`, `cli-3`, and `packages` all concluded success; the remaining jobs were skipped under draft selection. No failing pull-request check was observed. The ambient serial-runtime integration gate mentioned as Q-RUNTIME was not assessed, per this mission; this review uses only the specified pull-request run and candidate contents. No rerun or workflow dispatch was initiated.

## R6 recipe review

### Perses field before remote-target return — fixed

`collectApplicationStatusResult` now computes `persesStatus` at `cmd/baha/app_status_result.go:143` before the `hasRemoteApplicationTarget` early return at `:144-149`, and includes `Perses: persesStatus` in that return at `:145-148`. The local result also assigns the same state later. This closes the r6 remote-target omission.

### Positive parsed JSON equality for `app status --json` — fixed

`TestBahaStatusPersesCLIEntrypointResolvesWithoutContainer` parses the explicit `baha app status --json` output and now calls `assertPersesConfiguredUnverified(t, appReport)` at `cmd/baha/app_perses_cli_test.go:295-310`. The selected fixture is built without a Perses container or Perses health probe; the helper requires exact equality with `configured_unverified` at `:112-124`. This is a positive parsed-field equality assertion, not a substring check. The root `baha status --json` selected case and unselected `not_configured` case remain covered at `:427-460`.

The public state path remains: `PersesStatusNow` (`internal/capability/perses.go:185-195`) maps unselected or invalid pin to `not_configured`, and selected plus valid `PersesDefaultRelease` to `configured_unverified`. `ValidatePersesRelease` (`:97-106`) validates static release metadata only; it does not observe runtime health. No code path returns `verified`; that state is reserved for a real Perses health path. The public JSON field is `Perses` with `json:"perses,omitempty"` (`cmd/baha/app_status_result.go:38`).

### Documentation — still blocking and internally inconsistent

The #1575 change at `docs/spec/management-access-v1.md:41-44` now says a selected but unprovisioned surface must report `not_configured`, never `configured_unverified` or `verified`. Its state definition at `:55-60` says `configured_unverified` means the surface is selected and its pinned release validated, while reachability is unverified because no health probe exists. The code's `PersesStatusNow` validates the compiled default pin and checks manifest selection only; a selected surface with no running Perses instance therefore yields `configured_unverified`. The new `not_configured` bullet contradicts the implemented and tested selected/no-health state. Clarify that `not_configured` means unselected or invalid/unavailable declaration, while selected + valid pin and no health evidence is `configured_unverified`.

PR #1577 remains OPEN/DRAFT at `29dba54dddb02f48568c571e9ce37f671d21e6aa`. Its English release note (`docs/releases/v0.4.28.md:15`) still says selected-but-unprovisioned Perses is `unsupported` and “never as configured”; the German release note (`docs/de/releases/v0.4.28.md:13`) says the equivalent. English and German reference lines (`docs/reference/releases.md:31`, `docs/de/reference/releases.md:30`) also use `unsupported` rather than the three state names. They do not state the same three states word-for-word and conflict with #1575's `configured_unverified` result for selected + valid pin + no health proof. The r7 candidate does not edit #1577's documentation.

## Verdict and correction recipe

REJECT exact candidate `a5a5abedc3f9b5f72a2ff3819ed847293869eea9`. Both r6 code/test findings are fixed: the Perses field is set before the remote-target return and parsed `app status --json` now receives an exact `configured_unverified` assertion. The blocking issue is documentation: the #1575 spec's selected-but-unprovisioned sentence contradicts its three-state definition and actual code, and live #1577 English/German release/reference prose still does not use the same three-state vocabulary or meanings.

Correction recipe: define `not_configured` consistently with the code for unselected/invalid declarations; define selected + valid pin + absent health evidence as `configured_unverified`; reserve `verified` for a real health-path observation. Align #1577 English and German release/reference text to those same three state names and meanings. Keep #1577 WAIT; it was not changed, so no new #1577 re-verdict is due until its documentation candidate changes. Do not assess the separate ambient serial-runtime Q-RUNTIME gate. No PR update or merge is authorized by this review.

## repo-rule compliance

Read-only review from a fresh product clone. No product files, PRs, workflows, CI, containers, or VMs were changed or started; no local tests were run. Evidence is stored only in the actual planning repository. The quarantined stale-ref product checkout was not used. Evidence contains no markdown checkbox lines.


## Planning validation STATE

`python3 scripts/plan.py render && python3 scripts/plan.py check` and a separate `python3 scripts/plan.py check` both fail in existing planning metadata before validating this evidence: `scripts/plan.py:883` raises `ValueError: not enough values to unpack (expected 2, got 1)` while splitting a source reference. Five unrelated task cards have a URL, not the required `repo#number`, at line 19: `tasks/t-20261115-bughunt-d28-app-new-reg.md`, `tasks/t-20261115-bughunt-d28-bad-config-quiet.md`, `tasks/t-20261115-bughunt-d28-i18n-achtung.md`, `tasks/t-20261115-bughunt-d28-state-dir-target.md`, and `tasks/t-20261115-bughunt-d28-tmp-selection.md`. Their metadata was left unchanged. This is a planning validation STATE, not a product CI failure. The review evidence passes `git diff --check` and the no-checkbox scan.

END mission-rev1575-r7.md DONE — REJECT candidate a5a5abedc3f9b5f72a2ff3819ed847293869eea9.
