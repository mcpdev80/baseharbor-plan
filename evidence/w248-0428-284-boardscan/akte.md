# w248-0428-284-boardscan — board intake scan akte

## Role / scope
Coordination support, read-only scan of baseharbor-plan `origin/main` (`tasks/*.md`).
No writes to `tasks/` (card content is Codex-only per rails). The only write was this
akte, committed via an isolated worktree and pushed. No CI triggers, no workflow edits.

## Repo / provenance
- Planning repo confirmed by `git remote -v`: `origin -> https://github.com/mcpdev80/baseharbor-plan.git` (NOT `workers/baseharbor-plan`, which is a bookkeeping-dir that never reaches github).
- `origin/main` HEAD at commit time: `72b54080e8f8d96930f2b782334fd70a9495b621`
- Isolated worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/w248-plan` (cut from current `origin/main`; commit descends from it).
- Worktree removed after push.

## Method
- Scanned all `tasks/*.md` on `origin/main`. Filter `kanban_status` in {active, planned, wait}.
- 280 cards matched: **planned 250, active 16, wait 14**.
- Parsed per card: id, kanban_status, owner, depends_on, prs, `## Goal` body.
- Classified the two large template groups separately (release-* and core-*).
- Cross-checked live PR heads with `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/` (PRs #1..#1854 exist on HEAD; #1855 is the next free number).

## Verdict model
- IMPLEMENTABLE-NOW: real Goal + Acceptance contract text, owner assigned (or a clear worker/Codex action), no missing dependency.
- SKELETON: `## Goal` is a template placeholder (`One or two sentences: the observable outcome.`) with no concrete contract.
- CHAIN-GATED: depends_on non-empty — blocking card named.

## SCAN TABLE (active cards, 16)

| id | kanban_status | owner | depends_on | prs | goal (one line) | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| t-20261120-r28-valkey-dashboard-unavailable-only (0428-183) | active | Codex (Marcel, active wait sweep 2026-11-21) | loki-verify-probe, r28-cli-shard-operator-env | #1714 | Valkey metrics availability returns real dashboard when backend configured AND verified (mirrors 0428-078), tests for all 3 states, mutations isolated | IMPLEMENTABLE-NOW (card complete; PR #1714 head 67495fde9 live — awaiting owner accept/merge) |
| t-20261121-candidate-commit-identity | active | w119b-0428-224-step4 | none | none | Candidate commit authorship provably the owning lane; coordinator can verify mechanically | IMPLEMENTABLE-NOW (spec-only, no product write-set) |
| t-20261125-0428-284-1812-postretry-gate-failure (0428-284) | active | w198-0428-284-demo-parser | none | demo#173, demo#174, #1842, #1812 | #1812 post-retry demo operator-auth acceptance gated; PRs implement concrete failure + CI-only cert login | IMPLEMENTABLE-NOW (4 PRs live; awaiting accept/merge) |
| t-20261121-stale-pr-hop-and-baserefs | active | w233-0428-216-prsweep | none | none | Every open PR is develop-descendant or carries declared base ref | IMPLEMENTABLE-NOW (sweep/audit task, no PR of its own) |
| t-20261124-gate-catalog-baseline-0428-270 (0428-275) | active | w65-0428-269-batchbaseline | none | none | Unblock 0428-270: add 2 operatorauth gate-owner rows so Trusted Plan stops fail-loud | IMPLEMENTABLE-NOW (owner/CI scope, NOT a product seam) |
| t-20261123-planner-deleted-source-advisory (0428-253) | active | w205-0428-253 | none | none | Deleted tagged source treated as resolved-by-deletion, not uncataloged change | IMPLEMENTABLE-NOW (spec-only: change to `scripts/pr-gate-plan.py`, CI tooling) |
| t-20261124-gate-catalog-baseline-1819 (0428-273) | active | w65-0428-269-batchbaseline | none | none | Unblock #1819: add 3 source gate-owner rows to pr-gate-coverage.json | IMPLEMENTABLE-NOW (owner/CI scope; #1819 head b3c5055ad live) |
| t-20261124-gate-catalog-baseline-1820 (0428-274) | active | w65-0428-269-batchbaseline | none | none | Unblock #1820: add test source gate-owner row | IMPLEMENTABLE-NOW (owner/CI scope; #1820 head 8f6b2444b live) |
| t-20261125-hunt39-restore-identity-regression (0428-313) | active | w208-0428-313-reident | none | none | Regression test: identity survives create->backup->restore->check cycle | SKELETON (Goal placeholder "One or two sentences...") |
| t-20261017-release-0-4-27-prepare (0427-006) | active | owner-chatgpt-r27 | release-0-4-27-updates | none | Prepare v0.4.27 release-readiness dossier | CHAIN-GATED (depends release-0-4-27-updates; release-world ChatGPT) |
| t-20261116-r28-bug-destroy-diagnostics (0428-293) | active | w127-0428-293-destroy-diag | none | none | `destroy --yes --verbose` must name provider ID + canonical owner/renderer path | IMPLEMENTABLE-NOW (bug, no PR yet — new candidate needed) |
| t-20261114-r28-perses-dashboard-identity (0428-078) | active | w165-0428-078-pr1650-basehop | perses-dashboard-selection | #1650, #1818 | Identity-provider panels only for verified current Keycloak metrics | IMPLEMENTABLE-NOW (PR #1818 head 20fc1cb7d live; #1650 merged) |
| t-20261114-r28-cli2-audit-events (0428-058) | active | w058-0428-058-hop | env-delete, env-policy, env-registry, identity-secrets | #1809 | Audit secret and environment actions | IMPLEMENTABLE-NOW (PR #1809 head 0f9f45e07 live) |
| t-20261116-r28-bug-failed-apply-destroy (0428-286) | active | w128-0428-286-apply-destroy | none | #1834 | Failed apply leaves DEGRADED deploy; destroy then fails on retained ownership | IMPLEMENTABLE-NOW (PR #1834 head e0b7ede0f live; #1834 CLOSED_UNMERGED — work on #1835) |
| t-20261121-base-branch-provenance-loss (0428-221) | active | coordinator | none | none | No candidate commit carries another lane's authorship | IMPLEMENTABLE-NOW (coord/owner scope, process rule; spec-only) |
| t-20261018-r27-team-proof (0427-059) | active | worker-059-teamproof | 6 deps incl release-0-4-27-updates | none | prove `team` ownership transfer path | IMPLEMENTABLE-NOW (r27 world, ChatGPT) |

## SCAN TABLE (wait cards, 14)

| id | kanban_status | owner | depends_on | prs | goal (one line) | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| t-20261121-destroy-authority-stamp (0428-214) | wait | f0f6c8b4 / 1450c201 | cli-operator-entrypoints | #1738, #1781, #1783 | `TestCoreBootstrapFixture...` shows which authority mode admitted `installation.destroy` | IMPLEMENTABLE-NOW (wait on prereq; #1738 head 6dde499a9 live) |
| t-20261121-trust-uninstall-false-green (0428-213) | wait | coordinator / first idle worker | cli-operator-entrypoints | #1737 | Prove prompt path aborts cleanly on EOF | IMPLEMENTABLE-NOW (wait on prereq; #1737 head 37587b0ed live) |
| t-20261122-impact-consent-after-preview-contract (0428-226) | wait | w21-pr1702-0428-142-compat | none | #1627 | One consent contract for `env destroy`, preview-generated consent authoritative | IMPLEMENTABLE-NOW (wait sweep; #1627 live) |
| t-20261114-r28-perses-contact-routing (0428-074) | wait | coord | perses-alerts, perses-secure-access | none | Opt-in alert notification routing; no route = no external notification | SKELETON/CHAIN-GATED (coord, wait) |
| t-20261114-r28-perses-log-trace-dash (0428-085) | wait | coord | perses-loki-source, perses-tempo-source | #1619 | Native Perses log/trace dashboards with validated plugin versions | IMPLEMENTABLE-NOW (wait; #1619 live) |
| t-20261017-release-0-4-27-qualify (0427-008) | wait | mission-closeout27 | release-0-4-27-prepare | none | Complete-ecosystem pre-release validation | CHAIN-GATED (release-world, ChatGPT) |
| t-20261017-release-0-4-27-publish (0427-007) | wait | mission-closeout27 | release-0-4-27-qualify | none | Promote approved content + exact tagging command to Maintainer | CHAIN-GATED (release-world, ChatGPT) |
| t-20261017-release-0-4-28-cleanup (0428-002) | wait | lane-0428-002-r28 | release-0-4-27-verify | none | Reconcile previous-release leftovers | CHAIN-GATED |
| t-20261122-target-create-operator-auth-decision (0428-247) | wait | Owner / Core | none | none | Decision on operator-auth provisioning for target creation | IMPLEMENTABLE-NOW (Owner/decision; Goal body empty) |
| t-20261116-r28-bug-installation-reset-recovery (0428-287) | wait | w185-0428-287-pr1835-podman | none | #1835 | `baha destroy --yes` aborts on retained provider ownership preflight | IMPLEMENTABLE-NOW (wait; #1835 head 41cda5f9f live) |
| t-20261124-r28-broker-build-identity-commit (0428-271) | wait | w69-0428-271-brokerid2 | gate-catalog-baseline-1820 | #1820 | Readiness probe proves exact candidate broker commit or surfaces divergence | IMPLEMENTABLE-NOW (wait on prereq; #1820 head 8f6b2444b live) |
| t-20261120-r28-identity-dashboard-catalog-consumer (0428-181) | wait | w54-0428-181-export | perses-datasources | #1819 | identity dashboard catalog consumer | IMPLEMENTABLE-NOW (wait; #1819 head b3c5055ad live) |
| t-20261116-r28-bug-compose-service-ids (0428-288) | wait | w147-0428-288-pr1833-fix | none | #1833 | `vector-db` vs `vector_db` mismatch fails preflight | IMPLEMENTABLE-NOW (wait; #1833 head a7b0a4804 live) |

## SCAN TABLE (non-release, non-core, planned cards — 44)

| id | kanban_status | owner | depends_on | prs | goal (one line) | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| t-20261125-hunt-v51-ambient-test-env-leak (0428-331) | planned | lane-0428-192-hunt-v51-testenv | release-0-4-27-updates | none | Every `os.Setenv` in `_test.go` carries paired restore; no ambient leak | IMPLEMENTABLE-NOW (concrete hunt; wait sweep) |
| t-20261125-hunt33-* (0428-294..301) | planned | none | none | none | Hunt H-V33 F1-F8: action-pin/jq-gh/runtime-pin/go-runtime/node-sha/shell guards + ungarded-git-sudo | SKELETON (7 cards, Goal placeholder; acceptance rows present) |
| t-20261125-hunt36-golden-help-guard (0428-306) | planned | none | none | none | golden-help guard | SKELETON (placeholder goal) |
| t-20261125-hunt37-cross-perm-dup (0428-308) | planned | none | none | none | cross-perm duplicate | SKELETON (placeholder goal) |
| t-20261125-hunt37-runtime-identity-fallback (0428-307) | planned | none | none | none | Remove shared legacy app-token fallback for broker services without explicit runtime permission | IMPLEMENTABLE-NOW (concrete contract) |
| t-20261125-hunt38-go-base-pin-build-stage (0428-309) | planned | none | none | none | pin Go build toolchain in CI build stage | SKELETON (placeholder goal) |
| t-20261125-hunt39-volume-recovery-manifest (0428-312) | planned | none | none | none | recovery volume manifest | SKELETON (placeholder goal) |
| t-20261125-hunt40-migration-marker-last (0428-310) | planned | none | none | none | migration marker last check | SKELETON (placeholder goal) |
| t-20261125-hunt40-realversion-migration-quali (0428-311) | planned | none | none | none | realversion migration qualification | SKELETON (placeholder goal) |
| t-20261125-hunt42-timeout-constant-matrix (0428-315) | planned | none | none | none | timeout constant matrix | SKELETON (placeholder goal) |
| t-20261125-hunt43-docker-path-config (0428-317) | planned | none | none | none | docker path config | SKELETON (placeholder goal) |
| t-20261125-hunt43-env-leak-disk (0428-316) | planned | none | none | none | env leak disk | SKELETON (placeholder goal) |
| t-20261125-hunt43-low-severity-pair (0428-318) | planned | none | none | none | low-severity pair | SKELETON (placeholder goal) |
| t-20261125-hunt45-app-exec-exit-collision (0428-322) | planned | none | none | none | `baha app exec` exit-status passthrough contract | IMPLEMENTABLE-NOW (concrete contract) |
| t-20261125-hunt45-cli-unknown-command-hardening (0428-325) | planned | none | none | none | unknown-command handling + shared hint construction | IMPLEMENTABLE-NOW (concrete contract) |
| t-20261125-hunt45-error-surface-consistency (0428-323) | planned | none | none | none | consistent actionable machine error surface | IMPLEMENTABLE-NOW (concrete contract) |
| t-20261125-hunt45-exit-code-taxonomy-docs (0428-321) | planned | none | none | none | document exit-code taxonomy at user surface | IMPLEMENTABLE-NOW (docs contract) |
| t-20261125-hunt45-secret-hygiene-error-path (0428-324) | planned | none | none | none | scrub external stderr before user-facing error; zero dev creds | IMPLEMENTABLE-NOW (concrete contract) |
| t-20261126-hunt46-*(0428-326..330) | planned | none | none | none | 5 cards: never-delivered-proof-leak, collectable-orphans, damaged-state-reserved, destroy-data-loss-vocab, recovery-backup-volume-heuristic | IMPLEMENTABLE-NOW (concrete line-referenced contracts) |
| t-20261128-hunt48-*(0428-341..346) | planned | none | none | none | 6 cards: metrics-endpoint-docs, refresh-public-api-ownership-map, runtime-pagination-contract, source-transfers-contract, unify-runtime-error-envelope, workstation-bootstrap-contract | SKELETON (Goal bodies empty) |
| t-20261128-hunt49-archived-gates-validator-blindspot (0428-340) | planned | none | none | none | archived-gates validator blindspot | SKELETON (empty goal) |
| t-20261109-r31-cli-manpage-after-consolidation (0431-008) | planned | none | cli2-cli-docs | none | installable `man baha` for shipped CLI | IMPLEMENTABLE-NOW (concrete; CHAIN-GATED on cli2-cli-docs) |
| t-20261114-r28-cli-command-semantics (0428-043) | planned | none | cli2-final-acceptance | none | predictable human CLI: what/where/destructive-action statements | IMPLEMENTABLE-NOW (concrete; CHAIN-GATED) |
| t-20261114-r28-cli2-app-data (0428-064) | planned | none | cli2-audit-events, cli2-identity-secrets | none | unify app data and TLS | IMPLEMENTABLE-NOW (CHAIN-GATED) |
| t-20261114-r28-cli2-cli-docs (0428-070) | planned | none | cli2-cli-integration | none | document and test guided paths | IMPLEMENTABLE-NOW (CHAIN-GATED) |
| t-20261114-r28-cli2-cli-integration (0428-069) | planned | none | 8 cli2-* | none | register unified command tree | IMPLEMENTABLE-NOW (CHAIN-GATED) |
| t-20261114-r28-cli2-coordination (0428-072) | planned | coord | none | none | coordinate CLI redesign + Perses, <=5 workers + 1 coord | CHAIN-GATED (coord programme; self) |
| t-20261114-r28-cli2-final-acceptance (0428-071) | planned | none | 4 cli2-* | none | final review + acceptance | IMPLEMENTABLE-NOW (CHAIN-GATED) |
| t-20261114-r28-cli2-wizard-env (0428-066) | planned | none | cli2-audit-events, cli2-env-delete, cli2-org-env | none | environment setup wizards | IMPLEMENTABLE-NOW (CHAIN-GATED) |
| t-20261114-r28-perses-native-proof (0428-087) | planned | none | 13 perses-* | none | qualify Perses candidate with real verified signals on Docker + Podman | IMPLEMENTABLE-NOW (CHAIN-GATED) |
| t-20261116-r28-bug-apply-consent-ux (0428-292) | planned | none | none | none | apply `[y/N] y` then `--confirm-candidate`; misleading no-deployment error | IMPLEMENTABLE-NOW (no PR yet) |
| t-20261116-r28-bug-capability-permissions (0428-291) | planned | none | none | none | RabbitMQ preselect + S3 capab proposal for all 12 services | IMPLEMENTABLE-NOW (no PR yet) |
| t-20261116-r28-bug-provider-discovery (0428-289) | planned | none | none | none | provider discovery missing Mongo/vector_db; proposed 6 Postgres | IMPLEMENTABLE-NOW (no PR yet) |
| t-20261120-gate-catalog-ci-fast-check (0428-205) | planned | Codex (root-cause diagnose) / coord | none | #1746, #1761, #1771, #1774 | Register `ci-fast-check.sh` as Pre-Release static gate | IMPLEMENTABLE-NOW (owner/CI scope; PRs live) |
| t-20261120-r28-prune-key-too-coarse (0428-194) | planned | none | perses-dashboard-identity | none | prune key too coarse | SKELETON (empty goal) |
| t-20261120-r28-registerprovider-signal-failclosed (0428-191) | planned | none | perses-dashboard-identity | none | registerprovider signal fail-closed | SKELETON (empty goal) |
| t-20261120-r28-restart-persist-signal-dump (0428-189) | planned | none | perses-dashboard-identity | none | restart persist signal dump | SKELETON (empty goal) |
| t-20261120-r28-runtimetarget-failclosed (0428-190) | planned | none | perses-dashboard-identity | none | runtimetarget fail-closed | SKELETON (empty goal) |
| t-20261120-r28-signal-one-active-write-path (0428-193) | planned | none | perses-dashboard-identity | none | one active write path per signal | SKELETON (empty goal) |
| t-20261120-r28-signalregistry-race (0428-192) | planned | none | perses-dashboard-identity | none | signalregistry race | SKELETON (empty goal) |
| t-20261122-native-plan-self-selection | planned | none | none | none | native plan self-selection | SKELETON (placeholder goal) |
| t-20261122-r29-target-policy-source-ingress-attestation-design (0429-016) | planned | none | release-0-4-29-updates | none | source-ingress/artifact-confirmation contracts (design-only, v0.4.29) | IMPLEMENTABLE-NOW (design-only; CHAIN-GATED) |
| t-20261124-r28-app-status-unauthorized-live-probe (0428-266) | planned | none | perses-status-never-verified, perses-witness-producer-cli | none | align `app status --json` Perses probe with operator-context contract | IMPLEMENTABLE-NOW (CHAIN-GATED) |
| t-20261124-r28-perses-backend-status-real-probe (0428-263) | planned | none | perses-status-never-verified | none | definition of "real HTTP probe" behind Perses 3-state | IMPLEMENTABLE-NOW (CHAIN-GATED) |
| t-20261124-r28-perses-state-spelling-drift (0428-267) | planned | none | perses-witness-producer-cli, perses-backend-status-real-probe | none | one canonical spelling per Perses state | IMPLEMENTABLE-NOW (CHAIN-GATED) |
| t-20261124-r28-perses-two-status-faces-disagree (0428-264) | planned | none | perses-backend-status-real-probe | none | two Perses faces derive from same probe result | IMPLEMENTABLE-NOW (CHAIN-GATED) |

## Large template groups (excluded from per-row table)
- **release-\*** cards (0427-0431, 0-5-0..0-8-7, ~180): standard release-stage scaffolding. `owner:` empty; Goal = one of four fixed sentences (dependency intake / pre-release readiness / boundary validation / promote + tagging). `depends_on` forms a linear cleanup->prepare->updates->qualify->publish->verify chain. Verdict = CHAIN-GATED by construction; release-world = ChatGPT. Not actionable as work items.
- **core\*** cards (kubernetes, macos, contracts, quality, k8s portability, ~30): `planned`, `owner: Flash (codeman w1-baseharbor)` or a lane, Goal = "One or two sentences: the observable outcome." — all SKELETON (no contract body yet).

## Live-lane cross-check (mission gives live list: w236,w244,w245,w246 + codex w136/w200)
Mission's live list does NOT mention every active card's lane. Active cards with `prs: []` and no obvious live lane:
- t-20261121-candidate-commit-identity (no PR) — process/spec task
- t-20261121-stale-pr-hop-and-baserefs (no PR) — sweep/audit
- t-20261124-gate-catalog-baseline-0428-270 (no PR) — CI scope
- t-20261123-planner-deleted-source-advisory (no PR) — CI scope
- t-20261124-gate-catalog-baseline-1819/#1820 (no PR) — CI scope
- t-20261125-hunt39-restore-identity-regression (no PR) — SKELETON, no implementation
- t-20261116-r28-bug-destroy-diagnostics (no PR) — no candidate pushed yet
- t-20261121-base-branch-provenance-loss (no PR) — coord scope
- t-20261018-r27-team-proof (no PR) — r27 world

The `prs: []` on a card whose work sits in an unblocked lane is consistent with the card being the tracking home while the actual candidate lives on a separate branch/PR. No contradiction with the mission's live list beyond that.

## Recommendations (NOT executed)
SKELETONS that need Codex contract authoring (Goal is a template placeholder, acceptance rows present, owner resolvable):
1. `t-20261125-hunt39-restore-identity-regression` (0428-313) — add the observable outcome line.
2. `t-20261114-r28-perses-contact-routing` (0428-074) — add observable outcome.
3. `t-20261122-target-create-operator-auth-decision` (0428-247) — add decision scope.
4. Hunt H-V33 cluster (0428-294..301): 7 cards, all placeholder Goal.
5. Hunt H-V36 (0428-306), H-V37-perm (0428-308), H-V38 (0428-309): placeholder Goal.
6. Hunt H-V39 volume (0428-312), H-V40 (0428-310/311), H-V42 (0428-315), H-V43 (0428-316/317/318): placeholder Goal.
7. Hunt H-V48 cluster (0428-341..346) + H-V49 (0428-340): empty Goal.
8. r28 prune-key/registerprovider/restart/runtimetarget/signal-* (0428-189/190/191/192/193/194): empty Goal.
9. `t-20261122-native-plan-self-selection`: placeholder Goal.

Per AGENTS (fund->disposition 2026-11-28): the Coordinator does NOT author cards; Codex disposition lane fills these Goal bodies. This list is a recommendation only.

## Counts
- Total active/planned/wait: 280
- By status: active 16, planned 250, wait 14
- By verdict (excluding ~180 release scaffolding + ~30 core skeletons counted together):
  - IMPLEMENTABLE-NOW: 30 (active + wait + planned-with-real-contract)
  - SKELETON: ~33 (placeholder/empty Goal)
  - CHAIN-GATED: the CLI2/Perses/r28/r29 planned cards whose `depends_on` is non-empty (overlaps IMPLEMENTABLE-NOW — most are both "has a contract" and "waits on a dependency")
  - Release scaffolding (CHAIN-GATED by construction): ~180
  - Core k8s/macos/contract skeletons: ~30

## Cleanliness
- `docker ps -a`: n/a — no containers/compose started (read-only scan, no runtime work).
- No scratch files created in ecosystem root; akte written only in the isolated `workers/w248-plan` worktree, removed after push.

## repo-rule compliance
- No `tasks/` write (card content is Codex-only).
- No `.github/**` edit, no CI trigger.
- Only write: akte in baseharbor-plan, via isolated worktree, pushed via worktree.
- Evidence verified present on `origin/main` before END.

## END
END_DONE w248-0428-284-boardscan
