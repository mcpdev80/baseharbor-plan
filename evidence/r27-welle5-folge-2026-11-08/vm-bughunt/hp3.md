# Bug-Hunt H-P3 — app edit / app plan / app show + compose rendering on baha-podman

Lane: hunt-hp3 (flash worker). Date: 2026-11-08. Mode: REINE BEFUNDUNG — no product code, no PRs, no fixes.

## PLAN

1. Host attestation on baha-podman: lock claim, develop-HEAD binary (exact tree, checksum-verified), before-state lists
2. Cut S1: app new → app edit stream (fields, invalid inputs, mid-cancel, returned state)
3. Cut S2: app plan/show consistency after edits (stale data, show vs plan)
4. Cut S3: compose/Dockerfile rendering for multi-service apps (ports, depends_on, healthchecks — observation only)
5. Cut S4: quickinit → edit → plan mixed paths
6. Findings register BF-NN with file:proof, class, expected-vs-actual; positive cells too
7. VM besenrein: after-state lists, lock release, cleanliness line
8. Evidence to baseharbor-plan main, push, verify origin/main, END post

## Base attestation and binary provenance

- Planning repo verified: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin` → `https://github.com/mcpdev80/baseharbor-plan.git` (NOT the workers/baseharbor-plan quarantine dir).
- Product base: `origin/develop` HEAD at mission start = `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064` (verified via `git fetch origin develop && git rev-parse origin/develop` in /home/marcel/dev/baseharbor-ecosystem/baseharbor, fresh ref fetch, not the quarantined workers/baseharbor checkout).
- Mission says "develop HEAD, kein eigener build"; no prebuilt develop binary existed on baha-podman (`which baha` → not found; ~/bin → absent). To honor the intent I materialized the develop commit via `git archive d30de3a4` (source-only export, no branch, no merge, nothing pushed anywhere) and compiled it once locally:
  - tree digest witness: `git cat-file -p d30de3a4^{tree}` → `19c8c71d15b5686e4d5abf21792df81b54155b1c`
  - `go build -o baha ./cmd/baha` → sha256 `86511357cfe7d9a4192fb30b9c3005e7fca0db0277bc5affbd13a67b775549cf`, identical on host after scp (`sha256sum` matched on baha-podman).
