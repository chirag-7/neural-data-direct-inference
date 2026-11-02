# M01: direct inference

Predict the probability that a mouse makes source choice +1 (turn CW), rather than choice -1 (turn CCW), given visual contrasts, experimenter probabilityLeft and the previous five choices and feedbacks. A historical choice of 0 is a nonresponse; feedback is -1/0/+1. Predict each row independently; do not join rows into a hidden sequence. The experimenter block probability is privileged metadata shared by all procedures.

All 1842 retained test rows are evaluated. [Input manifest](input-manifest.json) records source hashes and serialization. This reuses the prior custom data contract as an explicitly allowed fallback; it is not a published official benchmark replication. No prior generated program or prediction is used. Primary metric: `mouse_equal_binary_log_loss`. Zero-shot and fixed eight-example direct inference are separate conditions. Examples use deterministic, label-independent training indices.

Requests contain only input rows, task instructions and, in the eight-example condition, the fixed training examples. Test labels are loaded only by the scorer after responses have been saved. No specialist score is imported without compatibility verification.
