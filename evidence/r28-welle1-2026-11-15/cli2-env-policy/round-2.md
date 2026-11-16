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

### Repo-rule compliance

- No product file written, no branch cut, no push, no force-push.
- `.github/**` untouched. No CI dispatch/rerun. No merge. No subagent.
- Evidence written only in baseharbor-plan (the planning repo). Plan repo working tree shown below; local uncommitted edits are a different lane's perses round-2, not mine — left untouched.

## END

BLOCKED — scope/verification mismatch: recipe code does not exist at any verifiable input; candidate SHA not resolvable in clone; branch name differs from assigned candidate. Awaiting Owner/coordinator decision (rebase to the recipe's candidate branch, or a corrected recipe with a resolvable SHA).
