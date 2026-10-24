# v0.4.26 current native qualification

Public source and CI checkpoint, 2026-10-25 (Europe/Berlin).

- Owner-authorized Connector [PR #14](https://github.com/mcpdev80/baseharbor-node-connector/pull/14) merged as `5658d19aa2e5b70c84e38ded30196e07c651bc2e`; exact tree `72110bffc38551c4da75a3295b5142bacad79edc` matches reviewed source `2ecea22c259bdb42c70d9e3e510faeb367fd17c9`.
- Source CI [40139359070](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40139359070) passed before merge. Existing trigger marker was preserved; one expected-head non-force fast-forward started native qualification.
- Actual Console pin: `0941e184226c035d3d309ab1074eeaf99153b2a3` ([PR #13](https://github.com/mcpdev80/baseharbor-console/pull/13)); Core `3e27497b4ef7b567858ba646bc3071bee37d19bd` and Demo `09595781b68e1f41caaba9aec1402eb8009d700f` remain fixed.
- Genuine native [run 40140091435](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40140091435), push attempt 1: Docker job `121009844363` and Podman job `121009844377` are running; acceptance is PENDING.
- Current manifests pass the unchanged Core resolver and DAG validation. Canonical generated pins SHA256: `8421e3c8e6d33ad3e442537f95e75891531a4da03a37b78f1c018cfb2af4f0a2`.
- Previous run `40137607614` remains failed historical evidence. Selected 63, complete 65, promotion and tag remain pending; release eligibility is false. Existing task states remain ACTIVE/WAITING.

This receipt records actual integration and scheduling, not independent source review or release approval.
