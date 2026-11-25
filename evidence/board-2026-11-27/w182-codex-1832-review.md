# w182-codex-1832-review — PR #1832 independent review

## PLAN

1. Read the mission and verify task, candidate, base, and review boundaries.
2. Verify remote candidate provenance, exact diff, author, and affected-source catalogization.
3. Check card contract and independently verify required GitHub Actions runs and review evidence.
4. Record a SHA-specific verdict and evidence in baseharbor-plan; comment on PR only if authorized outcome is clear.
5. Publish evidence, verify remote state, and post the required lane END status.

## Evidence

Mission read: candidate SHA `976a258c1a170bbaa55ce030ac292a879a11e526`; card `t-20261116-r28-bug-metrics-discovery`. Planning repo remote witness: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`. Product checkout remote witness confirmed `https://github.com/mcpdev80/baseharbor.git` via lane-origin/origin/upstream; checkout had unrelated dirty state and was not used for candidate evidence.

Stop directive received from owner: stand down to standby. Independent diff review and run-attempt verification were not completed. The initial read-only GitHub query showed PR #1832 already MERGED at head `976a258c1a170bbaa55ce030ac292a879a11e526`; at that time the merge SHA had not yet been re-queried in this lane. No PR comment, merge, CI rerun, or product-repository write performed. The initial stand-down note was recorded before retrospective work. The PR merge SHA was supplied by the owner and then independently confirmed via the GitHub PR API.

## RETROSPECTIVE exact-head notes

Candidate: PR #1832, head `976a258c1a170bbaa55ce030ac292a879a11e526`, base `develop` at `a87da7d179e08d43e8987885c38ab459ff1d887d`; merged as `2a141387dbbaf24f52501a0f66f1abf61cf8fcda`. The exact PR API file list contains eight paths:

- `cmd/baha/app_init_detection.go` (142 additions, 3 deletions): records metrics source module and proven HTTP path; resolves source/service/internal-port/path as one tuple; limits paths to `/q/metrics`, `/actuator/prometheus`, and `/metrics`; fails closed on ambiguous workload/module attribution.
- `internal/repositoryinspect/capability_detectors.go` (107 additions, 3 deletions): extracts/classifies only exact registry paths and scans `.properties` alongside existing source/config formats.
- `cmd/baha/app_init_prompts.go`, `cmd/baha/app_init_selection.go`, and `cmd/baha/app_init_wizard.go`: carry and validate the detected endpoint path through guided selection and prompt flow rather than silently hardcoding an arbitrary path.
- `cmd/baha/app_init_metrics_boundary_test.go` and `internal/repositoryinspect/metrics_endpoint_boundary_test.go`: add exact-registry, arbitrary-path rejection, source/service attribution, and quick-init/detector regressions.
- `cmd/baha/app_init_wizard_test.go`: adds wizard regressions for the detected source tuple/path.

Scope check: all eight paths are metrics detection, wizard/selection, and tests. The PR file list has no `.github/**`, `ci.yml`, auth/consent, or source-catalog file. No changes were made by this review lane.

Hosted Actions verification for exact head (links identify attempts of one workflow run):

- Run ID `45591459360`, attempt 2: `completed`, `success`, head exactly `976a258c1a170bbaa55ce030ac292a879a11e526` ([attempt 2](https://github.com/mcpdev80/baseharbor/actions/runs/45591459360/attempts/2)).
- Run ID `45591459360`, attempt 3: `completed`, `success`, same exact head ([attempt 3](https://github.com/mcpdev80/baseharbor/actions/runs/45591459360/attempts/3)). `PR Selected Checks` was successful on attempt 3 (job `139182259222`).
- Important identity detail: GitHub reports the same workflow run ID for attempts 2 and 3; they are two successful attempts, not two distinct run IDs. The only distinct earlier successful run found on this PR branch was `45582189971`, whose head was `cee9ff8a1938647375bad90c7d1a0f996eef10e1`; it is not exact-head evidence and is not counted as such. Thus the mission wording “two runs” is supported as attempts 2 and 3, while a requirement for two unique same-head run IDs is not supported by the API record.

This is retrospective scope and CI evidence after merge, not a completed pre-merge independent verdict. The original `END_BLOCKED` was accepted because owner stand-down preceded that verdict.
