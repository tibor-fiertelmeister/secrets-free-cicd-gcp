# Security Test Plan

| Test | Expected | Status |
|---|---|---|
| Offline baseline assertions | Pass | Local execution only |
| Terraform validation | Pass | Pending |
| Main manual deployment | Object created | Pending |
| List objects as runtime | 403 with storage.objects.list | Pending; workflow includes check |
| Read/delete object as runtime | Permission denied | Pending |
| Fork with its own valid OIDC token | STS rejects trust condition | Pending |
| Feature branch token exchange | STS rejects trust condition | Pending |
| Different workflow or event | STS rejects trust condition | Pending |
| Invalid audience or expired token | STS rejects token | Pending |

Negative identity tests require a controlled test workflow that actually requests a token and attempts exchange; a skipped job is not proof of STS rejection. Never weaken the production trust condition for testing. Record sanitized evidence and distinguish permission denial from network or configuration failures. Static tests are string-level regression checks, not proof of effective IAM.
