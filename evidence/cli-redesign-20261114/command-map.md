# Proposed CLI command mapping

Snapshot derived from Core `b3014008`, CLI/internal source unchanged through `cd77e20e`. All proposed new names are pending the contract task; `/` indicates context-specific routing, not equivalent aliases. The existing contract and safety behavior are not replaced by this table. See [code-entry-index](code-entry-index.md). Root `destroy` means full installation, and target `delete` is detach/recovery; do not confuse them.

| Old command | Proposed destination |
| --- | --- |
| `baha new` | `baha guided task selection → app setup new / target new / platform stack new / platform provider author init / app setup init` |
| `baha init` | `baha app setup init` |
| `baha list` | `baha app list` |
| `baha up` | `baha app up / platform local up` |
| `baha status` | `baha app status / platform local status` |
| `baha inspect` | `baha app setup inspect` |
| `baha plan` | `baha app plan` |
| `baha doctor` | `baha app doctor / platform local doctor` |
| `baha update` | `baha system update` |
| `baha backup` | `baha app data backup` |
| `baha restore` | `baha app data restore` |
| `baha destroy` | `baha platform destroy` |
| `baha down` | `baha app down / platform local down` |
| `baha open` | `baha app urls` |
| `baha logs` | `baha app logs` |
| `baha provider` | `baha platform provider + platform provider author` |
| `baha stack` | `baha platform stack` |
| `baha workspace` | `baha app source` |
| `baha target` | `baha target` |
| `baha use` | `baha context use` |
| `baha node` | `baha platform node` |
| `baha onboard` | `baha platform remote connect / access user invite / access tenant init` |
| `baha workstation` | `baha access workstation` |
| `baha user` | `baha access user` |
| `baha dev` | `baha system domain / credentials / hosts / cleanup` |
| `baha config` | `baha platform organization / system shell prompt` |
| `baha shell-init` | `baha system shell init` |
| `baha policy` | `baha app policy` |
| `baha access` | `baha access grant` |
| `baha agent` | `baha system agent` |
| `baha mcp` | `baha system mcp` |
| `baha serve` | `baha platform local serve` |
| `baha app` | `baha app` |
| `baha connect` | `baha app connection add` |
| `baha disconnect` | `baha app connection remove` |
| `baha connections` | `baha app connection list` |
| `baha openbao` | `baha platform secrets` |
| `baha trust` | `baha system trust` |
| `baha login` | `baha access login` |
| `baha logout` | `baha access logout` |
| `baha whoami` | `baha access whoami` |
| `baha version` | `baha system version` |
| `baha tui` | `baha system tui` |
| `baha completion` | `baha system shell completion` |
| `baha provider add` | `baha platform provider add` |
| `baha provider list` | `baha platform provider list` |
| `baha provider inspect` | `baha platform provider show` |
| `baha provider verify` | `baha platform provider verify` |
| `baha provider remove` | `baha platform provider remove` |
| `baha provider init` | `baha platform provider author init` |
| `baha provider test` | `baha platform provider author test` |
| `baha stack list` | `baha platform stack list` |
| `baha stack show` | `baha platform stack show` |
| `baha stack create` | `baha platform stack new` |
| `baha workspace init` | `baha app setup init / app source add` |
| `baha workspace map` | `baha app source path` |
| `baha workspace show` | `baha app source list` |
| `baha workspace resolve` | `baha app source component list` |
| `baha workspace status` | `baha app source list (Statusdetails)` |
| `baha workspace update` | `baha app pull` |
| `baha target list` | `baha target list` |
| `baha target show` | `baha target show` |
| `baha target policy` | `baha target policy` |
| `baha target create` | `baha target new` |
| `baha target delete` | `baha target remove` |
| `baha target activate` | `baha context use` |
| `baha target deactivate` | `baha context clear` |
| `baha node add` | `baha platform node add` |
| `baha node connect` | `baha platform node connect` |
| `baha node list` | `baha platform node list` |
| `baha node status` | `baha platform node status` |
| `baha node disconnect` | `baha platform node disconnect` |
| `baha workstation new` | `baha access workstation new` |
| `baha workstation list` | `baha access workstation list` |
| `baha workstation revoke` | `baha access workstation revoke` |
| `baha user list` | `baha access user list` |
| `baha user offboard` | `baha access user offboard` |
| `baha dev hosts` | `baha system hosts` |
| `baha dev cleanup` | `baha system cleanup` |
| `baha dev credentials` | `baha system credentials` |
| `baha dev domain` | `baha system domain` |
| `baha config prompt` | `baha system shell prompt` |
| `baha config organization` | `baha platform organization` |
| `baha policy check` | `baha app policy check` |
| `baha policy explain` | `baha app policy explain` |
| `baha access assign` | `baha access grant assign` |
| `baha access offboard` | `baha access grant remove` |
| `baha agent describe` | `baha system agent describe` |
| `baha mcp serve` | `baha system mcp serve` |
| `baha app new` | `baha app setup new` |
| `baha app workspace` | `baha app source` |
| `baha app init` | `baha app setup init` |
| `baha app create` | `baha app setup new` / `baha app setup init`; technische Operation `app.create` erhalten |
| `baha app list` | `baha app list` |
| `baha app show` | `baha app status` |
| `baha app plan` | `baha app plan` |
| `baha app preflight` | `baha app plan` |
| `baha app edit` | `baha app setup edit` |
| `baha app footprint` | `baha app plan` |
| `baha app inspect` | `baha app setup inspect` |
| `baha app apply` | `baha app up` |
| `baha app backup` | `baha app data backup` |
| `baha app restore` | `baha app data restore` |
| `baha app env` | `baha app data env / app data services` |
| `baha app sql` | `baha app data sql` |
| `baha app cache` | `baha app data cache` |
| `baha app creds` | `baha app data services` |
| `baha app secure-profile` | `baha app data export` |
| `baha app logs` | `baha app logs` |
| `baha app shell` | `baha app exec` |
| `baha app exec` | `baha app exec` |
| `baha app update` | `baha app pull --up` |
| `baha app tls` | `baha app data tls` |
| `baha app status` | `baha app status` |
| `baha app doctor` | `baha app doctor` |
| `baha app down` | `baha app down` |
| `baha app stop` | `baha app down` |
| `baha app up` | `baha app up` |
| `baha app destroy` | `baha app setup destroy` |
| `baha app secret` | `baha app data secrets` |
| `baha app runtime-identity` | `baha app data secrets identity` |
| `baha app evidence` | `baha app data export` |
| `baha app version` | `baha app status / app source list` |
| `baha app versions` | `baha app list --all-targets / app status` |
| `baha app prune` | `baha app setup prune` |
| `baha openbao status` | `baha platform secrets status` |
| `baha openbao bootstrap` | `baha platform secrets bootstrap` |
| `baha openbao unseal` | `baha platform secrets unseal` |
| `baha openbao rotate` | `baha platform secrets rotate` |
| `baha trust status` | `baha system trust status` |
| `baha trust export` | `baha system trust export` |
| `baha trust install` | `baha system trust install` |
| `baha trust uninstall` | `baha system trust uninstall` |
| `baha target policy show` | `baha target policy show` |
| `baha target policy set` | `baha target policy edit` |
| `baha config organization set` | `baha platform organization set` |
| `baha config organization show` | `baha platform organization show` |
| `baha config organization check` | `baha platform organization check` |
| `baha config organization update` | `baha platform organization update` |
| `baha app workspace init` | `baha app setup init / app source add` |
| `baha app workspace map` | `baha app source path` |
| `baha app workspace show` | `baha app source list` |
| `baha app workspace resolve` | `baha app source component list` |
| `baha app workspace status` | `baha app source list (Statusdetails)` |
| `baha app workspace update` | `baha app pull` |
| `baha app footprint show` | `baha app plan` |
| `baha app secure-profile export` | `baha app data export` |
| `baha app tls update` | `baha app data tls (Wizard/Flags)` |
| `baha app secret set` | `baha app data secrets set` |
| `baha app secret list` | `baha app data secrets list` |
| `baha app secret delete` | `baha app data secrets delete` |
| `baha app secret tls-set` | `baha app data secrets set (TLS-validiertes Paar)` |
| `baha app runtime-identity rotate` | `baha app data secrets identity rotate` |
| `baha app runtime-identity revoke` | `baha app data secrets identity revoke` |
| `baha prompt` | `baha system shell prompt (intern)` |
| `baha __complete` | `baha system shell completion (intern)` |
| `baha new target` | `baha target new` |
| `baha new provider` | `baha platform provider author init` |
| `baha new workspace` | `baha app setup init / app source` |
| `baha onboard --invite` | `baha access user invite` |
| `baha onboard --import` | `baha platform remote connect` |
| `baha onboard --init-tenant` | `baha access tenant init` |
| `baha login --init-tenant` | `baha access tenant init` |
| `baha new application / app` | `baha app setup new` |
| `baha new stack / development-stack` | `baha platform stack new` |
| `baha access --assign / --offboard` | `baha access grant assign / remove` |
