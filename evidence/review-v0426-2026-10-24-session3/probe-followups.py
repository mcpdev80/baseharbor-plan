import importlib.util,json,subprocess,tempfile,copy,sys
from pathlib import Path
from unittest.mock import patch
base=Path.cwd()
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p60=load('p60',base/'source1060/scripts/pr-gate-plan.py');c60=load('c60',base/'source1060/scripts/pr-check-runner.py')
mp=json.loads((base/'source1060/scripts/pr-gate-map-v1.json').read_text());req=json.loads((base/'source1060/scripts/release-requirements.json').read_text())
d={'target_base_sha':'a'*40,'head_sha':'b'*40,'merge_base_sha':'c'*40,'integration_sha':'d'*40,'broad_required':False,'reasons':[],'changes':[{'path':p,'status':'modified'} for p in ['internal/openbao/bootstrap.go','internal/openbao/bootstrap_test.go']]}
result=p60.plan(d,req,mp)
print('1060 bootstrap pair:',result['coverage_status'],[c['id'] for c in result['required_validation_checks']],result['unresolved_coverage'])
try:c60.execute_validation('openbao-package-tests',base/'source1060')
except Exception as e:print('1060 openbao execute:',type(e).__name__,str(e))
def fake(cmd,**kw):
 pattern=cmd[cmd.index('-list')+1] if '-list' in cmd else cmd[cmd.index('-run')+1]
 name=pattern.lstrip('^')+'Replacement'
 return subprocess.CompletedProcess(cmd,0,stdout=name+'\n' if '-list' in cmd else '=== RUN   '+name+'\n--- PASS: '+name+' (0.0s)\n',stderr='')
with patch.object(c60.subprocess,'run',side_effect=fake):
 print('1060 exact SQL safety names replaced:',c60.execute_validation('wizard-core918-native-sql-safety-tests',base/'source1060'))
c56=load('c56',base/'source1056/scripts/pr-check-runner.py');p56=load('p56',base/'source1056/scripts/pr-gate-plan.py');r56=load('r56',base/'source1056/scripts/pr-diff-base.py')
pins=json.loads(subprocess.check_output(['git','-C',str(base/'review-core'),'show','388967621c90750e59c5faab35344b46d4108fef:docs/releases/v0.4.26.consumer-pins.json'],text=True))
for label,mut in [('cycle',lambda x:x['ecosystem']['core']['consumes'].update(connector=x['ecosystem']['connector']['commit'])),('wrong-origin',lambda x:x['gates']['integration/static/live-console']['console']['origin'].update(commit='f'*40)),('wrong-console-repo',lambda x:x['gates']['integration/static/live-console']['console'].update(repository='attacker/repo'))]:
 with tempfile.TemporaryDirectory() as td:
  root=Path(td);f=root/'docs/releases/v0.4.26.consumer-pins.json';f.parent.mkdir(parents=True);x=copy.deepcopy(pins);mut(x);f.write_text(json.dumps(x))
  print('1056 '+label+':',c56.validate_pins_data('pins-data-validation',root))
with tempfile.TemporaryDirectory() as td:
 root=Path(td)
 def git(*a):return subprocess.check_output(['git','-C',td,*a],text=True,stderr=subprocess.DEVNULL).strip()
 git('init','-q');git('config','user.name','Reviewer');git('config','user.email','review@example.test')
 f=root/p56.BOOTSTRAP_AKTE_FILENAME;f.parent.mkdir(parents=True);f.write_text(p56.BOOTSTRAP_AKTE_TITLE+'\n```json\n{}\n```\n');git('add','.');git('commit','-qm','base');B=git('rev-parse','HEAD')
 f=root/'internal/unreviewed/security.go';f.parent.mkdir(parents=True);f.write_text('unreviewed change');git('add','.');git('commit','-qm',p56.BOOTSTRAP_AKTE_TITLE);H=git('rev-parse','HEAD');T=git('rev-parse','HEAD^{tree}');I=git('commit-tree',T,'-p',B,'-p',H,'-m','integration')
 d=r56.resolve_pr_diff(root,B,H,I);result=p56.plan(d,req,mp,root,'mcpdev80/baseharbor','develop');print('1056 arbitrary source with bootstrap title:',result['coverage_status'],result['selected_gates'],[c['id'] for c in result['required_validation_checks']])