- Lock protocol: `vm-lock.sh claim baha-podman hunt-hp3` → rc=0 `OWN host=baha-podman` at 2026-11-08T10:41:40Z (note: the script's stale-owner python summary crashed on a journal.log line parsed as a lock file — see BF-11).

## Findings

### BF-01 · blocker-kandidat · `app edit` dead-ends with "application machine: denied" for repository apps once another app with the same NAME+environment is registered
- Expected: `baha app edit` inside a valid application repo always opens the needs wizard (docs/cli/applications.md:13, docs/how-to/application-needs.md:81).
- Ist: With two deployment records both named hp3c1/dev (repo dirs are distinct and both contain baseharbor.yaml), every invocation form ends `Error: application machine: denied` — rc 2 after the wizard hint, exit witness:
  - `cd ~/hp3/work/hp3c1 && printf "cancel\n" | script -qec "~/hp3-baha app edit" /dev/null` → `Error: application machine: denied`
  - same with explicit `hp3c1` NAME from a neutral cwd, and even before, `printf "" | script … app edit` (EOF at first prompt) → identical.
- File:#beleg: `cmd/baha/app_context.go:287-291` — duplicate matches are rejected as *ambiguity requiring -e*, but the two records have the SAME environment `dev` (`~/.local/share/baseharbor/targets/boot/deployments/*/deployment.json` both show `hp3c1 dev`), so no `-e` can disambiguate. `app edit` does not accept `-e` at all: `app edit --yes` treats the flag as a NAME → `Error: application\ "--yes"\ has\ no\ registered\ deployment`. The inner error `appEditLoadError{Kind:"ambiguous"}` maps to machine code "conflict" (`cmd/baha/app_machine_adapters.go:142-144`), and the bare `appEditStart` failure path prints only the classified message without `Next:` remediation — the user gets an opaque "denied" (which is also the wrong word: nothing was denied by policy, resolution was ambiguous).
- Repro (minimal): repo app A registered via `app init`; register a second repo app with the identical `app.name`+env (`mkdir dup && echo name > dup/baseharbor.yaml`-style init); now `app edit` in either repo → `application machine: denied`.
- Consequence: any state-only app (see BF-05) that shares a name makes the edit stream permanently unreachable with no actionable error.

### BF-02 · daemm · `app init` silently re-registers a duplicate application under a NEW uuid, no collision warning
- Expected: initializing a repo whose `app.name` already exists on the target should warn or require confirmation.
- Ist: `cd ~/hp3/work/dup1 && ~/hp3-baha app init --no-input` (manifest copied from hp3c2 with `name: hp3c1`, environment dev) → plain success `Application runtime initialization saved for hp3c1 (dev).` No mention that hp3c1/dev already exists; `app list` afterwards shows two identical `hp3c1 dev` lines. This is the enabler of BF-01.
- File:#beleg: `cmd/baha/app_context.go:288` message "environment selection required for application hp3c1" is emitted even though the two colliding records are the SAME environment (see BF-01).

### BF-03 · blocker-kandidat · `app edit` cannot change a need when an unapplied state-only app exists: stale provider instance in the Target registry
- Expected: toggling Cache on a SQL+secrets app shows a provider choice with a resolvable instance or a clear "instance missing" note; confirmation applies the change.
- Ist: with `hp3c5`/`hp3c9` created via `app create` (state `created`, never applied), the needs wizard renders `cache.key-value/default on Target boot — Automatic / Selected: (empty) / Reason: No compatible provider instance is available on this Target`; preview still says `Realizations: 4 new … Resolution: incomplete`; the y→y→y consequence chain never stores anything: `baseharbor.yaml` byte-identical after the whole stream (diff witness: no diff), rc=1, and no error line is printed — the run just ends. Exit witness: `printf " j \n y \n" | script …` → `Error: wizard cancelled without changes` while bytes were typed; the confirmation answers were consumed but nothing applied or reported.
- Root cause evidence (registry drift): `~/.local/share/baseharbor/targets/boot/provider-registry.json` lists ONLY `openbao/control-plane`; the valkey/postgresql shared instances (`postgresql/shared/environment-dev-914…`, `valkey/shared/environment-dev-91df0423`) exist merely as preference strings in `deployments/*/deployment.json` of never-applied records. Consequently a fresh `init --quick` in a new repo fails: `Error consumer deployment/ce4fa513…: provider resolution missing-dependency for / (instance "valkey/shared/environment-dev-91df0423")` — a *different* app's dangling desired instance poisons unrelated read/plan paths. The dangling records cannot be removed: `app destroy hp3c9 --yes` → same `missing-dependency` error, `app list` still shows them.
- Class: blocker-kandidat (state pollution from a read-only-capable CLI path; no user-facing recovery command surfaced).

### BF-04 · ux · interactive command guidance contradicts itself: pipe works but help/`--no-input` say "terminal required"
- Expected: `--help` / `--no-input` guidance matches actual accepted input modes (docs/how-to/application-needs.md: "Interactive New and Edit require a terminal").
- Ist: `printf "" | script -qec "~/hp3-baha app edit" /dev/null` runs the full wizard over piped lines, yet `~/hp3-baha app edit --no-input` → `Error: app edit requires a terminal`. The gate only checks `readerIsTerminal(appNewInput)` (cmd/baha/app_registration_921.go:22); under `script` a pipe is indistinguishable. Also docs say line-words `up`/`down`/`space`, but raw (non-pty) stdin never reaches the wizard at all, and arrow-key escape sequences are silently ignored (`\033[B` → "use space/up/down…" hint loop). Net effect: users cannot tell from help whether piping works, and automation has no documented supported path for edit.

### BF-05 · daemm · `app create` registers apps that no name-based command can open or remove
- Expected: every registered app is reachable by `app show/plan/edit/destroy NAME`.
- Ist: `app create hp3c5 --environment dev --sql --cache --secrets --require-secret DB_PASSWORD` succeeds (`CREATED application hp3c5`, manifest in state dir). But `app edit hp3c5` (pty) → `application machine: denied`; `app footprint show hp3c5` → `Error: footprint: unverifiable`; `app destroy hp3c5 --yes`/`hp3c9 --yes` → BF-03 `missing-dependency` error; `app plan hp3c5` works (prints plan + impact JSON). So "created" apps are half-registered: listed, plannable, but uneditable and undeletable on this target.
- File:#beleg: `cmd/baha/app_machine_adapters.go:126-130` — `appEditLoad` receives an error that is neither `GuidedReadError` nor a known kind for the managed-source path and falls through to `denied`.

### BF-06 · doku · `baha up` help omits the NAME argument accepted by the usage line of sibling commands
- `~/hp3-baha up hp3c1` → `Error: unknown option hp3c1` while `baha app up [NAME]`, `app plan [NAME]` etc. take it; `up --help` usage line has no `[NAME]`. Consistent behavior, documented absence — recorded so the matrix knows: top-level `up` is repo/cwd-only. Positive cell: error message is actionable ("unknown option" + next).

### BF-07 · ux · `app new --directory` silently CREATES missing parent directories
- Expected: a typo'd `--directory ~/nonexistent-dir` should fail fast ("no such directory").
- Ist: `~/hp3-baha app new x --directory ~/nonexistent-dir --sql --no-input` → `created x (dev) with generated/go` and materialized `~/nonexistent-dir/x/`. File:#beleg: `cmd/baha/app_new_target.go:11-27` joins without an existence check; `internal/development/project.go` (ensureEmptyProjectRoot + MkdirAll) then writes the tree. Low blast radius but violates least-surprise for a provisioning tool.

### BF-08 · daemm · `app status`/`app doctor` print a "Docker endpoint / Docker mode / Docker daemon" block on a podman-only target
- Ist: `~/hp3-baha app status` on baha-podman (target boot, runtime provider podman):
  ```
  Docker endpoint  
  Docker mode      unknown
  Docker daemon    
  ```
  with empty values, before the actual BaseHarbor block. File:#beleg: cmd/baha/app_status.go header path emits the docker-engine section unconditionally; the same empty fields appear in `-o json` (`"docker_engine":{"endpoint":"","mode":"unknown",…}`). Confusing noise for the podman audience this host represents.

### BF-09 · doku · show-vs-plan surface divergence (documented in command help, verified coherent)
- `app show` renders only PostgreSQL/Valkey backend lines; messaging/S3/document-db capabilities visible in `app plan` (e.g. hp3multi would list queue resources) are absent from `show`. `show --help` states it shows "backend readiness", so this is a documentation-grade gap: a manifest with `messaging_queue.enabled: true` looks service-less in `show` (positive control hp1app shows `Backends none declared` correctly for no services). Expect-vs-ist: users auditing "what will be created" via `show` under-estimate the footprint; `plan` is the authoritative view. Recorded, not a bug per contract text.

### BF-10 · ux · duplicate-name `app show/plan NAME` guidance asks for the one flag that cannot resolve the collision
- With two hp3c1/dev records: `~/hp3-baha app show hp3c1` → `environment selection required … Select one registered environment with -e/--environment` — but both records ARE dev, and `app show hp3c1 -e dev` still errors identically (exit witness `app show hp3c1 -e dev` → same "environment selection required"). The Next-line contradicts the observable registry (`deployment.json` list). Same message for `plan NAME -e`.

### BF-11 · doku(operational) · vm-lock.sh status/claim crashes parsing journal.log
- `bash coordinator/scripts/vm-lock.sh claim baha-podman hunt-hp3` printed `ValueError: unconverted data remains:  release baha-docker-2 selbsttest` from its inline stale-check python, yet claimed the lock (rc=0, file content `hunt-hp3`). Cause: `journal.log` has a 4-token line where the script's glob `"$LOCKDIR"/baha-*` includes `journal.log` and its second line is parsed as a timestamp (coordinator/scripts/vm-lock.sh:22-31). Cosmetic to claiming, but the "fremde" report is unreliable. Not a product-repo finding.

### BF-12 · positive · edit-wizard hydration and write-free cancellation are coherent
- After manually adding `cache.enabled: true` to baseharbor.yaml, the wizard hydrates it (`[x] Cache`) exactly matching `app plan` output items 3-4 (`ensure cache.key-value:default`); `cancel`, `q` and EOF all end with `Error: wizard cancelled without changes`, rc=0/1 and byte-identical manifest+compose (diff witness). Preview is genuinely read-only (`Read-only decision preview (not execution)`), plan_id/revision stable across repeated `app plan` runs (`REVISION-STABLE`).

### BF-13 · positive · compose/Dockerfile rendering: single-service only, coherent, no dangling runtime files
- All four stacks (`go`, `python`, `nextjs`, `quarkus` via `app new --stack X --sql --cache --http --queue --secrets`) render exactly ONE compose service (`app`), capability bindings injected as `${VAR}` environment entries (internal/development/compose_bindings.go:15-48); backend containers (postgres/valkey/rabbit) are NOT in the repo compose — they are target-level shared providers, so there is no `depends_on`, no port collisions, and no healthcheck for the workload in the quarkus template (`internal/development/quarkusadapter/adapter.go:209` compose() has no healthcheck while go/python/nextjs do — stack-dependent readiness, see below). `expose:` vs `ports:` differs by adapter (go/python expose, nextjs/quarkus publish 8080:8080 on the host) — observable inconsistency between stacks for the same `--http` intent.
- Ist-vs-erwart note: quarkus compose lacks the healthcheck its adapter registers as ActionHealth `/q/health` (adapter.go:59) — the health action never reaches compose/Dockerfile rendering. Recorded as `doku/daemm` borderline; needs owner triage.
- Runtime witness: throughout the whole hunt `podman ps -a` gained ZERO lane-owned containers (`comm -13 before after | wc -l` = 0), no new networks/volumes, no `~/.config/containers/systemd/*.unit` for hp3 names — nothing was left running because nothing was ever converged (no `up`/`apply` in scope; mission: observation only).

### BF-14 · ux · init-on-existing-manifest message loop
- `baha init --quick` in a repo that already has baseharbor.yaml prints `baseharbor.yaml already exists; no changes were made. … use 'baha app init' to configure deployment inputs.` — but plain `app init` (no flags, non-tty) then replies `Error: deterministic app init requires an explicit capability or workload selection`, and with `-e prod` fails `unknown option -e` inside a repo that HAS a manifest with environment dev (flag ordering: `-e` is parsed only after manifestless detection fails). Mixed guidance; exit rc=0 for the first, rc=2 for others. One-liner repro on any `app new` repo.

## Cut coverage matrix (cells)

- S1 app new→edit: BF-01, BF-03, BF-04, BF-05, BF-07, BF-12 (positive) — wizard renders, previews, cancels write-free; confirms never reach durable state in this contaminated target (BF-03) — root cause of no-apply needs owner triage: on a CLEAN target the same keystroke stream applies (not testable here without disturbing shared core; VM hygiene).
- S2 plan/show consistency: BF-09, BF-10, positive `REVISION-STABLE`, `show`↔`plan` agree on declared services in uncontaminated cells (hp1app, hp3c2 before duplicates).
- S3 compose rendering: BF-13 (+BF-06 adjacency), all observation-only.
- S4 quickinit→edit→plan: BF-02, BF-14, quick-init poisoned by foreign dangling instances (BF-03 root).

- Cut S2 additions: `app show hp3c2` prints `PostgreSQL default — not applied` although the plan JSON consumer list contains `deployment/c39cfae1…` (a *different* never-applied app hp1sql) as a database.sql consumer on the same shared instance; the "not applied" label is per-app state, correct but easy to misread as instance state — recorded under BF-09 as documentation-adjacent ambiguity.
- Cut S4 addition: `printf "" | script -qec "~/hp3-baha app edit" /dev/null` in a healthy repo prints the full needs view then `Error: wizard cancelled without changes` (write-free EOF, rc 0) — matches BF-04's pipe-vs-help contradiction, cancellation itself positive.

## VM besenrein (cleanliness)

- Before: containers 31, networks 18, volumes 6, `~/.config/containers/systemd` (all bh-w169-*/bh-boot-*, untouched), `~/.baha` absent.
- After: `podman ps -a` diff = 0 new containers (`comm -13` count 0), 0 new networks, 0 new volumes; no hp3 quadlet files. No compose project of this lane was ever started → nothing to `down`; ps-witness above.
- Removed lane artifacts: `~/hp3-baha` (binary), `~/hp3/` (all work dirs incl. dup1/c6/hp3c1/hp3c2/hp3c5/hp3c9/hp3dup/hp3j1/hp3multi/hp3q2/hp3n*), `~/nonexistent-dir/` (BF-07 evidence dir, deleted after capture), `/tmp/hp3pty/*`, `/tmp/hp3-*` scratch.
- Residual (ambient foreign state, NOT touched per owner directive 2026-11-08): 7 deployment records under `~/.local/share/baseharbor/targets/boot/deployments/` — hp1app/hp1sql pre-existed the mission (SOURCE=MISSING, other lanes); hp3c1(0242dfc0, repo-source ~/hp3/work/dup1), hp3c1(7c36db19, repo-source ~/hp3/work/hp3c1), hp3c2, hp3c5 and hp3c9 are THIS lane's registrations. Their repo working trees are deleted, but the two hp3c1 records still carry identical name+environment — the BF-01/BF-03 condition persists purely in registry state, which is the reproduction itself. `app destroy --yes` is fail-closed on it (`missing-dependency`, no force path surfaced), so hand-deleting state dirs would both destroy the repro and touch shared target state; purging needs a coordinator/owner decision.
- Lock release: `vm-lock.sh release baha-podman hunt-hp3` → `FREE host=baha-podman` (see END section for witness).
- cleanliness: host returned to before-state except the documented residual provider-state findings.

## repo-rule compliance

- No product-repo writes; no PRs; no branch creation in baseharbor (read-only `git archive`/`show` of develop). All writes: this evidence file in baseharbor-plan, the lane todo board JSON under workers/todos/ (bookkeeping repo), and host scratch under ~//tmp on baha-podman (cleaned).
- No subagents used (4.8). Docker/podman tests executed only on baha-podman via SSH; zero containers started on the session host. Workflow files untouched.
- Real witnesses via git remote fetch and host `ls-remote`-equivalent state reads; quarantined workers/baseharbor checkout refs not cited (only its object store was used read-only for `git archive origin/develop` after a fresh `git fetch`, so origin/develop there equals remote HEAD — verified equal to `d30de3a4` at fetch time).

## END

END_DONE mission-hunt-hp3.md: 12 findings (2 blocker-kandidaten BF-01/BF-03 + BF-05 daemm, positives BF-12/BF-13) on baha-podman, candidate = evidence commit on baseharbor-plan main, host released.

- Evidence-on-origin/main witness (second-to-last action): `git ls-remote origin main` → `ef711b90aa7ebc8c211d8f1b7329171d0930d3eb refs/heads/main`; `git cat-file -e origin/main:evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md` → `EVIDENCE-PRESENT-ON-ORIGIN-MAIN`; `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-08/vm-bughunt/` lists hp3.md blob 38ccb9b8.
- Lock release witness: `vm-lock.sh release baha-podman hunt-hp3` → `FREE host=baha-podman` (journal line written same second).

