# Bug-Hunt H-X3 — target-lebenszyklus & referenz-semantik auf baha-podman

- Card/mission: mission-hunt-hx3.md (Bug-Hunt H-X3, pure findings, no product code, no PRs)
- Shift: r27-welle5-folge-2026-11-08 / round-1
- Worker session: laptop (podman), no subagents (4.8)
- Planning repo verified (origin/main): 9b076e3e746e71a6c12f30f6e06c14f2c093f96e (`git ls-remote origin main`)
- Host: baha-runner-podman (192.168.6.148, `baha-podman`), rootless podman 5.7.0
- Binary: `/home/marcel/.local/bin/baha` — BaseHarbor dev, commit 46ea6c73d17f1eb30f9346803f30b6cb6233c42c (develop binary; no own build, per mission)
- baseharbor-plan origin/main HEAD at commit time: 9b076e3e
- Worktree read-only: /tmp/opencode/mission-hunt-hx3-wt @ 5c5e24a7c (main aff1532c), used for source evidence only
- VM lock: claimed `baha-podman` for lane `mission-hunt-hx3`, released at END

## PLAN

- Read mission + AGENTS; attestation (host, develop binary, baseharbor-plan origin/main)
- Baseline host state (target list/show, deployments, apps, podman ps/net/volumes)
- Cut 1: target create a second podman target with --reference local (clone? conflict? shared state?)
- Cut 2: target delete -> what happens with apps/records/at target (orphaned?) + recovery/restore
- Cut 3: target activate/use/switch — status/list/show consistency after switch, BASEHARBOR_TARGET vs activated
- Cut 4: two podman targets same runtime — core-sharing, ports, names
- Record positive findings
- Per-finding BF-NN with file:#evidence + class
- VM sweep (baha target/list, podman ps/net/volumes) + cleanliness line
- Release VM lock; publish evidence to origin/main; END

## Baseline / attestation

- Targets present: `boot` (podman, access local, SELECTOR default,effective) and `local` (docker, access local, SELECTOR implicit). `boot` is the active Core target.
- `boot` holds shared Core state (postgres, openbao, keycloak, valkey) running as `bh-boot-shared-*` containers on `baseharbor-boot-*` networks — NOT mine, left untouched.
- Develop binary commit 46ea6c73 (built unknown) at ~/.local/bin/baha; not on PATH (must call full path).
- No ~/.baha; state under ~/.local/share/baseharbor + ~/.config/baseharbor.
- Host disk 54% used, no pressure.

## Host baseline (captured before work)

- `baha app list`: hp1app, hp1sql, hp3c1 (x2), hp3c2 = `configured MISSING` (repos gone); hp3c5, hp3c9 = `created OK`.
- `baha target list`: boot (podman, effective), local (docker, implicit).
- `podman ps`: shared Core containers `bh-boot-shared-*` on `baseharbor-boot-default`/`-secrets`/`baseharbor-identity-core-boot` networks.
- boot runtime.env exposes dynamically assigned ports: `BASEHARBOR_POSTGRES_PORT=15433`, `BASEHARBOR_OPENBAO_PORT=18201`.

## Findings

### BF-01 — `--reference` is an ACCESS reference, not a target-clone reference; creating a second target that reuses an access name with a different reference fails with a typed conflict
- class: doku / clarity
- command/exit/output:
  - `baha target create podman2test --runtime-provider podman --access local --access-provider local --reference local --scope default` => `Target podman2test created (runtime podman, access local via local, scope default)` (exit 0).
  - `--reference` is parsed into `cfg.Access[accessName]` (source `cmd/baha/target_mutation.go:78`); it names the access the target binds, never a source target to clone. There is no target-clone / `--reference <target>` semantics.
  - Creating a target that binds an access name already used with a *different* reference fails: `target_mutation.go:73-76` -> `access "local" already exists with different provider/reference`.
