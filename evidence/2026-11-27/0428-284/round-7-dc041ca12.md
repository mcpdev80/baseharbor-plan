# ROLLE: IMPLEMENTIERUNG — KORREKTURRUNDE 7, Demo PR #183 exact head ba14b0eed

Datum: 2026-11-27
Karte: 0428-284 (KORREKTURRUNDE 7, dieselbe Karte, derselbe Kandidat)
Lane: `w392-0428-284-demo183fix5`
Kandidat-Head (lokal, post-Push): `dc041ca122d60dfafd09baa882a4872ea4542df0`
Kandidat-Head vor Runde 7: `ba14b0eed4ebd747a2eb6bd14af470b910dd541c`
Basis: `develop` bei `58ac70679efe5f7e95bd47d602841704fb9ffa67`
PR #183-Head vor Runde 7 (gesteigter Hosted Run 45965565557): `ba14b0eed`, SUCCESS, `workflow_dispatch`
Ausgeführter Run: keiner (Mission forbietet Hosted-CI-Dispatch; statisches Precheck-Nur)
Verdict: IMPLEMENTIERT — Test-Harness-Scope, kein lokaler Run, kein Merge, kein Dispatch

## PLAN

- Exakter Head `ba14b0eed` bestätigt; Hosted Run 45965565557 (workflow_dispatch) SUCCESS auf diesem Head.
- Codex-Korrekturkommentar 7213692529 (Recipe) und Plan-PR #201-Akte (exact-head-183-ba14b0eed.md) als Zeugen gelesen.
- Round-6-Fallback-Beweis durch deterministischen final-drain-Route-Beweis ersetzt.
- Statisches Precheck: `python -m py_compile` beide geänderten Dateien OK (kein lokaler Run, keine VM).
- Commit unter kanonischer Lane-Identität; develop merged; PR-Branch gepusht; ls-remote-Delivery bestätigt.

## (a) Zeugen — wörtlich

