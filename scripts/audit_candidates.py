"""Input-only resource audit. Projections are not empirical capability results."""
from pathlib import Path
import csv,hashlib,json,zipfile
import numpy as np
import tiktoken
from prepare import ROOT,OLD,clean,dump

enc=tiktoken.get_encoding('o200k_base')

def headers(path):
 result={}
 with zipfile.ZipFile(path) as z:
  for name in z.namelist():
   with z.open(name) as f:
    version=np.lib.format.read_magic(f)
    shape,order,dtype=(np.lib.format.read_array_header_1_0(f) if version==(1,0) else np.lib.format.read_array_header_2_0(f))
    result[name.removesuffix('.npy')]=dict(shape=list(shape),dtype=str(dtype))
 return result

def main():
 tasks=json.loads((ROOT/'registry/tasks.json').read_text())['tasks'];rows=[]
 for task in tasks:
  bid=task['benchmark_id'];p=OLD/f'data/cache/{bid}/data.npz';row=dict(benchmark_id=bid,title=task['title'],category=task['category'],data_available=False,assessment='pending_adapter',is_model_capability_failure=False)
  if bid=='M04':p=OLD/'data/cache/cognitive-v1.npz'
  if p.exists():
   h=headers(p);row.update(data_available=True,source_data_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),array_headers=h)
   if 'test_x' in h:
    shape=h['test_x']['shape'];row['n_test_cases']=shape[0]
    with np.load(p,allow_pickle=False) as z:
     x=z['test_x'];ids=np.unique(np.linspace(0,len(x)-1,min(5,len(x)),dtype=int));counts=[]
     for i in ids:
      text=json.dumps(clean(x[i].tolist()),separators=(',',':'),allow_nan=False);counts.append(len(enc.encode(text)))
    row.update(tokenizer='o200k_base; exact for this serialization on sampled cases, approximate for Sol6.1',sampled_case_indices=ids.tolist(),sampled_input_tokens=counts,projected_full_test_input_tokens=float(np.mean(counts)*shape[0]),input_only_two_api_models_cost_projection_usd=float(np.mean(counts)*shape[0]*3.25/1e6),projection_excludes='Task instructions, metadata, JSON wrapper, output/reasoning, retries, cache-write and long-context surcharges. This is a projection from deterministic input-only samples, not a proven lower bound.')
  if bid in ['K01','K06','I10','M01','B03','D02','M04','K05','C06','L04','J08']:row.update(assessment='execution_admitted',reason='Frozen full retained-test requests; actual execution status is in primary-summary.json.')
  elif bid in ['A09','A14','G01','H01','H02','H16','I07','K04','F04','E06','E01']:
   row.update(assessment='deferred_full_panel_resource_budget',reason='The sampled full-test numeric-input projection exceeds the remaining shared API budget or leaves insufficient room for required outputs/reasoning. Not a measured model failure. Subsampling/feature extraction/streaming could define a future separately frozen protocol; no partial score will be labeled full-test.')
  elif bid=='C06':row.update(assessment='candidate_dense_output',reason='24 native calcium recordings are manageable inputs, but each requires900 direct output numbers; requires output-format feasibility and budget check.')
  elif bid=='L04':row.update(assessment='candidate_calibration_needed',reason='A neuron-specific place field is not identifiable from position/velocity alone without labeled calibration. A future fixed in-context calibration condition can be specified; this is not inability to read numeric input.')
  elif bid=='H08':row.update(assessment='deferred_context_and_full_panel_budget',reason='Each retained night has1440x3000 raw EEG samples. A whole-night numeric prompt exceeds context; epoch/window processing changes available context and requires a separately frozen protocol and budget.')
  elif bid=='A15':row.update(assessment='deferred_native_audio_interface',reason='The selected text/image model interfaces do not accept native audio. A spectrogram or waveform-text variant is possible but is a changed input protocol; full numeric-waveform context/cost is prohibitive for this budget.')
  elif bid=='B01':
   inp=OLD/'data/cache/B01/inputs.npz';row.update(data_available=inp.exists(),assessment='deferred_whole_recording_context',reason='The retained voltage matrix has320000x32 samples (10.24million values). A full-recording numeric prompt exceeds context. Chunked spike sorting also requires cross-chunk unit-identity reconciliation, a different protocol not silently substituted.')
   if inp.exists():row['array_headers']=headers(inp)
  elif bid=='B07':
   chunks=list((OLD/'data/cache/B07').glob('**/chunk.raw'));row.update(data_available=bool(chunks),n_recordings=len(chunks),bytes_per_recording=chunks[0].stat().st_size if chunks else None,assessment='deferred_direct_bitstream_resources',reason='Each input chunk is4096x384 int16 samples. Direct compression requires a verifiable lossless encoded bitstream, not model-written codec code. Full input/output resources exceed this bounded study; no compression score is inferred from a textual codec description.')
  elif bid=='B08':
   chunks=list((OLD/'data/cache/B08').glob('*.npz'));row.update(data_available=bool(chunks),n_recordings=len(chunks),array_headers=headers(chunks[0]) if chunks else None,assessment='deferred_direct_bitstream_resources',reason='Seven full event streams contain about1.05million events. Exact reconstruction/timing validation needs actual bitstreams and the declared decoder; no codec-generating program will be substituted. A streaming protocol is future work.')
  elif bid=='L06':row.update(assessment='deferred_dense_posterior_output',reason='The retained scoring protocol requests10000 ten-dimensional posterior draws for each of10 observations:1million output scalars. Direct full posterior output exceeds the selected response budget. A posterior mean/covariance or generated sampler would be a different task; no sampler program is substituted.')
  elif bid=='N05':row.update(data_available=(OLD/'data/cache/N05/metadata.json').exists(),assessment='incompatible_native_binary_interface',reason='The task is reading a binary NWB file. The chosen inference interface accepts text/images and forbids tools. Having a loader extract fields for the model would perform the task for it. A schema/text question variant would be a new task.')
  elif bid=='C05':
   files=list((OLD/'data/cache/spikefinder').glob('*.test.calcium.csv'));shapes=[]
   for f in files:
    with f.open() as stream:
     reader=csv.reader(stream);header=next(reader);n=sum(1 for _ in reader)
    shapes.append(dict(file=f.name,n_rows=n,n_csv_columns=len(header)))
   row.update(data_available=bool(files),input_csv_shapes=shapes,assessment='deferred_full_trace_output_budget',reason='The five retained preparations require framewise expected-spike outputs for every valid calcium trace. Native full traces/output panels exceed this study budget. Windowing or a prospectively fixed subset is possible, but is not the same full benchmark.')
  elif bid=='J08':row.update(assessment='candidate_image_output_adapter',reason='All four model families can receive images. Two images can be attempted with direct polygon-mask outputs; a deterministic geometry rasterizer is permitted scoring infrastructure, not a model-generated solver. A valid image adapter must preserve field dimensions and all five expert scorers.')
  row['source_leads']=task.get('candidate_sources',[]);rows.append(row)
 dump(ROOT/'registry/feasibility-audit.json',dict(scope='30 inherited candidates; resource/interface audit, not a survey of all neuroscience or model incapability test',token_estimates_use_no_test_targets=True,rows=rows))
 lines=['# Full-panel feasibility audit','', 'These dispositions describe the current frozen interface and $20 cumulative API budget. Resource deferral is not a measured model failure. Input-only projections omit outputs, reasoning and overhead; estimates are not proven bounds. Candidate official-source links remain leads, not verified matching SOTA results.','', '| Task | Assessment | Input-only API projection (both older models) | Reason |','|---|---|---|---|']
 for r in rows:lines.append(f"| {r['benchmark_id']} | {r['assessment']} | {r.get('input_only_two_api_models_cost_projection_usd','—')} | {r.get('reason','')} |")
 (ROOT/'docs/feasibility-audit.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps([dict(task=r['benchmark_id'],assessment=r['assessment'],input_projection_usd=round(r.get('input_only_two_api_models_cost_projection_usd',0),2)) for r in rows]))

if __name__=='__main__':main()
