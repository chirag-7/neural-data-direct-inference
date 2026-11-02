# J08: execution report

**Synaptic puncta segmentation** · Zero-shot · 2 images ×5 expert raters

## Steps completed

1. Reused the cached, provenance-tracked source inputs; no old general-model scores or generated programs were imported.
2. Sealed actual input prompts, output schema, data hash and request configuration before dispatch. Test labels were withheld from preparation.
3. Ran direct predictions with the declared routing: Sol through Codex, older models through API. No prediction text was executed.
4. Validated IDs, shapes, finite values and task bounds; rejected tool use in harness traces. Preserved original infrastructure and formatting failures.
5. Scored only complete panels with the retained native scorer. Partial coverage receives no numeric benchmark score.
6. Rescored the archived/local reference predictions on the same retained cases.

## Final model panels

| Model | Execution | Reasoning | Valid records | Native score |
|---|---|---|---|---|
| gpt-4.1-2025-04-14 | openai_api | none | 2/2 | 0.0 |
| gpt-5-2025-08-07 | openai_api | low | 2/2 | 0.0 |
| gpt-5.6-sol | codex_harness_chatgpt | medium | 2/2 | 0.05277766387649796 |
| gpt-6.1-sol | codex_harness_chatgpt | medium | 2/2 | 0.11458460113209715 |

## Interpretation limits

- Only 2 retained fields; five experts are repeated annotations of each field, not ten independent biological samples. Inputs are explicitly quantized8bit; model polygons use a fixed geometry decoder.

Specialist training/calibration is unequal; displayed references are not certified current SOTA. No statistical superiority claim is made.

[Input manifest](input-manifest.json) · [Overall findings](../../analysis/README.md) · [Machine-readable primary results](../../results/primary-summary.json) · [Reference rescoring](../../results/reference-validation.json)
