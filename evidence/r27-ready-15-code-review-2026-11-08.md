# v0.4.27 — 15 Ready cards against develop (2026-11-08)

Source snapshot: `mcpdev80/baseharbor/develop` `b73a13a909b2d7b811d6956b3bdaf93f17b80454`. Only release v0.4.27 Ready cards, no Closed task lifecycle changes. This is a source-based triage, **not** a claim that all fifteen scenarios passed on a runtime.

| Card | Source evidence / finding | Triage |
| --- | --- | --- |
| 0427-138 EOF cancel | `cmd/baha/app_new_wizard.go` has `appNewAbortOnEOF`, mode/confirm EOF handling and existing pre-consent regression, but every interactive prompt is not independently covered | Ready, needs full prompt matrix |
| 0427-139 Names and reserved words | `runAppNewWizard` silently called `slugifyAppName` on raw name; no navigation keyword check | **Claimed** in PR [#1465](https://github.com/mcpdev80/baseharbor/pull/1465), add visible result + reserved-word regression |
| 0427-140 Create-only init | `cmd/baha/app_new.go` suggested `baha up` immediately; Wizard create-only path in `application_provider_preferences.go` likewise | **Claimed** in PR #1465, explicit init/up instructions and tests |
| 0427-141 Quick-init diagnosis | `manifestFromDetectedProject` returned a generic no-requirements message and no app-plan dry-run hint | **Claimed** in PR [#1466](https://github.com/mcpdev80/baseharbor/pull/1466), diagnostic + test |
| 0427-142 Success/Next and yes/no | Headless and Wizard create-only messages differed; `promptYesNo` still returns `fmt.Errorf` on malformed input | Ready; #1465 reduces output divergence, but **not** entire acceptance |
| 0427-143 Needs TUI | `appNewSelectionTerminal.View` prints `P` while `Update` accepts `p`; `choicesForSelection` can propagate errors. Four separate UI checks required | Ready, focused TUI patch/tests |
| 0427-144 Foreign records | `cmd/baha/app_wizard_controller.go` provider choice refresh and `internal/application` state resolution involved; the two-app foreign-record acceptance remains unproven | Ready, requires stateful regression |
| 0427-145 Raw prompt SIGINT | Linux `path_prompt_linux.go` disables ISIG, intercepts Ctrl-C as `context.Canceled`; terminal restore is deferred, but no explicit Interrupted message or PTY signal regression evidenced | Ready, needs PTY regression |
| 0427-146 Docker network pool | Resource/network creation errors originate in runtime paths; no verified pool-exhaustion guidance or synthetic network error regression in this review | Ready, requires targeted error reproduction |
| 0427-147 Orphan lock | Lifecycle lock ownership and status need a fake-live-holder regression; no evidence of process PID/state in error in this review | Ready, needs lock fixture |
| 0427-148 Ambiguous list | `cmd/baha/commands.go` top-level `baha list` intentionally selects one Target, and `target_list_ambiguity_test.go` covers discovery separately; help lacked explicit target selection instructions | **Claimed** in PR #1466, keep fail-closed and explain recovery |
| 0427-149 Name collision | `internal/application/identity_resolution.go` validates authoritative identities, but duplicate registration and cleanup across existing UUIDs is broader than a help-only change | Ready, registry/lifecycle integration |
| 0427-150 Stale provider edit | Provider impact/registry refresh needs a state-only foreign-app fixture; not proven resolved by current policy checks | Ready, lifecycle integration |
| 0427-151 Edit surface nits | Four distinct user-facing symptoms (help/pipe, missing parent directory, Podman display, init loop); no all-four acceptance proof | Ready, split by bounded code owner if implementation starts |
| 0427-152 Destroy data root | `cmd/baha/runtime_destroy_all.go` performs installation/owner-scoped destruction; acceptance specifically requires recovery of owned Core from persisted data roots and foreign preservation, not proven by generic destroy test | Ready, ownership-critical integration |

## Work ownership / CI

- Shared product PR #1465: 0427-139 + 0427-140 (partial shared output improvement for 0427-142).
- Shared product PR #1466: 0427-141 + 0427-148.
- The other eleven cards have **no new worker claim** from this review; existing reservations stay intact.
- CI for both PRs must pass exact source heads; do not merge solely because build or ordinary Go units passed.
- Before any closure record exact merged SHA, required runtime checks where applicable, `resolution: accepted`, immutable evidence URL; regenerate `plan.py render && plan.py check`.
