# Akte: CLI2 contract round 1 (0428-049 / t-20261114-r28-cli2-contract)

- type: evidence (contract authoring, plan-only deliverable)
- release: v0.4.28
- card: 0428-049
- task: t-20261114-r28-cli2-contract
- owner: lane-cli2-contract-r28
- produced: 2026-11-14 (shift 0428)
- candidate base: develop @ `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (product repo `mcpdev80/baseharbor`)
- planning base: `origin/main` @ `3aa218da73504b3ff428b687d253095bee7fa9dd`
- deliverable: `evidence/cli-redesign-20261114/contract/cli-command-contract-v1.md` + this akte

## Scope and method

This lane wrote the reviewed CLI2 command contract for the implementation packages, per the owner brief, command map, code-entry index and the four completed audits. The lane read the actual `develop @ 0e9ccb582` source tree (persistent clone at `/tmp/opencode/core-wt`, `git show 0e9ccb582:<path>` reproduces every witness) and the shipped CLI docs, then reconciled each proposed name/flag/format against current behaviour. No product file was changed, no `.github/**` touched, no CI rerun, no container/compose started, no subagent spawned. This is a plan-only deliverable; there is no product change and therefore no PR is required (mission merge-frost + evidence-only deliverable).

Work plan recorded in the live board `workers/todos/mission-cli2-contract.md.json` (id/title/steps), the mission evidence `## PLAN` list, and this akte.

## Inputs

- Owner working brief: `evidence/cli-redesign-20261114/brief.md`
- Proposed command mapping: `evidence/cli-redesign-20261114/command-map.md`
- Static code-entry index: `evidence/cli-redesign-20261114/code-entry-index.md`
- Audit access: `evidence/cli-redesign-20261114/audit-access.md`
- Audit app: `evidence/cli-redesign-20261114/audit-app.md`
- Audit interface: `evidence/cli-redesign-20261114/audit-interface.md`
- Audit wizards: `evidence/cli-redesign-20261114/audit-wizards.md`
- audit-platform.md: draft lane-notes, not on origin/main (still `in work`); platform/environment paths treated as **VORLAEUFIG (provisional)** and flagged as such.

## What the contract fixes

- **Command tree / taxonomy** (§4-7, §10): `app`, `env`, `target`, `context`, `platform`, `access`, `system` groups with their leaves mapped from the current `develop` tree (root `baha`, `cmd/baha/commands.go:33-166`).
- **Stable shared flags** (§3): `-t/--target`, `-e/--environment`, `-c/--component`, `--yes/-y`, `--json/-o`, `--no-input`, with current-vs-contract state and safe defaults.
- **`app data` group** (§7): `env`, `secrets`, `services`, `tls`, `backup`, `restore`, `export`, `secrets identity`.
- **`target remove`** (§5): new leaf that retains runtime + data; `delete` = detach/recovery alias.
- **Identity model** (§6): stable per-environment/app/target IDs, shared environments, name independence; `app.id` committed in `baseharbor.yaml` (brief line 14) stated as an open decision.
- **Output/error formats** (§8): format vocabulary, accepted spellings, machine envelope, exit-code table, version marker.
- **`access` group** (§9): `user`, `workstation`, `grant`, `login`, `logout`, `whoami`, `onboard` — with carried audit-finding (no audit event on the mutation surface).
- **Migration + testing matrix** (§12): every old leaf/flag → destination.
- **Unresolved owner decisions** (§11): 10 items with safe defaults; no invented behaviour.

## Findings carried from the four audits

- audit-access F1: `baha app creds --reveal` prints plaintext password + URI with one gate and no audit → contract fixes masked-by-default + explicit `--reveal`; implementation adds per-reveal audit + (recommended) second consent gate.
- audit-access F2/F3: identity/access mutation surface writes no audit event → contract requires audit events for `access`/`onboard`/auth/data; reveal paths need per-reveal audit.
- audit-interface 2.2/5.x: unknown-option suggestions reconstruct from the prose Usage string; incomplete wizard surface; `Achtung` token in English output → contract requires English `Warning:` + a non-Usage option-truth source.
- audit-interface 2.4: exit codes correct but undocumented → contract documents the table.
- audit-interface 3.1: `--no-input` satisfied by discipline (~81 sites) → contract introduces a central gate.
- audit-interface §7 / audit-wizards 5.4: HTTP-vs-MCP stream parity and absent arrow navigation → contract states safe defaults.
- audit-app item 3: `app show` (authored manifest) ≠ `app status` (readiness) → contract keeps both distinct.
- audit-app item 5: `app workspace update` (multi-repo) vs `app update` (single-app + backup policy) collapsed to one `app pull` → contract keeps them distinct.
- audit-wizards 4.3: deployment-preset vocabulary encodes `development/test/staging/production` → contract states name independence.

## Open owner decisions (contract §11)

`app.id` in committed contract; `-t`/`-c` shorthand; environment name semantics; `app exec` grammar; `app pull`/`--up` naming; `Achtung` replacement; `app show` vs `app status`; `--no-input` central gate; HTTP-vs-MCP parity; arrow-key navigation. Each has a stated safe default; none invents behaviour.

## Repo-rule compliance

- No product file created, changed, deleted or reverted. MERGE-FROST respected.
- Evidence written only inside the planning repo: `evidence/cli-redesign-20261114/contract/`.
- No `.evidence/` directory, no main-branch writes in the product repo.
- No subagents (AGENTS 4.8). Every step run inside this lane.
- No Docker/Podman, no GitHub-hosted runs, no `.github/**`, no CI reruns.

## Evidence witnesses (checked-out tree @ 0e9ccb582)

- product develop head: `0e9ccb582f5bdcdc74049bbe3996263cdce6500c` (`git show 0e9ccb582:<path>` reproduces all)
- `cmd/baha/commands.go:33-166` — current root command tree
- `cmd/baha/commands.go:209-255` — appended app lifecycle/data surface
- `cmd/baha/app.go:256` — authored YAML omits `ApplicationID`
- `cmd/baha/app_update.go:44` — current source update (no `--up`)
- `cmd/baha/app_access.go:129` — `--reveal` prints plaintext password + URI (no audit)
- `cmd/baha/output.go:31-40` — `unsupported output format` usage error
- `internal/machine/contract.go:13` — `ContractVersion = "v1"`
- `internal/cli/cli.go:82-91` — exit codes
- `cmd/baha/main.go:187` — `--target` global strip

## PLAN (work list)

- Read mission, card, brief, command-map, code-entry-index, four audits; verify plan remote + product base
- Attest plan `origin/main`; cut own branch on develop base inside planning repo
- Claim satisfied (card already `active`, owner `lane-cli2-contract-r28`); no re-claim
- Write `cli-command-contract-v1.md` + akte `contract/round-1.md`
- Witnesses: `ls-tree` of the akte, `ls-remote` of my branch, ancestor witness
- Push evidence to planning `origin/main`; attest `ls-remote origin/main` before END
- Post END to `594fd2f5-4e80-43b6-9841-92879146a85e`

## END

- lane: lane-cli2-contract-r28
- status: DONE (contract + akte written; plan-only deliverable, no PR)
- candidate SHA: plan branch `lane-cli2-contract-r28` (base develop `0e9ccb582`; planning origin/main `3aa218da`)
- note: MERGE-FROST; evidence-only deliverable, no product change, no PR — reported per mission line 2.
