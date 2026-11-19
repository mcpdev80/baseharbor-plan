# 0428-115 fix-3 (r4) — DE two-phase paragraph: transaction semantics + final clause

Card: t-20261118-enrollment-two-phase-boundary-doc (0428-115), PR #1685,
branch `lane-0428-115-twophase-doc`. Mission: mission-115r2-wording-hopf.md, r4 stage
(CODEX-REVIEW REQUEST CHANGES comment 6999389290 on head 711e04c303e7ca00eb9d34d4d7af1f504842a546).

## PLAN

- Reality check: ls-remote develop + lane branch head, PR #1685 state.
- Read review comments (6993699816 / 6997988022 / 6998325146 / 6999389290).
- Worktree at 711e04c30; base attestation; monotonic (no hopf needed — develop unmoved).
- Fix DE wording (1): "in getrennten Transaktionen verpflichtet werden" -> per-transaction commit semantics.
- Fix DE wording (2): tighten "halten einen konkurrierenden Antrag vom Serial-Schreiben fern".
- Verify identifiers code-formatted, denial cases not repeated, EN/Store comment untouched.
- docs audit + language audit + strict mkdocs builds; commit; normal push.
- Observe exact-head CI run to terminal.
- Evidence here, on baseharbor-plan origin/main before END.

## Handoff vermerk (Uebergabe)

Predecessor lanes are released: the r2 lane (mission-115r2) delivered 711e04c30 (r3, evidence
fix-2.md in evidence/r28-welle4-2026-11-19/enrollment-twophase/), and the earlier lanes
85ea1938 / 2d4e.. are gone. This lane is the r4 correction pass named on free seat; it takes the
card to the end of the review cycle. No second branch was created (AGENTS 3.8: exactly one
candidate per chain).

## Base attestation and branch provenance

Remote truth (ls-remote, this session, 2026-11-19):

    $ git ls-remote origin refs/heads/develop refs/heads/lane-0428-115-twophase-doc
    ec592fd3852328439ae9de8763c816ae9dd88dcc	refs/heads/develop
    711e04c303e7ca00eb9d34d4d7af1f504842a546	refs/heads/lane-0428-115-twophase-doc

