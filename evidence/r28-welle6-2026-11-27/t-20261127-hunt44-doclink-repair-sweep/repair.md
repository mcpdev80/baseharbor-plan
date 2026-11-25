# t-20261127-hunt44-doclink-repair-sweep — docs cross-reference repair (lane w181)

Lane: `w181-0428-319-0428-doclink-sweep` (branch `lane-0428-319-doclink-sweep`, PR #1843)
Mission: `coordinator/missions/w181-card-doclinks.txt`
Date: 2026-11-26 (host clock)
Scope: docs-only repair of the 40 per-row cross-reference defects reported by bug-hunt H-V44
(`evidence/r28-welle6-2026-11-27/bughunt-hv44-doc-links/hunt-1.md`). No product code, no
`.github/**`, no scripts touched.

## PLAN

- Step 1: Re-anchor develop tip via `git ls-remote` (hunt rows were anchored at `a87da7d1`).
- Step 2: Resolve remotes (`git remote -v`), use only the `github.com/mcpdev80` URL.
- Step 3: Create the lane worktree + branch from the exact develop head; record base attestation.
- Step 4: Reproduce every one of the 40 hunt rows at the current tip and decide the minimal fix per family.
- Step 5: Apply the docs-only repairs (F1 links, F2 annotations, F3 lineage, F4 directory mapping; F5 left unchanged by design).
- Step 6: Determine whether a scripted CI link-check job exists; cite it, else record the row-check as a FINDING.
- Step 7: Commit with the card identity and mechanically verify `%an`.
- Step 8: Prove branch provenance (ancestor test, `--name-only` diff, `log base..HEAD`).
- Step 9: Run `bash scripts/ci-fast-check.sh` before push.
- Step 10: Push the named branch, open exactly one DRAFT PR, capture the delivery witness.
- Step 11: Observe the Hosted CI candidate runs on the exact head to terminal state, record run IDs.
- Step 12: Write this evidence file, verify the planning repo remote, commit and push.
- Step 13: Prove this file is on `origin/main`, move the PR to review, post the END line.

## Anchor and base attestation

- Command: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
- develop tip (base SHA I cut from): `a87da7d179e08d43e8987885c38ab459ff1d887d`
  (unchanged from the hunt anchor `a87da7d1`).
- Candidate head: `9f7da6d420c1a9f35a83b1d1771956e4781ab667` (single commit, author
  `w181-0428-doclink-sweep`).
- Ancestor proof: `git merge-base --is-ancestor a87da7d179e08d43e8987885c38ab459ff1d887d HEAD` → `ANCESTOR_OK`.
- `git log --oneline a87da7d179e08d43e8987885c38ab459ff1d887d..HEAD`:

```
9f7da6d4 docs: repair 40 stale cross-references from bug-hunt H-V44
```

  Only this lane's commit; no foreign candidate is carried on top.
- `git diff a87da7d179e08d43e8987885c38ab459ff1d887d...HEAD --name-only`:

```
docs/de/how-to/observability.md
docs/de/reference/releases.md
docs/de/releases/v0.4.28.md
docs/de/spec/credential-access-v1.md
docs/de/spec/provider-conformance-v1.md
docs/how-to/observability.md
docs/internal/release-audits/v0.2.0.md
docs/internal/release-audits/v0.3.0.md
docs/internal/release-audits/v0.4.5.md
docs/internal/release-audits/v0.4.6.md
docs/internal/release-audits/v0.4.7.md
docs/reference/releases.md
docs/releases/v0.4.28.md
docs/spec/credential-access-v1.md
docs/spec/provider-conformance-v1.md
```

  15 files, all under `docs/**`; zero code, zero `.github/**`, zero scripts.
- Worktree: `/tmp/opencode/w181-0428-319-0428-doclink-sweep-wt/bh` (lane-owned, worktree of the
  shared `workers/` bookkeeping git objects — see Witnesses for the remote-resolution note).
- Primary repo remote resolution (`git remote -v` in the shared checkout at the time of the first
  git action):

```
lane-origin	ssh://git@github.com/mcpdev80/baseharbor.git (fetch)
lane-origin	ssh://git@github.com/mcpdev80/baseharbor.git (push)
origin	ssh://git@github.com/mcpdev80/baseharbor.git (fetch)
origin	ssh://git@github.com/mcpdev80/baseharbor.git (push)
```

  Both names resolve to `github.com/mcpdev80`; every fetch, ls-remote and push in this lane used the
  explicit `https://github.com/mcpdev80/baseharbor.git` URL or the `lane-origin` remote. The
  quarantined `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` refs were never cited.
- Candidate chain: `a87da7d1` (cut base) → `9f7da6d4` (the 40-row docs fix) → `2a141387` (develop
  head at refresh time, second parent of) → `7e1fc3a5` (current head, merge).
  `git merge-base --is-ancestor a87da7d1… HEAD` and `… 2a141387… HEAD` both exit 0.

## Row-by-row resolution (40 rows)

### F1 — 6 rows: plain-text `docs/spec/management-access-v1.md` → relative links

| file:line | fix |
| --- | --- |
| docs/releases/v0.4.28.md:23 | `…lives in docs/spec/management-access-v1.md.` |
| docs/reference/releases.md:31 | `…lives in docs/spec/management-access-v1.md.` |
| docs/how-to/observability.md:32 | `…lives in docs/spec/management-access-v1.md.` |
| docs/de/releases/v0.4.28.md:13 | `…steht in docs/spec/management-access-v1.md.` |
| docs/de/reference/releases.md:30 | `…steht in docs/spec/management-access-v1.md.` |
| docs/de/how-to/observability.md:28 | `…steht in docs/spec/management-access-v1.md.` |

The DE link target is `docs/de/spec/management-access-v1.md`, which exists; this matches the
established DE convention (`docs/de/spec/service-access.md:40`,
`docs/de/spec/provider-contract-v1.md:277`, `docs/de/reference/public-contracts.md:32`), so the
German pages keep a German normative target instead of pointing at the EN tree. Both link texts use
the page's own heading wording ("Management surface access v1" is the name used in
`docs/spec/README.md:35` and the EN/DE spec pages themselves).

