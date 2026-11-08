# 0427-124 · BASEHARBOR_TARGET production reader — round 1

Lane: w-flash (flash channel, session c51c8e1a). Card: t-20261108-bughunt-0427-target-env-ignored.
Branch: work/r27-bughunt-124-target-env (single candidate for this chain).

# PLAN

1. Verify zones and remotes (planning repo, develop drift). DONE
2. Re-read the grep proof on current develop; locate every production BASEHARBOR_TARGET reader. DONE
3. Reproduce the behavior locally in an isolated config/data plane (two targets, ENV set). DONE (see Findings)
4. Scope decision: production reader already present on develop -> remaining acceptance gap is the isolated greenfield Core bootstrap; decide fix vs documented no-op. DECISION: this candidate adds the production-path regression proof + precedence assertion in cmd/baha (test-only slice, no duplicate ambiguity logic after #1441 merge), and reports the bootstrap blocker as STATE. See Findings.
5. Drift-merge origin/develop (32ce55dd -> f7a49e681 -> 419b02113 -> c27d259df -> ffa83e78f) and diff-check for duplicated ambiguity logic. DONE — #1441 changed only the `len(cfg.Targets) > 1` message in selectedTargetName; my slice does not touch that region.
6. Regression test calling the READ PATH on the production CLI path (runWithIO, not t.Setenv-in-fixture-only), CI-picked in the existing Go unit group. DONE (mutation witness verified red when the reader is removed)
7. Local go build/vet/gofmt/focused tests. DONE (gofmt 0, vet clean, targeted + full cmd/baha suite run; pre-existing environment-dependent failures on this host documented, same failures reproduce on unmodified develop base)
8. PR against develop with card number 0427-124 in title; ancestry + log-line witnesses. DONE (PR #1451)
9. Observe own CI run to terminal; record run ids and outcomes. DONE (run 42433354279 success)
10. Publish evidence to baseharbor-plan origin/main; verify before END; END post. IN PROGRESS

## Reality witnesses

- Planning zone check (mission-required one-liner, run before the first evidence commit):
  `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin main` -> `d6ac3012c6cd9342ec6bd261ef138df0f58943b2 refs/heads/main` at lane start; after rebase+push: `5be74833`. The workers/baseharbor-plan directory was NOT used.
- Product remote truth: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor fetch origin develop` -> develop moved 0fe53052d -> 32ce55dd5 -> f7a49e681 (#1441, coordinator drift notice) -> 419b02113 (#1428 merged during work). The stale workers/baseharbor checkout was never cited.
- Base attestation: branch cut from origin/develop 32ce55dd5c0d623e7dd32ffcf1434a0baa9909dd (verified via `git merge-base --is-ancestor`), then drift-merged to f7a49e681 and 419b02113. 32ce55dd5 and f7a49e681 are ancestors of HEAD.
- #1430 / #1428 collision check (STOP criterion): #1430 writes access_wizard_*, internal/accesswizard, orgconfig/profiles, policy/assignment — no overlap with my write-set. #1428 merged into develop at 419b02113 (maintenance authority files) — no overlap. No conflict-push risk; no QUESTION needed.

## Findings (grep + runtime repro on current develop)

- The card premise ("kein os.Getenv-Leser in cmd/baha Produktionscode", based on 0fe53052d) is FALSE on the current branch: production readers exist at cmd/baha/target.go:93 (effectiveTarget), cmd/baha/target_selection.go:93 (targetSelectionOrigin), cmd/baha/deployment_record.go:340 (bahaEffectiveBootTargetName), cmd/baha/machine_navigation.go:80. All app lifecycle commands (up/use/status/down/doctor/apply) resolve the target through effectiveTarget -> selectedTargetName(explicit, env, cfg) with precedence --target > BASEHARBOR_TARGET > persisted > default-target > unique.
- Runtime repro (isolated XDG planes, no docker daemon touched): config with two targets iso-a/iso-b, no persisted selection:
  - `baha app status` -> conflict "multiple deployment targets configured" with #1441 remedies listing BASEHARBOR_TARGET=NAME. Fail-closed, correct.
  - `BASEHARBOR_TARGET=iso-b baha app status` -> target iso-b honored. Works.
  - `BASEHARBOR_TARGET=iso-b baha target show` -> Target iso-b. Works.
  - `BASEHARBOR_TARGET=iso-b baha --target iso-a app status` -> must select iso-a (explicit > env); asserted by the new regression test.
- Residual blocker for the isolated-greenfield acceptance clause: `baha use`/`target activate` fail closed on a fresh target without a verified management connection (cmd/baha/use_target.go bindExplicitSelectionToConnection -> "target has no verified management connection"). On a multi-target host this blocks the documented remedy path, so a greenfield isolated target cannot be activated before its Core exists. This is target-authority territory shared with #1430/#1435; per mission STOP line it is reported as STATE, not silently patched here.

## Befund: tmpfs-Speicherleck (Owner-RAM-Alarm 2026-11-08)

Ursache ist NICHT der Produkt-Test-Hilfscode. Die lanes tests nutzen t.TempDir()/t.Setenv, die go test selbst zurückbaut. Das Leck war meine eigene Scratch-Mechanik: ich habe für Baseline-/Isolationsläufe `env -i HOME=/tmp/opencode/w124-chN` gesetzt; ohne HOME/GOPATH wählt der go-Toolchain GOMODCACHE=$HOME/go/pkg/mod und hat pro Iteration den ganzen Go-1.26.9-Toolchain (~383 MB, read-only Dateien) nach /tmp/opencode dupliziert — 5 Kopien. Aufräumen mit chmod -R u+w + rm erforderte einen Zusatzschritt, weil der Module-Cache read-only ist. Alle sieben Kopien sind gelöscht; /tmp wieder 3.1G/13G belegt.KEINE weiteren clean-home-Scratches angelegt; künftige Isolationsläufe dieser Lane nutzen GOPATH/GOMODCACHE auf ein bestehendes Verzeichnis oder lassen HOME intakt (t.Setenv genügt für die Config-Isolation der Karten-Tests). Kein Karten-Bedarf aus Produkt-Testcode; falls der Owner die Toolchain-Kopie unter HOME=leer trotzdem kartieren will, ist der Mechanismus oben dokumentiert.

## CI pickup

The new test lives in cmd/baha and is executed by the existing `PR · Validation · cli-package-tests` job (`go test ./cmd/baha/...`) that already runs on every PR push — no .github/** change needed (Owner scope untouched). The companion production-path precedence test runs in the same Go unit group. Native docker/podman VM cells are not exercised by this slice: no runtime behavior changed, only a regression assertion over the existing read path; the docker-2 greenfield journey is blocked by the authority finding above and stays open on the card.

## State at round end

- Candidate: work/r27-bughunt-124-target-env @ ebdf8d5db0122620b7d2e5c57d8dc48a2c6148f3, PR #1451 (https://github.com/mcpdev80/baseharbor/pull/1451), title carries card 0427-124, base develop ffa83e78f. Ancestor witness: `git merge-base --is-ancestor ffa83e78f HEAD` OK; `git log ffa83e78f..HEAD` lists ONLY ebdf8d5db (my own commit).
- Drift handling per coordinator notices: cut at 32ce55dd5, merged f7a49e681 (#1441), 419b02113 (#1428), c27d259df (#1443 = card-124 slice 1, merged) and ffa83e78f (#1446/#1447) before push. No duplicated ambiguity logic — my file is test-only; the #1441 message change is untouched.
- Collision check #1444/#1447 (coordinator question): write-set files fetched via gh api; intersection of the two PRs is EMPTY and neither claims cmd/baha/target_environment_production_path_test.go. No conflict, no repair needed for this slice.
- Own run observed to terminal on the exact candidate head (self-run duty): CI · Source & Quality run 42433354279 -> completed/success on PR #1451; PR · Source format pass, PR · Trusted pass, Release Source Preflight pass; Targeted HA docker/podman + validate skipping (not selected for this path). The new tests run inside the go-test group the CI already executes for cmd/baha.

## VM cleanliness

No VM, container or compose project was started or touched by this lane (local `baha target show`/`app status` reads only against throwaway XDG dirs; `go test` is sandboxed). `docker ps` and `podman ps` untouched on baha-docker/baha-podman hosts.

## URTEIL

The card premise is disproved on current develop: BASEHARBOR_TARGET IS read on the production paths (effectiveTarget and the selection chain), precedence --target > BASEHARBOR_TARGET > persisted holds, and this lane published the CI-picked production-path regression (slice 1 #1443 merged; slice 2 PR #1451 awaiting review). The isolated docker-2 greenfield acceptance clause remains blocked by the `use`/`target activate` management-connection binding (target-authority territory of #1430/#1435, reported as STATE, not silently patched). Card stays open until a native isolated `baha up` journey passes or the Owner re-scopes that clause to the authority card.

## END

END_PENDING — mission file: mission-124.md
