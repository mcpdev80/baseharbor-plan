# Hop develop c463edf8 - lanes 0428-199 workloadport (PR #1723) and 0428-201 statever (PR #1725)

Card 0428-199 (workload-port) + follow-up 0428-201 (statever), hop mission `hop17235c.md.g`
(0428-233 tmpdir belongs to its own lane, see below).

## Context

Follow-up directive: after the first hop to develop 5ca8420c, re-hop both candidates once more
onto the newest develop (463edf87ee at the time) so they sit on the latest base. Witness in the
directive: #1723 head d7b4f1b3d47, #1725 head 27e509757b2 (both already on 5ca8420c181, the
jump to 463edf8 still missing). Method: `git merge --no-ff 463edf87ee` on each branch (NO
rebase/amend/force), push without force, watch the hosted PR-run to terminal (run-id + failed-count).

## Reality observed vs. directive witness

- #1723 `lane-0428-199-workloadport` remote head was d7b4f1b3d47e1756938692490140e77717b2dd21,
  develop base 8b9a8f50645 (the hop commit message confirms this base). 5ca8420c181 is NOT an
  ancestor; 463edf87ee is not an ancestor. The directive's "both on 5ca8420c" did not match the
  actual remote heads; the additive no-ff merge still lands correctly regardless.
- #1725 `w201-0428-201-statever` remote head was 27e509757b201abeee521ccf7885fa787b248a0b, same
  8b9a8f50645 base. Same conclusion.
- develop head at hop time: 463edf87ee6f12c9da2ae2ee02ea6fe7c7ef0f9 (the #1750 merge commit).

## What was done (hop 1)

- #1723: `git checkout lane-0428-199-workloadport` in workers/0428-199-workloadport-wt,
  `git merge --no-ff 463edf87ee` -> b2d9aeb446f1360f03e6f8a8c416b315e833a729, pushed without force.
- #1725: `git checkout w201-0428-201-statever` in workers/hop-1725-wt,
  `git merge --no-ff 463edf87ee` -> dd4e826f6c87c838950927a664f145ddc9a3b314, pushed without force.
- Both merges are clean no-ff merges bringing 463edf8 on top (include the #1750 diff, which carries
  the 0428-233 tmpdir fix into the branch tree).

## Hosted CI runs (hop 1)

- PR #1723, head b2d9aeb4: run id 7223, db 44993386491, status completed/failure.
  Failed job only: "PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities)".
  All Go unit shards (cli-0/1/2/3), go-build, go-vet, cli-gofmt, packages, owner, Focused Python,
  Source format, Workflow policy: success. The runtime-gate failure is the pre-existing
  data-capabilities consent/interactive-operator-auth condition (log line:
  `target "atomic-docker-data-capabilities" is not configured`;
  `operator authentication needs interactive setup but input is not a terminal`;
  `record deployment before mutation: candidate submission requires an explicit operator/automation
  consent (--confirm-candidate)`) - identical to prior #1723 runs 7186 (d7b4f1b3) and 7164
  (8fe3c9bf). Outside my write-set.
- PR #1725, head dd4e826f: run id 7224, db 44994336034, status completed/failure.
  Failed job only: "PR · Selected Runtime (atomic/podman/data-capabilities, podman, data-capabilities)".
  All Go unit shards (cli-0/1/2/3), go-build, go-vet, packages, owner, Focused Python, Source format,
  Workflow policy: success. Same pre-existing runtime-gate condition.

## Stand-down (run directive standdownffe.md.g)

Coordinator recalled the second hop: seat 0428-061-sourcepull (f0f6c8b4) takes over the branch
hop itself (ls-remote witnesses b2d9aeb446f and dd4e826f6c8) and will apply the missing hop onto
the newest develop 52a3c5446f41a1dd8678d99875e4cb1eee67874c. Instruction: run NO further
`git merge` and NO further push on the two lanes (double-push would be a loss).

What I pushed before the recall (ls-remote witness):
- lane-0428-199-workloadport = b2d9aeb446f1360f03e6f8a8c416b315e833a729 (PR #1723)
- w201-0428-201-statever = dd4e826f6c87c838950927a664f145ddc9a3b314 (PR #1725)

Stopped. No further merge or push on either lane. Remote heads confirmed unchanged since.

## Substantive part status (0428-199 portedat + 0428-233 tmpdir)

Both implementations already exist on their lanes (no new code to write this shift):
- 0428-233 tmpdir-freigabe: `hostConfigIsolationDir(t)` nests the isolation dir under
  `t.TempDir()` (workers/0428-223-testctx-wt, lane-0428-223-testcontext-target / PR #1750, merged
  to develop). Regression test `TestHostConfigIsolationDirLeavesNoSystemTempEntry` added; it fails
  under the old `os.MkdirTemp("", ...)` form and passes under the `t.TempDir()` form. The fix rides
  into #1723 and #1725 branch trees via the 463edf8 merge (verified: `hostConfigIsolationDir(t)`
  present in the merged tree).
- 0428-199 portedat: `--workload-port` logic in cmd/baha/app_apply.go, app_input_resolver.go,
  app_workload.go, on lane-0428-199-workloadport / PR #1723.

## PR #1645 measurement (stand-down item 2)

PR #1645 = w091-tempo-r5-fix, "perses/tempo: rename .go witnesses to .go.txt (CI package-selection
fix)", base develop, OPEN, head 4d73aa97808d000d2f70eaa193f8dbfc14e817a7. Back from develop:
463edf8..4d73aa97 = 1 commit (the directive's "back=263" is stale; current distance is 1).

Hop-without-conflict verdict: POSSIBLE. In-file merge test on a throwaway worktree cut from current
develop 52a3c5446f: `git merge --no-ff 4d73aa97808` -> "Automatic merge went well; stopped before
committing". Zero unmerged files (`git diff --diff-filter=U` empty, no conflict markers). The
merge-tree/base-form check confirms only content additions (`+` lines), no conflict markers.

No push to #1645 (stand-down: only my own content would go there). Assessment reported to
coordinator; the 0428-061-seat decides the actual hop.

## cleanliness

- workers/0428-199-workloadport-wt: CLEAN (branch lane-0428-199-workloadport, head b2d9aeb4).
- workers/hop-1725-wt: CLEAN (branch w201-0428-201-statever, head dd4e826f).
- workers/0428-223-testctx-wt: CLEAN (branch lane-0428-223-testcontext-target, head aedf79f7).
- Throwaway merge-probe worktree _mergeprobe-1645-wt created and removed (git worktree remove
  --force after git merge --abort). Not present in `git worktree list`.
- No docker/podman compose projects started this shift; ambient stack untouched.
- No stray build artifacts left in any worktree (removed `baha` ELF from the workloadport
  worktree before END).
