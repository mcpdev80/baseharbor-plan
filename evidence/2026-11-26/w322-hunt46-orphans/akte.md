# w322-hunt46-orphans akte — H-V46 census: collectable orphans in reserved namespaces

Lane: w322-0428-249-pr1812gate. Mission: w322-hunt46-orphans.txt (H-V46, evidence-only, no product edits). Base develop 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74. Disjoint from w329-0428-326-hunt46-proofleak (never-delivered-proof scope). No product edits, no .github, no new cards, no card content.

## Visible ANSATZ BLOCK (required before any work)

- card frontmatter owner VERBATIM (fetched from develop at runtime): card t-20261126-hunt46-collectable-orphans-reserved-namespace, medium, ready, dependency-free (from mission file; no product card in write-set).
- git user.name: w322-0428-249-pr1812gate
- git user.email: w322-0428-249-pr1812gate@baseharbor.local
- literal commit invocation: git -c user.name='w322-0428-249-pr1812gate' -c user.email='w322-0428-249-pr1812gate@baseharbor.local' commit ...
- pre-push gate: git show -s --format=%an HEAD => w322-0428-249-pr1812gate

## METHOD (evidence-only; no product writes)

- /var/tmp/w322-hunt46-orphans-wt isolated worktree on origin/main (planning repo).
- Product read-only on develop via git grep/sed (no checkout writes, no build).
- Hunted: every path where a collect/garbage routine can claim or delete objects in a RESERVED namespace (prefix `baseharbor-internal-`) or carrying a RESERVED marker (`__baseharbor_...`, wizard-navigation name), quoting file:line, naming the guard that should have caught it, classifying leak/destructive vs cosmetic.

## FINDINGS TABLE

| file:line | routine | reserved surface | class | severity |
|---|---|---|---|---|
| internal/application/workload.go:216-218 (`selectWorkloadServices`) | workload service selector | reserved `baseharbor-internal-` service namespace | guarded (returns error, rejects) | no leak - guard fires |
| internal/application/manifest_validation.go:467-469 (`validateSecretKey`) | manifest secret-key validation | reserved `__baseharbor_` / `_baseharbor` marker | guarded (returns error) | no leak - guard fires |
| cmd/baha/app_new_wizard.go:252 | new-app wizard | reserved wizard-navigation name | guarded (usageError) | no leak - guard fires |
| internal/deployment/deployment_list.go:164 `CollectableOrphans` | ownerless-deployment collector | deployments namespace (UUID-keyed) | guarded: owner-missing guard (deploymentOwnerMissingForDetach) + DeploymentID==folder + Target match | no leak - fail-closed; foreign/blank/mismatched records excluded |
| internal/deployment/deployment_list.go:231-234 `CollectableOrphans` (same fn) | same | embedded DeploymentID/Target integrity | guarded | no leak - blank/mismatched excluded |
| internal/metrics/perses_datasource_lifecycle.go:276-287 `clearPersesDatasourceProvisioningFolder` | perses provisioning-file garbage | iterates ALL files in provisioning folder, NO reserved-marker check | UNGUARDED collect-all | cosmetic - provisioning files are transient runtime artifacts, not reserved-namespace objects; baseline/docs are materializer-written, not persisted here |
| internal/application/perses_datasource_seam.go:246-258 `removeDatasourceArtifactsLocal` | datasource-artifact cleanup | projectionRoot config.yaml + provisioning/ | guarded by manifest-bound caller (clearStalePersesDatasourceArtifacts) | no leak - caller is manifest-scoped |
| internal/deployment/environment_destroy_scope.go:132 `CollectEnvironmentDestroyScope` | env-destroy scope collector | environment deployments | guarded: global-app preservation + per-deployment owner re-check | no leak |
| internal/deployment/deployment_list.go:164 caller cmd/baha/target_definition_change_plan.go:140 | target-detach refusal | collectable orphans naming | guarded (refuses detach naming orphans) | no leak - refusal is the guard |

## ROOT-SURFACE SUMMARY (the hunt target)

- Reserved service namespace `baseharbor-internal-`: guarded at workload.go:216 (reject) and app_dev_routing.go:621 (internal, self-authored, not a leak).
- Reserved secret marker `__baseharbor_`: guarded at manifest_validation.go:467.
- Reserved wizard-name: guarded at app_new_wizard.go:252.
- The one collect-all with no reserved-marker gate: clearPersesDatasourceProvisioningFolder (metrics/perses_datasource_lifecycle.go:276) — iterates the provisioning folder and removes every non-dir file. Classified cosmetic: those are transient perses provisioning files written by the materializer, not objects in a reserved namespace or carrying a reserved marker. No destructive owner-loss.

