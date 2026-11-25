# Secrets-Free CI/CD on Google Cloud

A security-focused reference implementation of GitHub Actions OIDC, Google Cloud Workload Identity Federation, Terraform and least privilege IAM.

**Status: v0.1.0 prototype. Cloud deployment and live security validation pending.**

The runtime identity can upload a harmless artifact to one private Cloud Storage bucket. It cannot list or read objects under the intended policy. No long-lived cloud key is required. Bootstrap is performed separately by a human administrator.

## Documentation

- [Architecture and authentication flow](docs/architecture.md)
- [Threat model](docs/threat-model.md)
- [Security decisions](docs/security-decisions.md)
- [Setup and cleanup](docs/setup.md)
- [Security test plan](tests/security-tests.md)

## Local checks

```sh
python -m unittest discover -s tests -v
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
```

Offline CI does not request cloud credentials. The deployment workflow is manually triggered and requires a configured sandbox. Do not run it before completing setup.

## Costs and limitations

No persistent compute. Storage, operations and logging may incur charges. This is a learning lab, not production-ready. Action version tags must be pinned to reviewed full commit SHAs before enabling cloud access. Local state must not be committed. No cloud tests have been executed yet.

## License

MIT (existing repository license).
