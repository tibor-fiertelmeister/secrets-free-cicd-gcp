# Structured security testing

The existing baseline tests remain in place. Additional tests parse HCL and YAML, enforce a narrow resource and workflow allowlist, and exercise deliberately weakened configurations in memory. The HCL trust expression is compared against the expected serialized expression, not evaluated as CEL. YAML uses BaseLoader to preserve `on` and rejects duplicate mapping keys.

Dependencies are pinned with hashes for CPython 3.12 Windows amd64 and Linux x86_64 wheels. CI uses Ubuntu 24.04 and its Python 3.12 interpreter; the runner image and Python patch release remain mutable.

## Validation

Run `python -m unittest discover -s tests -v` in the activated virtual environment. The Windows dependency installation has passed; structured tests and Linux CI are pending validation at package creation.

## Limitations

This is a project-specific static regression gate, not a general Terraform policy engine. It does not evaluate Terraform plans, arbitrary expressions, shell scripts, inherited IAM, GitHub repository settings, or cloud state. Exact expression matching may reject equivalent changes. The gate itself can be modified by a PR. Dependency provenance and vulnerability assessment, live OIDC exchange, and actual IAM denial remain unverified.
