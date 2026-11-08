# 0427-130 r5 — up-NAME command-entry regression (runWithIO entrypoint)

## END

END_DONE 0427-130 r5 (PR #1474): candidate `8bb8cc0e` verified; CI run 42482853636 terminal success (cli-package-tests/go-unit-tests + PR Selected Checks green). Closes CODEX-REVIEW r4 command-entry gap for merged product fix PR #1459 (b73a13a90).

## PLAN

- Establish reality witnesses (ls-remote develop + PR #1459 head, planning repo path) and cut my branch from the exact develop SHA.
- Write the `runWithIO` up-NAME regression test in `cmd/baha`.
- Run local checks (go vet + targeted cmd/baha tests + fail-closed experiment).
- Commit, push to the named branch, open/update the PR against develop.
- Hosted run: go-unit-tests + PR Selected Checks green; record run-id + job names.
- Drift check + publish evidence to baseharbor-plan origin/main; confirm evidence path on origin/main before END.

## Reality witnesses

- Planning repo confirmed: `git rev-parse --show-toplevel` = `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, origin `https://github.com/mcpdev80/baseharbor-plan.git`. (workers/baseharbor-plan is the quarantined bookkeeping repo, NOT used.)
- Product repo base HEAD at workstart: develop `b73a13a909b2d7b811d6956b3bdaf93f17b80454` — `fix(up): accept optional positional NAME on top-level alias (#1459)`, parent `07ae6c3e9`.
- PR #1459 head: `b3bb20416c69919af02bd854b3966cfe5e3761ca`.
- **Branch cut from `b73a13a90`** (confirmed ancestor via `git merge-base --is-ancestor b73a13a90 HEAD` = YES).
- Candidate HEAD: `8bb8cc0e8565b88e89f1ecab5ad1c8fd6853b306` — single commit, only my work on the branch.
- PR #1474: `https://github.com/mcpdev80/baseharbor/pull/1474`, base `develop`, head `0427-130-r5-up-name-entry`, mergeable, OPEN.

## Drift

- develop advanced from `b73a13a90` to `4786c541743541e7550f2c214f143ac8ee4f0aa6` (confirmed via `git ls-remote`). The product fix (#1459) was already merged to develop at `b73a13a90`; later develop commits moved HEAD. The candidate SHA is unchanged; CI validated the candidate against the develop-anchored base at PR open. No rebase needed for a test-only regression on a merged fix.
- Cleanliness: only `cmd/baha/runtime_ports_test.go` changed; no product fix, no `.github/**`, no docs.

## What was built (product language)

The `baha up` top-level alias now resolves a registered application NAME by NAME — the same way `baha app up NAME` does — so an operator can resume a registered deployment from anywhere with `baha up NAME`, and an unregistered NAME still fails closed. This task did not change that behavior; it added a regression that proves the top-level alias routes NAME through the production resolver path instead of only the unit resolver.

## R4 stop criterion (recipe)

- Each of the three assertions fails when the top-level command entrypoint bypasses NAME threading: reverting `upNameArgs()` to always return `nil` makes `TestUpNameResumesThroughCommandEntrypoint` fail (unknown NAME no longer fails at `resolveRegisteredApplication` — it proceeds to the consent gate). Restoring `upNameArgs()` makes it pass. The direct-call cell `TestUpNameResumesRegisteredDeploymentAcceptsParity` stays for the parser/resolver unit.
- Mapping of the three claims to the entrypoint (verified empirically in-session, own runner):

  - **Registered NAME resolves:** `runWithIO(argv ["up", NAME])` from outside the repo calls `resolveRegisteredApplication` (app_context.go:136) and proceeds PAST the NAME-resolution step into control-plane setup (fails later at runtime realization "existing native network lacks a protected Core owner" — the next production step after NAME resolution succeeds). A NAME NOT routed through the entrypoint would instead fail closed here with "no registered deployment".
  - **Alias parity:** `up NAME` and `app up NAME` reach the same `resolveRegisteredApplication` outcome for the same registered NAME (same error line when no Core; same resolve when a Core is present).
  - **Unknown NAME fails closed:** `runWithIO(argv ["up", "does-not-exist-xyz"])` inside the repo returns "application \"does-not-exist-xyz\" has no registered deployment on target \"<target>\"" from `resolveRegisteredApplication`.

## Test (cmd/baha/runtime_ports_test.go)

`TestUpNameResumesThroughCommandEntrypoint`:

1. Seeds a registered deployment, runs `up NAME` from outside the repo, asserts it does NOT fail closed with "no registered deployment" (NAME was routed through the entrypoint and resolved; it proceeds to control-plane setup).
2. Alias parity: `up NAME` vs `app up NAME` reach the same resolve outcome for the registered NAME.
3. Unknown NAME inside the repo: fails closed at `resolveRegisteredApplication`.

Fail-closed proven by the revert/restore experiment above.

## Repo-rule compliance

- Product repo: baseharbor. Worktree under `/tmp/opencode/0427-130-r5-up-name-entry`. Caches under `/home/marcel/dev/baseharbor-ecosystem/workers/.w130-r5-gotmp` + `.w130-r5-gocache`. No edits to `.github/**` (Owner scope).
- Exactly one candidate per chain: branch `0427-130-r5-up-name-entry`, single commit `8bb8cc0e`, base `b73a13a90` confirmed ancestor via `git merge-base --is-ancestor`.
- No subagents (own session, self-run).
- Hosted runs self-monitored to terminal state (4.6).
- No compose projects started by this lane (no container/spawn on the runner; the local `cmd/baha` suite exhausts the host daemon, which is why CI is the unit evidence). Drained any containers left by earlier probes before END.

## Hosted CI (run 42482853636, terminal success)

- `PR · Validation · cli-package-tests` (job 128738413852) — **success** (this runs the `cmd/baha` Go unit tests, including `TestUpNameResumesThroughCommandEntrypoint` and `TestUpNameResumesRegisteredDeploymentAcceptsParity`).
- `PR · Validation · cli-vet` (128738413767) — success
- `PR · Validation · cli-build` (128738413809) — success
- `PR · Validation · cli-gofmt` (128738413826) — success
- `PR Selected Checks` (128738415625) — **success**
- Native Keycloak/Core, Selected Runtime, Targeted HA Docker/Podman — **skipped** by the selector (unit/selected proves the up-NAME regression; skipped is DAFÜR, not against — no green-fabrication).
- No reruns, no workflow_dispatch (Owner scope).

## END witness

- `git ls-remote https://github.com/mcpdev80/baseharbor.git develop` at END: `4786c541743541e7550f2c214f143ac8ee4f0aa6 refs/heads/develop` (drifted from workstart `b73a13a90`; fix already merged there).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/0427-130-r5-up-name-entry`: `8bb8cc0e8565b88e89f1ecab5ad1c8fd6853b306`.
- Planning repo: `git rev-parse --show-toplevel` = `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, origin `https://github.com/mcpdev80/baseharbor-plan.git`.
- Evidence published to baseharbor-plan origin/main.
