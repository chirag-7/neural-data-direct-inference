# Neural Data: Direct Inference

Pretrained general models return neuroscience predictions directly. **No model-written programs, model training, fitted estimator, tool calls or code execution occur inside model inference.** Evaluation code loads inputs, sends frozen requests, parses predictions and scores saved outputs.

Models: GPT-4.1 (`gpt-4.1-2025-04-14`), GPT-5 (`gpt-5-2025-08-07`), GPT-5.6 Sol and GPT-6.1 Sol. API availability is checked before paid execution; the Sol primary route is the ChatGPT-authenticated Codex harness. Reasoning effort is medium for models supporting it; GPT-4.1 has no reasoning-effort parameter. Requested model identities and usage are recorded per request; provider-reported identity is unavailable where the harness does not expose it.

## Current state

Thirty candidates inherited from the [separate code-generation study](https://github.com/chirag-7/neural-data-bench) are tracked in [the registry](registry/tasks.json). None of that study's generated-model scores is a direct-inference result. Three tasks (K01, K06 and I10) now have complete primary panels across all four models, with both Sol models rerun through the Codex harness. M01 remains incomplete. Four tasks have sealed requests for their entire retained test sets: K01 morphology (457 cells), K06 PV/SST (71 cells), I10 MRI quality (265 scans), and M01 mouse choice (1,842 cases).

These first four explicitly retain their earlier **custom data protocols**, as a fallback authorized by the user when official matching is impractical. They do not claim to restore official benchmarks or establish a current specialist winner. Other entries remain candidates, not completed experiments. Benchmark admission/deferral is based on data, interface and budget feasibility, not favorable performance.

Primary condition: zero-shot, with semantic task/label definitions and no labeled examples. A fixed eight-training-example condition can be prepared separately; pretrained weights remain fixed. Conditions are never pooled. Test cases within each request are processed as a batch; batch sizes and row order are frozen and may affect model behavior.

[Methods](docs/methods.md) · [Model availability](results/model-availability.json) · [Frozen request inventory](registry/request-seal.json) · [Task registry](registry/tasks.json)

## Reproduction and privacy

`scripts/prepare.py` builds losslessly serialized numerical prompts from the existing locally cached inputs without reading test labels. Raw source data and prompts containing their feature rows stay ignored; tracked manifests retain input and prompt hashes. `scripts/run_requests.py` sends only sealed requests through a loopback, memory-only credential bridge, with no silent retries. `scripts/score.py` scores saved outputs without calling any model. Source dataset use terms remain upstream.

The user-approved new-study API spending ceiling is $20 total, including historical calls. The original bridge has been stopped and its in-memory credential cleared; a new bridge permits only GPT-4.1 and GPT-5 API requests. No paid request can be sent until the user supplies a dedicated API key in the local password form. Credentials are never persisted, printed, committed or published. Availability does not guarantee generation success; all actual failures remain recorded.

## Execution routing update

GPT-5.6 Sol and GPT-6.1 Sol now use the Codex harness with ChatGPT authentication. GPT-4.1 and GPT-5 use the API. Sol API prediction results have been removed from the current study tree. Both Sol models are harness-only; usage-only receipts remain for spending accounting. See [routing and comparison limitations](docs/execution-routing.md) and [primary results](results/primary-report.md) and [harness results](results/codex-harness/summary.json).
