"""Decode direct polygons with fixed geometry; score against all five experts."""
from pathlib import Path
import hashlib,importlib.util,json
import numpy as np
from PIL import Image,ImageDraw
from score import ROOT,OLD

def decode(text,entry,manifest):
 obj=json.loads(text)
 if set(obj)!={'predictions'} or len(obj['predictions'])!=1:raise ValueError('Expected one prediction')
 p=obj['predictions'][0]
 if set(p)!={'id','value'} or p['id']!=entry['start']:raise ValueError('Wrong image ID or fields')
 rec=manifest['records'][p['id']];w,h=rec['width'],rec['height'];canvas=Image.new('I',(w,h),0);draw=ImageDraw.Draw(canvas)
 for idx,poly in enumerate(p['value'],1):
  if set(poly)!={'points'} or len(poly['points'])<3:raise ValueError('Invalid polygon')
  pts=poly['points']
  for point in pts:
   if len(point)!=2 or any(isinstance(v,bool) or not isinstance(v,int) for v in point):raise ValueError('Noninteger coordinates')
   if not (0<=point[0]<w and 0<=point[1]<h):raise ValueError('Coordinate outside image')
  draw.polygon([tuple(x) for x in pts],fill=idx)
 full=np.zeros(manifest['source_shape'][2:],dtype=np.int32);x0,y0,x1,y1=rec['crop_xyxy'];full[y0:y1,x0:x1]=np.asarray(canvas)
 return full

def main():
 seal=json.loads((ROOT/'registry/request-seal.json').read_text());manifest=json.loads((ROOT/'experiments/J08/input-manifest.json').read_text());panels={};attempts=[]
 for path in list((ROOT/'results/attempts').glob('*.json'))+list((ROOT/'results/codex-harness').glob('*.attempt.json')):
  a=json.loads(path.read_text())
  if a.get('output_kind')!='polygons':continue
  a['output_valid']=False
  if a['status']=='response_saved':
   try:
    if a.get('transport')=='codex_harness_chatgpt':
     assert not a['tool_items'];p=ROOT/a['prediction_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==a['prediction_sha256'];text=p.read_text()
    else:
     p=ROOT/a['response_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==a['response_sha256'];raw=json.loads(p.read_text())
     if raw.get('status')!='completed':raise ValueError('Incomplete response')
     text=''.join(c.get('text','') for o in raw.get('output',[]) if o.get('type')=='message' for c in o.get('content',[]) if c.get('type')=='output_text')
    decoded=decode(text,a,manifest);panels.setdefault(a['model'],{})[a['start']]=decoded;a['output_valid']=True
   except (ValueError,KeyError,TypeError,AssertionError) as exc:a['validation_error']=str(exc)
  attempts.append(a)
 rows=[];data=OLD/'data/cache/J08/data.npz';assert hashlib.sha256(data.read_bytes()).hexdigest()==manifest['source_data_sha256']
 for model in seal['models']:
  panel=panels.get(model,{});full=set(panel)=={0,1};row=dict(benchmark_id='J08',model=model,transport='codex_harness_chatgpt' if model in ('gpt-5.6-sol','gpt-6.1-sol') else 'openai_api',n_expected=2,n_valid_predictions=len(panel),complete=full,regime='zero_shot',reasoning_effort='low' if model=='gpt-5-2025-08-07' else ('none' if model.startswith('gpt-4') else 'medium'),metric='equal_image_rater_object_f1_iou_0.5',direction='higher',score=None,official_benchmark=False)
  if full:
   # Expert targets loaded only after all predictions have been saved.
   with np.load(data,allow_pickle=False) as z:y=z['test_y']
   path=OLD/'experiments/J08/adapter.py';spec=importlib.util.spec_from_file_location('j08_native_scorer',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
   pred=np.stack([panel[i] for i in range(2)]);row['score']=float(mod.score(pred,y));out=ROOT/f'results/predictions/J08--{model}--zero_shot.npz';np.savez_compressed(out,predictions=pred);row['prediction_path']=str(out.relative_to(ROOT));row['prediction_sha256']=hashlib.sha256(out.read_bytes()).hexdigest()
  rows.append(row)
 (ROOT/'results/image-summary.json').write_text(json.dumps(dict(summaries=rows,attempts=attempts),indent=2)+'\n')
 print(json.dumps(dict(valid_batches=sum(a['output_valid'] for a in attempts),complete_panels=sum(r['complete'] for r in rows),failures=[dict(model=a['model'],start=a['start'],reason=a.get('validation_error',a['status'])) for a in attempts if a['status']!='dispatched' and not a['output_valid']])))

if __name__=='__main__':main()