- Impact: an operator reading the `--reference` help (`baha target create NAME --reference REFERENCE`) infers a clone/alias reference; the flag actually selects the access the new target connects through. Confused with a clone reference would produce the access-exists conflict, not a clone. Class: doku.
- file:#beleg: `cmd/baha/target.go:506-507` (`--reference` -> `reference`), `cmd/baha/target_mutation.go:70-79` (access-name uniqueness check + `cfg.Access[accessName] = AccessDefinition{Provider, Reference}`).

### BF-02 — `use`/`activate` fail closed on a target whose runtime state has no `service-access/issuer`, even when the Core is visibly running on the same machine
- class: ux / daemm / blocker-kandidat
- command/exit/output:
  - `baha use boot` => `Error: target "boot" has no verified management connection: installation not verifiable as a genuine baseharbor Core installation, fails closed` (exit 1).
  - Yet `baha status` on boot reports `postgres READY`, `openbao` reachable, control plane started — the Core is clearly live.
  - Root cause verified on disk: `~/.local/share/baseharbor/targets/boot/service-access/issuer/` does NOT exist (only `runtime/`, `providers/`, `deployments/` present).
- Impact: a target that is running but whose management CA issuer directory is absent (fresh bootstrap, partial install, state moved/cleared) cannot be selected at all with `use`/`activate`, even though `status`/`doctor` read it fine. The operator is told to `baha core install` to "install a BaseHarbor Core", which does not exist as a subcommand in this build (`baha core --help` => `unknown command "core"`). Confusing dead-end guidance.
- file:#beleg:
  - `cmd/baha/use_target.go:61-112` `bindExplicitSelectionToConnection` -> `coreinstallation.Load(root)` then `coreinstallation.ResolverForTargetSelection`.
  - `internal/coreinstallation/authority.go:356-396` `ResolverForTargetSelection` -> `issuerStateDir = <root>/service-access/issuer`, `observeLocalIssuer` fails closed (maps any issuer error to `ErrUnverifiableInstallation`).
  - `internal/coreinstallation/authority.go:73` `ErrUnverifiableInstallation = "installation not verifiable as a genuine baseharbor Core installation, fails closed"`.
  - `cmd/baha/target.go` help (line 249): no `core` subcommand; `core install` referenced in the error text is unreachable.
- POSITIVE (counter): `baha status --target boot` and `BASEHARBOR_TARGET=boot baha status` both work (read path does not require the issuer), so the Core is fully observable — only the selection boundary fails closed.

### BF-03 — target delete requires 2 interactive provider-impact confirmations; fails with `impact-confirmation-required` in a non-TTY even with --yes
- class: ux / daemm
- command/exit/output:
  - `baha target delete podman2test` (no TTY): `Error: provider change: impact-confirmation-required` (exit 1); config unchanged, target still listed.
  - Same via pty (`printf "y\ny\n" | script -qec "…target delete podman2test" /dev/null`): both prompts `Achtung: confirm the displayed outcome without a working alternative (1/2, plan …)` / `(2/2, …)` accepted, then `Target podman2test definition detached; runtime/data owners retained. Recovery: <recovery_file>` (exit 0).
  - The detach emits a provider-impact scope `scope.confirmations_required=2`, `scope.destructive=false`; `--yes` does not imply either acknowledgement.
- Impact: automation / scripts / dispatch cannot detach a target definition (a non-destructive config-only action) without a pty. The action is config-only (no data deletion), yet it demands two interactive confirmations, matching the two-stage consent class seen in hx2 (BF-02).
- file:#beleg:
  - `cmd/baha/target_definition_change.go:52-61` builds `plan.Scope` with `ConfirmationsRequired: 2`, calls `ValidateProviderImpactScopeConsent` -> returns the impact-confirmation error when no consent.
  - `cmd/baha/target.go:448` `deleteTarget` -> `deleteTargetDefinition`.
- POSITIVE: on success, detachment is config-only — the original definition is persisted to `~/.config/baseharbor/target-recovery/<name>-<sha>.json` and runtime/deployments are preserved for `--from-recovery`.

