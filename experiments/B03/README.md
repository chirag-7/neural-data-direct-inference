# B03: direct numeric inference

Recover relative rigid tissue drift in micrometers from one ephys peak-count raster. Input rows are 90 one-second time bins and columns are 132 depth bins of 5 micrometers covering [-20,640] micrometers. Return 90 displacement values, one per time bin. A constant translation is unidentifiable; the scorer subtracts each trajectory mean. Do not output image coordinates, a program, or a registration formula.

[Input manifest](input-manifest.json) freezes every retained test case, input hash, output layout and units. No test targets are read during preparation. No training examples, fitted models, or model-written code are used. Primary score: `recording_mean_motion_rmse_um` (lower is better). This is an explicitly custom protocol, not a published official benchmark replication. Zero-shot missing calibration must be considered when interpreting comparisons with trained specialists.
