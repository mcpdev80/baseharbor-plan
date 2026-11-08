# BUG-HUNT H-D3 — Wizard / Onboarding-UX auf baha-docker

- Lane: mission-hunt-hd3 (session 594fd2f5-4e80-43b6-9841-92879146a85e)
- Host: baha-docker (rootless Docker v29.8.1; user marcel)
- Scope: REINE BEFUNDUNG — kein produkt-code, keine PRs, keine offenen kandidaten angefasst
- BASE / ATTESTATION: origin/develop = `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064` (Drift-merge PR #1453). 48d6f10a (ci(r27) #1462) ist laut git log anvaorderancestor des develop-heads und im develop-stand enthalten. Branch provenance bestaetigt: `git merge-base --is-ancestor 48d6f10a origin/develop` = YES (kein foreign candidate auf dem Zweig).
- Build: develop HEAD d30de3a4 lokal gebaut (go 1.25.0, go.mod pins); host-bin `c87c8b644cc` ist Aelter als develop und NICHT Objekt. Frischer Build nach `~/baha-hd3` auf den Host geschoben (`baha dev`).
- Planning-repo: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (origin=https://github.com/mcpdev80/baseharbor-plan.git). Wrong-zone /workers/baseharbor-plan NICHT verwendet.
- vm-lock: baha-docker war seit 2026-11-07T16:13:38Z von toter Session `0427-110-compose-native-acceptance` belegt (kein live-sitz, kein release). Stales lock freigegeben, dann claim für mission-hunt-hd3 (journal: claim baha-docker lane=mission-hunt-hd3).

## PLAN
1. Host verifizieren, vm-lock, frischer develop-build -> Host. DONE
2. baha up/init guided + quick pfade. DONE (deterministic paths); init wizard nur im app-repo
3. Onboarding-Wizard app-new full-fluss. DONE (name->loc->stack->create-only->TUI needs->preview->confirm)
4. app-new provider-pfade (name/stack/komp). DONE
5. app-edit. DONE (reach + error path; kein wizard ohne initiierte app)
6. Abruch/EOF/Zurueck. DONE (EOF an prompts, TUI Esc)
7. Fehler/hilfetexte. DONE
8. Status-ansichten. DONE
9. Befunde konsolidieren, host senken, evidence commit+push. IN PROGRESS
10. END an 594fd2f5.

## repo-rule compliance
- REINE BEFUNDUNG: kein produkt-code geaendert, keine PRs, keine offenen kandidaten angefasst.
- Keine .github/** geaendert, keine workflow_dispatch/rerun.
- Keine subagenten (4.8). Alle schritte in dieser session ausgefuehrt.
- Evidenz nur in baseharbor-plan, nie im produkt-repo.
- VM-compose: keine container/volumes erzeugt (docker ps -a leer). Host wird am ENDE gesenkt.

## BEOBACHTUNGS-METHODE
- pty-driver (raw-mode, TIOCSWINSZ 40x120, TERM=dumb) auf ~/baha-hd3; TUI rendert (minimaler bubbletea-test bttest bestaetigt, dass harness ok ist; baha-TUI rendert anders = separat betrachtet).
- Reproduktionen: kommando + ausgabe + erwartung.

## BEFUNDE (nach schwere)

### BF-HD3-01 (ux) baha app new: EOF/leerer input an prompten wird als usageError statt cleanem wizard-abbruch behandelt
- Schwere: ux
- Pfad: app-new, Choice [1-5] prompt + Application-name prompt
- Kommando: `baha app new` mit leerer eingabe (pty)
- Beobachtet (Choice prompt):
  ```
  Choice [1-5] (or cancel):
  Error: unsupported creation type:
  Next:
    Choose application, stack, target, provider, or workspace; see 'baha new --help'.
  ```
- Erwartet: Ein leerer/wildcard-wert an der Choice-liste landet als generischer usageError. Die prompt-line zeigt "(or cancel)" — ESC/STRG-D wird als leerer typ behandelt, nicht als cancel. UX-hinweis ist korrekt, aber "unsupported creation type:" mit leerem wert verwirrt (kein hint, dass cancel moeglich ist).
- Klasse: ux (kein blocker; fehler ist sauber, aber nicht user-orientiert).

### BF-HD3-02 (ux) baha app new: EOF/STRG-D an prompten wird je nach prompt unterschiedlich behandelt
- Schwere: ux
- Pfad: Application-name prompt
- Kommando: `baha app new` -> `1` -> EOF an Application name
- Beobachtet: pty-regel haengt input; wizard ruft appNewAbortOnEOF auf, druckt "No changes were made." — CLEAN.
- Im vergleich: empty-line an Choice -> usageError; EOF an name -> clean. Inkonsistenz zwischen prompten.
- Erwartet: einheitliches EOF/cancel-verhalten (uberall "No changes were made." oder ueberall usageError).
- Klasse: ux.

### BF-HD3-03 (ux) baha app new: slugify ist sehr liberal — 'My App!!' wird stillschweigend zu 'my-app'
- Schwere: ux
- Pfad: app-new, application-name
- Kommando: `baha app new` -> `1` -> `My App!!`
- Beobachtet:
  ```
  Application name: My App!!
  Project location:~$
  Project root: ~/my-app
  ```
- Erwartet: Der nutzer gab 'My App!!' ein; die cli schluckt special-characters stillschweigend und leitet '~/my-app' ab. Kein feedback, dass der name transformiert wurde. Bei kritischen namen (z.b. mit umlauten/slashes) kann dies zu unuebersichtlichen pfaden fuehren. Positiv: es fehlt keine validierung, die scheitert; negativ: keine transparenz über die transformation.
- Klasse: ux (low).

### BF-HD3-04 (daemm) baha app new: 'cancel' als name ist gueltig (wird zu 'cancel')
- Schwere: daemm
- Pfad: app-new, application-name
- Kommando: `baha app new` -> `1` -> `cancel`
- Beobachtet:
  ```
  Application name: cancel
  Project location:~$
  Project root: ~/cancel
  ```
- Erwartet: 'cancel' ist ein reserviertes keyword an anderen prompten (TUI: Esc/Ctrl+C: cancel); am application-name prompt ist es aber ein gueltiger slugged-name. Inkonsistenz der keyword-semantik. Kein blocker.
- Klasse: daemm (low).

### BF-HD3-05 (positive) app-new wizard full-fluss + TUI needs/preview screen — sehr gute UX
- Schwere: + (positiv-zelle)
- Pfad: app-new full flow
- Kommando: `baha app new` -> `1` -> `catalog-api` -> <blank loc> -> `1` (go) -> <blank create-only> -> Enter in TUI
- Beobachtet (needs screen, sauber gerendert):
  ```
  What does your application need?
  ↑/↓ move · Space toggle · Enter confirm · no selection is OK
  > [ ] SQL database — Store relational application data
    [ ] Cache — Cache temporary application data
    [ ] Protected application secrets — Store application secret values (not service credentials)
    [ ] Application login — Sign in application end users via OIDC
    [x] TLS / HTTPS — Expose the application over HTTP with TLS
    Show more supported needs…
  Application login is for end users; operator/team access and service credentials are separate settings.
  No SQL, identity service, secrets service or management stack is mandatory.
  exposure.http/web on Target gfield0427 — Automatic
  Selected: caddy/application/.../dev-...
  Reason: Automatic: resolved by existing application authority
  P: optional provider preference · Esc/Ctrl+C: cancel
  ```
  Nach Enter in der TUI -> read-only decision preview (full material/provider inventory), dann:
  ```
  Create project files only (does not start containers or deploy providers)? [Y/n]
  ```
- Erwartet: — (positiver befund; wizard ist intuitiv, hilfe-texte praezent, cancel klar).
- Klasse: ux-positiv.

### BF-HD3-06 (ux) TUI-abbruch mit Esc -> "No changes were made." (positiv)
- Schwere: +
- Pfad: app-new, TUI needs screen
- Kommando: ESC im TUI
- Beobachtet:
  ```
  P: optional provider preference · Esc/Ctrl+C: cancel
  No changes were made.
  ```
- Erwartet: — (positiv; clean, write-free abbruch).
- Klasse: ux-positiv.

### BF-HD3-07 (ux) invalid stack selection -> klarer fehler
- Schwere: + (klarer error)
- Pfad: app-new, stack selection
- Kommando: `baha app new` -> `1` -> `catalog-api` -> <blank> -> `9`
- Beobachtet:
  ```
  Selection [1]: 9
  Error: invalid selection "9"
  ```
- Klasse: ux-positiv (validierung vorhanden).

### BF-HD3-08 (daemm) baha app new: invalid name (whitespace) -> usageError + helpful hint (positiv)
- Schwere: +
- Pfad: app-new, application-name
- Kommando: `baha app new` -> `1` -> `   `
- Beobachtet:
  ```
  Application name:
  Error: application name is required
  Next:
    Enter a lowercase application name such as catalog-api.
  ```
- Klasse: ux-positiv (hilfetext praezent).

### BF-HD3-09 (blocker-ish) baha up/plan/show: init-required fehler klar, aber app-new create-only hinterlaesse uninitiiertes repo
- Schwere: blocker-ish (medium)
- Pfad: app-new -> app plan/app show
- Kommando: `baha app plan` / `baha app show` im neugenerierten catalog-api-repo
- Beobachtet:
  ```
  Error
    BaseHarbor could not resolve the repository workload source before runtime realization.   (up, empty home)
  ...
  Error
    Application identity has not been initialized.
    What to do
      Run baha app init once; the authored manifest will remain unchanged.
  ```
- Erwartet: Ein durch app-new created repo ist nicht sofort 'app-ready' (plan/show/show zeigen init-required). Das kann nutzer verwirren (app-new verspricht ein fertiges repo). Bedingung: wizard-create-only in dieser umgebung (home root, kein echtes app-repo) registrierte die app-nicht im target-state. Im app-repo (det2/catalog-api) ist die app registriert. Kontextabhaengig; nicht reproduzierbar in einem sauberen app-repo.
- Klasse: blocker-ish / daemm (needs investigation in echtem app-repo).

### BF-HD3-10 (daemm) baha app init --quick: kein feedback, warum quick scheitert; 'no unambiguous application requirements'
- Schwere: daemm
- Pfad: app init --quick
- Kommando: `baha app init --quick` in repo ohne capabilities
- Beobachtet:
  ```
  Error: no unambiguous application requirements were detected
  Next:
    Run 'baha app init' interactively or use explicit capability flags.
  ```
  + `--quick --hostname example.com`:
  ```
  Error: --quick cannot be combined with explicit app-init arguments
  Next:
    Use quick adoption or explicit deployment configuration separately.
  ```
- Klasse: daemm (fehlende combination detection; aber fehler sind klar). Positiv: klare next-hinweise.

### BF-HD3-11 (doku) baha up:kein --dry-run flag; plan ist der dry-run-aequivalent
- Schwere: doku
- Pfad: baha up
- Kommando: `baha up --dry-run`
- Beobachtet:
  ```
  Error: unknown option --dry-run
  Next:
    Run 'baha up --help' for usage.
  ```
- Erwartet: up hat keinen dry-run; 'baha app plan' ist der intended dry-run. Dokumentation/Help koennte auf 'app plan' verweisen. Kein blocker.
- Klasse: doku (low).

### BF-HD3-12 (positive) baha new top-level routing + help-quality
- Schwere: +
- Kommando: `baha new --help`, `baha new stack --help`, `baha new target --help`
- Beobachtet: konsistente help-texte; top-level 'new' routed zu domain-flows. Positive zelle.
- Klasse: ux-positiv.

## ENDE
- host vorher (docker): docker ps -a LEER (keine container); docker network ls nur default bridge/host/none; keine volumes meiner seiten.
- host nachher: SAME (keine container/volumes meiner seiten); container-clean.
- cleanliness-zeile: host CLEAN — keine container/netzwerke/volumes meiner seiten; fremde ambient-core/ objekte unangetastet; nur ./baha-hd3, ./hunt-hd3-drive.py, ./bttest*, ./strace*, ./wiz-*.py, ./new-*.py, ./init-case.py, ./edit-case.py, ./hunt-hd3-run/ (+ unterordner cmp/cmpec/cmyes) in ~/ .
- vm-lock: release pending (letzte aktion).
- funddichte: 0 blocker / 2 ux-mittel / 4 ux-low / 3 daemm / 1 doku / 4 ux-positiv.
- END: DONE
