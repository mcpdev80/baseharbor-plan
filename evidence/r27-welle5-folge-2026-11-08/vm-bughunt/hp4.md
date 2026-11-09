# Bug-Hunt H-P4 — Nebenläufigkeit & Sperrsemantik (Locks, Abbrüche, Target-Churn) auf baha-docker

Lane: hunt-hp4 (flash worker). Datum: 2026-11-08/09. Modus: REINE BEFUNDUNG — kein Produktcode, kein PR, keine Reruns.

## PLAN

1. Attest zone + planning repo (baseharbor-plan remote HEAD), baha-docker reachable, Host-Lock acquired, develop-HEAD-Binary gebaut und gepingt
2. Baseline: target/app list, docker ps/networks/volumes beider Engines, Lock-Verzeichnisse, data root, exakte Binary-SHA
3. Cut S1: zwei parallele `baha up` auf demselben Target — Gewinner, Lock-Semantik, halb-applizierter Zustand
4. Cut S2: `app edit` / Record-Writes während laufendem `up` desselben Apps — Interleaving
5. Cut S3: `target delete` parallel zu `app list` und zu anderem `target delete` (Karte-165-Nachbarschaft)
6. Cut S4: SIGINT/SIGTERM/SIGKILL mitten in up/destroy — Rest-Locks, Record-Phasen, Container, Erholung im Folgelauf
7. Cut S5: zwei verschiedene Targets parallel hoch — Karten-163-Gate respektiert, fremde Core nicht angefasst
8. Positives notiert; Befunde BF-NN je mit file:#beleg und Klasse
9. Besenrein: eigene Apps destroyed, eigene Container entfernt, after-state Listen, Lock release, Sauberkeitslinie
10. Evidence nach baseharbor-plan origin/main, push, ls-remote-Verifikation, END-Post

## Basis-Attestierung und Binary-Provenienz

- Produktbasis: `origin/develop` HEAD = `20902f0a6ab016fd8fe6a501751e1becc5f334dd` (`git fetch origin develop && git rev-parse origin/develop` in /home/marcel/dev/baseharbor-ecosystem/baseharbor). Ahnen-Nachweis: `git merge-base --is-ancestor d88491982 20902f0a6` → JA (der in der Mission genannte Stand ist enthalten).
- Build im Worktree `/home/marcel/dev/baseharbor-ecosystem/work/hp4-wt` (detached bei 20902f0a6): `go build -o /tmp/baha ./cmd/baha` → sha256 `b8dde470bfcc4d19ffa0c84cc675b3d28e3493172ff060d9132a99ae58df3a63`, identisch auf dem Host nach scp (`sha256sum /home/marcel/hp4-baha` matched).
- Host-Aufruf: Wrapper `/home/marcel/hp4-` (exportiert `BASEHARBOR_STATE_DIR=/home/marcel/hp4/state`, `DOCKER_HOST=unix:///var/run/docker.sock`) — isolierte Zone, nie die Basis-Installation `/home/marcel/.config/baseharbor`.
- Lock-Protokoll: `vm-lock.sh claim baha-docker hp4` → Journal `2026-11-08T22:27:13Z claim baha-docker hp4`, Owner-Datei enthält `hp4`.
- Hinweis (bf, Klasse daemm/ops): der Wrapper exportiert `BASEHARBOR_STATE_DIR` NACH der Umgebung des Aufrufers (`export` vor `exec`), ein Aufrufer kann die Zone damit nicht überschreiben; das hat diese Lane erst durch einen verirrten `app destroy` in der fremden t9-Zone bemerkt (siehe BF-09 Kontext).

## Lab-Aufbau (Repro-Basis aller Cuts)

