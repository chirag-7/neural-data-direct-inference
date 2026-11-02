# I10: execution report

**MRI scan quality** · Zero-shot · 265 scans

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
| gpt-4.1-2025-04-14 | openai_api | none | 265/265 | 0.5150877192982456 |
| gpt-5-2025-08-07 | openai_api | medium | 265/265 | 0.6235087719298246 |
| gpt-5.6-sol | codex_harness_chatgpt | medium | 265/265 | 0.6308771929824561 |
| gpt-6.1-sol | codex_harness_chatgpt | medium | 265/265 | 0.6110526315789474 |

## Interpretation limits


Specialist training/calibration is unequal; displayed references are not certified current SOTA. No statistical superiority claim is made.

[Input manifest](input-manifest.json) · [Overall findings](../../analysis/README.md) · [Machine-readable primary results](../../results/primary-summary.json) · [Reference rescoring](../../results/reference-validation.json)
