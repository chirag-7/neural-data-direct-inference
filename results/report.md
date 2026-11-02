# Historical API direct-inference results

Direct inference; no tools, code generation, external model fitting or weight updates.

These are API observations for GPT-4.1 and GPT-5 only; Sol models are scored separately from harness outputs. Scores appear only for complete retained test sets. These are explicitly custom-protocol fallbacks. Partial requests are not completed benchmarks. No original code-generation result is used.

| Task | Model | Condition | Valid predictions / test cases | Status | Native score |
|---|---|---|---|---|---|
| I10 | gpt-4.1-2025-04-14 | zero_shot | 265 / 265 | complete | 0.5150877192982456 |
| I10 | gpt-5-2025-08-07 | zero_shot | 265 / 265 | complete | 0.6235087719298246 |
| K01 | gpt-4.1-2025-04-14 | zero_shot | 457 / 457 | complete | 0.548860348737196 |
| K01 | gpt-5-2025-08-07 | zero_shot | 457 / 457 | complete | 0.7753325621746674 |
| K06 | gpt-4.1-2025-04-14 | zero_shot | 71 / 71 | complete | 0.8006944444444444 |
| K06 | gpt-5-2025-08-07 | zero_shot | 71 / 71 | complete | 0.837202380952381 |
| M01 | gpt-4.1-2025-04-14 | zero_shot | 1842 / 1842 | complete | 0.6118205661953511 |
| M01 | gpt-5-2025-08-07 | zero_shot | 1842 / 1842 | complete | 1.376978037139105 |

Specialist current-best matching is unresolved for these fallback contracts; no claim of superiority to field SOTA is made.
