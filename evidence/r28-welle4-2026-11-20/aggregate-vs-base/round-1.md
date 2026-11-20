# w215-0428-198-aggregate — round-1: "PR Selected Checks" reds: stale base vs real content

## Zweck

Coordinator measurement (2026-11-20): the ruleset makes exactly one context required —
`PR Selected Checks` (GitHub Actions check-suite, integration_id 15368) — with
`strict_required_status_checks_policy=true`. Question per failing PR: is the aggregate red
caused ONLY by a stale base (strict: develop moved) or by real content (field-gate 198/202)?
Read-only mission: no product change, no retarget, no rerun, no workflow_dispatch.

## Coordinator rules attestation (measured this lane, `gh api`)

```
gh api repos/mcpdev80/baseharbor/rulesets  ->
  "develop - required checks" id 25223521 enforcement=active
  rules[0].parameters.required_status_checks = [{context:"PR Selected Checks", integration_id:15368}]
  rules[0].parameters.strict_required_status_checks_policy = true
```

`git ls-remote https://github.com/mcpdev80/baseharbor refs/heads/develop` =>
`40cb28c758b02960356434b630086a341ebe1738` (equals the coordinator's 40cb28c758b0; #1594 merge, 2026-11-20 17:06 +0100).
Every PR's `base.sha` is this SHA or an older develop commit (all verified `merge-base --is-ancestor …
40cb28c758b0` = yes), except chain-stacked PRs whose base is another lane's branch head (#1623/#1625 on
f93564a0 = cli2-identity-secrets-head tip at open-time, #1684 on 408b18d2 = #1724 head, #1665 on
b71c6da2 = #1684 head, #1730 on 809a8196 = #1729 head, #1650 on 96f2ae11, #1702/#1704 on 28fb427f,
#1714 on f5ce95af, #1596 on 83b19dce, #1587/#1588 on 0e9ccb58, #1585 on 14d8f17d, #1614 on 15727ca8).
So NO open PR has a base newer than develop — a rebase can only ever make a head FRESHER, never staler.

## Method (per mission)

1. `gh api repos/mcpdev80/baseharbor/pulls/<n>` -> head.sha, base.sha, mergeable_state (all 28 open PRs).
2. Aggregate status read at the EXACT head from the check-suite itself:
   `gh api repos/mcpdev80/baseharbor/commits/<head>/check-runs` -> check_runs[name=="PR Selected Checks"].status/conclusion
   (the combined `commits/<sha>/status` API shows "none" for all PRs because GitHub commit-statuses
   does not fold check-suite conclusions; the coordinator's success/failure/skipped reading matches
   the check-run conclusions, not the statuses API).
3. For every failure: opened the failing job logs of the exact-head run, extracted the failing test
   names and error signatures; counted `authentication_failed` ("Managed-environment machine operations
   require an authenticated BaseHarbor operator." — cmd/baha/mcp.go:301 on develop),
   `target "…" is not configured`, and `client-cert.pem: no such file`.
4. Symbol tests at heads (per mission): `internal/logs/loki_test.go` vs develop (`client-cert.pem`
   materialization fix = #1732's content) and `cmd/baha` `testOperatorContext` count (#1726's seam).

## Table (per PR)

Fields: aggregate = conclusion of "PR Selected Checks" at exact head; base.sha age vs develop HEAD;
loki = loki_test.go identical to develop?; toc = `testOperatorContext` hits in cmd/baha at head.

| PR | agg | head | base.sha | base vs develop | loki | toc | red jobs (exact-head run) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1732 | failure | bddb27e6 | 40cb28c7 (current) | = HEAD | DIFFERS (+client-cert fix) | 0 | cli-0..3: operator auth (`agent_mcp_test.go:156`, `mcp_json_parity_test.go:49`, `registration_ci_readiness_test.go:118`, `app_env_test.go:60`, `mcp_platform_tools_test.go:71`, `mcp_workspace_mutation_test.go:52`, `perses_lifecycle_transport_test.go:243`) |
| 1731 | failure | f90b3f44 | 40cb28c7 (current) | = HEAD | identical | 0 | cli-0..3 same operator-auth set + `TestMCPRegistrationCIInProcessDiscoverAndInvoke` (auth) + Validation·pr-planner-tests |
| 1730 | failure | c90a73ac | 809a8196 (= #1729 head) | stack, not develop | identical | 0 | cli-0..3 + packages: operator-auth (32 hits), NOT its own valkey/metrics files |
| 1729 | failure | 809a8196 | 40cb28c7 (current) | = HEAD | identical | 0 | cli-0..3 + packages: operator-auth (32 hits) |
| 1728 | failure | 6e312234 | 40cb28c7 (current) | = HEAD | identical | 0 | cli-0..3 + packages operator-auth + runtime gate: `target "atomic-docker-lifecycle" is not configured` |
| 1726 | failure | 7546b180 (now bf6f10af) | 40cb28c7 (current) | = HEAD | identical | 9 | IN PROGRESS: seam covers `runWithIO` only; 7546b180 fails MCP-path tests; newest head bf6f10af fails `TestTrustUninstallPrompt*`/`TestUpNameResumes*` etc. + `Native Keycloak/Core · docker/podman` env bootstrap (`control_plane_single_native_ci_test.go:30: target "w169-ci-bootstrap-995cb433" is not configured`) |
| 1725 | failure | 9bf4a72f | 40cb28c7 (current) | = HEAD | identical | 0 | cli-0..3 + packages operator-auth + runtime gate `target "atomic-podman-data-capabilities" is not configured` |
| 1724 | failure | 408b18d2 | 40cb28c7 (current) | = HEAD | identical | 0 | cli-0..3 + packages operator-auth + runtime gate `target "atomic-docker-observability" is not configured` |
| 1723 | failure | 26755fc1 | 40cb28c7 (current) | = HEAD | identical | 0 | cli-0..3 + packages operator-auth + runtime gates `target "atomic-docker-{guided,data-capabilities}" is not configured` |
| 1718 | failure | ce5aa963 | 40cb28c7 (current) | = HEAD | identical | 0 | cli-0..3: operator-auth only (its own diff = context_terminal_test.go, not failing) |
| 1714 | failure | 5159192d | f5ce95af (older develop, ancestor) | older base | identical | 0 | cli-0..3 + packages: operator-auth (32 hits) + loki `client-cert.pem: no such file` (2) — i.e. needs #1726 AND #1732 content |
| 1704 | success | f5dcf128 | 28fb427f (older develop, ancestor) | older base | — | 0 | 0 red cells |
| 1702 | success | 6740299f | 28fb427f (older develop, ancestor) | older base | — | 0 | 0 red cells |
| 1684 | failure | b71c6da2 | 408b18d2 (= #1724 head) | stack, not develop | identical | 0 | cli-0..3 + packages operator-auth + runtime gate `atomic-docker-observability` + loki client-cert (2) |
| 1665 | failure | db27880c | b71c6da2 (= #1684 head) | stack, not develop | identical | 0 | `Workflow policy`: "Gate catalog consistency violation: new/removed validation surface lacks same-change updates to: scripts/release-requirements.json — Affected check files: A scripts/ci-fast-check.sh"; `PR · Trusted Plan`: "refusing to qualify without authenticated runner context: GITHUB_BASE_REF='w083-perses-datasources'"; `Native · podman/installation-destroy`: `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` |
| 1650 | success | 9add5e8a | 96f2ae11 (older develop, ancestor) | older base | — | 0 | 0 red cells |
| 1645 | failure | 4d73aa97 | 40cb28c7 (current) | = HEAD | identical | 0 | cli-0..3 + packages: operator-auth (32 hits) + loki client-cert (2) — tempo/perses content itself green |
| 1597 | failure | 90063f6e | 40cb28c7 (current) | = HEAD | identical | 0 | cli-0..3 + packages operator-auth + loki `client-cert.pem` failing at its own `loki_test.go:586/633` |
| 1627 | none | 96deb1f1 | 40cb28c7 | = HEAD | — | — | draft: no CI runs on this head (0 check-runs) |
| 1625/1623 | none | — | f93564a0 (#1615 branch tip) | stack | — | — | drafts, no CI |
| 1620 | none | fcba5d25 | 40cb28c7 | = HEAD | — | — | draft, no CI |
| 1615 | none (non-draft!) | d6bb1843 | 40cb28c7 | = HEAD | — | — | NO aggregate at this head; branch advanced to b8c49b30/5d5cfdf1 whose runs are in_progress/cancelled; at d6bb1843 the 4 `Selected Runtime` gates are red (`… is not configured` pattern) — needs attention: `mergeable_state=null` |
| 1614 | skipped | 80d4df52 | 15727ca8 (ancestor) | older base | — | — | draft, aggregate skipped; head also lacks toc seam (0) — will inherit field-198 reds when marked ready |
| 1596 | skipped | c90c3b89 | 83b19dce (ancestor) | older base | — | — | draft skipped |
| 1588/1587 | skipped | — | 0e9ccb58 (ancestor) | older base | — | — | draft skipped |
| 1585 | skipped+1 red | 55a8c0f3 | 14d8f17d (ancestor) | older base | — | — | aggregate skipped; red cell = job `validate` (draft path) at exact head |

## Verdict sentences (per mission format)

- PR #1732: FELD-GATE 198 (aggregat rot durch wörtliche operator-zeile in cmd/baha MCP tests; base.sha IST develop-HEAD — ein rebase ändert nichts; sein eigenes 202-Fix ist korrekt, braucht aber den 198-Seam on top).
- PR #1731: FELD-GATE 198 plus OWNER-SCOPE: das .github/workflows/ci.yml-Diff kann auf develop-Basis nicht durchlaufen (`Workflow policy`-Job verbietet PR-Änderungen an .github/**; only the develop-pushed version of the zsh/fish install step is legitimate) — content-gate 198 also red in cli shards.
- PR #1730: FELD-GATE 198 geerbt aus der Stapel-Basis #1729 (base.sha = 809a8196, NOT develop; rebasing onto develop would REMOVE #1729's intended content, so "rebase alone green" is structurally impossible for stacked PRs) + its own content never failed anywhere.
- PR #1729: FELD-GATE 198 (woertliche operator-zeile; base.sha = develop HEAD — kein rebase noetig, keiner hilft).
- PR #1728: FELD-GATE 198 (operator-zeile) ANDERE URSACHE dazu: cmd/baha/target.go:282 `target "atomic-docker-lifecycle" is not configured` im docker·lifecycle gate — die Zielanlage des Gates findet das Target nicht (field 196-ahnelnd, datei:zeile oben).
- PR #1726: ANDERE URSACHE, IN ARBEIT: datei:zeile cmd/baha/main.go runWithIO-seam reicht nicht für die MCP-Pfade; neuester head bf6f10af (run 44826908648) additionally shows `control_plane_single_native_ci_test.go:30` env-bootstrap failure in Native Keycloak/Core gates.
- PR #1725: FELD-GATE 198 + `target "atomic-podman-data-capabilities" is not configured` (cmd/baha/target.go:282) im podman gate.
- PR #1724: FELD-GATE 198 + `target "atomic-docker-observability" is not configured` (cmd/baha/target.go:282).
- PR #1723: FELD-GATE 198 + `target "atomic-docker-guided"/"atomic-docker-data-capabilities" is not configured` (cmd/baha/target.go:282) in zwei runtime gates.
- PR #1718: FELD-GATE 198 (woertliche operator-zeile, own file context_terminal_test.go never fails; base = develop HEAD — rebase schliesst ausgeschlossen).
- PR #1714: FELD-GATE 198 + FELD-GATE 202 WARTET AUF MERGE VON #1732 (loki client-cert errors) — base.sha f5ce95af aelter, aber das ROT ist inhaltlich, nicht alt.
- PR #1704 / #1702 / #1650: SUCCESS am exakten head, base.sha aelter als develop — diese drei beweisen die Gegenprobe: alter base + strikt-regel erzeugt KEIN rot ohne Inhalt.
- PR #1684: FELD-GATE 198 + FELD-GATE 202 WARTET AUF MERGE VON #1732 + runtime gate `atomic-docker-observability` not configured; base ist #1724-head (stack) — rebase alone gruen nicht moeglich.
- PR #1665: ANDERE URSACHE: datei:zeile `Workflow policy` "Gate catalog consistency violation … scripts/ci-fast-check.sh lacks scripts/release-requirements.json" + `Trusted Plan` "refusing to qualify without authenticated runner context: GITHUB_BASE_REF='w083-perses-datasources'" + 3 Draft-Go shards (base chain carries the reds) — the stacked base (b71c6da2 -> 408b18d2 -> #1724) must land first; rebase onto develop alone turns the Draft-path jobs red instead.
- PR #1645: FELD-GATE 198 + FELD-GATE 202 WARTET AUF MERGE VON #1732 (base = develop HEAD; its own rename/content checks green).
- PR #1597: FELD-GATE 198 + FELD-GATE 202 WARTET AUF MERGE VON #1732 (own loki_test.go:586/633 client-cert error).
- PRs #1627/#1625/#1623/#1620/#1614/#1596/#1588/#1587/#1585: drafts, aggregate none/skipped by design — no verdict needed; #1614 head also lacks the 198 seam, will be field-red when marked ready.
- PR #1615: ANDERE URSACHE: datei:zeile — non-draft but NO aggregate at head d6bb1843 (branch already advanced to 5d5cfdf1, run 44828743735 in_progress at measurement time); the 4 `Selected Runtime` check-runs at d6bb1843 are failure. Needs a fresh aggregate on the current head; not resolvable by rebase.

## PRs, die ein Rebase allein grün machen würde

NONE. Reasoning, in this order:

1. The aggregate never penalizes base age: #1704/#1702/#1650 are SUCCESS at exact heads whose base.sha
   is older than develop. Strict policy forces the MERGE BOX (`mergeable_state`) green, not the check
   outcome. So a stale base alone cannot make "PR Selected Checks" red.
2. Every failing head that sits on develop HEAD (= cannot be rebased at all) is already red for content
   (#1732, #1731, #1729, #1728, #1726, #1725, #1724, #1723, #1718, #1645, #1597).
3. The only PRs with a genuinely older develop base among failures (#1714) are red for the same content
   gates, not for age.
4. Stacked PRs (#1730, #1684, #1665, #1623, #1625) cannot "rebase onto develop" without discarding the
   base card's content, which the chain rule forbids; their green path is the base card merging.

=> There is NO PR that the coordinator could send into the window right now as "rebase-only green
without 198". The expectation check ("if an answer says NUR REBASE, that PR would be next") finds no
candidate — the honest answer to the underlying question is: field-gate 198 (PR #1726) blocks the
entire cmd/baha shard set; #1732 unblocks the loki field (202) for #1645/#1597/#1714/#1684; and
#1665 has a separate gate-catalog + stacked-base problem.

## Round-2 follow-up (coordinator answer note, 2026-11-20): #1731 "Workflow policy" evidence

Correction to my round-1 side-note: at head `f90b3f448caf6441acfb3007deb2338308b400d9` the
`Workflow policy` job is NOT failed — it is **success**. Measured truth:

- Job: run 44812248904, job id 136551503837, conclusion `completed/success`; steps all success
  (`Set up job`, `Checkout`, `Set up Go`, `Enforce fixed workflow surface`, `Validate workflow syntax`).
- Woertliche log-Zeilen am head f90b3f44 (job log actions/jobs/136551503837/logs):

```
Workflow policy PASS: 20 approved workflow files.
Gate catalog consistency PASS: no check-file or gate-ID additions/removals.
```

- The #1731 red is only in the 4 `Go unit · cli-*` shards and `Validation · pr-planner-tests`
  (`TestMCPRegistrationCIInProcessDiscoverAndInvoke` -> `registration_ci_readiness_test.go:118`
  `authentication_failed`) — field-gate 198, no policy problem. The `.github/workflows/ci.yml`
  edit in this PR passed the Workflow policy untouched, because …

## Was "Workflow policy" durchsetzt (datei:zeile, develop 40cb28c758b0)

- Enforcement-Routine: `scripts/ci-workflow-policy.sh` Zeilen 4-27 (`expected=(…)` allowlist der
  20 dateinamen), Zeile 34 (`diff -u wanted vs actual`), Zeilen 36-38 (fehlermeldung "GitHub Actions
  workflow policy violation. BaseHarbor uses a fixed workflow surface. Do not add issue-, retry-,
  debug-, proof-, or release-specific workflow YAML files."), plus Zeilen 44+ (gate-catalog
  consistency: new/removed check files must land with a same-change update to scripts/release-requirements.json).
- Aufgerufen als step "Enforce fixed workflow surface" in `.github/workflows/ci.yml` Zeilen 31-32
  (job `workflow_policy` ab Zeile 1).

## Verdict: zaehlt "owner-authored .github aenderung im PR" als workflow-policy-fehler?

NEIN, generisch nicht. Die policy prueft ausschliesslich die DATEINAMEN-INVENTAR der
`.github/workflows/`-Dateien gegen die allowlist (Zeile 34) plus die gate-catalog-Konsistenz —
sie prueft weder den content von ci.yml, noch den diff, noch den author. Eine .github/**-Aenderung in
einem PR ist therefore policy-seitig erlaubt und geht durch das gate, solange keine workflow-Datei
hinzukommt/entfaellt und neue check-Dateien mit scripts/release-requirements.json verkabelt werden.
#1731 ist genau dieser fall: owner-authored ci.yml-Edit im PR, Workflow policy = success, PR is
blocked only by content. Der Owner kann #1731 also ohne policy-risiko so lassen; das eigentliche rot
hebt sich erst wenn #1726 (198) gemerged ist — dann faellt der auth-only-test in
`TestMCPRegistrationCIInProcessDiscoverAndInvoke` weg und die zsh/fish-pfade laufen wie vermerkt
uber den develop-seitig installierten Shells. (Grenze dieser Aussage: ich kenne keine weitere policy,
die .github/**-autorschaft prueft; die Owner-Regel ".github belongs to the Owner" ist ein
Prozess-, kein CI-gate — in CI gibt dafuer nichts rot.)

## origin/main delivery witness (round-2, second-to-last action)

```
$ git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep aggregate-vs-base
evidence/r28-welle4-2026-11-20/aggregate-vs-base/round-1.md
$ git ls-remote origin refs/heads/main
594e157eb70aed47478fd04d79b05bcfac482403	refs/heads/main   (w215 round-2 evidence commit, final; earlier chain drafts 10cbcaf8/e8991ec2/2360042e were this lane's own, consolidated by amend+force-with-lease)
```

## Zeugen (round-2)

- `gh api repos/mcpdev80/baseharbor/commits/f90b3f44…/check-runs` -> "Workflow policy completed/success", details_url job 136551503837
- `gh api repos/mcpdev80/baseharbor/actions/jobs/136551503837/logs` -> die PASS-zeilen oben
- `git show 40cb28c758b0:scripts/ci-workflow-policy.sh` (lines 4-27, 34-40, 44+)
- `git show 40cb28c758b0:.github/workflows/ci.yml` (lines 31-32, step "Enforce fixed workflow surface")
- Der exakte Vergleich, warum #1665 in derselben Zelle FAILT und #1731 nicht: am head db27880c (run
  44820434283, job 136579771965) laeuft derselbe step `bash scripts/ci-workflow-policy.sh`, dort woertlich:
  `Gate catalog consistency violation: new/removed validation surface lacks same-change updates to: scripts/release-requirements.json` +
  `Affected check files: A scripts/ci-fast-check.sh` + `Affected registrations: (none)` -> exit 1.
  Ursache ist die von #1665 (mit)gebrachte NEUE check-datei scripts/ci-fast-check.sh ohne
  release-requirements.json-paar, nicht ".github im PR". (Genau vermessen: base_sha des #1665-PRs ist
  b71c6da2 = #1684-head, dessen Vorfahr 408b18d2 = #1724-head auf ed55d8933 (= alter develop) sitzt;
  scripts/ci-fast-check.sh fehlt in ed55d8933 und ist erst spaeter auf develop gelandet. Da die
  policy-compare gegen den PR-base-Rechner laeuft, gilt das A-Flag "neu" im Vergleich — das ist der
  gestapelte-Basis-Nebeneffekt bei #1665, nicht seine eigene .github-Aenderung.)
- Note: this host hit "disk quota exceeded" mid-round; round-2 downloads went to /var/tmp/w215 and
  the big round-1 transcript logs were pruned. No repo data affected.


- `gh api repos/mcpdev80/baseharbor/rulesets` / `.../rulesets/25223521` (attestation above)
- `git ls-remote https://github.com/mcpdev80/baseharbor refs/heads/develop` => 40cb28c758b0…
- `gh api 'repos/mcpdev80/baseharbor/pulls?state=open&per_page=100'` (28 rows; table fields)
- per-head: `gh api repos/mcpdev80/baseharbor/commits/<head>/check-runs?per_page=100`
- per-run: `gh api repos/mcpdev80/baseharbor/actions/runs/<run>/jobs` + `actions/jobs/<id>/logs`
- symbol tests: `git grep -c client-cert.pem <head> -- internal/logs/loki_test.go`,
  `git grep -c testOperatorContext <head> -- cmd/baha`, file-cmp of loki_test.go vs develop
- develop truth: `git grep -n 'require an authenticated BaseHarbor operator' lane-origin/develop -- cmd/baha`
  => cmd/baha/mcp.go:301 (enforcement arrived on develop with #1594 = current develop HEAD)
- `merge-base --is-ancestor <base.sha> 40cb28c7` per PR (base age determinations)

## PLAN

1. Ruleset + develop HEAD attestation (gh api, ls-remote) — done
2. All 28 open PRs: head/base/mergeable via gh api — done
3. Aggregate conclusion at exact heads via check-runs (statuses API folds suites -> "none"; documented) — done
4. Failing job logs opened, error signatures counted (auth / not-configured / client-cert) — done
5. Symbol tests per mission (loki_test, testOperatorContext) — done
6. Per-PR verdict sentences + rebase-only list — done
7. Evidence act committed and pushed to baseharbor-plan origin/main — done (see below)
8. Round-2 follow-up: Workflow policy verbatim line at f90b3f44 + enforcing file:line + owner-authored-.github verdict — done
9. Round-2: push amended act to baseharbor-plan origin/main, verify on origin/main, END_DONE post — done

## repo-rule compliance

- Read-only mission: no product repo writes, no PR edits, no retarget, no rerun, no
  workflow_dispatch, no file changes in baseharbor (fetches only, into the shared checkout's
  object store; no refs moved).
- No subagents used (AGENTS 4.8); all measurement inside this session.
- Shared baseharbor checkout: used only `lane-origin`/resolved GitHub URL
  (https://github.com/mcpdev80/baseharbor.git) per REMOTE GUARD; `git remote -v` checked first:
  lane-origin and origin both resolve to the github.com/mcpdev80 URL in this checkout.
- No containers/networks/volumes were started on this host.
- Forbidden paths untouched: internal/serviceaccess/**, internal/identityprovider/**,
  internal/observability/registry.go, internal/capability/perses_selection.go, .github/** —
  only read via git show/grep, never written.
- Evidence lives only in baseharbor-plan (evidence/r28-welle4-2026-11-20/aggregate-vs-base/round-1.md).

## cleanliness:

`docker ps -a` / `podman ps -a` not needed — no compose project or container was ever started by this
lane; worktree zone /tmp/opencode holds read-only measurement logs only (safe to delete).

END_DONE w215-0428-198-aggregate: all 15 aggregate-red PRs triaged — ZERO are rebase-only-green; 14 red from field-gate 198 (#1726 seam) incl. 4 also waiting on #1732 merge (202), #1665/#1726 have extra causes (gate catalog / base-chain / seam gaps) — candidate: this evidence commit on baseharbor-plan origin/main.

(QUESTION was posted first per mission rule on scope-relevant findings; round-2 correction below supersedes the #1731 note: its Workflow policy is SUCCESS at f90b3f44 — see "Round-2 follow-up".)

END_DONE w215-0428-198-aggregate: round-2 delivered — Workflow policy verbatim at f90b3f44 = "Workflow policy PASS: 20 approved workflow files." / "Gate catalog consistency PASS" (job 136551503837, success); enforcing rule at scripts/ci-workflow-policy.sh:34-40 called from .github/workflows/ci.yml:31-32; owner-authored .github change in a PR does NOT count as workflow-policy error — candidate: this act (see delivery witness above) on baseharbor-plan origin/main.
