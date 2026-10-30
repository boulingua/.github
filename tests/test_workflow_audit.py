from pathlib import Path
import sys
import unittest
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from org_audit import inspect_workflow


class WorkflowAudit(unittest.TestCase):
    def findings(self, text):
        return inspect_workflow(yaml.load(text, Loader=yaml.BaseLoader))

    def test_quoted_and_global_write_permissions(self):
        for text in ['permissions: write-all', 'permissions: {contents: "write"}', 'jobs: {build: {permissions: {contents: write}}}']:
            self.assertTrue(self.findings(text), text)

    def test_dynamic_failure_suppression(self):
        for value in ['true', '"true"', '"${{ always() }}"']:
            self.assertTrue(self.findings('continue-on-error: ' + value))
        self.assertEqual(self.findings('continue-on-error: false'), [])

    def test_shell_failure_and_push_variants(self):
        for script in ['python verify_urls.py || :', 'python check_files.py || echo failed', 'npm ci || echo no-lockfile', 'git -C org/foo push origin main']:
            self.assertTrue(inspect_workflow({'run': script}), script)

    def test_read_only_build_and_cleanup(self):
        self.assertEqual(inspect_workflow({'permissions': {'contents': 'read'}, 'run': 'npm ci\npython verify_urls.py\nkill "$server_pid" || true'}), [])


if __name__ == '__main__':
    unittest.main()
