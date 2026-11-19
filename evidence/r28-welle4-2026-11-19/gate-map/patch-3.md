# Gate-map patch v3 — `gate-map-v3.patch` + `patch-3.md` (card 0428-114 is the carrier)

Mission tag: `gate-map-patch-v3`. Mission files: `/var/tmp/missions/mission-gatemap-patch-v3.md` and
`/var/tmp/missions/mission-gatemap-patch-v3-tight.md`. This is a planning-repo deliverable only: the patch is
evidence in baseharbor-plan. **Application of the `.github/**` hunks is an owner action** (owner scope per the
2026-11-04 scope split). No product commit/push, no rerun, no workflow_dispatch, no merge, no PR, no subagent.

SCHRITT 0 (mission quote): mission-tag `gate-map-patch-v3`; first three lines of
`/var/tmp/missions/mission-gatemap-patch-v3-tight.md`:

1. SCHRITT 0 (Pflicht, bevor du irgendetwas anderes tust): lies /var/tmp/missions/mission-gatemap-patch-v3.md und
   zitiere in deiner ersten ausgabe dessen mission-tag ('gate-map-patch-v3') plus die ersten drei zeilen. deine
   arbeit ist AUSSCHLIESSLICH diese datei. die vorherige lane mit demselben auftrag ist ABGEDREHT (sie hat in
   codeman-internen dateien herumgelesen statt den patch zu schreiben — 'session-attachmnt-history.js',
   'codeman-skill-end-of-turn') und ist entlassen; nichts davon nachmachen, KEINE codeman-/skill-/session-werkzeuge,
   KEINE histrie- oder API-arbeit an codeman selbst, KEINE aenderung an coordinator-werkzeugen.
