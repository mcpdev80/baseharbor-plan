# H-V24 actionability-desk — round 1 (read-only befundung, no product change, no PR, no hosted matrix, no foreign-host test)

- Lane: `w225-0428-204-huntact` (laptop:2)
- Card slice: H-V24, coordinator/BUG-HUNT.md rotation 2026-11-21, develop-Anker `40cb28c758b02960356434b630086a341ebe1738`
- Mission (H-V24): the two merges #1717 (operator-auth gate at `internal/operatorauth/authorization.go:285`) and #1594 (dev-to-trusted-local auto-admit removal) forced the CLI to require a verified principal in managed environments. Nothing has checked whether the **message a real user sees** tells them what to do next. This desk audits every operator-auth refusal site for actionability (missing precondition / next command / path). Befund only + card drafts.
- Result: **DONE** — 7 distinct operator-auth refusal sites inventoried, each rubriced a/b/c, 1 actionable-deficiency finding, 1 finding-like (covered), 6 actionability-complete.

## Basis-Attestation (ls-remote develop)

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop
```

- Worktree (read-only, under /tmp/opencode): `/tmp/opencode/w225-actionability-desk-wt` checked out at exactly develop head `40cb28c758b02960356434b630086a341ebe1738`.
- `git -C /tmp/opencode/w225-actionability-desk-wt merge-base --is-ancestor 40cb28c758b02960356434b630086a341ebe1738 HEAD` → `OK develop IS ancestor of worktree HEAD`.
- `git -C /tmp/opencode/w225-actionability-desk-wt log --oneline 40cb28c758b02960356434b630086a341ebe1738..HEAD` → empty (no own commits; read-only).
- Product repo remote guard (first git action, URL contains github.com/mcpdev80):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v
lane-origin	https://github.com/mcpdev80/baseharbor.git (fetch)
lane-origin	https://github.com/mcpdev80/baseharbor.git (push)
origin	https://github.com/mcpdev80/baseharbor.git (fetch)
origin	https://github.com/mcpdev80/baseharbor.git (push)
upstream	https://github.com/mcpdev80/baseharbor.git (fetch)
upstream	https://github.com/mcpdev80/baseharbor.git (push)
```

- Planning repo remote (evidence target, verified before first evidence commit):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

- Planning main HEAD at commit time: `git -C baseharbor-plan rev-parse origin/main` → `5ed2949db42613c5294f930a9ba6a4f99b0fae1c`.

## Basis-Merges attestiert (beide im develop-Anker)

- #1717 `3653369a4 Add opaque single-use local operation grants (#1717)` — gates `AuthorizeMachineOperation` with `grantRequired=true`; ancestor of develop: `git merge-base --is-ancestor 3653369a4 40cb28c758` → confirmed via ancestor path. Gate text at `internal/operatorauth/authorization.go:285`.
- #1594 `40cb28c758 Merge pull request #1594 from mcpdev80/cli2-env-policy-head` — `0428-053 Replace name-based env policy with explicit trustedLocal policy`; removes the dev→trusted-local auto-admit that let a `!ok` principal through in managed environments. Present at develop head (this is the merge commit itself).
- Both merges are ancestors of / equal to develop anchor `40cb28c758b02960356434b630086a341ebe1738`. Read-only: no build, no rerun, no foreign-host test.

## Methode (read-only source audit)