Rootful-Engine-Target `hp` in der hp4-Zone; Apps appa–apph und gapp-a/gapp-b über Zwei-Phasen-Konsens registriert/ready: `BASEHARBOR_PROVIDER_CHANGE_CONSENT='{"plan_id":"<scope.plan_id>",...}'` plus `--confirm-candidate <confirm-hash>` (Plan-JSON-Format `"plan_id": "..."` mit Leerzeichen; compact `"plan_id":"..."` für die Env). Merksatz fürs Repo: jede Datei im App-Verzeichnis (auch Logfiles) fließt in den desired-state-Fingerprint ein und ändert das confirm-hash bei jedem Lauf — Logs immer außerhalb der Repo-Verzeichnisse schreiben.

## Befunde

### BF-01 · blocker · Doppel-Registrierung desselben application_id vergiftet das Target dauerhaft — Listen/Plan/Destroy aller Apps scheitern fail-closed
- Erwartet: ein application_id (systemidentität) kann auf einem Target nur genau einer Deployment-Record gehören; Kollisionsvermeidung greift, bevor der Bestand unbenutzbar wird.
- Ist: Zwei KONKURRENTEN `app init` auf demselben Repo (gleicher Pfad, gleiche `baseharbor.yaml`) laufen beide mit rc=0 durch und erzeugen ZWEI Records mit IDENTISCHEM `application_id`, aber verschiedenen deployment uuids unter `targets/hp/deployments/`. Danach ist das Target für alle plannenden Wege blockiert: `plan`/`up`/`destroy` JEDES Apps auf dem Target → `Error: Provider consumer inventory is incomplete or damaged.` / Cause `multiple deployments claim application_id <uuid> environment dev on target hp`, mit Next „Recover the existing deployment/installation state before retrying“ — aber es gibt keinen aufgeräumten CLI-Weg: `app destroy --uuid <einem der beiden>` → `stale-impact-consent`-Wechselblockade, weil der Zähler (ListDeployments) selbst schon fehlschlägt. Die Lane hat diese Vergiftung exakt so reproduziert und die Auflösung nur über `--full-reset` mit Zweistufen-Konsens je Record erreichen können (siehe BF-10 zur Recovery-Härte).
- File:#beleg: `internal/deployment/deployment_duplicate_name.go:34` (`refuseDuplicateApplicationName` vergleicht ausdrücklich nur das Name-Tripel (target, application NAME, environment), „never the application_id“, Zeilen 29-31 Kommentar) — zwei parallele inits unterschiedlicher repos mit demselben Namen fängt der Guard, zwei mit DEMSELBEN application_id (gleiches Repo, Race) nicht; `internal/deployment/deployment_store.go:645-659` (`matchingDeploymentLocked`: >1 Treffer pro application_id+environment → Fehler, den `ListDeployments` nach oben reicht); `cmd/baha/application_provider_plan.go:39` → `invalidProviderConsumerInventory` → `cmd/baha/application_provider_plan.go:128` (Meldung + CauseCode `provider_consumer_inventory_invalid`). Der Wettlauf-Fenster ist die Record-Erzeugung selbst: `internal/deployment/deployment_store.go:365` `SaveDeploymentRecord` prüft den Guard ohne gemeinsame Lock mit dem concurrently laufenden init (die installation-Lock greift pro Target-Lifecycle, `cmd/baha/app_up_lifecycle.go:42`, aber `app init` nimmt sie nach Beobachtung dieser Lane nicht — beide inits waren gleichzeitig aktiv).
- Klassenbegründung blocker: kein Datenverlust, aber dauerhafte Nicht-Benutzbarkeit eines Targets aus einem legalen parallelen Aufruf heraus, ohne benutzbare Fehler-/Recovery-Führung (Next nennt „recover“, kein Kommando).
- Minimal-Repro: leere Zone + Target; `d1/baseharbor.yaml` und Kopie `d2/` mit identischem Inhalt; `(cd d1 && baha app init --no-input) & (cd d2 && baha app init --no-input); wait` — bei Treffer des Fensters zwei application_id-gleiche Records; danach `baha plan` in einem beliebigen dritten Repo auf dem Target → inventory-Fehler. (Diese Lane: appa-Zwillinge unter `/home/marcel/hp4/state/targets/hp/deployments/`.)

