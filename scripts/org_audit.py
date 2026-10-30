#!/usr/bin/env python3
"""Audit workflow permissions and failure propagation across an org checkout.

The course caller/module contract is enforced by kit_drift.py; this command
runs that check too. YAML values are parsed so quoting cannot bypass a rule.
"""
from pathlib import Path
import re
import shlex
import subprocess
import sys
import yaml

GATE_CMD = re.compile(r'\b(?:verify_\w*|check_\w*|\w*audit\w*|pa11y|lychee|conformance_\w*|npm\s+(?:ci|test)|kit\s+check)\b')
MASK_FAILURE = re.compile(r'\|\|\s*(?:true\b|:\s*(?:$|;)|echo\b|exit\s+0\b)')
WRITERS = {'peter-evans/create-pull-request', 'stefanzweifel/git-auto-commit-action', 'endbug/add-and-commit', 'ad-m/github-push-action'}


def inspect_workflow(document):
    findings = []

    def walk(value, location='workflow'):
        if isinstance(value, dict):
            permission = value.get('permissions')
            if permission == 'write-all' or (isinstance(permission, dict) and permission.get('contents') not in (None, 'read', 'none')):
                findings.append((location, 'workflow grants contents write access', False))
            if 'continue-on-error' in value and str(value['continue-on-error']).lower() != 'false':
                findings.append((location, 'continue-on-error can suppress failure', True))
            action = str(value.get('uses', '')).split('@')[0].lower()
            if action in WRITERS:
                findings.append((location, f'automatic repository writer: {action}', False))
            script = value.get('run')
            if isinstance(script, str):
                for line in script.replace('\\\n', ' ').splitlines():
                    if line.lstrip().startswith('#'):
                        continue
                    try:
                        tokens = shlex.split(line, comments=True)
                    except ValueError:
                        tokens = line.split()
                    if 'git' in tokens and 'push' in tokens[tokens.index('git') + 1:]:
                        findings.append((location, 'workflow pushes Git changes', False))
                    if GATE_CMD.search(line) and MASK_FAILURE.search(line):
                        findings.append((location, 'required command failure is masked: ' + line.strip(), True))
                    if re.search(r'\bset\s+\+e\b', line) and GATE_CMD.search(script):
                        findings.append((location, 'failure propagation disabled around a required command', True))
            for key, child in value.items():
                walk(child, f'{location}.{key}')
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f'{location}[{index}]')
    walk(document)
    return findings


def main():
    org = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    here = Path(__file__).resolve().parent
    exceptions = yaml.safe_load((here / 'org-audit-exceptions.yml').read_text()) or {}
    archived = set(exceptions.get('archived', []))
    scheduled = {(x['repo'], x['file']): x for x in exceptions.get('scheduled', [])}
    repos = sorted(p.parent for p in org.glob('*/.git'))
    if not repos:
        print('::error::no repositories found; the audit examined nothing')
        return 1
    bad, scanned, used = 0, 0, set()
    active = [p for p in repos if p.name not in archived]
    for repo in active:
        workflow_dir = repo / '.github/workflows'
        for path in sorted(set(workflow_dir.glob('*.yml')) | set(workflow_dir.glob('*.yaml'))):
            scanned += 1
            relative = path.relative_to(repo).as_posix()
            key = (repo.name, relative)
            try:
                document = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
                if not isinstance(document, dict):
                    raise ValueError('workflow must be a mapping')
                findings = inspect_workflow(document)
            except (ValueError, yaml.YAMLError) as exc:
                findings = [('workflow', f'invalid YAML: {exc}', False)]
            for location, reason, suppression in findings:
                exception = scheduled.get(key) if suppression else None
                if exception and all(str(exception.get(k, '')).strip() for k in ['reason', 'destination']):
                    used.add(key)
                    print(f'::warning::{repo.name}/{relative}:{location}: {reason}; scheduled for {exception["destination"]}')
                else:
                    bad += 1
                    print(f'::error::{repo.name}/{relative}:{location}: {reason}')
    for key, entry in scheduled.items():
        if key not in used and (org / key[0]).exists() and key[0] not in archived:
            bad += 1
            print(f'::error::unused or invalid exception: {key[0]}/{key[1]}')
    print(f'Workflow audit: {len(active)} active repositories, {scanned} workflows, {bad} findings')
    drift = subprocess.run([sys.executable, str(here / 'kit_drift.py'), str(org)])
    return int(bool(bad or drift.returncode))


if __name__ == '__main__':
    raise SystemExit(main())
