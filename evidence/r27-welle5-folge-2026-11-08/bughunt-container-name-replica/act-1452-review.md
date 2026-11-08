# CODEX-REVIEW 0427-128 container-name replica — PR #1452

## Verdict

ROLLE: REVIEW
URTEIL: korrektur (inhaltliche Abnahme ausgesetzt wegen rotem Hosted-CI-Gate)

## STATE: hosted CI failure

The live PR head is `c551fcd01a9276e2346624d47c689d2a562fd8e4`, base `develop` at `e39b0004346cdfd082e34ba55d94d24757bbbd27`. GitHub reports the PR open and mergeable. `gh pr checks` on this exact head reports `PR · Source format` failure and `PR Selected Checks` failure; the other required validation jobs shown here passed, while unrelated selected cells were skipped.

Exact failing log from run `42437310258`, job `PR · Source format` (`128598825185`):

```text
internal/runtime/container_identity_test.go
##[error]Process completed with exit code 1.
```

This is a hosted formatting failure. Under the workflow ownership boundary, the source review stops at this STATE and does not inspect or judge the candidate's implementation criteria yet. The claimed `go test ./internal/...` and `cli-guided-tests` successes do not replace the failed hosted check.

## Correction recipe

- File: `internal/runtime/container_identity_test.go`.
- Change: format the file with the repository's Go formatter (`gofmt -w internal/runtime/container_identity_test.go`) and commit the formatting correction on the existing PR candidate chain.
- Test requirement: allow the normal GitHub PR workflow to run on the resulting exact head; `PR · Source format` and `PR Selected Checks` must both pass. Do not rerun or dispatch workflows manually.
- Stop criterion: do not resume source-contract review until the exact new PR head has terminal green `PR · Source format` and `PR Selected Checks`. Then review planned-name derivation, quiesce diagnostics, cross-project collision coverage, and whether retirement/stop paths must use the same identity contract.

## Candidate and evidence provenance

- Exact PR head fetched from GitHub: `c551fcd01a9276e2346624d47c689d2a562fd8e4`.
- Exact PR base fetched from GitHub: `e39b0004346cdfd082e34ba55d94d24757bbbd27` (`develop`); `gh api repos/mcpdev80/baseharbor/pulls/1452` reported these head/base SHAs and `mergeable: true`.
- Exact-head hosted run: `42437310258`; Source format failed, PR Selected Checks failed.
- Round-1 evidence cited by the assignment: `evidence/r27-welle5-folge-2026-11-08/bughunt-container-name-replica/round-1.md`.
- Planning repository verified as `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; `origin` fetch and push URLs are `https://github.com/mcpdev80/baseharbor-plan.git`.

END_DONE integration-1452-review: ROLLE REVIEW; CI STATE blocks source review at candidate `c551fcd01a9276e2346624d47c689d2a562fd8e4`.

## R2 continuation — content review on corrected head

ROLLE: REVIEW
Current verdict remains KORREKTUR / request changes. The exact PR #1452 head is `978503376c34e447fc0f82451c35b43fb9fa8fd5`, base/develop `e39b0004346cdfd082e34ba55d94d24757bbbd27`, OPEN and MERGEABLE. Fresh `git ls-remote` witnesses matched both SHAs; `git merge-base --is-ancestor e39b0004346cdfd082e34ba55d94d24757bbbd27 978503376c34e447fc0f82451c35b43fb9fa8fd5` returned 0. The delta from the previously reviewed `c551fcd01a9276e2346624d47c689d2a562fd8e4` is only gofmt formatting in `internal/runtime/container_identity_test.go`; `git diff --ignore-all-space` for that file is empty.

Hosted run `42440204879` is terminal success on this exact head. `PR · Source format` and `PR Selected Checks` passed, as did the displayed CLI validation and source-contract jobs. `Targeted HA · docker` and `Targeted HA · podman` were skipped. Thus the gofmt blocker is resolved, but the card's native Docker backup acceptance is not evidenced by this run.

### Finding 1 — production Compose render is not reachable through the declared interface

`internal/runtime/container_identity.go:24-25` declares `RuntimeConfigProvider.ConfigJSONProjectFilesEnv(context.Context, string, string, ...string)`. The actual production method has the signature `ConfigJSONProjectFilesEnv(context.Context, string, string, map[string]string, ...string)` in `internal/runtime/compose_files.go:65` and `internal/providers/runtime/podman/lifecycle.go:228`; Podman embeds the Compose backend. These method sets are not compatible, so the production `Compose` and Podman provider do not satisfy the assertion at `internal/runtime/service_stop.go:80`. The `expectedContainerNameSet` helper at `container_identity.go:36-48` also calls the wrong shape and is only covered by a test stub with that same incorrect signature. Consequently production selected-stop falls back to `<project>-<service>-1` (or the Podman project-service alias) instead of consuming the rendered pinned name/replica set. The parser test at `container_identity_test.go:33-74` proves parsing only; it does not prove the production caller uses the set. The reported service/native-name error at `service_stop.go:91` is useful, but it reports this false rejection rather than accepting the valid pinned identity.

There is a second raw-name check after the stop at `service_stop.go:142`. It still uses `ContainerMatchesProjectResource`, which only accepts the canonical ordinal or Podman alias. Keep the same rendered planned set for post-stop verification too; the Podman stop path issues `systemctl stop` and lists all containers afterward, so a stopped pinned container may remain observable and be rejected by this raw check.

### Finding 2 — cross-project test does not cover the new pinned-name matcher

