# fix-r11 — l14-profile-bindwording

## PLAN

- [ ] Eigenes worktree anlegen (fetch origin work/r27-profile-contract, worktree add /tmp/opencode/l14-profile-bind-wt)
- [ ] ÄNDERUNG 1 EN: docs/spec/credential-access-v1.md — EnrollDevice-Satzteil ersetzen
- [ ] ÄNDERUNG 2 DE: docs/de/spec/credential-access-v1.md — deutscher Satzteil ersetzen
- [ ] Prüfpunkte: grep counts, diff --name-only, merge-base develop, go build + go test
- [ ] Push auf work/r27-profile-contract, ls-remote == head
- [ ] Evidence + codeman agent post END_DONE

## Repo-Regel-Konformität

- Mikro-Aufgabe, Scope strikt auf die zwei credential-access-v1.md Dateien begrenzt.
- Nichts wird umformuliert; nur der beschlossen替换替换替换 replacement text wird eingesetzt.
- Kein force-push, keine run-logs. Nur gezieltes `git add` der zwei Dateien.

## Evidence (nachweis)

- EN old `installation ID, pinned CA`: working tree count 0 (git grep vs HEAD = 1, i.e. phrase absent in worktree) ✓
- EN new `neither reads nor binds`: present, line 198 ✓
- DE old `Installations-ID, pinned CA`: working tree count 0 ✓
- DE new `liest und bindet es nicht`: present, line 200 ✓
- `git diff --name-only` vs 03f51437 = exactly `docs/de/spec/credential-access-v1.md`, `docs/spec/credential-access-v1.md` ✓
- `git merge-base --is-ancestor develop work/r27-profile-contract` = exit 0 (develop is ancestor) ✓
- `go build ./...` = exit 0 ✓
- `go test ./contracts/managementaccess/v1` = ok (0.056s) ✓
- push `03f51437..775f7a23 work/r27-profile-contract` (no run-logs, no force-push) ✓
- ls-remote `775f7a2355fbddd56a196b704f021e635e223228` == local HEAD ✓

## END

DONE — fix-r11 applied, verified, pushed. candidate SHA 775f7a2355fbddd56a196b704f021e635e223228

