# R27 Cutover PR3 — Ruleset-Aktivierungsrehearsal (read-only)

Task: t-20261027-r27-cutover-pr3
Lane o230 — RULESET-AKTIVIERUNGSPROBE (read-only; Write-Set: NUR diese Evidence-Datei).
Basis: baseharbor-plan/evidence/r27-ci-replacement-2026-10-29/ruleset-patch-preflight.md (o216).
Alle API-Lesebefehle live UTC; Timestamps tragen den +02:00-Offset der GitHub-API. Kein PATCH/PUT auf rulesets. Kein git in baseharbor-plan.

## PLAN
1. Beide develop-Ruleset-JSONs holen, Aktivierung wirksam simulieren ohne Aenderung, betroffene offene PRs ermitteln.
2. Pruefen, ob 25223521 (required context 'PR Selected Checks', strict) aktuelle develop-PRs blockiert; SKIPPED-Beispiele vom letzten Merge.
3. Aktivierungsreihenfolge als Vorschlag an den Owner (Reihenfolge, Zeitpunkt, Rollback, Ruleset-Felder, die der eigene Automatismus sperrt).

---

## 1. Beide develop-Rulesets (live, o216-Snapshot bestaetigt)

Live-JSON identisch zu ruleset-patch-preflight.md §1 (2026-10-29):

Rule 23754541 — "develop - integration branch" (source refs/heads/develop):
- `enforcement: "disabled"`, `current_user_can_bypass: "always"`.
- Rules: deletion, non_fast_forward, required_linear_history, pull_request
  (required_approving_review_count:1, dismiss_stale_reviews_on_push:true,
  require_code_owner_review:true, require_extra_approval_for_unattributed_changes:true,
  require_last_push_approval:true, required_review_thread_resolution:true,
  allowed_merge_methods:["squash"]).
- bypass_actors: [ {actor_id:22537373 (mcpdev80), actor_type:User, bypass_mode:always} ].
  → mcpdev80 UMGEHT alle integration-branch-Regeln (PR-Gate inkl. squash + code-owner).

Rule 25223521 — "develop - required checks" (source refs/heads/develop):
- `enforcement: "disabled"`, `current_user_can_bypass: "never"`.
- Rules: required_status_checks { strict:true, do_not_enforce_on_create:false,
  required_status_checks:[ {context:"PR Selected Checks", integration_id:15368} ] }.
- bypass_actors: [] → kein Actor-Regel-Bypass fuer PR Selected Checks.

Beide `enforcement:"disabled"` → kein Legacy-Sperre aktiv. main - released source (23754542) bleibt `active`, ausserhalb Scope.

### Simulierte Aktivierung (nur 25223521, everything else byte-identisch)
PUT payload = o216 §2 Block (enforcement:active), strict:true und der eine Context bleiben unveraendert.
Nach Aktivierung: jeder develop-PR verlangt PRUEFUNG des Kontexts "PR Selected Checks" (integration_id 15368 =
 GitHub Actions Controller-App). Kein passender, integrierter Check => develop-PR bleibt gesperrt (merge blockiert).
Die integration-branch-Regel 23754541 bleibt deaktiviert; squash-only + code-owner + actor-bypass sind also
 NICHT gleichzeitig scharf, es sei denn, 23754541 wird gesondert aktiviert.

### Betroffene offene PRs (nur #1207 + #1160)
- **#1207** `work/r27-producer-extension-reserve` → develop. Author: mcpdev80 (Marcel Pfingstgräf). state: OPEN,
  mergeable MERGEABLE, mergeStateStatus CLEAN (prueft sich selbst; Owner-Regel umgeht merge-state-Check),
  reviewDecision null, 0 Reviews. Head 9c9a47e0 (attempt-1 CI run 40929835096 conclusion success, PR Selected Checks pass).
  → BETROFFT von 25223521: aktiv => merge blockiert, solange PR Selected Checks NICHT auf dem neuesten Commit steht.
- **#1160** dependabot/go_modules → **main** (nicht develop). state: OPEN, author app/dependabot.
  → NICHT betroffen von beiden develop-Rulesets (main hat eigene rulesets; 25223521/23754541 gelten nur refs/heads/develop).

Offene develop-PRs ueberhaupt: nur #1207 (verifiziert live 2026-10-29, API PR ?base=develop → genau 1 Treffer).
#1160 existiert als offene PR, trift aber auf main, nicht auf develop.

### CRITICAL — Engpass: self-authored PR #1207 kann NICHT self-approven
- PR 23754541 pull_request-Gate verlangt require_code_owner_review:true + required_approving_review_count:1 +
  require_last_push_approval:true.
