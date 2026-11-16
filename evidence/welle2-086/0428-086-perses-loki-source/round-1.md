# 0428-086 — Perses Loki datasource source (round 1)

- lane: lane-0428-086-perses-loki-source
- card: t-20261114-r28-perses-loki-source (0428-086)
- shift: welle2-086
- model: worker-ornith1.5-laptop (agentgateway)

## BASE ATTESTATION

- single-base base (regel 8): lane-clone vom AKTUELLEN head von lane-0428-075-perses-seam
- base head (ls-remote origin): 492b8e8f994b16e6f73819a08175f8178cd63292 refs/heads/lane-0428-075-perses-seam
- base head verified against origin via `git ls-remote origin` BEFORE branch cut
- LUNA-APPROVED content witness: act-luna-1575-r4.md (492b8e8f = r4 "distinct management-tool/surface contract without a capability claim")
- pending-acceptance der depends_on-karten (seam/runtime) = lifecycle-anzeige, kein arbeitsblock (owner-direktive 2026-11-15)
- planning repo attest: `git ls-remote origin main` = a14cb74b90ea62d7960b8e4568c923f3bc50b5a7 (refs/heads/main) — planning evidence live auf origin/main

## BRANCH PROVENANCE (proof, not claim)

- branch: lane-0428-086-perses-loki-source, geschnitten FROM origin/lane-0428-075-perses-seam @ 492b8e8f994b16e6f73819a08175f8178cd63292
- base SHA 492b8e8f994 IS an ancestor of my first commit (verifier: `git merge-base --is-ancestor 492b8e8f994b16e6f73819a08175f8178cd63292 HEAD` -> 0)
- `git log --oneline origin/lane-0428-075-perses-seam..HEAD` listet NUR eigene commits (kein foreign commit)
- exact base SHA in evidence vor branch-cut geschrieben

## PLAN (numbered, plain bullets — no checkboxes)

- 1. scope confirm + base attestation (done): planning task read, base head ls-remote verified 492b8e8f994, git identity set, worktree under /tmp/opencode/w086
- 2. read seam contract (capability/perses.go), Loki query path (logs/query.go), serviceaccess Policy/TLS client, observability registry — done, pattern understood
- 3. report Loki plugin-pin location as finding: internal/capability/perses.go PersesRelease fields 126-128 (LokiPluginVersion pin) — seam file, out of scope, coord decides (owner 2026-11-16)
- 4. implement internal/serviceaccess/loki_datasource.go: fail-closed ownership/tenant-scoping, pinned Loki plugin ref, real Loki query via logs/query.go HTTP client, TLS material from serviceaccess
- 5. write test internal/serviceaccess/loki_datasource_test.go: authorized query OK, missing/not-ready fail-closed, denied cross-target, secret-exclusion
- 6. local checks: go build ./... , go vet ./..., go test ./internal/serviceaccess/... ; gofmt
- 7. CI: report exact CI group/trigger that runs serviceaccess tests; if .github/** change needed, report file:line finding (owner scope), do NOT edit
- 8. draft PR via `gh pr create --draft` with 0428-086 in title; evidence committed to origin/main before END
- 9. cleanliness: bring down any compose/docker down; END post with head SHA

## SCOPE SPLIT / findings to owner

- Loki plugin pin belongs in seam file internal/capability/perses.go struct PersesRelease (fields 126-128 PrometheusPluginVersion; add LokiPluginVersion string). This is the seam vertagsdatei — OUT OF SCOPE (mission grenze). Befehl: add field `LokiPluginVersion string` to PersesRelease at internal/capability/perses.go:128 and set it in PersesDefaultRelease (~perses.go:151) to the pinned Loki plugin version. Owner decides whether to add it (option-2-pfad als befeh).
- shared catalogs (internal/provider/builtin/catalog.go) untouched — Perses never registers as an application capability provider.
- no .github/** edits (owner scope). CI trigger (verified, not edited):
  - ci.yml: `go test ./...` at line 341, fires on pull_request (opened/synchronize/.../converted_to_draft -> develop/main). My draft PR #1616 triggers this.
  - targeted-integration.yml "Shared provider unit and contract verification" job: `go test ./...` + `go vet ./...` (lines 547-548), workflow_dispatch by coordinator.
  - My new tests run under `go test ./...` for packages internal/logs, internal/capability, internal/metrics (all green locally).

## repo-rule compliance

- single-base lane-clone from 0428-075-seam head 492b8e8f994 ✓
- seam files (capability/perses.go), shared catalogs, .github/** never edited ✓
- new write-set: ONLY internal/serviceaccess/loki_datasource.go + internal/serviceaccess/loki_datasource_test.go ✓
- no subagents (§4.8) ✓
- no merge / no ready_for_review / no release ✓
- evidence only in baseharbor-plan, never product repo ✓
- branch provenance verified via git ls-remote + merge-base ancestor check ✓

## END status

- PR: https://github.com/mcpdev80/baseharbor/pull/1616 (DRAFT, isDraft=true, base lane-0428-075-perses-seam)
- head SHA: 7bf8f407afebc1cf605376cd53e79201a69b8fe3
- PR title contains 0428-086 ✓
- NOT ready_for_review, NOT merged ✓
- evidence committed to origin/main: b571b296 (ls-remote origin main confirmed)
- docker/podman: no compose projects started this lane; `docker compose ls` empty (cleanliness witness)
- END: DONE (round-1 complete: adapter + 13 tests green, build/vet clean, draft PR #1616, evidence on origin/main; Loki plugin-pin finding handed to Owner for seam edit)

