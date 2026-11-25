# w140 END_BLOCKED finding (demo fix routing corrected)

- Hypothesis 'demo mutation lacks --confirm-candidate' DISPROVED by faithful VM repro (w140): run_consented re-binds; guided drive.py reaches READY in all 3 docker gates.
- Reproducible failure: IN_SYNC apply step (demo journey run.sh:10 class) demands RE-CONSENT and aborts.
- Consequence: #1812 Light-gate requal blocked on demo TEST-path fix (mission w152), then demo pin update + develop hop + Docker->Podman batches.
- Zero writes by this lane (branch at b4112772, 0 commits).
