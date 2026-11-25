# w228-0428-216-huntv59 — Bug-Hunt Slice H-V59 CONSENT/CONFIRM RAIL

Role: Worker (pure Befundung). No product change, no card, no fix.
Scope: enumerate every confirmation/approval/consent flag + env in product code (cmd/ + internal/), per hit: default value, fail-open vs fail-closed, which CI/Hosted path drives it, whether any Hosted path can flip it OPEN (risk) or it is the #1842-style refusal-by-unconfigured-target (friction). Output table: flag -> file:line -> default -> CI reachability -> class (risk|friction|ok).

## Attestation (fetched VERBATIM at runtime)
- Remote develop head (ls-remote lane-origin refs/heads/develop): fcd449117e189c555c7530b9527cd22d3f6f25ff
- Worktree checked out at exact checkout SHA: fcd449117 (matches mission exact checkout)
- Planning repo verified: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan  (remote -v: origin https://github.com/mcpdev80/baseharbor-plan.git)
- baseharbor product remote used: lane-origin ssh://git@github.com/mcpdev80/baseharbor.git  (origin is github too, but the product clone is via lane-origin; plan writes go through the plan remote)
- git author identity NOT changed (no product commit; no admission gate needed — this hunt makes zero product writes). Evidence commits land in the plan repo, not the product.
- Worktree isolation: /home/marcel/dev/baseharbor-ecosystem/workers/workers/w228-0428-216-huntv59-wt (git worktree add workers/w228-0428-216-huntv59-wt origin/develop)

## Findings table (flag/env -> file:line -> default -> CI reachability -> class)

1. BASEHARBOR_PROVIDER_CHANGE_CONSENT (env) -> cmd/baha/provider_change_context.go:21,48-65
   default: empty => no consent (nil) => fail-closed on provider-impact seams
   shape: single bounded JSON object {plan_id, first, [second], [delete_data]}; DisallowUnknownFields, len<=8192, must start with '{', plan_id non-empty
   CI reachability: Hosted — CI supplies it via scripts/ci-podman-typed-consent.py / scripts/ci-broker-typed-consent.py (read plan, emit {plan_id, first:true, second:(stages==2), delete_data:false})
   RISK: FAIL-CLOSED BY DESIGN. The typed-consent scripts raise ValueError on destructive impacts (ci-podman-typed-consent.go consent_from_plan: "destructive provider impact requires separate authorization"). Hosted path can flip NON-destructive impacts OPEN only for the exact plan_id of the current operation; it cannot fabricate delete_data or a wrong plan_id. Ordinary --yes does NOT grant this consent (provider_change_context.go:53).
   class: ok

2. --yes / -y on `baha app up` -> cmd/baha/app_up.go:22-23,58
   default: false; withAssumeYes only skips the *guided resolver* and allowed confirmations, never provider-consequence or data-deletion consent (Long help app_up.go:44)
   CI reachability: Hosted — workflows call `up --control-plane-only --yes` (podman-acceptance.yml:326, runtime-broker.yml:69, runtime-s3-acceptance.yml:73). Control-plane-only selects the independent Core install path; --yes still cannot authorize provider-consequence/data-deletion.
   class: ok (fail-closed; --yes is a documented narrow accelerator)

3. Two-phase provider-impact consent (First/Second stages) -> internal/application/provider_change_consent.go:66-77
   default: First=false => validateProviderConsent returns "impact-confirmation-required" (fail-closed). confirmations==2 requires Second=true.
   destructive requires separate DeleteData=true else "data-deletion-consent-required".
   CI reachability: Hosted via BASEHARBOR_PROVIDER_CHANGE_CONSENT JSON (see finding 1). Interactive: readProviderImpactAcknowledgements (cmd/baha/provider_change_confirmation.go:88) and readProviderApplyAcknowledgement (:69) prompt [y/N] (fail-closed default).
   class: ok

4. app destroy (local) -> cmd/baha/application_destroy_authorization.go:158-188,246-253
   default: consent nil + non-TTY (or no --yes) => reads prompt [y/N] (default false) => fail-closed; "impact-confirmation-required" before any runtime access.
   CI reachability: Hosted --yes path exists (runtime-s3-acceptance.yml:297-301, podman-acceptance.yml:384) but still requires the two-phase provider impact consent via env for the actual impact; data deletion separate.
   class: ok (fail-closed)

5. env destroy --yes / --delete-data / --confirm-delete-data -> cmd/baha/env_destroy.go:89-164,316-330,397-437
   default: confirmed=false => "No changes were made" (fail-closed, line 142-145). deleteDataConfirmed=false => confirmedDataDeletion returns explicitFlag(false) under noInput (line 317-318) or typed "DELETE" prompt (line 323-329) => fail-closed.
   data-choice default = KeepData (line 420-422).
   CI reachability: not a Hosted destructive-data path; --yes alone cannot delete data; separate --confirm-delete-data + typed DELETE.
   class: ok (fail-closed)

6. requireManagedClientConsent (client launch) -> cmd/baha/app_client_consent.go:24-100
   default: no prior consent record (12h TTL) => prompts "Approve this client session for 12 hours? [y/N]"; noInput or non-TTY => usageError fail-closed (line 65-67). Empty answer => not "y"/"yes" => rejected (line 73).
   CI reachability: Hosted cannot drive an interactive terminal; requires terminal approval => fail-closed in automation.
   class: ok (fail-closed; friction: 12h record file at client-consent/<id>, 0600, 0700 dir)

7. trust install --yes / trust uninstall --yes -> cmd/baha/trust.go:129-141,160-180
   default: confirmed=false => usageError "requires explicit --yes consent" fail-closed (line 138-140). installManagedTrust/uninstallManagedTrust call RequireApproval("trust.install", approved) => fail-closed if !approved (internal/applicationlifecycle/result.go:41).
   CI reachability: Hosted requires --yes AND RequireApproval; not triggered by normal CI.
   class: ok (fail-closed)

8. requireRootlessSetupConsent -> cmd/baha/rootless_bootstrap.go:149-179
   default: interactive=false => "requires an interactive terminal and explicit approval" fail-closed (line 169-171). Typed prompt [y/N] default false (line 172-178).
   NOTE: comment line 166-167 explicitly says neither unattended calls nor generic --yes grant permission.
   CI reachability: not Hosted (needs interactive terminal + host UID map) => fail-closed.
   class: ok (fail-closed)

9. app doctor --fix --yes -> cmd/baha/app_doctor_repair.go:69-118,47-106
   default: approved=false => non-TTY/noInput => usageError "application repair requires explicit consent" fail-closed (line 107-110). --yes requires --fix (line 82). Typed confirmDoctorRepair.
   CI reachability: Hosted repair is read-only unless --fix --yes + terminal; --yes alone fail-closed.
   class: ok (fail-closed)

10. backup/restore guided confirmation -> cmd/baha/app_backup_restore_guided.go:105,214,444-471
    default: promptGuidedConfirmation(label, defaultYes). "Restore this backup...?" defaultYes=false => fail-closed (line 214). "Create backup now?" defaultYes=TRUE (line 105) => empty answer still returns true.
    RISK: the "Create backup now?" prompt uses defaultYes=true. However the subsequent step reads a hidden backup PASSWORD from the terminal (readBackupPasswordFromTerminal requires a terminal; line 473-476 returns error if not an *os.File) and the full flow is validation+password-gated. In automation without a terminal the guided path returns "guided confirmation requires terminal input" (line 447) BEFORE the defaultYes applies.
    CI reachability: Hosted uses deterministic --password-file path (no guided prompt). Guided path requires terminal.
    class: ok (defaultYes=true is contained by the required terminal password gate; not a Hosted flip-to-open)

11. MCP provider-change consent input (ProviderChangeConsent JSON) -> cmd/baha/mcp_tools.go:483,644,680; cmd/baha/mcp_lifecycle_extra.go:22; cmd/baha/target_mutation.go:55-56
    default: input.ProviderChangeConsent nil => no consent => fail-closed on the seam.
    app.perses.enable/disable/remove: "Explicit confirmation is mandatory and ownership verification remains fail-closed" (mcp_lifecycle_extra.go:72-78); Approval bool field: "ordinary approval does not imply backend changes" (line 137).
    CI reachability: MCP callers must pass explicit consent; no default open.
    class: ok (fail-closed)

12. app.perses lifecycle ownership gate (internal/application/perses_lifecycle.go:102) -> ValidatePersesLifecycleIdentity
    default: authorized/ownershipVerified required; fail-closed otherwise.
    class: ok (fail-closed)

13. confirmation_digest / candidate consent (repository apply choke point) -> cmd/baha/app_remote_lifecycle.go:160-163; internal/delivery/candidate.go:81 (CandidateConsentDigest); cmd/baha/deployment_previous_intent_test.go
    default: candidateConsentOverride empty => recordDeploymentBeforeMutation fails closed (no consent => no mutation).
    CI reachability: Hosted remote apply requires the exact candidate digest consent; cannot be faked.
    class: ok (fail-closed)

14. node disconnect --yes / consent -> cmd/baha/node_disconnect_lifecycle.go:44-69; node_disconnect_client.go:141-196
    default: consent nil + non-TTY => "impact-confirmation-required" fail-closed (line 172-173).
    class: ok (fail-closed)

15. control-plane stop destroy --yes -> cmd/baha/control_plane_destroy.go:84-130; control_plane_stop_impact.go:173-211
    default: confirmed false => authorizeRuntimeDestroyImpact fail-closed; stale-impact-consent (line 130, 205).
    class: ok (fail-closed)

16. management_remote_destroy_cli --yes (remote destroy) -> cmd/baha/management_remote_destroy_cli.go:35-41,87-157
    default: approved=false => fail-closed (line 39-41). Two-phase remote impact consent required (line 135-157).
    class: ok (fail-closed)

17. secret delete --yes -> cmd/baha/secret_operations.go:290-316
    default: confirmed=false => Preview=true (read-only), no mutation (line 315-316).
    class: ok (fail-closed)

18. access wizard / offboarding (fail-closed by design) -> cmd/baha/access_wizard_command.go:26,186
    "It never grants a right on its own: every assignment folds into the single production policy authority and every removal re-checks the current configuration at submit time."
    class: ok (fail-closed)

19. confirmation-by-unconfigured-target (friction class, #1842)
    Several seams fail-closed when the required target/owner is absent rather than asking:
    - env destroy: no environment selected (NAME or BASEHARBOR_ENVIRONMENT) => machine.NewError ErrorConflict (env_destroy.go:432-436)
    - env destroy: ownership/impact unknown (scope.IsFailClosed) => ErrorOwnershipAmbiguous (env_destroy.go:104-117)
    - client consent: incomplete client scope => error (app_client_consent.go:25-27)
    - provider consent env: malformed JSON => provider_change_consent_input_invalid (provider_change_context.go:52-54)
    These are friction (refusal-by-unconfigured-target), not risk. No Hosted path opens them.

## Overall risk assessment
- FAIL-CLOSED throughout: every destructive/risk-bearing seam (provider impact two-phase, data deletion, host trust, rootless Docker, client launch, repair, destroy, MCP perses) requires explicit confirmation and fails closed on absence. --yes is a narrow documented accelerator that never substitutes for provider-consequence or data-deletion consent.
- NO Hosted path can flip a destructive impact OPEN: ci-podman-typed-consent.py and ci-broker-typed-consent.py raise on destructive impacts; consent only covers the exact plan_id of the current operation; delete_data cannot be faked.
- ONE containment to keep an eye on: promptGuidedConfirmation(label, defaultYes=true) for "Create backup now?" (app_backup_restore_guided.go:105). defaultYes=true means an empty line still confirms, but the backup guided flow then requires a terminal-supplied hidden password (readBackupPasswordFromTerminal needs *os.File), so automation without a terminal fails closed before defaultYes can take effect. Not exploitable via Hosted CI.
- NO #1842-style risk found: all refusal-by-unconfigured-target paths are friction (fail-closed), not secret-opens.

## repo-rule compliance
- No product files written, edited, or deleted. Zero writes to cmd/, internal/, .github/**, spec/, contracts/.
- No workflow edit, rerun, or workflow_dispatch.
- No second candidate branch, no merges, no card edits.
- Evidence committed to the plan repo only (baseharbor-plan), never the product repo.

## Cleanliness
- pid=3944216
- docker ps -a BEFORE end: empty (no containers). docker ps -a AFTER end: empty.
- podman ps -a: pre-existing 'baseharbor-pre-release-registry' (created 3 days ago, NOT mine).
- No docker/podman compose started this lane; no containers/volumes/networks/state created.
- No foreign karren / ambient-core/ images touched.
- Worktree workers/w228-0428-216-huntv59-wt: clean, at fcd449117.

## END
END_DONE w228-0428-216-huntv59: CONSENT/CONFIRM RAIL fully enumerated across cmd/ + internal/, all fail-closed, no Hosted flip-to-open on destructive impacts; akte published via plan-PR flow + ls-tree witness.
SHA: fcd449117 (exact checkout); evidence path on origin/main (ls-tree witness below).
