# Fix 1 — MCP/HTTP edit path fails loud on partial provider-change

- Card: t-20261118-mcp-partial-change-success (0428-120)
- Owner: worker-ornith1.5
- Branch: lane-0428-120-mcp-status, base HEAD `8dccd4fe1a52bbcc61c67f7809079f33b8040d64` (develop)
- Base is ancestor: `git merge-base --is-ancestor 8dccd4fe1 ... HEAD` => YES

## PLAN

- Card read, owner verified via plan.py (state: active)
- Reality-attest develop: `git ls-remote origin develop` => 8dccd4fe1 (matches mission + task source)
- Branch lane-0428-120-mcp-status cut from exact base 8dccd4fe1; base is ancestor of HEAD
- Red evidence written first (this akte documents repro before the fix)
- Fix applied in app_registration_921.go apply-handler only (MCP/HTTP scope); no cmd/baha internals (118), no outcomeMatchesImpact (116)
- Regression test wired into existing cmd/baha MCP/HTTP test group (CI coverage)
- build/vet + affected unit tests on exact head
- PR base develop (lane-0428-120-mcp-status)

## Red: the silent-success repro (before fix)

- Root: `appMachineChangeDesired` (cmd/baha/app_machine_adapters.go:521-531) calls
  `RecordProviderChangeResult(fresh.Plan, outcomes)`. That function
  (internal/application/provider_change_result.go:13) defaults `result.Status = "partial"`.
- `RecordProviderChangeResult` sets status `"complete"` only on
  plan.Complete && applied == len(impacts) (line 65) and `"failed"` only when
  every impact failed (line 67-69). An impact that is simply MISSING from
  `outcomes` (unattestable, stays `"pending"`) leaves applied < len and failed == 0,
  so status stays `"partial"` and `resultErr` is nil.
- CLI edit path (cmd/baha/app_edit_apply.go:372) mirrors the contract:
  `if changeErr == nil && result.Status != "complete"` => `&appMachineError{Code: "partial"}`.
  Fail-closed.
- MCP/HTTP edit path (cmd/baha/app_registration_921.go:187-201) does NOT mirror it:
  ```
  result, err := appMachineChangeDesired(...)
  if err != nil { ... return machineMCPFailure(...) }
  return nil, result, nil   // <-- no result.Status check; partial surfaces as success
  ```
  A partial (e.g. one unattestable pending impact, no failed impact) returns
  `nil` error, MCP `IsError:false` => the command exits 0 despite an unattested
  impact. That is the silent-success surface hunt 917 befund-1 (MEDIUM).
- Repro (unit-only, no container): `appMachineChangeDesired` with a `Complete: true`
  plan of two impacts but an `apply` returning only one `applied` outcome (second
  impact missing => pending). `RecordProviderChangeResult` returns
  `(status=partial, nil)`. Before fix: `app_registration_921.go:201` returns
  `nil, result, nil` => IsError:false. After fix: same inputs must surface a
  structured `verification_failed` (same public code the CLI `partial` ->
  `classifyAppMachineError` maps to), with the result as details.
- Scope guard: fix touches ONLY the apply-handler return in app_registration_921.go.
  No change to cmd/baha machine-edit internals (0428-118 territory) and no change
  to outcomeMatchesImpact (0428-116 home, pin holds). No shared helper needed.

## CLEANLINESS

- No container/compose project started (R1, unit-only).
- No .github/** touched, no workflow_dispatch / rerun.
- Worktree /tmp/opencode/120-mcp-status-wt only; git untouched elsewhere.
- Base move handled: develop moved 8dccd4fe1 -> 9a37b4bc6 (PR #1663/demo#164 merged);
  branch rebased (no force of shared history) onto new base, affected checks rerun.
- cleanliness: OK — no test-eigen artefacts.

## Green: exact-head run on new base

- Rebased branch onto 9a37b4bc6 (new develop HEAD); log shows ONLY my commit
  23837dcc on top of base 9a37b4bc6; base is ancestor of HEAD.
- go build/vet + TestCore921 green on new base (local).
- CI run 44426400958 (pull_request, head 23837dcc5) COMPLETED success:
  Source format, Native gate plan, Workflow policy, PR Trusted Plan,
  Focused Python, go-vet, Go unit (cli-0/1/2/3, owner, packages), go-build,
  cli-gofmt all success; targeted docker/podman/HA/release gates skipped (no
  affected path). Run-ID 44426400958, status completed, conclusion success.
- PR #1688, base develop, head 23837dcc, mergeable, 1 commit / 2 files.

## END

END_DONE mission-120-mcp-status.md: fix-1 red->green, PR #1688 base develop, CI run 44426400958 completed success, evidence on origin/main; candidate SHA 23837dcc5 (base 9a37b4bc6 after develop move)
