import importlib.util,json,subprocess,copy
from pathlib import Path
root=Path('review1060-r2').resolve()
def load(name,file):
 s=importlib.util.spec_from_file_location(name,root/'scripts'/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p=load('planner','pr-gate-plan.py');r=load('resolver','pr-diff-base.py')
def git(*a):return subprocess.check_output(['git','-C',str(root),*a],text=True,stderr=subprocess.DEVNULL).strip()
R='9f715184af7b89ca3011aa4a0636c45138fe2c6b';B='65aa063e90767c85af976081c100be1817370e67'
assert p.OPENBAO_RETRY_HEAD==R
T=git('merge-tree','--write-tree',R,B).splitlines()[0]
H=git('commit-tree',T,'-p',R,'-p',B,'-m','review-only #1052 clean target forward')
I=git('commit-tree',T,'-p',B,'-p',H,'-m','review-only #1052 integration')
d=r.resolve_pr_diff(root,B,H,I)
checks=p.openbao_retry_checks(d,root,'mcpdev80/baseharbor','develop')
assert [c['id'] for c in checks]==['source-contracts','openbao-package-tests']
print(json.dumps({'reviewed_source':R,'base':B,'head_simulation':H,'integration_simulation':I,'tree':T,'changes':d['changes'],'checks':[c['id'] for c in checks]},indent=2))
for label,mut in [('missing-integration',lambda x:x.update(integration_sha=None)),('fake-integration',lambda x:x.update(integration_sha=B)),('wrong-merge-base',lambda x:x.update(merge_base_sha='f'*40)),('extra-path',lambda x:x['changes'].append({'path':'internal/openbao/not-reviewed.go','status':'modified'})),('wrong-status',lambda x:x['changes'][0].update(status='added'))]:
 x=copy.deepcopy(d);mut(x);assert p.openbao_retry_checks(x,root,'mcpdev80/baseharbor','develop') is None,label
 print(label+': REJECT')
for repo,branch in [('other/repo','develop'),('mcpdev80/baseharbor','main')]:
 assert p.openbao_retry_checks(d,root,repo,branch) is None
 print(repo+'/'+branch+': REJECT')
F=git('commit-tree',T,'-p',H,'-m','unreviewed identical-tree single parent followup')
J=git('commit-tree',T,'-p',B,'-p',F,'-m','review-only followup integration')
x=r.resolve_pr_diff(root,B,F,J)
assert p.openbao_retry_checks(x,root,'mcpdev80/baseharbor','develop') is None
print('same-tree unreviewed linear followup: REJECT')
