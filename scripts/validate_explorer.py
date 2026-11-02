"""Independent audit of the new display payload and derived count denominators."""
from pathlib import Path
import json, math
r=Path(__file__).resolve().parents[1]
def load(n):return json.loads((r/n).read_text())
d=load('web/data/direct-inference.json');lag=load('web/data/generation-lags.json');front=load('web/data/specialist-frontier.json')
full=[t for t in d['tasks'] if t['complete_all_four']];assert len(full)==10
assert len({t['id'][0] for t in full})==7
canonical=load('results/primary-summary.json')['summaries']
for t in d['tasks']:
 for row in t['rows']:
  src=next(z for z in canonical if z['benchmark_id']==t['id'] and z['model']==row['model'])
  assert src['score']==row['score']
  assert row['complete'] or row['score'] is None
for p in lag['task_pairs']:
 t=next(t for t in full if t['id']==p['benchmark_id']);ss=sorted(row['score'] for row in t['rows']);q1=.25*ss[0]+.75*ss[1];q3=.75*ss[2]+.25*ss[3]
 assert math.isclose(q3-q1,p['panel_iqr'],rel_tol=1e-12,abs_tol=1e-12)
 delta=(p['newer_score']-p['older_score'])*(-1 if p['direction']=='lower' else 1)
 assert math.isclose(delta,p['direction_adjusted_delta'],abs_tol=1e-12)
for s in lag['summaries']:
 assert sum(s['counts'].values())==10
 rows=[p for p in lag['task_pairs'] if p['older']==s['older'] and p['newer']==s['newer']]
 for k,v in s['counts'].items():assert v==sum(p[s['analysis']]==k for p in rows)
assert len(lag['task_pairs'])==60 and len(lag['summaries'])==18
assert len([t for t in front['tasks'] if t['best_specialist']])==2
assert len([t for t in front['tasks'] if t['best_available_reference']['classes']['raw']=='general_better'])==3
assert all('gpt-6-sol' not in t['general_scores'] for t in front['tasks'])
print('PASS: canonical scores, partial handling, 60 deltas/IQRs, 18 count rows, reference scopes and model roster')
