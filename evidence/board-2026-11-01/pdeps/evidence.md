# pdeps — Dependabot Alert-Raumung Evidence

## PLAN

1. Dependabot Alerts erfassen (gh api repos/mcpdev80/baseharbor/dependabot/alerts)
2. PR #1160 go-jose/v4 Bump prüfen: existiert offener Bump-Zweig? Falls ja: reben + push; falls nein/veraltet: selbst go.mod/go.sum auf aktuelle go-jose/v4 Patches bringen
3. go build ./... && go test ./... lokal im Worktree; PR Selected Checks bis terminal
4. Alert-Code-Scan-Alt prüfen; falls nicht Bump-deckend: END_BLOCKED mit Alert-IDs

## END_DONE

<!-- filled on completion -->
