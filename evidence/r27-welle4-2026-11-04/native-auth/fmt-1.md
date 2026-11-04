# w93-nativeauth-fmt — gofmt native credential adapters

- Task: w93 micro-fix on existing PR #1362 (branch work/r27-native-auth head 3c17b24). Only red CI check = "PR . Source format" (gofmt). Format ONLY `internal/credential/native/sources.go`, no content change, no renaming.
- Coord: f49a3303. Evidence SHA target: fmt-1.md (bullets, no markdown checkboxes anywhere).
- END: END_DONE w93-nativeauth-fmt: head=ed0c99b1 gates=gruen lsremote=ed0c99b1 | PR #1362 now fully green: previously-red "PR · Source format" gate (job 126484457479) SUCCESS, whole CI · Source & Quality workflow 41803412038 green; go build/vet/native 11/11 tests green locally at ed0c99b1

## PLAN

- Step 1: Read mission + predecessor w89 contract; verify baseharbor repo, PR #1362, branch work/r27-native-auth. Create worktree /tmp/opencode/w93-fmt-wt @ 3c17b24.
- Step 2: Reality check — gofmt -l internal/credential/native/ = exactly one red file: sources.go.
- Step 3: gofmt -w sources.go (formatting only); confirm gofmt -l empty.
- Step 4: go build ./... + go test ./internal/credential/... -count=1 green; git diff shows only whitespace/format.
- Step 5: Commit style(credential): gofmt native adapters; push; ls-remote == head.
- Step 6: Watch PR . Source format gate + changed go-unit end-of-run (own run); finalize evidence + board JSON + post END_DONE.

## CI evidence (own run)

- PR #1362 headRefOid = ed0c99b1 (state OPEN, draft) on branch work/r27-native-auth; git ls-remote origin == ed0c99b1 == local head.
- CI run 41803412038 (workflow "CI · Source & Quality", trigger pull_request) = green: Workflow policy SUCCESS, PR · Source format SUCCESS (job 126484457479). All product gates (Release Source Preflight, Targeted HA docker/podman, PR · Exact Candidate, PR · Consumer Pins, PR · Selected Runtime, PR · Public Contracts, etc.) correctly SKIPPED — single-file formatting change does not trigger product gates.

## repo-rule compliance

- Scope: formatting only, per mission. No content, no renaming, no new behavior. gofmt is the canonical Go formatter; applying it cannot introduce logic changes.
- CI rule 5.3/5.4: smallest matching gate (gofmt source-format), reuse existing green evidence for unchanged SHA where applicable.
