import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class Baseline(unittest.TestCase):
    def test_trust_configuration(self):
        text = (ROOT/'terraform/main.tf').read_text()
        for claim in ('repository_owner_id', 'repository_id', 'refs/heads/main', 'workflow_dispatch', 'workflow_ref'):
            self.assertIn(claim, text)
        self.assertNotIn('roles/editor', text)
        self.assertNotIn('roles/owner', text)
        self.assertIn('roles/storage.objectCreator', text)
        self.assertNotIn('google_service_account_key', text)
    def test_workflow(self):
        text = (ROOT/'.github/workflows/deploy.yml').read_text()
        self.assertIn('id-token: write', text)
        self.assertNotIn('credentials_json', text)
        self.assertNotIn('pull_request_target', text)
        self.assertNotIn('id-token: write', (ROOT/'.github/workflows/ci.yml').read_text())
    def test_ignore(self):
        text = (ROOT/'.gitignore').read_text()
        for pattern in ('*.tfstate', '*.tfvars', 'gha-creds-*.json'):
            self.assertIn(pattern, text)
if __name__ == '__main__': unittest.main()
