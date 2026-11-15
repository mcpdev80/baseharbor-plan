# PR #1575 Review R8 (r7 correction: Perses spec text aligned to three-state contract)

## PLAN

1. Read r7 akte (act-1575-review-r7.md, plan main 405d8f11): r7 code/test findings accepted as fixed; one documentation blocker remains — the #1575 spec's selected-but-unprovisioned sentence contradicts its own three-state definition and actual code; live #1577 EN/DE release/reference prose still uses `unsupported` instead of the three states.
2. Fix the #1575 spec text (docs/spec/management-access-v1.md): define `not_configured` as unselected OR invalid/unavailable pin (fail-closed), and selected + valid pin + no health evidence as `configured_unverified`, consistent with code and the `verified` definition.
3. Part-2 (owner tasking): correct #1577 EN/DE release/reference prose to the same three state names — separate draft, own lane, own PR.
4. Local build/vet; exact-headed pull_request run terminal; round-8.md; push both candidate branches; END for BOTH cards (0428-075 and 0428-077 separately). No merge (frost).

## Provenance

Fresh clone at `/tmp/opencode/mission-1575-r4`. Exact product witness from `git ls-remote origin refs/heads/develop refs/pull/1575/head refs/.../head`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
a5a5abedc3f9b5f72a2ff3819ed847293869eea9	refs/pull/1575/head
```

#1575 candidate chain on develop (doc-only r8):

```text
af308e66 docs(0428-075): align Perses not_configured/configured_unverified with three-state contract (r8)
a5a5abedc3f9b5f72a2ff3819ed847293869eea9 fix(0428-075): set Perses field before remote-target early return (r7)
28492bd12419f2c2e02048e07bfb92d09bb9735f fmt(0428-075): gofmt perses.go constants
181872c90a6e87b853e83198fbe87f198119ae23 fix(0428-075): expose Perses three-state contract in public status JSON (r5)
792c921cbcdb87158aa9abfbd28e2f266a44af5a ci(0428-075): re-trigger hosted CI for exact head c195a9a (r4)
c195a9a2049253accdf57a082e6eb33fc36ec7dd test(0428-075): execute the genuine baha status path for the Perses seam + unknown-owner fail-closed (r3)
dc670bfd4d32baf29afde0e4b021bfdb63f4e0be fix(0428-075): ground Perses seam in manifest truth, fail-closed + unverified reachability
61f76fa18897d4a0709c09c27ae67e1ded8dba20 feat(0428-075): define optional Perses provider seam (fail-closed)
```

`git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c af308e66` succeeded. PR #1575 stays OPEN/DRAFT, base `develop`, branch `lane-0428-075-perses-seam`.

## Part-1: #1575 spec text — fixed

The r7 blocker was an internal contradiction in `docs/spec/management-access-v1.md`. The r7-corrected bullet at `:41-44` said a selected-but-unprovisioned surface reports `not_configured`, while the three-state definition at `:55-62` defined `not_configured` as "no Perses selection" and `configured_unverified` as "selected + valid pin + no health probe". The code's `PersesStatusNow` (`internal/capability/perses.go`) maps selected + valid pin + no health observation to `configured_unverified`, so the bullet wrongly conflated the selected case with the fail-closed default.

R8 aligns the bullet and the state definitions:

- `not_configured`: the manifest does not select a working Perses surface — either no `perses` selection at all, or a selection with an invalid or unavailable pin. Fail-closed default, never "configured".
- `configured_unverified`: the surface is selected and its pinned release validated against the compiled default pin, but this Core defines the seam only and ships no Perses health probe, so reachability stays unverified. The only reachable state for a selected surface.
- `verified`: only when a real Perses health probe observes the surface.

The three states now match each other and the code. Build clean (`go build ./...` exit 0). The #1575 branch head is `af308e66`, a doc-only change on top of the r7 candidate — no code/test modification.

## Part-2: #1577 release/reference prose — fixed (own lane)

The r7 akte noted live #1577 English and German release/reference prose (EN release `docs/releases/v0.4.28.md:15`, DE release `docs/de/releases/v0.4.28.md:13`, EN reference `docs/reference/releases.md:31`, DE reference `docs/de/reference/releases.md:30`) still used `unsupported` for the selected-but-unprovisioned case and never stated the three states.

#1577 belongs to a separate draft (its own commit history, not the #1575 seam), so this is owner-tasked work in a dedicated lane, not a follow-up edit inside #1575. Own PR #1583, base `develop`, head `mission-1577-077`, exact head `e51911a5`. All four files were changed to the same three-state vocabulary and meanings as the #1575 spec: `not_configured` (fail-closed, unselected or invalid/unavailable pin) and `configured_unverified` (selected + valid pin + no health probe), with `verified` reserved for a real health-path observation. No `unsupported` remains in any Perses context. `git diff --check` clean.

## Hosted runs

Exact headed pull_request runs, all terminal success:

```
0428-075  run 43670440466  success  a5a5abedc  pull_request  CI · Source & Quality
0428-077  run 43671069449  success  e51911a    pull_request  CI · Source & Quality
```

No rerun or workflow dispatch was initiated. No failing or cancelled check observed on either. The ambient serial-runtime integration gate (Q-RUNTIME) was not assessed, per mission scope. No PR update or merge is authorized by this review.

## Local verification

Go toolchain from go.mod. On the exact candidate working copies:

```text
go build ./...   -> exit 0 (0428-075 af308e66; 0428-077 e51911a5)
```

Doc-only edits; no product test changes. No markdown checkbox lines in evidence.

## repo-rule compliance

Evidence is in the actual planning repository. Product remote state was measured from a fresh clone and `git ls-remote`. No product code, PRs, workflows, CI, containers, or VMs were changed or started beyond the two doc-only candidate branches. The #1575 candidate was not merged (frost honoured). The #1577 correction is a separate draft (PR #1583, own lane, not edited inside #1575). Both candidate branches sit exactly on their exact heads.

## END DONE (0428-075)
