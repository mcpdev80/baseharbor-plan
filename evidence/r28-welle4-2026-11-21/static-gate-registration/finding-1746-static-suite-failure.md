# PR #1746 full static suite failure - finding classification (2026-11-21)

ROLE: coordinator evidence, read-only measurement. No product change.

## Witness

- Candidate: `refs/pull/1746/head` = `9ddcde356e9ed452ddbf00440ab8189add586d3e`, base `develop` = `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3`, back=0, ahead=4.
- Isolated gate run `44943804395` (`atomic/static/ci-fast-check`, demo pin `5d1cf312e18d06915db35c340bebe4e3d4f39d45`): completed/success.
- Full static run `44944570763` (all six v0.4.28 static gates): completed/failure. Failing jobs:
  - `136970241182` Static - shell-ux (59953 bytes), `136970241191` Static - init (62178 bytes),
    `136970241203` Static - config-matrix, `136970241277` Static - mcp (59810 bytes), plus `136970326775` Pre-Release Checks.
- Log lines (de-escaped, verbatim substrings):
  - init + shell-ux: `authenticate the BaseHarbor operator` / `Configure operator OIDC if required, run 'baha login' for the selected Target/environment, then retry.`
  - mcp: `RuntimeError: MCP contract mismatch: missing=[] unexpected=['baseharbor.app.perses.disable', 'baseharbor.app.perses.enable', 'baseharbor.app.perses.remove', 'baseharbor.app.perses.status']`

## Classification

1. **init / shell-ux / config-matrix = inherited prerequisite, not PR #1746.** Same failure class as the red `cmd/baha` cases in card `0428-223` (t-20261121-develop-full-suite-red) and as PR #1723/#1725: the managed operator-auth context is not established in the static gate environment, so the gate fails closed on `baha login`. Card `0428-223` is the single owner of that prerequisite; #1746 inherits it. No lane may weaken the auth check.
2. **mcp = card 0428-225 (t-20261121-mcp-release-gate-perses-tool-drift), now hosted-proven.** Four Perses tools are exposed by the MCP surface but absent from the release-gate contract list: `baseharbor.app.perses.disable`, `.enable`, `.remove`, `.status`. `missing=[]` proves the contract expects fewer tools than the binary offers, so this is contract drift, not a build break. Remedy candidates: register the four tools in the gate contract under Owner scope (`scripts/**`), or drop the tools from the MCP surface in a separate card. Coordinator decision: keep both routes open, ask the Owner, because the fix location is `scripts/**` (Owner scope, AGENTS 3.8).

## Consequence for PR #1746

The candidate itself is coherent (its own gate run is green). Card `0428-208` moves to `wait`: content dependency on card `0428-223` (operator-auth context) and on the MCP contract registration. No merge before both are cleared and the independent review plus the stated Coordinator/Release Owner approvals are recorded.