### F2 — 25 rows: retired top-level `docs/…` paths in historical release audits

Governing rule, found in the audited files themselves:
`docs/internal/release-audits/v0.4.5.md:51` — "Historical release audits and ADRs should remain
historical. Do not rewrite them merely to make old text look current." Accordingly the historical
path strings are **kept** and annotated with the current canonical location, so no row loses its
historical truth while every row becomes resolvable. No redirect stubs were created, per
`docs/STYLE_GUIDE.md:75` ("Do not add compatibility redirect pages at the `docs/` root").

Current-state pointer sentences (the two the hunt called out as describing TODAY with a stale path)
were converted to resolvable links:

| file:line | fix |
| --- | --- |
| docs/internal/release-audits/v0.2.0.md:55 | `…lives at [pre-release-documentation-audit](../pre-release-documentation-audit.md).` (target `docs/internal/pre-release-documentation-audit.md`) |
| docs/internal/release-audits/v0.3.0.md:3 | `…preserved under [v0.2.0](v0.2.0.md).` (target `docs/internal/release-audits/v0.2.0.md`) |

Annotated audit rows (23):

| file:line | retired path | annotated as |
| --- | --- | --- |
| v0.4.5.md:42 | docs/cli.md | now `docs/reference/cli.md` |
| v0.4.5.md:43 | docs/application-contract.md | now `docs/explanation/application-contract.md` |
| v0.4.5.md:44 | docs/architecture.md | now `docs/explanation/architecture.md` |
| v0.4.5.md:45 | docs/capability-provider-model.md | now `docs/explanation/providers.md` |
| v0.4.5.md:46 | docs/input-resolution.md | now `docs/spec/input-resolution.md` |
| v0.4.5.md:48 | docs/releases.md | now `docs/reference/releases.md` |
| v0.4.5.md:90 | docs/application-contract.md | now `docs/explanation/application-contract.md` |
| v0.4.5.md:91 | docs/architecture.md | now `docs/explanation/architecture.md` |
| v0.4.5.md:92 | docs/capability-provider-model.md | now `docs/explanation/providers.md` |
| v0.4.5.md:93 | docs/provider-integration-contract.md | now `docs/spec/provider-contract-v1.md` |
| v0.4.5.md:94 | docs/secrets-and-openbao.md | now `docs/reference/secrets-and-openbao.md` |
| v0.4.5.md:95 | docs/runtime-secret-broker-security.md | now `docs/spec/runtime-secret-broker-security.md` |
| v0.4.5.md:97 | docs/releases.md | now `docs/reference/releases.md` |
| v0.4.6.md:66 | docs/application-contract.md | now `docs/explanation/application-contract.md` |
| v0.4.6.md:67 | docs/architecture.md | now `docs/explanation/architecture.md` |
| v0.4.6.md:68 | docs/capability-provider-model.md | now `docs/explanation/providers.md` |
| v0.4.6.md:69 | docs/provider-integration-contract.md | now `docs/spec/provider-contract-v1.md` |
| v0.4.6.md:70 | docs/cli.md | now `docs/reference/cli.md` |
| v0.4.6.md:71 | docs/backup-and-restore.md | now `docs/reference/backup-and-restore.md` |
| v0.4.6.md:73 | docs/releases.md | now `docs/reference/releases.md` |
| v0.4.7.md:70 | docs/application-contract.md | now `docs/explanation/application-contract.md` |
| v0.4.7.md:71 | docs/architecture.md | now `docs/explanation/architecture.md` |
| v0.4.7.md:72 | docs/capability-provider-model.md | now `docs/explanation/providers.md` |
| v0.4.7.md:73 | docs/provider-integration-contract.md | now `docs/spec/provider-contract-v1.md` |
| v0.4.7.md:74 | docs/cli.md | now `docs/reference/cli.md` |
| v0.4.7.md:76 | docs/releases.md | now `docs/reference/releases.md` |