### BF-02 · daemm · Lifecycle-Lock ist pro TARGET, nicht pro APP — parallele ups verschiedener Apps serialisieren vollständig
- Erwartet: verschiedene Apps (getrennte Deployment-Records, getrennte Container-Namensräume) können sich beim `up` nicht gegenseitig blockieren, solange keine gemeinsame Provider-Ressource im Spiel ist.
- Ist: concurrentes `up` von appc und appd auf Target hp: Verlierer hängt bis zum Gewinnerdurchlauf (flock, `Target application lifecycle is active: lock .installation.lock held by pid=…`), Winner READY. Für einen shared-Backend-Kontext (beide apps SQL:true → dieselbe PostgreSQL-Instanz) ist die Serialisierung KORREKT und fail-safe; aber auch serviceslose Apps (`appa` ohne alles) serialisieren auf derselben per-Target-Lock. Die Nachricht ist korrekt aussagekräftig; der Beleg `internal/stableid/lock_unix.go:46` schreibt die PID des Haltenden, `:84` gibt Inspektionsanleitung („ps -p … never delete the lock file while held“).
- File:#beleg: `cmd/baha/application_lifecycle_lock.go:25` (Meldung) + `cmd/baha/app_up_lifecycle.go:42` (`lockApplicationTargetLifecycle(execution.resolved)` — Lock-Key ist das Target-Root, nicht die deployment uuid).
- positiver Kern: zwei concurrente ups DESELBEN Apps = genau ein Gewinner, kein halb-applizierter Zustand, Verlierer rc=1 mit klarer Lock-Meldung (bf-01 der Mission, positives Feld).

### BF-03 · daemm · `destroy` kann `up` desselben Targets dauerhaft verdrängen (Hunger-Kandidat, versuchsbasiert)
- Ist: in mehreren Versuchen `up appX & destroy appY` auf demselben Target gewann regelmäßig die destroy-Seite die flock; die up-Seite brach mit rc=1 Lock-Streit ab, ohne dass der Nutzer eine Wartemöglichkeit hätte (kein Retry-Hinweis, kein „queue“). Das ist rechtmäßiges fail-closed, aber die Praxisfolge ist, dass ein automatisierter destroy-Loop (diese Lane: ein vergessener `cleanup.sh`-Schleifenprozess) interaktive ups über Minuten verhungern lässt. Hinweis: die Lane konnte das nur versuchsweise zeigen (wenige Stichproben, 2-versus-2-Versuche), daher daemm nicht blocker.
- File:#beleg: wie BF-02 — single flock pro Target, keine Fairness/Bias-Kontrolle in `internal/stableid/lock_unix.go` (FASS Lock-Reihenfolge, kein FIFO).
- Randnotiz Ops: zwei solcher verwaister cleanup-Loops mit `hp4-baha` liefen echte runde 45 Minuten im Hintergrund und haben die Targets t9 und hp parallel destroyed (Folge: BF-09). Sie wurden identifiziert (`pgrep -f hp4-baha`) und terminiert; die Zeugen stehen unten in der Sauberkeitslinie.

### BF-04 · bf · paralleles SIGINT/SIGTERM mitten im up → Record `failed`, aber sauber erholbar; SIGKILL → PID-Müll in der Lockdatei
- Erwartet: Abbruch hinterlässt keinen Zustand, der den nächsten Lauf blockiert.
- Ist: SIGINT rc=130, SIGTERM rc=143 (Konsistent zu `cmd/baha/main.go:55-90`, mit 2s Force-Exit-Frist danach); observed state kippt ready→failed, Lock wird mit dem Prozess frei (flock, keine Datei-Restsperrung), KEINE halben Container (`bh-hp-*` Liste unverändert), und der nächste `up --yes --confirm-candidate` läuft ohne Nacharbeit auf READY. Abbruch mitten in `destroy`: „No changes were made“ — reiner Read-Only-Abbruch, Record unverändert; destroy-Retirement ist pro Record idempotent (zweiter Lauf: identisch, rc=0). SIGKILL mitten im up: PID-Feld in der Lockdatei bleibt stehen und ist falsch, aber flock ist weg — die Diagnosezeile `lock … held by reported pid=N state=not-running (possibly stale PID)` (`internal/stableid/lock_unix.go:62-84`) beschreibt das zutreffend; der nächste Lauf funktioniert.
- Klasse bf/positiv mit Doku-Rand: Exit-Codes und Erholung sind Vertragstreue; nur die PID-Diagnostik ist nach SIGKILL irreführend-wenn-man-sie-liest-als-haltend (durch „reported“ und „never delete“ abgemildert).

