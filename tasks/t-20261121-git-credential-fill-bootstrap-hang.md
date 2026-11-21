---
id: t-20261121-git-credential-fill-bootstrap-hang
card_number: "0428-217"
card_short_title: "0428-217 credential-fill hang"
title: "0428-217 · CLI: first target create hangs on git credential fill against example.invalid"
type: bug
areas: [cli]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
owner: coordinator
kanban_status: review
kanban_lane: review
kanban_summary: "The first authenticated Git operation inside a test or a first-time target bootstrap never returns a clean failure: it invokes…"
kanban_title: 0428-217 · 0428-217 credential-fill hang
priority: high
depends_on: []
blocked_by: []
prs: [mcpdev80/baseharbor#1742]
wait_reason: ""
blocker: ""

---

- [ ] t-20261121-git-credential-fill-bootstrap-hang · 0428-217 git credential fill must not block in test or first-run paths #task #release/v0-4-28 #status/review #view/review #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** coordinator · **Priority:** high  
    **PR:** [baseharbor#1742](https://github.com/mcpdev80/baseharbor/pull/1742)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** coordinator  
**Priority:** high  
**PRs:** [baseharbor#1742](https://github.com/mcpdev80/baseharbor/pull/1742)  
**Source:** 
<!-- /generated:links -->

## Goal

The first authenticated Git operation inside a test or a first-time target bootstrap never returns a clean failure: it
invokes `git credential fill`, which blocks on a prompt (or on a helper that has no terminal) and the caller reports a
timeout/OOM-shaped failure instead of "no credential for this host". Fix the call path so credential lookup is
non-interactive by construction in test and bootstrap contexts, and the failure names the missing credential.

## Why

Found while reproducing 0428-206. Two independent witnesses, same class:

1. CODEX's own exact-base reproduction at develop `40cb28c758b0` recorded: *"Initial invocation without prompt suppression
   stalled at a test's `git credential fill` against `https://example.invalid` and was interrupted; the second run needed
   `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/bin/true SSH_ASKPASS=/bin/true`."*
   (`evidence/r28-welle4-2026-11-21/other-domain-test-split/codex-review-r2.md`, plan `8a086890`)
2. Lane `0428-206-testsplit-recount` traced the call path to file:line in its round-2 akte
   (`evidence/r28-welle4-2026-11-21/other-domain-test-split/round-2.md`, plan `6391293a`):
   `cmd/baha/app_inspect_remote.go:28` → `internal/.../host.go:135` → `internal/.../gitcredential.go:49` / `:68`.

The Owner recorded the same class independently on card `t-20261114-r28-cli2-identity-secrets` (0428-078 note): a runtime
fails at the first `baha target create` even after the Demo selector-order fix. This card exists so the finding is not
trapped in an akte (Fund→Karte duty, Owner directive 2026-11-08).

## Scope

Allowed write-set (to be confirmed by the implementing lane before the first edit — the two `gitcredential`/`host` files
must be reported here if they are not under `cmd/baha/`):

- `cmd/baha/app_inspect_remote.go`
- `cmd/baha/app_update.go` — **added by Coordinator amendment 2026-11-21 07:5xZ after CODEX-REVIEW
  `evidence/r28-welle4-2026-11-21/git-credential-fill/review-1.md` Finding 2.** The lane found the same
  prompt-hang class in the update path (`gitOutput`, `gitIsAncestor` invoke `git` directly), so the two
  `cmd.Stdin = strings.NewReader("")` assignments are in scope from now on. The amendment is conditional:
  acceptance criterion 4 below must be satisfied in the same PR, otherwise the two lines are removed.
- the Git host/credential helper files reached from it (`host.go`, `gitcredential.go`), **excluding** any path under
  `internal/operatorauth/**`, `internal/identityprovider/**`, `internal/serviceaccess/**` (Owner rails).

Forbidden: `.github/**` (Owner scope — if a workflow env var is needed, report the line to the Coordinator), the Owner
stack `#1615`/`#1625`/`#1623` (branch `cli2-identity-secrets-head`), `#1650`/`#1606`, `#1614`, `#1731`, `#1704`,
`internal/observability/registry.go`, `internal/capability/perses_selection.go`.

## Acceptance criteria

1. With **no** prompt suppression in the environment (`GIT_TERMINAL_PROMPT` unset, no `GIT_ASKPASS`), the code path either
   (a) never calls `git credential fill` in test/bootstrap contexts, or (b) fails with a message that names the host and
   the missing credential. Blocking on a prompt is not an acceptable outcome in any CI or first-run context.
2. A regression test proves the failure content, not just `err != nil`, and proves the asserted branch is reachable from
   the production call path (honesty rubric, 2026-11-21).
3. The existing hosted cells that currently need `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/bin/true SSH_ASKPASS=/bin/true` as a
   workaround keep passing; the workaround is documented as no longer required in the akte, and any place that still
   requires it is named with file:line.

4. (`Coordinator amendment`) The `cmd/baha/app_update.go` writes are covered by a focused regression that
   exercises `gitOutput`/`gitIsAncestor` through the production update path with no controlling terminal and
   asserts a bounded failure instead of a hang. Without that regression, criterion 1's PR must drop the file.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | Go unit shards for `./cmd/baha/` (PR Selected Checks) |
| Evidence | `baseharbor-plan/evidence/r28-welle4-2026-11-21/git-credential-fill-bootstrap-hang/round-1.md` |

## Notes

- Derived from a diagnosis card, not from a hunt matrix slice; the two witnesses above are the full provenance.
- This card is currently **read-only for the queue**: it is not commissioned until 0428-204 (`#1726`) or `#1615` is merged,
  because both touch the CLI Git paths. Commissioning is a Coordinator action with a stated reason.

Lane '0428-217-credfill' auf laptop:2 begonnen; write-set BESTAETIGUNG ist schritt 1 der mission (die karte erlaubt verschiebungen ausserhalb der zwei dateien, meldung an mich vor dem ersten write ausserhalb von cmd/baha/). Kein besetzter pfad: app_commands.go haelt 0428-210/#1739, mcp.go + MCP-tests haelt 0428-218/#-neu.

PR #1742 eroeffnet (head 0df7efc00bb3, base develop) aber DRAFT = keine required checks, deshalb formal 'review' mit meinem hinweis an die lane: undraften + gehosteten durchgang selbst beobachten (§4.6). write-set ueber der karte: 'cmd/baha/app_update.go' + drei dateien unter 'internal/credential/native/' (erlaubt, aber meldepflichtig laut karte — von ihr im PR-body gemeldet, fehlt noch in der AKTE). Kein tabu-pfad beruehrt (kein '.github/**', kein 'internal/operatorauth/**'). Gemessene datei-liste: app_inspect_remote.go, app_update.go, credfill_noninteractive_test.go, gitcredential.go, host.go.

END_DONE abgenommen, und ihr 'geerbt'-satz ist von MIR DURCHGEZOEHLT statt Etikettiert (buchfuehrungs-regel aus #1738/#1737): protokoll-vergleich der eindeutigen first-level-namen — durchgang 44863102857 (develop-basis, PR #1739) = **196**, ihr durchgang 44874605168 = **197**; der EINEE namliche neue name ist 'TestAppListAllTargetsWorksAfterInstallationDestroy' = fall von 0428-210/#1739 (scheitert ebenfalls auf develop, NICHT ihrer), und ES ist nichts weggefallen; gate-text-zeilen = 0 in beiden. heisst: ihr kandidat bringt KEINEN neuen fall, und die rote 'PR Selected Checks' ist an dieser basis der develop-zustand OHNE #1615 — beleg fuer die KLASSE (run 44854729670 cli-0..3 SUCCESS am #1615-head), nicht fuer ihren kandidat. PR #1742 draft=false (von ihr selbst undrafted), base develop, head 0df7efc00bb3, write-set = 5 dateien mit je EINER zeile begruendung in der akte (plan a233bc16): 'cmd/baha/app_inspect_remote.go', 'cmd/baha/app_update.go' (ausdtruecklich 'NOT named in the card', nur non-TTY stdin — karte war zu eng, ich ziehe nach), 'internal/credential/native/{gitcredential.go:38, host.go, credfill_noninteractive_test.go}'. OFFENER ZEUGE fuer die abnahme: ich finde im packages-shard-protokoll KEINE 'internal/credential'-paketzeile (meine grep-treffer waren checkout-plumbing) — ihre meldung 'internal/credential/native ok in CI' braucht die zelle, die den test laeuft.

### Coordinator scope amendment (2026-11-21, after CODEX-REVIEW review-1.md)

- Finding 2 is resolved by widening the write-set (above) rather than by shrinking the PR, because the
  `app_update.go` hang is the same class the card names in its title ("first target create hangs on git
  credential fill"): `gitOutput`/`gitIsAncestor` run `git` during `baha update` and inherit any prompt.
- Finding 1 stands as the correction requirement: the regression must reproduce Git's own prompt/askpass
  path under a bounded deadline (explicit PTY or `GIT_ASKPASS`/`SSH_ASKPASS` + `GIT_TERMINAL_PROMPT=0`),
  not a `/dev/tty` helper that a CI runner can satisfy without exercising the production behaviour.
- Bookkeeping correction by the Coordinator: the earlier "196 vs 197" comparison used the aggregated
  `gh run view --log`, which omits whole job sections; counts must be taken per job (`--job <id> --log`).
  Re-measured per job: PR #1742 head `0df7efc00bb3` = 197 distinct first-level FAIL names, PR #1702 head
  `b2f2fd3ac172` = 194, and the only names that differ between them are the three
  `TestPersesLifecycle*` cases that card 0428-142 fixes.

CODEX-REVIEW review-1.md = 'Verdict: REQUEST CHANGES' (plan c5ee4b5c/23b49a46). Befund 1: 'internal/credential/native/credfill_noninteractive_test.go:57-60' benutzt '/dev/tty' statt echtes git-prompt-/askpass-verhalten mit deadline; der production-seam ('gitcredential.go:41-60' -> 'host.go:32-40') wird gerufen, aber der beweis haengt an einem helper, den der runner fuellen kann. Befund 2: write-set-verletzung in 'cmd/baha/app_update.go:456' + ':515' (nicht kartiert) — ICH ENTSSCHEIDE: karte ist ausdruecklich erweitert (plan-Commit dieses Arbeitsgangs) plus akzeptanzkriterium 6 (fokussierte regression fuer den update-pfad), sonst sind die zwei zeilen zu entfernen. URTEIL plus mein rechenfehler: die 196-vs-197-rechnung, die ich dem reviewer mitgab, stammte aus dem AGGREGIERTEN log; per-job gemessen ist die korrektur in der karte dokumentiert.

CODEX-REVIEW (akte review-1.md, plan c5ee4b5c + 23b49a46) = 'Verdict: REQUEST CHANGES'. Befund 1: 'internal/credential/native/credfill_noninteractive_test.go:45-82' ruft den echten seam ('gitcredential.go:41-60' -> 'host.go:32-40'), aber der helper Zeile 57-60 liest '/dev/tty' statt echtes git-prompt-/askpass-verhalten; beweis waere auch ohne fix gruen. Befund 2: 'cmd/baha/app_update.go:456' + ':515' waren nicht im write-set — ICH ERWEITERTE DIE KARTE ausdtruecklich (plan f52d8949) plus akzeptanzkriterium 4 (fokussierte regression ueber den update-pfad ohne kontrollierendes terminal, bounded failure statt hang); bleibt die regression aus, sind die zwei zeilen zu entfernen. ZUSATZ: mein 196/197-war aus dem aggregierten log; per-job nachgemessen 197 (#1742) gegen 194 (#1702) — in der karte dokumentiert, damit der reviewer nicht mit meinen alten zahelen urteilt.

korrekturrunde 2 geliefert und von mir am head 719d28a888ab nachgemessen: draft=false, mergeable MERGEABLE, base develop. ALLE vier cli-shards pass, 'PR Selected Checks' pass, 'PR · Trusted Plan' pass. Delta gegen merge-base = 8 dateien, und JEDE davon steht im erlaubten schreib-set der karte (zeilen 69-77: cmd/baha/app_inspect_remote.go als erster punkt, cmd/baha/app_update.go durch meine amendment, dazu die git host/credential helper dateien). Mein amendment-punkt ist erfuellt: kriterium 4 (update-pfad regression) mit mutation belegt (akte round-2-promptproof.md). Inhalt, von mir gelesen: 'cmd.Stdin = os.Stdin' wird 'cmd.Stdin = strings.NewReader("")'' und 'GIT_TERMINAL_PROMPT=0' wird VOR den native-pfad gehoben, damit ein fehlendes nativ credential fail-closed statt am prompt zu haengen. Offen: develop ist weitergezogen (77c1e60f51b9), head ist kein nachkomme, also letzter hop wie bei #1739.

korrekturrunde 2 geliefert und von mir am head 719d28a888ab nachgemessen: draft=false, mergeable MERGEABLE, base develop. ALLE vier cli-shards pass, 'PR Selected Checks' pass, 'PR - Trusted Plan' pass. Delta gegen merge-base = 8 dateien, und JEDE davon steht im erlaubten schreib-set der karte (zeilen 69-77: cmd/baha/app_inspect_remote.go als erster punkt, cmd/baha/app_update.go durch meine amendment, dazu die git host/credential helper dateien). Mein amendment-punkt ist erfuellt: kriterium 4 (update-pfad regression) mit mutation belegt (akte round-2-promptproof.md). Inhalt, von mir gelesen: cmd.Stdin = os.Stdin wird durch eine leser-zeichenkette ersetzt, und GIT_TERMINAL_PROMPT=0 wird VOR den native-pfad gehoben, damit ein fehlendes nativ credential fail-closed statt am prompt zu haengen. Offen: develop ist weitergezogen (77c1e60f51b9), head ist kein nachkomme, also letzter hop wie bei 1739.
