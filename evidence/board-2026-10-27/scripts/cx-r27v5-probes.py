#!/usr/bin/env python3
"""Read-only candidate probes; all Git mutations use temporary bare remotes."""
import json
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

SOURCE = Path(sys.argv[1]).resolve()
ARTIFACT = (Path(sys.argv[2]) if len(sys.argv) > 2 else
            Path(__file__).resolve().parents[1] / 'cx-r27v5-cb7d8213/trusted-pr-plan.zip')
sys.path.insert(0, str(SOURCE / 'scripts'))
import receipt_writer as writer
import receipt_tasklink as tasklink
import receipt_verifier as verifier
import test_receipt_postrun as workflow

spec = importlib.util.spec_from_file_location('review_planning', Path(__file__).resolve().parents[3] / 'scripts/plan.py')
planning = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = planning
spec.loader.exec_module(planning)


def git(root, *args, check=True):
    return subprocess.run(['git', '-C', str(root), *args], capture_output=True,
                          check=check).stdout.decode().strip()


def seed(root, note='---\nid: example\n---\nbody\n'):
    bare, local = root / 'remote.git', root / 'local'
    subprocess.run(['git', 'init', '--bare', '-q', str(bare)], check=True)
    local.mkdir()
    git(local, 'init', '-q', '-b', 'main')
    git(local, 'config', 'user.name', 'Review fixture')
    git(local, 'config', 'user.email', 'review@example.invalid')
    (local / 'tasks').mkdir()
    (local / 'tasks/example.md').write_text(note)
    git(local, 'add', '.')
    git(local, 'commit', '-qm', 'seed')
    git(local, 'remote', 'add', 'origin', str(bare))
    git(local, 'push', '-q', 'origin', 'main')
    return bare, local


with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    # Real shell decoder, with no implicit checkout/PYTHONPATH as on extract_plan.
    block = workflow._extract_run_block('decode')
    env = dict(os.environ, GITHUB_OUTPUT=str(root / 'out'))
    env.pop('PYTHONPATH', None)
    proc = subprocess.run(['bash', '-c', block], cwd=root, env=env, capture_output=True, text=True)
    print('decoder_fresh_job:', proc.returncode, proc.stderr.strip().splitlines()[-1])
    env['PYTHONPATH'] = str(SOURCE / 'scripts')
    with zipfile.ZipFile(root / 'plan.zip', 'w') as z:
        real = zipfile.ZipFile(ARTIFACT).read('pr-plan.json')
        z.writestr('pr-plan.json', real)
    proc = subprocess.run(['bash', '-c', block], cwd=root, env=env, capture_output=True, text=True)
    print('decoder_real_artifact_after_shape_and_import_repair:', proc.returncode,
          proc.stderr.strip().splitlines()[-1])
    # Decoder bypasses unique() and does not bind authenticated head/run.
    raw = json.dumps(workflow.FAKE_PLAN)[:-1] + ',"integration_sha":"' + 'd' * 40 + '"}'
    with zipfile.ZipFile(root / 'plan.zip', 'w') as z:
        z.writestr('pr-plan.json', raw)
    proc = subprocess.run(['bash', '-c', block], cwd=root, env=env, capture_output=True, text=True)
    print('decoder_duplicate_integration:', proc.returncode,
          'candidate_sha=' + 'd' * 40 in (root / 'out').read_text())
    forged = dict(workflow.FAKE_PLAN, head_sha='e' * 40, run_id=999)
    with zipfile.ZipFile(root / 'plan.zip', 'w') as z:
        z.writestr('pr-plan.json', json.dumps(forged))
    (root / 'out').write_text('')
    proc = subprocess.run(['bash', '-c', block], cwd=root, env=env, capture_output=True, text=True)
    print('decoder_wrong_head_and_run:', proc.returncode, (root / 'out').read_text().splitlines())

proc = subprocess.run([sys.executable, str(SOURCE / 'scripts/receipt_writer.py'),
                       '--planning', '/tmp', '--plan', 'a' * 40, '--run', '1',
                       '--attempt', '1', '--product', str(SOURCE), '--publish'],
                      capture_output=True, text=True)
