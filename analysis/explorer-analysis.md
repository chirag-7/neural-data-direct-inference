# Direct-inference comparisons

Ten complete four-model tasks form the primary cohort; C06 is separately displayed and excluded from these aggregates. Each task counts once. Missing predictions are not zero. Source: results/primary-summary.json; audited comparator predictions: results/reference-validation.json. No old code-generation general-model score is used.

Raw means direction-adjusted native difference with absolute tolerance 1e-9; it is not percentage accuracy or significance. R is that difference divided by the IQR of the same four general-model scores, using inclusive/type-7 interpolation. |R| ≤0.1 or ≤0.5 is within band, including the boundary (1e-12 ratio tolerance). A zero IQR with a nonzero difference is not estimable; no epsilon denominator is invented. These post-hoc bands do not establish equivalence, practical importance, randomness, or a scaling law.

Specialist-only includes SpikeInterface B03 and archived StarDist J08 among the complete tasks; C06 OASIS is outside this cohort. The broader reference table additionally includes conventional trained estimators, domain models and a mathematical audit. None is certified current global SOTA. All reference predictions were rescored on the retained targets, but input, calibration and fitting access can differ. Best general selects the best of four observed test scores per task; it is a post-hoc envelope, not a single deployable model. The specialist is not added to the four-point IQR.

Six pairs share the same ten tasks and are dependent. Category/filter results often have one task. Public tasks, synthetic diagnostics B03/M04, unequal transport/reasoning/repairs and omitted calibration in D02 limit interpretation. L04 is 64-example in-context inference; other tasks are zero-shot. There are no repeated-generation or biological uncertainty intervals. Do not average incompatible native score differences.

## All model pairs

|Lag|Pair|Rule|Better|Worse|Tie/within|Unavailable|
|---|---|---|---:|---:|---:|---:|
|1|gpt-4.1-2025-04-14 → gpt-5-2025-08-07|raw|7|2|1|0|
|1|gpt-4.1-2025-04-14 → gpt-5-2025-08-07|iqr_0.1|7|2|1|0|
|1|gpt-4.1-2025-04-14 → gpt-5-2025-08-07|iqr_0.5|7|2|1|0|
|1|gpt-5-2025-08-07 → gpt-5.6-sol|raw|7|3|0|0|
|1|gpt-5-2025-08-07 → gpt-5.6-sol|iqr_0.1|7|3|0|0|
|1|gpt-5-2025-08-07 → gpt-5.6-sol|iqr_0.5|2|2|6|0|
|1|gpt-5.6-sol → gpt-6.1-sol|raw|9|1|0|0|
|1|gpt-5.6-sol → gpt-6.1-sol|iqr_0.1|8|1|1|0|
|1|gpt-5.6-sol → gpt-6.1-sol|iqr_0.5|7|1|2|0|
|2|gpt-4.1-2025-04-14 → gpt-5.6-sol|raw|9|1|0|0|
|2|gpt-4.1-2025-04-14 → gpt-5.6-sol|iqr_0.1|9|1|0|0|
|2|gpt-4.1-2025-04-14 → gpt-5.6-sol|iqr_0.5|8|1|1|0|
|2|gpt-5-2025-08-07 → gpt-6.1-sol|raw|8|2|0|0|
|2|gpt-5-2025-08-07 → gpt-6.1-sol|iqr_0.1|8|2|0|0|
|2|gpt-5-2025-08-07 → gpt-6.1-sol|iqr_0.5|5|1|4|0|
|3|gpt-4.1-2025-04-14 → gpt-6.1-sol|raw|10|0|0|0|
|3|gpt-4.1-2025-04-14 → gpt-6.1-sol|iqr_0.1|10|0|0|0|
|3|gpt-4.1-2025-04-14 → gpt-6.1-sol|iqr_0.5|9|0|1|0|

## Best general versus references

|Scope|Rule|General better|Reference better|Tie/within|Unavailable|Not estimable|
|---|---|---:|---:|---:|---:|---:|
|best_specialist|raw|1|1|0|8|0|
|best_specialist|iqr_0.1|1|1|0|8|0|
|best_specialist|iqr_0.5|1|1|0|8|0|
|best_available_reference|raw|3|7|0|0|0|
|best_available_reference|iqr_0.1|2|4|4|0|0|
|best_available_reference|iqr_0.5|2|4|4|0|0|

## Interpretation

GPT-6.1 improves numerically over GPT-4.1 on all ten complete tasks, but only three trajectories improve at every step; J08 adds a nondecreasing trajectory with a tie. This suggests endpoint improvement alongside uneven intermediate steps, not universal smooth scaling. Best-general beats the retained reference on B03, K05 and K06; only B03 is an eligible specialist comparison. K05 is a tiny native advantage and the reference inputs differ. These results do not justify replacing laboratory pipelines. The incomplete calcium task and the selected ten-task cohort limit generalization.
