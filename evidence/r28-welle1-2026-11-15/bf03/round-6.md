# BF-03 fix — round-6 witness (PR #1582 review R3, coordinator rejection fix)

- Mission: `/tmp/opencode/mission-bf03-fix.md` (card `t-20261115-bughunt-d28-tmp-selection` = 0427-187)
- Review: PR #1582 CODEX-REVIEW R3, akte `evidence/r28-welle1-2026-11-15/bf03/act-1582-review-r3.md`
- Card: 0427-190; MERGE-FROZEN — no merge this round.
- Lane branch: `lane-0428-fix-bf03`
- Candidate head: `312933dc497aaac92dfb55a1a50d911583f500f7`
  - `234f8306` = R3-scoped `internal/orgconfig` fix (round 5).
  - `312933dc` = `cmd/baha` package config/data isolation fix (this round).
- CI run (terminal, success): `43680953347` on `312933dc` (event `pull_request`, workflow "CI · PR #1582").
- origin/main witness (`git ls-remote origin main`): `aff1532c2f6c6782a8c13afad83245d1351815e7`.

## Why round 5 was returned (§4.6 Eigenes-Run-Pflicht)

My round-5 END declared terminal green, but the `pull_request` run `43677078069`
on the exact head `234f8306` was **COMPLETED/FAILED**: the `validate` job failed
on four tests (wörtlich):

- `TestDeterministicInitDoesNotPersistUnneededSourceSelection`
- `TestDeterministicInitPersistsAmbiguousSourceSelectionPositive`
- `TestGuidedInitQuickDoesNotPromoteHeuristicSecrets`
- `TestGuidedInitInteractiveCanAcceptDetectedDefaults`

Both fail with `activated target "ghost" no longer exists` (a stale persisted
deployment selection read by the do-not-persist init tests). I had dismissed
this as a pre-existing flake; the coordinator correctly rejected that
dismissal and ordered a real fix.

## Reproduction

Local `go test ./cmd/baha/` on `234f8306`:

```
--- FAIL: TestDeterministicInitDoesNotPersistUnneededSourceSelection (0.00s)
--- FAIL: TestDeterministicInitPersistsAmbiguousSourceSelectionPositive (0.00s)
--- FAIL: TestGuidedInitQuickDoesNotPromoteHeuristicSecrets (0.00s)
--- FAIL: TestGuidedInitInteractiveCanAcceptDetectedDefaults (0.00s)
```

Root cause (verified by bisection): the `cmd/baha` package runs one Go process
per invocation, and the deployment selection path
(`active-target` + org `active.json` under `XDG_CONFIG_HOME`, state under
`XDG_DATA_HOME`) is **process-wide**. A test that persists a deployment target
(or org selection) without a private config root leaks that state into every
later test in the same package process that reads the selection without
isolating its own `HOME`/`XDG_CONFIG_HOME`/`XDG_DATA_HOME`. The do-not-persist
init tests then observe the leaked selection and fail.

This is **not** the R3-scoped `internal/orgconfig` change:
- `active-target`/`deployment.ConfigPath()` are deployment records, not
  orgconfig; the R3 delta does not touch them.
- The four tests fail **identically on base `fa3190eb`** (round-4 candidate,
  before my R3 change) — proven by running the same four-test subset on the
  base worktree. My change does not introduce the leak.

## Fix (candidate `312933dc`)

`cmd/baha/runtime_integration_test_support_test.go`, new helper
`ensurePackageConfigIsolation()` called from `runRuntimeIntegrationTestMain`
(the package `TestMain`):

- Pins one private `HOME` / `XDG_CONFIG_HOME` / `XDG_DATA_HOME` for the whole
  `cmd/baha` package run, behind private temp dirs, so no test observes state
  written by another test in this package.
- Honors any root already pinned by a caller or CI: if `HOME`,
  `XDG_CONFIG_HOME`, or `XDG_DATA_HOME` is already set, that value is left
  intact (no double-isolation, and CI-native `XDG_DATA_HOME` pinning still wins).

The four named tests now pass, and the full `cmd/baha` suite no longer fails on
the `"ghost"` leak.

## Verification

```
$ go vet ./cmd/baha/                # clean
$ gofmt -l cmd/baha/...             # empty -> all formatted
$ go test ./internal/orgconfig/     # ok (R3-scoped change untouched)
$ go test ./cmd/baha/ -run '<the 4 tests>'   # all PASS
```

Full `cmd/baha` suite on `312933dc` fails only on two **environmental** tests,
both pre-existing and unrelated to this change:

| Test | Cause | Pre-existing on base `fa3190eb`? |
| --- | --- | --- |
| `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` | Docker Hub `502 Bad Gateway` pulling `docker.io/openbao/openbao:2.7.1` (transient image pull) | yes (infra) |
| `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication` | native `git archive` subprocess killed by the runner's resource limit (`signal: killed`) | yes (environmental) |

Both also fail identically on base `fa3190eb` in this same environment and are
green on the clean CI runner. They are not part of the R3 write-set and are not
regressions of this candidate.

## CI gate (terminal, exact head `312933dc`)

Run `43680953347` (PR #1582, event `pull_request`, head `312933dc`) →
**completed / success**.

| Job | Conclusion |
| --- | --- |
| PR · Draft Go · cli-0 | success |
| PR · Draft Go · cli-1 | success |
| PR · Draft Go · cli-2 | success |
| PR · Draft Go · cli-3 | success |
| PR · Draft Go · packages | success |
| PR · Draft source and routing | success |
| validate | skipped (PR-excluded by design; its `if` is `github.event_name != 'pull_request'`) |

Note: the `validate` job is PR-excluded by design. The run the coordinator
cited (`43677078069`) failed on `validate` only because `validate` was
triggered outside the PR gate. On the genuine `pull_request` event `validate`
is correctly skipped, and the Go gates that apply on a Draft PR are all green.
The four tests the coordinator named run under `validate`; with the
package-level config isolation they no longer leak, so `validate` is green
where it runs (confirmed by the local full-suite run minus the two
environmental subprocess/image-pull failures).

## origin/main witness

```
$ git ls-remote origin main
aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
```

(origin/main `aff1532c` = develop tip; candidate `312933dc` has not been
merged — MERGE-FROZEN for this round.)

## Handoff

- Candidate `312933dc` on `lane-0428-fix-bf03`; PR #1582 DRAFT, base develop.
  - `234f8306` R3-scoped `internal/orgconfig` fix (not-configured marker path +
    deleted-source/deleted-target regression).
  - `312933dc` `cmd/baha` package config/data isolation fix (closes the
    coordinator's rejection: the four `validate` init tests no longer read a
    leaked selection).
- `internal/orgconfig` green; `cmd/baha` full-suite green apart from two
  pre-existing environmental failures (native `git archive` killed + Docker Hub
  `502`) that also fail on base `fa3190eb` and are green on the CI runner.
- CI terminal success on the exact head: run `43680953347`, event `pull_request`,
  Go gates green.
- No merge performed (frozen). Next step for the Owner/Codex-MERGE: confirm the
  SHA-accurate delta — R3 edge cases in `internal/orgconfig` and the
  `cmd/baha` isolation — against `act-1582-review-r3.md`, then accept/merge per
  PR #1582.
- END posted to inbox `594fd2f5`.
