# r27 image-transfer — Evidence (Round 2, Lane w234) REJECT-Korrektur

## PLAN
- Mission + card + act-1402b.md (REJECT) gelesen; base (origin/develop bc8670c1) attestiert
- work/r27-image-transfer auf c8272e9f3d04654fb711fbc5a716eb538bdba6dd (develop 7c393b0d jetzt Ahn)
- Punkt 1: platform-identitaet FAIL-CLOSED — inspectRuntimeImagePlatform + Verify(arch+OS) + 4 negative tests
- Punkt 2: red-first mutantenbeleg — GREEN -> MUTANT RED -> RESTORED GREEN
- Punkt 3: Docker+Podman isolated transfer auf baha-docker UND baha-podman + fabrik-rueckbau
- Punkt 4: develop einmerge/push, go-unit-tests + PR Selected Checks TERMIN GRUEN
- Punkt 5: diese akte mit 5-gegenueberstellungstabelle

## Status
- Lane: w234-image-transfer-r2
- End: IN ARBEIT (Evidence on origin/main steht aus)

## Base attestation (Owner: base provenance is proof)
- Base ref cut from: origin/develop
- Base SHA (current develop tip): bc8670c1dc6a2d7b5bf602ae7450f2e778a6f97a
- verify: git merge-base --is-ancestor bc8670c1... HEAD -> YES (merge-base == develop tip)
- Commit log lists ONLY: c8272e9f (merge develop), 5b710b6d (my fix) + carried develop tips
- Foreign candidate carried? NO — only develop (bc8670c1) + my commits
- Branch: work/r27-image-transfer (existing PR #1402, updated in place — exactly one candidate per chain)

## Round-2 Gegenlesung: URTEIL + REZEPT vs act-1402b.md

### 5-gegenueberstellungstabelle (REJECT finding -> Fix -> Beleg)

- Finding 1 (platform identity not fail-closed):
  Fix: inspectRuntimeImagePlatform jetzt (string,string,error), fail-closed auf command-error/malformed/empty;
  Verify(digest,manifestDigest,arch,os) vergleicht arch UND os exakt; empty => fail-closed.
  Beleg: application_image_transfer.go + 4 neue negative tests (command-error/leer/malformed/os-drift)
  TESTS GREEN (race-20); MUTANT (fail-open revert) -> ROT -> RESTORE -> GRUEN.

- Finding 2 (real mutant proof absent):
  Fix: reproduzierbarer Mutante = inspectRuntimeImagePlatform auf fail-open zurückgesetzt.
  Beleg: GREEN (4 tests) -> MUTANT ROT (3 tests rot: command-error/leer/malformed) -> RESTORE GRUEN.
  Transcript unten.

- Finding 3 (VM smokes + teardown absent):
  Fix: isolierter transfer-smoke real docker auf baha-docker + real podman auf baha-podman,
  pane-zeugnisse + fabrik-rueckbau + null-pruefung (0 container, smoke binary remote, kein baha).

- Finding 4 (hosted gate red at candidate):
  Fix: develop einmerge -> neuer head c8272e9f, CI auf neuem head neu getriggert.
  Beleg: run 42213910864 go-unit-tests SUCCESS + PR Selected Checks SUCCESS (+ go-vet/build/gofmt).

- Finding 5 (integration base stale):
  Fix: develop 7c393b0d...bc8670c1 eingemerged; base jetzt current develop tip.
  Beleg: merge-base == develop tip; PR base_sha bc8670c1.

## Evidence checked
- Mission: coordinator/missions/w234-image-transfer-r2.txt
- Card: baseharbor-plan/tasks/t-20261018-r27-image-transfer.md
- Review: baseharbor-plan/evidence/r27-welle5-2026-11-06/image-transfer/act-1402b.md (REJECT, 5 findings)
- Round-1 evidence: .../image-transfer/round-1.md
- Precedent: .../vm-smoke/round-2.md (w227/w232 hosts = blank VMs; baha-docker->baha-runner-docker,
  baha-podman->baha-runner-podman = Host-Namens-Altlast; verboten nur baha-runner-docker-2)
- PR #1402: head c8272e9f, base bc8670c1 (current develop), run 42213910864

## Point 2 — Red-first mutant transcript (local, race-20)
Green (fixed code):
  --- PASS: TestImageTransferFailsClosedOnPlatformInspectCommandError
  --- PASS: TestImageTransferFailsClosedOnPlatformInspectEmptyOutput
  --- PASS: TestImageTransferFailsClosedOnPlatformInspectMalformedOutput
  --- PASS: TestImageTransferFailsClosedOnOsDrift
  ok github.com/mcpdev80/baseharbor/cmd/baha

Mutant (inspectRuntimeImagePlatform reverted to fail-open, returns "", "", nil on every error):
  --- FAIL: TestImageTransferFailsClosedOnPlatformInspectCommandError
      platform inspect command error must fail closed, got ... architecture "amd64" != source ""
  --- FAIL: TestImageTransferFailsClosedOnPlatformInspectEmptyOutput
      ... architecture "amd64" != source ""
  --- FAIL: TestImageTransferFailsClosedOnPlatformInspectMalformedOutput
      ... architecture "amd64" != source ""
  FAIL github.com/mcpdev80/baseharbor/cmd/baha

Restored (fixed code):
  --- PASS (alle 4) 
  ok github.com/mcpdev80/baseharbor/cmd/baha
-> fail-open mutant is caught by the negative tests (red), restore is green.

## Point 3 — VM smokes (both hosts, real native tools)
Tool: ./w234-smoke (docker | podman), fail-closed platform-identity round-trip.

baha-docker (baha-runner-docker), tool=docker:
  POSITIVE source resolved: docker.io/library/hello-world@sha256:c567b23...8fdba78ef arch=amd64 os=linux
  POSITIVE OK: transferred identity verified (digest+arch+OS)
  arch-drift OK (fail-closed): "arm64" != "amd64"
  os-drift OK (fail-closed): "windows" != "linux"
  command-error OK (fail-closed): exit status 1
  ALL GREEN on docker

baha-podman (baha-runner-podman), tool=podman:
  POSITIVE source resolved: docker.io/library/hello-world@sha256:c567b23...8fdba78ef arch=amd64 os=linux
  POSITIVE OK: transferred identity verified (digest+arch+OS)
  arch-drift OK (fail-closed): "arm64" != "amd64"
  os-drift OK (fail-closed): "windows" != "linux"
  command-error OK (fail-closed): exit status 125
  ALL GREEN on podman

Factory teardown + null-pruefung (beide hosts, post-run witness):
  baha-docker: smoke binary removed (ls: No such file); docker containers=0; docker rootless containers=0;
    baha binary absent; ~/.config/baha ~/.baha ~/.cache/baha absent.
  baha-podman: smoke binary removed; podman containers=0; baha binary absent; baha config paths absent;
    load 0.22/0.17/0.14.
  -> beide hosts factory-fresh, 0 container, kein owned resource hinterlegt.

## Point 4 — Hosted gates (run 42213910864, head c8272e9f)
  go-unit-tests: success
  PR Selected Checks: success
  go-vet / go-build / gofmt / cli-package-tests / cli-vet / cli-guided-tests / cli-build / source-contracts: success
  (workflow policy, trusted plan, focused python: success; HA/validated/demo/selected-runtime: skipped — not targeted)

## Write-set (mission: NUR application_image_transfer.{go,_test})
- cmd/baha/application_image_transfer.go (fail-closed platform identity)
- cmd/baha/application_image_transfer_test.go (new negative tests, OS field)
- Keine .github, kein subagent, kein zweiter PR, kein root-checkout, kein Produkt-Branch-Auftauschung.

## ls-remote (echt, wortlich head == c8272e9f3d)
origin/work/r27-image-transfer -> c8272e9f3d04654fb711fbc5a716eb538bdba6dd
https://github.com/mcpdev80/baseharbor.git work/r27-image-transfer -> c8272e9f3d04654fb711fbc5a716eb538bdba6dd

## END an 841e7734 (vorbereitet, nach Evidence on origin/main)
END_DONE w234-image-transfer-r2: head=c8272e9f3d failclosed=JA (arch+OS mandatory, empty=>fail-closed, 4 negative tests)
mutante=ROT+GRUEN belegt (fail-open mutante durch negative tests gefangen)
rauche=beide-hosts+teardown (baha-docker docker GREEN, baha-podman podman GREEN, 0 container post-run)
lauf=42213910864 TERMIN GRUEN (go-unit-tests + PR Selected Checks)
lsremote=c8272e9f3d (real) | round-2 REJECT alle 5 Punkte umsetzen, PR #1402 in place aktualisiert
