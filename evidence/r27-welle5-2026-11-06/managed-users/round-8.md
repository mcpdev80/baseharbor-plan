# Round 8 evidence — managed-users activation empty-body fix (t-20261018-r27-managed-users)

- Mission: `coordinator/missions/w265-mu-emptybody-fix.txt` (KARTE t-20261018-r27-managed-users, RUNDE 8).
- Coordinator: ec2254ac. Lane: w265-mu-emptybody-fix.
- PR: #1397, branch `work/r27-managed-users`. Same PR, same chain (AGENTS 3.8). No second PR.
- Base at testate: cut from `b880f91e24a9338ffa75a9006ab7d26cad65a714` (round-7 head = current PR #1397 head).
  `git merge-base HEAD b880f91e24a` = `b880f91e24a`; `git merge-base --is-ancestor origin/develop HEAD` rc=0.
- Review applied: `act-1397f.md` (CODEX-REVIEW round 8, REJECT).

## PLAN (PUNKTE statt Checkboxen)

- Pflicht 1 (Fixture-Umbau): `TestInviteManagedUserActivationEmptyBodyIsRefused` so umbauen, dass der post-create (resolve-after-create) lookup den NEU angelegten, eigentums-erfuellten benutzer (managed-invite marker, enabled, emailVerified=false) zurueckgibt und die ECHTE aktivierungs-anfrage (/execute-actions-email) erreicht wird; haupt-fixture, route, version-guard UNVERAENDERT.
- Pflicht 2 (kausale Mutanten-Doktrin): in ISOLERTER kandidat-kopie den production `requiredActions`-wert auf nil setzten (payload=>nil) => dieselbe zelle faellt ROT (fail-closed guard); exaque quelle zurueck => GRUEN aus DERSSELBEN zelle. Roh-transcript + vorher/nachher-datei-hash.
- Pflicht 3: fokessierte identityprovider-checks + hosted PR Selected Checks am FINAL-kopf terminal selbst beobachten.

## Was round 8 fixt

Round-7-Test `TestInviteManagedUserActivationEmptyBodyIsRefused` war FALSCHLICH GRUEN: sein server lieferte `[]` bei BEIDEN lookups, die routine stieg VOR der aktivierungs-zeile aus (resolve-after-create-Fehler beim zweiten []-lookup), nie auf der `/execute-actions-email`-zeile (frueher fehler, nicht der behauptete).

Rezept round 8: fixture umbauen, so dass der resolve-after-create-lookup den neu angelegten eigentums-erfuellten benutzer zurueckgibt => ECHTE aktivierungs-anfrage wird erreicht. Der aktivierungs-handler liest den request-body und lehnt einen leeren body VOR decode ab (fail-closed). Weil die production-route die dokumentierte nicht-leere string-array sendet, ist die zelle GRUEN, weil sie jetzt den genuine activation call erreicht (der 'right reason'). Die kausale mutation (payload=>nil) loest den fail-closed guard aus und macht genau diese zelle ROT.

## Empirischer beweis (probe, reverted)

isolierte probe in `/tmp/opencode/w265-mu-emptybody-fix`:
- VOR fix (beide lookups []): `REACHED_ACTIVATION=false ERR="managed invite: created account could not be resolved to exactly one owned user"` (frueher fehler).
- NACH fix (post-create lookup liefert owned user): `REACHED_ACTIVATION=true ERR=<nil> SEEN_BODY=["VERIFY_EMAIL","UPDATE_PASSWORD"]` (echte aktivierungs-anfrage erreicht, body = dokumentierte string-array).

## Korrekturen

- `internal/identityprovider/managed_user_invite_test.go` `TestInviteManagedUserActivationEmptyBodyIsRefused`:
  - resolve-after-create-lookup (zweites GET) liefert jetzt `{"id":"u1", ..., emailVerified:false, attributes:{baseharbor.scope:[managed-invite]}}` => routine erreicht `/execute-actions-email`.
  - handler am `/execute-actions-email` liest `r.Body` und faellt fail-closed auf leeren body VOR decode.
  - assert: einladung mit nicht-leerem body erreicht und vollendet die aktivierung (err == nil).
- `internal/identityprovider/managed_user_invite.go` UNVERAENDERT: sha256 `8812f40b8ccccff1f126f52202c5fc8aa77659b84dc652bbc708b5f0d96149ab` (vorher == nachher; fail-closed guard `required-actions list must not be empty` bleibt).

## Kausale RED/GREEN auf der echten quell-zeile

- GUARDED (production `requiredActions := []string{"VERIFY_EMAIL", "UPDATE_PASSWORD"}`): die zelle `TestInviteManagedUserActivationEmptyBodyIsRefused` GRUEN.
- MUTANT (isolierte kopie `/tmp/opencode/w265-mu-emptybody-fix-mutant`; production `requiredActions` auf nil gesetzt, payload=>nil): dieselbe zelle ROT — `invite with the documented non-empty body must reach and complete genuine activation, got error: managed activation: required-actions list must not be empty`.
  - mutant route hash: `73513d8972cefd91af5940790ef24c554fbb896617abedc12a475483c1067707`.
  - exaque Quelle zurueck (route hash 8812f40b) => GRUEN aus DERSSELBEN zelle.
- Beweis: payload=>nil loest DEN fail-closed guard aus => zelle ROT; restore => GRUEN aus derselben zelle.

## Transcript (local; green)

```
# probe (round-7 defect): REACHED_ACTIVATION=false (frueher [])
# probe (round-8 fix): REACHED_ACTIVATION=true ERR=<nil> SEEN_BODY=["VERIFY_EMAIL","UPDATE_PASSWORD"]

$ sha256sum internal/identityprovider/managed_user_invite.go
8812f40b8ccccff1f126f52202c5fc8aa77659b84dc652bbc708b5f0d96149ab  (unveraendert)

$ gofmt -l internal/identityprovider/managed_user_invite.go internal/identityprovider/managed_user_invite_test.go
(empty -- clean)

$ go vet ./internal/identityprovider/
(exit 0)

$ go build ./internal/identityprovider/
(exit 0)

$ go test -race ./internal/identityprovider/ -run 'TestInviteManagedUser' -count=1
ok  	github.com/mcpdev80/baseharbor/internal/identityprovider	1.042s

$ go test ./internal/identityprovider/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/identityprovider	7.967s

# mutant (payload=>nil):
$ go test ./internal/identityprovider/ -run 'TestInviteManagedUserActivationEmptyBodyIsRefused' -v
--- FAIL: TestInviteManagedUserActivationEmptyBodyIsRefused
    managed_user_invite_test.go:184: invite with the documented non-empty body must reach and complete genuine activation, got error: managed activation: required-actions list must not be empty
```

## Hosted CI — PR #1397 (run 42288242265, terminal success)

- Run-id: `42288242265` (CI · PR #1397), head SHA `47a10ab056a5cdc4f81d4d0b65802e05ee2286f5` = meine exakte kopie, branch `work/r27-managed-users`.
- conclusion = completed/success.
- Per-job: go-vet success, go-build success, go-unit-tests success, Source format success, Focused Python success, PR Selected Checks success, Trusted Plan success, Workflow policy success.
- Correctly SKIPPED (test-only identityprovider diff): Targeted HA · podman, Targeted HA · docker, validate, Release Source Preflight, PR · Demo Pin, PR · Consumer Pins, PR · Runner Interface, PR · Exact Candidate, PR · Selected Runtime, PR · Public Contracts.
- Kein `failed`/`error`/`cancelled`. Kein roter log-line.

## Branch provenance

- Base attest: commit direkt auf `b880f91e24a9338ffa75a9006ab7d26cad65a714` (round-7 kopie). `git merge-base --is-ancestor b880f91e24a HEAD` rc=0; `git merge-base HEAD b880f91e24a` = `b880f91e24a`.
- `git log --oneline -3` zeigt MEINE commits allein auf `b880f91e24a` (kein foreign commit):
  `47a10ab0 ... round 8` / `b880f91e ... round 7` / `fa2acd22 ... round 6`.
- `git push origin HEAD:work/r27-managed-users`.
- `git ls-remote origin refs/heads/work/r27-managed-users` AFTER push: `47a10ab056a5cdc4f81d4d0b65802e05ee2286f5`.
- One integration candidate per chain: `work/r27-managed-users` only. No second PR invented.

## write-set

- Nur `internal/identityprovider/managed_user_invite_test.go`. Route `managed_user_invite.go` UNVERAENDERT (hash 8812f40b). Kein `.github/**`, kein anderes produkt-paket.

## repo-rule compliance

- write-set honoriert. Kein `.github`-change, kein workflow_dispatch/rerun (nur `gh run`/`gh pr` reads, bestehende PR-checks).
- no subagents/task/agent tools; jeder schritt in dieser session (w265).
- caches/isolierte kopien unter /tmp/opencode/w265-*; kein evidence im produkt-repo, kein main-branch-write in baseharbor.
- evidence nur in baseharbor-plan (evidence/r27-welle5-2026-11-06/managed-users/round-8.md).

## VM COMPOSE

- kein docker/podman compose projekt gestartet (pure unit + hosted CI lane). Kein teardown noetig.

## END

END_DONE w265-mu-emptybody-fix: head=47a10ab056a5 fixture_reicht_aktivierung_erreicht route_hash=8812f40b unveraendert mutante=payload=>nil ROT (73513d89) restore GRUEN aus zelle lauf=42288242265 TERMINAL/success lsremote=47a10ab056a5 akte=evidence/r27-welle5-2026-11-06/managed-users/round-8.md main | round 8: fixture erreicht echte /execute-actions-email + fail-closed empty-body guard VOR decode; kausale ROT/GRUEN auf echter quell-zeile; PR #1397 CI terminal success am exakten kopf 47a10ab0; evidence zu origin/main.

### ls-tree witness (evidence auf origin/main BEFORE END post)

- `git ls-tree origin/main -- evidence/r27-welle5-2026-11-06/managed-users/round-8.md`:
  - `100644 blob 7aa876efb5c45751826ed93a29054ecab56ac4a4  evidence/r27-welle5-2026-11-06/managed-users/round-8.md`
- origin/main HEAD: `daa888c1572c50c2b36c3ab29604762326408de1`; my evidence commits `08c9307` + `1b1c46e` + `767cc36` + `fcbc542` pushed.