### BF-04 — target delete is config-only and leaves deployment records / runtime state intact (orphaned records are NOT cleaned; no app-delete path for source-less records)
- class: doku / daemm
- command/exit/output:
  - After `baha target delete podman2test`, `boot`'s 7 deployment records were untouched; boot still `EFFECTIVE`, `doctor` all OK.
  - `baha app list --all-targets` shows 5 records with `SOURCE=MISSING` (hp1app, hp1sql, hp3c1 x2, hp3c2) — their repos (`/home/marcel/hp3/work/hp1app`, …) no longer exist. These are ORPHANED on boot.
  - `baha destroy hp1app` => `Error: unknown argument hp1app`; `baha destroy` only takes `[--yes] [--delete-data] | --all`. No per-app removal exists for a source-less deployment.
- Impact: when a target is detached, its deployments are retained (by design, for recovery) but the deployment records pointing at now-missing source repos become uncollectable orphans — `destroy` cannot reach them (needs the app repo) and there is no `baha app delete/remove` subcommand. `app list --all-targets` surfaces them as `SOURCE=MISSING` (the only detection path).
- file:#beleg:
  - `cmd/baha/target_definition_change.go:101-113` detach: only `delete(plan.cfg.Targets, name)` + recovery write; no deployment/runtime wipe.
  - `cmd/baha/target_definition_change.go:150-165` `lockExistingTargetDefinitionLifecycle` only reads `/.installation.lock` for a lifecycle lock.
  - `cmd/baha/app_commands.go:110-118` `app list --all-targets` renders `SOURCE` = MISSING/OK via `deployment.SourceAvailable`.
  - `cmd/baha/target.go:448-487` destroy usage string has no app argument.
- POSITIVE: `app list --all-targets` is a correct orphan-detector (TARGET/APPLICATION/STATE/SOURCE); the missing piece is a cleanup path for the MISSING records.

### BF-05 — `--reference` on `target create` is an ACCESS reference; "two podman targets" with the same local reference do NOT create two Cores — the second target's control-plane `up` connects to the existing shared Core and creates no separate project/volumes/names
- class: architecture / shared-state / blocker-kandidat
- command/exit/output:
  - `baha target create podman2test --runtime-provider podman --access local --access-provider local --reference local --scope default` (2x podman on same machine) then `baha up --control-plane-only --yes`:
    - `[OK] postgres verified TLS query succeeded on 127.0.0.1:15433` — the SAME port as boot's runtime.env.
    - `BaseHarbor Core READY: SQL + Secrets + Identity.` (exit 0).
    - No `bh-podman2test-shared` project created; `podman ps` shows only `bh-boot-shared-*`; no `baseharbor-podman2test-*` network; `podman2test` state dir never created.
  - After: `podman2test` has no state dir (`ls ~/.local/share/baseharbor/targets/podman2test` => No such file); `status` still shows `Selection source: boot (configured-default)`, effective boot.
- Impact: two podman targets on the same host are NOT isolated runtime domains. A second target's control-plane startup reuses the already-running shared Core (same ports 15433/18201, same `baseharbor-boot-*` networks, same `bh-boot-shared-*` containers) rather than failing on port/name conflict. The `--scope`/`--reference` inputs do not partition the machine's shared Core. An operator expecting two independent podman Cores gets one shared Core — a shared-state / port-collision hazard that silently resolves instead of erroring.
- file:#beleg:
  - `internal/runtime/project_names.go:7-9` `SharedProjectName(namespace)` => `bh-<namespace>-shared`; the Core project is keyed by the *target name*, but the running discovery resolves the existing shared Core on the machine.
  - `cmd/baha/target.go:603-605` `targetRuntimeProjectName(target) = SharedProjectName(target.Name)`.
  - boot runtime.env `BASEHARBOR_POSTGRES_PORT=15433`, `BASEHARBOR_OPENBAO_PORT=18201` reused by the second `up` (no new assignment).
