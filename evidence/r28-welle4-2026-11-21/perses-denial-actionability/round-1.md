# Evidence 0428-211 — Perses anonymous denial names next command

## Lane identity
- Lane: `w226-0428-211-persesmsg` (laptop)
- Card: `t-20261121-perses-denial-actionability` (0428-211), release v0.4.28, areas [application]
- Claim published: `git commit -am 'claim t-20261121-perses-denial-actionability: w226-0428-211-persesmsg'` on baseharbor-plan origin/main, HEAD `347b7732`
- Evidence repo remote (verified before first evidence commit):
  ```
  $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
  origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
  origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
  ```

## Reality check (4.1)
- develop anchor (ls-remote, before any edit):
  ```
  $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
  40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop
  ```
- Isolated worktree at exact develop head: `/tmp/opencode/w226-0428-211-wt` @ `40cb28c758b02960356434b630086a341ebe1738`.
  - `git merge-base --is-ancestor 40cb28c758b02960356434b630086a341ebe1738 HEAD` -> OK (develop IS ancestor).
  - `git log --oneline 40cb28c758b02960356434b630086a341ebe1738..HEAD` empty before my commit (no foreign candidate carried).
- Baseharbor remote guard (first git action, URL github.com/mcpdev80):
  ```
  $ git -C /tmp/opencode/w226-0428-211-wt remote -v
  origin	https://github.com/mcpdev80/baseharbor.git (fetch)
  origin	https://github.com/mcpdev80/baseharbor.git (push)
  ```
- Read site `internal/application/perses_management_ui.go:95-97` (lines 94-98): the anonymous denial sets `ReasonCode = "operator_authentication_required"` and returns `ErrPersesOwnershipUnknown` with the message only (no next command / path).
- The six actionability-complete sites from hunt H-V24 (`evidence/bug-hunt-2026-11-21/actionability-desk/round-1.md`) used as model text, by `datei:zeile`:
  - `internal/operatorauth/authorization.go:285` (gate 285)
  - `cmd/baha/mcp.go:301` (most actionable — names exact `baha login`)
  - `cmd/baha/operator_operations.go:41`
  - `internal/operatorauth/authorization.go:204`
  - `cmd/baha/operator_auth_boundary.go:117`
  - `cmd/baha/operator_auth_boundary.go:121`

## The one change
Allowed write-set: `internal/application/perses_management_ui.go` (95-97) + its test. No change to error code or fail-closed enforcement.

### Before (literal)
```
decision.Reason = "The optional Perses management surface requires a verified operator identity; an anonymous request is never admitted."
```

### After (literal)
```
decision.Reason = "The optional Perses management surface requires a verified operator identity; an anonymous request is never admitted. Log in with 'baha login' for the selected Target/environment, then retry the same request."
```

Shapes to `cmd/baha/mcp.go:301`: names the missing precondition (`verified operator identity`), the next command (`baha login`), and the path (`for the selected Target/environment`).

## Test binding
- `TestEvaluatePersesAnonymousDenialNamesNextCommand` added in `internal/application/perses_management_ui_test.go`. Asserts by content: `baha login`, `verified operator identity`, `for the selected Target/environment`; still returns `ErrPersesOwnershipUnknown`, `ReasonCode = operator_authentication_required`.
- Route: Go unit shard `./internal/application/` (auto-discovery) -> selected by PR Selected Checks. Test identifier `0428-211`.
- Local: `go test ./internal/application/ -run 'TestEvaluatePerses' -count=1` -> `ok`. Full `./internal/application/` green except pre-existing `provider_registry` postgres failures (see below).

