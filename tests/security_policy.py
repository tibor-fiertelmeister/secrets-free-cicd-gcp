"""Narrow, fail-closed policy for this reference implementation."""
import re
import hcl2
import yaml

class PolicyError(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise PolicyError(message)

class WorkflowLoader(yaml.BaseLoader):
    pass

def mapping(loader, node):
    result = {}
    for k, v in node.value:
        key = loader.construct_object(k)
        require(isinstance(key, str) and key not in result, 'Duplicate or invalid YAML key')
        result[key] = loader.construct_object(v)
    return result

WorkflowLoader.add_constructor('tag:yaml.org,2002:map', mapping)

def workflow(text):
    return yaml.load(text, Loader=WorkflowLoader)

def terraform(text):
    return hcl2.loads(text)

def resource_map(doc):
    result = {}
    for block in doc.get('resource', []):
        for kind, names in block.items():
            for name, body in names.items():
                key = (kind.strip('"'), name.strip('"'))
                require(key not in result, 'Duplicate resource')
                result[key] = body
    return result

EXPECTED = {
 ('google_project_service','apis'), ('google_iam_workload_identity_pool','github'),
 ('google_iam_workload_identity_pool_provider','github'), ('google_service_account','runtime'),
 ('google_service_account_iam_member','federation'), ('google_storage_bucket','demo'),
 ('google_storage_bucket_iam_member','runtime')}
CLAIMS = ["assertion.repository_owner_id == '${var.repository_owner_id}'", "assertion.repository_id == '${var.repository_id}'", "assertion.ref == 'refs/heads/main'", "assertion.event_name == 'workflow_dispatch'", "assertion.workflow_ref == '${var.repository}/.github/workflows/deploy.yml@refs/heads/main'"]
CONDITION = '${join(" && ", [' + ', '.join('"'+c+'"' for c in CLAIMS) + '])}'

def check_terraform(doc):
    require(not any(k in doc for k in ('module','data','import','moved')), 'Unexpected Terraform block')
    r = resource_map(doc)
    require(set(r) == EXPECTED, 'Unexpected or missing resource (including IAM/key resources)')
    p = r['google_iam_workload_identity_pool_provider','github']
    require(p.get('attribute_condition') == CONDITION, 'Trust condition changed')
    require(p.get('attribute_mapping') == {'"google.subject"':'"assertion.sub"','"attribute.repository_id"':'"assertion.repository_id"'}, 'Attribute mapping changed')
    require(p.get('oidc') == [{'__is_block__':True,'issuer_uri':'"https://token.actions.githubusercontent.com"'}], 'OIDC issuer or audience configuration changed')
    require(p.get('workload_identity_pool_id') == '${google_iam_workload_identity_pool.github.workload_identity_pool_id}', 'Wrong identity pool')
    f = r['google_service_account_iam_member','federation']
    require(f.get('role') == '"roles/iam.workloadIdentityUser"' and f.get('service_account_id') == '${google_service_account.runtime.name}' and f.get('member') == '"principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository_id/${var.repository_id}"', 'Federation binding changed')
    b = r['google_storage_bucket','demo']
    require(b.get('public_access_prevention') == '"enforced"' and b.get('uniform_bucket_level_access') is True and b.get('force_destroy') is False, 'Bucket protection weakened')
    i = r['google_storage_bucket_iam_member','runtime']
    require(i.get('role') == '"roles/storage.objectCreator"' and i.get('bucket') == '${google_storage_bucket.demo.name}' and i.get('member') == '"serviceAccount:${google_service_account.runtime.email}"', 'Runtime IAM binding changed')

def check_workflow(doc, deploy=False):
    require(isinstance(doc, dict), 'Invalid workflow')
    require(doc.get('on') == ('workflow_dispatch' if deploy else ['push','pull_request']), 'Unexpected workflow trigger')
    require(doc.get('permissions') == ({} if deploy else {'contents':'read'}), 'Unexpected workflow permissions')
    name = 'deploy' if deploy else 'validate'
    require(set(doc.get('jobs',{})) == {name}, 'Unexpected jobs')
    job = doc['jobs'][name]
    require(job.get('permissions', doc['permissions']) == ({'contents':'read','id-token':'write'} if deploy else {'contents':'read'}), 'Unexpected job permissions')
    if deploy:
        require(job.get('if') == "github.ref == 'refs/heads/main'", 'Deployment branch guard changed')
    require('uses' not in job, 'Reusable job not allowed')
    actions = {}
    for step in job.get('steps',[]):
        if 'uses' in step:
            use = step['uses']
            require(re.fullmatch(r'[\w.-]+/[\w./-]+@[0-9a-f]{40}', use), 'Unpinned action')
            action = use.split('@')[0]
            require(action not in actions, 'Duplicate action')
            actions[action] = step.get('with',{})
    expected = {'actions/checkout','google-github-actions/auth','google-github-actions/setup-gcloud'} if deploy else {'actions/checkout','hashicorp/setup-terraform'}
    require(set(actions) == expected, 'Unexpected or missing action')
    require(actions['actions/checkout'].get('persist-credentials') == 'false', 'Checkout credentials retained')
    if deploy:
        require(actions['google-github-actions/auth'] == {'workload_identity_provider':'${{ vars.WIF_PROVIDER }}','service_account':'${{ vars.GCP_SERVICE_ACCOUNT }}'}, 'Authentication inputs changed')
        require(re.fullmatch(r'\d+\.\d+\.\d+', actions['google-github-actions/setup-gcloud'].get('version','')), 'Unpinned gcloud')
    else:
        require(re.fullmatch(r'\d+\.\d+\.\d+', actions['hashicorp/setup-terraform'].get('terraform_version','')), 'Unpinned Terraform')
        runs = [s.get('run','') for s in job.get('steps',[])]
        require('terraform -chdir=terraform init -backend=false -lockfile=readonly' in runs, 'Readonly init missing')
        require(set(job) == {'runs-on','steps'}, 'Unexpected CI job configuration')
        require(job.get('runs-on') == 'ubuntu-24.04', 'CI runner changed')
        require(set(doc) == {'name','on','permissions','jobs'}, 'Unexpected CI workflow configuration')
        require(job.get('steps', [])[4:] == EXPECTED_GATE_STEPS, 'Required security gate steps changed')
        require(len(job.get('steps', [])) == 9, 'Unexpected CI step count')
        for step in job['steps'][:4]:
            require(set(step) <= {'uses','with','run'}, 'Unexpected CI setup step configuration')


EXPECTED_GATE_STEPS = [{'name': 'Install hash-locked scanner', 'run': 'python3.12 -m venv .venv-audit\n.venv-audit/bin/python -m pip install --require-hashes --only-binary=:all: -r requirements-audit.txt\n.venv-audit/bin/python -m pip check\n'}, {'name': 'Audit scanner dependencies', 'run': '.venv-audit/bin/python -m pip_audit -r requirements-audit.txt --require-hashes --strict'}, {'name': 'Audit project dependencies', 'run': '.venv-audit/bin/python -m pip_audit -r requirements-dev.txt --require-hashes --strict'}, {'name': 'Install hash-locked test dependencies', 'run': 'python3.12 -m venv .venv\n.venv/bin/python -m pip install --require-hashes --only-binary=:all: -r requirements-dev.txt\n.venv/bin/python -m pip check\n'}, {'run': '.venv/bin/python -m unittest discover -s tests -v'}]
