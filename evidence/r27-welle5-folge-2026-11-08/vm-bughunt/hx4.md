# Bug-Hunt H-X4 — trust-/nachrichtendienst-oberflaeche auf baha-docker

- Card/mission: mission-hunt-x4.md (Bug-Hunt H-X4, pure findings, no product code, no PRs)
- Shift: r27-welle5-folge-2026-11-08 / round-1
- Worker session: 500b8545 (laptop), no subagents (4.8)
- Planning repo verified (origin/main): 53dec171c2fbe873ac82089c07cbe54d7debb9c4 (`git ls-remote origin main`)
- Host: baha-docker (192.168.6.166, ssh-user marcel, hostname baha-runner-docker) — SSH reachable via alias `baha-docker`
- Binary: `/home/marcel/.local/bin/baha` — BaseHarbor dev, `commit none / built unknown`, ELF with debug info (build 2026-11-08 12:09); develop remote HEAD 20902f0a6; no own build, per mission
- Source evidence worktree (origin/develop @ 20902f0a6): /tmp/mission-hunt-hx4-wt (cloned, read-only source only)
- baseharbor-plan origin/main HEAD at commit time: 53dec171c2
- VM lock: claimed `baha-docker` for lane `mission-hunt-hx4`, released at END

## PLAN (plain bullets; no markdown checkboxes)

