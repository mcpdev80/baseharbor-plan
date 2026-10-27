#!/usr/bin/env python3
"""Compare the actual immutable reusable schema against candidate call inputs."""
import subprocess
import sys
from pathlib import Path
import yaml
repo, source = Path(sys.argv[1]), Path(sys.argv[2])
old = subprocess.check_output(['git', '-C', str(repo), 'show',
    'f57b30ed:.github/workflows/receipt-shadow.yml'], text=True)
new = (source / '.github/workflows/receipt-approval.yml').read_text()
schema = yaml.load(old, Loader=yaml.BaseLoader)['on']['workflow_call']['inputs']
caller = yaml.load(new, Loader=yaml.BaseLoader)['jobs']['shadow']
print('selected_reusable_source:', caller['uses'])
print('selected_reusable_inputs:', sorted(schema))
print('unsupported_caller_inputs:', sorted(set(caller['with']) - set(schema)))
