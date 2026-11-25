# Bug-hunt H-V45: cmd/baha error-message and exit-code surface (read-only findings)

Lane: w186-0428-224-hunt-v45
Date: 2026-11-25
Slice: H-V45 (pure FINDING, no product changes, read-only)
Candidate SHA: n/a — read-only hunt; no branch, no product commits (see Anchor).

## PLAN

- Step 0: Numbered plan created in the todos board file (`workers/todos/w186-0428-224-hunt-v45.json`). No native `todowrite` tool is exposed in this session's toolset, so per dispatch rule the board file (a) is the visible and sufficient leg; Code-Mode was not used to hunt for the tool. This ## PLAN list is leg (b).
- Step 1: Anchor rule — ls-remote develop tip, fresh worktree at exact tip, base attestation.
- Step 2: Inventory the error surface (main.go exit paths, internal/cli, internal/machine, cmd/baha helpers).
- Step 3: Exit-code taxonomy consistency (where codes 0/1/2/7/130/143 and child passthroughs come from; what is documented).
- Step 4: Error-text leak classes (secrets in output/argv, runtime stderr echo, password buffers).
- Step 5: Actionable-resolution hints — standard or ad-hoc? (usageError discipline, Next-action coverage, doctor pattern).
- Step 6: Per-row findings + proposed card lines in this evidence directory.
- Step 7: Cleanliness (docker ps before/after, no state left).
- Step 8: Evidence push to baseharbor-plan origin/main, ls-tree witness, END post.

## Anchoring and remote witnesses

