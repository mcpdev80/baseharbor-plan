#!/usr/bin/env python3
"""Create/check release cards; v0.4.26 retains only its four completion stages. Standard library only."""
import pathlib
import re
import sys

STAGES = (
    ('cleanup', 'Release start: reconcile old PRs, tasks and branches'),
    ('updates', 'Release start: integrate Renovate updates before feature work'),
    ('prepare', 'Pre-release: complete ecosystem readiness and candidate preparation'),
    ('qualify', 'Pre-release: obtain complete authenticated approval'),
    ('publish', 'Release: promote the approved candidate and deliver exact tagging commands'),
    ('verify', 'Release: verify publication, artifacts, Pages and closeout'),
)
VERSION = re.compile(r'^v\d+\.\d+\.\d+(?:\.\d+)?$')


def stages_for(version):
    """The startup policy starts after the already-running v0.4.26 release."""
    return STAGES[2:] if version == 'v0.4.26' else STAGES


def targets(vault):
    result = {}
    for release in vault.releases.values():
        if release['kind'] == 'release' and VERSION.fullmatch(release['id']):
            result[release['id']] = release['id']
        # Only explicitly planned concrete versions; never invent a release from an x-series.
        for version in release.get('cycle_versions', []):
            if VERSION.fullmatch(version):
                result[version] = release['id']
    for task in vault.tasks.values():
        if task['version'] and VERSION.fullmatch(task['version']):
            result[task['version']] = task['release']
    return dict(sorted(result.items(), key=lambda x: tuple(map(int, x[0][1:].split('.')))))


def stage_id(version, stage):
    return 't-20261017-release-' + version[1:].replace('.', '-') + '-' + stage


def scope_tasks(vault, version, release):
    return [t for t in vault.tasks.values() if not t['meta'].get('release_stage') and
            t['release'] == release and (t['version'] == version or release == version)]


def expected_dependencies(vault, version, release, stage):
    names = [s for s, _ in stages_for(version)]
    index = names.index(stage)
    deps = [stage_id(version, names[index - 1])] if index else []
    if stage == 'prepare':
        deps += [t['id'] for t in scope_tasks(vault, version, release)]
    return sorted(set(deps))


def problems(vault):
    if not (vault.root / 'RELEASE_WORKFLOW.md').exists():
        return []
    errors = []
    planned = targets(vault)
    valid_stages = {s for s, _ in STAGES}
    for release in vault.releases.values():
        for version in release.get('cycle_versions', []):
            if not VERSION.fullmatch(version):
                errors.append((release['path'], f'invalid concrete cycle version {version!r}'))
    for task in vault.tasks.values():
        stage = task['meta'].get('release_stage')
        if stage and (stage not in valid_stages or task['version'] not in planned or
                      stage not in {name for name, _ in stages_for(task['version'])}):
            errors.append((task['path'], 'unknown release stage or concrete version'))
    for version, release in planned.items():
        for stage, _ in stages_for(version):
            matches = [t for t in vault.tasks.values() if t['version'] == version and
                       t['meta'].get('release_stage') == stage]
            if len(matches) != 1:
                errors.append((vault.releases[release]['path'],
                               f'{version} needs exactly one {stage} release card; run scripts/release_cycles.py sync'))
                continue
            task = matches[0]
            if task['release'] != release or task['id'] != stage_id(version, stage):
                errors.append((task['path'], 'release-cycle identity/series mismatch'))
            if task['done'] and task['resolution'] == 'accepted' and any(not vault.accepted(dep) for dep in task['depends_on']):
                errors.append((task['path'], 'accepted release stage has unfinished prerequisites; reopen and requalify it'))
            expected = expected_dependencies(vault, version, release, stage)
            if not set(expected).issubset(task['depends_on']):
                errors.append((task['path'], f'release-cycle prerequisites missing; run scripts/release_cycles.py sync'))
        startup = stage_id(version, 'updates')
        # No retroactive startup requirement for the already-running release.
        if version != 'v0.4.26':
            for task in scope_tasks(vault, version, release):
                if startup not in task['depends_on']:
                    errors.append((task['path'], f'release-start intake prerequisite missing: {startup}'))
    return errors


def set_dependencies(path, dependencies):
    text = path.read_text(encoding='utf-8')
    value = 'depends_on: [' + ', '.join(sorted(set(dependencies))) + ']'
    new, count = re.subn(r'^depends_on:.*$', value, text, count=1, flags=re.M)
    if count != 1:
        raise ValueError(f'{path}: expected one depends_on field')
    if new != text:
        path.write_text(new, encoding='utf-8')


def sync(root):
    from plan import Vault, release_tag
    vault = Vault(root).load()
    planned = targets(vault)
    for version, release in planned.items():
        for stage, title in stages_for(version):
            tid = stage_id(version, stage)
            path = root / 'tasks' / (tid + '.md')
            if path.exists():
                task = vault.tasks.get(tid)
                if not task or task['meta'].get('release_stage') != stage or task['version'] != version:
                    raise ValueError(f'{path}: existing ID belongs to different work; never overwrite it')
                continue
            template = (root / 'templates' / 'release-cycle' / (stage + '.md')).read_text(encoding='utf-8')
            for key, value in {'id': tid, 'version': version, 'release': release,
                               'release_tag': release_tag(release), 'title': title}.items():
                template = template.replace('{{' + key + '}}', value)
            path.write_text(template, encoding='utf-8')
    vault = Vault(root).load()
    for version, release in planned.items():
        for stage, _ in stages_for(version):
            task = vault.tasks[stage_id(version, stage)]
            deps = task['depends_on']
            if version == 'v0.4.26':
                retired = {stage_id(version, 'cleanup'), stage_id(version, 'updates')}
                deps = [dep for dep in deps if dep not in retired]
            set_dependencies(task['path'], deps + expected_dependencies(vault, version, release, stage))
        if version != 'v0.4.26':
            for task in scope_tasks(vault, version, release):
                set_dependencies(task['path'], task['depends_on'] + [stage_id(version, 'updates')])
    return len(planned)


def main():
    import argparse
    from plan import ROOT, Vault, render, cmd_check
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['sync'])
    parser.add_argument('--root', type=pathlib.Path, default=ROOT)
    args = parser.parse_args()
    count = sync(args.root)
    render(Vault(args.root).load())
    print(f'{count} concrete release cycles synchronized; existing claims/status/evidence preserved.')
    return cmd_check(args.root)


if __name__ == '__main__':
    sys.exit(main())
