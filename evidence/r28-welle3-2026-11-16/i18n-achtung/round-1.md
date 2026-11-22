# i18n-Achtung — round-1 evidence (card 0428-093, task t-20261115-bughunt-d28-i18n-achtung)

- Mission: `/var/tmp/missions/mission-093-i18n-achtung.md`
- Card: `0428-093` / `t-20261115-bughunt-d28-i18n-achtung` (BF-04 from H-D28, akte `evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md`)
- Rolle: WORKER — implement, test, deliver draft PR (NO merge, NO ready_for_review, NO force-push, NO subagent)
- Branch: `lane-0428-093-i18n-abachtung` cut from develop HEAD (see base attestation below)
- Base SHA (attestation): `34c2ede594afc215b1e46eea251a587162224aa0` = `origin/develop` HEAD (ls-remote witness below)
- Evidence path lives in baseharbor-plan ONLY (product repo gets code only)

## ## PLAN

 - 0. Reality witnesses: remote develop HEAD via ls-remote, planning-repo verify
 - 1. Confirm the 15 Germanism sites (grep -rn "Achtung", non-test) match the H-D28 finding
 - 2. Scope decision: user output "Achtung:" -> "Warning:" + contract marker value rename "Achtung" -> "Warning" + consumer/golden/docs consistency
 - 3. Edit the 15 product Go sites (9 user output + 3 contract setters + contract schema consts)
 - 4. Pull golden/testdata + demo golden rules + English docs consistent (German docs stay German)
 - 5. Regression test covering one output case + one JSON-contract case, wired into an existing CI group
 - 6. build / vet / gofmt
 - 7. Push via refspec (draft PR), run to terminal state
 - 8. Evidence to origin/main, teardown compose/containers, END post

## Reality witnesses

```
$ git ls-remote --heads https://github.com/mcpdev80/baseharbor.git develop
34c2ede594afc215b1e46eea251a587162224aa0	refs/heads/develop
```

Base attestation — branch cut from develop HEAD:
```
$ git rev-parse origin/develop
34c2ede594afc215b1e46eea251a587162224aa0
$ git rev-parse HEAD
34c2ede594afc215b1e46eea251a587162224aa0
$ git merge-base HEAD origin/develop
34c2ede594afc215b1e46eea251a587162224aa0   # == base, no foreign candidate carried
```
Base SHA `34c2ede5...` is an ancestor of the first commit (same SHA; the diff lands on top of develop HEAD).

## Befund: the 15 Germanism sites

grep -rn "Achtung" --include="*.go" (non-test) — exactly 15, matches H-D28 BF-04:

User output (English, user-visible "Achtung:" prefix — the actual Germanism):
- cmd/baha/control_plane_stop_impact.go:180
- cmd/baha/node_disconnect_client.go:158
- cmd/baha/target_definition_change.go:33
- cmd/baha/application_stop_impact.go:189
- cmd/baha/runtime_destroy_impact.go:178
- cmd/baha/runtime_destroy_impact.go:180
- cmd/baha/provider_change_confirmation.go:42
- cmd/baha/provider_change_confirmation.go:82
- cmd/baha/provider_change_confirmation.go:84
- cmd/baha/provider_change_confirmation.go:104
- cmd/baha/application_restore_authorization.go:158

Contract marker value setter "Achtung" (machine-readable `attention` field):
- internal/application/provider_change_scope.go:59  s.Attention = "Achtung"
- internal/application/provider_change_plan.go:93    p.Attention = "Achtung"
- internal/application/provider_change_plan.go:98    p.Attention = "Achtung"

All 15 non-test .go sites (full grep):

```
cmd/baha/control_plane_stop_impact.go:180        fmt.Fprintln(out, "Achtung: review this selected Core stop, affected consumers and retained recovery locations.")
cmd/baha/node_disconnect_client.go:158           fmt.Fprintln(out, "Achtung: review node access loss and all known Core/local recovery owners.")
cmd/baha/target_definition_change.go:33          fmt.Fprintln(out, "Achtung: review this Target access change, retained data and actual recovery location.")
cmd/baha/application_stop_impact.go:189          fmt.Fprintln(out, "Achtung: review the current application stop, affected consumers and retained recovery locations.")
cmd/baha/runtime_destroy_impact.go:178           fmt.Fprintln(out, "Achtung: permanent destruction requires two current-plan confirmations and separate data-deletion consent.")
cmd/baha/runtime_destroy_impact.go:180           fmt.Fprintln(out, "Achtung: selected runtime removal requires two current-plan confirmations; persistent data and protected owners remain.")
cmd/baha/provider_change_confirmation.go:42      fmt.Fprintln(out, "Achtung: review the concrete consequences and required acknowledgements below.")
cmd/baha/provider_change_confirmation.go:82      label = "Achtung: confirm the displayed changes and permanent data deletion"
cmd/baha/provider_change_confirmation.go:84      label = "Achtung: confirm the displayed outcome without a working alternative"
cmd/baha/provider_change_confirmation.go:104     fmt.Fprintf(out, "Achtung: separately authorize permanent deletion of the displayed owned data (plan %s)? [y/N]: ", plan.PlanID)
cmd/baha/application_restore_authorization.go:158 fmt.Fprintln(out, "Achtung: restore can overwrite newer owned data. ...")
cmd/baha/provider_external_removal.go:36         fmt.Fprintln(out, "Achtung: review all Target bindings and the unknown live access consequences.")
internal/application/provider_change_scope.go:59 s.Attention = "Achtung"
internal/application/provider_change_plan.go:93  p.Attention = "Achtung"
internal/application/provider_change_plan.go:98  p.Attention = "Achtung"
```

