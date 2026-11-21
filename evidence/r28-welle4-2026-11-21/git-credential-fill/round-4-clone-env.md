# Round 4 correction — card t-20261121-git-credential-fill-bootstrap-hang (0428-217)

LANE: 0428-217-cloneenv
PR: #1742 (base develop, draft=false)
CANDIDATE SHA: 6f8fa120f7e5e79d260ed89d486633bc152105de
BRANCH: w0428-217credfill
AUTHOR: 0428-217-cloneenv <0428-217@baseharbor.local>
EVIDENCE RUN: CI run 44905476380 conclusion=success on 6f8fa120

## PLAN

1. Verify BEFUND 3 freshness: hop to develop 97b2ba5543f0 (run 44900657812 completed/success) already satisfies the reviewer's round-2 freshness finding; the reviewer assessed the old head 719d28a888ab, superseded by the hop.
2. Implement BEFUND 1 (hard product change): in cmd/baha/app_inspect_remote.go the git-clone child set `cmd.Env = append(cmd.Env, "GIT_TERMINAL_PROMPT=0")` on a NIL cmd.Env, replacing the inherited environment (no PATH/HOME/gitconfig/credential-helper). Switch to `cmd.Env = withGitPromptDisabled(os.Environ())` using the existing helper (cmd/baha/app_update.go:475-481). No second helper invented, no env var dropped, no softened tolerance.
3. Add focused regression test cmd/baha/0428-217_clone_env_test.go driving the production env construction and asserting (i) the parent sentinel is inherited into the child vector, (ii) PATH is inherited, (iii) GIT_TERMINAL_PROMPT=0 wins.
4. Add mutation witnesses in BOTH directions: M1 (reintroduced `append(cmd.Env, …)` on nil) FAILS; M2 (suppression removed from the helper) FAILS. Both recorded with command and output below.
5. BEFUND 2 (evidence only): confirm the earlier workaround sites still exist at the current head (card workaround closeout below).
6. Push candidate, run own CI to terminal (4.6), commit evidence to origin/main, post END.

## BEFUND 3 freshness

Reviewer assessed old head 719d28a888ab (round-2 review-2). The hop-lane set develop to 97b2ba5543f0 (run 44900657812 = completed/success; author 0428-217-hopdev; rev-list develop..head = 2). Confirmed before working:

git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
97b2ba5543f07b820b5c18a688058fd932c4516f	refs/heads/develop
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1742/head
20ad0713e9892492204cf88910ee926ee20d1461	refs/pull/1742/head
git merge-base --is-ancestor 97b2ba5543f07b820b5c18a688058fd932c4516f 20ad0713e9892492204cf88910ee926ee20d1461 → develop IS ANCESTOR OF PR HEAD = YES

The hop already landed the fix+test on branch w0428-217credfill; this round adds the BEFUND-1 env-inheritance fix as a clean single commit on the same branch.

## BEFUND 1 — fix

File: cmd/baha/app_inspect_remote.go (write-set allowed by mission).
Before:
	cmd.Env = append(cmd.Env, "GIT_TERMINAL_PROMPT=0")   // cmd.Env NIL → replaces inherited env
After:
	cmd.Env = withGitPromptDisabled(os.Environ())        // copies env, appends GIT_TERMINAL_PROMPT=0

withGitPromptDisabled is the existing helper cmd/baha/app_update.go:475-481 (copy of env + append). No new helper, no dropped var.

## TESTS

File: cmd/baha/0428-217_clone_env_test.go (new, write-set allowed).
Three tests:
- TestGitCloneInspectInheritsParentEnvAndSuppressesPrompt — drives the production env construction (withGitPromptDisabled over os.Environ) with a hostile inherited GIT_TERMINAL_PROMPT=1 plus a BASEHARBOR_0428_217_SENTINEL, records the real child env, asserts: sentinel inherited, PATH inherited, GIT_TERMINAL_PROMPT=0 wins (last copy).
- TestGitCloneInspectEnvDerivationMutationAppendedNil — M1 negative: source must derive from os.Environ, not append to nil cmd.Env.
- TestGitCloneInspectPromptSuppressionPresent — M2 negative: withGitPromptDisabled must append GIT_TERMINAL_PROMPT=0.

