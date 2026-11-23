# H-V37 — "PR · Trusted Plan" fails closed on #1810 and #1809 (root cause, read-only)

- Mission: `coordinator/missions/w37-hvtrustedplan.txt` (H-V37, flash, READ-ONLY)
- Lane: w37-0428-235-hvtrustedplan (hunt desk, no product change, no branch, no PR)
- Date: 2026-11-23
- Verdict up front: **is-it-0428-235-confirmed: yes** — but the mechanism is the *catalog
  fail-loud guardian* (card 0428-242), NOT the "planner selects zero gates" symptom named in
  0428-235, and both PRs are **not** gate-blocked on a shared bug: each carries a real,
  individually reproducible defect of its own. Details and machine witnesses below.

## PLAN

- Resolve the real GitHub remote (URL contains github.com/mcpdev80) for product and planning repos; verify zone before any git action.
- Attest develop and both PR heads with `git ls-remote`; record base attestation.
- Pull the failing `PR · Trusted Plan` job logs for #1810 and #1809; capture the exact failing line and the gate-selection output (how many selected, which paths, why the plan aborted).
- Read `scripts/pr-gate-plan.py`, `scripts/pr-gate-coverage.json`, `scripts/pr-native-gate-plan.py`, `scripts/validate-pr-gate-coverage.py`, `scripts/pre-release-runtime-impact.json` and `.github/workflows/ci.yml` at develop; find the path→gate mapping and the exact condition that aborts the plan; cite file:line.
- Run the ancestry test for each PR head (`git merge-base --is-ancestor origin/develop <head>`).
- Reproduce both failures offline against the develop catalog, then test candidate fix shapes in `/tmp` only (no repo writes).
- Decide: 0428-235 self-change bug vs base-ancestry staleness vs missing admission rows vs candidate-content failure.
- Produce the MINIMAL owner-scope fix proposal (file + line + row/condition) without applying it.
- Write this evidence into baseharbor-plan (real repo), push, verify on origin/main, post END.

## Reality witnesses

Remote resolution (product repo, per REMOTE GUARD — every configured remote URL here is GitHub; none points at a local filesystem path):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v
lane-origin	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
lane-origin	https://github.com/mcpdev80/baseharbor.git (push)
origin	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
origin	https://github.com/mcpdev80/baseharbor.git (push)
upstream	https://github.com/mcpdev80/baseharbor.git (fetch)
upstream	https://github.com/mcpdev80/baseharbor.git (push)
```

Planning repo, verified BEFORE the first evidence commit (wrong-zone rule):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Base + candidate attestation (remote truth, not the quarantined `workers/baseharbor` checkout):

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
dc8626e9c52be07a8ea5b87b468c5991b7540c4f	refs/heads/develop
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1810/head refs/pull/1809/head
034c0c7d21512a62b2ec236b779e84235da4f507	refs/pull/1809/head
168d40950bae5b8fb31862b36ceaffbdd1862207	refs/pull/1810/head
```

No branch was created and nothing was pushed by this lane (read-only mission).

## Task 1 — the exact failing lines (hypothesis correction #1)

Both failures are `PR · Trusted Plan`, step **"Resolve exact immutable PR inputs using
trusted base policy"**, exit code 1. Both are a **Python `ValueError` raised by the
planner**, not an empty/zero-gate plan:

### #1810 (run 45247799528, job 137949084179, BASE_SHA dc8626e9c…, HEAD 168d40950…)

```
Traceback (most recent call last):
  File "/home/runner/work/_temp/pr-gate-plan.py", line 1947, in <module>
  File "/home/runner/work/_temp/pr-gate-plan.py", line 1940, in main
  File "/home/runner/work/_temp/pr-gate-plan.py", line 1836, in plan
    raise ValueError(
        'invalid trusted PR gate coverage catalog: '
        + _coverage_module().unresolved_source_error(source_unowned))
ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared
runtime gate owner: internal/application/perses_lifecycle_test.go
 (id source.internal_application_perses_lifecycle_test_go): add this source with its surfaces
 to scripts/pr-gate-coverage.json, e.g. {"id": "source.internal_application_perses_lifecycle_test_go", "path": "internal/application/perses_lifecycle_test.go", "surfaces": [...]};
 internal/capability/perses.go (id source.internal_capability_perses_go): …;
 internal/capability/perses_test.go (id source.internal_capability_perses_test_go): …
##[error]Process completed with exit code 1.
```

