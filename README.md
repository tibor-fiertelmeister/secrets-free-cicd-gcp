# Secrets-Free CI/CD on Google Cloud

A security-focused learning lab exploring GitHub Actions OIDC, Google Cloud Workload Identity Federation, Terraform and least-privilege IAM.

**Status: prototype - offline CI and structured security tests validated; cloud deployment and live security validation pending.**

The intended runtime identity can upload a harmless artifact to one private Cloud Storage bucket without listing or reading objects. No long-lived cloud key is intended to be required. Bootstrap is performed separately by a human administrator.

## Security controls and evidence

| Control | Status |
| --- | --- |
| Branch protection and required CI checks | Verified by negative IAM test in PR #1 |
| Excessive IAM role detection | Text-marker and structured regression tests passed |
| Full action SHA pinning | Configured; format checked in CI |
| Invalid SHA format detection | CI run #4 failed; corrected in #5 |
| Terraform provider locking and read-only initialization | Verified locally and in CI runs #6 and #12 |
| Windows and Linux provider checksums | Generated |
| Terraform CLI 1.17.2 | Configured and validated in CI |
| Google Cloud CLI 594.0.1 | Configured; runtime validation pending |
| Dependabot weekly updates | Execution observed; automated provider update PR #3 created |
| Structured HCL and YAML validation | Passed locally and in CI run #12 |
| Mutation testing | Passed locally and in CI run #12 |
| Python dependency locking | Four packages, six SHA-256 hashes; Windows and Linux installation passed |
| OIDC / WIF / effective least privilege | Pending live cloud validation |

Negative IAM test: [PR #1](https://github.com/tibor-fiertelmeister/secrets-free-cicd-gcp/pull/1), closed without merging. See [CI runs](https://github.com/tibor-fiertelmeister/secrets-free-cicd-gcp/actions) for build evidence. Offline CI run #12 passed all 11 unittest methods, as did local Windows validation. The Dependabot major provider upgrade in PR #3 remains subject to review.

## Documentation

- [Architecture and authentication flow](docs/architecture.md)
- [Threat model](docs/threat-model.md)
- [Security decisions](docs/security-decisions.md)
- [Setup and cleanup](docs/setup.md)
- [Security test plan](tests/security-tests.md)
- [Supply chain hardening](docs/supply-chain-hardening.md)
- [Structured security testing and evidence](docs/security-test-hardening.md)

## Local checks

Use CPython 3.12 on Windows amd64 or Linux x86_64. Create a virtual environment:

```sh
python -m venv .venv
```

Activate it in Windows CMD with `.venv\Scripts\activate.bat`, or on Linux with `source .venv/bin/activate`. Then run:

```sh
python -m pip install --require-hashes --only-binary=:all: -r requirements-dev.txt
python -m pip check
python -m unittest discover -s tests -v
terraform -chdir=terraform init -backend=false -lockfile=readonly
terraform -chdir=terraform validate
```

Offline CI does not request cloud credentials. Internet access is needed for downloading dependencies unless they are already available locally. Deployment is manually triggered and requires a configured sandbox. Do not run it before completing setup.

## Costs and limitations

No persistent compute is planned. Storage, operations and logging may incur charges if deployed. No cloud tests have been executed yet. This is a learning lab, not production-ready. Static tests are project-specific regression checks, not a semantic policy engine or proof of effective IAM. The gate itself can be modified by a PR. Action pinning and package hashes do not establish source trust or absence of vulnerabilities. Hosted runner images and Python patch versions remain mutable. Local state must not be committed.

## License

MIT (existing repository license).
