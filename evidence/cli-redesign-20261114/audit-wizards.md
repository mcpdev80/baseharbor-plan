# Audit: wizard / steered CLI paths (source, target, platform) — IST-ZUSTAND

Card: `t-20261114-r28-cli2-audit-wizards` (0428-048)
Lane: `lane-0428-wizards`
Type: pure inventory / IST-ZUSTAND (merge-frost, owner directive 2026-11-14).
No product change, no PR, no release, no tag. Write right is `baseharbor-plan` only.

Inputs (this lane, fetched from `origin/main`):
- brief: `evidence/cli-redesign-20261114/brief.md`
- command map: `evidence/cli-redesign-20261114/command-map.md`
- static code-entry index: `evidence/cli-redesign-20261114/code-entry-index.md`
- companion interface audit (this group): `evidence/cli-redesign-20261114/audit-interface.md`
- BaseHarbor plan `t-20261114-r28-cli2-contract` (the implementation owner of every proposed name below).

Scope: the *smallest guided workflow* (brief line 7) as it currently exists on `develop` — every
interactive/steered wizard and every place the CLI guides the operator instead of taking a plain
argument. Branches covered: **source / app** (`app new`, `app init`, `app workspace`), **target**
(`new target`, `target activate`, target deployment policy), **platform** (`new provider`,
`stack`, `config prompt`), plus the root `new` chooser, the `access` wizard and the onboarding wizard.
Verdicts per item: `trifft` / `weicht ab` / `Konsistenz-Risiko`.

## PLAN

- Read mission, brief, command-map, code-entry-index.
- Pin product base: `develop` = `0e9ccb582` (witness below) in a persistent clone in this lane's zone.
- Inventory wizard/steered paths per branch, each with `file:line` at `0e9ccb582`.
- Judge each item against Core `AGENTS.md`, `docs/DEVELOPMENT_GUIDELINES.md` and the owner brief.
- Cite external norms (clig.dev, Model Context Protocol elicitation) via context7 MCP / web search.
- Write this dossier to `evidence/cli-redesign-20261114/audit-wizards.md`, push to plan `origin/main`,
  post END to the lane.

## 0. Zone and provenance witnesses

Wrong-zone guard (mandated one-liner):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```

`workers/baseharbor-plan` was never touched. The quarantined `workers/baseharbor` checkout was never
cited: all product truth comes from `git ls-remote` on GitHub and from a fresh clone in this lane's own
zone (`/tmp/opencode/wizards-audit-wt/core`).

Base attestation:

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote origin develop
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
$ git -C /tmp/opencode/wizards-audit-wt/core rev-parse HEAD
0e9ccb582f5bdcdc74049bbe3996263cdce6500c
$ git -C /tmp/opencode/wizards-audit-wt/core merge-base --is-ancestor 0e9ccb582 HEAD; echo $?
0
```

The audited snapshot is exactly `origin/develop` at `0e9ccb582`
("chore: pin v0.4.27 demo acceptance (#1573)"). Clone method:
`git clone --no-checkout --filter=blob:none https://github.com/mcpdev80/baseharbor.git` then
`git checkout 0e9ccb582f5bdcdc74049bbe3996263cdce6500c` in `/tmp/opencode/wizards-audit-wt/core`.
The clone detaches at that SHA, so the ancestry test is trivially satisfied; no branch was cut and no
PR was opened, per merge-frost. Every `file:line` reference below was read from that snapshot and is
reproducible with `git show 0e9ccb582:<path>`. The card `t-20261114-r28-cli2-audit-wizards` was
already published `active` with an owner by the coordinator (`plan origin/main 6ad3edaa`), so the claim
requirement is satisfied by the published state; `python3 scripts/plan.py claim` refuses to re-claim an
active card, so nothing was re-published.

## 1. Reference sources used