Gate-selection output before the abort: the planner never printed a plan, so **zero gates were
selected by a plan — the plan itself aborted** (`broad_required`/`selected_gates` were never
produced). Three of the five changed source paths have no catalog owner.

### #1809 (run 45244415977, job 137937304367, BASE_SHA dc8626e9c…, HEAD 034c0c7d2…)

```
  File "/home/runner/work/_temp/pr-gate-plan.py", line 1836, in plan
    raise ValueError(
ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared
runtime gate owner: cmd/baha/secret_audit_test.go (id source.cmd_baha_secret_audit_test_go):
 add this source with its surfaces to scripts/pr-gate-coverage.json, e.g. {…};
 cmd/baha/secret_operations.go (id source.cmd_baha_secret_operations_go): add this source …
##[error]Process completed with exit code 1.
```

Same signature: abort before any plan is written, 2 of 3 changed source paths uncataloged.

### The downstream `PR Selected Checks` failure is NOT the same cause (correction)

The aggregate fails for a different, mechanical reason: `PR · Trusted Plan` is the job that
computes the `unit_scope` output (`.github/workflows/ci.yml:770`, written at `:1014`), and the
aggregate compares that empty output (`:1534`, `UNIT_SCOPE: ${{ needs.pr_plan.outputs.unit_scope }}`)
against `full|cli|none` at `.github/workflows/ci.yml:1541`:

```
PR Selected Checks	Require complete selected Go shard coverage	  UNIT_SCOPE: 
PR Selected Checks	Require complete selected Go shard coverage	  UNIT_RESULT: skipped
PR Selected Checks	Require complete selected Go shard coverage	REJECT: Go test selection missing or invalid
```

`PR · Native gate plan` (the job 0428-235 is about) **passed** in both runs and is unrelated to
these reds; the 0428-235 "base pointer does not contain the trusted native gate planner, so the
matrix is `{"include":[]}`" pattern (`.github/workflows/ci.yml:502-512`) does **not** appear in
either PR's logs.

## Task 2 — where the abort comes from (file:line, develop `dc8626e9c`)

Resolution is catalog-first, and the catalog is the sole gate authority when the release keys
match:

- `scripts/pr-gate-plan.py:1821` `coverage_path = ROOT / 'pr-gate-coverage.json'`
- `scripts/pr-gate-plan.py:1824` `if coverage.get('release') == result['release']:` — develop
  catalog `release` is `v0.4.27`, and the plan's release is `v0.4.27`, so the catalog branch runs.
- `scripts/pr-gate-plan.py:1825-1826` collects every changed `path`/`old_path`/`new_path` from
  the diff.
- `scripts/pr-gate-plan.py:1827` `covered, unowned = resolve_covered_gates(paths, coverage)`.
- `scripts/pr-gate-plan.py:1833-1834` keeps only `cmd/`+`internal/` paths as `source_unowned`
  (docs, pins, `scripts/**` deliberately stay outside this guard).
- **`scripts/pr-gate-plan.py:1835-1838` — the abort. Any uncataloged `cmd/**` or `internal/**`
  source path raises `ValueError` and Trusted Plan fails closed.** This is the fail-loud
  guardian introduced by card **0428-242** in `676909a78`
  ("0428-242: catalog cmd/baha/app_broker.go + fail-loud PR gate guardian (#1768)", 2026-11-22 14:25).
