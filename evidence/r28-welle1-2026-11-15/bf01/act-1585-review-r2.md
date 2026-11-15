# PR #1585 Review R2 — BF-01 state-dir and private organization store

ROLE: CODEX-REVIEW (no merge; frost).

## PLAN

1. Verify current PR #1585 refs, base develop, exact head e7501204caf27ece99636152220d389ad86374d4, exact-head run 43689640514, and candidate ancestry/log.
2. Inspect the BF-01 isolation regression and prove it fails on exact develop and passes on the exact branch, with both SHAs and command outputs; confirm it traverses the registration guard without an early-exit shortcut.
3. Review combined internal/orgconfig/store.go semantics from BF-01 and #1582, including world-writable guard and private fallback; run the requested throwaway vet and record its witness.
4. Read access/init test diffs and verify expectations remain intact and no second target truth source was introduced.
5. Write SHA-exact verdict and actionable recipe, run planning validation, publish evidence to origin/main, update the board, and post END.