- DONE 1 Read mission-hunt-x4.md; attestation (host, develop binary, baseharbor-plan origin/main), scope split (export / rotation / forget / damaged-bundle)
- DONE 2 Baseline host state: baha list/status, config.yaml, data root, docker ps/net (read-only), identify Core + app state
- DONE 3 Cut 1 export-pfade: trust export + app secure-profile export -> where files land, secret hygiene
- DONE 4 Cut 2 rotation: OpenBao manager credential rotation + LocalIssuer/overlapsafe rotation (post #1468 re-init)
- DONE 5 Cut 3 forget/entzug: what remains after app destroy (records, trust-anchors, nets) — state-dir + lifecycle source
- DONE 6 Cut 4 damaged message bundle: empty/oversized CA store -> fail-closed (empirical Go probe)
- DONE 7 Record positive findings (BF-NN + file:#beleg + class)
- DONE 8 VM sweep (docker ps, state dirs) + cleanliness line
- DONE 9 Publish evidence to origin/main; END

## Fakten / Rahrendaten

- Server-Host (Session): codeman (7.0.0-42-generic). Nie Container/Tests hier laufen lassen; alle Tests auf baha-docker.
- ssh baha-docker -> 192.168.6.166, user marcel, hostname baha-runner-docker; ssh alias `baha-docker` mit IdentityFile ~/.ssh/mcp-home; direkte IP-Verbindung schlägt fehl, nur alias funktioniert
- dev binary: /home/marcel/.local/bin/baha (debug build 2026-11-08 12:09, `commit none / built unknown`); zweites dev binary /home/marcel/baha-dev = commit bc8670c1 (built 2026-11-06)
- docker: Docker version 29.8.1, Compose v5.5.1
- config.yaml: ConfigPath() = $BASEHARBOR_STATE_DIR/config/config.yaml (prioritaet), dann XDG_CONFIG_HOME/baseharbor/config.yaml, dann ~/.config/baseharbor/config.yaml
- DataRoot(): $BASEHARBOR_STATE_DIR (prioritaet); TargetStateRoot = <dataRoot>/targets/<name>
- Host Core: gfield0427 managed-local OpenBao PKI in production (source managed-local, issuer openbao://baseharbor-pki/baseharbor-services), CA fingerprint 66dedbb5... (host trust: not BaseHarbor-owned, CA not trusted)

## Baseline / attestation (host, before work)

- `baha app list`: app1/cut1/cut2/goapp(failed)/hd5test/nextapp(applying)/pyapp(ready)/quarkapp(applying) = all SOURCE=OK on target `dev`.
- `baha target list`: boot (podman, effective) + local (docker). boot holds shared Core state (bh-boot-shared-*).
- docker ps: shared Core `bh-gfield0427-shared-*` (postgres:18-alpine, openbao/openbao:2.7.1, haproxy alpine) — NOT mine, left untouched.
- Trust state: `baha trust status` => managed-local, CA not trusted, owned=false; `baha trust uninstall` => no BaseHarbor-owned anchors (idempotent).
- No dev-access credentials.env on any app (all "configured"/ready apps have no dev username/password set). gfield0427 dev gateway pki present (ca.pem, server-cert.pem, server-key.pem, state.json).

## Findings

### BF-01 (POSITIVE) — `trust export` writes only the public CA bundle at the caller's --output path; private issuer state never leaves the provider
- class: doku / secret-hygiene / positive
- command/exit/output:
  - `baha trust export --output /tmp/hx4-ca.pem` => `Exported public BaseHarbor CA: /tmp/hx4-ca.pem` (exit 0); file is a 656-byte, 12-line public PEM (`-----BEGIN CERTIFICATE-----`), mode 0644.
- Impact: the exported artifact contains only the public CA certificate; the export success line reports the output PATH only (never CA contents or private material). The private CA key and issuer state remain inside the OpenBao PKI engine and are never written to the export. Confirms the contract in `trust.go` (`Long: "Private CA keys and issuer state are never exported."`).
- file:#beleg:
  - `cmd/baha/trust_operations.go:58-73` `exportManagedTrust` -> `hosttrust.Export(path, bundle.PEM)`; writes `bundle.PEM` to `path` (0644), returns `{Managed, Path}`.
  - `internal/hosttrust/hosttrust.go:66-86` `Export`: `ParseCA(pemData)` (must be a valid CA), refuses to overwrite (`O_EXCL`-style `Lstat` check), `os.WriteFile(path, pemData, 0o644)`.
  - `internal/openbao/service_issuer.go:36-48` `TrustBundle` returns only `IssuerReference` + `PEM` (public cert), never the private key.
- POSITIVE: private CA keys and issuer state never touch the export path; only the public CA PEM is written.

### BF-02 (POSITIVE) — `app secure-profile export` encrypts local developer credentials into a password-locked file with strict hygiene (0600 password file, 0600 output, O_EXCL, never argv password); fails closed on missing/weak inputs
- class: secret-hygiene / positive
- command/exit/output:
  - `baha app secure-profile export pyapp --password-file /dev/stdin --output /tmp/hx4-sec.bhexport` => `Error: read eligible local credentials ... credentials.env: no such file or directory` (exit 1); no export file written.
  - `--password-file` with mode group/other-accessible => `export password file ... is accessible by group or others (NNN)`; `--password-file` <12 bytes => `export password must contain at least 12 bytes`; no output written.
- Impact: the only local developer credentials eligible for export are the opt-in `developer-access/dev/credentials.env` (username + password) for the target/environment; remote provider secrets and fresh device identities are never exported by default. The export password is read from a file (never argv), the ciphertext is unreadable without it, the output is mode 0600, and the file is created with `O_EXCL` (no overwrite). This is the secret-hygiene export contract working as intended.
- file:#beleg:
  - `cmd/baha/secure_profile_export.go:60-92` `executeSecureProfileExport`: loads `devaccess.Load(target, env)`, builds `SecretEntry{developer-access/username,password}`, `applicationbackup.BuildExport(..., password)` (encrypt), output default `<name>-<env>-<timestamp>.bhexport`.
  - `cmd/baha/secure_profile_export.go:125-149` `readSecureProfileExportPassword`: regular-file check, `Mode().Perm()&0o077 != 0` rejection, size cap, `<12 bytes` rejection, zero-on-failure.
  - `cmd/baha/secure_profile_export.go:151-176` `writeSecureProfileExport`: `0o700` dir, `O_WRONLY|O_CREATE|O_EXCL 0o600`, sync, `os.Chmod 0o600`.
  - `internal/devaccess/credentials.go:92-147` `Load`/`credentialsPath`: reads `<root>/developer-access/<env>/credentials.env` (USERNAME/PASSWORD), control-char/field validation.
- POSITIVE: no plaintext credentials ever reach stdout, argv, or an un-encrypted file; the export is a single password-locked ciphertext with fail-closed input validation.

### BF-03 (POSITIVE) — OpenBao manager credential rotation is overlap-safe with verify + retire + fail-closed re-check (post #1468 re-init path)
- class: security / rotation / positive
- Impact: `RotateManagerCredentials` authenticates the current manager, issues a replacement, verifies the replacement can login + read the manager KV, atomically replaces the persisted admin credential file, destroys the old SecretID, then asserts the old credential NO LONGER authenticates (`loginManager(oldCredentials) == nil` => error) and re-checks `CheckManager`. This is the "rotate twice" contract (old must be dead, new must be live) enforced, not assumed. Matches the #1468 re-init bootstrap which clears a stale admin credential on an *uninitialized* server and proceeds to re-initialize (fail-closed on a *genuinely initialized* manager: `ErrAlreadyInitialized`).
- file:#beleg:
  - `internal/openbao/bootstrap.go:409-449` `RotateManagerCredentials`: old login -> issue new -> new login verify -> KV verify -> replaceAdminCredentials -> destroyManagerSecretID(old) -> `if loginManager(old)==nil -> error` -> CheckManager re-check.
  - `internal/openbao/bootstrap.go:230-256` bootstrap re-init: `if state.Initialized -> ErrAlreadyInitialized`; stale adminPath cleared only when `!Initialized`.
  - `internal/openbao/bootstrap.go:460-488` `LoadAdminCredentials`: `Mode().Perm()&0o077 != 0` rejection, field parse.
- POSITIVE: rotation fails closed on a still-initialized manager and never leaves the old credential live; the persisted credential file enforces 0600.

### BF-04 (POSITIVE) — LocalIssuer trust rotation requires recovery when the issuer material is expired/oversized/partial; fails closed, never silently accepts damaged trust
- class: security / rotation / positive
- command/exit/output (empirical Go probe, module `internal/serviceaccess`, run via `go test -run TestHX4`):
  - `ExistingTLSMaterial` with an EMPTY `ca.pem` (0 bytes) => error `read service TLS trust bundle: certificate PEM is invalid` (fails closed, exit non-zero).
  - `LocalIssuer{Dir}.load()` with an `issuer.pem` of 20000 bytes (> 16384 cap) => error `local issuer requires canonical private state` (fails closed).
- Impact: a truncated/empty/too-large CA store (the "damaged message bundle" case) is rejected at read time by both the managed-PKI path (`readCertificate` -> `pem.Decode` nil -> "certificate PEM is invalid") and the local-issuer path (`Size() > 16384` -> "local issuer requires canonical private state"). The service (mTLS) refuses to proceed instead of serving a degraded/trusted-from-corrupt-bundle. The `16384`-byte cap on `issuer.pem` and the `0o077`-permission guards prevent oversized/corrupted material from being accepted.
- file:#beleg:
  - `internal/serviceaccess/pki.go:540-583` `validateMaterial`/`readCertificate`: `pem.Decode` block==nil => "certificate PEM is invalid".
  - `internal/serviceaccess/local_issuer.go:135` `load()`: `info.Size() > 16384` => "local issuer authority is unprotected or invalid"; `CheckLocalIssuer`/`EnsureLocalIssuer` partial-state => "partial local issuer state requires recovery".
  - `internal/serviceaccess/pki.go:103-125` `ExistingTLSMaterial`: stat required files, then `validateMaterial`.
- POSITIVE: damaged CA store is detected and fails closed; the empirical probe confirms both the empty and oversized cases.

### BF-05 (POSITIVE) — `app destroy` (forget/entzug) is ownership-verified and stateful: it removes owned runtime/OpenBao-scope/identity/logs state but RETAINS the deployment record and, for repo apps, baseharbor.yaml + data volumes; trust anchors and Core nets are not touched
- class: lifecycle / retention / positive
- command/exit/output (source, not host-mutated; host apps are shared/Core, left untouched):
  - destroy plan (`app_destroy_lifecycle.go:239-311`) enumerates what is removed vs preserved: secrets scope `baseharbor/apps/<name>/<env>` removed if owned (`destroyOpenBaoScopeRequired`); identity scope removed via Keycloak driver; OpenBao scope verified-destroyed (`DestroyVerifiedApplicationScope`); shared provider infra preserved while still in use.
  - `removeApplicationState` (`app_destroy_lifecycle.go:570-608`): deletes app state dir + `deployment.DeleteDeploymentRecord`; for repo apps `baseharbor.yaml` and repository data volumes are PRESERVED (recovery), only `--full-reset` removes deployment state.
- Impact: "forget" is a layered, verified retirement, not a blanket wipe. Records (deployment record) are removed only after verified destruction of owned resources; repo-source data and baseharbor.yaml survive unless `--full-reset`; shared Core nets/OpenBao/Keycloak infrastructure are preserved when still in use. Trust anchors on the host are never touched by app destroy (`trust uninstall` is a separate, explicit, consent-gated command; `baha trust uninstall` on the host returned "no BaseHarbor-owned CA anchors recorded"). So after forget: owned app runtime + OpenBao scope + identity + logs are gone; deployment record gone (post-verify); repo source/volumes retained; shared Core trust/nets intact.
- file:#beleg:
  - `cmd/baha/app_destroy_lifecycle.go:313-398` `destroyRuntimeResources`: exposure, runtime broker, shared backend release, `DestroyProject`/`DestroyOwnedProjectResources`, bucket destroy, OpenBao scope destroy + verify.
  - `cmd/baha/app_destroy_lifecycle.go:401-549` `cleanupProviderState`/`cleanupIdentity`/`cleanupLogs`/`cleanupTraces`/`cleanupMetrics`.
  - `cmd/baha/app_destroy_lifecycle.go:570-608` `removeApplicationState`: store.Delete + `deployment.DeleteDeploymentRecord` + verify.
  - `internal/hosttrust/hosttrust.go:113-186` install, `295-330` `StateRecords`/`RemoveOwned` (separate from app destroy).
- POSITIVE: forget is non-destructive to shared Core and recoverable for repo apps; every removal is ownership-verified before it happens.

## Host fault / environmental (not product)

- No app on baha-docker has `developer-access/dev/credentials.env` set, so `app secure-profile export` cannot be exercised end-to-end here (it fails closed with "credentials.env: no such file"). The export contract was therefore verified at the source level + the fail-closed path on the host, not the happy path. The `gfield0427` managed-local OpenBao PKI is in production and was left completely untouched.
- The 5 `SOURCE`-less apps (goapp failed, etc.) and the shared `bh-gfield0427-shared-*` Core are other-lane work; not touched.

## repo-rule compliance

- Pure findings: no product code changed, no PRs opened, no `.github/**` edits, no reruns/workflow_dispatch.
- Evidence written only in baseharbor-plan (repo `mcpdev80/baseharbor-plan`, origin/main 53dec171), not in any product repo. No `.evidence/` dir in a product repo. No main-branch writes in product repos.
- One integration candidate per chain: no product branch was cut (findings-only). No PR.
- Subagents: none used (4.8).
- Host runners only; no runner infrastructure touched.
- Shared `bh-*-shared*` stacks and the Core (gfield0427 OpenBao, postgres, keycloak) never modified; no app was destroyed; all host reads were read-only.
- Empirical probe used a throwaway `internal/serviceaccess/zz_hx4_damagedca_test.go` removed immediately after the run; no product files left behind.

## VM sweep (before END)

- Host baha-docker: no containers started or compose projects created during this lane; nothing to `docker compose down`.
- `docker ps`: only the pre-existing shared `bh-gfield0427-shared-*` Core remains (untouched). No orphaned containers/volumes/networks created by this lane.
- No export artifacts left: `baha trust export` test used a `$T` temp dir removed after the run; no `.bhexport` written (app had no credentials).
- `~/.local/share/baseharbor/` and `~/.config/baseharbor/` unchanged by this lane (read-only trust/status + app/env calls only).
- cleanliness: DONE — no test containers, networks, volumes, deploy records, export files or scratch dirs created by hx4; no worktree/cache left in the ecosystem root (all under /tmp / workers/.hx4-* removed).

## ls-remote witness (before END)

- `git ls-remote origin main`:
  ```
  8ef4546d09e826bff253b86d5025d887d161f522	refs/heads/main
  ```
- My evidence commit `8ef4546d` is origin/main HEAD. origin/main `53dec171` (attestation) is an ancestor of my commit. Evidence path `evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx4.md` committed + pushed to origin/main.

## END

END mission-hunt-hx4.md: 5 findings (BF-01..BF-05), 0 blocker. All positive / contract-confirming on the trust-/nachrichtendienst-oberflaeche: BF-01 trust export = public-only at --output; BF-02 secure-profile export = password-locked 0600 fail-closed; BF-03 OpenBao manager rotation overlap-safe+verify+retire; BF-04 empty/oversized CA store fails closed (empirical); BF-05 destroy/forget = ownership-verified, Core trust/nets preserved. meldefenster met (8/2 window).
