## PLAN

- Dispatched one hosted `Targeted Atomic Gate` `workflow_dispatch` run (workflow file `.github/workflows/targeted-demo-acceptance.yml`) with Core `ref=f14fb87c8f5afd91168e4f174d620c9f00e6341e`, `demo_ref=0249c9f73c21f46ba532fddc94a764e772f69acf`, `runtime=static`, and `gate=config-matrix`.
- Run `45442419205` completed with terminal conclusion `startup_failure`; GitHub reported zero jobs and no downloadable logs. There is no resolution log line proving which demo SHA was checked out, and no evidence that `tests/config-matrix/run.sh` executed.
- Disposition: STOP + QUESTION to Coordinator. The hosted proof is inconclusive; PR #170 remains open and draft. No merge or close was performed.
- Request: restore/identify a usable hosted runner path for this workflow and provide the resulting checkout resolution log plus gate result for the exact demo head before dispositioning #170.
