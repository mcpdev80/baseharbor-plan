# 0428-201/#1725: STOP — systemic governance finding (trusted-plan reads catalog from BASE; PR-new source cannot be admitted)

- karte 0428-201/#1725, sitz f0f6c8b4. BEFEHL-KORREKTUR: STOP my last catalog mission.
- #1753 proved SYSTEMIC: trusted-plan job checked out ef73b50b = trusted BASE, not HEAD, so the catalog is read from BASE — a same-PR catalog line cannot admit a NEW product source.
- For #1725 this is ENHANCED: internal/application/shared_backends_state_version_test.go does NOT exist in develop (PR-only), so a predecessor catalog PR is impossible (a catalog line on a missing file = fail-loud).
- DO NOT edit catalog, DO NOT push, DO NOT retry.

## PLAN

1. Discard my local catalog edit (checkout -- scripts/pr-gate-coverage.json). HEAD reset --hard back to 4e741fe30. Confirm catalog diff vs develop == EMPTY.
2. Witnesses: ls-remote current #1725 head. PROOF source is PR-new: git cat-file -e origin/develop:path -> ABSENT. Sibling exists on develop for contrast.
3. Confirm systemic: my hosted retry still fails with the same fail-loud ValueError (run id + source line).
4. Melden END_BLOCKED: current ls-remote head + systemic finding. Card goes to blocked — ingress requires a product-bearing predecessor lane OR a TP-policy decision at the owner (trusted-base vs head reading for catalog). No new catalog edit, no new push.

## BASE ATTESTATION

- Current worktree HEAD (git rev-parse): 4e741fe30ecbb0da702a9f8838818103737af3ca
- Current remote #1725 head (git ls-remote origin refs/pull/1725/head): e6907e591c44d30f63eca4f30b732dd31b8948b8 (the single hosted retry; FAILED hosted, never a passing candidate)
- develop HEAD (git ls-remote origin develop): ef73b50b6aee3dea8d4badf347c264daefa3d064 (trusted base)
- #1725 branch: w201-0428-201-statever
- Uncataloged source: internal/application/shared_backends_state_version_test.go (id source.internal_application_shared_backends_state_version_test_go)

## PROOF: source is PR-new (absent on develop)

- git cat-file -e origin/develop:internal/application/shared_backends_state_version_test.go -> `fatal: path 'internal/application/shared_backends_state_version_test.go' exists on disk, but not in 'origin/develop'` -> ABSENT on develop.
- Contrast: git cat-file -e origin/develop:internal/application/shared_backends_state.go -> EXISTS on develop (sibling already cataloged). This confirms the state_version test is the only PR-new source; the two .go siblings are already cataloged.

## SYSTEMIC finding (the #1753 class)

- My hosted retry run 45084235780 @ e6907e591 (catalog edit added INSIDE the PR) STILL FAILED with the identical fail-loud ValueError. This proves the trusted-plan job reads the catalog from the trusted BASE (ef73b50b), NOT from the PR HEAD — so a same-PR catalog line cannot admit a PR-new source.
- TP-failure source line (run 45082725205 and re-confirmed 45084235780, pr-gate-plan.py line 1833, job 'PR · Trusted Plan', step 'Resolve exact immutable PR inputs using trusted base policy'):
  - `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/application/shared_backends_state_version_test.go (id source.internal_application_shared_backends_state_version_test_go): add this source with its surfaces to scripts/pr-gate-coverage.json, e.g. {"id": "source.internal_application_shared_backends_state_version_test_go", "path": "internal/application/shared_backends_state_version_test.go", "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]}`
- The guardian's own suggested fix (add the catalog line to scripts/pr-gate-coverage.json) is impossible to satisfy within the PR: the base the guardian reads (ef73b50b) does not contain the file, and a same-PR line on a file absent from the trusted base is not seen by the guardian.

## Action taken

- Discarded my local catalog edit (checkout -- scripts/pr-gate-coverage.json); HEAD reset --hard back to 4e741fe30.
- Confirmed catalog diff vs develop == EMPTY (no catalog edit present in worktree HEAD).
- No new catalog edit, no new push in this turn. (e6907e591 was pushed once as the single hosted retry; it FAILED hosted — it is never a passing candidate and must not be re-pushed as one.)

## Card disposition

- Goes to blocked. Ingress requires either:
  - a product-bearing predecessor lane that adds `internal/application/shared_backends_state_version_test.go` to a base the trusted-plan reads, OR
  - a TP-policy decision at the owner (trusted-base vs HEAD reading for the catalog) — the guardian's fail-loud behavior on a legitimately PR-new source is a governance question, not a lane fix.

## END

END_BLOCKED w27-pr1627-0428-061-pull: 0428-201/#1725 STOP (systemic governance finding). current ls-remote #1725 head = e6907e591 (the single hosted retry, FAILED hosted run 45084235780; never a passing candidate). WORKTREE HEAD = 4e741fe30 (reset back from the discarded catalog commit); catalog diff vs develop == EMPTY — KEIN katalog-edit vorgenommen in dieser Sitzung. PROOF source is PR-new: git cat-file -e origin/develop:internal/application/shared_backends_state_version_test.go -> ABSENT on develop; sibling shared_backends_state.go EXISTS on develop (already cataloged). SYSTEMIC (#1753 class): trusted-plan reads the catalog from the trusted BASE ef73b50b, NOT PR HEAD; my hosted retry e6907e591 (catalog edit inside the PR) STILL failed with the identical fail-loud ValueError. TP-failure source line: `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/application/shared_backends_state_version_test.go (id source.internal_application_shared_backends_state_version_test_go)`. Ingress requires a product-bearing predecessor lane OR a TP-policy decision at the owner (trusted-base vs HEAD reading for the catalog). No new catalog edit, no new push. No subagents. cleanliness: git-only, docker ps -a clean (no containers started locally).
