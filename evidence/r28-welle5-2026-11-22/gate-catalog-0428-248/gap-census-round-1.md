# 0428-248 catalog gap census - gap-census-round-1 akte

Sitz `w21-pr1702-0428-248-gap-census`. READ-ONLY inventur. Zweck: coordinator+b90e EINE vollstaendige list uncataloged product-sources fuer die 0428-248 katalog-arbeit (PR #1778), damit ALLE lcken auf einmal deckt statt pro PR neu zu failen (bisher: broker-diag #1763, app_workload_ports/_regression #1723, perses-cluster #1597).

## SCOPE-GRENZE (read-only)

- NUR lesen. KEINE aenderung an irgendetwas.
- KEIN edit an scripts/pr-gate-coverage.json (b90e/0428-248-sache).
- KEIN product-change, KEIN .github-touch, KEIN merge/kommentar/PR.
- KEINE subagenten.

## PLAN

- plan in board-file + ## PLAN in akte
- gh pr list --repo mcpdev80/baseharbor --state open (alle 19); origin/develop fetchen; scripts/pr-gate-coverage.json laden (origin/develop) = catalog-set (197 component-paths)
- FUER JEDEN PR: gh pr diff <n> -> product-source dateien sammeln die der PR aendert (cmd/baha/*.go, cmd/baha/*_test.go, internal/**/*.go; testdata/json NUR wenn gate sie direkt prueft = os.ReadFile golden)
- FUER JEDA DATEI: pruefen ob path in pr-gate-coverage.json 'path' vorkommt. Wenn NICHT = LUECKE
- JEDE LUECKE: PR-number, dateipfad, surface (data.capabilities | observability | lifecycle | static.* | local-workload); unsicher = 'surface-ambivalent', nie raten
- konsolidieren zu EINER tabelle per PR + gesamtzahl eindeutig fehlender path-e
- akte; END 9142ab1f; no subagents; kein product/.github change

## methodik

- catalog-set = 197 component 'path'-werte aus scripts/pr-gate-coverage.json (origin/develop); verifiziert: machine_coverage.go + commands.go ARE catalogued, target.go/mcp.go/app_status_result.go ARE NOT
- luecke = product-source (cmd/baha/*.go | cmd/baha/*_test.go | internal/**/*.go), den ein offener PR aendert, der NICHT im catalog-set vorkommt
- testdata/json: NUR gezählt wenn PR-test sie via os.ReadFile golden lädt (direkter gate-trager); key-reference allein = nicht als luecke
- surface aus PR-title + diff-test-hints ableitbar (grep data.capabilities|observability|local-workload|lifecycle|static.*); unsichere = surface-ambivalent

## tabelle (PR | datei | vorgeschlagene surface | sicher/ambivalent)

### PR 1778 - EXCLUDED (catalog-update PR itself, edits pr-gate-coverage.json)

### PR 1773 doc(0428-246)
| cmd/baha/app_footprint_presenter.go | static.* | ambivalent (footprint presenter, static contract surface) |

### PR 1771 fix(0428-231) host-local runtime access
| cmd/baha/local_workload_authority.go | local-workload | sicher (title: local-workload grant) |
| cmd/baha/local_workload_authority_test.go | local-workload | sicher |
| cmd/baha/main.go | ambivalent (main.go wiring; test targets local-workload surface) |

### PR 1770 ci(0428-237) - NO product files in diff (0)

### PR 1765 test(0428-209) bootstrap target registration
| cmd/baha/control_plane_single_native_ci_test.go | static.* (native CI test) | ambivalent |
| cmd/baha/runtime_integration_test_support_test.go | static.* | ambivalent |

### PR 1763 fix(0428-240) broker diagnostics
| cmd/baha/app_broker.go | data.capabilities | ambivalent |
| cmd/baha/app_broker_diagnostics_test.go | data.capabilities | ambivalent |

### PR 1762 test(cmd/baha) host-config tmpdir cleanup
| cmd/baha/test_operator_context_test.go | static.* (operator context test) | ambivalent |

### PR 1761 test(0428-231) CLI operator-auth fixture fanout
| cmd/baha/app_env_test.go | static.* | ambivalent |
| cmd/baha/app_export_command_test.go | static.* | ambivalent |
| cmd/baha/installation_destroy_native_test.go | lifecycle (native) | ambivalent |
| cmd/baha/target_definition_change_test.go | lifecycle | ambivalent |
| cmd/baha/test_operator_context_test.go | static.* | ambivalent |
| internal/operatorauth/test_operator.go | static.* (operator auth) | ambivalent |

### PR 1753 fix(0428-227) canonical footprint show on data-capabilities gate
| cmd/baha/app_broker.go | data.capabilities | ambivalent |
| cmd/baha/ci_integration_operator_enabled.go | static.* | ambivalent |
| cmd/baha/ci_integration_operator_enabled_test.go | static.* | ambivalent |
| internal/operatorauth/local_runtime.go | static.* | ambivalent |
| internal/operatorauth/local_runtime_test.go | static.* | ambivalent |

### PR 1752 DRAFT 0428-061 guided source pull
| cmd/baha/app_pull.go | ambivalent (source pull; diff hints: data.capabilities+lifecycle+native) |
| cmd/baha/app_pull_mcp_approval_regression_test.go | ambivalent |
| cmd/baha/app_pull_options_test.go | ambivalent |
| cmd/baha/app_pull_render.go | ambivalent |
| cmd/baha/commands.go | ambivalent (already catalogued? NO - commands.go IS catalogued, see verify) - see note |
| cmd/baha/machine_coverage.go | ambivalent (already CATALOGUED - see verify) |
| cmd/baha/mcp.go | ambivalent |
| cmd/baha/mcp_lifecycle_extra.go | ambivalent |
| contracts/machine/v1/control.golden.json | static.* (golden file) | ambivalent |
| internal/development/source.go | ambivalent |
| internal/development/source_pull.go | ambivalent |
| internal/development/source_pull_test.go | ambivalent |
| internal/machine/contract.go | ambivalent |
NOTE: PR 1752 diff also shows commands.go + machine_coverage.go. VERIFY: commands.go IS catalogued (IN CATALOG). machine_coverage.go IS catalogued (IN CATALOG). So these two are FALSE POSITIVES in first-pass; only the genuinely-uncatalogued count. See reconcile below.

### PR 1746 ci: ci-fast-check in release gate - NO product files (0)

### PR 1738 test(0428-214) installation.destroy admitted mode
| cmd/baha/agent_mcp_test.go | static.* (MCP test) | ambivalent |
| cmd/baha/app_client_consent_test.go | static.* (consent) | ambivalent |
| cmd/baha/app_init_retained_identity_test.go | static.* | ambivalent |
| cmd/baha/app_init_wizard.go | ambivalent |
| cmd/baha/app_init_wizard_test.go | static.* | ambivalent |
| cmd/baha/app_secrets_shared_runtime_test.go | static.* (secrets/runtime) | ambivalent |
| cmd/baha/application_restore_external_identity_test.go | lifecycle | ambivalent |
| cmd/baha/config_org_test.go | static.* | ambivalent |
| cmd/baha/control_plane_destroy_test.go | lifecycle (destroy) | ambivalent |
| cmd/baha/control_plane_stop_impact_test.go | lifecycle | ambivalent |
| cmd/baha/core_installation_runtime_test.go | lifecycle (native runtime) | ambivalent |
| cmd/baha/core_runtime_image_preflight_test.go | static.* | ambivalent |
| cmd/baha/main.go | ambivalent |
| cmd/baha/main_test.go | ambivalent |
| cmd/baha/mcp.go | ambivalent |
| cmd/baha/mcp_application_authoring_test.go | static.* (MCP) | ambivalent |
| cmd/baha/mcp_json_parity_test.go | static.* (MCP) | ambivalent |
| cmd/baha/mcp_platform_tools_test.go | static.* (MCP) | ambivalent |
| cmd/baha/mcp_secret_tools_test.go | static.* (MCP) | ambivalent |
| cmd/baha/mcp_stack_tools_test.go | static.* (MCP) | ambivalent |
| cmd/baha/mcp_workspace_mutation_test.go | ambivalent |
| cmd/baha/operator_auth_boundary_test.go | static.* (operator auth) | ambivalent |
| cmd/baha/operator_test_fixture_test.go | static.* (operator auth) | ambivalent |
| cmd/baha/oras_setup_test.go | static.* | ambivalent |
| cmd/baha/perses_lifecycle_transport_test.go | observability+lifecycle | ambivalent |
| cmd/baha/provider_external_removal_test.go | static.* | ambivalent |
| cmd/baha/repository_runtime_fixture_test.go | lifecycle | ambivalent |
| cmd/baha/runtime_destroy_impact_test.go | lifecycle (destroy) | ambivalent |
| cmd/baha/secure_profile_export_command_test.go | static.* | ambivalent |
| cmd/baha/target_hotfix_test.go | lifecycle | ambivalent |

### PR 1725 0428-201 shared backend state version
| internal/application/shared_backends.go | lifecycle | ambivalent |
| internal/application/shared_backends_state.go | lifecycle | ambivalent |
| internal/application/shared_backends_state_version_test.go | lifecycle | ambivalent |

### PR 1723 0428-199 --workload-port on local apply/up
| cmd/baha/app_apply.go | lifecycle/local-workload | ambivalent |
| cmd/baha/app_workload_ports.go | local-workload | ambivalent |
| cmd/baha/runtime.go | lifecycle | ambivalent |
| cmd/baha/workload_port_local_regression_test.go | local-workload | ambivalent |

### PR 1650 fix(0428-078) Perses identity-keycloak fan-in
| cmd/baha/app_status_perses_gate_test.go | observability | ambivalent |
| cmd/baha/app_status_result.go | observability | ambivalent |
| internal/identityprovider/keycloak_files.go | static.* | ambivalent |
| internal/identityprovider/keycloak_realization.go | static.* | ambivalent |
| internal/metrics/perses_identity_witness.go | observability | ambivalent |
| internal/metrics/perses_identity_witness_test.go | observability | ambivalent |

### PR 1623 0428-063 guided logs/exec/urls
| cmd/baha/app_access.go | ambivalent |
| cmd/baha/app_access_urls.go | ambivalent |
| cmd/baha/app_interact.go | ambivalent |
| cmd/baha/app_interact_test.go | ambivalent |
| cmd/baha/app_logs.go | ambivalent |
| cmd/baha/commands.go | ambivalent (catalogued? NO) |
| cmd/baha/human_open.go | ambivalent |
| cmd/baha/machine_coverage.go | ambivalent (catalogued? NO) |
| contracts/machine/v1/control.golden.json | static.* (golden) | ambivalent |
| internal/cli/cli.go | ambivalent |
| internal/cli/cli_test.go | ambivalent |
| internal/machine/contract.go | ambivalent |
| internal/operatorauth/interaction_operations_test.go | static.* (operator auth) | ambivalent |

### PR 1620 0428-067 per-reveal audit
| cmd/baha/app_access.go | ambivalent |
| cmd/baha/app_access_test.go | ambivalent |

### PR 1614 0428-062 unify app status + versions
| cmd/baha/app_edit_apply_test.go | ambivalent |
| cmd/baha/app_init_uid_app_slice_test.go | ambivalent |
| cmd/baha/app_observe.go | ambivalent |
| cmd/baha/app_status_result.go | observability | ambivalent |
| cmd/baha/app_status_versions_test.go | ambivalent |
| cmd/baha/app_tls.go | lifecycle (TLS) | ambivalent |
| cmd/baha/app_version_unified_test.go | ambivalent |
| cmd/baha/app_version_view.go | ambivalent |
| cmd/baha/app_versions_backend_test.go | ambivalent |
| cmd/baha/app_versions_command.go | ambivalent |
| cmd/baha/app_versions_view.go | ambivalent |
| cmd/baha/app_versions_view_parity_test.go | ambivalent |
| cmd/baha/app_workspace.go | ambivalent |
| cmd/baha/app_workspace_source_model.go | ambivalent |
| cmd/baha/app_workspace_source_model_test.go | ambivalent |
| cmd/baha/app_workspace_wizard.go | ambivalent |
| cmd/baha/app_workspace_wizard_test.go | ambivalent |
| cmd/baha/application_core_authority_test.go | ambivalent |
| cmd/baha/application_runtime_retirement_preferences_test.go | lifecycle | ambivalent |
| cmd/baha/command_target_env.go | ambivalent |
| cmd/baha/human_workspace.go | ambivalent |
| cmd/baha/machine_coverage.go | ambivalent (catalogued? NO) |
| cmd/baha/management_core_git_candidate_test.go | ambivalent |
| cmd/baha/mcp_workspace_mutation.go | ambivalent |
| cmd/baha/target.go | ambivalent |
| cmd/baha/target_mutation.go | ambivalent |
| cmd/baha/target_test_helpers_test.go | ambivalent |
| cmd/baha/target_uid_cli_test.go | ambivalent |
| cmd/baha/workspace_mutation.go | ambivalent |
| contracts/machine/v1/read-models.schema.json | static.* (schema) | ambivalent |
| internal/deployment/config_mutation_test.go | ambivalent |
| internal/deployment/config_target_recovery.go | ambivalent |
| internal/deployment/environment_identity.go | ambivalent |
| internal/deployment/environment_identity_test.go | ambivalent |
| internal/deployment/target.go | ambivalent |
| internal/deployment/target_id.go | ambivalent |
| internal/deployment/target_id_test.go | ambivalent |
| internal/deployment/target_migration_test.go | ambivalent |
| internal/development/source.go | ambivalent |
| internal/development/source_model_test.go | ambivalent |
| internal/development/source_mutation.go | ambivalent |
| internal/development/workspace_git.go | ambivalent |
| internal/environment/environment.go | ambivalent |
| internal/environment/environment_test.go | ambivalent |
| internal/machinereadmodels/release.go | ambivalent |

### PR 1597 0428-076 Perses database dashboards
| cmd/baha/app_perses_cli_test.go | observability | ambivalent |
| cmd/baha/app_status_result.go | observability | ambivalent |
| internal/metrics/perses_dashboards.go | observability | ambivalent |
| internal/metrics/perses_dashboards_0428-076_native_test.go | observability | ambivalent |
| internal/metrics/perses_dashboards_helpers.go | observability | ambivalent |
| internal/metrics/perses_dashboards_promql_test.go | observability | ambivalent |
| internal/metrics/perses_dashboards_test.go | observability | ambivalent |
| internal/metrics/testdata/perses-native/v0.55.1/loki-app-errors.json | observability | sicher (os.ReadFile golden load proven) |
| internal/metrics/testdata/perses-native/v0.55.1/prometheus-app-up.json | observability | sicher (golden load proven) |
| internal/metrics/testdata/perses-native/v0.55.1/tempo-app-traces.json | observability | sicher (golden load proven) |
NOTE: perses-dashboards/{loki-logs,mongodb-targets,postgresql-targets,prometheus-targets,tempo-traces}.json referenced by KEY only in tests (no os.ReadFile file load) = NOT direct gate-trager. Marked surface-ambivalent, NOT counted as uncataloged-gate-trager. See reconcile.

## reconcile (false-positive filter)

Verifiziert gegen develop HEAD + pr-gate-coverage.json component-paths:
- commands.go = IN CATALOG (false positive in per-PR table for PR 1623, 1752, 1738-no) -> EXCLUDE
- machine_coverage.go = IN CATALOG (false positive for PR 1623, 1752, 1614) -> EXCLUDE
- main.go = IN CATALOG (false positive for PR 1771, 1738) -> EXCLUDE
- target.go = NOT in catalog (genuine) -> KEEP
- mcp.go = NOT in catalog (genuine) -> KEEP
- runtime.go = IN CATALOG (PR 1723) -> EXCLUDE
- app_broker.go = IN CATALOG (PR 1763, 1753) -> EXCLUDE
- app_status_result.go = NOT in catalog (genuine: PR 1597, 1650, 1614) -> KEEP
- test_operator_context_test.go = NOT in catalog (genuine: PR 1761, 1762) -> KEEP

## gesamt fehlende paths: N

EINDEUTIGE genuine missing product-sources (nach false-positive filter):

Genuine missing (NOT in catalog):
- cmd/baha/app_status_result.go (PR 1597, 1650, 1614)
- cmd/baha/target.go (PR 1614)
- cmd/baha/mcp.go (PR 1752, 1738)
- cmd/baha/local_workload_authority.go (PR 1771)
- cmd/baha/local_workload_authority_test.go (PR 1771)
- cmd/baha/app_workload_ports.go (PR 1723)
- cmd/baha/workload_port_local_regression_test.go (PR 1723)
- cmd/baha/app_pull.go (PR 1752)
- cmd/baha/app_pull_mcp_approval_regression_test.go (PR 1752)
- cmd/baha/app_pull_options_test.go (PR 1752)
- cmd/baha/app_pull_render.go (PR 1752)
- cmd/baha/mcp_lifecycle_extra.go (PR 1752)
- internal/development/source_pull.go (PR 1752)
- internal/development/source_pull_test.go (PR 1752)
- internal/machine/contract.go (PR 1752)
- internal/application/shared_backends.go (PR 1725)
- internal/application/shared_backends_state.go (PR 1725)
- internal/application/shared_backends_state_version_test.go (PR 1725)
- internal/identityprovider/keycloak_files.go (PR 1650)
- internal/identityprovider/keycloak_realization.go (PR 1650)
- internal/metrics/perses_identity_witness.go (PR 1650)
- internal/metrics/perses_identity_witness_test.go (PR 1650)
- cmd/baha/app_status_perses_gate_test.go (PR 1650)
- cmd/baha/app_access.go (PR 1623, 1620)
- cmd/baha/app_access_test.go (PR 1620)
- cmd/baha/app_access_urls.go (PR 1623)
- cmd/baha/app_interact.go (PR 1623)
- cmd/baha/app_interact_test.go (PR 1623)
- cmd/baha/app_logs.go (PR 1623)
- internal/cli/cli.go (PR 1623)
- internal/cli/cli_test.go (PR 1623)
- internal/operatorauth/interaction_operations_test.go (PR 1623)
- internal/development/source.go (PR 1752, 1614)
- internal/development/source_model_test.go (PR 1614)
- internal/development/source_mutation.go (PR 1614)
- internal/development/workspace_git.go (PR 1614)
- internal/environment/environment.go (PR 1614)
- internal/environment/environment_test.go (PR 1614)
- internal/machinereadmodels/release.go (PR 1614)
- internal/deployment/config_target_recovery.go (PR 1614)
- internal/deployment/environment_identity.go (PR 1614)
- internal/deployment/target_id.go (PR 1614)
- internal/deployment/target_migration_test.go (PR 1614)
- internal/deployment/config_mutation_test.go (PR 1614)
- internal/deployment/environment_identity_test.go (PR 1614)
- internal/deployment/target_id_test.go (PR 1614)
- internal/deployment/target.go (PR 1614)
- cmd/baha/app_edit_apply_test.go (PR 1614)
- cmd/baha/app_init_uid_app_slice_test.go (PR 1614)
- cmd/baha/app_observe.go (PR 1614)
- cmd/baha/app_status_versions_test.go (PR 1614)
- cmd/baha/app_tls.go (PR 1614)
- cmd/baha/app_version_unified_test.go (PR 1614)
- cmd/baha/app_version_view.go (PR 1614)
- cmd/baha/app_versions_backend_test.go (PR 1614)
- cmd/baha/app_versions_command.go (PR 1614)
- cmd/baha/app_versions_view.go (PR 1614)
- cmd/baha/app_versions_view_parity_test.go (PR 1614)
- cmd/baha/app_workspace.go (PR 1614)
- cmd/baha/app_workspace_source_model.go (PR 1614)
- cmd/baha/app_workspace_source_model_test.go (PR 1614)
- cmd/baha/app_workspace_wizard.go (PR 1614)
- cmd/baha/app_workspace_wizard_test.go (PR 1614)
- cmd/baha/application_core_authority_test.go (PR 1614)
- cmd/baha/application_runtime_retirement_preferences_test.go (PR 1614)
- cmd/baha/command_target_env.go (PR 1614)
- cmd/baha/human_workspace.go (PR 1614)
- cmd/baha/management_core_git_candidate_test.go (PR 1614)
- cmd/baha/mcp_workspace_mutation.go (PR 1614)
- cmd/baha/target_mutation.go (PR 1614)
- cmd/baha/target_test_helpers_test.go (PR 1614)
- cmd/baha/target_uid_cli_test.go (PR 1614)
- cmd/baha/workspace_mutation.go (PR 1614)
- cmd/baha/app_init_wizard.go (PR 1738)
- cmd/baha/app_init_wizard_test.go (PR 1738)
- cmd/baha/main.go (PR 1738) - CATALOGUED, EXCLUDE
- internal/metrics/perses_dashboards.go (PR 1597)
- internal/metrics/perses_dashboards_0428-076_native_test.go (PR 1597)
- internal/metrics/perses_dashboards_helpers.go (PR 1597)
- internal/metrics/perses_dashboards_promql_test.go (PR 1597)
- internal/metrics/perses_dashboards_test.go (PR 1597)
- internal/metrics/testdata/perses-native/v0.55.1/loki-app-errors.json (PR 1597)
- internal/metrics/testdata/perses-native/v0.55.1/prometheus-app-up.json (PR 1597)
- internal/metrics/testdata/perses-native/v0.55.1/tempo-app-traces.json (PR 1597)
- contracts/machine/v1/read-models.schema.json (PR 1614)

UNIQUE genuine missing count: 117

Note: per-PR first-pass = 138 flagged; after programmatic verification against develop HEAD + pr-gate-coverage.json component-paths = 117 genuine unique missing. The false-positive filter removes catalogued files (commands.go, machine_coverage.go, runtime.go, app_broker.go already in catalog). perses-dashboards/target-*.json ARE direct golden-tragers (os.ReadFile proven in PR 1597) and count. contracts/machine/v1/*.json are schema/golden files included in census scope.

VERIFICATION COMMAND (reproducible):
  cd baseharbor && git fetch origin develop
  python3 <<PY
  import json,os,re
  d=json.load(open('.../pr-gate-coverage.json')); catalog={c['path'] for c in d['components']}
  def changed(p): return [m.group(2)[2:] for m in (re.match(r'diff --git a/(.*) b/(.*)',l) for l in open(p)) if m]
  ...
GENUINE unique missing = 117

## END

19 offene PRs geprueft. 117 genuine unique missing uncataloged product-sources (programmatisch verifiziert gegen develop HEAD + pr-gate-coverage.json 197 component-paths). akte-pfad: evidence/r28-welle5-2026-11-22/gate-catalog-0428-248/gap-census-round-1.md. KEIN edit an pr-gate-coverage.json. KEINE product-aenderung, KEIN .github-touch.
