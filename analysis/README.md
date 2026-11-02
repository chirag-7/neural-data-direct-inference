# Direct-inference pilot: descriptive findings

10 benchmarks are complete across four models;1 additional benchmark has a partial model panel. These are custom retained protocols, not a comprehensive official neuroscience benchmark suite.

## Quantitative

| Question | Result |
|---|---|
| GPT-6.1 Sol numerically better than GPT-4.1 | 10/10 |
| Numerically worse | 0/10 |
| Numeric tie (tolerance1e-9) | 0/10 |
| Strict4.1→5→5.6→6.1 improvement | 3/10 (B03, K06, L04) |
| Nondecreasing, allowing numeric ties | 4/10 (B03, J08, K06, L04) |
| Best general score numerically beats retained reference | 3/10 (B03, K05, K06) |

Completion across all11 admitted tasks: gpt-4.1-2025-04-14:11/11; gpt-5-2025-08-07:10/11; gpt-5.6-sol:11/11; gpt-6.1-sol:10/11. Complete-case accuracy comparisons exclude the calcium task with missing outputs; this creates possible survivorship bias.

These are paired descriptive outcome counts, not independent replications, significance tests, practical-equivalence bands or a fitted scaling law. Native metric values are never averaged across tasks. Numeric ties do not imply statistical equivalence, and small differences do not imply practical superiority.

## Qualitative

Compact features, signal rasters and known-equation parameter recovery require different abilities from dense signal reconstruction and instance segmentation. A valid complete prediction can still be inaccurate. D02 omits neuron-specific calibration and is underdetermined in the zero-shot setting. L04 supplies 64 fixed examples in context; it is analyzed as a separate calibration condition. Fully synthetic tasks B03/M04 cannot establish biological generalization.

## Quantitative + qualitative

The newer endpoint improves more consistently than every adjacent generation. The intermediate ordering is mixed on most tasks, so this pilot supports task-dependent endpoint progress rather than a universal smooth generation law. The available task-specific references remain strong, especially for dense reconstruction, segmentation and exact-likelihood inference. B03 is synthetic with only4 recordings; K05's best-general advantage over the reference is small. Neither result establishes a general recommendation to replace specialist lab tools.

Transport and model generation are confounded: Sol uses the Codex harness;4.1/5 use the API. Some GPT-5 panels use low-effort recovery, Sol calcium timeouts use recorded low-effort recovery, and output batch sizes differ after truncation. There is one run per final configuration. There is no clean causal estimate of generation effects, uncertainty over model sampling, representative lab sample or contamination audit.

## References and audit

All 11 displayed task-specific reference prediction files were independently rescored against the same retained targets. They are local/archived references, not verified current-best published SOTA. Specialist training and calibration differ; J08 direct inputs also use an explicit8bit image representation. [Reference audit](../results/reference-validation.json), [primary results](../results/primary-report.md), [execution routing](../docs/execution-routing.md), [full-panel feasibility](../docs/feasibility-audit.md).
