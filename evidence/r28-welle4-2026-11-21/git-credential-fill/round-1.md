# 0428-217: git credential fill bootstrap hang — round-1

- Lane: w0428-217credfill (session laptop)
- Card: t-20261121-git-credential-fill-bootstrap-hang (0428-217), from hunt H-V25
- Candidate: 0df7efc00bb3cfd784c988613a9ec5f8fb6215b4
- PR: #1742, base develop (develop head 40cb28c758b02960356434b630086a341ebe1738)
- Hosted CI run: 44874605168 (pull_request, branch w0428-217credfill)

## PLAN (nummeriert)

- Reality check 4.1: develop = 40cb28c758b0 (three ls-remote witnesses), PR list empty
- Write-set confirm before first edit: grep credential fill / GIT_ASKPASS / SSH_ASKPASS in cmd/baha + internal
- Red-first 5.6: reproduce the hang on develop; name the sick SHA
- Implement fix: git credential fill fails closed non-interactively; caller surfaces host + no-credential error
- Fail-bild check: error names host + no credential, not timeout/panic/hang
- Push + PR (draft then ready, base develop); watch own run to terminal
- CI intake: show which existing shard runs the new test; prove my package green in hosted CI
- Evidence + cleanliness

## Basis-Attestation (ls-remote develop)

```
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop
```

Branch cut from exact develop head 40cb28c758b0 (ancestor of my commit, see provenance below).

Planning repo verified before first evidence commit:

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Wrong-zone note: /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor-plan is NOT the planning repo — not used.

## Write-set confirmation (Owner clarification 2026-11-21, write-set Pflicht)

Card 0428-217 names the two files `cmd/baha/app_inspect_remote.go` and `cmd/baha/mcp.go`.
Measured write-set of this candidate, each with a one-line "why needed":

