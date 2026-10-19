# Codeman hold during BaseHarbor CI stabilization — 2026-10-19

## Decision

Marcel explicitly paused Codeman: **PAUSED — BaseHarbor CI stabilization**. This later instruction supersedes the earlier general resumption only for Codeman and its workers. Completion of infrastructure repair does not automatically resume Codeman; a separate explicit Maintainer resumption is required.

The assigned CI/release infrastructure coordinator may repair integration/evidence infrastructure, independently qualify already reviewed source, and perform regular Maintainer merges only with real independent technical qualification and green required checks. No required-check bypass or fabricated approval is authorized. Native tests remain limited to authorized environments.

## Preserved ownership

- Do not start Codeman workers or take over paused product claims.
- Preserve worker o1's two unpublished, uncommitted core-921 binding files on its existing worktree/branch, based on f2bad5ef. Do not duplicate its CORE_921 implementation. Resume/integrate only after regular claim release or separately authorized owner continuation.
- The supplied ecosystem-local coordinator status and board reports were not available in the published GitHub trees or connected executor. This decision records the Maintainer instruction; it does not claim those local files were inspected or modified.
- Existing product source and claims remain intact; current CI coordination results belong to [the stabilization task](../tasks/t-20261019-ci-evidence-stabilization.md).

## Exit boundary

Keep Codeman paused after the stabilization handoff. Missing native recovery evidence and unpublished source ownership remain explicit blockers. Separate authorization, never inference from a green infrastructure PR, is needed to restart its workers.
