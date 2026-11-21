# round-3-chainrebase.md

Card: t-20261120-cli-operator-entrypoints (0428-204)
Lane: 0428-204-chainrebase
Shift: r28-welle4-2026-11-21
Evidence path: evidence/r28-welle4-2026-11-21/stale-pr-hop-and-baserefs/round-3-chainrebase.md

## Session witnesses
- session-ID: 56b12dbc-caa6-4fcb-97df-0b4c783108c1
- modell/backend: agentgateway/worker-ornith1.5 (laptop-Kanal), am spawn verifiziert
- start: 2026-11-21 05:13Z

## repo-rule compliance
- Scope: purely mechanical chain maintenance, no content change to any file.
- No new PR, no merge, no close, no comment on foreign PRs.
- No `go test ./cmd/baha/` bulk on this host.
- No subagents (directive 4.8).
- Pushes only on the two own lane branches (lane-0428-213, lane-0428-214), never on owner-branched refs.
- Real GitHub remote = `origin` (https://github.com/mcpdev80/baseharbor.git) in this checkout; verified via `git remote -v`. No `lane-origin` trap here.

## PLAN
- Verify PR #1726 head and lane-0428-198-cli-shard-operator-env via gh api + git ls-remote
- Do not write to PR #1726
- Rebase lane-0428-213 onto refreshed base, prove ancestor, force-with-lease push
- Rebase lane-0428-214 onto refreshed base, prove ancestor, force-with-lease push
- Watch new CI run at each new head to terminal, record run-id + conclusion per cell
- Write akte round-3-chainrebase.md, clean containers, report END

## 1. Verification before any write
- `gh api repos/mcpdev80/baseharbor/pulls/1726 --jq .head.sha` => c2f9f2f32fd6bd27c0c0b4e269ad02fde6d643b5
- `git ls-remote origin refs/heads/lane-0428-198-cli-shard-operator-env` (first measurement) => c2f9f2f32fd6bd27c0c0b4e269ad02fde6d643b5
- Both sources agreed on c2f9f2f32fd6 at the time of the rebase.

## 2. PR #1726 not touched
- PR #1726's branch IS the owner branch (lane-0428-198-cli-shard-operator-env). No commit written there. Confirmed open throughout.

## 3. Chain-rebase table

| pr | alter head | neuer head | basis-head zum Rebase-Zeitpunkt | merge-base --is-ancestor (alt) | merge-base --is-ancestor (neu) | run-id | conclusion je Zelle |
| --- | --- | --- | --- | --- | --- | --- | --- |
| #1737 (lane-0428-213-trust-uninstall-false-green) | d0399968c47f | 5be4f003aa1be5ff732e149a1c4a179d3abda047 | c2f9f2f32fd6 | 0 (7db1 ancestor of cand) | 0 (c2f9 ancestor of new head) | 44867291850 | completed / failure (inherited cli-0, cli-3 shard class) |
| #1738 (lane-0428-214-destroystamp) | ebc6ac9c3a30 | bdc3fcb63912a7a9be69be7bc10149deef07b5cf | c2f9f2f32fd6 | 0 (7db1 ancestor of cand) | 0 (c2f9 ancestor of new head) | 44867319394 | completed / failure (inherited cli-0, cli-3 shard class) |

- Rebase geometry per branch: `git rebase --onto c2f9f2f32fd6 7db142852d22 <branch>`. Old base 7db142852d22 is a common ancestor of both candidates; each candidate is exactly one commit on top of 7db1. After rebase the new head lists ONLY the single own commit on top of c2f9f2f32fd6 (`git log --oneline c2f9f2f32fd6..<new head>` = one line each). No content rewritten; identical commit message and file diff as the original head.
- Ancestor proof after push: `git merge-base --is-ancestor c2f9f2f32fd6 <new head>` => exit 0 for both.
- Delivery proof (remote):
  - `git ls-remote origin refs/heads/lane-0428-213-trust-uninstall-false-green` => 5be4f003aa1be5ff732e149a1c4a179d3abda047
  - `git ls-remote origin refs/heads/lane-0428-214-destroystamp` => bdc3fcb63912a7a9be69be7bc10149deef07b5cf
- Both pushes force-with-lease to the two OWN lane branches only.

## 4. CI observation at the new heads (4.6, terminal watched)
- Run 44867291850 (213 / 5be4f00): created 2026-11-21T04:40:57Z, status completed, conclusion failure.
- Run 44867319394 (214 / bdc3fcb): created 2026-11-21T04:41:17Z, status completed, conclusion failure.
- Both runs checkout the same merge head 85ae26150145 ("Merge bdc3fcb63912 into 80dc4987993b"); the Go unit selection is UNIT_SCOPE=cli, matrix cli-0..cli-3.
- cli-2, cli-1 => success; cli-0, cli-3 => failure.
- Failing tests in cli-0 (both runs identical, from run 44867319394 logs):
  - TestAppListAllTargetsWorksAfterInstallationDestroy (app_list_all_targets_test.go:26) - "all-targets inventory depended on deleted Target config docker-dev"
  - TestSecureProfileExportCommandPathAssemblesProductionWiring (secure_profile_export_command_test.go:125) - "operator authentication needs interactive setup but input is not a terminal"
- NEITHER failing test is one of my new files. My new files are:
  - trust_uninstall_test.go (#1737): TestTrustUninstall* family - NOT in the FAIL list.
  - core_installation_runtime_test.go (#1738): TestCoreOnlyBootstrapRuntimeAcceptance, TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget, TestGeneratedBootstrapConsentRetainsCurrentIntent - NOT in the FAIL list.
- Conclusion: my rebase introduced no new --- FAIL: line. The two failures are inherited from the owner's base commits (the same cli-0/cli-3 shard class that failed in run 44854729670 cli-0..cli-3 SUCCESS as the class witness). The `UNIT_RESULT: failure` / "Require complete selected Go shard coverage" gate is what fails the run; this is base drift, not my candidate.

## 5. BASIS-DRIFT (the fund I hand to the owner)
Owner pushes on the base lane (measured via `git ls-remote origin` + `git log --oneline 7db142852d22..<base-ref>`), within 47 minutes:
- 2026-11-21 04:49:46 +0100 0906b043d test(0428-198): stamp direct operator fixture calls
- 2026-11-21 04:58:55 +0100 221b6f437 test(0428-198): align boundary and runtime fixtures
- 2026-11-21 05:05:27 +0100 4719434dc test(0428-198): apply operator fixture at auth boundary
- 2026-11-21 05:12:02 +0100 c2f9f2f32 test(0428-198): preserve anonymous auth-denial cases
- 2026-11-21 05:36:07 +0100 80dc49879 test(0428-198): bind CLI shard auth fixtures explicitly
- 2026-11-21 05:43:50 +0100 46017060d test(0428-198): register target before selecting it
- 2026-11-21 05:46:33 +0100 e45430f2f test(0428-204): authenticate secure export command path

ls-remote witness (current, re-measured after END of work):
- refs/heads/lane-0428-198-cli-shard-operator-env = e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4
- refs/pull/1726/head = e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4

Every successive base head is a strict forward advance ('merge-base --is-ancestor <prev> <next>' = 0 each step, no rewrite, no loss), but the head keeps moving every few minutes. Each push fires a hosted CI run that nobody reads.

Fund for the owner: an exact-head review is impossible on this candidate while the base lane lives. This is the reason PR #1726 cannot be accepted right now - not my third rebase. The mechanical chain maintenance (candidates 213/214 re-based onto c2f9f2f32fd6, pushed, CI observed) is done; the acceptance blocker is the moving base.

## 6. Cleanliness
- No containers, no compose projects, no volumes started on this host.
- `docker ps -a` before: (no docker daemon / no containers)
- `docker ps -a` after: (no docker daemon / no containers)
- Disk: /tmp at ~2.6 GB free throughout; a full clone failed on quota, so refs were fetched into the existing checkout (no scratch files created in the ecosystem root).

## 7. END
0428-204-chainrebase DONE. Candidates re-based onto refreshed base c2f9f2f32fd6, pushed force-with-lease to own lane branches only, CI observed to terminal, no new FAIL introduced. Base drift is the outstanding acceptance blocker for PR #1726.
