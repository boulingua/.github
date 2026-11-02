"""A1 must preserve consumer contracts in arbitrarily named CI checkouts."""
from pathlib import Path
import os
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/kit_drift.py'


class CheckoutIdentity(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'course'
        self.kit = self.root / 'kit'
        self.put(self.kit, 'gates.yml', 'gates: []\n')
        self.put(self.kit, 'templates/deploy.yml', 'name: shared\njobs: {}\n')
        for rel in ['layouts/_partials/header.html', 'assets/css/custom.css',
                    'archetypes/default.md', 'layouts/home.html',
                    'layouts/_partials/head/theme-styles.html', 'scripts/shared.py']:
            self.put(self.kit, rel, 'shared\n')
        for lang in ['de', 'en', 'fr']:
            self.put(self.kit, f'i18n/{lang}.yaml', 'shared_label:\n  other: Shared\n')

    def put(self, base, rel, text):
        path = base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def consumer(self, identity, kind, code=None):
        code = code or identity
        self.put(self.repo, 'go.mod', f'module github.com/boulingua/{identity}\n')
        if kind != 'reading-library':
            self.put(self.repo, 'boulingua.yml', f'code: {code}\nkind: {kind}\n')
        self.put(self.repo, 'hugo.toml', f'baseURL = "https://boulingua.github.io/{identity}/"\n'
                 f'[params]\ncode = "{code}"\n[[module.imports]]\npath = "github.com/boulingua/kit"\n')
        if kind == 'reading-library':
            self.put(self.repo, 'go.mod', f'module github.com/boulingua/{identity}\nrequire github.com/boulingua/kit v1.23.0\n')
            self.put(self.repo, '.github/workflows/pages.yml', 'jobs:\n  build:\n    steps:\n'
                     '      - run: |\n          npm test\n          python scripts/verify.py\n'
                     '          hugo --panicOnWarning\n          python scripts/check_links.py\n')
            self.put(self.repo, 'layouts/home.html', 'Book catalogue\n')
        else:
            self.put(self.repo, '.github/workflows/deploy.yml', 'name: shared\njobs: {}\n')

    def check(self, expected=0):
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.repo)],
                                env={**os.environ, 'BLG_KIT': str(self.kit)},
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def test_renamed_catalogue_additions_pass_but_shared_key_replacement_fails(self):
        self.consumer('ressources', 'catalogue')
        for lang in ['de', 'en', 'fr']:
            self.put(self.repo, f'i18n/{lang}.yaml', 'catalogue_filter:\n  other: Filter\n')
        self.assertIn('1 course/product consumer', self.check())
        self.put(self.repo, 'i18n/en.yaml', 'shared_label:\n  other: Replaced\n')
        self.assertIn('i18n/en.yaml', self.check(1))

    def test_catalogue_cannot_copy_arbitrary_shared_code(self):
        self.consumer('ressources', 'catalogue')
        self.put(self.repo, 'scripts/shared.py', 'fork\n')
        self.assertIn('scripts/shared.py', self.check(1))

    def test_folder_name_does_not_grant_catalogue_privileges(self):
        self.repo = self.root / 'ressources'
        self.consumer('efl', 'course')
        self.put(self.repo, 'i18n/en.yaml', 'catalogue_filter:\n  other: Filter\n')
        self.assertIn('i18n/en.yaml', self.check(1))

    def test_renamed_hub_only_has_three_named_overrides(self):
        self.consumer('website', 'hub', 'hub')
        for rel in ['layouts/_partials/header.html', 'assets/css/custom.css', 'archetypes/default.md']:
            self.put(self.repo, rel, 'Hub component\n')
        self.check()
        self.put(self.repo, 'scripts/shared.py', 'fork\n')
        self.assertIn('scripts/shared.py', self.check(1))

    def test_hub_workflow_is_still_checked(self):
        self.consumer('website', 'hub', 'hub')
        for rel in ['layouts/_partials/header.html', 'assets/css/custom.css', 'archetypes/default.md']:
            self.put(self.repo, rel, 'Hub component\n')
        self.put(self.repo, '.github/workflows/deploy.yml', 'name: bypass\n')
        self.assertIn('caller differs', self.check(1))

    def test_identity_declarations_must_agree(self):
        self.consumer('ressources', 'catalogue')
        for relative, text in [
                ('boulingua.yml', 'code: efl\nkind: course\n'),
                ('go.mod', 'module github.com/elsewhere/ressources\n'),
                ('go.mod', 'module github.com/boulingua/unregistered\n'),
                ('go.mod', 'module github.com/boulingua/efl\n'),
                ('hugo.toml', 'baseURL = "https://boulingua.github.io/efl/"\n[params]\ncode="ressources"\n[[module.imports]]\npath="github.com/boulingua/kit"\n')]:
            with self.subTest(relative=relative, text=text):
                prior = (self.repo / relative).read_text()
                self.put(self.repo, relative, text)
                self.assertIn('identity cannot be verified', self.check(1))
                self.put(self.repo, relative, prior)
        (self.repo / 'go.mod').unlink()
        self.assertIn('go.mod is required', self.check(1))

    def test_available_git_origin_must_match_even_if_local_declarations_are_spoofed(self):
        self.consumer('ressources', 'catalogue')
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)
        for origin in ['https://github.com/boulingua/ressources.git',
                       'git@github.com:boulingua/ressources.git',
                       'ssh://git@github.com/boulingua/ressources.git']:
            subprocess.run(['git', '-C', str(self.repo), 'config', 'remote.origin.url', origin], check=True)
            self.check()
        for origin in ['https://github.com/boulingua/efl.git',
                       'https://github.com/attacker/ressources.git']:
            subprocess.run(['git', '-C', str(self.repo), 'config', 'remote.origin.url', origin], check=True)
            self.assertIn('Git origin disagrees', self.check(1))

    def test_renamed_library_retains_home_override_not_compatibility_partial_waiver(self):
        self.consumer('scriptlibrary', 'reading-library', 'hub')
        self.check()
        self.put(self.repo, 'layouts/_partials/head/theme-styles.html', 'temporary compatibility\n')
        self.assertIn('theme-styles.html', self.check(1))

    def library_compatibility(self):
        self.consumer('scriptlibrary', 'reading-library', 'hub')
        self.put(self.repo, 'go.mod', 'module github.com/boulingua/scriptlibrary\nrequire github.com/boulingua/kit v1.22.0\n')
        paths = ['layouts/_partials/head/custom-icons.html',
                 'layouts/_partials/head/theme-styles.html', 'static/brand/hub.svg']
        for path in paths:
            self.put(self.kit, path, 'Exact shared counterpart\n')
            self.put(self.repo, path, 'Exact shared counterpart\n')
        data = {'kit_pin': 'v1.22.0', 'files': {path: hashlib.sha256((self.kit/path).read_bytes()).hexdigest()
                                             for path in paths}}
        self.put(self.repo, 'kit-compatibility.json', json.dumps(data))
        return data

    def test_historical_compatibility_requires_all_exact_shared_bytes(self):
        data = self.library_compatibility()
        self.check()
        for path in data['files']:
            with self.subTest(path=path):
                original = (self.repo/path).read_text()
                self.put(self.repo, path, 'Altered copy\n')
                self.assertIn('bytes differ', self.check(1))
                self.put(self.repo, path, original)
        path = 'static/brand/hub.svg'
        # A locally edited manifest cannot bless a fork, even outside KIT_OWNED.
        self.put(self.repo, path, 'Altered copy\n')
        data['files'][path] = hashlib.sha256((self.repo/path).read_bytes()).hexdigest()
        self.put(self.repo, 'kit-compatibility.json', json.dumps(data))
        self.assertIn('current kit', self.check(1))

    def test_historical_compatibility_rejects_extra_paths_and_files(self):
        data = self.library_compatibility()
        data['files']['scripts/shared.py'] = hashlib.sha256(b'shared\n').hexdigest()
        self.put(self.repo, 'kit-compatibility.json', json.dumps(data))
        self.assertIn('manifest paths differ', self.check(1))
        data = self.library_compatibility()
        self.put(self.repo, 'scripts/shared.py', 'shared\n')
        self.assertIn('scripts/shared.py', self.check(1))

    def test_historical_compatibility_must_retire_on_pin_promotion(self):
        self.library_compatibility()
        self.put(self.repo, 'go.mod', 'module github.com/boulingua/scriptlibrary\nrequire github.com/boulingua/kit v1.23.0\n')
        self.assertIn('must retire', self.check(1))
        (self.repo/'kit-compatibility.json').unlink()
        self.assertIn('retire all', self.check(1))
        for path in ['layouts/_partials/head/custom-icons.html',
                     'layouts/_partials/head/theme-styles.html', 'static/brand/hub.svg']:
            (self.repo/path).unlink()
        self.check()

    def test_compatibility_published_dependencies_cannot_be_replaced(self):
        self.library_compatibility()
        original = (self.repo/'go.mod').read_text()
        for directive in ['replace github.com/boulingua/kit => ../other\n',
                          'replace "github.com/boulingua/kit" => ../other\n',
                          'replace (\n  "github.com/boulingua/kit" => ../other\n)\n',
                          'replace github.com/luizdepra/hugo-coder => ../other\n']:
            with self.subTest(directive=directive):
                self.put(self.repo, 'go.mod', original + directive)
                self.assertIn('cannot replace', self.check(1))

    def test_unparseable_catalogue_translations_are_not_exempted(self):
        self.consumer('ressources', 'catalogue')
        for text in ['- shared_label\n', 'invalid: [\n']:
            with self.subTest(text=text):
                self.put(self.repo, 'i18n/en.yaml', text)
                self.assertIn('i18n/en.yaml', self.check(1))


if __name__ == '__main__':
    unittest.main()
