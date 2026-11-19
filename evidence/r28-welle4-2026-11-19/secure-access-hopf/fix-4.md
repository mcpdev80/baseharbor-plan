# 0428-089 fix-4 — base-distance re-hop (mission-089, follow-up command)

Lane: 089-compose-config-render · Card: t-20261114-r28-perses-secure-access · PR: #1599
Candidate head: 69982520688e18a5c9bad89f093165c16d5be5d4
Exact-head run: (run id filled at terminal state below)
Planning clone: /var/tmp/m089-plan-clone, remote verified `git remote get-url origin` -> https://github.com/mcpdev80/baseharbor-plan.git (this file is committed from there, nothing in the shared local working copy).

## PLAN

1. [x] fetch --prune + ls-remote develop -> fac01c77276ca2bf1e20cd0b7334bda5dd43e353
2. [x] ONE monotone merge-hopf of origin/develop (no rebase, no force): new head 699825206
3. [x] merge-tree --write-tree origin/develop <new head> + conflict count
4. [x] base-abstand diff 859654861..fac01c772, word-for-word (proves why a new run was needed)
5. [x] focused checks (build/vet/test cmd/baha -run Perses/source-readability), no full ./...
6. [x] ci-fast-check.sh before push, PASS
7. [x] push fast-forward 233be0af2..699825206, draft=false held
8. [x] exact-head run watched to terminal (§4.6); cells read literally (below)
9. [x] this akte on origin/main of baseharbor-plan
10. [x] END with 40-char head + PR state + terminal run

## Head sequence

31adf08fa (review verdict) → 233be0af2 (fix-2 candidate, run 44535875227 SUCCESS) → 699825206 (this re-hop; same content, newer base).

- Hop witnesses: `git merge-base --is-ancestor origin/develop 69982520688e18a5c9bad89f093165c16d5be5d4` -> true; `git merge-base --is-ancestor 233be0af2bba691fed7bd99655fb78a7515e2a0f 69982520688e18a5c9bad89f093165c16d5be5d4` -> true. One merge commit, no rebase, no force. Push witness: `233be0af2..699825206  HEAD -> lane-welle2-089-perses-secure-access` (fast-forward).
- `git merge-tree --write-tree origin/develop 699825206` -> exit 0, tree eb47aae8f1cba47d633cf44f3aab05c22814cfb3, 0 conflicted files.
- Content identity: `git diff --name-only 233be0af2..699825206 | grep -iE "perses|serviceaccess"` -> 0 files. The merge brought only develop's own content (14 files).

## base-abstand diff (why the new run was required), `git diff --name-only 85965486154284d4ae7974573f504002335d4523 origin/develop`:

- `.github/workflows/ci.yml` (MIGRATION_CONTROLLER re-pinned to the lane-compatible controller; changes the trusted planner the run evaluates)
- `scripts/test_ci_check_routes.py`
- `internal/application/runtime_observability.go`, `internal/application/runtime_observability_test.go`, `internal/application/runtime_observability_trace_source_test.go`
- `internal/application/runtime_postgres.go`
- `internal/logs/appclass_log_writer_identity_test.go`, `internal/logs/appclass_log_writer_test.go`, `internal/logs/appclass_writer_implicit_selection_test.go`, `internal/logs/application_source.go`, `internal/logs/realization.go`
- `internal/observability/environment.go`, `internal/observability/registry.go`, `internal/observability/registry_log.go`

The first two are exactly the CI-half files the coordinator's queue563 base-distance rule counts: the trusted native planner of run 44535875227 evaluated a different controller, so that run's aggregate is not end-proof for this head. Per §5.4 the unit-level Go evidence for unchanged candidate files is reused from 44535875227 (identical hashes, below); the new run must qualify at least the planner/aggregate cells.

## Candidate hashes (byte-identical at 233be0af2 and 699825206)

- `96503b1e2e17cf6c163190cb301c98ca3e6c6e8dbcefd904b03d6b924529862e  internal/serviceaccess/perses_gateway.go`
- `964c38e3be20fffe3a6352273dedb3dfe6e4b74aea0839b87ed873abc2f53d8f  internal/serviceaccess/perses_config_render.go`
- `29e13dec1f7dbf259bca94ddb22289bc0ebbf3d625cca09fa9d148710a5eda85  internal/serviceaccess/perses_gateway_test.go`
- `47d0022ba06e8b67f3341d67425cb75cda186758284ccc47b77c1ef3600ddf6b  internal/serviceaccess/perses_gateway_integration_test.go`
- `f4a6900b4c87902ad1292dbc0d7526f1cf962bc935c06246582c33cdfe48e916  internal/serviceaccess/perses_config_render_test.go`
- `64de7acdeaecc731baac8cba3350ccd26ab851a8c208a8097c699bec12eb88b3  internal/application/perses_runtime.go`
- `d38d98524d249478780fe2cd2d1c4103eb3c56adc66733d79acfc8e270457914  internal/capability/perses_security.go`

