# CODEX-REVIEW — PR #1592 / 0428-088 host-witness recheck

Date: 2026-11-19  
Role: CODEX-REVIEW  
PR head: `76331c7d83055f821fa1e6ff21c1cc37d9a08ae9`  
Current develop: `da76c5cf9c963207038d5599bd130b89ecb1e8a4`  
Exact-head hosted PR run: [44467712113](https://github.com/mcpdev80/baseharbor/actions/runs/44467712113)  
Host evidence: [witness-1.md](../perses-runtime/witness-1.md), Planning commit `ebf15c9f236e48f202d5637a62876b5fa9117f38`

## Verification

- `git ls-remote` confirms the PR branch still points to `76331c7d83055f821fa1e6ff21c1cc37d9a08ae9`; `develop` points to `da76c5cf9c963207038d5599bd130b89ecb1e8a4`.
- PR #1592 is OPEN, head matches the reviewed SHA, and GitHub reports `BEHIND` / mergeable. The r4 dossier proves the Perses content blobs are unchanged across the base hops. Develop's `da76c5cf9` move is not contained in this head, so freshness is not satisfied.
- Run `44467712113` is terminal SUCCESS on the exact reviewed SHA. Required selected checks visible in the run passed (native gate plan, Go unit shards/packages, build, vet, focused Python, workflow policy, trusted plan, source format, selected checks). The runtime Docker job was SKIPPED; this is not treated as runtime evidence.
- The host witness runs `TestPersesRuntimeSmokeDockerIsolated` with `BASEHARBOR_PERSES_RUNTIME_SMOKE=1` on the exact candidate head, clean isolated worktrees, and rootless Docker. It records PASS at 19.32, 25.99, 14.50, 22.24, and 8.39 seconds, plus a second-worktree cross-check at 11.80 seconds. The develop comparison reports `no tests to run`; the test file is absent there. The evidence also records cleanup and no orphaned Perses artifacts.
- The unselected hosted trigger is recorded as owner-scope item 0428-114. Per the explicit 088-r3 precedent supplied for this acceptance, the exact-head host witness qualifies the runtime proof for this candidate. This does not change the owner-scope workflow finding.

## Verdict

**ACCEPT — candidate content and runtime behavior at `76331c7d8`.** The previously outstanding runtime-evidence finding is resolved by the exact-head host witness. No implementation correction is requested.

**MERGE DEFERRED — base freshness only.** The PR is behind current `develop` at `da76c5cf9`. After the authorized monotonic hop, require a fresh exact-head hosted PR run and recheck the unchanged-content proof before merge. No merge was performed in this review.

## CI cost note

Hosted run `44467712113` completed in 4m25s wall time. Selected checks executed and passed; runtime Docker was skipped. Host runtime witness elapsed time is 117.15 seconds across the five listed repetitions plus the independent 11.80-second cross-check and terminal 22.24/8.39-second repetitions as captured in the evidence (no hosted runner minutes charged for these host-local runs).

## END

END_ACCEPT_CONTENT / END_MERGE_DEFERRED: #1592 head `76331c7d83055f821fa1e6ff21c1cc37d9a08ae9`, run `44467712113` SUCCESS, exact-head host runtime witness accepted; merge awaits monotonic hop to `develop da76c5cf9` and fresh exact-head checks.