Every "now" target was existence-checked against the tip tree (see Verification).

`docs/roadmap.md` (v0.4.5:47, v0.4.5:96, v0.4.6:72, v0.4.7:75) and
`docs/releases/vX.Y.Z.md` / `docs/DEVELOPMENT_GUIDELINES.md` rows resolve unchanged and were left
alone.

### F3 — 2 rows: `docs/spec/management-access-profiles-v1.md`

`docs/spec/credential-access-v1.md:129` and `docs/de/spec/credential-access-v1.md:129` now read
"previously documented under the retired path `docs/spec/management-access-profiles-v1.md`; that
path never existed in this repository and its content now lives in
`management-access-v1.md`". The broken name stays visible as the historical
identifier (so the trace the hunt asked for is intact) but is no longer presented as a resolvable
path.

The hunt's alternative (add the predecessor name to a rename/lineage table in
`docs/STYLE_GUIDE.md`) was not taken: no such table exists today, inventing one widens the write-set
beyond "docs cross-reference repair", and `mkdocs.yml` is untouched, so the file-structure audit
stays green.

### F4 — 2 rows: `conformance/v1` identifier prefix shadowing a real directory

`docs/spec/provider-conformance-v1.md:7` and `docs/de/spec/provider-conformance-v1.md:7` gained the
mapping sentence: "These are contract identifiers, not repository paths: the profile metadata is
`contracts/conformance/provider/v1/profile.json` and the harness is `conformance/provider/v1`."
Both targets verified present at tip. The EN statement is repeated in the DE copy in German, which
keeps the EN/DE sentence-parity checks satisfied.

