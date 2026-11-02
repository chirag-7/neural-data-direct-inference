"""Publish only aggregate, audited predictions; no source feature rows or credentials."""
from pathlib import Path
import hashlib,json,shutil
from collections import defaultdict
import numpy as np
from score import ROOT,OLD,metric
from score_extended import native_score

LABELS={
 'B03':('Rigid ephys drift','Extracellular data','Spatial count raster','Motion RMSE (µm)','4 simulated recordings','Signal recovery'),
 'C06':('Calcium → expected spikes','Calcium imaging','Signal / time series','Animal-mean Pearson r','24 recording rows, grouped by neuron and animal','Signal recovery'),
 'D02':('Current → voltage','Voltage & intracellular','Signal / time series','Voltage RMSE (mV)','2 held-out sweeps;10 output chunks','Regression'),
 'I10':('MRI scan quality','Neuroimaging','Numeric feature table','Balanced accuracy','265 scans','Classification'),
 'J08':('Synaptic puncta segmentation','Anatomy & microscopy','Microscopy image','Object F1 at IoU ≥0.5','2 images ×5 expert raters','Segmentation'),
 'K01':('Dendritic morphology class','Cell & molecular data','Numeric feature table','Macro F1','457 cells','Classification'),
 'K05':('Cellular fraction estimation','Cell & molecular data','Numeric feature table','Donor/block macro RMSE','24 held-out bulk samples, grouped by donor/block','Regression'),
 'K06':('Optotagged PV / SST class','Cell & molecular data','Signal / time series','Class-balanced mouse accuracy','71 cells, grouped by mouse','Classification'),
 'L04':('Place-cell spike counts','Statistical inference','Numeric feature table','Bits per spike vs training mean','3,506 time bins from one neuron','Probabilistic prediction'),
 'M01':('Mouse choice probability','Cognition & control','Numeric feature table','Mouse-mean binary log loss','1,842 held-out choices','Probabilistic prediction'),
 'M04':('Q-learning parameter recovery','Cognition & control','Signal / time series','Range-normalized parameter MAE','24 simulated agents','Parameter estimation'),
}
REF_NAMES={'B03':'SpikeInterface raster registration','C06':'OASIS AR(1), calibrated','D02':'Training-selected passive response','I10':'Trained random forest','J08':'SynAPSeg StarDist archived masks','K01':'Trained morphology classifier','K05':'Donor-aware ridge regression','K06':'Training-selected SVM / ExtraTrees','L04':'Task-specific Poisson GLM','M01':'Task-specific behavioral GLM','M04':'Exact-likelihood posterior median'}

