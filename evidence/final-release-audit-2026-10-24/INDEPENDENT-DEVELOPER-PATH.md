# Independent developer-path review — pending W1 execution

Verdict: **NOT YET QUALIFIED**. This report structure is prepared from inspected real W1 fixture source. No W1 run, transcript, artifact or cleanup observation is claimed yet. Fill only after the actual selected 63 run supplies authenticated final-pair results.

## Execution and review distinction

The existing fixtures drive the real public CLI through a PTY against native Docker/rootless Podman and actual SQL. This is scripted real developer-path execution, independently reviewed by this audit lane; it is not a claimed separate manual/operator session. core-923 delegates execution and the documented independent developer-path report to the acceptance owner; it requires no additional operator session or duplicate full journey.

Frozen inputs: Core R `3e27497b4ef7b567858ba646bc3071bee37d19bd`; Demo D `09595781b68e1f41caaba9aec1402eb8009d700f`; Console U `51181967abfd3170b81857d51e9a4572c84b318b`; Connector K `c4363a28f5fd3d929a430bc6da630ee036bba104`. Any changed input must be explicitly reconciled before acceptance.

## Required actual origins

| Required gate | Run / attempt / actual qualification job | Artifact ID / authenticated ZIP digest | Outcome |
| --- | --- | --- | --- |
| atomic/docker/guided | Pending execution | Pending authentication | PENDING |
| atomic/podman/guided | Pending execution | Pending authentication | PENDING |
| atomic/docker/data-capabilities | Pending execution | Pending authentication | PENDING |
| atomic/podman/data-capabilities | Pending execution | Pending authentication | PENDING |

Each observation below needs the actual source-bound evidence manifest, matching runtime/resource profile, required non-skipped job steps, transcript/receipt bytes and final cleanup/foreign-sentinel proof. Overall green alone is insufficient; a failed later relevant attempt must not be hidden by older green.

## Journey mapping and observation ledger

The source-defined expectations below are inspection findings, not executed outcomes.

| Developer path | Existing real producer and expected evidence | Actual observation |
| --- | --- | --- |
| Pristine repository to running application | guided/run.sh + guided/drive.py; real app init/up, source-neutral workload components, canonical HTTPS route and READY; named Guided Adoption Happy Path | PENDING |
| Zero selected managed needs | guided/new_edit.py real app new PTY; complete Footprint with exactly zero requirements and Lifecycle: VERIFIED transcript; new-edit-zero.json | PENDING |
| New No/Cancel safety | Actual new command returns from No to picker then Cancel; compares native/protected state and refuses a written project on cancellation | PENDING |
| Edit No/Cancel safety | Actual edit command, retained needs/preview flow, unchanged source/native/protected state and actual Cancel outcome text | PENDING |
| CLI/JSON/MCP parity | footprint_parity uses real entry points on the same application/target and matching authoritative projection | PENDING |
| New application with SQL | data-capabilities/new_edit.py real PTY New with application-scoped PostgreSQL, uniquely observed native provider and real SQL marker | PENDING |
| Remove then re-add SQL | Actual Edit removes managed requirement, re-add reuses retained dedicated provider/volume and reads original SQL marker | PENDING |
| Compatible provider switch and return | Actual Edit selects existing shared provider then returns to original dedicated provider; observed Footprint bindings and original markers agree | PENDING |
| Shared/sibling and foreign preservation | Same shared volume identity/SQL marker, sibling SQL records retained, same foreign paused container ID/labels/paused state and volume bytes | PENDING |
| Structured SQL journey receipt | new-edit-sql.json requires all add/remove/switch, No/Cancel, own/shared/sibling/foreign, parity and native flags true | PENDING |
| Owned automatic cleanup | Existing acceptance EXIT first verifies foreign sentinel preservation, separately removes only its fixture resources, and reports actual cleanup success; no failed emergency cleanup converted to success | PENDING |

## Final independent assessment to complete

After authenticating all four origins, record exact observed steps and exceptions here, distinguish native proof from source-only assertions, and link actual receipts/transcripts. Summarize whether a developer can create zero-needs or SQL applications, decline/cancel safely, edit/add/remove/switch providers without losing own/shared/foreign resources, and observe equivalent CLI/JSON/MCP truth on both runtimes. Record material limitations explicitly. Keep this verdict pending if a required origin, transcript, marker, parity check or cleanup proof is missing.
