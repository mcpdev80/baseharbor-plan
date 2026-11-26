## PLAN — w266-0428-285-1820pre (#1820 chain pre-flight, read-only census)

Owner commission 2026-11-26. Card 0428-285 chain, slot 4 (#1842 → #1812 → #1819 → #1820). Read-only: NO branch mutation, NO rebase/merge/push of product, NO tests, NO CI trigger, NO workflow_dispatch, NO card edits, NO .github writes, NO direct plan-main push.

- [ ] Resolve remotes; isolated read-only worktree on `lane-origin/develop`; plan worktree off `origin/main`
- [ ] STATE WITNESS: ls-remote real heads for develop / #1820 / #1819 / #1812 / #1842; print every SHA
- [ ] ANCESTRY: `merge-base --is-ancestor develop .. 1820/1819`; `git log develop..1820`; payload-loss guard `git diff develop...1820 --name-status`
- [ ] WRITE-SET DISJOINTNESS: #1820 own files (1842..1820) vs 1842/1812/1819/1833/1650/1818 write sets; name collisions with file:line
- [ ] GATE/UNIT WITNESS GAP: jobs API per_page=100 incl attempts on 1820+1819 heads; confirm seam-C unit witness
- [ ] QUALIFICATION RECIPE: ordered absorb-hop steps for after #1819 merge
- [ ] AKTE: write evidence akte in plan worktree; push OWN branch; `gh pr create` vs baseharbor-plan (NO merge)
- [ ] EVIDENCE ON origin/main: ls-tree witness for evidence path before END post
- [ ] POST END_DONE line; clean up worktrees; `docker ps -a` witness

Scope: report only. No mutations, no CI triggers.
