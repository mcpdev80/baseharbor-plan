# w277 · 0428-273 · READ-ONLY #1819 hop pre-stage on the current tip

Lane: w277-0428-273-1819hoppre · Card: 0428-273 (t-20261124-gate-catalog-baseline-1819) · Chain slot 3: #1842 -> #1812 -> #1819 -> #1820
Mission: coordinator/missions/w277-0428-273-1819hoppre.txt · Commission 2026-11-26 · Mode: READ-ONLY (refresh of w258 preflight after product moves ae70964d7 -> ac7c970fe91a)

## ANSATZ (visible block, required before first commit)

- Card frontmatter owner VERBATIM (read at runtime from origin/main, `tasks/t-20261124-gate-catalog-baseline-1819.md` line 11): `owner: w65-0428-269-batchbaseline`
- Related consumer card 0428-181 (`tasks/t-20261120-r28-identity-dashboard-catalog-consumer.md` line 11): `owner: w54-0428-181-export`; PR #1819 headRefName `w54-0428-181-export`
- git identity this lane will use for its ONLY commit (plan akte): `user.name = w277-0428-273-1819hoppre`, `user.email = w277-0428-273-1819hoppre@baseharbor.local`
- Literal commit invocation: `git -c user.name='w277-0428-273-1819hoppre' -c user.email='w277-0428-273-1819hoppre@baseharbor.local' commit -m 'w277-0428-273-1819hoppre: read-only #1819 hop pre-stage akte on current tip'`
- Pre-push identity gate line: `git show -s --format=%an HEAD` — must print `w277-0428-273-1819hoppre` exactly before any push
- No product commit is made (read-only mission); the git identity above applies solely to this plan-repo evidence commit.

## PLAN

- 0. Verified plan repo remote + isolated plan worktree; evidence skeleton with ANSATZ block
- 1. STATE WITNESS: ls-remote develop tip + PR heads/state/mergeable for #1819/#1812/#1842/#1820/#1818/#1833/#1650
- 2. CARRIED-COMMIT INVENTORY on current tip, canonical/shortened/foreign classification, exact foreign count vs w258's 8
- 3. ANCESTRY/HOP ARITHMETIC: ancestor check, behind count, hop sequence, files the candidate must carry
- 4. CATALOG ROW CHECK at tip for 0428-273/0428-274 subjects + target-path resolution
- 5. SEAM-C PRESENCE: persesDashboardProvisionForLifecycle on tip/candidate + #1818 compile verdict
- 6. FIRE ORDER CHECK with file:line quotes; what is doable today vs after #1812 merges
- 7. AKTE via own plan branch + gh pr create against live main (no merge)
- 8. Verify evidence on origin/main, zero-mutation proof, cleanliness, END post

## 0) Wrong-zone + remote verification (first git actions)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:

    origin    https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin    https://github.com/mcpdev80/baseharbor-plan.git (push)

Correct planning repo confirmed (NOT workers/baseharbor-plan). Plan worktree for this lane: `workers/w277-0428-273-1819hoppre-plan` branched from `origin/main` @ `dd851feb461246865e265891a2c8f1d0c1c69517` (log line at worktree creation: "w274-0428-251-binddiag: read-only workflow zero-jobs diagnosis akte").

Product reads executed from a fresh read-only clone (blob:none) at `workers/w277-0428-273-1819hoppre-wt/baseharbor`, remote `origin https://github.com/mcpdev80/baseharbor.git` — the quarantined `workers/baseharbor` checkout was never used or cited.

