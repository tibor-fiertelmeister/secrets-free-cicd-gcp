import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Baseline(unittest.TestCase):
    def test_trust_configuration(self):
        text = (ROOT / 'terraform/main.tf').read_text()
        for claim in ('repository_owner_id', 'repository_id', 'refs/heads/main', 'workflow_dispatch', 'workflow_ref'):
            self.assertTrue(claim in text, f'Missing trust marker: {claim}')
        for forbidden in ('roles/editor', 'roles/owner', 'google_service_account_key'):
            self.assertFalse(forbidden in text, f'Forbidden marker: {forbidden}')
        self.assertTrue('roles/storage.objectCreator' in text, 'Missing Object Creator marker')

    def test_workflow(self):
        text = (ROOT / '.github/workflows/deploy.yml').read_text()
        self.assertTrue('id-token: write' in text, 'Missing deployment OIDC permission')
        for forbidden in ('credentials_json', 'pull_request_target'):
            self.assertFalse(forbidden in text, f'Forbidden workflow marker: {forbidden}')
        self.assertFalse('id-token: write' in (ROOT / '.github/workflows/ci.yml').read_text(), 'Offline CI must not request OIDC')

    def test_ignore(self):
        text = (ROOT / '.gitignore').read_text()
        for pattern in ('*.tfstate', '*.tfvars', 'gha-creds-*.json'):
            self.assertTrue(pattern in text, f'Missing ignore pattern: {pattern}')

    def test_action_pinning(self):
        for path in sorted((ROOT / '.github/workflows').glob('*.yml')):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                match = re.match(r'^\s*(?:-\s*)?uses:\s*(.*)$', line)
                if match:
                    self.assertTrue(re.fullmatch(r'[\w.-]+/[\w./-]+@[0-9a-f]{40}', match.group(1).split('#', 1)[0].strip()) is not None, f'Unpinned action: {path.name}:{number}')


if __name__ == '__main__':
    unittest.main()
