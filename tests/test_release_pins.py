from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
import yaml
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import release_pins as pins
import update_release_pins as update


class ReleasePins(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve();self.repo=self.root/'efl';self.repo.mkdir()
        self.kit=self.root/'kit';self.curriculum=self.root/'curriculum';self.org=self.root/'.github'
        for p in [self.kit,self.curriculum,self.org]:p.mkdir()
        (self.curriculum/'schema').mkdir();(self.curriculum/'VERSION').write_text('1.3.0\n')
        schema={'type':'object','required':['framework_version','language'],'properties':{'framework_version':{'const':'1.3.0'},'language':{'type':'string'}}}
        raw=json.dumps(schema);(self.curriculum/'schema/conformance.schema.json').write_text(raw)
        self.data={'schema_version':1,'state':'published','curriculum_schema_sha256':hashlib.sha256(raw.encode()).hexdigest()}
        for key,repo in pins.REPOSITORIES.items():self.data[key]={'repository':repo,'commit':{'org':'a','kit':'b','curriculum':'c'}[key]*40,'tag':'v1.3.0','version':'1.3.0'}
        (self.repo/'release-pins.json').write_text(json.dumps(self.data))
        (self.repo/'go.mod').write_text('module github.com/boulingua/efl\ngo 1.26.1\nrequire github.com/boulingua/kit v1.3.0\n')
        (self.repo/'boulingua.yml').write_text('kind: course\n')
        (self.repo/'curriculum.yml').write_text('framework_version: 1.3.0\nlanguage: en\n')
        path=self.repo/'.github/workflows/deploy.yml';path.parent.mkdir(parents=True)
        self.caller='jobs:\n  course:\n    uses: '+pins.WORKFLOW+'a'*40+'\n    with:\n      org_ref: '+'a'*40+'\n'
        path.write_text(self.caller)

    def git(self,path,*args):
        if args[0]=='status':return ''
        return self.data[{'kit':'kit','curriculum':'curriculum','.github':'org'}[path.name]]['commit']

    def test_real_checkout_identity_version_and_schema_are_required(self):
        with patch.object(pins,'git',side_effect=self.git):
            pins.check(self.repo,self.kit,self.curriculum,self.org)
            (self.curriculum/'VERSION').write_text('1.2.0')
            with self.assertRaisesRegex(ValueError,'VERSION'):pins.check(self.repo,self.kit,self.curriculum,self.org)
            (self.curriculum/'VERSION').write_text('1.3.0')
            (self.curriculum/'schema/conformance.schema.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'schema bytes'):pins.check(self.repo,self.kit,self.curriculum,self.org)
        with patch.object(pins,'git',side_effect=lambda p,*args:'' if args[0]=='status' else 'd'*40):
            with self.assertRaisesRegex(ValueError,'actual checkout'):pins.check(self.repo,self.kit,self.curriculum,self.org)
        with patch.object(pins,'git',return_value=' M audio/build_audio.py'):
            with self.assertRaisesRegex(ValueError,'tracked changes'):pins.check(self.repo,self.kit,self.curriculum,self.org)

    def test_missing_or_malformed_course_version_has_no_default(self):
        path=self.repo/'curriculum.yml'
        for text in ['framework_version: 1.3.0garbage\nlanguage: en\n','language: en\n']:
            path.write_text(text)
            with self.assertRaisesRegex(ValueError,'exact pinned'):pins.declarations(self.repo)
        path.unlink()
        with self.assertRaisesRegex(ValueError,'no default'):pins.declarations(self.repo)

    def test_hub_has_explicit_dependency_without_fake_conformance(self):
        (self.repo/'boulingua.yml').write_text('kind: hub\n');(self.repo/'curriculum.yml').unlink()
        self.assertFalse(pins.declarations(self.repo)[1])
        (self.repo/'release-pins.json').unlink()
        with self.assertRaises(FileNotFoundError):pins.declarations(self.repo)

    def test_org_pin_cannot_differ_between_workflow_input_caller_and_lock(self):
        with self.assertRaisesRegex(ValueError,'workflow input'):pins.declarations(self.repo,'d'*40)
        p=self.repo/'.github/workflows/deploy.yml';p.write_text(self.caller.replace('org_ref: '+'a'*40,'org_ref: '+'d'*40))
        with self.assertRaisesRegex(ValueError,'same immutable'):pins.declarations(self.repo)

    def test_historical_pins_cannot_be_reported_as_candidate_release(self):
        self.data.update(state='historical',curriculum_schema_sha256=None)
        (self.repo/'release-pins.json').write_text(json.dumps(self.data));pins.declarations(self.repo)
        with self.assertRaisesRegex(ValueError,'historical'):pins.check(self.repo,self.kit,self.curriculum,self.org)

    def test_new_schema_rejects_incompatible_manifest_even_with_matching_version(self):
        (self.repo/'curriculum.yml').write_text('framework_version: 1.3.0\n')
        with patch.object(pins,'git',side_effect=self.git):
            with self.assertRaisesRegex(ValueError,'language'):pins.check(self.repo,self.kit,self.curriculum,self.org)

    def test_unpublished_or_moving_refs_reject_before_update(self):
        with self.assertRaisesRegex(ValueError,'exact SemVer'):update.published_commit('boulingua/kit','v1')
        with patch.object(update,'command',return_value=''):
            with self.assertRaisesRegex(ValueError,'unpublished'):update.published_commit('boulingua/kit','v9.99.99')

    def test_update_plan_keeps_unrelated_versions_and_changes_all_dependency_surfaces(self):
        (self.repo/'go.sum').write_text('example.org/dependency v1.0.0 h1:keep\n')
        release={**self.data,'caller':self.caller,'caller_sha256':update.digest(self.caller.encode()),
                 'curriculum_schema_text':(self.curriculum/'schema/conformance.schema.json').read_text(),
                 'go_version':'1.26.1','kit_sum':'h1:module','kit_go_mod_sum':'h1:gomod'}
        changes,consumers,modules=update.plan(self.root,release)
        self.assertEqual(consumers,['efl']);self.assertEqual(modules,['efl'])
        self.assertIn(b'example.org/dependency v1.0.0 h1:keep',changes[self.repo/'go.sum'])
        for name in ['go.mod','go.sum','release-pins.json','curriculum.yml','.github/workflows/deploy.yml']:self.assertIn(self.repo/name,changes)
        self.assertIn(self.kit/'templates/deploy.yml',changes)
        self.assertEqual((self.repo/'go.sum').read_text(),'example.org/dependency v1.0.0 h1:keep\n')
        release['caller']+='\n'
        with self.assertRaisesRegex(ValueError,'caller digest'):update.plan(self.root,release)

    def test_rollback_preserves_later_edits_before_restoring_anything(self):
        target=self.repo/'go.mod';before=b'previous release\n';after=b'applied release\n'
        target.write_bytes(after);backup=self.root/'backup';(backup/'efl').mkdir(parents=True);(backup/'efl/go.mod').write_bytes(before)
        record={'rollback_backup':str(backup),'changes':[{'path':'efl/go.mod','before_sha256':update.digest(before),'after_sha256':update.digest(after)}]}
        receipt=self.root/'receipt.json';receipt.write_text(json.dumps(record))
        target.write_text('later author edit\n')
        with self.assertRaisesRegex(ValueError,'later edits'):update.rollback(self.root,receipt,True)
        self.assertEqual(target.read_text(),'later author edit\n')
        target.write_bytes(after);update.rollback(self.root,receipt,True)
        self.assertEqual(target.read_bytes(),before)

    def test_receipt_cannot_overwrite_dependency_or_input_manifest(self):
        target=self.repo/'go.mod';before=target.read_bytes()
        with self.assertRaisesRegex(ValueError,'outside'):
            update.apply(self.root,self.root/'does-not-exist.json',True,target)
        self.assertEqual(target.read_bytes(),before)

    def test_interrupted_update_can_restore_changed_and_untouched_files(self):
        release={**self.data,'caller':self.caller,'caller_sha256':update.digest(self.caller.encode()),
                 'curriculum_schema_text':(self.curriculum/'schema/conformance.schema.json').read_text(),
                 'go_version':'1.27.1','kit_sum':'h1:module','kit_go_mod_sum':'h1:gomod'}
        before=(self.repo/'go.mod').read_bytes();real_write=update.atomic_write
        def interrupted(path,content):
            if path==self.repo/'go.sum':raise OSError('simulated storage interruption')
            return real_write(path,content)
        with tempfile.TemporaryDirectory() as outside:
            manifest=Path(outside)/'published.json';manifest.write_text(json.dumps(release));receipt=Path(outside)/'apply.json'
            with patch.object(update,'published_commit',side_effect=lambda repo,tag:next(v['commit'] for k,v in self.data.items() if isinstance(v,dict) and v.get('repository')==repo)), patch.object(update,'prepare',side_effect=lambda tags,out:out.write_text(json.dumps(release))), patch.object(update,'atomic_write',side_effect=interrupted):
                with self.assertRaisesRegex(OSError,'interruption'):update.apply(self.root,manifest,True,receipt)
            self.assertNotEqual((self.repo/'go.mod').read_bytes(),before)
            self.assertEqual(json.loads(receipt.read_text())['state'],'applying locally')
            update.rollback(self.root,receipt,True)
            self.assertEqual((self.repo/'go.mod').read_bytes(),before)
            self.assertFalse((self.repo/'go.sum').exists())


if __name__=='__main__':unittest.main()
