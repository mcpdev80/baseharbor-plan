# CODEX-REVIEW — PR #1691 / 0428-121 OwnerApplication-anchor recheck

Date: 2026-11-19  
Role: CODEX-REVIEW  
PR head: `f28b97a53870bb3f5cb5c90618dea977df3f1c2b`  
Develop: `da76c5cf9c963207038d5599bd130b89ecb1e8a4`  
Exact-head run: [44495408370](https://github.com/mcpdev80/baseharbor/actions/runs/44495408370)  
Evidence: `env-filter-fix/fix-4.md` on Planning `origin/main` (`4c3eda3d` at review)

## Verified

- PR #1691 is OPEN, non-draft, CLEAN, and mergeable at the exact head above. `develop` is `da76c5cf9`; the candidate is monotonically based on it.
- Run `44495408370` is terminal SUCCESS on the exact head. Selected jobs passed, including `PR Selected Checks`, workflow policy, trusted plan, native gate plan, Source format, focused Python, go-build, go-vet, all six Go unit shards, and the selected Docker identity/observability runtime jobs. The remaining 19 checks were skipped by routing for unrelated runtime/HA/release paths.
- The implementation now anchors project resolution on `SignalSource.OwnerApplication`, derives the remaining environment, and fails closed for absent or repeated anchors and empty remainder. The caller API stays unchanged; no `ProviderPlacement.Environment` or `security.go` change is present.
- Published `fix-4.md` records the exact merge hop, runtime/target grammar, case table, and run. `fix-3.md` is also now present on `origin/main`.

## Blocking finding

The specific cases required in the owner handoff are only exercised at the helper level. `TestRoute2AnchorRuleTable` calls `projectTokenFromID` directly and its table contains only `OwnerApplication`, project, and expected resolved environment. It does not include a target/namespace input, `requestedEnvironment`, or expected visibility through `List`/`ListLogs`.

That means the two reported collision cases (`demo` + `bh-local-demo-prod-west` requested by `west`, and `demo-prod` + the same project requested by `west`) do not assert the actual list result at the acceptance seam. The existing end-to-end tests cover a simple `prod` match/mismatch and a separate hyphenated app `my-app` case, but do not combine the reported project/target collisions with the caller environment. This is the negative cross-environment visibility regression required by the previous review recipe.

## Recipe

Extend the regression table to drive `List`/`ListLogs` with the real `SignalSource` fields and assert visibility, using rows that include owner application, target/namespace/project, requested environment, and expected visibility:

- `demo`, project `bh-local-demo-prod-west`, caller `west` → excluded;
- `demo-prod`, same project, caller `west` → visible;
- `my-app`, project `bh-prod-my-app-dev`, caller `dev` → visible and caller `prod` → excluded;
- reserved `prometheus`, legacy bare ID, and duplicate anchors → excluded.

Keep the existing helper table as focused parser coverage. Push the regression update and capture a fresh exact-head run before re-review.

## Verdict

**REQUEST CHANGES.** The OwnerApplication-anchor implementation addresses the reported ambiguity, and the existing run is green. Merge is held until the collision rows assert the actual caller-visible list behavior at the requested-environment boundary.

## CI cost note

Exact-head run `44495408370` completed from 09:19:51Z to 09:27:28Z (7m37s wall time). Selected jobs passed; runner-minute billing is not exposed in the available run summary. No local tests were run by this reviewer.

## END

END_REQUEST_CHANGES: #1691 / head `f28b97a53870bb3f5cb5c90618dea977df3f1c2b` / run `44495408370` SUCCESS / add List-seam assertions for anchor matrix / no merge.
