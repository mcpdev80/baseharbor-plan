# w22-delivery-wording2 — Evidence

ROLLE: Worker (Lane w22-delivery-wording2). Coordinator: f49a3303.
TASK: PR #1333 / t-20261018-r27-delivery-boundary. Micro-task: replace three
wording spots in the two 0022-ADR files with already-resolved replacement text.

Base: 87d1df12. Worktree: /tmp/opencode/w22-delivery-wording2-wt.

## PLAN

1. Create dedicated worktree /tmp/opencode/w22-delivery-wording2-wt at 87d1df12.
2. Edit Stelle 1 — EN §2 paragraph (lines 32-35): replace "If a selection observes..." sentence with persisted-attestation wording.
3. Edit Stelle 2 — DE §2 paragraph (lines 32-36): replace corresponding German sentence with the exact wording given.
4. Edit Stelle 3a — EN trade-offs last bullet (line 64): replace whole bullet with record-save-vs-live wording.
5. Edit Stelle 3b — DE last nachteile bullet (line 70): replace whole bullet with the exact German wording given.
6. Verify checkpoints (grep counts, diff name-only == exactly two .md, no "still accepting"/"still akzeptiert").
7. Merge origin/develop, ancestry rc=0 vs ls-remote SHA, write-set grep-empty.
8. go build ./... + go test ./internal/deployment ./internal/delivery.
9. Push FF, confirm ls-remote == pushed SHA.
10. Write evidence, post END_DONE, tick all steps.

## repo-rule compliance

- Only the two ADR .md files touched (docs/decisions/... and docs/de/decisions/...).
- git diff --name-only == exactly the two .md files.
- No prose authored by me; every replacement is verbatim from the mission's resolved text.
- Write-set == exactly two files.

## Edit log

Stelle 1 (EN §2, lines 32-35): replaced the "If a selection observes both a direct
`baseharbor` owner and a delegated `external` owner active..." sentence with the
"persisted record attests conflicting active ownership..." sentence. Whole 5-line
block replaced verbatim from mission line 12.

Stelle 2 (DE §2, lines 32-36): replaced the corresponding German "Wenn eine
Auswahlen-Beobachtung gleichzeitig..." sentence with the exact "Wenn der
gespeicherte Datensatz einen widersprechenden aktiven Besitz belegt — ..." wording
(verbatim from mission line 15).

Stelle 3a (EN trade-offs line 64): replaced the whole "The invariant is checked at
record-save time; it does not prevent an operator..." bullet with the record-save-vs-live
wording (verbatim from mission line 17).

Stelle 3b (DE Nachteile line 70): replaced the whole "Der Invariant wird beim
Speichen ... still akzeptiert" bullet with the exact German wording (verbatim from
mission line 19).

## CHECKPOINTS (all pass, re-verified after plattenfest WIDERLEGUNG)

- grep -c 'If a selection observes' EN == 0; 'persisted record attests conflicting' == 1 ✓
- grep 'Auswahlen-Beobachtung' DE == 0 (empty); 'widersprechenden aktiven Besitz' == 1 ✓
- 'still accepting' in both == 0; 'still akzeptiert' in both == 0 ✓
- git diff --name-only == exactly the two .md files ✓
- commit 1dde4208, merge origin/develop (already up to date), ancestry rc=0 ✓
- go build ./... rc=0; go test ./internal/deployment ./internal/delivery ok (rc=0) ✓
- push FF OK 87d1df12..1dde4208 (no force) ✓
- ls-remote == 1dde42084bdab42227ef779dba0352dd1b3d4967 == pushed HEAD ✓
- merge-base --is-ancestor origin/develop HEAD rc=0 ✓

## FINAL SHA: 1dde42084bdab42227ef779dba0352dd1b3d4967

## END_DONE
w22-delivery-wording2: head=1dde4208 grep0=3stellen | ADR 0022 EN/DE wording3 applied (EN §2 persisted-attestation, DE §2 widersprechender Besitz, EN+DE trade-offs live-concurrent-acceptance out-of-scope); committed, merged develop FF, build+tests pass, pushed FF. ls-remote confirmed == pushed SHA, ancestry rc=0.