## NO PRODUCT LEAK FOUND IN RESERVED-NAMESPACE ORPHAN SURFACE

Every collectable-orphan / garbage routine in the targeted surface either (a) fires its reserved-marker/namespace guard, or (b) collects only manifest-scoped / UUID-keyed / owner-verified objects with fail-closed exclusion of foreign, blank, or mismatched records. The single unguarded collect-all (clearPersesDatasourceProvisioningFolder) is cosmetic. Scope-card / disposition proposals beyond census belong in akte prose for CODEX disposition, not in a product edit.

## DATED CORRECTION — 2026-11-26 (w335-0428-318-lowpair, acting for released lane w322-0428-249-pr1812gate, per CODEX-REVIEW HOLD comment 7197353979)

The census conclusion above was corrected to match live card 0428-327
(`tasks/t-20261126-hunt46-collectable-orphans-reserved-namespace.md`, frontmatter owner
verbatim: medium, ready, dependency-free). This is an evidence-content correction only: no
product file, no card content, no new card, no .github.

- What was wrong: the akte classified `CollectableOrphans`
  (`internal/deployment/deployment_list.go`) as safely guarded and listed "no leak -
  fail-closed; foreign/blank/mismatched records excluded." That is contradicted by the card
  and by the source at the census develop (5a37ddbd9a06dd44f6068d3266ff2ed853a84a74).
- The contradiction, verified against develop source: `CollectableOrphans` enumerates each
  `entry.IsDir()` child of `deployments/` as a `deploymentID` and calls
  `deploymentOwnerMissingForDetach` on it (deployment_list.go ~185-189) — there is **no**
  explicit `never-delivered` reservation skip. The only exclusion is blank / mismatched
  DeploymentID or blank / mismatched Target, which filters foreign records but NOT a crafted
  record whose `DeploymentID=="never-delivered"` and `Target==target`. The "missing record
  bails early" protection the akte relied on is therefore accidental, exactly as card 0428-327
  states (lines 44, 50, 56-58, 73).
- Corrected finding: `CollectableOrphans` does not skip the reserved `never-delivered`
  subdirectory; a crafted `never-delivered/deployment.json` with matching DeploymentID/Target
  is advertised as a collectable orphan. That is a real (low-medium) finding, not a guarded
  "no leak" outcome. It is the same root cause card 0428-327 fixes by adding an explicit
  reservation skip, so the census finding is now consistent with — and dispositioned by — the
  live card rather than the earlier misclassification.
- Scope-card / disposition proposals beyond census still belong in akte prose for CODEX
  disposition, not in a product edit: this correction makes the census finding point at card
  0428-327 as the owning card.

## CI RUN WITNESS (product candidate run 45827064336, unrelated to hunt but recorded)

- head 210d5d1056152019389da603831ecd2f450edcac (absorb of develop, w322-0428-249-pr1812gate)
- 54 jobs = 29 success / 9 failure / 16 skipped
- 14 Light gates executed; 6 pass (guided/lifecycle/failure/data-capabilities), 8 fail: full-destroy (docker+podman) = RuntimeAcceptanceError(operator_not_authenticated) + owned runtime evidence unavailable: ValueError (phase=owner-preview); connectivity/policy/reconciliation (docker+podman) = core-installation-not-loadable (runtime image not loaded)
- ci.yml byte-identical between head and develop (git diff empty)

## CLEANLINESS

- /var/tmp worktree only; no product writes, no build.
- before: `git worktree list` => /var/tmp/w322-hunt46-orphans-wt (detached HEAD e62533ee1a)
- after: same worktree, no new containers/volumes/networks/state dirs created (no docker/podman started)
- cleanliness: worktree holds only this akte.md; /var/tmp has no orphan compose project; no daemon pools touched

## END line

END_DONE w322-hunt46-orphans: census complete on develop 5a37ddbd9a; no product leak in reserved-namespace orphan surface; one cosmetic unguarded collect-all (metrics/perses_datasource_lifecycle.go:276-287). Akte via scoped plan PR.
