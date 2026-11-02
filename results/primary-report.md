# Primary direct-inference results

Transport and model generation are confounded. Primary Sol predictions use Codex; older models use API.

Only complete retained test panels receive scores. GPT-5.6 Sol and GPT-6.1 Sol API prediction results have been removed; only their Codex harness predictions are used.

| Task | Requested model | Execution | Predictions / expected | Condition | Reasoning | Native metric | Direction | Score |
|---|---|---|---|---|---|---|---|---|
| B03 | gpt-4.1-2025-04-14 | openai_api | 4 / 4 | zero_shot | none | recording_mean_motion_rmse_um | lower is better | 15.798265807018467 |
| B03 | gpt-5-2025-08-07 | openai_api | 4 / 4 | zero_shot | medium | recording_mean_motion_rmse_um | lower is better | 12.770538333366602 |
| B03 | gpt-5.6-sol | codex_harness_chatgpt | 4 / 4 | zero_shot | medium | recording_mean_motion_rmse_um | lower is better | 10.860646357738913 |
| B03 | gpt-6.1-sol | codex_harness_chatgpt | 4 / 4 | zero_shot | medium | recording_mean_motion_rmse_um | lower is better | 2.426070677122055 |
| C06 | gpt-4.1-2025-04-14 | openai_api | 24 / 24 | zero_shot | none | animal_mean_neuron_pearson_smoothed200ms | higher is better | 0.1088498533197865 |
| C06 | gpt-5-2025-08-07 | openai_api | 3 / 24 | zero_shot | low | animal_mean_neuron_pearson_smoothed200ms | higher is better | Incomplete |
| C06 | gpt-5.6-sol | codex_harness_chatgpt | 24 / 24 | zero_shot | low + medium | animal_mean_neuron_pearson_smoothed200ms | higher is better | 0.45480786297886755 |
| C06 | gpt-6.1-sol | codex_harness_chatgpt | 23 / 24 | zero_shot | low + medium | animal_mean_neuron_pearson_smoothed200ms | higher is better | Incomplete |
| D02 | gpt-4.1-2025-04-14 | openai_api | 10 / 10 | zero_shot | none | rmse | lower is better | 11.44394614468848 |
| D02 | gpt-5-2025-08-07 | openai_api | 10 / 10 | zero_shot | low | rmse | lower is better | 5.178963083689003 |
| D02 | gpt-5.6-sol | codex_harness_chatgpt | 10 / 10 | zero_shot | medium | rmse | lower is better | 7.413651131320161 |
| D02 | gpt-6.1-sol | codex_harness_chatgpt | 10 / 10 | zero_shot | medium | rmse | lower is better | 4.031296204035874 |
| I10 | gpt-4.1-2025-04-14 | openai_api | 265 / 265 | zero_shot | none | balanced_accuracy | higher is better | 0.5150877192982456 |
| I10 | gpt-5-2025-08-07 | openai_api | 265 / 265 | zero_shot | medium | balanced_accuracy | higher is better | 0.6235087719298246 |
| I10 | gpt-5.6-sol | codex_harness_chatgpt | 265 / 265 | zero_shot | medium | balanced_accuracy | higher is better | 0.6308771929824561 |
| I10 | gpt-6.1-sol | codex_harness_chatgpt | 265 / 265 | zero_shot | medium | balanced_accuracy | higher is better | 0.6110526315789474 |
| J08 | gpt-4.1-2025-04-14 | openai_api | 2 / 2 | zero_shot | none | equal_image_rater_object_f1_iou_0.5 | higher is better | 0.0 |
| J08 | gpt-5-2025-08-07 | openai_api | 2 / 2 | zero_shot | low | equal_image_rater_object_f1_iou_0.5 | higher is better | 0.0 |
| J08 | gpt-5.6-sol | codex_harness_chatgpt | 2 / 2 | zero_shot | medium | equal_image_rater_object_f1_iou_0.5 | higher is better | 0.05277766387649796 |
| J08 | gpt-6.1-sol | codex_harness_chatgpt | 2 / 2 | zero_shot | medium | equal_image_rater_object_f1_iou_0.5 | higher is better | 0.11458460113209715 |
| K01 | gpt-4.1-2025-04-14 | openai_api | 457 / 457 | zero_shot | none | macro_f1 | higher is better | 0.548860348737196 |
| K01 | gpt-5-2025-08-07 | openai_api | 457 / 457 | zero_shot | medium | macro_f1 | higher is better | 0.7753325621746674 |
| K01 | gpt-5.6-sol | codex_harness_chatgpt | 457 / 457 | zero_shot | medium | macro_f1 | higher is better | 0.7492339741566432 |
| K01 | gpt-6.1-sol | codex_harness_chatgpt | 457 / 457 | zero_shot | medium | macro_f1 | higher is better | 0.8048145991069695 |
| K05 | gpt-4.1-2025-04-14 | openai_api | 24 / 24 | zero_shot | none | donor_block_macro_rmse | lower is better | 0.07923892098401052 |
| K05 | gpt-5-2025-08-07 | openai_api | 24 / 24 | zero_shot | medium | donor_block_macro_rmse | lower is better | 0.056901052834444556 |
| K05 | gpt-5.6-sol | codex_harness_chatgpt | 24 / 24 | zero_shot | medium | donor_block_macro_rmse | lower is better | 0.07276827715795482 |
| K05 | gpt-6.1-sol | codex_harness_chatgpt | 24 / 24 | zero_shot | medium | donor_block_macro_rmse | lower is better | 0.06978553559228849 |
| K06 | gpt-4.1-2025-04-14 | openai_api | 71 / 71 | zero_shot | none | class_balanced_mouse_accuracy | higher is better | 0.8006944444444444 |
| K06 | gpt-5-2025-08-07 | openai_api | 71 / 71 | zero_shot | medium | class_balanced_mouse_accuracy | higher is better | 0.837202380952381 |
| K06 | gpt-5.6-sol | codex_harness_chatgpt | 71 / 71 | zero_shot | medium | class_balanced_mouse_accuracy | higher is better | 0.8423611111111111 |
| K06 | gpt-6.1-sol | codex_harness_chatgpt | 71 / 71 | zero_shot | medium | class_balanced_mouse_accuracy | higher is better | 0.8705357142857143 |
| L04 | gpt-4.1-2025-04-14 | openai_api | 3506 / 3506 | in_context_calibration | none | bits_per_spike_train_mean | higher is better | -30.101197246896238 |
| L04 | gpt-5-2025-08-07 | openai_api | 3506 / 3506 | in_context_calibration | low | bits_per_spike_train_mean | higher is better | -0.3787069088762826 |
| L04 | gpt-5.6-sol | codex_harness_chatgpt | 3506 / 3506 | in_context_calibration | low | bits_per_spike_train_mean | higher is better | 2.6918538723625716 |
| L04 | gpt-6.1-sol | codex_harness_chatgpt | 3506 / 3506 | in_context_calibration | low | bits_per_spike_train_mean | higher is better | 3.01077522859718 |
| M01 | gpt-4.1-2025-04-14 | openai_api | 1842 / 1842 | zero_shot | none | mouse_equal_binary_log_loss | lower is better | 0.6118205661953511 |
| M01 | gpt-5-2025-08-07 | openai_api | 1842 / 1842 | zero_shot | low (recovery) | mouse_equal_binary_log_loss | lower is better | 1.376978037139105 |
| M01 | gpt-5.6-sol | codex_harness_chatgpt | 1842 / 1842 | zero_shot | medium | mouse_equal_binary_log_loss | lower is better | 1.1679082999700556 |
| M01 | gpt-6.1-sol | codex_harness_chatgpt | 1842 / 1842 | zero_shot | medium | mouse_equal_binary_log_loss | lower is better | 0.5043277631808548 |
| M04 | gpt-4.1-2025-04-14 | openai_api | 24 / 24 | zero_shot | none | range_normalized_mae | lower is better | 0.24184119518527195 |
| M04 | gpt-5-2025-08-07 | openai_api | 24 / 24 | zero_shot | medium | range_normalized_mae | lower is better | 0.26775919901178896 |
| M04 | gpt-5.6-sol | codex_harness_chatgpt | 24 / 24 | zero_shot | medium | range_normalized_mae | lower is better | 0.2308041466669649 |
| M04 | gpt-6.1-sol | codex_harness_chatgpt | 24 / 24 | zero_shot | medium | range_normalized_mae | lower is better | 0.19138292777045207 |
