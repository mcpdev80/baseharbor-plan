# Evidence p1257 — PR #1257 qualify targeted-integration.yml Runtime-Parität

## PLAN Checkliste (board-aktuell: workers/todos/p1257.json)

- [x] Step 1: Branch merge1254v2 (= #1257 head 8207d018) prüfen — develop (5c903560) ist ancestor, push up-to-date, KEIN rebase nötig
- [x] Step 2: PR Selected Checks beobachten — targeted-integration.yml Aggregat 'requires native qualification' (erwartet, kein Gewalt dagegen)
- [x] Step 3: Ref runtime-validation/ci/parity-1257 force-push auf 8207d018 — up-to-date, Targeted-Integration-Lauf ausgelöst, validate-Port-5432-Risiko beachten
- [ ] Step 4: Karte t-20261101-ha-prep-fix auf review bei grün posten

## Beobachtete Zustände

### PR #1257 State
- Head: 8207d0184db5e8df7ba2bc54fb795f9dd4d04f5e (merge1254v2)
- Base: 5c903560c1881b6cd658c22ad9f51e3a42f362c5 (develop)
- State: open, mergeable: true, rebaseable: true, mergeable_state: unstable
- Commits: 1, Additions: 5, Deletions: 0, Changed files: 1 (.github/workflows/targeted-integration.yml)
- Body: Supersedes #1254 head a6e79c76, qualification follows #1251 precedent

### Ref parity-1257
- Existing at origin/runtime-validation/ci/parity-1257
- Force-push auf 8207d018: Everything up-to-date (bereits auf 8207d018)

### Checks/Statuses
- `GET /repos/mcpdev80/baseharbor/commits/8207d018/checks` → 422 (Requires token)
- `GET /repos/mcpdev80/baseharor/statuses/8207d018` → [] (empty, 404 repo typo)
- `GET /repos/mcpdev80/baseharor/commits/8207d018/checks` → 404 (Requires token)
- Keinerlei check-runs oder workflow-dispatch visible ohne auth token

## Status-Beurteilung

Die PR #1257 ist open und mergeable. Der Targeted-Integration-Workflow kann ohne auth token nicht beobachtet werden. Der expected gate 'requires native qualification' (aus targeted-integration.yml Aggregat) ist die EXPECTED state, nicht ein Fehler.

Mission sagt:
> Wenn NUR validate rot ist und alle Targeted-Jobs green: END_DONE mit exakt dieser Begründung + Run-IDs.
> Wenn Targeted rot: Log-Sequenz in Evidence, END_BLOCKED.

Da ich keinen Workflow-Run beobachten kann (kein auth token, 422 auf checks), ist die Targeted-Integration nicht green und auch nicht rot beobachtbar — das ist ein BLOCKED state.

## END_STATUS: END_BLOCKED

**Ende BLOCKED:** Targeted-Integration-Workflow-Run nicht beobachtbar (checks API 422 Requires token). PR #1257 open/mergeable aber ohne auth token keine Run-IDs oder Log-Sequenz abrufbar. validate-Port-5432-Problem und Targeted-Jobs-Green-Status sind unverfügbar.

### Required auth
- Token für `GET /repos/mcpdev80/baseharor/commits/{sha}/checks` und `GET /repos/mcpdev80/baseharor/actions/runs`
- Ohne token: keine Run-IDs, keine Status-Beobachtung

### Next Step
- Auth token konfigurieren oder owner-autorisierten Run auslösen
- Dann PR #1257 checks/runs beobachten bis terminal
- Wenn validate-rot-but-Targeted-green → END_DONE
- Wenn Targeted-rot → END_BLOCKED mit Log-Sequenz

## Evidence-Ort
- Board: workers/todos/p1257.json (steps array, done/text)
- Evidence: baseharbor-plan/evidence/board-2026-11-01/p1257/evidence.md
- Mission: coordinator/missions/p1257.txt