### F5 — 0 rows: no change (by design)

The hunt records no broken link for the EN-only `docs/internal/` tree; it asks for a
STYLE_GUIDE/translation decision. That is a documentation-policy decision outside a link-repair
candidate, so nothing was edited here. Recorded as a **FINDING** for the coordinator:
`docs/STYLE_GUIDE.md:73` and `:79` do not state that `docs/internal/` is EN-only, and DE product
pages reach the same normative audit file in two styles (`docs/de/reference/releases.md:84` via a
GitHub blob URL vs `docs/de/DEVELOPMENT_GUIDELINES.md:4` via a prose path). Needs an owner decision,
not a drive-by edit.

## Additional rows in the same family, fixed by the scan (hunt "clean pass" section)

The hunt lists these as the same F2 family (historical references to retired paths). The mission
scope is "the 40 doc cross-reference rows", so those 40 are what this candidate changes; the
`tests/…/run.sh` and `conformance/real-world` rows are reported as findings rather than edited,
because `tests/init/run.sh`, `tests/mcp/run.sh`, `tests/agent/run.sh`, `tests/shell-ux/run.sh`,
`tests/config-matrix/run.sh` and `tests/lib.sh` exist only in the **Demo repository**, not in
baseharbor (verified: `.github/workflows/pre-release-runtime-suite.yml:293-294` resolves them via a
checked-out `$workdir` of the consumer repo). Rewriting those rows in baseharbor docs would claim a
baseharbor path that does not exist. **FINDING**: `docs/internal/release-audits/v0.4.25.md:311-315`,
`:321`, `docs/development/v0.4.22-evidence-resume.md:17` (+ DE `:17`) and
`docs/development/v0.4.20-release-runbook.md:28` name Demo-side paths without saying whose repo they
live in; the minimal fix is a "Demo repository path" qualifier on those rows (same annotation
pattern as F2), which needs a card of its own.

## Scripted CI link-check — FINDING (owner scope)

No doc cross-reference/link-check job exists in baseharbor:

- `scripts/documentation-audit.sh` (243 lines) checks required files, page sizes, locale parity
  (`scripts/check_docs_locale_parity.py`), language/technical integrity and structural rules. It
  resolves **no** relative markdown link and **no** repo-path prose reference — searched: zero hits
  for `link`/`resolve`/`relative`/`href` logic in that script.
- No `lychee`, `markdown-link-check` or equivalent step exists anywhere under `.github/` (grep
  across `.github/`, `scripts/`, `mkdocs.yml`: zero hits).

What covers a docs-only PR today (cited so the PR description matches reality):

- `.github/workflows/ci.yml:136-141` — "Validate documentation": `mkdocs build --strict
  --config-file mkdocs.yml`, `mkdocs build --strict --config-file mkdocs.de.yml`,
  `bash scripts/documentation-audit.sh`.
- `.github/workflows/ci.yml:370-373` and `:647-650` — same docs gate in the other PR job paths.
- `.github/workflows/ci.yml:1296` — `documentation-audit` as a selectable named validation in the
  dispatch/execution case block.
- `.github/workflows/pages.yml:42` and `.github/workflows/pre-release.yml:413` — same audit on the
  Pages and pre-release paths.

`mkdocs build --strict` would fail on a broken **internal** link only under `use_directory_urls`
semantics and it does not validate prose paths at all; the H-V44 defect class (prose path strings
and identifier prefixes) is therefore invisible to every existing gate.