- `cmd/baha/app_inspect_remote.go` — named in card; git clone here feeds a non-TTY stdin + GIT_TERMINAL_PROMPT=0 so the read-only clone cannot prompt on the password line.
- `cmd/baha/app_update.go` — NOT named in the card; only makes gitOutput() and gitIsAncestor() run with a non-TTY stdin so the update/fetch path cannot hang on a prompt. Card was too narrow here — this is a scope expansion, flagged for the coordinator to reopen the card (no behavior beyond non-interactive; no prompt logic changed).
- `internal/credential/native/gitcredential.go` — outside cmd/baha/ (allowed: internal/credential/**); Resolve returns a host-named ErrGitCredentialUnavailable so the caller names the host and the missing credential.
- `internal/credential/native/host.go` — outside cmd/baha/ (allowed); ExecRunner forces the child fully non-interactive (GIT_TERMINAL_PROMPT=0, GIT_ASKPASS=/bin/false, SSH_ASKPASS=/bin/false), preserving HOME/PATH.
- `internal/credential/native/credfill_noninteractive_test.go` — outside cmd/baha/ (allowed); red-first regression, H-V26.

No tabu file touched: no internal/operatorauth/**, internal/identityprovider/**, internal/serviceaccess/**, internal/capability/perses_selection.go, internal/observability/registry.go, no .github/**.

## Reach (file:line)

- `internal/credential/native/gitcredential.go:38` GitCredentialSource.Resolve — host-named no-credential error.
- `internal/credential/native/gitcredential.go:78` gitUnavailable(host, err) — wraps host + sentinel.
- `internal/credential/native/host.go:31` ExecRunner.Invoke — appendNonInteractiveEnv on the child.
- `internal/credential/native/host.go:48` appendNonInteractiveEnv — GIT_TERMINAL_PROMPT=0 + GIT/SSH_ASKPASS=/bin/false.
- `cmd/baha/app_inspect_remote.go:61` git clone — non-TTY stdin + GIT_TERMINAL_PROMPT=0.
- `cmd/baha/app_update.go:454` gitOutput — non-TTY stdin.
- `cmd/baha/app_update.go:514` gitIsAncestor — non-TTY stdin.

## Red-first witness (H-V26)

Test: TestGitCredentialFillFailsClosedNamesHost, TestGitCredentialFillIsNonInteractiveProvesTheFix (internal/credential/native/credfill_noninteractive_test.go).

Sick SHA 40cb28c758b0 — both FAIL (error does not name host; no host-named sentinel):

```
=== TestGitCredentialFillFailsClosedNamesHost on sick 40cb28c75 ===
credfill_noninteractive_test.go:28: error must name the failing host, got "git: no native credential helper available for host: exit 1"
credfill_noninteractive_test.go:80: probe error must name the host, got "git: no native credential helper available for host: git: command failed with a non-zero exit status"
FAIL
```

Fix 0df7efc00 — both PASS.

Production hang proof (host, non-GitHub, read-only pty reproduction, not committed):

```
git credential fill with a real TTY stdin and NO GIT_TERMINAL_PROMPT=0 blocks indefinitely (pty repro rc=124 at 4s).
Production shape: git clone with cmd.Stdin=os.Stdin on a TTY with no native credential prompts on the password line.
```

No single sick commit — latent defect carried by whole develop 40cb28c75.

## CI intake (hosted, 5.3)

Shard: `PR · Go unit · packages` (ci.yml matrix shard `packages`; scripts/pr-unit-database.sh "packages"), runs every non-CLI Go package incl internal/credential/native.

Hosted CI run 44874605168 (pull_request, branch w0428-217credfill, run by this session — 4.6):

```
go-build      SUCCESS
go-vet        SUCCESS
internal/credential/native   ok   0.020s   (my package, my test runs here)
```

PR #1742 undrafted at 2026-11-21T06:14Z (GraphQL markPullRequestReadyForReview) so required checks run.

State (inherited red, not my change — recorded as STATE):
- packages-shard FAIL = `internal/logs` `TestPersesLokiDatasourceMultiSource*`. Verified FAIL identically on sick develop 40cb28c75 in a baseline worktree (identical loki_test.go failure) — NOT introduced by this candidate.
- cli-0..3 FAIL = inherited `cmd/baha` class (content #1615), pre-existing on develop.

## repo-rule compliance

- Write-set exactly the 5 files above; no tabu file touched; no .github/** (Owner scope).
- No subagents (AGENTS 4.8). No containers/networks/volumes started (native tests only, named form).
- Branch provenance: `git merge-base --is-ancestor 40cb28c758b0 HEAD` = true; `git log --oneline origin/develop..HEAD` lists ONLY 0df7efc00; `git diff origin/develop..HEAD --name-only` = the 5 write-set files.
- PR delivery: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1742/head` = 0df7efc00bb3cfd784c988613a9ec5f8fb6215b4.
- Evidence lives only in baseharbor-plan (this dossier); no evidence written into the product repo.

## cleanliness

No container/compose/volume started this shift (Go native tests only, named `-run`/`-skip` form).

Before: `docker ps -a` — ambient stack `bh-docker-dev-shared-*` absent (coordinator nudge: gone since ~03:0xZ); nothing of this lane's name present.
After: this lane started NOTHING; baseline worktree /tmp/baseline-logs removed.

`cleanliness:` no container/network/volume/state directory created by w0428-217credfill; scratch limited to the baseharbor-plan evidence path; worktree workers/0428-217credfill-wt at candidate 0df7efc00, porcelain clean.

## origin/main witness (evidence delivery)

```
$ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle4-2026-11-21/git-credential-fill
```

## END

END_DONE w0428-217credfill: 0428-217 fix complete — git credential fill now fails closed non-interactively with a host-named no-credential error. Write-set 5 files (3 outside cmd/baha/, all allowed; app_update.go scope expansion flagged for coordinator). Red-first witness FAIL on sick 40cb28c75 / PASS on fix. Candidate 0df7efc00, PR #1742 base develop. Hosted CI run 44874605168: go-build + go-vet SUCCESS, internal/credential/native = ok in CI; packages-shard FAIL (internal/logs) and cli-* FAIL are inherited pre-existing on sick develop, recorded as STATE.
