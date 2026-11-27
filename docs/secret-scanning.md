# Secret scanning and enforcement evidence

## Security problem and threat model

Keyless cloud authentication removes the need for a long-lived cloud service account key in the intended deployment flow. It does not prevent developers from accidentally committing other credentials. A credential committed to a public repository may already be exposed before CI runs. The objective of this control is to detect supported credential patterns and prevent changes that fail required CI checks from merging into main.

## Implementation

Offline CI runs Gitleaks immediately after checkout, before Terraform initialization, dependency installation and security unit tests. The action is pinned to a full commit SHA and the Gitleaks version is configured as 8.30.1. Checkout uses `fetch-depth: 0` and `persist-credentials: false`. The workflow retains read-only contents permissions and does not request cloud OIDC credentials. The action receives the ephemeral GitHub-provided `GITHUB_TOKEN`, not a long-lived cloud key.

Comments, artifact uploads and summaries are disabled through the action configuration. Observed scanner commands use redaction and a nonzero finding exit code (`--exit-code=2`). The default detection rules are used. Structured policy regression tests and mutation tests check the secret scanning gate configuration. These tests complement rather than replace actual scanner execution.

## Validation evidence — 2026-11-27

| Test | Observed result | Interpretation |
| --- | --- | --- |
| Clean branch, CI #22 | No leaks found; 13 unittest methods passed | Positive CI path works |
| Negative attempt, CI #23 | One commit scanned; no leaks found | AWS documentation example ends in EXAMPLE, matching the rule allowlist |
| Negative attempt, CI #24 | One commit scanned; no leaks found | Generated identifier contains digits outside the rule's A-Z / 2-7 character set |
| Corrected synthetic sample, commit `1c93ccc` | One finding; rule `aws-access-token`; entropy 4.021928; secret redacted; validate job failed | Actual scanner detection and push gate enforcement demonstrated |
| Negative-test pull request | Both required push and pull_request checks failed; merge button disabled | Branch protection enforcement demonstrated for this test |
| Local Windows regression suite | 13 unittest methods passed | Configuration regression tests passed |

The initial two samples were unsuitable for the intended negative test. Inspection of the version-specific AWS rule identified a restricted character set, an entropy threshold of 3, and an EXAMPLE suffix allowlist. These explain the observed non-detections consistently with the rule, although internal rule evaluation was not separately traced. The third sample matched the rule without changing the scanner configuration. No real credential or cloud resource was used. The successful push log showed the secret value as REDACTED and the subsequent Terraform setup step was skipped.

Evidence: [GitHub Actions runs](https://github.com/tibor-fiertelmeister/secrets-free-cicd-gcp/actions), [negative-test branch](https://github.com/tibor-fiertelmeister/secrets-free-cicd-gcp/tree/test/secret-scanning-gate). The negative-test branch must not be merged. The clean hardening branch was checked with `git ls-files secret-scanning-test.txt`, which returned no tracked file. The PR number and closure status were not recorded in the supplied evidence.

## Limitations and residual risks

- Pattern matching and entropy thresholds can miss secrets or flag harmless strings. One successful synthetic AWS identifier test does not establish universal detection.
- Observed push runs scanned one commit using `--log-opts=-1`. Full checkout history availability does not establish full-history scanning. The exact PR scan range and PR scanner failure details have not been independently inspected.
- CI executes after push; merge protection does not prevent initial disclosure. Push protection, local pre-commit scanning and credential revocation procedures are complementary controls, not validated here.
- The action is SHA-pinned and the binary version is configured, but independent binary checksum and provenance verification have not been demonstrated. The logs also show Node.js dependency deprecation warnings.
- A PR can modify the workflow and its regression tests. Independent policy ownership and review controls would be needed for stronger production assurance.
- No live cloud authentication, effective IAM or credential revocation testing has been performed.
