---
id: 2026-10-18-v0-4-27-task-coverage
status: proposed
sources: []
---

# v0.4.27 task coverage

Planning cut: 2026-10-18. No product acceptance implied. Original core-777 criteria are preserved verbatim in the epic. The table is an allocation, not replacement normative text. Each criterion below retains its original wording.

## Normative rules

- **UX:** [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md).
- **Local development needs no login:** [client-commands](../tasks/t-20261018-r27-client-commands.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
- **Workspace location:** [candidate-pack](../tasks/t-20261018-r27-candidate-pack.md), [native-auth](../tasks/t-20261018-r27-native-auth.md).
- **Native authentication first:** [native-auth](../tasks/t-20261018-r27-native-auth.md).
- **Minimal credential choice:** [native-auth](../tasks/t-20261018-r27-native-auth.md), [protected-credentials](../tasks/t-20261018-r27-protected-credentials.md).
- **Credential classes:** [profile-contract](../tasks/t-20261018-r27-profile-contract.md), [protected-credentials](../tasks/t-20261018-r27-protected-credentials.md).
- **Ownership:** [state-owner](../tasks/t-20261018-r27-state-owner.md), [protected-credentials](../tasks/t-20261018-r27-protected-credentials.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md).
- **Profile export/import:** [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [secure-export](../tasks/t-20261018-r27-secure-export.md).
- **Multi-device:** [app-binding](../tasks/t-20261018-r27-app-binding.md), [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
- **Export/import ≠ backup/restore ≠ platform DR:** [profile-contract](../tasks/t-20261018-r27-profile-contract.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md).
- **Recoverability:** [protected-credentials](../tasks/t-20261018-r27-protected-credentials.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md).
- **Console:** [public-surfaces](../tasks/t-20261018-r27-public-surfaces.md), [docs](../tasks/t-20261018-r27-docs.md).
- **Repository/artifact consumers:** [native-auth](../tasks/t-20261018-r27-native-auth.md), [artifact-resolution](../tasks/t-20261018-r27-artifact-resolution.md).
- **Security:** [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [team-auth](../tasks/t-20261018-r27-team-auth.md), [device-enrollment](../tasks/t-20261018-r27-device-enrollment.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
- **Parity:** [public-surfaces](../tasks/t-20261018-r27-public-surfaces.md).
- **Team onboarding with external corporate SSO (2026-10-06, consolidates #803):** [team-auth](../tasks/t-20261018-r27-team-auth.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
- **Managed Identity administration (2026-10-06):** [managed-users](../tasks/t-20261018-r27-managed-users.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md).
- **Independent installations per security boundary (2026-10-06):** [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
- **Guided removal and offboarding:** [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md).
- **Kubernetes boundary:** [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [docs](../tasks/t-20261018-r27-docs.md).
- **Dev Local vs Dev Remote (2026-10-06):** [device-enrollment](../tasks/t-20261018-r27-device-enrollment.md), [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
- **v0.4.24 Core/Node/CLI handoff (2026-10-09):** [node-service](../tasks/t-20261018-r27-node-service.md), [node-trust](../tasks/t-20261018-r27-node-trust.md), [node-cli](../tasks/t-20261018-r27-node-cli.md).
- **Superseded section:** [authority-contract](../tasks/t-20261018-r27-authority-contract.md).

### Developer UX

1. Every normal onboarding/offboarding flow has a documented happy path with the minimum possible number of human decisions.
   Owners: [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [docs](../tasks/t-20261018-r27-docs.md).
2. No wizard asks for information already discoverable from the selected installation, profile, native toolchain or current state.
   Owners: [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [docs](../tasks/t-20261018-r27-docs.md).
3. Advanced authentication, trust and provider details are progressively disclosed rather than shown by default.
   Owners: [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [docs](../tasks/t-20261018-r27-docs.md).
4. Repeated daily developer operations do not require repeated login/credential prompts while valid reusable access exists.
   Owners: [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [docs](../tasks/t-20261018-r27-docs.md).
5. Dev Local and trusted Dev Remote remain materially simpler than shared/Test/Prod operation.
   Owners: [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [docs](../tasks/t-20261018-r27-docs.md).
6. CLI wording and Console flows optimize for developer intent first, implementation detail second.
   Owners: [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [docs](../tasks/t-20261018-r27-docs.md). Console UI proof remains in [v0.4.28](../releases/v0.4.28.md); v0.4.27 owns domain/API parity.

### Frictionless local development

7. Clean local Docker/Podman developer journey works without `baha login`.
   Owners: [native-auth](../tasks/t-20261018-r27-native-auth.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
8. Existing Git credential helper authentication is reused without extra prompts.
   Owners: [native-auth](../tasks/t-20261018-r27-native-auth.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
9. Existing SSH-agent/config authentication is reused without extra prompts.
   Owners: [native-auth](../tasks/t-20261018-r27-native-auth.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
10. Existing local repository can be adopted without moving it.
   Owners: [native-auth](../tasks/t-20261018-r27-native-auth.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
11. BaseHarbor-created clone defaults to `~/baseharbor/repos/<host>/<owner-or-group>/<repo>`.
   Owners: [native-auth](../tasks/t-20261018-r27-native-auth.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).

### Runtime/target standards first

12. Existing kubeconfig/context works without creating duplicate BaseHarbor credentials.
   Owners: [native-auth](../tasks/t-20261018-r27-native-auth.md), [candidate-contract](../tasks/t-20261018-r27-candidate-contract.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
13. Kubernetes exec/OIDC/client-cert authentication can remain authoritative.
   Owners: [native-auth](../tasks/t-20261018-r27-native-auth.md), [candidate-contract](../tasks/t-20261018-r27-candidate-contract.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
14. Architecture allows cloud-native credential chains without requiring a BaseHarbor-specific cloud login contract.
   Owners: [native-auth](../tasks/t-20261018-r27-native-auth.md), [candidate-contract](../tasks/t-20261018-r27-candidate-contract.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
15. Native access failure produces actionable guidance before offering managed storage.
   Owners: [native-auth](../tasks/t-20261018-r27-native-auth.md), [candidate-contract](../tasks/t-20261018-r27-candidate-contract.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).

### Temporary credentials

16. Session-only credential is not persisted in Git, portable intent or OpenBao.
   Owners: [native-auth](../tasks/t-20261018-r27-native-auth.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
17. Temporary secret files, if unavoidable, are owner-only and cleaned up.
   Owners: [native-auth](../tasks/t-20261018-r27-native-auth.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
18. Normal output/logs do not expose the credential.
   Owners: [native-auth](../tasks/t-20261018-r27-native-auth.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).

### Secure credentials

19. Secure choice persists eligible credential material in the authoritative protected/OpenBao store.
   Owners: [protected-credentials](../tasks/t-20261018-r27-protected-credentials.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
20. Future operations can reuse it without repeated credential prompts.
   Owners: [protected-credentials](../tasks/t-20261018-r27-protected-credentials.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
21. Only references/non-secret metadata enter declarative/profile state.
   Owners: [protected-credentials](../tasks/t-20261018-r27-protected-credentials.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
22. Rotation/revocation preserves the same repository/target logical reference.
   Owners: [protected-credentials](../tasks/t-20261018-r27-protected-credentials.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
23. Secure local credentials are recoverable through the supported recovery model.
   Owners: [protected-credentials](../tasks/t-20261018-r27-protected-credentials.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).

### Export/import

24. Default export contains no secret values.
   Owners: [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [secure-export](../tasks/t-20261018-r27-secure-export.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
25. Secure credential export requires explicit opt-in.
   Owners: [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [secure-export](../tasks/t-20261018-r27-secure-export.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
26. Secret-bearing export is encrypted, authenticated and versioned.
   Owners: [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [secure-export](../tasks/t-20261018-r27-secure-export.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
27. Import validates before mutation.
   Owners: [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [secure-export](../tasks/t-20261018-r27-secure-export.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
28. Import restores secret material into the protected destination store.
   Owners: [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [secure-export](../tasks/t-20261018-r27-secure-export.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
29. Conflicts are explicit and fail closed.
   Owners: [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [secure-export](../tasks/t-20261018-r27-secure-export.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
30. Remote target secrets are not silently exported.
   Owners: [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [secure-export](../tasks/t-20261018-r27-secure-export.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
31. Multi-device local setup can be recreated without requiring manual BaseHarbor state surgery.
   Owners: [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [secure-export](../tasks/t-20261018-r27-secure-export.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).

### Lifecycle boundaries

32. Developer profile export/import is documented separately from #399 Application Recovery Unit.
   Owners: [profile-contract](../tasks/t-20261018-r27-profile-contract.md), [secure-export](../tasks/t-20261018-r27-secure-export.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [docs](../tasks/t-20261018-r27-docs.md).
33. Platform disaster recovery is not conflated with profile export.
   Owners: [profile-contract](../tasks/t-20261018-r27-profile-contract.md), [secure-export](../tasks/t-20261018-r27-secure-export.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [docs](../tasks/t-20261018-r27-docs.md).
34. Short-lived runtime identities are regenerated rather than treated as portable developer credentials where appropriate.
   Owners: [profile-contract](../tasks/t-20261018-r27-profile-contract.md), [secure-export](../tasks/t-20261018-r27-secure-export.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [docs](../tasks/t-20261018-r27-docs.md).
35. Recovery/seal material is handled separately from ordinary exported secrets.
   Owners: [profile-contract](../tasks/t-20261018-r27-profile-contract.md), [secure-export](../tasks/t-20261018-r27-secure-export.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [docs](../tasks/t-20261018-r27-docs.md).

### UX

36. Existing authentication success causes no credential questionnaire.
   Owners: [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [docs](../tasks/t-20261018-r27-docs.md).
37. When input is required, the normal persistence choice is no more complex than secure-for-future-use vs session-only.
   Owners: [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [docs](../tasks/t-20261018-r27-docs.md).
38. Advanced authentication types/options appear only when needed.
   Owners: [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [docs](../tasks/t-20261018-r27-docs.md).
39. Human wording follows "as little as possible, as much as necessary."
   Owners: [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [docs](../tasks/t-20261018-r27-docs.md).

### Cross-surface

40. CLI/JSON/MCP/Console consume the same credential-source semantics.
   Owners: [public-surfaces](../tasks/t-20261018-r27-public-surfaces.md), [access-proof](../tasks/t-20261018-r27-access-proof.md), [docs](../tasks/t-20261018-r27-docs.md). Console UI proof remains in [v0.4.28](../releases/v0.4.28.md); v0.4.27 owns domain/API parity.
41. Machine surfaces remain secret-safe.
   Owners: [public-surfaces](../tasks/t-20261018-r27-public-surfaces.md), [access-proof](../tasks/t-20261018-r27-access-proof.md), [docs](../tasks/t-20261018-r27-docs.md).
42. No Console-only credential database or CLI-only credential behavior exists.
   Owners: [public-surfaces](../tasks/t-20261018-r27-public-surfaces.md), [access-proof](../tasks/t-20261018-r27-access-proof.md), [docs](../tasks/t-20261018-r27-docs.md). Console UI proof remains in [v0.4.28](../releases/v0.4.28.md); v0.4.27 owns domain/API parity.

### Team onboarding and external SSO

43. Local Docker/Podman works without login while shared remote dev denies anonymous/forged trusted-local access.
   Owners: [team-auth](../tasks/t-20261018-r27-team-auth.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [candidate-ingress](../tasks/t-20261018-r27-candidate-ingress.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
44. New team member attaches the configured Target and uses external corporate SSO without managed Keycloak or per-user provider setup.
   Owners: [team-auth](../tasks/t-20261018-r27-team-auth.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [candidate-ingress](../tasks/t-20261018-r27-candidate-ingress.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
45. Authenticated nonmember is denied; mapped developer cannot access another team/prod, reveal secrets or administer providers without permission.
   Owners: [team-auth](../tasks/t-20261018-r27-team-auth.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [candidate-ingress](../tasks/t-20261018-r27-candidate-ingress.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
46. Wrong issuer/tenant/audience, missing/overage claims and expired sessions fail closed with actionable output.
   Owners: [team-auth](../tasks/t-20261018-r27-team-auth.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [candidate-ingress](../tasks/t-20261018-r27-candidate-ingress.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
47. Same app on local and remote Targets uses different secret values correctly; no cross-target fallback or profile secret replication.
   Owners: [team-auth](../tasks/t-20261018-r27-team-auth.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [candidate-ingress](../tasks/t-20261018-r27-candidate-ingress.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
48. Private secret-store access works through the supported access path without distributing manager credentials.
   Owners: [team-auth](../tasks/t-20261018-r27-team-auth.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [candidate-ingress](../tasks/t-20261018-r27-candidate-ingress.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
49. Two clients observe one remote deployment/provider identity and safe conflicting-update behavior.
   Owners: [team-auth](../tasks/t-20261018-r27-team-auth.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [candidate-ingress](../tasks/t-20261018-r27-candidate-ingress.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
50. Offboarding respects documented expiry/revalidation/revocation bounds.
   Owners: [team-auth](../tasks/t-20261018-r27-team-auth.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [candidate-ingress](../tasks/t-20261018-r27-candidate-ingress.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
51. CLI/JSON/MCP/HTTP share decisions and actor attribution; onboarding is separate from bootstrap.
   Owners: [team-auth](../tasks/t-20261018-r27-team-auth.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [candidate-ingress](../tasks/t-20261018-r27-candidate-ingress.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
52. Pre-freeze Core/HTTP/contract-fixture evidence is explicitly separated from real Kubernetes lifecycle implementation/acceptance in #102 (v0.7) and #320 (v0.8).
   Owners: [team-auth](../tasks/t-20261018-r27-team-auth.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [candidate-ingress](../tasks/t-20261018-r27-candidate-ingress.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).

### Managed Identity administration

53. A team using the existing BaseHarbor-managed Identity service can create/invite a colleague, assign an access profile and onboard them without external SSO.
   Owners: [managed-users](../tasks/t-20261018-r27-managed-users.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
54. Profiles reuse organization/team configuration and support one or multiple Targets with explicit operation/scope/environment permissions.
   Owners: [managed-users](../tasks/t-20261018-r27-managed-users.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
55. Account activation/password/MFA stays with the authentication service; no copied administrator token or second user database is needed.
   Owners: [managed-users](../tasks/t-20261018-r27-managed-users.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
56. Provider management capabilities/permissions are checked before mutation; unsupported administration is actionable.
   Owners: [managed-users](../tasks/t-20261018-r27-managed-users.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
57. Repeated onboarding is idempotent; ambiguous existing identities are rejected.
   Owners: [managed-users](../tasks/t-20261018-r27-managed-users.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
58. Non-admin users cannot create users or grant/revoke access; profile tampering/import cannot elevate permissions.
   Owners: [managed-users](../tasks/t-20261018-r27-managed-users.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
59. CLI/JSON/MCP/HTTP share Core authorization and provider-adapter behavior; Console has no independent identity/access store.
   Owners: [managed-users](../tasks/t-20261018-r27-managed-users.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md). Console UI proof remains in [v0.4.28](../releases/v0.4.28.md); v0.4.27 owns domain/API parity.
60. Management operations are excluded from the Application Runtime REST API.
   Owners: [managed-users](../tasks/t-20261018-r27-managed-users.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
61. Onboarding profile/reference contains no default secret/session export; any enrollment capability has the stated lifetime/recipient/replay protections.
   Owners: [managed-users](../tasks/t-20261018-r27-managed-users.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
62. Access change/revocation is verified against effective permissions and documented stale-session bounds; unrelated identity/provider resources survive.
   Owners: [managed-users](../tasks/t-20261018-r27-managed-users.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
63. General account/business-user administration for other applications remains out of scope.
   Owners: [managed-users](../tasks/t-20261018-r27-managed-users.md), [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).

### Guided removal and offboarding

64. An operator can remove only BaseHarbor access without deleting the underlying managed Identity user.
   Owners: [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
65. Managed-user deletion is a separate explicit guided action with impact review and permission check.
   Owners: [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
66. A Dev Remote workstation can be revoked independently without affecting other workstations or remote application/platform state.
   Owners: [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
67. Local connection removal cannot accidentally delete or revoke the remote installation.
   Owners: [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
68. The wizard distinguishes local cleanup, remote device revocation and unused enrollment revocation.
   Owners: [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
69. Back/cancel and failed authorization/state revalidation produce no partial destructive mutation.
   Owners: [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).

### Topology and authority

70. Topology documents independent local/Dev/Prod authorities, their admitted Targets, identity ownership and explicit secret-store placement.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
71. One installation supports multiple admitted Targets without one mandatory Core per Target; Target and management connection remain distinct.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
72. Two authorized workstations connected to the same installation observe one authoritative deployment/provider state and the same permitted Target references, with bounded conflict handling.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
73. Dev and Prod need no Baha-to-Baha traffic, registry/user/grant synchronization, shared administrator credential or Dev-owned dependency.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
74. The client connects directly to the selected authorized Core; network isolation is not bypassed by forwarding, profile import or cached metadata.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
75. Managed-Identity onboarding completes through account invitation/activation, scoped profile assignment and minimal profile import without external SSO, duplicate user storage or developer OpenBao setup.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
76. Anonymous shared-Dev access and environment-label-based trusted-local escalation are denied.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
77. Target listing and all operations enforce the selected installation's identity and operation/resource scope; Dev identities/sessions/profiles cannot implicitly authorize Prod.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
78. Copied/tampered profiles, equal local aliases and stale client metadata do not create grants or redirect credentials to an untrusted installation.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
79. Wrong/unavailable remote store fails explicitly; no cross-installation store fallback or default remote-secret export occurs.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
80. Grant/revoke is verified independently in each boundary, including documented stale-session bounds; no global offboarding guarantee is presented.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
81. Standalone local Docker/Podman use still works without remote services or login; native kube/Git/cloud authentication remains first-class.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
82. Namespace-first and explicit cluster-wide scopes are covered by contract fixtures and linked Kubernetes requirements, without claiming completed Kubernetes runtime acceptance.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
83. CLI/JSON/MCP/management HTTP and Console share Core policy, actor attribution and provider adapters; no independent Console identity/access store or Application Runtime management route is introduced.
   Owners: [authority-contract](../tasks/t-20261018-r27-authority-contract.md), [connection-client](../tasks/t-20261018-r27-connection-client.md), [state-owner](../tasks/t-20261018-r27-state-owner.md), [mutation-lock](../tasks/t-20261018-r27-mutation-lock.md), [team-proof](../tasks/t-20261018-r27-team-proof.md). Console UI proof remains in [v0.4.28](../releases/v0.4.28.md); v0.4.27 owns domain/API parity.

### Dev Local and Dev Remote

84. Dev Local works without login, onboarding bundle or remote Core.
   Owners: [device-enrollment](../tasks/t-20261018-r27-device-enrollment.md), [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
85. A fresh authorized workstation can connect to a trusted Dev Remote Core by importing one enrollment bundle and can immediately perform permitted operations without interactive login.
   Owners: [device-enrollment](../tasks/t-20261018-r27-device-enrollment.md), [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
86. Import validates Core destination/trust and bundle integrity before persisting or using credential material.
   Owners: [device-enrollment](../tasks/t-20261018-r27-device-enrollment.md), [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
87. The imported device identity is bounded, auditable, renewable and individually revocable.
   Owners: [device-enrollment](../tasks/t-20261018-r27-device-enrollment.md), [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
88. Two independently enrolled workstations can use the same Dev Remote Core and observe one authoritative remote state.
   Owners: [device-enrollment](../tasks/t-20261018-r27-device-enrollment.md), [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
89. Revoking workstation A does not revoke workstation B.
   Owners: [device-enrollment](../tasks/t-20261018-r27-device-enrollment.md), [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
90. No Core/OpenBao recovery/root material, provider administrator credential or remote application secret is included in the enrollment bundle.
   Owners: [device-enrollment](../tasks/t-20261018-r27-device-enrollment.md), [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
91. Secret-bearing import material is never emitted into logs, evidence, normal machine output or portable Application Intent.
   Owners: [device-enrollment](../tasks/t-20261018-r27-device-enrollment.md), [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
92. Trusted Dev Remote cannot be selected merely by naming an environment `dev`; it requires explicit installation policy/enrollment.
   Owners: [device-enrollment](../tasks/t-20261018-r27-device-enrollment.md), [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).
93. Shared-team/Test/Prod onboarding continues to use authenticated user/session flows and does not inherit this trusted-device shortcut.
   Owners: [device-enrollment](../tasks/t-20261018-r27-device-enrollment.md), [device-lifecycle](../tasks/t-20261018-r27-device-lifecycle.md), [client-commands](../tasks/t-20261018-r27-client-commands.md), [onboarding-wizard](../tasks/t-20261018-r27-onboarding-wizard.md), [team-proof](../tasks/t-20261018-r27-team-proof.md), [local-parity-proof](../tasks/t-20261018-r27-local-parity-proof.md).

### v0.4.24 handoff

94. Import/enrollment binds the local developer device to one explicitly selected management Core without treating that Core as a deployment Target. `baha use` selects the intended context; application placement remains a separate Target decision with deterministic explicit-argument precedence.
   Owners: [connection-client](../tasks/t-20261018-r27-connection-client.md), [node-cli](../tasks/t-20261018-r27-node-cli.md), [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [public-surfaces](../tasks/t-20261018-r27-public-surfaces.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
95. A portable developer profile/enrollment bundle holds only Core/Target references, scope, public trust anchors and revocable device credentials as explicitly permitted; never exports OpenBao unseal keys, Keycloak provider-admin credentials, live SQL backups, etcd DCS snapshots or Patroni state.
   Owners: [connection-client](../tasks/t-20261018-r27-connection-client.md), [node-cli](../tasks/t-20261018-r27-node-cli.md), [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [public-surfaces](../tasks/t-20261018-r27-public-surfaces.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
96. Local Dev remains usable without BaseHarbor login. Dev Remote uses Core-authorized device enrollment, scoped mTLS and optional organization OIDC; reconnect/renew/revoke/offboard follow the existing #846 Node/Target-access contracts, not a duplicate credential engine.
   Owners: [connection-client](../tasks/t-20261018-r27-connection-client.md), [node-cli](../tasks/t-20261018-r27-node-cli.md), [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [public-surfaces](../tasks/t-20261018-r27-public-surfaces.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
97. Test a revoked/expired/imported-into-wrong-Core profile, foreign installation and multi-Core selection as negatives; fail closed with a secret-safe reason and concrete next action.
   Owners: [connection-client](../tasks/t-20261018-r27-connection-client.md), [node-cli](../tasks/t-20261018-r27-node-cli.md), [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [public-surfaces](../tasks/t-20261018-r27-public-surfaces.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
98. Separate export/import for developer convenience from service backup/restore and disaster recovery. Provider recovery in #837/#845/#847/#848 remains installation-owned and requires independent verification; profile import is not a substitute.
   Owners: [connection-client](../tasks/t-20261018-r27-connection-client.md), [node-cli](../tasks/t-20261018-r27-node-cli.md), [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [public-surfaces](../tasks/t-20261018-r27-public-surfaces.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
99. Human wizard, noninteractive CLI, JSON and MCP expose the same resolved authority, ownership, allowed next action and remediation. Console consumption does not introduce a second management authority.
   Owners: [connection-client](../tasks/t-20261018-r27-connection-client.md), [node-cli](../tasks/t-20261018-r27-node-cli.md), [profile-codec](../tasks/t-20261018-r27-profile-codec.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [public-surfaces](../tasks/t-20261018-r27-public-surfaces.md), [team-proof](../tasks/t-20261018-r27-team-proof.md). Console UI proof remains in [v0.4.28](../releases/v0.4.28.md); v0.4.27 owns domain/API parity.

### Team/access profile wizard (comment 2026-10-05)

100. An authorized administrator creates a scoped team/access profile through name → Target multi-selection → rights → review, without provider/OpenBao configuration questions.
   Owners: [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
101. Small, large and duplicate-name Target lists remain usable; search, keyboard selection, pagination and preserved selections are demonstrated.
   Owners: [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
102. Effective rights per selected Target, installation identity and namespace/cluster-wide scope are clear before confirmation.
   Owners: [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
103. Back/cancel, empty/no-match/denied/offline states and stale selection conflicts have actionable behavior and no unintended mutation.
   Owners: [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
104. Profile creation, identity/group assignment and connection-profile export remain distinct; file import cannot confer server-side rights.
   Owners: [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
105. Dev profile creation cannot enumerate or grant Prod access through another independent installation.
   Owners: [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
106. Suggested roles/presets are understandable defaults, not a second identity directory or mandatory provider-specific role scheme.
   Owners: [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md).
107. CLI and Console demonstrate the same wizard semantics; JSON/MCP execute the equivalent validated operation without prompts.
   Owners: [access-profiles](../tasks/t-20261018-r27-access-profiles.md), [access-wizard](../tasks/t-20261018-r27-access-wizard.md), [access-proof](../tasks/t-20261018-r27-access-proof.md). Console UI proof remains in [v0.4.28](../releases/v0.4.28.md); v0.4.27 owns domain/API parity.

## Additional confirmed gaps

- Laptop-independent immutable deployment candidate and explicit image/build location: [candidate-contract](../tasks/t-20261018-r27-candidate-contract.md), [candidate-pack](../tasks/t-20261018-r27-candidate-pack.md), [candidate-ingress](../tasks/t-20261018-r27-candidate-ingress.md), [artifact-resolution](../tasks/t-20261018-r27-artifact-resolution.md).
- Restart-safe execution status and lost-response reconciliation: [execution-journal](../tasks/t-20261018-r27-execution-journal.md), [journal-wiring](../tasks/t-20261018-r27-journal-wiring.md), [state-recovery](../tasks/t-20261018-r27-state-recovery.md), [team-proof](../tasks/t-20261018-r27-team-proof.md).
- Remote web exposure remains explicitly rejected in the current guard: [remote-material](../tasks/t-20261018-r27-remote-material.md), [remote-docker-web](../tasks/t-20261018-r27-remote-docker-web.md), [remote-podman-web](../tasks/t-20261018-r27-remote-podman-web.md). Enable only independently qualified capabilities.
- Future three-runtime video: [video-proof](../tasks/t-20261018-r27-video-proof.md) proves Docker/Podman now; K3s proof/support remains on its existing roadmap.

- Shared minimal host and existing API dependency reconciliation: [management-host](../tasks/t-20261018-r27-management-host.md).
- Safe maintenance paths and archive/secret input transfer: [maintenance-client](../tasks/t-20261018-r27-maintenance-client.md).

- Changed remote publication and retained-owner transition: [remote-rollout](../tasks/t-20261018-r27-remote-rollout.md); first deployment/read-only parity alone cannot satisfy the two-developer update acceptance.

## Native delivery and real-world stage additions (2026-10-18)

Original 107 criteria remain unchanged. The following additions refine their operational implementation, not replace them.

- [delivery-boundary](../tasks/t-20261018-r27-delivery-boundary.md): bounded standards-first slice with explicit predecessor, owned paths and selected checks.
- [registry-access](../tasks/t-20261018-r27-registry-access.md): bounded standards-first slice with explicit predecessor, owned paths and selected checks.
- [image-transfer](../tasks/t-20261018-r27-image-transfer.md): bounded standards-first slice with explicit predecessor, owned paths and selected checks.
- [local-registry](../tasks/t-20261018-r27-local-registry.md): bounded standards-first slice with explicit predecessor, owned paths and selected checks.
- [stage-versions](../tasks/t-20261018-r27-stage-versions.md): bounded standards-first slice with explicit predecessor, owned paths and selected checks.
- [version-view](../tasks/t-20261018-r27-version-view.md): bounded standards-first slice with explicit predecessor, owned paths and selected checks.
- [promote](../tasks/t-20261018-r27-promote.md): bounded standards-first slice with explicit predecessor, owned paths and selected checks.
- [ci-consumption](../tasks/t-20261018-r27-ci-consumption.md): bounded standards-first slice with explicit predecessor, owned paths and selected checks.
- [delegated-handoff](../tasks/t-20261018-r27-delegated-handoff.md): bounded standards-first slice with explicit predecessor, owned paths and selected checks.

The existing video-proof ID now owns real multi-stage/artifact/promotion acceptance; filming is optional. No product support or acceptance is implied by these cards.
