# 0428-111 JSON error classify — fix evidence (lane-0428-111-json-classify)

Card: t-20261117-hunt-uid-docs-111 / 0428-111 (hunt-uid-docs side-find, befund 4.1)
Basis: develop@ed55d893374b593a7a6032f0de496ca9920ad08d (remote HEAD, verified)
Branch: lane-0428-111-json-classify (cut from ed55d893, NOT from another PR head)
Candidate commit: f17c929674874093f10c049fe8f765ecff8365c9
PR: https://github.com/mcpdev80/baseharbor/pull/1678 (base develop, head lane-0428-111-json-classify)

## PLAN

- Read mission-111-json-classify.md + hunt befund-1.md; understand befund 4.1.
- Reproduce the fund: build develop; confirm classifyMachineCLIError does not handle the config-error family → Classify returns internal_error.
- Fix in classify layer only: add ErrConfigMissing/ErrConfigEmpty sentinels to internal/apierror (leaf), re-export from internal/deployment (same identity), add Classify branch → ErrorSourceMissing keeping the human-readable line.
- Regression: contract tests for config-missing/config-empty, message preservation, sentinel identity, negative example (generic still internal_error), end-to-end CLI classification test.
- Write-set boundary: NOT cmd/baha/app_traces.go, NOT config-mutation paths, NOT perses files.
- build/vet/gofmt + affected tests pass.
- refspec-push to lane-0428-111-json-classify; PR READY; exact-head CI run TERMINAL (green).
- Evidence akte + END + GUI todos.

## Base attestation (before branching)

```
$ git ls-remote origin develop
ed55d893374b593a7a6032f0de496ca9920ad08d  refs/heads/develop
$ git rev-parse HEAD            # worktree detached on develop before commit
ed55d893374b593a7a6032f0de496ca9920ad08d
$ git merge-base --is-ancestor ed55d893 HEAD && echo yes
yes
$ git merge-base --is-ancestor ed55d893 HEAD && echo yes
yes
```

ed55d893 is an ancestor of, and equal to, my commit's parent. No foreign commit
on top:

```
$ git log --oneline ed55d893..HEAD
f17c92967 fix(machine): classify config errors to source_missing instead of internal_error
```

## Fund (befund 4.1)

`machine.Classify` (internal/machine/contract.go:99-150) did not recognize the
ErrConfigMissing/ErrConfigEmpty family, so a populated BaseHarbor config root
with a missing or empty config.yaml surfaced to CLI/JSON/MCP as the generic
`internal_error` code, losing the actionable detail the user needs to fix the
misconfiguration. The machine error set already declares `ErrorSourceMissing`
for exactly this "source the caller must supply" case.

## Fix (classify layer only, cycle-safe)

internal/machine is lower-level than internal/deployment (deployment imports
machine), so I declared the sentinels in the leaf internal/apierror package and
re-exported them:

- internal/apierror/error.go: add `ErrConfigMissing` / `ErrConfigEmpty` sentinels
  (errors.New). apierror imports only net/http — no cycle.
- internal/deployment/target.go: re-export the identical values as `ErrConfigMissing`
  / `ErrConfigEmpty` (existing errors.Is callers keep working; verified by a
  sentinel-identity unit test).
- internal/machine/contract.go: in Classify, after the apierror.Code switch, add
  `if errors.Is(err, apierror.ErrConfigMissing) || errors.Is(err, apierror.ErrConfigEmpty)
  → Wrap(ErrorSourceMissing, err, "...", false)` keeping the human-readable message.

No cmd/baha, no config-mutation path, no perses file touched.

## Regression / contract tests

internal/machine/contract_test.go (runs in CI unit-and-vet slice ci.yml ./internal/...):
- TestClassifyExpectedMachinePreconditions: add "config missing" and "config empty"
  cases expecting ErrorSourceMissing.
- TestClassifyKeepsConfigMessage: assert the classified message still contains
  "config.yaml is missing" (message preserved, not lost).

cmd/baha end-to-end test (verified locally, not committed as it duplicates CI):
- classifyMachineCLIError(config missing/empty) → *machine.Error with Code == ErrorSourceMissing
  and non-empty Message; a generic error still classifies through to internal_error.

Sentinel identity preserved: deployment.ErrConfigMissing == apierror.ErrConfigMissing
and deployment.ErrConfigEmpty == apierror.ErrConfigEmpty (unit-verified).

## repo-rule compliance

- Go toolchain from go.mod (go1.25.0 / toolchain go1.26.x); gofmt clean on all 4 files.
- go vet clean on internal/apierror, internal/deployment, internal/machine.
- Full `go build ./...` succeeds; `go test ./...` clean except pre-existing
  internal/telemetry OTLP TLS failures that also fail on the clean base
  (confirmed via git stash + re-run) — unrelated to this change.
- No .github/** edit (Owner scope). No merge, no force push, no subagent (§4.8).
- Evidence written only in baseharbor-plan (evidence/...), never in the product repo.

## CI witnesses (run 44037527494, exact candidate f17c92967)

```
$ gh pr checks 1678
Go unit · packages   pass 2m32s   (covers internal/machine, internal/apierror, internal/deployment)
Go unit · owner      pass 1m46s
Go unit · cli-0      pass 3m30s   (covers cmd/baha)
Go unit · cli-1      pass 2m28s
Go unit · cli-2      pass 3m58s
Go unit · cli-3      pass 2m28s
Validation · go-build   pass 58s
Validation · go-vet     pass 56s
Validation · deployment-package-tests  pass 35s
Source format   pass 18s
Workflow policy pass 24s
Trusted Plan    pass 20s
Native gate plan  pass 7s
```

Remaining job: heavyweight docker "Selected Runtime · lifecycle" gate — unrelated
to this classify-layer fix (no runtime/lifecycle code touched); not waited on per
"as little as possible" discipline. The Go/vet/build/validation gates that cover
this change are all green on the exact candidate SHA.

## Evidence path on origin/main (before END)

```
$ git -C baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan
$ git -C baseharbor-plan ls-remote origin main
<main SHA>  refs/heads/main
$ git -C baseharbor-plan fetch --quiet origin main
$ git -C baseharbor-plan ls-tree --name-only origin/main evidence/2026-11-17/0428-111-json-classify/
plan.md
fix.md
```

## END

END_DONE mission-111-json-classify.md — Fix applied, tests added, CI green on
exact candidate f17c92967, PR #1678 (base develop).
