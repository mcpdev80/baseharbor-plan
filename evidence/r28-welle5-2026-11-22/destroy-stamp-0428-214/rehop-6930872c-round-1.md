# 0428-214: PR #1738 re-hop round onto develop 6930872c

- karte 0428-214, sitz f0f6c8b4. PR #1738 re-hop. develop 6930872c (coreinst #1781 GEMERGT).
- My 241 is consolidated on #1780 — DO NOT push/touch #1780. Now only the additive re-hop of #1738 onto new develop.
- #1738 recut head = 2ba70a5 (owner, single-file cmd/baha/core_installation_runtime_test.go). core_installation_runtime_test is NOW cataloged (via #1781) -> Trusted Plan should pass.

## PLAN

1. Establish reality (remote guard, develop 6930872c via ls-remote, #1738 recut 2ba70a5).
2. Move branch lane-0428-214-destroystamp to develop 6930872c: git fetch origin develop; git merge --no-ff origin/develop (additive, second parent = develop-head, NO rebase/force/amend/force-with-lease). diff vs develop = ONLY cmd/baha/core_installation_runtime_test.go. Confirm log line lists only my commits.
3. Normal push, PR#1738 base=develop 6930872c, promote ready, exact-hosted. Prove delivery with git ls-remote. DO NOT touch #1780.
4. Exact run: Trusted Plan must now pass (coreinst cataloged via #1781) + four data-capabilities jobs (native+selected docker+podman). If selected still hangs on footprint-consent (#1780/241) = only report status, NOT my scope. Watch to terminal.
5. Write akte + END + cleanliness. Publish to baseharbor-plan origin/main (ls-tree verify). Post to coordinator.

## BASE ATTESTATION

- develop HEAD (ls-remote, github.com/mcpdev80): <paste from git ls-remote after fetch>.
- #1738 recut 2ba70a5: ancestor relationship confirmed.

## END

w27-pr1627-0428-061-pull <DONE|BLOCKED> — 0428-214 / PR #1738 re-hop. branch, head, PR#1738, run-id, 'cleanliness:'.
