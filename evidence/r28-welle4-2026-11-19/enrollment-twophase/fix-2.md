# Evidence: mission-115r2-wording-hopf — card 0428-115 (t-20261118-enrollment-two-phase-boundary-doc), PR #1685

Lane: this session (flash worker), r3 correction round. Branch: `lane-0428-115-twophase-doc`
(exactly one candidate per chain). Reviewer context: comment 6993699816 (r2) + REQUEST CHANGES
6998325146 on head 3b9a3f78e (2026-11-19). Final candidate: `711e04c303e7ca00eb9d34d4d7af1f504842a546`.

## PLAN (completed — board file: workers/todos/mission-115r2-wording-hopf.md.json)

Note: this session exposes no native todowrite tool, so the AGENTS 4.4 record exists as the
JSON board file (a) and this PLAN list (b). Work steps, all done:
- Reality check: ls-remote develop + branch, PR #1685 state.
- Planning repo path verified and quoted.
- Worktree + base attestation (exact base SHA, ancestor proof, own-commits-only log).
- DE two-phase paragraph rewritten once, grammatically, no denial-case repetition,
  `Grant` kept as the English term, identifiers in code spans.
- Monotonic base handling (develop unchanged this shift), normal push.
- docs-check + exact-head CI run observed to TERMINAL.
- Evidence pushed to origin/main before END.
- END posted.

## Handoff note (Uebergabe)

Predecessor lanes 85ea1938 / 2d4e.. for this card are released (mission file r3-stufe
line). This lane took the card from REQUEST CHANGES at 3b9a3f78e to a reviewable final
candidate. No second branch was invented: the local helper branch was renamed into the
named candidate chain before any push; `git ls-remote` shows exactly one remote candidate
branch `refs/heads/lane-0428-115-twophase-doc` throughout.

