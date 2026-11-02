"""Run frozen prediction prompts through Codex; never execute model output."""
from pathlib import Path
import argparse, concurrent.futures, hashlib, json, os, subprocess, time

ROOT = Path(__file__).resolve().parents[1]
MODELS = ['gpt-5.6-sol', 'gpt-6.1-sol']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tasks', nargs='+', required=True)
    ap.add_argument('--models', nargs='+', choices=MODELS, default=MODELS)
    ap.add_argument('--limit', type=int)
    ap.add_argument('--workers', type=int, default=2)
    args = ap.parse_args()
    seal = json.loads((ROOT/'registry/request-seal.json').read_text())
    outdir = ROOT/'results/codex-harness'
    outdir.mkdir(parents=True, exist_ok=True)
    jobs = [(sha, entry) for sha, entry in seal['requests'].items()
            if entry['benchmark_id'] in args.tasks and entry['model'] in args.models
            and entry['regime'] == 'zero_shot'
            and not (outdir/f'{sha}.attempt.json').exists()]
    jobs.sort(key=lambda item: (args.tasks.index(item[1]['benchmark_id']), item[1]['start'], item[1]['model']))
    if args.limit:
        jobs = jobs[:args.limit]

    def run(item):
        digest, entry = item
        obj = json.loads((ROOT/entry['request_path']).read_text())
        assert hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest() == digest
        prompt = (ROOT/entry['prompt_path']).read_text()
        assert hashlib.sha256(prompt.encode()).hexdigest() == entry['prompt_sha256']
        context = ROOT/'work/harness-contexts'/digest
        context.mkdir(parents=True, exist_ok=True)
        schema = context/'schema.json'
        schema.write_text(json.dumps(obj['text']['format']['schema']))
        final = outdir/f'{digest}.predictions.json'
        cmd = ['codex', 'exec', '--ephemeral', '--ignore-user-config',
               '--skip-git-repo-check', '--sandbox', 'read-only', '-C', str(context),
               '--model', entry['model'], '-c', 'model_reasoning_effort=medium',
               '-c', 'forced_login_method=chatgpt', '-c', 'web_search=disabled',
               '--disable', 'shell_tool', '--disable', 'apps', '--disable', 'browser_use',
               '--disable', 'computer_use', '--disable', 'memories',
               '--output-schema', str(schema), '--output-last-message', str(final), '--json', '-']
        record = dict(**entry, request_sha256=digest, transport='codex_harness_chatgpt',
                      requested_model=entry['model'], provider_reported_model=None,
                      reasoning_effort='medium', started_unix=time.time(), status='dispatched',
                      output_token_limit='Harness default; not the API request token ceiling',
                      command=cmd)
        attempt = outdir/f'{digest}.attempt.json'
        attempt.write_text(json.dumps(record, indent=2)+'\n')
        env = os.environ.copy()
        for name in ('OPENAI_API_KEY', 'CODEX_API_KEY'):
            env.pop(name, None)
        try:
            proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                                  cwd=context, env=env, timeout=600)
            log = outdir/f'{digest}.events.jsonl'
            log.write_text(proc.stdout)
            (outdir/f'{digest}.stderr.txt').write_text(proc.stderr)
            events = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
            tool_items = [e for e in events if e.get('item', {}).get('type') not in (None, 'agent_message', 'reasoning')]
            completed = any(e.get('type') == 'turn.completed' for e in events)
            record.update(exit_code=proc.returncode, events_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),
                          tool_items=tool_items, status='response_saved' if proc.returncode == 0 and completed and final.exists() and not tool_items else 'harness_failure',
                          usage=next((e.get('usage') for e in reversed(events) if e.get('type') == 'turn.completed'), None))
            if final.exists():
                record.update(prediction_path=str(final.relative_to(ROOT)), prediction_sha256=hashlib.sha256(final.read_bytes()).hexdigest())
        except subprocess.TimeoutExpired:
            record.update(status='timeout', timeout_seconds=600)
        except Exception as exc:
            record.update(status='infrastructure_error', error=str(exc))
        record['elapsed_seconds'] = time.time()-record['started_unix']
        attempt.write_text(json.dumps(record, indent=2)+'\n')
        print(json.dumps({k: record[k] for k in ('benchmark_id', 'model', 'start', 'stop', 'status')}), flush=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(run, jobs))

if __name__ == '__main__':
    main()
