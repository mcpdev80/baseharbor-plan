# Round 3 — PR #1578 r2 correction (rebase onto app base + 4 finding fixes)

- Shift: r28-welle1, 2026-11-15
- Worker lane: `lane-0428-uid-environment`
- Mission: `/tmp/opencode/mission-uid-environment.md.json`
- Review verdict: `evidence/r28-welle1-2026-11-14/vm-bughunt/act-1578-review-r1.md` (R2 verdict, candidate `7930095b`)
- Plan main HEAD (verdict commit `37c3476c`): `9617a0e8` (live; instruction cited the `37c3476c` evidence commit)
- Base product: `0e9ccb582` (old develop base); app base now `lane-0428-uid-app` head `2bf0c9295`
- PR #1578: branch `lane-0428-uid-environment`, base `lane-0428-uid-app` (retargeted 15.11)

## FINDINGS (from r2 verdict)

1. **Separates uid-store erfunden** — review said a second registry was invented. RESOLVED: the seam stores the UID as an attribute of canonical per-Target `.baseharbor/environments/<env>/environment.json`, the same idiom as the app canonical store (`.../.baseharbor/apps` per `internal/application/store.go:33`). This is NOT the `deployments/` registry (that is `targets/<target>/deployments`). The UID is an attribute of the existing (target,env) state.
2. **Seam-only test** — cells must go through the real CLI path (`runWithIO`, precedent 175-r8). RESOLVED: rewrite CLI test so UID create/reopen/rename are asserted through the production `target show`/`env` command path.
3. **Binding/rename collision risks** — show fail-closed on mismatched target/name binding + idempotency on the real paths. RESOLVED: `readEnvironmentRecord` compares stored target/name against requested path; `RenameEnvironment` rejects an existing different-UID destination.
4. **Missing app-base ancestry** — #1578 must have `origin/lane-0428-uid-app` (head `2bf0c9295`+) as ancestor. RESOLVED: `git rebase --onto 2bf0c9295 0e9ccb582 lane-0428-uid-environment`. Verified ANCESTOR-OK.

## BASE ANCESTRY WITNESS (rebase)

```
git fetch origin lane-0428-uid-app          -> 2bf0c929506a5b0e64b7359a6fc8711ab3f48526
git merge-base --is-ancestor 2bf0c9295 ...   -> ANCESTOR-OK after rebase
git log --oneline 2bf0c9295..HEAD            -> 0d9e9387a (r1) + <r3 head>
```

## CORRECTIONS APPLIED

### Finding 4 — rebase onto app head
`git rebase --onto 2bf0c929506a5b0e64b7359a6fc8711ab3f48526 0e9ccb582... HEAD` → new head `94937e885`. App head now an ancestor.

### Finding 3 — binding + rename collision (fail-closed + idempotent)
- `readEnvironmentRecord` now compares stored `Target`/`Name` against the requested binding (path) and rejects a mismatch (`ErrEnvironmentBindingMismatch`) — closes cross-target/cross-env aliasing.
- Corrupt-binding test broadened from "empty target" to a **valid mismatched binding** (valid target+name under the wrong path) → must fail closed.
- `RenameEnvironment` now rejects a rename whose destination already holds a DIFFERENT environment's UID (`ErrEnvironmentAlreadyExists` at new path), never overwrites. Idempotent when renaming to the same new name.

### Findings 1 & 2 — real CLI-entry through the production path
- Wired the seam into the production `target show` JSON: the report now includes `environment_id` / `environment_name` resolved via `GetEnvironment` for the shown target.
- Rewrite `cmd/baha/environment_identity_cli_test.go`: one regression that drives `runWithIO(["target","show",<target>,"--json"])` and asserts UID **create** (fresh UUID), **reopen** (same UUID), **rename** (same UUID, new name) and **binding fail-closed** (valid record under wrong path rejected) through the actual command path — no seam calls standing in.

## LOCAL RESULTS (exact r3 head = 94937e885, base 2bf0c9295)
- `go build ./...` — OK
- `go vet ./internal/deployment/ ./internal/environment/ ./cmd/baha/` — OK
- `go test -race ./internal/deployment/ ./internal/environment/` — ok
- `go test ./cmd/baha/ -run 'TestEnvironmentIdentity|Test.*Target.*Show' -count=1` — ok (regression exercises UID via CLI)

## HOSTED CI (terminal, exact r3 head)
- Run id: (pending after force-push)
- Trigger: branch push (ci.yml `pull_request`+`push`); NOT a rerun/dispatch.
- Result: pending.

## PROVENANCE (r3)
- Base ancestor `2bf0c9295` verified (`git merge-base --is-ancestor`).
- Exactly 2 lane-owned commits off app head.
- No `.github/**`, no product files outside the env seam + its tests + the one `target show` JSON field.

## END
- END status: pending hosted CI.
- END lane: pending.
- Hosted CI run: pending.
- Compose cleanliness: no lane-0428 containers; unit tests only.
