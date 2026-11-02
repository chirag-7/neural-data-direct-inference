"""Score harness panels separately from historical API panels."""
import hashlib, json
import numpy as np
from score import ROOT, OLD, parse_response, metric

def main():
    seal = json.loads((ROOT/'registry/request-seal.json').read_text())
    panels, attempts = {}, []
    for path in sorted((ROOT/'results/codex-harness').glob('*.attempt.json')):
        a = json.loads(path.read_text())
        a['output_valid'] = False
        if a['status'] == 'response_saved':
            try:
                p = ROOT/a['prediction_path']
                assert hashlib.sha256(p.read_bytes()).hexdigest() == a['prediction_sha256']
                assert not a['tool_items']
                data = {'status': 'completed', 'output': [{'type': 'message', 'content': [{'type': 'output_text', 'text': p.read_text()}]}]}
                values = parse_response(data, a)
                key = (a['benchmark_id'], a['model'], a['regime'])
                panel = panels.setdefault(key, {})
                if set(panel) & set(values):
                    raise ValueError('Overlapping batches')
                panel.update(values)
                a['output_valid'] = True
            except (ValueError, AssertionError, KeyError, TypeError) as exc:
                a['validation_error'] = str(exc)
        attempts.append(a)
    rows = []
    for task in seal['task_records']:
        bid = task['benchmark_id']
        data = OLD/f'data/cache/{bid}/data.npz'
        assert hashlib.sha256(data.read_bytes()).hexdigest() == task['source_data_sha256']
        with np.load(data, allow_pickle=False) as z:
            y = z['test_y']
            groups = z['test_groups'] if 'test_groups' in z.files else np.arange(len(y))
        for model in ('gpt-5.6-sol', 'gpt-6.1-sol'):
            panel = panels.get((bid, model, task['regime']), {})
            ids = sorted(panel)
            complete = ids == list(range(len(y)))
            rows.append(dict(benchmark_id=bid, model=model, transport='codex_harness_chatgpt',
                n_expected=len(y), n_valid_predictions=len(ids), complete=complete,
                metric=task['metric'], direction='lower' if bid=='M01' else 'higher',
                score=metric(bid,np.array([panel[i] for i in ids]),y,groups) if complete else None))
    result = dict(transport='codex_harness_chatgpt', summaries=rows, attempts=attempts,
                  historical_api_predictions_included=False)
    (ROOT/'results/codex-harness/summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(valid_batches=sum(a['output_valid'] for a in attempts),
                         attempted_batches=len(attempts), complete_panels=sum(r['complete'] for r in rows))))

if __name__ == '__main__':
    main()