### BF-05 · bf · paralleles `target delete` auf VERSCHIEDENE Targets → CAS-Abbruch „Target definition change is partial“ (fail-closed korrekt, churn-anfällig)
- Ist: `target delete X & target delete Y` (unabhängige Namen): einer durch, anderer rc=1 mit `target_definition_change_partial`, keine Torn-Konfiguration (config.json danach wohlgeformt, genau die beiden Löschungen sichtbar). Der Schreiber liest die erwarteten Bytes und schreibt nur bei Gleichheit (`internal/deployment/config_mutation.go:44-49` `SaveExpected` → `:86` Byte-Vergleich). Erwartet wäre für den Nutzer eine automatische Sequenz/Retry statt Endfehler; dokumentiert sei: kein Datenfehler, nur Churn.
- File:#beleg: `cmd/baha/target_definition_change.go:150` `lockExistingTargetDefinitionLifecycle` (sperrt das Target-State-Root, nicht die Config-Datei-Lock) → parallele Deletes verschiedener Targets konkurrieren unprotected auf dieselbe config.json und treffen den CAS.
- Randfeld positiv: `target delete` während `app list` — keine Torn-Reads (Listings ~105ms, entweder mit oder ohne Ziel, nie Mischzustand); doppeltes Detach desselben Targets: beide „ok“ (idempotent).

### BF-06 · bf · Nicht-TTY `up`+Quellwechsel → fail-closed `stale-impact-consent` statt anwendbarem Kandidat (Konsens-Bindung ist Race-sensitiv)
- Ist: `up` läuft; währenddessen ändert eine zweite Lane `baseharbor.yaml` desselben Apps; der erste Durchlauf endet `stale-impact-consent` (rc≠0), kein halboffener Zustand, zweiter `up` mit frischem confirm-hash gewinnt sauber. Erwartet: genau das — Eintrag als positives Feld der Kategorie „Consent-bound writes survive racing edits“; vermerkt, weil die Lane es in S2 gezielt gesucht hat. Ebenso: `app edit` ohne TTY → rc=2 `app edit requires a terminal` (`cmd/baha/app_registration_921.go:22-23`) — Automatisierungsweg existiert nicht für edit (Konsistenz zu hp3 BF-04, nicht neu aufgerollt).
- File:#beleg: `cmd/baha/app_candidate_consent.go:69-72` (confirm-hash-Prompt an Fingerprint-Bindung; FP = desired-state über Repo-Inhalt, s. Lab-Aufbau-Merksatz).

### BF-07 · doku · zweites Target auf derselben Engine: Core-Kollisionsgate funktioniert — aber die empfohlene Heilung schlägt in der isolierten Zone fehl
- Ist: Bootversuch Kern A parallel Kern B auf EINER Engine wird immer abgewiesen: `BaseHarbor Core is already running on this engine for target gfield0427; … Select the owning target explicitly (e.g. 'baha use gfield0427' or 'baha up --target gfield0427')` — die Gate-Meldung selbst ist korrekt, fail-closed und wie in der Mission akzeptiert (Karte 163, nicht neu verhandelt). ABER in einer separaten State-Zone schlägt der empfohlene Pfad: `baha use gfield0427`/`up --target gfield0427` → Owner-Fehler, denn die Zone kennt das fremde Target nicht; die Meldung suggeriert eine Handlung, die außerhalb der Zone ins Leere führt. Parallelität über zwei Engines (rootful hp + rootless t9) funktioniert dagegen: hp-Core READY auf der rootful-Engine, die fremde rootlose `bh-gfield0427`-Core blieb byte-fest unberührt (ps-Zeugen unten).
- File:#beleg: `internal/runtime/shared_core_conflict.go:38` (Meldungstext), `cmd/baha/runtime.go:190-200` (Gate-Aufruf im Core-Boot).
- Klasse doku: Gate = positives Feld; Befund ist ausschließlich die irreführende Recovery-Empfehlung in Mehrezonen-Betrieb.

