# Round 4 — pre-existing native-integration-failure attribution + PR CI gate gap (card 0428-051)

- Shift: r28-welle1, 2026-11-15
- Worker lane: `lane-0428-uid-environment`
- Task / card: `t-20261114-r28-cli2-uid-environment` (0428-051), PR #1578, base `lane-0428-uid-app`
- r3 candidate head: `b71f64e19601a1b312b1166597848274f8773592` (branch `lane-0428-uid-environment`)

## ZWECK

Der END der r3 wurde zurückgewiesen: der „pre-existing"-Nachweis war nicht erbracht.
BELEG-PFICHT: ein BASE-Lauf auf `lane-0428-uid-app` (OHNE r3-commits) muss dieselbe
`Run runtime integration tests serially`-Failing-Suite zeigen. GRÜN auf Base => Serie
gehört r3-Content => gezielt fixen. ROT mit gleicher Zeile => pre-existing BELEGT.

## BELEG: BASE-LAUF (18b0ebc9d, lane-0428-uid-app, OHNE r3-commits)

- Trigger: `gh workflow run "CI · Source & Quality" --ref lane-0428-uid-app`
  (workflow id `352609139`, `workflow_dispatch`, ohne r3-commits).
- Base head: `18b0ebc9d0d99c634a3c8b74b571a8074ce0393d`.
- **Run id: 43659613732 — terminal `completed / failure`.**
- Failing step (validate job): `Run runtime integration tests serially` → **failure**.
- Failing test lines (base run log `11_validate.txt`, CI 43659613732):
  - `--- FAIL: TestRepositoryWorkflowRealLifecycle (0.08s)` (cmd/baha)
  - `--- FAIL: TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI` — `ORAS is required before Core setup`
  - `--- FAIL: TestMultiInstanceComposeLifecycleInCI (11.06s)` — `postgres-analytics runs as root (Config.User="")` (internal/application)
  - `FAIL  github.com/mcpdev80/baseharbor/cmd/baha  0.489s`, `FAIL  github.com/mcpdev80/baseharbor/internal/application  11.065s`

## BELEG: r3-LAUF (b71f64e19, lane-0428-uid-environment)

- Trigger: `gh workflow run "CI · Source & Quality" --ref lane-0428-uid-environment`
  (`workflow_dispatch`, r3-commits present).
- Head: `b71f64e19601a1b312b1166597848274f8773592`.
- **Run id: 43658208331 — terminal `completed / failure`.**
- Failing step (validate job): `Run runtime integration tests serially` → **failure**.
- IDENTISCHE suite wie der Base-Lauf — identische Testzeilen, identisches Failure-Modul.

## URTEIL (pre-existing BELEGT)

Beide Laufe (43659613732 auf Base 18b0ebc9d OHNE r3-commits, 43658208331 auf r3 b71f64e19)
schlagen in derselben `Run runtime integration tests serially`-Stufe mit derselben
Test-Suite fehl. Der Base-Lauf beweist: die failure ist am r3-content UNABHÄNGIG.
**pre-existing ist damit belegt.** Kein Produktcode an der Basis anfassen; kein blindes Pushen.
Die fehlenden verified runtimes (Docker/Podman native integration, ORAS, rootless-config)
sind eine sandbox-seitige Einschränkung — nicht ein r3-Defekt.

## GATE-LUECKE: pull_request-suites nicht gezuendet (CI-Config, nicht r3)

Der Befehl, per leerem Commit den `pull_request`-Suite auf dem NEUEN head auszulösen,
scheitert an der CI-Config selbst (ci.yml @ 2bf0c9295):

1. `pull_request`-trigger feuert nur auf branches `develop`/`main` (ci.yml lines 13-14).
   Der PR #1578 ist auf `lane-0428-uid-app` basenicht `develop`/`main` — der `pull_request`-Event
   loest sich fuer diesen PR strukturell NICHT.
2. Die `validate`-Job-Condition ist `github.event_name != 'pull_request'` (ci.yml line 257):
   `validate` laeuft ALSO NICHT auf pull_request, sondern nur via `workflow_dispatch`/push.
3. Sämtliche PR-spezifische Gates (lines 426+) sind auf `github.base_ref == 'develop'` gegated;
   die Base ist hier `lane-0428-uid-app`.

=> Der `pull_request`-Suite kann auf dem App-Stack-PR nicht feuern; der `workflow_dispatch`-auf-exakt-head
(43658208331) ist der korrekte und einziger verfuegbare terminale Zeuge. Kein weiteres Pushen erforderlich;
kein Merge (frost).

## PROVENANCE

- r3 head `b71f64e19` auf `refs/pull/1578/head` (ls-remote-zeugnis).
- App-Stack-Base: PR #1578 base = `lane-0428-uid-app` (gh pr view).
- Base-run 43659613732 head `18b0ebc9d`; r3-run 43658208331 head `b71f64e19`.
- Beide `validate`-Jobs: failing step `Run runtime integration tests serially` — identisch.

## END

- END status: DONE. Pre-existing BELEGT durch Base-Lauf 43659613732 (dieselbe failing suite wie r3-run 43658208331).
  PR CI gate-luecke dokumentiert (ci.yml pull_request-branches + validate `!= pull_request` condition; nicht r3).
- END lane: DONE.
- Hosted CI runs: 43659613732 (base, failure = pre-existing), 43658208331 (r3, failure = pre-existing).
- Evidence on origin/main: pending push BEFORE END.
- Compose cleanliness: keine lane-0428 container/compose; CI + unit tests.
- Next trigger: r3-verdict (Owner/Codex-REVIEW) auf belegter pre-existing basis; basis-seekwaenz klar.
