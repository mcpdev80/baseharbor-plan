# Diagnostic graph native failure — independently authenticated

Run `40135623881`, push attempt1, actual Connector K `c4363a28f5fd3d929a430bc6da630ee036bba104`, Core R `3e27497b4ef7b567858ba646bc3071bee37d19bd`, Demo D `09595781b68e1f41caaba9aec1402eb8009d700f`, Console U `51181967abfd3170b81857d51e9a4572c84b318b` remains **FAILED**, not consumer acceptance. Current graph SHA256 dfd87ceb0191702e7b37a287b45ee8f792d00b926cc189a5ec9927f20d5570df is the failed c436 snapshot. No qualified private manifest exists; selected63 remains unstarted.

## Exact authenticated origins

| Runtime | Actual job | Diagnostic artifact | Authenticated ZIP SHA256 |
| --- | --- | --- | --- |
| Docker | 120996434480 | 12576884452 | d1ccf8ea4d040ab713b6948bd3ca23853d38ec2d421236f31c414a7324ddf04c |
| Podman | 120996434447 | 12577405079 | 501741c9e6a9231eb7a44e86b5cf1551bafe1b5e5149426a969350bab296141c |

GitHub job metadata independently confirms both jobs completed FAILURE only at actual Chromium checks. Production managed enrollment and exact runtime fixture cleanup passed before Chromium; both final owned-services/private-key cleanup steps completed SUCCESS. Artifact origin metadata names exact run40135623881/headc436; both same-name diagnostic uploads actually succeeded. No matrix-specific qualified private artifact exists.

Independently downloaded both ZIPs and matched their bytes to authenticated API digests. Each contains only browser-receipt.json; each binds exact K/R/D/run/attempt and records result failure, cleanup success, release_eligible false. Actual U is established by the current immutable manifest and reviewed exact checkout graph, not by inventing a missing diagnostic receipt field. ZIPs retained in consumer-evidence/joint3-0.zip (Podman) and joint3-1.zip (Docker); parsed receipts joint3-verified.json.

## Decisive actual observation

Both receipts and completed job logs contain exactly this public error:

`Core secrets failed: persist OpenBao recovery-file reference: Target configuration mutation requires its protected owner directory`

Both installations report phase secrets_failed, READY false, SQL true, Secrets false, Identity false. However the fixed one-read OpenBao status reports initialized=true, unsealed=true, manager_ready=true. Thus OpenBao bootstrap reached manager readiness; failure is protected target-configuration persistence of its recovery reference. It is not an initialization/credential-readiness timeout, and it does not authorize treating the incomplete installation as READY.

Both editor phases reached verified-editor-lifetime. Metadata, callback, token and machine discovery responses are200, and the popup was closed through the corrected flow. The initial actual apply refused with approval_required/impact-confirmation-required as expected. These observations preserve successful subpaths without relabelling the failed browser journey as success.

## Source classification and next boundary

Exact R `Config.saveWithPreparation` (`internal/deployment/config_mutation.go`) checks the config parent with `ProtectedStateOwner`; on Unix that requires current UID and no group/other mode bits. It deliberately does not repair existing unsafe ownership. Console start-fixture.sh manually mkdir-p's config/baseharbor then chmod600's config.yaml only; it does not explicitly protect the parent directory. With ordinary umask022 the directory is755. Runtime diagnostics prove the protected-parent refusal; original directory mode itself was not archived, so755 is a source-supported explanation rather than a measured stat value.

This is a concrete fixture-owned configuration preparation mismatch with the intended Core fail-closed boundary. Correct only the isolated owned fixture parent permissions/ownership precondition, add an actual shell-path regression, independently review/qualify/integrate new U and repin actual K. Do not weaken Core ownership checks, mark setup successful from OpenBao booleans, manufacture consent or reuse failed receipts. Core R and Demo D need no change for this observed cause; source and actual new native acceptance remain separate.
