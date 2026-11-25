# Secrets-Free CI/CD on Google Cloud

A security-focused learning lab exploring GitHub Actions OIDC, Google Cloud Workload Identity Federation, Terraform and least-privilege IAM.

**Status: prototype — offline CI validated; cloud deployment and live security validation pending.**

The intended runtime identity can upload a harmless artifact to one private Cloud Storage bucket without listing or reading objects. No long-lived cloud key is intended to be required. Bootstrap is performed separately by a human administrator.

## Security controls and evidence

| Control | Status |
| --- | --- |
| Branch protection and required CI checks | Verified by negative IAM test |
| Excessive IAM role detection | Verified for a prohibited text marker |
| Full action SHA pinning | Configured; format checked in CI |
| Invalid SHA format detection | Verified in CI run #4; corrected in #5 |
| Terraform provider locking and read-only initialization | Verified locally and in CI run #6 |
| Windows and Linux provider checksums | Generated |
| Terraform CLI 1.17.2 | Configured; CI run #6 passed |
| Google Cloud CLI 594.0.1 | Configured; runtime validation pending |
| Dependabot weekly updates | Configured; operation not verified |
| OIDC / WIF / effective least privilege | Pending live cloud validation |

Negative IAM test: [PR #1](https://github.com/tibor-fiertelmeister/secrets-free-cicd-gcp/pull/1), closed without merging. See [CI runs](https://github.com/tibor-fiertelmeister/secrets-free-cicd-gcp/actions) for build evidence.

## Documentation

- [Architecture and authentication flow](docs/architecture.md)
- [Threat model](docs/threat-model.md)
- [Security decisions](docs/security-decisions.md)
- [Setup and cleanup](docs/setup.md)
- [Security test plan](tests/security-tests.md)
- [Supply chain hardening](docs/supply-chain-hardening.md)

## Local checks

```sh
python -m unittest discover -s tests -v
terraform -chdir=terraform init -backend=false -lockfile=readonly
terraform -chdir=terraform validate
```

Offline CI does not request cloud credentials. Internet access is needed for downloading dependencies. Deployment is manually triggered and requires a configured sandbox. Do not run it before completing setup.

## Costs and limitations

No persistent compute is planned. Storage, operations and logging may incur charges if deployed. No cloud tests have been executed yet. This is a learning lab, not production-ready. Text-based tests are not a semantic policy engine. Action pinning is not a source-code audit. Hosted runner images remain mutable. Local state must not be committed.

## License

MIT (existing repository license).