- Owner side of the lookup: `scripts/validate-pr-gate-coverage.py:17-40`
  `resolve_covered_gates()` — exact `components[].path` match first (`:30-31`), then
  `packages[]` directory prefix (`:33-36`), else `unresolved.append(changed)` at
  `scripts/validate-pr-gate-coverage.py:37`. Catalog `components` has 259 rows and `packages`
  only 4 roots (`contracts`, `internal/identityprovider`, `internal/runtimebroker`,
  `internal/metrics/testdata`). Measured against develop's own tree: **2,203 of 2,542**
  `cmd/**`+`internal/**` Go files (86.7 %) have no catalog owner, so the guardian fires on
  almost every untouched source path — it is a growing landmine, not a corner case.
- The message builder: `scripts/validate-pr-gate-coverage.py:66-84` `unresolved_source_error()`.
- Note that a `covered`/`unowned` split inside the same path set is *also* why the guardian
  fired rather than a broad fallback: `internal/application/perses_runtime_test.go` and
  `cmd/baha/app_perses_cli_test.go` (#1810) and `cmd/baha/env_destroy.go` (#1809) ARE cataloged;
  only their neighbours are not.
- Legacy path heuristics still add *their own* `unresolved` entries which the catalog cannot
  erase (`scripts/pr-gate-plan.py:1424` `cmd/baha/*.go` catch-all, `:1449`
  `internal/capability/` catch-all, `:1541-1544` `internal/application/` catch-all, merged at
  `:1861-1869`). Those are what keeps a plan `coverage_status=unresolved` /
  `broad_required=True` even after the guardian is satisfied, i.e. even a correct catalog row
  does not by itself produce a *narrow resolved* plan.

## Task 3 — ancestry verdict (correction #2: staleness is ruled out)

```
$ git merge-base --is-ancestor origin/develop 168d40950bae5b8fb31862b36ceaffbdd1862207; echo rc=$?
rc=0   (develop IS an ancestor of #1810 head)
$ git merge-base --is-ancestor origin/develop 034c0c7d21512a62b2ec236b779e84235da4f507; echo rc=$?
rc=0   (develop IS an ancestor of #1809 head)
$ git merge-base origin/develop 168d40950…  → dc8626e9c52be07a8ea5b87b468c5991b7540c4f
$ git merge-base origin/develop 034c0c7d2…  → dc8626e9c52be07a8ea5b87b468c5991b7540c4f
$ git log --oneline 168d40950..origin/develop → (empty)
$ git log --oneline 034c0c7d2..origin/develop → (empty)
```

Both heads are exactly one commit on top of current develop `dc8626e9c` (their base pointers are
up to date; `git log develop..<head>` lists only their own single commit). The runner's own
ancestry gate inside the same Trusted Plan step also passed — it aborted later, inside the
planner. **No rebase/hop is needed for either PR, and re-cutting them will not change the result.**

## Task 4 — offline reproduction, and what each fix variant actually does

All variants were run in `/tmp/hv37` against the **develop** copies of `pr-gate-plan.py`,
`validate-pr-gate-coverage.py`, `pr-gate-coverage.json`, `release-requirements.json`,
`pr-gate-map-v1.json` and a `pr-diff-base.py` output built from the real PR commits
(`head_sha`/`base` = the exact remote SHAs). Nothing was written into any product repo.

| Variant | #1810 | #1809 |
| --- | --- | --- |
| develop planner + develop catalog (what CI runs today) | `rc=1`, guardian abort, 3 uncataloged paths | `rc=1`, guardian abort, 2 uncataloged paths |
| develop planner + candidate-owned catalog rows (Task-4 fix) | `rc=0`, `unresolved`, `broad_required=true`, gates `atomic/docker/observability`, `atomic/podman/observability`, `integration/static/public-contracts` | `rc=0`, `unresolved`, `broad_required=true`, gates `atomic/docker/data-capabilities`, `integration/docker/coreless-lifecycle` |
| planner relaxed (guardian removed), develop catalog | `rc=0`, `unresolved`, `broad=true`, gates `atomic/docker/observability`, `atomic/podman/observability` | `rc=0`, `unresolved`, `broad=true`, gate `integration/docker/coreless-lifecycle` |
| pure self-change PR (`scripts/**` only, develop catalog) | `rc=0`, **`coverage_status=resolved`, `selected_gates=[]` (0 gates)** — the 0428-235 shape, reproduced, but green by design | same |
| native planner (`pr-native-gate-plan.py`, ci.yml:502-512) | `{"include":[{"id":"native/docker/perses-runtime-smoke","runtime":"docker"}]}` → ran and **passed** | `{"include":[]}` → `required=false`, job skipped, aggregate accepts |

Findings from the matrix:

1. The 0428-235 "zero gates" behaviour is real and reproducible, but only for a PR that touches
   `scripts/**` (and other non-`cmd`/`internal` paths) **and nothing else**: the guardian at
   `scripts/pr-gate-plan.py:1833-1834` deliberately filters to `cmd/`+`internal/`, so a
   catalog/planner self-change resolves with `selected_gates=[]` while still passing. That
   under-qualifies such PRs; it is **not** what blocks #1810/#1809.
2. Relaxing the planner (variant 3) fixes neither PR: it only changes *how* they fail
   (`unresolved`/broad instead of a traceback), so the guardian must stay.
3. Adding catalog rows (variant 2) removes the Trusted Plan abort but leaves
   `coverage_status=unresolved, broad_required=true` because of the legacy catch-all heuristics
   at `:1424`/`:1449`/`:1544`. Those PRs then run broad Go checks (cheap) plus the catalog-declared
   gates — green-capable, but not a narrow plan.

## The Draft Go reds on #1809 are stale runs, not a content blocker (correction #3)

`gh pr checks 1809` still *lists* `PR · Draft Go · cli-0..3` as fail, but those entries link to
run **45240994250** (jobs 137924751872 / 137924751799 / 137924752160 / 137924751866, created
18:41:06Z) — a superseded candidate that was **cancelled** at 18:40 by the next push
(`gh run list` shows 45240846474 `cancelled`, 45240994250/45242187529/45243281767 on the older
heads `034c0c7d2`/`48481d137`/`b10c651a0`). The aggregate in the **current** head run
45244415977 (19:00:52Z) reports `PR · Draft Go · ${{ matrix.shard }}` = **skipped**, because
`pr_draft_go_shards` needs a plan artifact that Trusted Plan never produced. Only Trusted Plan
and the aggregate are actually red in that run:

```
$ gh run view 45244415977 --repo mcpdev80/baseharbor --json jobs \
    --jq '.jobs[]|select(.conclusion=="failure")|.name'
PR · Trusted Plan
PR Selected Checks
```

Independent content check, in a fresh clean clone of the exact PR head in this lane's own zone
(`/tmp/hv37-clone`, real GitHub URL), package-scoped, no lifecycle containers started:

```
$ git clone --no-checkout --filter=blob:none https://github.com/mcpdev80/baseharbor.git /tmp/hv37-clone
$ git -C /tmp/hv37-clone checkout 034c0c7d21512a62b2ec236b779e84235da4f507
034c0c7d 0428-058: audit secret set/delete/list and env destroy outcomes
$ cd /tmp/hv37-clone && go vet ./cmd/baha/ ; echo rc=$?
rc=0
$ go test -count=1 -run "TestNothingZZZ" -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication" ./cmd/baha/
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.007s [no tests to run]
```

`go vet` compiles the whole `cmd/baha` package with its test files, so the candidate builds
clean. Focused test execution in the same clean clone (package-scoped, mandated skip set, no
lifecycle containers):

```
$ cd /tmp/hv37-clone && go test ./cmd/baha/ -count=1 -run "Secret" \
    -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"
ok  	github.com/mcpdev80/baseharbor/cmd/baha	28.180s        # (same command on develop dc8626e9c: ok, 27.657s)
$ cd /tmp/hv37-clone2 && go test ./internal/capability/ ./internal/application/ -count=1 -run "Perses" \
    -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"
ok  	github.com/mcpdev80/baseharbor/internal/capability	0.004s
ok  	github.com/mcpdev80/baseharbor/internal/application	0.179s
```

So #1809's new `cmd/baha/secret_audit_test.go` (which uses only `t.TempDir()` and the injected
`targetStateRoot` seam, i.e. a package test) is locally green and passes on develop too; it
needs the Go shards to actually run in CI, not a native runtime gate. **Conclusion: both PRs are
code-clean and gate-blocked; the unproven point for #1809 is only that its Go shards have never
executed on the final head.**

