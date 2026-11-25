import unittest
from pathlib import Path
from security_policy import terraform, workflow, check_terraform, check_workflow, PolicyError
ROOT = Path(__file__).resolve().parents[1]
class Mutations(unittest.TestCase):
    def test_terraform_mutations(self):
        text = (ROOT/'terraform/main.tf').read_text(encoding='utf-8')
        changes = [('OR trust','" && "','" || "'), ('missing repository ID', 'assertion.repository_id ==', 'assertion.repository_id !='), ('commented branch', '    "assertion.ref ==', '    # "assertion.ref =='), ('public bucket','"enforced"','"inherited"'), ('broad role','roles/storage.objectCreator','roles/editor'), ('project scope','google_storage_bucket_iam_member','google_project_iam_member'), ('wrong issuer','https://token.actions.githubusercontent.com','https://example.com')]
        for name, old, new in changes:
            with self.subTest(name=name):
                self.assertIn(old,text)
                with self.assertRaises(PolicyError):
                    check_terraform(terraform(text.replace(old,new,1)))
        with self.assertRaises(PolicyError):
            check_terraform(terraform(text+'\nresource "google_service_account_key" "bad" { service_account_id = google_service_account.runtime.name }\n'))
    def test_workflow_mutations(self):
        for filename, deploy, old, new in [('ci.yml',False,'contents: read','contents: read\n  id-token: write'),('deploy.yml',True,'permissions: {}','permissions: write-all'),('deploy.yml',True,'workflow_dispatch','pull_request_target'),('deploy.yml',True,'persist-credentials: false','persist-credentials: true'),('deploy.yml',True,'id-token: write','id-token: read')]:
            with self.subTest(file=filename, change=new):
                text=(ROOT/'.github/workflows'/filename).read_text(encoding='utf-8')
                self.assertIn(old,text)
                with self.assertRaises(PolicyError):
                    check_workflow(workflow(text.replace(old,new,1)),deploy)
    def test_duplicate_yaml_key(self):
        with self.assertRaises(PolicyError):
            workflow('permissions: {}\npermissions: write-all\n')
