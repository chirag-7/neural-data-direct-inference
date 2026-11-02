# L04: execution report

**Place-cell spike counts** · 64 in-context examples · 3,506 time bins from one neuron

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
| gpt-4.1-2025-04-14 | openai_api | none | 3506/3506 | -30.101197246896238 |
| gpt-5-2025-08-07 | openai_api | low | 3506/3506 | -0.3787069088762826 |
| gpt-5.6-sol | codex_harness_chatgpt | low | 3506/3506 | 2.6918538723625716 |
| gpt-6.1-sol | codex_harness_chatgpt | low | 3506/3506 | 3.01077522859718 |

## Interpretation limits

- Separately labeled in-context condition:64 fixed, uniformly spaced training examples. All reasoning models use low effort. Reference GLM uses all training bins; comparison is not equal-data or equal-training.

Specialist training/calibration is unequal; displayed references are not certified current SOTA. No statistical superiority claim is made.

[Input manifest](input-manifest.json) · [Overall findings](../../analysis/README.md) · [Machine-readable primary results](../../results/primary-summary.json) · [Reference rescoring](../../results/reference-validation.json)
