# 0428-198 exact gate closure — 2026-11-21

- Prior failing witness: PR run [44864365574](https://github.com/mcpdev80/baseharbor/actions/runs/44864365574) reported missing authenticated operator context in the CLI shards.
- Current test harness uses test-only `testOperatorContext` and `runWithIOAsTestOperator`; no lane supplies auth environment variables and no production authorization code was changed for this gate.
- Exact post-fix hosted witness: PR #1587 run [44885697655](https://github.com/mcpdev80/baseharbor/actions/runs/44885697655) at `c43d816120651c33a7a9c02f6ee805ae78440602`: cli-0, cli-1, cli-2, cli-3 and `PR Selected Checks` PASS.
- Newer exact witness: PR #1743 run [44887314441](https://github.com/mcpdev80/baseharbor/actions/runs/44887314441) at `f0f25e49753ad6b06b490072739437eeec42de8a`: cli-0 through cli-3 and `PR Selected Checks` PASS.
- The test-only candidate PR #1726 was closed as superseded on 2026-11-21; the current base already carries the shared test fixture behavior. No changes were made to PR #1615.