(The mission text named develop "40b9901398" from the r2 cut; live develop has since moved to
ec592fd38, which is what the r3 lane already integrated — see fix-2.md. No newer hopf was
needed: develop had not moved between this lane's start and the push.)

- Base/branch-off point for this lane's work: previous candidate head
  `711e04c303e7ca00eb9d34d4d7af1f504842a546` (verified identical to the remote ref above).
- Ancestor test: `git merge-base --is-ancestor origin/develop HEAD` => develop `ec592fd385`
  IS an ancestor of 711e04c30 and of the new commit bb685c2dc. Monotonic, no hopf merge needed,
  no force used.
- The checkout was made from the fetched remote head, not from another PR head.

## Commits (git log origin/develop..HEAD, this candidate)

    bb685c2dc docs(0428-115 r4): correct transaction-commit wording and tighten the closing clause   <- this lane
    711e04c30 docs(0428-115 r3): same terminology fixes in the Store contract comment (no 'dead grant', Grant as the term)
    c9d935970 docs(0428-115 r3): state the DE two-phase boundary once, in code-formatted identifiers
    3b9a3f78e docs(0428-115 r3): smooth DE two-phase wording, drop redundant sentence
    fd55328e0 docs(0428-115 r2): fix DE two-phase wording for authorization Grant/denial
    0d53cd85c hopf-merge 0428-115: integrate develop ec592fd38 (PR #1687) before docs wording fix
    2039628ba docs(0428-115): make the enrollment consume/issue two-phase boundary explicit

Only this card's commits (own r2/r3 history + this r4 fix). No foreign candidate is carried.

## Change

Single file: `docs/de/decisions/0020-scoped-connector-enrollment.md`, only the two-phase
paragraph added by this card. Reviewer point 1 (commit semantics): the sentence
"die in getrennten Transaktionen verpflichtet werden" is replaced by "die jeweils in einer
eigenen Transaktion abgeschlossen werden" — German "verpflichten" means an obligation, not a
transaction commit; the new phrasing matches the EN text ("two phases that commit in separate
transactions"). Reviewer point 2 (final clause): "halten einen konkurrierenden Antrag vom
Serial-Schreiben fern" is replaced by a direct statement, "verhindern, dass ein konkurrierender
Antrag die Zertifikatsserial schreibt", followed by the tightened consequence sentence.
Additionally restored the blank line before the "Kern"-paragraph that r3 had dropped (EN and
the surrounding DE text are separated by paragraph breaks).

No content/behavior change: same facts as the EN paragraph (per-transaction commits; consumed
Grant with no active identity between phases; recovery only via fresh `Create`/`CreateRenewal`;
`Enroll` revokes when `RecordIssued` fails; guards `previous_certificate_serial` /
`certificate_serial IS NULL`; outcome: consumed Grant, never partial/second identity).
Identifiers stay in code formatting (`Consume`, `RecordIssued`, `Create`, `CreateRenewal`,
`Enroll`, `previous_certificate_serial`, `certificate_serial IS NULL`); `Grant` stays the term;
no denial-case repetition. EN docs and `internal/targetenrollment/authority.go` untouched by
this commit (r3 already aligned them and the reviewer confirmed they match the implementation).

## Local checks (before push)

- `bash scripts/documentation-audit.sh` => PASS (all sections, exit 0).
- `python3 scripts/documentation-language-audit.py` => PASS ("German navigation and human-guide coverage PASS", exit 0).
- `python3 scripts/check_docs_locale_parity.py` => "EN/DE page coverage OK: 168 matched Markdown pages".
- `mkdocs build --strict --config-file mkdocs.yml` => success (no warnings besides the vendor Material banner).
- `mkdocs build --strict --config-file mkdocs.de.yml` => success, strict-clean.
- The CI job that runs these is the docs job in `.github/workflows/ci.yml` (mkdocs strict EN+DE builds,
  line ~138) triggered on the PR; no .github/** change was needed (CI-Aufnahmepflicht satisfied by the
  existing documentation group).

## Candidate

- Final head: `bb685c2dca5b4d19159eca8ceda8cb9076638dd4` on `lane-0428-115-twophase-doc`.
- Push: normal fast-forward `711e04c30..bb685c2dc` (git push output above; no force).

## Exact-head CI (observed by this lane to terminal)

- Run `44457842661` on `bb685c2dca5b4d19159eca8ceda8cb9076638dd4`: observed via
  `gh run watch --exit-status` to terminal **completed / success, 0 failed or cancelled jobs**.
  Docs group green: `PR · Validation · documentation-audit`, `mkdocs-en-strict`, `mkdocs-de-strict`,
  `go-vet`, `go-build`, `Focused Python`; all `PR · Go unit` shards and both
  `PR · Native Keycloak/Core` (docker + podman) jobs passed. Heavyweight release gates
  skipped by the docs-change selection (as intended, no bypass).
- `PR Selected Checks` on the PR: **SUCCESS** (merge queue check, observed after terminal).
- Remote truth after push (`git ls-remote origin refs/heads/lane-0428-115-twophase-doc`):
  `bb685c2dca5b4d19159eca8ceda8cb9076638dd4`.

## Revision labels (reviewer findings -> resolution)

- r2 (6993699816): `Zuschuss`/`Leugnung`/`toter Zuschuss` -> fixed in fd55328e0: `Grant` is the
  term, denial rendered as Verweigerung/Ablehnung context, no "dead grant" (r4 touch: none open).
- r3 (6998325146): ungrammatical repeated denial cases -> single clean paragraph, real
  identifiers in code formatting (`previous_certificate_serial`, `certificate_serial IS NULL`),
  fixed in c9d935970 + 711e04c30.
- r4 (6999389290, this round): (1) "in getrennten Transaktionen verpflichtet werden" mistranslated
  commit semantics -> "die jeweils in einer eigenen Transaktion abgeschlossen werden";
  (2) awkward "halten einen konkurrierenden Antrag vom Serial-Schreiben fern" -> direct
  "verhindern, dass ein konkurrierender Antrag die Zertifikatsserial schreibt"; closing sentence
  tightened. Fixed in bb685c2dc, single file, DE-only. EN page and Store comment carry no such
  confusion (verified against EN text in this diff) and were not touched.

## Hygiene

- No containers/compose projects/networks/volumes were started by this lane (docs-only change);
  nothing to bring down. No writes outside `docs/de/decisions/0020-scoped-connector-enrollment.md`
  in the product repo; this evidence file is the only plan-repo write.

## END

- END_DONE: mission-115r2-wording-hopf.md — DONE (r4). Card t-20261118-enrollment-two-phase-boundary-doc
  (0428-115), PR #1685, final candidate `bb685c2dca5b4d19159eca8ceda8cb9076638dd4` on
  `lane-0428-115-twophase-doc`, base develop `ec592fd385` (ancestor-verified, monotonic, normal
  push, no force, no hopf needed). DE two-phase paragraph now states transaction-commit
  semantics correctly and the guard sentence reads directly; identifiers code-formatted; `Grant`
  as the term; no denial-case repetition. Exact-head run 44457842661 completed/success TERMINAL
  (0 failures), `PR Selected Checks` SUCCESS. Handoff: predecessor r3 head 711e04c30 (released
  lanes); this lane closes the card's review cycle — ready for CODEX-REVIEW final / CODEX-MERGE.
