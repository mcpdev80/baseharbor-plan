## PLAN — fmtfix

- 1) origin/develop im eigenen Worktree holen (`/workers/worktrees/fmtfix`)
- 2) gofmt -w auf NUR cmd/baha/podman_doctor_checks.go (nur Import-Einsortierung)
- 3) go build ./cmd/baha + go vet ./cmd/baha
- 4) Branch work/fmtfix, 1 Commit 'style: gofmt podman_doctor_checks.go', push
- 5) PR gegen develop (Labels/Body minimal), PRSC beobachten bis terminal
- 6) Evidence verifizieren; Karte t-20260427-* NICHT anfassen

## Repo-Rule Compliance
- Scope: EINE Datei, rein gofmt, kein goimports/Umstellung. Mission STOP eingehalten.
- PRSC (CI Fmt gate) wird als Pflicht-Check über PR-Self-Checks beobachtet.

## End line
END_DONE / END_BLOCKED — see handoff post.
