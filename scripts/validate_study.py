"""Verify routing, frozen payloads, output bounds and aggregate coverage."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from score import ROOT,parse_response
from score_extended import parse as tensor_parse
from score_images import decode


def rejected(fn,*args):
 try:fn(*args)
 except (ValueError,AssertionError,TypeError,KeyError):return True
 raise AssertionError('Malformed output was accepted')

def main():
 seal=json.loads((ROOT/'registry/request-seal.json').read_text());n=0
 for digest,e in seal['requests'].items():
  p=ROOT/e['request_path'];obj=json.loads(p.read_text());assert hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()==digest
  assert hashlib.sha256((ROOT/e['prompt_path']).read_bytes()).hexdigest()==e['prompt_sha256'];assert obj.get('store') is False and not obj.get('tools');n+=1
 sol={'gpt-5.6-sol','gpt-6.1-sol'}
 for p in (ROOT/'results/attempts').glob('*.json'):assert json.loads(p.read_text())['model'] not in sol
 for p in (ROOT/'results/raw').glob('*.json'):assert json.loads(p.read_text()).get('model') not in sol
 completed_harness=0
 for p in (ROOT/'results/codex-harness').glob('*.attempt.json'):
  a=json.loads(p.read_text());assert a['model'] in sol and a['transport']=='codex_harness_chatgpt'
  if a['status']=='response_saved':assert not a['tool_items'];completed_harness+=1
 summary=json.loads((ROOT/'results/primary-summary.json').read_text());bids={r['benchmark_id'] for r in summary['summaries']}
 assert len(bids)==11
 for bid in bids:
  rr=[r for r in summary['summaries'] if r['benchmark_id']==bid];assert len(rr)==4 and {r['model'] for r in rr}==set(seal['models'])
  for r in rr:
   assert r['transport']==('codex_harness_chatgpt' if r['model'] in sol else 'openai_api')
   assert (r['score'] is not None)==r['complete']
   if r['complete']:assert r['n_valid_predictions']==r['n_expected'] and np.isfinite(r['score'])
 assert sum(all(r['complete'] for r in summary['summaries'] if r['benchmark_id']==bid) for bid in bids)==10
 # Independent malformed-output fixtures: each exercises an actual parser boundary.
 entry=dict(benchmark_id='K01',start=0,stop=2)
 def response(p):return dict(status='completed',output=[dict(type='message',content=[dict(type='output_text',text=json.dumps(p))])])
 rejected(parse_response,response({'predictions':[{'id':0,'value':0},{'id':0,'value':1}]}),entry)
 rejected(parse_response,response({'predictions':[{'id':0,'value':0}]}),entry)
 te=dict(benchmark_id='D02',start=0,stop=1,prediction_shape=[2])
 rejected(tensor_parse,json.dumps({'predictions':[{'id':0,'value':[1]}]}),te)
 rejected(tensor_parse,json.dumps({'predictions':[{'id':0,'value':[True,1]}]}),te)
 rejected(tensor_parse,'{"predictions":[{"id":0,"value":[NaN,1]}]}',te)
 manifest={'records':[{'id':0,'width':3,'height':3,'crop_xyxy':[0,0,3,3]}],'source_shape':[1,2,3,3]}
 rejected(decode,json.dumps({'predictions':[{'id':0,'value':[{'points':[[0,0],[4,0],[0,1]]}]}]}),{'start':0},manifest)
 assert decode(json.dumps({'predictions':[{'id':0,'value':[{'points':[[0,0],[1,0],[0,1]]}]}]}),{'start':0},manifest).shape==(3,3)
 refs=json.loads((ROOT/'results/reference-validation.json').read_text());assert len(refs['references'])==11 and refs['all_rescored']
 usage=json.loads((ROOT/'results/api-usage.json').read_text());assert usage['spent_or_reserved_usd']<=20 and not usage['credential_persisted']
 # Scan deliverable text for accidental provider credentials without exposing any matches.
 paths=[p for d in ['results','registry','docs','scripts','experiments','analysis','web'] for p in (ROOT/d).rglob('*') if p.is_file() and 'prompts' not in p.parts and p.suffix not in ('.pyc','.npz')]
 patterns=(b'sk-'+b'proj-'+rb'[A-Za-z0-9_-]{24,}',b'sk-'+b'svcacct-'+rb'[A-Za-z0-9_-]{24,}')
 assert not any(any(re.search(pattern,p.read_bytes()) for pattern in patterns) for p in paths)
 result=dict(passed=True,sealed_payload_hashes_checked=n,completed_harness_batches_checked=completed_harness,negative_parser_fixtures=6,references_independently_rescored=11,admitted_tasks=11,complete_four_model_benchmarks=10,api_cost_upper_usd=usage['spent_or_reserved_usd'],sol_api_prediction_files=0,credential_prefix_matches=0)
 (ROOT/'results/validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
