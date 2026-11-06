# r27 secure-export round 2 CI receipt

Round 2 (w204, t-20261018-r27-secure-export). Closed the "standalone unused
adapter" gap: the adapter from round 1 is now callable from a public CLI
command, and the candidate passed the hosted CI gate.

## Candidate

- Commit: 179b91b105270f8a57d8f29ff61c67d752ec040d
- PR: #1396 (branch work/r27-secure-export)
- Head SHA on remote (ls-remote): 179b91b105270f8a57d8f29ff61c67d752ec040d
- develop (21d8d05cf1acf04729077e05eb350fcd3bb018ed) is an ancestor of the candidate.
- Preceding commits: 4668a593 (adapter), f382cc22 (develop merge), 652f57d5 (CLI wiring).

## Change-set (round 2)

- cmd/baha/secure_profile_export.go — new file, the public command
  `baha app secure-profile export [NAME] --password-file FILE [--output FILE]`.
  Resolves the target app, collects the opt-in local developer credentials for
  the target/environment (bounded explicit selection), encrypts via
  applicationbackup.BuildExport. Password read from an owner-only file (never
  argv), validated for perms/length. Read-only path only.
- cmd/baha/secure_profile_export_test.go — 6 command-layer cells: missing
  password-file, argv-password rejection, owner-only perms, min-length,
  production-path round-trip, wrong-password/tolerant-mutant RED probe.
- cmd/baha/commands.go — exactly one appended dispatch line
  (secureProfileExportCommand) after appCredsCommand; no other edit in that file.
- cmd/baha/machine_coverage.go — presentation-classification row for the new
  command (gofmt-aligned).
- docs/cli/command-index.md, docs/de/cli/command-index.md — two new rows each.
- docs/reference/cli-machine-coverage.md, docs/de/reference/cli-machine-coverage.md
  — regenerated / extended with the two new rows (EN machine-coverage is
  tool-generated; DE is maintained).

## Local verification (before re-push)

- gofmt -l cmd/baha/ clean.
- go vet ./internal/applicationbackup/ ./cmd/baha/ clean.
- go test ./internal/applicationbackup/ ./internal/devaccess/ ./internal/credential/ all ok.
- cmd/baha: TestHumanCommandIndexTracksExactCommandMetadata,
  TestMachineDocumentationTracksRegistryAndCommandTree,
  TestMachineCoverageCIRealTreeAndJSONClassification,
  TestSecureProfileExport* all pass.
- Full `go test ./...` run: all ok, no failures.
- `baha app --help` shows the registered `secure-profile` command.

## CI failure that drove round 2 (run 42139183143, failure)

Three root causes, all documentation/registry/format parity:

1. gofmt: classifyCommandCoverage treated the command group `baha app
   secure-profile` (which had Run set) as a leaf, so it fell through to the
   `gap` classification; and the presentation-classification edit to
   machine_coverage.go was not gofmt-aligned. Fixed by moving Run into the
   `export` child (group becomes a pure parent) and running gofmt -w.
2. Doc drift: docs/reference/cli-machine-coverage.md, docs/cli/command-index.md
   and docs/de/cli/command-index.md lacked the new rows. Regenerated the EN
   machine-coverage via BASEHARBOR_UPDATE_MACHINE_DOCS=1, added the EN/DE
   command-index rows, and added the DE machine-coverage rows so the EN->DE
   literal-integrity audit keeps the inline-code literals.
3. documentation-audit: check_de_translation_integrity.py reported 2 "literal
   lost" findings (baha app secure-profile / export present in EN reference,
   missing in the German reference). Resolved by the DE rows above.

## CI success receipt (run 42146087866, success)

Run: 42146087866, event pull_request, conclusion success.

Executed jobs (all success):
- Focused Python: success
- Trusted Plan: success
- Workflow policy: success
- PR Selected Checks: success
- PR · Validation · cli-build: success
- PR · Validation · cli-gofmt: success
- PR · Validation · cli-guided-tests: success
- PR · Validation · cli-package-tests: success
- PR · Validation · cli-vet: success
- PR · Validation · documentation-audit: success
- PR · Validation · go-build: success
- PR · Validation · go-unit-tests: success
- PR · Validation · go-vet: success
- PR · Validation · mkdocs-de-strict: success
- PR · Validation · mkdocs-en-strict: success
- PR · Validation · pages-candidate-build: success
- PR · Validation · source-contracts: success
- PR · Validation · wizard-registration-tests: success

Skipped (gated on other lanes / not required this PR):
- Consumer Pins, Demo Pin, Exact Candidate, Public Contracts, Runner Interface,
  Selected Runtime, Release Source Preflight, Targeted HA docker/podman, validate.

## End state

- CI green on candidate 179b91b1.
- PR #1396 head == 179b91b1 == ls-remote HEAD; develop (21d8d05c) is an ancestor.
- Merge + merge approval and Planning close-out remain the Coordinator/Owner
  channel (Codex-MERGE / Owner-approval), not this worker.

## Basis refresh (KOORD-ZURUECK)

develop moved to f01d2fb (stage-versions merge). New head 0001ca02
(develop merge, no conflict, commands.go line intact); ls-remote verbatim;
f01d2fb ancestor rc=0. CI run 42147787627 = success on the new head.