Planning repo verification (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`):

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Correct zone confirmed (not workers/baseharbor-plan).

Product repo remote resolution (`git remote -v` in `/home/marcel/dev/baseharbor-ecosystem/baseharbor`, FIRST git action):

```text
lane-origin	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
lane-origin	https://github.com/mcpdev80/baseharbor.git (push)
origin	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
origin	https://github.com/mcpdev80/baseharbor.git (push)
upstream	https://github.com/mcpdev80/baseharbor.git (fetch)
upstream	https://github.com/mcpdev80/baseharbor.git (push)
```

All three names resolve to the GitHub URL; `lane-origin` used for fetch/worktree.

Anchor rule — `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`:

```text
2a141387dbbaf24f52501a0f66f1abf61cf8fcda	refs/heads/develop
```

Base attestation: the hunt worktree `workers/w186-0428-224-hunt-v45-wt` was created detached at the exact tip (`git rev-parse HEAD` = `2a141387dbbaf24f52501a0f66f1abf61cf8fcda`, "HEAD is now at 2a141387d fix(0428-290): bind discovered metrics endpoints to workload sources (#1832)"). The tip SHA is trivially an ancestor of every finding claim because the hunt reads that exact tree and makes no commits.

Provenance witnesses (re-verified at END; tip unchanged):

```text
$ git merge-base --is-ancestor origin/develop HEAD
(ancestry OK: HEAD == origin/develop tip 2a141387d)
$ git diff origin/develop...HEAD --name-only
(empty — read-only hunt, zero product changes)
$ git log --oneline origin/develop..HEAD
(empty — no commits; therefore no foreign commits carried)
```

Method: scripted scans (Python) over all non-test Go files in `cmd/baha/` (445 files) and `internal/`, plus targeted reads of `cmd/baha/main.go`, `internal/cli/cli.go`, `internal/machine/contract.go`, and representative command files; augmented with `grep -n` per-row line verification.

## Findings

### F1 — The process exit-code taxonomy is undocumented at the user-facing surface

The code implements: 0 success, 1 runtime failure, 2 usage error (`internal/cli/cli.go:113-127`), 130 SIGINT (`cmd/baha/main.go:61-63`), 143 SIGTERM (`cmd/baha/main.go:83-86`), and arbitrary child-status passthrough 1-255 for `baha app exec` (`cmd/baha/app_exec.go:279` via `internal/cli/cli.go:122-125`). None of this is stated in the CLI reference: `docs/reference/cli.md` contains no "exit" section at all (grep: 0 hits), and `docs/reference/errors.md` covers only semantic outcome classes, never process exit codes (17 lines, no exit-code table). Scripts and agents cannot rely on a public contract, and the collision below (F3) is invisible.

Proposed card: "Document the baha exit-code taxonomy (0/1/2/130/143 + app exec passthrough) in docs/reference/cli.md and errors.md; add a machine-coverage check that the documented set matches cli.ExitCode behavior."

### F2 — The same auth failure class prints two different messages depending on entry point

- Non-JSON human path: `machine.Classify` maps an unclassified auth error to `ErrorAuthenticationFailed` with Next "Authenticate and retry." (`internal/machine/contract.go:128`), rendered as `Error` / `Resolution` / `What to do` blocks (`cmd/baha/main.go:251-271`).
- `--json` path with `BASEHARBOR_CI_INTEGRATION=1`: the process-wide synthetic operator prints to stderr `BaseHarbor machine operations require a verified operator session; set BAHA_TOKEN_FILE or run baha login for a remote Target` and exits 1 (`cmd/baha/ci_integration_operator_enabled.go:524-535`, message text at `ci_integration_operator_gate.go:16`).

The remediation vocabulary for authentication is already ad-hoc across files even in typed form: `Run 'baha login' for the selected Target/environment` (`cmd/baha/use_target.go:87`, `cmd/baha/operator_operations.go:45`), `Run the Core's first-owner onboarding or baha login, then retry.` (`cmd/baha/node_owner_context.go:26`), `Authenticate with the configured OIDC provider.` (`internal/operatorauth/authorization.go:206`), `Log in to the registered Core Target/environment.` (`cmd/baha/node_disconnect_client.go:29`).

Proposed card: "Define one canonical actionable hint per machine ErrorCode (starting with authentication_failed: name the concrete command, 'baha login <TARGET>'), route all auth-denial sites through it, and cover the invariant with a test in the CLI error-surface group."

### F3 — `baha app exec` child-status passthrough silently collides with the reserved codes 1 and 2

`cmd/baha/app_exec.go:279` returns `cli.WithExitCode(status.ExitStatus(), ...)`, and `cli.ExitCode` (`internal/cli/cli.go:122-125`) honors any child code 1-255. A workload command that itself exits 2 (a very common "usage error" convention) is indistinguishable, from the process exit status alone, from a baha flag parsing failure (code 2). The design comment in `cmd/baha/app_exec.go:266-270` explicitly claims the two classes are separated ("never maps to the usage exit code"), which holds only for baha's own failures, not for the passthrough. `baha app exec` is documented as excluded from the machine contract (`docs/reference/cli-machine-coverage.md:27`), so no typed disambiguation exists there either.

Proposed card: "Decide the app exec passthrough contract: either document the collision in cli.md (exit 2 may come from the child) or prefix machine-readable JSON output with a result envelope even for Presented failures; add a regression case for a child exiting with 2."

### F4 — `--json` failure rendering bypasses machine.Classify for the entire domain-error layer

`cmd/baha/main.go:65-68` calls `classifyMachineCLIError` (`main.go:300-376`), which hand-enumerates six sentinel errors (`main.go:308-364`) plus `appMachineError`, then falls through to `machine.Classify`. Every other typed domain error the CLI can return (e.g. the ~1198 plain `fmt.Errorf`/`errors.New` return sites in cmd/baha that wrap internal-package errors) reaches JSON rendering without any Code mapping beyond what `machine.Classify` recognizes. `machine.Classify` itself has no registry mapping — only apierror HTTP codes (`internal/machine/contract.go:117-132`) and stdlib sentinels — so a new typed internal error class silently lands in `internal_error` (`internal/machine/contract.go:152`) with exit code 1, no cause code and no Next.

Proposed card: "Add a central error-code registration (internal package sentinel → machine.ErrorCode) or a contract test that asserts every exported *Error/sentinel in internal/ classifies to a non-internal_error code from the CLI JSON surface."

### F5 — No secret redaction layer exists on the CLI error path

There is no redaction/scrub helper anywhere in `internal/cli`, `internal/machine` or `internal/apierror` (grep for `redact|scrub|mask` hits only unrelated payload masking, e.g. `internal/applicationinput/resolver.go:48`). Concrete leak classes found:

- Runtime stderr echo: compose failures embed raw `docker/podman compose` stderr into the user-facing error (`internal/runtime/compose_command.go:60-66` and `:90-96` `message = strings.TrimSpace(progress.String())` → `fmt.Errorf("compose %s: %s", ...)`), and the same pattern wraps `err.Error()` when stderr is empty. Docker Compose is known to echo `--env-file` variable content in some failure modes; there is no scrubbing anywhere between this string and `formatCLIErrorVerbose` (`cmd/baha/main.go:273`).
- `baha dev credentials` prints the plaintext password to **stdout** (`cmd/baha/dev_access.go:119`). Unlike `app export` — which zeroes its password buffer (`cmd/baha/app_export.go:200-203` with `zeroBytes` at `app_backup_restore.go:714-718`) and keeps secrets in entries it zeroes via `zeroExportEntries` (`app_export.go:195`) — the dev-access credentials struct holds the secret with no after-usage zeroing on the command path. The command is an explicit reveal seam (message at `dev_access.go:120`), so printing is by design; the missing zeroing is the hygiene gap versus the export path.
- Positive controls verified: `baha app connect` masks `PASSWORD`/`URI` unless the operator-authenticated reveal seam passes (`cmd/baha/app_access.go:131-144`), JSON mode never reveals (`app_access.go:120-121`); `baha app export` reports only "local credentials" wording with values encrypted to a file (`cmd/baha/app_export.go:212-225`); `provider_external.go` prints only `CredentialRef` references (`:91`, `:158`, `:587`).

Proposed card: "Introduce a shared secret-scrub on user-facing error strings built from external runtime output (at minimum the compose stderr capture path in internal/runtime/compose_command.go), and zero credential buffers after rendering in cmd/baha/dev_access.go; add a leak-detection test that runs failing-compose and reveal paths against a poisoned secret value."

### F6 — Exit 0 on `baha <garbage>` when the root command has a Run func

`internal/cli/cli.go:150-159`: an unknown subcommand produces a UsageError (exit 2) only `if len(c.Children) > 0 && c.Run == nil`; otherwise (`cli.go:160-162`) the parent Run is invoked with the garbage args. If the root command tree ever gains a root Run func, typos like `baha statup` would silently execute the default action instead of failing with 2. Today this is latent-hardening, not a live defect (root has children and no Run) — recorded so a future root Run does not regress the "unknown command" guarantee. The flag-suggestion mechanism has the same one-sidedness: command suggestions exist for unknown commands (`cli.go:152-154`) and flag suggestions for unknown flags (`cli.go:207-238`), but an unknown **sub-subcommand of a runnable parent** gets neither.

Proposed card: "Add a cli.Execute regression test asserting exit 2 + suggestion for unknown commands under a runnable parent (or forbid root Run + children combination statically)."

### F7 — Nine typed conflict/ownership errors ship no `Next` action at all

`machine.Error` literals without a `Next:` field (scripted scan of all `cmd/baha/*.go` + `internal/**/*.go`, non-test; 102 literals checked):

| file | line | code | cause |
| --- | --- | --- | --- |
| cmd/baha/control_plane_destroy.go | 145 | ErrorConflict | control_plane_destroy_partial |
| cmd/baha/control_plane_stop.go | 89 | ErrorConflict | control_plane_stop_partial |
| cmd/baha/node_disconnect_lifecycle.go | 89 | ErrorConflict | node_disconnect_partial |
| cmd/baha/node_disconnect_client.go | 216 | ErrorConflict | (no cause code) |
| cmd/baha/target_definition_change.go | 159 | ErrorConflict | target_definition_change_partial |
| cmd/baha/application_stop_impact.go | 172 | ErrorConflict | application_stop_partial |
| cmd/baha/target_definition_change_plan.go | 85 | ErrorOwnershipAmbiguous | target_definition_tenant_owner_unverifiable |
| cmd/baha/runtime_explorer_authority.go | 54 | ErrorConflict | runtime_mutation_partial |
| cmd/baha/provider_external_removal.go | 88 | ErrorOwnershipAmbiguous | provider_consumer_authority_unverifiable |

All are "partial completion" states — precisely the class where an operator most needs the next step (the sibling partial messages elsewhere do carry Next, e.g. `cmd/baha/app_machine_adapters.go:50-52`). Note `node_disconnect_client.go:216` additionally drops the CauseCode while its lifecycle twin keeps one.

Proposed card: "Add concrete Next actions (inspect X, re-run Y with flag Z) to the nine partial-completion/ownership errors above; add a lint or test requiring Next to be non-empty for ErrorConflict/ErrorOwnershipAmbiguous machine.Error literals."

### F8 — The remediation-class vocabulary is undeclared and mixes styles

All observed values (`grep Remediation:` over non-test Go): `requires developer input` (18), `operator_review` (17, snake_case), `requires operator approval` (7), `manual/admin action required` (6), `runtime provider implementation required` (2), `manual action required` (2), `requires operator action` (1), `requires host capacity` (1), plus three free-sentence values (`authenticate the BaseHarbor operator`, `initialize the application workspace source model`, `map the existing local repository/worktree for the declared source identity` — `cmd/baha/main.go:313,323`, `cmd/baha/mcp.go:333`, `cmd/baha/application_provider_plan.go:146`). `docs/reference/errors.md` never enumerates these classes, so neither casing nor set is contractually fixed; consumers cannot switch on them.

Proposed card: "Declare the remediation-class enum in docs/reference/errors.md (and the machine schema if JSON consumers exist), normalize operator_review → a style-consistent value, and map free-sentence Remediation sites to the enum while moving their sentences to Next."

### F9 — Hints themselves can be empty after trim, and are then silently dropped at render

- `usageError` discipline is strong: 613 call sites scanned, none single-arg, none with a literal empty hint.
- The render path skips hints that are whitespace-only (`cmd/baha/main.go:276` guards `strings.TrimSpace(usage.Hint) != ""`), so a hint composed only from variables can vanish at the user's terminal.
- `unknownOptionUsage` (`cmd/baha/ux.go:54-59`) always has a fallback hint — good — but the cli-package fallbacks at `internal/cli/cli.go:151-153` and `cli.go:178-181` (unknown command) are the ad-hoc twin of it: same "Did you mean … / Run --help" construction duplicated rather than shared, and `SuggestClosest` (`internal/cli/cli.go:431-445`, threshold ≤2) vs `Command.suggest` (`cli.go:447-471`, same logic re-implemented) can diverge on candidate ordering.
- The doctor "Next:" block (`cmd/baha/doctor.go:95-102`) prints bare commands (`baha doctor --fix`) while typed errors print prose-plus-command (`cmd/baha/main.go:263-265`); two hint idioms coexist.

Proposed card: "Centralize hint construction (one helper used by cli.Execute, ux.unknownOptionUsage and the doctor renderer) and add a unit test that a trimmed-empty Hint never occurs on any UsageError reaching main's renderer (e.g. by making usageError itself reject blank hints)."

### F10 — Positive control: PresentedError double-render guard is consistent; flag-name leak verified inert

- All 20 `cli.Presented(...)` sites (`doctor.go:102,140,166,200`; `app_doctor_repair.go:96`; `app_observe.go:260,350,378,397`; `app_commands.go:409,434`; `policy.go:45`; `management_remote_apply_cli.go:236`; `management_remote_destroy_cli.go:127,133,144`; `app_exec.go:279`) are immediately preceded by rendering their findings to `out`, and `main.go:248` correctly suppresses the generic block for them, so the human surface never shows "Error" twice for those paths; the JSON branch keeps the envelope instead (`main.go:65-68`) — the dual-surface contract holds.
- `unknown workload component <answer>` (`cmd/baha/app_interact.go:153`) interpolates the raw user answer; checked for injection-into-terminal risk: the value is only ever the component selector argument echoed once with the message — low severity note, not a leak.
- The `--baseharbor-hosts-write` hidden helper prints a bare error and exits 1 (`cmd/baha/main.go:31-48`) — internal plumbing, intentionally not on the taxonomy path; noted for completeness.

## Counts

- Findings: 10 (F1-F10; F10 is positive-control/hardening notes).
- Defect-grade rows needing cards: F1, F2, F3, F4, F5, F6, F7, F8, F9 (9 proposed card lines above).

## cleanliness

- No containers, networks, volumes or state directories were created by this lane (read-only hunt; no compose projects started).
- `docker ps -a` before (pid 1172229): header only, zero rows.
- `docker ps -a` after (pid 1200773, END verification):

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS   NAMES
```

- cleanliness: besenrein — no test-owned container/network/volume/state left on this host; worktree `workers/w186-0428-224-hunt-v45-wt` removed by the coordinator's standard lane cleanup.

## repo-rule compliance

- Read-only mission: no product-repo commits, no pushes to baseharbor, no PR (candidate = the develop tip itself).
- Tests: none run (pure static hunt); no CI triggered; no .github/** touched.
- Evidence lives only in baseharbor-plan (`evidence/r28-welle6-2026-11-27/bughunt-hv45-cli-errors/hunt-1.md`); written with lane identity `w186-0428-224-hunt-v45`.
- No subagents used; all steps executed in this session.
- No markdown checkboxes in this file (verified at write time).

## Evidence-on-origin witness

(filled as second-to-last action; see below)

END w186-0428-224-hunt-v45 DONE — 9 actionable findings (F1-F9) + 1 positive-control row (F10); candidate SHA n/a (read-only hunt anchored at develop 2a141387dbbaf24f52501a0f66f1abf61cf8fcda).
