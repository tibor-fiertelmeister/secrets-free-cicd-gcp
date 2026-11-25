import unittest
from pathlib import Path
from security_policy import terraform, workflow, check_terraform, check_workflow
ROOT = Path(__file__).resolve().parents[1]
class Structured(unittest.TestCase):
    def test_terraform(self):
        folder = ROOT / 'terraform'
        self.assertEqual({p.name for p in folder.glob('*.tf')}, {'main.tf'})
        self.assertFalse(list(folder.glob('*.tf.json')))
        check_terraform(terraform((folder/'main.tf').read_text(encoding='utf-8')))
    def test_workflows(self):
        folder = ROOT/'.github/workflows'
        self.assertEqual({p.name for p in folder.glob('*.y*ml')}, {'ci.yml','deploy.yml'})
        for name in ('ci.yml','deploy.yml'):
            check_workflow(workflow((folder/name).read_text(encoding='utf-8')), name=='deploy.yml')
