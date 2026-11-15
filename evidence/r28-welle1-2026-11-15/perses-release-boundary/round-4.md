# PR #1577 Release/Reference R4 (0428-077: spec-copy verified + unavailable-pin coverage)

## PLAN

1. Read r4 akte (act-1577-review-r4.md): REJECT — two doc findings on the r3 head `2c4ccc31`.
2. Finding 1: the `not_configured` branch in both how-to passages omits the unavailable-pin case — add it, matching the approved spec (unselected OR invalid/unavailable pin, fail-closed).
3. Finding 2: the four release/reference passages mention `verified` without stating the condition "only after a real health-path probe". Strategy change from r3: do not re-paraphrase; copy the approved spec's verified-sentence verbatim into each affected passage.
4. Card branch `0428-092-perses-boundary`, PR #1577 draft, pull_request run on exact head terminal, round-4.md, END. No merge (frost).

## Candidate and provenance

PR #1577 is OPEN and DRAFT, base `develop`, branch `0428-092-perses-boundary`, exact head `fe6c795cea2e94f1c2772f3b9737e231d244ff1d`. Product `git ls-remote` witness:

```text
fe6c795cea2e94f1c2772f3b9737e231d244ff1d	refs/heads/0428-092-perses-boundary
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
fe6c795cea2e94f1c2772f3b9737e231d244ff1d	refs/pull/1577/head
af308e66d38ad1204345bbe83d066dd7548ea6e6	refs/pull/1575/head
```

The r3 head `2c4ccc31` is a direct ancestor: `git rev-list --count 2c4ccc31..fe6c795c` is `1` (fast-forward), and `0e9ccb58` is an ancestor of `fe6c795c`. Fresh review clone `/tmp/opencode/w077-pr1577-review-r3-wt`; the pre-existing review worktree was not used for this edit.

## Approved spec source (copied verbatim)

`docs/spec/management-access-v1.md:51-64`, exact head `af308e66`, the three-state block. The verified sentence copied verbatim into each release/reference passage:

> `verified` — only when a real Perses health probe observes the surface. Pin validation alone MUST NOT emit this state.

## What r4 required and how it is satisfied

### Finding 1 — how-to `not_configured` now includes unavailable pin (both languages)

- `docs/how-to/observability.md:32`: "when Perses is not selected, **or is declared with an invalid or unavailable pin**, that is the normal state ... `not_configured` (fail-closed)."
- `docs/de/how-to/observability.md:28`: "Wenn Perses nicht gewählt ist **oder mit einer ungültigen oder nicht verfügbaren Pin deklariert ist**, ist das der Normalzustand ... `not_configured` (fail-closed)."

Matches the spec's `not_configured` definition exactly.

### Finding 2 — verified defined identically in all four release/reference passages

The approved spec's verified sentence was inserted verbatim into each passage, so every `verified` occurrence in a Perses context now carries the health-path clause in the same passage:

- `docs/releases/v0.4.28.md:15` (EN release)
- `docs/de/releases/v0.4.28.md:13` (DE release)
- `docs/reference/releases.md:31` (EN reference)
- `docs/de/reference/releases.md:30` (DE reference)

The weaker "no release reports Perses as verified when Perses is not provisioned" phrasing (which could imply a false positive tied to provisioning) is removed from the EN release in favour of the spec's exact condition. The DE release was corrected of a typo ("Normalzustund" -> "Normalzustand") during this edit.

## Grep witness

- `rg -n -i 'perses.*(unsupported|not supported)|(unsupported|not supported).*perses' docs` -> **no matches**. The obsolete `unsupported` Perses state is gone.
- Every `verified` occurrence in a Perses-context file (release, reference, how-to, both languages) contains the health-path clause "only when a real Perses health probe observes the surface" / German equivalent in the same passage.

## Hosted run

Exact headed pull_request run on the corrected card head:

```
0428-077  run 43677962027  success  fe6c795c  pull_request  CI · Source & Quality  (PR #1577)
```

No workflow dispatch was needed — the branch push ignited the run. No rerun or dispatch was initiated. No failing or cancelled check observed. The ambient serial-runtime integration gate (Q-RUNTIME) was not assessed, per mission scope.

## repo-rule compliance

Evidence is in the actual planning repository. Product remote state was measured from a fresh clone and `git ls-remote`. No product code, workflows, CI, containers, or VMs were changed beyond the six doc files on the card branch. `git diff --check` passes. PR #1577 was NOT merged (frost honoured). Both candidate heads sit exactly on `fe6c795c`. No markdown checkbox lines in evidence.

## END DONE (0428-077)