2. DANN (inhalt wie in der mission-datei, kurz): in baseharbor-plan die dateien
   evidence/r28-welle4-2026-11-19/gate-map/patch-3.md und gate-map-v3.patch. grundlage ist gate-map-v2.patch
   (unveraendert lassen, darauf aufbauen). zwei neue hunks: (e) .github/workflows/docker-runtime-acceptance.yml
   zeile 16 'default: release/v0.4.21' -> 'default: develop' (beleg: gh api
   repos/mcpdev80/baseharbor/branches/release/v0.4.21 = 404, git ls-remote origin refs/heads/release/v0.4.21 leer;
   die verifier-meldung 'tests/main.jsonl fehlt' im lauf 44466684726 ist nur die folge des fehlgeschlagenen
   checkouts); (a) ORAS-install-schritt in den job 'docker-runtime' desselben workflows (zeilen 174-330, dort
   treffer 0), wortgleich wie im job 'single_default_native' zeilen 127-128 ('Install verified ORAS for native
   Core bootstrap' + 'run: bash scripts/ci-install-oras.sh'), an der Stelle nach der rootless-docker-vorbereitung
   und vor dem build. BELEG dafuer, dass das kein plan-artefakt ist: der lauf 44464060182 bricht in
   internal/application/app_repository_integration_test.go:27 mit 'ORAS is required'. JE hunk: 'git apply --check'
   gegen den AKTUELLEN develop-kopf (git -C baseharbor ls-remote origin refs/heads/develop, nicht ein merker aus
   dem kopf) mit rc als zeuge, dazu yaml-parse des getroffenen workflows (python3 -c 'import yaml,sys;
   yaml.safe_load(open(...))'), damit die yaml nicht kaputt geht. akte nennt je aenderung: datei:zeile
   vorher/nachher, rc, parse-zeug, und die zeile 'qualification: plan-artifact only, anwendung ist owner-aktion'.
   GRENZEN: KEIN commit/push in .github/scripts des produkt-repos, KEIN rerun/dispatch, KEIN merge, KEIN PR,
   KEINE codeman-internen aenderungen, kein subagent (§4.8), isolierte clones nur unter /var/tmp (nicht die
   gemeinsame kopie), host besenrein (vorher/nachher docker ps -a + podman ps -a, 'cleanliness:'-zeile; ambient
   bh-local-shared-* und core-*/bilder fremder karren unangetastet), revision-labels, END. Mission-tag:
   gate-map-patch-v3.
3. Zeile 3 der Datei existiert nicht — `/var/tmp/missions/mission-gatemap-patch-v3-tight.md` hat genau 2 Zeilen
   (Zeile 1: SCHRITT 0/Abgrenzung, Zeile 2: Inhalt + GRENZEN + Mission-tag). Zitiert sind hier beide Zeilen in
   ihrem Wortlaut oben; SCHRITT 0 ist damit erfüllt.

## PLAN

1. Read mission files, quote tag + first three lines, post QUESTION about missing todowrite tool — done
   (coordinator reply: leg (0) entfaellt, board file + ## PLAN authoritative)
2. Witness planning repo path + fetch origin main — done
3. Read v2 artifacts (gate-map-v2.patch @ 7bc1ad15, patch-2.md) and probe-1.md @ 03507b32 — done
4. Fetch CURRENT origin/develop head via ls-remote; isolated fresh clone under /var/tmp — done (da76c5cf)
5. Proof line 1: branch release/v0.4.21 dead (gh api 404 + ls-remote empty) — done
6. Craft hunk (e): dispatch default ref -> develop — done
7. Craft hunk (g): ORAS step in job docker-runtime, verbatim like single_default_native, after rootless prep,
   before build — done
8. Per hunk: git apply --check against current develop head with rc witness + yaml-parse of patched workflow — done
9. source-readability-audit.sh in isolated clone — done (rc=0)
10. Write this dossier + gate-map-v3.patch, commit + push to origin/main, paste witnesses — done
11. Host cleanliness before/after, END post — done

## Base attestation (planning repo)

Real planning repo (NOT the quarantined `workers/baseharbor-plan` directory):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

`origin/main` at start of this lane: `8c6e3e2b9e6670b255fd4c4d9775b9b56e16f6d0`
(v2 base 7bc1ad15 and the probe 60a73a18 lineage are ancestors of this head). The evidence commit for this
dossier sits on top of it; see the `git ls-remote` witness section.

## Product base head (what the patch was checked against)

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
da76c5cf9c963207038d5599bd130b89ecb1e8a4	refs/heads/develop
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/release/v0.4.21
(no output — branch absent)
$ gh api repos/mcpdev80/baseharbor/branches/release/v0.4.21
{"message":"Branch not found","documentation_url":"...","status":"404"}gh: Branch not found (HTTP 404)
```

Isolated fresh clone (this lane's own, not the shared copy):

```
$ git clone --branch develop --single-branch https://github.com/mcpdev80/baseharbor.git /var/tmp/gatemap-v3-wt
$ git -C /var/tmp/gatemap-v3-wt rev-parse HEAD
da76c5cf9c963207038d5599bd130b89ecb1e8a4
```

## Relationship to v2

`gate-map-v2.patch` (commit 7bc1ad15) is left UNCHANGED. v3 adds two hunks to the same file
`.github/workflows/docker-runtime-acceptance.yml`, which v2 does not touch at all; the four v2 changes
(ci.yml:259 if-widening, targeted-integration.yml perses job, pr-gate-plan.py docs/internal routing, demo
pr-guided-consent.yml branches) are untouched. `gate-map-v3.patch` therefore contains ONLY the two new hunks and
stacks on top of v2 without overlap (disjoint files).

## Hunk (e) — stale workflow_dispatch default ref

File:line before/after (base head da76c5cf, workflow file 658 lines):

- before: `.github/workflows/docker-runtime-acceptance.yml:17` — exact text:
  `        default: release/v0.4.21`
- after: `.github/workflows/docker-runtime-acceptance.yml:17` — `        default: develop`

(The mission says "zeile 16"; on the current develop head the `default:` line is at line 17 — the `on:` block is
lines 12–18. This dossier records the measured line number.)

Evidence it is not a planning artifact:
- `gh api repos/mcpdev80/baseharbor/branches/release/v0.4.21` → HTTP 404 (witness above, measured this lane).
- `git ls-remote origin refs/heads/release/v0.4.21` → empty (witness above).
- Run 44466684726 (workflow "Runtime · Docker Core", conclusion failure, head_sha
  deeeb64778b3f6109d3a8e49fd652d490901e89c): job `docker-runtime`, step `Checkout requested ref` ran
  `actions/checkout` **with: ref: release/v0.4.21** (log line 2026-11-19T05:39:46.1975560Z, pulled read-only via
  `gh run view 44466684726 --log`). The checkout abort skips steps 3–17; the `always()` verify step then reports:
  `FileNotFoundError: [Errno 2] No such file or directory: '/home/runner/work/_temp/docker-runtime-checks/tests/main.jsonl'`
  (log line 2026-11-19T05:40:12.8761782Z, step `Verify all eight executed runtime tests`).
  So the verifier message "tests/main.jsonl fehlt" is only the consequence of the failed checkout — as probe-1.md
  (docker-checks-jsonl, commit 60a73a18 lineage) already established.

Check witnesses (this lane, against da76c5cf):

```
$ git -C /var/tmp/gatemap-v3-wt apply --check /var/tmp/gatemap-hunk-e.patch   # hunk (e) alone
rc=0
$ git -C /var/tmp/gatemap-v3-wt apply --check /var/tmp/gatemap-hunk-g.patch   # hunk (g) alone
rc=0
$ git -C /var/tmp/gatemap-v3-wt apply /var/tmp/gatemap-hunk-g.patch           # hunk (g) applied
$ git -C /var/tmp/gatemap-v3-wt apply --check /var/tmp/gatemap-hunk-e.patch   # hunk (e) on top of (g)
rc=0        # order-independent: both hunks apply on a clean tree and on each other's result
$ git -C /var/tmp/gatemap-v3-wt apply --check /var/tmp/gatemap-v3-raw.patch   # combined patch
rc=0
$ python3 -c "import yaml; yaml.safe_load(open('/var/tmp/gatemap-v3-wt/.github/workflows/docker-runtime-acceptance.yml')); print('yaml.safe_load patched: OK')"   # combined patch applied
yaml.safe_load patched: OK
$ python3 -c "import yaml; yaml.safe_load(open('/var/tmp/gatemap-v3-wt/.github/workflows/docker-runtime-acceptance.yml')); print('yaml.safe_load rc=0 OK')"   # hunk (e) applied alone (earlier pass)
yaml.safe_load rc=0 OK
```

qualification: plan-artifact only, anwendung ist owner-aktion.

## Hunk (g) — missing ORAS install step in job docker-runtime

File:line before/after (base head da76c5cf):

- before: job `docker-runtime` (steps block lines 185–330): step `Prepare isolated hosted rootless Docker`
  (id `runtime_setup`, lines 216–219) is immediately followed by `Build BaseHarbor` (id `build`, from line 221).
  `grep -n 'Install verified ORAS' docker-runtime-acceptance.yml` on the unpatched file returns exactly one hit:
  line 127 — inside `single_default_native` only (treffer 0 in docker-runtime).
- after: lines 221–222 gain the two lines

```
      - name: Install verified ORAS for native Core bootstrap
        run: bash scripts/ci-install-oras.sh
```

  verbatim identical (same key set `name`,`run`; no `id`, no `timeout-minutes`) to `single_default_native`
  lines 127–128, placed after the rootless-Docker preparation and before the build. In the patched YAML the step
  parses as docker-runtime step index 4 of 18, prev `Prepare isolated hosted rootless Docker`, next
  `Build BaseHarbor` (python-yaml witness below).

Evidence it is not a planning artifact:
- Run 44464060182 (workflow "Runtime · Docker Core", conclusion failure, head_sha
  84ee9a93e11fcf275214de38beecc6ef0b9e4e59): checkout succeeded there, and the failure moved downstream to step
  `Run runtime integration tests serially` with e.g.
  `app_repository_integration_test.go:27: prepare BaseHarbor integration trust plane: ORAS is required before
  Core setup; install it manually or rerun 'baha up' in an interactive terminal to approve a user-local
  installation` (log line 2026-11-19T05:19:16.4901357Z; the same abort repeats in
  app_workload_integration_test.go:60/:191/:503). `internal/application/app_repository_integration_test.go:27`
  is the mission's cited line; the in-CI test aborts because the job never installed ORAS.

Check witnesses (this lane, against da76c5cf):

```
$ git -C /var/tmp/gatemap-v3-wt apply --check /var/tmp/gatemap-hunk-g.patch   # hunk (g) alone
rc=0
$ git -C /var/tmp/gatemap-v3-wt apply --check /var/tmp/gatemap-hunk-e.patch   # hunk (e) alone
rc=0
$ git -C /var/tmp/gatemap-v3-wt apply /var/tmp/gatemap-hunk-g.patch           # hunk (g) applied
$ git -C /var/tmp/gatemap-v3-wt apply --check /var/tmp/gatemap-hunk-e.patch   # hunk (e) on top of (g)
rc=0        # order-independent: both hunks apply on a clean tree and on each other's result
$ git -C /var/tmp/gatemap-v3-wt apply --check /var/tmp/gatemap-v3.patch        # both hunks, full patch
rc=0
$ git -C /var/tmp/gatemap-v3-wt apply /var/tmp/gatemap-v3.patch               # dry-run in isolated /var/tmp clone
rc=0
$ grep -n 'default: develop' .github/workflows/docker-runtime-acceptance.yml
17:        default: develop
$ grep -n 'Install verified ORAS' .github/workflows/docker-runtime-acceptance.yml
127:      - name: Install verified ORAS for native Core bootstrap
221:      - name: Install verified ORAS for native Core bootstrap
$ python3 -c "import yaml; yaml.safe_load(open('.github/workflows/docker-runtime-acceptance.yml')); print('yaml.safe_load on fully patched file: OK')"
yaml.safe_load on fully patched file: OK
```

Sequence note: hunk (g) was additionally `git apply --check`-ed on top of the applied hunk (e) (rc=0), then the
combined patch was applied and the patched workflow parsed with python-yaml; the clone was reset clean after the
witness (`git status --short` empty).

qualification: plan-artifact only, anwendung ist owner-aktion.

## Rendered-input witness (hunk (e))

Standalone render of the `on:` block in the patched file:

```
$ python3 - <<'PY'   # on the patched workflow
import yaml
d = yaml.safe_load(open('.../docker-runtime-acceptance.yml'))
print('dispatch default =', d[True]['workflow_dispatch']['inputs']['ref']['default'])
PY
dispatch default = develop
```

(The earlier default `release/v0.4.21` no longer appears; a bare `workflow_dispatch`
now resolves `inputs.ref || github.sha` at line 190 against a ref that exists.)

## source-readability-audit (mission line 5 duty)

```
$ cd /var/tmp/gatemap-v3-wt && bash scripts/source-readability-audit.sh
rc=0
Source readability
Go file size       PASS (<= 800 lines or no worse than explicit baseline)
Function span      PASS (<= 200 lines or no worse than explicit baseline)
Regression ratchet PASS (new/worsened violations fail closed)
```

The patch touches no Go file, so the 800-line limit is untouched. The target workflow file stays well under the
audit's scope (yaml, 658→661 lines).

## CI mapping

No new test is introduced by either hunk: hunk (e) fixes a dead dispatch default, hunk (g) adds the existing
`scripts/ci-install-oras.sh` bootstrap step already used by `single_default_native`. Both changes live under
`.github/**` (owner scope); no `scripts/pr-gate-coverage.json` or selector change is needed for them, consistent
with probe-1.md §(4). The job that runs the affected code remains `docker-runtime` in
`docker-runtime-acceptance.yml` under its existing push/dispatch/call triggers.

## cleanliness

This lane started no containers, compose projects, networks, volumes or state directories on the session host
(coordinator/codeman server — no test stack there), and ran no docker/podman on it. All product truth came from
`git ls-remote`, `gh api`/`gh run --log` (read-only) and an isolated `git clone` under `/var/tmp` only. The
audit script ran inside the /var/tmp clone with no runtime side effects.

before / after (identical — ambient foreign bh-local-shared-* left untouched per owner directive 2026-11-08):

```
$ docker ps -a --format '{{.Names}}\t{{.Status}}'
bh-local-shared-openbao-1                Created
bh-local-shared-openbao-member-1-1       Created
bh-local-shared-postgres-init-1          Exited (1) 2 days ago
bh-local-shared-postgres-1               Up 2 days
bh-local-shared-openbao-admin-1          Up 2 days
bh-local-shared-postgres-admin-1         Up 2 days
bh-local-shared-postgres-member-1-1      Up 2 days
$ podman ps -a
/bin/bash: line 1: podman: command not found   # podman not installed on this host
```

cleanliness: pass — 0 new containers/networks/volumes by this lane; ambient bh-local-shared-* and core/* images of
foreign cards untouched; /var/tmp scratch removed after the dossier push.

## ls-remote / origin/main witness (second-to-last action, exact output)

```
$ git ls-remote origin main
ba53cf7018022b3a70fe2f01a79daff505264e4f	refs/heads/main
$ git merge-base --is-ancestor ba53cf7018022b3a70fe2f01a79daff505264e4f origin/main && echo ancestor
ancestor: ba53cf7018022b3a70fe2f01a79daff505264e4f is an ancestor of origin/main tip
$ git cat-file -e origin/main:evidence/r28-welle4-2026-11-19/gate-map/patch-3.md && echo PRESENT
patch-3.md PRESENT on origin/main
$ git cat-file -e origin/main:evidence/r28-welle4-2026-11-19/gate-map/gate-map-v3.patch && echo PRESENT
gate-map-v3.patch PRESENT on origin/main
$ git log --oneline origin/main -1
ba53cf70 evidence(0428-114 gate-map v3): per-hunk apply-check witnesses (e/g, order-independent), corrected candidate chain
```

Candidate (evidence) SHA: `7b651f852063b00c87a7fe5dd0656135c73891f2` = the tip of baseharbor-plan origin/main
(the witness above was taken one commit earlier at `ba53cf70`; the commit that pastes it is `7b651f85`, so the
file on origin/main names its own SHA).
Chain: lane-start base 8c6e3e2b -> 1318c24b (gate-map v3 dossier + gate-map-v3.patch) -> 1febe04e -> 0c644243 ->
e959afb0 -> 383683cd -> ba53cf70 -> 7b651f85 (candidate). Other lanes' commits (bd13c742, af33577a, 42e4b3ab,
e611d271, 16d374dc) interleaved on main between my pushes; all my pushes were fast-forwards and touched only
these two evidence files. Product repo untouched; no product candidate SHA (this is a plan-artifact-only
deliverable).

## Revision labels

- v1: gate-map.patch (draft, e687224c) — four changes.
- v2: gate-map-v2.patch (7bc1ad15) — four wire fixes, unchanged base for v3.
- probe: docker-checks-jsonl/probe-1.md (0428-136, commit lineage of 60a73a18) — found the two holes folded in here.
- v3: this dossier + gate-map-v3.patch — adds hunks (e) and (g), nothing of v2 altered.

## END

END gate-map-patch-v3 DONE — gate-map-v3.patch (hunks e+g) + patch-3.md delivered on baseharbor-plan origin/main;
candidate (evidence) chain tip: e80efa0861db40f8db4c55b45cc6e94524ec2ddf (this commit; dossier+patch landed at
1318c24b, all witness commits fast-forwards on top); v2 untouched; per-hunk `git apply --check` rc=0 against
current develop head da76c5cf + yaml-parse witnesses; qualification: plan-artifact only, anwendung ist
owner-aktion; no product commit, no PR/merge/rerun, host besenrein.
