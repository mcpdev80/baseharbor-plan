# Befund 1 — CLI destructive-scope warning strings are German fallback text

- file:line: multiple, `cmd/baha/*.go`
- Type: consumer-visible CLI string (user-facing output)
- SHA base: `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`
- Repo: `https://github.com/mcpdev80/baseharbor.git`

## Finding
Twelve live `Achtung:` strings are printed verbatim to the end user on destructive / consent-gated CLI paths. They are German fallback/label text rendered directly by `fmt.Fprintln`/`fmt.Fprintf` with no i18n layer.

Lines:
- `cmd/baha/control_plane_stop_impact.go:180` — `Achtung: review this selected Core stop, affected consumers and retained recovery locations.`
- `cmd/baha/node_disconnect_client.go:158` — `Achtung: review node access loss and all known Core/local recovery owners.`
- `cmd/baha/target_definition_change.go:33` — `Achtung: review this Target access change, retained data and actual recovery location.`
- `cmd/baha/application_stop_impact.go:189` — `Achtung: review the current application stop, affected consumers and retained recovery locations.`
- `cmd/baha/runtime_destroy_impact.go:178` — `Achtung: permanent destruction requires two current-plan confirmations and separate data-deletion consent.`
- `cmd/baha/runtime_destroy_impact.go:180` — `Achtung: selected runtime removal requires two current-plan confirmations; persistent data and protected owners remain.`
- `cmd/baha/provider_change_confirmation.go:42` — `Achtung: review the concrete consequences and required acknowledgements below.`
- `cmd/baha/provider_change_confirmation.go:82` — label `Achtung: confirm the displayed changes and permanent data deletion`
- `cmd/baha/provider_change_confirmation.go:84` — label `Achtung: confirm the displayed outcome without a working alternative`
- `cmd/baha/provider_change_confirmation.go:104` — prompt `Achtung: separately authorize permanent deletion of the displayed owned data (plan %s)? [y/N]: `
- `cmd/baha/application_restore_authorization.go:158` — `Achtung: restore can overwrite newer owned data. Confirm this exact archive/owner plan twice ...`
- `cmd/baha/provider_external_removal.go:36` — `Achtung: review all Target bindings and the unknown live access consequences.`

## User impact
HIGH. These appear on destructive / irreversible operations (stop, destroy, restore, provider change, disconnect, Core stop). `Achtung:` is the German "Warning/Caution" and is the lead token of a safety-critical consequence notice. A German-speaking operator reads it as an intended warning; an English-speaking operator sees an untranslated word embedded in an English sentence — a genuine i18n regression that degrades the warning's visibility.

## Context
- The value `Achtung` is also a **model const** in `contracts/provider-impact/v1/impact.schema.json:33` and `:1051` (`attention: { const: Achtung }`) and set in `internal/application/provider_change_plan.go:93,98` / `provider_change_scope.go:59`. That model value is language-neutral on the wire; the regression is the **rendered CLI surface**, not the data model.
- No i18n / locale / string-bundle directory exists in the repo (searched). The German text is hardcoded in Go string literals.
- Untouched by cards 093 (Achtung->warning dual-match) and 099 (demo consumer rename). Git log shows these strings descend from v0.4.25 capability-contract work (PR #905).
