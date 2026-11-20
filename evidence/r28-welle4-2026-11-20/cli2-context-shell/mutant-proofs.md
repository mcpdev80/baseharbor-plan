# 0428-068 — mutant proofs (blocker 4, one per stage)

Recorded live during r2 on head `bf923b52` (post-rebase). Each mutant was introduced one at a time; each made **only its own test** red; each was restored immediately after proof. Precedent: 078.

## Proof A — wrapper `export BASEHARBOR_TARGET` line (blocker 2, parent-shell effect)

- **What:** comment out `export BASEHARBOR_TARGET="$_baha_ctx"` in the bash wrapper body in `cmd/baha/completion_setup.go`.
- **Effect:** `TestEndToEndBashInteractiveContextUseAndClear` goes RED (`AFTER_IS=<empty>` — the target is no longer exported in the parent shell).
- **Restored.** The export in the parent shell is exactly the blocker-2 fix.

## Proof B — interactive guard `[[ $- == *i* ]]` (blocker 2, non-interactive untouched)

- **What:** change `if [[ $- == *i* ]]; then` to `if false; then` in the bash wrapper body.
- **Effect:** `TestInteractiveGuardPresent` goes RED — the interactive guard is absent.
- **Restored.** Without the guard, the wrapper is defined in every shell (CI, `bash -c`, pipelines see it) — the defect the guard prevents.

## Proof C — recursion guard `command baha` (blocker 2, recursion safety)

- **What:** change `command baha` to bare `baha` in the wrapper body.
- **Effect:** `TestEndToEndBashInteractiveContextUseAndClear` goes RED — the wrapper now calls itself (infinite recursion / re-eval instead of the real program).
- **Restored.** `command baha` is the recursion guard: the wrapper must call the real `baha` binary, never itself.

## Test that ties them together

`TestEndToEndBashInteractiveContextUseAndClear` sources the generated bash wrapper in a real `bash -i`:

1. runs `baha context use <target>` (no `eval`),
2. reads `BASEHARBOR_TARGET` from a subsequent command in the same interactive shell → proves the parent exported it (Proof A),
3. runs `baha context clear` and reads `BASEHARBOR_TARGET` again → proves it is unset in the parent,
4. the wrapper is present only under `[[ $- == *i* ]]` (Proof B) and uses `command baha` (Proof C).

All three proofs are covered by this single end-to-end path plus `TestInteractiveGuardPresent`.
