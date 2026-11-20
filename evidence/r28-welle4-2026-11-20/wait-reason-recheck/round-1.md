# w212-0428-202-waitrecheck — wait-reason recheck dossier (round 1)

Lane: w212-0428-202-waitrecheck. Mission: /var/tmp/note-212-waitrecheck.txt (read-only planning help).
No product changes, no PR edits, no card writes, no reruns, no workflow_dispatch, no subagents, no posts to third sessions.

## Purpose

PR #1732 (card 0428-202) turned `PR · Go unit · packages` SUCCESS at its exact head (bddb27e6251e,
base develop 40cb28c758b0; job 136574098983, run 44818799733). That removes one half of the field gate
blocking the wait column. This dossier rechecks every `kanban_status: wait` card against that truth:
(A) identity, (B) literal wait_reason and which gate it names (198 / 202 / BOTH / OTHER),
(C) the reason true AFTER this tick (only-198 / unchanged / no-longer-a-gate-but-X with proof),
(D) whether the card's PR packages cell could already be green at the same head because #1732 fixes the
cause — measured by check-runs (read-only, §5.4) plus the base-drift trap control (symbol test).

## Base attestation

- baseharbor develop tip (measured): `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
  → 40cb28c758b02960356434b630086a341ebe1738.
- Symbol test at that tip: `git show 40cb28c758b0:internal/logs/loki_test.go | grep -c 'client-cert.pem'` → **0**.
  The fixture fix is NOT in develop; it lives only on PR #1732's head and bases containing it.
- baseharbor-plan main (board): ls-remote → 9ec80af890920d8c188bd172a7c239d31eeb6a57 (at mission start),
  then e81b2075b398a0b05da19ff8cd4c2b0f996516ce (final pull; also `git ls-remote … refs/heads/main` witness).
  Both heads yield the same wait set of **35 cards** (`git grep -l -a "^kanban_status: wait" origin/main -- tasks/`;
  mission said "rund 33" — 35 is exact at this tick).
- REMOTE GUARD: in the shared baseharbor checkout all three remotes (origin, lane-origin, upstream) resolve to
  https://github.com/mcpdev80/baseharbor.git (measured by `git remote -v`); all reads went through github URLs.
  workers/baseharbor was not used as evidence. Card texts read only from origin/main objects.

## Method

1. Wait set: `git -C baseharbor-plan grep -l -a "^kanban_status: wait" origin/main -- tasks/` (35 files);
   card_number, kanban_title and wait_reason extracted per file from the origin/main blob.
2. PR heads: `gh api repos/mcpdev80/baseharbor/pulls/<n>` (head sha, state, draft, merged, base sha);
   cross-checked with `git fetch --refs origin refs/pull/<n>/head` then `git rev-parse FETCH_HEAD`
   for the heads lacking a lane-origin ref.
3. Cell truth at each head: `gh api repos/mcpdev80/baseharbor/commits/<sha>/check-runs?per_page=100`,
   selecting `PR · Go unit · cli-0..3`, `PR · Go unit · packages`, `PR · Draft Go · packages`,
   `PR Selected Checks`, `PR · Selected Runtime*`. Read-only; no rerun, no dispatch.
4. Base-drift trap control: symbol test `client-cert.pem` at each head; and at each PR's
   potential_merge_commit / merge_commit_sha to see whether #1732's fix is ALREADY in that head's CI base.
5. Required-check question: `repos/mcpdev80/baseharbor/branches/develop/protection` (404, not protected),
   `rulesets` (single ruleset, enforcement: disabled), `only_required_for_action` field (null),
   `check_suites` (app: GitHub Actions).

## Table A–D (all 35 wait cards)

Legend gate: which field gate the wait_reason names. C: corrected verdict this tick.
D: "was-202-now-198" = packages cell failing at head from the loki fixture (fix only via #1732 merge);
"packages-green" = measured green; "0-runs" = zero check-runs at head; "-" = no PR.

| # | A card · file (tasks/) · title | B gate named | C verdict | D packages at head |
|---|---|---|---|---|
| 1 | 0427-007 · t-20261017-release-0-4-27-publish · promote the validated | OTHER | unchanged (owner: #1574 CONFLICTING) | - |
| 2 | 0427-008 · t-20261017-release-0-4-27-qualify · complete required candidate | OTHER | unchanged (candidate not frozen, run 43633496362 FAIL) | - |
| 3 | 0427-010 · t-20261017-release-0-4-27-verify · verify publication | OTHER | unchanged (owner: tag missing) | - |
| 4 | 0428-002 · t-20261017-release-0-4-28-cleanup · reconcile old PRs | OTHER | unchanged (chain waits on 0427-verify) | - |
| 5 | 0427-059 · t-20261018-r27-team-proof · prove two workstations share | OTHER | unchanged (approved; frost-bis) | - |
| 6 | 0427-169 · t-20261108-smoke-0427-operator-api-undocumented · operator API runbook | OTHER | unchanged (approved; frost-bis, 0.4.28 window) | #1587 Draft cell success (merge-sya 0; no PR CI) |
| 7 | 0427-186 · t-20261109-r27-target-policy-presets · editable presets | OTHER | unchanged (approved; frost-bis) | #1588 merge-commit unfetchbar (no PR CI) |
| 8 | 0428-065 · t-20261114-r28-cli2-app-export · app export UX | OTHER | **no-gate-but: base ineligible** — #1625 draft, PR-base 010db47dae0e is a lane-internal ref with 0 check-runs; reason itself says "kein base-allowlist, kein exact-head run" | #1625 0-runs |
| 9 | 0428-063 · t-20261114-r28-cli2-app-interact · guide app logs | OTHER | unchanged (red at stack-base ca930ce6, waits content of #1615; head 4cbf92960cb5 has 0 check-runs) | #1623 0-runs |
| 10 | 0428-062 · t-20261114-r28-cli2-app-status · unify app status | OTHER | unchanged (draft on develop, content of CLI2 contract cards); packages actually GREEN | #1614 Draft-Go packages=success (merge-sya 0) |
| 11 | 0428-072 · t-20261114-r28-cli2-coordination · coordinate five workers | OTHER | unchanged (coordination card, no own work) | - |
| 12 | 0428-055 · t-20261114-r28-cli2-env-delete · env deletion lifecycle | OTHER | **no-gate-but: merge conflict + 0-runs** — #1627 draft, mergeable=DIRTY vs current develop, 0 check-runs at head; waits on 0428-053 + env registry accepted | #1627 0-runs |
| 13 | 0428-056 · t-20261114-r28-cli2-org-env · organization env | OTHER | unchanged (content of #1594/0428-053); its PR #1596 cells are green | #1596 Draft-Go packages+cli all success (merge-sya 0; Ready cells skipped) |
| 14 | 0428-067 · t-20261114-r28-cli2-wizard-platform · platform wizards | OTHER | **no-gate-but: 0-runs + prerequisite unaccepted** — #1620 draft, 0 check-runs; waits 0428-053 | #1620 0-runs |
| 15 | 0428-073 · t-20261114-r28-perses-alerts · alert rules | OTHER | unchanged (owner decision: real Prometheus evaluator; waits 0428-083) — note: #1704 cells all green | #1704 packages=success |
| 16 | 0428-074 · t-20261114-r28-perses-contact-routing · notification routing | OTHER | unchanged (owner decision opt-in; waits 0428-073) | - |
| 17 | 0428-076 · t-20261114-r28-perses-dashboard-databases · database dashboards | BOTH | only-198 — #1597 head 90063f6ec66c: cli-0..3=failure (198), packages=failure with symbol 0 at head and potential-merge clientcert=0 → content waits #1732 merge; gofmt/vet/build green | #1597 packages=failure (both cell families) |
| 18 | 0428-078 · t-20261114-r28-perses-dashboard-identity · identity dashboard | ANDERE | unchanged — #1650 head 9add5e8a2122: packages=success AND cli-0..3=success, Selected Checks=success; wait is the r8 REQUEST CHANGES, not a gate | #1650 packages=success |
| 19 | 0428-083 · t-20261114-r28-perses-datasources · connect Prometheus datasources | BOTH | unchanged (own cells green per reason; waits field gate + merge order #1724 first) — measured: #1684 packages=failure @b71c6da27e8b, potential-merge clientcert=0 | #1684 packages=failure |
| 20 | 0428-085 · t-20261114-r28-perses-log-trace-dash · log/trace views | BOTH | only-198 — card cites #1645 (head 4d73aa97808d): cli-0..3=failure, packages=failure, symbol 0 at head and potential-merge 0 → content waits #1732 merge | #1645 packages=failure |
| 21 | 0427-189 · t-20261115-bughunt-d28-state-dir-target · bf01 state-dir | OTHER | unchanged (approved; cherry-pick in TRIAGE-QUEUE; frost-bis) | #1585 0-runs (draft) |
| 22 | 0428-149 · t-20261119-orgconfig-error-redaction · orgconfig redaction | ANDERE | unchanged — #1596 head c90c3b89007e: Draft-Go packages+cli success; Ready selected checks skipped; local commit f113baf not integrated; waits parent PR owner | #1596 Draft packages=success |
| 23 | 0428-143 · t-20261119-r28-app-source-verification-none-ignored · verification=none | BOTH | only-198 — #1729 head 809a8196e1cf: cli-0..3+Selected Checks=failure (198); packages=failure due 202, potential-merge clientcert=0 → needs #1732 merge | #1729 packages=failure |
| 24 | 0428-142 · t-20261119-r28-perses-status-backend-witness · backend witness | ANDERE | unchanged — #1702 head 6740299f91c0: ALL cells green (packages, cli-0..3, Selected Checks = success); waits a worker seat + Codex corrections + fresh exact-head run | #1702 packages=success |
| 25 | 0428-150 · t-20261119-r28-window-integrity-verify · window integrity | OTHER | unchanged (needs merged cards) | - |
| 26 | 0428-200 · t-20261120-deployment-version-mismatch-masked · version mismatch | BOTH | only-198 — #1728 head 6e3122344f87: cli-0..3=failure; packages=failure, potential-merge clientcert=0 → needs #1732 merge; gofmt/vet/build green | #1728 packages=failure |
| 27 | 0428-177 · t-20261120-perses-tmpfs-mountpoint · tmpfs mountpoint | BOTH | only-198 — #1724 head 408b18d2dc7b: cli-0..3=failure; packages=failure, potential-merge clientcert=0 → needs #1732 merge; own smoke cells success | #1724 packages=failure |
| 28 | 0428-178 · t-20261120-r28-cli2-context-precedence-evidence · context precedence | 198-variant | unchanged — #1718 head ce5aa9633630: cli-0..3=failure; packages cell ABSENT (never ran at head); waits #1615 (9dccd0ed6768, run 44817430166) | #1718 packages=none (0 Go-unit runs) |
| 29 | 0428-202 · t-20261120-r28-packages-shard-develop-regression · packages shard (own card) | 202→198 | unchanged (own card: packages green at own head; waits only 0428-198) | #1732 packages=success (measured) |
| 30 | 0428-179 · t-20261120-r28-shell-wrapper-tests-not-skippable · shell wrappers | 198-variant | unchanged — #1731 head f90b3f448caf: cli-0..3=failure, packages cell ABSENT at head; waits #1615 merge | #1731 packages=none (0 Go-unit runs) |
| 31 | 0428-176 · t-20261120-r28-stale-draft-pr-1665-closeout · restack or close | ANDERE | unchanged — #1665 head db27880c108a: 0 check-runs; overlap #1684 + 0428-177 prerequisite | #1665 0-runs |
| 32 | 0428-183 · t-20261120-r28-valkey-dashboard-unavailable-only · valkey dashboards | BOTH | needs BOTH MERGES — #1714 head 5159192dadee: cli-0..3+packages=failure; base 40cb… lacks #1732 (potential-merge clientcert=0) AND lacks 198's content; waits merge of #1732 AND #1726 then hop | #1714 packages=failure |
| 33 | 0428-201 · t-20261120-shared-backend-state-version-message · shared state version | BOTH | only-198 — #1725 head 9bf4a72f742b: cli-0..3=failure; packages=failure, potential-merge clientcert=0 → needs #1732 merge | #1725 packages=failure |
| 34 | 0428-203 · t-20261120-verif-none-stale-target · stale target none switch | BOTH | needs TWO merges — #1730 head c90a73ac8128: cli+packages=failure; stacked on #1729 lane (potential-merge clientcert=0) which itself waits 198 → merge chain #1726 + #1732 + #1729 then hop | #1730 packages=failure |
| 35 | 0428-199 · t-20261120-workload-port-flag-ignored-locally · workload-port | BOTH | only-198 — #1723 head 26755fc1edfb: cli-0..3=failure; packages=failure, potential-merge clientcert=0 → needs #1732 merge | #1723 packages=failure |

## Cards that now hang only on 198

Content-complete, own cells green except the 198-family (cli-0..3 + aggregate) and a packages cell whose
red is fixable ONLY by merging #1732 (their CI bases lack the fix — potential-merge symbol test = 0 everywhere):

- 0428-076 (#1597), 0428-085 (#1645), 0428-143 (#1729), 0428-200 (#1728), 0428-177 (#1724),
  0428-201 (#1725), 0428-199 (#1723) — after #1732 merges AND 0428-198/#1726 goes green in the field.
- 0428-202 (#1732) itself: its own packages cell is green; only 198's cli cell blocks it.
- 0428-183 (#1714) and 0428-203 (#1730) hang on the two MERGES (#1732 + #1726; 203 additionally its
  stacked base #1729), then a hop — not on a live gate beyond that.
- 0428-083 (#1684) keeps its extra merge-order trigger (merge #1724 first, then rebase) plus the field gate.

## Cards with another reason (not the 198/202 field gate)

- 0427-007 / 0427-010 / 0428-002 / 0427-008 / 0427-059 / 0427-169 / 0427-186 / 0427-189: release-world and
  frost-bis owner points (unchanged; release world is ChatGPT's per §2 — no 0.4.28 relevance for this tick).
- 0428-065, 0428-063, 0428-055, 0428-067, 0428-176: their PRs have **zero check-runs at head** (draft/
  lane-base); they wait on prerequisites (0428-057/#1615, 0428-053, #1684) and on becoming a base the CI
  trigger admits — not on the cli/packages field gate. 0428-055 additionally mergeable=DIRTY.
- 0428-062, 0428-073, 0428-074: prerequisite cards / owner decisions; 0428-073's #1704 is fully green.
- 0428-078: #1650 cells ALL green — pure review round (r8 REQUEST CHANGES), no gate.
- 0428-149 (#1596): green draft cells, waits integration of local commit f113baf57 + the draft-review route.
- 0428-142 (#1702): everything green at exact head, waits a worker seat and the Codex corrections run.
- 0428-150: needs several merged cards to be meaningful.
- 0428-178 (#1718), 0428-179 (#1731): cli-0..3 red, packages cell never ran at head (no Go-unit run in
  their suite) — they wait on 0428-057/#1615 merge (run 44817430166), the same rail 198 points at.

## "PR Selected Checks" — required or optional?

Measured at the current develop state:
- Branch protection on develop: `GET /repos/mcpdev80/baseharbor/branches/develop/protection` → **404 "Branch not
  protected"**. Rulesets: exactly one ("develop - integration branch"), **enforcement: disabled**.
- The check-run objects carry `only_required_for_action: null` (field only meaningful with protection/rulesets).
- The "PR Selected Checks" check-run belongs to a GitHub Actions check suite (app "GitHub Actions"), i.e. it
  is a job of the CI workflow itself (a planner/aggregate job), not an external required status context.

Verdict: with rulesets DISABLED there is **nothing technically required at all** right now — matching AGENTS
("Rulesets remain disabled… do not claim live Required Check enforcement"). Whether the aggregate binds as
required comes from the BASE plan's selection logic in `.github/workflows/ci.yml` (Owner scope), not from
protection. For review-dependency decisions: treat Selected Checks as a derived AGGREGATE signal that will
become a required check only once rulesets are re-enabled and verified. Cards whose review depends on it
(0428-085's note, 0428-083's note) should depend instead on the terminal per-cell results, which this
dossier measured per head.

## ## repo-rule compliance

- Read-only mission; no product work exists to build or fast-check. `bash scripts/ci-fast-check.sh` does not
  exist in the planning repo (this lane makes no product candidate, so no PR/CI gate applies here).
- No card, PR, branch or product file was changed by this lane. Before this evidence commit the worktree held
  ONLY the working-note revision of this dossier file (`git status --porcelain` showed one M line, now
  committed); it never held foreign or product changes.
- No rerun, no workflow_dispatch, no merge, no deploy, no post to third sessions (§4.6-style END goes only to
  the dispatching coordinator). No subagents (§4.8). No forbidden file was touched
  (internal/serviceaccess/**, internal/capability/perses_selection.go, internal/observability/registry.go,
  internal/identityprovider/**, .github/** — read never, written never).
- heads-up finding for the coordinator (no action by me): card 0428-085's wait_reason cites "PR #1645" but the
  card's prs field lists only `mcpdev80/baseharbor#1619`, and #1619 is CLOSED unmerged (measured). #1645 is open
  at 4d73aa97808d. The card text and prs field disagree (tasks/t-20261114-r28-perses-log-trace-dash.md,
  prs line vs wait_reason line).

## Cleanliness (before/after)

This lane started NO container, network, volume or compose project on this host (docker/podman were only
observed, never started; tests would have run only on baha-docker/baha-podman — none were needed).
- Before: `docker ps` empty; 1 ambient network (ssltest_default, foreign); 13 ambient volumes (foreign).
- After: identical (`docker ps` empty, same network and volume lists — nothing added, nothing removed).
- cleanliness: no lane-owned docker/podman state exists; ambient foreign stacks untouched (owner-direktive 2026-11-08).

## END

END_DONE w212-0428-202-waitrecheck: 35 wait cards rechecked against #1732's green packages cell; dossier on
baseharbor-plan main (SHA in the END post); 11 cards now hang only on the 198 rail (7 of them additionally
need #1732's MERGE), 24 have another reason; "PR Selected Checks" is a CI-internal aggregate, not a live
required check (rulesets disabled, protection 404).
