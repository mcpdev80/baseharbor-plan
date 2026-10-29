# o214 - producer PR2 profile pivot

## PLAN

0. Read dispatch and binding context; record plan and evidence dir.
1. Save the extension work on branch work/r27-producer-extension-reserve and push.
2. Write contracts/connection_profile_trust_test.go (positive baseline + single-removal required-field negatives) alongside extension_trust_test.go.
3. Planner check for the new path (simulate pr-gate-plan.py), assert integration/static/public-contracts selection.
4. go vet ./contracts/ + full go test ./contracts/ -count=1 + focused -run '^TestConnectionProfile' with GOPATH/GOCACHE in /tmp.
5. Commit forward (remove contracts/extension_trust_test.go in same commit), push, gh pr edit 1203 title+body citing RV1203D + reservation.
6. Report new head SHA + checks; publish evidence.

## repo-rule compliance

- baseharbor/AGENTS.md: test files in contracts/ use package `contracts_test`; JSON Schema 2020-12; one contract per test function; clone schema-valid baseline and mutate a single required field per case; assert schema rejection. New test file follows the same conventions as contracts/v0425_contracts_test.go.
- baseharbor/CONVENTIONS.md (if present): single mutation per negative; baseline validated first.
- baseharbor-plan: evidence-only write in the designated evidence/... path; no git in baseharbor-plan.

## Coordinator Recovery-Notiz (o214 EXITED vor Push)
- Lane stürzte nach lokalem Commit 908f1d09 (Profil-Negative) vor Push/PR-Edit ab.
- objects waren im geteilten Repo-Store → Coordinator übernahm (explizite Übergabe, Lane tot):
  go vet clean, go test ./contracts/ -run TestConnectionProfile PASS, Push auf
  work/r27-producer-extension-contracts, PR #1203 Titel/Body auf Profil-Slice umgestellt.
- Extension-Arbeit unverändert gesichert: work/r27-producer-extension-reserve = b9ebc475.
- rv1207 (CODEX-REVIEW am SHA 908f1d09) dispatched. Worktree o214 entfernt + Registry pruned.
- END coordinator-recovery DONE
