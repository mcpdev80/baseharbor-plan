---
id: t-20261114-r28-cli2-app-interact
card_number: "0428-063"
card_short_title: "Guide app logs exec and urls"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: Codex (maintainer, uebernommen) / coord (zeugnis)
kanban_status: active
kanban_lane: active
kanban_summary: "Guide app logs exec and urls. Follow the owner working brief, command mapping and code entry index; revalidate current develop…"
kanban_title: 0428-063 · Guide app logs exec and urls
priority: high
depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-identity-secrets, t-20261114-r28-cli2-source-model]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1623]
sources: []
blocker: ""
wait_reason: "remaining dependency is the develop-height broker readiness defect 0428-237"
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1623", "https://github.com/mcpdev80/baseharbor/actions/runs/45001383922"]
---
 HEAD
wait_reason: ""
=======
wait_reason: "remaining dependency is the develop-height broker readiness defect 0428-237"

 547b6a928 (kanban: t-20261114-r28-cli2-app-interact -> wait)

ZEUGNIS ZUR UEBERNAHME (gemessen, damit die karte den stand traegt): PR 1623 state OPEN, DRAFT (draft hat keine required checks), base develop, head 4cbf92960cb, rueckstand 586 commits gegen develop 8629450ef3c. ANCESTRY IN ORDNUNG, gemessen: die beiden spitzen aus 0428-057 (8963efd8a, bb5bb3676) SIND in develop - ihr inhalt ist laengst angekommen, die verknotungen 4463ac617/e9c313c5a sind eigene branch-verknotungen des kandidaten. Diff gegen betrifft cmd/baha/app_access.go, app_access_urls.go, app_interact*.go, app_logs.go, commands.go, human_open.go, machine_coverage.go, contracts/machine/v1/control.golden.json, docs/cli/applications.md. SORGFALT: weil cmd/baha betroffen ist, wuerden nach einem hop die nativen data-capabilities-reihen AUSGEFUEHRT und treffen den broker-defekt auf develop-Hoehe (0428-237) - zeuge PR 1762 durchgang 45001383922 (native docker 137144598339 FAIL 2m03s, podman 137144598342 FAIL 503 not_ready 4m57s). Revalidierung und read-only-befunde sind sofort richtig; terminal gruen erst nach 237. Keine meiner lanen schreibt an diesem branch - abgestimmt wie besprochen.