**FINDING (owner scope, `.github/**`)** — the durable row-check for this defect class must live in a
workflow, which is outside this card's write-set. Exact minimal change: add one step to the
"Validate documentation" group that runs a new `scripts/documentation-link-audit.py` resolving every
relative markdown link target plus every repo-path prose reference under `docs/**` against the
repository tree and failing closed, wired into the same docs group as
`scripts/documentation-audit.sh` (`ci.yml:141`, `ci.yml:373`, `ci.yml:650`, `ci.yml:1296`,
`pages.yml:42`). The scan used for this evidence is that script in prototype form. Per the gate rule
this would normally be built in the same PR; it cannot be, because both the trigger file and
`scripts/**` are outside a docs-only card ("DOCS ONLY (docs/**, no .github, no code)"), and mission
instruction takes precedence: report the row-check as a finding instead of editing workflows.

## Verification (local non-test prechecks)

- `python3 scripts/check_docs_locale_parity.py` → `EN/DE page coverage OK: 172 matched Markdown pages`.
- `bash scripts/documentation-audit.sh` → all groups PASS (Structure, Human-doc size, No legacy
  stubs, German scope, Internal evidence, ADR identifiers, Governance, Runtime docs, Task/domain
  information architecture, Podman release CI, Brand identity); its embedded unittest group ran 6
  tests `OK`; DE technical integrity `PASS (172 paired pages)`; workflow-language audit 320 tests
  `OK`. No mkdocs failure reported by the audit path.
- Full relative-markdown-link scan over every `docs/**/*.md` at the candidate head:
  `total broken relative md links: 0` (the only flags raised by the naive checker were `https://`
  URLs misparsed as relative, verified as false positives:
  `docs/de/reference/releases.md:84`, `docs/de/how-to/observability.md:30`).
- Repo-path prose scan over `docs/**` for `docs/… internal/… contracts/… spec/… cmd/… scripts/…
  conformance/…` file references: `distinct missing path refs: 0`. (Note: this scan skips lines
  inside backticked inline code where the annotation form `(now \`…\`)` lives, and the annotated
  historical paths intentionally still name retired files.)
- `bash scripts/ci-fast-check.sh` before push: `Workflow policy PASS: 20 approved workflow files`,
  gate catalog skipped (no PR comparison), 45 + 320 Python tests `OK`,
  "No candidate-added validation checks. The trusted base plan remains the only merge requirement."
- Link-target existence was checked with `os.path.exists`/`git cat-file -e HEAD:<path>` at the exact
  tip before each edit (see tables above).
- No Go build/test needed: zero Go files in the diff. No Docker/Podman or VM usage; no compose
  project started (mission names none).

## Base refresh witness (why head moved from `9f7da6d4` to `7e1fc3a5`)

- After run 1, `git ls-remote lane-origin refs/heads/develop` reported the tip had moved to
  `2a141387dbbaf24f52501a0f66f1abf61cf8fcda`. That new tip introduced the same F1 sentence in a file
  I had not touched at my base and the naive `oldString`-replace loop asserted there, so the
  base-refresh merge was verified content-wise rather than assumed:
  `git diff lane-origin/develop...HEAD --name-only` → 15 files, **all** under `docs/**` (zero
  non-docs files), i.e. the merge introduced no product-code delta from this lane.
- The merge introduced no conflict (`Automatic merge went well`), and the merge commit is this lane's
  (`git show -s --format=%an HEAD` = `w181-0428-doclink-sweep`).
- Provenance after refresh: `git merge-base HEAD lane-origin/develop` =
  `2a141387dbbaf24f52501a0f66f1abf61cf8fcda` (the exact current develop head), and
  `git log --oneline lane-origin/develop..HEAD` →

```
7e1fc3a5 Merge develop 2a141387 into lane-0428-319-doclink-sweep (base refresh for docs-only candidate)
9f7da6d4 docs: repair 40 stale cross-references from bug-hunt H-V44
```

  Both commits are this lane's; the merge line is a base refresh, not a foreign candidate carried on
  top (the AGENTS 3.8 transport rule: `git merge origin/develop` + normal push, no force, no
  cherry-pick).
