# l12-profile-docs — docs-only fix for PR #1324 (t-20261018-r27-profile-contract)

## END line
`END_DONE l12-profile-docs: head=<sha> | EN+DE credential-access-v1.md: rewrite contradicting present-tense EnrollDevice/hosttrust claims; independent CA/installation binding = future work (two card names)`

## Task / scope
- Mission `coordinator/missions/l12-profile-docs.txt` (Coord f49a3303).
- Review `review-1324j.md` (REJECT): EN `docs/spec/credential-access-v1.md:198-200` + DE `:200` still assert in present tense that EnrollDevice binds installation ID to enrollment, trust is validated through an existing hosttrust anchor, and the same CA is reused — while the code only checks self-consistency of the profile CA, never InstallationID. Present-tense assertions are contradictory with the deferred paragraphs.
- Scope: **docs-only**, no code/schema/test. One commit. Base = branch `work/r27-profile-contract` head `c50747a5`.
- Required rewrite: state that checked are (a) self-consistency of the profile certificate against its own fingerprint, (b) recipient of the request, (c) time window; independent CA / installation binding and same-CA relation to connection-profile are FUTURE WORK, naming the two cards; existing deferral section stays as reference, avoid repetition. DE sinngleich. No other paragraphs touched.
- STOP (mission): no merge; no code change (any attempt = END_BLOCKED).

## PLAN checklist
1. git fetch origin work/r27-profile-contract develop + worktree add /tmp/opencode/l12-profile-docs-wt work/r27-profile-contract.
2. Edit EN `docs/spec/credential-access-v1.md` lines 198-200 present-tense claims.
3. Edit DE `docs/de/spec/credential-access-v1.md` line 200 present-tense claims (sinngleich).
4. Write evidence `baseharbor-plan/evidence/r27-night-2026-11-02/profile-contract/docs-fix.md`.
5. `go test ./contracts/managementaccess/v1` (unverändert gr#fcn) + diff shows only the two .md files.
6. merge origin/develop; FF push; ls-remote; no run-logs; HANDOFF.

## repo-rule compliance
- baseharbor AGENTS / docs: docs-only change, single focused commit, no code/schema/test touched — matches review scope note exactly.
- Mission STOP respected: no merge, no code change.

## Evidence
- go test ./contracts/managementaccess/v1 (unchanged green) — see below.
- diff shows only the two .md files.
- ls-remote confirms both refs before/after.
- No hosted CI run logs (mission: KEINE run-logs).

## Diff target sentences (EN :198 + :200)
Remove present-tense: "EnrollDevice binds the validated management profile (installation ID, pinned CA, ...)"; "...an independent anchor check is deferred" left but framed as future; "Trust is validated through the shared `internal/hosttrust` anchor and fingerprint; ... reuses the same CA material".
Replace with: EnrollDevice checks certificate self-consistency against its own fingerprint, the request recipient, and the validity window; independent CA/installation binding and same-CA relation to connection-profile/v1 are deferred future work with cards t-20261018-r27-authority-contract and t-20261018-r27-state-owner. Existing "Deferred interfaces" section is retained as the anchor reference and not repeated.

## END l12-profile-docs
