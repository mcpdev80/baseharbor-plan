# act-1577-review-final.md — PR #1577 CODEX-REVIEW (frost, no merge)

ROLE: CODEX-REVIEW (no merge). Shift r28-welle1, 2026-11-15. Card 0428-092.

## PLAN

1. Verify PR #1577 head/base refs, candidate log/ancestry, exact-head run 43704566914.
2. Compare each of the six mirror files (before/after) against the 0428-092 scope (auth/role normative mirror; Perses pin/scope/state = factual mention + spec pointer).
3. Confirm `docs/spec/**` untouched; no word-walk findings, no new classes — APPROVE|REJECT against the rule only.
4. Write akte, validate, publish evidence on origin/main, verify remote, post END.

## Candidate and provenance

PR #1577 OPEN/DRAFT, branch `0428-092-perses-boundary`, base develop `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`, exact head `ab9086f5fc39d34348c7a5db49525cd14566c52a`. Product `git ls-remote`:

```text
ab9086f5fc39d34348c7a5db49525cd14566c52a	refs/heads/0428-092-perses-boundary
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
ab9086f5fc39d34348c7a5db49525cd14566c52a	refs/pull/1577/head
```

Base `0e9ccb582` is an ancestor of the reviewed head. Base-to-head log contains only the candidate's own commit:

```text
ab9086f5fc39d34348c7a5db49525cd14566c52a docs(0428-092): reduce Perses pin/scope/state to factual mention + spec pointer (owner decision 2026-11-15)
```

No foreign commit carried on top of the base.

## Scope (owner 0428-092, plan-head e1dd0508)

`docs/spec/management-access-v1.md` is NORMATIVE only for authentication and role-mapping findings. Perses PIN, RELEASE SCOPE and STATE SEMANTICS (not_configured/configured_unverified/verified) stay short factual release summaries — mention + pointer only, no normative verb, no spec anchor for Perses semantics. Review covers ONLY the agreed mirror spots.

## The six mirror files (before/after)

All EN+DE; pointer path `docs/spec/management-access-v1.md` stays English.

| File (EN/DE) | before | after |
| --- | --- | --- |
| docs/releases/v0.4.28.md (EN) | multi-sentence definition of the three states with "MUST NOT" language | single factual mention of the three names + pointer; normative definition lives in the spec |
| docs/de/releases/v0.4.28.md (DE) | equivalent normative definition (de) | equivalent mention + pointer (de) |
| docs/reference/releases.md (EN) | multi-sentence definition embedded in the reference paragraph | factual mention + pointer, surrounding scope sentence preserved |
| docs/de/reference/releases.md (DE) | equivalent normative definition (de) | equivalent mention + pointer (de) |
| docs/how-to/observability.md (EN) | procedural definition of the three states + health-path condition | factual status mention + spec pointer |
| docs/de/how-to/observability.md (DE) | equivalent procedural definition (de) | equivalent factual mention + spec pointer (de) |

- No normative "verified: only when a real Perses health probe observes" definition remains in any of the six files.
- The three names are mentioned, never defined, in these prose/release/reference/how-to files.

## Verification

- `docs/spec/**` untouched: zero `docs/spec/**` files in the diff (confirmed: only the six mirror files + `docs/releases/index.md`, `docs/de/releases/index.md`, `docs/development/pre-release-documentation-audit.md`, `docs/de/development/pre-release-readiness.md` — housekeeping, no Perses state definition).
- `git diff --check` clean.
- Scan `rg -n -i 'perses.*(unsupported|not supported)' docs` returns no unsupported/not-supported Perses state references in scope.

## CI witness

Exact-headed `pull_request` run 43704566914, head `ab9086f5`:

```json
{"conclusion":"success","databaseId":43704566914,"event":"pull_request","headSha":"ab9086f5fc39d34348c7a5db49525cd14566c52a","status":"completed","workflowName":"CI · Source & Quality"}
```

No rerun or workflow_dispatch initiated.

## Verdict

APPROVE #1577 at `ab9086f5fc39d34348c7a5db49525cd14566c52a`. All six agreed mirror spots reduced to factual mention + spec pointer under the 0428-092 owner scope; Perses pin/scope/state carry no normative verb; `docs/spec/**` untouched; no word-walk finding, no new class. CI success on exact head. No product code, workflow, CI, container or VM changed. PR #1577 NOT merged (frost honoured).

## repo-rule compliance

Evidence in the actual planning repository (verified before commit). Product remote state from a fresh clone and `git ls-remote`; the quarantined workers checkout was not used. No product code, `.github/**` files, CI, containers or VMs changed. No merge. No markdown checkbox lines.

## END mission-rev1577-final DONE — APPROVE #1577 at ab9086f5fc39d34348c7a5db49525cd14566c52a

## Planning validation

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed successfully. `git diff --check` passed. No Markdown checkbox lines.

Planning origin/main witness before push (`git ls-remote origin refs/heads/main`):

```text
5e91f65f518cfbd0da68c996c8069c7c8d9b8cd5	refs/heads/main
```