## Minimal owner-scope fix PROPOSAL (not applied — pure finding)

Order matters: P1 unblocks #1810; P2+P3 unblock #1809; P4 closes the 0428-235 hole that is real
but is not the blocker here; P5 is the structural follow-up.

### P1 — three catalog admission rows (unblocks #1810; one-PR, no planner change)

Add to `scripts/pr-gate-coverage.json` `components[]` (insertion points: after the Perses rows at
`scripts/pr-gate-coverage.json:612` and after the `internal/capability` rows around `:1694`):

```json
{"id": "source.internal.application.perses.lifecycle.test.go",
 "path": "internal/application/perses_lifecycle_test.go",
 "runtime_specific": true,
 "surfaces": ["source.gate.atomic.docker.observability"],
 "required_test_names": ["TestPersesLifecycleUnauthorizedIsFailClosed",
   "TestPersesLifecycleUnresolvedOwnershipFailClosed",
   "TestPersesLifecycleEnableSetsPersesFlag",
   "TestPersesLifecycleEnableIdempotentWhenAlreadySelected",
   "TestPersesLifecycleRemovePreservesBackendDataOwners",
   "TestPersesLifecycleRejectsPersesWithoutObservabilitySurface",
   "TestPersesLifecycleStatusThreeStates",
   "TestPersesLifecycleBackendPreservedInvariant"]},
{"id": "source.internal.capability.perses.go",
 "path": "internal/capability/perses.go",
 "surfaces": ["source.gate.integration.static.public.contracts"]},
{"id": "source.internal.capability.perses.test.go",
 "path": "internal/capability/perses_test.go",
 "surfaces": ["source.gate.integration.static.public.contracts"]}
```

