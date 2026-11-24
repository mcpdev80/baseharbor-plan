# PR-SWEEP LEDGER — 2026-11-25

Lane: w83-0428-216-hv26numbers (pivot from H-V26 numbers desk to owner-priority PR-sweep ledger).
Type: READ-ONLY ledger. No writes to baseharbor, no rebase, no rerun, no workflow_dispatch, no merge, no subagents, no product/PR edits.
Base (develop) SHA witnessed: `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2` (`git ls-remote origin refs/heads/develop`).

## REALITY WITNESSES

- Planning repo remote (verified before first evidence action):
  `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`
  (NOT `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan` — that is a directory inside the workers bookkeeping repo; commits there never reach GitHub.)
- Product remote: `https://github.com/mcpdev80/baseharbor.git`
- Read-only blob-less clone under `/tmp/hv26-sweep-wt` (remote `origin https://github.com/mcpdev80/baseharbor.git`); merge-base / behind-count computed against `origin/develop`.
- All CI data from GitHub-hosted runs via `gh api` (no local product tests, no VM, no compose, no docker/podman).
- No `.github` file touched, no rerun/workflow_dispatch fired, no baseharbor push/rebase.

## PLAN

- Attest planning remote URL + fetch fresh develop, confirm planning pin is real.
- For each open PR (#1826, #1823, #1820, #1819, #1818, #1812, #1650): capture head SHA (ls-remote), merge-base vs develop, behind/ahead delta, commits on head.
- For each PR: fetch exact-head Hosted CI run id + terminal state + which required gate ran vs skipped.
- Determine draft state + single-writer lane + chain-eligibility (serial chain #1812 -> #1819 -> #1820; #1818 behind #1819/C).
- Write this ledger + commit+push atomically to baseharbor-plan.
- Verify path on origin/main; report inline + evidence SHA.

## LEDGER

### Base / develop

- develop HEAD: `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2` (git ls-remote origin, 2026-11-24).
- All seven PRs base `develop` (confirmed via gh API `base.ref`). None based on main or a non-develop ref.

### PR ledger table

| PR | Card | head SHA (ls-remote) | merge-base vs develop | behind develop | commits on head | draft | single-writer lane |
| --- | --- | --- | --- | --- | --- | --- | --- |
| #1826 | 0428-279 | `a4dffedb90fc92f3d7f6d15e2860cdb97c2f33a5` | `46d3dccc1f6f` (=develop tip) | 0 | 1 | no | 0428-279 (release docs, demo-ref re-pin) |
| #1823 | 0428-277 | `abec98ea38f6...` | — | — | — | no | 0428-277 (fail-closed AuthorizationResult reveal) |
| #1820 | 0428-271 | `28803d11027197e7734fb3ec94bef9b34e224b0d` | `05ef48536905` | 2 | 4 | no | 0428-271 (broker commit-identity probe) |
| #1819 | 0428-181 | `17381017be986f0eccb25662ad742ad759296346` | `05ef48536905` | 2 | 2 | no | 0428-181 (Perses identity dashboard export) |
| #1818 | 0428-078 | `20fc1cb7d49602dc7f8aa0004a7562a81311d78c` | `3ebfb90daaf4` | 4 | 4 | no | 0428-078 (Perses identity-keycloak eligibility) |
| #1812 | 0428-249 | `47590207518ce9501f1b1bbb115d72d64a206d14` | `46d3dccc1f6f` (=develop tip) | 0 | 1 | no | 0428-249 (reload runtime image before ORAS) |
| #1650 | 0428-078 | `84943695be19300ef006a7986e1d110130943ce8` | `d4fa8c589e02` | 9 | 18 | no | 0428-078 (Perses identity-keycloak resolver fan-in) — owner-parked |

Notes:
- #1823 head changed this window: the exact-head CI run captured here is for head `f072dcb58302` (run 45395054488, success). The PR's *current* head is `abec98ea38f6` (force-pushed after), which has its own in-progress CI run 45407605826 (status in_progress, no terminal state yet).
- #1826 head changed this window: current head `a4dffedb90fc` has CI run 45404417242 (success). An earlier head `080ea8300fd0` had run 45401380970 (success). Both terminal success.
- #1812 and #1826 share the develop tip as merge-base (0 behind) — both were rebased onto current develop in-window (w81 force-pushed 1812 to 475902075).

### Exact-head Hosted CI (GitHub-hosted, via gh api)

| PR | exact head | run id | run name | event | terminal state | required gate ran vs skipped |
| --- | --- | --- | --- | --- | --- | --- |
| #1826 | `a4dffedb90fc` | 45404417242 | CI · PR #1826 | pull_request | completed / success | Go unit (cli-0/1/2/3, owner, packages) success; go-vet/go-build success; **Native Keycloak/Core skipped** (no runtime gate triggered by docs-only change) |
| #1823 | `f072dcb58302` | 45395054488 | CI · PR #1823 | pull_request | completed / success | Go unit + go-vet/go-build + Runner Interface + Focused Python success; **Native Keycloak/Core skipped**; Demo Pin/Evidence success |
| #1823 | `abec98ea38f6` (current) | 45407605826 | CI · PR #1823 | pull_request | in_progress / no conclusion | NOT TERMINAL — still running at ledger time |
| #1820 | `28803d110271` | 45382404741 | CI · PR #1820 | pull_request | completed / **cancelled** | Go unit (cli-0/1/2/3, owner, packages), go-vet/go-build, Exact Candidate, Runner Interface, Demo Pin success; then **cancelled before runtime gate** — PR · Selected Runtime never completed (terminal conclusion cancelled) |
| #1819 | `17381017be98` | 45380314808 | CI · PR #1819 | pull_request | completed / **cancelled** | same shape: Go unit/validation success then cancelled before runtime gate completes |
| #1818 | `20fc1cb7d496` | 45316544436 | CI · PR #1818 | pull_request | completed / success | Go unit + go-vet/go-build + **identity-provider-package-tests success** + Exact Candidate; **Native Keycloak/Core skipped** (no native runtime gate for 0428-078 keycloak change) |
| #1812 | `47590207518c` | 45398943139 | Pre-Release · v0.4.27 | **workflow_dispatch** (owner) | completed / **failure** | Source/Go-vet/Go-tests/Qualified success; Candidate · Runtime Image success; **all runtime Light/Integration/HA/Static gates SKIPPED** (run cancelled before gates executed — matches w81 STATE). This is the owner-dispatched v0.4.27 run on the new head, not a PR-pushed CI run. |
| #1650 | `84943695be19` | 45297432220 | CI · PR #1650 | pull_request | completed / success | Go unit + go-vet/go-build + **identity-provider-package-tests success**; **Native Keycloak/Core skipped** |

### Chain gating

- **Serial chain #1812 -> #1819 -> #1820 (strict serial).**
  - #1812 (0428-249, head 475902075, 0 behind develop) is the base. Its exact-head owner dispatch (45398943139) ran Source + Qualified + Candidate · Runtime Image green but the runtime Light gates did not execute (all skipped) — so #1812 is NOT green on gates yet; a fresh owner dispatch on this head is required (owner scope).
  - #1819 (0428-181, 2 behind develop, merge-base 05ef4853) is gated on #1812 merge. Its exact-head CI run 45380314808 cancelled before the runtime gate.
  - #1820 (0428-271, 2 behind develop, merge-base 05ef4853) is gated on #1819 merge. Its exact-head CI run 45382404741 cancelled before the runtime gate.
  - All three carry stale bases relative to the merge-chain tip; advancing any one changes the higher PRs' tested heads. None can advance without disturbing the others' exact-head CI.
- **#1818 (0428-078) behind #1819/C.** #1818 (4 behind develop, merge-base 3ebfb90d) and #1650 (0428-078, 9 behind, merge-base d4fa8c58) both target card 0428-078; they overlap (same card, divergent heads). #1818's exact-head CI run 45316544436 was success but selected no native runtime gate. #1650 is owner-parked.
- **Stale bases:** #1823 (current head moved), #1820, #1819, #1818, #1650 all sit behind current develop (#1826 and #1812 are at the develop tip after in-window rebase).

## CLEANLINESS

- Read-only ledger. No containers/compose started. `docker ps -a` witness: n/a (none started on this host — this desk never starts a stack).
- Read-only clone under `/tmp/hv26-sweep-wt`; no worktree, no product-repo writes, no .github/scripts touched, no rerun/workflow_dispatch fired.
- No baseharbor push/rebase/merge. Evidence delivered atomically to baseharbor-plan only.

## STATUS

Done — read-only PR-sweep ledger. Evidence committed to baseharbor-plan origin/main; report inline + evidence SHA.
