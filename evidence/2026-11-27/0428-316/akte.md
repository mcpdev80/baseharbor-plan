# Lane akte 0428-316 — hunt43 env-leak-to-disk (lane w396-0428-306-goldenhelp)

## PLAN (numbered, mirrors the board file workers/todos/w396-0428-306-goldenhelp.json)

1. Read mission + card 0428-316 (t-20261125-hunt43-env-leak-disk) + H-V43 hunt akte (w331 findings). DONE.
2. Claim 0428-316 via scripts/plan.py claim in an isolated plan worktree, render+check 0 errors, forward-only push to plan main. DONE (main 02395f708).
3. Base attestation for the product branch: ls-remote develop, ancestry proof, log-line proof.
4. Implement the smallest sufficient fix for FUND-A (podman quadlet ambient-env materialisation into the plaintext service .env): a narrow name-based suppression so a secret-bearing ambient value substituted into a rendered env literal is not written verbatim to disk; consent/auth semantics untouched; no .github edits; no new CI check entries.
5. Add regression tests in the affected package (auto-discovered by existing PR Go unit shards; CI-Aufnahmepflicht without new registrations).
6. Local pre-checks: gofmt/vet/build only.
7. Branch + commits under canonical lane identity, PR vs develop (draft until gate complete), transport via git merge origin/develop + normal push.
8. Two distinct executed run IDs on the exact head in Hosted CI (pair via authorized close+reopen if needed), monitored to terminal state by this lane.
9. Evidence akte published on plan main under evidence/2026-11-27/0428-316/, ls-tree origin/main witness, sha256.
10. Handoff: card to review (PR + exact head + run IDs + akte), END line to coordinator.

## Identity block (visible Ansatz block, owner admission rule)

- Card frontmatter owner VERBATIM after claim: `owner: "w396-0428-306-goldenhelp"` (lane w396-0428-306-goldenhelp; mission file header registers this lane; card 306 recommendation wait does not revoke the commission).
- git user.name: w396-0428-306-goldenhelp
- git user.email: w396-0428-306-goldenhelp@baseharbor.local
- Literal invocation: `git -c user.name=w396-0428-306-goldenhelp -c user.email=w396-0428-306-goldenhelp@baseharbor.local commit ...` (also for every merge commit).
- Pre-push gate line: `git show -s --format=%an HEAD` must print `w396-0428-306-goldenhelp` exactly before every push; on mismatch STOP + report.

## Remote / zone witnesses

- Planning repo: git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v → origin https://github.com/mcpdev80/baseharbor-plan.git (isolated worktree workers/w396-0428-316-plan used for all plan writes; no reset/stash/add-A in the shared checkout).
- Product remotes in shared worktree ../w396-0428-306-wt: origin may be a local path (quarantined); all product git ops use the URL https://github.com/mcpdev80/baseharbor.git (remote lane-origin), resolved to github.com/mcpdev80 before any op.

## Base attestation (product)

- git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop → (to record)
- Branch cut from that exact SHA; `git merge-base --is-ancestor <sha> HEAD` proof and `git log --oneline origin/develop..HEAD` listing ONLY lane commits to be recorded here before PR.

## Scope decision (finding-first, per mission line 4)

H-V43 akte (w331) recorded three findings. FUND-A is the disk leak the card names ("Umweltvariablen-Leak auf Speicher"): the podman quadlet renderer substitutes ${VAR} from the FULL ambient environment and writes the substituted value verbatim into `{project}-{service}.env` under ~/.config/containers/systemd (plaintext file). FUND-B (docker compose container env) and FUND-C (executor image validation) are already covered by card 0428-318 / PR #1862 (lane-0428-318-lowpair, "guard executor image + S3 admin file") — out of this card's scope to avoid duplicate chains. Smallest sufficient fix here: on the quadlet render path, when a service environment value is produced by ambient substitution, do not materialise the resolved secret text into the on-disk .env; instead keep the `${VAR}` reference so podman/systemd resolves it from the unit-level EnvironmentHost/ambient contract, or fail closed with a clear error when the reference cannot be preserved. Auth/consent semantics and file permissions untouched.

## Implementation log

