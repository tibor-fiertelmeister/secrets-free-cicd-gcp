# Secrets-Free CI/CD on Google Cloud

A security-focused learning lab exploring GitHub Actions OIDC, Google Cloud Workload Identity Federation, Terraform and least-privilege IAM.

**Status: prototype - static security tests, dependency vulnerability gate and secret scanning gate validated; cloud deployment and live security validation pending.**

The intended runtime identity can upload a harmless artifact to one private Cloud Storage bucket without listing or reading objects. No long-lived cloud key is intended to be required. Bootstrap is performed separately by a human administrator.

## Security controls and evidence

| Control | Status |
| --- | --- |
| Branch protection and required CI checks | Verified by negative IAM, dependency and secret scanning tests |
| Excessive IAM role detection | Text-marker and structured regression tests passed |
| Full action SHA pinning | Configured; format checked in CI |
| Invalid SHA format detection | CI run #4 failed; corrected in #5 |
| Terraform provider locking and read-only initialization | Verified locally and in CI runs #6 and #12 |
| Windows and Linux provider checksums | Generated |
| Terraform CLI 1.17.2 | Configured and validated in CI |
| Google Cloud CLI 594.0.1 | Configured; runtime validation pending |
| Dependabot weekly updates | Provider update PR #3 observed; Python updates configured, not yet verified |
| Structured HCL and YAML validation | Passed locally and in CI runs #12 and #16 |
| Mutation testing | Passed locally and in CI runs #16 and #22 |
| Python test dependency locking | Four packages, six SHA-256 hashes; Windows and Linux installation passed |
| Scanner dependency locking | 29 packages, 32 SHA-256 hashes; Windows and Linux installation passed |
| Dependency vulnerability scanning | Both requirements files passed locally and in CI run #16 on 2026-11-26 |
| Vulnerability gate enforcement | PR #5: vulnerable dependency detected, installation skipped, required checks failed, merge disabled |
| Secret scanning | Gitleaks 8.30.1; clean CI run #22 passed |
| Secret scanning gate enforcement | Synthetic AWS identifier detected and redacted; push and PR checks failed; merge disabled |
| OIDC / WIF / effective least privilege | Pending live cloud validation |

## Validation evidence

- [PR #1 - negative IAM test](https://github.com/tibor-fiertelmeister/secrets-free-cicd-gcp/pull/1), closed without merging.
- [PR #5 - negative dependency test](https://github.com/tibor-fiertelmeister/secrets-free-cicd-gcp/pull/5), closed without merging.
- [CI runs](https://github.com/tibor-fiertelmeister/secrets-free-cicd-gcp/actions): run #12 passed 11 unittest methods; run #16 passed 12 methods and both dependency audits. Local Windows validation also passed 12 methods.
- Secret scanning: run #22 passed 13 unittest methods; local Windows validation also passed 13 methods. Runs #23 and #24 did not detect the initial synthetic samples. A subsequent push detected the corrected sample, and both required checks failed on the negative-test PR. See the [secret scanning evidence](docs/secret-scanning.md).

The Dependabot major provider upgrade in PR #3 remains subject to review.

## Documentation

- [Architecture and authentication flow](docs/architecture.md)
- [Threat model](docs/threat-model.md)
- [Security decisions](docs/security-decisions.md)
- [Setup and cleanup](docs/setup.md)
- [Security test plan](tests/security-tests.md)
- [Supply chain hardening](docs/supply-chain-hardening.md)
- [Structured security testing and evidence](docs/security-test-hardening.md)
- [Dependency vulnerability scanning and enforcement evidence](docs/vulnerability-scanning.md)
- [Secret scanning and enforcement evidence](docs/secret-scanning.md)

## Local checks

Use CPython 3.12 on Windows amd64 or Linux x86_64. First create a separate scanner environment:

```sh
python -m venv .venv-audit
```

Activate it in Windows CMD with `.venv-audit\Scripts\activate.bat`, or on Linux with `source .venv-audit/bin/activate`. Then run:

```sh
python -m pip install --require-hashes --only-binary=:all: -r requirements-audit.txt
python -m pip check
python -m pip_audit -r requirements-audit.txt --require-hashes --strict
python -m pip_audit -r requirements-dev.txt --require-hashes --strict
```

Stop if any command fails. Only after both audits pass, deactivate the scanner environment and create the test environment:

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

The workflow named Offline CI does not request cloud credentials, but uses network services for dependency downloads and vulnerability advisories. Secret scanning runs in GitHub Actions; the local unittest suite checks gate configuration rather than executing Gitleaks. Deployment is manually triggered and requires a configured sandbox. Do not run it before completing setup.

## Costs and limitations

No persistent compute is planned. Storage, operations and logging may incur charges if deployed. No cloud tests have been executed yet. This is a learning lab, not production-ready. Static tests are project-specific regression checks, not a semantic policy engine or proof of effective IAM. The gate itself can be modified by a PR. Action pinning and package hashes do not establish source trust or absence of vulnerabilities. Vulnerability scanning covers known advisories for the listed Python dependencies at scan time, not Terraform providers, GitHub Actions or cloud workloads. No scheduled vulnerability scan is configured. Secret scanning is pattern-based; full Git history coverage and detection of arbitrary secrets are not established. Hosted runner images and Python patch versions remain mutable. Local state must not be committed.

## License

MIT (existing repository license).
