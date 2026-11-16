# Round 4 — r28 cli2-identity-secrets test-invariant port (card t-20261114-r28-cli2-identity-secrets, PR #1615)

Role: worker (session w073-perses-alerts). Model verified at session start.
Scope: port the ONE test-invariant loosening in `cmd/baha/agent_mcp_test.go` from the lane branch #1623 (`lane-0428-063-cli2-app-interact`) onto `cli2-identity-secrets-head` as exactly one fast-forward commit. No product change, no `.github/**`, no merge, no force-push, no subagent.

## BASE ATTESTATION
- Branch cut FROM (secrets-head): `bb5bb367641adbef92d2ade8651adf96bfd93d9a` (ls-remote below, `refs/heads/cli2-identity-secrets-head`).
- This SHA is an ancestor of my single commit (FF-only confirmed: `git merge-base --is-ancestor bb5bb3676... HEAD` → YES).
- My commit's parent is exactly `bb5bb3676...`. No other candidate carried on top: `git log bb5bb3676..HEAD` lists ONLY my commit.

## 1. REMOTE WITNESSES (via `git ls-remote origin`)
BEFORE push:
```
bb5bb367641adbef92d2ade8651adf96bfd93d9a	refs/heads/cli2-identity-secrets-head
4463ac61745c060ef0c55b904d800c54e434b680	refs/heads/lane-0428-063-cli2-app-interact
```
AFTER push:
```
8963efd8a1e48e4072e11f98b571b4ee334615dd	refs/heads/cli2-identity-secrets-head
```
- `cli2-identity-secrets-head` = `bb5bb3676...` (matches mission head).
- `lane-0428-063-cli2-app-interact` = `4463ac61...` (source of the loosening).

## 2. DIFF ZEUGE (step 1 of mission)
`git diff origin/cli2-identity-secrets-head origin/lane-0428-063-cli2-app-interact -- cmd/baha/agent_mcp_test.go`
```
diff --git a/cmd/baha/agent_mcp_test.go b/cmd/baha/agent_mcp_test.go
index 17d02e0e0..22f3afaec 100644
--- a/cmd/baha/agent_mcp_test.go
+++ b/cmd/baha/agent_mcp_test.go
@@ -43,7 +43,10 @@ func TestAgentDescribeJSON(t *testing.T) {
 		t.Fatalf("destroy safety metadata = %#v", destroy)
 	}
 	for _, operation := range got.Operations {
-		if operation.MCPTool == "" {
+		// Human-only authorization seams (secret.reveal, 0428-057) and host-
+		// only execution categories (app.exec, 0428-063; #787) carry no MCP
+		// tool by design and say so in the operation description.
+		if operation.MCPTool == "" && !strings.Contains(operation.Description, "MCP tool boundary by design") {
 			t.Fatalf("operation missing MCP tool: %#v", operation)
 		}
 	}
```
- Only `cmd/baha/agent_mcp_test.go` changes in scope.
- Full-tree diff on the lane carries many unrelated functional changes (e.g. `cmd/baha/app_access.go` app-logs rewrite with `parseReadOutputArgs`/`selectWorkloadComponentsForCommand`/`readViewLogsSelection`) — those are OUT OF SCOPE and intentionally NOT ported.
- My applied change is byte-identical to the lane loosening (`git diff origin/lane-0428-063... -- cmd/baha/agent_mcp_test.go` → empty).

## 3. APPLICABILITY DECISION (step 2)
- On secrets-head the "before" block is byte-identical: `strings` already imported (line 8 of the file); the guarded line is exactly `if operation.MCPTool == "" {` (line 46).
- Context lines match the lane's "before" exactly. No conflict. DECISION: YES — port the change as one commit.

## 4. APPLY (step 3)
- Checked out `cli2-identity-secrets-head` at `bb5bb3676` (FF-only; refspec push `origin HEAD:refs/heads/cli2-identity-secrets-head`).
- Applied exactly ONE commit with the loosening.
- Commit: `8963efd8a1e48e4072e11f98b571b4ee334615dd` — "port agent_mcp test-invariant to cli2-identity-secrets-head (human-only/auth and host-only seams carry no MCP tool by design, #1615 / lane 063)".
- refspec push: `git push origin HEAD:refs/heads/cli2-identity-secrets-head` → `bb5bb3676..8963efd8a  HEAD -> cli2-identity-secrets-head` (PUSH EXIT 0).
- new head (ls-remote witness AFTER push): `8963efd8a1e48e4072e11f98b571b4ee334615dd`.
- NOTE: GitHub printed a pre-existing dependabot advisory (3 vulns on default branch) on push — unrelated to this one-line test change; not a gate failure.

## 5. PROVENANCE (branch)
- `git log --oneline bb5bb3676..HEAD` lists ONLY my commit; its parent is `bb5bb3676...` (the base).
- `git merge-base --is-ancestor bb5bb3676... HEAD` → YES (fast-forward only).

## 6. TESTS (step 4)
`go build ./...`:
```
BUILD EXIT: 0
```
`go test ./cmd/baha/ -run TestAgentDescribeJSON -count=1`:
```
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.009s
```
targeted secret tests (secret.reveal / secret command scope / adapter requirements):
```
=== RUN   TestAppMachineAdaptersManagedSecretsRequirements
--- PASS: TestAppMachineAdaptersManagedSecretsRequirements (0.00s)
=== RUN   TestApplicationSecretCommandsAreDiscoverable
--- PASS: TestApplicationSecretCommandsAreDiscoverable (0.00s)
=== RUN   TestVerifyApplicationSecretScopeRecordsUsesProtectedDeploymentCredentials
--- PASS: TestVerifyApplicationSecretScopeRecordsUsesProtectedDeploymentCredentials (0.00s)
=== RUN   TestVerifyApplicationSecretScopesSkipsExplicitlySecretlessApps
--- PASS: TestVerifyApplicationSecretScopesSkipsExplicitlySecretlessApps (0.00s)
PASS
ok  	github.com/mcpdev80/baseharbor/cmd/baha	...
```
agent + MCP test group:
```
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.935s
```

## REPO-RULE COMPLIANCE
- No `.github/**` touched. No merge, no ready_for_review, no force-push, no subagent (§4.8). No second candidate branch (exactly one candidate per chain; worked on `cli2-identity-secrets-head`, the branch named in the mission). Evidence lives only in baseharbor-plan (`evidence/r28-welle1-20261115/cli2-identity-secrets/round-4.md`), never in the product repo. FF-only commit, base attested as ancestor.

## END
<END_DONE mission-secrets-r4-invariant.md: port agent_mcp test-invariant to secrets-head — new head 8963efd8a</END_DONE>