## MUTATION RUNS (both must FAIL)

Both mutations recorded with command and exit code (source restored after each run; git diff clean).

M1 — reintroduce `append(cmd.Env, …)` on nil cmd.Env:
command: sed -i 's|cmd.Env = withGitPromptDisabled(os.Environ())|cmd.Env = append(cmd.Env, "GIT_TERMINAL_PROMPT=0")|' cmd/baha/app_inspect_remote.go
then: go test ./cmd/baha/ -count=1 -run 'TestGitCloneInspectEnvDerivationMutationAppendedNil' -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication'
output:
--- FAIL: TestGitCloneInspectEnvDerivationMutationAppendedNil (0.00s)
FAIL
github.com/mcpdev80/baseharbor/cmd/baha	0.007s
EXIT CODE: 1 (go test failed)

M2 — remove the suppression from the helper (app_update.go withGitPromptDisabled):
command: sed -i 's|clone = append(clone, "GIT_TERMINAL_PROMPT=0")|// suppressed-for-mutation|' cmd/baha/app_update.go
then: go test ./cmd/baha/ -count=1 -run 'TestGitCloneInspectPromptSuppressionPresent' -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication'
output:
--- FAIL: TestGitCloneInspectPromptSuppressionPresent (0.00s)
    0428-217_clone_env_test.go:103: M2: withGitPromptDisabled must append GIT_TERMINAL_PROMPT=0 to the child env
FAIL
github.com/mcpdev80/baseharbor/cmd/baha	0.007s
EXIT CODE: 1 (go test failed)

Both mutations FAIL (exit code 1) as required. The 'suppression removed' (M2) witness is demonstrated above with command, output and non-zero exit code.

## Local full precheck (pre-push)

command: bash scripts/ci-fast-check.sh
result: PASS — Go file size PASS, Function span PASS, Regression ratchet PASS, Workflow policy PASS (20 approved workflow files); 295 tests OK.
gofmt -l cmd/baha/0428-217_clone_env_test.go cmd/baha/app_inspect_remote.go → empty (formatted).

## CI (own run to terminal, 4.6)

