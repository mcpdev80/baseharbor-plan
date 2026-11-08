# 0427-130 r5 — runWithIO up-NAME command-entry regression

- Task: 0427-130 r5. Product fix PR #1459 is merged to develop (HEAD `b73a13a90`).
- Goal: close the R4 review gap — add a `runWithIO` top-level command-entry regression for `baha up NAME` so the three claims (registered-name resolution, alias parity, unknown-name fail-closed) run through argv `["up", NAME]`, not through a direct `resolveRegisteredApplication` call.
- Stop criterion (from recipe): each of the three assertions fails when the entrypoint is bypassed; hosted `go-unit-tests` + `PR Selected Checks` terminal green on the exact head.

## PLAN

- Establish reality witnesses (ls-remote develop + PR #1459 head, planning repo path) and cut my branch from the exact develop SHA.
- Write the `runWithIO` up-NAME regression test in `cmd/baha`.
- Run local checks (go test ./cmd/baha/..., go vet, go build).
- Commit, push to the named branch, open/update the PR against develop.
- Hosted run: go-unit-tests + PR Selected Checks green; record run-id + job names in round-5.md.
- Drift check + publish evidence to baseharbor-plan origin/main; tear down any compose project; post END.

## Reality witnesses

- Planning repo confirmed: `git rev-parse --show-toplevel` = `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, origin `https://github.com/mcpdev80/baseharbor-plan.git`. (workers/baseharbor-plan is the quarantined bookkeeping repo, NOT used.)
- develop HEAD: `b73a13a909b2d7b811d6956b3bdaf93f17b80454` — `fix(up): accept optional positional NAME on top-level alias (#1459)`, parent `07ae6c3e9`.
- PR #1459 head: `b3bb20416c69919af02bd854b3966cfe5e3761ca`.

## Repo-rule compliance

- Product repo: baseharbor. Worktree under /tmp/opencode, caches under /tmp/opencode. No edits to .github/** (Owner scope). One candidate per chain on the mission branch. No subagents (own session). Hosted runs self-monitored. Evidence only in baseharbor-plan.
