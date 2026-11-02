# Execution routing amendment — 2026-11-01

At the user’s request, subsequent GPT-5.6 Sol and GPT-6.1 Sol predictions use the Codex CLI harness with ChatGPT authentication. GPT-4.1 and GPT-5 use the Responses API. The approved total new-study API ceiling is $20, including historical calls; the credential bridge must enforce that ceiling before additional paid dispatch.

At the user’s request, Sol API prediction responses, prediction files and attempt files have been removed from the current study tree. Sol scores come only from complete Codex harness panels in `results/codex-harness/`. `results/raw/` and `results/attempts/` retain GPT-4.1 and GPT-5 API observations only. Historical usage receipts remain solely for total spending accounting. Existing Git commits may retain prior snapshots; this change does not rewrite repository history.

Each harness request is a fresh ephemeral session with the frozen user prompt and prediction JSON schema, medium reasoning, read-only sandbox, an empty working directory, and tools prohibited. The empty directory is not a filesystem isolation boundary: correctness also requires the recorded trace to contain no tool invocation. Any observed tool invocation invalidates that batch. Model-written code is never executed. The harness adds its own instructions, so model generation and transport are confounded in comparisons against older API models; this study does not isolate pure model effects.

Requested model identity is recorded separately from provider-reported identity. A requested model name or model-authored claim is not evidence of a returned snapshot. If the CLI does not expose provider identity, that field remains unavailable.

Official CLI documentation: https://developers.openai.com/codex/noninteractive
