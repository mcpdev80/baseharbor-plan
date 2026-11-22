# 0428-241: PR OPEN round — footprint-show + record-deployment digest-consent harness

- karte 0428-241, sitz f0f6c8b4. TASK: open the finished footprint-digest-consent candidate as a PR. develop 3939aa5.
- Candidate: branch lane-0428-241-footprint-consent-harness head 68b26bd78 (test TestApplicationCapabilityLifecycleFootprintShowDigestConsent + scripts/ci-native-pr-gate.sh:83-84). Unit green, vet clean (previous shift evidence, fix-round-1.md).
- Base 68b26bd7 was stale (develop now 3939aa5). Move branch onto develop 3939aa5 via additive merge --no-ff, push, open one PR for card 0428-241, promote ready, exact-hosted.

## PLAN

1. Establish reality (remote guard, develop 3939aa5 via ls-remote, base 68b26bd78 ancestor of HEAD).
2. Move branch to develop 3939aa5: git fetch origin develop; git merge --no-ff origin/develop (additive, second parent = develop-head, NO rebase/force/amend). diff vs develop = ONLY footprint-consent test file + scripts/ci-native-pr-gate.sh (+ pre-release-integration.py if CORELESS_SHARD_TESTS). Confirm log line lists only my commits.
3. Normal push, open PR on develop (one PR for card 0428-241), promote ready, exact-hosted. Prove delivery with git ls-remote.
4. Exact run: selected docker+podman data-capabilities + native cells must now execute the footprint-show '-o json' record-deployment CELL with digest-consent GREEN. 'selected gruen: ja/nein' + run-id.
5. Write akte + END + cleanliness. Publish to baseharbor-plan origin/main (ls-tree verify). Post to coordinator.

## BASE ATTESTATION

- develop HEAD (ls-remote, github.com/mcpdev80): <paste from git ls-remote after fetch>.
- base 68b26bd78c3de89e11252e6d04a8d3ed16c804a7: ancestor of HEAD (git merge-base --is-ancestor origin/68b26bd... HEAD).
- git log --oneline origin/develop..HEAD lists ONLY my own commits.

## END

w27-pr1627-0428-061-pull <DONE|BLOCKED> — 0428-241: PR opened. branch, head, PR-number, class, run-id, 'cleanliness:'.
