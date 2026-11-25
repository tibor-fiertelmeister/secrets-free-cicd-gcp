# Setup (do not execute until reviewed)

1. Create a dedicated personal GCP project and review billing, budget alerts and API requirements. Budgets do not cap spending.
2. Install Git, Terraform and Google Cloud CLI. Clone the repository. Authenticate locally with `gcloud auth application-default login`; use a separate administrator with the permissions needed to enable APIs, configure WIF/IAM and create the bucket. Never export a service account key.
3. Obtain numeric repository and owner IDs from the GitHub REST API `https://api.github.com/repos/OWNER/REPO` (fields `id` and `owner.id`). Copy `terraform.tfvars.example` to `terraform.tfvars` and fill in values. Ensure the repository path is correct.
4. Review and pin all actions to verified full commit SHAs. Configure main branch protection and review requirements appropriate for the repository. Do not enable cloud access before this step.
5. Run `terraform init`, `terraform fmt`, `terraform validate`, `terraform plan` and, after reviewing the plan, `terraform apply` from the terraform directory. Commit the generated provider lock file, never state or tfvars.
6. Set repository Actions variables WIF_PROVIDER, GCP_SERVICE_ACCOUNT and DEMO_BUCKET from Terraform outputs. These identifiers are not secrets. Allow time for IAM propagation.
7. Manually run the deployment workflow on main. Inspect results without printing tokens. Verify artifact existence with the separate administrator.
8. Cleanup: remove demo objects using the administrator, then run `terraform destroy` and review the plan. APIs are intentionally left enabled. Remove repository variables and delete the dedicated sandbox project if no longer needed. Review billing.

The bucket name must be globally unique. If it conflicts, adjust the Terraform name. Do not upload credentials, state, logs or plan files.
