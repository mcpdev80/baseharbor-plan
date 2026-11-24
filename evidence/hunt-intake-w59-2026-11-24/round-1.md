# w59-0428-269-huntintake26 — bug-hunt H-V26 findings F1-F5 intake (planning-only)

Lane: `w59-0428-269-huntintake26`. Mission: `coordinator/missions/w59-0428-269-huntintake26.txt`.
Task: turn the H-V26 bug-hunt findings F1-F5 into baseharbor-plan cards. Planning-only: NO product-code,
NO `.github/**`, NO `scripts/**` edits, no product-repo commit/push/PR, no hosted run, no local product
test, no VM, no containers, no subagents.

## PLAN

1. Verify planning repo remote + fetch origin/main (real repo = `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, NOT `workers/baseharbor-plan`). — DONE, witness below.
2. Read the mission and the H-V26 dossier `evidence/r28-welle6-2026-11-24/bughunt-hv26-candidate-consent-gate/round-1.md` (origin/main) and pull every file:line witness. — DONE.
3. Re-measure each finding on the develop anchor 3ebfb90d in a read-only clone in this lane's own zone. — DONE, notes below.
4. Find the next free 0428-NNN and the carded 0428-189..194 / operatorauth predecessors for depends_on and cross-refs. — DONE (highest used = 0428-268; next free = 269).
5. F1: create the OWNER-scope card `produce baha-ci-operator-testonly in candidate artifact for pre-release runtime suite` and set 0428-249 blocked-behind it. — DONE (0428-269).
6. F2: cross-reference only — one body pointer in each consent card 0428-189..194, no new card. — DONE.
7. F3: create the bug card for the dead trusted-local fail-open seam. — DONE (0428-270).
8. F4: create the bug card for version-only broker build identity. — DONE (0428-271).
9. F5: create the OWNER-scope card for the missing native runtime gate on the authority seam. — DONE (0428-272).
10. `python3 scripts/plan.py render && python3 scripts/plan.py check` → 0 errors. — DONE.
11. Commit the specific files only, push to planning main. — DONE (`436a0a650..a1f1ff16d`).
12. Persist this evidence to baseharbor-plan origin/main and verify with ls-tree before END. — DONE (witness below).

## Intake result (F -> card)

- F1 -> NEW 0428-269 `t-20261124-r28-release-candidate-testonly-binary` (type task, priority high, owner "", planned, depends_on none, repos [mcpdev80/baseharbor]). Owner scope: the fix lives in `.github/workflows/pre-release.yml`.
  Additionally 0428-249 `t-20261122-runtime-image-registry-artifact-unknown` now declares `depends_on: [t-20261124-r28-release-candidate-testonly-binary]`, i.e. it is blocked-behind 0428-269, as the mission's F1 action required (render moved its derived state from "waiting" to the correct "blocked").
- F2 -> NO new card (by-design). Cross-reference only: one `## Cross-reference (bughunt-hv26 F2, by-design, no new card)` body section appended to each existing consent card 0428-189, 190, 191, 192, 193, 194 (all six `t-20261120-r28-*` registry/consent cards). Frontmatter of those cards untouched, so no status change.
- F3 -> NEW 0428-270 `t-20261124-r28-trusted-local-failopen-seam-dead` (type bug, planned, owner "", depends_on `t-20261120-trusted-local-operation-grant` = 0428-188, the operatorauth/trusted-local card the mission asked for; file:line `internal/operatorauth/authorization.go:276-282` with the `config.go:89-91` cause; acceptance item 2 is the one fail-open-closed regression).
- F4 -> NEW 0428-271 `t-20261124-r28-broker-build-identity-commit` (type bug, planned, owner "", depends_on none; file:line `cmd/baha/app_broker.go:652-672`, discard sites `:668-669`, call site `:641` via `verifyRuntimeBrokerRunning` `:192`).
- F5 -> NEW 0428-272 `t-20261124-r28-runtime-authority-gate-routing` (type task, planned, owner: "" OWNER-scope, depends_on none; file:line `scripts/pr-gate-plan.py:1643-1647` with `OPERATORAUTH_POLICY_FILES` at `:85-92`).

## Finding verification on develop 3ebfb90d (read-only clone in this lane's zone)

Clone: `/tmp/opencode/w59-0428-269-huntintake26-wt/bh` (blobless, checked out at exactly `3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd`). Remote: `https://github.com/mcpdev80/baseharbor.git`. `git ls-remote ... refs/heads/develop` → `3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd`, so the develop anchor is still current and equals the dossier's anchor.

- F1 REAL. `grep -c 'baha-ci-operator-testonly' .github/workflows/pre-release.yml` → **0**. `pre-release.yml:491-501` builds only `-o "$RUNNER_TEMP/pre-release-candidate/baha" ./cmd/baha` and uploads that directory as `pre-release-source-candidate`. `pre-release-runtime-suite.yml:315-318` under `set -euo pipefail` does `testonly="$RUNNER_TEMP/pre-release-candidate/baha-ci-operator-testonly"`, `test -s "$testonly"`, `chmod 0755`, `"$testonly" version | grep -F "$CANDIDATE_SHA"`. The release file dispatches `candidate_artifact: pre-release-runtime-candidate` at lines 716, 745, 794, 823 (and `pre-release-source-candidate` at 687). The CI path builds both binaries in `pr_candidate` (`ci.yml:1145-1146`, with the `version | grep -F "$GITHUB_SHA"` proofs at `:1147-1148`). Carded as 0428-269, no duplicate product card created per mission.
- F2 REAL and by-design, no card. The repository-source carve-out is `cmd/baha/deployment_record.go:520-521` (`record.Source.Kind == "repository" && state == "applying"`) with the fail-closed leaf at `:528-573`; consent is recomputed and constant-time compared in `cmd/baha/app_candidate_consent.go:190-197`. Cross-referenced into 0428-189..194 only.
- F3 REAL. `internal/operatorauth/config.go:89-91` → `ManagedEnvironmentWithPolicy(environment, false)`; `config.go:108-110` → `return !trustedLocal`; `config.go:98-100` → `TrustedLocalForEnvironment` returns `false`. New check: outside tests the ONLY caller of `ManagedEnvironmentWithPolicy` is `ManagedEnvironment` itself, so `!ManagedEnvironment(...)` at `authorization.go:276` is always false and the `trusted-local` allow at `authorization.go:277-279` is dead for production callers. Live deny path confirmed at `authorization.go:284-286` (`operator_authentication_required`); the live local path is the `local-runtime` grant at `authorization.go:270-275`. NOTE (dossier slip, harmless): the dossier cites `authorization.go:279` for the branch; the condition is at line **276** and the allow body at 277-279. The card cites both, so the seam is findable either way.
- F4 REAL. `cmd/baha/app_broker.go:652-672` ends with `_ = expectedCommit` / `_ = actualCommit` at `:668-669` under the "build provenance, not a runtime compatibility contract" comment; called with `ready.Version, ready.Commit` at `:641`.
- F5 REAL. `scripts/pr-gate-plan.py:1643-1647` (the `elif path in OPERATORAUTH_POLICY_FILES:` branch) does `area = 'operatorauth-explicit-policy'` and `require(AUTHORITY_PACKAGE_CHECKS + CODE_CHECKS)` with no `atomic/...` gate; the set that routes here is declared at `scripts/pr-gate-plan.py:85-92` and includes `internal/operatorauth/local_runtime.go`. The neighbouring `authority-package` branch (`:1640-1642`) likewise stays package-level, so no escalation exists on this path.

## Dedup and dependency choices

- operatorauth/trusted-local card search (`grep -l 'trusted-local|trustedLocal|local.workload' tasks`): the closest is **0428-188** `t-20261120-trusted-local-operation-grant` (type task, closed/accepted, baseharbor#1717, "Bind local operation grants"), which is the card that removed the dev-to-trusted-local auto-admit. Per mission ("depends_on the operatorauth/trusted-local card if one exists else none") 0428-270 declares it. Other candidates (0428-209 native-cell-operator-seam, 0428-243, 0428-231, 0428-250) are all closed and own different surfaces; 0428-247 is a `wait` target-create auth card. No existing planned card covers F1/F3/F4/F5.
- 0428-189..194 are the consent-flaeche cards the dossier excludes from F2/F3; they stay `planned` with their original `depends_on: [t-20261114-r28-perses-dashboard-identity]` — only a body pointer was added (mission rule: cross-references edit the body, never create cards).

## Publication hazard found while working (documented, not fixed)

The coordinator's `plan-sync.sh` runs from cron every minute (`crontab -l`: `* * * * * .../watch-keepalive.sh`, `codex-ear.sh`; every 2 min `coord-tick-once.sh`) and it **stashes all untracked and modified files in the shared baseharbor-plan checkout and hard-resets it to origin/main**. It wiped this lane's three already-written card files between my write and my first `plan.py check` (evidence: `git stash list` shows `stash@{0}: On main: plan-sync:auto:20261124T032952Z:vor-sync-210f38d5d` and nine older entries; `git reflog` shows `reset: moving to origin/main` twice inside the same minute). This is the same hazard the sibling intake lane w57 recorded in `evidence/hunt-intake-w57-2026-11-24/round-1.md` ("Ops hazard ... plan-sync.sh ... This lane hit it twice"). Nothing was lost here because the files were re-created in this lane's own zone (`/tmp/opencode/w59-0428-269-huntintake26-wt`) and published atomically from there: copy in → render → check → `git add <specific files>` → commit → push, in one script, with the push retried against a re-fetched origin/main. Recommendation for the coordinator: serialize `plan-sync.sh` with publishing lanes, skip the stash when the dirty files belong to a running publishing lane, or give lanes a private plan checkout to publish from.

## Remote witnesses

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` (verified BEFORE the first evidence commit, and the path is the real planning repo, not `workers/baseharbor-plan`):

    origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

- Card commit: `git -C baseharbor-plan push origin HEAD:main` → `436a0a650..a1f1ff16d`; base attestation `git merge-base --is-ancestor origin/main HEAD` passes (one commit directly on top of `436a0a6500748ebc3a2f1f46201677ac9a14cc2f`, and `git log --oneline origin/main..HEAD` listed only this lane's own commit before the push).
- Delivery proof (`git ls-remote origin refs/heads/main` after that push): `a1f1ff16dda3e76c43970644897ac9f42cdc2e0c refs/heads/main`.

Render/check at publish time: `python3 scripts/plan.py render && python3 scripts/plan.py check` → `711 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings` (the 10 warnings are pre-existing, unrelated `t-202611*-r27-*` dependency warnings).

## repo-rule compliance

- baseharbor-plan AGENTS/WORKFLOW: cards published to `main` directly; every new card is `owner: ""`, `kanban_status: planned`, `resolution: ""`; nothing marked accepted/qualified; no card closed. `render` + `check` run before the push with 0 errors.
- Write-set respected: only `tasks/*.md` plus the derived views `views/*`, `roadmap/cards.md`, `releases/v0.4.28.md` that `plan.py render` owns, plus this evidence file. No product repo, no `.github/**`, no `scripts/**` in a product repo.
- No local product test, no build, no `go test`, no VM, no container, no compose project, no hosted run, no PR (planning-only mission).
- No subagents (AGENTS 4.8): every step ran in this session.
- Evidence lives only in baseharbor-plan (`evidence/hunt-intake-w59-2026-11-24/round-1.md`), never in a product repo.

## cleanliness

This lane started no container, network, volume, compose project or state directory, on this host or any SSH host: `docker ps -a` / `podman ps -a` were not needed because nothing was created (the dossier's ambient `baseharbor-pre-release-registry` podman container was not touched). Lane-owned artifacts, all removed at END:
`/tmp/opencode/w59-0428-269-huntintake26-wt/bh` (read-only blobless clone) and its `publish.sh`.
cleanliness: besenrein — nothing started or stopped by this lane; only planning files were written.

## END w59-0428-269-huntintake26 DONE

- F1 -> 0428-269 (new Owner-scope task card, `t-20261124-r28-release-candidate-testonly-binary`) + 0428-249 now `depends_on` it (blocked-behind).
- F2 -> no card; cross-reference body section added to 0428-189, 190, 191, 192, 193, 194.
- F3 -> 0428-270 (new bug card, `t-20261124-r28-trusted-local-failopen-seam-dead`, depends_on 0428-188).
- F4 -> 0428-271 (new bug card, `t-20261124-r28-broker-build-identity-commit`).
- F5 -> 0428-272 (new Owner-scope task card, `t-20261124-r28-runtime-authority-gate-routing`).
- Planning candidate SHA: `a1f1ff16dda3e76c43970644897ac9f42cdc2e0c` on baseharbor-plan main (no product candidate exists: planning-only mission).
- Checks: 4 new cards, 1 blocked-behind edge, 6 cross-reference sections; render+check 0 errors; no product/CI/`.github`/`scripts` file edited.

## Publication witness (appended after the evidence push)

`git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep hunt-intake-w59`:

    tasks/t-20261124-r28-broker-build-identity-commit.md
    tasks/t-20261124-r28-release-candidate-testonly-binary.md
    tasks/t-20261124-r28-runtime-authority-gate-routing.md
    tasks/t-20261124-r28-trusted-local-failopen-seam-dead.md

`git -C baseharbor-plan ls-remote origin refs/heads/main`:
    a1f1ff16dda3e76c43970644897ac9f42cdc2e0c	refs/heads/main
## Witness correction (same lane, appended after the first publication)

The first publication witness in this file was taken before a further `plan-sync` cycle, so it showed
`origin/main` at the card commit `a1f1ff16d` and the evidence path not yet listed. Authoritative state
at END, re-measured with a fresh fetch (this file is committed in `5852bcb34`):

    git -C baseharbor-plan ls-remote origin refs/heads/main
    5852bcb34dc71a394650be4bacdea8517ed5adb7  refs/heads/main

    git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep hunt-intake-w59
    evidence/hunt-intake-w59-2026-11-24/round-1.md

`git merge-base --is-ancestor 5852bcb34dc71a394650be4bacdea8517ed5adb7 origin/main` → yes, so the card
commit `a1f1ff16d` is an ancestor of `origin/main` and both commits are live. Card files verified
individually on `origin/main` with `git cat-file -e origin/main:tasks/<file>`: 0428-269, 0428-270,
0428-271, 0428-272 all present; 0428-249 `depends_on: [t-20261124-r28-release-candidate-testonly-binary]`
present; the six consent cards 0428-189..194 carry the F2 cross-reference section.
`python3 scripts/plan.py check` on the fetched tree: `711 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings`.

Extra plan-sync observation: `plan-sync.sh` also hard-resets the shared checkout *after* a lane pushes, so a
`render`-touched derived file that belongs to another card (here `tasks/t-20261120-trusted-local-operation-grant.md`,
whose links block was stale) gets picked up into the lane's next commit unless it is explicitly excluded. This
lane excluded it: `5852bcb34` contains ONLY this evidence file (`1 file changed, 97 insertions(+)`).

## cleanliness witness (this host, END)

    docker ps -a   -> (no rows)
    podman ps -a   -> a14be1e261a4 baseharbor-pre-release-registry  registry:2.8.3  Exited (0)

That registry container is ambient (also listed in the H-V26 dossier, same id) and is NOT this lane's; it was
left untouched. This lane created no container, network, volume or compose project.
## Final publication witness (second-to-last action, fresh fetch)

    git -C baseharbor-plan ls-remote origin refs/heads/main
    ce1d061c012a5eadc9c62cc5fa3e5cb55b06c2a0  refs/heads/main

    git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep -E 'hunt-intake-w59|t-20261124-r28-(release-candidate|trusted-local|broker-build|runtime-authority)'
    evidence/hunt-intake-w59-2026-11-24/round-1.md
    tasks/t-20261124-r28-broker-build-identity-commit.md
    tasks/t-20261124-r28-release-candidate-testonly-binary.md
    tasks/t-20261124-r28-runtime-authority-gate-routing.md
    tasks/t-20261124-r28-trusted-local-failopen-seam-dead.md

    git merge-base --is-ancestor ce1d061c012a5eadc9c62cc5fa3e5cb55b06c2a0 origin/main
    yes: the evidence commit ce1d061c0 is an ancestor of origin/main

END_DONE w59-0428-269-huntintake26: planning candidate ce1d061c012a5eadc9c62cc5fa3e5cb55b06c2a0 (cards in a1f1ff16d) on baseharbor-plan main; F1->0428-269 (+0428-249 blocked-behind), F2->cross-refs in 0428-189..194, F3->0428-270, F4->0428-271, F5->0428-272; render/check 0 errors; no product/CI/scripts file touched.
