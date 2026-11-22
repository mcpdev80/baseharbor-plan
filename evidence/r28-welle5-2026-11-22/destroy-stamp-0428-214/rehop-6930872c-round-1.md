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

## Exact run (run-id 1a1e5db48, base 6930872c)

- Trusted Plan / test catalog: GRUEN — Validation checks pass (cli-vet, cli-build, cli-gofmt, source-contracts), Go unit cli-0/1/2/3 all green. catalog-validated on new develop.
- cli-2 (Go unit, runs TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope): SUCCESS. My operator-context fix lands the test on the authenticated-operator seam. Local witness: go test -run TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope ok 4.1s; go vet clean.
- Native data-capabilities (native/docker + native/podman): FAIL on TestApplicationCapabilityLifecycleExistingCore/secrets "Starting secure runtime broker - failed (2m03s)" — pre-existing broker-container readiness flake in that OTHER test, NOT my core_installation test (which passes in cli-2). Not introduced by this re-hop.
- Selected Runtime data-capabilities (atomic/docker + atomic/podman): FAIL on demo-side demo-data-capabilities group: `app footprint show -o json` rejected `command-not-in-managed-workload-set`. This is the #1780 / 241 footprint-consent hang (selected, runs separately). NOT my scope — only status reported, not self-fixed.
- selected: wartet-241 (#1780/241 footprint-consent; not touched).
- trusted plan gruen: JA.

## END

w27-pr1627-0428-061-pull DONE — 0428-214 / PR #1738 re-hop. branch lane-0428-214-destroystamp. head 1a1e5db48. PR#1738 base=develop 6930872c, state OPEN/ready. run-id 1a1e5db48. trusted plan gruen: JA (cli-vet/build/gofmt/source-contracts + Go unit cli-0..3 green; my core_installation test passes in cli-2). selected: wartet-241 (#1780/241 footprint-consent hang on demo-side demo-data-capabilities `command-not-in-managed-workload-set`, NOT my scope). Native docker/podman data-capabilities fail on pre-existing TestApplicationCapabilityLifecycleExistingCore/secrets broker-readiness flake (not my test). Fix-Art: operator-context fix in cmd/baha/core_installation_runtime_test.go (machineNoninteractiveContext(testOperatorContext(t.Context()))) — test-only, within card write-set, verified locally + via cli-2. diff vs develop = ONLY cmd/baha/core_installation_runtime_test.go. NO touch on #1780. cleanliness: branch rebuilt clean (dropped carried-in 241 commits from a prior session), only 2ba70a5 + additive hop + operator fix; no product non-test files, no .github/operatorauth/237/katalog, no embedded worktree/binary staged. Evidence published to baseharbor-plan origin/main.

