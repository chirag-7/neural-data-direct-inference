# M01: execution report

**Mouse choice probability** · Zero-shot · 1,842 held-out choices

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
| gpt-4.1-2025-04-14 | openai_api | none | 1842/1842 | 0.6118205661953511 |
| gpt-5-2025-08-07 | openai_api | low (recovery) | 1842/1842 | 1.376978037139105 |
| gpt-5.6-sol | codex_harness_chatgpt | medium | 1842/1842 | 1.1679082999700556 |
| gpt-6.1-sol | codex_harness_chatgpt | medium | 1842/1842 | 0.5043277631808548 |

## Interpretation limits

- GPT-5 uses low reasoning after medium-reasoning truncation. Successful low batches64 and recovery batches16 are combined without overlap; no accuracy feedback selected repairs.

Specialist training/calibration is unequal; displayed references are not certified current SOTA. No statistical superiority claim is made.

[Input manifest](input-manifest.json) · [Overall findings](../../analysis/README.md) · [Machine-readable primary results](../../results/primary-summary.json) · [Reference rescoring](../../results/reference-validation.json)
