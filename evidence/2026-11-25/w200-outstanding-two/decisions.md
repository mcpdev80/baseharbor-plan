# Two outstanding disposition blocks

## PLAN

1. Reconcile #1850 head, Trusted Plan failure, catalog schema, runtime surfaces, and existing CI routing.
2. Decide carrier-first sequencing and the draft-toggle deviation without changing branches or cards.
3. Reconcile #1650 foreign commit ancestry and state the post-hop review condition.
4. Publish both local decision drafts and this evidence akte on baseharbor-plan origin/main; post END_DONE.

## Visible owner and commit ansatz

Fresh origin/main task frontmatter for 0428-307: `owner: ""` (empty string; unassigned).

Fresh origin/main task frontmatter for 0428-078: `owner: w165-0428-078-pr1650-basehop`.

Evidence commit identity: git user.name `w200-outstanding-two`; git user.email `w200-outstanding-two@baseharbor.local`.

Literal commit invocation: `git -c user.name='w200-outstanding-two' -c user.email='w200-outstanding-two@baseharbor.local' commit -m 'evidence: deliver outstanding 1850 and 1650 decisions'`.

Pre-push author gate: `git show -s --format=%an HEAD` must equal `w200-outstanding-two`.

## Base and remote attestation

Planning origin remote audit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.

Baseharbor audit remote: `origin https://github.com/mcpdev80/baseharbor.git (fetch)` and `(push)`.

Evidence worktree was created from exact baseharbor-plan origin/main SHA `4934f9ba4`; verify that SHA is an ancestor of the first evidence commit.

## Decision 1 — #1850 / 0428-307

Keep the existing card 0428-307 and PR #1850; create no card. The exact candidate head was `e4e3e050bed27fa696d604f205d0a4315b6938e7`, with canonical author/committer `w211-0428-307-fallback`.

Trusted Plan job `139433831371` in PR-event run `45678903831` failed on three uncataloged paths: `internal/application/runtime_identity_workload.go`, `internal/application/runtime_identity_workload_fallback_test.go`, and `internal/application/runtime_identity_workload_test.go`. `PR Selected Checks` job `139434058291` failed as the `UNIT_SCOPE` cascade (`REJECT: Go test selection missing or invalid`); the Go unit matrix was skipped. Prior same-head run `45677961079` had Trusted Plan and Selected Checks skipped and is void.

Add three exact path-derived catalog components, each with surfaces `source.gate.atomic.docker.lifecycle` and `source.gate.atomic.podman.lifecycle`, and `runtime_specific: true`:

```json
{"id":"source.internal_application_runtime_identity_workload_go","path":"internal/application/runtime_identity_workload.go","runtime_specific":true,"surfaces":["source.gate.atomic.docker.lifecycle","source.gate.atomic.podman.lifecycle"]}
{"id":"source.internal_application_runtime_identity_workload_fallback_test_go","path":"internal/application/runtime_identity_workload_fallback_test.go","runtime_specific":true,"surfaces":["source.gate.atomic.docker.lifecycle","source.gate.atomic.podman.lifecycle"]}
{"id":"source.internal_application_runtime_identity_workload_test_go","path":"internal/application/runtime_identity_workload_test.go","runtime_specific":true,"surfaces":["source.gate.atomic.docker.lifecycle","source.gate.atomic.podman.lifecycle"]}
```

Fresh Core origin/develop schema proof: `scripts/validate-pr-gate-coverage.py:29-45` matches exact component paths and resolves surfaces against gate coverage; `:46-60` removes a Podman sibling for shared components unless `runtime_specific: true`; `:75-84` constructs the diagnostic component IDs. Existing lifecycle component examples are `scripts/pr-gate-coverage.json:661-683`. Docker and Podman lifecycle gates cover `source.gate.atomic.docker.lifecycle` at `:2770-2781` and `source.gate.atomic.podman.lifecycle` at `:3213-3224`. The PR's candidate planner maps runtime identity implementation and fallback test to both lifecycle jobs at `scripts/pr-gate-plan.py:1541-1553`; extend that same explicit case to include `runtime_identity_workload_test.go`, which currently falls through to the unresolved generic application case. Package regressions run in `PR · Go unit · packages` on pull_request; selected native lifecycle coverage runs on both engines.

Carrier-first is required: Trusted Plan reads catalog policy from trusted develop, so #1850's own catalog changes cannot qualify the three changed source paths in that same run. Merge a catalog-only carrier PR to develop containing the three rows. Then normally merge current origin/develop into the existing #1850 branch and requalify the new exact head with Trusted Plan executed green, the package unit tests executed, Docker and Podman lifecycle gates executed green, and terminal PR Selected Checks green. Keep one card and one product PR.

#1850 was non-draft before implementation and gates were green, contrary to its mission. Record the process deviation; do not undo/ready-toggle. It does not make either prior run qualify. Leave the PR open for carrier and requalification.

## Decision 2 — #1650 / 0428-078

Content-neutrality by itself is insufficient. Proceed without a separate provenance release only when both exact commits `ed2fb751` and `f89f506f` are ancestors of the updated develop tip, so neither remains in `git log origin/develop..HEAD`. The develop-side carrier must preserve those exact commit SHAs; squash or cherry-pick transport does not establish ancestry. Then normally merge updated develop into the existing #1650 branch, verify develop ancestry and card-only diff, and require a fresh exact-head pull_request run with Trusted Plan and PR Selected Checks successful before SHA-exact review. If either foreign SHA remains visible in the base-to-head log, #1650 remains blocked.

## END

END w200-outstanding-two DONE — #1850 carrier-first surfaces and qualification order decided; #1650 is acceptable only after both exact foreign SHAs are in updated develop and the hopped exact head passes CI.