print('workflow_writer_product_argument:', proc.returncode, proc.stderr.strip().splitlines()[-1])

with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    bare, local = seed(root)
    (local / 'plan.json').write_text('new local plan')
    git(local, 'add', '.')
    git(local, 'commit', '-qm', 'new unpublished plan')
    plan = git(local, 'rev-parse', 'HEAD')
    value = dict(gate=verifier.GATE, run=dict(id=17, attempt=1), sha='a' * 40,
                 status='pass', plan=plan, approved=None)
    path = verifier.path_for(value)
    commit = writer.commit_file(local, path, verifier.canonical(value))
    other = root / 'other'
    subprocess.run(['git', 'clone', '-q', '-b', 'main', str(bare), str(other)], check=True)
    git(other, 'config', 'user.name', 'Concurrent fixture')
    git(other, 'config', 'user.email', 'other@example.invalid')
    (other / 'unrelated').write_text('preserve')
    git(other, 'add', '.')
    git(other, 'commit', '-qm', 'concurrent')
    git(other, 'push', '-q', 'origin', 'main')
    result = writer.publish(local, path, commit)
    reachable = subprocess.run(['git', '-C', str(bare), 'merge-base', '--is-ancestor',
                                plan, 'main'], capture_output=True).returncode == 0
    print('new_plan_race_publish_success:', bool(result), 'plan_reachable:', reachable,
          'remote_paths:', git(bare, 'ls-tree', '-r', '--name-only', 'main').splitlines())
    # Approval race against the existing unapproved remote predecessor.
    original = git(local, 'rev-parse', 'HEAD')
    approved = dict(value, approved=dict(by='mcpdev80', at='2026-10-27T22:00:00Z', receipt_commit=original))
    edit = writer.commit_file(local, path, verifier.canonical(approved), expected=verifier.canonical(value))
    git(other, 'fetch', 'origin', 'main')
    git(other, 'reset', '--hard', 'origin/main')
    (other / 'unrelated2').write_text('preserve too')
    git(other, 'add', '.')
    git(other, 'commit', '-qm', 'concurrent approval')
    git(other, 'push', '-q', 'origin', 'main')
    try:
        writer.publish(local, path, edit)
        print('approval_race: SUCCESS')
    except verifier.ReceiptError as exc:
        print('approval_race:', str(exc))

for style in ('inline', 'block'):
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        evidence = 'evidence: ["https://example.invalid/old"]' if style == 'inline' else 'evidence:\n  - "https://example.invalid/old"'
        bare, local = seed(root, '---\nid: example\n' + evidence + '\nprs:\n  - "mcpdev80/baseharbor#17"\n---\nbody\n')
        try:
            publication = tasklink.publish_evidence(local, 'tasks/example.md',
                                                    'https://example.invalid/new', 'a' * 40, 'b' * 40)
            note = git(bare, 'show', 'main:tasks/example.md')
            print('card_' + style + '_published:', publication,
                  'old_preserved:', 'https://example.invalid/old' in note,
                  'prs_preserved:', 'mcpdev80/baseharbor#17' in note,
                  'evidence_keys:', note.count('evidence:'),
                  'parsed:', verifier.front_matter(note))
            try:
                planning.parse_frontmatter(note + '\n')
                print('planning_parser_' + style + ': ACCEPT')
            except ValueError as exc:
                print('planning_parser_' + style + ': REJECT:', str(exc))
        except Exception as exc:
            print('card_' + style + ':', type(exc).__name__, str(exc))

print('issuance_missing_task:', tasklink.resolve_task_from_pr(17, Path('/nonexistent'),
      lambda path: {'body': 'Closes #18'} if '/pulls/' in path else {'body': 'tasks/nonexistent.md'}))

# Duplicate metadata must agree with the real Planning parser.
note = '---\nid: example\nprs: ["mcpdev80/baseharbor#1"]\nprs: ["mcpdev80/baseharbor#17"]\n---\n'
print('approval_parser_duplicate_prs:', verifier.front_matter(note))
try:
    planning.parse_frontmatter(note)
except ValueError as exc:
    print('real_planning_parser_duplicate_prs:', exc)