`container_identity_test.go:8-24` has a foreign-project negative case, but it tests `ContainerMatchesProjectResource` with the canonical `owned-keycloak-db-0-1` name. The pinned-name parser cases at lines 33-74 do not test project labels, and `containerNameInPlannedSet` at `container_identity.go:98-107` has no direct foreign-project regression. Add the requested case where a foreign project carries the exact pinned native name and service label, and prove the planned-set path rejects it without mutation. Existing canonical-label coverage does not establish this new code path.

### Finding 3 — retirement and control-plane stop still use the old identity contract

`internal/runtime/service_retirement.go:63` still checks `ContainerMatchesProjectResource` against `<project>-<service>-1`; `cmd/baha/control_plane_stop_observation.go:49` does the same. A pinned name such as `linkding-web` is rejected in both paths. The card explicitly puts the same identity contract on these paths in its Scope section (`tasks/t-20261108-bughunt-0427-container-name-replica.md`), and Acceptance requires `app down`, `up --yes`, and `destroy` to work with both identity classes. These paths therefore remain in this card's acceptance scope; there is no evidence-backed basis to move them to a follow-up card.

### Required runtime acceptance evidence

The task card requires a native Docker repository workload using `container_name` to complete `baha app backup` through READY to a written archive, plus the existing default-name case. Run `42440204879` skipped `Targeted HA · docker`, and round-2 records only package build/test results, not a post-fix native backup transcript. The code review also finds the production render interface mismatch above, so this acceptance item is not satisfied.

## Correction recipe

- `internal/runtime/container_identity.go:24-48`: make `RuntimeConfigProvider` match the real config method signature, including the `environment map[string]string` parameter, and pass the real workdir/environment to Compose rendering. Remove or correct the mock-only helper so its test double implements the exact production interface.
- `internal/runtime/service_stop.go:79-91,142`: use the same validated rendered planned-name set for initial selected-container validation and final process verification. Preserve project/service labels, fail closed when the required render cannot be obtained or parsed, and include service plus native name in the rejection message.
- `internal/runtime/service_retirement.go:21-64` and its owned call sites, plus `cmd/baha/control_plane_stop_observation.go:20-52`: thread the effective rendered per-service name set into retirement and control-plane observation, and match only the same project/service/planned native identity. Keep the card's stated ownership and destroy semantics.
- `internal/runtime/container_identity_test.go` and `internal/runtime/service_stop_test.go`: add a production-interface test for a pinned name flowing through `StopOwnedProjectServices`, a stopped-pinned postcondition test, and the exact cross-project pinned-name negative case. Add corresponding retirement/control-plane tests for pinned and default names. These tests are under `internal/runtime` and must run in the existing GitHub `go test ./internal/...` validation job on `pull_request` and every PR-head push; the current hosted `cli-guided-tests` run is green but its existing tests do not exercise the production render assertion.
- Native acceptance: execute the card's Docker backup flow for both pinned and default names on the designated Docker test host and retain the command/output proving READY-to-written-archive. Do not claim the skipped hosted HA cell as a pass.
- Stop criterion: production Compose and Podman implementations actually feed the rendered planned set; pinned and default names pass backup/quiesce, stop verification, retirement and control-plane ownership paths; a foreign project with the same pinned name is rejected; native Docker backup evidence and exact-head required CI are green. Until then, keep 0427-128 in review/correction, not accepted and not split to a follow-up.

## R2 evidence provenance

- Round-1 evidence was confirmed on planning `origin/main`: `100644 blob aae5ffdde15019d4777983cb497d68aef27597f1 evidence/r27-welle5-folge-2026-11-08/bughunt-container-name-replica/round-1.md`.
- Round-2 evidence was confirmed on planning `origin/main`: `100644 blob 87fbedbaca24c7616621dd60301d01edd0dccf80 evidence/r27-welle5-folge-2026-11-08/bughunt-container-name-replica/round-2.md`.
- The prior act is on planning `origin/main` as `100644 blob 589da8d6ce4986543478f8c446c7b23682893545 evidence/r27-welle5-folge-2026-11-08/bughunt-container-name-replica/act-1452-review.md` before this R2 append. Candidate SHA remained unchanged through the review; no product, workflow, branch or PR mutation was performed by this reviewer.

END_DONE integration-1452-review-r2: KORREKTUR; planned render interface is not implemented by production providers and retirement/control-plane paths still reject pinned names; candidate `978503376c34e447fc0f82451c35b43fb9fa8fd5`.

## R2 addendum — inventory and refreshed planning witnesses

A further production handoff confirms the set is not yet wired end-to-end: `cmd/baha/app_workload.go:653-659` still constructs the expected inventory as only `<project>-<service>-1` and passes that to `StopOwnedProjectServices`. `internal/runtime/compose_resources.go:114-128,167-170` indexes and inspects only the exact resource names in that inventory. Thus even after correcting the `RuntimeConfigProvider` method signature, pinned native names must be carried in the validated expected resource inventory or separately validated by project/service labels; otherwise resource inspection does not verify the pinned resource's ownership. Keep the current fail-closed project label check and never infer ownership from a matching native name alone.

The refreshed round-2 note remains format-only; its current Planning `origin/main` blob is `83cea2968c378db2a041892269a27a8a3be38253 evidence/r27-welle5-folge-2026-11-08/bughunt-container-name-replica/round-2.md`. The task card was also refreshed on `origin/main` and still explicitly lists `service_retirement.go:63` and `control_plane_stop_observation.go:49` in scope, and requires both `app down`, `up --yes` and `destroy` for both name classes. No follow-up split is warranted by the current contract.
