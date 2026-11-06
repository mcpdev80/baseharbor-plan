## PLAN

- Read mission, review-1399a, task card; confirm branch provenance (base develop f01d2fbdea6 ancestor, head 88cee2b21d7)
- Reproduce bug: drifted/zero-evidence observation with Synced=true/Healthy=true returns success in delegated path
- Implement fail-closed: call DriftObservation.validate() in HandOff, block true Synced/Healthy without full external evidence; drift => never synced/healthy true
- Add three negation cells: no-evidence true-flag, digest-mismatch true-flag, drift true-flag; keep positive evidence-backed cell green
- Mutant: remove validate() call -> three negation cells go RED; git-diff + counterprobe to prove real mutation
- Local race-20 + build + vet + format on new head; hosted TERMINAL run witnessed to terminal; ls-remote exact==head
- Push round-2.md + ls-tree witness, commit evidence to origin/main; post END to Coordinator 841e7734
