#!/usr/bin/env python3
"""Validate explicit suite dependency pins against declarations and real checkouts."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
import yaml
from jsonschema import Draft202012Validator

SEMVER = re.compile(r'(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z')
SHA = re.compile(r'[a-f0-9]{40}\Z')
REPOSITORIES = {'org':'boulingua/.github','kit':'boulingua/kit','curriculum':'boulingua/curriculum'}
WORKFLOW = 'boulingua/.github/.github/workflows/course-build.yml@'

def kit_module_path(version):
    if not SEMVER.fullmatch(version): raise ValueError('exact kit SemVer required')
    major = int(version.split('.')[0])
    return 'github.com/boulingua/kit' + (f'/v{major}' if major >= 2 else '')


def load_pins(path):
    data=json.loads(path.read_text())
    if data.get('schema_version')!=1 or data.get('state') not in {'historical','published'}:
        raise ValueError('release-pins.json needs schema_version1 and an explicit historical/published state')
    for key,repo in REPOSITORIES.items():
        record=data.get(key,{})
        if record.get('repository')!=repo or not SHA.fullmatch(str(record.get('commit',''))):
            raise ValueError(key+': expected repository and immutable40-character commit')
        if key!='org' and not SEMVER.fullmatch(str(record.get('version',''))):
            raise ValueError(key+': exact numeric SemVer required')
    digest=data.get('curriculum_schema_sha256','')
    if not (data['state']=='historical' and digest is None) and not re.fullmatch('[a-f0-9]{64}',str(digest)):
        raise ValueError('exact curriculum conformance schema digest required for a published release')
    return data

def declarations(repo, expected_org=None):
    pins=load_pins(repo/'release-pins.json')
    matches=re.findall(r'(?m)^\s*(?:require\s+)?(github\.com/boulingua/kit(?:/v[0-9]+)?)\s+([^\s]+)',(repo/'go.mod').read_text())
    if matches!=[(kit_module_path(pins['kit']['version']),'v'+pins['kit']['version'])]:raise ValueError('go.mod must pin exactly the declared kit version and major module path')
    caller=yaml.load((repo/'.github/workflows/deploy.yml').read_text(),Loader=yaml.BaseLoader)
    job=caller.get('jobs',{}).get('course',{})
    org=pins['org']['commit']
    if job.get('uses')!=WORKFLOW+org or job.get('with',{}).get('org_ref')!=org:
        raise ValueError('workflow uses, explicit org_ref and release lock must identify the same immutable commit')
    if expected_org is not None and expected_org!=org:raise ValueError('workflow input org_ref differs from its caller and release lock')
    kind=(yaml.safe_load((repo/'boulingua.yml').read_text()) or {}).get('kind')
    if kind not in {'course','hub','catalogue'}:raise ValueError('explicit supported consumer kind required')
    course=kind=='course'
    manifest=repo/'curriculum.yml'
    if course and not manifest.is_file():raise ValueError('course curriculum.yml is required; no default framework version')
    if manifest.exists():
        metadata=yaml.safe_load(manifest.read_text())
        version=metadata.get('framework_version')
        if not isinstance(version,str) or not SEMVER.fullmatch(version) or version!=pins['curriculum']['version']:
            raise ValueError('curriculum.yml must declare the exact pinned framework version')
    return pins,course

def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args],text=True,stderr=subprocess.PIPE).strip()

def check(repo, kit, curriculum, org, expected_org=None, require_published=True):
    pins,course=declarations(repo,expected_org)
    if require_published and pins['state']!='published':raise ValueError('historical pins are not a release of the remediated suite')
    for key,path in [('kit',kit),('curriculum',curriculum),('org',org)]:
        if git(path,'status','--porcelain','--untracked-files=all'):
            raise ValueError(key+': tracked changes or untracked source files differ from the pinned release bytes')
        if git(path,'rev-parse','HEAD')!=pins[key]['commit']:raise ValueError(key+': actual checkout differs from release lock')
        if key!='org':
            tag='v'+pins[key]['version']
            if git(path,'rev-parse',tag+'^{commit}')!=pins[key]['commit']:raise ValueError(key+': version tag differs from actual checkout')
    if (curriculum/'VERSION').read_text().strip()!=pins['curriculum']['version']:
        raise ValueError('curriculum VERSION differs from the declared version/tag')
    schema_path=curriculum/'schema/conformance.schema.json'
    if hashlib.sha256(schema_path.read_bytes()).hexdigest()!=pins['curriculum_schema_sha256']:
        raise ValueError('curriculum schema bytes differ from the release lock')
    schema=json.loads(schema_path.read_text());Draft202012Validator.check_schema(schema)
    if course:
        errors=list(Draft202012Validator(schema).iter_errors(yaml.safe_load((repo/'curriculum.yml').read_text())))
        if errors:raise ValueError('course conformance schema: '+'; '.join(e.message for e in errors[:5]))
    return pins

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('repo',type=Path);ap.add_argument('--org-ref');ap.add_argument('--resolve-only',action='store_true');ap.add_argument('--kit',type=Path);ap.add_argument('--curriculum',type=Path);ap.add_argument('--org',type=Path);ap.add_argument('--github-output',type=Path);args=ap.parse_args()
    try:
        pins,_=declarations(args.repo,args.org_ref)
        if not args.resolve_only:
            if any(p is None for p in [args.kit,args.curriculum,args.org]):raise ValueError('all three actual checkouts are required')
            check(args.repo,args.kit,args.curriculum,args.org,args.org_ref)
        if args.github_output:
            with args.github_output.open('a') as out:
                for name in REPOSITORIES:out.write(name+'='+pins[name]['commit']+'\n')
        print('Explicit release declarations verified'+(' (checkout validation follows)' if args.resolve_only else ' against actual checkouts/schema'))
        return 0
    except (OSError,ValueError,KeyError,TypeError,AttributeError,yaml.YAMLError,subprocess.CalledProcessError) as exc:
        print('::error::'+str(exc));return 1

if __name__=='__main__':raise SystemExit(main())
