# CODEX-REVIEW 0427-174 r2 — PR #1506

ROLLE: REVIEW
URTEIL: approve

## PLAN

1. Pin the current PR head and develop base from GitHub; verify ancestry and own-commit range.
2. Inspect the candidate diff, owner-error classifications, production CLI path, loan recheck, and regressions against the prior review findings.
3. Compare develop and candidate binaries with the permission-denied installation fixture; inspect hosted checks and test routing.
4. Publish this SHA-specific verdict in the planning evidence vault.

## Candidate and provenance

Repository: `mcpdev80/baseharbor`, PR #1506, task 0427-174.

- PR head: `1080ac444d4b7d0f1cf6d20d31b51d51519fbc7a`.
- Fetched develop head: `b3a8042d18ea60f162a32a51df34a499cad6a237`.
- `git merge-base --is-ancestor b3a8042d18ea60f162a32a51df34a499cad6a237 1080ac444d4b7d0f1cf6d20d31b51d51519fbc7a`: exit 0.
- `git log --oneline b3a8042d18ea60f162a32a51df34a499cad6a237..1080ac444d4b7d0f1cf6d20d31b51d51519fbc7a`: exactly the two candidate commits `fe7346d05` and `1080ac444`; no foreign commit is carried.
- The PR is open and mergeable. Product write set contains no `.github/**` path.

## Findings

1. Permission-denied is distinct from missing and foreign at the production CLI path. `internal/deployment/deployment_owner_classification.go:39-67` classifies permission and other filesystem read failures as access errors; `deployment_store.go:157-183` wraps them as `ErrDeploymentOwnerAccessDenied`; `cmd/baha/app_context.go:294-313` emits the access error with the installation path and repair guidance. This is not merely a package-helper assertion: the isolated fixture was exercised through `baha app status fixture-app` using both built binaries. With the fixture's `installation.json` mode set to `000`, develop printed `application "fixture-app" has no registered deployment on target "local"`; the candidate printed `deployment state for local// is not readable by this Target: ... Core installation.json is not accessible to this user — check owner and permissions before its state is loadable: open /tmp/opencode/0427-174-fixture/state/targets/local/runtime/installation.json: permission denied`. This directly demonstrates the corrected CLI classification and actionable path/hint.

2. A loan recheck read failure is not converted into foreign ownership. `internal/deployment/deployment_owner_loan_recheck_test.go:18-55` injects permission-denied into the actual loan recheck loader path and asserts `ErrDeploymentOwnerAccessDenied` and explicitly rejects `ErrDeploymentOwnerForeign`. The production path in `deployment_store.go:204-210` propagates `verifyLoanOwnerGuarantees` errors.

3. A present but malformed installation fails closed with its own named error; it is neither missing nor foreign. `deployment_store.go:171-183` separates access/read errors, malformed validation errors, and the remaining foreign verdict. `internal/deployment/deployment_owner_malformed_state_test.go:19-73` corrupts the actual installation document, asserts `ErrDeploymentOwnerMalformedState`, rejects Missing and Foreign, and verifies `ListDeployments` preserves that classification. `:75-105` separately protects a positively loaded divergent target as genuinely Foreign. This covers the requested non-hash/content-validation error case without weakening the actual foreign-owner check.

4. CI routing is durable and the relevant hosted checks passed on the exact head. Run `42558911822` is terminal `completed/success`, event `pull_request`, head exactly `1080ac444d4b7d0f1cf6d20d31b51d51519fbc7a`. `PR · Validation · go-unit-tests` and `PR · Validation · deployment-package-tests` succeeded, as did `PR Selected Checks`. The tests in `internal/deployment` are run by `deployment-package-tests`: `scripts/pr-check-runner.py:170-175` maps that selected check to `go test ./internal/deployment/...`; `.github/workflows/ci.yml:964-969` dispatches it through the PR validation matrix. The command CLI regression is included in `go-unit-tests`, which runs `scripts/pr-unit-database.sh`; the workflow is triggered for pull requests to develop/main (`ci.yml:10-17`) and the selected PR validation ran it on this head.

5. Native status is reported without counting skips as green. The exact run passed both Native destroy retry Docker and Podman jobs (`128970808615`, `128970808622`). Native Keycloak/Core, Targeted HA Docker, and Targeted HA Podman were skipped; they are not evidence of execution. They did not fail the aggregate: `PR Selected Checks` passed.

## Verdict and actionable landing recipe

APPROVE PR #1506 at the exact head above. The three corrected error distinctions are exercised by regressions and the permission-denied behavior is confirmed through the candidate binary against develop. Before landing, retain the exact-head `PR Selected Checks` success and verify the develop ancestry remains true. Treat native Keycloak/Core and Targeted HA cells from run `42558911822` as skipped, not passed; rerun/require them only if the merge contract or owner-selected native impact requires execution. Stop landing if the PR head changes, ancestry is lost, or a required selected check is no longer successful.

## repo-rule compliance

- Review was read-only against the product repository; no candidate files were changed.
- Evidence is stored only in the canonical `baseharbor-plan` repository. Its origin is `https://github.com/mcpdev80/baseharbor-plan.git`.
- No workflow files were edited and no CI rerun was triggered.

END_DONE 0427-174-r2-review: APPROVE PR #1506 head 1080ac444; exact hosted run 42558911822 success with native Keycloak/Core skipped.