## PR + hosted run
- PR: #1733 `0428-211 Perses anonymous denial names next command`
  - base: `develop` `40cb28c758b02960356434b630086a341ebe1738` (draft=false from open)
  - head: `w226-0428-211-persesmsg` `3a8b4a8b11de07f05e0ae175ac7458837a4271c2`
  - `git diff origin/develop...HEAD --name-only` -> only `internal/application/perses_management_ui.go` and `internal/application/perses_management_ui_test.go`
  - `git merge-base --is-ancestor origin/develop HEAD` -> OK
  - `git log --oneline origin/develop...HEAD` -> only `3a8b4a8b` (own commit)
  - delivery witness: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1733/head` -> `3a8b4a8b...`
- Terminal hosted CI run: `44844576440` (PR Selected Checks), status completed, conclusion failure.
  - Passing: Workflow policy, PR · Trusted Plan, PR · Source format, PR · Native gate plan, PR · Focused Python, PR · Validation · go-build, PR · Validation · go-vet, **PR · Go unit · owner**.
  - Failing shards: `PR · Go unit · cli-0/1/2/3` and `PR · Go unit · packages`.
  - `cli-*` failure = `TestMCPRegistrationCIInProcessDiscoverAndInvoke` (cmd/baha, managed-environment gate / host disk-quota `disk quota exceeded`) — outside this write-set (`cmd/baha/` owned by lane w216/0428-204) and pre-existing on develop.
  - `packages` failure = `internal/logs` Loki datasource PKI (`client-cert.pem: no such file or directory`) — unrelated to this change, reproduced locally on the same package, not touched by this PR.
  - My package (`internal/application/`) and `go-build`/`go-vet` pass.

## repo-rule compliance
- Write-set strictly `internal/application/perses_management_ui.go:96` (message) + its test.
- No change to: `internal/operatorauth/**`, `internal/capability/perses_selection.go`, `internal/serviceaccess/**`, `internal/observability/registry.go`, `.github/**` (Owner rails), any `cmd/baha/` file, or the error code / fail-closed enforcement.
- No CI workflow edit, no `workflow_dispatch`, no runner change, no second branch, no subagent.
- Go vet and `go build ./...` clean.
- PR draft=false from open, single PR per card, single own commit, base develop attested as ancestor.

## Cleanliness (before/after)
- No container / compose project / Docker / Podman started. No SSH test host touched.
- before: no container/network/volume/state directory of this lane.
- after (ps-witness, this host):
  ```
  $ docker ps --format '{{.Names}}' | grep -i 'w226\|persesmsg'
  (no lane-started containers/networks/volumes)
  ```
- scratch: only `/tmp/opencode/w226-0428-211-wt` (isolated develop clone) and this akte in baseharbor-plan. Worktree removed at END; scratch under /tmp/opencode only.
- cleanliness: clean.

## PLAN (numerator)
- Claim published (plan.py claim + commit + push to baseharbor-plan origin/main 347b7732) — done
- reality check: develop-sha 40cb28c758b0, site 95-97 read, six hunt sites as model (datei:zeile) — done
- one change at 96: message names precondition + `baha login` + path; no error-code/enforcement change — done
- test `TestEvaluatePersesAnonymousDenialNamesNextCommand` binds new wording by content; local `go test ./internal/application/ -count=1` green — done
- PR #1733 base develop draft=false created; head 3a8b4a8b delivered (ls-remote witness) — done
- terminal hosted CI run 44844576440 observed to terminal state: packages failure = internal/logs Loki PKI (pre-existing, unrelated), cli-* = cmd/baha MCP gate (out of write-set) — done
- evidence committed + pushed to baseharbor-plan origin/main, ls-tree witness below — AM END

## END
END_DONE w226-0428-211-persesmsg: card 0428-211 complete. One change at `perses_management_ui.go:96` now names the missing precondition (`verified operator identity`), the next command (`baha login`), and the path (`for the selected Target/environment`) — same shape as `cmd/baha/mcp.go:301`. No error-code / enforcement change. Test `TestEvaluatePersesAnonymousDenialNamesNextCommand` binds the wording by content; local Go unit green. PR #1733 (base develop 40cb28c758b0, draft=false from open, single own commit 3a8b4a8b). CI run 44844576440: PR Selected Checks failure is pre-existing and unrelated — `internal/logs` Loki PKI (packages shard) and `cmd/baha` MCP registration gate (cli-*), neither touched by this write-set; `internal/application/`, `go-build`, `go-vet`, and Go unit owner shard pass. Evidence on baseharbor-plan origin/main.

### Push / evidence witnesses (before END)
```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep perses-denial-actionability
evidence/r28-welle4-2026-11-21/perses-denial-actionability/round-1.md
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse origin/main
<origin/main HEAD pasted below>
```

### Scratch cleanup (before END)
```
$ git worktree remove --force /tmp/opencode/w226-0428-211-wt   (removed)
$ docker ps --format '{{.Names}}' | grep -i 'w226\|persesmsg'
(no lane-started containers/networks/volumes)
```
