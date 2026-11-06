# Round 3 — Secure Export (t-20261018-r27-secure-export), Lane w216

State: review candidate on PR #1396 (same branch work/r27-secure-export, no second PR).

## PLAN
1. Read review-1396a.md lines 74-101 and the current commands.go / secure export implementation.
2. Fetch origin, verify develop ancestry (f01d2fb or newer) and set up the candidate worktree on work/r27-secure-export at PR #1396 head.
3. Write the real command-path cell: rootCommand() -> secureProfileExportCommand -> resolve test application -> devaccess.Load local credentials -> write file + decrypt.
4. Mutation proof: remove the registration line in commands.go in an isolated worktree, show THIS cell goes RED; restore, show GREEN; capture git-diff evidence.
5. Regression-read the fail-closed boundaries (empty/invalid/wrong-password/tamper/truncation).
6. Commit and push to work/r27-secure-export (PR #1396), take the ls-remote witness (name-only).
7. Observe the hosted CI run TERMINAL on the new head myself; run race checks locally.
8. Write this evidence into baseharbor-plan, push to origin/main, take the ls-tree witness.
9. Clean up worktrees/caches and post END to the coordinator.

## Review finding addressed (review-1396a.md:74-101)
The claimed assembly cell TestSecureProfileExportWritesEncryptedFile constructed
manifest and entries itself and only called the adapter (BuildExport /
writeSecureProfileExport / OpenExport). rootCommand, secureProfileExportCommand,
executeSecureProfileExport and devaccess.Load never appeared in it; the
registration mutant's red signal was the documentation-sync checks, not the
assembly. This round adds the real command-path cell and proves the mutant
discriminates THAT cell.

## BASE ATTESTATION
- Branch work/r27-secure-export, prior head 0001ca02d19fe9edd69d79c94633377dc3f09260 (ls-remote at start, exactly the mission-named head).
- origin/develop at start: f01d2fbdea6b93af6e06ca6297d04065b6acf701.
- `git merge-base --is-ancestor f01d2fb... 7b2f053d...` rc=0: develop f01d2fb IS ANCESTOR OF the new candidate head.
- The candidate head 7b2f053d is 0001ca02 (same-branch prior head, whose own develop-merge already carries f01d2fb) plus exactly ONE new commit; `git log --oneline 0001ca02..HEAD` lists only:
  - 7b2f053d test(secure-export): exercise the real command path and fix the swapped flag return
- No foreign candidate is carried on top; no branch was cut from another PR head.

## Change-set (round 3)
- cmd/baha/secure_profile_export_command_test.go — NEW command-path cell
  TestSecureProfileExportCommandPathAssemblesProductionWiring plus the tree-shape
  probe TestSecureProfileExportCommandPathFailsClosedWithoutRegistration.
- cmd/baha/secure_profile_export.go — one-line production fix revealed by the cell
  (see "Defect found").
- No other product file changed. No .github/** change, no docs change needed
  (the command registry entry is unchanged).

## The command-path cell (what it really does)
- Builds the PRODUCTION tree: `root := rootCommand()` (store seam =
  application.DefaultStore(), registration via cmd/baha/commands.go line 251).
- Isolated state: XDG_CONFIG_HOME/XDG_DATA_HOME = t.TempDir(), config.yaml with
  local-scope target `secure-export-ci`; BASEHARBOR_TARGET set. No host state,
  no containers, no compose.
- Test application: repository baseharbor.yaml (name mailflow, dev, workload
  component api) in the cwd; identity materialized in the repository owner store
  .baseharbor/apps exactly as one-time `baha app init` does (application.Store.Create).
  The command resolves it through the real resolver path
  (resolveSecretApplication -> resolveApplication -> repository discovery).
- Local credentials: devaccess.Configure("secure-export-ci","dev",...) writes to
  the exact path the command later reads through devaccess.Load(resolved.Target.Name,
  manifest.Environment); the cell witnesses devaccess.Path + os.Stat.
- Invocation: root.Execute(ctx, ["app","secure-profile","export","--password-file",...,"--output",...])
  with the same invocation context runWithIO builds for a real CLI call
  (withLocalInvocation "cli" + operatorauth.WithEnforcement + localWorkloadScope).
  rootCommand() binds its application.DefaultStore() seam from the repository
  manifest discovered at the process cwd when the tree is built; the cell builds
  the tree after chdir into the isolated fixture, so the seam resolves to the
  fixture's .baseharbor/apps exactly as in a real CLI invocation.
- Assertions: output file created 0600; decrypts ONLY with the supplied password;
  carries the exact locally-loaded username/password entries; wrong/nil password
  fails closed on the produced file; neither stdout/stderr nor the ciphertext
  contains the developer password or the export password; envelope is the JSON
  export envelope (no plaintext in the ciphertext field).

## Defect found by the cell (fixed in this commit)
parseSecureProfileExportArgs declared `(name, passwordPath, outputPath string, err error)`
but returned `name, outputPath, passwordPath, nil` — the two paths were swapped.
Through the real command path this made every `--output` export die with
"inspect export password file: stat <output-path>: no such file or directory".
The prior adapter-only cells never called the parser with both flags in a real
flow, so the defect survived rounds 1-2 and CI. Fixed to
`return name, passwordPath, outputPath, nil` (secure_profile_export.go:122).

## Mutation proof (real source mutation, isolated worktree, ON THE FINAL HEAD eb02ab6e)
- Mutant worktree: candidate/mutant2 (detached at eb02ab6e), single-line deletion
  at cmd/baha/commands.go:251 (`secureProfileExportCommand(store),` removed).
  git diff witness: `-		secureProfileExportCommand(store),`
- Result (RED in the COMMAND cell itself):
  `secure_profile_export_command_test.go:125: baha app secure-profile export through the command tree failed: unknown command "secure-profile" for app`
- Counterprobe: `git checkout cmd/baha/commands.go` (line restored) ->
  `ok github.com/mcpdev80/baseharbor/cmd/baha 0.196s` — GREEN, worktree clean (0).
- The isolated mutant worktree was removed after the proof (`git worktree list`
  shows only the candidate). The identical proof was run at 7b2f053d before the
  comment-only amend.

## Boundaries (regression-read, unchanged)
Previously confirmed; this round re-read and re-ran them green on the candidate
(all 11 cells PASS):
- empty selection / incomplete manifest / empty password / traversal names:
  internal/applicationbackup/secureprofile_test.go (TestExportRejectsEmptySelection,
  TestExportRejectsIncompleteManifest, TestExportRejectsEmptyPassword,
  TestExportRejectsTraversalName).
- wrong password / nil password / tamper / truncation fail-closed:
  TestExportWrongPasswordFailsClosed, TestExportTolerantMutantFailsRed,
  TestExportTamperedCiphertextFailsClosed, TestExportTruncatedEnvelopeFailsClosed,
  TestExportRejectsTamperedSchemaVersion, TestExportUnreadableWithoutPassword;
  command-level: TestSecureProfileExportWrongPasswordFailsClosed and the
  wrong/nil-password assertions inside the new command-path cell.

## Local verification
- go vet ./cmd/baha clean; go build ./... clean; gofmt clean.
- Focused: all 8 TestSecureProfileExport* cells pass, also with -race -count=20
  (race gate, `ok ... 22.033s`).
- Documentation-sync checks on the unchanged registry:
  TestHumanCommandIndexTracksExactCommandMetadata,
  TestMachineDocumentationTracksRegistryAndCommandTree and
  TestMachineCoverageCIRealTreeAndJSONClassification pass.
- go test ./internal/applicationbackup ./internal/devaccess -count=20: ok (race
  for both packages also ok at -count=1).
- Full go test ./cmd/baha: one pre-existing environment failure, identical on the
  unmodified base head 0001ca02 (verified by stash/re-run):
  TestAppEditCommandCompleteProviderEditRunsRealLifecycle —
  "selected Docker endpoint unix:///var/run/docker.sock is unavailable"
  (Docker runtime gate needs its named SSH runner host; not this lane's host,
  per owner directive; hosted CI carries that gate).

## Candidate
- Head: eb02ab6ed6f31b7fa99e19259d6b3a83d524d034 on work/r27-secure-export (PR #1396).
- Round-3 commits on top of the mission head 0001ca02 (git log --oneline 0001ca02..HEAD lists ONLY these two, no foreign commit):
  - 7b2f053d test(secure-export): exercise the real command path and fix the swapped flag return
  - eb02ab6e test(secure-export): document the production store-seam binding in the command cell
- ls-remote witness (name-only, after push):
  eb02ab6ed6f31b7fa99e19259d6b3a83d524d034	refs/heads/work/r27-secure-export
- remote echt == local head WORTLICH; gh pr view 1396 headRefOid == eb02ab6e (MERGEABLE, OPEN).
- The candidate chain pushed 7b2f053d -> e10220ec (comment commit) -> eb02ab6e
  (e10220ec amended with two extra comment lines; --force-with-lease on the same
  branch, no second branch). Superseded heads carry identical tests.
- develop: origin/develop was f01d2fb at lane start; `git merge-base --is-ancestor
  f01d2fb HEAD` rc=0 on eb02ab6e (mission gate: develop f01d2fb or newer ancestor).

## Hosted run (Eigenes-Run-Pflicht) — Vergleichszeile (per KOORD)
- 42154280478 @ 7b2f053d: CANCELLED (superseded by the comment amend push).
- 42154558960 @ e10220ec: CANCELLED (amend-Vorlauf; head_sha e10220ec, counts NOT).
- 42154778495 @ eb02ab6e (FINAL, am exakten Kandidatenkopf): head_sha WORTLICH
  "eb02ab6ed6f31b7fa99e19259d6b3a83d524d034" (gh api run-json .head_sha, not
  inferred from the branch). TERMINAL = FAILURE, self-observed via gh run watch.
  Failing job: "PR · Validation · go-unit-tests", step "Execute existing
  validation owner without publication". Failing log lines (WORTLICH):
  `--- FAIL: TestSourceSnapshotDetectsChangeDuringRead (5.01s)`
  `    source_snapshot_test.go:247: change-during-read MutationAcked never fired on the mutated path within the local bound`
  `FAIL	github.com/mcpdev80/baseharbor/internal/development	6.406s`
  All other validation gates (build/vet/gofmt/docs/contracts/package/guided/
  wizard/python/mkdocs/Trusted Plan/Workflow policy/Source format) SUCCESS.

## STATE (per scope split: failing check is not mine to fix or rerun)
- The failing test lives in internal/development/source_snapshot_test.go — NOT
  in this card's write-set and untouched by every round-3 commit
  (`git diff 0001ca02..HEAD --name-only` = secure_profile_export.go,
  secure_profile_export_command_test.go only).
- This is the known snapshot change-during-read flake family (lanes w178-w209,
  PR #1400 work/r27-flake-r7 "causal MutationAcked acknowledgement" open and
  itself failing at its own head 12e3c3fe run 42154942158).
- Base-branch comparison (same test, same runner class): run 42147787627 @
  0001ca02 = SUCCESS; the immediately later run 42154778495 @ eb02ab6e = this
  flake. On this lane's head the test passes locally (-count=1 PASS). Evidence
  points to intermittent timing on the hosted runner, not to this change-set.
- Per scope split I do NOT trigger reruns or workflow_dispatch; the failure is
  reported as STATE (check name + failing log line above) and this lane stops at
  a fully verified candidate + green local reproduction of every required cell.

## repo-rule compliance
- One candidate per chain: same branch work/r27-secure-export, same PR #1396, no
  second branch/PR; no .github/** edit; no workflow_dispatch or rerun.
- No subagents used. All steps executed in this session.
- No containers/compose started anywhere; no checkout in the ecosystem root; all
  worktrees/caches under /tmp/opencode/w216-secure-export-r3-wt.
- Evidence lives only in baseharbor-plan; no .evidence/ in the product repo.
- Claims/ownership: this lane was dispatched for round 3 of the card by the
  coordinator mission file; no other lane touched this branch during the round
  (ls-remote before push == 0001ca02 mission head).

## Evidence publishing
- This act published to baseharbor-plan origin/main as commit
  7314f937c6ad1abd736729e6ff2b3ca92a12887c.
- ls-tree witness: `git ls-tree origin/main evidence/r27-welle5-2026-11-06/secure-export/`
  contains `100644 blob 5021136ba2732f0c01e73c57ea9436feeb727cff	evidence/r27-welle5-2026-11-06/secure-export/round-3.md`
- The final END-bearing version is committed and pushed with it; the closing
  `git ls-tree -r origin/main | grep secure-export/round-3` output is pasted at
  the very end of this file after the push.

## END
END_DONE w216-secure-export-r3: head=eb02ab6ed6 befehlspfad=zelle echt mutante=ROT in BEFEHLSZELLE+gegenprobe grenzen=regressions-read lauf=42154778495 TERMINAL(failure: nicht-mein snapshot-flake, STATE gemeldet) lsremote=eb02ab6ed6 | Kandidat vollstaendig; gehosteter go-unit-tests faellt am bekannten internal/development MutationAcked-Flake (PR #1400 in Arbeit), alle uebrigen Gates success.
