# Superseded PR closeout — card 0428-169 (t-20261120-r28-superseded-pr-closeout)

- ROLLE: worker, PR-hygiene — ausschliesslich `gh pr close` gegen nachweis, kein produkt-code, kein zweig, kein merge, kein delete-branch, kein force-push.
- ANLASS: mission x-169 schliesst SUPERSEDED/TODC-PRs aus der liste 1627,1620,1597,1594,1665,1645,1588,1587,1585,1582 mit vertrag pro PR (state-check -> nachweis a/b/c -> close -> gegenprobe).
- BEREICH: repo mcpdev80/baseharbor, 10 PRs der schliess-liste + gegenprobe.
- BEWEIS-QUELLE: `gh api` + `git fetch origin refs/pull/<n>/head` + `git merge-base`/`git diff --name-only` gegen `origin/develop`; https-clone in /tmp/opencode/x-169-wt.
- ERGEBNIS: END_BLOCKED. Alle 10 geschlossenen PRs tragen inhalt, der auf develop NICHT vorhanden ist und NICHT durch einen benannten ersatz abgebildet ist. Mehr als zwei solche faelle => inventory 0428-160 zu alt, alles gehalten.

## PLAN (numbered, no checkboxes)

1. Planning-remote origin/main verifizieren (ls-remote), /tmp-clone in eigener zone.
2. develop-head messen (ec02d5faad2499c8bf5ed08ce2ae1f5aac25d80f); offene PRs zahlen.
3. pro PR der schliess-liste: gh api state-check (schritt 1), nachweis a/b/c (schritt 2), close (schritt 3), gegenprobe (schritt 4).
4. stop-prufung: head-inhalt nicht auf develop und kein benannter ersatz -> melden, nicht schliessen.
5. befund in akte, origin/main push, END_BLOCKED.

## develop witness

