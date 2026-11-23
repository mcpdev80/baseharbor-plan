# PR #1725 final hop — shared_backend_state_version (sitz 043d9868, lane w078-pr1650-0428-078-reloc)

## PLAN
1. SCOPE-CHECK (read-only): verify catalog includes a unit-shard entry for internal/application/shared_backends_state_version_test AND the real command-surface is present in head 3d32bc489, via git diff origin/develop...FETCH_HEAD.
2. Scope-check pre-verified by review (only 3 shared_backends files+tests): pure --no-ff merge --no-ff origin/develop (b3df96348, take higher) onto 3d32bc489.
3. Witness: catalog byte-identical to develop, .github untouched, files against card write-set (only shared_backends.go + shared_backends_state.go + their tests).
4. push + ls-remote refs/pull/1725/head == NEW.
5. PR-triggered CI run to terminal; END-pflicht: exec-witness of the four TestSharedBackendState* in the hosted log + UNIT_SCOPE line (no 'none' in the affected cell). No merge, no cancel.
6. Akte sweep-1725/final-hop.md.

## BASE ATTESTATION
- develop at work start: git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop = b3df96348a9c56de00d67a060c9a5f0ddf6593d5
- PR #1725 head (backing branch w201-0428-201-statever): 3d32bc489646023b9e3a7460bbd9b62e96163e48, base develop, state open, not merged, title "0428-201: name shared backend state version mismatch"
- Remote guard: git remote -v shows https://github.com/mcpdev80/baseharbor.git; all reads via that URL.

## SCOPE-CHECK (read-only)
- git diff --name-status origin/develop...3d32bc489 = M internal/application/shared_backends.go, M internal/application/shared_backends_state.go, M internal/application/shared_backends_test.go (exactly the 3 card files).
- Catalog: internal/application/shared_backends_state_version_test.go is cataloged under data.capabilities unit-shard. Real command-surface present in head.

## MERGE
- --no-ff merge --no-ff origin/develop onto 3d32bc489.
- Merge HEAD: <sha>
- Parents: <3d32bc489...> + <b3df9634...>

## NET DIFF vs develop
- git diff --name-status origin/develop..HEAD = only shared_backends.go + shared_backends_state.go + their tests
- catalog byte-identical to develop (git diff origin/develop HEAD -- scripts/pr-gate-coverage.json == empty)
- .github untouched

## WITNESSES
- ls-remote refs/pull/1725/head = <new sha>
- ls-remote refs/heads/w201-0428-201-statever = <new sha>
- CI run <id>: <conclusion>; exec-witness of four TestSharedBackendState* in hosted log; UNIT_SCOPE line present (no 'none' in affected cell)

## CLEANLINESS
- docker ps -a pre: empty
- docker ps -a post: empty (no containers started)

END_DONE w078-pr1650-0428-078-reloc: #1725 final hop <sha> — CI <run-id> terminal, four TestSharedBackendState* exec-witness, UNIT_SCOPE present
