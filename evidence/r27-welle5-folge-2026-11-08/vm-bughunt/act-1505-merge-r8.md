# CODEX-MERGE 0427-173 r8 — PR #1505

ROLLE: MERGE

## Pre-merge verification

- Owner-authorized standalone merge instruction received for PR #1505 head `a42822f542436651a6f0df94f574574632648dc8`.
- Live PR head remained exactly `a42822f542436651a6f0df94f574574632648dc8`; base develop was `942111d5a1c43f5257bf1627a966fa9e6c6f24bd`.
- Review act `act-1505-review-r8.md` records APPROVE for the exact head.
- Run `42590616765` was terminal success on the exact candidate. `PR Selected Checks` from GitHub Actions integration 15368 passed; deployment-package-tests, go-unit-tests, build, vet, gofmt, docs and destroy-retry Docker/Podman passed. Native Keycloak/Core and other displayed unrelated cells were skipped and not counted as green.
- No unresolved review threads. `develop` rulesets 23754541 and 25223521 reported `enforcement=disabled`; branch protection endpoint returned 404. No approval override or CI bypass was used.

## Merge and develop verification

Executed the normal squash merge with expected-head guard:

`gh pr merge 1505 --repo mcpdev80/baseharbor --squash --match-head-commit a42822f542436651a6f0df94f574574632648dc8`

GitHub reports PR #1505 merged at `2026-11-09T09:32:25Z`; merge commit is `e072e142ec9511f3cc86ffa67c7debd022d7760a`. `git ls-remote` witnessed:

`e072e142ec9511f3cc86ffa67c7debd022d7760a refs/heads/develop`

Post-merge develop runs on that exact merge commit both completed successfully:

- Runtime · Docker Core: run `42594213927`, success.
- Runtime · Podman Core: run `42594213963`, success.

Planning task `t-20261108-bughunt-app-prune-dangling-record` remains in review because its dependency `t-20261108-bughunt-list-stale-after-kill` is not yet accepted. The product merge is confirmed; no premature task closure was recorded.

END 0427-173 r8 MERGE: merged by squash without force or bypass; develop head `e072e142ec9511f3cc86ffa67c7debd022d7760a`; post-merge Docker and Podman Core runs succeeded.