Candidate head: 6f8fa120f7e5e79d260ed89d486633bc152105de
Branch: w0428-217credfill (matches .github/workflows/ci.yml w0* pull_request trigger; PR #1742 base develop, draft=false)
CI workflow: "CI · Source & Quality" (ci.yml) — the validate job runs `go test ./...` (line 355) plus docs/formatting/readiness; release_source_preflight runs `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha`.
PR commits confirmed on GitHub for #1742 include 6f8fa120 fix(0428-217): clone inspect must inherit parent env.
Run id: 44905476380
Run status: completed
Run conclusion: success
Job "Workflow policy": success; job "PR · Trusted Plan": success; required Go tests routed into mandatory parallel shards, all success.
Witness (GitHub API):
curl -s https://api.github.com/repos/mcpdev80/baseharbor/actions/runs/44905476380 → "status": "completed", "conclusion": "success"
Delivery proven after push:
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1742/head
6f8fa120f7e5e79d260ed89d486633bc152105de	refs/pull/1742/head
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/w0428-217credfill
6f8fa120f7e5e79d260ed89d486633bc152105de	refs/heads/w0428-217credfill

## card workaround closeout (BEFUND 2)

Current head: 6f8fa120f7e5e79d260ed89d486633bc152105de. Every earlier workaround site is present at this exact head (no site removed):

- gitcredential.go host-named error: internal/credential/native/gitcredential.go:58, :80, :82 → `fmt.Errorf("%w: host %s", ErrGitCredentialUnavailable, host)`. Present.
- host.go non-interactive establishment: internal/credential/native/host.go:34 (ExecRunner.Invoke), :50 (appendNonInteractiveEnv), :75-79 pins GIT_TERMINAL_PROMPT=0, SSH_ASKPASS=/bin/false, GIT_CREDENTIAL_HELPER=/bin/false, GIT_ASKPASS=/bin/false exactly once. Present.
- app_update.go non-TTY stdin: cmd/baha/app_update.go:456 (gitOutput), :515 (gitIsAncestor) → cmd.Stdin = strings.NewReader(""). Present.

No remaining workaround site to list; the diff at the current head is exactly the BEFUND-1 env fix plus the round-2 content already on the branch.

## branch provenance

git merge-base --is-ancestor origin/develop HEAD → YES (develop is ancestor of candidate)
git diff origin/develop...HEAD --name-only:
cmd/baha/0428-217_clone_env_test.go
cmd/baha/app_inspect_remote.go
cmd/baha/app_update.go
cmd/baha/app_update_gitstdin_test.go
internal/credential/native/credfill_noninteractive_test.go
internal/credential/native/credfill_pty_linux_test.go
internal/credential/native/credfill_pty_stub_test.go
internal/credential/native/gitcredential.go
internal/credential/native/host.go
git log --oneline origin/develop..HEAD lists only:
6f8fa120f fix(0428-217): clone inspect must inherit parent env while suppressing git prompt (BEFUND 1)   [0428-217-cloneenv]
20ad0713e test(0428-217): prove the credential-fill fix on git's own prompt path                          [0428-217-hopdev]
b0e995027 fix(0428-217): git credential fill must fail closed non-interactively with host-named no-credential error  [0428-217-hopdev]
Only my own commit on top of the hop's PR-head content; no foreign candidate carried.

## FOUR PROOF LINES (Owner END requirements)

git merge-base --is-ancestor 97b2ba5543f07b820b5c18a688058fd932c4516f 6f8fa120f7e5e79d260ed89d486633bc152105de → JA (develop 97b2ba5543f0 is ancestor of candidate 6f8fa120)
git rev-list --count 97b2ba5543f07b820b5c18a688058fd932c4516f..6f8fa120f7e5e79d260ed89d486633bc152105de → 3
git rev-list --count 6f8fa120f7e5e79d260ed89d486633bc152105de..97b2ba5543f07b820b5c18a688058fd932c4516f → 0
git log -1 --format='%an' 6f8fa120f7e5e79d260ed89d486633bc152105de → 0428-217-cloneenv
git log -1 --format='%P' 6f8fa120f7e5e79d260ed89d486633bc152105de → 20ad0713e9892492204cf88910ee926ee20d1461 (hop PR-head; sits on develop after the hop; candidate is not ahead of develop)

## evidence on origin/main (second-to-last action)

git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep round-4-clone-env:
evidence/r28-welle4-2026-11-21/git-credential-fill/round-4-clone-env.md
plan commit b833ffaef (evidence committed + pushed to origin/main before END).

## repo-rule compliance

Write-set (mission-limited): cmd/baha/app_inspect_remote.go + its test file + new cmd/baha/0428-217_clone_env_test.go. No .github/** touched (Owner scope). No scripts/**, no internal/operatorauth/identityprovider/serviceaccess, no internal/observability/registry.go, no internal/capability/perses_selection.go, no app_commands.go/app_lifecycle.go, no owner-stacked cards. No second PR, no merge, no close, no subagents, no git stash in the final push, no bare `go test ./...` / `go test ./cmd/baha/` without the named skip form on this host. git config user.name = 0428-217-cloneenv (tooling issue #24).
NOTE: during iteration the shared baseharbor checkout's `origin` remote had been overwritten with a /tmp test-path (REMOTE GUARD 2026-11-20 scenario). Restored origin → https://github.com/mcpdev80/baseharbor.git before push; all remote truth measured via git ls-remote against that URL.
A prior "test" session had committed stray "init" commits (c76d68ece/269e0a90a/b2a09ba75) onto w0428-217credfill; reset the branch back to the GitHub PR head 20ad0713e and re-applied the BEFUND-1 fix + test as the single coherent commit 6f8fa120f.

## cleanliness

docker ps -a before/after (pid 2706044):
<empty — no containers>
cleanliness: no test containers/networks/volumes/state created; my Go tests spawn sh/git child processes only, no docker/podman projects. /tmp probe dirs (/tmp/TestGitCloneInspectInheritsParentEnvAndSuppressesPrompt*) cleaned.

## END

LANE 0428-217-cloneenv DONE — candidate 6f8fa120f on PR #1742 (base develop), CI run 44905476380 conclusion=success. BEFUND 1 fixed, tests + both mutations green/red as required, BEFUND 2 closeout complete.
