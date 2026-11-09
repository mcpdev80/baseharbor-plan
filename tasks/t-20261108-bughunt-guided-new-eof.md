---
id: t-20261108-bughunt-guided-new-eof
card_number: "0427-170"
card_short_title: "New subwizard EOF cancel"
type: bug
areas: [cli, lifecycle]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: "0427-170 · New subwizard EOF cancel"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1496]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: [https://github.com/mcpdev80/baseharbor/pull/1496, https://github.com/mcpdev80/baseharbor/actions/runs/42513832507]
---
- [x] t-20261108-bughunt-guided-new-eof · Target/provider guided EOF cancellation #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/cli #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1496](https://github.com/mcpdev80/baseharbor/pull/1496)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1496), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42513832507)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1496](https://github.com/mcpdev80/baseharbor/pull/1496)  
**Source:** 
<!-- /generated:links -->

## Reproduction from develop (2026-11-08)

- Production `cmd/baha/human_new.go` has guided paths `runGuidedNewLocalTarget` and `guidedCreateProvider`.
- Both call `bufio.Reader.ReadString('\n')` directly and return raw `read ...: EOF` for Ctrl-D or unterminated partial input, including a partially entered `y` at final consent.
- The outer `baha new` chooser already treats EOF as cancellation; child guided target/provider paths do not. This is an independent UX/consent regression, not part of the accepted `app new` wizard EOF card 0427-138.
- Scope is limited to these two guided child prompts. Existing explicit headless target/provider creation semantics stay unchanged; no remote/Core runtime changes.

## Acceptance

- Empty and partial EOF at each target/provider question and confirmation abort cleanly (not a raw CLI error).
- Unterminated `y` cannot authorize creation; no target configuration or provider skeleton is written.
- Non-EOF I/O errors continue to propagate; fully terminated explicit yes still uses the unchanged creation path.
- Actual normal `cmd/baha` CI executes the new tests, plus source formatting, build/vet, final selected checks.
- Existing CLI application and Remote-Core worker paths remain unmodified.

## Implementation 2026-11-08

- [PR #1496](https://github.com/mcpdev80/baseharbor/pull/1496) on `fix/0427-170-guided-new-eof`, head `bb3c05d70fc73fc00c687898abb10377d08fe9fe`.
- `human_new.go`: preserve unchanged interactive/headless guard but delegate to tested reader-injected guided target/provider handlers. At every prompt, including confirmation, `io.EOF` cancels with no mutation. Other read errors continue to propagate.
- `human_new_eof_test.go`: 8 target EOF/partial scenarios, 4 provider EOF/partial scenarios; asserts clean cancellation and no target config or provider files.
- Await exact-head selected CI and final gate before accepting or closing.

## Accepted and merged — 2026-11-08

- [PR #1496](https://github.com/mcpdev80/baseharbor/pull/1496) squash-merged to `develop` at **`fc9ed173ddf5e3d52c5468ced7b86423daabb58a`** from exact head `bb3c05d70fc73fc00c687898abb10377d08fe9fe`.
- [Required CI #42513832507](https://github.com/mcpdev80/baseharbor/actions/runs/42513832507) terminal **SUCCESS**: real full `go-unit-tests` (`cmd/baha` included, 574.281s), Source format, gofmt, go-build, go-vet, Workflow policy, native Docker and Podman destroy-retry, and final `PR Selected Checks` all passed. Required jobs did not skip.
- Result: interactive target/provider child wizards return clean cancellation for an empty or unterminated EOF at every tested prompt. A partial `y` at final consent cannot mutate configuration or write a provider skeleton. Explicit non-interactive commands, remote Core, provider registration, CI workflows and security policy remain unchanged.
- Status **closed**, resolution `accepted`, no active owner; no additional release action.