- Branch lane-0428-316-envleak-disk cut from the exact develop head ea5218d72e263f21e79853b679af50074dab8c25 (ls-remote witness above; merge-base --is-ancestor ANCESTOR_OK; git log --oneline origin/develop..HEAD lists only lane commits).
- Fix (FUND-A disk sink), internal/providers/runtime/podman:
  - quadlet_render.go: quadletLoadComposeModel now keeps an unaliased source clone of every Compose document, and after the ambient ${VAR} expansion pass runs quadletRestoreAmbientEnvironmentRefs dematerialises, in every service `environment` block (mapping and sequence form), each entry whose SOURCE was exactly one ${NAME} reference that only the ambient process environment defines. The expanded plaintext is replaced by the original reference, so the on-disk {project}-{service}.env contains the reference, never the operator secret; podman/systemd resolves it from the unit process environment at service start.
  - Declared-scope protection: names provided by the project envFile or the explicit managed environment layer stay resolved exactly as before (byte-for-byte), so managed runtime contracts (e.g. DB_PASSWORD via runtime.env in TestRenderComposeProjectQuadletsMapsManagedRuntimeSemantics) are unchanged.
  - quadlet_project.go: cloneQuadletYAMLNode previously aliased child Content slices; every "clone" silently mutated together with the original (yaml.Node.Content is a shared slice). Now it deep-copies Content. This aliasing is the reason the H-V43 materialisation existed and also why an earlier restore attempt no-op'd.
  - No .github/** edits; no new CI check entries.
- Tests (same package internal/providers/runtime/podman, existing CI group PR · Go unit shards + package discovery; catalog already resolves all four changed paths to atomic/podman/lifecycle via BASE rows — verified against the base controller planner, zero unresolved sources):
  - TestRenderComposeProjectQuadletsKeepsAmbientSecretOutOfEnvFile (mapping form: bare reference not materialised; WriteQuadletProject disk witness; literals and ${MISSING:-fallback} defaults unchanged).
  - TestComposeEnvSequenceFormKeepsAmbientReference (sequence KEY=${VAR} form).
  - TestQuadletSingleAmbientReferencePinsTheRestoreFilter (reference detection: literal, embedded-mix, undefined-name all pass through).
- Local pre-checks: gofmt clean, go vet ./internal/providers/runtime/podman OK, go build ./... OK. Named-form focused runs of the package's quadlet render tests only (no RunsRealLifecycle cases) to validate before push; qualification comes from Hosted CI.


## Hosted CI (self-run duty)

(to be appended: two distinct run IDs on exact head + terminal status)

## cleanliness

(to be appended; no containers/compose projects are started by this lane — unit-scope work only; docker/podman native gates run in Hosted CI)

## END

(to be appended: END_DONE / END_BLOCKED w396-0428-306-goldenhelp: <one line + candidate SHA>)

## Runtime semantics witnesses (local probes, non-qualifying)

- `podman create --env-file` with `KEY=${VAR}`: the container receives the raw reference text, with or without the ambient variable set in the process environment (probes 2026-11-27, containers removed immediately).
- systemd `EnvironmentFile=` (systemd 259, user instance via `systemd-run --user`): `VAR_REF=${W396_SYSTEMD_AMBIENT}` with `Environment=W396_SYSTEMD_AMBIENT=resolved-by-systemd` yielded `VAR_REF=[${W396_SYSTEMD_AMBIENT}]` → systemd does NOT substitute `${VAR}` inside env files.
- Consequence: a reference must never reach the container THROUGH the env file. The fix therefore keeps ambient-sourced entries entirely OUT of the on-disk file and projects them on the unit instead (valueless `Environment=KEY`, which podman resolves from the unit process environment — the same host-environment semantics compose uses).
- Scratch cleanup: all probe containers/networks/dirs removed; `podman ps -a`/`network ls` show no w396 leftovers; `~/.config/containers/systemd` and `~/.config/systemd/user` hold no w396 files.

## Final design (replaces the interim notes above)

1. `quadletLoadComposeModel` expands against the full compose map, runs the two-stage **environment restore walk** (`quadletRestoreEnvironmentEntries` + `matchingChildValue`) so every service-environment scalar the AMBIENT stage alone resolved returns to its `${NAME}` reference (or `:-` fallback text) in the rendered document; `project` = envFile + managed names so declared names stay resolved.
2. A quadlet-only `quadletComposeEnv` decoder (consumer boundary) resolves ambient references for one-off consumers (`quadletExpandAmbientOnlyReferences`); the shared `composeEnv` (JSON surface) stays original.
3. `quadletRenderServiceEnvironment` keeps whole-value ambient entries out of the `.env` file and records them in `QuadletProject.AmbientEnvironment`; the unit emits valueless `Environment="KEY"` lines.
4. Mixed text (`prefix-${SECRET}`) keeps the established file projection (accepted limitation; the H-V43 FUND-A shape is the bare reference form).
5. `cloneQuadletYAMLNode` deep-copies `Content` (fixes latent aliasing).

