# H-V24 operator-auth ACTIONABILITY census — ## PLAN

READ-ONLY bug-hunt (AGENTS §3.3.5; Befund only; NO product/PR/merge/subagents §4.8).
Scope: operator-auth messaging on develop. Judge, per operator-facing denial on the develop
surface, whether the message tells the operator the concrete next command/flag (actionable)
or is a bare denied/unauthorized (NOT actionable). No product changes. Draft card proposals
text-only, filed as a card proposal, not implemented.

## Base / provenance
- Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (verified via `git -C baseharbor-plan remote -v`)
- Product remote used for evidence: `https://github.com/mcpdev80/baseharbor.git` (the github.com/mcpdev80 remote; NOT the quarantined workers/checkout)
- develop HEAD (remote, `git ls-remote`): `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2` `fix(0428-249): build baha-ci-operator-testonly artifact with its build tag (#1825)` — matches mission's expected 46d3dccc-line, after #1825
- Base attest: `git merge-base --is-ancestor 46d3dccc... HEAD` -> TRUE (46d3dccc IS the develop HEAD, verified ancestor)
- Worktree: /tmp/opencode/w82-hv24-actionability-wt (full clone, branch develop @ 46d3dccc)
- Hosted-only: no local go test/docker executed. Read-only source scan.

## Scan method
1. Read operator-auth core: internal/operatorauth/authorization.go (#1717 opaque local grants, #1821 removed dead trusted-local fail-open arm, :285 fail-closed :285), internal/machine/contract.go (Error struct + Next field).
2. Traced CLI display path: cmd/baha/main.go:244 formatCLIErrorVerbose -> renders `Message`, optional `Resolution` (Remediation), optional `What to do` (Error.Next); cmd/baha/operational_errors.go:35 classifyOperationalFailure; cmd/baha/secret_operations.go:89 classifySecretOutcome.
3. Grep every operator-facing denial string in cmd/baha/app_commands.go + cmd/baha/mcp.go + operatorauth paths + secret/environment/app_interact reveal seams.

## Message table (file:line | string | actionable Y/N)

| file:line | message string | actionable? | why |
|---|---|---|---|
| internal/operatorauth/authorization.go:287-294 | "Managed-environment machine operations require an authenticated BaseHarbor operator." + Next: "Authenticate the operator for the selected Target and environment, then retry the same operation." | YES | Names the next action (authenticate for that Target+environment, retry). |
| internal/operatorauth/authorization.go:339-346 (RequireHumanOperator) | "A human secret reveal requires an authenticated BaseHarbor operator; the runtime/workload identity cannot satisfy it." + Next: "Authenticate the operator for the selected Target and environment, then repeat the reveal." | YES | Explicitly explains why runtime identity fails and names next step (operator authenticate, repeat reveal). |
| cmd/baha/mcp.go:328-336 (ensureManagedEnvironmentOperatorBoundary wrap) | "Managed-environment machine operations require an authenticated BaseHarbor operator." + Remediation: "authenticate the BaseHarbor operator" + Next: "Configure operator OIDC if required, run 'baha login' for the selected Target/environment, then retry." | YES | Best-in-class: names `baha login` with the exact flag shape for the selected Target/environment. |
| cmd/baha/operator_auth_boundary.go:124 | usageError "operator authentication needs interactive setup but input is not a terminal" + hint "Configure operator OIDC using explicit environment settings or re-run in an interactive terminal; BaseHarbor will not prompt on piped input." | YES | Names concrete next command (environment settings or interactive terminal). |
| cmd/baha/operator_auth_status.go:51-52 (app plan `Operator access:` line) | Status token `NOT_CONFIGURED`, Detail "operator authentication is not configured for this Target/Environment boundary" | PARTIAL | States the fact (not configured) but does NOT name the remediation command; the user must already know to run `baha login`. Not a denial, but a read-only status with no actionable next step. |
| cmd/baha/operational_errors.go:35 | "Authentication or authorization failed." + Next: "Verify the configured credentials/permissions and retry." | PARTIAL | Bare-ish: generic message, Next is vague ("verify credentials") and does not name `baha login`. Matches the NOT-actionable bar only for the non-operator-auth path (image/source pull, etc.), not for the operator-auth core denials. |
| cmd/baha/app_commands.go (Operator access line, ~348) | "Operator access: <mode> · <status> · <session>" e.g. "operator authentication is not configured" | NO | A status label, not a denial; no command/flag is named. Not actionable. |

## Befund (findings)
- The operator-auth denial strings themselves (authorization.go :285, RequireHumanOperator :339, mcp.go :328) are all ACTIONABLE: every one carries a non-empty machine.Error.Next that the CLI renders as a `What to do` line, and the mcp.go path even names `baha login`. The #1717 auto-admit removal and #1821 fail-closed arm did NOT sacrifice actionability in the operator-facing surface.
- One genuine NOT-actionable (weak) finding: cmd/baha/operational_errors.go:35 "Authentication or authorization failed." + Next "Verify the configured credentials/permissions and retry." — bare denial, Next does not name `baha login`. But this path is the generic transport-layer classifier (image/source pull, docker/podman 401), NOT the operator-auth seam the census targets. So it is a real but tangential weak-finding.
- Status-only non-actionability: cmd/baha/operator_auth_status.go:51-52 NOT_CONFIGURED and the app_commands.go Operator-access label report the fact without naming the remediation command. Worth a card: surface the next command when status != READY.

## Card proposals (text only, NOT implemented)
- Card A (targeted to census scope): `t-<NNN>-operator-auth-bare-transport-denial` — title: "bare transport-layer auth-failure Next does not name baha login"; regression idea: a test on `classifyOperationalFailure` for a `Unauthorized` docker/image error asserts Next references the credential/credentials/`baha login` remediation rather than a generic "verify credentials".
- Card B (status/actionability): `t-<NNN>-operator-auth-status-implies-command` — title: "`app plan`/`app inspect` Operator-access NOT_CONFIGURED status does not surface the remediation command"; regression idea: when `collectOperatorAuthObservation().Status != "READY"`, append the next command (e.g. `baha login`) to the printed status block.

## repo-rule compliance
- Read-only scan only. No product files edited. No .github/** touched. No local test suite or docker executed. Subagents: none.
- Evidence lives in baseharbor-plan evidence/ (not in a product repo). One atomic evidence commit + optional card commit.

## STOP / END status
- Befund: 1 tangential weak finding (operational_errors.go:35) + 2 status-only actionability gaps. All operator-auth CORE denials are actionable. Card proposal drafted (Card A), no card committed yet — awaiting Owner scope decision on whether a card is warranted (the census core denials are actionable; the one weak finding is outside the operator-auth seam).
- END line: (pending Owner decision on card)
