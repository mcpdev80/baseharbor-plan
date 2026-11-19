# 0428-115 fix-4 (r5) — DE identity-write guard: name both conditions

Card: t-20261118-enrollment-two-phase-boundary-doc (0428-115), PR #1685,
branch `lane-0428-115-twophase-doc`. Mission: mission-115r2-wording-hopf.md, r5 stage
(CODEX-REVIEW comment 6999847636; head bb685c2dc recognized on content except one spot).

## PLAN

- Reality check: ls-remote develop + lane branch head, PR #1685 head.
- Worktree at bb685c2dc; base attestation; monotonic; hopf only if develop moved.
- Fix DE wording: add the second identity-write guard condition
  `consumed_at IS NOT NULL` in `RecordIssued` verbatim after the EN model; no other
  rewording, no content step.
- docs-check (scripts/documentation-audit.sh) locally; commit; normal push to the named branch.
- Observe exact-head CI run to terminal.
- Evidence here, on baseharbor-plan origin/main before END.

## Handoff vermerk (Uebergabe)

Predecessor chain: the r4 lane (f11d4b4e, released) delivered head bb685c2dc (evidence
fix-3.md in evidence/r28-welle4-2026-11-19/enrollment-twophase/). This lane is the r5
correction pass on the same candidate branch; it takes the card to the end of the review
cycle. No second branch was created or pushed (AGENTS 3.8: exactly one candidate per
chain); local branch names are session plumbing only, the remote candidate remains
`lane-0428-115-twophase-doc`.

## Base attestation and branch provenance

Remote truth (ls-remote, this session, 2026-11-19):

```text
ec592fd3852328439ae9de8763c816ae9dd88dcc  refs/heads/develop
bb685c2dca5b4d19159eca8ceda8cb9076638dd4  refs/heads/lane-0428-115-twophase-doc
bb685c2dca5b4d19159eca8ceda8cb9076638dd4  refs/pull/1685/head
```

Base cut: bb685c2dca5b4d19159eca8ceda8cb9076638dd4 (predecessor head, task-specified).
Develop at start: ec592fd3852328439ae9de8763c816ae9dd88dcc. Ancestor test:
`git merge-base --is-ancestor ec592fd385 bb685c2dc` passes, so develop is already
contained in the branch — monotonic, **no hopf merge needed**, no force.

First commit this lane: 50f87cfb8dd6e87913044f96cc0204af1423b61c.
`git merge-base --is-ancestor ec592fd3852328439ae9de8763c816ae9dd88dcc 50f87cfb8` passes.

`git log --first-parent ec592fd3852328439ae9de8763c816ae9dd88dcc..50f87cfb8dd6e87913044f96cc0204af1423b61c`:

```text
50f87cfb8 docs(0428-115 r5): name both identity-write guard conditions in the DE paragraph (serial-is-null and consumed-at IS NOT NULL)
bb685c2dc docs(0428-115 r4): correct transaction-commit wording and tighten the closing clause
711e04c30 docs(0428-115 r3): same terminology fixes in the Store contract comment (no 'dead grant', Grant as the term)
c9d935970 docs(0428-115 r3): state the DE two-phase boundary once, in code-formatted identifiers
3b9a3f78e docs(0428-115 r3): smooth DE two-phase wording, drop redundant sentence
fd55328e0 docs(0428-115 r2): fix DE two-phase wording for authorization Grant/denial
0d53cd85c hopf-merge 0428-115: integrate develop ec592fd38 (PR #1687) before docs wording fix
2039628ba docs(0428-115): make the enrollment consume/issue two-phase boundary explicit
```

All commits are this card's own chain plus its documented hopf — no foreign candidate carried.

## The change

`docs/de/decisions/0020-scoped-connector-enrollment.md`, two-phase paragraph. The EN page
names two guards on the identity write: "the serial-is-null guard plus consumed-grant
predicate in the identity write". The DE page named only `certificate_serial IS NULL`.
This commit adds the missing condition verbatim per the EN model and the source
(`internal/database/connector_enrollment.go` RecordIssued: `AND consumed_at IS NOT NULL`):

```diff
-`previous_certificate_serial` in `Consume` und die Bedingung
-`certificate_serial IS NULL` in `RecordIssued` verhindern, dass ein konkurrierender
+`previous_certificate_serial` in `Consume` und die Bedingungen
+`certificate_serial IS NULL` und `consumed_at IS NOT NULL` in `RecordIssued` verhindern, dass ein konkurrierender
```

Singular "Bedingung" -> plural "Bedingungen"; identifiers stay code-formatted (backticks);
no other sentence touched; EN page untouched; no content step.

## Checks

- Local `bash scripts/documentation-audit.sh`: PASS (all sections, exit 0) at 50f87cfb8.
- Hosted run: `CI · Source & Quality` run `44460025899` on head 50f87cfb8dd6e87913044f96cc0204af1423b61c —
  observed to terminal state (result recorded in the END section below).

## Revision labels (reviewer findings -> resolution)

- r2 (6993699816): terminology Grant/denial — fixed in fd55328e0 (prior lanes).
- r3 (6998325146): single clean paragraph, code-formatted identifiers — fixed in
  c9d935970 + 711e04c30 (prior lanes).
- r4 (6999389290): transaction-commit semantics + tightened closing clause — fixed in
  bb685c2dc (r4 lane, released).
- r5 (6999847636, this round): DE named only one identity-write guard (serial-is-null);
  EN names both (serial-is-null AND consumed_at IS NOT NULL). Fixed in 50f87cfb8 by
  adding `consumed_at IS NOT NULL` verbatim per the EN model, no further rewording.

## Hygiene

- No containers/compose projects/networks/volumes started by this lane (docs-only change);
  nothing to bring down. Worktree lives under /tmp/opencode/w-hopf-r5-wt.
- Product-repo write set: exactly `docs/de/decisions/0020-scoped-connector-enrollment.md`.
  No `.github/**` changes. This evidence file is the only plan-repo write.
- Planning repo verified: remote of /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan is
  https://github.com/mcpdev80/baseharbor-plan.git (never the workers/ directory).

## END

- END_DONE: mission-115r2-wording-hopf.md — DONE (r5). Card t-20261118-enrollment-two-phase-boundary-doc
  (0428-115), PR #1685, final candidate `50f87cfb8dd6e87913044f96cc0204af1423b61c` on
  `lane-0428-115-twophase-doc`, base develop `ec592fd385` (ancestor-verified, monotonic, normal
  push, no force, no hopf needed — develop already contained). DE paragraph now names both
  identity-write guard conditions exactly as the EN page does. Exact-head run 44460025899:
  TERMINAL result recorded below. Handoff: predecessor r4 head bb685c2dc (lane released);
  this lane closes the card's review cycle — ready for CODEX-REVIEW final / CODEX-MERGE.
