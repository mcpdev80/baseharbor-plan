# Welle2c object 2 — review record / CODEX-REVIEW

Date: 2026-11-17
Task: `welle2c`, object 2; PR #1604. The mission labels this as 0428-079 messaging, but the live PR title/body and Planning source identify it as 0428-081 Perses Valkey dashboard (`t-20261114-r28-perses-dashboard-valkey`, owner `w081`). The separate 0428-079 messaging card still points to PR #1603. Per the owner's explicit continuation for PR #1604, this review uses the live 0428-081 task contract; no card mapping was changed here.

## Reviewed candidate and identity

- PR #1604 head after mechanical develop hopf: `beb4402892c40b8d630cc051173de62c37054a3b` (`wt-0428-081`).
- Exact base develop: `0ec4706b12c8fa869a2c23db18b6cab4f91f2178`.
- Hopf commit: `beb4402892c40b8d630cc051173de62c37054a3b`, parents `7c085668cdb1c13cae4bff76eda02a3c4c0de97a` and `0ec4706b12c8fa869a2c23db18b6cab4f91f2178`.
- `mergeable=true`, `mergeable_state=clean`, PR open and ready; zero conversation comments, zero inline comments, zero submitted reviews, zero unresolved review threads.
- Identity check: SHA-256 of `git diff --binary 4094448543359a13ba312119304f1f70d3bc40a9...7c085668cdb1c13cae4bff76eda02a3c4c0de97a` equals SHA-256 of `git diff --binary 0ec4706b12c8fa869a2c23db18b6cab4f91f2178...beb4402892c40b8d630cc051173de62c37054a3b`: `d8ea7c0f5745f6f58936b14277482fde038c5b2eb80ccc3a7db714862a39191d`.
- The reviewed content delta is four files: Valkey selection whitespace, the explicit unavailable Valkey artifact/API, focused tests, and its golden reason file. Product content is unchanged by the develop hopf and was approved per the mission's batch15 record.

## Contract and evidence

- The actual 0428-081 contract requires dashboards only when supported signals are validated, explicit unavailable coverage when no native signal exists, no fabricated Valkey metrics/exporter, and focused CI tests.
- The candidate records Valkey `RequiresAdapter`, exports an explicit unavailable status with a reason, ships no dashboard panels while no native signal exists, and tests the unavailable catalog, reason serialization, deterministic output, availability status and golden file.
- Run [44049695785](https://github.com/mcpdev80/baseharbor/actions/runs/44049695785) completed `success` on the exact head `beb4402892c40b8d630cc051173de62c37054a3b` at 2026-11-17T08:51:51Z. `PR Selected Checks` completed SUCCESS from GitHub Actions integration 15368. Workflow policy, native gate plan, source format, trusted plan, focused Python, go-build, go-vet and all selected Go unit shards succeeded. Runtime/release gates were skipped by the trusted impact plan; no runtime service or native integration is required for the unavailable-only artifact. Approximate run cost: 1,155 completed non-skipped job-seconds = 20 runner-minutes.
- Live develop rulesets: required-check ruleset 25223521 is active and requires `PR Selected Checks` from integration 15368 with strict up-to-date checks. Develop integration ruleset 23754541 is disabled. No protection or CI bypass was used.
- No GitHub APPROVE was submitted because the PR author is `mcpdev80` and GitHub blocks self-review. This is the separate Codex review record under the already-authorized formal-review bypass; required checks remain enforced.

## Verdict

APPROVE — the actual 0428-081 contract is satisfied by the exact candidate and required `PR Selected Checks` is green. Eligible for squash merge only while PR head remains `beb4402892c40b8d630cc051173de62c37054a3b` and develop remains `0ec4706b12c8fa869a2c23db18b6cab4f91f2178`.

END welle2c object 2 review: APPROVE; squash merge remains pending.
