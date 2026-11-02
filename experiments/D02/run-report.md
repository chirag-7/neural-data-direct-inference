# D02: execution report

**Current → voltage** · Zero-shot · 2 held-out sweeps;10 output chunks

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
| gpt-4.1-2025-04-14 | openai_api | none | 10/10 | 11.44394614468848 |
| gpt-5-2025-08-07 | openai_api | low | 10/10 | 5.178963083689003 |
| gpt-5.6-sol | codex_harness_chatgpt | medium | 10/10 | 7.413651131320161 |
| gpt-6.1-sol | codex_harness_chatgpt | medium | 10/10 | 4.031296204035874 |

## Interpretation limits

- Zero-shot input omits cell-specific calibration; membrane parameters cannot be uniquely identified. GPT-5 uses a complete low-reasoning recovery panel.

Specialist training/calibration is unequal; displayed references are not certified current SOTA. No statistical superiority claim is made.

[Input manifest](input-manifest.json) · [Overall findings](../../analysis/README.md) · [Machine-readable primary results](../../results/primary-summary.json) · [Reference rescoring](../../results/reference-validation.json)
