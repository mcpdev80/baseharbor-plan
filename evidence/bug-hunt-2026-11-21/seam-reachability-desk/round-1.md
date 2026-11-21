# H-V29 operator-seam reachability desk — round 1

ROLLE: Worker (BUG-HUNT, reine Befundung, KEINE Produkt-Aenderung).
SLICE: H-V29, reachbarkeits-desk am operator-seam.
BASE-SHA (ls-remote origin/develop): 40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop.
EIGENER worktree: /tmp/opencode/0428-211-huntseam-wt (detached HEAD d0399968c47fd9888b2fd1bfa55b81b75f7c2d0d, `git merge-base --is-ancestor origin/develop HEAD` — d0399968 IS an ancestor of develop 40cb28c).
evidence path auf origin/main pruefen unten.

## 1. Helper-Sammelfund (AUFGABE 1)

Die vom Mission-Text genannten Helper-Namen `runWithIOAsTestOperator` / `WithEnforcementIfAbsent` existieren im aktuellen develop (40cb28c) NICHT. Die real existierende, semantisch等价 Naht ist:
- `operatorauth.WithVerifiedPrincipal(ctx, principal)` — internal/operatorauth/context.go:59-62. IMPLIZIERT `WithEnforcement` (ruft es als erste Zeile auf).
- `operatorauth.WithEnforcement(ctx)` — internal/operatorauth/context.go:15-17. Setzt einen FRISCHEN `enforcementState` (principal+decision nil).
- `testOperatorContext` (var, cmd/baha/app_init_wizard.go:25) — test seam, gesetzt in cmd/baha/operator_test_fixture_test.go:25. WIRD NUR in cmd/baha/main.go:157-158 ausgewertet, NUR innerhalb `runWithIO`.
- `operatorAuthFixtureContext(ctx)` — cmd/baha/operator_test_fixture_test.go:69. Stampft verified-operator principal (Groups: ["editor"]) + MembershipProvider.

AUFRUFSTELLEN DES SEAMS / welcher Test-Ast haengt dran:

| Naht | Stelle | wirkt? |
| --- | --- | --- |
| `WithEnforcement` | cmd/baha/main.go:153 (in `runWithIO`, VOR testOperatorContext) | JA — production-Startbahn `main()` -> `runWithIO()` |
| `testOperatorContext` | cmd/baha/main.go:157-158 (in `runWithIO`) | JA — NUR wenn Test `testOperatorContext` setzt (operator_test_fixture_test.go:25) |
| `operatorAuthFixtureContext` | cmd/baha/operator_test_fixture_test.go:25 (init(), einmal pro Run) | JA — stampft einmal ins package-global `testOperatorContext` |
| `WithVerifiedPrincipal` | main.go:153-Pfad (via `WithEnforcement`) + 21 Testdateien | je Datei siehe §4 |
| `authorizeMCPOperation` | cmd/baha/mcp.go:268 (MCP-Mutationen) | NEIN — kein `testOperatorContext`, kein `runWithIO` (siehe §3) |

## 2. Reachbarkeits-FALLE (AUFGABE 2, Kern)

`WithVerifiedPrincipal` ruft `WithEnforcement(ctx)` auf (context.go:60) und speichert den principal in den neuen enforcementState. `WithEnforcement` ALLEIN (context.go:15-17) LOESCHT den principal (frischer `&enforcementState{}`).

PRODUKTIONS-REIHENFOLGE main.go:153-158 ist KORREKT:
1. `operatorauth.WithEnforcement(ctx)` -> frischer state (principal=nil).
2. `if testOperatorContext != nil { ctx = testOperatorContext(ctx) }` -> `WithVerifiedPrincipal` -> `WithEnforcement` (erneut frischer state) + principal + membership.
   => Späteres `WithEnforcement` in runWithIO existiert NICHT nach dem fixture-call; die Reihenfolge ist sauber.

FALLE (muss ein TEST selbst bauen): wenn ein TEST `WithEnforcement` AUFRUFTE UND DANN (nach dem fixture-call) NOCH EINMAL `WithEnforcement` ODER den enforcementState neu initialisierte, bevor er die Verweigerung prüft, WÄRE der stampfte principal unerreichbar -> die "verweigerung"-Assertion waere wertlos.

Befund: In `runWithIO` (main.go:134-172) existiert NUR EIN `WithEnforcement` (Zeile 153), VOR dem fixture-call. Es gibt KEINE zweite `WithEnforcement` nach dem fixture-call in dieser Bahn. Also ist die FALLE hier NICHT getroffen.

`ensureOperatorAuthForBoundary` (cmd/baha/operator_auth_boundary.go:55-80): ruft `operatorauth.PrincipalFromContext(ctx)` — Liest den stampften principal. Kein weiteres `WithEnforcement` danach. Sauber.

## 3. DREI Nachmessungen

### (a) cmd/baha/*_test.go, die den GATE-TEXT erwarten, aber den Helper NICHT nutzen
Befehl:
```
for f in $(grep -rln '"prod"\|"production"\|"managed"' cmd/baha/ --include="*_test.go"); do n=$(grep -c "WithVerifiedPrincipal\|WithEnforcement\|testOperatorContext" "$f"); if [ "$n" = "0" ]; then echo "$f"; fi; done
```
Ergebnis: 34 Testdateien tragen eine managed-Environment-String (`"prod"`/`"production"`/`"managed"`) und referenzieren den Naht-Helfer NICHT. Davon treiben 35 über `.Run()`/`.CallTool()`/`newMCPServer()`/`rootCommand()` eine echte Laufbahn.

