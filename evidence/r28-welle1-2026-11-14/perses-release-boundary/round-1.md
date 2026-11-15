# PR #1577 Release/Reference R1 (0428-077: Perses release/reference three-state alignment)

## PLAN

1. Read r7 akte (act-1575-review-r7.md) and the owner tasking: align #1577 English and German release/reference prose to the same three Perses state names as the #1575 spec.
2. Verify #1577 is a separate draft (own commit history, not the #1575 seam); open own PR on base develop.
3. Fix the four affected files: EN release `docs/releases/v0.4.28.md:15`, DE release `docs/de/releases/v0.4.28.md:13`, EN reference `docs/reference/releases.md:31`, DE reference `docs/de/reference/releases.md:30`.
4. Exact-headed pull_request run terminal; round-1.md; push; END. No merge (frost).

## Provenance

Fresh clone at `/tmp/opencode/mission-1575-r4`. Exact product witness from `git ls-remote origin`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
29dba54dddb02f48568c571e9ce37f671d21e6aa	refs/pull/1577/head
```

Own branch head (ls-remote witness):

```text
ls-remote origin refs/heads/mission-1577-077 -> e51911a5
ls-remote origin refs/pull/1583/head          -> e51911a5 (current)
```

Own candidate chain on develop (doc-only r1):

```text
e51911a5 docs(0428-077): align EN+DE release/reference to Perses three-state names (not_configured/configured_unverified)
29dba54dddb02f48568c571e9ce37f671d21e6aa (base: existing #1577 head)
```

`git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c e51911a5` succeeded. PR #1583 is OPEN/DRAFT, base `develop`, branch `mission-1577-077`.

## What was wrong

The four flagged files used `unsupported` for the selected-but-unprovisioned Perses case and never stated the three machine-readable states. That conflicts with the #1575 seam's `configured_unverified` result for selected + valid pin + no health observation and with the three-state vocabulary in `docs/spec/management-access-v1.md`.

## Fix

All four files now use the same three-state names and meanings as the #1575 spec:

- `not_configured`: no working Perses selection — unselected, or declared with an invalid or unavailable pin. Fail-closed, never "configured"/"verified".
- `configured_unverified`: selected with a valid pin but no Perses health probe; reachability stays unverified. Only reachable state for a selected surface.
- `verified`: only when a real Perses health probe observes the surface.

Changed lines:

- `docs/releases/v0.4.28.md:15` (EN release)
- `docs/de/releases/v0.4.28.md:13` (DE release)
- `docs/reference/releases.md:31` (EN reference)
- `docs/de/reference/releases.md:30` (DE reference)

No `unsupported` remains in any Perses context. `git diff --check` clean.

## Hosted run

Exact headed pull_request run:

```
0428-077  run 43671069449  success  e51911a5  pull_request  CI · Source & Quality
```

No rerun or workflow dispatch was initiated. No failing or cancelled check observed. The ambient serial-runtime integration gate (Q-RUNTIME) was not assessed.

## repo-rule compliance

Evidence is in the actual planning repository. Product remote state was measured from a fresh clone and `git ls-remote`. No product code, PRs, workflows, CI, containers, or VMs were changed beyond the doc-only candidate branch. PR #1577's original draft was not merged (frost honoured); this is a separate draft (PR #1583). No markdown checkbox lines in evidence.

## END DONE (0428-077)