- POSITIVE: no orphaned containers/networks/volumes from the second target — the reuse was clean; cleanup removed the config entry and its recovery file.

### BF-06 (POSITIVE) — activate/use/switch status/list/show are consistent across all three selection sources
- class: doku / positive
- command/exit/output:
  - `baha status` (no override) => `Selection source: boot (configured-default)`, EFFECTIVE boot.
  - `BASEHARBOR_TARGET=boot baha status` => `Selection source: boot (environment)`, EFFECTIVE boot.
  - `baha status --target boot` => `Selection source: boot (explicit)`, EFFECTIVE boot.
  - `BASEHARBOR_TARGET=podman2test baha status` (target deleted) => `Error: target "podman2test" is not configured` (fails closed; no silent fallback to boot).
  - `baha target list --output json` exposes per-target `selectors` (boot: `["default","effective"]`, local: `["implicit"]`); podman2test had `selectors=[]` while active-less.
- Impact: the CLI surfaces all three selection sources distinctly and refuses unknown targets instead of guessing. Operators can tell a persisted default from an env override from an explicit flag. Consistent between `status`/`list`/`show`.
- file:#beleg: `cmd/baha/target.go` selection precedence; `status` prints the source; `target list --output json` prints selectors.

### BF-07 (POSITIVE) — delete/restore round-trip preserves the original target definition byte-exactly
- class: doku / positive
- command/exit/output:
  - `baha target create podman2test … --scope default` then `delete` => recovery file `podman2test-113a78a255d1c2e294f2ddc07f8c64c65e2636756d776381436f46faed515cd1.json` containing `{"definition":{"runtime":{"provider":"podman"},"access":{"reference":"local"},"scope":"default","openbao":{}},"access":{"provider":"local","reference":"local"}}`.
  - `baha target create podman2test --from-recovery <file>` (pty, 2 confirms) => `Target podman2test definition restored; live access and authentication remain to be verified.` (exit 0), reappears in `target list`.
  - Final `delete` + recovery-file removal returned config to exactly `boot` + `local`.
- Impact: the detach/restore lifecycle is recoverable and non-destructive for the definition; retention is verified by byte-back in the detach result (`target_definition_change.go:104`).

## Host fault (environmental, not product)

- The 5 `SOURCE=MISSING` deployment records (hp1app, hp1sql, hp3c1 x2, hp3c2) are leftovers from other lanes' work whose source repos were removed; they are orphans on the shared `boot` Core. Not caused by this lane. The `boot` Core itself (postgres/openbao/keycloak) was healthy at check time (all OK in `baha doctor`).

## repo-rule compliance

- Pure findings: no product code changed, no PRs opened, no `.github/**` edits, no reruns/workflow_dispatch.
- Evidence written only in baseharbor-plan (repo `mcpdev80/baseharbor-plan`), not in any product repo. No `.evidence/` dir in a product repo. No main-branch writes in product repos.
- One integration candidate per chain: no product branch was cut (findings-only). No PR.
- Subagents: none used (4.8).
- Host runners only; no runner infrastructure touched.
- Shared `bh-*-shared*` stacks and the `boot` Core never modified; only config entries created/deleted for the lane's own `podman2test` target.

## VM sweep (before END)

- `baha target list`: only `boot` (podman, effective) + `local` (docker) remain — my `podman2test` config entry and its recovery file removed.
- `podman ps`: `no hx3/podman2test containers` — clean, no orphaned containers/volumes/networks.
- `~/.config/baseharbor/config.yaml`: restored to exactly `boot` + `local`.
- recovery dir `~/.config/baseharbor/target-recovery/`: empty (my `podman2test-*.json` removed).
- cleanliness: DONE — no test containers, networks, volumes, deploy records or scratch dirs for hx3 remain; host disk 54%.

## END

END mission-hunt-hx3.md: 7 findings (BF-01..BF-07), 2 blocker-kandidaten (BF-02 `use`/`activate` fail-closed without issuer; BF-05 second podman target silently reuses shared Core, no isolation), meldefenster met.
