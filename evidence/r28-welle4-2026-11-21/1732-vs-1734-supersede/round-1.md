# w231 read-round: does PR #1734 (0428-212) supersede PR #1732 (0428-202)?

Mission: read-only decision round, no product code, no PR, no card change.
Lane: w231-0428-202-supersede. Date: 2026-11-21.

## PLAN

1. Fetch pull refs from lane-origin and record develop SHA. (done)
2. Compare file sets of PR #1732 and #1734 (`gh pr view --json files`) and commit logs vs develop. (done)
3. Ancestry/content proof: patch-ids per commit; show the three Loki fixture sites side by side (file:line) in both PRs. (done)
4. One-sentence decision proposal: (a) #1732 superseded / (b) #1732 heals more / (c) independent. (done — see ## vorschlag)
5. This dossier in baseharbor-plan evidence, pushed to origin/main. (this commit)
6. END post to coordinator with plan SHA.

## beweis

Planning-repo verification (rule: evidence lives only in baseharbor-plan):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Remote guard on the product checkout (all three names resolve to the GitHub URL):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v
lane-origin	https://github.com/mcpdev80/baseharbor.git (fetch)
lane-origin	https://github.com/mcpdev80/baseharbor.git (push)
origin	https://github.com/mcpdev80/baseharbor.git (fetch)
origin	https://github.com/mcpdev80/baseharbor.git (push)
upstream	https://github.com/mcpdev80/baseharbor.git (fetch)
upstream	https://github.com/mcpdev80/baseharbor.git (push)
```

Step 1 — fetch pull refs, develop SHA:

```
$ git -C baseharbor -c fetch.prune=false fetch lane-origin "+refs/pull/*/head:refs/remotes/lane-origin/pr/*"
$ git ls-remote lane-origin refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738	refs/heads/develop
$ git rev-parse lane-origin/pr/1732 lane-origin/pr/1734
bddb27e6251ec6bc76574a1dcdb13fc7ce017f24
75770bd2d0434bfed11d7c1b106064a5a08d5a51
```

Both heads match the SHAs named in the mission.

Step 2 — file sets and commits vs develop:

```
$ gh pr view 1732 --repo mcpdev80/baseharbor --json files -q '.files[].path'
internal/logs/loki_test.go
$ gh pr view 1734 --repo mcpdev80/baseharbor --json files -q '.files[].path'
internal/logs/loki_test.go
```

Both PRs (and both `git diff --name-only lane-origin/develop...HEAD`) touch exactly ONE file: `internal/logs/loki_test.go`. Both are OPEN, both base develop `40cb28c758b0`.

```
$ git log --oneline lane-origin/develop..lane-origin/pr/1732
bddb27e62 test(loki): materialize mTLS client keypair in test PKI fixture
$ git log --oneline lane-origin/develop..lane-origin/pr/1734
75770bd2d test(logs): prove passing health verdicts came from a reached probe
430e2722c test(logs): assert the fixture server identity carries server-auth before the probe witness
0dc299ccb test(logs): split Loki datasource health witness into probe-rejection and precondition subtests
```

Step 3 — ancestry and content:

```
$ git merge-base --is-ancestor lane-origin/pr/1732 lane-origin/pr/1734
NO   (exit 1 — #1732's commit is NOT an ancestor of #1734)
$ git merge-base --is-ancestor lane-origin/develop lane-origin/pr/1732  # and .../pr/1734
develop ancestor of both: YES
$ git diff --patch lane-origin/develop...lane-origin/pr/1732 | git patch-id --stable
c5161717889b4b733009d992aa5b386763db96af
$ git diff --patch lane-origin/develop...lane-origin/pr/1734 | git patch-id --stable
d00847f19fd8c59a292c3e687962e33686f0beb2
$ for c in 430e2722c 0dc299ccb 75770bd2d; do git show $c | git patch-id --stable; done
8bf85e9f36f8bbde12a9f9d305efd4d29023734d 430e2722c7471e9632e6403732532ee696f5c70e
96bbcad1c5c8f1a05daebf124cbd347719ecf925 0dc299ccbd001aa6b3b68b735777cafc7214bacf
b4fe4b2dc2a6de2289f0d4b7dbf64c27dcd48650 75770bd2d0434bfed11d7c1b106064a5a08d5a51
```

No patch-id repeats: #1734 contains no cherry-picked copy of #1732's commit. #1732's content effect is nonetheless present in #1734 — demonstrated below at the three named fixture sites.

The develop-side failures (owner note baseharbor-plan `3c142896`: "packages still show the same three missing Loki client-certificate fixture failures (0428-202/#1732)") are exactly these three asserts in `lane-origin/develop:internal/logs/loki_test.go`:

- site 1 — `internal/logs/loki_test.go:522` `--- FAIL: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource`, "health must pass for a healthy multi-source Loki"
- site 2 — `internal/logs/loki_test.go:589` `--- FAIL: TestPersesLokiDatasourceMultiSourcePartialMatchability`, "expected 2 per-source queries, got 0"
- site 3 — `internal/logs/loki_test.go:633` `--- FAIL: TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed`, "expected 2 per-source queries even on full miss, got 0"

All three fail from one cause: `materializeLokiServiceAccessPKI` never wrote `client-cert.pem`/`client-key.pem`, so `serviceaccess.ExistingTLSMaterial` stats a missing file and `VerifyPersesLokiDatasourceHealth` fails before reaching the probe.

Site pairs after each PR (file:line at each head):

| site (develop failure) | #1732 head bddb27e62 | #1734 head 75770bd2d |
| --- | --- | --- |
| 1 QueryOneSelectorPerSource | `internal/logs/loki_test.go:554` | `internal/logs/loki_test.go:671` (inside `t.Run("HealthyMultiSourceLoki", …)`) |
| 2 PartialMatchability | `internal/logs/loki_test.go:621` | `internal/logs/loki_test.go:751` |
| 3 NoneMatchFailsClosed | `internal/logs/loki_test.go:665` | `internal/logs/loki_test.go:813` |

The healing change, side by side.

#1732, single hunk appended inside `materializeLokiServiceAccessPKI` (diff hunk `@@ -487,6 +487,38 @@`), effective writes at head `internal/logs/loki_test.go:516` and `:518`:

```go
clientKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
...
client := &x509.Certificate{ SerialNumber: big.NewInt(3),
    Subject: pkix.Name{CommonName: "loki-client"}, ...,
    ExtKeyUsage: []x509.ExtKeyUsage{x509.ExtKeyUsageClientAuth} }
...
if err := os.WriteFile(filepath.Join(dir, "client-cert.pem"), clientCertPEM, 0o600); err != nil { t.Fatal(err) }
if err := os.WriteFile(filepath.Join(dir, "client-key.pem"), clientKeyPEM, 0o600); err != nil { t.Fatal(err) }
```

#1734, commit `0dc299ccb`, hunk `@@ -487,6 +601,40 @@`, refactors the same function into `materializeLokiServiceAccessPKIWithClient(t, files, issueClient bool)` (`internal/logs/loki_test.go:536-548`); `materializeLokiServiceAccessPKI` delegates with `issueClient=true` (`:538`) and the equivalent writes land at `internal/logs/loki_test.go:632`/`:635` with `CommonName: "baseharbor-service-client"`. #1734 additionally asserts the PKI material exists before the probe witness (`:421`: `for _, name := range []string{"ca.pem", "server-cert.pem", "server-key.pem", "client-cert.pem", "client-key.pem"}`), so every former failure site runs on head material in both PRs.

Conclusion of step 3: for each of the three failing asserts, the identical content effect (CA-signed client keypair with `ExtKeyUsageClientAuth` written into the fixture PKI dir) recurs in #1734 — not "similar": the same code shape at the paired file:line sites above, reachable unconditionally through `materializeLokiServiceAccessPKI` at `lane-origin/pr/1734:538`.

Hosted-CI witness per card records:

- #1734 (0428-212, card handoff): terminal run `44845451055` at exact head `75770bd2d043`, `PR · Go unit · packages` SUCCESS — all three client-cert fixture failures healed at this head.
- #1732 (0428-202, card wait_reason): run `44818799733` at exact head `bddb27e6251e`, `PR · Go unit · packages` SUCCESS (job `136574098983`).
- The two PRs touch the SAME single file; they cannot both merge (second conflicts on `internal/logs/loki_test.go`), so retaining both violates "ein PR pro Karte" for one thing (AGENTS 3.3.8).

## vorschlag

Decision: (a) — PR #1732 is superseded by PR #1734 in content: #1734's commit `0dc299ccb` re-implements the exact same fixture healing (CA-signed mTLS client keypair written by `materializeLokiServiceAccessPKI`) that #1732's single commit adds, proven at all three site pairs (`loki_test.go:554/621/665` in #1732 ↔ `loki_test.go:671/751/813` in #1734, both against develop sites `522/589/633`), with the packages shard green at each exact head — while #1734 additionally delivers card 0428-212's own probe-rejection vs precondition witness split.

Sub-note: nothing from #1732 needs to survive separately — card 0428-202's whole contract (a green packages shard on develop `40cb28c758b0`) is delivered by #1734 at the same base.

## folgen fuer die karten

- 0428-202 (`t-20261120-r28-packages-shard-develop-regression`, state `wait`, gated on 0428-198): close as superseded by 0428-212 / #1734 (plan `superseded` resolution pointing there, per schema), and close PR #1732 without merge once #1734 merges — or immediately, since #1734 carries the same fix. Both actions are coordinator/owner actions; this lane posts no PR comment and changes no card.
- 0428-212 (`t-20261121-loki-verify-probe`, state `review`): continue as-is — #1734 is the single integration candidate for the Loki fixture on develop `40cb28c758b0`; its cli-0..3 red stays attributed to 0428-198/0428-204, not to this card. After #1734 merges, the develop regression that motivated 0428-202 is fixed and no follow-up card is needed.
- Window consequence: do not "refresh" or rerun #1732 to keep it alive.

PRs examined for the END line: 2 (#1732 checked, #1734 checked) — file sets, logs, diffs, patch-ids, ancestry, site pairs, hosted-run witnesses.

## repo-rule compliance

- Read-only mission: no product code, no branches, no PR creation/comment/close, no card edits (proposal only, to the coordinator).
- Remote truth measured only via `git ls-remote lane-origin`, fetched pull refs in the shared `baseharbor` checkout (never the quarantined `workers/baseharbor`), and `gh pr view` against `mcpdev80/baseharbor`; `git remote -v` resolved every name to a github.com/mcpdev80 URL before use.
- Planning evidence committed only in `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (remote verified above), never in a product repo; no `.evidence/` anywhere.
- No subagents (AGENTS 4.8); every step executed in this session.
- No `.github/**` touched; no CI runs triggered, rerun or dispatched.
- Todo list mirrored in `workers/todos/w231-0428-202-supersede.json` and the ## PLAN above (AGENTS 4.4); this session exposes no native todowrite tool, so leg (0) was skipped per dispatch instruction.
- This file contains no markdown checkbox lines anywhere.

## cleanliness

Nothing was started: no containers, no compose projects, no VM sessions, no worktrees, no background processes; nothing to bring down.

```
ps-witness: only transient git/gh commands ran on this host; docker/podman were never invoked
(this lane starts no stacks — there is nothing of its own to clean).
```

Scratch: `/tmp/opencode/w231-diff-1732.patch` and `/tmp/opencode/w231-diff-1734.patch` (diff captures for the table above; under /tmp/opencode, deletable anytime). Note: the first write of this dossier disappeared between tool calls in this sandbox; it was rewritten in one pass and then committed — no content lost.

END_DONE w231-0428-202-supersede: #1734 (75770bd2d) supersedes #1732 (bddb27e62) in content — decision (a); see this dossier, plan SHA on origin/main.
