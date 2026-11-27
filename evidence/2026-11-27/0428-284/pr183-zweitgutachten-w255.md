# Zweitgutachten: baseharbor-demo PR #183

## Umfang und Belege

- Rolle: unabhängiges, read-only Review. Kein PR- oder Branch-Schreibzugriff, kein Merge, kein Push und keine lokalen Tests.
- Geprüfter Head: `e3ae7008b938ea58f0f4285da68f121ba60a22c9`.
- PR: https://github.com/mcpdev80/baseharbor-demo/pull/183 — OPEN, Base `develop`, Head stimmt mit dem geprüften SHA überein.
- Remote-Witness: `git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/pull/183/head refs/heads/develop` ergab `e3ae7008b938ea58f0f4285da68f121ba60a22c9 refs/pull/183/head` und `58ac70679efe5f7e95bd47d602841704fb9ffa67 refs/heads/develop`.
- SHA-genauer Vergleich: `git diff 58ac70679efe5f7e95bd47d602841704fb9ffa67...e3ae7008b938ea58f0f4285da68f121ba60a22c9 --name-status` enthält ausschließlich `M tests/guided/drive.py` und `M tests/guided/test_consent_capture.py`. Merge-base ist genau `58ac70679efe5f7e95bd47d602841704fb9ffa67`.
- Hosted run [46045731548](https://github.com/mcpdev80/baseharbor-demo/actions/runs/46045731548): `workflow_dispatch`, `completed/success`, exakter Head `e3ae7008b938ea58f0f4285da68f121ba60a22c9`.
- Vergleichsakten auf Plan-main: `evidence/2026-11-27/0428-284/pr183-r10-verdict-w267.md` und `evidence/2026-11-27/0428-284/pr183-r11-verdict-w267.md`; Implementiererakte: `coordinator/evidence-staging/2026-11-27/pr183-r11-w392.md`.

## Befund 1 — TRAEGT

`tests/guided/drive.py:283-298` beschreibt den Helper-Vertrag und ein mögliches Log-Suffix. Der direkte Test in `tests/guided/test_consent_capture.py:1082-1131` schreibt jedoch selbst ein künstliches Log mit einem Suffix, setzt einen kürzeren Capture-Prefix und ruft `reconcile_capture_from_log` direkt auf. Er prüft damit Append-once und Idempotenz des Helpers unter einer konstruierten Vorbedingung, nicht dass `run_tty` diesen Zustand auf dem Produktionspfad tatsächlich herstellt oder die Reconciliation dort benötigt.

Der Produktionsaufruf in `drive.py:509-529` ist vorhanden und liest nach Flush/fsync das Log ab `bytes_read`. Beide Leseschleifen erhöhen `bytes_read` synchron zu den gelesenen Chunks und schreiben die Chunks auch in `capture_buffer`. Die Tests belegen keinen nichtleeren Rest an diesem Aufruf. Die Gleichheit von Log und Transcript im Test 25 kann bereits durch die normalen Leseschleifen erfüllt sein; sie beweist keine Ausführung mit einem ungelesenen Tail.

## Befund 2 — TRAEGT

`tests/guided/test_consent_capture.py:933-936` initialisiert `drained["final_drain_chunks"]` und hängt Hook-Chunks daran an. Im geprüften Test werden diese Werte danach nicht gelesen oder asserted. Die betreffenden Laufzeitassertions bei `:942-974` prüfen Digest-Präsenz/-Anzahl und Log-Transcript-Gleichheit, nicht die Hook-Beobachtung. Die einzige weitere Verwendung des Puffernamens ist die Initialisierung und das Append; die Kommentare bei `:975-1023` ersetzen keine Assertion.

Zudem hält derselbe Kommentarblock fest, dass der Digest im Main-Loop gelesen wird und `FINAL_DRAIN_CHUNKS == 0` ist (`:985-989`), womit die Digest-Assertions gerade keine Ausführung des Final-drain-Hooks zeigen. `test_26` (`:1082-1131`) testet weiterhin nur den Helper separat. Damit fehlt sowohl die direkte Hook-Beobachtungsassertion als auch ein tatsächlich darauf beruhender negativer Kontrollfall.

## Empfehlung an Owner: r12 erforderlich; nicht freigeben

Beide Befunde tragen auf dem exakten Head. Der erfolgreiche Dispatch-Run belegt die Ausführung des gewählten Hosted-Jobs, behebt aber die inhaltlichen Testlücken nicht. Eine Freigabe ist nach diesem Review nicht vertretbar.

Konkretes r12-Rezept:

- Befund 1: `test_26` entweder ausdrücklich als synthetischen Unit-Test des Helper-Vertrags kennzeichnen und alle Aussagen streichen, dass er den Produktionszustand von `run_tty` beweist; zusätzlich einen deterministischen Test auf dem tatsächlichen `run_tty`-Pfad schaffen, der den Log/Capture-Versatz an einer kontrollierten Grenze erzeugt und die Reconciliation des realen Aufrufs genau einmal prüft. Falls diese Abweichung im unterstützten PTY-Modell unmöglich ist, stattdessen die Garantie auf den belegten Main-loop-Pfad beschränken und keine Produktionsdivergenz behaupten.
- Befund 2: den Hook-Puffer im Test direkt auswerten und auf den erwarteten Sentinel/Chunk prüfen. Der Test muss den Hook vor dem zu prüfenden `run_tty`-Aufruf setzen und einen kontrolliert ausgeführten Final-drain-Chunk erzeugen; ein negativer Kontrollfall muss durch deaktivierten/falsch angeschlossenen Hook genau an dieser Beobachtungsassertion fehlschlagen. Transcript-/Log-Gleichheit allein ist dafür kein Ersatz.
- Nach r12 erneut den vollständigen Diff des neuen exakten Heads prüfen und einen erfolgreichen Hosted-Run genau auf diesem SHA nachweisen. Dieses Gutachten genehmigt weder Merge noch Push.

## Ende

END_DONE w255-0428-251-demo170codex: unabhängiges Zweitgutachten abgeschlossen; beide Befunde tragen, r12 erforderlich. Geprüfter Head e3ae7008b938ea58f0f4285da68f121ba60a22c9.