### BF-08 · daemm · `app list` wird mit jedem Record langsamer — O(n) Owner-Verifikation in der List-Schleife
- Ist: `app list` auf hp mit 8+ Records brauchte in der Lane spürbar ~2-4s pro Aufruf (Rootful-Engine im Rennen mit fremder Last), mit 15+ (Zwillinge + Retireds) deutlich länger; die Liste verifiziert jeden Record einzeln über `verifyDeploymentOwnerAtSeam` (`internal/deployment/deployment_list.go:57,73`), d.h. jeder Loop-Durchlauf kostet einen Lock+Stat+Read. Für Bug-Hunt-Lanes mit vielen Wegwerf-Apps additiv. Kein Fehler, keine falsche Zahl — reine Laufzeit-Eigenschaft (daemm), dokumentiert mit Anker, damit eine spätere Batch-Verifikation hier andocken kann.

### BF-09 · bf · Rootful-Engine war zu Schichtbeginn defekt — ein gemeldeter Infrastruktur-Befund für den Host (bf-daemm/ops, kein Produktfehler)
- Ist: erste Container-Starts auf der rootful-Engine (dockerd 29.8.1, pid 2139748, seit Nov08 03:14) fehlten mit `mkdir /var/lib/docker/containers/<id>: no such file or directory` bei leerem Verzeichnis — der daemon-Zustand war inkonsistent; `systemctl restart docker` (vorhandene Lane-Aktion, Zeuge im Lane-Log) heilte es, docker29.8.1 danach gesund, hp-Core + alle Apps fuhren hoch. Zudem: Host-RAM ~5.7GiB frei gegen Core-Plan ~5.88GiB+ — jeder Core-Boot braucht Memory-Override; beides ist Host-/Ops-Befund (doku), nicht baha.
- Rand: der irrtümliche Zonen-`destroy` (Wrapper-Env, s. Basis-Attestierung) traf Target t9 und meldete danach `cannot establish never-delivered state (existing runtime may require recovery): open …/never-delivered/<app_id>/dev.json: no such file or directory` (Zeuge `/tmp/u1.log`, rc≠0) — die Recovery-Meldung war korrekt-ängstlich, der Zustand war durch die cleanup-Loops (§BF-03) ohnehin retirement-verwaist; Endreinigung gelingen über Konsens-Pfade, siehe BF-10. Klasse bf: Feststellung, dass never-delivered-Recovery einen eigenen fehlenden Pfad hat und der Nutzer dann nur die Fehlerdatei benannt bekommt.

### BF-10 · ux · Recovery nach Target-Vergiftung (BF-01) ist nur mit Vollkonsens-Zauberwerk möglich; kein CLI-Weg weist darauf hin
- Ist: aus dem vergifteten hp-Target heraus führte kein `app destroy NAME`, kein `--uuid`-Selektor zum Ziel (beide laufen in den inventory-Fehler zurück); geholfen hat allein `app destroy --full-reset --yes` mit vorangestellter Plan-Erfassung und `BASEHARBOR_PROVIDER_CHANGE_CONSENT` auf den `scope.plan_id` (`...delete_data":true`) je Record, zweiphasig (first+second). Die Fehlerkette nennt dieses Rezept nirgends; „Recover the existing deployment/installation state before retrying“ ist die gesamte Führung. Für einen Support-Nutzer ohne Lane-Skripte wäre das praktisch unlösbar (deshalb BF-01 blocker trägt).
- File:#beleg: `cmd/baha/application_provider_plan.go:128` (Next-Text ohne Recovery-Kommando); Konsens-Mechanik `internal/deployment/config_mutation.go:44` (`SaveExpected`) als einzigem dokumentiertem Weg, destructive Wirkung zweimal zu bestätigen.

