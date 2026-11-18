# CODEX-REVIEW — PR #1592 / 0428-088

Review date: 2026-11-18
Candidate before base refresh: `7ca9fc1c5fb8a8ed3b48559ead50192d4189125e`
Current develop: `907f16713cbf38693d30c9dadaad7fe299759219`
Local base-refreshed candidate: `aaeeae801dc4b50b338aeefc9718fc5861d137a8` (not pushed; exact-head CI not run)

## Evidence

- PR #1592 is OPEN, ready, based on `develop`; before refresh GitHub reported `BEHIND`.
- `git ls-remote origin` witnessed develop `907f16713cbf38693d30c9dadaad7fe299759219`, lane and PR head `7ca9fc1c5fb8a8ed3b48559ead50192d4189125e`.
- A normal merge of current develop was made in the existing isolated worktree. The prior and refreshed task patch IDs match (`b36f7c94c7097baa71e735d89054cc73a4ed5a19`); `git diff --check origin/develop...HEAD` is clean.
- No refreshed candidate was pushed, so there is no exact-head CI witness for `aaeeae8`.

## Finding

**BLOCKING — Perses TLS mounts have no corresponding projected files.** `writePersesUIComposeService` mounts `./providers/management-ui/perses/server.cert` and `server.key` read-only. `EnsurePersesManagementUI` creates the directory and a `persistence` marker only; unlike the neighboring management UI setup, it never calls `serviceaccess.EnsureTLSMaterial` or projects certificate/key files. The compose definition therefore refers to missing host paths, despite the comments claiming TLS projection. The existing runtime smoke evidence says container startup passed, but it does not reconcile the source-level missing-file path; the exact-head gate after the base refresh is also still absent.

## Recipe / disposition

Worker correction: in `internal/application/perses_runtime.go`, either generate and project the certificate/key using the approved `serviceaccess` TLS flow and configure Perses to consume them, or remove the mounts and revise the security contract/configuration to match the actual supported transport. Add a regression that asserts the selected runtime contains both readable files and that the Perses process uses the intended TLS configuration; ensure this test executes in the relevant CI/native gate. Run the focused suite and isolated runtime smoke. Then normally push the corrected lane, observe the new exact-head CI to terminal, and request a fresh review. Stop criterion: either certificate/key material is proven present and consumed, or the approved contract explicitly supports the resulting transport with evidence.

**CODEX-REVIEW: REQUEST CHANGES** at the refreshed local candidate. No merge. Mission stop rule applies to following objects until this finding is resolved and the exact candidate is re-reviewed.
