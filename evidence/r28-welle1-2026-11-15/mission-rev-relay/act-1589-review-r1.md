# act-1589-review-r1.md — PR #1589 CODEX-REVIEW (frost, no merge)

ROLE: CODEX-REVIEW (no merge). Shift r28-welle1, 2026-11-15. Card 0427-020 (consumption examples).

## PLAN

1. Verify PR #1589 head/base refs, exact-head run witness (from lane akte).
2. Examples use only accepted APIs (no invented flags) — check every `baha` command/flag in the example ymls against develop.
3. No `.github/**` changes.
4. EN/DE pattern consistent; diff = docs only.
5. Write APPROVE/REJECT, validate, publish evidence on origin/main, verify remote, post END.

## Candidate and provenance

PR #1589 OPEN/DRAFT (frost), base develop `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`, exact head `442755b35dc3c6d6a4d18915f510adee9113d32f`. Product `git ls-remote`:

```text
442755b35dc3c6d6a4d18915f510adee9113d32f	refs/pull/1589/head
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
```

Base `0e9ccb582` is an ancestor of the reviewed head (`git merge-base --is-ancestor` succeeded). Base-to-head log contains only the candidate's own commit (docs/0427-020 consumption examples).

## Point 2 — examples use only accepted APIs (no invented flags)

Every `baha` command used in the example workflows resolves to a registered develop subcommand, and every flag used is supported on develop:

Example commands (github-actions/consume.yml, gitlab-ci/pipeline.yml):

```
baha version
baha app inspect . --plain
baha app inspect . -o json
baha app plan -o json
baha app secret set API_KEY --stdin
baha app preflight
baha app apply --yes
baha app status -o json
baha app env dev --format json
baha app creds postgres
baha app down --yes
```

- All subcommands present in the develop `baha` registered-inventory (140 subcommands; `secret`, `preflight`, `apply`, `status`, `env`, `creds`, `down`, `plan`, `inspect`, `version` all registered).
- Flags verified against develop: `app inspect --plain` and `-o json` (`cmd/baha/app_inspect.go` Usage: `--plain`, `-o json|--output json|--json`); `app plan -o json` (`cmd/baha/app_commands.go:242` Usage `baha app plan [NAME] [-o json|--output json]`, `parseReadOutputArgs`); `app env --format json` (`cmd/baha/app_env.go:21` Usage `--format dotenv|shell|json|yaml`). No invented flags.

## Point 3 — no .github changes

```
git diff --name-only develop..1589 | grep '^\.github/'   -> (none)
```

OK: no `.github/**` files touched.

## Point 4 — EN/DE pattern consistent; diff = docs only

```text
docs/de/example/github-actions/README.md   +54
docs/de/example/gitlab-ci/README.md        +52
docs/de/how-to/ci-consumption.md           +224
docs/example/github-actions/README.md      +53
docs/example/github-actions/consume.yml    +97
docs/example/gitlab-ci/README.md           +50
docs/example/gitlab-ci/pipeline.yml        +69
docs/how-to/ci-consumption.md              +214
mkdocs.de.yml                              +3
mkdocs.yml                                 +3
```

- EN/DE parallel files: how-to 1:1 (ci-consumption.md), example 4 EN : 2 DE (github-actions + gitlab-ci README + yml each mirrored).
- Relative link resolves: `docs/example/github-actions/README.md -> ../../how-to/ci-consumption.md` (present at head); `docs/example/gitlab-ci/README.md -> ../../how-to/ci-consumption.md`.
- mkdocs nav wired for both languages: `mkdocs.yml` lines 127-129 (`CI consumption of a release`, `GitHub Actions example`, `GitLab CI example`).
- No product code: only docs/ + mkdocs nav.

## CI witness

Exact-headed `pull_request` run for #1589 (from lane akte): success on head `442755b3`. No rerun or workflow_dispatch initiated; no failing or cancelled check.

## Verdict

APPROVE #1589 at `442755b35dc3c6d6a4d18915f510adee9113d32f`. Examples use only accepted develop APIs (`--plain`, `-o json`, `--format json` all supported; no invented flags); no `.github/**` change; EN/DE parallel pattern consistent; relative mkdocs links resolve; diff is docs-only (+ mkdocs nav). CI success on exact head. No product code, workflow, CI, container or VM changed. PR #1589 NOT merged (frost honoured).

## repo-rule compliance

Evidence in the actual planning repository (verified before commit). Product remote state from a fresh clone and `git ls-remote`; the quarantined workers checkout was not used. No product code, `.github/**` files, CI, containers or VMs changed. No merge. No markdown checkbox lines.

## END mission-1589-r1 DONE — APPROVE #1589 at 442755b35dc3c6d6a4d18915f510adee9113d32f

## Planning validation

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed successfully. `git diff --check` passed. No Markdown checkbox lines.

Planning origin/main witness before push (`git ls-remote origin refs/heads/main`):

```text
8216d11a6d21c62dd6193a9f13162ad3201719e4	refs/heads/main
```