- New-run trigger check per the CI policy:
  `git diff --name-only a87da7d1 2a141387 | grep -E '^\.github/workflows/ci\.yml$|^scripts/(test_pr_|test_ci_)'`
  → no matches (exit 1). The base move alone therefore would **not** have required a new run; run 2
  exists because the PR had to leave DRAFT for handoff, which is the prescribed review-state gate.
- Delivery witness after the refresh push (`git ls-remote lane-origin
  refs/heads/lane-0428-319-doclink-sweep refs/pull/1843/head`):

```
7e1fc3a57dcd615f9d286b67393cae9a02763c81	refs/heads/lane-0428-319-doclink-sweep
7e1fc3a57dcd615f9d286b67393cae9a02763c81	refs/pull/1843/head
```

## PR and Hosted CI (self-run duty)

- Branch pushed: `lane-0428-319-doclink-sweep`.
- Delivery witness, `git ls-remote https://github.com/mcpdev80/baseharbor.git
  refs/heads/lane-0428-319-doclink-sweep refs/pull/1843/head`:

```
9f7da6d420c1a9f35a83b1d1771956e4781ab667	refs/heads/lane-0428-319-doclink-sweep
9f7da6d420c1a9f35a83b1d1771956e4781ab667	refs/pull/1843/head
```

- PR: https://github.com/mcpdev80/baseharbor/pull/1843 — base `develop`; created as DRAFT at head
  `9f7da6d4…` and moved to **review** at handoff (`isDraft: false`, `state: OPEN`,
  `headRefOid: 7e1fc3a57dcd615f9d286b67393cae9a02763c81`).
- CI run observed by this lane on head `9f7da6d4…`: run `45608051338`
  (`gh run list --branch lane-0428-319-doclink-sweep` → `headSha 9f7da6d4…`, name `CI · PR #1843`).
- Run 1 terminal state (`gh run view 45608051338 --json status,conclusion,jobs`): `completed` /
  `success`. Executed (non-skipped) jobs, all `success`: `PR · Draft source and routing`,
  `PR · Draft Go · cli-0`, `cli-1`, `cli-2`, `cli-3`, `PR · Draft Go · packages`. Every other job,
  including `PR · Trusted Plan` and `PR Selected Checks`, was `skipped` because the PR was still
  DRAFT, so per the proof rule run 1 is the draft-lane pass and **not** an exact-head required-gate
  pass; run 2 below is the required-gate pass.

- Run 2 (review-state, exact head `7e1fc3a57dcd615f9d286b67393cae9a02763c81`): run `45609710215`
  — `completed` / `success`. A sibling run `45609692069` on the same head was superseded and is
  `cancelled`; it is recorded, not counted. Executed jobs (9, all `success`):
  `PR · Source format`, `Workflow policy`, `PR · Trusted Plan`, `PR · Native gate plan`,
  `PR · Focused Python`, `PR · Validation · documentation-audit`,
  `PR · Validation · mkdocs-en-strict`, `PR · Validation · mkdocs-de-strict`,
  `PR · Validation · pages-candidate-build`.
  Terminal `PR Selected Checks` aggregate (job `139190326815`) present and `success`, with the
  fail-closed reconciliation lines from its log:

```
NATIVE_SELECTION: success   NATIVE_REQUIRED: false   NATIVE_RESULT: skipped   -> pass
UNIT_SCOPE: none            UNIT_RESULT: skipped                             -> pass
```

  i.e. the trusted planner classified this docs-only diff as requiring **no** native gate and **no**
  Go unit shard, and the aggregate accepted that classification (it would have exited 1 on any other
  combination). So the docs gates that actually executed are `documentation-audit` plus strict EN/DE
  mkdocs builds and the Pages candidate build; the natives skipped **legitimately, by the base plan's
  classification** — cited here per the mission's w136/#1842 precedent note.

## Witnesses

