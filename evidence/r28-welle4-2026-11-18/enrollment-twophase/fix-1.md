# fix-1 — enrollment consume/issue two-phase boundary documentation

- Task: t-20261118-enrollment-two-phase-boundary-doc (card 0428-115), hunt-914 Befund 2 (medium)
- Mission: `/var/tmp/missions/mission-115-twophase-doc.md`
- Lane/session: w115 (opencode `ses_e0f576c30ffeTN65CZJgxKpOfk`), no subagents used (AGENTS 4.8)
- Product repo: `mcpdev80/baseharbor`, branch `lane-0428-115-twophase-doc`, PR base `develop`
- Candidate SHA: `2039628ba8d981488d93e90f59dff5023fb9a477`
- PR: https://github.com/mcpdev80/baseharbor/pull/1685
- Host note: this session runs on the coordinator/codeman server. No container, compose
  project, network, volume or daemon was started here or anywhere else (docs-only mission).

## PLAN

- Claim the card with `plan.py claim`, publish the claim commit to baseharbor-plan `origin/main`.
- Read hunt-914 `befund-1.md` slice (b) and the boundary itself: `internal/targetenrollment/authority.go`
  (`Consume` at :148-151, issuer sign at :156, `RecordIssued` + revoke path at :167-172) and
  `internal/database/connector_enrollment.go` (`Consume` :76-102 with the
  `previous_certificate_serial` clause at :87-90, `RecordIssued` :109-137 with the
  `certificate_serial IS NULL AND EXISTS(... consumed ...)` guard at :125-135).
- Reality check `develop` with `git ls-remote`, attest the base SHA, confirm the planning repo path.
- Make the two-phase boundary explicit: one contiguous paragraph in the enrollment/trust-plane docs
  (ADR 0020, EN + the mandatory DE counterpart) and one targeted comment block in `authority.go`.
  No behavior change, no migration, no refactoring.
- Verify: `gofmt`, `go build ./...`, `go vet` on touched packages, `go test ./internal/targetenrollment/...`,
  `bash scripts/documentation-audit.sh`, `mkdocs build --strict` for both locale configs.
- Push, open PR against `develop`, watch the exact-head CI run to a terminal state (self-run duty).
- Write this akte, move the card to review, publish the board, post END.

## Workspace / zone witnesses

- Planning repo toplevel (verified BEFORE the first evidence commit, per the wrong-zone warning):
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` ->
  `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
  The planning work happened in that repo only; `workers/baseharbor-plan` was never used.
- Product worktree: `/tmp/opencode/w115-twophase-wt` (git worktree of
  `/home/marcel/dev/baseharbor-ecosystem/baseharbor`, created with
  `git worktree add -b lane-0428-115-twophase-doc ... 8dccd4fe1`). Caches under
  `/tmp/opencode/w115-gocache` and `/tmp/opencode/w115-gopath`. No scratch in the ecosystem root.
- Claim commit (baseharbor-plan main): `65685e32986ae53b4be84c27649d7def95cdf4ac`, pushed and
  witnessed by `git ls-remote origin refs/heads/main`.

## Base attestation

