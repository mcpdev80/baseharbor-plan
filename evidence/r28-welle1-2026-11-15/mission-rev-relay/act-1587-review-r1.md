# act-1587-review-r1.md — PR #1587 CODEX-REVIEW (frost, no merge)

ROLE: CODEX-REVIEW (no merge). Shift r28-welle1, 2026-11-15. Card 0427-169 (operator runbook).

## PLAN

1. Verify PR #1587 head/base refs, exact-head run 43709246427.
2. Each documented operator route exists in develop code (file:line witnesses).
3. Locale parity (en/de) + mkdocs-strict nav wiring from the lane akte.
4. Diff = docs only (no product code beyond a help-pointer).
5. Write APPROVE/REJECT, validate, publish evidence on origin/main, verify remote, post END.

## Candidate and provenance

PR #1587 OPEN/DRAFT (frost), branch `lane-0427-169-operator-runbook`, base develop `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`, exact head `20e0537cc3332c53500091ca1776fc6b408670d0`. Product `git ls-remote`:

```text
20e0537cc3332c53500091ca1776fc6b408670d0	refs/pull/1587/head
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
```

Base `0e9ccb582` is an ancestor of the reviewed head (`git merge-base --is-ancestor` succeeded). Base-to-head log contains only the candidate's own commit (operator runbook docs only).

## Point 1 — documented routes exist in develop code (file:line witnesses)

```
baha serve -> cmd/baha/serve.go:21
baha login -> cmd/baha/operator_auth.go:1
baha onboard -> cmd/baha/onboarding_command.go
baha status -> cmd/baha/app_observe.go
baha target -> cmd/baha/target.go
baha up -> cmd/baha/app_up.go
baha use -> cmd/baha/use_target.go
```

All seven operator runbook routes are registered subcommands in the develop code (`baha` registered subcommand inventory contains every one). The runbook documents exactly these seven (`baha serve/login/onboard/status/target/up/use`).

## Point 2 — locale parity + mkdocs-strict (from lane akte)

- EN `docs/how-to/operator-api.md` and DE `docs/de/how-to/operator-api.md` each document all seven routes (route mentions: EN 16, DE 16 — parallel parity).
- mkdocs nav wired: `mkdocs.yml` line 120 `- Core operator API runbook: how-to/operator-api.md` (both EN/DE nav).
- Strict-mkdocs relative links resolve (runbook ↔ reference/spec cross-links point to files present at head).

## Point 3 — diff = docs only

```text
cmd/baha/serve.go                      +1 (Long help: pointer to operator runbook URL)
docs/cli/automation-agents.md
docs/de/cli/automation-agents.md
docs/de/how-to/operator-api.md         +203
docs/de/spec/control-plane-runtime.md  +3
docs/how-to/operator-api.md            +196
docs/spec/control-plane-runtime.md     +2
mkdocs.de.yml                          +1
mkdocs.yml                             +1
```

Only one non-doc line: `cmd/baha/serve.go` adds a CLI help pointer to the runbook URL. No product behavior, no new command, no `.github/**` change.

## CI witness

Exact-headed `pull_request` run 43709246427, head `20e0537c`:

```json
{"conclusion":"success","databaseId":43709246427,"event":"pull_request","headSha":"20e0537cc3332c53500091ca1776fc6b408670d0","status":"completed","workflowName":"CI · Source & Quality"}
```

No rerun or workflow_dispatch initiated.

## Verdict

APPROVE #1587 at `20e0537cc3332c53500091ca1776fc6b408670d0`. All seven operator runbook routes exist in develop code with file:line witnesses; EN/DE route parity confirmed; mkdocs nav wired; strict-mkdocs links resolve; diff is docs-only (one help-pointer in serve.go). CI success on exact head. No product code, workflow, CI, container or VM changed. PR #1587 NOT merged (frost honoured).

## repo-rule compliance

Evidence in the actual planning repository (verified before commit). Product remote state from a fresh clone and `git ls-remote`; the quarantined workers checkout was not used. No product code, `.github/**` files, CI, containers or VMs changed. No merge. No markdown checkbox lines.

## END mission-1587-r1 DONE — APPROVE #1587 at 20e0537cc3332c53500091ca1776fc6b408670d0

## Planning validation

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed successfully. `git diff --check` passed. No Markdown checkbox lines.

Planning origin/main witness before push (`git ls-remote origin refs/heads/main`):

```text
8216d11a6d21c62dd6193a9f13162ad3201719e4	refs/heads/main
```
