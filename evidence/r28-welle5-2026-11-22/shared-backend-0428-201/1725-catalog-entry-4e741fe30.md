# 0428-201/#1725: add catalog line for shared_backends_state_version_test.go (TP fail-loud confirmed) + re-host

- karte 0428-201/#1725, sitz f0f6c8b4. TP finding CONFIRMED (owner+coordinator verified): #1725 brings new product source internal/application/shared_backends_state_version_test.go WITHOUT a catalog line -> Trusted Plan fail-loud (run 45082725205, job 'PR · Trusted Plan').
- Test-to-CI adoption duty: same lane, same PR. Add catalog entry to scripts/pr-gate-coverage.json (this lane's write-set for THIS card, per mission).
- NO subagent.

## PLAN

1. HEAD 4e741fe30 retained (up-to-date with develop ef73b50b). NO further hop. Confirm catalog diff vs develop empty pre-edit.
2. Catalog entry under components, pattern-faithful (analog cmd.baha.target.runtime.access.provider.test.go): id + path of new test file. SURFACES: pick gate surfaces that actually run this test (query catalog which gate covers internal/application package natively — likely data-capabilities atomics OR lifecycle surface; choose with justification). runtime_specific only if needed.
3. Before next hosted cycle: try to REPRODUCE the TP check LOCALLY (python3 scripts/pr-gate-plan.py with diff-base inputs; read TP 'resolve exact immutable PR inputs using trusted base policy' source). LOCAL GREEN = push. LOCAL NOT REPRODUCIBLE = justified ONE hosted cycle (CI-efficiency, justification in akte).
4. SUSPICION CHECK: guardian might read catalog from TRUSTED BASE (merge-base) not HEAD ('immutable trusted base', plan-script lines ~257/~565). If after head-side entry the hosted TP STILL reports uncataloged: STOP with file:line of read-path + local reproduction — systemic governance finding (same class as #1765), then coordinator/owner/codex decides, NOT you.
5. push + ls-remote witness + EXACT hosted bis terminal. Report head + run-id + entry-justification + gates.

## BASE ATTESTATION

- HEAD (git ls-remote origin refs/pull/1725/head): 4e741fe30ecbb0da702a9f8838818103737af3ca
- develop HEAD (git ls-remote origin develop): ef73b50b6aee3dea8d4badf347c264daefa3d064
- #1725 branch: w201-0428-201-statever
- Uncataloged source (guardian): internal/application/shared_backends_state_version_test.go (id source.internal_application_shared_backends_state_version_test_go)

## END

END_DONE|END_BLOCKED w27-pr1627-0428-061-pull: 0428-201/#1725 catalog entry. head, run-id, entry-justification, gates, 'cleanliness:'
