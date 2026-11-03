# CI Access — Runde 10 (Lane w70-ci-access-j)

**Task:** `t-20261022-r27-ci-access`  |  **PR #1357**  |  **Branch:** `work/r27-ci-access-ab`
**Candidate head (verified):** `e9c9e826725e6001088f18bacd7e5a8598cac4c7`  |  **Base `develop`:** `0107d8e1530ff3469048022d7035a2a472dbda34`
**Role:** Worker  |  **Coord:** f49a3303  |  **Evidence:** `baseharbor-plan/evidence/r27-welle3-2026-11-03/ci-access/qualify-10.md`

## PLAN-Checkliste

1. fetch origin work/r27-ci-access-ab + develop, ls-remote==e9c9e826, worktree add — [ ]
2. BEFUND-1: 12-zeilen Matrix {Check,Execute}x{6 Fehlermaterialien} fertigstellen, beide Route-Flag-Assertions je Zeile, readyz NACH Execute neu reiden — [ ]
3. BEFUND-2: kaputter-key vs defektes-cert trennen, je eigener Test mit eigenen Ursachen — [ ]
4. BEFUND-3: HandlerReached aus handler.go entfernen, Zaehlung in test-only Wrapper, handler.go gegen develop UNVERAENDERT — [ ]
5. Lokal: gofmt leer, diff ^-func Test leer, go test gruen, merge develop drift rc=0 — [ ]
6. push FF, gh pr checks --watch terminal, Evidence schreiben — [ ]

## Repo-Regel-Konformität (wird am Ende ausgefüllt)

- Write-Set: `client_test.go` NUR; `handler.go` rueckgaengig auf develop-stand
- `git diff origin/develop -- internal/runtimeexecutor/handler.go` == leer (END-pflicht)
- diff `^-func Test` == leer (nichts loeschen)
- gofmt leer; GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go test ./internal/runtimeexecutor -count=1 -timeout 8m gruen
- merge develop drift rc=0
- push FF, EIGENES-RUN: gh pr checks --watch terminal

## END-Lane

WIRD GEFÜLLT: DONE | BLOCKED
