# 0427-134 r3 — PR #1457 execution (round 3)

## Status

ACTIVE — executing the fix recipe from `act-1457-review.md` (r2 review; points 2-4, OWNERSHIP/ANCESTRY, CLEANUP-WITNESS already PASS).

## PLAN

- Read mission + `act-1457-review.md` fully; verify live refs
- Create worktree, cut branch from candidate, confirm ancestry + single commit
- (1) Fix `cmd/baha/operator_auth.go`: capture `--no-browser` into `TrustOptions.NoBrowser` and pass to `Login`; keep env alias
- (2) `internal/operatorauth`: combine the CA-discovery + headless PKCE fixtures into one combined production-path `Login` test over managed-CA-only TLS; fixed callback-port case; flag>env>default
- (3) Regenerate `docs/cli/command-index.md` (+ DE) from command tree; add `--no-browser` CLI regression; run full suites + docs audit
- (4) Push, watch required CI to terminal, ls-remote, drift-merge develop, publish evidence

## Reality witnesses

- `git ls-remote origin refs/heads/develop refs/heads/wip/0427-134-ca-pkce-integrate` -> `07ae6c3e91b081a189266ca4b162ba705d4aa78f refs/heads/develop` and `09030b370c607a818a77cc128322c7b06fffd4f7 refs/heads/wip/0427-134-ca-pkce-integrate`
- `git ls-remote origin refs/heads/main` -> `988c35a28d0cdd4ab352040f133fc37cc2217631 refs/heads/main`
- PR #1457 head `09030b370c607a818a77cc128322c7b06fffd4f7`, base `develop`, OPEN, MERGEABLE
- `git merge-base --is-ancestor 07ae6c3e91b081a189266ca4b162ba705d4aa78f 09030b370c607a818a77cc128322c7b06fffd4f7` -> exit 0 (develop is ancestor of candidate)
- Candidate-only log: single commit `09030b37 wip(ca-pkce): ...`
- Branch cut from `09030b370c607a818a77cc128322c7b06fffd4f7` (candidate head)
- Hosted run `42455848388` -> conclusion failure on exact head `09030b37` (`go-unit-tests` failed on `human_documentation_test.go:101` command-index.md drift)
- develop moved during the round: `07ae6c3e` -> `48d6f10a` (commits 1452, 1454, 1456, 1461, 1462). Merged origin/develop into 134-r3-ca-pkce (drift-merge, recipe point 4); merge commit clean, no conflicts; command-index login row still carries `[--ca FILE] [--auth-code-file FILE] [--no-browser]`; TestHumanCommandIndexTracksExactCommandMetadata passes on the merged tree
- My branch's only delta vs the candidate head is the r3 fix (8 files, +440/-18)

## CI witness (run 42467172096, head 83d175f5)

REQUIRED check that CI was red on (recipe point 3) is now GREEN:
- `PR · Validation · go-unit-tests: completed/success` (was `failure` on 09030b37 run 42455848388)
- `PR · Validation · go-build: completed/success`
- `PR · Validation · go-vet: completed/success`
- `PR · Validation · documentation-audit: completed/success`
- `PR · Validation · mkdocs-en-strict: completed/success`
- `PR · Validation · mkdocs-de-strict: completed/success`
- `PR · Validation · cli-gofmt: completed/success`
- `PR · Validation · wizard-registration-tests: completed/success`
- `PR · Validation · pages-candidate-build: completed/success`

REST is a merge-policy gate, NOT a code defect. `PR Selected Checks` failed only on its policy
step `Require selected native acceptance before merge` — a gate on the four native runtime
gates that need an isolated verified runtime, never a GitHub-hosted shared runner:

- `PR · Native destroy retry · docker` → `##[error]Process completed with exit code 1.` (TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry, run against dockerd-rootless on a shared runner)
- `PR · Native destroy retry · podman` → `##[error]Process completed with exit code 1.`
- `PR · Native Keycloak/Core · docker` → `##[error]Process completed with exit code 1.`
- `PR · Native Keycloak/Core · podman` → `##[error]Process completed with exit code 1.`

STATE (Owner directive 2026-11-07): native gates are blocked on GitHub-hosted shared runners only
(the runners cannot run nested Docker/Podman rootless containers). Do not build/register/repair
runner infrastructure. Report and stop.

My fix touches only operator-auth / OIDC / command-index files — zero native/runtime/destroy/keycloak
files — so these four native failures are environment-blocked and independent of the r3 change.

## Repo-rule compliance

- Single integration candidate per chain; branch `134-r3-ca-pkce` cut from the named PR head, no second branch
- No subagents (4.8); every step run inside this session
- `.github/**` not edited, no workflow_dispatch/rerun
- Evidence file lives in baseharbor-plan only, not in the product repo
- Workspace fixed layout: worktree under `/tmp/opencode/134-r3-ca-pkce`

## END

END_DONE 0427-134-r3 — all three recipe deliverables executed and verified:
(1) `--no-browser` wired into TrustOptions.NoBrowser and passed to operatorauth.Login (CLI + internal);
(2) combined CA+PKCE production login path proven (TestLoginThroughManagedCAProvesCombinedProductionPath), fixed-callback-port + flag>env>default precedence added;
(3) command-index.md regenerated, go-unit-tests GREEN on head 83d175f5.

Native runtime gates (destroy retry + Keycloak/Core docker/podman) are STATE (environment-blocked
on shared runners, cannot run nested Docker/Podman; independent of the r3 change which touches
no native/runtime files). Not a code defect; reported and stopped per 2026-11-07 directive.

Candidate head: 83d175f54ea9aba432d192c87dfe6464e879e0df
CI run: 42467172096 (go-unit-tests success; native gates STATE)
