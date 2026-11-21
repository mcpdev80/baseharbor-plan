# 0427-186 review on #1588 — 2026-11-21

- PR #1588: https://github.com/mcpdev80/baseharbor/pull/1588
- Candidate SHA: `993b3ec062d27e7e792e27e6a73ffbb4189e3403`
- Exact `pull_request` run: [44895998000](https://github.com/mcpdev80/baseharbor/actions/runs/44895998000) completed success at that SHA, with base `develop` at `57d2f2751086b8c918a5a460aa87eb5db002335a`.
- Current develop subsequently advanced when #1665 merged at `77c1e60f51b91003ac3ddc391008c15e4a713a5c`; the #1588 run is therefore not current-base merge evidence.

## Review findings

1. `internal/deployment/immutable_provenance.go` `FromVerifiedCandidate` treats `sourceAvailable == true`, repository kind, a non-empty repository path and a non-empty digest as proof that the source is verified, clean, committed and on a verified remote. It sets `Dirty=false`, `CommitVerified=true`, `RemoteCommitVerified=true` without inspecting the worktree, commit or remote.
2. It leaves `Branch` empty. The policy evaluator denies every configured `AllowedBranches` policy when branch is empty, so the provided test/staging/production branch presets cannot admit a valid candidate.
3. `AdmissionEvidenceForApplyingMutation` sets approval verified when passed the policy's `requireApproval` setting. That couples proof to the requested policy flag rather than to an independently checked approval. The candidate consent check later in the mutation path is a separate check and must be bound to the exact candidate before admission evidence claims approval.
4. OCI verification is inferred from source kind and a non-empty digest. The applying record path currently writes repository sources, and the helper does not verify an OCI manifest/digest against the delivered artifact.
5. `executeRemoteApplicationApply` evaluates the previously persisted source record before the mutation path constructs and validates the current candidate. The final admission must bind to the candidate that is about to be recorded/applied, not stale prior source state.

These findings make the current code fail-closed for missing branch evidence in common paths, while also allowing the helper to overstate source/remote/approval facts. A green run is not acceptance. Card 0427-186 is active for remediation; no merge has been attempted.