## Scope decision (documented, not parked)

The value "Achtung" is a machine-readable contract marker (`attention` field):
- JSON schema `const` (normative): contracts/provider-impact/v1/scope.schema.json, contracts/provider-impact/v1/impact.schema.json
- Set as a canonical marker in 3 Go sites
- Asserted by 30+ test sites (`!= "Achtung"`)
- Consumed by presence, not by literal: demo `tests/fixture-consent.py:28` reads `plan.get("attention")` truthy; Go logic checks `!= ""` (presence). No external consumer (console/demo/docs) matches the literal "Achtung" for the contract field.
- User-output golden rules in baseharbor-demo tests/guided/drive.py match the literal "Achtung:" prompt prefix (lines 507-508, 203).

Decision (both options allowed by mission: "string-wert korrigieren ODER feld-praezisierung"):
- User output (English, user-visible): "Achtung:" -> "Warning:" (precedent exists in provider_change_presentation.go "Warning:").
- Contract marker value: rename canonical "Achtung" -> "Warning" across setter (3) + schema const (2) + golden/testdata (2) + the 30+ test assertions. Internal and uniform, so the rename preserves structural integrity and removes the Germanism from the machine contract too.
- Consumer pull (golden dateien konsistent nachziehen):
  - baseharbor-demo tests/guided/drive.py: match "Warning:" instead of "Achtung:".
  - English docs (docs/**, contracts/README.md) reference the contract marker in prose; align to "Warning".
  - German docs (docs/de/**) are German by design: "Achtung" is correct there, LEFT UNCHANGED.
- NOT in scope: translating every "Achtung" in the repo; German docs; .github/** (Owner scope).

## Repo-rule compliance

- Only product files under my write-set edited; no .github/** touched; no merge; no ready_for_review; no force-push; no subagent.
- Contract change scoped to the `attention` marker only; no behavioral logic change (logic only checks presence).
- German docs untouched.

## TODO

- Evidence committed and on origin/main (second-to-last action)
- Draft PR pushed via refspec, run to terminal state (Eigenes-run-pflicht)
- Compose/container teardown before END

## Evidence: CI run (Eigenes-run-pflicht, terminal SUCCESS)

Run `43950312560` on exact head `55550400c1e41769d646fb73864b66d91606bf70`:
```
$ gh api repos/mcpdev80/baseharbor/actions/runs/43950312560
run_id=43950312560 status=completed conclusion=success event=pull_request sha=55550400c1e41769d646fb73864b66d91606bf70
```
Jobs: `PR · Draft Go · cli-0/1/2/3` = success; native/runtime/Demo/HA = skipped (draft, no native runtime required). My regression test runs under the `release_source_preflight` "Run release-source tests" step (`ci.yml:125`, `go test ./cmd/baha`) — durable GitHub CI evidence, no `.github` change needed (existing group covers `cmd/baha`).

First run 43950312560 was CANCELLED (concurrency cancellation); re-triggered `gh run rerun 43950312560` and watched to terminal SUCCESS.

## END

END_DONE lane-0428-093-i18n-abachtung: i18n Achtung localized. 15 non-test sites (9 user output + 3 contract setters + contract schema consts + 30+ test assertions + golden/testdata) changed Achtung->Warning. Draft PR #1663 base develop, head 55550400, 51 files. CI run 43950312560 (sha 55550400) TERMINAL SUCCESS; cli-0/1/2/3 Go shards pass; regression TestProviderImpactConsequenceHintIsEnglishOutputAndContractMarker runs under release_source_preflight 'go test ./cmd/baha' (ci.yml:125), no .github change needed. Evidence on origin/main b127c1c2. Compose: none started this lane.

## Findings for Owner (out of this lane's write-set)

1. baseharbor-demo golden rules in tests/guided/drive.py match the CLI prompt text literally:
   - drive.py:507-508 `(?:Confirm the displayed provider changes|Achtung: confirm the displayed outcome without a working alternative)`
   - drive.py:203 same alternation
   - new_edit_helpers_test.py:190 matches `Achtung: separately authorize permanent deletion...`
   These need the same Achtung->Warning update in baseharbor-demo for the demo acceptance run to pass against this candidate. baseharbor-demo is a pinned consumer; not editable from the product branch. Report for Owner to land.
2. German docs (docs/de/**) intentionally left "Achtung" — correct, out of scope.
3. Contract value "Warning" is read by baseharbor-demo tests/fixture-consent.py:28 by presence (`plan.get("attention")`), not by literal — the presence check is unaffected by the rename.

