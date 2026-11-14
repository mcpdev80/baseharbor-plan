# Audit: CLI surface, dialogs, output formats, flags (IST-ZUSTAND)

Card: `t-20261114-r28-cli2-audit-interface` (0428-047) · Lane: `lane-0428-audit-interface`
Type: pure inventory (merge-frost, owner directive 2026-11-14). No product change, no PR, no release, no tag.
Inputs: [brief](brief.md), [command mapping](command-map.md), [code entry index](code-entry-index.md).

## Plan

1. Claim leg: card published `active` with owner `lane-0428-audit-interface` on plan `origin/main`
   (`6b34b1d9`, coordinator). `python3 scripts/plan.py claim` refuses to re-claim an active card, so
   the claim requirement is satisfied by the published state; nothing was re-published.
2. Locate the authoritative planning repo and read the redesign inputs (brief, command-map, code-entry-index).
3. Pin product truth: `develop` = `0e9ccb582`, plus a clean persistent clone at exactly that SHA.
4. Inventory interactive/surface paths: wizard dialogs, output formats, global and per-command flags,
   completion / shell surface, exit codes, machine (JSON/MCP/HTTP) surface — each with file:line.
5. Judge each item against Core `AGENTS.md` and `docs/DEVELOPMENT_GUIDELINES.md` plus the owner brief
   decisions. Verdicts: `trifft` / `weicht ab` / `Konsistenz-Risiko`.
6. Cite external reference sources (context7 MCP, web search) for CLI-UX and MCP norms.
7. Deliver this dossier to `evidence/cli-redesign-20261114/audit-interface.md`, push to plan main,
   set the card to `review`, post END.

## 0. Zone and provenance witnesses

Wrong-zone guard (mandated one-liner):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```

`workers/baseharbor-plan` was never used. The quarantined `workers/baseharbor` checkout was never cited:
all product truth comes from `git ls-remote` on GitHub and from a fresh clone in this lane's own zone.

Base attestation:

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote origin develop
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
$ git -C /tmp/opencode/audit-interface-wt/core rev-parse HEAD
0e9ccb582f5bdcdc74049bbe3996263cdce6500c
$ git -C /tmp/opencode/audit-interface-wt/core merge-base --is-ancestor 0e9ccb582 HEAD; echo $?
0
```

The audited snapshot is exactly `origin/develop` at `0e9ccb582`
("chore: pin v0.4.27 demo acceptance (#1573)"). Clone method:
`git clone --no-checkout --filter=blob:none https://github.com/mcpdev80/baseharbor.git`
then `git checkout 0e9ccb582f5bdcdc74049bbe3996263cdce6500c`, in
`/tmp/opencode/audit-interface-wt/core`. The clone detaches at that SHA, so the ancestry test is
trivially satisfied (`0e9ccb582` is HEAD); no branch was cut and no PR was opened, per merge-frost.
All `file:line` references below were read from that snapshot and are reproducible with
`git show 0e9ccb582:<path>`.

## 1. Reference sources used

- Command Line Interface Guidelines, "Interactivity" and "Errors": prompt only when stdin is a TTY;
  `--no-input` must never prompt and must fail with an actionable message telling the user which flag
  to pass; never require a prompt; confirm before dangerous actions with an explicit non-interactive
  escape hatch. <https://clig.dev> (retrieved 2026-11-14 via web search).
- Model Context Protocol 2026-07-28, client elicitation and Multi Round-Trip Requests (SEP-2322,
  SEP-2260): a server may ask the client for input only while processing a request, returns an
  `InputRequiredResult` with `elicitation/create`, and MUST handle decline/cancel or a client that
  cannot interact. <https://github.com/modelcontextprotocol/modelcontextprotocol>
  (`docs/specification/2026-07-28/client/elicitation.mdx`,
  `docs/docs/2026-07-28/learn/client-concepts.mdx`, `docs/seps/2322-MRTR.mdx`), retrieved 2026-11-14
  through the context7 MCP server (`/modelcontextprotocol/modelcontextprotocol`).
- Bubble Tea v2 (the TUI framework in `go.mod`): `charm.land/bubbletea/v2 v2.0.9` plus
  `charm.land/lipgloss/v2 v2.0.6` and `github.com/charmbracelet/x/term v0.2.2`; the project
  therefore already owns a terminal-input-capable dependency that the raw line editors could use.
