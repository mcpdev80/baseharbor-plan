---
id: t-20261116-r28-guided-rootless-bootstrap
card_number: "0428-098"
card_short_title: "Guided rootless bootstrap"
type: task
areas: [runtime, cli, security]
release: v0.4.28
version: ""
parent: v0.4.28
owner: "ChatGPT"
kanban_status: active
kanban_lane: active
kanban_summary: A fresh Linux workstation can complete the supported baha up new local-Core journey without manually discovering how to install…
kanban_title: "0428-098 · Guided rootless bootstrap"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1664]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261116-r28-guided-rootless-bootstrap · Guided rootless runtime prerequisite repair #task #release/v0-4-28 #status/active #view/active #area/cli #area/runtime #area/security #kind/task
    <!-- generated:card -->
    **Owner:** ChatGPT · **Priority:** high  
    **PR:** [baseharbor#1664](https://github.com/mcpdev80/baseharbor/pull/1664)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** v0.4.28  
**Depends on:** none  
**Owner:** ChatGPT  
**Priority:** high  
**PRs:** [baseharbor#1664](https://github.com/mcpdev80/baseharbor/pull/1664)  
**Source:** 
<!-- /generated:links -->

## Goal

A fresh Linux workstation can complete the supported `baha up new` local-Core journey without manually discovering how to install Rootless Docker prerequisites. BaseHarbor diagnoses the actual selected Target/runtime endpoint, explains each proposed change, requests explicit user approval and verifies the repaired runtime before proceeding. No silent privilege escalation, host mutation or fallback to system Docker.

## Reproduction (2026-11-16)

- Host: Ubuntu Linux, Docker CLI available; default Docker context resolves to `unix:///var/run/docker.sock`; system Docker works.
- BaseHarbor selects `unix:///run/user/1000/docker.sock`, which does not exist; `systemctl --user is-active docker` reports `inactive`.
- `baha up new` installs ORAS v1.3.6 to `~/.local/bin` after an explicit `[y/N]` prompt, then stops at `Verify and prepare the BaseHarbor runtime image`: selected rootless Docker endpoint unavailable, no fallback.
- `dockerd-rootless-setuptool.sh check --force` reports missing `uidmap` (`newuidmap`, `newgidmap`). The setup tool without `--force` rejects the concurrently running rootful Docker.
- An optional apt installation yielded ORAS 1.3.0; this was not the failing prerequisite. ORAS's user-local install had already succeeded. Do not misdiagnose it as a sudo problem.

## Scope and responsibilities

- Trace the actual first-run CLI command path, selected Target configuration, Docker context/endpoint selection, runtime verification, ORAS installer and Linux platform adapter before implementation. Retain existing explicit-Target and policy semantics; avoid creating a second bootstrap stack or disguising an endpoint selection defect as a missing daemon.
- Preflight the actual chosen runtime: CLI/daemon, rootless identity, socket availability, Docker context/Target endpoint compatibility, `dockerd-rootless-setuptool.sh`, `uidmap`, user namespace/subuid/subgid prerequisites, and required user service availability. Diagnose unsupported platforms/distros explicitly.
- For every proposed installation or system/user-service change, explain reason, exact change, privileges, consequences, and which existing Docker installation remains untouched; request affirmative consent (default No) before applying changes. Distinguish user-only operations from elevated package/configuration operations. Never invoke sudo or privilege escalation on a No response or implicitly in noninteractive mode.
- On approved supported Linux platforms, install only missing prerequisites via a vetted distro-specific mechanism, configure/enable/start Rootless Docker in the user scope as needed, then verify socket, rootless security mode and actual target provider communication. Do not overwrite Docker contexts, remove rootful Docker, modify unrelated services or fall back silently.
- Handle partial failure and cancellation with actionable instructions, state-aware retry and no misleading success. Record no credentials or sensitive host information in logs. Already-valid setup must be idempotent and prompt-free.
- Audit ORAS: reuse a compatible executable from PATH or the managed user install; validate required version before download, verify the installed binary, keep a user-local install unprivileged, and request separately explained approval before any privileged alternative. Do not install an older apt candidate or demand sudo if the supported user-local install is functional.
- Preserve Docker and rootless Podman selection and configured remote Targets: never force a Rootless Docker setup when another supported provider/endpoint was explicitly selected.

## Acceptance

- First-run `baha up new` on an intentionally unconfigured supported Linux host detects missing prerequisites, offers one understandable informed repair plan, and only performs approved operations; successful repair completes runtime preflight and resumes Core setup without a manual shell workaround.
- User denial/cancellation makes zero host changes, fails safely with a clear next step, and never invokes privileged commands; partial approval does not authorize unlisted follow-on changes.
- Noninteractive invocation produces machine-readable actionable missing-prerequisite diagnostics and no implicit install, sudo prompt or hang; explicit automation consent, if implemented, must be separate and narrowly scoped.
- Rootful Docker alone must not count as a working Rootless Docker endpoint, nor be silently selected as a fallback. Preserve already working rootful/remote Target behavior according to explicit selection policy.
- Rootless Docker already correctly configured, and ORAS already present at a compatible version, execute without unnecessary installations/prompts. Running rootful and rootless daemons simultaneously is supported without interference.
- For unsupported OS/distro, missing sudo privileges, failed package installation or broken user services: no hidden fallback, no unbounded retry, and precise remediation.
- Human-facing explanations and diagnostics conform to the v0.4.28 English CLI UX and translated docs policy; redact secrets and avoid leaking host-specific paths into generic error contracts.

## Required checks and CI mapping

- Update relevant existing runtime/CLI/ORAS tests and add dedicated unit and regression tests for consent Yes/No, denial/no side effects, user vs elevated operations, preflight/repair state transitions, incorrect context, missing socket, missing uidmap, unsupported platform, rootful coexistence, idempotence, ORAS PATH/user-local version precedence and failure/retry.
- Add isolated Linux integration coverage with simulated package/service commands and a native end-to-end first-run smoke on Docker rootless; verify provider-selection nonregression with rootless Podman and explicitly selected remote/other existing Targets. Unit fakes are not substitutes for required native evidence.
- Register every new test in the actual test-to-check/CI gate mapping; audit `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, appropriate packages and workflows/triggers. Prove relevant changes select the checks and unrelated changes do not expand the suite unnecessarily. A skipped/missing test is not a pass.
- Acceptance requires exact commit SHA, test IDs, selected CI checks, triggering PR paths/events, actual passing run URLs/results for both relevant provider paths, and documentation changes. Coordinate shared `.github/**` and central CLI files with owning lanes; do not bypass CI or silently merge.

## Dependencies and file ownership

- Coordinate with v0.4.28 CLI platform/access wizard work (`t-20261114-r28-cli2-wizard-platform`) and the CLI integration/contract owner to avoid duplicate wizard logic or competing shared-file edits. Verify existing Docker endpoint behavior delivered by v0.4.27 `t-20261101-docker-engine-1245` before changing runtime selection.
- Candidate source areas to inspect: `cmd/baha` local Core setup / CLI preflight, `internal/runtime` Docker endpoint selection and provider detection, existing ORAS installer, platform-specific bootstrap and native runtime tests. Exact file ownership must be resolved against current `develop` prior to implementation.

## Handoff

Implementation candidate: [baseharbor#1664](https://github.com/mcpdev80/baseharbor/pull/1664) (draft, feature branch `feat/0428-098-guided-rootless-pr`). Replaces prematurely opened and closed PR #1662. Implementation includes guided repair, consent/fail-closed regression tests, EN/DE documentation and existing-gate source mappings. Await exact-head CI and real first-run Linux evidence before acceptance; no merge/release claimed.