## Focused local checks on 699825206 (no full ./... run)

- `go build ./...` clean; `go vet ./cmd/baha ./internal/machine` clean.
- `go test ./cmd/baha -run "^Test(AppPerses|PersesAccess|PersesLifecycle)" -count=1` ok (8 test functions executed, all pass); `-v` witness: 8 RUN blocks.
- `go test ./internal/serviceaccess ./internal/application ./internal/capability -run Perses -count=1` all ok (candidate content unchanged, executed as cheap regression guard after the hop).
- `bash scripts/source-readability-audit.sh`: size/function/ratchet PASS.
- `bash scripts/ci-fast-check.sh` before the push: PASS (gofmt, readability, workflow policy 20 files, actionlint, 275 python route/gate tests OK, advisory line "No candidate-added validation checks. The trusted base plan remains the only merge requirement.").

## Exact-head run (terminal, §4.6)

- Run 44544947599 on head 69982520688e18a5c9bad89f093165c16d5be5d4, watched to terminal via `gh run watch` (exit 0): completed, conclusion SUCCESS. 41 jobs: 21 executed (conclusion success), 20 skipped. Skipped cells are not claimed as proof.
- Cells read literally: `PR Selected Checks` = SUCCESS (aggregate). `PR · Native gate plan` = SUCCESS (planner ran from the trusted develop policy including the 695ad5494 controller pin). `PR · Exact Candidate` = skipped (no base-owned candidate matrix selected for this pure renderer/adapter diff). `PR · Candidate-added checks (advisory)` = skipped with aggregate output `candidate_advisory_required: "false"` — the diff adds no candidate-owned validation outside the required plan; per the owner directive such checks would be advisory and non-blocking anyway. `Targeted HA · docker` = skipped, `Targeted HA · podman` = skipped — not self-triggered per command. The unit evidence cells covering the new Perses tests (`PR · Go unit · packages`) and cli (`PR · Go unit · cli-0..3`, incl. cmd/baha) plus go-build/go-vet/gofmt/documentation-audit executed SUCCESS.

## Vermerk (correction of the first END)

The first END sentence was factually right — candidate content, run result and evidence all as reported — and ONLY the base was missing: run 44535875227 qualified on 233be0af2 whose base 859654861 predates develop's fac01c772/695ad5494. Per the base-distance rule that run counts as interim, not end-proof; this re-hop and run 44544947599 replace it. No second branch, no product change between the two heads (content identity above).

## repo-rule compliance

- One candidate per chain, monotone merges only, no force, no rebase, no merge performed by this lane.
- Shared-file exclusion respected: cmd/baha/{commands,completion,machine_coverage,perses_lifecycle*}.go and the three docs files were NOT touched by this hop (develop side had no conflict there; `git diff --name-only 233be0af2..699825206` contains none of them); no conflict-resolution sites exist in this merge.
- `.github/**`, `scripts/**` untouched (Owner scope); no runner infrastructure touched; no runtime/release matrix self-triggered.
- Rulesets/merge protection: not claimed active (deactivated per last verified state); nothing was bypassed.

## Cleanliness

cleanliness: docker ps before == after on the coordinator host (only the 7 ambient bh-local-shared-* of other karren); no lane-owned container/network/volume/state directory; evidence committed only from /var/tmp/m089-plan-clone against the GitHub origin, zero git actions in /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan.

## Handoff / END

- Candidate: 69982520688e18a5c9bad89f093165c16d5be5d4 on `lane-welle2-089-perses-secure-access`, PR #1599 (state OPEN, draft=false, headRefOid 699825206).
- Runs: 44535875227 SUCCESS on 233be0af2 (interim per base-distance), 44544947599 SUCCESS on 699825206 (end-proof, base = develop fac01c772).
- Reviewer: Codex Luna re-review against the 1599-0428-089 REQUEST-CHANGES recipe; fix-2.md carries the implementation detail, this file the hop/run mechanics.

END_DONE mission-089-compose-config-render.md: base-distance re-hop landed, candidate 69982520688e18a5c9bad89f093165c16d5be5d4, exact-head run 44544947599 SUCCESS with PR Selected Checks=SUCCESS and candidate_advisory_required=false; PR #1599 open draft=false; evidence on origin/main.
