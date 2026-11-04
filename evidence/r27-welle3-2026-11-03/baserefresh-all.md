## w102-baserefresh-all — Evidence

ROLLE: Worker (Lane w102). Coord f49a3303. Mechanische basis-aktion: ALLE offenen r27-zweige auf develop f8ef4255 als Vorfahr bringen. Zielrepo baseharbor. develop = f8ef4255 (3 devex-commits).

### Zielzustand / Basis
- origin/develop = f8ef4255 ci(devex): surface nonblocking consumer follow-up in PR checks
- Zielrepo: /home/marcel/dev/baseharbor-ecosystem/baseharbor (Go-Modul github.com/mcpdev80/baseharbor)
- Alle 6 r27-zweige waren Uralte-Basis (develop NICHT Vorfahr) außer branch 2; merge erzeugte je 1 neuen base-commit.

### Ergebnis-Tabelle (branch -> neuer head, rc, Konflikt ja/nein)

- Branch 1 work/r27-ci-authority-ab (alt da99cac4) -> 5a5f1b38f5151ef5d0beabfd0f5343f1b58f72e9 | merge rc=0 | Konflikt nein | build ok | push ok | ls-remote verified
- Branch 2 work/r27-native-auth (alt 0958107f) -> 0958107f (UNCHANGED) | merge rc=0 (already up to date) | Konflikt nein | build ok | remote bereits auf f8ef4255 (prior merge 5fee8072) | kein Refresh nötig
- Branch 3 work/r27-profile-codec (alt 73a75b5e) -> d68251ee00e6d23ed6ef83016cc9cc880bdf478f | merge rc=0 | Konflikt nein | build ok | push ok | ls-remote verified
- Branch 4 work/r27-workstation-enrollment (alt 2a4df949) -> SKIP | Konflikt JA (voraussichtlich) | w96 aktiv: main-worktree + /tmp/opencode/w90-enroll-wt auf diesem Zweig, staged new internal/workstationenrollment/** + contracts/workstationenrollment/v1/**; merge confliziert auf contracts-path | remote head unverändert 2a4df949 | w96 schließt Zweig selbst | laut Mission NICHT pitchen
- Branch 5 work/w92-team-auth-claim-mapping (alt 1043d12d) -> bfaddb37f4550fb1475af2acfc1070a50d52241f | merge rc=0 | Konflikt nein | build ok | push ok | ls-remote verified
- Branch 6 work/r27-candidate-contract (alt 0468a896 remote) -> remote MID-REFRESH | CANNOT push | divergent: remote 0468a896 hat 4 eigene Commits (488a39e6 runtime --confirm-candidate fix + ece31b80 test + 4ffc3151 chore + 0468a896 merge), meine Linie 0c28eebf würde diese orphanen | merge rc=0 (lokal, content-only), build ok | kein Push, kein Force | Frage an Owner

### Pre-existing failures (außerhalb Scope, nicht durch Refresh eingeführt)
- internal/telemetry: TestRegisteredOTLPActualConsumerTokenTrustAndClientIdentity, TestRegisteredOTLPDriftBeforeAndDuringDeliveryNeverVerifies, TestRegisteredOTLPBasicCredentialActuallyAuthenticatesReceiver schlagen auf ALLEN Zweigen fehl — geprüft auf branch-Head vor merge (da99cac4) = vorhanden => nicht durch w102 eingeführt. Build (go build ./...) auf allen Zweigen rc=0.

### Push-Hinweise
- GitHub Internal Server Error während der Ausführung (4×); nach kurzer Pause jeweils erfolgreich. Nicht reproduzierbar als lokaler Fehler.

### END
- END_BLOCKED w102-baserefresh: refreshed=3/6 (branch1/3/5 gepushed, branch2 bereits auf Basis) | konflikte=branch4 (w96 aktiv, contracts-path) + branch6 (remote mid-refresh, divergence) | 3/6 fertig; branch4 skip laut Mission; branch6Owner-Entscheidung nötig — kein Push möglich ohne Orphanen von Remote-Work
- NÄCHSTER TRIGGER: Owner-Entscheidung branch6 (Force-push meiner Refresh-Linie gegen Remote-Rest-Arbeit? oder andere Linie); nach w96-Freigabe branch4 neu dispatchen