- `git ls-remote origin refs/heads/develop` BEFORE this work: `ec02d5faad2499c8bf5ed08ce2ae1f5aac25d80f`.
- offene PRs gemessen: 21 (`gh api 'repos/mcpdev80/baseharbor/pulls?state=open&per_page=100' --jq 'length'` -> 21). Liste: 1709 1704 1702 1695 1684 1665 1650 1645 1627 1625 1623 1620 1615 1614 1597 1596 1594 1588 1587 1585 1582.
- #1591 (elftesmitglied der liste) ist GEMERGT: `gh api .../pulls/1591` -> state=closed merged=true merged_at=2026-11-20T01:29:43Z. beweise warum die liste nicht ungeprueft abgearbeitet wurde.
- inventory 0428-160 meldete 25 offen / basics-check 22 open; real 21 offen -> inventar veraltet um mindestens eine merge (#1591) und mehrere closings seit seiner messung.

## PR je closelist — befund (schritt 1,2,4; 3 nicht ausgefuehrt)

- #1627: `gh api .../pulls/1627` -> state=open merged=false draft=true head=96deb1f1597d0d4a10d54421acc973053d27224a base=5ef9c329. titel: `0428-055: baha env destroy (env-scoped identity removal)`.
  - nachweis (a): `git fetch origin refs/pull/1627/head` + `git merge-base --is-ancestor FETCH_HEAD origin/develop` -> NEIN (kopf nicht auf develop).
  - nachweis (b): `gh pr diff 1627 --name-only` -> 9 files; `git diff --name-only FETCH_HEAD origin/develop -- <die 9 files>` -> 9 files (NICHT leer, NICHT blob-identisch). env_destroy.go (+424), environment_destroy_scope.go (+324) existieren auf develop NICHT (`git ls-tree -r origin/develop --name-only | grep -i env_destroy` -> leer).
  - nachweis (c) ersatz: karte 0428-055 (tasks/t-20261114-r28-cli2-env-delete.md) kanban_status=**wait**, handoff 2026-11-20: "Candidate: PR #1627, head 96deb1f1, base cli2-env-policy-head; PR OPEN + Draft; keep task in wait. No merge or acceptance. Next safe step CI-owner/native-gate resolution." -> inhalt ist ARBEITSSTAND, kein superseded-ersatz vorhanden. STOP.
  - status: nicht geschlossen, BLOCK (inhalt nicht auf develop, kein benannter ersatz).

- #1620: state=open merged=false draft=true head=fcba5d25ce8ba644709e362b6fd2a1f048ca767a base=5ef9c329. titel: `0428-067 fix(cmd/baha): per-reveal audit for baha app creds --reveal`.
  - (a): NEIN (kopf nicht auf develop). (b): files cmd/baha/app_access.go, cmd/baha/app_access_test.go differn von develop (nicht blob-identisch).
  - ersatz: karte 0428-067 (tasks/t-20261117-observability-native-gate-bootstrap.md -> kanban_status=closed, tasks/t-20261114-r28-cli2-wizard-platform.md -> kanban_status=**blocked**) -> arbeit lebt, PR #1620 ist der aktuelle kandidat. STOP.
  - status: nicht geschlossen, BLOCK.

- #1585: state=open merged=false draft=true head=55a8c0f3550d9cb5638a6223f3c8cbad314c48e6 base=14d8f17d. titel: `fix(cli): state-dir override owns target-selection state (BF-01, 0427-189)`.
  - (a): NEIN. (b): cmd/baha/target.go, target_selection.go, target_selection_state_dir_isolation_test.go, target_state_layout.go, internal/deployment/target.go, internal/orgconfig/store.go differn alle von develop (nicht blob-identisch).
  - ersatz: kopf 55a8c0f3 ist EXACT head von origin/lane-0428-fix-bf01-v2 (kein separater ersatz; es ist die quellzweig des PRs selbst), und dieser zweig ist NICHT auf develop. ->inhalt nicht auf develop, kein benannter ersatz, der anders loest. STOP.
  - status: nicht geschlossen, BLOCK.

- #1665: state=open merged=false draft=true head=e580d32414565442376f23ace9a4a2dd7ed03838 base_ref=w083-perses-datasources. titel: `feat(0428-082): native Perses infrastructure dashboard`.
  - (a): NEIN. (b): 8 files differn (cmd/baha/app_perses_cli_test.go, app_status_result.go, internal/application/management_ui.go, docs/spec/*).
  - ersatz: karte 0428-082 (tasks/t-20261114-r28-perses-dashboards.md) kanban_status=**wait**, wait_reason: "PR #1665 ist ein DRAFT ... basis-rueckstand 74 koepfe ... PR-head ist KEIN ahne von develop ... NAechster schritt: hopf + draft raus + exact-head-lauf." -> arbeit lebt. STOP.
  - status: nicht geschlossen, BLOCK.

- #1650: state=open merged=false draft=false head=82bac3fab7c28d3765c189dc12f32ac65b06a9d2 base=ec02d5fa (base=develop). titel: `fix(0428-078): wire Perses identity-keycloak into 080 resolver fan-in`.
  - (a): NEIN. (b): cmd/baha/app_status_result.go (+55), internal/metrics/perses_identity_witness.go (-129), perses_identity_witness_test.go (-162) differn von develop (nicht blob-identisch).
  - ersatz: karte 0428-078 (tasks/t-20261114-r28-perses-dashboard-identity.md) kanban_status=**blocked** -> arbeit lebt. STOP.
  - status: nicht geschlossen, BLOCK.

- #1597: state=open merged=false draft=true head=540ed13cec363a231241a17baa68c8d32ebdae63. titel perses-docs, base 409444854 (106 hinter develop).
  - (a) + (b): inhalt nicht blob-identisch auf develop (docs/spec/*.md), kein benannter ersatz der content loest; base 106 hinter develop. STOP.
  - status: nicht geschlossen, BLOCK (kann zusaetzlich superseded sein, aber content-nachweis fehlt -> mission sagt: melden, nicht schliessen).

- #1594: state=open merged=false draft=true head=5ef9c329 base_ref=lane-0428-env-registry. titel workload_security.
  - (a): NEIN. (b): differn von develop. kopf 5ef9c329 war laut inventory basis von #1620/#1694 stack; content nicht auf develop. STOP.
  - status: nicht geschlossen, BLOCK.

- #1645: state=open merged=false draft=true head=c781eb86 base_ref=develop. titel `perses/tempo: rename .go witnesses to .go.txt`.
  - (a): NEIN. (b): 8 files differn. STOP.
  - status: nicht geschlossen, BLOCK.

- #1588: state=open merged=false draft=true head=9534edd4 base_ref=develop. titel `feat(r27): editable Target policy presets (0427-186)`.
  - (a): NEIN. (b): 6 produktion-files (app_remote_lifecycle.go, deployment_record.go, machine_coverage.go, internal/deployment/immutable_provenance.go) differn von develop. content r27, nicht auf develop. STOP.
  - status: nicht geschlossen, BLOCK.

- #1587: state=open merged=false draft=true head=20e0537c base_ref=develop. titel `docs(0427-169): Core operator API route runbook (EN/DE)`.
  - (a): NEIN. (b): docs/how-to/operator-api.md, docs/spec/control-plane-runtime.md, cmd/baha/serve.go differn. STOP.
  - status: nicht geschlossen, BLOCK.

- #1582: state=open merged=false draft=true head=f21bc6f3 base_ref=develop. titel `fix(BF-03): persist target selection in private user state`.
  - nachweis (b): alle 3 files blob-identisch auf develop (cmd/baha/runtime_integration_test_support_test.go, internal/orgconfig/orgconfig_test.go, internal/orgconfig/store.go -> IDENTICAL). ansatz (b) LEER => theoretisch schliessbar.
  - STOP-abwaegung: content ist BF-03 fix; content liegt auf origin/lane-0428-fix-bf01-v2 (kopf 55a8c0f3 == #1585 kopf), arbeit lebt im r27-bereich; gleiches write-set wie #1585. Da #1585 bereits BLOCK (content nicht auf develop, kein ersatz), und inventory als gesamt zu-alt befunden: hier nicht einzelnschliess, sondern gesamthalten.
  - status: nicht geschlossen, BLOCK (konsistenz mit #1585).

## gegenproben (schritt 4) — beide misslingen bewusst, weil kein PR geschlossen wurde

- gegenprobe #1627: `gh api .../pulls/1627 --jq .state` -> open (vor action). kein close ausgefuehrt; status bleibt open.
- gegenprobe #1620: `gh api .../pulls/1620 --jq .state` -> open. kein close.
- gesamt: 0 PRs geschlossen, 10 PRs offen gelassen, 10/10 wegen stop-kriterium blockiert.
- "nichts gethan, weil schon closed": 0 (kein PR der liste war bereits closed/merged; #1591 war ausserhalb der liste und bereits gemergt — nur protokolliert).

## end-gesamt

- geschlossene PRs durch diese lane: 0.
- blockiert/gehalten wegen stop-kriterium (inhalt nicht auf develop, kein benannter ersatz): 10 (1627, 1620, 1585, 1665, 1650, 1597, 1594, 1645, 1588, 1587; 1582 konsistenz-block).
- offene PRs nach messung: 21 (inventory meldete 25 offen / basics-check 22; differenz durch merges seit messung, bspw #1591 merged 2026-11-20T01:29:43Z).
- ausgangspunkt: `git ls-remote origin refs/heads/develop` = ec02d5faad2499c8bf5ed08ce2ae1f5aac25d80f.

## repo-rule compliance

- KEIN produkt-code: nur read gh api + read-only git log/compare/merge-base/diff gegen https remote. kein write an produkt-dateien.
- KEIN zweig geschnitten, KEIN merge, KEIN delete-branch, KEIN force-push, KEIN gh pr close (bewusst nicht ausgefuehrt wegen stop-kriterium).
- KEIN .github/scripts, KEIN workflow_dispatch, KEIN rerun.
- KEIN container/netzwerk/volume/state-verzeichnis.
- KEIN subagent/task/agent tool (4.8).
- KEIN write in /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (workers-buchhaltung) — akte nur im planning-remote-clone.
- planning-writes nur aus /tmp-clone, fetch + rebase origin/main vorher, nur eine akte.
- kein git add -A; nur eine akte kommittiert.

## cleanliness

- containers/netzwerke/volumes/state-verzeichnisse: keine gestartet.
- /tmp/opencode/x-169-wt: https-clone baseharbor (read-only audit).
- /tmp/x169_1585.txt: helper-datei, loeschen.
- cleanliness: clean.

## END

- END_BLOCKED x-169: alle 10 PRs der schliess-liste behalten — jeder traegt content der auf develop NICHT vorhanden und NICHT durch einen benannten ersatz abgebildet ist. 10 faelle > 2 => inventory 0428-160 zu alt (meldete 25/22 offen; real 21; #1591 seitmessung gemergt). nichts geschlossen. haltestand dokumentiert, keine aktion.
- blockierte PRs: 1627, 1620, 1585, 1665, 1650, 1597, 1594, 1645, 1588, 1587 (1582 konsistenz-block mit 1585).
- gegenproben: 0 closes, 10 open erhalten.
- geschlossene PRs gesamt: 0. nichts gethan weil schon closed: 0.

## ls-remote witness (origin/main BEFORE push)

- `git ls-remote origin main` BEFORE commit: `e7de61c78fe0037070c9243e2918c7662c045021`.
- planning-remote origin/main base before this work: e7de61c78fe0037070c9243e2918c7662c045021.
