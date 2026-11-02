"""Explicit technical recoveries chosen on validity, never accuracy."""
from pathlib import Path
import hashlib,json,shutil,time
ROOT=Path(__file__).resolve().parents[1]
def dump(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')

def main():
 path=ROOT/'registry/request-seal.json';seal=json.loads(path.read_text());new={};archived=0
 # Unbilled quota failures can retry the identical sealed request after credit restoration.
 # Every previous attempt remains in a separate audit directory.
 for p in list((ROOT/'results/attempts').glob('*.json')):
  a=json.loads(p.read_text())
  if a.get('http_status')==429 and ('credit_balance_exhausted' in a.get('error','') or 'insufficient_quota' in a.get('error','')):
   dest=ROOT/'results/api-attempt-history'/a['request_sha256'];dest.mkdir(parents=True,exist_ok=True)
   shutil.move(str(p),str(dest/f"quota-{int(time.time()*1000)}.json"));archived+=1
 # GPT5 M01: keep valid low-effort64 batches; split only missing/incomplete64 batches into16.
 for digest,e in list(seal['requests'].items()):
  if e['benchmark_id']!='M01' or e['model']!='gpt-5-2025-08-07' or e.get('model_configuration')!='low_reasoning_recovery':continue
  p=ROOT/f'results/attempts/{digest}.json';a=json.loads(p.read_text()) if p.exists() else None
  if a and a.get('response_status')=='completed':continue
  e['primary_include']=False;e['active']=False
  obj=json.loads((ROOT/e['request_path']).read_text());prefix,tail=obj['input'].rsplit('Test inputs: ',1);rows=json.loads(tail)
  for start in range(e['start'],e['stop'],16):
   stop=min(start+16,e['stop']);r=json.loads(json.dumps(obj));r['input']=prefix+'Test inputs: '+json.dumps([v for v in rows if start<=v['id']<stop],separators=(',',':'))
   r['text']['format']['schema']['properties']['predictions'].update(minItems=stop-start,maxItems=stop-start)
   sha=hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest();req=f'work/requests/{sha}.json';dump(ROOT/req,r);prompt=f'experiments/M01/prompts/zero_shot-low16-{start:05d}.txt';(ROOT/prompt).write_text(r['input'])
   new[sha]=dict(e,start=start,stop=stop,n_predictions=stop-start,primary_include=True,active=True,request_path=req,prompt_path=prompt,prompt_sha256=hashlib.sha256(r['input'].encode()).hexdigest(),model_configuration='low_reasoning_recovery_small_batch')
 # D02 GPT5 is rerun as a complete low-effort panel; never mix low/medium estimates.
 for digest,e in list(seal['requests'].items()):
  if e['benchmark_id']!='D02' or e['model']!='gpt-5-2025-08-07':continue
  if e.get('model_configuration')=='low_reasoning_recovery':continue
  e['primary_include']=False;e['active']=False
  obj=json.loads((ROOT/e['request_path']).read_text());obj['reasoning']={'effort':'low'}
  sha=hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest();req=f'work/requests/{sha}.json';dump(ROOT/req,obj)
  new[sha]=dict(e,primary_include=True,active=True,request_path=req,reasoning_effort='low',model_configuration='low_reasoning_recovery')
 seal['requests'].update(new);dump(path,seal)
 print(json.dumps(dict(archived_unbilled_quota_attempts=archived,new_recovery_requests=len(new))))

if __name__=='__main__':main()