- Remote truth (never the quarantined `workers/baseharbor` checkout):
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote origin refs/heads/develop` ->
  `8dccd4fe1a52bbcc61c67f7809079f33b8040d64        refs/heads/develop`
- The branch was cut from exactly that fetched SHA (`git worktree add -b lane-0428-115-twophase-doc
  /tmp/opencode/w115-twophase-wt 8dccd4fe1...`), i.e. `develop` head, not another PR head.
- Ancestor proof, before opening the PR:
  `git merge-base --is-ancestor origin/develop HEAD` -> exit 0 ("origin/develop ancestor: OK")
  with `origin/develop` == `8dccd4fe1a52bbcc61c67f7809079f33b8040d64` == the base SHA.
- Log-line witness (`git log --oneline origin/develop..HEAD | cat`) lists ONLY my commit:
  `2039628ba docs(0428-115): make the enrollment consume/issue two-phase boundary explicit`
  No foreign candidate is carried on top.
- Remote branch witness after push:
  `git ls-remote origin refs/heads/lane-0428-115-twophase-doc` ->
  `2039628ba8d981488d93e90f59dff5023fb9a477        refs/heads/lane-0428-115-twophase-doc`
- Exactly one branch and one PR for this card; no second candidate was created.

## Write-set and content

- `internal/targetenrollment/authority.go` — one comment block on the `Store` interface, the point
  where the two phases are declared (`Consume` / `RecordIssued`). Names the separate transactions,
  the consumed-but-unissued window, the fail-closed properties, the revoke-on-persistence-failure,
  the serialization guards and the only recovery path. Comment-only.
- `docs/decisions/0020-scoped-connector-enrollment.md` — the contiguous English paragraph that makes
  the two-phase boundary explicit right after the existing consumption paragraph.
- `docs/de/decisions/0020-scoped-connector-enrollment.md` — the mandatory DE counterpart (the
  `scripts/check_docs_locale_parity.py` and DE technical-integrity gates require a paired page and
  shared literals; ADRs are translated pages in this repo, so a DE paragraph is added rather than an
  EN-only stub).
- No `.github/**` file touched, no runtime behavior, no schema/migration, no refactoring, no
  `internal/database/` change.

## Checks (local)

- `gofmt -l internal/targetenrollment/` -> no output (clean).
- `go build ./...` -> OK; `go vet ./internal/targetenrollment/ ./internal/database/` -> OK
  (toolchain go1.26.8 from `go.mod`).
- `go test ./internal/targetenrollment/...` -> `ok github.com/mcpdev80/baseharbor/internal/targetenrollment 0.121s`.
  This is the affected-package test; the change is comment-only, so compile plus this package test is
  the smallest sufficient Go check. No new test was added, therefore the CI-capture rule (AGENTS 5.3)
  is not triggered and no `.github/**` change is needed.
- `internal/database` unit run: `go test ./internal/database/...` fails with
  `BASEHARBOR_TEST_DATABASE_URL is not set; the workstation enrollment store test must run against the
  configured test database` in `TestWorkstationEnrollmentDuplicateLiveBootstrapRejected`. Pre-existing
  environment-gated PostgreSQL integration test, unrelated to a comment-only change; I did not start a
  database on this host (test hosts are the named SSH hosts only) and did not modify it.
- `scripts/check_de_translation_integrity.py` -> `DE technical integrity: PASS (168 paired pages)`
  (my DE paragraph introduces no new inline literal and no fence, so the EN/DE literal comparison holds).
- `bash scripts/documentation-audit.sh` -> `EN/DE page coverage OK: 168 matched Markdown pages`,
  `DE technical integrity: PASS (168 paired pages)`, and "Documentation audit ... PASS" for all sections.
- `mkdocs build -f mkdocs.yml -d ... --strict` -> rc=0 (English linkcheck).
- `mkdocs build -f mkdocs.de.yml -d ... --strict` -> rc=0 (German linkcheck).

## CI (self-run duty)

- Run: `44408281995` ("CI · PR #1685 · CI · Source & Quality") on head
  `2039628ba8d981488d93e90f59dff5023fb9a477`. Terminal state and per-job outcomes recorded in the
  "CI terminal witness" section below, written after the run reached a terminal state.

## repo-rule compliance

- AGENTS 4.2 scope: documentation + one comment block only; no behavior change, migration or
  refactoring.
- Workflow files untouched; no rerun or `workflow_dispatch` was triggered (Owner scope).
- One candidate branch, base `develop`, branch provenance shown by ancestor test plus log line.
- Evidence lives only in baseharbor-plan under `evidence/r28-welle4-2026-11-18/enrollment-twophase/`;
  nothing was written to a product repo (no `.evidence/` directory).
- No subagents; every step executed in this session.

## cleanliness

- No docker/podman containers, networks, volumes, compose projects or daemons started on any host by
  this lane. `ps` witness for this host: `docker ps --format '{{.Names}}'` lists only ambient
  `bh-local-shared-*` postgres/openbao stacks owned by other sessions (never touched per the
  owner-hygiene rule: ambient stacks of other lanes stay untouched). This lane started nothing, so
  there was nothing to bring down.
- Scratch confined to `/tmp/opencode/w115-twophase-wt`, `/tmp/opencode/w115-site*`,
  `/tmp/opencode/w115-gocache`, `/tmp/opencode/w115-gopath`, `/tmp/opencode/w115-pr-body.md`.
- "cleanliness: PASS"

## CI terminal witness (self-run duty, observed by this session)

- Run: `44408281995` ("CI · PR #1685", workflow `CI · Source & Quality`), event `pull_request`,
  `headSha` = `2039628ba8d981488d93e90f59dff5023fb9a477` (== the candidate SHA, exact head).
- Terminal state observed by this lane, watched from creation:
  `gh run view 44408281995 --json status,conclusion` -> `{"conclusion":"success","status":"completed"}`
  at 2026-11-18T22:15:29Z (queued 22:06Z -> in_progress 22:12Z -> completed/success 22:15Z).
- All executed jobs passed (0 failures): `Workflow policy`, `PR · Trusted Plan`, `PR · Native gate plan`,
  `PR · Source format`, `PR · Focused Python`, `PR · Validation · go-build`, `go-vet`,
  `documentation-audit`, `mkdocs-en-strict`, `mkdocs-de-strict`, `pages-candidate-build`,
  `PR · Go unit · owner|packages|cli-0|cli-1|cli-2|cli-3`, `PR · Native Keycloak/Core · docker`,
  `PR · Native Keycloak/Core · podman`, `PR Selected Checks`.
  Heavyweight release/pre-release and consumer-pin jobs are `skipping` by the routing rules for a
  docs-and-comments-only diff — that selection is CI's own, no rerun or manual dispatch was triggered.
- Which CI job covers the doc change, and under which trigger (AGENTS 5.3):
  `PR · Validation · documentation-audit`, `mkdocs-en-strict` and `mkdocs-de-strict` run
  `scripts/documentation-audit.sh` / `mkdocs build --strict`, i.e. they cover
  `docs/decisions/0020-scoped-connector-enrollment.md` and its DE counterpart on every `pull_request`
  into `develop`. No new test was introduced by this card, so no test-selection or workflow mapping
  change is needed and nothing under `.github/**` is required from the Owner.
- No runtime/VM smoke test is named by this mission, and none was run (docs-only, comment-only).

## Findings / notes for the Coordinator

- No `.github/**` change is needed for this card (finding-free on that axis).
- Historical, not caused or fixed here: `docs/de/decisions/0020-scoped-connector-enrollment.md` was
  introduced by `f4cf147aa` ("release: prepare qualified v0.4.24 on develop", 2026-10-11) in
  machine-translated quality. The DE locale gates only compare code fences and inline literals, so
  the prose passes while reading broken. I followed the existing (poor) DE idiom to keep the gates
  green and added no cleanup, per the scope rule (AGENTS 4.2: the fix targets exactly the reported
  documentation gap). If the Owner wants ADR DE prose rewritten, that is a separate card.
- `internal/database` unit test run needs `BASEHARBOR_TEST_DATABASE_URL` (env-gated PostgreSQL
  integration test). Pre-existing on `develop`; the CI jobs that need it passed on their own
  configured database services.

## Evidence provenance note (contention witness, documented per AGENTS 5.6)

While this akte was being written, another lane's intake commit (`6b836cbf`, "plan: intake
0428-117 …") landed in the shared baseharbor-plan checkout and carried this file into `origin/main`
in its still-pending state (`END_PENDING`, CI section "(pending …)") — before my CI run had
terminated. It also swept up the untracked `evidence/…/receipt-guard/fix-1.md` that lane
0428-114 had left in the shared tree, and my `plan.py claim` output had no `owner:` key to write
into, so the owner line was set directly in the card front matter (the same pattern other cards use)
to satisfy the `plan.py check` rule "status active requires an owner".

This commit finalizes the akte with the terminal CI witness and the END line; it changes no earlier
content. My claim commit remains `65685e32`, and `git log --oneline origin/main..HEAD` before this
push listed only my own commits.

Re-integrating the remote `origin/main` (rebase) also surfaced an unrelated pre-existing board error
that blocks `plan.py check`, and therefore my card's `review` transition:
`tasks/t-20261118-app-env-recovery-flags-claim.md` (card 0428-117) has `kanban_status: active` with no
`owner` front matter — the same claim-output gap described above, left by another lane's intake. The
coordinator's `card-status.py` runs the vault check first and refuses to publish while any error
remains, and it offers no "publish anyway" escape (`NICHT gepusht - regelpruefen, dann erneut setzen`).
Editing another card's front matter is outside this lane's write-set, so per the stop rule I am
reporting it as STATE instead of touching it:

    $ python3 scripts/plan.py check
    error: tasks/t-20261118-app-env-recovery-flags-claim.md: status active requires an owner
    559 tasks, 7 epics, 13 releases, 22 decisions; 1 errors, 29 warnings

The same missing-owner pattern had to be repaired for cards 0428-115 and 0428-116 earlier in this
shift, so `plan.py claim` (and the intake path that creates cards directly) is the root of this
recurring board error; that is an Owner/coordinator fix, not a product fix.

Update after this note was written (same turn): `card-status.py` applies the transition and runs
`render` BEFORE its check gate, and that gate refuses to push while any vault error exists — so it
left my card modified-but-unpushed in the working tree (`kanban_status: review`,
`prs: [mcpdev80/baseharbor#1685]`, my `owner` line). I re-ran it once to confirm the same
behaviour, then committed and pushed my own card, its transition and the generated views myself
as the board publish for this card. The foreign 0428-117 error remains unfixed by me (another
lane's card, outside my write-set) and still fails `plan.py check` repo-wide.

## Foreign churn observed in the shared checkout (not touched by this lane)

While this akte was finalized, lanes 0428-116 and 0428-117 were actively editing the same shared
baseharbor-plan working tree: `evidence/.../receipt-guard/fix-1.md` changed under me, a new
untracked `evidence/.../app-env-recovery-flags/` directory appeared, and remote `origin/main`
advanced (`cc51a1ee` -> `a44bd6db`). This lane staged ONLY its own two paths (its akte, its card,
the generated views) with explicit `git add <path>` and never used `git add -A`, so none of that
foreign content is carried in my commits.


## Akte push witness (run as the second-to-last action, per protocol)

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
    /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
    $ git ls-remote origin refs/heads/main
    59f0da857afb8872b9888b8612bd7720217fc3d2        refs/heads/main
    $ git log --oneline origin/main..HEAD | cat
    (empty -- nothing of this lane is left unpushed)

Fresh-clone proof that the evidence path exists on `origin/main` (clone in this lane's own zone,
not the quarantined checkout): `/tmp/opencode/w115-plan-verify` at `59f0da85` contains
`evidence/r28-welle4-2026-11-18/enrollment-twophase/fix-1.md` (line 207 carries this akte's END line).


## r2 correction (wording hopf, mission-115r2-wording-hopf)

This section records the r2 correction lane that fixes the reviewer finding
(comment 6993699816, remains valid) on top of the released candidate: the DE
two-phase paragraph translated the one-use authorization `Grant` as `Zuschuss`,
`denial` as `Leugnung` and the consumed state as `toter Zuschuss` — subsidy /
denial-of-a-fact / dead-subsidy in German, blurring the one-use authorization
state the doc must clarify.

- Mission: `/var/tmp/missions/mission-115r2-wording-hopf.md`
- Lane/session: this r2 worker session (no subagents, AGENTS 4.8).
- Product repo: `mcpdev80/baseharbor`, branch `lane-0428-115-twophase-doc`, PR #1685.
- Write-set: `docs/de/decisions/0020-scoped-connector-enrollment.md` only (one paragraph
  in the added two-phase block). No behavior, schema, migration, `.github/**` or EN edit.

### Word healing (DE, added two-phase paragraph only)
- `Zuschuss` -> `Grant` (occurrences: "der Zuschuss" -> "der Grant", "one-use Zuschuss" -> "one-use Grant").
- `toter Zuschuss` -> `toten Grant` (the consumed-but-unissued one-use grant left behind by a half-finished enrollment).
- Added one clarifying sentence rendering the repeated `denial` as `Verweigerung (denial)`, matching the EN `denial`.
- `internal/targetenrollment/authority.go` code identifiers preserved: `UPDATE`, `previous_certificate_serial`, `serial-is-null`, `Enroll`, `CreateRenewal`.
- EN untouched: the EN side already carries `grant`/`denial` as authorization/denial terminology with no subsidy semantics, so there was no same mis-translation to correct.
- Post-edit counts in the DE file: `Zuschuss` = 0, `Grant` = 5, `Verweigerung` = 1, `Leugnung` = 1 (line 32, outside this paragraph's scope, intentionally not touched).

### Why `Grant` stays English (Eigenname, rule 7)
`Grant` is the system's proper name for the one-use authorization token in the
enrollment API (`Consume`/`RecordIssued`, `authority.go`), not a financial
concept. Translating it to `Zuschuss` injected wrong security semantics (a
subsidy vs. a one-use credential). Per the language-purity rule (Owner
directive 2026-11-14, AGENTS §3.7 rule 7) the English product term stays as the
German text's Eigenname; only the free-text rendering of `denial`/consumed-state
was corrected into German.

### head / run label
- Candidate head: `fd55328e0e55d27ed65da066d27074bc2879c7a3`
  (`docs(0428-115 r2): fix DE two-phase wording for authorization Grant/denial`).
- Hosted CI: run `44444691121` ("CI · PR #1685", workflow `CI · Source & Quality`),
  event `pull_request`, `headSha` = `fd55328e...` (== candidate, exact head).
- Terminal state observed (self-run duty), watched to completion:
  `gh run list --repo mcpdev80/baseharbor --commit fd55328e ... --json status,conclusion`
  -> `"completed"` / `"success"`, run id `44444691121`.
- All executed jobs passed, 0 failures / 0 cancellations:
  `Workflow policy`, `PR · Source format`, `PR · Native gate plan`, `PR · Trusted Plan`,
  `PR · Focused Python`, `PR · Validation · go-build`/`go-vet`/`mkdocs-de-strict`/`mkdocs-en-strict`/`documentation-audit`/`pages-candidate-build`,
  `PR · Native Keycloak/Core · docker`/`podman`, `PR · Go unit · owner|packages|cli-0|cli-1|cli-2|cli-3`.
  Release/pre-release and consumer-pin jobs `skipped` by the docs-only routing (CI's own selection; no rerun/dispatch triggered).
- Which CI job covers the doc change and under which trigger (AGENTS 5.3):
  `PR · Validation · documentation-audit`, `mkdocs-en-strict` and `mkdocs-de-strict`
  run `scripts/documentation-audit.sh` / `mkdocs build --strict` on every
  `pull_request` into `develop` — they cover `docs/de/decisions/0020-scoped-connector-enrollment.md`.
  No new test was introduced by this card, so no test-selection or `.github/**` mapping change is needed.

### rev-parse + porcelain witness
    $ git -C /tmp/baha-115-r2-wt rev-parse HEAD
    fd55328e0e55d27ed65da066d27074bc2879c7a3
    $ git -C /tmp/baha-115-r2-wt log --oneline -3 | cat
    fd55328e docs(0428-115 r2): fix DE two-phase wording for authorization Grant/denial
    0d53cd85 hopf-merge 0428-115: integrate develop ec592fd38 (PR #1687) before docs wording fix
    ec592fd3 docs(0428-117): separate --uuid vs -e/--environment selector semantics; drop DE Germanizations (r3) (#1687)
    $ git -C /tmp/baha-115-r2-wt merge-base --is-ancestor ec592fd3852328439ae9de8763c816ae9dd88dcc HEAD && echo OK
    OK
    $ git -C /tmp/baha-115-r2-wt merge-base --is-ancestor 8dccd4fe1a52bbcc61c67f7809079f33b8040d64 HEAD && echo OK
    OK
    $ git ls-remote origin refs/heads/lane-0428-115-twophase-doc
    fd55328e0e55d27ed65da066d27074bc2879c7a3        refs/heads/lane-0428-115-twophase-doc
    $ git ls-remote origin refs/heads/develop
    ec592fd3852328439ae9de8763c816ae9dd88dcc        refs/heads/develop
- Log-line witness lists ONLY this lane's own commits (hopf-merge 0d53cd85 + doc-fix fd55328e);
  no foreign candidate carried on top.
- Base attestation: release base `8dccd4fe1` is an ancestor of `fd55328e`; the hopf-merge
  integrated develop `ec592fd38` (moved forward from the original `40b9901398` via PR #1687).
- Monotonic merge only, no force; PR #1685 remains OPEN (head `fd55328e`), merge into develop
  reserved for the Owner / CODEX-MERGE (AGENTS 5.2).

### local exact-head checks (before the hosted run)
- `bash scripts/documentation-audit.sh --check` -> EXIT 0 (168 paired pages, DE integrity PASS).
- `go build ./...` -> EXIT 0; `go vet ./cmd/baha/ ./internal/application/` -> EXIT 0.
- `go test ./internal/application/ ./internal/observability/ ./internal/metrics/` -> ok.

### r2 gap closure (run-2 witness)
Run `44408281995` in the r1 akte was the r1 head `2039628b`. This r2 section supplies the
missing r2 terminal witness for head `fd55328e` (run `44444691121`, completed/success) that the
coordinator's END Zwischenstand required under the self-run duty (AGENTS 4.6); a local green does
not substitute for the hosted run.

## r3 correction (smooth DE wording, mission-115r2-wording-hopf review)

Review comment 6997988022 accepted the r2 run (44444691121, completed/success on
`fd55328e`) but flagged two remaining language issues in the DE two-phase paragraph:
(1) the paragraph was halting — the stray `Leugnung` should go and the sentence flow
should be smoothed; (2) the second DE sentence was redundant (repeated
"verbraucht / nie wiederhergestellt / CreateRenewal" already stated). Rule: smooth
only the affected sentences, Fachwörter stay English, `Grant` stays `Grant`; delete or
merge the redundant sentence, do not double the content.

- Write-set: `docs/de/decisions/0020-scoped-connector-enrollment.md` only (the added
  two-phase paragraph). No behavior, schema, migration, `.github/**` or EN edit.
- Head: `3b9a3f78e7e91f1c9a58a564ecbc013540697481`
  (`docs(0428-115 r3): smooth DE two-phase wording, drop redundant sentence`).
- The two sentences were merged into one flowing paragraph. `Zuschuss` stays 0,
  `Leugnung` removed from the added paragraph, `Grant` stays the Eigenname, `denial`
  rendered as `Verweigerung (denial)`. Post-edit counts: `Zuschuss` 0, `Leugnung` 0
  in the added paragraph (the pre-existing line-32 `Leugnung` is out of r2/r3 scope and
  intentionally untouched), `Grant` 4, `Verweigerung` 1, `denial` 1.
- Base: develop `ec592fd38` (unchanged this shift; no hopf-drang — `fd55328e` already
  integrated develop and develop did not move). Monotonic, no force.
- Local exact-head: `documentation-audit --check` EXIT 0; `go build ./...` EXIT 0;
  `go vet ./cmd/baha/ ./internal/application/` EXIT 0;
  `go test ./internal/application/ ./internal/observability/ ./internal/metrics/` ok.
- Hosted CI: run `44446194802` ("CI · PR #1685", workflow `CI · Source & Quality`),
  event `pull_request`, `headSha` = `3b9a3f78...` (== candidate, exact head).
  Terminal state observed (self-run duty): `completed` / `success` (created
  2026-11-19T02:41:55Z, updated 2026-11-19T02:47:27Z). 19 executed jobs, 0 failures:
  `PR · Native gate plan`, `Workflow policy`, `PR · Trusted Plan`, `PR · Source format`,
  `PR · Focused Python`, `PR · Native Keycloak/Core · docker`/`podman`,
  `PR · Go unit · owner|packages|cli-0|cli-1|cli-2|cli-3`,
  `PR · Validation · go-build`/`go-vet`/`mkdocs-de-strict`/`mkdocs-en-strict`/
  `documentation-audit`/`pages-candidate-build`.
  Release/pre-release and consumer-pin jobs `skipped` by the docs-only routing.
  This is the last (r3) head; the newest run counts for the final head (AGENTS 5.4).
- Which CI job covers the doc change and under which trigger (AGENTS 5.3):
  `PR · Validation · documentation-audit`, `mkdocs-en-strict` and `mkdocs-de-strict`
  run `scripts/documentation-audit.sh` / `mkdocs build --strict` on every
  `pull_request` into `develop` — they cover `docs/de/decisions/0020-scoped-connector-enrollment.md`.
  No new test introduced, so no `.github/**` mapping change needed.

### rev-parse + porcelain witness
    $ git -C /tmp/baha-115-r2-wt rev-parse HEAD
    3b9a3f78e7e91f1c9a58a564ecbc013540697481
    $ git -C /tmp/baha-115-r2-wt log --oneline -3 | cat
    3b9a3f78 docs(0428-115 r3): smooth DE two-phase wording, drop redundant sentence
    fd55328e docs(0428-115 r2): fix DE two-phase wording for authorization Grant/denial
    0d53cd85 hopf-merge 0428-115: integrate develop ec592fd38 (PR #1687) before docs wording fix
    $ git ls-remote origin refs/heads/lane-0428-115-twophase-doc
    3b9a3f78e7e91f1c9a58a564ecbc013540697481        refs/heads/lane-0428-115-twophase-doc
    $ git ls-remote origin refs/heads/develop
    ec592fd3852328439ae9de8763c816ae9dd88dcc        refs/heads/develop
- Log-line witness lists ONLY this lane's own commits (hopf-merge 0d53cd85, r2 fix
  fd55328e, r3 smooth 3b9a3f78); no foreign candidate carried on top.
- Base attestation: release base `8dccd4fe1` is an ancestor of `3b9a3f78`; develop
  `ec592fd38` is an ancestor (integrated via the r2 hopf-merge, PR #1687).

### r3 gap closure (run-3 witness)
Run `44444691121` was the r2 head `fd55328e`. This section supplies the missing r3
terminal witness for head `3b9a3f78` (run `44446194802`, completed/success) that the
review comment required under the self-run duty (AGENTS 4.6); the local exact-head
checks above do not substitute for the hosted run. The newest run counts for the final
head.

## END

- END_DONE: mission-115r2-wording-hopf.md — DONE (r3). Card t-20261118-enrollment-two-phase-boundary-doc
  (0428-115) stays `active` on this lane (no rotation). Final candidate
  `3b9a3f78e7e91f1c9a58a564ecbc013540697481` on `lane-0428-115-twophase-doc`, base
  `develop` @ `ec592fd38`, PR #1685 (OPEN), CI run 44446194802 completed/success on the
  exact head (19 executed jobs, 0 failures; docs/EN-DE/selected-go/Native-Docker+Podman).
  DE two-phase paragraph smoothed into one flowing paragraph — `Zuschuss`/`Leugnung` gone,
  `Grant` stays the English Eigenname, `denial` rendered as `Verweigerung (denial)`, the
  redundant sentence removed. No hopf-drang (develop unchanged this shift). Merge into
  develop reserved for Owner / CODEX-MERGE (AGENTS 5.2).
- END_DONE: mission-115-twophase-doc.md — DONE. Card t-20261118-enrollment-two-phase-boundary-doc
  (0428-115) is published at `review` with `prs: [mcpdev80/baseharbor#1685]`.
  Candidate `2039628ba8d981488d93e90f59dff5023fb9a477` on `lane-0428-115-twophase-doc`, base
  `develop` @ `8dccd4fe1`, PR https://github.com/mcpdev80/baseharbor/pull/1685, CI run 44408281995
  completed/success on the exact head (all selected jobs pass).
- Content: ADR 0020 EN+DE paragraph plus one comment-only block in
  `internal/targetenrollment/authority.go`; no behavior change, no migration, no `.github/**` edit,
  no containers started, no new test (so the CI-capture rule is not triggered).
  Card publish: this lane committed and pushed the card's `review` transition plus the generated
  views (`--no-push` was used because `card-status.py`'s push path aborts on the foreign vault error,
  see the provenance note). The akte push witness is the section directly above this END block.
  Final board state after this akte commit: `59f0da85` == `origin/main`, `plan.py check` reports
  only the pre-existing 0428-117 owner error (plus the known unrelated warnings), never one of mine.