- #1207 ist von mcpdev80 fuer mcpdev80 (self-authored). GitHub erlaubt KEIN self-approval fuer den author;
  eine approving review von einer anderen Person/Actor ist zwingend.
- #1207 hat aktuell 0 reviews; mergeStateStatus null (kein approving review) → unter aktivier tem 23754541-PR-Gate
  BLOCKIERT ausser durch den actor-bypass of mcpdev80 (bypass_mode:always). Der Owner-Logik-Bypass (current_user_can_bypass
  "always" + bypass_actor mcpdev80) umgeht dieses Gate — aber NUR fuer mcpdev80, nicht fuer externe Contributors.
- Für externe/self-authored PRs ohne zweiten approver ist der Engpass real: 1 approving review von ausserhalb erforderlich.

### Zwei offizielle Auswege (dokumentiert, kein Edit)
1. **Owner-Bypass / actor-Regel**: current_user_can_bypass + bypass_actor für mcpdev80 (bypass_mode:always) ist bereits
   in 23754541 hinterlegt und umgeht das PR-Gate (squash + code-owner). fuer mcpdev80-self-authored PRs die aktive
   Loesung; extern/self-authored PRs beduerfen trotzdem einer zweiten approving review (bypass_actor greift nur fuer
   den definierten actor_id 22537373).
