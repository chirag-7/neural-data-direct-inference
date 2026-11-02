# K06: direct inference

Predict independently optotagged mouse interneuron genetic class from extracellular average waveform features. Class 0 is PV; class 1 is SST. The first six features are scalar waveform summaries; the remaining 81 are normalized samples spanning -0.5 to +1.5 ms.

All 71 retained test rows are evaluated. [Input manifest](input-manifest.json) records source hashes and serialization. This reuses the prior custom data contract as an explicitly allowed fallback; it is not a published official benchmark replication. No prior generated program or prediction is used. Primary metric: `class_balanced_mouse_accuracy`. Zero-shot and fixed eight-example direct inference are separate conditions. Examples use deterministic, label-independent training indices.

Requests contain only input rows, task instructions and, in the eight-example condition, the fixed training examples. Test labels are loaded only by the scorer after responses have been saved. No specialist score is imported without compatibility verification.
