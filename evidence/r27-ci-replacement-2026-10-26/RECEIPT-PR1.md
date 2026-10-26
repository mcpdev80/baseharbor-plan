# Minimal receipt PR 1 — 2026-10-26

Owner: Codex under Marcel's explicit minimal-receipt assignment.

Planning decision and five rewritten evidence stories: a2e426add43b61c9217a7736d39b217728c27586. No signature keys, attestation bundles, payload archive or retention/recovery subsystem.

Draft PR: https://github.com/mcpdev80/baseharbor/pull/1090
Source: ec82d476126291d372df2c13bd36273767574869
Branch: work/r27-minimal-receipt
Baseline: develop 433a5702c9735ffbf1e9fffe7a7ae513b1c5c396.

Exactly five added files: receipt_writer.py, receipt_verifier.py, test_receipt_chain.py and paired EN/DE minimal-ci-receipts.md. Production workflows unchanged. Six focused tests PASS (real temporary Git, fake live API), including wrong SHA, dead run, edited/edit-reverted receipt, strict schema, provenance and offline retained approval. Documentation audit PASS. Additional source review identified and resolved tested-integration binding and introduction-commit idempotency gaps; no remaining concrete blocker found within the protected-writer model. This is not hosted acceptance.

Live verification reads the existing bounded trusted-pr-plan only while GitHub is the witness; it retains no artifact. Pilot accepts fresh attempt 1 only. Retained mode requires a caller-pinned protected Planning revision and never uses GitHub.

Remaining: exact target-side legacy mapping/test discovery before merge; one real contributor pilot with automatic task linkage and authenticated Owner approval in PR 2; accepted final-check cutover in PR 3. No native matrix or automatic rerun requested. Initial legacy run: https://github.com/mcpdev80/baseharbor/actions/runs/40373999800 .

The automatic approval reviewer rejected publication of regenerated roadmap/release views because their complete files include extensive pre-existing Planning content. Those local handoff/metadata/view edits have not been published; explicit scoped user approval is required. The smaller five-story rewrite and this bounded handoff are separate from that rejected payload.
