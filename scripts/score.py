"""Validate saved direct predictions and score only complete retained test panels."""
from pathlib import Path
import hashlib,json,math
import numpy as np
from sklearn.metrics import balanced_accuracy_score,f1_score
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT.parent/'neural-data-bench'

def parse_response(data,entry):
 if data.get('status')!='completed':raise ValueError('Response did not complete')
 text=''.join(c.get('text','') for o in data.get('output',[]) if o.get('type')=='message'
              for c in o.get('content',[]) if c.get('type')=='output_text')
 obj=json.loads(text)
 if set(obj)!= {'predictions'}:raise ValueError('Unexpected response keys')
 preds=obj['predictions'];expected=list(range(entry['start'],entry['stop']))
 if [p.get('id') for p in preds]!=expected:raise ValueError('Missing, duplicate, reordered or unexpected row IDs')
 values=[]
 for p in preds:
  if set(p)!= {'id','value'}:raise ValueError('Unexpected prediction keys')
  v=p['value']
  if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):raise ValueError('Nonfinite/nonnumeric value')
  if entry['benchmark_id']=='M01':
   if not 0<=v<=1:raise ValueError('Probability out of range')
  elif v not in (0,1) or int(v)!=v:raise ValueError('Invalid class label')
  values.append(float(v))
 return dict(zip(expected,values))

def metric(bid,p,y,groups):
 if bid=='K01':return float(f1_score(y,p.astype(int),labels=[0,1],average='macro',zero_division=0))
 if bid=='I10':return float(balanced_accuracy_score(y,p.astype(int)))
 if bid=='K06':return float(np.mean([np.mean([np.mean(p[groups==g]==y[groups==g]) for g in np.unique(groups[y==c])]) for c in (0,1)]))
 if bid=='M01':
  q=np.clip(p,1e-6,1-1e-6);loss=-(y*np.log(q)+(1-y)*np.log1p(-q))
  return float(np.mean([np.mean(loss[groups==g]) for g in np.unique(groups)]))
 raise ValueError('Unknown scorer')

def main():
 seal=json.loads((ROOT/'registry/request-seal.json').read_text());items={};attempts=[]
 for digest,entry in seal['requests'].items():
  path=ROOT/f'results/attempts/{digest}.json'
  if not path.exists():continue
  a=json.loads(path.read_text());a['output_valid']=False
  if a['status']=='response_saved':
   try:
    raw=ROOT/a['response_path'];assert hashlib.sha256(raw.read_bytes()).hexdigest()==a['response_sha256']
    values=parse_response(json.loads(raw.read_text()),entry)
    a['output_valid']=True
    key=(entry['benchmark_id'],entry['model'],entry['regime'])
    panel=items.setdefault(key,{})
    if set(values)&set(panel):raise ValueError('Overlapping batches')
    panel.update(values)
   except (ValueError,AssertionError,KeyError,TypeError) as exc:a['validation_error']=str(exc)
  attempts.append(a)
 summaries=[]
 for task in seal['task_records']:
  bid=task['benchmark_id'];data=OLD/f'data/cache/{bid}/data.npz'
  assert hashlib.sha256(data.read_bytes()).hexdigest()==task['source_data_sha256']
  # Scorer-only target access; never returned to the model API.
  with np.load(data,allow_pickle=False) as z:
   truth=z['test_y'];groups=z['test_groups'] if 'test_groups' in z.files else np.arange(len(truth))
  for model in seal['models']:
   panel=items.get((bid,model,task['regime']),{});ids=sorted(panel)
   full=ids==list(range(len(truth)))
   row=dict(benchmark_id=bid,model=model,regime=task['regime'],n_expected=len(truth),n_valid_predictions=len(ids),
    coverage=len(ids)/len(truth),complete=full,status='complete' if full else ('partial' if ids else 'not_measured'),
    metric=task['metric'],direction='lower' if bid=='M01' else 'higher',score=None,
    official_benchmark=False,specialist_current_best_verified=False)
   if full:
    p=np.array([panel[i] for i in ids]);row['score']=metric(bid,p,truth,groups)
    pred=ROOT/f'results/predictions/{bid}--{model}--{task["regime"]}.json'
    pred.parent.mkdir(exist_ok=True);pred.write_text(json.dumps(dict(row_ids=ids,predictions=p.tolist()),indent=2)+'\n')
    row['prediction_path']=str(pred.relative_to(ROOT));row['prediction_sha256']=hashlib.sha256(pred.read_bytes()).hexdigest()
   summaries.append(row)
 result=dict(paradigm='Direct inference; no tools, code generation, external model fitting or weight updates',
  n_complete_tasks=sum(all(r['complete'] for r in summaries if r['benchmark_id']==bid) for bid in sorted({r['benchmark_id'] for r in summaries})),
  attempts_dispatched=len(attempts),valid_response_batches=sum(a['output_valid'] for a in attempts),
  invalid_response_batches=sum(a['status']=='response_saved' and not a['output_valid'] for a in attempts),
  summaries=summaries,attempts=attempts)
 (ROOT/'results/summary.json').write_text(json.dumps(result,indent=2)+'\n')
 lines=['# Direct-inference results','',result['paradigm']+'.','',
  'Scores appear only for complete retained test sets. These are explicitly custom-protocol fallbacks. Partial requests are not completed benchmarks. No original code-generation result is used.', '',
  '| Task | Model | Condition | Valid predictions / test cases | Status | Native score |','|---|---|---|---|---|---|']
 for r in summaries:lines.append(f"| {r['benchmark_id']} | {r['model']} | {r['regime']} | {r['n_valid_predictions']} / {r['n_expected']} | {r['status']} | {r['score'] if r['score'] is not None else '—'} |")
 lines+=['','Specialist current-best matching is unresolved for these fallback contracts; no claim of superiority to field SOTA is made.','']
 (ROOT/'results/report.md').write_text('\n'.join(lines))
 print(json.dumps({k:result[k] for k in ['n_complete_tasks','attempts_dispatched','valid_response_batches','invalid_response_batches']}))

if __name__=='__main__':main()
