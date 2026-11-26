# PR #1753 independent review — 71deb610a03b

## PLAN

1. Verify the live GitHub remote, exact PR head/base, ancestry and exact hosted run identity.
2. Read card 0428-227 and inspect the full candidate diff, focusing on canonical footprint show, operator data-capabilities authorization, and preservation of gate intent.
3. Identify every required exact-head CI gate, including Docker data-capabilities; inspect only remote hosted logs and count only executed gates.
4. Withhold verdict until run 44972857723 and every required gate are terminal; record exact SHA, evidence and findings.
5. Preserve the existing #1750 review in progress; make no product changes, local tests, merge, close, comments, or reruns.

## Status

## Exact refs and diff

- Planning repository remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1753/head refs/heads/develop` returned `71deb610a03b910fb0fbc924c0639fb197b6c646 refs/pull/1753/head` and `6209874428f08dc3e90d6e29a42b30683ce9932a refs/heads/develop`.
- GitHub PR API reports #1753 OPEN, ready for review (`isDraft=false`), base `develop`, head `71deb610a03b910fb0fbc924c0639fb197b6c646`. GitHub compare reports `ahead_by=2`, `behind_by=0`, merge-base exactly `6209874428f08dc3e90d6e29a42b30683ce9932a`.
- Full PR file diff is limited to `cmd/baha/ci_integration_operator_enabled.go` (+16) and `cmd/baha/ci_integration_operator_enabled_test.go` (+69).

## Review findings

The operator exception is narrowly constrained. `ci_integration_operator_enabled.go:1,24-27` exists only under the `baseharbor_ci_operator_testonly` build tag and requires the disposable acceptance environment. Existing gate validation at `:96-106` requires both gate environment values to agree, runtime to be Docker or Podman, target name to equal `atomic-<runtime>-<gate>` and the selected `BASEHARBOR_TARGET`, and a local, tenantless target with matching runtime provider. The new allow rule at `:138-147` adds only `gate == "data-capabilities"` plus the canonical exact command predicate `:246-249`; the shared fail-closed rejection remains at `:189-190`. I found no path here that admits a mutation or a noncanonical footprint command.

The regression `ci_integration_operator_enabled_test.go:352-419` verifies the canonical JSON read is admitted on data-capabilities and guided, while flag variations, a named-target form, unrelated app logs, and the lifecycle gate remain rejected. This preserves the existing gate boundary and gate intent at source level.

Blocking finding: card 0428-227 requires the data-capabilities Docker job to pass on this exact SHA. Exact run `44972857723` completed SUCCESS, including `PR Selected Checks` job `137057431390` SUCCESS, but `Targeted HA · docker` job `137056209067` and `PR · Selected Runtime` job `137056261917` both completed SKIPPED. The `PR · Native gate plan` job `137056208147` log explains why: the develop base did not contain the trusted native gate planner, so it produced `matrix={"include":[]}` and warned that no native runtime checks could be selected. A green aggregate with the required Docker data-capabilities gate skipped is not acceptance evidence. The code change can be accepted only after the required mapping/selection dependency is available and the Docker data-capabilities gate actually executes and passes at an exact current head. Card 0428-228 identifies that shared path-to-gate mapping as the coordinator-owned dependency; the native planner itself is based on trusted develop policy.

## Current hold — verdict withheld

The source change and scoped positive/negative regression look correct, but the mandatory Docker data-capabilities job did not execute on the requested exact run. The latest coordinator note reports a separate exact run on PR #1723, head `8fe3c9bfb3c`, run `44972884814`, Docker data-capabilities job `137056660905`: it executed and failed before the footprint boundary because the runtime-consent path required explicit operator/automation consent (`--confirm-candidate`). The same run reportedly passed atomic/docker/guided. This reported failure belongs to card 0428-223, not the footprint-show admission change.

Per the stated order, #1753 remains held until 0428-223 is resolved and then the #1753 Docker data-capabilities gate executes on a current exact head, by the 0428-228 path mapping or an authorized targeted-gate run. No verdict is issued now. No product branch, workflow or PR metadata was changed; no local tests were run.

## CI evidence

- Exact run `44972857723`, head `71deb610a03b910fb0fbc924c0639fb197b6c646`: terminal SUCCESS.
- `PR Selected Checks` job `137057431390`: SUCCESS.
- `PR · Native gate plan` job `137056208147`: SUCCESS, but selected an empty native matrix because trusted planner was absent from base.
- `Targeted HA · docker` job `137056209067`: SKIPPED.
- `PR · Selected Runtime` job `137056261917`: SKIPPED.
- Go unit jobs `137056260017` (cli-0), `137056259974` (cli-1), `137056259975` (cli-2), `137056259985` (cli-3), and `137056260026` (packages): SUCCESS. These do not replace the required native Docker evidence.
- `docker ps -a` was not run; no local tests or containers were started.

## cleanliness

Before snapshot: command `docker ps -a`, shell pid 1625899. After snapshot: command `docker ps -a`, shell pid 1633232. Both showed the same eight pre-existing containers, all exited; this review started no containers. The exact output is recorded in the #1750 review evidence at `evidence/r28-welle5-2026-11-22/oras-0428-229/review-1750-head4bd779b1.md`.

## END codex-rev-1747 BLOCKED

Reason: hold for order step (b), an executed #1753 Docker data-capabilities gate after resolving the separate 0428-223 consent blocker.
