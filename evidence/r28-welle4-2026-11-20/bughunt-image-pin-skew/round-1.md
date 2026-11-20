# Bug-Hunt H-V15 — Core provider image pin skew

**Hunt:** H-V15 (reine Befundung, kein Commit, kein PR, kein Merge)
**Pruefschnitt:** Welche Bild-Referenzen schreibt BaseHarbor, und was passiert bei Versionsschiebung (neuer Core / altes Pin; altes Pin / geaenderter Registry-Pfad)?
**Anchor (develop) SHA:** `36d075fad77fa61ac8c153e979855546589b32c2`
**Evidence witness — `git ls-remote origin refs/heads/develop` (Produkt-Repo, /var/tmp-clone):**

```
36d075fad77fa61ac8c153e979855546589b32c2\trefs/heads/develop
```

Gegen develop-head `36d075fad77fa61ac8c153e979855546589b32c2` gelesen, 2026-11-20. Clone: `/var/tmp/baha-hv15` (fresh `git clone https://github.com/mcpdev80/baseharbor.git`, `git fetch origin`).

## PLAN

1. Clone develop in /var/tmp, `git ls-remote origin refs/heads/develop` in die Akte.
2. Anker lesen: `internal/deployment/config_mutation.go`, `target.go`, `internal/runtime/project.go`, Workflow-Pin-Pruefung (nur lesen).
3. Image-Pin-Erzeugung tracen (Inventory -> Plan -> RewriteOwnedComposeImages -> apply).
4. Versionsschiebung gegen `coreupdate.Build`/`ClassifyHAPostgresPin`/`verifyImage` messen (ERWARTET vs. IST).
5. Destroy/Retry- und Schreibpfad ohne Pruefung pruefen.
6. Akte schreiben, Cleanliness-Check, END-Meldung.

## 1. Wo entsteht ein image-pin, und ist er deterministisch reproduzierbar?

**Erwartet (Vertrag):** Ein image-pin ist eine immutable OCI-Referenz `<repository>@<sha256:digest>`. Er muss auf identischer Eingabe identisch wiederholbar sein — deterministisch aus Release-Pin + inventarisierter Runtime-Identitaet.

**Gemessen (Ist):**

- Release-Pins sind das einzige Desire-Oberfeld und kommen aus dem in die Binary embedded Catalog `internal/coreupdate/releases/v0.4.24.json`. `LoadRelease` liest ihn via `//go:embed` (`internal/coreupdate/catalog.go:14-41`), validiert `release`-Mismatch und ruft `Build(normalized, nil, release.Providers)` (`catalog.go:57`). Kein mutabler OCI-Tag-Fallback: "A missing release must fail; no mutable OCI tag fallback is allowed" (`catalog.go:35`).
-pins in `v0.4.24.json`:
  - sql: `docker.io/library/postgres:18-alpine` @ `sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873` (version `18`)
  - secrets: `docker.io/openbao/openbao:2.7.1` @ `sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf` (version `2.7.1`)
  - identity: `quay.io/keycloak/keycloak:26.8.0` @ `sha256:b0f60d489d51c5d113390bdf5461d4c06e6051be026c05549f2e1e10ec352bcc` (version `26.8.0`)
  - backing (HA postgres): `ghcr.io/zalando/spilo-18:4.1-p2` @ `sha256:258a87d34699387f3b6b45d30874c21c6b838ed51c9371ae2a70151d57137990`
- Inventory (Installed-Seite): `ProjectServiceImageIdentity` liest `{{.Config.Image}}|{{.Image}}` aus `container inspect` (`internal/runtime/compose_resources.go:537-545`) und leitet Digest aus `RepoDigests` ueber `verifiedImageRepositoryDigest` ab (`internal/runtime/image_identity.go:40-63`). Nur `docker.io/`-Normalisierung, keine Tag-Aufloesung hier.
- `ownedTaggedImage` (`cmd/baha/update_image_reference.go:16-55`) recovering die taggte Referenz **nur** aus der owned, protected Compose-Declaration: es verlangt `ref == base+"@"+digest` und `parts[1] == digest` (`update_image_reference.go:51`). Weicht die Runtime-Referenz vom owned Pin ab, faellt die Funktion mit `canonical runtime image differs from owned provider pin` zu (`update_image_reference.go:52`).
- `Build` (`internal/coreupdate/plan.go:121-175`) setzt Desired aus `catalog.Providers`; `validDigest` prueft `sha256:` + 71 Zeichen (`plan.go:62-68`).
- Apply: `RewriteOwnedComposeImages` schreibt exakt `img.Value = delta.Desired.Image + "@" + delta.Desired.Digest` (`internal/coreupdate/compose_images.go:70`). `ClassifyHAPostgresPin` (`internal/coreupdate/ha_postgres_pin.go:10-43`) und `RewriteOwnedSpiloImages` (`internal/coreupdate/ha_spilo_compose.go:64-145`) schreiben analog fuer die drei Spilo-Mitglieder.

