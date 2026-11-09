---
id: t-20261108-bughunt-rawmode-prompt-sigint
card_number: "0427-145"
card_short_title: "Ctrl-C breaks raw prompt"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: SIGINT at a raw prompt = clean cancel with message and restored terminal; signal regression in the existing field.
kanban_title: 0427-145 · Ctrl-C breaks raw prompt
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1472]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/42481779497", "https://github.com/mcpdev80/baseharbor/commit/4786c541743541e7550f2c214f143ac8ee4f0aa6"]
---
- [x] t-20261108-bughunt-rawmode-prompt-sigint · Bug Hunt v0.4.27: Ctrl-C breaks raw prompt #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1472](https://github.com/mcpdev80/baseharbor/pull/1472)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42481779497), [proof 3](https://github.com/mcpdev80/baseharbor/commit/4786c541743541e7550f2c214f143ac8ee4f0aa6)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1472](https://github.com/mcpdev80/baseharbor/pull/1472)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
SIGINT at a raw prompt = clean cancel with message and restored terminal; signal regression in the existing field.

## Problem (source evidence in the dossier)
At the Project location prompt the path input runs in raw mode (path_prompt_linux.go, ICANON/ECHO/ISIG off): Ctrl-C ends without an Interrupted line and the terminal stays raw until process exit. Source: hunt H-P1 BF-10.

## Acceptance
SIGINT at a raw prompt = clean cancel with message and restored terminal; signal regression in the existing field.

## Dependencies and file ownership
None. Write-set: cmd/baha path prompt raw mode.

## Audit note (Karten-Audit 2026-11-08)
Audit 2026-11-08 (zuerklaeren): the missing Interrupted line was observed non-deterministically; the deterministic part (terminal restore) is what acceptance must pin. [Dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/karten-audit-2026-11-08.md)


## PR and owner — 2026-11-08

- Claimed by `chatgpt-r27-path-signal` for [PR #1472](https://github.com/mcpdev80/baseharbor/pull/1472). Raw path Ctrl-C displays a clean cancellation and retains `context.Canceled`; real PTY regression verifies ISIG-off entry, Ctrl-C and restoration of the terminal local flags.
- Exact-head CI and signal regression pending. Do not close or claim user-host proof before terminal PASS.


## Accepted — 2026-11-08

- [PR #1472](https://github.com/mcpdev80/baseharbor/pull/1472), exact head `36ce785320e71ac1ad3169c24aa67ab3d47d1d00`, merged to develop as `4786c541743541e7550f2c214f143ac8ee4f0aa6`.
- [CI #42481779497](https://github.com/mcpdev80/baseharbor/actions/runs/42481779497): terminal SUCCESS including targeted Linux PTY regression, Go-unit, build/vet, native Docker/Podman destroy retry and selected checks.
- `path_prompt_linux.go` now reports `Interrupted. No changes were made.` on raw Ctrl-C and returns `context.Canceled`; real PTY test verifies input signal and restored termios local flags. All card acceptance criteria covered. `resolution: accepted`, worker claim released.
