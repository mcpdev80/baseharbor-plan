# Mission H-P3 — visible plan (single source of truth)

Evidence file: baseharbor-plan `evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md`

## PLAN

1. Host attestation on baha-podman: lock file protocol, develop-HEAD binary (built from exact origin/develop tree, checksum-verified transfer), before-state lists (ps, containers, ~/.baha)
2. Cut S1: app new → app edit stream (change fields, invalid inputs, cancel mid-way, returned state)
3. Cut S2: app plan/show consistency after edits (does show reflect what plan computes? stale data?)
4. Cut S3: compose/Dockerfile rendering for multi-service apps (ports, depends, healthchecks — observation only, containers never left running)
5. Cut S4: quickinit → edit → plan mixed paths
6. Findings register: BF-NN per finding with file:proof (command, exit, output excerpt) + class (ux/daemm/doku/blocker-kandidat) + expected-vs-actual; positive cells noted too
7. VM besenrein: after-state lists, compose down witness, lock release, cleanliness line
8. Evidence to baseharbor-plan main, push, verify on origin/main, END post

MELDEFENSTER: END with dossier once 8+ findings or 2 blocker-kandidaten are in.
