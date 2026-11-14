# ## PLAN — 0428-075 r4 (r5 correction)

- Read r5 REJECT verdict + r5 akte; confirm branch head `792c921cb`, provenance.
- Trace current status JSON shape + perses surface wiring.
- `capability/perses.go`: add three-state constants (`not_configured`, `configured_unverified`, `verified`) + `State()` method.
- `internal/application/management_ui.go`: compute real three-state in `ApplicationManagementUISurfaces`.
- `cmd/baha/app_status_result.go`: expose a machine-readable `perses` JSON field with the exact vocabulary.
- `cmd/baha/app_perses_cli_test.go`: positive is-equality assertion for `configured_unverified` (selected, no health proof) + unknown-owner fail-closed.
- `docs/spec/management-access-v1.md`: align Perses prose to the three states.
- Local build/vet/tests; exact-headed hosted CI; `round-6.md`; push; push evidence to origin/main; END.