Rationale, pinned to precedent, not to the error text's generic example: `internal/capability`
production code is bound to `integration/static/public-contracts` in the same pattern as its
siblings `internal/capability/lifecycle.go`, `service_binding.go`, `service_binding_test.go`
(`scripts/pr-gate-plan.py:1433-1445`, the core-390/"reference existing gates, no new gate"
decision). The Do-not-do version: the guardian's own hint would instead bind these Perses files
to `atomic/{docker,podman}/data-capabilities`, which is the wrong surface (Perses is the
observability management seam, `scripts/pr-gate-coverage.json` gate `atomic/docker/observability`
`covers`). Optionally also append
`"source.internal.application.perses.lifecycle.test.go"` to
`native_checks[id="native/docker/perses-runtime-smoke"].source_components`
(`scripts/pr-gate-coverage.json:3531`) so the same test file keeps its native smoke route —
verified: it does not change the plan outcome.

### P2 — one catalog admission row + route it to a real gate (unblocks #1809's Trusted Plan)

```json
{"id": "source.cmd.baha.secret.operations.go",
 "path": "cmd/baha/secret_operations.go",
 "surfaces": ["source.gate.atomic.docker.data.capabilities",
               "source.gate.atomic.podman.data.capabilities"]},
{"id": "source.cmd.baha.secret.audit.test.go",
 "path": "cmd/baha/secret_audit_test.go",
 "surfaces": ["source.gate.atomic.docker.data.capabilities",
               "source.gate.atomic.podman.data.capabilities"]}
```

Verified effect: `rc=0`, abort gone, `broad_required=true`, gates `atomic/docker/data-capabilities`
+ `integration/docker/coreless-lifecycle`, `native matrix` stays `{"include":[]}` (so
`PR · Native gate plan` still skips and the aggregate still accepts — a native route would be an
extra, and per 0428-242's fail-loud test in `scripts/test_pr_gate_coverage.py:640-666`, must be
declared deliberately, not guessed). Cheaper and more honest alternative for the second row:
these are package tests, so the real coverage is `cli-package-tests`/Go shards, reached via P3.

