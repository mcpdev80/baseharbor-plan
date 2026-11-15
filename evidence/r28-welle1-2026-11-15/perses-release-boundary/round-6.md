# PR #1577 Release/Reference R6 (0428-092: Perses state prose reduced to mention + spec pointer)

ROLE: CODEX (docs-only, no merge). Card 0428-092, PR #1577, branch `0428-092-perses-boundary`.

## Work plan

1. Read mission `/tmp/opencode/mission-092-pointer.md` + corrected owner scope (0428-092, plan-head e1dd0508).
2. Identify every affected Perses place in the prose/release/reference/how-to files (EN+DE); classify auth/role mirror vs Perses pin/scope/state.
3. Replace each normative Perses state sentence with a one-sentence factual mention of the three state names + a pointer to docs/spec/management-access-v1.md; keep Perses pin/scope as factual release summaries, no normative verb; pointer path stays English; leave docs/spec/** untouched.
4. diff-check, push new head, watch pull_request run to terminal, write round-6.md with before/after table, publish evidence to origin/main, END. No merge (frost).

## Candidate and provenance

PR #1577 is OPEN and DRAFT, base `develop`, branch `0428-092-perses-boundary`, exact head `ab9086f5fc39d34348c7a5db49525cd14566c52a`. Product `git ls-remote` witness:

```text
ab9086f5fc39d34348c7a5db49525cd14566c52a	refs/heads/0428-092-perses-boundary
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
ab9086f5fc39d34348c7a5db49525cd14566c52a	refs/pull/1577/head
af308e66d38ad1204345bbe83d066dd7548ea6e6	refs/pull/1575/head
```

The r4 head `fe6c795c` is a direct ancestor: `git rev-list --count fe6c795c..ab9086f5` is `1` (fast-forward); `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` is an ancestor of the candidate. Fresh review clone `/tmp/opencode/w077-pr1577-review-r3-wt`; the pre-existing review worktree was not used for this edit. The branch was cut from `develop` head `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`, an ancestor of the first commit.

## Scope decisions (owner 0428-092, plan-head e1dd0508)

- The pointer to `docs/spec/management-access-v1.md` is used ONLY as the normative anchor for places that mirror normative state semantics.
- Perses PIN, RELEASE SCOPE and STATE SEMANTICS (not_configured / configured_unverified / verified) are NOT derived normatively from the spec; these places stay short factual release summaries and carry the pointer only as a "definition lives in spec" note, NOT as a normative claim.
- The three states are mentioned, never defined, in the prose/release/reference/how-to files.
- No change to `docs/spec/**` (seam #1575 ownership).

Classification: the auth/role-mirror prose exists only in `docs/spec/**` (the seam #1575 files, out of scope for this card). The prose/release/reference/how-to files touched here carry only Perses pin/scope/state content; each was reduced to a factual mention + spec pointer.

## Before / after of replaced mirror places (file:line alt -> pointer)

All edits EN+DE; pointer path `docs/spec/management-access-v1.md` stays English.

| File (EN/DE) | line | before (normative state sentence) | after (mention + pointer) |
| --- | --- | --- | --- |
| docs/releases/v0.4.28.md (EN) | 15 | multi-sentence definition of not_configured/configured_unverified/verified with "MUST NOT" language | single sentence: status may read the three names depending on selected/pinned/reachable; normative definition lives in docs/spec/management-access-v1.md |
| docs/de/releases/v0.4.28.md (DE) | 13 | equivalent normative definition (de) | equivalent mention + pointer (de) |
| docs/reference/releases.md (EN) | 31 | multi-sentence definition embedded in the reference paragraph | single factual mention + pointer, surrounding scope sentence preserved |
| docs/de/reference/releases.md (DE) | 30 | equivalent normative definition (de) | equivalent mention + pointer (de) |
| docs/how-to/observability.md (EN) | 32 | procedural definition of the three states + health-path condition | factual status mention + spec pointer |
| docs/de/how-to/observability.md (DE) | 28 | equivalent procedural definition (de) | equivalent factual mention + spec pointer (de) |

## Verification

`git diff --check` clean; `git diff --stat` shows only the six files. The pointer path `docs/spec/management-access-v1.md` appears in all six edited files and stays English in both languages. No state sentence with normative "MUST" language remains in the prose; the three names appear only as mentions followed by the pointer. `docs/spec/**` untouched.

## Hosted run

Exact headed pull_request run on the corrected card head:

```
0428-092  run 43704566914  success  ab9086f5  pull_request  CI · Source & Quality  (PR #1577)
```

No workflow dispatch was needed — the branch push ignited the run. No rerun or dispatch was initiated. No failing or cancelled check observed. The ambient serial-runtime integration gate (Q-RUNTIME) was not assessed, per mission scope. No `.github/**` file was edited; runners are GitHub-hosted shared runners only.

## repo-rule compliance

Evidence is in the actual planning repository (verified before commit). Product remote state measured from a fresh clone and `git ls-remote`; the quarantined workers checkout was not used. No product code, workflows, CI, containers, or VMs were changed beyond the six doc files on the card branch. PR #1577 was NOT merged (frost honoured). Both candidate heads sit exactly on `ab9086f5`. No markdown checkbox lines in this evidence file.

## END DONE (0428-092)
