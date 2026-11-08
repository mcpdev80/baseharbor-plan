# 0427-124 · BASEHARBOR_TARGET production reader — round 1

Lane: w-flash (flash channel, session c51c8e1a). Card: t-20261108-bughunt-0427-target-env-ignored.
Branch: work/r27-bughunt-124-target-env (single candidate for this chain).

## PLAN

1. Verify zones and remotes (planning repo, develop drift). DONE
2. Re-read the grep proof on current develop; locate every production BASEHARBOR_TARGET reader. DONE
3. Reproduce the behavior locally in an isolated config/data plane (two targets, ENV set). DONE (see Findings)
4. Scope decision: production reader already present on develop -> remaining acceptance gap is the isolated greenfield Core bootstrap; decide fix vs documented no-op. DECISION: this candidate adds the production-path regression proof + precedence assertion in cmd/baha (test-only slice, no duplicate ambiguity logic after #1441 merge), and reports the bootstrap blocker as STATE. See Findings.
5. Drift-merge origin/develop (32ce55dd -> f7a49e681 -> 419b0211) and diff-check for duplicated ambiguity logic. DONE — #1441 changed only the `len(cfg.Targets) > 1` message in selectedTargetName; my slice does not touch that region.
6. Regression test calling the READ PATH on the production CLI path (runWithIO, not t.Setenv-in-fixture-only), CI-picked in the existing Go unit group. IN PROGRESS
7. Local go build/vet/gofmt/focused tests. PENDING
8. PR against develop with card number 0427-124 in title; ancestry + log-line witnesses. PENDING
9. Observe own CI run to terminal; record run ids and outcomes. PENDING
10. Publish evidence to baseharbor-plan origin/main; verify before END; END post. PENDING

## Reality witnesses

- Planning zone check (mission-required one-liner):
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

## CI pickup

The new test lives in cmd/baha and is executed by the existing `PR · Validation · cli-package-tests` job (`go test ./cmd/baha/...`) that already runs on every PR push — no .github/** change needed (Owner scope untouched). The companion production-path precedence test runs in the same Go unit group. Native docker/podman VM cells are not exercised by this slice: no runtime behavior changed, only a regression assertion over the existing read path; the docker-2 greenfield journey is blocked by the authority finding above and stays open on the card.

## State at round end

- Candidate: work/r27-bughunt-124-target-env @ (see origin ls-remote witness below), PR #1443 (branch reused per single-candidate rule; card 0427-124 in title), base develop 419b02113.
- CI: (filled below after terminal observation)

## VM cleanliness

No VM, container or compose project was started or touched by this lane (local `baha target show`/`app status` reads only against throwaway XDG dirs; `go test` is sandboxed). `docker ps` and `podman ps` untouched on baha-docker/baha-podman hosts.

## URTEIL

PENDING

## END

PENDING
