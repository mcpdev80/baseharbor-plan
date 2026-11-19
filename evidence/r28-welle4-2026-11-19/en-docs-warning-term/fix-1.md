# fix-1 — en-docs-warning-term (r28-welle4, 2026-11-19)

Mission: `mission-en-docs-warning-term.md` — Karte t-20261119-r28-en-docs-warning-term (card 0428-131), baseharbor, develop pinned da76c5cf9.
Found in: evidence/r28-welle4-2026-11-19/verify-env-chain/befund-1.md (chain 0428-130). The shipped EN catalog prints the acknowledging marker 'Warning' (wired by 0428-126); some EN documentation still said 'Achtung' — i18n term drift with the wrong polarity. German documents intentionally keep 'Achtung'.

Revision labels: r1 (single pass, this dossier).

## PLAN

1. (done) Reality check: develop + card note
2. (done) Isolated worktree under /var/tmp, base attestation
3. (done) Findings: grep 'Achtung' over EN docs, file:line list
4. (done) One documentation-spot fix per finding: 'Achtung' -> 'Warning'
5. (done) Control grep empty; docs-audit CI coverage confirmed (no .github change needed)
6. (done) This dossier, committed and pushed to baseharbor-plan origin/main
7. (done) Candidate commit + push, PR #1697 against develop
8. (done) Exact-head CI watched to terminal state — run 44478483899 completed SUCCESS
9. (done) Host cleanliness, END post

## W1 reality witnesses

Live develop head (`git ls-remote origin refs/heads/develop` from the product clone):

    da76c5cf9c963207038d5599bd130b89ecb1e8a4        refs/heads/develop

Mission-pinned da76c5cf9 = live head. Card note read: tasks/t-20261119-r28-en-docs-warning-term.md (intake commit 4962e642, planning repo = /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan, toplevel verified via `git rev-parse --show-toplevel`).

## W2 basis attestation

Branch cut: `git worktree add --detach /var/tmp/en-docs-warning-term-wt/baseharbor da76c5cf9c963207038d5599bd130b89ecb1e8a4`, then local branch `lane-0428-131-en-docs-warning-term`. Base SHA cut from: da76c5cf9c963207038d5599bd130b89ecb1e8a4 (develop; no merge commits were needed — `git merge origin/develop` reported "Already up to date", so the chain is a single linear commit on develop head).

    git merge-base --is-ancestor da76c5cf9c963207038d5599bd130b89ecb1e8a4 HEAD   exit=0 (ancestor)

Log-line (`git log --oneline da76c5cf9..HEAD`), only own commits:

    3448f73e6 docs: use the shipped EN marker term 'Warning' in EN internal docs (0428-131)

## Fundliste (findings, grep -rn "Achtung" vorher)

Command in the worktree at da76c5cf9 (repo root, excluding .git and docs/de/):

    grep -rn "Achtung" docs/ | grep -v "^docs/de/"

Findings — EN documentation spots (all in docs/internal/, English prose strings):

- docs/internal/v0.4.25-installation-destruction-runtime-evidence.json:381 — `"Achtung and two current acknowledgements",`
- docs/internal/v0.4.25-destruction-workspace-checkpoint.json:28 — `...authorizeApplicationDestruction presents Achtung, collects current outer-scope...`
- docs/internal/v0.4.25-external-provider-delivery-source-evidence.json:103 — `...displays concrete source/destination effects with Achtung and two current confirmations...`

Out-of-scope occurrences (documented, NOT changed — product code/tests, mission bound the work to documentation). After the docs fix, the full-tree grep (minus docs/de) shows exactly these four, all correct by design:

- cmd/baha/provider_change_confirmation_test.go (2 lines): DE-locale test fixtures asserting the German catalog genuinely renders 'Achtung' — correct by design.
- cmd/baha/cli_consent_i18n_test.go (2 lines): same class, DE-locale i18n assertions.

