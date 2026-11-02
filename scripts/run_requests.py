"""Send pre-sealed direct prediction requests, never execute returned text."""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,time,urllib.request,urllib.error,threading
ROOT=Path(__file__).resolve().parents[1]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--bridge',required=True);ap.add_argument('--tasks',nargs='+');ap.add_argument('--regime',default='zero_shot')
 ap.add_argument('--limit',type=int);ap.add_argument('--workers',type=int,default=4);args=ap.parse_args()
 seal=json.loads((ROOT/'registry/request-seal.json').read_text());rank={m:i for i,m in enumerate(seal['models'])}
 requests=[(sha,r) for sha,r in seal['requests'].items() if (not args.tasks or r['benchmark_id'] in args.tasks) and r['regime']==args.regime]
 requests.sort(key=lambda x:(args.tasks.index(x[1]['benchmark_id']) if args.tasks else x[1]['benchmark_id'],x[1]['start'],rank[x[1]['model']]))
 requests=[(s,r) for s,r in requests if not (ROOT/f'results/attempts/{s}.json').exists()]
 if args.limit:requests=requests[:args.limit]
 (ROOT/'results/attempts').mkdir(parents=True,exist_ok=True);(ROOT/'results/raw').mkdir(exist_ok=True)
 rates={'gpt-4.1-2025-04-14':(2,8),'gpt-5-2025-08-07':(1.25,10),'gpt-5.6-sol':(4,20),'gpt-6.1-sol':(2,10)}
 # Upper bound treats every input token as a 1.25x cache write, even when cheaper.
 # Includes already dispatched attempts from previous invocations and in-flight reserves.
 budget={'usd':0.0};lock=threading.Lock()
 for apath in (ROOT/'results/attempts').glob('*.json'):
  old=json.loads(apath.read_text());ir,orr=rates[old['model']]
  if old.get('usage'):
   u=old['usage'];budget['usd']+=(1.25*u['input_tokens']*ir+u['output_tokens']*orr)/1e6
  elif old['status'] not in ('budget_deferred',):budget['usd']+=old.get('conservative_reservation_usd',0)
 def send(item):
  digest,entry=item;request_file=ROOT/entry['request_path'];obj=json.loads(request_file.read_text())
  assert hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()==digest
  ir,orr=rates[entry['model']]
  reservation=(1.25*len(json.dumps(obj).encode())*ir+obj['max_output_tokens']*orr)/1e6
  with lock:
   if budget['usd']+reservation>5.0:
    print(json.dumps(dict(benchmark_id=entry['benchmark_id'],model=entry['model'],status='budget_deferred')),flush=True)
    return dict(status='budget_deferred')
   budget['usd']+=reservation
  record=dict(**entry,request_sha256=digest,status='dispatched',started_unix=time.time())
  record['conservative_reservation_usd']=reservation
  path=ROOT/f'results/attempts/{digest}.json';path.write_text(json.dumps(record,indent=2)+'\n')
  try:
   req=urllib.request.Request(args.bridge.rstrip('/')+'/responses',data=json.dumps(obj).encode(),headers={'Content-Type':'application/json'},method='POST')
   with urllib.request.urlopen(req,timeout=330) as r:data=json.load(r)
   raw=ROOT/f'results/raw/{digest}.json';raw.write_text(json.dumps(data,indent=2)+'\n')
   record.update(status='response_saved',response_status=data.get('status'),returned_model=data.get('model'),
    response_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),response_path=str(raw.relative_to(ROOT)),usage=data.get('usage'))
   u=data.get('usage',{})
   if 'input_tokens' in u and 'output_tokens' in u:
    actual_upper=(1.25*u['input_tokens']*ir+u['output_tokens']*orr)/1e6
    with lock:budget['usd']+=actual_upper-reservation
  except urllib.error.HTTPError as exc:
   record.update(status='http_error',http_status=exc.code,error=exc.read().decode()[:2000])
  except Exception as exc:record.update(status='transport_error',error=str(exc))
  record['elapsed_seconds']=time.time()-record['started_unix'];path.write_text(json.dumps(record,indent=2)+'\n')
  print(json.dumps({k:record.get(k) for k in ['benchmark_id','model','start','stop','status','response_status','http_status','elapsed_seconds']}),flush=True)
  return record
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
  results=list(pool.map(send,requests))
 print(json.dumps(dict(dispatched=sum(r['status']!='budget_deferred' for r in results),responses_saved=sum(r['status']=='response_saved' for r in results),conservative_cost_upper_usd=budget['usd'])),flush=True)

if __name__=='__main__':main()
