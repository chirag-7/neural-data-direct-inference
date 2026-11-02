"""Strict validation and native scoring of saved tensor predictions only."""
from pathlib import Path
import hashlib,importlib.util,json
import numpy as np
from score import ROOT,OLD


def parse(text,entry):
 obj=json.loads(text)
 if set(obj)!={'predictions'}:raise ValueError('Unexpected response keys')
 expected=list(range(entry['start'],entry['stop']));preds=obj['predictions']
 if [p.get('id') for p in preds]!=expected:raise ValueError('Missing/duplicate/reordered IDs')
 result={}
 for p in preds:
  if set(p)!={'id','value'}:raise ValueError('Unexpected prediction fields')
  # JSON bool is not a numeric prediction.
  def boolean(v):return isinstance(v,bool) or (isinstance(v,list) and any(boolean(x) for x in v))
  if boolean(p['value']):raise ValueError('Boolean prediction')
  a=np.asarray(p['value'],dtype=float)
  if list(a.shape)!=entry['prediction_shape'] or not np.isfinite(a).all():raise ValueError('Wrong shape or nonfinite prediction')
  if entry.get('nonnegative') and (a<0).any():raise ValueError('Negative expected count')
  bounds=entry.get('bounds')
  if bounds and ((a<bounds[0]).any() or (a>bounds[1]).any()):raise ValueError('Prediction outside bounds')
  if entry['benchmark_id']=='M04' and ((a<[.01,.1]).any() or (a>[.99,10]).any()):raise ValueError('Parameter outside allowed ranges')
  result[p['id']]=a
 return result


def native_score(bid,p,y):
 p=np.asarray(p,dtype=np.float64);y=np.asarray(y,dtype=np.float64)
 if bid=='D02':return float(np.sqrt(np.mean((p-y)**2)))
 if bid=='M04':return float(np.mean(np.abs(p-y)/[.98,9.9]))
 if bid=='B03':
  error=(p-p.mean(axis=1,keepdims=True))-(y-y.mean(axis=1,keepdims=True))
  return float(np.sqrt(np.mean(error**2,axis=1)).mean())
 if bid=='L04':
  from scipy.special import gammaln
  p=np.maximum(p.reshape(-1),1e-12);y=np.asarray(y).reshape(-1);ref=json.loads((OLD/'data/cache/L04/metadata.json').read_text())['train_null_mean']
  return float(np.sum((ref-y*np.log(ref)+gammaln(y+1))-(p-y*np.log(p)+gammaln(y+1)))/(y.sum()*np.log(2)))
 if bid=='C06':
  path=OLD/'experiments/C06/adapter.py';spec=importlib.util.spec_from_file_location('c06_native_scorer',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  return float(mod.score(p,y)['score'])
 if bid=='K05':
  path=OLD/'experiments/K05/adapter.py';spec=importlib.util.spec_from_file_location('k05_native_scorer',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  return float(mod.score(p,y)['score'])
 raise ValueError('Unknown native scorer')


def main():
 seal=json.loads((ROOT/'registry/request-seal.json').read_text());panels={};attempts=[]
 paths=list((ROOT/'results/attempts').glob('*.json'))+list((ROOT/'results/codex-harness').glob('*.attempt.json'))
 for path in paths:
  a=json.loads(path.read_text())
  if a.get('output_kind')!='tensor':continue
  a['output_valid']=False
  if a['status']=='response_saved':
   try:
    harness=a.get('transport')=='codex_harness_chatgpt'
    if harness:
     assert not a['tool_items'];p=ROOT/a['prediction_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==a['prediction_sha256'];text=p.read_text()
    else:
     assert a['model'] in ('gpt-4.1-2025-04-14','gpt-5-2025-08-07')
     p=ROOT/a['response_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==a['response_sha256'];raw=json.loads(p.read_text())
     if raw.get('status')!='completed':raise ValueError('Response incomplete')
     text=''.join(c.get('text','') for o in raw.get('output',[]) if o.get('type')=='message' for c in o.get('content',[]) if c.get('type')=='output_text')
    values=parse(text,a);a['output_valid']=True
    if seal['requests'].get(a['request_sha256'],{}).get('primary_include',True):
     key=(a['benchmark_id'],a['model'],a['regime']);panel=panels.setdefault(key,{})
     if set(values)&set(panel):raise ValueError('Overlapping batches')
     panel.update(values)
    else:a['primary_excluded']=True
   except (ValueError,TypeError,KeyError,AssertionError) as exc:a['validation_error']=str(exc)
  attempts.append(a)
 summaries=[]
 for task in seal['task_records']:
  if task.get('output_kind')!='tensor':continue
  bid=task['benchmark_id'];manifest=json.loads((ROOT/f'experiments/{bid}/input-manifest.json').read_text());data=Path(manifest['source_data_path']);assert hashlib.sha256(data.read_bytes()).hexdigest()==task['source_data_sha256']
  for model in seal['models']:
   panel=panels.get((bid,model,task['regime']),{});ids=sorted(panel);complete=ids==list(range(task['n_prediction_records']))
   row=dict(reasoning_effort='none' if model.startswith('gpt-4') else ' + '.join(sorted({e.get('reasoning_effort','medium') for e in seal['requests'].values() if e['benchmark_id']==bid and e['model']==model and e['regime']==task['regime'] and e.get('primary_include',True)})),benchmark_id=bid,model=model,transport='codex_harness_chatgpt' if model in ('gpt-5.6-sol','gpt-6.1-sol') else 'openai_api',regime=task['regime'],n_expected=task['n_prediction_records'],n_valid_predictions=len(ids),complete=complete,metric=task['metric'],direction=task['direction'],score=None,n_test_cases=task['n_test'],official_benchmark=False)
   if not complete and bid=='C06':row['unavailable_reason']='Dense output truncation; further recovery deferred under the remaining study budget.' if model=='gpt-5-2025-08-07' else 'One recording timed out at600seconds with both medium and low reasoning; no full-panel score.'
   if complete:
    p=np.stack([panel[i] for i in ids])
    if bid=='D02':p=p.reshape(task['n_test'],500)
    # Test targets accessed only here, after complete predictions are persisted.
    with np.load(data,allow_pickle=False) as z:y=z['truth'] if bid=='M04' else z['test_y']
    row['score']=native_score(bid,p,y)
    pred=ROOT/f'results/predictions/{bid}--{model}--{task['regime']}.json';pred.parent.mkdir(exist_ok=True);pred.write_text(json.dumps(dict(predictions=p.tolist()))+'\n');row['prediction_path']=str(pred.relative_to(ROOT));row['prediction_sha256']=hashlib.sha256(pred.read_bytes()).hexdigest()
   summaries.append(row)
 result=dict(summaries=summaries,attempts=attempts)
 (ROOT/'results/extended-summary.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(valid_batches=sum(a['output_valid'] for a in attempts),attempted_batches=len(attempts),complete_panels=sum(r['complete'] for r in summaries),failures=[dict(task=a['benchmark_id'],model=a['model'],start=a['start'],reason=a.get('validation_error',a['status'])) for a in attempts if a['status']!='dispatched' and not a['output_valid'] ])))

if __name__=='__main__':main()
