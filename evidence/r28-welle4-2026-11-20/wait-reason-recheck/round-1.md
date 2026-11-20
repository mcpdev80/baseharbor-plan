# w212-0428-202-waitrecheck — wait-reason recheck dossier (round 1)

Lane: w212-0428-202-waitrecheck. Mission: /var/tmp/note-212-waitrecheck.txt.
Read-only planning assistance: no product changes, no PR edits, no card writes, no reruns, no dispatch.

## PLAN
1. Turn-start basics checks; verify remote reality (baseharbor develop, baseharbor-plan main, PR #1732).
2. Enumerate all `kanban_status: wait` cards from origin/main of baseharbor-plan.
3. Per card: card number, filename, title, literal wait_reason, gate named (198/202/BOTH/OTHER).
4. Per card: corrected reason after this tick (only-198 / unchanged / no-gate-but-X with proof).
5. Per card with PR: check-runs at current head (read-only gh api) + loki_test.go symbol test (client-cert.pem) to classify packages-red.
6. Clarify whether "PR  Selected Checks" is a required check or optional signal.
7. Write dossier evidence/r28-welle4-2026-11-20/wait-reason-recheck/round-1.md.
8. Verify evidence on origin/main (fetch + ls-tree witness), commit, push.
9. Cleanliness check, END post to coordinator with plan-main SHA.

## Planning repo verification
`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch) (push) — confirmed real planning repo, not workers/baseharbor-plan.

(working notes below)
