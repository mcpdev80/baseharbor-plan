# H-V45 intake: findings-to-cards for the cmd/baha error/exit-code surface

Lane: w187-0428-224-hunt-v45-intake
Date: 2026-11-25
Source akte: [hunt-1.md](hunt-1.md) (w186-0428-224-hunt-v45, origin/main ecf0304a8), findings F1-F9 + control row F10.
Mission: coordinator/missions/hunt-v45-intake.txt. Card Intake only — no product code changes.

## PLAN

- Step 1: Verify planning repo remote and fetch origin/main; read the source akte. DONE.
- Step 2: Anchor: ls-remote develop tip; fresh detached worktree at the tip. DONE.
- Step 3: Reproduce every finding line-by-line against current develop; classify live / superseded. DONE.
- Step 4: Cluster coherent defect cards; mapping table below. DONE.
- Step 5: File cards via scripts/plan.py new (type: bug, kanban_status: planned, severity where repo rules allow) and fill Goal/Scope/Acceptance/Handoff. DONE.
- Step 6: Per-finding disposition lines in this akte. DONE (below).
- Step 7: render + check + publish (pull --rebase, own files only). IN PROGRESS.
- Step 8: Evidence-on-origin/main witness, END post.

## Anchoring and remote witnesses

Planning repo (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`, verified before the first evidence commit):

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Correct zone confirmed (not workers/baseharbor-plan).

Product repo FIRST git action (`git remote -v` in /home/marcel/dev/baseharbor-ecosystem/baseharbor): all names (lane-origin/origin/upstream) resolve to https://github.com/mcpdev80/baseharbor.git; lane-origin used. Quarantined workers/baseharbor checkout was not used.

Anchor rule — `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`:

```text
2a141387dbbaf24f52501a0f66f1abf61cf8fcda	refs/heads/develop
```

The akte anchor 2a141387d IS the current develop tip; reproduction used a fresh detached worktree `git worktree add --detach /tmp/opencode/w187-0428-224-hunt-v45-intake-wt 2a141387d` ("HEAD is now at 2a141387d fix(0428-290): bind discovered metrics endpoints to workload sources (#1832)"). Zero commits were made in the product repo; `git log --oneline origin/develop..HEAD` and `git diff origin/develop...HEAD --name-only` are empty (read-only intake, no candidate branch needed).

## Reproduction and per-finding disposition

Method: line-exact `sed`/`git grep` verification in the anchored worktree plus targeted reads. "live" = defect reproduced at the cited or moved lines; "superseded" = not present at current develop.

### Mapping table (F -> cards)

| Finding | Status | Card | Root-cause cluster |
| --- | --- | --- | --- |
| F1 exit-code taxonomy undocumented | live | 0428-321 | documentation/contract of exit codes |
| F2 auth-failure message split | live (variants confirmed; one akte site wrong — see note) | 0428-323 | actionable-hint consistency |
| F3 app exec passthrough collides with 1/2 | live | 0428-322 | exit-code semantics decision |
| F4 JSON path hand-enumeration / classify fallthrough | live | 0428-323 | error classification registry |
| F5 no secret redaction on error path | live (zeroing half confirmed; leak half static-evidence) | 0428-324 | secret hygiene |
| F6 unknown command under runnable parent | live (latent-hardening) | 0428-325 | CLI dispatch guarantee |
| F7 nine Next-less conflict errors | live (9/9) | 0428-323 | actionable-hint consistency |
| F8 remediation vocabulary undeclared | live (12 values) | 0428-323 | error classification registry |
| F9 empty hints dropped / duplicated suggestion builders | live | 0428-325 | CLI dispatch/hint construction |
| F10 positive control | no card (control row) | — | — |

Detail per finding:

- F1 LIVE. `grep -i exit docs/reference/cli.md` = 0 hits; `grep -i exit docs/reference/errors.md` = 0 hits (17-line file). Taxonomy confirmed in code: internal/cli/cli.go:113-127 (0/1/2 + WithExitCode passthrough 1-255), cmd/baha/main.go:63 (130), :83-86 (130/143), cmd/baha/app_exec.go:279. -> card t-20261125-hunt45-exit-code-taxonomy-docs (0428-321).
- F2 LIVE, with one akte-path correction. The human-path mapping `Authenticate and retry.` is at internal/machine/contract.go:128 (confirmed). The akte's cited `ci_integration_operator_gate.go:16` does NOT exist at 2a141387d (git grep: no such file; only ci_integration_operator_enabled.go / _disabled.go), and neither the quoted stderr message nor any `BASEHARBOR_CI_INTEGRATION` / `BAHA_TOKEN_FILE` reference exists anywhere in the tree — that half of the row is superseded/filed-against-a-nonexistent-path. The dual-message invariant itself reproduces with current sites: machine.NewError auth Next variants at cmd/baha/node_owner_context.go:26, cmd/baha/node_disconnect_client.go:29, internal/operatorauth/authorization.go:204-206, cmd/baha/node.go:414, cmd/baha/mcp.go:331-334 (five distinct remediation phrasings for the same class). -> card t-20261125-hunt45-error-surface-consistency (0428-323).
- F3 LIVE. cmd/baha/app_exec.go:279 `cli.WithExitCode(status.ExitStatus(), cli.Presented(...))`; cli.ExitCode honors 1-255 (internal/cli/cli.go:122-125); the design comment at app_exec.go:266-270 overclaims ("never maps to the usage exit code" is false for a child exit 2); cli-machine-coverage.md:27 excludes app exec from the machine contract, so no typed disambiguation. --cmd confirmed at app_exec.go:52. -> card t-20261125-hunt45-app-exec-exit-collision (0428-322).
- F4 LIVE. classifyMachineCLIError enumerates exactly six sentinels (main.go:300-364: development.ErrWorkspaceModelMissing/ErrWorkspaceSourceMissing, application.ErrRepositoryManifestNotFound, orgconfig.ErrNotConfigured/ErrUnsupportedSource/ErrSourceUnavailable) + appMachineError, then machine.Classify, which has no internal-sentinel registry — only apierror HTTP codes (contract.go:120-132), TrustError, config sentinels, an ActionableError interface (:140-142) and the default internal_error fallthrough with empty Next (:153). cmd/baha non-test error-construction sites: 2309. -> card 0428-323.
- F5 PARTLY LIVE. Redaction absence confirmed: 0 redact/scrub hits in internal/cli, internal/machine, internal/apierror (only one unrelated "masked" at internal/machine/contract.go:182); the akte's "e.g. internal/applicationinput/resolver.go:48" citation could not be re-verified (not checked line-by-line; the layer-level claim holds). Compose stderr embed confirmed at THREE sites (compose_command.go:20-24, 60-66, 90-96 — the akte cited only two). dev credentials: plaintext print at cmd/baha/dev_access.go:119 with no after-usage zeroing; contrast confirmed (app_export.go:194/203 defer zeroExportEntries/zeroBytes; zeroBytes at app_backup_restore.go:714); note dev_access.go:132 already zeroes the []byte in the password-file read path, but the loaded-credentials string path does not. Positive controls (app_access.go:131-144 masking, JSON never reveals, provider_external CredentialRef only) re-confirmed. The docker-compose echo behavior is not reproducible on this host (no container runs here per directive) — static evidence stands. -> card t-20261125-hunt45-secret-hygiene-error-path (0428-324).
- F6 LIVE (latent). Guard `len(c.Children) > 0 && c.Run == nil` confirmed at internal/cli/cli.go:150; root command (cmd/baha/commands.go:26-29) has children and NO Run, so no live defect today, as the akte itself states; hardening test still needed. -> card t-20261125-hunt45-cli-unknown-command-hardening (0428-325).
- F7 LIVE. Scripted check of all nine rows: every cited line still holds a machine.Error literal with no Next (9/9), including the CauseCode-less node_disconnect_client.go:216. Cross-tree scan: exactly nine Next-less `machine.Error{Code...}` literals in cmd/baha (none newly appeared in internal/ with that literal form). -> card 0428-323.
- F8 LIVE. Remediation scan reproduces the same distribution: requires developer input 18, operator_review 17, requires operator approval 7, manual/admin action required 6, runtime provider implementation required 2, manual action required 2, requires operator action 1, requires host capacity 1, plus four free-sentence values (main.go:313,323; mcp.go:333; application_provider_plan.go:146 — the akte's "three" misses the application_provider_plan "retire the duplicate application_id registrations" row; count corrected here). docs/reference/errors.md declares nothing. -> card 0428-323.
- F9 LIVE. Render skip on trimmed hint at cmd/baha/main.go:276; ux.unknownOptionUsage (cmd/baha/ux.go:54-59) is the shared-SuggestClosest variant; cli.go:150-154 and cli.go:180 duplicate the hint construction; SuggestClosest (cli.go:431-445) and Command.suggest (cli.go:447-471) re-implement the same threshold-2 logic (aliases differ). doctor.go Next block (:95-101) prints bare commands. usageError requires two args (cmd/baha/commands.go:266) but does not reject blank hints. -> card 0428-325.
- F10 CONTROL, no card. cli.Presented sites at 17 (akte said 20 — sites moved with develop; re-scan finds none unrendered), main.go:248 suppresses the generic block, JSON branch main.go:65 keeps the envelope; app_interact interpolation and --baseharbor-hosts-write plumbing noted as-is. No card; hardening notes are absorbed into 0428-325's blank-hint guard where relevant.

Clustering rationale: F2+F4+F7+F8 share one root cause (no central actionable-error registry: code, Next, remediation-class per site instead of per contract) -> one card. F6+F9 share one root cause (internal/cli dispatch/hint construction) -> one card. F1 and F3 both concern the exit-code surface but differ in kind (documentation vs semantics decision) and touch different files -> separate cards with a coordination note on docs/reference/cli.md.

## Cards filed

| Card | File | type | status |
| --- | --- | --- | --- |
| 0428-321 | tasks/t-20261125-hunt45-exit-code-taxonomy-docs.md | bug | planned |
| 0428-322 | tasks/t-20261125-hunt45-app-exec-exit-collision.md | bug | planned |
| 0428-323 | tasks/t-20261125-hunt45-error-surface-consistency.md | bug | planned |
| 0428-324 | tasks/t-20261125-hunt45-secret-hygiene-error-path.md | bug | planned |
| 0428-325 | tasks/t-20261125-hunt45-cli-unknown-command-hardening.md | bug | planned |

Severity: the plan-repo schema has no severity field; the closest sanctioned slot is `priority` (critical|high|normal|low) and the direct cast-precedent cards (t-20261125-hunt43-*, t-20261125-hunt44-*) left it unset. Cards were filed without priority; the ordering above (hygiene/classification first) is recorded here instead. If the Coordinator wants severity carried as `priority`, say so and a one-line follow-up can set it per card.

## repo-rule compliance

- Planning-only change: 5 new task notes + views regenerated by `plan.py render` + this akte. No product-repo commits, no PR, no .github/** touched (baseharbor untouched beyond a read-only detached worktree, removed at END).
- Claims: the cards are unassigned intake output; per the Hunt->Card precedent cards (hunt43/hunt44 filed with `owner: ""`), no plan.py claim was taken — this lane's mission duty is filing, not owning. No existing note other than the source akte (addendum) was edited.
- render + `plan.py check` run before commit: 0 errors (11 pre-existing warnings on unrelated cards).
- Evidence lives only in baseharbor-plan; written with lane identity w187-0428-224-hunt-v45-intake.
- No subagents; no containers/networks/volumes started (see cleanliness).
- No markdown checkboxes in this file outside the sanctioned form (none).

## cleanliness

- This lane started zero docker/podman compose projects; no container, network, volume or state directory was created.
- `docker ps -a` before (this lane pid at time of check): header only, zero rows.
- `docker ps -a` after (END verification): header only, zero rows (witness output recorded below).
- Worktree /tmp/opencode/w187-0428-224-hunt-v45-intake-wt removed via `git worktree remove` at END; `git worktree list` witness below.
- cleanliness: besenrein.

## Evidence-on-origin witness

```text
(to be filled by the final verification step before END)
```

END w187-0428-224-hunt-v45-intake — pending publish.