**Befund: VERHALTEN KORREKT.** Der Pin ist deterministisch reproduzierbar: Desire kommt aus einem embedded, versionierten, unveraenderbaren JSON mit fester Digest-Struktur; die Apply-Seite schreibt `<image>@<digest>` exakt aus dem Delta. Der Digest ist kein Tag, sondern der immutable OCI-Index. Identische Eingabe -> identisches Ergebnis.

## 2. Versionsschiebung: fail-closed, uebernahme oder gemischter run?

**Erwartet (Vertrag):** divergence zwischendevelop-Pin und Bestands-Car-Pin muss fail-closed sein — ein "stille Übernahme" oder gemischter Run (ein Mitglied neu, altes Pin verbleibt) ist nicht moeglich.

**Gemessen (Ist) — messen an `Build` (`plan.go:142-173`):**

- **A — Major-Schiebung (Car=postgres:17, develop=postgres:18):** `current.Image != target.Image` -> `NoChange` faellt weg; `providerDowngrade("17","18")` = false; aber `current.Kind == SQL && split("17")[0] != split("18")[0]` -> **Unsupported** ("PostgreSQL major upgrade requires an explicit supported migration") (`plan.go:163`). `reconcileNativeCoreProviders` dreht `Unsupported` in `unsupported provider ... upgrade` zurueck und bricht ab (`cmd/baha/update_core_native.go:488-491`). -> **fail-closed.**
- **B — gleicher Major, anderer digest (Car=postgres:18-alpine @digestA, develop @digestB):** `Image` identisch, `Version` identisch (`18`), aber `Digest` ungleich -> `NoChange` faellt weg; kein Downgrade, gleicher Major; Fall `current.Kind == SQL` -> **BackupRequired**. Apply verlangt `RecoveryPoint` (physisches Postgres-Backup) (`plan.go:268-272`) und `RewriteOwnedComposeImages` prueft in der Compose die inventarierte Referenz (`compose_images.go:66-68`) -> faellt closed ab, wenn abweichend. -> **Backup-verpflichtet, sonst fail-closed.**
- **C — Registry-Pfad-Schiebung (Car=`docker.io/library/postgres:18-alpine`, develop=`ghcr.io/.../postgres:18`):** `current.Image != target.Image` -> kein `NoChange`; `ownedTaggedImage` verlangt `canonicalImageRepository(base) == canonicalImageRepository(parts[0][:tag])` und `ref == base+"@"+digest` (`update_image_reference.go:51`) -> **mismatch, fail-closed.** Die Inventory-Seite erkennt einen abweichenden Registry-Pfad und wirft `canonical runtime image differs from owned provider pin`.
- **D — HA Spilo Major/Transition (Car=spilo 18-4.1-p1, develop=18-4.1-p2):** `safeSpiloTransition` (`ha_spilo_compose.go:35-60`) erlaubt nur Patch-Erhoehung gleicher Major (`next[2] >= old[2]`); sonst `checkpointPath` -> `UNSUPPORTED: unknown, major-changing or downgraded Spilo transition` (`ha_spilo_compose.go:30`). `ClassifyHAPostgresPin` setzt fuer eine safe Transition nur `BackupRequired` und nur bei `postgres-member-1`/Scope shared (`ha_postgres_pin.go:30-41`); der Roll erfordert zwingend `VerifyRecovery` + DCS-Evidence (`patroni_cluster_roll.go:249-264`). -> **fail-closed / recovery-verpflichtet.**

**Befund: VERHALTEN KORREKT.** Jede messbare Divergenz (Major, Digest, Registry-Pfad, Spilo-Patch) endete in Unsupported, BackupRequired-mit-Recovery oder einem Rewrite-Ablehnung. Kein Pfad ueberspringt die Pruefung; die Compose-Referenz wird beim Apply gegen die inventarierte Identitaet gegengecheckt. Ein gemischter Run ist nicht abbildbar.

## 3. Verliert ein Destroy/Retry-Zyklus das Pin, und woher kommt es dann neu?

**Erwartet (Vertrag):** ein Pin ist durable; ein Retry/Restore darf es nicht verlieren und aus einer unsicheren Quelle neu setzen.