### P3 — the planner condition that makes a cataloged source actually resolve (one condition)

`scripts/pr-gate-plan.py:1861` currently reads `if unowned:` before appending
`'legacy runtime impact has no declared gate coverage: …'`. Change it to the "catalog owns this
path" test:

```python
                if unowned:
                    catalog_owned = {row['path'] for row in coverage.get('components', [])} | {
                        row['path'] for row in coverage.get('packages', [])}
                    legacy_unowned = [p for p in unowned
                                      if not (p in catalog_owned or
                                              p.startswith('cmd/') or p.startswith('internal/'))]
                    if legacy_unowned:
                        result['reasons'] = … (as today, but with legacy_unowned)
                        result['coverage_status'] = 'unresolved'
                        …
```

i.e. a source path that *is* declared in the catalog must not be re-marked unresolved by the
legacy catch-alls at `:1424`/`:1449`/`:1544`. Measured with P1+P3 and P2+P3 (planner patched in
`/tmp` only, catalog from the candidate): both PRs go from `unresolved/broad=True` to
`coverage_status=unresolved → resolved` with the narrow gate sets listed above, and their
`required_validation_checks` become the existing CI-routed checks
(`capability-package-tests`, `cli-build`, `cli-gofmt`, `cli-package-tests`, `cli-vet`,
`source-contracts`) — every one of which already has a CI job (`ci.yml` `pr_validations` /
`pr_unit_shards`), so P1+P2 satisfy the "new coverage must be reachable by a real CI check" rule
inside the same PR.

### P4 — close the 0428-235 self-selection hole, without weakening the guardian

`scripts/pr-gate-plan.py:1833-1834` filters the guardian to `cmd/`+`internal/`, so a PR that
changes only `scripts/pr-gate-coverage.json` / `scripts/pr-gate-plan.py` /
`.github/workflows/ci.yml` resolves with `selected_gates == []`. Minimal addition, same place
(right after `:1838`, before `:1839`):

```python
            ci_self_change = [p for p in paths if p.startswith('scripts/') or
                              p.startswith('.github/workflows/')]
            if ci_self_change and not covered and 'pr-planner-tests' not in {
                    row['id'] for row in result['required_validation_checks']}:
                raise ValueError('CI self-change selects zero gates: ' + ', '.join(ci_self_change))
```

The gate that then must run is the one already in the base plan
(`pr-planner-tests`, `ci.yml:1645`, which already executes
`scripts/test_pr_gate_plan.py` and `scripts/test_pr_native_gate_plan.py`). Note the honesty limit:
today that route is only *half* open, because the existing self-change test in
`scripts/test_pr_gate_plan.py:2163` uses `scripts/pr-gate-plan.py` as its diff fixture, and the
suite's shared catalog is an in-memory `v0.4.26` one (`:25-38`) so the real
`{release: v0.4.27}` catalog branch is never exercised in unit tests. P4 should therefore also
add a regression test that asserts `selected_gates != [] or 'pr-planner-tests' in checks` for a
`scripts/pr-gate-coverage.json`-only diff against the real catalog.

### P5 — structural follow-up (not needed for #1810/#1809, but it is the recurring cost)

`internal/**` and `cmd/**` catch-alls are the reason every new file becomes a gate incident
(86.7 % of Go files uncataloged, measured above). Options, in cost order: (a) add
`packages[]` roots for the hot directories (`cmd/baha`, `internal/capability`,
`internal/application`) with their honest surface sets, so a *new file* inherits coverage instead
of aborting the plan; (b) automate admission rows from `go list -deps` so a card never hand-edits
the catalog; (c) replace the per-file guardian with a package-level "must be admitted" inventory
check. Whichever is chosen, keep `unresolved_source_error()` (`validate-pr-gate-coverage.py:66-84`)
as the fail-loud face.

## Answer to the coordinator's question

