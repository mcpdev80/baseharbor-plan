# w218 — PR-HOP #1819 (card t-20261120-r28-identity-dashboard-catalog-consumer, 0428-181)

Mission: `coordinator/missions/w218-1819-hop.txt`. Chain-hop only: no content changes,
no merges, no card writes, no `.github` edits, no plan pushes beyond this akte.

## PLAN

1. Resolve remotes and real GitHub URLs (`gh api pulls/1812 .head.ref`, PR #1819 head). — done
2. Fetch #1812 hop-branch head and develop tip; record base attestations. — done
3. Start worktree off branch head `17381017b` (`workers/w218-0428-181-0428-285-1819hop-wt`). — done
4. `git merge` #1812 head `394559e`; STOP+STATE on conflicts. — done, clean
5. `git merge` `origin/develop` (`28296a2e`); STOP+STATE on conflicts. — already contained
6. Identity: card owner VERBATIM via `git -c`; `%an` gate before push. — done
7. Ancestor witnesses for `394559e` + develop tip; payload-diff stat (ADD-ON rule). — done
8. Normal push to `w54-0428-181-export`; `ls-remote` delivery witness. — done
9. Watch fresh `pull_request` run(s) to terminal; executed census per_page=100; two distinct greens. — done
10. Evidence akte pushed to origin/main, then END post. — this file

## Identity block (visible ANSATZ)

- Card frontmatter owner VERBATIM (fetched at runtime from `origin/main`,
  `tasks/t-20261120-r28-identity-dashboard-catalog-consumer.md`): `owner: w54-0428-181-export`
- git identity used: user.name `w54-0428-181-export`, user.email `w54-0428-181-export@baseharbor.local`
- Literal invocation pattern:
  `git -c user.name=w54-0428-181-export -c user.email=w54-0428-181-export@baseharbor.local commit ...`
  (merge commits and the attestation commit carry this author)
- Pre-push gate line and result: `git show -s --format=%an HEAD` → `w54-0428-181-export`

## Remote resolution (REMOTE GUARD)

`git -C .../baseharbor remote -v` — the only remote used is `lane-origin`:

```
lane-origin https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
lane-origin https://github.com/mcpdev80/baseharbor.git (push)
```

(`origin`/`upstream` point at the same GitHub URL; all fetch/push went through `lane-origin`, verified to contain `github.com/mcpdev80`.)

## Base attestations (`git ls-remote lane-origin`, before push)

- #1819 head (branch cut point): `17381017be986f0eccb25662ad742ad759296346` refs/heads/w54-0428-181-export
- #1812 head (`.head.ref` = `lane-0428-249-runtime-image-fix`): `394559ec6cf5680f6c46ca8d40203fa2666fb70e`
- develop tip: `28296a2e6e920592741c9397486358deac7e95b2`
- `git log --oneline -1 394559e` → `hop(0428-284): re-admit PR #1812 onto current develop w198-0428-284-demo-parser`

## Hops performed

1. Worktree `workers/w218-0428-181-0428-285-1819hop-wt`, branch `lane-w218-1819-hop` cut from `17381017b`.
2. `git merge --no-edit lane-origin/pr-1812` → merge commit `a3ee25f63` (46 files, +2212/−386). No conflicts.
3. `git merge --no-edit lane-origin/develop` → "Already up to date" (develop tip `28296a2e` is an
   ancestor of #1812 head `394559e`; the mission's expectation "28296a2e or later" is met by
   ancestry through the #1812 hop).
4. `git commit --allow-empty` attestation commit `b3c5055ad` (the candidate head) with the card-owner identity.

## Ancestor witnesses

```
git merge-base --is-ancestor 394559e HEAD   -> exit 0, printed "OK: 394559e ancestor of HEAD"
git merge-base --is-ancestor 28296a2e HEAD  -> exit 0, printed "OK: develop 28296a2e ancestor of HEAD"
git merge-base --is-ancestor 17381017b HEAD -> exit 0, printed "OK: 1819 head 17381017b ancestor of HEAD"
```

`git log --oneline lane-origin/develop..HEAD` lists only this chain's own commits
(1819 card commits `9f84f47a7`/`17381017b`, the #1812 lane history ending at `394559e`,
merge `a3ee25f63`, attestation `b3c5055ad`) — no foreign candidate on top.

## Content-retention proof (ADD-ON hop lesson)

`git diff lane-origin/develop...HEAD --stat`:

```
 .github/workflows/pre-release-runtime-suite.yml    |  20 ++
 internal/application/runtime_postgres.go           | 109 ++++++
 internal/metrics/perses_dashboard_provision.go     | 388 +++++++++++++++++++++
 .../metrics/perses_dashboard_provision_test.go     | 327 +++++++++++++++++
 4 files changed, 844 insertions(+)
```

Not empty; the #1819 card payload (identity dashboard provisioning + postgres runtime hook) is retained. Three of four payload files are byte-identical to `17381017b` (verified with `git diff --quiet 17381017b HEAD -- <file>` → SAME). The fourth, `.github/workflows/pre-release-runtime-suite.yml`, DIFFERS from `17381017b`: on this base the #1812 lane (`9140b2cbd` + merge `64d3dc0e7`) already carries its own reload-step changes to that file, and the hop's auto-merge resolved in favor of develop+#1812's version while keeping #1819's 2 added insertions region differently placed. Per the workflow-files-are-Owner-scope rule I did NOT edit `.github/**`. Finding for the coordinator (file: consequence): `git diff HEAD 17381017b -- .github/workflows/pre-release-runtime-suite.yml` shows a 2-insertion/34-deletion delta vs the old #1819 head, i.e. #1819's earlier standalone reload-step variant is superseded by #1812's version now in the chain. This is expected chain behavior (base branch wins), not a payload drop of the card's Go content.

## Delivery witness (after push)

```
git ls-remote lane-origin refs/heads/w54-0428-181-export refs/pull/1819/head
b3c5055ad2566b639c2b0d4f4c2848b045221ebf	refs/heads/w54-0428-181-export
b3c5055ad2566b639c2b0d4f4c2848b045221ebf	refs/pull/1819/head
```

Exactly one candidate: the PR head branch `w54-0428-181-export`. The local helper branch
`lane-w218-1819-hop` was never pushed (the post-push `ls-remote` above shows no such ref).

## Local non-test prechecks

- `go build -o /tmp/opencode/baha-w218 ./cmd/baha` → OK
- `go vet ./internal/metrics/ ./internal/application/` → OK
- `go test ./internal/metrics/ -count=1 -run PersesDashboardProvision` (named form; no lifecycle containers) → ok
- `scripts/ci-fast-check.sh` exceeded my 120 s local budget (full build sweep); test execution belongs to Hosted CI.

## Hosted CI (self-run duty) — terminal

Census: `GET /repos/mcpdev80/baseharbor/actions/runs?head_sha=b3c5055ad...&per_page=100`
Observed in_progress repeatedly by this session, watched to terminal by this session.

- Run 1: id `45694363486`, name "CI · PR #1819", event `pull_request`, head `b3c5055ad` → **completed, success**
  - Executed check census (per_page=100) on that head: `PR · Exact Candidate`, `PR · Trusted Plan`,
    `PR · Source format`, `Workflow policy`, `PR · Native gate plan`, `PR · Runner Interface`,
    `PR · Demo Pin`, `PR · Focused Python`, `PR · Go unit · packages`, `PR · Go unit · cli-0..3`,
    `PR · Validation · go-build/go-vet/ci-policy/ci-actionlint/pr-planner-tests/receipt-execution-tests/ci-executor-tests`,
    `PR · Go unit · owner`, `PR · Candidate-added checks (advisory)`,
    `PR · Selected Runtime ... / Executed docker · data-capabilities`, `PR Selected Checks` → all **success**;
    remaining gates skipped (not selected for this diff).

Two distinct greens (mission requirement), both executed on ancestors of the final head `b3c5055ad`:

- Run A: `45691594250` — #1812's hop re-qualification run, head `394559e` (merged into candidate): **completed, success** (recorded in the w214 hop akte, `evidence/r28-welle6-2026-11-25/w214-0428-284-1812-hop/`).
- Run B: `45694363486` — this hop's run on the exact candidate head `b3c5055ad`: **completed, success**.

## cleanliness

- No containers or compose projects were started by this lane on any host; `docker ps -a` shows no lane-owned stacks (nothing of mine to bring down; ambient stack untouched).
- Worktrees: product hop worktree `workers/w218-0428-181-0428-285-1819hop-wt` retained for review; plan worktree `workers/w218-0428-181-0428-285-1819hop-plan` removed after this push.

## repo-rule compliance

- Chain hop only: zero content edits (merge commits + empty attestation commit).
- No `.github/**` edits, no workflow_dispatch/rerun triggers, no merges, no card writes.
- Identity admission rule satisfied (card owner `%an` gate before push).
- All remote truth via `git ls-remote lane-origin` / GitHub API; quarantined checkout untouched.

## Evidence-on-origin/main witness

(second-to-last action, output pasted below)

## END

END_DONE w218-0428-181-0428-285-1819hop: PR #1819 new head b3c5055ad (ancestors: 394559e OK, develop 28296a2e OK); greens 45694363486 (exact head, pull_request, PR Selected Checks success) + 45691594250 (#1812 394559e).

## origin/main verification (exact output)

```
git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle6-2026-11-25/w218-0428-181-0428-285-1819hop/1819-pr-hop-akte.md
evidence/r28-welle6-2026-11-25/w218-0428-181-0428-285-1819hop/1819-pr-hop-akte.md
```
