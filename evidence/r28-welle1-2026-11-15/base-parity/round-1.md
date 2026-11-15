# r28-welle1 base-parity Zeugnis — round-1 (mission-baseparity.md)

Lane: flash worker, read-only Verify/Abnahme-Schicht. Datum: 2026-11-15.
These geprüft: „alle failure-signaturen der 7 roten exact-head/runs sind base-/runner-seitig, nicht kandidat-seitig.“

## PLAN

- Schritt 1: Realitätsabgleich (gh auth, 7 SHAs gegen origin, Planning-Repo) — erledigt
- Schritt 2: Zelle 1 — je run fehlgeschlagenes job+step wörtlich + Signaturnormalisierung — erledigt
- Schritt 3: Zelle 1b/2 — Baseline-run 43757001183 + Signaturvergleich je PR — erledigt
- Schritt 4: Zelle 3 — Verwurzelung (git log/annotate auf develop, file:line-Zeugen) — erledigt
- Schritt 5: Zelle 4 — Urteil-Tabelle — erledigt
- Schritt 6: Akte + Commit + Push auf origin/main + END — läuft

## Planungszonen-Zeuge (Pflicht)

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` = `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (echtes Planning-Repo, remote https://github.com/mcpdev80/baseharbor-plan.git). Das verwarnte `workers/baseharbor-plan`-Verzeichnis wurde nicht verwendet; sein Toplevel ist `workers` (Buchhaltungsrepo) — gemieden.
- Produktesearch-Zeuge: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor rev-parse --show-toplevel` = `/home/marcel/dev/baseharbor-ecosystem/baseharbor`, `git remote get-url origin` = https://github.com/mcpdev80/baseharbor.git; read-only genutzt (fetch/log/show/archive, Arbeitsbäume nur unter /tmp/opencode/bp).

## Zelle 1 — Wörtliche Fehlstellen je run (gh run view --log)

Alle 7 runs sind `workflow_dispatch`, exact head SHA bestätigt gegen `gh pr view --json headRefOid` und `git ls-remote`.

| Run | Head | Job::Step (failure) | Wörtliche Kernzeile |
| --- | --- | --- | --- |
| 43754874604 | 85b4cbb5 (#1590) | validate :: Validate documentation | `spec/management-access-v1.md: literal lost: …(7)` → `DE technical integrity: FAIL (7 findings across 167 paired pages)` (log:875) |
| 43754876950 | b85efaf6 (#1591) | validate :: Run runtime integration tests serially | 5× `prepare BaseHarbor integration trust plane: ORAS is required before Core setup; install it manually or rerun 'baha up' in an interactive terminal…` + 1× `runtime_multi_integration_test.go:102: postgres-analytics runtime security: bh-local-multi-ci-206131-dev/postgres-analytics runs as root (Config.User="")` |
| 43754879419 | f55d9f94 (#1592) | validate :: Validate documentation | identische 7 `literal lost` + `DE technical integrity: FAIL (7 findings across 167 paired pages)` (log:879) |
| 43754882137 | 018b4e58 (#1594) | validate :: Run runtime integration tests serially | 5× ORAS + `bh-local-multi-ci-204673-dev/postgres-analytics runs as root` |
| 43755008378 | 3a91e2a8 (uid-target, #1580) | validate :: Run runtime integration tests serially | 5× ORAS + `bh-local-multi-ci-203079-dev/postgres-analytics runs as root` |
| 43756793609 | eda0cd61 (#1595) | validate :: Run runtime integration tests serially | 5× ORAS + `bh-local-multi-ci-203035-dev/postgres-analytics runs as root` |
| 43757001183 | develop 0e9ccb582 (BASELINE) | validate :: Run runtime integration tests serially | 5× ORAS + `bh-local-multi-ci-203618-dev/postgres-analytics runs as root` |

Normalisierte Signaturen:

- Signatur D = `DE technical integrity: FAIL (7 findings across 167 paired pages)` über genau diese 7 Literale in `docs/spec/management-access-v1.md`: `baha app status --json`, `baha status --json`, `configured_unverified`, `management-ui`, `not_configured`, `perses`, `verified`.
- Signatur O = `ORAS is required before Core setup` in den 5 Tests `TestRepositoryWorkflowRealLifecycle` (app_repository_integration_test.go:27), `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI` (app_workload_integration_test.go:60), `…ComposeWorkloadOnlyLifecycleInCI` (:191), `…ComposePinnedWorkloadLifecycleInCI` (:347), `…BuildWorkloadRebuildsSourceChangesInCI` (:503).
- Signatur R = `postgres-analytics runtime security: … runs as root (Config.User="")` in `TestMultiInstanceComposeLifecycleInCI` (runtime_multi_integration_test.go:102).

Vor dem jeweils FALSCH-gegangenen Step waren in allen 7 runs alle content-Gates grün, die bis dahin liefen (Checkout→docs bzw. Checkout→unit bei den O/R-runs: workflow syntax, formatting, source readability, unit+package tests alle success).

## Zelle 2 — Vergleich gegen Baseline 43757001183 (develop 0e9ccb582)

Baseline-Signatursatz = {O, R}; Baseline `Validate documentation` = `DE technical integrity: PASS (167 paired pages)` (log:868).

- Runs 43754876950 / 43754882137 / 43755008378 / 43756793609 (#1591/#1594/uid-target/#1595): exakt {O, R} — identische Testnamen, identische file:line, identische Meldungen (nur Per-Run-Projektzahl `ci-<N>` variiert). **BASE-PARITY BESTÄTIGT.**
- Runs 43754874604 / 43754879419 (#1590/#1592, Perses-Kette): Signatur D, in der Baseline NICHT vorhanden. Sie ist KEIN Runner-/Base-Defekt, sondern additive Kandidaten-Kette: die 7 Literale existieren auf develop 0e9ccb582 in beiden Dateien gar nicht in Backticks (`git show 0e9ccb582…:docs/spec/management-access-v1.md | grep -cE '…'` = 0; DE = nur `exact`/`limited`). Eingeführt wurden sie ausschließlich commits auf dem Perses-Zweig zwischen Baseline und head: `git log 0e9ccb582..85b4cbb5 -- docs/spec/management-access-v1.md` = `61f76fa18`, `181872c90`, `a5a5abedc`, `af308e66d` (alle 0428-075 auf lane-0428-075-perses-seam, 2026-11-14/15). Die PR-Diffs #1590/#1592 selbst (base=075-seam) berühren die Doku nicht (`gh pr diff --name-only` = 0 Treffer) — der Defekt sitzt im Base-Branch der Kette, nicht im letzten Commit. **KEINE base-parity → ECHTER Kandidaten-/Zweig-Defekt:** EN/DE-Parity-Verstoß (Doku-Übersetzungs literals wurden im EN-only gepflegt).
- Verankerungscheck Ancestry: 0e9ccb582 ist Vorfahr aller 6 heads (`git merge-base --is-ancestor` = YES je); alle heads = exakte remote branch tips (`git rev-list --count tip..head` = 0 je; #1590: head = fetcher branch-tip). Keine head trägt develop-commits jünger als die Baseline (`git log 0e9ccb582..head --merges` = leer).
- Hinweis zur Vergleichbarkeit: die Baseline-Zelle lief docs→integration (docs PASS, dann O/R FAIL); bei #1590/#1592 blockierte docs (D) vor dem Integration-Step, ihr O/R-Verhalten ist in diesen runs also unbeobachtet — nach D-Korrektur würde dieselbe base-Seitige O/R-Signatur dort erwartet (dieselbe Workflow-Datei, derselbe Runner).

## Zelle 3 — Verwurzelung (file:line-Zeugen)

Signatur D (7 DE-findings):
- Datei: `docs/spec/management-access-v1.md` (EN) vs `docs/de/spec/management-access-v1.md` (DE). Gate-Logik: `scripts/check_de_translation_integrity.py:34-36` (inline-backtick-Vergleich EN⊆DE, Meldung `literal lost`) und `:40` (`DE technical integrity: FAIL …`), aufgerufen von `scripts/documentation-audit.sh:160`.
- Ursprungs-commits: `61f76fa18 feat(0428-075): define optional Perses provider seam (fail-closed)` (EN-Datei, Backtick-Literale), dann `181872c90`/`a5a5abedc`/`af308e66d` (u. a. `baha app status --json`/`baha status --json`) — alle auf refs/heads/lane-0428-075-perses-seam (Zweigtip af308e66d), NOT auf develop. Diese Commits fließen als Kanten-Base in #1590/#1592 ein. Die DE-Seite wurde in `0e9ccb582..heads` nie gepflegt (`git log 0e9ccb582..85b4cbb5 -- docs/de/spec/management-access-v1.md` = leer), deshalb genau 7 findings; `af308e66d` nennt in seiner Message „align … with three-state contract“ ohne DE-Spiegelung.

Signatur O (ORAS fehlt am Runner):
- Fehlerquelle: `cmd/baha/oras_setup.go:40-41` (`errors.New("ORAS is required before Core setup; …")` in `ensureORASForCoreUpWith` bei nicht-interaktiv fehlendem `oras` im PATH; eingeführt mit `0e4d8378a feat: approve user-local ORAS setup during Core up`, 2026-11-11, auf develop). Aufrufpfad: `baha up --control-plane-only --yes` in `cmd/baha/runtime_integration_test_support_test.go` (ensureIntegrationTrustPlane → `runWithIO ["up" …]`, `t.Fatalf("prepare BaseHarbor integration trust plane: %v", …)` Zeile 840).
- Runner-Seite: der CI-Job `validate` (der bei workflow_dispatch auf develop/heads läuft) hat KEINEN `Install verified ORAS`-Step; der Step existiert nur im PR-Pfad `pr_native_destroy` (Zeuge: `git show 0e9ccb582…:.github/workflows/ci.yml` — validate-Job-Zeilen 256-423 ohne ORAS, ORAS-Step nur Zeile 485; eingeführt mit `693380523 fix: resolve PR onboarding CI failures`, 2026-11-11, 2 Zeilen ci.yml). => Die ORAS-Pflicht wurde 0e4d8378a dem Core-up-Pfad auferlegt, aber die develop/dispatch-Zelle `validate` nie nachgezogen (693380523 bediente nur den PR-Zweig). Reiner base/runner-Defekt.
- Benötigte Korrektur liegt unter `.github/workflows/ci.yml` (Owner-Scope) — als Befund gemeldet, nicht geändert.

Signatur R (postgres-analytics runs as root):
- Prüfer: `internal/application/runtime_multi_integration_test.go:99-102` ruft `containersecurity.VerifyComposeService` je service; die Root-Meldung kommt aus `internal/testsupport/containersecurity/security.go:57-58` (`if isRootUser(r.Config.User) && !rootlessPodman()` → `… runs as root`). Test eingeführt `dae7de51f` (2026-09-08), auf develop. Der root-Pfad ist runtime-abhängig: auf einer echten rootless-Podman-Zelle wäre `Config.User=""` toleriert; die `validate`-Zelle läuft mit `BASEHARBOR_TEST_RUNTIME: docker` (ci.yml:276) auf ubuntu-latest.
- Seite: die generierten application-Compose-Dateien setzen für die postgres-Instanzen (auch analytics) gar kein `user:` mehr (Zeugen: `internal/application/runtime_postgres.go` render-Pfade ohne `user`-Key; `internal/runtime/assets/compose.yaml` ohne jedes `user:`-Feld; `shared_backends_test.go:202` und `runtime_postgres_test.go:505` erzwingen ausdrücklich, dass generierte Composes KEIN `user:` enthalten). Lastige develop-Änderungen: `f8fe4701b fix: allow postgres volume initialization` (2026-11-11 11:55, entfernt `user: postgres`), `a987d6372 fix: grant PostgreSQL startup capabilities` (12:04), `83d97738e fix: scope postgres TLS key to service user` (12:11), `b22c0008a fix: support arbitrary container uids and readable projections` (2026-11-11 00:07, letzte Fassung von `internal/runtime/assets/compose.yaml`) — alle auf develop. => Der Root-Lauf ist eine bewusste develop-Entscheidung (rootless-Docker-remap), aber der multi-Instanz-Tester wurde nicht mitgenommen; baseline-identischer Fail. Kein Kandidat der Welle ändert `internal/runtime/assets`, `runtime_postgres.go`-Render oder `runtime_multi_integration_test.go` vs Baseline (`git diff --name-only 0e9ccb582..head` = leer je; #1594 ändert nur `workload_security.go`, kein Pfad dieses Tests — Fund bleibt base-seitig).

## Zelle 4 — Urteil-Tabelle

| Kette / PR | Run | Signaturen | Urteil |
| --- | --- | --- | --- |
| #1591 env-registry | 43754876950 | O,R | **base-parity** |
| #1594 cli2-env-policy | 43754882137 | O,R | **base-parity** |
| #1580 uid-target | 43755008378 | O,R | **base-parity** |
| #1595 cli2-source-model | 43756793609 | O,R | **base-parity** |
| develop BASELINE | 43757001183 | O,R | Referenz (rot durch O,R — base-Defekt belegt) |
| #1590 perses-selection | 43754874604 | D (O,R nicht beobachtbar: Step skipped nach Docs-Fail) | **echter Kandidaten-/Zweig-Defekt** (EN/DE literals in lane-0428-075-perses-seam nicht gespiegelt; Korrektur: 7 Literale nach docs/de pflegen ODER Backticks im EN entfernen) |
| #1592 perses-runtime | 43754879419 | D (wie oben) | **echter Kandidaten-/Zweig-Defekt** (derselbe Fund, dieselbe Base-Kette) |

Gesamtthese: für 4/6 PRs voll bestätigt (base-parity). Für die Perses-Kette (#1590/#1592) widerlegt: additive Signatur D ist zweig-seitig erzeugt (Commits 61f76fa18..af308e66d) — Kandidaten-Defekt, kein Base-/Runner-Defekt. Hinweis: ob D die Kette auch unter O/R „retten“ würde, ist offen, da der Integration-Step nach Docs-Fail skipped; der Docs-Step ist aber deterministisch, D bleibt bis zur Korrektur.

## Befunde (für Coordinator/Owner)

- FINDING-1 (Owner-Scope, .github/**): `.github/workflows/ci.yml` validate-Job (~line 283ff, develop 0e9ccb582) braucht einen `Install verified ORAS`-Step (analog `scripts/ci-install-oras.sh`, wie Zeile 485/486 im pr_native_destroy-Job), sonst bleibt jede develop/dispatch-Zelle in „Run runtime integration tests serially“ ROT (Signatur O). file:line-Zeuge: ci.yml:485-486 vs validate-JOB-Block ohne Step.
- FINDING-2 (base-Defekt Produktcode/asset): `postgres-analytics` im multi-instance-Pfad läuft ohne `user:` → runtime_multi_integration_test.go:102 fails auf develop selbst (Signatur R). Verwurzelt in den UID-Änderungen 83d97738e/b22c0008a/f8fe4701b/a987d6372 (alle 2026-11-11, develop); der multi-Instanz-Tester wurde nicht mitgenommen; blockiert alle develop/dispatch-Zellen.
- FINDING-3 (Perses-Kette): EN-only-Doku in `docs/spec/management-access-v1.md` durch 61f76fa18/181872c90/a5a5abedc/af308e66d ohne DE-Spiegelung → Doku-Korrektur auf lane-0428-075-perses-seam nötig, danach neue exact-head runs für #1590/#1592 (deren O/R-Lane unabhängig; nach FINDING-1-Korrektur wird der restliche Integrationspfad erst sichtbar).
- FINDING-4 (Kontrollverlust-Notiz): Die 6 PR-heads sind Ketten-base-branches (uid-target, env-registry, 075-seam, perses-runtime…), nicht develop; Base-Parity-Vergleiche müssen die Kanten-Base mitdenken (wie hier geschehen).

## cleanliness

- Read-only Mission: keine Container/Netzwerke/Volumes/State-Verzeichnisse auf diesem Host oder einem Ziel-Host erzeugt (keine docker/podman-Befehle; SSH-Hosts nicht benötigt). Alle Artefakte unter /tmp/opencode/bp/ (logs/, parity/ docs-extract, *.txt, *.sh, *.yml).
- Produktrepo baseharbor: nur fetch/show/log/merge-base (keine Schreibrefs außer fetched remote-tracking refs).
- Planungszonen-Check: `workers/baseharbor-plan` wurde nicht committet; nur `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (Toplevel-Zeuge oben). Fremde Working-Tree-Änderung dort (`cli2-uid-target/driftfix-r1.md`, anderer Lane) wurde NICHT angerührt oder committet.
- state-Verzeichnisse: /tmp/opencode/bp ist das einzige state-Verzeichnis dieser Lane.

## Candidate / Evidence provenance

- KEIN Produktkandidat, KEIN PR (Abnahme-/Zeugnis-Mission). Candidate = die 7 bestehenden gehosteten runs (URLs in Zelle 1-Tabelle; alle under https://github.com/mcpdev80/baseharbor/actions/runs/<id>).
- Runs/Logs gemessen 2026-11-15 (MESZ) gegen exakte head SHAs (gh pr view headRefOid + ls-remote bestätigt).
- Diese Akte enthält keine Markdown-Checkboxes (Kontrolle: `grep -cE '^\s*- \[' round-1.md` = 0, beim Commit-Lauf ausgeführt).

## repo-rule compliance

- §4.6 Eigenes-Run-Pflicht: keine neuen gehosteten Läufe ausgelöst (read-only Mission, Mission: „nur bestehende runs lesen“); alle 7 Referenz-Run-Ergebnisse wörtlich aus `gh run view --log` aufgenommen.
- Owner-Scope `.github/**`: nicht editiert; FINDING-1 mit file:line gemeldet.
- §4.8 keine Subagenten; alles in dieser Session ausgeführt.
- Evidence ausschließlich in baseharbor-plan (diese Datei), keine Produktrepo-Schreibaktion, keine Checkboxes in dieser Akte.

## END

END_DONE mission-baseparity.md: Base-Parity für #1591/#1594/#1580/#1595 bestätigt (Signaturen O,R baseline-identisch); #1590/#1592 tragen additiven Zweig-Defekt D (Perses-EN/DE literals, Commits 61f76fa18..af308e66d) — These teilweise widerlegt, Befunde 1-4 in der Akte.
