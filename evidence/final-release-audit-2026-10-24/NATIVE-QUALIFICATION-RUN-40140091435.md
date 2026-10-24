# v0.4.26 current native qualification

Public source and CI checkpoint, 2026-10-25 (Europe/Berlin).

- Owner-authorized Connector [PR #14](https://github.com/mcpdev80/baseharbor-node-connector/pull/14) merged as `5658d19aa2e5b70c84e38ded30196e07c651bc2e`; exact tree `72110bffc38551c4da75a3295b5142bacad79edc` matches reviewed source `2ecea22c259bdb42c70d9e3e510faeb367fd17c9`.
- Source CI [40139359070](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40139359070) passed before merge. Existing trigger marker was preserved; one expected-head non-force fast-forward started native qualification.
- Actual Console pin: `0941e184226c035d3d309ab1074eeaf99153b2a3` ([PR #13](https://github.com/mcpdev80/baseharbor-console/pull/13)); Core `3e27497b4ef7b567858ba646bc3071bee37d19bd` and Demo `09595781b68e1f41caaba9aec1402eb8009d700f` remain fixed.
- Genuine native [run 40140091435](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40140091435), push attempt 1: Podman job `121009844377` completed SUCCESS; Docker job `121009844363` completed FAILURE. Both final owned cleanups passed; joint acceptance is NOT QUALIFIED.
- Current manifests pass the unchanged Core resolver and DAG validation. Canonical generated pins SHA256: `8421e3c8e6d33ad3e442537f95e75891531a4da03a37b78f1c018cfb2af4f0a2`.
- Previous run `40137607614` remains failed historical evidence. Selected 63, complete 65, promotion and tag remain pending; release eligibility is false. Existing task states remain ACTIVE/WAITING.

This receipt records actual integration and scheduling, not independent source review or release approval.

## Terminal diagnosis and bounded follow-up

The corrected ordinary-retirement consent UI and application destroy succeed on both runtimes. Docker then fails inside the generated Next.js CLI journey; its finally cleanup throws `ownership_ambiguous` / `runtime_retirement_unverified` for a shared SQL reference. This final cleanup can replace an earlier exception, so the first failing operation is not established by the existing receipt. The source-bound Podman manifest artifact is `12578388334`, digest `sha256:d2856bf7820c5b656e83a39dbfcb4d424339a5aa1c24ed9c2e8373ad4ce01c5a`; Docker diagnostic artifact is `12578887752`, digest `sha256:d6aafb5487275e636603a9e8fb7517a14c7a88c3bf991520c1ab8ed07ebf2f4c`.

Owner release-completion scope continues with a bounded Console fixture diagnostic correction: preserve the original generated-application failure, retain attempted cleanup and report both through the existing public-error allowlist. No Core guard change, timeout increase, skipped assertion or native acceptance waiver is authorized by this diagnosis. New source and native outcomes must remain explicit. Selected63/full65, promotion and tagging remain pending.

## Diagnostic source integration

Console [PR14](https://github.com/mcpdev80/baseharbor-console/pull/14) is integrated as `b3426c59f69e4098184fe15a45a6a907d8abebd0`, exact tree `f3aff9dcec06f655f83b9d5a5ac66978c11b8580`, matching the locally verified three-file correction. Source CI `40141591495` / job `121014291888` passed; all69 contracts, TypeScript, lint and architecture checks pass. Owner-authorized acceptance is recorded; no independent review is claimed for this new correction.

Connector [PR15](https://github.com/mcpdev80/baseharbor-node-connector/pull/15), source `2615ad6d14a1c57d2b743afc0d12966a29a88e48`, changes only the actual Console pin. Its source CI `40141723194` is running. A fresh matching-source native diagnosis remains necessary. This source correction does not claim to fix the unobserved primary Docker failure.
