# PR #1754 merged - witness for card 0428-229 (0428-229 cells missing runner prerequisites)

- Merge: squash into `develop`, merge commit `82825e95a6f6083702d0ba5401d97f356085c722`, `mergedAt 2026-11-22T03:42:20Z`,
  PR state `MERGED`, approved exact head `0975e67131921808d65d32580a6e60a88e54724e`.
- Hosted proof at that exact head:
  - Draft PR run `44980710684` completed/success, 33 jobs, 0 failed.
  - cli-3 job `137080402549` installs the shells (`sudo apt-get install -y zsh fish`, `zsh: /usr/bin/zsh`,
    `fish: /usr/bin/fish`) and then emits `--- PASS: TestEndToEndInstalledZshAndFishWrappers (8.02s)` plus
    `ok github.com/mcpdev80/baseharbor/cmd/baha 8.026s`; the canonical shard afterwards reports
    `No changed Go packages.` as designed for a workflow-only diff.
  - Ready-state PR run `44980875340` completed/success.
- Independent review: `codex-rev-*` verdict file for head `0975e671` (published by seat `fecbada9`).
- Post-merge develop verification: push workflow runs `44981840188` (Runtime Docker Core) and `44981840193`
  (Runtime Podman Core) both completed/success at the merge commit `82825e95a6f`.
- Consequences carried forward: the cli-3 blocker in PR #1750 (job `137070473455`) and PR #1752 (job `137077374467`)
  is resolved by content, but only after those heads hop onto `82825e95a6f`; the hop wave is dispatched to seat
  `b90e4ba1` (mission sha `2203dec27755`).
- cleanliness: nothing started by this record; planning-only change.
