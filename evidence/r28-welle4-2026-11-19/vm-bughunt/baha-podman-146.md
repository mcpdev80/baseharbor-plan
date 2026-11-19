## PLAN

- Set up: claim baha-podman vm-lock, verify podman 5.7.0 reachable and clean, clone baseharbor to /tmp against https://github.com/mcpdev80/baseharbor.git, fetch develop-desk stand (HEAD 7ee6f817, 1019190d8 confirmed ancestor)
- Read perses lifecycle (enable/status/disable/remove), ownership-safe remove seam, and destructive-consent i18n (EN 'Warning' / DE 'Warnung', abort-path vs confirm-path)
- Test 1: enable -> status -> disable -> remove on one application; verify ownership evidence preserved and 'remove' refuses when a foreign object holds the same name (ownership-safe, not last-writer-wins)
- Test 2: abort an enable (host middleware gone / network busy) and inspect remaining partial state; test whether disable/remove are still possible afterwards (partial-state case)
- Test 3: destructive commands in both languages; verify correct locale marker (EN 'Warning', DE 'Warnung') and that the abort path yields the same text as the confirm path (deviation = UX/doc finding with file:line)
- Test 4: guided rootless bootstrap; verify it reaches a runnable state or that a step is missing from the docs (undocumented step = finding)
- Write akte to baseharbor-plan/evidence/r28-welle4-2026-11-19/vm-bughunt/baha-podman-146.md; ## PLAN as numbered list without markdown checkboxes; findings sorted by severity with command-accurate repro + file:line; 'cleanliness:' line
- Publish evidence (fetch + rebase origin/main, ls-remote witness, paste origin/main proof), render + check + board publish
- Release vm-lock; compose DOWN witness; END post
