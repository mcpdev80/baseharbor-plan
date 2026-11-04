# Classification 1 — t-20261104-r27 consent-abort (w138b, worker)

- Lane: w138-fortsetzung (worker) · Coord: f49a3303 · Repo: baseharbor
- Messkopf w120-fix: 59134bc8a3239622f1cc498a74e9dde72f6e2e83 (develop e444ae117173dcf84e7aa8b17f73c020d3e2923c IS Vorfahr)
- Binaries: kandidat 59134bc8 -> /home/marcel/w138b-binmerged; develop e444ae11 -> /home/marcel/w138b-bindevelop
- Kein produkt-aenderung; keine workflow-aenderung; keine subagenten; kein rerun als ersatz fuer analyse
- Evidence-Regel: nur messen, nicht entscheiden. A/B-Leseregel des Owners: A=Erfolg und B=Fehlgeschlagen => Produkt korrekt, Karte ist Stapel-/Betriebs-Eigenheit. A=Fehlgeschlagen => echte Luecke im Zerstoerungs-pfad.

## ZELLEN-TABELLE

Jede Zelle: Befehl (isoliertes XDG, eigener rootless-docker-pfad, eigener git-repo-stapel), rc, eine wortliche zeile.

### ZELLE A — develop e444ae11 ALLEIN + isolierte rootless-umgebung

- Befehl: `baha app init --sql demo-db --workload-component demo-app --no-input` (git-tracked repo, baseharbor.yaml mit sql+https-exposure, compose.yaml), dann `baha app apply --no-input` (OHNE --confirm-candidate), dann `baha app destroy --yes`
- Umgebung: XDG_CONFIG_HOME=/home/marcel/w138b/cell-A-develop/config, XDG_DATA_HOME=/home/marcel/w138b/cell-A-develop/state, docker context=rootless, eigener git-pfad
- rc apply (ohne Kennung): 1 — wortliche fehlzeile: `provider change: impact-confirmation-required`
- rc destroy (real, nach abgelehnter auslieferung): 1 — wortliche fehlzeile: `Error: incomplete deployment state for local// [4cb71ac3-bc21-4104-9391-656b44291e59]: deployment.json is missing: file does not exist`

### ZELLE B — develop e444ae11 + EIGENER stapel mit geteiltem netz

- Status: NICHT-AUSFUEHRBAR (nicht erfunden)
- Grund: Der geteilte sql-backend (`runtime/bh-local-shared/shared-backends/postgresql`) braucht den postgresql-runtime-adapter. In dieser isolierten umgebung ist er NICHT registriert: `baha stack create shared-backends --component runtime:sql:postgresql --scope repository` => `Error: development stack postgresql is not available`. Der hostweite stapel `bh-local-shared` (compose project com.docker.compose.project=bh-local-shared, netz baseharbor-local-default) ist ein gemeinsam-zustand auf baha-runner-docker-2; ihn anzustossen waere eine aenderung am geteilten zustand => laut mission STOP + MELDEN. Kein podman-rechner auf diesem host (nur docker).
- Ersatzmessung: der eigene stapel (repository-scope, app-role only) konnte angelegt werden, liefert aber KEINEN sql-geteilten-backend => keine messbare zerstroerung ueber den geteilten netz-pfad.

### ZELLE C — kandidat 59134bc8a323 + isoliert (bereits in w138 r3 vorbereitet, hier erneut auf neuem kopf)

- Befehl: identisch zu A (`baha app init --sql demo-db --workload-component demo-app --no-input`, `baha app apply --no-input` OHNE --confirm-candidate, `baha app destroy --yes`)
- Umgebung: XDG_CONFIG_HOME=/home/marcel/w138b/cell-C-candidate/config, XDG_DATA_HOME=/home/marcel/w138b/cell-C-candidate/state, docker context=rootless, eigener git-pfad
- rc apply (ohne Kennung): 1 — wortliche fehlzeile: `provider change: impact-confirmation-required`
- rc destroy (real, nach abgelehnter auslieferung): 1 — wortliche fehlzeile: `Error: incomplete deployment state for local// [bf5dc762-b275-4192-8ba6-21f658d6cd9a]: deployment.json is missing: file does not exist`

### ZELLE D — kandidat 59134bc8a323 + geteiltes netz

