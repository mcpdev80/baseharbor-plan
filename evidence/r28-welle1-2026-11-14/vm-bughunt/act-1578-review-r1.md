# PR #1578 Review R1

## PLAN

1. Read task contract, fetch exact PR #1578 candidate/base, and verify hosted run witness.
2. Review UID lifecycle, idempotency, lock safety, rename behavior, CLI-entry tests, role separation, and file ownership.
3. Record SHA-specific verdict, evidence, and correction recipe in planning repository.
4. Validate and publish evidence to planning origin/main, verify remote presence, and post END.

ROLLE: CODEX-REVIEW. Read-only review; no merge.

## Candidate and provenance

- PR #1578 is OPEN/DRAFT, base `develop`, head branch `lane-0428-uid-environment`, candidate `670402fdefc57440a144365fce672b909a661228`.
- Exact `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1578/head` output:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
670402fdefc57440a144365fce672b909a661228	refs/pull/1578/head
```

- `git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c 670402fdefc57440a144365fce672b909a661228`: exit 0.
- `git log --format='%H %an <%ae> %s' 0e9ccb582f5bdcdc74049bbe3996263cdce6500c..670402fdefc57440a144365fce672b909a661228` lists only the task commit: `670402fdefc57440a144365fce672b909a661228 lane-0428-uid-environment <lanes@baseharbor.local> feat(environment): durable non-secret env identity per (target,env)`.
- Fresh clone `/tmp/opencode/mission-rev1578-review` was checked out detached at the exact candidate; product diff is four files, all within `internal/environment` and `internal/deployment`. No application, target, CLI, or workflow paths are changed. `git diff --check` is clean.

## Contract and review findings

BLOCKER — Rename stability is only implemented on the in-memory value, not in persisted state. `internal/environment/environment.go:78-85` returns a renamed value with its ID preserved, but persistence is keyed by environment name at `internal/deployment/environment_identity.go:43-56`. `GetEnvironment(target, newName)` at lines 130-145 looks only at that new-name path and creates a fresh UUID if it does not exist. There is no persisted rename operation or old-name-to-ID lookup. The rename unit test at `internal/environment/environment_test.go:75-92` tests only the pure value helper and does not exercise persistence. Thus a renamed environment reopened under its new name gets a new ID, contrary to the owner rule and contract §6 that names are mutable while environment IDs are stable.

BLOCKER — The serialized record writes the generated ID into the `name` field. `internal/deployment/environment_identity.go:80-85` marshals `EnvironmentRecord{Target: target, Name: id, Identity: id}`; line 116 repeats the same construction. The record therefore fails to retain the environment name and cannot serve as correct renameable metadata. The existing tests assert identity equality and path existence, but do not decode and assert `Target`, `Name`, or `Identity` together.

BLOCKER — No test enters through the real CLI, and the new seam is not called from `cmd/baha`. The diff adds only `internal/environment` and `internal/deployment` unit tests; `rg -n 'GetEnvironment|EnvironmentID' cmd --glob '*.go'` returns no matches. Tests exercise constructors and the store helper directly, so they do not prove any `baha` invocation creates/reuses the UID or preserves it on rename. This misses the mission's explicit real-CLI-entry criterion and leaves the capability unreachable through the CLI.

PASS — The identity type is a generated UUIDv4 and carries no secret material. The stored environment is scoped beneath the target state root rather than under an application or deployment path. The implementation does not reuse application IDs, deployment IDs, or target IDs. However, because record target/name metadata is not validated on read (`readEnvironmentRecord`, lines 61-73), add fail-closed binding validation and coverage before accepting cross-target isolation as complete.

PASS WITH GAP — A registry write lock is used for first creation after priming the target root (`environment_identity.go:147-179`; shared lock at `registry_lock.go:38-59`). The 32-goroutine test exercises concurrent first registration of one `(target,name)` (`environment_identity_test.go:81-133`). However, the bounded retry is a tight 4096-iteration loop and its exhaustion path assumes a winner has already persisted a readable record (`environment_identity.go:165-185`); consider a bounded retry/backoff with a safe contention error or a guaranteed read-after-winner test. No runtime compose project was started.

Correction recipe: persist a stable identity independently of the mutable name while keeping a single authoritative per-target environment state (not a second registry). Implement rename as an atomic metadata update retaining the UID; validate stored target/name binding on read; serialize the actual name, not the UID. Wire the relevant CLI operation to the seam in coordination with the CLI owner, and add end-to-end command tests that create/open, rename, and reopen through the actual `baha` entry point. Include regression assertions for brownfield reuse, concurrent first create, all record fields, and cross-target separation. Keep PR #1578 draft until these results are part of a candidate.

## Hosted CI witness

- Run `43644615047` completed with conclusion `success` on the exact candidate SHA `670402fdefc57440a144365fce672b909a661228`, event `pull_request`, workflow `CI · Source & Quality`.
- Active jobs passed: `PR · Draft source and routing`, `PR · Draft Go · cli-0`, `cli-1`, `cli-2`, `cli-3`, and `packages`.
- `PR Selected Checks`, workflow policy, source format, validation, and native/runtime jobs were skipped under draft selection. The run is terminal-success for the selected draft jobs; skipped checks are not reported as passed.
- No rerun or workflow dispatch was triggered. Current product CI selection maps Go package changes to the Draft Go groups; the mission requires actual CLI-entry tests to be included in the appropriate Go CLI group when added. `.github/**` is Owner scope and was not edited.

## Repo-rule compliance

- Evidence repository root, verified before the evidence commit: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (`git rev-parse --show-toplevel`).
- Planning `main` was fast-forward refreshed before review recording; reviewed planning HEAD was `acd32b2521bde91907d480b8f8e3043b9892cff6`.
- Exact `git ls-remote origin main` output immediately before publishing this evidence:

```text
acd32b2521bde91907d480b8f8e3043b9892cff6	refs/heads/main
```

- Only this evidence file is intended for the review commit. A pre-existing unrelated modified planning file was left untouched.
- `python3 scripts/plan.py check`: 531 tasks, 7 epics, 13 releases, 21 decisions; 0 errors, 10 pre-existing dependency warnings.

## Verdict

REJECT PR #1578 at `670402fdefc57440a144365fce672b909a661228` for persisted rename instability, incorrect serialized name metadata, and absence of real CLI integration/entry-point tests. Identity generation, target-scoped location, and the selected exact-head draft CI jobs otherwise show the intended direction. No merge.

END DONE — PR #1578 rejected; review evidence to be published on planning origin/main.
