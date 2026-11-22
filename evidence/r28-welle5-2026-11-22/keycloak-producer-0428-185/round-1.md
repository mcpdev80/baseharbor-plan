# 0428-185 keycloak-producer-target-mismatch — round-1 akte

Card `0428-185`, branch `lane-0428-185-producer-target`, base develop `8629450e` (= `acc343239681` per card). Owner order: fix the producer/witness target mismatch.

## PLAN

- Read card + task (acceptance 1-3, boundaries)
- Claim via scripts/plan.py claim + commit + push (done before edit)
- ls-remote + base attestation: develop = `8629450e`
- Messen: producer vs witness contract, datei:leile
- Fix (STOPPED on scope question — see below)
- Regression test
- PR + hosted run

## Base attestation

- develop HEAD (origin/develop): `8629450ef3c5198bb675331c12f56b2c9377aa1c`
- `internal/metrics/perses_identity_witness.go` NOT present on develop (`git ls-tree origin/develop --name-only internal/metrics/ | grep -c perses_identity_witness` = 0)
- `perses_identity_witness.go` lives ONLY on branch `origin/lane-0428-078-perses-identity-on-resolver` (commit `47f5953c`), which is NOT an ancestor of develop

## Messen (producer vs witness)

Producer, develop `internal/identityprovider/keycloak_realization.go`:
- line 136: `registrationID := "keycloak:" + r.files.Project`
- line 157-160: `signals["keycloak-metrics"] = observability.ProviderSignalRuntime{ Network: r.files.ConsumerNetwork, Target: "keycloak:9000" }`
- line 187: `ID: registrationID`  => registered source ID is `keycloak:<files.Project>`, Target `keycloak:9000`.

Witness (0428-078 `47f5953c`, `internal/metrics/perses_identity_witness.go` `keycloakMetricSignals`, lines 140-160):
- line 141: `if source.Provider != capability.ProviderKeycloak || source.ID != expectedID { continue }`
- line 149: `if strings.TrimSpace(source.Target) != "keycloak:9000" || ... { continue }`
- `expectedID` comes from `KeycloakMetricsRegistrationIDAt` (line 96) = `"keycloak:" + project` from `keycloakStateIdentity`.

Measured result: on the witness's OWN terms, producer and witness AGREE — both use ID `keycloak:<project>` and Target `keycloak:9000`. The card's stated mismatch ("witness looks for target = m.Name") does NOT match the witness code I found (it checks `source.Target == "keycloak:9000"`, not `m.Name`).

## STOP — scope question for coordinator

The card's write-set names `internal/metrics/perses_identity_witness.go` as a fix target, but that file does NOT exist on develop. It exists only on the 0428-078 lane branch (`47f5953c`), which is not merged to develop. The card references a witness contract (target = m.Name) that differs from the witness code actually present on the 0428-078 branch. Two possibilities:
1. The witness is meant to be created/re-landed by this card (but it already exists on another branch, so "create" conflicts with ownership).
2. The card's base should be the 0428-078 branch, not develop.
3. The card's described mismatch is a prior witness variant; the current 0428-078 witness does NOT exhibit the stated mismatch.

Cannot proceed to fix without a decision on which branch/file is the true base. Raising to coordinator per card instruction "STOP (melden)".

## Cleanliness

No edits made (write-set untouched). Worktree: `workers/0428-185-wt` (detached at develop HEAD). `docker ps -a`: empty. No containers/networks/volumes created.
