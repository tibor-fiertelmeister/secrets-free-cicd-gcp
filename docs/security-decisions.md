# Security Decisions

- ADR-001: OIDC instead of static keys. Reduces persistent credential exposure; temporary credentials remain sensitive.
- ADR-002: Dedicated pool and provider with numeric IDs, main branch, manual event and exact workflow path. Names alone can be reused. A compromised trusted workflow remains dangerous.
- ADR-003: Service account impersonation for explicit separation of federation and resource authorization. Direct federation is an alternative with fewer steps.
- ADR-004: Bucket-scoped objectCreator, not project Editor. Demonstrates artifact deployment without granting listing, reading or deletion. Bootstrap uses separate human credentials.
- ADR-005: Local state for the initial single-user lab. Remote protected state and locking are future improvements.
- ADR-006: Manual deployment; offline PR validation has no OIDC permission. Review and SHA-pin actions and configure branch protection before granting cloud access.
- ADR-007: EU storage, no persistent compute, no soft-delete retention for disposable artifacts. This trades recovery for reduced lab storage cost.