No mkdocs nav exclusion: docs/internal/** is listed in mkdocs.yml:10 only as exclude from the site; the files remain repository documentation and are inside the grep scope the card defines.

## Aenderungsliste (one documentation-spot correction per finding)

Exactly the word 'Achtung' -> 'Warning'; no content, sentence-structure or other-word changes. German files untouched (`git status --short docs/de` empty).

- docs/internal/v0.4.25-installation-destruction-runtime-evidence.json:381 -> `"Warning and two current acknowledgements",`
- docs/internal/v0.4.25-destruction-workspace-checkpoint.json:28 -> `...presents Warning, collects...`
- docs/internal/v0.4.25-external-provider-delivery-source-evidence.json:103 -> `...effects with Warning and two current confirmations...`

Diffstat: 3 files changed, 3 insertions(+), 3 deletions(-).

## Grep nachher (control, at candidate 3448f73e6)

    grep -rn "Achtung" docs/ | grep -v "^docs/de/"        -> empty (exit 1)
    grep -rn "Achtung" docs/ --include="*.md" | grep -v "^docs/de/"   -> empty (card step-4 form)

All three edited JSON files re-parsed with python3 json.load — OK.

## CI coverage of the docs check (no .github change needed)

Existing docs-audit runs in the affected CI group already; none of these files required a workflow or trigger edit, so no Owner-scope finding:

- scripts/pr-gate-plan.py:24 registers validation id 'documentation-audit' -> `bash scripts/documentation-audit.sh`, executed by the `PR · Validation · documentation-audit` case at .github/workflows/ci.yml:1186.
- The same script also runs inside the `Validate documentation` steps at .github/workflows/ci.yml:140 (release_source_preflight), :322 (validate, push events) and :599 (main_release_source, main-targeting PRs).
- mkdocs strict EN build (which would catch rendered-HTML regressions) runs per scripts/pr-gate-plan.py:26 -> .github/workflows/pages.yml:build and via the same Validation dispatch.
- Local reproduction on the candidate: `bash scripts/documentation-audit.sh` -> all groups PASS (exit 0), including the locale/governance groups.

## Candidate + PR + run

- Branch: lane-0428-131-en-docs-warning-term (single candidate per chain, no second branch; ls-remote showed no pre-existing remote lane for this card).
- Head SHA: 3448f73e697cd7fdb1a338ef8422b5d484bbe814
- PR: https://github.com/mcpdev80/baseharbor/pull/1697 (base develop, one PR per card)
- CI run: 44478483899 ("CI · Source & Quality", headSha 3448f73e6...) — watched by this session via `gh run watch --exit-status`, exit 0.
  - terminal result: status=completed, conclusion=success. 14 jobs success (incl. Workflow policy, PR · Source format, PR · Native gate plan, PR · Trusted Plan, PR · Validation · go-build/go-vet, PR · Focused Python, PR · Go unit · cli-0..3/packages/owner, PR Selected Checks); all remaining jobs SKIPPED by their documented `if:` conditions (base_ref==main gates, native runtime gates not selected for a docs-only diff, validate = non-PR path).
  - observation: no `PR · Validation · documentation-audit` job materialized in this run — scripts/pr-gate-plan.py offers it but the plan did not select it for the docs/internal-only diff. My candidate was nonetheless format/readability-green and my local `bash scripts/documentation-audit.sh` is PASS. The card's acceptance sentence "ein docs-check laeuft in der betroffenen CI-gruppe mit (bestehender docs-audit genuegt)" is met by the existing registration (pr-gate-plan.py:24, ci.yml:1186/:322/:599); if the coordinator wants documentation-audit force-selected for docs/** paths, that selection lives in pr-gate-plan.py / the plan output — flagged here, not a .github defect.

## Cleanliness

- BEFORE (this host; no containers were started by this lane): `docker ps -aq` = 7 (all ambient `bh-local-shared-*` projects of other lanes/core images, untouched), `podman ps -aq` = 0.
- No containers, networks, volumes or state directories were created by this lane; AFTER must equal BEFORE.
- AFTER: `docker ps -aq` = 7 (same seven `bh-local-shared-*` ambient containers, byte-identical names), `podman ps -aq` = 0. Host unchanged by this lane.
- cleanliness: host besenrein — this lane started no containers, compose projects, networks, volumes or state directories; before/after counts equal (7/0 docker ambient-only, 0 podman).

## repo-rule compliance

- Docs-only change; no product code, no .github/** edits, no merge, no CODEX verdict, no subagents (§4.8).
- German files unchanged (owner requirement); exact-word replacement only.
- Worktree isolated under /var/tmp/en-docs-warning-term-wt; evidence lives only in baseharbor-plan.

END_DONE mission-en-docs-warning-term.md: candidate 3448f73e697cd7fdb1a338ef8422b5d484bbe814, PR #1697 (base develop), CI run 44478483899 terminal SUCCESS (observed by this session); docs/internal EN 'Achtung' -> 'Warning' at 3 spots, docs/de untouched, grep control empty; host clean (docker 7 ambient / podman 0, before==after).
