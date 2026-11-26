# w258-0428-273-1819preflight — read-only preflight of PR #1819

- Shift: w258-1819-preflight
- Card: 0428-273 (add #1819 catalog rows) — context card for this read-only preflight
- Mission: `coordinator/missions/w258-1819-preflight.txt`
- Mode: READ-ONLY befund of PR #1819 against CURRENT origin/develop. NO product write, NO `.github/**`, NO PR, NO CI trigger, NO rerun, NO rebase, NO hop, NO merge, NO local test execution. Chain constraint `#1842 -> #1812 -> #1819`: rebase/qualify/MERGE stay strictly after #1812.
- Evidence origin: plan repo `origin` = `https://github.com/mcpdev80/baseharbor-plan.git` (verified `git -C baseharbor-plan remote -v`). Product remote used: `https://github.com/mcpdev80/baseharbor.git` via `git clone --filter=blob:none` in `/tmp/opencode/w258-1819-preflight-wt`. No git operations touched the quarantined `workers/baseharbor` checkout.

## PLAN

- Read mission + card 0428-273 + w254 akte for exact scope; verify plan-product remotes
- Real-time witnesses: `git ls-remote` develop / 1819head / 1812head
- `gh pr view 1819` + `gh api pulls/1819/commits per_page=100` -> authors -> flag non-canonical identity vs card frontmatter `(lane X)`
- Ancestry status: is develop a descendant of the PR head's merge-base; merge-tree prediction of inherited tip (throwaway worktree, no auto-merge)
- Payload census: `git diff develop...1819head --name-status` -> payload-loss disease absent (non-empty); compare against card write-set
- Catalog check: every 1819 changed path resolves to a focused runtime gate on develop
- seam-C note: confirm #1819 tree still resolves `persesDashboardProvisionForLifecycle` (seam-C) for the later #1820/#1818 stack
- Write evidence akte via plan-PR branch path; origin/main witness
- Cleanliness witness + END_DONE

## Base attestation

- Plan repo remote (first git action, before any evidence op): `origin https://github.com/mcpdev80/baseharbor-plan.git` (verified `git -C baseharbor-plan remote -v`), `planrem` / `upstream2` same — all github.com/mcpdev80.
- Product remote: `https://github.com/mcpdev80/baseharbor.git` — used ONLY via read-only clone in `/tmp/opencode/w258-1819-preflight-wt`. The `workers/baseharbor` quarantined checkout (force-push incident 2026-11-06) was never cited.
- develop exact head (ls-remote witness): `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` = `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee refs/heads/develop`.
- #1819 head (ls-remote witness): `b3c5055ad2566b639c2b0d4f4c2848b045221ebf refs/pull/1819/head`.
- #1812 head (ls-remote witness): `0922888af8fd70be4049cec529c69aebc057a356 refs/pull/1812/head`.

## VISIBLE ANSATZ BLOCK (canonical lane identity admission)

- Card frontmatter owner (fetched from origin/main at runtime, card `t-20261124-gate-catalog-baseline-1819.md`, line 10): `w65-0428-269-batchbaseline`. This card is a read-only befund; no product commit is authored by this lane, so no canonical commit identity is used. No commit is created in the product repo.
- Git user.name / user.email this lane would use for ANY product commit (none authored this shift): not applicable — no product commit created.
- No `git -c user.name=... -c user.email=...@baseharbor.local commit ...` invocation this shift.
- Pre-push `git show -s --format=%an HEAD` gate: not applicable (no product commit).

## 1) PR #1819 identity & state

`gh pr view 1819 --repo mcpdev80/baseharbor`:

- number 1819, title "0428-181 wire Perses identity dashboard into export path"
- state OPEN, baseRefName develop, headRefName `w54-0428-181-export`
- additions 844, deletions 0, updatedAt 2026-11-25T20:56:51Z, mergeStateStatus BEHIND
- head exact: `b3c5055ad2566b639c2b0d4f4c2848b045221ebf`

Authors of the 11 commits on `gh api pulls/1819/commits per_page=100` (raw `commit.author`):

| sha | author.name | author.email | verdict vs card frontmatter `(lane X)` |
| --- | --- | --- | --- |
| 9f84f47a | w54-0428-181-export | w54-0428-181-export@baseharbor.local | OK — card payload, canonical lane identity (0428-181) |
| 17381017 | w54-0428-181-export | w54-0428-181-export@baseharbor.local | OK — card payload fix, canonical lane identity |
| 9140b2cb | Codex | codex@openai.com | FLAGGED — author `Codex <codex@openai.com>`, message "ci: reload candidate image before runtime publish" |
| 64d3dc0e | lv4-verify | worker@baseharbor.local | FLAGGED — author `lv4-verify <worker@baseharbor.local>`, merge develop into `lane-0428-249-runtime-image-fix` |
| 2ea41620 | lv4-verify | worker@baseharbor.local | FLAGGED — same, merge develop into `lane-0428-249-runtime-image-fix` |
| 3859d466 | lv4-verify | worker@baseharbor.local | FLAGGED — "release-requirements: add v0.4.28 to 14 docker/podman light gate rows" |
| 10129196 | lv4-verify | worker@baseharbor.local | FLAGGED — "Drop scripts/release-requirements.json from #1812" |
| eafd5e6d | lv4-verify | worker@baseharbor.local | FLAGGED — merge develop into `lane-0428-249-runtime-image-fix` |
| 394559ec | w198-0428-284-demo-parser | w198-0428-284-demo-parser@baseharbor.local | FLAGGED — "hop(0428-284): re-admit PR #1812 onto current develop" |
| a3ee25f6 | w205 | w205@baseharbor.local | FLAGGED — merge `lane-origin/pr-1812` into `lane-w218-1819-hop` |
| b3c5055a | w54-0428-181-export | w54-0428-181-export@baseharbor.local | OK — card payload hop attestation, canonical lane identity (0428-181) |

Verdict: only the 3 card-payload commits (9f84f47a, 17381017, b3c5055a) carry the canonical `(lane X)` identity `w54-0428-181-export`. The 8 carried commits carry non-canonical identity strings: `Codex <codex@openai.com>`, `lv4-verify <worker@baseharbor.local>` (a foreign lane `0428-249-runtime-image-fix`), and `w198-0428-284-demo-parser` / `w205` (0428-284 hop commits). Per the mission, this is a befund — the candidate SHA carries foreign-lane commit identities on top of its own payload. Candidate commit identity admission (card t-20261121 / w155) would require a clean canonical-author chain; the current #1819 head does NOT present one.

## 2) Ancestry status

- #1819 head's own merge-base with develop = `28296a2e6e920592741c9397486358deac7e95b2`.
- `git merge-base --is-ancestor 28296a2e origin/develop` -> YES. develop IS a descendant of (supersedes) #1819's base. The #1819 branch root `9f84f47a` descends from develop's history.
- #1819 head contains 11 commits not on develop: the 3 card-payload commits (9f84f47a, 17381017, b3c5055a) plus 8 carried commits (foreign merges + 0428-249 gate work + 0428-284 hop).
- `git log --oneline origin/develop..HEAD` (own-commits-only gate):

  ```
  b3c5055a chore(0428-181): pr-hop base attestation - merged #1812 head 394559e and develop 28296a2e into #1819 candidate
  a3ee25f6 Merge remote-tracking branch 'lane-origin/pr-1812' into lane-w218-1819-hop
  394559ec hop(0428-284): re-admit PR #1812 onto current develop w198-0428-284-demo-parser
  eafd5e6d Merge remote-tracking branch 'origin/develop' into lane-0428-249-runtime-image-fix
  10129196 Drop scripts/release-requirements.json from #1812: restore develop state
  3859d466 release-requirements: add v0.4.28 to 14 docker/podman light gate rows
  2ea41620 Merge remote-tracking branch 'origin/develop' into lane-0428-249-runtime-image-fix
  64d3dc0e Merge remote-tracking branch 'origin/develop' into lane-0428-249-runtime-image-fix
  9140b2cb ci: reload candidate image before runtime publish
  17381017 fix(0428-181): RC1 fail-closed producer-path regression + RC2 byte/hash-stability (Codex review)
  9f84f47a 0428-181 wire Perses identity dashboard into export path
  ```

- The carried commits include a foreign lane `0428-249-runtime-image-fix` and 0428-284 hops — i.e. a foreign candidate is carried on top of the #1819 payload. Per one-integration-candidate-per-chain, a clean rebase of #1819's 3-payload-commit chain onto the post-#1812 develop head is required before merge; the current head does not satisfy the own-commits-only gate.
- merge-tree prediction (`git merge-tree --messages --write-tree origin/develop <1819head>`): produced merge tree `3e3ef42dd792b1093dfdfdcda631a467de5584ef`, exit 0, no conflict messages. `git diff --name-only origin/develop 3e3ef42d` == exactly the 4 changed files; the merge tree equals #1819's own payload resolution (no develop conflict on the 4 payload files). So #1819 would cleanly absorb develop's tip: the 4 payload files resolve to the 1819 version; develop's 14 commits since `28296a2e` (incl. #1853 planner-deleted-source handling) layer underneath. Inheritance is content-clean; the only defect is the carried foreign commits / ancestry, not a conflict.

## 3) Payload census (`git diff develop...1819head --name-status`)

```
M .github/workflows/pre-release-runtime-suite.yml
M internal/application/runtime_postgres.go
A internal/metrics/perses_dashboard_provision.go
A internal/metrics/perses_dashboard_provision_test.go
```

- 4 files, 844 insertions, 0 deletions. Payload-loss disease ABSENT: all changed files are non-empty (`runtime_postgres.go` +109 real lines incl. the `ensurePersesDashboardRuntime` apply-boundary call site; `perses_dashboard_provision.go` 367 non-empty lines; `perses_dashboard_provision_test.go` a real 327-line test; `pre-release-runtime-suite.yml` +30 lines of OCI image-load-before-publish guards).
- Card write-set = `scripts/pr-gate-coverage.json` (the card 0428-273 asks to ADD catalog rows there). The #1819 payload touches NONE of `scripts/**` — this PR is a product change, not the catalog row change. The catalog rows for its paths live on develop (see section 4). This is expected and correct per the card's split ownership.

## 4) Catalog check (does every 1819 path resolve to a focused runtime gate on develop?)

 develop `scripts/pr-gate-coverage.json`: 301 components, 301 unique ids, 0 duplicates. Official validator `validate-pr-gate-coverage.py` -> "PR gate coverage catalog is valid".

Resolved via `resolve_covered_gates()` against develop's catalog:

| changed path | catalog row (develop) | resolving gate | runtime gate? |
| --- | --- | --- | --- |
| `internal/application/runtime_postgres.go` | `source.internal_application_runtime_postgres_go` | `atomic/docker/data-capabilities` | yes, focused |
| `internal/metrics/perses_dashboard_provision.go` | `source.internal_metrics_perses_dashboard_provision_go` | `atomic/docker/data-capabilities` | yes, focused |
| `internal/metrics/perses_dashboard_provision_test.go` | `source.internal_metrics_perses_dashboard_provision_test_go` | `atomic/docker/data-capabilities` | yes, focused |
| `cmd/baha/app_broker_compat_test.go` (card 0428-274, #1820) | `source.cmd_baha_app_broker_compat_test_go` | `atomic/docker/data-capabilities` | yes, focused |

- All 4 target paths resolve to `atomic/docker/data-capabilities` (a focused runtime gate), so `UNRESOLVED = NONE` for the 1819 write-set.
- This is the exact row the w254 akte recorded as already landing on develop via PR #1822 (commit `90086a1f`). No row added this shift (dedup rule).
- The only catalog difference develop->1819head is the 3 `runtime_identity_workload*` components (PR #1850, foreign) present on develop but absent on 1819head — NOT in the 1819 payload and not in the 0428-273/0428-274 write-set.
- No `.github/**` edit needed by this lane (the OCI image-load guard in `pre-release-runtime-suite.yml` is part of the #1812 carryover, not this card; and `.github/**` is Owner scope — not touched).

## 5) seam-C note (`persesDashboardProvisionForLifecycle`)

- `persesDashboardProvisionForLifecycle` EXISTS in the 1819 head tree (4 occurrences in `internal/metrics/perses_dashboard_provision.go`), declared as the apply-boundary entry the lifecycle seam `application.RegisterPersesDashboardProvisioner` calls; wired via `internal/application/runtime_postgres.go:EnsureRuntime` -> `ensurePersesDashboardRuntime`, and registered in `init()` (`RegisterPersesDashboardProvisioner(persesDashboardProvisionForLifecycle)`).
- `git merge-base <1819head> <1812head>` = `394559ec` — #1819 head carries #1812's content, so the same seam-C entry is present on the later #1818/#1820 stack head. The symbol is intact and resolves. (Note: the symbol does NOT exist on develop — `internal/metrics/perses_dashboard_provision.go` does not exist there — which is exactly why the seam must be carried by the 0428-181 payload, and why the clean rebase must happen on a develop head post-#1812, per the chain constraint.)
- Read-only grep only; no product change.

## Cleanliness

- `docker ps -a` before: zero containers (coordinator/codeman server, read-only befund).
- `docker ps -a` after: zero containers.
- No containers / networks / volumes / state directories created.
- Throwaway read-only clones in `/tmp/opencode/w258-1819-preflight-wt` and `/tmp/opencode/w258-1819-preflight-wt/mtree-wt` (outside the ecosystem); product repo never mutated.

## Git evidence delivery

- Plan repo remote (first git action): `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push) — verified `git -C baseharbor-plan remote -v`.
- Evidence path to publish: `evidence/w258-1819-preflight/akte.md`
- Commit strategy: isolated clone `git clone https://github.com/mcpdev80/baseharbor-plan.git /tmp/opencode/w258-plan-wt`, `git add -f` the akte (bypassing the bookkeeping repo .gitignore), commit, push to origin/main, remove clone. Never rebase/reset/stash/checkout -f in the shared `baseharbor-plan` checkout; never `git add -A` there.
- plan origin/main before push: `9e9e53cf775699b4ea80bd8e72e776e3bce61ad1 refs/heads/main`.

## Outcome

#1819 (card 0428-181, context card 0428-273) preflight:

- Content READY: the 4-file payload is non-empty (no payload-loss disease); all 3 payload paths resolve to a focused runtime gate (`atomic/docker/data-capabilities`) on develop; seam-C `persesDashboardProvisionForLifecycle` present and resolves on the 1812-carrying head; merge-tree inheritance from develop tip is content-clean (no conflict).
- ANCESTRY DEFECT (the one blocker, matching the mission's "qualified-content EXCEPT ancestry"): the candidate head `b3c5055a` carries 8 foreign commits (foreign lane `0428-249-runtime-image-fix` gate work, `Codex`/`lv4-verify` non-canonical authors, 0428-284 hops) on top of the 3-card-payload commits. `git log --oneline origin/develop..HEAD` does NOT list only own commits; carried commit authors are non-canonical. This must be cleaned by a focused rebase of the 3-payload-commit chain onto the post-#1812 develop head before merge.
- Chain constraint honored: NO rebase, NO hop, NO push, NO merge, NO CI trigger, NO rerun. Hop fires only after #1812 lands (chain `#1842 -> #1812 -> #1819`).

## END

END_DONE w258-0428-273-1819preflight: candidate #1819 qualified-content EXCEPT ancestry — 8 foreign carried commits carry non-canonical authors; hop/qualify/merge fire strictly after #1812 lands. Read-only befund, no product write, no CI trigger, no local test.
