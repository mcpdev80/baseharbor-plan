# round-2 — cli2-env-policy (korrekturrunde, task t-20261114-r28-cli2-env-policy, PR #1594)

Lane: `cli2-org-env-head` (this worker). Recipe/branch named in mission: `cli2-env-policy-head`.

## PLAN

- read recipe act and reproduce
- verify candidate SHA e5ad8a68 against source
- apply targeted fix in internal/operatorauth/config.go (+ table tests)
- build/vet and test
- commit on candidate branch, fast-forward only, evidence + END post

## Scope mismatch found — STOP, no code change

### Reproduction of the recipe's premise vs reality

- Recipe target: `internal/operatorauth/config.go` policy-aware helper `ManagedEnvironmentWithPolicy(environment, trustedLocal)`; companion `ResolveWithPolicy`.
- Recipe candidate SHA (verify against): `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d`.

### Witnesses

- `git ls-remote --heads origin` shows the SHA only as a remote-side ref pointer:
  `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d  refs/heads/cli2-env-policy-head`
- `git cat-file -t e5ad8a6882550168ea262b18dfbdf8c2e4518c1d` → **fatal: could not get object info** (object not present in this clone).
- `git grep -n "ManagedEnvironmentWithPolicy\|ResolveWithPolicy" e5ad8a68...` → **fatal: unable to parse object: e5ad8a68...** (the SHA is not a resolvable tree/blob here).
- `git show <candidate>:internal/operatorauth/config.go` → **fatal: path ... exists on disk, but not in '<candidate>'**.
- Search across current tree AND all of git history (`git log --all -S ...`): **no matches** for either `ManagedEnvironmentWithPolicy` or `ResolveWithPolicy`.
- Current working branch `cli2-org-env-head` HEAD = `b85efaf6c94cd158de68a6b8f837dc4a23be455a`; last commit `internal/deployment: env-registry app/target/node association on environment.json (0428-054)`. The operator-auth policy helper the recipe names is absent from this branch too.

### Conclusion

- The recipe's described code (`ManagedEnvironmentWithPolicy`, `ResolveWithPolicy`) exists nowhere I can verify: not in the working branch, not in git history, and the candidate SHA `e5ad8a68` is an unverifiable remote-side ref in this clone (cannot read its tree or the referenced file).
- Additionally the recipe names a different integration branch (`cli2-env-policy-head`) than my assigned branch (`cli2-org-env-head`). AGENTS 3.8 / mission: exactly one integration candidate per chain; I must stay on the named candidate.
- The recipe's own STOP criterion applies: if the bool semantics it assumes are not the one encoded by the current code, report file:line to the coordinator instead of acting unilaterally. The precondition of the fix (the helper existing to correct) is not met.

### Evidence provenance (on origin/main)

- Push witness: `To https://github.com/mcpdev80/baseharbor-plan.git  90df3b46..ac66ddd8  main -> main` — my commit `ac66ddd8` reached origin/main.
- `git merge-base --is-ancestor ac66ddd8 origin/main` → **YES** (after `git fetch origin main`), confirms `ac66ddd8` is on origin/main (an ancestor; other lanes advanced the tip to `03903828`).
- `git ls-tree --name-only ac66ddd8 evidence/r28-welle1-2026-11-15/cli2-env-policy/` lists `act-luna-r1.md` and `round-2.md`.
- Note: `git ls-remote origin/main` returns a transport error in this clone (`fatal: 'origin/main' does not appear to be a git repository`); the push line above plus the successful fetch/ancestry check are the authoritative witnesses for presence on origin/main.

### Repo-rule compliance

- No product file written, no branch cut, no push of anything but my own plan-evidence, no force-push.
- `.github/**` untouched. No CI dispatch/rerun. No merge. No subagent.
- Evidence written only in baseharbor-plan (the planning repo). Plan repo working tree shown below; local uncommitted edits (perses round-2 files) belong to another lane — left untouched.

## END

END_DONE
BLOCKED — scope/verification mismatch: recipe helper `ManagedEnvironmentWithPolicy`/`ResolveWithPolicy` absent from working branch AND git history; candidate SHA `e5ad8a68` is an unverifiable remote-side ref in this clone (not a resolvable tree/blob; `git grep` → "unable to parse object"); named branch `cli2-env-policy-head` differs from assigned candidate `cli2-org-env-head`. No code change, no branch cut, no force-push. Awaiting Owner/coordinator decision: either rebase this lane to the recipe's candidate branch, or supply a corrected recipe with a resolvable SHA.

Evidence provenance: push `90df3b46..ac66ddd8` and `03903828..60d940d6` on plan origin/main; `git merge-base --is-ancestor ac66ddd8 origin/main` → YES.
