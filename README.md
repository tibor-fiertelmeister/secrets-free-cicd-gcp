# Secrets-Free CI/CD on Google Cloud

A security-focused reference implementation demonstrating
how CI/CD pipelines can authenticate to Google Cloud without
storing long-lived cloud credentials.

> Project status: Under active development.

## Project Overview

Traditional CI/CD pipelines often rely on long-lived service
account keys to authenticate to cloud environments.

These credentials introduce security risks, including
credential leakage, unauthorized access, excessive privileges,
and operational overhead associated with key rotation.

This project explores a keyless authentication architecture
using GitHub Actions, OpenID Connect (OIDC), and Google Cloud
Workload Identity Federation (WIF).

## Objectives

- Eliminate stored long-lived cloud credentials from CI/CD.
- Use short-lived, federated workload identities.
- Enforce least privilege IAM permissions.
- Restrict authentication to authorized GitHub workflows.
- Manage cloud infrastructure through Infrastructure as Code.
- Validate security controls through positive and negative tests.
- Document architectural decisions and residual risks.

## Technology Stack

| Technology | Purpose |
|---|---|
| GitHub Actions | CI/CD automation |
| OpenID Connect | Federated workload authentication |
| Google Cloud WIF | Identity federation and trust management |
| Google Cloud IAM | Authorization and access control |
| Terraform | Infrastructure as Code |

## Security by Design

The proposed architecture follows these security principles:

- No long-lived service account keys.
- Least privilege access.
- Explicit identity trust boundaries.
- Separation of authentication and authorization.
- Restricted workflow permissions.
- Secure handling of infrastructure state.
- Reproducible security validation.

## Project Roadmap

- [x] Repository initialization
- [ ] Architecture design
- [ ] Threat modeling
- [ ] GCP sandbox environment
- [ ] Terraform infrastructure
- [ ] OIDC and Workload Identity Federation
- [ ] Least privilege IAM implementation
- [ ] CI/CD pipeline implementation
- [ ] Security hardening
- [ ] Positive and negative security testing
- [ ] Final documentation and deployment evidence

## Cost Considerations

The project is designed as a minimal-cost cloud security lab.

It avoids continuously running compute resources and uses
only the cloud services necessary to demonstrate secure
workload authentication and authorization.

## Scope and Limitations

This is an educational security reference implementation,
not a production-ready deployment.

Security controls will be documented and validated
incrementally throughout the project.

## License

This project is licensed under the MIT License.
