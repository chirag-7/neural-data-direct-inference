# M04: execution report

**Q-learning parameter recovery** · Zero-shot · 24 simulated agents

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
| gpt-4.1-2025-04-14 | openai_api | none | 24/24 | 0.24184119518527195 |
| gpt-5-2025-08-07 | openai_api | medium | 24/24 | 0.26775919901178896 |
| gpt-5.6-sol | codex_harness_chatgpt | medium | 24/24 | 0.2308041466669649 |
| gpt-6.1-sol | codex_harness_chatgpt | medium | 24/24 | 0.19138292777045207 |

## Interpretation limits

- Fully synthetic diagnostic; this does not establish biological generalization.

Specialist training/calibration is unequal; displayed references are not certified current SOTA. No statistical superiority claim is made.

[Input manifest](input-manifest.json) · [Overall findings](../../analysis/README.md) · [Machine-readable primary results](../../results/primary-summary.json) · [Reference rescoring](../../results/reference-validation.json)