def main():
 primary=json.loads((ROOT/'results/primary-summary.json').read_text())['summaries'];front=json.loads((OLD/'analysis/specialist-frontier-v1/comparison.json').read_text());by={t['benchmark_id']:t for t in front['tasks']};tasks=[];refs=[]
 for bid,meta in LABELS.items():
  manifest=json.loads((ROOT/f'experiments/{bid}/input-manifest.json').read_text());path=OLD/('data/cache/cognitive-v1.npz' if bid=='M04' else f'data/cache/{bid}/data.npz');assert hashlib.sha256(path.read_bytes()).hexdigest()==manifest['source_data_sha256']
  ref=by[bid].get('best_available_reference');reference=None
  if ref:
   records=json.loads((OLD/f'results/{bid}.json').read_text());records=records if isinstance(records,list) else records.get('records',[])
   found=next((r for r in records if r.get('model') in ref['methods'] and r.get('prediction_file')),None)
   if found:
    predpath=OLD/found['prediction_file']
    with np.load(predpath,allow_pickle=False) as z:
     keys=z.files;pred=z['predictions'] if 'predictions' in keys else z[keys[0]]
    with np.load(path,allow_pickle=False) as z:
     y=z['truth'] if bid=='M04' else z['test_y'];groups=z['test_groups'] if 'test_groups' in z.files else np.arange(len(y))
    if bid in ['K01','K06','I10','M01']:value=metric(bid,pred,y,groups)
    elif bid=='J08':
     import importlib.util
     spec=importlib.util.spec_from_file_location('j08_reference',OLD/'experiments/J08/adapter.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);value=mod.score(pred,y)
    else:value=native_score(bid,pred,y)
    assert np.isclose(value,ref['score'],rtol=1e-7,atol=1e-7),(bid,value,ref['score'])
    reference=dict(name=REF_NAMES[bid],score=float(value),kind='Archived specialist masks' if bid=='J08' else 'Local task-specific reference',current_best_verified=False,recorded_score=ref['score'],recomputed_score=float(value),prediction_sha256=hashlib.sha256(predpath.read_bytes()).hexdigest(),reference_type=found.get('reference_type'),source=f'https://github.com/chirag-7/neural-data-bench/tree/main/experiments/{bid}',source_prediction_file=found['prediction_file'],comparison_limit='Same retained test cases and native scorer; specialist training/calibration differs. Not a certified current-best published score.'+(' Direct models receive8bit PNG and return polygons; archived specialist used original image inputs.' if bid=='J08' else ''))
    refs.append(dict(benchmark_id=bid,**reference))
  scores=[r for r in primary if r['benchmark_id']==bid]
  notes=[]
  if bid=='C06':notes.append('Timed-out Sol requests use separately recorded low-effort recovery with the same data and output schema; other Sol requests retain medium reasoning.')
  if bid=='C06':notes.append('GPT-6.1 Sol is incomplete:one recording timed out at600seconds in both medium and low-effort requests; its23/24 valid rows receive no full-panel score.')
  if bid=='C06':notes.append('GPT-5 is incomplete: dense output truncation followed by the study API budget limit. Its partial predictions are not assigned a score.')
  if bid=='D02':notes.append('Zero-shot input omits cell-specific calibration; membrane parameters cannot be uniquely identified. GPT-5 uses a complete low-reasoning recovery panel.')
  if bid=='M01':notes.append('GPT-5 uses low reasoning after medium-reasoning truncation. Successful low batches64 and recovery batches16 are combined without overlap; no accuracy feedback selected repairs.')
  if bid=='L04':notes.append('Separately labeled in-context condition:64 fixed, uniformly spaced training examples. All reasoning models use low effort. Reference GLM uses all training bins; comparison is not equal-data or equal-training.')
  if bid=='K05':notes.append('Zero-shot: no paired cellular-fraction calibration or single-cell reference atlas is supplied.')
  if bid=='J08':notes.append('Only 2 retained fields; five experts are repeated annotations of each field, not ten independent biological samples. Inputs are explicitly quantized8bit; model polygons use a fixed geometry decoder.')
  if bid in ['B03','M04']:notes.append('Fully synthetic diagnostic; this does not establish biological generalization.')
  tasks.append(dict(id=bid,title=meta[0],category=meta[1],input=meta[2],metric_label=meta[3],test_units=meta[4],operation=meta[5],condition='64 in-context examples' if bid=='L04' else 'Zero-shot',rows=scores,complete_all_four=len(scores)==4 and all(r['complete'] for r in scores),reference=reference,notes=notes,source=f'https://github.com/chirag-7/neural-data-direct-inference/tree/main/experiments/{bid}',manifest={k:v for k,v in manifest.items() if k in ('source_data_sha256','test_shape','source_shape','n_test','n_prediction_records','numeric_serialization','input_transform','output_transform','protocol_status','protocol')}))
 audit=json.loads((ROOT/'registry/feasibility-audit.json').read_text());usage=json.loads((ROOT/'results/api-usage.json').read_text())
 # Spending is a conservative uncached/cache-write upper bound, not a billing statement.
 data=dict(title='Neural Data · Direct Inference',revision='pilot-11-tasks',models=['gpt-4.1-2025-04-14','gpt-5-2025-08-07','gpt-5.6-sol','gpt-6.1-sol'],tasks=tasks,api_cost_upper_usd=usage['spent_or_reserved_usd'],api_cap_usd=20,audit=[dict(id=r['benchmark_id'],title=r['title'],assessment=r['assessment'],reason=r.get('reason',''),input_projection_usd=r.get('input_only_two_api_models_cost_projection_usd')) for r in audit['rows'] if r['benchmark_id'] not in LABELS],caveats=['These are retained custom protocols, not30 restored official benchmarks.','Sol models use the Codex harness; GPT-4.1/GPT-5 use API. Transport, instructions and some reasoning budgets differ.','No model-generated solver, external fitting, tool calls or weight updates are used in direct inference. L04 has fixed in-context examples.','Complete-case comparisons exclude the calcium task with missing model outputs; completion and survivorship bias must be considered separately.','One prediction run per final configuration; no claim of a scaling law, statistical equivalence or broad population-level superiority.','References are verified local/archived comparisons, not certified latest specialist SOTA.'])
 out=ROOT/'web';out.mkdir(parents=True,exist_ok=True);(out/'data.json').write_text(json.dumps(data,ensure_ascii=False,allow_nan=False)+'\n')
 # Recompute compatible explorer analyses before mirroring the published source.
 import runpy
 runpy.run_path(str(ROOT/'scripts/build_explorer_analysis.py'),run_name='__main__')
 shutil.copytree(out,ROOT/'website/dist',dirs_exist_ok=True)
 (ROOT/'results/reference-validation.json').write_text(json.dumps(dict(references=refs,all_rescored=True,roundtrip_tolerance='1e-7 absolute/relative for archived float32 prediction roundtrips; recomputed values are displayed',no_old_general_scores_imported=True),indent=2)+'\n')
 print(json.dumps(dict(tasks=len(tasks),complete_all_four=sum(t['complete_all_four'] for t in tasks),complete_model_panels=sum(r['complete'] for t in tasks for r in t['rows']),references_rescored=len(refs))))

if __name__=='__main__':main()
