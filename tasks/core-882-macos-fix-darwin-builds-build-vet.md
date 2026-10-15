---
id: core-882
type: bug
release: v0.4.29
version: ""
parent: core-818
owner: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#882"]
source_updated: "2026-10-15T16:49:30Z"
labels: [kind/bug, area/runtime, area/evidence, area/compatibility]
early: true
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-882 · macOS: fix Darwin builds and verify build/vet #task #release/v0-4-29 #status/planned #view/ready
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.29](../releases/v0.4.29.md)  
**Parent:** [core-818](../epics/core-818-host-platforms.md)  
**Depends on:** none  
**Required by:** [core-819](core-819-architecture-host-interface-guard.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#882](https://github.com/mcpdev80/baseharbor/issues/882)
<!-- /generated:links -->

## Goal

`cmd/baha` compiles for `GOOS=darwin` (arm64 and amd64) and CI keeps it that way. Pulled ahead of v0.4.29; targets `develop` (the agreed develop prerequisite exception in #155).

## Scope

- Problem: `cmd/baha/app_backup_restore_guided.go` has no build constraint but uses Linux-only `golang.org/x/sys/unix` symbols: `unix.MemfdCreate`/`unix.MFD_CLOEXEC` (in-memory backup password file, `:572`), `unix.TCGETS`/`unix.TCSETS`, and passes `/proc/self/fd/<fd>` (`:591`) to the in-process password-file reader. `.github/workflows/ci.yml` builds and tests on Linux only.
- Split the platform mechanics by build constraint, guided backup/restore semantics unchanged:
  - **Linux:** existing `memfd` + `/proc/self/fd/<fd>` and `TCGETS`/`TCSETS`, byte-for-byte equivalent.
  - **Darwin — Variant A (confirmed by the project owner 2026-10-15):** private, operation-scoped in-memory secret source. The guided wrapper calls `baseRun` in the same process (no backup child); pass private secret authority directly to that operation, preserve repeated reads and existing password validation; no generated disk password file; platform-correct terminal control (e.g. `TIOCGETA`/`TIOCSETA`). Public `--password-file` stays a real owner-only regular file; do not weaken its checks to accept pipes or external handles.
  - The secret never enters logs, errors, argv or the environment on either platform.
- Add a cheap non-runtime gate to the existing `ci.yml` (no new workflow, so `scripts/ci-workflow-policy.sh` stays unchanged): `GOOS=darwin GOARCH=arm64|amd64 go build ./...` and `go vet ./...`.
- Keep Linux unit tests; qualify the actual Darwin in-process handoff in the native Darwin lane (core-823). Move portable helpers such as `shellDisplayPath` to common source.
- Out of scope: Darwin release artifacts, installer, self-update (core-822); any support-level change (compiling ≠ SUPPORTED/TESTED/PORTABILITY-VERIFIED).

## Acceptance

- `GOOS=darwin` build and vet pass for arm64 and amd64 in `ci.yml` on every PR.
- Linux guided backup/restore behavior and tests unchanged.
- Darwin password handoff writes no secret file and leaks no secret.
- Source size limits and `gofmt` pass.
- Guided backup/restore supports repeated authorized reads of the same validated in-memory bytes.
- No plaintext secret in argv, environment, logs, errors, machine output or generated disk password files.
- The private handle/reader is bound to the current operation, not a public token protocol or global secret registry; externally supplied, forged, stale, replayed or cross-operation identifiers cannot activate it.
- Public user-provided password files keep their regular-file, permission, size and validation checks.
- Success, validation/apply failure and cancellation revoke/remove the handle and zero owned secret buffers; repeated/concurrent operations neither retain nor exchange secrets.
- Terminal state is restored on completion/failure/cancellation; cleanup preserves the original error.
- Native Darwin backup/restore and race/isolation regressions qualify the adapter; encryption, consent and restore-before-mutation validation stay intact.
- No generated disk-backed temporary-password fallback. (The earlier child-process criteria were based on an incorrect assumption and are replaced: `readBackupPasswordFile` uses `os.Stat`/`os.ReadFile` on a regular owner-only file; the native macOS descriptor measurement shares the read offset and returns empty on a second read — keep its reproduction in evidence.)

## Required checks

- Darwin cross build/vet for both architectures; Linux unit tests; native Darwin lane for the handoff.

## Dependencies and file ownership

- No task dependencies. Owns `cmd/baha/app_backup_restore_guided*.go` platform split and the darwin step in `ci.yml` (coordinate the `ci.yml` edit with the core-893 owner, who owns that file in v0.4.26).

## Handoff

- Not started.

The 2026-10-10 "two sessions" release assignment and the shared release PR of the source are superseded by the task-PR model ([decision](../decisions/2026-10-15-task-prs-supersede-shared-release-prs.md)); the platform scope itself is current per [v0.4.29](../releases/v0.4.29.md).
