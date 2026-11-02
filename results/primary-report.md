# Primary direct-inference results

Transport and model generation are confounded. Primary Sol predictions use Codex; older models use API.

Only complete retained test panels receive scores. GPT-5.6 Sol and GPT-6.1 Sol API prediction results have been removed; only their Codex harness predictions are used.

| Task | Requested model | Execution | Predictions / expected | Native metric | Direction | Score |
|---|---|---|---|---|---|---|
| I10 | gpt-4.1-2025-04-14 | openai_api | 265 / 265 | balanced_accuracy | higher is better | 0.5150877192982456 |
| I10 | gpt-5-2025-08-07 | openai_api | 265 / 265 | balanced_accuracy | higher is better | 0.6235087719298246 |
| I10 | gpt-5.6-sol | codex_harness_chatgpt | 265 / 265 | balanced_accuracy | higher is better | 0.6308771929824561 |
| I10 | gpt-6.1-sol | codex_harness_chatgpt | 265 / 265 | balanced_accuracy | higher is better | 0.6110526315789474 |
| K01 | gpt-4.1-2025-04-14 | openai_api | 457 / 457 | macro_f1 | higher is better | 0.548860348737196 |
| K01 | gpt-5-2025-08-07 | openai_api | 457 / 457 | macro_f1 | higher is better | 0.7753325621746674 |
| K01 | gpt-5.6-sol | codex_harness_chatgpt | 457 / 457 | macro_f1 | higher is better | 0.7492339741566432 |
| K01 | gpt-6.1-sol | codex_harness_chatgpt | 457 / 457 | macro_f1 | higher is better | 0.8048145991069695 |
| K06 | gpt-4.1-2025-04-14 | openai_api | 71 / 71 | class_balanced_mouse_accuracy | higher is better | 0.8006944444444444 |
| K06 | gpt-5-2025-08-07 | openai_api | 71 / 71 | class_balanced_mouse_accuracy | higher is better | 0.837202380952381 |
| K06 | gpt-5.6-sol | codex_harness_chatgpt | 71 / 71 | class_balanced_mouse_accuracy | higher is better | 0.8423611111111111 |
| K06 | gpt-6.1-sol | codex_harness_chatgpt | 71 / 71 | class_balanced_mouse_accuracy | higher is better | 0.8705357142857143 |
| M01 | gpt-4.1-2025-04-14 | openai_api | 128 / 1842 | mouse_equal_binary_log_loss | lower is better | Incomplete |
| M01 | gpt-5-2025-08-07 | openai_api | 0 / 1842 | mouse_equal_binary_log_loss | lower is better | Incomplete |
| M01 | gpt-5.6-sol | codex_harness_chatgpt | 0 / 1842 | mouse_equal_binary_log_loss | lower is better | Incomplete |
| M01 | gpt-6.1-sol | codex_harness_chatgpt | 0 / 1842 | mouse_equal_binary_log_loss | lower is better | Incomplete |
