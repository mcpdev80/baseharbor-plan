# Direct agent entry points completed

All five active repositories now have root `AGENTS.md`, root `CLAUDE.md` importing it, and `.github/copilot-instructions.md` following it. Existing project engineering instructions are preserved; consumer contributor guides state the active planning authority. README and product code are unchanged.

Agents must read the current planning instructions and assigned task, follow ownership before implementation, and update/push status, blockers, PR/source SHA, actual verification and handoff in the task note. Acceptance remains with the Maintainer. Source GitHub issues retain discussion/history only.

| Merged PR | Merge SHA |
| --- | --- |
| [baseharbor#939](https://github.com/mcpdev80/baseharbor/pull/939) | `21caece423956450679080aff25614c623f46fae` |
| [baseharbor-plan#2](https://github.com/mcpdev80/baseharbor-plan/pull/2) | `12196b1a34eb28554076db2aed2511a6e794fcc8` |
| [baseharbor-demo#115](https://github.com/mcpdev80/baseharbor-demo/pull/115) | `a92347900ed4d1015d9bcde3d265cf9326664a40` |
| [baseharbor-console#6](https://github.com/mcpdev80/baseharbor-console/pull/6) | `4724d9962486de5c9f4d226a8a27edcaf8da2fcc` |
| [baseharbor-node-connector#7](https://github.com/mcpdev80/baseharbor-node-connector/pull/7) | `813f08a307f2357f2e16ae9307ea247186ea7dda` |

Verification: all three instruction files independently found in the actual target-branch tree of every repository after merge; relative instruction/import targets checked before publication. Planning PR #2 validation passed; Connector PR #7 source check passed. Native transport/enrollment jobs were skipped for this documentation-only change and are not claimed as runtime evidence.

The 86 migrated planning issues remain closed with preserved original text and destination references. Renovate #889 remains external tooling. No permanent issue deletion was performed; source links remain usable.

Outstanding external actions: real Obsidian UI acceptance and retiring BaseHarbor Project #4. Neither is claimed complete; ai-coding-system Project #1 is outside scope.