- Command Line Interface Guidelines, "Interactivity" and "Errors": prompt only when stdin is a TTY;
  `--no-input` must never prompt and must fail with an actionable message telling the user which flag to
  pass; blank/missing input offers a task-specific wizard, arrows/Enter and Tab where appropriate;
  cancellation preserves state. <https://clig.dev> (retrieved 2026-11-14 via web search).
- Model Context Protocol 2026-07-28, client elicitation and Multi Round-Trip Requests (SEP-2322 /
  SEP-2260): a server may ask the client for input only while processing a request and MUST handle a
  decline/cancel or a client that cannot interact.
  <https://github.com/modelcontextprotocol/modelcontextprotocol> (`docs/specification/2026-07-28/client/elicitation.mdx`,
  `docs/seps/2322-MRTR.mdx`), retrieved 2026-11-14 through the context7 MCP server
  (`/modelcontextprotocol/modelcontextprotocol`).
- Bubble Tea v2 (`charm.land/bubbletea/v2 v2.0.9` + `charm.land/lipgloss/v2 v2.0.6`), already a
  terminal-input-capable dependency the raw line editors could reuse; the CLI currently reads raw lines,
  not a TUI, so there is no arrow/Tab key handling in the wizards.
- Internal contracts used as the judgment basis: Core `AGENTS.md` "Work and verify"
  ("Mutations follow plan -> preflight -> apply -> verify; CLI, JSON and MCP share domain semantics.
  Preserve ownership, concrete consequence/consent checks and secret protection.") and
  `docs/DEVELOPMENT_GUIDELINES.md` §3 (contracts, not products), §6 (secrets never enter normal data
  paths), §7 (one authoritative source of truth), §8 (one lifecycle), §9 (CLI/JSON/MCP share one
  semantic core), §10 (tests prove invariants).

## 2. Wizard architecture (shared contract)

The wizards are not ad-hoc prompts; they share a single read-only-controller discipline that the brief
demands ("no interactive dead ends", "cancellation preserves state", "protected operations follow
plan -> preflight -> apply -> verify").

- The application wizard is a pure navigation state machine with **no mutation hook**.
  `cmd/baha/app_wizard_controller.go:16-60` declares `appWizardPhase` (`needs` / `providers` /
  `preview` / `decided` / `aborted`) and `appWizardEvent` (`next`/`back`/`cancel`/`eof`/`yes`/`no`);
  the controller struct explicitly states in comments it "contains no filesystem, process or domain
  mutation hook" (`:62-75`) and returns only an immutable `appWizardDecision` intent (`:173-180`).
- It opens only when a TTY is present and never in `--no-input` mode: `newAppWizardController` returns
  `errAppWizardNonInteractive` when `!input.TTY || input.NoInput` (`app_wizard_controller.go:81-83`).
  This is **constructional**, not discplinary — the brief's "`--no-input` and scripts never block"
  requirement is met at the controller entry for the whole app wizard.
- It never executes a decision: `Step`/`SelectNeed`/`SelectProvider` all return navigation state and
  "never invokes a mutation or consent hook" (`app_wizard_controller.go:257-258, 327-328`). The caller
  (`app_new_wizard.go:183-199`) acquires `lockApplicationTargetLifecycle` and asks for a separate
  confirmation before the controller reaches `decided`; the controller's `decided` phase additionally
  rejects a stale preview by re-reading read-only authorities and comparing a JSON snapshot
  (`app_wizard_controller.go:302-318`). This is exactly the plan -> preflight -> apply -> verify split.
- Cancellation is state-preserving: `appNewAbortOnEOF` prints "No changes were made" and never writes
  (`app_new_wizard.go:292-301`); the loop treats EOF as cancel, never as approve (`app_new_wizard.go:167-171`).

Verdict for 2: `trifft`. The wizard skeleton matches the brief's guided-workflow contract by
construction (TTY gate, no mutation hook, snapshot-verified preview, state-preserving cancel). The
residual risk is that this discipline is enforced for the **app** wizard by the shared controller, but
the source/target/platform wizards below are independent line-read loops and re-derive the discipline
per file.

## 3. Source / app branch (app new, app init, app workspace)

### 3.1 `baha app new` — guided greenfield
Witnesses (`cmd/baha/app_new_wizard.go`, `cmd/baha/human_new.go`, `cmd/baha/application_provider_preferences.go`):

- Root chooser `baha new` prints a 1-5 menu and dispatches to the domain flow: `cmd/baha/human_new.go:30-51`;
  `runHumanNewSelection` maps `application` -> `appNewCommand`, `target` -> `guidedNewLocalTarget`,
  `provider` -> `guidedCreateProvider`, `workspace` -> `appWorkspaceCommand` (`human_new.go:55-73`).
  Non-interactive it refuses with an explicit creation-type error (`human_new.go:27-28`).
- The wizard steps: name (`promptLine`, `app_new_wizard.go:49`) -> slug normalization that rejects
  navigation words as names (`normalizeAppNewWizardName`, `:229-243`) -> project location (current dir
  default, else home-rooted `promptDirectoryPathFrom` with Tab completion on Linux, `:391-459`) ->
  stack profile (organization default or numbered menu, `guidedStackProfile`, `:469-503`, with a
  "create new" branch `guidedCreateStackProfile`, `:505-607`) -> guided capability placement
  (`guidedCapabilityPlacement`, `:609-658`) -> the shared `app_wizard_controller` needs/provider/preview
  loop (`runAppNewWizard`, `:35-225`).
- Source identity: `baha new`/`app new` resolve the root to a directory and never scan a neighbouring
  repo; the chosen name is required before any filesystem mutation (`:53-61`).

Contract check vs brief:
- "Current directory as project default; other directory path guidance starts at home with shell Tab
  support" (`brief` line 9). `guidedNewApplicationRoot` defaults to `os.Getwd()` (`app_new_wizard.go:391-392`),
  falls back to `os.UserHomeDir()` (`:406-409`), and on Linux offers `promptPathWithCompletionBase`
  (`cmd/baha/path_prompt_linux.go:27-58`, raw-termios line completion). **Trifft.**
- "Components are optional and unique per app ... multiple per source". `guidedStackProfile` rejects
  duplicate component ids with a numeric suffix and enforces "at least one component"
  (`app_new_wizard.go:553-583`). **Trifft.**
- "Setup completion once persists; active context is per terminal only". The wizard sets nothing about a
  persisted completion state; `--no-input` is the only persistence-free switch. See item 5.

Verdict: `trifft`, with one small drift on identity (3.3).

### 3.2 `baha app init` — guided brownfield adopt
Witnesses (`cmd/baha/app_init_wizard.go`, `cmd/baha/app_runtime_init.go` via code-entry index):

- `appGuidedInitCommand` guards non-interactive with no argument: `noInput(ctx) && len(args) == 0` ->
  usage error pointing at `--quick` or the deterministic flags (`app_init_wizard.go:81-83`). `--quick`
  accepts unambiguous detections and safe defaults without any prompt (`:84-113`).
- A terminal runs `runAppInitWizard` which prints the detection summary, asks only about missing/ambiguous
  signals (`collectGuidedInitSelection`, `buildGuidedInitManifest`), then confirms `Write baseharbor.yaml?`
  (`app_init_wizard.go:123-190`).
- Secret names found from env files are treated as "heuristic evidence only" and never promoted to
  required contract entries without explicit confirmation in quick mode (`manifestFromDetectedProject`,
  `app_init_wizard.go:228-238`).

Contract check vs brief:
- "greenfield and `init` brownfield; no separate human config-only create path, but preserve underlying
  domain/MCP operation" (`brief` line 10). The `--quick` non-interactive path preserves the deterministic
  manifest generator for CI/scripts; the wizard delegates the final write through the production
  `authorizeMCPOperation(ctx, "app.adopt", ...)` (`app_init_wizard.go:166`). **Trifft.**
- "no accidental neighbouring-repo scan". Detection runs on `"."` only (`detectAppProject(".")`,
  `app_init_wizard.go:101`). **Trifft.**

Verdict: `trifft`.

### 3.3 `baha app workspace` — guided source/component mapping
Witnesses (`cmd/baha/app_workspace_wizard.go`):

- `runAppWorkspaceWizard` resolves the manifest, authorizes `workspace.init`, detects local repo/worktree
  candidates from the manifest dir and its parent (`detectedWorkspaceCandidates`, `app_workspace_wizard.go:272-300`),
  then loops per-component: component name -> `guidedWorkspaceSource` (reuse existing / new local / OCI) ->
  "Add another component?" -> validate -> confirm `Write workspace configuration?` (`:19-126`).
- `guidedWorkspaceSource` reads the checkout's `remote.origin.url` and current branch as the portable
  identity and rejects an empty repository identity ("the local filesystem path is intentionally not
  portable identity"), `app_workspace_wizard.go:207-215`.

Contract check vs brief:
- "App source is a Git repo ... local directory or supported OCI source; components are optional and unique
  per app ... pull impacts the entire Git repo, with preview of shared impacts. No accidental
  neighbouring-repo scan." (`brief` line 9). Detection is scoped to the manifest dir + one parent level
  (`:272-300`); the identity is the repository URL, not the path. **Trifft** for source guidance.
- "No accidental neighbouring-repo scan" — the one-parent scan is a minor widening beyond the manifest dir
  but is bounded and documented. Low risk.

Verdict: `trifft`.

### 3.4 Identity drift: `app.id` is generated, not committed (Konsistenz-Risiko)
Witnesses (`cmd/baha/app.go`, `cmd/baha/app_commands.go`, `cmd/baha/app_init_wizard.go`):

- `app.go:115` documents that "the authored source deliberately omits the system-owned ApplicationID"; the
  creation write zeroes `m.ApplicationID` (`app.go:256`, `app_commands.go:47`) so the versioned
  `baseharbor.yaml` carries name + environment only.
- The brief explicitly requests the contrary ("nonsecret `app.id` committed in versioned `baseharbor.yaml`
  and generated at new/init, reused by another checkout/Core, no manual UUID request; preserve historical ID
  and reject conflicts", `brief` line 14) and flags it as "must be versioned/migrated, coordinated with
  Core and Git authority" (`brief` line 14).

Verdict: **weicht ab** by design. Current behaviour is the opposite of the proposed destination; the brief
lists it as an unresolved decision to be resolved via the contract task (`t-20261114-r28-cli2-contract`),
not as a defect. The wizard already preserves a generated ID internally (`app_init_wizard.go`
`MustNewApplicationID` detection), but does not persist it — consistent with today's contract, divergent
from the proposal.

## 4. Target branch (`new target`, `target activate`, deployment policy)

### 4.1 `baha new target` — guided local target
Witnesses (`cmd/baha/human_new.go`, `cmd/baha/target_definition_change.go`):

- `runGuidedNewLocalTarget` reads name -> runtime (docker/podman) -> scope -> "make the default?" through a
  bounded step list with per-field validation and a `back`/`cancel` escape (`guidedNewLocalTargetWithInput`,
  `human_new.go:85-174`). Non-interactive it refuses with an explicit runtime-provider command hint
  (`human_new.go:79-81`).
- Confirmation and then the deployment-policy wizard feed into the deterministic `createTarget`
  (`human_new.go:169-173`).

Contract check vs brief: "target `create` / `new`" (`command-map.md:70`, `brief` line 15). Trifft. The
guided path only builds arguments for the same production `createTarget`; no divergent behaviour.

Verdict: `trifft`.

### 4.2 `baha target activate` — interactive name selection
Witness (`cmd/baha/target_activate_wizard.go`):

- `guidedTargetActivation` checks `noInput(ctx) || !readerIsTerminal(appNewInput)` and refuses with a
  two-line actionable error if non-interactive (`target_activate_wizard.go:16-18`), then lists targets
  and accepts a number or name or `cancel` (`:31-53`).
- It re-reads config at submit time and fails closed if a concurrent operator deleted the target
  (`:54-63`), and binds the selection through the single production management-connection boundary before
  persisting (`bindExplicitSelectionToConnection`, `:69-71`).

Verdict: `trifft`. State-preserving cancel, fail-closed on concurrent change, non-interactive guard all
present.

### 4.3 Target deployment policy wizard
Witness (`cmd/baha/target_deployment_policy_wizard.go`):

- `guidedTargetDeploymentPolicy` proposes best-practice defaults without hard-coding policy by target
  name: "an older scripted/EOF flow leaves policy unset: an explicit operator selection is required before
  imposing restrictions" (`:13-15`). Empty line defaults to `development`, `none`/`cancel` leaves policy
  unset (`:26-32`).
- It maps the chosen preset through `deployment.DeploymentPolicyPreset` and offers per-field
  customization, then re-validates the assembled flags (`:65-87`).

Contract check vs brief: "Environment names are unrestricted by fixed `dev/test/prod` semantic special
cases ... behaviour follows explicit policy/authorization" (`brief` line 12). The wizard avoids target-name
special-cases but **does** offer `development/test/staging/production/custom/none` as the preset vocabulary
(`:18`) — a fixed semantic set that the brief says should not dictate behaviour. It is opt-in and
customizable, so it does not *enforce* the restriction, but the default preset vocabulary still carries the
very `dev/test/prod` semantics the brief wants de-coupled.

Verdict: **weicht ab** (low severity). The wizard is genuinely editable and fails closed when unset, but
its preset menu encodes `development/test/staging/production` as the choice set (`target_deployment_policy_wizard.go:18`),
which the brief explicitly discourages. A contract-task follow-up should ask whether the preset vocabulary
itself should be dropped in favour of arbitrary named policies.

## 5. Platform branch (`new provider`, `stack`, `config prompt`, completion)

### 5.1 `baha new provider` — guided authoring skeleton
Witness (`cmd/baha/human_new.go`):

- `guidedCreateProvider` reads a `namespace/name` provider ID and confirms skeleton creation before
  delegating to `providerInitCommand().Run` (`human_new.go:183-217`). Non-interactive it requires the ID
  explicitly (`human_new.go:177-179`). Provider registration is authoring via a skeleton, not a runtime
  provider — consistent with "external provider registration is not provider authoring" (`brief` line 15).

Verdict: `trifft`.

### 5.2 `baha config prompt` — guided shell prompt
Witnesses (`cmd/baha/prompt.go`):

- `runPromptWizard` reads a boolean and a choice through `askPromptBool` / `askPromptChoice` with
  default/current-value placeholders and a "choose one of the listed values" re-request loop
  (`prompt.go:205-260`). Non-interactive sites carry `noInput(ctx)` (`prompt.go:63`).

Verdict: `trifft`.

### 5.3 Shell completion: `-e`/`--environment` hardcodes `dev/test/prod` (Konsistenz-Risiko)
Witness (`cmd/baha/completion.go`):

- `completeCommandLine` special-cases the `-e`/`--environment` flag and returns a fixed candidate list
  `{dev, test, prod}` (`completion.go:84-88`) — the only place the completion engine synthesizes
  environment values, and it hard-codes the three semantic names.
- `completionAcceptsApplicationName` lists a fixed command set for which app-name completion is enabled
  (`completion.go:127-129`); completion itself is read-only and deterministic (`completion.go:22`).

Contract check vs brief: "Environment names are unrestricted by fixed `dev/test/prod` semantic special
cases ... Environments, apps and targets each have stable IDs" (`brief` line 12, 13). The completion
engine still suggests only `dev/test/prod` for `-e`, so a shell user autocomplete on an arbitrary named
environment (e.g. a `prod`-named environment that is not production, or a custom-named one) gets no
suggestion. This is a UX-surface drift, not a data-path one, but it is exactly the fixed-semantic case the
brief wants gone, and it sits behind the same declarative-flag problem the interface audit flags
(`audit-interface.md` 2.1: no machine-readable flag schema, so completion and help cannot derive values
from real state).

Verdict: **Konsistenz-Risiko**. Two independent facts: (a) the environment completion candidates are
hard-coded (`completion.go:84-88`), and (b) completion cannot enumerate environments/apps/targets from
live state because there is no flag schema or store-backed candidate source for `-e`. Both should be
resolved together in the contract task.

### 5.4 Completion wiring completeness (Konsistenz-Risiko)
Witnesses (`cmd/baha/commands.go:167`, `cmd/baha/completion.go:22-57`):

- `__complete` is registered as a hidden child and wired at `cmd/baha/commands.go:167`; root
  `baha completion bash|zsh|fish` emits the shell scripts (`completion.go:22-40`). Completion is
  read-only and never invokes mutation (`completion.go:22`).
- Arrows/Tab in the interactive wizards do **not** exist: the line editors are raw
  `bufio.Reader.ReadString('\n')` loops with numeric/text entry only. The only Tab/line completion is
  `promptPathWithCompletion` on Linux (`cmd/baha/path_prompt_linux.go:27-58`). No arrow-key navigation
  exists in any wizard.

Contract check vs brief: "arrows/Enter and Tab where appropriate" (`brief` line 7). Enter and Tab are
supported where a path is involved (Linux) and Enter everywhere; arrow-key navigation is absent. Because
the project already depends on Bubble Tea v2, the absence is a deliberate architecture choice, not a
missing dependency.

Verdict: **Konsistenz-Risiko** (low). "Tab where appropriate" is met on Linux paths and by shell
completion; "arrows ... where appropriate" is not implemented in any wizard. The contract is satisfied
for Enter/Tab; the arrow-key half of the brief is unimplemented.

## 6. Access / onboarding wizards (platform-side guided paths)

### 6.1 `baha access` wizard (assign / offboard)
Witness (`cmd/baha/access_wizard_command.go`, `internal/accesswizard/wizard.go`):

- `accessAssignCommand`/`accessOffboardCommand` load the accepted production `orgconfig.Manager`, fail
  closed on incomplete config (`loadAccessWizardAuthority`, `access_wizard_command.go:195-223`), run a
  bounded pure controller that "never decides" (`:19-20`), validate every reviewed Target before any
  write, and commit the whole set atomically via `CommitActive` — a failed Target leaves the store
  byte-identical (`:65-90`, `:139-160`).
- The wizard binds the human-reviewed subject to the exact CLI argument via `validateAccessWizardPerson`
  BEFORE calling the authority (`access_wizard_command.go:251-259`).

Verdict: `trifft`. Fails closed, single production authority, atomic all-or-nothing — matches the brief's
"protected operations follow plan -> preflight -> apply -> verify" and "every assignment folds into the
single production policy authority".

### 6.2 Onboarding wizard
Witness (`internal/onboardingwizard/onboardingwizard.go`, `cmd/baha/onboarding_command.go`):
The onboarding wizard drives remote Core connect / tenant init through the same fail-closed authority and
`noInput(ctx)` guards already counted in 5.4/3.1. Verdict: `trifft`.

## 7. Cross-cutting: `--no-input` enforcement and secrets (re-companion audit 2.1 / 3.1)

- `--no-input` sets `OutputOptions.NonInteractive` once (`cmd/baha/main.go:183-184`) but is enforced at
  81+ hand-written sites (`noInput(ctx)` / `opts.NonInteractive`), e.g. the wizards at
  `app_wizard_controller.go:81`, `human_new.go:27,79,177`, `target_activate_wizard.go:16`,
  `app_init_wizard.go:81,115`, `prompt.go:63`, `node.go:163-164,696`. Nothing fails a forgotten prompt;
  the contract is satisfied today by discipline, not construction. Same finding as
  `audit-interface.md` 3.1. Verdict: **Konsistenz-Risiko** (carried, not repeated).
- Secrets: `listApplicationSecrets` returns metadata only ("Secret values are never returned",
  `cmd/baha/app_secret.go:92`); `setApplicationSecret`/`deleteApplicationSecret` keep protected bytes out
  of transport DTOs and audit metadata (`cmd/baha/secret_operations.go:21,43`). `app secret` is the
  single managed-secret authority; no plaintext leaks into normal output. Verdict: `trifft` for the
  reveal/mask contract — masked by construction, no unmasked path found at this snapshot.
- `app runtime-identity` rotate/revoke "without changing any stored baseharbor:// secret references" and
  "never grants operator API access" (`cmd/baha/app_runtime_identity.go:18`), matching the brief's
  "app data secrets ... OpenBao protection and audit apply to all access paths" (`brief` line 11). Verdict:
  `trifft`.

## 8. Summary table

| # | Path | Verdict | Witness (file:line @0e9ccb582) |
| --- | --- | --- | --- |
| 2 | Shared app-wizard state machine (TTY gate, no mutation hook, snapshot-verified preview, cancel preserves state) | trifft | `cmd/baha/app_wizard_controller.go:16-97,257-324,379` |
| 3.1 | `baha app new` greenfield (name->location->stack->placement) | trifft | `app_new_wizard.go:35-225`; `human_new.go:30-73`; `path_prompt_linux.go:27-58` |
| 3.2 | `baha app init` brownfield + `--quick` | trifft | `app_init_wizard.go:64-190` |
| 3.3 | `baha app workspace` guided component/source mapping | trifft | `app_workspace_wizard.go:19-126,207-215` |
| 3.4 | `app.id` generated, not committed (diverges from proposal) | weicht ab | `app.go:115,256`; `brief` line 14 |
| 4.1 | `baha new target` guided | trifft | `human_new.go:85-174` |
| 4.2 | `baha target activate` name selection | trifft | `target_activate_wizard.go:15-91` |
| 4.3 | deployment-preset vocabulary fixes dev/test/staging/production | weicht ab | `target_deployment_policy_wizard.go:13-32`; `brief` line 12 |
| 5.1 | `baha new provider` authoring skeleton | trifft | `human_new.go:176-217` |
| 5.2 | `baha config prompt` guided | trifft | `prompt.go:205-260` |
| 5.3 | completion `-e` hardcodes dev/test/prod | Konsistenz-Risiko | `completion.go:84-88` |
| 5.4 | arrows absent in wizards; Tab only on Linux paths | Konsistenz-Risiko | `path_prompt_linux.go:27-58`; `commands.go:167` |
| 6.1 | `baha access` assign/offboard wizard | trifft | `access_wizard_command.go:19-174,251-259` |
| 7 | `--no-input` discipline vs construction; secrets masked | Konsistenz-Risiko / trifft | `main.go:183`; `app_wizard_controller.go:81`; `secret_operations.go:21` |

## 9. Findings for the contract task (`t-20261114-r28-cli2-contract`)

- Fix 3.4: decide the `app.id` in-manifest contract (propose commit + migrate + reject-conflict) — the
  wizard currently omits it by design.
- Fix 4.3: drop the fixed `development/test/staging/production` preset vocabulary from
  `guidedTargetDeploymentPolicy` in favour of arbitrary named policies, or justify the vocabulary.
- Fix 5.3: enumerate `-e`/`--environment` completion candidates from live state (environments/apps)
  instead of the hard-coded `{dev, test, prod}` (`completion.go:84-88`); this depends on the flag schema
  gap in `audit-interface.md` 2.1.
- Fix 5.4: decide whether arrow-key navigation is in scope; Enter/Tab are already present.

## 10. END

`lane-0428-wizards` DONE. Pure IST-ZUSTAND inventory, no product change, no PR, no release, no tag.
Evidence on plan `origin/main`. END posted to `594fd2f5-4e80-43b6-9841-92879146a85e`.