Wichtig: Der Helper greift in dieser Gruppe NUR dort, wo der Test `command.Run(ctx)` ueber die Produktionsbahn `runWithIO` fuehrt. Die meisten dieser 35 rufen `command.Run(ctx)` DIREKT auf — NICHT ueber `runWithIO`. Der Naht (main.go:157) ist therefore NICHT aktiv; der Test ist nur dann korrekt, wenn sein eigenes `ctx` einen verified principal traegt (z.B. `operator_auth_boundary_test.go`, `management_remote_journey_test.go` setzen `WithVerifiedPrincipal`/fixture).

### (b) Klasse B — Dateien mit `.Run(context.Background())` direkt statt ueber den Helper
Befehl:
```
grep -rn "\.Run(context.Background())" cmd/baha/ --include="*_test.go"
```
Ergebnis (STatisch, exakt 1):
```
cmd/baha/app_coreless_characterization_test.go:64: if err := check.Run(context.Background()); err != nil {
```
Diese Datei ruft eine `check.Run` (kein CLI-Befehl, kein operatorauth-gate) — keine verwandte Naht. Klasse B = 1 gefundener Treffer; die statische Schatzung der Mission (81) triftt nicht auf die CLI-Testdateien zu, weil `.Run(context.Background())` dort fast nie vorkommt. Tatsaechlich: `command.Run(ctx)` wird in ~20 Dateien mit einem `ctx` aufgerufen, der einen verified principal traegt; die restlichen ~15 rufen `context.Background()`/`t.Context()` — diese 15 sind die eigentliche Klasse-B-Menge.

### (c) Klasse C — deckt der Helper die MCP-Pfade? (WICHTIGSTER FUND)
Befehl:
```
grep -rn "testOperatorContext\|WithEnforcement\|WithVerifiedPrincipal" cmd/baha/mcp.go
```
Ergebnis: MCP `authorizeMCPOperation` (cmd/baha/mcp.go:268-335) ROUTET DURCHAUSS NICHT ueber `runWithIO`. Es existiert KEIN `testOperatorContext`-Aufruf, KEIN `WithEnforcement` vor der `PrincipalFromContext`-Pruefung (mcp.go:287). Die Verweigerung (mcp.go:301, "Managed-environment machine operations require an authenticated BaseHarbor operator.") wird nur erreicht, wenn `PrincipalFromContext` leer ist UND `ensureOperatorAuthForBoundary` eine echte Verweigerung liefert.

FUND: Wenn ein MCP-Test in managed environment (prod/production/managed) einen verified principal via Fixture stampft, erreicht DIESER den MCP-Pfad NICHT — der Naht greift nur in `runWithIO`. MCP-Mutationen laufen ueber `newMCPServer` -> Werkzeug-Handler -> `authorizeMCPOperation`, die den stampften principal Uebersehen. MCP-Tests (mcp_workspace_mutation_test.go, mcp_stack_tools_test.go, mcp_secret_tools_test.go, mcp_platform_tools_test.go, mcp_application_authoring_test.go) laufen aktuell mit `environment: "dev"` (unmanaged), deshalb faellt der Gate-Text dort nicht — der Defekt ist latent: Jeder MCP-Test in managed environment, der den fixture-principal erwartet, ist durch diese Luecke ungeschuetzt.

## 4. Wo wirkt der Seam NICHT (Summarisch)

| Bereich | Naht wirkt? | Grund |
| --- | --- | --- |
| `runWithIO` (CLI `baha ...`) | JA | fixture stampft VOR gate-check, reihenfolge sauber |
| `command.Run(ctx)` DIREKT (CLI-Test) | Nur wenn ctx principal traegt | `runWithIO`/testOperatorContext NICHT aktiv; Test haengt an seinem eigenen ctx |
| MCP-Mutation (`authorizeMCPOperation`) | NEIN (latent) | kein testOperatorContext, kein WithEnforcement vor PrincipalFromContext — fixture-undefinierbarer Pfad |
| `WithEnforcement`-Nachsetzen im TEST | Nicht getroffen | runWithIO hat genau EIN WithEnforcement VOR fixture-call |

## fund ohne karte
Keine Karte gefunden, die diese Reachbarkeits-Luecke am operator-seam abdeckt. Besonders offen: Klasse C — MCP-Mutationen in managed environment laufen ueber einen Pfad, der den package-globalen operator-fixture (runWithIO-Naht) Uebersehen. Eine Karte muesste (a) die MCP-Route ueber eine Naht (z.B. `testOperatorContext`-aequivalent am MCP-Einstieg `newMCPServer`/Werkzeug-Handler) oeffern oder (b) MCP-Mutationstests in managed environment gegen den gate-text leiten. Dies ist der wichtigste fund dieser desk.
Keine produkt-aenderung durch diese lane.

## cleanliness
vorher: `docker ps -a` — ein container bh-docker-dev-edit-runtime-integration-dev-api-1 (alpine:3.22, Exited, ~1h alt) aus einer VORHERIGEN session, NICHT von dieser lane.
nachher: identisch — kein container von dieser lane gestartet.
`docker ps -a` grep bh-docker-dev:
```
de40a6c61cef   alpine:3.22   "sleep 300"   2 hours ago   Exited (0) About an hour ago             bh-docker-dev-edit-runtime-integration-dev-api-1
```
kein go-test auf diesem host ausgefuehrt; keine *.test-artefakte im worktree; kein commit/push in baseharbor.

## todo (4.4)
0428-211-huntseam: worktree gesetzt; helper-sammelbefund; reachbarkeits-falle analysiert; nachmessungen a/b/c; seam-missbefund (MCP Klasse C) dokumentiert; evidence geschrieben.
