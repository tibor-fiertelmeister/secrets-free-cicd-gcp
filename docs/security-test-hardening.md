# Structured security testing

The existing baseline tests remain in place. Additional tests parse HCL and YAML, enforce a narrow resource and workflow allowlist, and exercise deliberately weakened configurations in memory. The HCL trust expression is compared against the expected serialized expression, not evaluated as CEL. YAML uses BaseLoader to preserve `on` and rejects duplicate mapping keys.

Dependencies are pinned with hashes for CPython 3.12 Windows amd64 and Linux x86_64 wheels. CI uses Ubuntu 24.04 and its Python 3.12 interpreter; the runner image and Python patch release remain mutable.

## Dependency lock

| Package | Version | SHA-256 hashes |
| --- | --- | --- |
| python-hcl2 | 8.2.0 | 1 |
| PyYAML | 6.0.4 | 2 |
| lark | 1.3.1 | 1 |
| regex | 2026.11.24 | 2 |

The four packages and six wheel hashes are recorded in `requirements-dev.txt`. Hash-enforced binary-only installation passed locally using downloaded Windows wheels and in Linux CI. Local `pip check` reported no broken requirements.

## Validation

Run `python -m unittest discover -s tests -v` in the activated virtual environment.

| Evidence | Result |
| --- | --- |
| Local Windows baseline before hardening | 6/6 passed, 0.013 s |
| Local Windows after hardening | 11/11 passed, 0.319 s |
| GitHub Actions Offline CI #12 | 11/11 passed, 1.136 s |
| CI #12 validate job | Passed, 24 s |
| CI #12 hash-locked dependency installation | Passed |
| CI #12 Terraform read-only initialization and validation | Passed |

The 11 unittest methods comprise six baseline methods, two structured validation methods and three mutation test methods (Terraform mutations, workflow mutations and duplicate YAML keys). Mutation methods may exercise multiple cases; the method count is not a count of individual attack scenarios. The tests do not modify the deployed cloud environment.

Evidence: [GitHub Actions runs](https://github.com/tibor-fiertelmeister/secrets-free-cicd-gcp/actions), Offline CI #12 on `hardening/security-tests`, and local Windows console output.

## Limitations

This is a project-specific static regression gate, not a general Terraform policy engine. It does not evaluate Terraform plans, arbitrary expressions, shell scripts, inherited IAM, GitHub repository settings, or cloud state. Exact expression matching may reject equivalent changes. The gate itself can be modified by a PR. Dependency provenance and vulnerability assessment, live OIDC exchange, and actual IAM denial remain unverified. Passing tests establish only the behavior covered by the implemented checks.
