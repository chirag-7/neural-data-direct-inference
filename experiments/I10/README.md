# I10: direct inference

Predict expert structural MRI scan quality using only the supplied MRIQC image-quality metrics. Class 0 means include (rater 1 rated doubtful or accept); class 1 means exclude (rater 1 rated -1). You do not receive the MRI images. This is a retained processed-metric diagnostic, not a restored official paper evaluation.

All 265 retained test rows are evaluated. [Input manifest](input-manifest.json) records source hashes and serialization. This reuses the prior custom data contract as an explicitly allowed fallback; it is not a published official benchmark replication. No prior generated program or prediction is used. Primary metric: `balanced_accuracy`. Zero-shot and fixed eight-example direct inference are separate conditions. Examples use deterministic, label-independent training indices.

Requests contain only input rows, task instructions and, in the eight-example condition, the fixed training examples. Test labels are loaded only by the scorer after responses have been saved. No specialist score is imported without compatibility verification.
