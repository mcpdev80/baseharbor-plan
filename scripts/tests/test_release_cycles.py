"""Recurring release operations cannot disappear from the planning graph."""
import pathlib
import shutil
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import plan
import release_cycles as cycles
from test_plan import Fixture, REPO, task_note as original_task_note


def task_note(*args, **kwargs):
    return original_task_note(*args, **kwargs).replace("v1.0", "v1.0.0").replace("v1-0", "v1-0-0")


class ReleaseCycleTests(unittest.TestCase):
    def fixture(self):
        fixture = Fixture()
        self.addCleanup(shutil.rmtree, fixture.dir)
        for short, full in [('v1.0', 'v1.0.0'), ('v2.0', 'v2.0.0')]:
            old = fixture.dir / 'releases' / (short + '.md')
            new = fixture.dir / 'releases' / (full + '.md')
            new.write_text(old.read_text().replace(short, full))
            old.unlink()
        shutil.copy(REPO / 'RELEASE_WORKFLOW.md', fixture.dir / 'RELEASE_WORKFLOW.md')
        shutil.copytree(REPO / 'templates/release-cycle', fixture.dir / 'templates/release-cycle')
        return fixture

    def test_missing_release_stages_are_rejected_and_sync_fills_them(self):
        f = self.fixture().finish()
        vault = plan.Vault(f.dir).load()
        self.assertEqual(len(cycles.problems(vault)), 12)
        self.assertEqual(cycles.sync(f.dir), 2)
        code, output = f.checked()
        self.assertEqual(code, 0, output)
        self.assertEqual(len(plan.Vault(f.dir).load().tasks), 12)

    def test_scope_and_startup_dependencies_are_complete_and_acyclic(self):
        f = self.fixture()
        f.add_task('core-1', task_note('core-1', 'A: implementation'))
        f.finish()
        cycles.sync(f.dir)
        vault = plan.Vault(f.dir).load()
        self.assertIn(cycles.stage_id('v1.0.0', 'updates'), vault.tasks['core-1']['depends_on'])
        prepare = vault.tasks[cycles.stage_id('v1.0.0', 'prepare')]
        self.assertIn('core-1', prepare['depends_on'])
        self.assertIn(cycles.stage_id('v1.0.0', 'updates'), prepare['depends_on'])
        self.assertEqual(f.checked()[0], 0)
        f.add_task('core-2', task_note('core-2', 'B: added scope'))
        errors = cycles.problems(plan.Vault(f.dir).load())
        self.assertTrue(any('prerequisites missing' in msg for _, msg in errors))
        self.assertTrue(any('intake prerequisite missing' in msg for _, msg in errors))
        cycles.sync(f.dir)
        self.assertEqual(cycles.problems(plan.Vault(f.dir).load()), [])

    def test_series_only_materializes_explicit_versions(self):
        f = self.fixture().finish()
        release = f.dir / 'releases/v1.0.0.md'
        series = f.dir / 'releases/v1.x.md'
        series.write_text(release.read_text().replace('v1.0.0', 'v1.x').replace('kind: release', 'kind: series\ncycle_versions: [v1.0.0]'))
        release.unlink()
        planned = cycles.targets(plan.Vault(f.dir).load())
        self.assertEqual(planned['v1.0.0'], 'v1.x')
        self.assertNotIn('v1.x', planned)
        cycles.sync(f.dir)
        self.assertEqual(f.checked()[0], 0)

    def test_sync_is_idempotent_and_preserves_claims_and_handoffs(self):
        f = self.fixture().finish()
        cycles.sync(f.dir)
        path = f.dir / 'tasks' / (cycles.stage_id('v1.0.0', 'cleanup') + '.md')
        path.write_text(path.read_text().replace('owner: ""', 'owner: tester')
                        .replace('#status/planned', '#status/active') + '\nPreserve this real handoff.\n')
        f.run('render')
        before = {str(p): p.read_text() for p in f.dir.rglob('*.md')}
        cycles.sync(f.dir)
        f.run('render')
        self.assertEqual(before, {str(p): p.read_text() for p in f.dir.rglob('*.md')})
        self.assertIn('owner: tester', path.read_text())
        self.assertIn('Preserve this real handoff.', path.read_text())

    def test_duplicate_stage_and_missing_stage_fail(self):
        f = self.fixture().finish()
        cycles.sync(f.dir)
        tid = cycles.stage_id('v1.0.0', 'cleanup')
        path = f.dir / 'tasks' / (tid + '.md')
        other = f.dir / 'tasks/t-20261017-other.md'
        other.write_text(path.read_text().replace(tid, 't-20261017-other'))
        self.assertTrue(any('exactly one cleanup' in msg for _, msg in cycles.problems(plan.Vault(f.dir).load())))
        other.unlink()
        path.unlink()
        self.assertTrue(any('exactly one cleanup' in msg for _, msg in cycles.problems(plan.Vault(f.dir).load())))

    def test_current_release_bootstrap_does_not_rewrite_active_work(self):
        f = self.fixture()
        p = f.dir / 'releases/v1.0.0.md'
        (f.dir / 'releases/v0.4.26.md').write_text(p.read_text().replace('v1.0.0', 'v0.4.26'))
        p.unlink()
        note = task_note('core-1', 'A: ongoing', status='active', release='v0.4.26', extra='existing owner')
        f.add_task('core-1', note)
        f.finish()
        cycles.sync(f.dir)
        self.assertEqual((f.dir / 'tasks/core-1-x.md').read_text(), note)
        vault = plan.Vault(f.dir).load()
        current = [t for t in vault.tasks.values() if t['version'] == 'v0.4.26' and t['meta'].get('release_stage')]
        self.assertEqual({t['meta']['release_stage'] for t in current}, {'prepare', 'qualify', 'publish', 'verify'})
        self.assertEqual(vault.tasks[cycles.stage_id('v0.4.26', 'prepare')]['depends_on'], ['core-1'])
        cycles.sync(f.dir)
        self.assertFalse((f.dir / 'tasks' / (cycles.stage_id('v0.4.26', 'cleanup') + '.md')).exists())
        self.assertFalse((f.dir / 'tasks' / (cycles.stage_id('v0.4.26', 'updates') + '.md')).exists())
        prepare = f.dir / 'tasks' / (cycles.stage_id('v0.4.26', 'prepare') + '.md')
        cycles.set_dependencies(prepare, ['core-1', cycles.stage_id('v0.4.26', 'updates')])
        cycles.sync(f.dir)
        current = plan.Vault(f.dir).load()
        self.assertEqual(current.tasks[cycles.stage_id('v0.4.26', 'prepare')]['depends_on'], ['core-1'])
        self.assertEqual(f.checked()[0], 0)

    def test_accepted_release_stage_cannot_hide_unaccepted_scope(self):
        f = self.fixture().finish()
        cycles.sync(f.dir)
        tid = cycles.stage_id('v1.0.0', 'prepare')
        path = f.dir / 'tasks' / (tid + '.md')
        path.write_text(path.read_text().replace('- [ ]', '- [x]').replace('#status/planned', '#status/closed')
                        .replace('resolution: ""', 'resolution: accepted')
                        .replace('evidence: []', 'evidence: ["https://example.org/proof"]'))
        errors = cycles.problems(plan.Vault(f.dir).load())
        self.assertTrue(any('reopen and requalify' in msg for _, msg in errors))

    def test_required_policy_and_templates_exist(self):
        self.assertTrue((REPO / 'RELEASE_WORKFLOW.md').exists())
        for stage, _ in cycles.STAGES:
            self.assertTrue((REPO / 'templates/release-cycle' / (stage + '.md')).exists())


if __name__ == '__main__':
    unittest.main()
