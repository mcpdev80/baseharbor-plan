# Round 3 Rebase -- lane-0428-213-trust-uninstall-false-green (#1737)

Lane: 0428-213-rebase1737
Role: Worker (REBASE, no content change)
Card: t-20261121-trust-uninstall-false-green (0428-213), PR #1737
Content already accepted: akte round-2-autharm.md, head 8b38c4f88f3e, bidirectional gate proof in cmd/baha/trust_uninstall_test.go
New head after rebase: 3010b212c8afdd5aba454852e8443486224df541 (author 0428-213-rebase1737)

## PLAN

- Create own worktree + set author identity, verify author name literally before every commit
- fetch + measure current basis head via lane-origin ls-remote, record exact line in evidence
- rebase content-commit 8b38c4f88f3e onto measured basis head (not stale 7546b1806aac)
- Symptom tests: ancestor check, rev-list count=1, diff name-only = only card files
- force push with lease to lane-0428-213-trust-uninstall-false-green
- Run own CI gate to terminal, record run-id + conclusion per cell + byte counts
- Write evidence akte with repo-rule compliance + cleanliness + todo tick

## repo-rule compliance

- Rebase/cherry-pick only. No product code, no .github/**, no scripts/**, no internal/operatorauth/**, internal/identityprovider/**, internal/serviceaccess/** changes.
- Write-set on disk: cmd/baha/trust_uninstall_test.go only (identical blob 01fe6dd1 to accepted content 8b38c4f88).
- No merge, no close, no comment. No subagents.
- No bare go test ./cmd/baha/ on this host; named -run form used (TestTrustUninstall* PASS).
- No runner infrastructure touched; no .github/** edited; no workflow_dispatch/rerun issued.

## BASE ATTESTATION

- Measured basis head (origin/main tracked as lane basis):
  git -C baseharbor ls-remote lane-origin refs/heads/lane-0428-198-cli-shard-operator-env
  -> e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4
- This SHA is an ancestor of our first commit:
  git merge-base --is-ancestor e45430f2f1b7... HEAD -> exit 0 (PASS)
- git diff origin/<base>..HEAD --name-only on #1737:
  cmd/baha/trust_uninstall_test.go  (only our card file, NOT 25)
- git log origin/<base>..HEAD lists ONLY:
  3010b212c test(0428-213 r2): prove operator-auth gate reachable in both directions
- Repo remote (planning): origin https://github.com/mcpdev80/baseharbor-plan.git

## WHY THE ORIGINAL REBASE COMMAND FAILED

- The two prior colleagues failed rebasing onto 7546b1806aac because that is NOT the current basis head; it is an ANCESTOR of the real basis (9 commits behind).
- Real current basis head (measured via ls-remote + gh api): e45430f2f1b7 (NOT 7546b1806aac).
- git merge-base --is-ancestor 7546b1806aac e45430f2 -> 0 (ancestor), 9 commits between.
- git rebase --onto e45430f2 7546b1806aac <branch> dragged in 3 foreign commits (0428-198/204 fixtures) and conflicted -> aborted.
- The owner commit d0399968c (04:24, author Marcel Pfingstgrafen) touches cmd/baha/trust_uninstall_test.go AND trust_status_regression_test.go; the measured basis e45430f2 does NOT carry it. Correct move: cherry-pick ONLY our content 8b38c4f88 onto the measured basis and drop the owner commit from the PR (it belongs to the basis, per mission).

## SYMPTOM TESTS (acceptance criteria)

- git merge-base --is-ancestor e45430f2 HEAD -> exit 0 PASS
- git rev-list --count e45430f2..HEAD -> 1 (only our content commit 3010b212c)
- git diff --name-only e45430f2 HEAD -> cmd/baha/trust_uninstall_test.go only (NOT 25)
- content blob HEAD:cmd/baha/trust_uninstall_test.go == 01fe6dd1 == accepted 8b38c4f88 blob (byte-identical)

## PUSH / DELIVERY

- git ls-remote lane-origin refs/heads/lane-0428-213-trust-uninstall-false-green -> 3010b212c8afdd5aba454852e8443486224df541
- git ls-remote lane-origin refs/pull/1737/head -> 3010b212c8afdd5aba454852e8443486224df541 (PR head matches)
- fetch output confirms forced update: + 8b38c4f88...3010b212c lane-0428-213-trust-uninstall-false-green
- PR #1737 now has exactly 1 commit (author 0428-213-rebase1737); owner commit d0399968c removed from PR.
- Note: git push via remote alias failed (git 2.53.0 transport "hostname contains invalid characters"); direct HTTPS URL push succeeded.

## CI GATE (4.6, own run to terminal)

- CI run 44883097577 on head 3010b212c. Jobs: PR Trusted Plan SUCCESS, source format SUCCESS, cli-build SUCCESS, cli-gofmt SUCCESS, Focused Python SUCCESS, Native gate plan SUCCESS.
- FAILING jobs (cli-0, cli-1, cli-2, cli-3, cli-vet): INHERITED red, NOT from my commit.
  - cli-0 fail: TestAppListAllTargetsWorksAfterInstallationDestroy -> deleted Target config "docker-dev" missing: config.yaml missing. Inherited from #1739/#210 (0428-210).
  - cli-vet fail: TestMCPRegistrationCIInProcess hits operator-auth gate (mcp.go:309) on anonymous MCP call; present on measured basis e45430f2 (git grep confirms).
- Inheritance PROVEN: prior run 44878429408 on head 8b38c4f88 (same card, pre-rebase) shows identical failures: cli-0/1/2/3 failure + cli-vet failure. Same red before and after this rebase.
- My file is gofmt-clean; my content set is only cmd/baha/trust_uninstall_test.go.
- Local named test (test-runner rule, no bare ./cmd/baha/):
  go test ./cmd/baha/ -count=1 -run 'TestTrustUninstall' -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication' -> ok (3.185s)
- CI policy note: PR is now OPEN (was DRAFT); candidate-added checks are ADVISORY and skip. Required base-plan checks are the inherited red above.

## cleanliness

- docker ps -a BEFORE: empty (no containers)
- docker ps -a AFTER: empty (no containers)
- docker volume ls BEFORE: local 7e62a6e..., local 68854a0..., bh-docker-dev-shared_postgres-data-1 (pre-existing ambient)
- docker volume ls AFTER: identical (no volume created/removed by this lane)
- podman ps -a: empty
- I started NO containers/compose during this lane (rebase-only work). No residuum. ambient-core untouched.

## Todo tick

- All 7 steps in todos/0428-213-rebase1737.json marked done.

## Status

END 0428-213-rebase1737 DONE
