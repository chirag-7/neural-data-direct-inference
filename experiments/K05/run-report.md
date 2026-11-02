# K05: execution report

**Cellular fraction estimation** · Zero-shot · 24 held-out bulk samples, grouped by donor/block

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
| gpt-4.1-2025-04-14 | openai_api | none | 24/24 | 0.07923892098401052 |
| gpt-5-2025-08-07 | openai_api | medium | 24/24 | 0.056901052834444556 |
| gpt-5.6-sol | codex_harness_chatgpt | medium | 24/24 | 0.07276827715795482 |
| gpt-6.1-sol | codex_harness_chatgpt | medium | 24/24 | 0.06978553559228849 |

## Interpretation limits

- Zero-shot: no paired cellular-fraction calibration or single-cell reference atlas is supplied.

Specialist training/calibration is unequal; displayed references are not certified current SOTA. No statistical superiority claim is made.

[Input manifest](input-manifest.json) · [Overall findings](../../analysis/README.md) · [Machine-readable primary results](../../results/primary-summary.json) · [Reference rescoring](../../results/reference-validation.json)
