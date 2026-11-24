## #170 disposition evidence — window-independent review

### Exact #170 hunk and intended behavior

PR #170 is open/draft at head `0249c9f73c21f46ba532fddc94a764e772f69acf`, parent/demo develop `c23bd9ac58919302ffad3a43f43afb1a34bfbc96`. Its only changed file is `tests/config-matrix/run.sh`.

The hunk appears intended to bootstrap the shared Core control plane in a consent-allowed isolated directory before the matrix cases. The success assertion is `baha doctor` followed by `grep -q '^READY'` at run.sh lines 34-35. A failed consented `baha up` prints `config-matrix-core-up.txt` and exits 1 at lines 28-32. The block runs only when `DEMO_SUITE` is empty (line 27).

The fixture wrapper's concrete rejection is `fixture-consent.py:91`, `fixture command outside selected Demo source or registered Core bootstrap project`. Its registered-root exception requires the allowed root to be a direct child of `RUNNER_TEMP`, have the `baseharbor-core-bootstrap.` prefix, and equal the current working directory (`fixture-consent.py:82-89`). The existing correct bootstrap pattern creates the directory directly under `RUNNER_TEMP` and runs the command from inside it (`tests/core-bootstrap.sh:5-15`).

The #170 version instead creates `matrix_root` under `DEMO_ROOT` (`config-matrix/run.sh:9`), points `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT` at that root (`line 29`), and invokes `run_consented` without `cd` into it (`line 30`). That is not the registered-root exception: the directory's parent is `DEMO_ROOT`, not `RUNNER_TEMP`, and the command's current directory is not `matrix_root`. When the caller's current directory is inside the Demo source, the wrapper's broader source-root check (`fixture-consent.py:79`) accepts the old in-source nested bootstrap as well. Therefore the current evidence does not show that the hunk prevents this wrapper rejection; in an external working directory it does not meet the wrapper's exception conditions.

### Hosted history

- **Run [45052561097](https://github.com/mcpdev80/baseharbor/actions/runs/45052561097)**, created 2026-11-22 18:06 UTC, used Core candidate `8561447dc5ff70b5fbd74b0b5da9c2a680e83869`, Demo SHA `c23bd9ac58919302ffad3a43f43afb1a34bfbc96`, gate `config-matrix`; job 137302542638 (`Static · config-matrix / Executed static · config-matrix`) failed. The log shows the gate invocation sets `DEMO_SUITE=static`, and the first failure is `workload-only: initialization failed` with `authentication_failed`. `contract_check.py:57` raises this diagnostic when `baha app init --quick --json` fails (line 55). In run order, `config-matrix/run.sh:7` executes `contract_check.py` before creating `matrix_root` at line 9 or reaching the bootstrap guard at line 27. This run therefore did not execute the #170 hunk. It postdates the #170 commit timestamp, but it checked out its parent `c23bd9a`, so it tested pre-hunk Demo source.
- **Run [44909067224](https://github.com/mcpdev80/baseharbor/actions/runs/44909067224)** also failed `Static · config-matrix`; its log records Demo SHA `5d1cf312e18d06915db35c340bebe4e3d4f39d45` and the same `workload-only` authentication failure. It predates #170 and does not exercise the bootstrap hunk.
- **Run [45432650561](https://github.com/mcpdev80/baseharbor/actions/runs/45432650561)** used Core develop SHA `f14fb87c8f5afd91168e4f174d620c9f00e6341e`; its `Static` job and `Reference Journey` job were both skipped. Other recent Pre-Release runs with Reference Journey jobs (44902168397, 44975747939, 45015867089, 45402677135, 45434224033, 45438096326) also report `skipped`. The successful run 45015867089 executed/reused `ci-fast-check`, not config-matrix.

The hosted `atomic/static/config-matrix` route explicitly sets `DEMO_SUITE=static` at `pre-release-runtime-suite.yml:262`; it cannot exercise the conditional bootstrap hunk. The only executed config-matrix failures found in the relevant hosted history fail earlier in `contract_check.py:57` with operator authentication. The Owner-designated 0428-284/#1812 test-certificate login path and 0428-285/#1827 Core fixture/operator-allow-list path address distinct authentication/fixture behavior; their existence does not constitute hosted proof for #170's hunk.

### Verdict and next authorized step

Verdict remains **UNPROVEN**. Neither a hosted reproduction showing #170's hunk is needed nor hosted proof that develop already covers the hunk's behavior was found. PR #170 remains open/draft; no PR changes were made.

Wait for the Owner's explicit window signal, after 0428-283 lands and Demo develop advances. Then use the single authorized dispatch slot for `atomic/static/config-matrix` against the new Demo develop tip without the #170 hunk, and record its exact checkout SHA and result. No dispatch is authorized before that signal.

END_DONE w113b-n170 round-7: evidence recorded; disposition held unproven; no dispatch or PR change.
