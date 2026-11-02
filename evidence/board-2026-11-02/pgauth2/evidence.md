# pgauth2 — Evidence

## STATUS
active — fixing FATAL: permission denied for database "postgres"/"template1"/"openbao" on OpenBao's PG backend path.

## PLAN
1. [in progress] Read mission pgauth2.txt + baseharbor/AGENTS.md; establish worktree on origin/develop. Worktree `pgauth2-fix` created @ aef6b0e1 (origin/develop).
2. [todo] Run-Log: which role connects when (user/database/auth) — line in evidence.
3. [todo] Locate init path: postgres-init/role provisioning for OpenBao (internal/** + compose templates) — grep.
4. [todo] Minimal fix: correct GRANTs / DB pre-seed or separate role + test/adjust internal/** (Echt-Fix, no superuser bypass).
5. [todo] Proof: go test ./internal/... -run 'Openbao|OpenBao|Postgres' local (before/after).
6. [todo] PR 'fix(secrets): grant OpenBao postgres backend the right privileges'; watch PRSC terminal.
7. [todo] Card via plan.py new + claim; publish planning + evidence.

## repo-rule compliance
- baseharbor/AGENTS.md: no .github/workflows/*, no scripts/pr-*, no subagent/codeman-Spawn, no merge, no interactive question dialog (QUESTION line to Coord instead). Scoped to internal/runtime + compose template only.
