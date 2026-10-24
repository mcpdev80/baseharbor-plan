import sys, importlib.util, unittest
from pathlib import Path
sys.path.insert(0, str(Path('review-core/scripts').resolve()))
import test_pr_gate_plan as t
original = t.Exact1060BindingTests._make_four_file_reviewed_head
def bound(self, *a, **kw):
    sha = original(self, *a, **kw)
    from unittest.mock import patch
    for attr, value in [('EXACT_1060_REVIEWED_HEAD', sha), ('EXACT_1060_REVIEWED_HASHES', {p:self.git('rev-parse', sha+':'+p) for p in t.planner.EXACT_1060_REVIEWED_FILES})]:
        ctx=patch.object(t.planner, attr, value); ctx.start(); self.addCleanup(ctx.stop)
    return sha
t.Exact1060BindingTests._make_four_file_reviewed_head = bound
unittest.main(module=t, argv=['probe','Exact1060BindingTests'], verbosity=2)
