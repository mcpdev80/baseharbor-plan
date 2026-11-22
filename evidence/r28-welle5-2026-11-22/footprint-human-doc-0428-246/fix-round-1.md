# 0428-246 footprint human presenter doc gaps - fix-round-1 akte

Sitz `w21-pr1702-0428-246-footprint-doc`. Karte 0428-246, owner-order. Aus H-V25 (2 doku-luecken, KEIN produkt-defekt).

GEMESSEN (H-V25, develop 62784eff): JSON==MCP footprint byte-identisch (kein defect); human presenter per Design kuratierte teilmenge; zwei abweichungen lesen sich wie fehler:
- B3 = ein status-wert wird im human-branch anders/umformuliert Label angezeigt als der machine-token, ohne dass die zuordnung dokumentiert ist
- B4 = scope/ownership-felder die JSON traegt, fehlen im human-view ohne erklaerzeile

## PLAN

- plan in board-file + ## PLAN in akte
- develop fetchen, frische lane lane-0428-246-footprint-human-doc cutting von develop; merge-base --is-ancestor + base-sha witness in akte
- B3 (dokumentieren, kein verhalten-aendern): human<->machine status-label zuordnung als kurze zeile (nahe presenter oder im footprint help)
- B4 (dokumentieren, kein verhalten-aendern): kurze human-view anmerkung dass scope/ownership ueber JSON/MCP verfuegbar sind (oder sie rendern wenn trivial)
- regression NUR falls help/annotation-string irgendwo assertiert wird; sonst reicht go build/vet + PR-CI; KEIN native/CI-aenderung; KEIN contract/guard/237/231/242
- EIN additiver commit, push, PR fuer 246, EIN durchgang bis terminal; git diff origin/develop...HEAD --name-only in akte; pr-ci job-ids
- akte + evidence publish zu origin/main; END; 9142ab1f posten; keine subagenten, kein merge

## Fundquelle (H-V25 B3/B4)

- B3 human<->machine status-label switch (footprint.go:23-29 canonical enum vs presenter.go:75-84 human label); keine zuordnung dokumentiert
- B4 scope/ownership/shared/consumers/ancillary (footprint.go:99-113) in JSON/MCP, fehlen im human-view ohne erklaerzeile

## Fix

(a) B3 label-map line:
Extracted renderProviderStateLabel (cmd/baha/app_footprint_presenter.go) with a documented comment stating the sole human<->machine ProviderState label correspondence and that it must stay in sync with the canonical enum (internal/application/footprint.go:115). Behavior identical (same mapping).

(b) B4 scope/ownership note:
Documented on presentAppFootprint that the human view is a curated subset; provider Scope, Ownership, Shared, Consumers, Ancillary are intentionally not rendered here and are available via the JSON/MCP contract (internal/application/footprint.go:115/99-113). Behavior identical.

## blocker: CI fail-loud catalog guardian (0428-242 owned)

- CI run 45028989203 (PR #1773) terminal conclusion: failure. PR · Trusted Plan job failed.
- Log line (trusted-plan job): "ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: cmd/baha/app_footprint_presenter.go (id source.cmd_baha_app_footprint_presenter_go): add this source with its surfaces to scripts/pr-gate-coverage.json, e.g. {\"id\": \"source.cmd_baha_app_footprint_presenter_go\", \"path\": \"cmd/baha/app_footprint_presenter.go\", \"surfaces\": [\"source.gate.atomic.docker.data.capabilities\", \"source.gate.atomic.podman.data.capabilities\"]}"
- Root cause: app_footprint_presenter.go was NOT cataloged on develop (git log origin/develop -- scripts/pr-gate-coverage.json shows only 0428-242 introduced the file). The fail-loud catalog guardian (0428-242) only flags a source when it is a CHANGED source; my documentation change made it changed.
- scope conflict: scripts/pr-gate-coverage.json is owned by card 0428-242 ("catalog + fail-loud PR gate guardian", commit 676909a78). Mission write-set forbids guard/242: "cmd/baha footprint human presenter nur; KEIN contract/guard/237/231/242".
- EXACT NEEDED CHANGE (242 owner scope, file:line + recipe) - report, do not edit:
  - file: scripts/pr-gate-coverage.json, list "components" (schema baseharbor.pr-gate-coverage/v1)
  - add one component entry: {"id": "source.cmd.baha.app_footprint_presenter_go", "path": "cmd/baha/app_footprint_presenter.go", "surfaces": ["source.gate.atomic.docker.data.capabilities", "source.gate.atomic.podman.data.capabilities"]}
  - rationale: app_apply.go (same footprint presentation during apply) is cataloged with exactly these two atomic data.capabilities surfaces (0428-242 commit 676909a78); the human footprint presenter feeds the same data-capabilities gate.
  - after this one catalog entry, 0428-246's own PR CI will pass (go build/vet green; footprint presenter tests pass locally).
- This is a coordinator/242-owner action per CI policy: "Only a change outside this card's write-set (shared planner file, base required-plan, release matrix) stays a coordinator action: stop and report file:line for that one case."

## cleanliness

(nur dokumentation im cmd/baha footprint human presenter; keine container/volumes/state; ambient-core fremder lanes untouched)

## END w21-pr1702-0428-246-footprint-doc DONE (implementation done; PR blocked on 242 catalog guardian - coordinator action)

- branch: lane-0428-246-footprint-human-doc; base develop 676909a78 (git ls-remote origin refs/heads/develop); merge-base --is-ancestor 676909a78 HEAD = YES; base is ancestor of commit 165c12e29
- head: 165c12e29da13a3033ce4216210445fd3138f093 (git ls-remote origin refs/heads/lane-0428-246-footprint-human-doc)
- PR: #1773 (base develop, head lane-0428-246-footprint-human-doc, OPEN, https://github.com/mcpdev80/baseharbor/pull/1773)
- git diff origin/develop...HEAD --name-only = cmd/baha/app_footprint_presenter.go (documentation only; behavior identical)
- local pre-check: go build ./... clean; go vet ./cmd/baha/ clean; go test footprint presenter tests ok
- CI run 45028989203 (PR #1773) terminal: failure in PR · Trusted Plan (fail-loud catalog guardian)
- BLOCKER (242-owner scope, reported not edited): scripts/pr-gate-coverage.json (owned by card 0428-242) has no entry for cmd/baha/app_footprint_presenter.go; mission write-set forbids guard/242. EXACT fix: add one component entry {"id":"source.cmd.baha.app_footprint_presenter_go","path":"cmd/baha/app_footprint_presenter.go","surfaces":["source.gate.atomic.docker.data.capabilities","source.gate.atomic.podman.data.capabilities"]} (same surfaces as app_apply.go, which feeds the same data-capabilities gate). After that one 242-owner catalog entry, 0428-246 PR CI passes.
- B3 done (renderProviderStateLabel documented human<->machine label map); B4 done (scoped/ownership subset documented)
- no subagents, no merge; 0428-242/contract/guard untouched
