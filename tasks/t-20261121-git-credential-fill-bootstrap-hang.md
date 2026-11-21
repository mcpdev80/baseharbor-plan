---
id: t-20261121-git-credential-fill-bootstrap-hang
card_number: "0428-217"
card_short_title: "0428-217 credential-fill hang"
title: "0428-217 · CLI: first target create hangs on git credential fill against example.invalid"
type: bug
areas: [cli]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: active
kanban_lane: active
kanban_summary: "The first authenticated Git operation inside a test or a first-time target bootstrap never returns a clean failure: it invokes…"
kanban_title: 0428-217 · 0428-217 credential-fill hang
priority: high
depends_on: []
blocked_by: []
prs: []
wait_reason: ""
blocker: ""

---

- [ ] t-20261121-git-credential-fill-bootstrap-hang · 0428-217 git credential fill must not block in test or first-run paths #task #release/v0-4-28 #status/active #view/active #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** coordinator  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

The first authenticated Git operation inside a test or a first-time target bootstrap never returns a clean failure: it
invokes `git credential fill`, which blocks on a prompt (or on a helper that has no terminal) and the caller reports a
timeout/OOM-shaped failure instead of "no credential for this host". Fix the call path so credential lookup is
non-interactive by construction in test and bootstrap contexts, and the failure names the missing credential.

## Why

Found while reproducing 0428-206. Two independent witnesses, same class:

1. CODEX's own exact-base reproduction at develop `40cb28c758b0` recorded: *"Initial invocation without prompt suppression
   stalled at a test's `git credential fill` against `https://example.invalid` and was interrupted; the second run needed
   `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/bin/true SSH_ASKPASS=/bin/true`."*
   (`evidence/r28-welle4-2026-11-21/other-domain-test-split/codex-review-r2.md`, plan `8a086890`)
2. Lane `0428-206-testsplit-recount` traced the call path to file:line in its round-2 akte
   (`evidence/r28-welle4-2026-11-21/other-domain-test-split/round-2.md`, plan `6391293a`):
   `cmd/baha/app_inspect_remote.go:28` → `internal/.../host.go:135` → `internal/.../gitcredential.go:49` / `:68`.

The Owner recorded the same class independently on card `t-20261114-r28-cli2-identity-secrets` (0428-078 note): a runtime
fails at the first `baha target create` even after the Demo selector-order fix. This card exists so the finding is not
trapped in an akte (Fund→Karte duty, Owner directive 2026-11-08).

## Scope

Allowed write-set (to be confirmed by the implementing lane before the first edit — the two `gitcredential`/`host` files
must be reported here if they are not under `cmd/baha/`):

- `cmd/baha/app_inspect_remote.go`
- the Git host/credential helper files reached from it (`host.go`, `gitcredential.go`), **excluding** any path under
  `internal/operatorauth/**`, `internal/identityprovider/**`, `internal/serviceaccess/**` (Owner rails).

Forbidden: `.github/**` (Owner scope — if a workflow env var is needed, report the line to the Coordinator), the Owner
stack `#1615`/`#1625`/`#1623` (branch `cli2-identity-secrets-head`), `#1650`/`#1606`, `#1614`, `#1731`, `#1704`,
`internal/observability/registry.go`, `internal/capability/perses_selection.go`.

## Acceptance criteria

1. With **no** prompt suppression in the environment (`GIT_TERMINAL_PROMPT` unset, no `GIT_ASKPASS`), the code path either
   (a) never calls `git credential fill` in test/bootstrap contexts, or (b) fails with a message that names the host and
   the missing credential. Blocking on a prompt is not an acceptable outcome in any CI or first-run context.
2. A regression test proves the failure content, not just `err != nil`, and proves the asserted branch is reachable from
   the production call path (honesty rubric, 2026-11-21).
3. The existing hosted cells that currently need `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/bin/true SSH_ASKPASS=/bin/true` as a
   workaround keep passing; the workaround is documented as no longer required in the akte, and any place that still
   requires it is named with file:line.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | Go unit shards for `./cmd/baha/` (PR Selected Checks) |
| Evidence | `baseharbor-plan/evidence/r28-welle4-2026-11-21/git-credential-fill-bootstrap-hang/round-1.md` |

## Notes

- Derived from a diagnosis card, not from a hunt matrix slice; the two witnesses above are the full provenance.
- This card is currently **read-only for the queue**: it is not commissioned until 0428-204 (`#1726`) or `#1615` is merged,
  because both touch the CLI Git paths. Commissioning is a Coordinator action with a stated reason.

Lane '0428-217-credfill' auf laptop:2 begonnen; write-set BESTAETIGUNG ist schritt 1 der mission (die karte erlaubt verschiebungen ausserhalb der zwei dateien, meldung an mich vor dem ersten write ausserhalb von cmd/baha/). Kein besetzter pfad: app_commands.go haelt 0428-210/#1739, mcp.go + MCP-tests haelt 0428-218/#-neu.
