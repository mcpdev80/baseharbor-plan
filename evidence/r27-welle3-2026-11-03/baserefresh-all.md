## w102-baserefresh-all — Evidence

ROLLE: Worker (Lane w102). Coord f49a3303. Mechanische basis-aktion: ALLE offenen r27-zweige auf develop f8ef4255 als Vorfahr bringen. Zielrepo baseharbor. develop = f8ef4255 (3 devex-commits).

### Zielzustand / Basis
- origin/develop = f8ef4255 ci(devex): surface nonblocking consumer follow-up in PR checks
- Zielrepo: /home/marcel/dev/baseharbor-ecosystem/baseharbor (Go-Modul github.com/mcpdev80/baseharbor)

### Ergebnis-Tabelle (6er-Tabelle: branch -> neuer head, rc, Konflikt ja/nein)

- Branch 1 work/r27-ci-authority-ab (alt da99cac4) -> 5a5f1b38f5151ef5d0beabfd0f5343f1b58f72e9 | merge rc=0 | Konflikt nein | build ok | push ok | ls-remote verified
- Branch 2 work/r27-native-auth (alt 0958107f) -> 0958107f (UNCHANGED) | merge rc=0 (already up to date) | Konflikt nein | build ok | remote bereits auf f8ef4255 (prior merge 5fee8072) | kein Refresh nötig
- Branch 3 work/r27-profile-codec (alt 73a75b5e) -> d68251ee00e6d23ed6ef83016cc9cc880bdf478f | merge rc=0 | Konflikt nein | build ok | push ok | ls-remote verified
- Branch 4 work/r27-workstation-enrollment (alt 2a4df949) -> 2a4df949 (UNTOUCHED) | SKIP | Konflikt ja (voraussichtlich, contracts/workstationenrollment/v1/**) | w96 aktiv: main-worktree + /tmp/opencode/w90-enroll-wt auf diesem Zweig, staged new internal/workstationenrollment/** + contracts/workstationenrollment/v1/**; merge confliziert auf contracts-path | remote head unverändert 2a4df949 | w96 schließt Zweig selbst | laut Mission NICHT pitchen
- Branch 5 work/w92-team-auth-claim-mapping (alt 1043d12d) -> bfaddb37f4550fb1475af2acfc1070a50d52241f | merge rc=0 | Konflikt nein | build ok | push ok | ls-remote verified
- Branch 6 work/r27-candidate-contract (remote tip 0468a896) -> bed005160a7a178d9358ee3920ded6c43e5096d6 | merge rc=0 | Konflikt nein | build ok | push ok (via explicit SHA, remote tip war stale FF-reading) | ls-remote verified | remote tip 0468a896 = w80/w97 fertige Arbeit (4 eigene Commits, kein weiterer Writer laut Coord); refresh f8ef4255 darauf aufgepfropft, 6 Commits ahead, erster Parent = 0468a896

### Ergebnis-Summary
- refreshed: 5/6 (branch1,3,5,6 NEU refreshed; branch2 war schon auf Basis; branch4 laut Mission Skippet)
- konflikte: branch4 (w96 aktiv, contracts-path) — korrekt übersprungen; keine content-konflikte bei den 4 refreshed zweigen
- PR-Status NIEMALS angefasst (nur force-pushes auf Branch-Köpfe, keine PRs)

### Pre-existing failures (außerhalb Scope, nicht durch Refresh eingeführt)
- internal/telemetry: TestRegisteredOTLPActualConsumerTokenTrustAndClientIdentity, TestRegisteredOTLPDriftBeforeAndDuringNeverVerifies, TestRegisteredOTLPBasicCredentialActuallyAuthenticatesReceiver — schlagen auf ALLEN Zweigen fehl, geprüft auf branch-Head vor merge (da99cac4 / 0468a896) = vorhanden => nicht durch w102 eingeführt.
- internal/externalprovider: TestDiscoverCertificateDirectoryMatchesWildcardAndKey — "certificate directory ... is not a directory" (env-/FS-abhängig), geprüft auf remote tip 0468a896 = vorhanden (PRE_MERGE_RC=1) => nicht durch w102 eingeführt.
- go build ./... auf allen refreshed zweigen rc=0.

### Push-Hinweise
- GitHub Internal Server Error während der Ausführung (mehrfach); nach kurzer Pause erfolgreich.
- branch6: lokaler Ref-Tracking war stale (FF-Rejection trotz erstem-Parent-auf-remote-tip); Push per explizitem SHA (bed00516:work/r27-candidate-contract) erfolgreich. Branch-Schutz NICHT aktiv (gh API 404).

### END
- END_DONE w102-baserefresh: refreshed=5/6 (branch1=5a5f1b38, branch3=d68251ee, branch5=bfaddb37, branch6=bed00516 gepushed+verified; branch2 schon auf Basis) | konflikte=branch4 (w96 aktiv, contracts-path, laut Mission Skippet) | build ok auf allen; pre-existing telemetry+externalprovider-fails out of scope | PR-Status nicht angefasst
- END_LINE in board: END_DONE
