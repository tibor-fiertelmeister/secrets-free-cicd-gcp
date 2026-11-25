# Supply chain hardening

External actions are pinned to full commit SHAs obtained from upstream release tags. Pinning limits mutable-tag risk; it does not establish that the pinned code is safe. Dependabot proposes weekly updates for review.

The baseline tests check textual markers and action references in current YAML files; they are not a semantic policy engine. Failure messages avoid dumping entire configuration files.

Negative IAM test evidence: [PR #1](https://github.com/tibor-fiertelmeister/secrets-free-cicd-gcp/pull/1). The prohibited role was detected and the required checks blocked merging.

Pending: verify updated action runtime compatibility in CI, generate and commit the Terraform provider lock file, pin CLI versions, and validate cloud deployment in a sandbox. No live cloud validation is claimed.