- Internal contracts used as the judgment basis: Core `AGENTS.md` ("Work and verify":
  "Mutations follow plan -> preflight -> apply -> verify; CLI, JSON and MCP share domain semantics.
  Preserve ownership, concrete consequence/consent checks and secret protection.") and
  `docs/DEVELOPMENT_GUIDELINES.md` §6 (secrets never enter normal data paths), §8 (one lifecycle),
  §9 (CLI/JSON/MCP share one semantic core), §12 (source readability limits).

## 2. Surface inventory: routing, help, errors, exit codes

| # | Item | IST-ZUSTAND (file:line at 0e9ccb582) | Contract check | Verdict |
| --- | --- | --- | --- | --- |
| 2.1 | Command tree, no declarative flag schema | `internal/cli/cli.go:20-31` (`Command{Name,Hidden,Aliases,Summary,Usage,Long,Examples,Run,Children,HelpGroups}`); routes positionally at `internal/cli/cli.go:94-135`; every command parses its own options inside `Run`; `cmd/baha/` holds 429 non-test Go files, `cmd/baha/commands.go:28-163` builds the root tree | Core `AGENTS.md` "CLI, JSON and MCP share domain semantics"; `DEVELOPMENT_GUIDELINES.md:74-78` §9 | `trifft` for semantics (machine surface is delegated to the same CLI `Run` funcs, e.g. `cmd/baha/mcp_lifecycle_extra.go:11-13`), but there is no machine-readable option schema behind the surface: option truth lives only in prose `Usage` strings plus scattered per-file parsers. This is what makes the drift in 2.2, 4.x and 5.x possible. | Konsistenz-Risiko |
| 2.2 | Unknown-option suggestions are reconstructed from the Usage string | `internal/cli/cli.go:204-214` `knownFlags()` = fixed global list + regex `--[A-Za-z0-9][A-Za-z0-9-]*\|-[A-Za-z]` over `c.Usage`; `cli.go:171-202` `decorateUsageError` adds a suggestion only when the message contains "unknown" and `NoSuggestions` is false; `cli.go:395-435` Levenshtein cutoff (commands distance <=2, flags <=3 then <=2) | brief line 7 "no interactive dead ends"; clig.dev "Errors" (tell the user what to pass) | `trifft` in shape. Consequence: any option that is parsed but absent from the Usage string is invisible to `--help`, to the suggestion engine and to completion. Verified misses: `baha app secret set` Usage `cmd/baha/app_secret.go:31` advertises no `--json` although `app_secret.go:33` calls `parseReadOutputArgs`, which accepts `--json` (`cmd/baha/output.go:23-24`) and honours it at `app_secret.go:59`. Same shape in `baha trust uninstall` (`cmd/baha/trust.go:164`, `--json` handled), and in the `baha target` group where `--json` is advertised in Usage (`cmd/baha/target.go:167,173`) yet `knownFlags` takes the flag set from a single `Usage` string per command, so group-level wording and child-level wording can disagree. | weicht ab |
| 2.3 | Root help and help paging | `internal/cli/cli.go:95-108` (no args prints help, exit 0; `help` and `--help`/`-h` both work); `cli.go:244-248` `Help` wraps through `writeMaybePaged`; `internal/cli/pager.go:12-42` uses `$PAGER`, default `less -FRX`, only when writer is a TTY, >=28 lines (`pager.go:10`) and `TERM != dumb` | DEVELOPMENT_GUIDELINES §7 one source of truth; STYLE_GUIDE "Do not manually duplicate syntax that can be generated from code" | `trifft`: help is generated from the tree, paging is guarded for non-TTY and `TERM=dumb`, and failure of the pager falls back to direct write (`pager.go:40-42`). | trifft |

Note for the contract task (t-20261114-r28-cli2-contract): the pager is the only place in the
human surface that spawns `$PAGER` from the environment (`internal/cli/pager.go:22-39`); it takes no
user data, but a redesign that moves help to `system shell completion`-style generated pages should
keep the TTY/`TERM=dumb`/`exec.LookPath` guards and the silent direct-write fallback.

### 2.4 Exit codes (no documented contract)

| Signal | Code | Witness |
| --- | --- | --- |
| success | 0 | `internal/cli/cli.go:82-91` `ExitCode` |
| usage error | 2 | `cli.go:86-89` (`*cli.UsageError` -> 2) |
| runtime failure | 1 | `cli.go:90` (fallback) |
| internal hosts-writer IPC failure | 1 | `cmd/baha/main.go:43-46` |
| SIGINT / first cancellation | 130 | `main.go:61-63`, `main.go:83` |
| SIGTERM / second signal | 143 | `main.go:84-86`, `main.go:102-103` |
| grace window exceeded | 130 or 143 by signal | `main.go:90-99` (2s timer) |

Search of `docs/spec/`, `docs/reference/` and `docs/cli/` finds no table of these codes: the only
statement is the generic "check each command's exit status" in `docs/cli/automation-agents.md:57`,
and `docs/reference/errors.md` types outcomes but never numbers them. Contract text exists only as
a Go doc comment (`internal/cli/cli.go:39`, `:81`).

External norm: the conventional split is 0 success, 1 generic failure, 2 misuse of a command line,
and 128+n for signal death - the same mapping clig.dev relies on for "Errors" and what GNU
standards document. baha already implements that mapping (see table above); it is only undocumented.

Verdict: Konsistenz-Risiko. The codes are correct and stable in code, and machine callers in CI
cannot learn the meaning of 2 vs 1 vs 130 from any shipped reference page, while
`docs/reference/cli.md:18` declares "Command-specific --help remains the authoritative syntax" -
help text carries no exit-code section at all (`internal/cli/cli.go:323-332` renders global options
and a help hint only).

## 3. Global options and the stable-meaning flags (-t / -e / -c / --yes / --no-input / --agents)

Global options are stripped before dispatch in one pass, `cmd/baha/main.go:157-211`:

| Option | Handler | Behaviour witness | Verdict |
| --- | --- | --- | --- |
| `-q`, `--quiet`, `--silent` | `main.go:175-176` | `internal/cli/terminal.go:172-176,183-185` (sections suppressed, `FAILED` always kept) | trifft |
| `-v`, `--verbose` | `main.go:177-178` | `cmd/baha/ux.go:12-25` (preflight details), `main.go:69` (`formatCLIErrorVerbose`) | trifft |
| `--quiet` + `--verbose` together | `main.go:204-206` | typed usage error, exit 2 | trifft |
| `--no-color` | `main.go:179-180` | `internal/cli/terminal.go:120-128` plus `NO_COLOR` env and `TERM=dumb` | trifft |
| `--plain` | `main.go:181-182` | `terminal.go:122-125` (forces no-colour + reduced motion), `terminal.go:154` (`TTY()` false), `cmd/baha/tui.go:80-82` refuses the TUI in plain mode | trifft |
| `--no-input` / `--non-interactive` | `main.go:183-184` | see 3.1 | Konsistenz-Risiko |
| `--version` | `main.go:185-186`, refusal to combine with a command at `main.go:135-141` | `baha --version` prints three lines to stdout | trifft |
| `--target NAME` / `--target=NAME` | `main.go:187-199`, context injection `main.go:142` `withTargetOverride` | resolution order `cmd/baha/target_selection.go:95-115`: explicit -> `BASEHARBOR_TARGET` -> persisted -> configured default -> unique -> implicit-local | weicht ab (see 3.2) |
| (env) `BASEHARBOR_REDUCED_MOTION` | `main.go:207-209` | only accessibility option; consumed `terminal.go:121-125`, `tui.go:88` | Konsistenz-Risiko |

The rendered `Global options:` block, `internal/cli/cli.go:323-330`, lists quiet/silent, verbose,
plain, no-color, no-input and version but omits `--target` and `--non-interactive`, while
`cmd/baha/main.go:187-199` and `main.go:183` implement both. `docs/cli/global-options.md:5-15` does
document `--target` and `--non-interactive`, so the help output is the narrower of the two truths.
Verdict: weicht ab - one fact (which global options exist) has two different authoritative
statements, against DEVELOPMENT_GUIDELINES §7.

### 3.1 `--no-input` is honoured but not centrally enforced

- Contract: brief line 7 - "`--no-input` and scripts never block and get typed actionable errors";
  clig.dev "Interactivity" - with `--no-input` do not prompt and fail with a message naming the flag
  that supplies the value.
- Implementation: the flag only sets `OutputOptions.NonInteractive`
  (`cmd/baha/main.go:183-184` -> `internal/cli/terminal.go:18-28` -> `terminal.go:153`). There is no
  central gate: the check is 81 hand-written sites (`noInput(ctx)` or `opts.NonInteractive`);
  accessor `cmd/baha/ux.go:50-52`; e.g. `cmd/baha/provider_change_confirmation.go:30`,
  `cmd/baha/app_secret.go:236`, `cmd/baha/human_new.go:27,79,177`, `cmd/baha/repository_up.go:171,235,281`,
  `cmd/baha/node.go:163-164,696`, `cmd/baha/doctor.go:107,169`.
- Fail-closed behaviour is right where it was added deliberately: `provider_change_confirmation.go:29-31
  + 58-73` makes `--yes` insufficient for impact or data-deletion consent; `app_secret.go:236-241` names
  `--stdin`/`--file`; `tui.go:81-83`; `prompt.go:63-65`; `app_wizard_controller.go:80-83`
  (`errAppWizardNonInteractive`). EOF is treated as cancellation, never approval
  (`app_init_prompts.go:403-414`, `trust.go:205-212`).
- Gap: nothing fails a forgotten prompt. A `bufio.NewReader(in).ReadString('\n')` that is not
  preceded by `noInput(ctx)` blocks in a script; correctness depends on all 81 sites staying
  individually correct. Verdict: Konsistenz-Risiko (contract satisfied today by discipline, not by
  construction).

### 3.2 `-t` (target) does not exist

- Contract: brief line 8 - "`-t` target, `-e` environment, `-c` one or comma-separated components
  throughout applicable commands. Names and meaning must be consistent."
- IST: the only target selector is the global `--target NAME`/`--target=NAME`
  (`cmd/baha/main.go:187-199`) plus `BASEHARBOR_TARGET` and the persisted selection
  (`cmd/baha/target_selection.go:95-115`). A repository-wide scan for a `-t` option finds only
  unrelated uses (`internal/hosttrust/browser_nss.go:148`, `git -c`/`sh -c` exec arguments).
- Consequence for the redesign: no shorthand parity with `-e`/`-o`/`-y`; scripts written against the
  target contract in the brief cannot be expressed. Verdict: weicht ab.

### 3.3 `-e` / `--environment`: consistent where present, absent where the brief expects it

Both spellings are accepted together in the sites that implement them - `cmd/baha/runtime.go:93`,
`cmd/baha/policy.go:80`, `cmd/baha/onboarding_command.go:152`, `cmd/baha/config_org.go:237,274` - so
the pair itself is consistent (42 Usage strings carry `-o`, 12 carry `-e`, `grep -oE '\-[A-Za-z]\b'`
over `Usage:` lines in `cmd/baha`). Gaps against "throughout applicable commands":

- `baha node add` accepts only long `--environment` (`cmd/baha/node.go:301`), its own
  `unknownOptionUsage` candidate list confirms the long-only form (`node.go:306`).
- `baha app new` documents `-e ENV|--environment ENV` (`cmd/baha/app_new.go:36`) and `baha app init`
  documents it too (`cmd/baha/commands.go:215`), but the read group does not: `baha app status` Usage
  `cmd/baha/app_observe.go:205` advertises only `[NAME] [-o json|--output json]`, and `app plan` /
  `app show` reach the environment only through the positional resolver
  (`cmd/baha/app_status_result.go:127`). The environment selector has no consistent surface across
  the app group.

### 3.4 `-c` / `--component`: three different names for one concept

Contract: brief line 8, one `-c` meaning "one or comma-separated components".
IST:

- `baha app workspace init` (and the `baha workspace` twin): `--component COMPONENT=SOURCE[@SUBPATH]`,
  `cmd/baha/app_workspace.go:81,102,105`, candidate list `app_workspace.go:115`.
- `baha stack` authoring: a second, unrelated `--component` (`cmd/baha/stack.go:176,185`).
- `baha app init` / `app new`: the workload selector is `--workload-component NAME`
  (`cmd/baha/app.go:310-311,322-323,343,585-590,612-631`; Usage line
  `cmd/baha/commands.go:215`).
- Nowhere is there a `-c` short form, and nowhere does a command accept a comma-separated component
  list; the workspace form takes one `KEY=VALUE` per repetition.
- Verdict: weicht ab. The same word ("component") carries two different grammars
  (`COMPONENT=SOURCE[@SUBPATH]` vs a bare logical name) and neither matches the brief.

### 3.5 `--yes` / `-y`: 58 long-form sites, 16 files also carry the shorthand

- Files that accept both: `cmd/baha/app_up.go:22-23`, `cmd/baha/runtime.go:83`, `cmd/baha/target.go:573`,
  `cmd/baha/trust.go:132,174`, `cmd/baha/update.go:125`, `cmd/baha/dev_hosts.go:98`, `cmd/baha/node.go`,
  `cmd/baha/app_runtime_init.go:105`, `cmd/baha/provider_external.go:210`,
  `cmd/baha/management_remote_destroy_cli.go:37,44,56`, `cmd/baha/management_remote_apply_cli.go:54`,
  `cmd/baha/control_plane_cli.go:13`, `cmd/baha/app_workload_ports.go:601`.
- Files that accept only `--yes`: `cmd/baha/app_lifecycle.go:429` (`app destroy`/`app stop`),
  `cmd/baha/app_secret.go:299`, `cmd/baha/app_runtime_identity.go:17,24,56`, `cmd/baha/app_doctor_repair.go:50,58,72`,
  `cmd/baha/doctor.go`, `cmd/baha/config_org.go`, `cmd/baha/onboarding.go`, `cmd/baha/user_command.go`,
  `cmd/baha/workstation_command.go`, `cmd/baha/dev_workstation_cleanup.go`, `cmd/baha/runtime_destroy_all.go:184`.
- The completion layer advertises the shorthand unconditionally: `cmd/baha/completion.go:167-168`
  maps `-y` -> "accept safe defaults without prompting" from the Usage regex, so a `-y` candidate can
  appear for a command whose parser would reject it with an unknown-option error
  (`cmd/baha/ux.go:54-59`).
- Semantics where `--yes` exists are contract-correct: `--yes` never buys consequence or deletion
  consent (`cmd/baha/provider_change_confirmation.go:29-31` with the explicit comment at `:27-28`,
  `cmd/baha/commands.go:78` "``--yes`` does not replace provider-consequence or data-deletion consent"),
  and `cmd/baha/target.go:579` documents what `--yes` does honour on the detach path.
- Verdict: Konsistenz-Risiko. Safe by design, inconsistent by spelling - and the completion surface
  is the visible symptom.

### 3.6 `--agents` is a documentation-only mode, correctly fenced

- `cmd/baha/app_agents.go:12-13` marker constants, `:30-33` refuses ambiguous marker pairs,
  `:79-81` rejects duplicates; `cmd/baha/app_input_resolver.go:222` rejects mixing `--agents` with
  initialization arguments, `:29` states the bounded-section promise.
- `cmd/baha/agents_root_help_test.go:17` pins the help wording so `init --agents` is never shown
  alongside lifecycle arguments. Both `baha init` (`cmd/baha/commands.go:39`) and `baha app init`
  (`commands.go:215`) advertise it.
- Verdict: trifft (brief line 10 keeps documentation and configuration separate).

## 4. Output formats

| Item | IST (0e9ccb582) | Contract check | Verdict |
| --- | --- | --- | --- |
| The format vocabulary | exactly two formats: `human` and `json` (`cmd/baha/output.go:12-15`); any other value -> typed usage error `unsupported output format` (`output.go:31-40`) | DEVELOPMENT_GUIDELINES §9 "Presentation differs. Domain behavior does not." | trifft |
| Flag spellings accepted | `--json`, `-o json`, `--output json`, `-ojson`, `--output=json` (`output.go:20-50`); all five forms reach 72 call sites | - | Konsistenz-Risiko: `-o` doubles as the output *destination* in `baha trust export`, stated only in the coverage table (`cmd/baha/machine_coverage.go:77` "CLI --json (--output is CA destination)") |
| Who declares it | `parseReadOutputArgs` is called in 72 places, but only 42 Usage strings contain `-o` (`grep -c` over `Usage:` lines). Commands that accept JSON silently: `baha app show` (`cmd/baha/app_show.go:43`, parser called `:47`), `baha app secret tls-set` (`app_secret_tls.go:30`), `baha app runtime-identity*` (`app_runtime_identity.go:17`), `baha app prune` (`app_prune.go:43`) | `docs/reference/cli.md:18` names `--help` the authoritative syntax | weicht ab |
| Machine error envelope | `internal/machine/contract.go:61-70` + `:150-157` `ResultError{contract_version, error{code,message,cause,retryable,next,resource,remediation_class,details}}`, 21 stable codes (`contract.go:34-56`) | DEVELOPMENT_GUIDELINES §6 (secret-safe), §9 | trifft; `cmd/baha/main.go:65-68` prints the envelope on stderr only when JSON was requested and the failure was not already rendered |
| Human error rendering | `main.go:217-260` splits `machine.Error` into Error / Affected / Resolution / What to do blocks, keeps `Next:` for usage and actionable errors | brief line 7 "typed actionable errors" | trifft |
| Streaming exception | `logs`, `exec`, `shell`, `sql`, `cache` are excluded from the machine surface by design (`cmd/baha/machine_coverage.go:166-170`) because raw streams can carry secrets | DEVELOPMENT_GUIDELINES §6 | trifft |

One asymmetry worth the contract task: `internal/machine/contract.go:13` pins `ContractVersion = "v1"`
for the whole machine surface, while `internal/cli/cli.go:20-31` carries no version marker for the human
surface. A compat shim (task 130) that renames `app secure-profile` to `app data export` therefore has a
versioned contract on one side and an unversioned, prose-declared syntax (`docs/reference/cli.md:18`) on
the other.

## 5. Wizard and dialog surface

Central contract: brief line 7 - blank/missing input offers a task-specific wizard, arrows/Enter and
Tab where appropriate, cancellation preserves state, no interactive dead ends; DEVELOPMENT_GUIDELINES
§9 requires the same semantics through MCP.

| # | Surface | IST (0e9ccb582) | Verdict |
| --- | --- | --- | --- |
| 5.1 | Selection widgets with arrows | exactly two places use a raw-mode selector: `cmd/baha/app_init_prompts.go:97-160` (`term.MakeRaw`, `:104` documents "Use up/down to move, Space to toggle, Enter to confirm", `:146-160` renders), plus `cmd/baha/path_prompt_linux.go:43-58` for path entry with `:105` Tab completion and `:119` swallowing arrow escapes. Every other choice is a numbered line prompt: `promptLine` (`app_init_prompts.go:356-370`), `promptYesNo` (`:380-391`), the numbered capability fallback (`:60-86`), `target_activate_wizard.go:35-52`, `provider_change_confirmation.go:77-112` | weicht ab (the brief promises arrows/Tab "where appropriate"; the surface is inconsistent by construction) |
| 5.2 | Two input engines in one process | the wizard prompts read through a shared `*bufio.Reader` (`app_init_prompts.go:403-414`), while the raw-mode selector interleaves `reader.ReadByte` (`:113`) with `\x1b`-sequence parsing (`:141-155`), and the TUI uses its own framework loop. Mixing buffered and raw reads on one fd is the known hazard; the raw-mode path is guarded only by `readerIsTerminal` (`:56`) | Konsistenz-Risiko |
| 5.3 | Cancel preserves state | the wizard controller holds intent only, no mutation hook (`app_wizard_controller.go:26` `errAppWizardAbort`, `:167-171` `abort()` clears the decision, `:173-181` `intent()` is described as "intent only"); EOF is cancellation, never approval (`app_init_prompts.go:409-413`, `trust.go:205-212`); the workspace wizard test pins that a cancelled wizard writes nothing (`app_workspace_wizard_test.go:145`) | trifft |
| 5.4 | Non-interactive refusal | `newAppWizardController` refuses without TTY or with `--no-input` (`app_wizard_controller.go:80-83`); `app new` and the `new` chooser refuse politely with the flag recipe (`app_new.go:36-40`, `human_new.go:27,79,177`) | trifft |
| 5.5 | Consent prompts | two-stage acknowledgement plus separate data-deletion consent (`provider_change_confirmation.go:58-112`); a second, looser single-prompt variant used by the apply path (`:58-73`); `app destroy` requires `--yes` plus the plan acknowledgements (`app_lifecycle.go:425-437`, `application_destroy_authorization.go:169`) | Konsistenz-Risiko: two acknowledgement grammars coexist ("y" per stage vs one "Apply these changes?" that fills both fields) |
| 5.6 | German token inside English output | `"Achtung"` is the machine-facing attention marker (`internal/application/provider_change_scope.go:59`, `provider_change_plan.go:93,98`) and is interpolated verbatim into 12 English prompt strings, e.g. `cmd/baha/provider_change_confirmation.go:42,82,84,104`, `application_stop_impact.go:177`, `application_restore_authorization.go:158`, `control_plane_stop_impact.go:180`, `runtime_destroy_impact.go:178,180`, `target_definition_change.go:33`, `provider_external_removal.go:36`, `node_disconnect_client.go:158` | weicht ab. The card contract requires English CLI UX; the untranslated token reaches the developer and `-o json` (`Details` at `provider_change_confirmation.go:44-56`) |
| 5.7 | TUI | `cmd/baha/tui.go:54-102`, Bubble Tea program (`go.mod`: `charm.land/bubbletea/v2 v2.0.9`); refuses `--plain`, `--no-input` and non-TTY with an actionable redirect (`tui.go:80-87`) | trifft |

External norms for 5.1-5.5: clig.dev "Interactivity" (prompt only on a TTY, always a flag path,
confirm before dangerous actions) and MCP 2026-07-28 elicitation/MRTR, where a server that needs
user input returns `resultType: "input_required"` with `elicitation/create` requests and must handle
decline or cancel - the protocol-level equivalent of "cancel preserves state", and the shape the
contract task should compare `app.edit` two-phase consent against
(`cmd/baha/machine_coverage.go:73-74`).

## 6. Completion and shell surface

| Item | IST (0e9ccb582) | Verdict |
| --- | --- | --- |
| Commands | `baha completion bash\|zsh\|fish` (`cmd/baha/completion.go:22-45`), hidden `baha __complete` (`completion.go:47-59`), `baha shell-init bash\|zsh\|fish` (`cmd/baha/prompt.go:426-449`), hidden `baha prompt` (`prompt.go:263-268`), `baha config prompt` wizard (`prompt.go:29-33`) | trifft: deterministic, read-only, no mutation in the completion path |
| Candidate generation | walks the live tree (`completion.go:98-104`), derives flags from the Usage regex (`completion.go:153-177`), adds the fixed global set (`completion.go:115-123`), adds application names only for a hard-coded command-name list (`completion.go:127-134`) | Konsistenz-Risiko: the same Usage-String dependency as 2.2, so a flag missing from Usage is also missing from Tab completion, and `completionAcceptsApplicationName` (`:128-133`) omits commands such as `creds`, `evidence`, `secret` and `footprint` |
| Environment candidates | literal `dev`/`test`/`prod` (`completion.go:84-89`) | weicht ab - brief line 12 says environments are unrestricted by a fixed `dev/test/prod` special case; the shell surface hard-codes exactly that triple |
| Shell scripts | bash `complete -o default -F` (`completion.go:208-224`), zsh `compadd -d` (`:226-243`), fish `complete -c baha -f -a` (`:245-253`); shell-init exports `baha_target_activate`/`baha_target_deactivate` as `BASEHARBOR_TARGET` mutations (`prompt.go:451-488`) | trifft. POSIX sh is not covered; per the 0428-047 acceptance line, that must be reported as a constraint, not assumed |

## 7. Machine interfaces (CLI vs JSON vs MCP vs HTTP)

Contract: DEVELOPMENT_GUIDELINES §9 - one semantic core, presentation differs, no interface may
bypass policy, ownership, reconciliation, verification or evidence; brief line 16 - human-only
reveal stays out of ordinary machine output.

- Coverage is declared, not silent: `currentCommandCoverage()` walks the live tree and classifies each
  path as `semantic` / `presentation` / `excluded` / `alias` / `gap`
  (`cmd/baha/machine_coverage.go:21-93`); the routing table is `:95-131`
  (`cliMachineOperations`), presentation reasons `:132-160`, exclusions `:161-180`,
  per-command semantic-mode notes `:181-196`.
- Machine contexts force non-interactivity: MCP lifecycle sets `NonInteractive/Quiet/Plain`
  (`cmd/baha/mcp_lifecycle_extra.go:11-15`), `cmd/baha/mcp.go:385-390`, HTTP executor
  (`cmd/baha/machine_http_executor.go:110`). Verdict: trifft - the MCP analogue of clig.dev
  "never require a prompt", and it matches the MRTR model where a server that needs input returns
  `input_required` instead of blocking.
- Sensitive reveal is excluded from machine output by explicit note, not by accident:
  `cmd/baha/machine_coverage.go:189` (`baha app env`: MCP exposes masked values only, `--reveal` and
  loading the protected dotenv file are execution-host credential access and explicitly excluded),
  and the `baha app creds` entry in `cliSemanticModes` (`machine_coverage.go:190`) which keeps CLI
  credential reveal operator-local and out of MCP. Verdict: trifft with brief line 11.
- Parity risk: `agent describe` publishes the coverage table (`cmd/baha/agent.go:64-79`) with
  `machine.ContractVersion = "v1"` (`internal/machine/contract.go:13`), while the human surface
  carries no version (see 4). Renames land on the human side first, so a compat shim
  (`t-20261114-r28-cli2-compat-shim`) must bridge an unversioned syntax against a versioned
  contract. Verdict: Konsistenz-Risiko.
- HTTP bindings are enumerated separately from the operation registry
  (`internal/machine/http.go:11-25`, includes `logs`/`exec`/`terminal_*` streams) while the CLI
  coverage table declares those very modes excluded from MCP (`machine_coverage.go:166-170`).  A machine client reading only `agent describe` sees no MCP tool, a client reading the HTTP
  catalogue sees an endpoint. Verdict: Konsistenz-Risiko for the contract task to resolve.

## 8. Environment-name special cases reachable from the surface

Brief line 12: "Environment names are unrestricted by fixed `dev/test/prod` semantic special cases;
same capabilities irrespective of name, behavior follows explicit policy/authorization." IST - the
name is still load-bearing at five surface-visible decision points:

1. Shell completion hard-codes `dev/test/prod` (`cmd/baha/completion.go:84-89`) -> weicht ab.
2. Authorization boundary skips enforcement for `dev`/`development`
   (`internal/operatorauth/config.go:83-90` `ManagedEnvironment`), consumed by
   `cmd/baha/mcp.go:341-345` -> weicht ab (behaviour follows the name, not a policy).
3. Installation destroy authorizes at the highest-ranked name
   (`cmd/baha/runtime_destroy_authority.go:75-85`, `dev|development` 0 ... `prod|production` 3)
   -> Konsistenz-Risiko: a name chooses the authority level.
4. Prompt colour and PROD indicator derive from the name
   (`cmd/baha/prompt.go:333-352`, `:369-385`) -> Konsistenz-Risiko (cosmetic, but it is the same
   hard-coded triple).
5. Default environment resolution falls back to `"dev"` in 20+ places (e.g.
   `cmd/baha/mcp.go:331-337`, `mcp_tools.go:87`, `node.go:336`, `onboarding.go:63`,
   `management_remote_status.go:38`) -> Konsistenz-Risiko; brief line 12 asks for guided/automatic
   initial local context without a hard-coded `dev` rule.

## 9. Verdict roll-up

| Area | trifft | weicht ab | Konsistenz-Risiko |
| --- | --- | --- | --- |
| Routing / help / errors (2.x) | 2.3 | 2.2 | 2.1, 2.4 |
| Global options and stable-meaning flags (3.x) | 3.6 | 3.2, 3.4, global-options help block | 3.1, 3.3, 3.5, `BASEHARBOR_REDUCED_MOTION` |
| Output formats (4) | format vocabulary, machine envelope, human errors, stream exclusion | undocumented `--json` on 4+ commands, `-o` double meaning | one-versioned-one-unversioned surface |
| Wizards and dialogs (5) | 5.3, 5.4, 5.7 | 5.1, 5.6 | 5.2, 5.5 |
| Completion / shell (6) | scripts, read-only guarantee | hard-coded `dev/test/prod` | Usage-derived flag discovery, name-completion list |
| Machine interfaces (7) | forced non-interactivity, reveal exclusion, declared coverage | - | parity/version, HTTP-vs-MCP stream catalogue |
| Environment special cases (8) | - | items 1, 2 | items 3, 4, 5 |

Nothing in this inventory contradicts a safety contract: `--yes` never buys consequence consent,
reveal stays out of machine output, cancel and EOF never authorize a mutation, and the machine
surfaces are explicitly classified rather than silently missing. The real exposure is discoverability
and naming: help text, Tab completion and the suggestion engine all reconstruct option truth from
prose `Usage` strings (`internal/cli/cli.go:204-214`, `cmd/baha/completion.go:153-177`), so every
parser that grows an option without growing its Usage line silently loses it from the interface.
That single mechanism explains 2.2, the 4.x format rows and 6 row 2.

## 10. Handoff and limits of this audit

- Static inventory only. Nothing here was executed against a live Docker or Podman Target, so actual
  TTY-versus-non-TTY behaviour of the raw-mode selector (5.2), the pager spawn (2.3) and the
  `--no-input` gate (3.1) is asserted from code paths and unit-level tests in the same snapshot, not
  from a runtime journey. Native proof belongs to the implementation cards that own those paths.
- Scope discipline: no product file was read into a change set, no branch was created, no PR opened,
  no workflow touched, no container or compose project started; the only writes are inside
  baseharbor-plan (`evidence/cli-redesign-20261114/audit-interface.md` and this card).
  Merge-frost respected: this dossier proposes no candidate and authorizes no release or tag.
- For the contract task (`t-20261114-r28-cli2-contract`), the open decisions this audit surfaces are:
  (a) an option truth source other than the `Usage` string; (b) whether `-t` and `-c` are introduced
  or the brief wording is relaxed; (c) the documented exit-code table; (d) the English replacement for
  the `Achtung` marker (a machine-facing value change, so contract- and schema-visible); (e) whether
  HTTP stream bindings stay outside the MCP exclusion list; (f) how environment names stop carrying
  authorization meaning.
- Sibling cards touched by the same evidence, to avoid duplicate findings: 0428-048 (guided journeys)
  owns 5.1/5.2 prompts end-to-end; 0428-046 (audit access) owns 8 item 2; the compat-shim card owns the
  4 version-parity row.

## Evidence on origin/main

Placeholder replaced below by the `git ls-tree` witness before END.

END_PENDING