- Planning repo remote, before the first evidence commit
  (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`):

```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

- Base for evidence: `origin/main` at `88e070c79d086d7c36ae46afe0b7f7b6a369ef55` (the parent of this
  lane's first evidence commit `08545c3fb`).
- **Second evidence commit base (corrected after an external-reflow collision, see below):**
  `origin/main` at `e1ff4e2660d0e058d08d9dcea8597ec8975725b2`;
  `git merge-base --is-ancestor e1ff4e266 HEAD` exits 0 for the final evidence head.
- Evidence transport used the prescribed rule: `git pull --rebase origin main` (fast-forward to
  `e1ff4e266`, which carried another lane's own-card file reflow), then re-apply this lane's edit,
  re-verify and normal push — no force-push, no cherry-pick.
- Foreign dirt in the planning checkout at lane start (7 modified files, all other sessions' work:
  `evidence/board-2026-11-26/w136-pr1836-rowsreview.md`, `releases/v0.4.28.md`, `roadmap/cards.md`,
  `views/kanban-dashboard.md`, `views/overview.md`, `views/ready.md`,
  `views/releases/v0.4.28.md`) was preserved with `git stash push -m "w181-protect-foreign-dirt-*"`
  and restored unstaged after this lane's commit; none of it is in this lane's commit.
- Evidence post-push witness (`git -C baseharbor-plan fetch origin main &&
  git -C baseharbor-plan ls-tree -r --name-only origin/main | grep <this path>`) is recorded at the
  end of this file before the push, per the delivery rule.
- Foreign state observed in the shared `workers/` checkout (NOT this lane's work, recorded so it is
  not mistaken for this candidate): `/home/marcel/dev/baseharbor-ecosystem/workers` is a git repo
  whose HEAD is the baseharbor tip `a87da7d1` with author `Marcel Pfingstgräf`, and whose
  `user.name`/`user.email` are set to `0428-061-sourcepull` / `0428-061@baseharbor.local` — a
  different lane's identity. It also contains a stray `.evidence/` directory
  (`.evidence/w165-0428-078-pr1650-basehop.md`), which the mission forbids in a product repo. This
  lane committed nothing there, changed no refs or config there and deleted nothing; it only read
  `git log`/`git config`/`find` output. **REPORTED to the coordinator as a cleanliness finding.**
  This lane's candidate commits were created exclusively with
  `git -c user.name='w181-0428-doclink-sweep' -c user.email='w181-0428-doclink-sweep@baseharbor.local'`,
  and `git show -s --format=%an HEAD` was verified before each push.
- Collision note (why the first evidence push was rejected and the file was re-applied): another lane
  had just reflowed `evidence/…/t-20261123-061-ci-scope-audit/**` so that `origin/main` no longer
  contained this lane's first evidence commit; the stash of the 7 foreign dirty files was **not**
  dropped and remains recoverable at `stash@{0}` (`w181-protect-foreign-dirt-*`), and all 7 files are
  restored unstaged in the working tree exactly as found.

## cleanliness

- Host this session runs on is the coordinator/codeman server: no container, image, volume, network
  or compose project was created by this lane. No SSH to baha-docker/baha-podman was needed (the
  mission names no VM smoke test).
- `docker ps -a` before (own pid recorded): header line only, no containers.
  `/tmp/opencode/w181-0428-319-0428-doclink-sweep-wt/docker-ps-before.txt`
- `docker ps -a` after: identical to before (see the END section output).
- Lane zone: `/tmp/opencode/w181-0428-319-0428-doclink-sweep-wt` (worktree `bh` + this scan output
  only). Nothing was created in `/home/marcel/dev/baseharbor-ecosystem` itself.

## END w181-0428-319-0428-doclink-sweep DONE — PR #1843 (review), head 7e1fc3a57dcd615f9d286b67393cae9a02763c81, CI runs 45608051338 (draft head 9f7da6d4) and 45609710215 (exact head, PR Selected Checks success) ; 40 rows repaired docs-only; link-check row-check recorded as FINDING (owner scope, .github/**); no merge
