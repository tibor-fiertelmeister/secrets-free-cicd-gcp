# Supply chain hardening

External actions are pinned to full commit SHAs obtained from upstream release tags. Pinning limits mutable-tag risk; it does not establish that pinned code is safe. Dependabot is configured for weekly GitHub Actions and Terraform updates for review; operation remains unverified.

The Terraform CLI is pinned to 1.17.2. The Google provider lock file records 6.50.0 and checksums generated for Windows and Linux AMD64. CI uses read-only dependency initialization. Google Cloud CLI is configured at 594.0.1 ([release notes](https://docs.cloud.google.com/sdk/docs/release-notes)); deployment runtime validation is pending.

## Evidence

- [PR #1](https://github.com/tibor-fiertelmeister/secrets-free-cicd-gcp/pull/1): prohibited IAM role marker detected and required checks blocked merging.
- Offline CI #4: malformed action SHA detected. Run #5 passed after correction (fe37ac7).
- Offline CI #6: read-only initialization and baseline tests passed (116a2aa). Local Windows initialization and validation also passed.
- The additional lock-file and CLI pinning marker tests require a new CI run.

## Limitations

Baseline tests inspect textual markers, not effective IAM or semantic workflow policy. SHA format checking does not establish commit existence or provenance. Failure messages avoid dumping entire configuration files. CLI version pins do not independently attest binary integrity. Hosted runner images remain mutable. Deployment actions, cloud authentication and effective permissions remain untested in a live sandbox. No live cloud validation is claimed.
