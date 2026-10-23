# Codeman handoff — 2026-10-22 (evening, full-speed resumption day)

Authority: `decisions/2026-10-22-codeman-resumption-full-speed.md`. Follows `../codeman-2026-10-21/HANDOFF.md`.
All claims below verified live by the coordinator (gh/git reads at ~18:10 UTC) unless marked worker-reported.

## Done and verified today
- Source **A/B/C merged** to baseharbor `develop` (now `2adae47a…`): PRs #1033/#1035/#1036 via Form3 heads
  (parents [source, develop]; chain/diff gates green; BLOCKED-state shown to be unenforceable noise —
  `evidence/board-2026-10-22/o14-diag3-merge-blocked.md`). Admin-owner merge pattern, actor `mcpdev80`,
  8/8 scope blobs equal frozen sources (`codex-merge-1030.md`, MERGE-BATCH-2).
- **Demo PR #116 merged** to demo `main` (`ee62eb2f…`): cleanup-accounting unified per f6 audit
  (`q15-demo-cleanup-race.md` + `f6-demo-audit.md`).
- Docs #1031 and CHANGELOG-gate #1034 merged earlier (develop `7fbc1ec5`, `984d7160`).
- Freeze execution sheet built and **independently verified** (`q16-freeze-tracker.md`,
  `q17-freeze-sheet-verify.md` — corrections C1–C4 noted; sheet usable with those fixes).
- Independent **CODEX REVIEW** of the native-evidence plan: verdict *CHANGES REQUIRED / PRE-READY: NO*,
  expanded gate set + correct freeze order C → Demo-pin → D → Console U → Connector N
  (`codex-review-demo-plan.md`). This review is the governing recipe for the current phase.
- Prepare-card evidence ledger assembled (`o15-prepare-evidence.md`): per checklist MET/PENDING/BLOCKED
  with proof links.
- Podman gate chain: rootless runner healed, `#1008` fix merged earlier, VM-net incident closed
  (`p23-*.md` successors in board-2026-10-19/-20 folders; three-point-check rule now in RUNBOOK §10).

## In flight (coordinator-managed lanes)
- **DONE 18:5xZ: Demo pin PR #117 MERGED → D = `896dc3cb68a8c9b9585940c4696410de5a338c52`** (core.ref blob == C
  verified; `codex-merge-1030.md` MERGE-DEMO-PIN). Native dispatch on C+D started (q18); consumer final pins U/N
  by o16 in flight.
- **DONE: Consumer refreeze+pins green.** o16 found old locks pinned `d5417bde` (hash mismatch after A/B/C) and
  refroze both consumers: console PR #7 head `0ea88f5` CI SUCCESS incl. source-lock verification;
  connector PR #8 head `570864c` all checks SUCCESS (`o16-consumer-pins.md`). Both DRAFT, merge after native
  dispatch evidence per recipe order.
- **Native dispatch executed (f7) on C+D: 1 PASS / 7 FAIL-gates.** Dominant NEW class: guided
  `new-edit-new-zero-no` missing `Read-only decision preview (not execution)` assertion (suspect Source C
  surface text; fix mission T1 running, flash lane). Secondary: journey-podman F5-hang-class (likely same
  root), data-podman 8-min step cap (T4 recipe running), backup-restore-podman cleanup-provenance
  incomplete (T3 diagnosis running). Static/mcp + backup-restore-docker PASS. Full table:
  `evidence/board-2026-10-22/f7-native-dispatch.md`. Prepare remains NOT ready until reruns on fixed C2.

## Known-good native evidence (pre-freeze, still applicable per review caveats)
- Docker backup-restore `29886110551` success; MCP static parity on earlier candidates;
  guided-light/heavy failures rooted in the `[Y/n]` wizard hang — **fixed by merged B**; reruns required
  on the frozen candidate, not assumed.

## Next triggers (board must be updated at each)
1. Demo pin PR merged → record D (40-hex) here + on prepare card evidence.
2. Native dispatch set complete → results table here.
3. Console U / Connector N pinned & green → close PENDING markers.
4. Final 65-gate matrix dispatch (owner go per o13b runbook) → `evidence/codeman-2026-10-23/matrix.md`.
5. Prepare acceptance (CODEX REVIEW verdict + owner) — only after 1–3. Publish/tag stay owner-gated.

Lane/evidence index: `evidence/board-2026-10-22/` (38 files). Planning remote before this commit: `e4894fa`.

## CMD-A matrix triage (q24, run 39853157648)
26 jobs, 4 failed = 1 REAL-DEFECT + 3 cascade. NOT preview-line related: `ecosystem_release_pins.py:124`
fetches `release/v0.4.26` in a consumer repo which does not exist yet. q24 follow-up: NOT a repo gap - the matrix
dispatch passed a non-existent `consumer_ref` branch; correct usage is empty consumer_ref (auto-resolves
`work/v0.4.26-integrations-docs`) or its real 40-hex tip. Rerun wave must use those inputs; no branches to create.

## C2 minted (2026-10-23 ~01:20)
Core develop = C2 `2f005813dc6d7fa94de164388b2531d025af31bc` (#1040 selector fix + #1038 preview-line fix merged;
fresh CI 10 success/10 conditional-skip). #1039 pending check-generation fix (q28). Demo #118 head moved past
reviewed d9c78b57 by fetch-fix c1285a8 -> head-delta review q29 before merge. Codex verdicts: all four review
cards CHANGES-REQUIRED with concrete recipes (codex-verdicts-2026-10-23.md) - being executed by o31/q27 lanes.
Next: #1039 green -> D2 = demo(main + #118 + core.ref=C2) -> W1 dispatch per f9 sheet.

## W1 preflight findings (o32/o33)
Defect ledger fully IN-C2. Atomic acceptance gate is STILL-BROKEN for bare-SHA dispatch (checkout refspec limit);
correct mode = ref: develop + internal resolve step. Fix PR in flight (f12); f9 sheet must dispatch W1 with
ref=develop + SHA via resolve inputs, consumer_ref="" (q24). o31 made #1041 green (c3697113).

## Freeze trigger rules (o34, full table in o34-integration-triggers.md)
Branch names are workflow-specific: core+connector key off `work/v0.4.26-integrations-docs` (exact-list triggers),
console keys off `release-integration/**` wildcards, demo per its own filters. Step 7 must create the per-repo
named branch; commit messages must satisfy the guard at resolve (L29 style) - check table before pushing.

## Demo cleanup chain CLOSED (T3)
#118 rounds: c1285a8 (last-row bug, o35/o38 proven FAIL) -> 8d27e3c (rowfix, accounting invariant gap, codex G)
-> 08f36ba (exact set equality, BOTH executable repros gate exit 0, o40) -> **MERGED, demo main = `82d042b`**.
Repro scripts now permanent under evidence/board-2026-10-22/scripts/. Pending for D2: core #1039/#1042
selector qualification (f14) + #1041 merge, then pin core.ref=C2 on main 82d042b.
