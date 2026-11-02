from pathlib import Path
import json, shutil, statistics, itertools, csv, hashlib
root=Path(__file__).resolve().parents[1]; old=root/'registry/explorer-metadata'; web=root/'web'
d=json.loads((web/'data.json').read_text()); canonical=json.loads((root/'results/primary-summary.json').read_text())['summaries'];
for task in d['tasks']:
 for row in task['rows']:
  actual=next(r for r in canonical if r['benchmark_id']==row['benchmark_id'] and r['model']==row['model'])
  assert actual['score']==row['score'], 'Site score differs from canonical result'
 models=d['models']; tasks=d['tasks']; complete=[t for t in tasks if t['complete_all_four']]
def dump(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def writecsv(p,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows([{k:json.dumps(v) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in rows])
# Original frontend data stays the single source of task metadata; scores originate in primary-summary.
dump(web/'data/direct-inference.json',d)
facets=json.loads((old/'task-facets.json').read_text());facets['assignments']=[a for a in facets['assignments'] if a['benchmark_id'] in {t['id'] for t in tasks}]
for a in facets['assignments']:
 a['scope']='executed';a['evidence']=[{'path':'experiments/'+a['benchmark_id']+'/run-report.md'}]
 p=root/'docs/task-classification'/f"{a['benchmark_id']}.md";p.parent.mkdir(parents=True,exist_ok=True);p.write_text('# '+a['benchmark_id']+' classification\n\n'+a['rationale']+'\n\n'+json.dumps({k:a[k] for k in ['input_type','operation','generalization']},indent=2)+'\n\nSee the [run report](../../experiments/'+a['benchmark_id']+'/run-report.md). Labels describe the protocol, not a measured claim of out-of-distribution robustness.\n')
(root/'docs/task-classification/README.md').write_text('# Task filters\n\nInput data type describes what the model receives. Analysis task describes the requested transformation. Generalization setting describes the evaluation boundary (for example held-out animals), not whether the model successfully generalizes. These labels carry over from the retained task contracts, reviewed for direct inference; each task has its own rationale. Auxiliary identifiers do not create a second modality. Filters intersect; small subset counts are descriptive.\n')
dump(web/'data/task-facets.json',facets)
catold=json.loads((old/'catalog.json').read_text()); entries=[];records=[]
for t in tasks:
 e=next(e.copy() for e in catold['entries'] if e['id']==t['id']);e.update(task=t['title'],executed_slice=t['test_units'],data=t['input'],limitations=' '.join(t['notes']),resource=t['input']);entries.append(e)
 for row in t['rows']:records.append(dict(row,slice_id='Full retained test',status='ok' if row.get('complete') else 'incomplete',not_scored_reason=f"Incomplete predictions: {row.get('n_valid_predictions',0)} / {row.get('n_expected',0)}; no full-test score"))
 r=t['reference']; records.append(dict(benchmark_id=t['id'],model='reference-'+t['id'],display_name=r['name'],score=r['score'],slice_id='Full retained test',status='ok',metric=t['rows'][0]['metric'],direction=t['rows'][0]['direction'],display_reference_class='historical_specialist' if t['id']=='J08' else 'local_specialist' if t['id'] in ['B03','C06'] else 'conventional_reference',reference_type=r['reference_type']))
fams=[f for f in catold['families'] if f['code'] in {t['id'][0] for t in tasks}]
dump(web/'data/catalog.json',{'entries':entries,'families':fams})
dump(web/'data/summary.json',dict(measured_tasks=11,measured_families=8,model_attempts=44,models=models,reference_envelopes=[{'benchmark_id':t['id'],'slice_id':'Full retained test','model':'reference-'+t['id']} for t in tasks]))
(web/'data/measurements.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records));shutil.copyfile(web/'data/measurements.jsonl',web/'data/comparison-measurements.jsonl')
writecsv(web/'data/measurements.csv',[{k:r.get(k) for k in ['benchmark_id','model','score','metric','direction','status','transport']} for r in records])
def raw(delta):return 'numerical_tie' if abs(delta)<=1e-9 else 'better' if delta>0 else 'worse'
def band(delta,iqr,threshold):
 if abs(delta)<=1e-9:return 'within_band'
 if not iqr:return 'not_estimable'
 return 'better' if delta/iqr>threshold+1e-12 else 'worse' if delta/iqr < -threshold-1e-12 else 'within_band'
pairs=[];patterns=[];front=[]
for t in complete:
 scores={r['model']:r['score'] for r in t['rows']};v=[scores[m] for m in models];q1,_,q3=statistics.quantiles(v,n=4,method='inclusive');iqr=q3-q1;sign=-1 if t['rows'][0]['direction']=='lower' else 1
 for i,j in itertools.combinations(range(4),2):
  delta=(v[j]-v[i])*sign
  pairs.append(dict(benchmark_id=t['id'],family=t['id'][0],metric=t['rows'][0]['metric'],direction=t['rows'][0]['direction'],lag=j-i,older=models[i],newer=models[j],older_score=v[i],newer_score=v[j],direction_adjusted_delta=delta,q1=q1,q3=q3,panel_iqr=iqr,normalized_gap=delta/iqr if iqr else None,raw=raw(delta),**{f'iqr_{a}':band(delta,iqr,a) for a in [.1,.5]}))
 gains=[(v[i+1]-v[i])*sign for i in range(3)]; ss=[0 if abs(x)<=1e-9 else 1 if x>0 else -1 for x in gains]
 cls='strictly_improving' if all(s>0 for s in ss) else 'strictly_declining' if all(s<0 for s in ss) else 'numerically_flat' if all(s==0 for s in ss) else 'nondecreasing_with_ties' if all(s>=0 for s in ss) else 'nonincreasing_with_ties' if all(s<=0 for s in ss) else 'mixed_reversals'
 patterns.append(dict(benchmark_id=t['id'],task=t['title'],family=t['id'][0],direction=t['rows'][0]['direction'],scores=scores,trajectory_class=cls,step_pattern=' '.join('+' if s>0 else '−' if s<0 else '=' for s in ss),adjacent_direction_adjusted_gains=gains))
 best=max(v,key=lambda x:x*sign);ref=t['reference'];delta=(best-ref['score'])*sign
 classes={k:('general_better' if z=='better' else 'specialist_better' if z=='worse' else z) for k,z in [('raw',raw(delta))]+[(f'iqr_{a}',band(delta,iqr,a)) for a in [.1,.5]]}
 comp=dict(methods=['reference-'+t['id']],name=ref['name'],score=ref['score'],direction_adjusted_delta=delta,raw_native_delta=best-ref['score'],gap_in_general_panel_iqr=delta/iqr if iqr else None,classes=classes)
 front.append(dict(benchmark_id=t['id'],task=t['title'],family_code=t['id'][0],metric=t['rows'][0]['metric'],direction=t['rows'][0]['direction'],general_scores=scores,best_general_models=[m for m in models if scores[m]==best],best_general_score=best,q1=q1,q3=q3,general_panel_iqr=iqr,best_available_reference=comp,best_specialist=comp if t['id'] in ['B03','J08'] else None))
sums=[]
for i,j in sorted(itertools.combinations(range(4),2),key=lambda ij:(ij[1]-ij[0],ij[0])):
 for mode in ['raw','iqr_0.1','iqr_0.5']:
  rows=[p for p in pairs if p['older']==models[i] and p['newer']==models[j]];keys=['better','worse','numerical_tie','incomplete'] if mode=='raw' else ['better','worse','within_band','not_estimable'];sums.append(dict(lag=j-i,older=models[i],newer=models[j],analysis=mode,n_tasks=len(rows),counts={k:sum(r[mode]==k for r in rows) for k in keys}))
lag=dict(revision='direct-inference-v1',models=models,n_tasks=10,n_families=7,thresholds=[.1,.5],summaries=sums,task_pairs=pairs,input_sha256=hashlib.sha256((root/'results/primary-summary.json').read_bytes()).hexdigest())
frontier=dict(revision='direct-inference-v1',tasks=front);pat=dict(models=models,tasks=patterns)
for name,obj in [('generation-lags',lag),('specialist-frontier',frontier),('generation-patterns',pat)]:
 dump(web/f'data/{name}.json',obj);dump(root/f'analysis/{name}-v1/summary.json',obj)
writecsv(root/'analysis/generation-lags-v1/task-pairs.csv',pairs);writecsv(root/'analysis/generation-lags-v1/counts.csv',[{**{k:v for k,v in s.items() if k!='counts'},**s['counts']} for s in sums]);writecsv(root/'analysis/specialist-frontier-v1/task-comparisons.csv',front)
methods='''# Direct-inference comparisons\n\nTen complete four-model tasks form the primary cohort; C06 is separately displayed and excluded from these aggregates. Each task counts once. Missing predictions are not zero. Source: results/primary-summary.json; audited comparator predictions: results/reference-validation.json. No old code-generation general-model score is used.\n\nRaw means direction-adjusted native difference with absolute tolerance 1e-9; it is not percentage accuracy or significance. R is that difference divided by the IQR of the same four general-model scores, using inclusive/type-7 interpolation. |R| ≤0.1 or ≤0.5 is within band, including the boundary (1e-12 ratio tolerance). A zero IQR with a nonzero difference is not estimable; no epsilon denominator is invented. These post-hoc bands do not establish equivalence, practical importance, randomness, or a scaling law.\n\nSpecialist-only includes SpikeInterface B03 and archived StarDist J08 among the complete tasks; C06 OASIS is outside this cohort. The broader reference table additionally includes conventional trained estimators, domain models and a mathematical audit. None is certified current global SOTA. All reference predictions were rescored on the retained targets, but input, calibration and fitting access can differ. Best general selects the best of four observed test scores per task; it is a post-hoc envelope, not a single deployable model. The specialist is not added to the four-point IQR.\n\nSix pairs share the same ten tasks and are dependent. Category/filter results often have one task. Public tasks, synthetic diagnostics B03/M04, unequal transport/reasoning/repairs and omitted calibration in D02 limit interpretation. L04 is 64-example in-context inference; other tasks are zero-shot. There are no repeated-generation or biological uncertainty intervals. Do not average incompatible native score differences.\n'''
for name in ['generation-lags','specialist-frontier','generation-patterns']:(root/f'analysis/{name}-v1/methods.md').write_text(methods)
report=methods+'\n## All model pairs\n\n|Lag|Pair|Rule|Better|Worse|Tie/within|Unavailable|\n|---|---|---|---:|---:|---:|---:|\n'
for s in sums:
 c=s['counts'];report+=f"|{s['lag']}|{s['older']} → {s['newer']}|{s['analysis']}|{c['better']}|{c['worse']}|{c.get('numerical_tie',c.get('within_band',0))}|{c.get('incomplete',c.get('not_estimable',0))}|\n"
report+='\n## Best general versus references\n\n|Scope|Rule|General better|Reference better|Tie/within|Unavailable|Not estimable|\n|---|---|---:|---:|---:|---:|---:|\n'
for scope in ['best_specialist','best_available_reference']:
 for mode in ['raw','iqr_0.1','iqr_0.5']:
  cs=[t[scope]['classes'][mode] if t[scope] else 'unavailable' for t in front];report+=f"|{scope}|{mode}|{cs.count('general_better')}|{cs.count('specialist_better')}|{cs.count('within_band')+cs.count('numerical_tie')}|{cs.count('unavailable')}|{cs.count('not_estimable')}|\n"
report+='\n## Interpretation\n\nGPT-6.1 improves numerically over GPT-4.1 on all ten complete tasks, but only three trajectories improve at every step; J08 adds a nondecreasing trajectory with a tie. This suggests endpoint improvement alongside uneven intermediate steps, not universal smooth scaling. Best-general beats the retained reference on B03, K05 and K06; only B03 is an eligible specialist comparison. K05 is a tiny native advantage and the reference inputs differ. These results do not justify replacing laboratory pipelines. The incomplete calcium task and the selected ten-task cohort limit generalization.\n'
(root/'analysis/explorer-analysis.md').write_text(report)