## Step 1 — Reality witnesses

    $ git ls-remote origin refs/heads/develop
    ec592fd3852328439ae9de8763c816ae9dd88dcc        refs/heads/develop
    $ git ls-remote origin refs/heads/lane-0428-115-twophase-doc
    3b9a3f78e7e91f1c9a58a564ecbc013540697481        refs/heads/lane-0428-115-twophase-doc
    $ gh pr view 1685 --json state,headRefName,headRefOid,baseRefName
    OPEN, base=develop, head=3b9a3f78e... (PR #1685 "docs(0428-115): document the enrollment consume/issue two-phase boundary")

Mission text said develop "aktuell 40b9901398"; the actual remote develop head at start is
`ec592fd38` (40b9901398 has been superseded; `git log --oneline 40b9901398..origin/develop`
lists 1 newer commit: ec592fd38, PR #1687 merge). The branch already contained ec592fd38
(`git merge-base --is-ancestor` => yes), so the r2 hopf-merge 0d53cd85 is current and no new
hopf-merge commit was required ("No hopf-drang" case of the mission).

## Step 2 — Planning repo path verification

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
    /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
    (workers/baseharbor-plan resolves to /home/marcel/dev/baseharbor-ecosystem/workers — the
    quarantined bookkeeping dir, NOT the planning repo; not used.)

## Step 3 — Base attestation

- Base ref cut from: remote `lane-0428-115-twophase-doc` @ `3b9a3f78e7e91f1c9a58a564ecbc013540697481`
  (the reviewed head; this is the card's own chain, not a foreign candidate).
- Develop base: `ec592fd3852328439ae9de8763c816ae9dd88dcc`, verified ancestor of HEAD:

    $ git merge-base --is-ancestor ec592fd385 HEAD
    ancestor-yes

- Own-commits-only log (`git log --oneline --no-merges origin/develop..HEAD`) at final head:

    711e04c30 docs(0428-115 r3): same terminology fixes in the Store contract comment (no 'dead grant', Grant as the term)
    c9d935970 docs(0428-115 r3): state the DE two-phase boundary once, in code-formatted identifiers
    3b9a3f78e docs(0428-115 r3): smooth DE two-phase wording, drop redundant sentence
    fd55328e0 docs(0428-115 r2): fix DE two-phase wording for authorization Grant/denial
    2039628ba docs(0428-115): make the enrollment consume/issue two-phase boundary explicit

  All commits are this card's chain (predecessor rounds + this lane's two r3 commits); no
  foreign candidate is carried on top. Push witness (remote before/after, second push):

    remote before: c9d9359702e77282e628a4ad4e66bbab2ab2bc57
    remote after:  711e04c303e7ca00eb9d34d4d7af1f504842a546   (3b9a3f78e..c9d935970 fast-forward, then c9d935970..711e04c30; NO force, monotonic)

## Steps 4-5 — Wording fixes

DE paragraph in `docs/de/decisions/0020-scoped-connector-enrollment.md` (commit c9d935970),
final text of the added two-phase paragraph:

> Verbrauch (`Consume`) und Identitätseintragung (`RecordIssued`) sind zwei Phasen
> einer Einschreibung, die in getrennten Transaktionen verpflichtet werden. Nach dem
> Commit von `Consume` ist der Grant dauerhaft verbraucht, ohne dass eine aktive
> Knotenidentität existiert; dieses Fenster ist absichtlich und bleibt fail-closed.
> Der verbrauchte Grant wird nie wiederhergestellt; die einzige Erholung ist ein
> frisches `Create` oder `CreateRenewal`. Wenn `RecordIssued` fehlschlägt, widerruft
> `Enroll` außerdem das Zertifikat, das es signiert hat. Die Klausel
> `previous_certificate_serial` in `Consume` und die Bedingung
> `certificate_serial IS NULL` in `RecordIssued` halten einen konkurrierenden
> Antrag vom Serial-Schreiben fern, sodass eine halb fertige Einschreibung einen
> endgültig verbrauchten Grant hinterlässt — nie eine teilweise Identität oder eine
> zweite Identität für einen Knoten.

Mapping to the r3 reviewer recipe (comment 6998325146):
- Phases in separate transactions: stated once.
- After `Consume` commits: Grant consumed, no active node identity: stated once.
- Recovery requires a fresh `Create` or `CreateRenewal`: stated once.
- `Enroll` revokes the issued certificate when `RecordIssued` fails: stated once.
- The repeated denial-case sentence ("Falschumfang, abgelaufene Genehmigung oder ein
  bereits verbrauchter Grant führen zur gleichen Verweigerung (denial)") was REMOVED —
  those cases are already covered by the preceding historical DE paragraph, which was
  left untouched per the recipe ("Do not touch historical DE text").
- Actual guards named with code formatting: `previous_certificate_serial` and
  `certificate_serial IS NULL` (the literal SQL condition from
  `internal/database/connector_enrollment.go:126`), replacing the pseudo-identifiers
  `serial-is-null` / `serial-write`. Method names `Consume`, `RecordIssued`, `Create`,
  `CreateRenewal`, `Enroll` are code spans.
- `Grant` stays the English Eigenname; no `Zuschuss`, `Leugnung` or `toter Zuschuss`
  anywhere in the added text; "tot" replaced by "endgültig verbraucht".
- Grammar fixed ("Der eine-use Grant zwischen die Phasen gestellt ist" is gone; one
  clean, declinated sentence per fact).

Additional same-round fix (commit 711e04c30): the `Store` contract comment in
`internal/targetenrollment/authority.go` carried the same two defects the reviewer
objected to — the pseudo-identifier "serial-is-null guard"/"serial write" and the term
"dead grant". Per the mission rule that a page must not carry the same terminology
confusion, it was aligned with the DE fix: `Grant` capitalized as the term, "consumed
Grant" instead of "dead grant", and the guard named as `certificate_serial IS NULL`.
EN ADR prose was NOT touched (see Findings).

Checks that validate the changed paths:
- `bash scripts/documentation-audit.sh` — all PASS (incl. "ADR identifiers", German scope, DE technical integrity).
- `mkdocs build --strict` equivalents ran hosted: `PR · Validation · mkdocs-de-strict` and
  `PR · Validation · mkdocs-en-strict` — both success in run 44453258359.
- `gofmt -l` clean; `go build ./...` and `go vet ./internal/targetenrollment/` pass.
- `go test ./internal/targetenrollment/` ok (comment-only change).
- New tests: none added, so the CI-capture rule (AGENTS 5.3) is not triggered; no `.github/**` change needed.

## Step 6 — Base handling / hopf

`git merge origin/develop` => "Already up to date" (branch already contained develop
`ec592fd38` via the r2 hopf-merge 0d53cd85). Monotonic normal pushes only; no force; no
merge executed by this lane (merge into develop is reserved for CODEX-MERGE, AGENTS 5.2).

## Step 7 — Hosted CI on the exact head (Eigenes-Run-Pflicht)

- Run `44453258359`, "CI · Source & Quality", event pull_request, head
  `711e04c303e7ca00eb9d34d4d7af1f504842a546`, observed by this lane from in_progress to
  TERMINAL: **completed / success**. 20 executed jobs, 0 failures, 18 skipped (docs-change
  selection; skips are the normal selection outcome, no bypass).
  Key jobs: PR · Validation · documentation-audit success; mkdocs-en-strict / mkdocs-de-strict
  success; PR · Go unit (owner/cli-0..3/packages) success; PR · Source format success;
  PR · Native gate plan success; Native Keycloak/Core docker+podman success.
- Run `44453155419` on intermediate head c9d935970 was cancelled by the workflow's
  concurrency group when 711e04c30 was pushed (superseded intermediate, documented per
  CI discipline).

## Findings

- Terminology drift in the EN ADR paragraph (`docs/decisions/0020-scoped-connector-enrollment.md`):
  it uses pseudo-identifier "serial-is-null guard" and the term "dead ... grant" (lines 43-46
  of the added block) — the same expressions the r3 review objected to in DE. The reviewer
  recipe explicitly said "Do not touch ... EN docs", so this lane left the EN text unchanged.
  If the reviewer wants the EN/DE terminology fully aligned, the two-line fix is: replace
  "serial-is-null guard" with the literal condition (`certificate_serial IS NULL`) and
  "dead, permanently consumed grant" with "permanently consumed grant".
- `docs/de/releases/v0.4.9.md:26` contains "Leugnungspolitik" (historical release text, this
  card's write-set does not include it; noted only).
- Mission's "develop aktuell 40b9901398" was stale: actual develop is ec592fd38 (PR #1687
  merged after it); handled by the ancestor check above.

## Cleanliness

- No containers/compose projects were started by this lane (docs/comment-only change);
  `ps-witness`: nothing to bring down. Worktree `/tmp/opencode/w-hopf-115r2-wt` lives in tmp
  and is removed after END. No files created in the ecosystem root.

## END

- END_DONE: mission-115r2-wording-hopf.md — DONE (r3). Card t-20261118-enrollment-two-phase-boundary-doc
  (0428-115), PR #1685, final candidate `711e04c303e7ca00eb9d34d4d7af1f504842a546` on
  `lane-0428-115-twophase-doc`, base develop `ec592fd38` (ancestor-verified, monotonic, no force).
  DE two-phase paragraph now states each fact once, grammatically, with code-formatted real
  identifiers (`previous_certificate_serial`, `certificate_serial IS NULL`); denial-case list
  removed; `Grant` stays the term. Store comment aligned. Exact-head run 44453258359 completed/success,
  observed terminal by this lane. Ready for CODEX-REVIEW (final) / CODEX-MERGE.
