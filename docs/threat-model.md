# Threat Model

Scope: public repository, hosted runner, OIDC issuer, STS, IAM Credentials API, service account, private artifact bucket and local Terraform state. Assets: temporary tokens, trust configuration, state, repository integrity and artifacts.

| Threat | Control | Residual risk / verification |
|---|---|---|
| Fork requests a valid token | Numeric repository and owner IDs | Live fork rejection pending |
| Untrusted branch or event | Exact ref, event and workflow_ref conditions | Live negative tests pending |
| Token tampering or wrong audience | STS signature, issuer, expiry and audience validation | Live validation pending |
| Compromised main workflow | Branch protection, review, pinned actions | Authorized code can still misuse its access |
| Excessive IAM | Bucket-scoped objectCreator | Can create arbitrary objects and incur costs |
| Credential theft | Temporary tokens, no token logging | Replay possible before expiry |
| State disclosure | Local state ignored, restricted filesystem | Local compromise or accidental upload |
| Supply-chain compromise | Review and SHA-pin actions before cloud activation | Runner and dependencies remain trusted |
| Cost abuse | Manual trigger, dedicated sandbox, cleanup | Budgets are alerts, not hard caps |

Trust boundaries: GitHub to Google Cloud; bootstrap administrator to runtime identity; runtime identity to target bucket. Do not use corporate data or production credentials.
