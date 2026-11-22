# Fan-in plan for the closed unmerged leader PR #1726 (card 0428-198)

Measured on 2026-11-22 against develop `82825e95a6f6083702d0ba5401d97f356085c722`.

## Why #1726 is closed without a merge

- Hosted state: `state=CLOSED`, `mergedAt=null`, `mergeCommit=null`, closed `2026-11-21T09:09:20Z`, zero comments,
  head `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4`, branch `lane-0428-198-cli-shard-operator-env`, 29 changed files.
- Recorded reason (`evidence/r28-welle4-2026-11-21/cli-shard-operator-env/round-4.md`): "The test-only candidate PR
  #1726 was closed as superseded on 2026-11-21; the current base already carries the shared test fixture behaviour."
- That sentence is only half true and the board inherited the error: `git cherry` reports **all 11 own commits as not
  patch-equivalent** in develop, and develop contains **zero** occurrences of `testIsolatedSelectionContext` while PR
  #1750 head contains seven. The shared context therefore arrives with **#1750 (card 0428-223)**, not before. The
  design reason for superseding stands: #1726 stamped the operator fixture into ~26 individual test files plus
  `cmd/baha/main.go`, `cmd/baha/mcp.go`, `cmd/baha/app_init_wizard.go`, whereas #1750 provides one helper that the
  affected tests call. Overlap between the two file sets is exactly one file (`cmd/baha/app_init_wizard_test.go`).

## Board-truth correction

Card 0428-198 was `closed` with `resolution: accepted` while its only PR never merged. Corrected to
`resolution: superseded`, `superseded_by: t-20261121-develop-full-suite-red`, evidence pointing at this file. No
other card's state changed for this reason.

## Children: what is actually theirs

| PR | branch base | own commits above the dead leader | own files | applies onto develop as a patch |
| --- | --- | --- | --- | --- |
| #1737 | `lane-0428-198-...` @ `e45430f` | 2 | `cmd/baha/trust_uninstall_test.go` | no - context drift at line 57 |
| #1738 | same | 1 | `cmd/baha/core_installation_runtime_test.go` | yes |
| #1740 | same | 4 | `cmd/baha/control_plane_single_native_ci_test.go`, `cmd/baha/runtime_integration_test_support_test.go` | no - collision at line 818 of the support file, which is the file #1750 extends |
| #1741 | same | 2 | `cmd/baha/mcp_operator_seam_test.go` | yes |

A direct additive hop of any child onto develop hits 19-20 conflicted files, because the base brings the whole 26-file
stamping set with it. Their own contribution is one or two test files.

## Route (replacement base integration)

1. Land the leader content once, as #1750/card 0428-223. This is the shared operator-context mechanism the family
   needs; #1726 is not re-opened and its branch is not reused.
2. For each child card, a lane branches from current develop (after step 1), cherry-picks that child's own commits,
   and resolves only the drift inside its one or two files. Cards carrying them: 0428-213 (#1737), the 0428-217/204
   line (#1738), 0428-209 (#1740), 0428-218 (#1741). #1740 must be sequenced last of the four, because it edits the
   same support file #1750 introduces the helper into.
3. Each re-routed card publishes its own PR against develop, gets its own exact-head hosted CI and an independent
   verdict, and merges on its own merits - one PR per card.
4. The four stale stacked PRs are then closed by the Owner or CODEX-MERGE with a pointer to their replacements; a lane
   closes nothing.
5. Until step 1 is merged, all four wait cards keep the named dependency, so nobody rediscovers the 19-20 conflicts.