## 1) STATE WITNESS (all remote truth via git ls-remote / gh api, host clock 2026-11-26)

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`:

    ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee refs/heads/develop

Develop tip = `ac7c970fe91a` = the second product move named in the mission (ae70964d7 -> ac7c970fe91a confirmed present in tip history; #1853 merged).

PR heads (`git ls-remote ... refs/pull/<n>/head`):

| PR | head SHA (ls-remote) | mission expected | match |
| --- | --- | --- | --- |
| #1819 | b3c5055ad2566b639c2b0d4f4c2848b045221ebf | b3c5055ad256… | YES |
| #1812 | 0922888af8fd70be4049cec529c69aebc057a356 | 0922888af | YES |
| #1842 | 4f570ff966cd5e8d3043e8bd6363e1ea4e87d0d6 | 4f570ff96 | YES |
| #1820 | 8f6b2444bdc9baabf4f492e930533c7c36406979 | 8f6b2444b | YES |
| #1818 | 20fc1cb7d49602dc7f8aa0004a7562a81311d78c | 20fc1cb7d | YES |
| #1833 | a7b0a48048c11d20234160eede941532ddc33156 | a7b0a4804 | YES |
| #1650 | 37c4d847ca377d1555163ac4791c8ba08b85de77 | 37c4d847c | YES |

PR state (`gh pr view --json number,state,baseRefName,headRefName,mergeable,isDraft,headRefOid,updatedAt`):

| PR | state | base | headRefName | mergeable | draft | head | updatedAt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1819 | OPEN | develop | w54-0428-181-export | MERGEABLE | false | b3c5055ad2 | 2026-11-25T20:56:51Z |
| 1812 | OPEN | develop | lane-0428-249-runtime-image-fix | MERGEABLE | false | 0922888af8 | 2026-11-25T21:59:37Z |
| 1842 | OPEN | develop | w177-0428-284-demo-pin-1812 | MERGEABLE | false | 4f570ff966 | 2026-11-26T01:57:15Z |
| 1820 | OPEN | develop | fix/broker-build-identity | MERGEABLE | false | 8f6b2444bd | 2026-11-25T22:06:38Z |
| 1818 | OPEN | develop | lane-0428-078-cf-fix | MERGEABLE | false | 20fc1cb7d4 | 2026-11-24T03:01:19Z |
| 1833 | OPEN | develop | lane-0428-288-compose-ids | MERGEABLE | false | a7b0a48048 | 2026-11-25T00:35:19Z |
| 1650 | OPEN | develop | lane-0428-078-perses-identity-on-resolver | MERGEABLE | false | 37c4d847ca | 2026-11-26T02:19:59Z |

All seven heads are unchanged relative to the mission brief; every PR is OPEN, non-draft, base develop. #1842 red-state is per the mission brief (not re-probed here: no CI inspection was ordered and none was run).

## 2) CARRIED-COMMIT INVENTORY (`git log --format='%h %an %ae %cn %ce %s' origin/develop..b3c5055ad2`)

Canonical admission criterion (card 0428-181 frontmatter owner + PR headRefName + w258 table): `w54-0428-181-export` / `w54-0428-181-export@baseharbor.local`.

| # | sha | author name | author email | classifier | verdict |
| --- | --- | --- | --- | --- | --- |
| 1 | b3c5055a | w54-0428-181-export | w54-0428-181-export@baseharbor.local | card payload (hop attestation) | CANONICAL (own) |
| 2 | a3ee25f6 | w205 | w205@baseharbor.local | hop-merge lane (lane-w218-1819-hop) — shortened form of a lane identity; carries pr-1812 | FOREIGN |
| 3 | 394559ec | w198-0428-284-demo-parser | w198-0428-284-demo-parser@baseharbor.local | 0428-284/#1812 hop lane | FOREIGN |
| 4 | eafd5e6d | lv4-verify | worker@baseharbor.local | lane-0428-249-runtime-image-fix merge | FOREIGN |
| 5 | 10129196 | lv4-verify | worker@baseharbor.local | 0428-249/#1812 gate work | FOREIGN |
| 6 | 3859d466 | lv4-verify | worker@baseharbor.local | 0428-249 gate work | FOREIGN |
| 7 | 2ea41620 | lv4-verify | worker@baseharbor.local | 0428-249 merge | FOREIGN |
| 8 | 64d3dc0e | lv4-verify | worker@baseharbor.local | 0428-249 merge | FOREIGN |
| 9 | 9140b2cb | Codex (committer w53-0428-152-alertfix) | codex@openai.com | 0428-152 alertfix ci commit | FOREIGN |
| 10 | 17381017 | 0428-061-sourcepull | 0428-061@baseharbor.local | 0428-181 payload FIX, shortened form | SAME-LANE shortened form (content = card payload; identity NOT canonical per w155 rule "shortened same-lane formatting as documentation vs genuinely foreign") |
| 11 | 9f84f47a | w54-0428-181-export (committer 0428-061-sourcepull) | w54-0428-181-export@baseharbor.local | 0428-181 payload base | CANONICAL author / shortened-form committer |

Classification deltas vs w258: same 11 carried commits; w258 table listed `17381017`'s author as `w54-0428-181-export`, at the tip `git log %an` shows `0428-061-sourcepull <0428-061@baseharbor.local>` (gh commit-object reading vs git-log author field). This is the documented same-lane shortened form (it is the 0428-181 fix commit), not a new foreign lane.

Count verdict at the current tip:
- carried commits not on develop: 11 (unchanged)
- canonical card-payload commits (author exactly `w54-0428-181-export`): 2 (b3c5055a, 9f84f47a)
- same-lane shortened form (0428-181 content, non-canonical identity): 1 (17381017)
- FOREIGN carried commits: **8** — a3ee25f6, 394559ec, eafd5e6d, 10129196, 3859d466, 2ea41620, 64d3dc0e, 9140b2cb
- w258's "8 foreign carried commits" is CONFIRMED UNCHANGED at tip ac7c970fe91a. The two product moves (ae70964d7 -> ac7c970fe91a) added develop-side commits only (#1850/#1852/#1853 landings); they did not touch #1819's head, so the carried-commit composition is identical.

## 3) ANCESTRY / HOP ARITHMETIC

- `git merge-base --is-ancestor origin/develop b3c5055a` -> **NO**: develop (`ac7c970fe91a`) is NOT an ancestor of the #1819 head. Hop required.
- `git merge-base origin/develop b3c5055a` = `28296a2e6e920592741c9397486358deac7e95b2`.
- What the candidate misses: `git log --oneline b3c5055a..origin/develop | wc -l` = **14** commits. First 10 subjects:

      ac7c970f Merge pull request #1853 from mcpdev80/lane-0428-253-planner-deleted-source
      228ecc5b chore(1853): marker to trigger fresh CI run (0428-253)
      0ba631de Merge remote-tracking branch 'origin/develop' into HEAD
      b69fc54d correction(1853): route test_pr_ci_fallback + test_pr_gate_coverage into pr-planner-tests (0428-253)
      ae70964d Merge pull request #1850 from mcpdev80/lane-0428-307-runtime-identity-fallback
      6b153b8d fix(0428-307): fail closed on missing runtime identity permission (card t-20261125-hunt37)
      fcd44911 Merge pull request #1852 from mcpdev80/carrier-0428-307-catalog
      030e5848 correction(1853): revert ci.yml pr-planner-tests hunk to develop (0428-253)
      d3db4d89 Merge remote-tracking branch 'origin/develop' into carrier-0428-307-catalog
      4ca3f465 Merge origin/develop into lane-0428-253-planner-deleted-source (PR-hop #1853, w217)

  (remaining 4: 10df9c69, 3c1ebc6f, 90c8017b ci(planner) deleted source rows (0428-253), 150e3c0e fix(0428-307) catalog carrier)
- Exact later-lane hop sequence (execute ONLY after #1812 lands, per fire order §6), per owner transport rule (`git merge origin/develop` + normal push, no force/cherry-pick):

      git fetch origin refs/pull/1819/head            # checkout the PR head FIRST (never a foreign base)
      git checkout -b <lane> FETCH_HEAD               # or the existing branch w54-0428-181-export
      git merge origin/develop                        # ONE ordinary merge commit, tip witness ac7c970fe or newer
      # identity for the new commit: git -c user.name=<executing lane from card frontmatter> -c user.email=<same>@baseharbor.local commit (merge)
      git show -s --format=%an HEAD                   # pre-push gate: must equal the lane exactly
      git push origin <lane>                          # NORMAL push, no force
      git diff --name-status origin/develop...HEAD    # PAYLOAD GUARD: must be NON-EMPTY (below)

  Note the merge absorbs the 14 develop commits; it does NOT remove the 8 foreign carried commits from history — the defect w258 flagged is ancestry-only after a hop, and the own-commits-only log line will still list the carried merges. Whether a bare hop suffices (vs a clean re-stack of the 3-payload chain) is a Codex decision at review, per the identity-admission boundary (w267/w279 missions); this lane states the arithmetic only.
- Payload guard at current tip: `git diff --name-status origin/develop...b3c5055a` (NON-EMPTY, no payload-loss disease):

      M	.github/workflows/pre-release-runtime-suite.yml
      M	internal/application/runtime_postgres.go
      A	internal/metrics/perses_dashboard_provision.go
      A	internal/metrics/perses_dashboard_provision_test.go

- Files the candidate must still carry (PR files API, `gh api repos/mcpdev80/baseharbor/pulls/1819/files`): same 4 files — pre-release-runtime-suite.yml (modified, 20 changes), runtime_postgres.go (modified, 109), perses_dashboard_provision.go (added, 388), perses_dashboard_provision_test.go (added, 327).
- The candidate carries NO scripts/pr-gate-coverage.json changes (0 scripts files in payload) — consistent with card 0428-273's rule that the catalog rows land on develop via the w65 baseline, NOT inside #1819.

## 4) CATALOG ROW CHECK at develop tip ac7c970fe91a (`scripts/pr-gate-coverage.json`)

Card 0428-273 subjects (3 rows) + card 0428-274 subject (1 row). Rows live under the `components:` list. file:line (git show origin/develop:scripts/pr-gate-coverage.json piped to grep -n):

| subject path | file:line | row id | occurrences | surfaces | target resolves on develop tree? |
| --- | --- | --- | --- | --- | --- |
| internal/application/runtime_postgres.go | :1613 (id :1612) | source.internal_application_runtime_postgres_go | 1 | docker+podman data.capabilities | YES |
| internal/metrics/perses_dashboard_provision.go | :1621 (id :1620) | source.internal_metrics_perses_dashboard_provision_go | 1 | docker+podman data.capabilities | NO — file introduced by #1819 payload, absent on develop |
| internal/metrics/perses_dashboard_provision_test.go | :1629 (id :1628) | source.internal_metrics_perses_dashboard_provision_test_go | 1 | docker+podman data.capabilities | NO — same |
| cmd/baha/app_broker_compat_test.go (0428-274) | :1637 (id :1636) | source.cmd_baha_app_broker_compat_test_go | 1 | docker+podman data.capabilities | YES |

- EXACTLY-ONCE verdict: all four 0428-273/0428-274 gate-owner rows landed by the #1822 batch baseline exist exactly once at the current tip — no duplicates (path-scoped grep count = 1 each; catalog-wide duplicate scan found 0 duplicate paths across 301 component rows).
- Target-path resolution census at the tip (ls-tree based, 301 component rows): **7 rows point at paths absent from the develop tree**, versus w254's "0 unresolved" census. Findings (report-only, no edit):
  - internal/metrics/perses_dashboard_provision.go — dangling on develop BY DESIGN (introduced by #1819 itself; row must pre-exist for the planner; resolves once #1819 merges)
  - internal/metrics/perses_dashboard_provision_test.go — same, by design
  - internal/metrics/identity_dashboard_witness.go — expect same category (introduced by #1650 payload; verify at #1650 qualification)
  - internal/metrics/perses_dashboards_keycloak.go — expect same category (introduced by #1819/#1650-side payload; verify)
  - cmd/baha/installation_reset_preservation_test.go — NOT a 0428-273/274 row; candidate of a planner-deleted-source case already routed by the #1853 planner work (commits 90c8017b / b69fc54d) — flag for the 0428-253 owner
  - cmd/baha/w128_failed_apply_destroy_test.go and cmd/baha/w287_destroy_after_failed_apply_test.go — same category as above (deleted-source rows). These 5 non-perses dangling rows are OUTSIDE this card's write-set; documented as befund only.
- Verdict for #1819's purpose: the catalog rows #1819 needs are present, unique, and gate-routed (docker+podman data.capabilities) at the current tip. Trusted Plan's missing-gate-owner rejection cause is resolved for this PR on top of develop; what remains blocking is ancestry/qualification sequencing, not catalog.

## 5) SEAM-C PRESENCE (persesDashboardProvisionForLifecycle)

- On develop tip: file `internal/metrics/perses_dashboard_provision.go` does NOT exist; the symbol occurs nowhere in the develop tree (one of the two perses_dashboard_provision rows above is precisely this seam). Seam-C is NOT yet on develop.
- On the #1819 candidate head: `internal/metrics/perses_dashboard_provision.go:84` (declaration), comment refs :66/:76, registration `internal/metrics/perses_dashboard_provision.go:309` -> `RegisterPersesDashboardProvisioner(persesDashboardProvisionForLifecycle)` in `init()`.
- Diff status: `git diff --name-status origin/develop...b3c5055a -- <seam files>` = `A` (added) for both files → #1819's diff does NOT remove or rename the seam; it introduces it.
- Signature as read (line 84): `func persesDashboardProvisionForLifecycle(m application.Manifest, runtimeDir, namespace string) error`, registered against `func RegisterPersesDashboardProvisioner(fn func(m Manifest, runtimeDir, namespace string) error)` (internal/application/runtime_postgres.go:386 in the candidate).
- #1818 clean-rebuild compile verdict: **NO — not as-is on the bare develop tip.** #1818's later clean rebuild can compile against the seam ONLY when the candidate carries it in, i.e. built on a head that includes #1819's merged content (chain order #1812 -> #1819 -> #1820; #1818 depends on that landing, not on develop today). Supporting API check: `application.Manifest.ObservabilityManagementUI` (manifest.go:95) and `.Perses` (manifest.go:99) are identical on develop tip and the candidate (zero diff in manifest.go), and #1819's write-set does not touch internal/application/manifest.go, so no manifest-API collision arises from the hop.

## 6) FIRE ORDER CHECK (quotes with file:line)

Owner sequencing directive, coordinator/AGENTS.md line 21 (#1819-Auflösung, Owner-Lesart 2026-11-25):

> "#1819-Auflösung (Owner-Lesart 2025-11-25): disjunkte Vorarbeit an #1819 darf parallel laufen; Rebase, Qualifikation und MERGE von #1819 bleiben strikt NACH #1812 (Kette #1812→#1819→#1820)."

Kettenschutz rule verbatim, coordinator/PROTOCOL.md line 1610 (OWNER RULE VERBATIM LOCKED):

> "Kettenschutz: #1812 -> #1819 -> #1820 bleibt Sequenz; keine parallelen Neuauflagen" — covers the HOP/new-head/CI-pair itself (not only review+merge).

Queue position, coordinator/QUEUE.md line 33:

> "| W3 | #1819 review -> merge (w136) | chain: after #1812 lands (Kettenschutz #1812->#1819->#1820) | #1812 merged |"

Card-level statement, baseharbor-plan origin/main `tasks/t-20261124-gate-catalog-baseline-1819.md` line 67:

> "AUTGELÖST 2026-11-25 (Owner-Lesart zur Mehrdeutigkeit #1819): disjunkte Vorarbeit darf parallel laufen; Rebase/Qualifikation/Merge bleiben strikt NACH #1812 (Serie #1812->#1819->#1820). Kein Freeze, keine Umordnung."

Legitimately doable TODAY for #1819: read-only preparation only — state witnesses, carried-commit inventory, ancestry arithmetic, catalog/seam verification, hop recipe documentation (this akte). NOT doable until #1812 (which itself waits on #1842) lands: any hop/push/new head, any CI run on a new head, any qualification, review-fire or merge of #1819.

## 7) Cleanliness + zero-mutation proof

- Host: coordinator host only. No container, no compose project, no VM work started (docker/podman untouched by this read-only mission). `git status` in the fresh clone: clean (read-only fetches into refs/witness only).
- Created paths (all in lane zone, listed for cleanup by owner): `workers/w277-0428-273-1819hoppre-wt/` (blob:none clone), `workers/w277-0428-273-1819hoppre-plan/` (plan worktree, removed after push), `workers/todos/w277-0428-273-1819hoppre.json` (board file), `/tmp/opencode/w277-*` (extraction scratch).
- Zero-mutation proof: every ref SHA above comes from `git ls-remote`/`gh api` (read-only). No push to any product remote, no PR edit, no workflow_dispatch, no rerun, no branch mutation. Before/after ls-identity for develop + all seven PR heads is in §1 and repeated at END below.
- Quarantined-checkout rule honored: /home/marcel/dev/baseharbor-ecosystem/workers/baseharbor was not read for any witness.

## 8) Findings register (report-only)

1. #1819 head carries 8 foreign commits at the tip (unchanged vs w258); ancestry defect remains; Codex decides hop-vs-re-stack at qualification time.
2. Catalog census at tip shows 7 dangling component rows (paths absent on develop); 2 are by-design #1819 seam rows, ~2 are #1650/#1819-side introduced, 3 (incl. cmd/baha/installation_reset_preservation_test.go, w128/w287 destroy tests) look like planner-deleted-source cases routed by #1853 — belongs to 0428-253 owner, outside this card's write-set.
3. w258's author table vs git-log author field differ on 17381017 (gh commit-object vs git %an): documented as same-lane shortened form; no new foreign lane.

## 9) Publication witnesses

- Plan akte commit: `c1770a8ce84ff555c52b8440f5e91e9c59bf10fa` on branch `w277-0428-273-1819hoppre-akte`, author `w277-0428-273-1819hoppre <w277-0428-273-1819hoppre@baseharbor.local>` (pre-push gate printed exactly).
- `git log --oneline origin/main..HEAD` = exactly one line: `c1770a8ce w277-0428-273-1819hoppre: read-only #1819 hop pre-stage akte on current tip`; base attestation: `origin/main` = `dd851feb461246865e265891a2c8f1d0c1c69517` (ls-remote at worktree creation), ancestor check `git merge-base --is-ancestor origin/main HEAD` = YES.
- Plan PR: https://github.com/mcpdev80/baseharbor-plan/pull/80 (state OPEN, base main, head c1770a8ce) — created via `gh pr create`, NOT merged (admin squash-merge per precedent #52/#61/#62).
- Branch delivery proof: `git ls-remote origin refs/heads/w277-0428-273-1819hoppre-akte` = `c1770a8ce84ff555c52b8440f5e91e9c59bf10fa`.
- Zero-mutation AFTER (identical to §1 BEFORE):

      ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee refs/heads/develop
      37c4d847ca377d1555163ac4791c8ba08b85de77 refs/pull/1650/head
      0922888af8fd70be4049cec529c69aebc057a356 refs/pull/1812/head
      20fc1cb7d49602dc7f8aa0004a7562a81311d78c refs/pull/1818/head
      b3c5055ad2566b639c2b0d4f4c2848b045221ebf refs/pull/1819/head
      8f6b2444bdc9baabf4f492e930533c7c36406979 refs/pull/1820/head
      a7b0a48048c11d20234160eede941532ddc33156 refs/pull/1833/head
      4f570ff966cd5e8d3043e8bd6363e1ea4e87d0d6 refs/pull/1842/head

END_DONE w277-0428-273-1819hoppre: read-only pre-stage complete — carried 11 / foreign 8 unchanged at tip ac7c970fe; develop NOT ancestor (behind 14); catalog rows 1x each (2 by-design seam paths dangling); seam-C candidate-only (file:84), #1818 cannot compile it from bare tip; Kettenschutz quote recorded; plan PR reported below; zero product mutation witnessed by identical ls-remote before/after.
