"""Derive descriptive pilot reports from complete primary panels."""
from pathlib import Path
import json
from collections import defaultdict
from score import ROOT

def main():
 site=json.loads((ROOT/'web/data.json').read_text());tasks=site['tasks'];full=[t for t in tasks if t['complete_all_four']];models=site['models'];counts=dict(better=0,worse=0,numeric_tie=0);strict=[];nondec=[];refwins=[];rows=[]
 for t in full:
  rr=[next(r for r in t['rows'] if r['model']==m) for m in models];u=[r['score']*(-1 if r['direction']=='lower' else 1) for r in rr];delta=u[-1]-u[0];outcome='better' if delta>1e-9 else 'worse' if delta< -1e-9 else 'numeric_tie';counts[outcome]+=1
  isstrict=all(b-a>1e-9 for a,b in zip(u,u[1:]));isnondec=all(b-a>=-1e-9 for a,b in zip(u,u[1:]));ref=t['reference'];best=max(u);beats=bool(ref and best>ref['score']*(-1 if rr[0]['direction']=='lower' else 1)+1e-9)
  if isstrict:strict.append(t['id'])
  if isnondec:nondec.append(t['id'])
  if beats:refwins.append(t['id'])
  rows.append(dict(benchmark_id=t['id'],endpoint_outcome=outcome,strict_stepwise_improvement=isstrict,nondecreasing_allowing_ties=isnondec,best_general_numerically_beats_reference=beats,condition=t['condition'],category=t['category']))
 completion={m:sum(any(r['model']==m and r['complete'] for r in t['rows']) for t in tasks) for m in models}
 result=dict(completion_across_all_admitted_tasks=completion,n_admitted_tasks=len(tasks),n_complete_four_model_benchmarks=len(full),endpoint_6_1_vs_4_1=counts,strict_stepwise=strict,nondecreasing=nondec,best_general_beats_available_reference=refwins,rows=rows,tie_tolerance=1e-9,statistical_significance_tested=False,scaling_law_claim=False,limitations=site['caveats'])
 out=ROOT/'analysis';out.mkdir(exist_ok=True);(out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
 text=f'''# Direct-inference pilot: descriptive findings

{len(full)} benchmarks are complete across four models;{len(tasks)-len(full)} additional benchmark has a partial model panel. These are custom retained protocols, not a comprehensive official neuroscience benchmark suite.

## Quantitative

| Question | Result |
|---|---|
| GPT-6.1 Sol numerically better than GPT-4.1 | {counts['better']}/{len(full)} |
| Numerically worse | {counts['worse']}/{len(full)} |
| Numeric tie (tolerance1e-9) | {counts['numeric_tie']}/{len(full)} |
| Strict4.1→5→5.6→6.1 improvement | {len(strict)}/{len(full)} ({', '.join(strict)}) |
| Nondecreasing, allowing numeric ties | {len(nondec)}/{len(full)} ({', '.join(nondec)}) |
| Best general score numerically beats retained reference | {len(refwins)}/{len(full)} ({', '.join(refwins)}) |

Completion across all11 admitted tasks: {'; '.join(m+':'+str(n)+'/11' for m,n in completion.items())}. Complete-case accuracy comparisons exclude the calcium task with missing outputs; this creates possible survivorship bias.

These are paired descriptive outcome counts, not independent replications, significance tests, practical-equivalence bands or a fitted scaling law. Native metric values are never averaged across tasks. Numeric ties do not imply statistical equivalence, and small differences do not imply practical superiority.

## Qualitative

Compact features, signal rasters and known-equation parameter recovery require different abilities from dense signal reconstruction and instance segmentation. A valid complete prediction can still be inaccurate. D02 omits neuron-specific calibration and is underdetermined in the zero-shot setting. L04 supplies 64 fixed examples in context; it is analyzed as a separate calibration condition. Fully synthetic tasks B03/M04 cannot establish biological generalization.

## Quantitative + qualitative

The newer endpoint improves more consistently than every adjacent generation. The intermediate ordering is mixed on most tasks, so this pilot supports task-dependent endpoint progress rather than a universal smooth generation law. The available task-specific references remain strong, especially for dense reconstruction, segmentation and exact-likelihood inference. B03 is synthetic with only4 recordings; K05's best-general advantage over the reference is small. Neither result establishes a general recommendation to replace specialist lab tools.

Transport and model generation are confounded: Sol uses the Codex harness;4.1/5 use the API. Some GPT-5 panels use low-effort recovery, Sol calcium timeouts use recorded low-effort recovery, and output batch sizes differ after truncation. There is one run per final configuration. There is no clean causal estimate of generation effects, uncertainty over model sampling, representative lab sample or contamination audit.

## References and audit

All 11 displayed task-specific reference prediction files were independently rescored against the same retained targets. They are local/archived references, not verified current-best published SOTA. Specialist training and calibration differ; J08 direct inputs also use an explicit8bit image representation. [Reference audit](../results/reference-validation.json), [primary results](../results/primary-report.md), [execution routing](../docs/execution-routing.md), [full-panel feasibility](../docs/feasibility-audit.md).
'''
 (out/'README.md').write_text(text)
 # Decentralized task reports link frozen contracts, predictions and reference evidence.
 for t in tasks:
  lines=[f"# {t['id']}: execution report",'',f"**{t['title']}** · {t['condition']} · {t['test_units']}",'', '## Steps completed','', '1. Reused the cached, provenance-tracked source inputs; no old general-model scores or generated programs were imported.','2. Sealed actual input prompts, output schema, data hash and request configuration before dispatch. Test labels were withheld from preparation.','3. Ran direct predictions with the declared routing: Sol through Codex, older models through API. No prediction text was executed.','4. Validated IDs, shapes, finite values and task bounds; rejected tool use in harness traces. Preserved original infrastructure and formatting failures.','5. Scored only complete panels with the retained native scorer. Partial coverage receives no numeric benchmark score.','6. Rescored the archived/local reference predictions on the same retained cases.','', '## Final model panels','', '| Model | Execution | Reasoning | Valid records | Native score |','|---|---|---|---|---|']
  for r in t['rows']:lines.append(f"| {r['model']} | {r['transport']} | {r.get('reasoning_effort','medium')} | {r['n_valid_predictions']}/{r['n_expected']} | {r['score'] if r['complete'] else 'Not complete within this run'} |")
  lines+=['','## Interpretation limits','']+['- '+x for x in t['notes']]+['','Specialist training/calibration is unequal; displayed references are not certified current SOTA. No statistical superiority claim is made.','', '[Input manifest](input-manifest.json) · [Overall findings](../../analysis/README.md) · [Machine-readable primary results](../../results/primary-summary.json) · [Reference rescoring](../../results/reference-validation.json)']
  (ROOT/f"experiments/{t['id']}/run-report.md").write_text('\n'.join(lines)+'\n')
 # Retain all30 source leads, but distinguish admitted tasks and deferred scope.
 p=ROOT/'registry/tasks.json';reg=json.loads(p.read_text());measured={t['id']:t for t in tasks};audit={t['id']:t for t in site['audit']}
 for t in reg['tasks']:
  bid=t['benchmark_id']
  if bid in measured:t.update(status='complete_four_model_panel' if measured[bid]['complete_all_four'] else 'partial_model_panel',protocol_status='retained_custom_protocol_fallback',run_report=f'experiments/{bid}/run-report.md',reason='All four complete' if measured[bid]['complete_all_four'] else 'GPT-5 dense outputs truncated with further recovery deferred under the study budget; GPT-6.1 Sol timed out on one recording at600seconds with medium and low effort.')
  elif bid in audit:t.update(status='deferred_from_pilot',reason=audit[bid]['reason'])
 reg['status']=f"Pilot stopped at{len(tasks)} admitted tasks;{len(full)} complete four-model panels; 19 source candidates deferred."
 p.write_text(json.dumps(reg,indent=2)+'\n')
 print(json.dumps(result|{'rows':'see analysis/summary.json','limitations':'see docs'}))

if __name__=='__main__':main()