**Gemessen (Ist):**
- `ComposeCheckpoint` (Core SQL/Secrets/Identity): `Capture`/`Stage`/`Restore` schreiben den Originalzustand in einen sha256-`checkpointName` (`internal/coreupdate/compose_transaction.go:23-40`) und vergleichen beim Restore `current` mit `original`/`pinned` -> `cannot restore Compose modified by another owner` (`compose_transaction.go:204`). Die Divergenz pruefung macht einen Restore dicht, wenn ein anderer Owner dazwischen geschrieben hat.
- `HAPostgresComposeCheckpoint` (`ha_spilo_compose.go:149-193`): Stage schreibt original in einen `Previous.Image@Digest+Desired.Image@Digest`-Checkpoint; bei Divergenz `Spilo Compose drift; refusing replay`.
- Pin-Nachschprung kommt ausschliesslich aus `coreupdate.LoadRelease` (embedded Catalog) oder aus der owned Compose-Declaration (`ownedTaggedImage`); niemals aus einem laufenden, nicht-owned Image oder einer Remote-Tag-Aufloesung.
- `baha update` holt zwar die Release-Metadaten von GitHub (`performSelfUpdate` -> `resolveSelfUpdateRelease`, `fetchReleaseJSON`), aber der **pinned Desired-Digest** kommt aus dem embedded Catalog der heruntergeladenen, checksumme-verifizierten Binary (`reconcileNativeCoreProviders` -> `inspectSelectedCoreRuntimePlan` -> `coreupdate.LoadRelease(release)`). Die Release-Pins auf `main` und `develop` sind identisch (`git diff origin/main develop -- internal/coreupdate/releases/` = leer).

**Befund: VERHALTEN KORREKT.** Das Pin ist durables Checkpoint-Material; ein Retry/Restore darf es nicht verlieren und hoest es nicht aus einer unsicheren Quelle nach. Destroy/Retry bleibt innerhalb der owned Pin-Struktur.

## 4. Gibt es einen Pfad, der ein Pin ohne Pruefung ueberschreibt?

**Erwartet (Vertrag):** jedes Umschreiben einer owned `image:`-Zeile muss an die fail-closed Rewrite-Pruefung (`RewriteOwnedComposeImages`/`RewriteOwnedSpiloImages`) gekoppelt sein; kein freies Schreiben.

**Gemessen (Ist):**
- Alle Apply-Pfade laufen ueber `RewriteOwnedComposeImages` (`compose_images.go:14`) bzw. `RewriteOwnedSpiloImages` (`ha_spilo_compose.go:64`): beide verwerfen (`return nil, fmt.Errorf(...)`) bei abweichender Inventar-Referenz, ungueltigem Digest, Downgrade oder nicht-owned Owner. Es gibt keinen alternaten Writer, der eine owned `image:`-Zeile direkt setzt.
- `ownedTaggedImage` schreibtauch nicht — es ist rein lesend und recoveryend; es wirft beiMismatch.
- Die einzige Schreibstelle des Pin-Werts ist `compose_images.go:70` (`img.Value = delta.Desired.Image + "@" + delta.Desired.Digest`) — und sie ist an die Pruefung vor Zeile 47-54 gekoppelt.
- `.github/**` ist owner-scope; die Workflow-Pin-Pruefung (z. B. `docker-runtime-acceptance.yml:149-167` `TestRepositoryComposePinnedWorkloadLifecycleInCI`, `ci-core-rootless-runtime.sh`) ist nur gelesen, nicht geaendert.

**Befund: VERHALTEN KORREKT.** Kein Pfad ueberschreibt ein owned Pin ohne die fail-closed Rewrite-Pruefung.

## repo-rule compliance

- Reine Befundung, KEINE Produktänderung. Keine Produkt-datei geschrieben, kein Commit, kein PR, kein Merge.
- Plan-Write nur in `/var/tmp`-Kontext; Akte ins evidence-Verzeichnis geschrieben. KEIN Write in `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.
- KEINE `.github`-Aenderung (owner-scope); Workflow-Pin-Pruefung nur gelesen.
- KEINE subagenten/exec-code-delegation. Alle Messungen direkt im /var/tmp-Clone mit read/grep/shell.
- Produkt-Remote nur via `git ls-remote origin refs/heads/develop` im frischen /var/tmp-Clone (`/var/tmp/baha-hv15`) gelesen. Der quarantinierte checkout `workers/baseharbor` wurde nicht zitiert.

## cleanliness

- container: (keiner gestartet — VM/container-Tests nicht erforderlich, reine Quell-Befundung)
- networks: (keine)
- volumes: (keine)
- state dirs: (keine geschrieben)
- ambient-core / bilder fremder karren: unangetastet
- clone: `/var/tmp/baha-hv15` (git clone, unveraendert, nur gelesen)
- cleanliness: CLEAN — keine container/networks/volumes/state-zwecke angelegt, nichts fremder karren beruehrt.

## Evidence-Sha (plan-clone)

`git log -1 --format=%H` im planning-clone ist erst nach dem Schreiben der Akte relevant; die Akte liegt als Datei vor (kein commit im plan-repo).
