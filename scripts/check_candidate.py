#!/usr/bin/env python3
"""Check immutable candidate source inputs without granting release status."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys
import yaml
from jsonschema import Draft202012Validator
from release_pins import git, SHA, SEMVER

def validate(root,manifest):
    data=json.loads(manifest.read_text())
    if data.get('schema_version')!=1 or data.get('mode')!='candidate' or data.get('deploy') is not False:
        raise ValueError('candidate manifest must explicitly disable deployment')
    include_drafts=data.get('include_drafts',False)
    if not isinstance(include_drafts,bool):raise ValueError('include_drafts must be a boolean')
    code=data.get('course')
    registry=yaml.safe_load((root/'org/suite.yml').read_text())['repositories']
    if code not in registry or registry[code].get('archived') or registry[code].get('kind') not in {'course','hub','catalogue'}:
        raise ValueError('unsupported shared course/hub candidate')
    actual={}
    for name in ['course','kit','curriculum','org']:
        expected=data.get(name+'_commit','')
        if not SHA.fullmatch(expected):raise ValueError(name+': immutable40-character commit required')
        repo=root/name
        if git(repo,'rev-parse','HEAD')!=expected:raise ValueError(name+': checked-out commit differs from candidate manifest')
        if git(repo,'status','--porcelain','--untracked-files=all'):raise ValueError(name+': source checkout is not clean')
        actual[name]=expected
    repo=root/'course';config=yaml.safe_load((repo/'boulingua.yml').read_text())
    expected_code=registry[code].get('site_code',code)
    if config.get('code')!=expected_code or config.get('kind')!=registry[code]['kind']:
        raise ValueError('actual course identity differs from candidate selection')
    version=(root/'curriculum/VERSION').read_text().strip()
    if not SEMVER.fullmatch(version):raise ValueError('candidate framework VERSION is invalid')
    schema_path=root/'curriculum/schema/conformance.schema.json';schema=json.loads(schema_path.read_text());Draft202012Validator.check_schema(schema)
    manifest_path=repo/'curriculum.yml'
    if config['kind']=='course':
        metadata=yaml.safe_load(manifest_path.read_text())
        if metadata.get('framework_version')!=version:raise ValueError('course declaration differs from actual candidate framework VERSION')
        errors=list(Draft202012Validator(schema).iter_errors(metadata))
        if errors:raise ValueError('candidate schema rejects course: '+errors[0].message)
    return {'schema_version':1,'mode':'candidate','deploy':False,'include_drafts':include_drafts,'course':code,'actual_commits':actual,
            'framework_version':version,'schema_sha256':hashlib.sha256(schema_path.read_bytes()).hexdigest(),
            'source_manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),
            'scope':'Exact candidate source inputs only; full build/gates must still pass. No published release or deployment approval.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('root',type=Path);ap.add_argument('manifest',type=Path);ap.add_argument('--receipt',type=Path,required=True);a=ap.parse_args()
    try:
        result=validate(a.root.resolve(),a.manifest);a.receipt.write_text(json.dumps(result,indent=2)+'\n');print(result['scope']);return 0
    except (OSError,ValueError,KeyError,TypeError,yaml.YAMLError) as exc:print('::error::'+str(exc));return 1

if __name__=='__main__':raise SystemExit(main())
