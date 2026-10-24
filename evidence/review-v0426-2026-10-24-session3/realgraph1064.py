import importlib.util,json,subprocess
from pathlib import Path
root=Path('review-core').resolve()
def mod(name,path):
 s=importlib.util.spec_from_file_location(name,root/'scripts'/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p=mod('p','pr-gate-plan.py');r=mod('r','pr-diff-base.py')
def git(*a): return subprocess.check_output(['git','-C',str(root),*a],text=True).strip()
R=p.EXACT_1060_REVIEWED_HEAD;B='54dfa458528e958be0ea3d8157a46bd501e76eb1'
for path,h in p.EXACT_1060_REVIEWED_HASHES.items(): assert git('rev-parse',R+':'+path)==h
T=git('merge-tree','--write-tree',R,B).splitlines()[0]
H=git('commit-tree',T,'-p',R,'-p',B,'-m','review-only synthetic forward merge')
I=git('commit-tree',T,'-p',B,'-p',H,'-m','review-only synthetic integration')
d=r.resolve_pr_diff(root,B,H,I)
checks=p.exact_1060_binding(d,root,'mcpdev80/baseharbor','develop')
assert checks is not None
print(json.dumps({'base_simulation':B,'reviewed':R,'forward_head':H,'integration':I,'tree':T,'checks':[c['id'] for c in checks],'changes':d['changes']},indent=2))
for label,mut in [('wrong-repo',lambda x:None),('missing-integration',lambda x:x.update(integration_sha=None)),('wrong-status',lambda x:x['changes'][0].update(status='added')),('changed-merge-base',lambda x:x.update(merge_base_sha='f'*40))]:
 import copy
 x=copy.deepcopy(d);mut(x)
 assert p.exact_1060_binding(x,root,'other/repo' if label=='wrong-repo' else 'mcpdev80/baseharbor','develop') is None,label
 print(label+': rejected')
