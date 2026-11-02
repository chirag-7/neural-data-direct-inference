# K05: direct numeric inference

Predict three orthogonally measured cellular fractions [Astro,EndoMural,Inhib] in human DLPFC from bulk gene expression. Return three probabilities in [0,1]. The fractions refer to all nuclei, including unclassified Other, so they need not sum to one. Inputs are log2(1+CPM), 2000 genes selected using training variance only. No paired labeled examples or single-cell reference atlas are supplied in this zero-shot condition. This differs from calibrated supervised deconvolution.

[Input manifest](input-manifest.json) freezes every retained test case, input hash, output layout and units. No test targets are read during preparation. No training examples, fitted models, or model-written code are used. Primary score: `donor_block_macro_rmse` (lower is better). This is an explicitly custom protocol, not a published official benchmark replication. Zero-shot missing calibration must be considered when interpreting comparisons with trained specialists.