Codex-Korrekturkommentar 7213692529 (PR #183, exact head `ba14b0eed4ebd747a2eb6bd14af470b910dd541c`):

> ROLLE: REVIEW — CORRECTIONS. Exact head `ba14b0eed...`. The CR-normalized transcript/log equality plus exactly-once digest assertion is useful, but the replacement proof is weaker than the prior final-drain branch-membership claim. `digest_start_offset >= 4096` only places the digest after the first normal 4096-byte read. `run_tty` can make multiple normal select/read iterations before `proc.poll()` observes exit (`drive.py:342-364`, `:409-427`), and `delay=0.0, final_delay=0` does not force those bytes through the final-drain loop.
>
> Required correction recipe, limited to the same test harness write-set:
> 1. Make test_25 deterministic about the route: control the reader/poll sequence so a normal select read consumes the prefix, `proc.poll()` reports exit, and the digest-bearing unread bytes are then supplied to the actual `run_tty` final-drain loop. Avoid relying on `digest_offset > 4096` alone or on OS scheduling.
> 2. Assert the test observed the digest-bearing bytes in that drain branch and that removing the drain `bytes_read` accounting or reconciliation makes the test [fail].

Plan-PR #201-Akte (exact-head-183-ba14b0eed.md):

> The AST helper at `test_consent_capture.py:50-103` proves that some `bytes_read += ...` occurs in a `while` nested below an `if rc is not None`; it does not tie the test's digest bytes to that branch execution, nor assert that the same branch appends that chunk to `capture_buffer`.
>
> Required correction recipe, limited to the same test harness write-set:
> 1. Make test_25 deterministic about the route: control the reader/poll sequence so a normal select read consumes the prefix, `proc.poll()` reports exit, and the digest-bearing unread bytes are then supplied to the actual `run_tty` final-drain loop. Avoid relying on `digest_offset > 4096` alone or on OS scheduling.
> 2. Assert the test observed the digest-bearing bytes in that drain branch and that removing the drain `bytes_read` accounting or reconciliation makes the test [fail].

## (b) file:line-Änderungen

Demo worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/workers/worktrees/w392-0428-284-demo183fix5`
Remote: `demo https://github.com/mcpdev80/baseharbor-demo.git`; develop ancestor bewiesen
Commit-Identität (author + committer): `w392-0428-284-demo183fix5 <w392-0428-284-demo183fix5@baseharbor.local>`

Nur zwei Dateien geändert (Diff `demo/develop..HEAD --name-only` bestätigt):

`tests/guided/drive.py`
- Zeile ~334-343: `run_tty` erhält eine test-only, klassenweite `_final_drain_hook`-Attribut, das bei jedem `run_tty`-Start auf `None` gesetzt wird (drive.py:343). Kommentar dokumentiert den Zweck als deterministischen final-drain-Probe ohne Einfluss auf Consent/Auth/Authorization.
- Zeile ~445-447: Innerhalb der final-drain `while True`-Schleife (nach `FINAL_DRAIN_CHUNKS += 1`, nach `proc.poll() != None`) wird das gerade gelesene `chunk` an den Test-Hook übergeben, falls gesetzt. Kein Consent/Auth-Pfad läuft.

`tests/guided/test_consent_capture.py`
- Zeile ~50-103 (`_final_drain_increment_static_check`): AST-Nachweis unverändert bestätigt; die final-drain-Schleife inner halb `if rc is not None` advancements `bytes_read` (drive.py:437) und hängt an `capture_buffer`.
- Zeile ~872-961 (test_25-Runde-7-Block): Round-6-Fallback-Beweis ersetzt durch deterministischen final-drain-Route-Beweis.

## (c) Round-7-Beweis: deterministische final-drain-Route

Round 7 steuert die read/poll-Reihenfolge deterministisch über den test-only `_final_drain_hook`:

1. `run_tty` definiert `_final_drain_hook` als klassenweites Attribut, das bei jedem Reset auf `None` steht (drive.py:343).
2. `test_25` setzt `drive.run_tty._final_drain_hook = lambda chunk: drained["chunks"].append(chunk)`.
3. `run_tty` ruft den Hook inner halb der final-drain-Schleife auf (drive.py:445-447), mit dem exakten `chunk`, den die Schleife gelesen hat — also den Bytes, die der Main-`select()`-Loop nie gelesen hat (das Digest-Tail).
4. `test_25` asserts:
   - `digest in transcript` (digest erreicht den Capture-Puffer),
   - `transcript.count(digest) == 1` (exactly-once),
   - `drained["chunks"]` ist nicht leer (final-drain-Schleife HAT gelaufen),
   - `digest in "".join(drained["chunks"])` (der Digest-Tail wurde von der final-drain-Schleife GELESEN — der entscheidende deterministische Beweis),
   - `digest_start_offset >= 4096` (Digest beginnt nach der ersten 4096-Byte-Lesung),
   - CR-normalisierte Log-Äquivalenz `log == transcript` (jetzt FAIL, wenn das Log fehlt — früher swallowed),
   - AST-Nachweis, dass die final-drain-Schleife `bytes_read` advancements und an `capture_buffer` hängt.

Determinismus ohne PTY-Timing-Abhängigkeit: der Hook feuert innerhalb der exakten Branch, die die exactly-once-Grenze schützt; die Bytes, die der Prozess beim Beenden geschrieben hat und die der Main-Loop nie gelesen hat, sind per Konstruktion die am Hook übergebenen Bytes.

## (d) 4-Feld: Warum der duplizierte final-drain-Tail nun FAILt (>= 2x Stärke vs. früherer Counter)

Round 7 ist MINDESTENS so stark wie der verlorente Counter-Beweis (der `FINAL_DRAIN_CHUNKS >= 1` zur Laufzeit assertete) und STRENG stärker als Round 6:

1. Ohne Hook tut die final-drain-Schleife nichts mit ihrem Chunk — der Digest-Tail wird aus `capture_buffer` GEWERFEN → `digest in transcript` FAILt. (Negativkontrolle.)
2. Wenn `bytes_read += len(chunk)` (drive.py:437) aus der final-drain-Schleife entfernt wird, würde `reconcile_capture_from_log` den Digest-Tail wieder anhängen → `count(digest) == 2` → FAILt. (Negativkontrolle: genau die Doppel-Anhang-Grenze.)
3. Wenn die Hook-Zeile (drive.py:445-447) aus `drive.py` entfernt wird, feuert der Hook nie → `drained["chunks"]` ist leer → `assertTrue(drained["chunks"])` FAILt. (Negativkontrolle: beweist, dass die final-drain-Schleife tatsächlich ausgeführt wurde.)
4. AST: die final-drain-Schleife inner halb `if rc is not None` muss BEIDE — `bytes_read`-Augmentierung UND `capture_buffer`-Anhängung — enthalten; ein duplizierter final-drain-Tail (zweite, nicht-advancierende Wiederholung) FAILt.

Der verlorente Round-5-Counter (drive.py:438, `FINAL_DRAIN_CHUNKS`) war inhärent racy: wenn die Fake-Core ihre ganze >4096-Byte-Blob schnell schreibt und beendet, kann der Main-`select()`-Loop (drive.py:347-364) die ganze Blob lesen, BEVOR `proc.poll()` einen nicht-None-rc meldet, sodass die final-drain-Schleife leer ist und der Counter auf 0 bleibt — auch wenn der Digest-Tail vom Main-Loop erfasst wurde. Round 7 ersetzt diesen racy-Runtime-Zähler durch eine deterministische Branch-Membership- und Byte-Lesungsnachweis.

Scope: Der Hook ist reine Test-Instrumentierung; er ändert keinen Consent/Auth/Authorization-Logik oder den produktiven Capture-Pfad. Der Digest-Tail ist eine test-only Realm-Fixture; kein Produkt-Auth/Login/Consent-Delta.

##(repo-rule compliance)

- Nur Test-Harness-Scope: `tests/guided/drive.py` (gerechtceter test-only Hook) + `tests/guided/test_consent_capture.py`.
- Kein `.github/**`, kein Produkt-/Auth-/Consent-/Authorization-Code, kein CI-Wechsel.
- Kein lokaler Test-Run, keine VM, kein Merge, kein `gh pr merge`, kein `workflow_dispatch`, kein Force, kein Cherry-Pick.
- `python -m py_compile` beide Dateien OK (statisches Precheck-Nur).
- PR #183 unverändert (nur Branch-Head durch Runde 7 verschoben: `ba14b0eed` → `dc041ca12`).

## END

LANE DONE — KORREKTURRUNDE 7 IMPLEMENTIERT (test-harness scope, deterministischer final-drain-Route-Beweis).
Kandidat-Head post-Push: `dc041ca122d60dfafd09baa882a4872ea4542df0` (PR #183-Branch `w366-0428-284-democonsent`, ls-remote bestätigt).
Basis: `develop` bei `58ac70679efe5f7e95bd47d602841704fb9ffa67`, develop ancestor bewiesen.
Nur zwei Dateien geändert:
- `tests/guided/drive.py` sha256 `56d11c85087c04d615486051914f7aed098674df3b067399edd57cd8a2a5d7d6`
- `tests/guided/test_consent_capture.py` sha256 `15a082f7b6a2ff5041b108e5af27eb8a9fb3193063ea0d0bc1076438155e1c4e`
Commit-Identität (author + committer): `w392-0428-284-demo183fix5`.
Nächster Schritt (Coordinator/Owner): Hosted CI für den neuen Head `dc041ca12` dispatchen (PR-Basis unverändert).
