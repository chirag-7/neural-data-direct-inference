"""Assemble explicitly routed primary panels; never mix prediction transports."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def main():
    routing = json.loads((ROOT/'registry/execution-routing.json').read_text())['primary_routes']
    api = json.loads((ROOT/'results/summary.json').read_text())['summaries']
    harness = json.loads((ROOT/'results/codex-harness/summary.json').read_text())['summaries']
    rows = [r for r in api+harness if r['transport'] == routing[r['model']]]
    rows.sort(key=lambda r: (r['benchmark_id'], list(routing).index(r['model'])))
    result = dict(comparison_caveat='Transport and model generation are confounded. Primary Sol predictions use Codex; older models use API.', summaries=rows)
    (ROOT/'results/primary-summary.json').write_text(json.dumps(result, indent=2)+'\n')
    lines = ['# Primary direct-inference results', '', result['comparison_caveat'], '',
             'Only complete retained test panels receive scores. GPT-5.6 Sol and GPT-6.1 Sol API prediction results have been removed; only their Codex harness predictions are used.', '',
             '| Task | Requested model | Execution | Predictions / expected | Native metric | Direction | Score |',
             '|---|---|---|---|---|---|---|']
    for r in rows:
        lines.append(f"| {r['benchmark_id']} | {r['model']} | {r['transport']} | {r['n_valid_predictions']} / {r['n_expected']} | {r['metric']} | {r['direction']} is better | {r['score'] if r['score'] is not None else 'Incomplete'} |")
    (ROOT/'results/primary-report.md').write_text('\n'.join(lines)+'\n')

if __name__ == '__main__':
    main()
