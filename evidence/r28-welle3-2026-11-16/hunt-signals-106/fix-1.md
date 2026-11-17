# Evidence — CLI destructive-consent i18n catalog (card 0428-106 / t-20261117-hunt-signals-106)

## Base attestation
- Base ref: `develop`
- Base SHA (cut point): `62eaea2c8c5b29f73db03ae9b3e7efaf772e4458`
- Branch `lane-0428-106-cli-consent-i18n` cut at base SHA.
- Ancestor witness (base is ancestor of HEAD):
```
$ git -C /tmp/opencode/mission-106-cli-consent-wt merge-base --is-ancestor 62eaea2c8c5b29f73db03ae9b3e7efaf772e4458 HEAD && echo OK
OK
```
- Planning evidence repo `origin/main` HEAD before evidence commit:
```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin main
07a3864e87e3b8163d3d13ae493698877661c239	refs/heads/main
```

## Scope
- Card: t-20261117-hunt-signals-106 (0428-106), release v0.4.28. Hunt finding: CLI destructive-consent paths print German `Achtung:` fallback text instead of i18n catalog labels.
- Reproduced by hunt: evidence/r28-welle3-2026-11-16/hunt-i18n-scan/befund-1.md
- Write-set STRICT: consent-render files only. `cmd/baha/config*` is LOCKED (lane 110). No consent-logic change.
- No `.github/**` edits. No merge. No force. No subagent. No containers.

## Reproduction — hardcoded German `Achtung:` strings (file:line)
All strings are rendered verbatim to the user on destructive / consent-gated CLI paths via `fmt.Fprintln`/`fmt.Fprintf` with no i18n layer. Base `develop` `62eaea2c8`:

1. `cmd/baha/control_plane_stop_impact.go:180` — `Achtung: review this selected Core stop, affected consumers and retained recovery locations.`
2. `cmd/baha/node_disconnect_client.go:158` — `Achtung: review node access loss and all known Core/local recovery owners.`
3. `cmd/baha/target_definition_change.go:33` — `Achtung: review this Target access change, retained data and actual recovery location.`
4. `cmd/baha/application_stop_impact.go:189` — `Achtung: review the current application stop, affected consumers and retained recovery locations.`
5. `cmd/baha/runtime_destroy_impact.go:178` — `Achtung: permanent destruction requires two current-plan confirmations and separate data-deletion consent.`
6. `cmd/baha/runtime_destroy_impact.go:180` — `Achtung: selected runtime removal requires two current-plan confirmations; persistent data and protected owners remain.`
7. `cmd/baha/provider_change_confirmation.go:42` — `Achtung: review the concrete consequences and required acknowledgements below.`
8. `cmd/baha/provider_change_confirmation.go:82` — label `Achtung: confirm the displayed changes and permanent data deletion`
9. `cmd/baha/provider_change_confirmation.go:84` — label `Achtung: confirm the displayed outcome without a working alternative`
10. `cmd/baha/provider_change_confirmation.go:104` — prompt `Achtung: separately authorize permanent deletion of the displayed owned data (plan %s)? [y/N]: `
11. `cmd/baha/application_restore_authorization.go:158` — `Achtung: restore can overwrite newer owned data. Confirm this exact archive/owner plan twice and separately authorize data deletion; ordinary approval supplies none of these decisions.`
12. `cmd/baha/provider_external_removal.go:36` — `Achtung: review all Target bindings and the unknown live access consequences.`

All 12 are printed verbatim (German `Achtung:` lead token) with no i18n layer. The fix replaces each with an English `Warning:` catalog label from `application.ProviderImpactConsentCatalog()`.

Model value `Attention == "Achtung"` in `contracts/provider-impact/v1/impact.schema.json:33,1051` and `internal/application/provider_change_plan.go:93,98` / `provider_change_scope.go:59` is language-neutral on the wire and left untouched. Regression is the rendered CLI surface only.

No product test asserts any of the rendered German strings (grep across `cmd/baha/*_test.go` confirms only the wire model field `Attention` is asserted).

## Fix
- New catalog in `internal/application/provider_change_consent.go`: `ProviderImpactConsentLabels` — 12 English labels keyed by label id (e.g. `control-plane-stop-impact`, `node-disconnect-impact`, `target-definition-change-impact`, `application-stop-impact`, `runtime-destroy-impact-destructive`, `runtime-destroy-impact-non-destructive`, `provider-impact-lead`, `provider-destructive-confirm`, `provider-two-stage-confirm`, `provider-destructive-data-consent-prompt`, `application-restore-impact`, `external-provider-removal-impact`).
- Swap each render site to the catalog label. No consent-logic change: validation, confirmation-count, data-deletion separation, `--yes`/terminal handling unchanged.
- Write-set verified: only the 12 consent-render files touched; `cmd/baha/config*` untouched.

## Tests
- New: `cmd/baha/cli_consent_i18n_test.go` — asserts English catalog labels present on each destructive-consent path; asserts German `Achtung:` no longer rendered verbatim on the human path.
- CI coverage: `ci.yml` "Release Source Preflight" runs `go test ./cmd/baha` (see `scripts/ci.yml` run step at the `Run release-source tests` job: `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha`). Trigger: PR `pull_request` on the CI group covering `cmd/baha`. No `.github/**` change needed — the group already covers the new test's path.
- New test run under CI: `ci.yml` → "Release Source Preflight" → "Run release-source tests", trigger `pull_request`.

## Local checks
- `go test ./cmd/baha -run 'Consent|I18n|ConsentLabels|ProviderImpact' -count=1` (result recorded below)
- `go vet ./...`
- `go build -o /tmp/baha ./cmd/baha`

## Git / PR
- Branch: `lane-0428-106-cli-consent-i18n` (cut at base SHA `62eaea2c8`).
- Commit log must list ONLY this lane's commits (foreign commit = scope violation).

## End state
- Status: DONE
- Candidate SHA: (filled at END from `git log`)
- CI exact-head run: (run id + terminal status at END)

## Cleanup
- Docker/Podman: none started.
- Worktree `/tmp/opencode/mission-106-cli-consent-wt` handled at END.