- Status: NICHT-AUSFUEHRBAR (nicht erfunden)
- Grund: identisch zu B — der sql-geteilte-backend ist hier nicht messbar; der hostweite shared-stack wird nicht angestossen (gemeinsamer zustand). Eigener app-role-stapel ohne sql-geteilten-backend => keine messbare zerstroerung ueber den geteilten netz-pfad.

## ZELLEN-ERGEBNIS (nur messung, keine entscheidung)

- A apply rc=1 (provider change: impact-confirmation-required); A destroy rc=1 (deployment.json missing)
- C apply rc=1 (provider change: impact-confirmation-required); C destroy rc=1 (deployment.json missing)
- A und C sind WORTLICH identisch am messbaren punkt (apply-abweisung + zerstroerung ohne vorherige auslieferung)
- B und D: NICHT-AUSFUEHRBAR (sql-geteilten-backend hier nicht verfuegbar; hostweiter shared-stack nicht anstossen)

## EIGENTUMS-QUELLE (read-only, datei:zeile)

Die karte geht inhaltlich darum, wer den eigentum am shared-backend haelt. Messung der lese- statt schreib-seite:

- destroy/apply prueft den shared-sql-owner aus dem STAPEL-ZUSTAND, nicht aus dem anwendungs-deployment:
  - cmd/baha/app_destroy_authorization.go:91 — `application.ProviderScopeOwner{Owner: "application-deployment", Subject: record.Identity.DeploymentID, Reference: filepath.Join(root, "deployment.json")}` — canonical deployment owner aus deployment.json des eigenen deployments
  - internal/application/shared_core_sql.go:13 — `verifyCoreSharedPostgreSQL` ruft `verifySharedPostgresStateOwnership(state, key)` auf; `key := sharedBackendApplicationKey(m)` abgeleitet aus manifest name/environment
  - internal/application/shared_backends_state.go:15 — `loadSharedBackendState(path, environment)` liest den shared-backend zustand (state.Applications[key]) — das ist die eigentumsquelle fuer den geteilten backend
  - internal/application/shared_backends_resources_runtime.go:32 — `SharedPostgresResourcesAt`: `Owner: app.Application + "/" + app.Environment`, `ProviderScope: ScopeShared` — der owner des shared sql ist der stapel-konsumer, nicht das eigene deployment
- Satz was dort stehen wuerde: Der zerstoerer liest den eigentum am shared backend aus dem shared-backend-state (`state.Applications[sharedBackendApplicationKey(m)]`), also aus der stapel-definition/-registrierung, und verifiziert gegen `verifySharedPostgresStateOwnership`. Er liest ihn NICHT aus dem anwendungs-zustand (deployment.json) allein — das deployment.json ist nur der canonical owner fuer das eigene deployment (app_destroy_authorization.go:91).

## GRENZEN-ABGLEICH

- Kein produktcode-aenderung (nur evidence/classification-1.md geschrieben)
- Keine .github-/workflow-aenderung, kein rerun/workflow_dispatch
- Keine subagenten, kein zweiter branch, kein merge, kein force-push
- Kein scratch in der oekosystem-wurzel (alle bins/state unter /home/marcel/w138b; worktrees unter /tmp)
- Geteilte stapel des rechners nicht zerstoert oder umbaut (B/D nur gemeldet)

## END

END_DONE w138-consent-classify: A=rc1(provider change: impact-confirmation-required; destroy rc1 deployment.json missing) B=NICHT-AUSFUEHRBAR(sql-geteilten-backend hier nicht verfuegbar, hostweiter shared-stack nicht anstossen) C=rc1(provider change: impact-confirmation-required; destroy rc1 deployment.json missing) D=NICHT-AUSFUEHRBAR(sql-geteilten-backend hier nicht verfuegbar) eigentumsquelle=internal/application/shared_backends_state.go:15 loadSharedBackendState + shared_core_sql.go:13 verifySharedPostgresStateOwnership (owner aus stapel-state, nicht aus deployment.json allein) lsremote=59134bc8a323 | A und C wortlich identisch am messbaren punkt (apply-abweisung + destroy-vor-auslieferung); B/D nicht messbar in isolierter umgebung, kein produkt-befund, keine entscheidung abgeliefert