- Single worktree at exact develop head. No matrix, no `go test`, no hosted run.
- Source read with `git show` (merge diffs), `sed`/`awk` (context), and literal `grep` witnesses below.
- Every operator-auth refusal site collected by: `grep -rn "operator_authentication_required\|Managed-environment machine operations\|Tenant-scoped machine operations\|Operator authentication is not configured\|requires a verified operator identity\|requires an authenticated operator" --include=*.go internal/ cmd/` (witness in ## suchbefehle).
- Actionability rubric per site (mission step 3): (a) does the message name the missing precondition, (b) does it name the next command, (c) does it name the path? (a)-missing = befund; (b)-missing only when the message asserts an interactive path that does not exist = befund.
- The CLI formatter that renders the message (`cmd/baha/main.go:217` `formatCLIErrorVerbose`) shows `Error` + `Affected` + `Resolution` + `What to do` (= `machine.Error.Next`). The JSON channel serializes `machine.Error` fields (`code/message/cause/next/resource/remediation_class`). The MCP channel returns the same `*machine.Error` to the tool caller. Evidence that a site has a non-empty `Next`/hint = actionability present for (b)/(c).

## 1) MELDUNGS-INVENTAR — operator-auth refusal sites

Columns: `datei:zeile | wörtliche Meldung | Kanal | a (Präbedingung genannt?) | b (Nächster Befehl?) | c (Weg?) | Rubrik / Befund`

| datei:zeile | wörtliche Meldung | Kanal | a | b | c | Rubrik / Befund |
| --- | --- | --- | --- | --- | --- | --- |
| `internal/operatorauth/authorization.go:285` | `"Managed-environment machine operations require an authenticated BaseHarbor operator."` + `Next: "Authenticate the operator for the selected Target and environment, then retry the same operation."` | machine.Error (CLI `What to do` / JSON `next` / MCP tool error) | yes — "authenticated … operator" is the named missing precondition | yes — "Authenticate the operator … then retry the same operation" | yes — authenticate operator for the selected Target/environment (path named; exact `baha login` not stated, but the path is) | (b) actionability-complete. This is the primary gate. `a` present; `b`+`c` present via `Next`. See §2 for the one caveat (no concrete `baha login` command). |
| `cmd/baha/mcp.go:301` | `"Managed-environment machine operations require an authenticated BaseHarbor operator."` + `Remediation: "authenticate the BaseHarbor operator"` + `Next: "Configure operator OIDC if required, run 'baha login' for the selected Target/environment, then retry."` | machine.Error → MCP tool error | yes | yes — explicit `baha login` named | yes — "for the selected Target/environment"; OIDC-configure path named | (b) actionability-complete. Strictly more actionable than `authorization.go:285`: it names the exact `baha login` command and the OIDC pre-step. This is the most actionable of the two identical-text sites. |
| `cmd/baha/operator_operations.go:41` | `"Operator authentication is not configured."` + `Next: "Configure operator OIDC for the selected Target/environment and log in."` | machine.Error (operator identity path) | yes — "not configured" / OIDC not configured | yes — "Configure operator OIDC … and log in" | yes — OIDC for selected Target/environment then login | (b) actionability-complete. `a`+`b`+`c` all present. |
| `internal/application/perses_management_ui.go:96` | `"The optional Perses management surface requires a verified operator identity; an anonymous request is never admitted."` | machine.Error (ErrPersesOwnershipUnknown) | yes — "requires a verified operator identity" | **no** — no next command / no login instruction | **no** — no path named | (b) **BEFUND**: missing (b) and (c). The message names the missing precondition (a: "verified operator identity") but gives no next command and no path. Perses access is an optional management surface reached via `baha status --json`; a user hitting this anonymous-denial gets the reason but not the remediation command. Note: this is the same gate family that surfaces in `app_perses_cli_test.go` (other-domain split group 6). |
| `internal/operatorauth/authorization.go:204` | `"Tenant-scoped machine operations require an authenticated operator."` + `Next: "Authenticate with the configured OIDC provider."` | machine.Error (tenant-scoped path) | yes — "authenticated operator" | yes — "Authenticate with the configured OIDC provider" | yes — configured OIDC provider (path named) | (b) actionability-complete. Tenant-scoped (verified-principal-with-membership) sub-path, not the anonymous managed gate. |
| `cmd/baha/operator_auth_boundary.go:117` | usageError `"operator authentication needs interactive setup but input is not a terminal"` + hint `"Configure operator OIDC using explicit environment settings or re-run in an interactive terminal; BaseHarbor will not prompt on piped input."` | usageError (CLI/JSON `Next`) | yes — input is not a terminal / not configured | yes — "re-run in an interactive terminal" / "Configure operator OIDC using explicit environment settings" | yes — interactive terminal OR explicit env settings | (b) actionability-complete. Non-interactive-input edge; the hint names both the cause and both remediation paths. |
| `cmd/baha/operator_auth_boundary.go:121` | prompt text `"Operator authentication is not configured. Configure it now?"` + header `"<ENV> requires authenticated BaseHarbor operator access."` | interactive prompt (TTY) | yes — "not configured" | yes — interactive prompt offers "Configure it now?" (1. Managed Keycloak, 2. External OIDC) | yes — interactive wizard path (managed-keycloak or external-oidc) | (b) actionability-complete. This is the interactive bootstrap entry; it does assert a working interactive path (unlike a bogus interactive claim). |

## 2) BEFUND — actionability deficiency (one actionable-deficiency finding)

**Site: `internal/application/perses_management_ui.go:96`** — the Perses operator-access anonymous denial names the missing precondition (a: "verified operator identity") but provides **no next command (b) and no path (c)**. A user running `baha status --json` against a managed environment without a logged-in operator receives `"The optional Perses management surface requires a verified operator identity; an anonymous request is never admitted."` with no `Next`/hint on the returned `ErrPersesOwnershipUnknown` error and no remediation command. Per mission step 3, (a)-present but (b)-missing = **befund**. This is a real gap distinct from the two primary gates (which both carry actionable `Next` fields).

- Distinct from `cmd/baha/app_commands.go:106` (already card 0428-209/210, all-targets config loss) — different site, different cause.
- Distinct from `cmd/baha/mcp.go:301` / `internal/operatorauth/authorization.go:285` — different site; those two already carry actionable `Next`.
- Family match: same `operator_authentication_required` reason-code family as `authorization.go:204` (which IS actionable) — hence "wie 0428-2xx, andere Stelle" if the coordinator folds it in, but the missing-(b)/(c) deficiency is its own defect.

**NOT a befund (actionability-complete, reported for completeness):** all other six sites (table rows 1,2,3,5,6,7) name the missing precondition (a) AND the next command / path (b/c). Notably `mcp.go:301` is the most actionable — it names the exact `baha login` command and the OIDC pre-configure step.

**Minor note (non-blocker, not a card):** `authorization.go:285`'s `Next` says "Authenticate the operator for the selected Target and environment, then retry" but does not name the concrete `baha login` command, whereas `mcp.go:301` does. This is a consistency gap, not a missing-actionability defect — the path is stated. Reported here only so the owner can decide whether to unify the wording; it is not a card.

## 3) KARTENENTWÜRFE

### Card A — Perses anonymous-denial actionability (the befund)

- **Goal:** the Perses operator-access anonymous denial (`internal/application/perses_management_ui.go:96`) must tell the user the next command to satisfy the missing precondition, not just the reason.
- **Scope (read-only evidence today; fix is an implementation decision):** `internal/application/perses_management_ui.go` line 95-97 (`operator_authentication_required` / `ErrPersesOwnershipUnknown`). Edit scope if owner assigns: the caller that surfaces `ErrPersesOwnershipUnknown` to the CLI/JSON/MCP user (`internal/application/perses_*.go` / `cmd/baha/app_perses_cli.go`). Product read-only; `.github/**` untouched.
- **Scope file list:** `internal/application/perses_management_ui.go:95-97` (message + error), caller site that renders the error to the user.
- **Acceptance criteria:** (1) the operator-authenticated-but-anonymous Perses denial surfaces a `Next`/hint or remediation naming the login path; (2) no regression to the fail-closed anonymous-denial (still denied without a verified principal); (3) CLI text + JSON `next` field + MCP tool error all carry the actionability.
- **Test-binding field:** `cmd/baha/app_perses_access_cli_test.go` (other-domain test-split group 6, `app_perses_cli.go:158`, error class `operator authentication needs interactive setup but input is not a terminal` / `Managed-environment … authenticated BaseHarbor operator`). Add a test asserting the Perses anonymous-denial message carries a `Next`/remediation. CI group: needs a real CI check reaching `app_perses_cli.go` (report exact trigger change as Owner finding if `.github/**` needed).
- **Stop criterion:** befund recorded; card closed after owner assigns fix + gating test exists in this PR.

## 4) DOPPELINGS-PRÜFUNG (mission step 4)

- `cmd/baha/app_commands.go:106` (`--all-targets` flag switch in `appListCommand`) → **already card 0428-209/210** (all-targets config loss: `internal/apierror/error.go:17` `ErrConfigMissing` / `internal/deployment/config_mutation.go:214`). Not re-reported.
- Seam error message as such → **already card 0428-204**. Not re-reported.
- The two identical-text primary gates (`authorization.go:285` / `mcp.go:301`) carry actionable `Next` — **not befund**.
- **One genuinely new site** found: `perses_management_ui.go:96` — actionability-deficient (missing b/c), reported as Card A, distinct from all above with the "wie 0428-2xx, andere Stelle" note for the shared `operator_authentication_required` family.

## 5) SUCHBEFEHLE (zeugen — literal grep runs)

```
$ grep -rn "operator_authentication_required\|Managed-environment machine operations\|Tenant-scoped machine operations\|Operator authentication is not configured\|requires a verified operator identity\|requires an authenticated operator" --include=*.go internal/ cmd/
internal/operatorauth/config.go:84:// and therefore requires an authenticated operator session instead of a trusted
internal/operatorauth/authorization.go:203:			decision.ReasonCode = "operator_authentication_required"
internal/operatorauth/authorization.go:204:			decision.Reason = "Tenant-scoped machine operations require an authenticated operator."
internal/operatorauth/authorization.go:284:			decision.ReasonCode = "operator_authentication_required"
internal/operatorauth/authorization.go:285:			decision.Reason = "Managed-environment machine operations require an authenticated BaseHarbor operator."
internal/application/perses_management_ui.go:95:		decision.ReasonCode = "operator_authentication_required"
internal/application/perses_management_ui.go:96:		decision.Reason = "The optional Perses management surface requires a verified operator identity; an anonymous request is never admitted."
cmd/baha/mcp.go:300:				CauseCode:   "operator_authentication_required",
cmd/baha/mcp.go:301:				Message:     "Managed-environment machine operations require an authenticated BaseHarbor operator."
cmd/baha/operator_auth_boundary.go:121:	configure, err := promptYesNo(bufio.NewReader(interactive.In), interactive.Out, "Operator authentication is not configured. Configure it now?", true)
cmd/baha/operator_operations.go:41:		return result, machine.NewError(machine.ErrorAuthenticationFailed, "Operator authentication is not configured.", "Configure operator OIDC for the selected Target/environment and log in.", false)

$ git -C /tmp/opencode/w225-actionability-desk-wt merge-base --is-ancestor 40cb28c758b02960356434b630086a341ebe1738 HEAD
OK

$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop
```

## repo-rule compliance

- Read-onlybefundung mission. **No product write, no PR, no hosted matrix, no workflow_dispatch, no rerun.**
- No edits to `internal/operatorauth/**`, `internal/serviceaccess/**`, `internal/identityprovider/**`, `internal/capability/perses_selection.go`, `internal/observability/registry.go`, `.github/**`. Product read-only only; `.github/**` findings reported as Owner findings (§2 note, no edit).
- No subagents (4.8); every step executed in this own session; no post to third sessions; no second owner on a card.
- Worktree scratch only under `/tmp/opencode/w225-actionability-desk-wt` (no stray files in ecosystem root).
- `git status --porcelain` on the develop worktree: empty (read-only, no product write).
- Remote witness: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` → `40cb28c758b02960356434b630086a341ebe1738`; develop IS ancestor of worktree HEAD; no own commits.

## Container / Netz / Volumen — vorher/nachher + Cleanliness

- **KEINE** Container / Compose Projects / Docker / Podman gestartet. **KEINE** SSH-Tests auf einem fremden Rechner (mission: KEIN Test auf einem fremden Rechner). No `baha-docker`/`baha-podman` host touched.
- vor: keine netzwerke/volumes/Container dieser Lane.
- nach (ps-witness, this host) — `docker ps --format '{{.Names}}'`: pre-existing foreign stacks only, none started by this lane.
- cleanliness: **clean.** No container/network/volume/state directory started by this lane. Scratch limited to `/tmp/opencode/w225-actionability-desk-wt` (partial checkout, read-only) and this akte in baseharbor-plan. Worktree removed at END.

## END

`END_DONE w225-0428-204-huntact: actionability-desk complete — 7 operator-auth refusal sites inventoried, 1 befund (perses_management_ui.go:96 missing next-command/path), 6 actionability-complete (incl. mcp.go:301 the most actionable). No product change, no PR, no matrix, no foreign-host test.`

## PLAN (nummeriert)

- baseharbor fetch + develop-sha notieren (40cb28c758b0); baseharbor-plan fetch (12fca1a → 5ed2949 at commit time) — done
- drei vorherige round-1 akten gelesen (cli-test-inventory-develop, other-domain-test-split, native-keycloak-core-cell) — done
- beide Merges attestiert: #1717 3653369a (gate 285) + #1594 40cb28c75 (auto-admit-entfernung) beide im develop-Anker — done
- Read-only-Worktree /tmp/opencode/w225-actionability-desk-wt am exact develop 40cb28c758 aufgesetzt (base-attestation ls-remote, ancestry OK, keine eigenen Commits) — done
- Meldungs-Inventar: 7 operator-auth-Abweisungsstellen inventarisiert (datei:zeile + wörtliche Meldung + Kanal + a/b/c) — done
- Frage pro Stelle rubriziert; 1 Befund (perses_management_ui.go:96, b/c fehlt), 6 handlungstauglich — done
- Doppelungsregel: app_commands.go:106 = karte 0428-209/210 (nicht erneut), seam-meldung = 0428-204 (nicht erneut); 2 identische primäre Gates (285/mcp:301) mit next = kein befund — done
- Kartenentwurf Card A (perses anonymous-denial) fertig — done
- Akte evidence/bug-hunt-2026-11-21/actionability-desk/round-1.md mit allen Pflichtsektionen geschrieben — done
- evidence zu origin/main pushen (fetch + ls-tree witness) — AM END
- scratch-worktree aufräumen (git worktree remove) — AM END
- END an coordinator-session 9142ab1f mit baseharbor-plan-sha — AM END
