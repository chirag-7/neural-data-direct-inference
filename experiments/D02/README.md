# D02: direct numeric inference

Predict passive voltage DEFLECTION in mV relative to pre-step rest, for a held-out current step in one mouse neuron. Input is all 500 current values in pA, sampled at 500Hz, centers t=(index+0.5)*0.002 seconds. Return the requested 100 time samples only, in order. There is no cell-specific labeled calibration in this zero-shot condition; membrane parameters are not supplied. Use your prior knowledge, returning actual numeric deflections. This condition tests an underdetermined zero-shot extrapolation; it does not isolate calibrated biophysical prediction.

[Input manifest](input-manifest.json) freezes every retained test case, input hash, output layout and units. No test targets are read during preparation. No training examples, fitted models, or model-written code are used. Primary score: `rmse` (lower is better). This is an explicitly custom protocol, not a published official benchmark replication. Zero-shot missing calibration must be considered when interpreting comparisons with trained specialists.

GPT-5 primary predictions are a complete low-reasoning rerun after medium-output truncation. Valid medium outputs are retained for audit and excluded from the primary panel; no predictions are mixed across effort configurations.
