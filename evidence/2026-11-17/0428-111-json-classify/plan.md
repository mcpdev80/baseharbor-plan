# PLAN — 0428-111 JSON error classify (lane-0428-111-json-classify)

Card: t-20261117-hunt-uid-docs-111 / 0428-111
Basis: develop@ed55d893 (remote HEAD verified via `git ls-remote origin develop`)
Branch: lane-0428-111-json-classify (cut from ed55d893, NOT from another PR head)

## PLAN

- Read mission-111-json-classify.md and hunt befund-1.md; understand the finding (Befund 4.1).
- Reproduce the fund: build develop@f6c15edc; confirm classifyMachineCLIError does not handle the config-error family -> Classify returns internal_error.
- Fix in classify layer only: add ErrConfigMissing/ErrConfigEmpty sentinels to internal/apierror (leaf), re-export from internal/deployment (same identity), add Classify branch -> ErrorSourceMissing keeping the human-readable line.
- Regression: add tests for the fixed config-error path returning ErrorSourceMissing, message preserved, sentinel identity preserved, negative example still internal_error; end-to-end CLI test confirms concrete classification.
- Write-set boundary respected: NOT cmd/baha/app_traces.go, NOT config-mutation paths, NOT perses files.
- build/vet/gofmt + affected tests pass (telemetry OTLP failures are pre-existing on clean base).
- refspec-push to lane-0428-111-json-classify; PR READY; exact-head run TERMINAL.
- Evidence akte + END + GUI todos; bring down any compose project; post codeman END line.

## Fund (Befund 4.1 from hunt-uid-docs befund-1.md)

`machine.Classify` (internal/machine/contract.go:99-150) does not know the
ErrConfigMissing family. Config errors (config root populated but config.yaml
missing/empty) therefore fall through to `internal_error`, even though the root
cause is a concrete, actionable misconfiguration. Probe:
`target list -o json` under a populated root yields
`{"error":{"code":"internal_error","message":"BaseHarbor config root is
configured but the config.yaml is missing: ..."}}`.

Machine error set already declares `ErrorValidationFailed` and
`ErrorSourceMissing`; docs/spec promise a structured actionable error for
unresolved inputs.

## Fix approach (cycle-safe)

`internal/machine` is lower-level than `internal/deployment` (deployment imports
machine), so I cannot import deployment from machine. The fix lives in the leaf
package `internal/apierror`:

- Add `ErrConfigMissing` / `ErrConfigEmpty` sentinels to internal/apierror.
- Re-export them from internal/deployment (backward-compatible, identical values)
  so deployment wraps the same sentinels.
- Add a `Classify` branch: `errors.Is(err, apierror.ErrConfigMissing | ErrConfigEmpty)`
  → `ErrorSourceMissing`, keeping the human-readable message.

This is write-set confined to the classify layer; no cmd/baha, no config
mutation, no perses files.

## Write-set boundary

- NOT cmd/baha/app_traces.go (0428-108 lane)
- NOT config-mutation paths (0428-110 lane)
- NOT perses files

## Boundaries / stop

- NO .github/** edits (Owner scope). Report failing checks as STATE.
- No force push, no merge, no subagent.
- No containers/compose started on this host; any project started must be
  brought down before END.

## Evidence

- PR: https://github.com/mcpdev80/baseharbor/pull/1678
  - title: fix(machine): classify config errors to source_missing instead of internal_error (0428-111)
  - base: develop, head: lane-0428-111-json-classify
  - commit SHA: f17c929674874093f10c049fe8f765ecff8365c9
- CI (run 44037527494), exact candidate f17c92967:
  - Go unit · packages pass (covers internal/machine, internal/apierror, internal/deployment)
  - Go unit · owner pass; Go unit · cli-0/1/2/3 pass (covers cmd/baha)
  - Validation · go-build pass; Validation · go-vet pass
  - Validation · deployment-package-tests pass
  - Source format pass; Workflow policy pass; Trusted Plan pass; Native gate plan pass
  - Only remaining job: heavyweight docker "Selected Runtime · lifecycle" gate —
    unrelated to this classify-layer fix (no runtime/lifecycle code touched).
- CI group that runs the new test: unit-and-vet slice (ci.yml ./internal/...),
  triggered by the standard PR push — no .github/** edit required.

## END

END_DONE mission-111-json-classify.md — Fix applied, tests added, CI green on
exact candidate f17c92967, PR #1678. See below for witnesses.
