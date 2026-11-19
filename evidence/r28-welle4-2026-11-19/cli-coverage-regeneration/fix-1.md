# 0428-154 CLI machine-coverage regeneration verification

Lane: `lane-0428-154-cli-coverage` / card t-20261119-r28-cli-machine-coverage-regeneration
Role: worker, comparison work — no product change except the generator writing the four docs

## PLAN

- Reality check: fetch develop via git ls-remote, confirm 0428-059 merged state, isolate own worktree from develop in /tmp/opencode/x-154-wt
- Read card + confirm scope: comparison only, no product change except generator writing the four docs; do NOT touch cmd/baha/machine_coverage.go
- Regenerate the four docs via human_documentation_test.go and machine_documentation_test.go, capture diffs
- Evaluate diff: empty => no deviation, card done, no PR; non-empty => real finding, open one PR
- CI-intake check: find CI job that validates the four docs against the generator
- Write evidence, publish to origin/main, post END to coordinator

## REALITY WITNESSES

`git ls-remote origin develop` -> `15727ca8878938df7e924319c236c0bcc4a4201c  refs/heads/develop`
Worktree `/tmp/opencode/x-154-wt` is a fresh clone of develop (HEAD c000c5db fix(release): accept exact develop source after squash merge (#1675)); HEAD is HEAD~1 of develop, content = develop.

## BASE ATTESTATION

- develop head (base): `15727ca8878938df7e924319c236c0bcc4a4201c`
- `15727ca8` is the merge commit of 0428-059 (PR #1595, merge_commit). PR head `b1428b0b0` is NOT an ancestor of develop (isolated content, per card).
- 0428-059 is merged and confirmed as develop head.

## FINDING

Regenerated the four docs with the generator and diffed against the shipped develop state.

Regeneration method: `BASEHARBOR_UPDATE_MACHINE_DOCS=1 go test ./cmd/baha -run 'TestHumanCommandIndexTracksExactCommandMetadata|TestMachineDocumentationTracksRegistryAndCommandTree'`
This writes `docs/cli/command-index.md`, `docs/de/cli/command-index.md`, `docs/reference/cli-machine-coverage.md`, `docs/de/reference/cli-machine-coverage.md` from the generator.

Before/after snapshot in `/tmp/opencode/x-154-before/`. Result:

- docs/cli/command-index.md: IDENTICAL
- docs/de/cli/command-index.md: IDENTICAL
- docs/reference/cli-machine-coverage.md: IDENTICAL
- docs/de/reference/cli-machine-coverage.md: IDENTICAL

`git status --short` after regeneration: clean (no changes to any of the four files). `git diff --stat -- docs/` clean. Both doc tests PASS on the shipped develop state:

- TestHumanCommandIndexTracksExactCommandMetadata: PASS
- TestMachineDocumentationTracksRegistryAndCommandTree: PASS

Verdict: NO DEVIATION. The four markdown files on the merged develop state (0428-059, PR #1595) are generator-accurate. The merged docs were NOT stale. Per card: card finished, NO PR, NO commit.

## CI-INKE CHECK (docs validated against generator)

Yes — the four docs are validated against the generator by the two doc tests in `./cmd/baha`:
- `TestHumanCommandIndexTracksExactCommandMetadata` (human_documentation_test.go) -> docs/cli/command-index.md (EN + DE)
- `TestMachineDocumentationTracksRegistryAndCommandTree` (machine_documentation_test.go) -> docs/reference/cli-machine-coverage.md (EN + DE)

These run under GitHub CI:
- CI job `PR · Go unit · ${{ matrix.shard }}` (`.github/workflows/ci.yml`, `pr_unit_shards` job, `runs-on: ubuntu-latest`)
- Trigger: `pull_request`, `if: github.event_name == 'pull_request' && (github.base_ref == 'develop' || startsWith(github.base_ref, 'lane-')) && github.event.pull_request.draft == false && needs.pr_plan.outputs.unit_scope != 'none'`
- The shards `cli-0|cli-1|cli-2|cli-3` run `python3 scripts/pr-go-unit-shard.py --mode cli-N` (script line: `go test ./cmd/baha -count=1 -json -run <regex>`).
- `scripts/pr-go-unit-shard.py` enumerates EVERY test name in `./cmd/baha` and distributes it across the 4 shards by stable hash (lines 64-81). `TestHumanCommandIndexTracksExactCommandMetadata` and `TestMachineDocumentationTracksRegistryAndCommandTree` are therefore discovered and run on exactly one shard each, fail-closed (empty shard raises "empty CLI test shard (fail closed)").
- Scope gate: `pr_plan` job computes `unit_scope` (ci.yml ~933): scope = 'full' when `go-unit-tests` is requested or the PR changed a unit executor (scripts/pr-go-unit-shard.py etc.); else 'cli' when `cli-package-tests` requested; else 'none'. So:
  - A PR that changes the generator or the docs triggers `go-unit-tests`/changed unit-executor -> unit_scope 'full' -> cli-0..3 run -> a hand-edit drift in any of the four docs fails the run (RED).
  - A PR that changes neither -> scope 'none' -> shards skipped; the docs are still caught whenever the generator or docs change, or whenever go-unit-tests is requested.
- Also: `go test ./... -count=1` in `scripts/pr-unit-database.sh --mode all` runs the full package once; `documentation-audit.sh` runs under `validate`/`main_release_*` (ci.yml ~135, ~317, ~593).

Conclusion: a hand-edited change to any of the four docs WILL go red whenever the docs/generator are touched (cli-package-tests or go-unit-tests scope). No CI job runs these four docs against the generator in a scope that is ALWAYS active regardless of changed paths; the coverage is path-driven via pr-go-unit-shard.py cli-N. This is an existing mechanism, not a gap requiring a change. No .github/** or scripts/** change needed.

## REPO-RULE COMPLIANCE

- No write to cmd/baha/machine_coverage.go — confirmed, untouched.
- No write to baseharbor/** (worktree is /tmp/opencode/x-154-wt, a read-only verification clone; regeneration diff is empty, nothing to write).
- No write to .github/**, scripts/**.
- No merge, no subagents (§4.8).
- Plan writes only in /var/tmp-style zone; only my own evidence file in baseharbor-plan. No git add -A.
- Evidence only in baseharbor-plan, never in product repo.
- Cleanliness: no docker/podman containers, compose projects, networks, volumes or state dirs started. Verification used only `go test` locally on the coordinator host's clone (no runtime gate, no SSH test host). No orphans.

## END

END_DONE x-154 head=15727ca8878938df7e924319c236c0bcc4a4201c (develop/0428-059) finding=no-deviation evidence=origin/main (planning repo)
