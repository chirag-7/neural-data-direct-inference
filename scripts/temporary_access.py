"""Loopback credential intake; only sealed direct-prediction requests can leave."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import hashlib,json,secrets,threading,time,urllib.request,urllib.error,urllib.parse

ROOT=Path(__file__).resolve().parents[1]
NONCE=secrets.token_urlsafe(24)
PORT=8768
BASE='/'+NONCE
ORIGIN=f'http://127.0.0.1:{PORT}'
KEY=None
LIMIT=5.0
SPENT=0.0
ROWS=[]
DONE=set()
LOCK=threading.Lock()
MODELS={'gpt-4.1-2025-04-14':(2,8),'gpt-5-2025-08-07':(1.25,10),
        'gpt-5.6-sol':(4,20),'gpt-6.1-sol':(2,10)}

def persist():
 (ROOT/'results/api-usage.json').write_text(json.dumps(dict(new_study_ceiling_usd=LIMIT,
  spent_or_reserved_usd=SPENT,credential_persisted=False,requests=ROWS),indent=2)+'\n')

class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def send(self,status,data,html=False):
  raw=(data if isinstance(data,str) else json.dumps(data)).encode()
  self.send_response(status)
  for name,value in {'Content-Type':'text/html; charset=utf-8' if html else 'application/json',
   'Cache-Control':'no-store','Content-Security-Policy':"default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'",
   'X-Content-Type-Options':'nosniff','Content-Length':str(len(raw))}.items():self.send_header(name,value)
  self.end_headers();self.wfile.write(raw)
 def valid_host(self):return self.headers.get('Host')==f'127.0.0.1:{PORT}'
 def do_GET(self):
  if not self.valid_host():return self.send(403,{'error':'Invalid host'})
  if self.path==BASE+'/':
   return self.send(200,'''<!doctype html><title>Neural Data · direct inference access</title>
<style>body{font:18px system-ui;max-width:700px;margin:60px auto;padding:24px;color:#243746}input{display:block;width:94%;padding:14px;margin:16px 0}button{padding:12px 20px}</style>
<h1>Temporary direct-inference API access</h1><p>Enter the dedicated benchmark API key here, not in chat. This loopback-only process keeps it in memory and never writes it to files or logs.</p>
<p>Only frozen prediction requests to GPT-4.1, GPT-5, GPT-5.6 Sol and GPT-6.1 Sol are allowed. No tools, code execution or model training. This new run has a <b>$5 application spending ceiling</b>.</p>
<form method="post" action="credential"><label>Dedicated OpenAI API key<input type="password" name="api_key" autocomplete="off" required></label><button>Provide temporary access</button></form>''',True)
  if self.path==BASE+'/status':return self.send(200,dict(ready=KEY is not None,budget_usd=LIMIT,spent_or_reserved_usd=SPENT,requests=len(ROWS)))
  prefix=BASE+'/models/'
  if self.path.startswith(prefix) and self.path[len(prefix):] in MODELS:
   if not KEY:return self.send(409,{'error':'Temporary access is not ready'})
   return self.forward('GET','https://api.openai.com/v1/models/'+self.path[len(prefix):])
  return self.send(404,{'error':'Not found'})
 def do_POST(self):
  global KEY,SPENT
  if not self.valid_host():return self.send(403,{'error':'Invalid host'})
  length=int(self.headers.get('Content-Length','0'))
  if length>12000000:return self.send(413,{'error':'Request too large'})
  raw=self.rfile.read(length)
  if self.path==BASE+'/credential':
   if self.headers.get('Origin')!=ORIGIN:return self.send(403,{'error':'Invalid origin'})
   if KEY:return self.send(409,{'error':'Access already supplied'})
   key=urllib.parse.parse_qs(raw.decode()).get('api_key',[''])[0].strip()
   if not key.startswith('sk-') or len(key)<30:return self.send(400,{'error':'Expected an OpenAI API key'})
   KEY=key;return self.send(200,'<title>Access ready</title><h1>Temporary access is ready</h1><p>The credential remains in memory only. Return to Codex.</p>',True)
  if self.path!=BASE+'/responses':return self.send(404,{'error':'Not found'})
  if not KEY:return self.send(409,{'error':'Temporary access is not ready'})
  try:
   obj=json.loads(raw);model=obj['model'];rates=MODELS[model]
   digest=hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
   seal=json.loads((ROOT/'registry/request-seal.json').read_text())
   entry=seal['requests'][digest]
   assert obj.get('store') is False and not obj.get('tools')
   assert 0<obj['max_output_tokens']<=8192
   assert entry['model']==model and entry['regime'] in ('zero_shot','few_shot_8')
  except (ValueError,KeyError,AssertionError,FileNotFoundError):return self.send(400,{'error':'Request is not sealed direct inference'})
  reserve=(len(raw)*rates[0]+obj['max_output_tokens']*rates[1])/1000000
  with LOCK:
   if digest in DONE:return self.send(409,{'error':'Request already dispatched; no silent repeat'})
   if SPENT+reserve>LIMIT:return self.send(402,{'error':'Application spending ceiling reached'})
   SPENT+=reserve;DONE.add(digest)
   row=dict(request_sha256=digest,model=model,task=entry['benchmark_id'],regime=entry['regime'],
    reserved_max_usd=reserve,status='dispatched',time_unix=time.time())
   ROWS.append(row);persist()
  return self.forward('POST','https://api.openai.com/v1/responses',obj,row,rates,reserve)
 def forward(self,method,url,obj=None,row=None,rates=None,reserve=0):
  global SPENT
  req=urllib.request.Request(url,data=json.dumps(obj).encode() if obj else None,method=method,
   headers={'Authorization':'Bearer '+KEY,'Content-Type':'application/json'})
  try:
   with urllib.request.urlopen(req,timeout=300) as response:
    data=json.load(response);request_id=response.headers.get('x-request-id')
   if row is not None:
    usage=data.get('usage',{});cost=(usage.get('input_tokens',0)*rates[0]+usage.get('output_tokens',0)*rates[1])/1000000
    with LOCK:
     if 'input_tokens' in usage and 'output_tokens' in usage:SPENT+=cost-reserve
     row.update(status=data.get('status','received'),usage=usage,returned_model=data.get('model'),
      request_id=request_id,uncached_rate_cost_usd=cost);persist()
   return self.send(200,data)
  except urllib.error.HTTPError as exc:
   msg=exc.read().decode().replace(KEY,'[REDACTED]')
   if row is not None:
    with LOCK:
     row.update(status='http_error',http_status=exc.code,error=msg[:1500]);persist()
   return self.send(exc.code,{'error':msg[:1500]})
  except Exception as exc:
   if row is not None:
    with LOCK:
     row.update(status='transport_error',error=str(exc).replace(KEY,'[REDACTED]'));persist()
   return self.send(502,{'error':'Transport failed; reservation retained'})

if __name__=='__main__':
 print(ORIGIN+BASE+'/',flush=True)
 try:ThreadingHTTPServer(('127.0.0.1',PORT),Handler).serve_forever()
 finally:KEY=None
