# K01: direct inference

Predict independently annotated mouse dendritic morphology from electrophysiological measurements. Class 0 is aspiny; class 1 is spiny. These are morphology labels, not transcriptomic cell types.

All 457 retained test rows are evaluated. [Input manifest](input-manifest.json) records source hashes and serialization. This reuses the prior custom data contract as an explicitly allowed fallback; it is not a published official benchmark replication. No prior generated program or prediction is used. Primary metric: `macro_f1`. Zero-shot and fixed eight-example direct inference are separate conditions. Examples use deterministic, label-independent training indices.

Requests contain only input rows, task instructions and, in the eight-example condition, the fixed training examples. Test labels are loaded only by the scorer after responses have been saved. No specialist score is imported without compatibility verification.
