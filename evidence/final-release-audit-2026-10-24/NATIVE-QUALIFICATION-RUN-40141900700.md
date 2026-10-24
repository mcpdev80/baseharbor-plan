# v0.4.26 diagnostic successor native run

Console [PR14](https://github.com/mcpdev80/baseharbor-console/pull/14) and Connector [PR15](https://github.com/mcpdev80/baseharbor-node-connector/pull/15) are integrated after their actual successful source CI. Owner-authorized acceptance is recorded; this is not a new independent source review. Console tree `f3aff9dcec06f655f83b9d5a5ac66978c11b8580` and Connector tree `d7cd2304d979bbdc151ea924b5543bb37c75fd59` exactly match checked source trees.

Actual U is `b3426c59f69e4098184fe15a45a6a907d8abebd0`; actual K is `ff71e384e71d92f94dbf212ff394bce53ae9707e`. Core R and Demo D remain unchanged. Fresh actual manifests pass the unchanged resolver/DAG checks; canonical pins SHA256 is `220b62d5690c910e215d9127648f9131aa6115be3487b8cdfe9cf21adca64afd`.

One expected-head non-force trigger fast-forward started [40141900700](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/40141900700), attempt1: Docker job121015244697 and Podman job121015244679. Actual native result remains PENDING. The three-file fixture correction preserves the original generated-app exception, still attempts unchanged cleanup and reports both failures through the existing public redaction boundary; it does not claim to fix the previously masked Docker cause.

Previous run40140091435 remains Docker FAILURE / Podman SUCCESS, with both owned cleanups successful. Its original public graph and artifacts remain preserved. The Podman manifest ZIP digest and its exact source/run/attempt/job bindings were checked locally; that old-source success is not relabelled as a new U/K execution. Selected63/full65, promotion and tagging remain pending. No release approval is claimed.

## Terminal result and assigned Core diagnosis

Run40141900700 finished Docker FAILURE / Podman SUCCESS. Both final owned cleanups succeeded. The new allowlisted logs prove the primary generated Next.js app destroy itself returns ownership_ambiguous/runtime_retirement_unverified; the same error in cleanup was secondary. No source or native success is inferred from this failure.

The generated HTTP-only app requests no SQL. Independent source inspection identifies a concrete candidate mismatch to reproduce: the complete Target plan may select an already-unbound logical SQL module retained by the earlier retired application, while the final verifier additionally demands a new SQL binding release by the current HTTP-only app. All canonical ownership, measured-zero, no-remaining-reference and required physical Core checks must remain enforced. Owner release-completion scope assigns a bounded Core regression and correction on a separate branch; no Core change is accepted or merged yet. No broad native/full rerun until the deterministic regression establishes the issue and the successor source is qualified.
