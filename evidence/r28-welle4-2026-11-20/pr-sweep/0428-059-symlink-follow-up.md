# 0428-059 post-merge symlink containment follow-up

Date: 2026-11-20

## Verified candidate

- PR: https://github.com/mcpdev80/baseharbor/pull/1706
- Branch: `codex/0428-059-symlink-containment`
- Base: `develop` at `15727ca8878938df7e924319c236c0bcc4a4201c`
- Exact candidate: `930df12a482595bba06748ded501fe082f0aab76`
- Exact hosted run: https://github.com/mcpdev80/baseharbor/actions/runs/44635693057 — terminal SUCCESS at the exact candidate; `PR Selected Checks` SUCCESS.
- Merge: https://github.com/mcpdev80/baseharbor/commit/97abbe1572a74170e3414448fe2dce843309c10a — PR merged 2026-11-19 23:19:12 UTC; remote `develop` verified at this SHA.

## Defect and correction

Post-merge review of #1595 found that local workspace subpaths could escape their intended root through symlinks, and repository tree fingerprinting could follow symlink targets. The follow-up canonicalizes and validates resolved paths against the permitted root, and fingerprints symlink link text using `Lstat`/`Readlink` without traversing targets. Regression coverage exercises local and repository subpath escapes, dangling/external links, target-content invariance, retargeting and type changes. No `security.go` change.

## Verification

Local focused tests passed:

- `go test ./internal/development -count=1`
- `go test ./cmd/baha -run '^(TestResolveWorkspaceRejectsSubpathSymlinkEscapes|TestResolveWorkspaceLocalDirectoryWithSubPaths|TestWorkspaceSourceModelWritesRequireUpdatePermission|TestRepositoryTreeFingerprintDoesNotFollowSymlinks|TestRepositoryDesiredStateFingerprintTracksLocalSourceFiles)$' -count=1`
- `go vet ./internal/development ./cmd/baha`
- `go build ./cmd/baha`
- source-readability audit and `git diff --check`

The exact hosted run passed selected Go shards/packages, focused Python, build, vet, source-format, workflow policy, native gate plan and trusted plan. Native Docker/Podman, runtime and release gates were skipped by the impact selection; this path-containment/fingerprint correction did not alter runtime service behavior or CI. An independent review of the exact diff found no blocker. No release or tag was created.