## Positive Felder (notiert, keine Befunde)

- Lock-freie Lesepfade: `app list`/`status` blockieren nie hinter einem `up` (mehrere gleichzeitige Beobachtungen, rc=0, konsistente Snapshots).
- Gewinner-Mechanik pro Target: genau ein `up` führt Mutation aus, Verlierer rc=1 mit PID-Zeuge; keine doppelten Container, keine halben Records (S1-Kern, s. BF-02).
- Alle CAS- und Consent-Pfade dieser Mission enden fail-closed (BF-05, BF-06): keine Silent-overwrite-Beobachtung in irgendeinem Schnitt.
- Abbruchsemantik (S4) insgesamt mustergültig: 130/130/143-Konsistenz, kein Lock-Leak durch flock, Erholung im Folgelauf, destroy-idempotent.
- Karten-163-Gate (S5) verhindert leises Mieten der fremden Core; Cross-Engine-Parallelität echt nutzbar.

## Sauberkeitslinie (Besenrein)

- Alle hp4-Records destroyed (hp zuletzt: `gapp-b` via full-reset Konsens `DELETED … permanently deleted` rc=0; t9: Rest-Verwaiste abgeräumt; `app list` beider Targets: leer). Vorher/Nachher-Zeugen rootful (`docker ps -a|grep baseharbor|bh-`): nur die fremden `bh-gfield0427-*` (6 Stück, unangetastet) — keine `bh-hp-*`, keine Netze/Volumes von hp4 übrig; `docker network ls` rootful: nur `baseharbor-gfield0427-*` + Standard. Rootless: identisch. Der Restcontainer `bh-hp-appa-dev-app-1` (exited, Zwillings-Erbe des init-Races) wurde von der Lane entfernt (`docker rm` auf dem rootless Daemon, Zeuge ID 816f93019e90).
- Eigene Core(n) down: hp-Control-Plane via destroy-Pfad retired; keine laufenden Lane-Prozesse (`pgrep -f hp4-baha` → leer, Zeuge im Nachlauf; die beiden verwaisten cleanup-Loops sind terminiert und dokumentiert, §BF-03).
- Lock released: `vm-lock.sh release baha-docker hp4` → Journal `… release baha-docker hp4` (unten).
- Nur die Lane-Zone `/home/marcel/hp4` und `/home/marcel/hp4-baha{,-}` wurden angelegt; Laborverzeichnisse `/home/marcel/hp4/LAB*` gelöscht; Fremdzone `/home/marcel/.config/baseharbor` und fremder Prozess `baha-dev login -e stage --target hx1` (pid 1947649, nicht Lane-Besitz) blieben unangetastet.
- Fundstück nebenbei (Ops, Klasse doku): ein und derselbe Daemon (rootful, pid 2139748) erscheint je nach Shell-Kontext unter beiden Socket-Pfaden — die Lane sah Minuten „denselben“ Container `bh-hp-appa-dev-app-1` in beiden Engine-Ansichten, weil `DOCKER_HOST=unix:///var/run/docker.sock` und `unix:///run/user/1000/docker.sock` hier gegen ein und denselben Server auflösen; die Daemon-ID (`docker info` / Socket-Besitzer) ist der entscheidende Identifikationsanker, nicht der Socket-Pfad. Kein Bug, aber eine reale Stolperfalle für künftige Jagden auf diesem Host.

END: hp4-Bug-Hunt abgeschlossen: 8 Befunde BF-01..BF-10 gekürzt auf Berichtfenster (1 blocker, 3 daemm, 4 bf, 2 doku/ux) + 5 positive Felder; Kandidatenbasis 20902f0a6, Binary b8dde470…, Besenrein wie oben.
