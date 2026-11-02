from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
import yaml
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import check_candidate as candidate


class CandidateValidation(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        for name in ['org','course','kit','curriculum']:(self.root/name).mkdir()
        (self.root/'org/suite.yml').write_text('repositories:\n  efl: {kind: course, archived: false}\n')
        (self.root/'course/boulingua.yml').write_text('code: efl\nkind: course\n')
        (self.root/'course/curriculum.yml').write_text('framework_version: 1.3.0\nlanguage: en\n')
        (self.root/'curriculum/VERSION').write_text('1.3.0\n');(self.root/'curriculum/schema').mkdir()
        (self.root/'curriculum/schema/conformance.schema.json').write_text(json.dumps({'type':'object','required':['language']}))
        self.data={'schema_version':1,'mode':'candidate','deploy':False,'course':'efl',**{n+'_commit':str(i)*40 for i,n in enumerate(['course','kit','curriculum','org'],1)}}
        self.manifest=self.root/'inputs.json';self.save()
    def save(self):self.manifest.write_text(json.dumps(self.data))
    def git(self,path,*args):return '' if args[0]=='status' else self.data[path.name+'_commit']

    def test_exact_candidate_pass_is_not_a_published_release(self):
        with patch.object(candidate,'git',side_effect=self.git):receipt=candidate.validate(self.root,self.manifest)
        self.assertEqual(receipt['mode'],'candidate');self.assertFalse(receipt['deploy']);self.assertIn('No published release',receipt['scope'])
    def test_candidate_cannot_request_deployment_or_floating_refs(self):
        self.data['deploy']=True;self.save()
        with self.assertRaisesRegex(ValueError,'disable deployment'):candidate.validate(self.root,self.manifest)
        self.data['deploy']=False;self.data['kit_commit']='main';self.save()
        with patch.object(candidate,'git',side_effect=self.git):
            with self.assertRaisesRegex(ValueError,'immutable'):candidate.validate(self.root,self.manifest)
    def test_registered_hub_alias_does_not_require_course_conformance(self):
        (self.root/'org/suite.yml').write_text('repositories:\n  website: {kind: hub, site_code: hub, archived: false}\n')
        (self.root/'course/boulingua.yml').write_text('code: hub\nkind: hub\n')
        (self.root/'course/curriculum.yml').unlink()
        self.data['course']='website';self.save()
        with patch.object(candidate,'git',side_effect=self.git):
            self.assertEqual(candidate.validate(self.root,self.manifest)['course'],'website')
        (self.root/'course/boulingua.yml').write_text('code: another-hub\nkind: hub\n')
        with patch.object(candidate,'git',side_effect=self.git):
            with self.assertRaisesRegex(ValueError,'identity'):candidate.validate(self.root,self.manifest)
    def test_course_cannot_bypass_conformance_by_declaring_itself_a_hub(self):
        (self.root/'course/boulingua.yml').write_text('code: efl\nkind: hub\n')
        with patch.object(candidate,'git',side_effect=self.git):
            with self.assertRaisesRegex(ValueError,'identity'):candidate.validate(self.root,self.manifest)
    def test_draft_review_scope_is_explicit_and_still_cannot_deploy(self):
        self.data['include_drafts']=True;self.save()
        with patch.object(candidate,'git',side_effect=self.git):
            receipt=candidate.validate(self.root,self.manifest)
        self.assertTrue(receipt['include_drafts']);self.assertFalse(receipt['deploy'])
        self.data['include_drafts']='false';self.save()
        with self.assertRaisesRegex(ValueError,'boolean'):candidate.validate(self.root,self.manifest)
    def test_actual_dirty_wrong_or_schema_incompatible_sources_fail(self):
        with patch.object(candidate,'git',return_value='f'*40):
            with self.assertRaisesRegex(ValueError,'checked-out'):candidate.validate(self.root,self.manifest)
        with patch.object(candidate,'git',side_effect=lambda p,*a:' M source.py' if a[0]=='status' else self.git(p,*a)):
            with self.assertRaisesRegex(ValueError,'not clean'):candidate.validate(self.root,self.manifest)
        (self.root/'course/curriculum.yml').write_text('framework_version: 1.3.0\n')
        with patch.object(candidate,'git',side_effect=self.git):
            with self.assertRaisesRegex(ValueError,'language'):candidate.validate(self.root,self.manifest)
    def test_candidate_workflow_has_no_deployment_privilege_or_job(self):
        path=Path(__file__).resolve().parents[1]/'.github/workflows/candidate-check.yml'
        workflow=yaml.load(path.read_text(),Loader=yaml.BaseLoader)
        self.assertEqual(workflow['permissions'],{'contents':'read'})
        self.assertEqual(list(workflow['jobs']),['candidate'])
        self.assertEqual(workflow['jobs']['candidate']['permissions'],{'contents':'read'})
        self.assertNotIn('environment',workflow['jobs']['candidate'])
        self.assertNotIn('deploy-pages',path.read_text());self.assertNotIn('pages: write',path.read_text())
        self.assertIn('candidate-ci/**',workflow['on']['push']['branches'])

if __name__=='__main__':unittest.main()
