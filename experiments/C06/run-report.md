# C06: execution report

**Calcium → expected spikes** · Zero-shot · 24 recording rows, grouped by neuron and animal

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
| gpt-4.1-2025-04-14 | openai_api | none | 24/24 | 0.1088498533197865 |
| gpt-5-2025-08-07 | openai_api | low | 3/24 | Not complete within this run |
| gpt-5.6-sol | codex_harness_chatgpt | low + medium | 24/24 | 0.45480786297886755 |
| gpt-6.1-sol | codex_harness_chatgpt | low + medium | 23/24 | Not complete within this run |

## Interpretation limits

- Timed-out Sol requests use separately recorded low-effort recovery with the same data and output schema; other Sol requests retain medium reasoning.
- GPT-6.1 Sol is incomplete:one recording timed out at600seconds in both medium and low-effort requests; its23/24 valid rows receive no full-panel score.
- GPT-5 is incomplete: dense output truncation followed by the study API budget limit. Its partial predictions are not assigned a score.

Specialist training/calibration is unequal; displayed references are not certified current SOTA. No statistical superiority claim is made.

[Input manifest](input-manifest.json) · [Overall findings](../../analysis/README.md) · [Machine-readable primary results](../../results/primary-summary.json) · [Reference rescoring](../../results/reference-validation.json)
