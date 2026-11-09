---
id: t-20261107-oci-pull-error-propagation
card_number: "0427-119"
card_short_title: "OCI pull error propagation"
type: task
areas: [deployment, registry]
release: v0.4.27
version: ""
parent: ""
owner: mcpdev80
kanban_status: closed
kanban_lane: closed
kanban_summary: "oras pull reports failures with the same classification as oras resolve: a genuinely missing oras binary is still unambiguously…"
kanban_title: "0427-119 · OCI pull error propagation"
priority: normal
depends_on: [t-20261017-release-0-4-27-updates, t-20261107-r27-runtime-broker-oras-missing-edge-readiness]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1434]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1434", "https://github.com/mcpdev80/baseharbor/actions/runs/42396424816"]
wait_reason: ""

---

- [x] t-20261107-oci-pull-error-propagation · OCI: pull uses same error classification as resolve #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/deployment #area/registry #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 · **Priority:** normal  
    **PR:** [baseharbor#1434](https://github.com/mcpdev80/baseharbor/pull/1434)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1434), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42396424816)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261107-r27-runtime-broker-oras-missing-edge-readiness](t-20261107-r27-runtime-broker-oras-missing-edge-readiness.md)  
**Owner:** mcpdev80  
**Priority:** normal  
**PRs:** [baseharbor#1434](https://github.com/mcpdev80/baseharbor/pull/1434)  
**Source:** 
<!-- /generated:links -->

## Goal

`oras pull` reports failures with the same classification as `oras resolve`: a genuinely missing oras binary is still unambiguously recognised, other pull errors are not mislabelled as a missing binary, and no sensitive command output leaks. Closes the residual finding accepted on broker card #0427-118 where the pull path wrapped errors with `%v`, losing the `exec.ErrNotFound` identity.

## Scope

- In scope: the OCI pull path in `cmd/baha/application_registry_source.go` (`pullResolvedRuntimeImage`, ~:417) reusing the classifier in `internal/orgconfig/source_oci.go` (`classifyNativeToolFailure`, ~:158) so it matches `Resolve` (~:138); the error-wrapping that currently uses `%v` and drops the sentinel identity; one targeted regression test.
- Out of scope: any new CI pipeline or workflow trigger; any change to the security contract or secret handling; the broker readiness and management-host-lock behaviour (already accepted on #0427-118); oras resolve behaviour itself (only the pull path aligns to it).

## Acceptance

- `oras pull` uses the same error classification as `oras resolve` (shared classifier, not a divergent inline check).
- A missing oras binary remains unambiguously identifiable (the `exec.ErrNotFound` sentinel is preserved through the error chain, asserted with `errors.Is`).
- Other pull failures (registry/auth/network/non-zero exit) are NOT classified as a missing binary.
- Sensitive error message content (command output, tokens, URLs) stays protected and is not surfaced in the returned error.
- One targeted regression test proves the distinction: missing-binary vs other-error, over the real pull path.

## Required checks

- New test (package `cmd/baha` or `internal/orgconfig`): e.g. `TestApplicationRegistrySourcePullErrorClassification` — assert `errors.Is(err, <missing-binary sentinel>)` for the missing-binary case and assert NOT that sentinel for an injected other-error, and that the message carries no sensitive output. Use a fake exec/result so no live runtime is required (the behaviour is error classification, not a Docker/Podman journey).
- Execution: covered by the existing Go unit suite that already runs `pullResolvedRuntimeImage`/classify tests (`go test ./cmd/baha` / `./internal/orgconfig` in the current cli/go-unit checks). No new gate or trigger is required; confirm the new test name is selected by that existing check for a relevant change and not for an unrelated one.
- Handoff records exact source SHA, the test → existing check → result, and confirms no security-contract diff.

## Dependencies and file ownership

- Owned files or areas: `cmd/baha/application_registry_source.go` (pull path), `internal/orgconfig/source_oci.go` (classifier), and the new test file.
- Shared files: none with in-flight cards; does not touch `.github/**`, `scripts/*` CI seam, or the `serve.go` management-host-lock area.

## Handoff

- **Accepted 2026-11-07 (ChatGPT review):** Core PR #1434 merged as `8a3f58da905fad52327d33466fde1d9568092519` (candidate head `4808a20e1308758a5b1df02ec602bb33a6250f3e`). CI run [42396424816](https://github.com/mcpdev80/baseharbor/actions/runs/42396424816) completed **success** at that exact candidate: `PR Selected Checks`, `go-unit-tests` (`go test ./cmd/baha`, complete `cmd/baha` suite), `go-build`, `go-vet`, `cli-gofmt`, `Source format` all PASS. Runtime jobs skipped by normal path selection and not required for this pure error-classification change. Reviewed diff covers shared OCI native-tool classifier, preserved `exec.ErrNotFound` identity, redaction of ordinary pull failures and `TestApplicationRegistrySourcePullErrorClassification` on the real `pullResolvedRuntimeImage` path. No `.github/**` or security-contract changes. Acceptance confined to OCI pull error classification; not a Docker/Podman end-to-end release qualification.

- 2026-11-07: PR #1434 implementiert, `wait` bis finale CI/Review des exakten Heads. Kein Merge/Closed behauptet. Bestehender Lane-Owner bleibt bestehen.

- 2026-11-07: ChatGPT hat 0427-119 nach Prüfung der veröffentlichten Datei-Reservierungen übernommen. Product-Branch `fix/0427-119-oci-pull-errors`, PR https://github.com/mcpdev80/baseharbor/pull/1434, Head `bbb388d2fc11b6d94925300f000056edf327b5f1`. Kein Overlap mit den zum Übernahmezeitpunkt offenen Core-PRs; unveröffentlichte Codeman-Dateien sind nicht einsehbar. Fix und Regressionstest committed, PR-CI/Review noch ausstehend; keine Abnahme/Closed.

- Follow-up to #0427-118 (accepted, PR #1425 merged). Planned, awaiting assignment; prerequisites accepted.

owner merged PR#1434 (develop 8a3f58da9): pull nutzt geteilte redacted native-tool classifier, missing-tool identity + stderr redaction belegt (test(oci) asserts). follow-up der akzeptierten broker-karte #0427-118 damit abgeschlossen.
