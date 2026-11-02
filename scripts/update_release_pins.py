#!/usr/bin/env python3
"""Prepare/apply one published foundation set across all shared consumers.

prepare resolves published immutable SemVer tags and verifies their actual
contracts. apply is a dry run unless --write is explicit. Neither command
creates tags, commits, pushes, merges or deploys anything.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import yaml
from jsonschema import Draft202012Validator
from release_pins import SEMVER, WORKFLOW, REPOSITORIES, declarations

def digest(data):return hashlib.sha256(data).hexdigest()

def atomic_write(path,content):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.release-pin-',dir=path.parent)
    temp=Path(name)
    try:
        with os.fdopen(fd,'wb') as stream:stream.write(content);stream.flush();os.fsync(stream.fileno())
        if path.exists():temp.chmod(path.stat().st_mode & 0o777)
        else:temp.chmod(0o644)
        temp.replace(path)
    finally:temp.unlink(missing_ok=True)

def command(args,cwd=None):
    result=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
    if result.returncode:raise ValueError('command failed: '+' '.join(args)+'\n'+result.stderr[-1200:])
    return result.stdout.strip()

def published_commit(repository,tag):
    if not tag.startswith('v') or not SEMVER.fullmatch(tag[1:]):raise ValueError('immutable exact SemVer tag required: '+tag)
    rows=command(['git','ls-remote','--tags','https://github.com/'+repository+'.git','refs/tags/'+tag,'refs/tags/'+tag+'^{}']).splitlines()
    refs={row.split()[1]:row.split()[0] for row in rows if row.strip()}
    # Annotated immutable release tags are the suite publication contract.
    commit=refs.get('refs/tags/'+tag+'^{}')
    if not commit:raise ValueError(repository+' '+tag+' is unpublished or not an annotated release tag')
    return commit

def checkout(repository,tag,root):
    root.mkdir();command(['git','init','-q',str(root)])
    command(['git','-C',str(root),'fetch','--quiet','--depth=1','https://github.com/'+repository+'.git','refs/tags/'+tag])
    command(['git','-C',str(root),'checkout','--quiet','--detach','FETCH_HEAD'])
    return root

def caller_for(template,org_commit):
    document=yaml.load(template,Loader=yaml.BaseLoader)
    job=document.get('jobs',{}).get('course',{})
    if job.get('uses')!=WORKFLOW+org_commit or job.get('with',{}).get('org_ref')!=org_commit:
        raise ValueError('published kit caller does not use the chosen immutable org commit; release org, align kit template, then release kit')
    return template

def align_caller(kit,tag,write=False):
    commit=published_commit(REPOSITORIES['org'],tag)
    with tempfile.TemporaryDirectory(prefix='boulingua-org-contract-') as td:
        tree=checkout(REPOSITORIES['org'],tag,Path(td)/'org')
        if not (tree/'scripts/release_pins.py').is_file():raise ValueError('published org has no explicit release pin contract')
    path=kit/'templates/deploy.yml';text=path.read_text()
    text,n=re.subn(r'(uses:\s*boulingua/\.github/\.github/workflows/course-build\.yml@)[^\s]+',lambda m:m[1]+commit,text)
    if n!=1:raise ValueError('expected one shared workflow in kit template')
    text,n=re.subn(r'(?m)^(\s*org_ref:\s*)[^\s]+$',lambda m:m[1]+commit,text)
    if n!=1:raise ValueError('expected one explicit org_ref in kit template')
    caller_for(text,commit)
    if write:path.write_text(text)
    print(('Aligned' if write else 'Would align')+' kit caller to '+commit+'; publish this kit revision before preparing consumer updates')

def prepare(tags,output):
    with tempfile.TemporaryDirectory(prefix='boulingua-release-') as td:
        root=Path(td);records={};trees={}
        for name,repository in REPOSITORIES.items():
            tag=tags[name];commit=published_commit(repository,tag)
            tree=checkout(repository,tag,root/name)
            if command(['git','-C',str(tree),'rev-parse','HEAD'])!=commit:raise ValueError('tag moved while preparing '+name)
            records[name]={'repository':repository,'tag':tag,'version':tag[1:],'commit':commit};trees[name]=tree
        if not (trees['org']/'scripts/release_pins.py').is_file():raise ValueError('published org revision lacks the explicit pin validator')
        if (trees['curriculum']/'VERSION').read_text().strip()!=records['curriculum']['version']:raise ValueError('published curriculum VERSION differs from its tag')
        schema_bytes=(trees['curriculum']/'schema/conformance.schema.json').read_bytes()
        schema=json.loads(schema_bytes);Draft202012Validator.check_schema(schema)
        kit_module=(trees['kit']/'go.mod').read_text()
        if not re.search(r'(?m)^module github.com/boulingua/kit\s*$',kit_module):raise ValueError('published kit module identity differs')
        go_version=re.search(r'(?m)^go ([0-9]+\.[0-9]+(?:\.[0-9]+)?)\s*$',kit_module)
        if not go_version:raise ValueError('published kit lacks an exact Go toolchain floor')
        template=caller_for((trees['kit']/'templates/deploy.yml').read_text(),records['org']['commit'])
        downloaded=json.loads(command(['go','mod','download','-json','github.com/boulingua/kit@'+tags['kit']],cwd=root))
        if downloaded.get('Version')!=tags['kit'] or not all(downloaded.get(k,'').startswith('h1:') for k in ['Sum','GoModSum']):raise ValueError('Go did not return verified module digests')
        if downloaded.get('Origin',{}).get('Hash')!=records['kit']['commit']:raise ValueError('Go module origin differs from the published kit commit')
        result={'schema_version':1,'state':'published',**records,
                'curriculum_schema_sha256':digest(schema_bytes),'curriculum_schema_text':schema_bytes.decode(),
                'caller':template,'caller_sha256':digest(template.encode()),'go_version':go_version[1],
                'kit_sum':downloaded['Sum'],'kit_go_mod_sum':downloaded['GoModSum']}
        for name,record in records.items():
            if published_commit(record['repository'],record['tag'])!=record['commit']:raise ValueError(name+' tag changed during preparation')
        output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
        print('Prepared published foundation manifest:',output)

def plan(root,release):
    if release.get('schema_version')!=1 or release.get('state')!='published':raise ValueError('a prepared published manifest is required')
    if digest(release['caller'].encode())!=release['caller_sha256']:raise ValueError('caller digest mismatch')
    if digest(release['curriculum_schema_text'].encode())!=release['curriculum_schema_sha256']:raise ValueError('conformance schema digest mismatch')
    schema=json.loads(release['curriculum_schema_text']);Draft202012Validator.check_schema(schema)
    caller_for(release['caller'],release['org']['commit'])
    changes={};consumers=[];modules=[]
    for repo in sorted(root.iterdir()):
        gomod=repo/'go.mod'
        if not gomod.is_file() or 'github.com/boulingua/kit ' not in gomod.read_text():continue
        modules.append(repo.name);text=gomod.read_text()
        text,n=re.subn(r'(github\.com/boulingua/kit\s+)v[^\s]+',lambda m:m[1]+'v'+release['kit']['version'],text)
        if n!=1:raise ValueError(repo.name+': expected exactly one kit requirement')
        text=re.sub(r'(?m)^go [^\s]+$', 'go '+release['go_version'],text)
        changes[gomod]=text.encode()
        gosum=repo/'go.sum';sums=gosum.read_text().splitlines() if gosum.exists() else []
        prefix='github.com/boulingua/kit v'+release['kit']['version']
        sums=[line for line in sums if not line.startswith(prefix+' ') and not line.startswith(prefix+'/go.mod ')]
        sums += [prefix+' '+release['kit_sum'],prefix+'/go.mod '+release['kit_go_mod_sum']]
        changes[gosum]=('\n'.join(sorted(set(sums)))+'\n').encode()
        caller=repo/'.github/workflows/deploy.yml'
        if not caller.is_file():continue # independently built product, not a shared caller
        consumers.append(repo.name);changes[caller]=release['caller'].encode()
        pins={key:release[key] for key in ['schema_version','state','org','kit','curriculum','curriculum_schema_sha256']}
        changes[repo/'release-pins.json']=(json.dumps(pins,indent=2)+'\n').encode()
        manifest=repo/'curriculum.yml'
        if manifest.exists():
            content,n=re.subn(r'(?m)^framework_version:\s*[^\n]+$', 'framework_version: '+release['curriculum']['version'],manifest.read_text())
            if n!=1:raise ValueError(repo.name+': missing or duplicate framework_version')
            data=yaml.safe_load(content);errors=list(Draft202012Validator(schema).iter_errors(data))
            if errors:raise ValueError(repo.name+': new schema rejects conformance manifest: '+errors[0].message)
            changes[manifest]=content.encode()
        elif (yaml.safe_load((repo/'boulingua.yml').read_text()) or {}).get('kind')=='course':raise ValueError(repo.name+': missing course conformance manifest')
    if not consumers:raise ValueError('no shared consumers found')
    changes[root/'kit/templates/deploy.yml']=release['caller'].encode()
    return changes,consumers,modules

def apply(root,path,write=False,receipt=None):
    root=root.resolve();path=path.resolve()
    if receipt:
        receipt=receipt.resolve()
        if receipt.is_relative_to(root) or receipt==path:raise ValueError('receipt and rollback backups must be outside the repos and separate from the manifest')
        if write and receipt.exists():raise ValueError('preserve the existing receipt; choose a new apply receipt')
    release=json.loads(path.read_text())
    # Reject unpublished/moved refs before even planning writes.
    for name in REPOSITORIES:
        record=release[name]
        if published_commit(record['repository'],record['tag'])!=record['commit']:raise ValueError(name+': published ref no longer matches prepared manifest')
    with tempfile.TemporaryDirectory(prefix='boulingua-release-recheck-') as td:
        fresh=Path(td)/'manifest.json'
        prepare({name:release[name]['tag'] for name in REPOSITORIES},fresh)
        if json.loads(fresh.read_text())!=release:raise ValueError('prepared manifest differs from actual published foundation content/digests')
    changes,consumers,modules=plan(root,release)
    before={p:p.read_bytes() if p.exists() else None for p in changes}
    record={'state':'planned','release_manifest_sha256':digest(path.read_bytes()),'consumers':consumers,'modules':modules,
            'changes':[{'path':str(p.relative_to(root)),'before_sha256':digest(before[p]) if before[p] is not None else None,'after_sha256':digest(content)} for p,content in changes.items()]}
    if write:
        if receipt is None:raise ValueError('--write requires --receipt outside the repos to preserve rollback inputs')
        backup=receipt.parent/(receipt.stem+'-before')
        if backup.exists():raise ValueError('rollback backup already exists; never overwrite prior release evidence')
        backup.mkdir(parents=True)
        for p,content in changes.items():
            if before[p] is not None:
                target=backup/p.relative_to(root);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(before[p])
        record['state']='applying locally';record['rollback_backup']=str(backup)
        atomic_write(receipt,(json.dumps(record,indent=2)+'\n').encode())
        for p,content in changes.items():
            current=p.read_bytes() if p.exists() else None
            if current!=before[p]:raise ValueError('source changed after planning: '+str(p))
            atomic_write(p,content)
        record['state']='applied locally; not committed or published';record['rollback_backup']=str(backup)
    if receipt:atomic_write(receipt,(json.dumps(record,indent=2)+'\n').encode())
    print(record['state']+': '+str(len(consumers))+' shared callers; '+str(len(modules))+' module consumers; '+str(len(changes))+' files')

def rollback(root,receipt,write=False):
    root=root.resolve();record=json.loads(receipt.read_text());backup=Path(record['rollback_backup']);restore=[]
    for entry in record['changes']:
        path=(root/entry['path']).resolve()
        if not path.is_relative_to(root):raise ValueError('rollback path escapes suite root')
        current=digest(path.read_bytes()) if path.is_file() else None
        if current==entry['before_sha256']:continue # already unchanged/restored, including incomplete apply
        if current!=entry['after_sha256']:
            raise ValueError('preserve later edits before rollback: '+entry['path'])
        before=entry['before_sha256'];content=(backup/entry['path']).read_bytes() if before else None
        if content is not None and digest(content)!=before:raise ValueError('rollback backup digest mismatch: '+entry['path'])
        restore.append((path,content))
    if write:
        for path,content in restore:
            if content is None:path.unlink()
            else:atomic_write(path,content)
    print(('Restored' if write else 'Would restore')+' '+str(len(restore))+' exact prior files; no Git history or deployment changed')

def candidate_snapshot(root,output):
    root=root.resolve();records={};consumers={}
    for name,directory in [('org','.github'),('kit','kit'),('curriculum','curriculum')]:
        repo=root/directory
        paths=command(['git','-C',str(repo),'ls-files','--cached','--others','--exclude-standard','-z']).split('\0')
        records[name]={'head':command(['git','-C',str(repo),'rev-parse','HEAD']),
                       'working_tree_status':command(['git','-C',str(repo),'status','--porcelain']),
                       'files':{rel:digest((repo/rel).read_bytes()) for rel in sorted(set(paths)) if rel and (repo/rel).is_file()}}
    for repo in sorted(root.iterdir()):
        if not (repo/'.github/workflows/deploy.yml').is_file():continue
        lock,_=declarations(repo)
        consumers[repo.name]={'declared_release':lock,'files':{rel:digest((repo/rel).read_bytes()) for rel in ['go.mod','go.sum','curriculum.yml','release-pins.json','.github/workflows/deploy.yml'] if (repo/rel).is_file()}}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps({'schema_version':1,'state':'local candidate only; no immutable release or hosted acceptance',
                                  'foundations':records,'consumers':consumers,
                                  'next_action':'Complete candidate checks, select versions, publish approved foundations in documented order, then prepare/apply the exact published set.'},indent=2)+'\n')
    print('Recorded three actual working trees and',len(consumers),'consumer declarations:',output)

def candidate_inputs(root,code,output,include_drafts=False):
    root=root.resolve()
    if not re.fullmatch('[a-z][a-z0-9-]*',code) or not (root/code/'.github/workflows/deploy.yml').is_file():
        raise ValueError('select an actual shared course or hub')
    result={'schema_version':1,'mode':'candidate','deploy':False,'include_drafts':include_drafts,'course':code}
    with tempfile.TemporaryDirectory(prefix='boulingua-candidate-refs-') as td:
        for name,directory in [('course',code),('kit','kit'),('curriculum','curriculum')]:
            repo=root/directory
            if command(['git','-C',str(repo),'status','--porcelain','--untracked-files=all']):
                raise ValueError(directory+': commit reviewed candidate files before preparing immutable hosted inputs')
            commit=command(['git','-C',str(repo),'rev-parse','HEAD'])
            check=Path(td)/name;check.mkdir();command(['git','init','-q',str(check)])
            command(['git','-C',str(check),'fetch','--quiet','--depth=1','https://github.com/boulingua/'+directory+'.git',commit])
            if command(['git','-C',str(check),'rev-parse','FETCH_HEAD^{commit}'])!=commit:raise ValueError(directory+': remote candidate commit differs')
            result[name+'_commit']=commit
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2)+'\n')
    print('Prepared exact remotely available candidate inputs; org identity will be the executing workflow commit:',output)

def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='action',required=True)
    p=sub.add_parser('prepare');p.add_argument('--org-ref',required=True);p.add_argument('--kit-ref',required=True);p.add_argument('--curriculum-ref',required=True);p.add_argument('--output',type=Path,required=True)
    t=sub.add_parser('align-caller');t.add_argument('kit',type=Path);t.add_argument('--org-ref',required=True);t.add_argument('--write',action='store_true')
    a=sub.add_parser('apply');a.add_argument('root',type=Path);a.add_argument('manifest',type=Path);a.add_argument('--write',action='store_true');a.add_argument('--receipt',type=Path)
    r=sub.add_parser('rollback');r.add_argument('root',type=Path);r.add_argument('receipt',type=Path);r.add_argument('--write',action='store_true')
    s=sub.add_parser('snapshot');s.add_argument('root',type=Path);s.add_argument('--output',type=Path,required=True)
    c=sub.add_parser('candidate-inputs');c.add_argument('root',type=Path);c.add_argument('--course',required=True);c.add_argument('--output',type=Path,required=True);c.add_argument('--drafts',action='store_true',help='include unpublished teaching drafts in the review-only build')
    args=ap.parse_args()
    try:
        if args.action=='candidate-inputs':candidate_inputs(args.root,args.course,args.output,args.drafts)
        elif args.action=='snapshot':candidate_snapshot(args.root,args.output)
        elif args.action=='align-caller':align_caller(args.kit,args.org_ref,args.write)
        elif args.action=='prepare':prepare({name:getattr(args,name+'_ref') for name in REPOSITORIES},args.output)
        elif args.action=='apply':apply(args.root,args.manifest,args.write,args.receipt)
        else:rollback(args.root,args.receipt,args.write)
        return 0
    except (ValueError,OSError,KeyError,TypeError,yaml.YAMLError) as exc:print('::error::'+str(exc));return 1

if __name__=='__main__':raise SystemExit(main())
