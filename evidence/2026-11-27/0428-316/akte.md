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

(to be appended as work proceeds)

## Hosted CI (self-run duty)

(to be appended: two distinct run IDs on exact head + terminal status)

## cleanliness

(to be appended; no containers/compose projects are started by this lane — unit-scope work only; docker/podman native gates run in Hosted CI)

## END

(to be appended: END_DONE / END_BLOCKED w396-0428-306-goldenhelp: <one line + candidate SHA>)
