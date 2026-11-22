# 0428-245 footprint unused presenter fix - fix-round-1 akte

Sitz `w21-pr1702-0428-245-footprint-unused`. Karte 0428-245, owner-order. Aus H-V22 fund B3 (dep-freie echte karte).

GEMESSEN (H-V22, develop 64eab13e): human-readable footprint presenter laesst das Feld Unused weg, das der JSON/MCP footprint-contract meldet; zwei ausgabe-flaechen widersprechen sich fuer denselben footprint.

## PLAN

- plan in board-file + ## PLAN in akte
- develop fetchen, frische lane lane-0428-245-footprint-unused-presenter cutting von develop; merge-base --is-ancestor + base-sha witness in akte
- human-presenter (cmd/baha, app footprint show human branch) so anpassen, dass Unused konsistent zum JSON/MCP contract render-wird (oder explizit N/A wenn nicht anwendbar); NUR anzeige; KEIN contract-/guard-/daten-modell-umbau; KEIN app_candidate_consent (236/227), KEIN app_broker/237, KEIN operator_test_fixture_test.go (231), KEIN .github/scripts
- regression: assert dass human- UND JSON-footprint-flaechen fuer denselben datensatz im Unused-feld uebereinstimmen; ueber bestehende PR-CI/cli-shard gate (kein neuer CI-job, keine .github)
- EIN additiver commit, normaler push, PR fuer 245, EIN durchgang bis terminal; git diff origin/develop...HEAD --name-only in akte; cli/pr-ci job-ids (gruen); zeuge human==json fuer Unused
- akte + evidence publish zu origin/main; END; 9142ab1f posten; keine subagenten, kein merge/kommentar

## Fundquelle (H-V22 B3)

- internal/application/footprint.go:122: `Footprint.Unused []string` im canonical JSON schema (`json:"unused"`)
- internal/application/footprint.go:347-350: Unused befuellt (resloved-nicht-selected provider instances)
- cmd/baha/app_footprint_presenter.go:22 `renderAppFootprint` iteriert/druckt Unused NIEMALS -> human flaechen verliert unused
- cmd/baha/app_footprint_show.go:65-82 JSON path marshaled view.Footprint (incl. unused); human path (options.JSON=false) ruft renderAppFootprint das es wegliesst
- Same resolved view -> JSON tragt `unused: [instanceIDs]`, human druckt nichts.

## Fix

- Display-only change in renderAppFootprint (cmd/baha/app_footprint_presenter.go):
  - summary count after "No provider realizations selected." block: `Unused (resolved but not selected): %d` when len(fp.Unused) > 0
  - per-instance lines in the Details section: `- %s: resolved but not selected (unused)` for each fp.Unused instanceID
- No contract/guard/data-model change; no app_candidate_consent (236/227), no app_broker/237, no operator_test_fixture_test.go (231), no .github/scripts.
- Regression test TestAppFootprintShowHumanAndJSONAgreeOnUnused (cmd/baha/app_footprint_show_test.go): builds a Footprint with Unused=["orphaned-cache","stale-queue"], asserts human + JSON surfaces both carry the instance IDs, the count summary, and no GuidedReadContext metadata leaks.

## human vs json Unused

- SAME resolved footprint (Unused=["orphaned-cache","stale-queue"]):
  - JSON path (app_footprint_show.go:65-82) marshals view.Footprint -> JSON carries `"unused":["orphaned-cache","stale-queue"]`
  - Human path (renderAppFootprint) now prints:
    - `Unused (resolved but not selected): 2`
    - `- orphaned-cache: resolved but not selected (unused)`
    - `- stale-queue: resolved but not selected (unused)`
  - both surfaces carry the identical instance IDs and count; agreement verified by new regression test + go vet + go build green on commit ef11a3017.

## regression

- CI run 45025176987 (PR #1772) terminal conclusion: success
- jobs: PR · Validation · cli-vet (run 45025176987, job 137216617691) success; PR · Validation · cli-gofmt (job 137216617740) success; PR · Validation · cli-build (job 137216617750) success; PR · Validation · wizard-footprint-command-tests (job 137216617816) success; PR · Validation · wizard-footprint-presenter-tests (job 137216617711) success; PR · Validation · source-contracts (job 137216617724) success; PR · Focused Python success.
- local pre-check before push: go test ./cmd/baha/ -run TestAppFootprintShowHumanAndJSONAgreeOnUnused + same-authority + completeness tests -> ok; go vet ./cmd/baha/ clean; go build ./... clean.
- regression runs over existing PR-CI validation group (PR · Validation · cli-* / wizard-footprint-*); no new CI job, no .github change.

## cleanliness

(nichts geaendert ausser cmd/baha human presenter + test; keine container/volumes/state; ambient-core fremder lanes untouched)

## END w21-pr1702-0428-245-footprint-unused DONE

- branch: lane-0428-245-footprint-unused-presenter; base develop 64eab13e2 (git ls-remote origin refs/heads/develop); merge-base --is-ancestor 64eab13e2 HEAD = YES; base is ancestor of commit ef11a3017
- head: ef11a3017d2cb40f51cb6ded31877f3d57e21768 (git ls-remote origin refs/heads/lane-0428-245-footprint-unused-presenter)
- PR: #1772 (base develop, head lane-0428-245-footprint-unused-presenter, OPEN, https://github.com/mcpdev80/baseharbor/pull/1772)
- CI run 45025176987 terminal conclusion success; job ids in akte (cli-vet 137216617691, cli-gofmt 137216617740, cli-build 137216617750, wizard-footprint-command-tests 137216617816, wizard-footprint-presenter-tests 137216617711, source-contracts 137216617724)
- git diff origin/develop...HEAD --name-only = cmd/baha/app_footprint_presenter.go, cmd/baha/app_footprint_show_test.go
- git log origin/develop..HEAD = only ef11a3017 (my commit); no foreign commit
- write-set: display-only human presenter + regression test; no product contract/guard/model, no app_candidate_consent, no app_broker, no operator fixture, no .github
- no subagents, no merge, no comment