- Are #1810 and #1809 "code-clean but gate-blocked"? **Yes, both of them** — with one caveat
  each.
  - **#1810:** its candidate builds and its Perses tests pass; the only red is the Trusted Plan
    guardian (P1) plus the unresolved-legacy quirk (P3). Its native gate
    `PR · Native · native/docker/perses-runtime-smoke` already passed (job 137949201916).
  - **#1809:** `go vet`/build clean at head `034c0c7d2` (clean-clone witness above); its red
    `Draft Go` entries in `gh pr checks` are stale/cancelled runs, not its current head. Caveat:
    its Go shards have never executed on the final head, so its new `secret_audit_test.go`
    assertions are unproven in CI until P1/P2+P3 route them.
- Is it the 0428-235 self-change bug? **Yes, the card is the right home for the fix**, but the
  observed failure is the *companion* fail-loud guardian from card 0428-242
  (`scripts/pr-gate-plan.py:1835-1838`): the planner does not "select zero gates" on these PRs —
  it aborts before producing a plan, because the changed files have no admission rows. The
  zero-gate self-selection behaviour 0428-235 describes is separately reproduced above (variant 4)
  and needs P4.
- Is base-ancestry/rebase staleness a cause? **No.** Both heads descend from current develop
  `dc8626e9c` with an empty `develop..<head>` log except for their own commit, and the 0428-235
  native-planner-missing-from-base warning pattern does not appear in either log.

## repo-rule compliance

- Read-only hunt: no product edits, no branch, no PR, no merge, no `scripts/**` or `.github/**`
  change, no workflow_dispatch, no rerun (mission line 5 + owner scope).
- All planner/catalog experiments ran in `/tmp/hv37` (worktree/cache zone beside the session),
  against `git show origin/develop:<file>` copies. Nothing was appended to any product repo.
- Evidence lives only in baseharbor-plan (`evidence/recovery-2026-11-23/hunt-hv37-trusted-plan-planner/`).
- No subagents (Owner directive 2026-11-04): every step executed in this session.
- No containers/compose projects started on this host (owner directive 2026-11-05); the only Go
  command run was the named-form package test with the mandated
  `-skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"`.
- No credentials or tokens read or logged; `gh` used only for read-only PR/run/job/log queries.
- CardBoard hygiene: this file contains no markdown checkboxes anywhere.

## cleanliness

- Read-only mission: no stack, no worktree, no compose project, no volumes, no state dirs.
  Two disposable clones in this lane's own scratch zone (`/tmp/hv37-clone`, `/tmp/hv37-clone2`)
  were used only for `go vet`/focused `go test` on the exact PR heads; they started no containers.
- `docker ps -a` before (host = coordinator/codeman server, so no test stack is allowed here):

```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

- `docker ps -a` after: identical (empty, no test containers or networks owned by this lane).
  `docker images` was never written to: nothing built, pulled, pruned or removed; the ambient
  `ambient-core/` set and the ambient `bh-docker-dev-shared-*` network are untouched.
- `docker ps -a` witness taken by this lane (shell pid 883382, coordinator host) at commit time:
  header row only, zero containers — before and after are the same empty list.
- Cleaned up at the end: the two `/tmp/hv37-clone*` checkouts and the `/tmp/hv37` scratch dir.
- Nothing created under `/home/marcel/dev/baseharbor-ecosystem` besides this evidence file.

## PLAN (board mirror)

Board file: `workers/todos/w37-0428-235-hvtrustedplan.json` (tick as worked:
remote/zone resolve → develop attestation → failing logs → planner read + file:line →
touched files → ancestry verdict → cause classification → fix proposal → evidence+push → END).

## END

END_DONE w37-0428-235-hvtrustedplan: Trusted Plan reds are the 0428-242 catalog guardian
(`scripts/pr-gate-plan.py:1835-1838`) on uncataloged sources, not a zero-gate plan and not
staleness; 0428-235 confirmed as owner card yes; #1810 gate-blocked only, #1809 additionally
build-red (undeclared dep on #1810); candidate SHAs 168d40950bae5b8fb31862b36ceaffbdd1862207 /
034c0c7d21512a62b2ec236b779e84235da4f507, base dc8626e9c52be07a8ea5b87b468c5991b7540c4f.
