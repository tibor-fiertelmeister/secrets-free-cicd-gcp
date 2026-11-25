terraform {
  required_version = ">= 1.7, < 2.0"
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}
provider "google" {
  project = var.project_id
}
variable "project_id" { type = string }
variable "repository_id" { type = string }
variable "repository_owner_id" { type = string }
variable "repository" {
  type = string
  description = "GitHub owner/repository"
}
variable "region" {
  type = string
  default = "EU"
}
resource "google_project_service" "apis" {
  for_each = toset(["iam.googleapis.com", "iamcredentials.googleapis.com", "sts.googleapis.com", "storage.googleapis.com", "cloudresourcemanager.googleapis.com"])
  service = each.value
  disable_on_destroy = false
}
resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "github-cicd"
  depends_on = [google_project_service.apis]
}
resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"
  attribute_mapping = {
    "google.subject" = "assertion.sub"
    "attribute.repository_id" = "assertion.repository_id"
  }
  attribute_condition = join(" && ", [
    "assertion.repository_owner_id == '${var.repository_owner_id}'",
    "assertion.repository_id == '${var.repository_id}'",
    "assertion.ref == 'refs/heads/main'",
    "assertion.event_name == 'workflow_dispatch'",
    "assertion.workflow_ref == '${var.repository}/.github/workflows/deploy.yml@refs/heads/main'"
  ])
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}
resource "google_service_account" "runtime" {
  account_id = "github-cicd-runtime"
  depends_on = [google_project_service.apis]
}
resource "google_service_account_iam_member" "federation" {
  service_account_id = google_service_account.runtime.name
  role = "roles/iam.workloadIdentityUser"
  member = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository_id/${var.repository_id}"
}
resource "google_storage_bucket" "demo" {
  name = "${var.project_id}-cicd-demo"
  location = var.region
  uniform_bucket_level_access = true
  public_access_prevention = "enforced"
  force_destroy = false
  soft_delete_policy { retention_duration_seconds = 0 }
  depends_on = [google_project_service.apis]
}
resource "google_storage_bucket_iam_member" "runtime" {
  bucket = google_storage_bucket.demo.name
  role = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.runtime.email}"
}
output "workload_identity_provider" { value = google_iam_workload_identity_pool_provider.github.name }
output "service_account" { value = google_service_account.runtime.email }
output "bucket" { value = google_storage_bucket.demo.name }