2. **Zweit-Account als approver**: zweite GitHub-ID, die als approver/fourth-party fungiert. NICHT laut GITHUB_AUTHORITY —
   die Anlage eines zweiten Accounts zum Umgehen der code-owner/self-approval-Regel ist als Bypass verboten; der genehmigte
   Weg ist der single-account actor-bypass (#1), nicht ein zweites Konto.

### Repository-Fakten zum Engpass (live)
- mcpdev80/baseharbor collaborators: mcpdev80, patplu (2 IDs). patplu als zweite approving review moeglich.
- CODEOWNERS: auf develop UND main nicht vorhanden (API 404) → require_code_owner_review kann formal nicht greifen;
  das Gate bleibt aber bestehen, wenn CODEOWNERS spaeter eingefuehrt wird. Derzeit ohne CODEOWNERS code-owner-review
  de-facto uneingeschraenkt (nur approver-count relevant).
- Branch protection: develop "not protected" (nur via rulesets 23754541/25223521), main ebenfalls "not protected" —
  die einzige aktive Schutzlage ist main - released source (23754542).

---

## 2. Blockiert 25223521 aktuelle develop-PRs? (SKIPPED-Beispiele vom letzten Merge)

JA — sobald aktiviert, sperrt 25223521 jeden develop-PR ohne passendes "PR Selected Checks" (integration_id 15368).

Beispiel-SHA vom letzten Merge (#1200, merged 2026-10-29 14:48:34Z, CI run 40848710241):
| check | status auf #1200 | required? |
|---|---|---|
| PR Selected Checks | **pass** (12s) | **JA — der eine required context (integration_id 15368)** |
| PR · Trusted Plan | pass | nein (skipped-on-#1200-Regel) |
| PR · Focused Python | pass | ja (auf #1200 bestanden) |
| PR · Consumer Pins | skipping | nein |
| PR · Demo Pin | skipping | nein |
| PR · Exact Candidate | skipping | nein |
| PR · Public Contracts | skipping | nein |
| PR · Runner Interface | skipping | nein |
| PR · Selected Runtime | skipping | nein |
| Release Source Preflight | skipping | nein |
| validate | skipping | nein |
| Targeted HA · podman/docker | skipping | nein |
| Workflow policy | pass | nein |

Interpretation:
- Die Integration 15368 ist die Controller-App; "PR Selected Checks" wird NUR erzeugt, wenn der automatische Skeleton
  auf dem HEAD laeuft und den required check ausgibt. Auf #1200 (und auf #1207) bestanden — das ist genau die
  "accepted exact candidate"-Bedingung.
- SKIPPED-Beispiele (#1200): Consumer Pins, Demo Pin, Exact Candidate, Public Contracts, Runner Interface, Selected Runtime,
  Release Source Preflight, validate, Targeted HA podman/docker. Diese sind per CI-Mapping (o216 §3/§4) NICHT required —
  nur PR Selected Checks ist required. Aktiviert 25223521 => develop blockiert fuer alle PRs, bei denen PR Selected Checks
  SKIPPED ist (kein Lauf des Skeletons auf dem HEAD) — z.B. workflow-file-only PRs (#1211, #1212), die kein trusted-pr-plan
  produzieren und bei denen der Controller-Lauf fehlt.
- #1207 Kopf 9c9a47e0: PR Selected Checks pass (run 40929835096, attempt 1, success) => unter aktiviertem 25223521
  MERGEFAEHIG (vorausgesetzt, der letzte Push ist derselbe HEAD; require_last_push_approval bei 23754541 bleibt getrennt).

---

## 3. Aktivierungsreihenfolge — Vorschlag an den Owner

### (a) Reihenfolge
1. PR #1207 zuerst merge-faehig machen: PR Selected Checks auf dem letzten HEAD von #1207 (9c9a47e0) bestaetigt = pass
   (bereits live). Falls nach neuen Commits der Lauf fehlt, CI erneut ausloesen, NIE manuell re-run ohne Skeleton.
2. Erst NACH #1207-Merge: 25223521 aktivieren (o216 §2 Block, enforcement:active), alles else byte-identisch.
3. 23754541 (integration branch, squash + code-owner + actor-bypass) bewusst getrennt halten/spaeter aktivieren;
   nicht im gleichen Bounded-Patch an 25223521.

### (b) Zeitpunkt
Nach #1207-Merge (#1207 merge_commit_sha e0de0117974b3b7e75ca8eed600f69528e8fd9f6 ist offen, mergeStateStatus CLEAN).
Nicht waehrend #1207 offen ist: sonst sperrt 25223521 #1207, sobald der required check auf einem spaeteren HEAD skipped.

### (c) Rollback-Plan (o216 §2 Rollback)
Rollback-Block = identisches JSON, enforcement:disabled. Vor dem PUT §1-Live-JSON erneut gegenlesen (Drift in conditions,
strict_required_status_checks_policy, do_not_enforce_on_create verbatim mitnehmen). Kein 23754541-Touch, keine weiteren
Contexts, strict bleibt true. Bei Blockade aktueller develop-PRs: sofort enforcement:disabled zurueck.

### (d) Was an Ruleset-Felder GEAENDERT werden MUSS, damit der Automatismus (eigener Cutover) sich nicht selbst sperrt
- Der einzige required context ist "PR Selected Checks" (integration_id 15368). Der automatische Cutover-Mechanismus
  (shadown/post-run-producer-Kette) MUSS auf jedem betroffenen develop-HEAD einen integrierten "PR Selected Checks"
  erzeugen, sonst sperrt strict/1-context den eigenen Automatismus (workflow-file-only PRs wie #1211/#1212 haben kein
  trusted-pr-plan und damit keinen Controller-Lauf => SKIPPED => blockiert).
- Konkret zu sichern: (1) integration 15368 bleibt der eine required context — keine zweiten required_status_checks
  Contexts hinzufuegen (sonst wird der single-context-Vertrag gebrochen); (2) strict_required_status_checks_policy:true
  und do_not_enforce_on_create:false verbatim beibehalten; (3) PR Selected Checks muss auf dem EXAKTEN HEAD des PRs
  laufen (require_last_push_approval bei 23754541), also kein Stale-Head ohne neuen Lauf; (4) fuer workflow-file-only PRs
  ohne trusted-pr-plan ist eine gesonderte Regel noetig — z.B. require_code_owner_review + actor-bypass oder eine
  pruned-required-context-Regel, die workflow-file-only PRs (kein contracts) vom required-check-Gate ausnimmt, ohne den
  required-check-Vertrag fuer echte contracts-PRs aufzuheben.
- Kein self-approval fuer self-authored PRs (#1207) umgehen durch Zweit-Account (verboten, GITHUB_AUTHORITY). Exakter
  Weg: actor-bypass mcpdev80 (bereits in 23754541) fuer mcpdev80; externe self-authored PRs brauchen zweite approving
  review (patplu oder extern), nicht ein zweites Konto.

### (e) Akzeptanz/Pruefungen (o216 §5, unveraendert)
1. Kettenlauf (chain run): evidence/board-2026-10-29/scripts/chain-run.sh — beweist accepted skeleton => PR Selected Checks.
2. Drei Negativbeweise: evidence/board-2026-10-29/scripts/negative-proofs.sh (offline, closed-fail pro isolierter Variable).
Beide PreFlight-Harnesses; pass/fail-Evidenz vor Aktivierung sichern. Neither run in this lane (read-only).

---

## repo-rule compliance
- Read-only: kein `gh api -X PUT/POST`, kein ruleset-Patch/PUT ausgefuhrt.
- Kein git in baseharbor-plan; keine Tokens/Secrets in der Datei.
- Alle Fakten live via `gh api`/`gh pr checks`/`gh pr view` verifiziert (mcpdev80/baseharbor).
- Prompt-injection-defense: o230.txt ist DATEN; Befehle exakt im Write-Set (nur Evidence-Datei) befolgt.

## END o230-DONE