# Neural Data · Direct Inference

General models receive neuroscience inputs and return **actual predictions**. No model-written solver is executed, no external estimator is fitted, and pretrained weights remain fixed. This is separate from the [earlier code-generation study](https://github.com/chirag-7/neural-data-bench).

## Pilot stopping point

**10 benchmarks complete across four models, across 8 broad categories.** An 11th task, calcium-to-spike inference, has incomplete GPT-5 and GPT-6.1 Sol panels. The user reduced scope from30 inherited candidates to approximately 10–15 completed benchmarks; 19 remaining candidates are explicitly deferred rather than padded with partial scores or claims of model inability.

[Results website](https://neural-data-direct-inference.almondkoala21.chatgpt.site) · [Primary scores](results/primary-report.md) · [Descriptive analysis](analysis/README.md) · [Per-task directory](experiments) · [Methods](docs/methods.md) · [Validation](results/validation.json)

Models: GPT-4.1 (`gpt-4.1-2025-04-14`), GPT-5 (`gpt-5-2025-08-07`), GPT-5.6 Sol and GPT-6.1 Sol.

- **Both Sol models are Codex-harness-only**, authenticated through ChatGPT. Harness traces are checked for tool use. Requested identity is recorded separately from provider identity; the CLI does not independently expose a returned snapshot.
- GPT-4.1 and GPT-5 use the restricted Responses API bridge. Sol API prediction results were removed from the current study tree. Usage-only receipts remain for total spending accounting; prior Git snapshots are not rewritten.
- Primary conditions are zero-shot except L04, which provides64 fixed, uniformly spaced training examples in context. No test labels are supplied.
- Truncation and timeout recoveries are explicitly recorded. Reasoning effort, batch sizes and transport differ in some panels; the study does **not** isolate a pure model-generation effect.

## Read the results correctly

Every full score covers every retained test case under its custom protocol. These are **not30 restored official benchmarks**. A valid score may be poor. Missing/incomplete panels have no assigned score. Every website plot aligns direction so better performance is higher; native score tables preserve the original units.

The 11 task-specific reference prediction files were independently rescored on the same retained cases. They include local trained methods, exact-likelihood estimators and archived specialist masks. They are **not certified latest specialist SOTA**, and their training/calibration budgets differ from the general models. [Reference audit](results/reference-validation.json).

The pilot's descriptive endpoint comparison favors 6.1 over 4.1 on 10/10 complete tasks, while only 3/10 improve strictly at every adjacent generation. This is not a scaling law or a statistical/practical superiority claim. [Assumptions and interpretation](analysis/README.md).

## Organization

| Location | Contents |
|---|---|
| `experiments/<ID>/` | Input manifest, specific protocol, recovery notes and execution report |
| `registry/` |30 source candidates, feasibility audit, frozen request digests and routing |
| `results/primary-summary.json` | Canonical final scores and coverage across transports |
| `results/raw/`, `results/attempts/` | GPT-4.1/GPT-5 API observations only |
| `results/codex-harness/` | Sol prediction outputs, event traces and request metadata |
| `results/*-attempt-history/` | Preserved capacity/quota failures and explicitly retried attempts |
| `results/predictions/` | Complete native prediction arrays, without target labels |
| `analysis/` | Descriptive aggregate tables, caveats and interpretation |
| `web/` | Reviewable website assets and aggregate data; no raw input rows |
| `scripts/` | Preparation, routing, strict parsing, native scoring, validation and website data generation |

## Reproduction and limits

Source data and physiological input prompts remain local and ignored. Dataset-specific manifests record source hashes, shapes, rendering, selection, target definitions and upstream links. Reconstructing the cached arrays requires upstream dataset access and the linked acquisition adapters; redistribution terms remain upstream. This repository does not bundle source data or claim one-command inference reproduction without those prerequisites.

With the verified source caches available, the scoring scripts reproduce results from saved prediction outputs without calling a model:

```sh
python3 scripts/score.py
python3 scripts/score_harness.py
python3 scripts/score_extended.py
python3 scripts/score_images.py
python3 scripts/assemble_primary_results.py
python3 scripts/build_site_data.py
python3 scripts/finalize_reports.py
python3 scripts/validate_study.py
```

Use the pinned numerical dependencies in `requirements.txt`. Input preparation never reads test targets. The scorer validates IDs, dimensions, finite values, task bounds and complete coverage; reference rescoring uses the same native target/aggregation contracts. The website is buildless; preview with `python3 -m http.server --directory web`.

The conservative new-study API cost upper bound is approximately **$19.15**, including discarded Sol API calls, below the approved **$20 total cap**. It assumes uncached/cache-write pricing and is not an invoice; actual billing may be lower. Codex subscription usage is separate. Credentials are memory-only, never committed. No further paid inference is planned at this stopping point.

The results website is owner-private. [Deployment identity and asset hashes](docs/site-deployment.json) link the deployed Site snapshot to the reviewed `web/` source. Temporary API access was stopped at the pilot endpoint and its in-memory credential cleared.

## Results explorer analysis

The direct-inference website uses the original study’s explorer layout and chart components, with independently derived direct-inference scores. Ten complete four-model tasks across seven categories enter the macro tables; C06 remains separately visible with partial coverage.

- [All pair/lag and specialist comparison tables](analysis/explorer-analysis.md)
- [Generation lags, native differences and IQR bands](analysis/generation-lags-v1/)
- [Best-general versus measured specialists and all references](analysis/specialist-frontier-v1/)
- [Task classification rationale](docs/task-classification/README.md)

Rebuild with `python scripts/build_explorer_analysis.py` after `scripts/build_site_data.py` has produced the canonical task payload. The latter now calls the explorer analysis builder automatically. No model calls are needed for this analysis. IQR bands are descriptive sensitivities, not statistical equivalence or significance.
