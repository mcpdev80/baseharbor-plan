# r27 image-transfer — Evidence (Round 1, Lane w225)

## PLAN

- Read mission + card; verify base (origin/develop ea656d1fcfce9ee14145a8dfaffb9e993fd29497); create work/r27-image-transfer worktree under /tmp/opencode/w225-wt
- Decide transfer path (native registry pull/copy over OCI) vs target-native store vs save/load/OCI archive; record rationale + rejected alternatives in this file
- Implement cmd/baha/application_image_transfer.go: digest-preserving copy + immutable reference (no trunk-drift) + explicit failure on transfer-target errors (no half-success)
- Write positive (digest-preserving copy, digest/architecture verification) + negative (hostile/truncated archive, wrong digest, wrong architecture, tag drift) tests, all real
- Local gates: build, vet, gofmt, race-20
- Hosted Docker + Podman isolated load/pull smokes on named SSH hosts only
- Push candidate, draft->ready PR against develop; show base SHA as ancestor + real ls-remote == head
- Publish evidence to origin/main (ls-tree witness), bring down compose, END to coordinator

## Base attestation

- Base ref cut from: origin/develop
- Base SHA: ea656d1fcfce9ee14145a8dfaffb9e993fd29497
- Branch: work/r27-image-transfer (new, per mission; no existing remote branch)
