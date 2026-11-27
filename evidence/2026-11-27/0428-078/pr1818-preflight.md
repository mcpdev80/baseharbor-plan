# PR #1818 preflight disposition

Date: 2026-11-27. Read-only preflight; no product source, workflow, card, or task fields were edited, and no PR was merged.

## PLAN

- Read the live #1818 PR head, all runs on that exact SHA, its job results, current develop, #1812 state, and card 0428-078.
- Classify the latest #1818 run separately from the current chain blocker.
- Record the worker's forward-hop recipe and the existing card status.

## Candidate and last run

`mcpdev80/baseharbor#1818` is OPEN on branch `lane-0428-078-cf-fix`, head `20fc1cb7d49602dc7f8aa0004a7562a81311d78c`, base `develop`. The latest and only pull-request run on this exact head is run `45316544436` (`CI · PR #1818`), completed SUCCESS on 2026-11-24.

The run's `PR · Trusted Plan`, `PR Selected Checks`, `PR · Demo Pin`, and `PR · Exact Candidate` checks passed. The selected Docker data-capabilities, Docker identity, Docker observability, Podman data-capabilities, and Podman observability runtime gates all executed and passed. There is no failing Runtime Image job in this run; the relevant image-pin check `PR · Demo Pin` passed. Therefore the run itself is not a Trusted Plan or runtime-image failure. It is stale for present integration: the candidate is 4 commits ahead and 76 behind current develop, and GitHub reports `mergeStateStatus=BEHIND`.

The current serial-chain state is independently blocked: `mcpdev80/baseharbor#1812` is OPEN, head `6ab5310d17358bc0f4c86ef09bea476b82517e3e`, and GitHub reports `mergeStateStatus=BLOCKED`. The 0428-078 card's blocker explicitly sequences `#1812 -> #1819 -> #1820`, then a refreshed #1855 with exact-head Codex acceptance, before closing #1650/#1818. Thus #1818 is presently chain-blocked as well as behind; its old green run does not clear that chain or qualify its current integration state.

## Forward-hop recipe for the owning worker

At this observation, the product `develop` tip was `ea5218d72e263f21e79853b679af50074dab8c25`; #1818's merge base with develop was `3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd`. The owner must wait until the serial prerequisites permit #1818 to proceed. At that time, fetch `origin/develop` and record the exact live 40-character SHA immediately before transport; the observed SHA here is historical context, not a future base instruction.

Use the existing #1818 branch and merge that exact current develop tip forward with an ordinary merge commit. Do not rebase, cherry-pick, recut the branch, or force-push. Conflict risk is high: the branch is 76 commits behind, and its edits overlap the Perses dashboard-selection and Keycloak identity implementation areas that have continued to change. Review each conflict against current develop while preserving the accepted Keycloak provider-label queries and the latest dashboard registration/selection implementation; do not resolve by blindly taking either side.

After transport, obtain a fresh Hosted pull_request run on the final exact head. Require `PR · Trusted Plan` and `PR Selected Checks` SUCCESS, with the applicable dashboard Go tests and selected runtime gates actually executed and green. `PR · Demo Pin` must remain green if the source-pin check is selected. A skipped or old-head result does not qualify the new head. No local test result is evidence for this preflight.

## Card 0428-078 state

On Plan main `bddfd98fc0a22a126c357c2c7811711a2e26af1e`, `tasks/t-20261114-r28-perses-dashboard-identity.md` has `kanban_status: blocked` and `kanban_lane: blocked`. Its owner field is `w359-0428-288-1833requal`, not empty. The blocker records the serial prerequisite sequence and the prior #1855 failure; this preflight does not alter or clear it.

## Provenance

Planning repository remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`. Evidence base: `bddfd98fc0a22a126c357c2c7811711a2e26af1e` from `origin/main`. Executing lane: `w255-0428-251-demo170codex`. Commit identity: `w255-0428-251-demo170codex <w255-0428-251-demo170codex@baseharbor.local>`. Commit invocation: `git -c user.name="w255-0428-251-demo170codex" -c user.email="w255-0428-251-demo170codex@baseharbor.local" commit -m "evidence: preflight PR 1818 chain status"`. Identity gate: `git show -s --format=%an HEAD` must print exactly `w255-0428-251-demo170codex`.
