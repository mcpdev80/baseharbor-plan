# Independent read-only review — PR #1627 / 0428-055

Reviewed 2026-11-19.

- Live PR is open and Draft at head `49e164ccbd6552a98854ceceaabfafa748775ed1`, based on `cli2-env-policy-head` `5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3`.
- No exact-head workflow runs or statuses. Its base PR #1594 and predecessor #1591 are also open Draft stack entries. Exact checks and rebasing onto a current accepted base are therefore still required.

## Finding — environment destroy preview exceeds the applied operation

The preview says scoped deployments will be removed, but the confirmed path calls only `deployment.DestroyEnvironmentIdentity(...)`. That function removes the environment identity directory and leaves deployments/runtime resources in place. The `--delete-data` branch likewise records additional typed consent but does not invoke a data deletion operation, while the result describes that deletion as consented. The existing integration test checks identity removal and sibling environment state, not scoped deployment/runtime/data removal or partial failure/retry behavior.

This is a lifecycle correctness blocker: report only what the apply path actually does, or implement and verify the promised deletion semantics before making the destructive claim. Do not merge on current evidence.

No PR/product files, comments, claims, or merge state were changed by this review.
